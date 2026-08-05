"""Seven convex design formulations behind one explicit CVXPY interface."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Iterable, Literal, Mapping, Sequence

import cvxpy as cp
import numpy as np
from numpy.typing import ArrayLike, NDArray

from .model import AffineShell, DesignModel, QuadratureGraph

FloatArray = NDArray[np.float64]
ProgramKind = Literal[
    "min_defect",
    "min_rate",
    "frobenius",
    "mode_minimax",
    "scalar_minimax",
    "multi_shell",
    "response",
]


@dataclass(frozen=True)
class ResponseTerm:
    """One fixed affine response ``P T_degree Q - target``."""

    degree: int
    left: FloatArray = field(repr=False)
    right: FloatArray = field(repr=False)
    target: FloatArray = field(repr=False)
    weight: float = 1.0

    @classmethod
    def build(
        cls,
        degree: int,
        left: ArrayLike,
        right: ArrayLike,
        target: ArrayLike,
        *,
        weight: float = 1.0,
    ) -> "ResponseTerm":
        return cls(
            int(degree), np.asarray(left, dtype=float), np.asarray(right, dtype=float),
            np.asarray(target, dtype=float), float(weight),
        )


@dataclass(frozen=True)
class DesignRequest:
    """A frozen specification for one retained convex formulation.

    ``multi_shell`` supports ``metric='frobenius'`` (QP) and
    ``metric='spectral_max'`` (SDP).  ``response`` applies fixed left/right
    response maps and supports Frobenius QP, spectral SDP, column-max SOCP,
    or scalar LP metrics.  Edge-group penalties are convex group norms;
    reweighting or support selection is deliberately outside this object.
    """

    kind: ProgramKind
    degree: int = 2
    rate_cap: float | None = None
    defect_cap: float | None = None
    metric: str = "spectral"
    shell_weights: Mapping[int, float] = field(default_factory=dict)
    modes: FloatArray | None = field(default=None, repr=False)
    scalar_outputs: FloatArray | None = field(default=None, repr=False)
    response_terms: tuple[ResponseTerm, ...] = field(default=(), repr=False)
    edge_groups: tuple[tuple[int, ...], ...] = ()
    group_penalty_weight: float = 0.0

    @classmethod
    def minimum_defect(cls, rate_cap: float, degree: int = 2) -> "DesignRequest":
        return cls("min_defect", degree=degree, rate_cap=float(rate_cap))

    @classmethod
    def minimum_rate(cls, defect_cap: float, degree: int = 2) -> "DesignRequest":
        return cls("min_rate", degree=degree, defect_cap=float(defect_cap))

    @classmethod
    def frobenius_shell(
        cls, rate_cap: float, degree: int = 2, *,
        edge_groups: Sequence[Sequence[int]] = (), group_penalty_weight: float = 0.0,
    ) -> "DesignRequest":
        return cls(
            "frobenius", degree=degree, rate_cap=float(rate_cap), metric="frobenius",
            edge_groups=tuple(tuple(map(int, group)) for group in edge_groups),
            group_penalty_weight=float(group_penalty_weight),
        )

    @classmethod
    def minimax_modes(
        cls, rate_cap: float, modes: ArrayLike, degree: int = 2,
    ) -> "DesignRequest":
        return cls(
            "mode_minimax", degree=degree, rate_cap=float(rate_cap),
            metric="column_max", modes=np.asarray(modes, dtype=float),
        )

    @classmethod
    def minimax_scalar_responses(
        cls, rate_cap: float, modes: ArrayLike, outputs: ArrayLike, degree: int = 2,
    ) -> "DesignRequest":
        return cls(
            "scalar_minimax", degree=degree, rate_cap=float(rate_cap), metric="scalar_max",
            modes=np.asarray(modes, dtype=float),
            scalar_outputs=np.asarray(outputs, dtype=float),
        )

    @classmethod
    def multi_shell(
        cls, rate_cap: float, shell_weights: Mapping[int, float], *,
        metric: Literal["frobenius", "spectral_max"] = "frobenius",
    ) -> "DesignRequest":
        return cls(
            "multi_shell", rate_cap=float(rate_cap), metric=metric,
            shell_weights={int(k): float(v) for k, v in shell_weights.items()},
        )

    @classmethod
    def response_weighted(
        cls,
        rate_cap: float,
        terms: Sequence[ResponseTerm],
        *,
        metric: Literal["frobenius", "spectral_max", "column_max", "scalar_max"] = "frobenius",
    ) -> "DesignRequest":
        return cls(
            "response", rate_cap=float(rate_cap), metric=metric,
            response_terms=tuple(terms),
        )

    def validate(self, model: DesignModel) -> None:
        graph = model.graph
        if self.rate_cap is not None and (not np.isfinite(self.rate_cap) or self.rate_cap <= 0):
            raise ValueError("rate_cap must be finite and positive")
        if self.defect_cap is not None and (not np.isfinite(self.defect_cap) or self.defect_cap <= 0):
            raise ValueError("defect_cap must be finite and positive")
        if self.kind in {"min_defect", "frobenius", "mode_minimax", "scalar_minimax", "multi_shell", "response"} and self.rate_cap is None:
            raise ValueError(f"{self.kind} requires a fixed rate_cap")
        if self.kind == "min_rate" and self.defect_cap is None:
            raise ValueError("min_rate requires a fixed defect_cap")
        if self.kind not in {"multi_shell", "response"}:
            model.shell(self.degree)
        if self.kind == "multi_shell":
            if not self.shell_weights or any(
                not np.isfinite(weight) or weight <= 0
                for weight in self.shell_weights.values()
            ):
                raise ValueError("multi-shell weights must be nonempty and positive")
            for degree in self.shell_weights:
                model.shell(degree)
            if self.metric not in {"frobenius", "spectral_max"}:
                raise ValueError("unsupported multi-shell metric")
        if self.kind in {"mode_minimax", "scalar_minimax"}:
            rank = model.shell(self.degree).shell.rank
            if self.modes is None or self.modes.ndim != 2 or self.modes.shape[0] != rank:
                raise ValueError("modes must have shape (quotient rank, mode count)")
            if not np.all(np.isfinite(self.modes)):
                raise ValueError("modes must be finite")
            norms = np.linalg.norm(self.modes, axis=0)
            if np.min(norms) <= 0 or np.max(np.abs(norms - 1.0)) > 1e-8:
                raise ValueError("every quotient mode must be Euclidean unit normalized")
            if self.kind == "scalar_minimax":
                if self.scalar_outputs is None or self.scalar_outputs.shape != (graph.node_count, self.modes.shape[1]):
                    raise ValueError("scalar outputs must have shape (node count, mode count)")
                if not np.all(np.isfinite(self.scalar_outputs)):
                    raise ValueError("scalar outputs must be finite")
        if self.kind == "response":
            if not self.response_terms:
                raise ValueError("response formulation requires at least one affine response term")
            if self.metric not in {"frobenius", "spectral_max", "column_max", "scalar_max"}:
                raise ValueError("unsupported response metric")
            for term in self.response_terms:
                rank = model.shell(term.degree).shell.rank
                if term.weight <= 0 or not np.isfinite(term.weight):
                    raise ValueError("response weights must be finite and positive")
                if term.left.ndim != 2 or term.left.shape[1] != graph.node_count:
                    raise ValueError("every response left map must have node_count columns")
                if term.right.ndim != 2 or term.right.shape[0] != rank:
                    raise ValueError("every response right map must have quotient-rank rows")
                shape = (term.left.shape[0], term.right.shape[1])
                if term.target.shape != shape:
                    raise ValueError("response target has the wrong shape")
                if not all(np.all(np.isfinite(value)) for value in (term.left, term.right, term.target)):
                    raise ValueError("response maps and targets must be finite")
                if self.metric == "scalar_max" and shape != (1, 1):
                    raise ValueError("scalar-max responses must all be scalar")
        if not np.isfinite(self.group_penalty_weight) or self.group_penalty_weight < 0:
            raise ValueError("group_penalty_weight must be finite and nonnegative")
        if self.group_penalty_weight > 0 and not self.edge_groups:
            raise ValueError("a positive group penalty requires at least one edge group")
        seen: set[int] = set()
        for group in self.edge_groups:
            if not group:
                raise ValueError("edge groups must be nonempty")
            for edge in group:
                if not 0 <= edge < graph.edge_count:
                    raise ValueError("edge-group index out of range")
                if edge in seen:
                    raise ValueError("edge groups must be disjoint")
                seen.add(edge)


@dataclass(frozen=True)
class SolverConfig:
    solver: str = "CLARABEL"
    verbose: bool = False
    options: Mapping[str, Any] = field(default_factory=dict)

    def resolved_options(self) -> dict[str, Any]:
        name = self.solver.upper()
        defaults: dict[str, Any]
        if name == "CLARABEL":
            defaults = {
                "tol_gap_abs": 1e-9,
                "tol_gap_rel": 1e-9,
                "tol_feas": 1e-9,
                "max_iter": 1000,
            }
        elif name == "SCS":
            defaults = {"eps": 1e-8, "max_iters": 250000, "normalize": True}
        elif name == "OSQP":
            defaults = {"eps_abs": 1e-9, "eps_rel": 1e-9, "max_iter": 250000, "polishing": True}
        elif name in {"SCIPY", "HIGHS"}:
            defaults = {}
        else:
            raise ValueError(f"unsupported solver {self.solver!r}")
        defaults.update(dict(self.options))
        return defaults


@dataclass
class DesignResult:
    request: DesignRequest
    status: str
    solver: str
    objective: float | None
    gamma: FloatArray | None
    rate_bound: float | None
    epigraph: float | None
    duals: dict[str, Any]
    metadata: dict[str, Any]
    verification: Any | None = None

    @property
    def feasible_candidate(self) -> bool:
        return self.gamma is not None and self.status in {"optimal", "optimal_inaccurate"}


def _affine_expression(affine: AffineShell, gamma: cp.Variable) -> cp.Expression:
    expression: cp.Expression = cp.Constant(affine.constant)
    for edge in range(affine.edge_terms.shape[0]):
        expression = expression + gamma[edge] * affine.edge_terms[edge]
    return expression


def _spectral_block(expression: cp.Expression, bound: cp.Expression) -> cp.Expression:
    rows, cols = expression.shape
    return cp.bmat(
        [[bound * np.eye(rows), expression], [expression.T, bound * np.eye(cols)]]
    )


def _common_constraints(
    model: DesignModel, gamma: cp.Variable, rate_bound: cp.Expression | float,
) -> tuple[list[cp.Constraint], dict[str, cp.Constraint]]:
    graph = model.graph
    exactness = graph.h1_matrix @ gamma == graph.h1_rhs
    positivity = gamma >= 0
    rate = graph.endpoint_incidence @ gamma <= rate_bound * graph.weights
    return [exactness, positivity, rate], {
        "exactness": exactness,
        "positivity": positivity,
        "rate": rate,
    }


def _group_penalty(request: DesignRequest, gamma: cp.Variable) -> cp.Expression:
    if request.group_penalty_weight == 0 or not request.edge_groups:
        return cp.Constant(0.0)
    return request.group_penalty_weight * sum(
        (cp.norm(gamma[list(group)], 2) for group in request.edge_groups), cp.Constant(0.0)
    )


def _compile_problem(
    model: DesignModel, request: DesignRequest,
) -> tuple[cp.Problem, cp.Variable, dict[str, Any]]:
    request.validate(model)
    graph = model.graph
    gamma = cp.Variable(graph.edge_count, name="gamma")
    handles: dict[str, Any] = {"kind": request.kind, "expressions": {}}

    if request.kind == "min_rate":
        rate_variable = cp.Variable(name="rate_bound")
        constraints, common = _common_constraints(model, gamma, rate_variable)
        affine = model.shell(request.degree)
        residual = _affine_expression(affine, gamma)
        block = _spectral_block(residual, cp.Constant(float(request.defect_cap)))
        psd = block >> 0
        constraints.append(psd)
        problem = cp.Problem(cp.Minimize(rate_variable), constraints)
        handles.update(common)
        handles.update({"rate_variable": rate_variable, "psd": [psd], "residuals": [residual], "affines": [affine]})
        if not problem.is_dcp():
            raise AssertionError("minimum-rate SDP failed CVXPY's DCP audit")
        handles["problem_class"] = "SDP"
        return problem, gamma, handles

    constraints, common = _common_constraints(model, gamma, float(request.rate_cap))
    handles.update(common)

    if request.kind == "min_defect":
        affine = model.shell(request.degree)
        residual = _affine_expression(affine, gamma)
        epigraph = cp.Variable(name="spectral_epigraph")
        psd = _spectral_block(residual, epigraph) >> 0
        constraints.append(psd)
        problem = cp.Problem(cp.Minimize(epigraph), constraints)
        handles.update({"epigraph": epigraph, "psd": [psd], "residuals": [residual], "affines": [affine], "psd_scales": [1.0]})
    elif request.kind == "frobenius":
        affine = model.shell(request.degree)
        residual = _affine_expression(affine, gamma)
        objective = 0.5 * cp.sum_squares(residual) + _group_penalty(request, gamma)
        problem = cp.Problem(cp.Minimize(objective), constraints)
        handles.update({"residuals": [residual], "affines": [affine]})
    elif request.kind == "mode_minimax":
        affine = model.shell(request.degree)
        residual = _affine_expression(affine, gamma)
        epigraph = cp.Variable(name="mode_epigraph")
        soc: list[cp.Constraint] = []
        mode_affines: list[tuple[FloatArray, FloatArray]] = []
        assert request.modes is not None
        for column in range(request.modes.shape[1]):
            mode = request.modes[:, column]
            constraint = cp.SOC(epigraph, residual @ mode)
            constraints.append(constraint)
            soc.append(constraint)
            mode_affines.append((affine.constant @ mode, np.einsum("enr,r->en", affine.edge_terms, mode)))
        problem = cp.Problem(cp.Minimize(epigraph), constraints)
        handles.update({"epigraph": epigraph, "soc": soc, "residuals": [residual], "affines": [affine], "mode_affines": mode_affines})
    elif request.kind == "scalar_minimax":
        affine = model.shell(request.degree)
        residual = _affine_expression(affine, gamma)
        epigraph = cp.Variable(name="scalar_epigraph")
        upper: list[cp.Constraint] = []
        lower: list[cp.Constraint] = []
        scalar_affines: list[tuple[float, FloatArray]] = []
        assert request.modes is not None and request.scalar_outputs is not None
        for column in range(request.modes.shape[1]):
            mode = request.modes[:, column]
            output = request.scalar_outputs[:, column]
            scalar = output @ residual @ mode
            up, low = scalar <= epigraph, -scalar <= epigraph
            constraints.extend([up, low])
            upper.append(up)
            lower.append(low)
            scalar_affines.append((
                float(output @ affine.constant @ mode),
                np.einsum("n,enr,r->e", output, affine.edge_terms, mode),
            ))
        problem = cp.Problem(cp.Minimize(epigraph), constraints)
        handles.update({"epigraph": epigraph, "upper": upper, "lower": lower, "residuals": [residual], "affines": [affine], "scalar_affines": scalar_affines})
    elif request.kind == "multi_shell":
        residuals: list[cp.Expression] = []
        affines: list[AffineShell] = []
        weights: list[float] = []
        for degree, weight in sorted(request.shell_weights.items()):
            affine = model.shell(degree)
            residuals.append(_affine_expression(affine, gamma))
            affines.append(affine)
            weights.append(float(weight))
        if request.metric == "frobenius":
            objective = sum(
                (0.5 * weight * cp.sum_squares(residual) for weight, residual in zip(weights, residuals, strict=True)),
                cp.Constant(0.0),
            )
            problem = cp.Problem(cp.Minimize(objective), constraints)
        else:
            epigraph = cp.Variable(name="multi_shell_epigraph")
            psd = []
            for weight, residual in zip(weights, residuals, strict=True):
                constraint = _spectral_block(weight * residual, epigraph) >> 0
                constraints.append(constraint)
                psd.append(constraint)
            problem = cp.Problem(cp.Minimize(epigraph), constraints)
            handles.update({"epigraph": epigraph, "psd": psd, "psd_scales": weights})
        handles.update({"residuals": residuals, "affines": affines, "shell_objective_weights": weights})
    elif request.kind == "response":
        responses: list[cp.Expression] = []
        response_affines: list[AffineShell] = []
        response_weights: list[float] = []
        for term in request.response_terms:
            affine = model.shell(term.degree)
            base = _affine_expression(affine, gamma)
            response = term.left @ base @ term.right - term.target
            response_affine = AffineShell(
                affine.shell,
                term.left @ affine.constant @ term.right - term.target,
                np.asarray([term.left @ edge_term @ term.right for edge_term in affine.edge_terms]),
            )
            responses.append(response)
            response_affines.append(response_affine)
            response_weights.append(term.weight)
        handles.update({
            "residuals": responses, "affines": response_affines,
            "response_weights": response_weights,
        })
        if request.metric == "frobenius":
            objective = sum(
                (0.5 * weight * cp.sum_squares(response) for weight, response in zip(response_weights, responses, strict=True)),
                cp.Constant(0.0),
            )
            problem = cp.Problem(cp.Minimize(objective), constraints)
        elif request.metric == "spectral_max":
            epigraph = cp.Variable(name="response_epigraph")
            psd = []
            for weight, response in zip(response_weights, responses, strict=True):
                constraint = _spectral_block(weight * response, epigraph) >> 0
                constraints.append(constraint)
                psd.append(constraint)
            problem = cp.Problem(cp.Minimize(epigraph), constraints)
            handles.update({"epigraph": epigraph, "psd": psd, "psd_scales": response_weights})
        elif request.metric == "column_max":
            epigraph = cp.Variable(name="response_column_epigraph")
            soc = []
            mode_affines = []
            for weight, response, response_affine in zip(response_weights, responses, response_affines, strict=True):
                for column in range(response.shape[1]):
                    constraint = cp.SOC(epigraph, weight * response[:, column])
                    constraints.append(constraint)
                    soc.append(constraint)
                    mode_affines.append((
                        weight * response_affine.constant[:, column],
                        weight * response_affine.edge_terms[:, :, column],
                    ))
            problem = cp.Problem(cp.Minimize(epigraph), constraints)
            handles.update({"epigraph": epigraph, "soc": soc, "mode_affines": mode_affines})
        else:
            epigraph = cp.Variable(name="response_scalar_epigraph")
            upper, lower, scalar_affines = [], [], []
            for weight, response, response_affine in zip(response_weights, responses, response_affines, strict=True):
                scalar = weight * response[0, 0]
                up, low = scalar <= epigraph, -scalar <= epigraph
                constraints.extend([up, low])
                upper.append(up)
                lower.append(low)
                scalar_affines.append((
                    weight * float(response_affine.constant[0, 0]),
                    weight * response_affine.edge_terms[:, 0, 0],
                ))
            problem = cp.Problem(cp.Minimize(epigraph), constraints)
            handles.update({
                "epigraph": epigraph, "upper": upper, "lower": lower,
                "scalar_affines": scalar_affines,
            })
    else:  # pragma: no cover - guarded by the Literal/API constructors
        raise ValueError(f"unsupported design kind {request.kind}")

    if not problem.is_dcp():
        raise AssertionError("retained formulation failed CVXPY's DCP audit")
    handles["problem_class"] = (
        "SDP" if "psd" in handles else
        "SOCP" if "soc" in handles or (
            request.group_penalty_weight > 0 and bool(request.edge_groups)
        ) else
        "LP" if "upper" in handles else "QP"
    )
    return problem, gamma, handles


def _constraint_dual(constraint: cp.Constraint) -> Any:
    value = constraint.dual_value
    if isinstance(value, list):
        return [np.asarray(item, dtype=float) for item in value]
    return None if value is None else np.asarray(value, dtype=float)


def solve_design(
    model: DesignModel,
    request: DesignRequest,
    config: SolverConfig | None = None,
    *,
    verify: bool = True,
) -> DesignResult:
    """Compile, solve, and independently verify one convex design problem."""
    cfg = config or SolverConfig()
    problem, gamma_variable, handles = _compile_problem(model, request)
    solver = cfg.solver.upper()
    installed = {name.upper() for name in cp.installed_solvers()}
    if solver not in installed:
        raise RuntimeError(f"requested solver {solver} is not installed; available={sorted(installed)}")
    try:
        value = problem.solve(
            solver=solver, verbose=cfg.verbose, **cfg.resolved_options()
        )
    except Exception as exc:
        return DesignResult(
            request, "solver_error", solver, None, None, None, None, {},
            {"exception": f"{type(exc).__name__}: {exc}", "problem_class": handles.get("problem_class")},
        )
    status = str(problem.status)
    gamma = None if gamma_variable.value is None else np.asarray(gamma_variable.value, dtype=float).reshape(-1)
    rate_bound = request.rate_cap
    if "rate_variable" in handles and handles["rate_variable"].value is not None:
        rate_bound = float(handles["rate_variable"].value)
    epigraph = None
    if "epigraph" in handles and handles["epigraph"].value is not None:
        epigraph = float(handles["epigraph"].value)
    duals: dict[str, Any] = {}
    for key in ("exactness", "positivity", "rate"):
        duals[key] = _constraint_dual(handles[key])
    for key in ("psd", "soc", "upper", "lower"):
        if key in handles:
            duals[key] = [_constraint_dual(constraint) for constraint in handles[key]]
    metadata = {
        "problem_class": handles.get("problem_class"),
        "solver_name": getattr(problem.solver_stats, "solver_name", solver),
        "solve_time": getattr(problem.solver_stats, "solve_time", None),
        "num_iters": getattr(problem.solver_stats, "num_iters", None),
        "handles": handles,
        "condition_report": model.condition_report(),
    }
    result = DesignResult(
        request, status, solver,
        None if value is None or not np.isfinite(value) else float(value),
        gamma, rate_bound, epigraph, duals, metadata,
    )
    if verify and result.feasible_candidate:
        from .certificates import verify_result

        result.verification = verify_result(model, result)
    return result


@dataclass
class PruneAttempt:
    removed_edge: tuple[int, int]
    candidate_score: float
    objective_threshold: float
    support_before: tuple[int, ...]
    accepted: bool
    reason: str
    status: str
    objective: float | None
    farkas_verified: bool | None = None


@dataclass
class PruneResult:
    model: DesignModel
    result: DesignResult
    kept_original_edges: tuple[int, ...]
    gamma_on_original_graph: FloatArray
    attempts: list[PruneAttempt]


def _request_degrees(request: DesignRequest) -> tuple[int, ...]:
    if request.kind == "multi_shell":
        return tuple(sorted(request.shell_weights))
    if request.kind == "response":
        return tuple(sorted({term.degree for term in request.response_terms}))
    return (request.degree,)


def _restrict_request_edges(
    request: DesignRequest, kept_local: Sequence[int],
) -> DesignRequest:
    if not request.edge_groups:
        return request
    new_index = {old: new for new, old in enumerate(kept_local)}
    groups = tuple(
        restricted
        for group in request.edge_groups
        if (restricted := tuple(new_index[edge] for edge in group if edge in new_index))
    )
    # A positive penalty may lose every group only when every grouped edge
    # was deleted.  The remaining penalty is then identically zero.
    weight = request.group_penalty_weight if groups else 0.0
    return replace(request, edge_groups=groups, group_penalty_weight=weight)


def prune_and_reoptimize(
    model: DesignModel,
    request: DesignRequest,
    config: SolverConfig | None = None,
    *,
    objective_relative_allowance: float = 0.0,
    objective_absolute_allowance: float = 1e-7,
    minimum_candidate_gamma: float = 0.0,
) -> PruneResult:
    """Deterministically remove weak edges, then solve the exact same program.

    This is a nonconvex outer support heuristic.  Every inner problem is the
    original convex formulation on the reduced permitted graph; no claim is
    made that the final support has minimum cardinality.
    """
    if objective_relative_allowance < 0 or objective_absolute_allowance < 0:
        raise ValueError("objective allowances must be nonnegative")
    cfg = config or SolverConfig()
    current_model = model
    current_request = request
    current_result = solve_design(current_model, current_request, cfg)
    if not current_result.feasible_candidate or current_result.verification is None or not current_result.verification.passed:
        raise RuntimeError("initial convex design lacks a verified feasible certificate")
    original_indices = list(range(model.graph.edge_count))
    attempts: list[PruneAttempt] = []
    baseline = float(current_result.objective)

    while True:
        assert current_result.gamma is not None
        ordered = sorted(
            range(current_model.graph.edge_count),
            key=lambda edge: (
                float(current_result.gamma[edge]),
                tuple(map(int, current_model.graph.edges[edge])),
            ),
        )
        progress = False
        for local_edge in ordered:
            if current_result.gamma[local_edge] < minimum_candidate_gamma:
                continue
            if current_model.graph.edge_count <= 1:
                break
            kept_local = [edge for edge in range(current_model.graph.edge_count) if edge != local_edge]
            removed = tuple(map(int, current_model.graph.edges[local_edge]))
            trial_graph = current_model.graph.restrict_edges(kept_local)
            # Nodes and weights do not change when support is pruned, so the
            # certified sampling quotient must not be recomputed.  Reusing
            # the current ShellData preserves exact certificates, declared
            # rank policies, custom sample bases, and the precise quotient
            # frame; only the edge-affine terms are restricted.
            trial_shells = {
                degree: AffineShell(
                    affine.shell,
                    affine.constant.copy(),
                    affine.edge_terms[np.asarray(kept_local, dtype=int)].copy(),
                )
                for degree, affine in current_model.shells.items()
            }
            trial_model = DesignModel(trial_graph, trial_shells)
            trial_request = _restrict_request_edges(current_request, kept_local)
            trial = solve_design(trial_model, trial_request, cfg)
            verified = bool(trial.verification is not None and trial.verification.passed)
            threshold = baseline * (1.0 + objective_relative_allowance) + objective_absolute_allowance
            accepted = verified and trial.objective is not None and trial.objective <= threshold
            farkas_verified: bool | None = None
            reason = "verified objective-preserving reoptimization" if accepted else "unverified or objective allowance exceeded"
            if trial.status in {"infeasible", "infeasible_inaccurate"}:
                from .certificates import find_farkas_certificate, verify_farkas_certificate

                cert = find_farkas_certificate(trial_model, rate_cap=trial_request.rate_cap)
                if cert is not None:
                    report = verify_farkas_certificate(trial_model, cert, rate_cap=trial_request.rate_cap)
                    farkas_verified = report.passed
                    reason = "verified Farkas-infeasible reduced support" if report.passed else "solver infeasible without verified ray"
            attempts.append(PruneAttempt(
                removed,
                float(current_result.gamma[local_edge]),
                float(threshold),
                tuple(original_indices),
                accepted,
                reason,
                trial.status,
                trial.objective,
                farkas_verified,
            ))
            if accepted:
                original_indices.pop(local_edge)
                current_model, current_request, current_result = trial_model, trial_request, trial
                progress = True
                break
        if not progress:
            break

    # One final solve is mandatory even when the last attempted removal failed.
    final_result = solve_design(current_model, current_request, cfg)
    if not final_result.feasible_candidate or final_result.verification is None or not final_result.verification.passed:
        raise RuntimeError("final exact reoptimization did not verify")
    full_gamma = np.zeros(model.graph.edge_count, dtype=float)
    assert final_result.gamma is not None
    full_gamma[np.asarray(original_indices, dtype=int)] = final_result.gamma
    return PruneResult(current_model, final_result, tuple(original_indices), full_gamma, attempts)


def classify_request_cone(model: DesignModel, request: DesignRequest) -> str:
    """Return the canonical retained cone class without solving."""
    problem, _, handles = _compile_problem(model, request)
    if not problem.is_dcp():  # defensive; _compile_problem already checks
        raise AssertionError("non-DCP formulation")
    return str(handles["problem_class"])
