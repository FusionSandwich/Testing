"""Integrated goal-oriented angular adaptation for the verified 2-D S_N model.

This module couples the structure-preserving components without hiding their
certificates.  A user-supplied ``problem_factory`` rebuilds angularly dependent
sources, boundary data, cross sections, and response kernels on every accepted
quadrature; this avoids silently interpolating physical data with a transfer
that preserves the wrong moments.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .adaptivity import (
    AdaptationResult,
    IndicatorResult,
    adapt_positive_quadrature,
    contributon_smoothness_indicator,
    dual_weighted_indicator,
    graph_heat_bootstrap,
)
from .graph_generator import GraphGenerator, fit_graph_generator
from .quadrature import PositiveQuadrature
from .sn2d import SN2DProblem, SN2DSolution, solve_direct, solve_discrete_adjoint

FloatArray = NDArray[np.float64]
ProblemFactory = Callable[[PositiveQuadrature], SN2DProblem]
ProblemSolver = Callable[[SN2DProblem], SN2DSolution]
FeatureFunction = Callable[[FloatArray], FloatArray]


@dataclass(frozen=True)
class SN2DGoalIndicator:
    """Auditable components of the per-direction angular indicator."""

    dwr: IndicatorResult
    contributon: IndicatorResult
    ray_bootstrap: FloatArray
    absolute_combined: FloatArray
    combined: FloatArray
    graph: GraphGenerator


@dataclass(frozen=True)
class AdaptiveSN2DIteration:
    iteration: int
    node_count: int
    responses: dict[str, float]
    maximum_indicator: float
    relative_response_change: float
    moment_residual: float
    transport_residual: float
    transport_converged: bool
    refined_indices: tuple[int, ...]
    coarsened_indices: tuple[int, ...]
    coarsening_rolled_back: bool


@dataclass(frozen=True)
class AdaptiveSN2DResult:
    quadrature: PositiveQuadrature
    problem: SN2DProblem
    solution: SN2DSolution
    history: tuple[AdaptiveSN2DIteration, ...]
    converged: bool
    reason: str


def _boundary_illumination(problem: SN2DProblem) -> FloatArray:
    """Positive angular illumination proxy used before all ray paths exist."""

    q = problem.quadrature
    ox = q.nodes[:, 0]
    oy = q.nodes[:, 1]
    illumination = np.einsum(
        "gaij,ij->a", problem.source, problem.grid.cell_areas
    )
    for a in range(q.n_node):
        if ox[a] > 0.0:
            illumination[a] += ox[a] * float(
                np.einsum("gj,j->", problem.boundary.left[:, a, :], problem.grid.dy)
            )
        elif ox[a] < 0.0:
            illumination[a] += -ox[a] * float(
                np.einsum("gj,j->", problem.boundary.right[:, a, :], problem.grid.dy)
            )
        if oy[a] > 0.0:
            illumination[a] += oy[a] * float(
                np.einsum("gi,i->", problem.boundary.bottom[:, a, :], problem.grid.dx)
            )
        elif oy[a] < 0.0:
            illumination[a] += -oy[a] * float(
                np.einsum("gi,i->", problem.boundary.top[:, a, :], problem.grid.dx)
            )
    return illumination


def sn2d_goal_indicator(
    problem: SN2DProblem,
    solution: SN2DSolution,
    response_names: Sequence[str] | None = None,
    graph_degree: int = 2,
    k_nearest: int = 8,
    ray_bootstrap_weight: float = 0.05,
    pseudo_time: float = 0.02,
    epsilon_response: float = 1e-12,
) -> SN2DGoalIndicator:
    """Construct DWR, contributon, and ray-bootstrap angular indicators.

    The DWR residual proxy is the fitted graph Laplacian of the spatially
    integrated forward angular flux.  It vanishes for angular constants and is
    weighted by exact discrete adjoints.  The independent contributon
    curvature term targets response-relevant nonsmooth angular structure.  The
    positive graph-heat bootstrap of source/boundary illumination prevents a
    zero indicator when the current grid has not represented a streaming ray.
    """

    names = tuple(problem.response_kernels) if response_names is None else tuple(response_names)
    if not names:
        raise ValueError("at least one response is required for goal-oriented adaptation")
    missing = [name for name in names if name not in problem.response_kernels]
    if missing:
        raise KeyError(f"unknown response names: {missing}")
    if (
        not np.isfinite(ray_bootstrap_weight)
        or ray_bootstrap_weight < 0.0
        or not np.isfinite(epsilon_response)
        or epsilon_response <= 0.0
    ):
        raise ValueError("indicator weights must be finite and nonnegative/positive")
    graph = problem.graph or fit_graph_generator(
        problem.quadrature.nodes,
        problem.quadrature.weights,
        maximum_degree=graph_degree,
        k_nearest=k_nearest,
    )
    area = problem.grid.cell_areas
    forward = np.einsum("gaij,ij->a", np.abs(solution.angular_flux), area)
    adjoint_rows = []
    for name in names:
        adjoint = solve_discrete_adjoint(problem, name).reshape(
            problem.n_group,
            problem.quadrature.n_node,
            problem.grid.nx,
            problem.grid.ny,
        )
        adjoint_rows.append(np.einsum("gaij,ij->a", np.abs(adjoint), area))
    adjoints = np.vstack(adjoint_rows)
    angular_residual = np.abs(graph.generator @ forward)
    residuals = np.broadcast_to(angular_residual, adjoints.shape)
    response_values = np.asarray([solution.responses[name] for name in names])
    dwr = dual_weighted_indicator(
        residuals, adjoints, response_values, epsilon_response=epsilon_response
    )
    contributon = contributon_smoothness_indicator(
        forward, adjoints, graph, epsilon_response=epsilon_response
    )
    illumination = _boundary_illumination(problem)
    bootstrap = graph_heat_bootstrap(illumination, graph, pseudo_time=pseudo_time)
    bootstrap = np.maximum(bootstrap, 0.0)
    maximum = float(np.max(bootstrap, initial=0.0))
    if maximum > 0.0:
        bootstrap = bootstrap / maximum
    # Normalize the two goal terms independently before combination.  Their
    # raw scales differ and must not make one family disappear numerically.
    dwr_scaled = dwr.combined / max(float(np.max(dwr.combined, initial=0.0)), epsilon_response)
    contrib_scaled = contributon.combined / max(
        float(np.max(contributon.combined, initial=0.0)), epsilon_response
    )
    combined = np.maximum(dwr_scaled, contrib_scaled)
    combined = np.maximum(combined, ray_bootstrap_weight * bootstrap)
    absolute = np.maximum(dwr.combined, contributon.combined)
    # The bootstrap is dimensionless.  Scale it by a robust nonzero goal level
    # when available; otherwise retain the explicit bootstrap weight as the
    # only signal in a pre-ray state.
    positive_goal = absolute[absolute > 0.0]
    goal_scale = float(np.median(positive_goal)) if positive_goal.size else 1.0
    absolute = np.maximum(absolute, ray_bootstrap_weight * goal_scale * bootstrap)
    return SN2DGoalIndicator(
        dwr, contributon, bootstrap, absolute, combined, graph
    )


def _response_change(
    previous: dict[str, float] | None,
    current: dict[str, float],
    names: Sequence[str],
    floor: float,
) -> float:
    if previous is None:
        return math.inf
    values = []
    for name in names:
        values.append(abs(current[name] - previous[name]) / (abs(current[name]) + floor))
    return float(max(values, default=0.0))


def run_adaptive_sn2d(
    problem_factory: ProblemFactory,
    initial_quadrature: PositiveQuadrature,
    feature_function: FeatureFunction,
    target_moments: ArrayLike,
    response_names: Sequence[str] | None = None,
    solver: ProblemSolver = solve_direct,
    maximum_iterations: int = 6,
    response_tolerance: float = 1e-3,
    indicator_tolerance: float = 0.1,
    moment_tolerance: float = 1e-8,
    refine_fraction: float = 0.2,
    coarsen_fraction: float = 0.05,
    angular_radius: float = 0.08,
    graph_degree: int = 2,
    k_nearest: int = 8,
    ray_bootstrap_weight: float = 0.05,
) -> AdaptiveSN2DResult:
    """Run a deterministic solve-estimate-refine/coarsen-recertify loop."""

    if int(maximum_iterations) != maximum_iterations or maximum_iterations < 1:
        raise ValueError("maximum_iterations must be a positive integer")
    maximum_iterations = int(maximum_iterations)
    for value, name in (
        (response_tolerance, "response_tolerance"),
        (indicator_tolerance, "indicator_tolerance"),
        (moment_tolerance, "moment_tolerance"),
    ):
        if not np.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
    target = np.asarray(target_moments, dtype=float).reshape(-1)
    if np.any(~np.isfinite(target)):
        raise ValueError("target_moments must be finite")

    quadrature = initial_quadrature
    previous_responses: dict[str, float] | None = None
    history: list[AdaptiveSN2DIteration] = []
    last_problem: SN2DProblem | None = None
    last_solution: SN2DSolution | None = None
    reason = "maximum iterations reached"
    converged = False

    for iteration in range(maximum_iterations):
        problem = problem_factory(quadrature)
        if (
            problem.quadrature.n_node != quadrature.n_node
            or not np.allclose(problem.quadrature.nodes, quadrature.nodes)
            or not np.allclose(problem.quadrature.weights, quadrature.weights)
        ):
            raise ValueError("problem_factory must preserve the supplied quadrature")
        solution = solver(problem)
        names = (
            tuple(problem.response_kernels)
            if response_names is None
            else tuple(response_names)
        )
        indicator = sn2d_goal_indicator(
            problem,
            solution,
            names,
            graph_degree=graph_degree,
            k_nearest=k_nearest,
            ray_bootstrap_weight=ray_bootstrap_weight,
        )
        features = np.asarray(feature_function(quadrature.nodes), dtype=float)
        if features.ndim != 2 or features.shape != (target.size, quadrature.n_node):
            raise ValueError("feature_function must return shape (len(target), node_count)")
        moment_residual = float(
            np.linalg.norm(features @ quadrature.weights - target, ord=np.inf)
        )
        change = _response_change(
            previous_responses, solution.responses, names, max(response_tolerance * 1e-3, 1e-14)
        )
        maximum_indicator = float(np.max(indicator.absolute_combined, initial=0.0))
        accepted = (
            iteration > 0
            and solution.converged
            and change <= response_tolerance
            and maximum_indicator <= indicator_tolerance
            and moment_residual <= moment_tolerance
        )
        if accepted or iteration == maximum_iterations - 1:
            history.append(
                AdaptiveSN2DIteration(
                    iteration=iteration,
                    node_count=quadrature.n_node,
                    responses={name: solution.responses[name] for name in names},
                    maximum_indicator=maximum_indicator,
                    relative_response_change=change,
                    moment_residual=moment_residual,
                    transport_residual=solution.residual_norm,
                    transport_converged=solution.converged,
                    refined_indices=(),
                    coarsened_indices=(),
                    coarsening_rolled_back=False,
                )
            )
            if accepted:
                converged = True
                reason = "response, indicator, moment, and transport gates passed"
            last_problem, last_solution = problem, solution
            break

        adaptation: AdaptationResult = adapt_positive_quadrature(
            quadrature,
            indicator.combined,
            feature_function,
            target,
            refine_fraction=refine_fraction,
            coarsen_fraction=coarsen_fraction,
            angular_radius=angular_radius,
        )
        history.append(
            AdaptiveSN2DIteration(
                iteration=iteration,
                node_count=quadrature.n_node,
                responses={name: solution.responses[name] for name in names},
                maximum_indicator=maximum_indicator,
                relative_response_change=change,
                moment_residual=moment_residual,
                transport_residual=solution.residual_norm,
                transport_converged=solution.converged,
                refined_indices=tuple(int(i) for i in adaptation.refined_indices),
                coarsened_indices=tuple(int(i) for i in adaptation.coarsened_indices),
                coarsening_rolled_back=adaptation.rolled_back_coarsening,
            )
        )
        same_rule = (
            adaptation.quadrature.n_node == quadrature.n_node
            and np.allclose(adaptation.quadrature.nodes, quadrature.nodes)
            and np.allclose(adaptation.quadrature.weights, quadrature.weights)
        )
        if same_rule or not np.isfinite(adaptation.exact_moment_residual):
            reason = "adaptation could not produce a distinct certified positive rule"
            last_problem, last_solution = problem, solution
            break
        previous_responses = dict(solution.responses)
        quadrature = adaptation.quadrature
        last_problem, last_solution = problem, solution

    if last_problem is None or last_solution is None:
        raise RuntimeError("adaptive loop did not execute")
    # If the loop ended immediately after accepting a new rule because of a
    # defensive break, ensure the returned problem actually uses the returned
    # quadrature.  Normal paths already satisfy this.
    if last_problem.quadrature.n_node != quadrature.n_node:
        last_problem = problem_factory(quadrature)
        last_solution = solver(last_problem)
    return AdaptiveSN2DResult(
        quadrature=last_problem.quadrature,
        problem=last_problem,
        solution=last_solution,
        history=tuple(history),
        converged=converged,
        reason=reason,
    )
