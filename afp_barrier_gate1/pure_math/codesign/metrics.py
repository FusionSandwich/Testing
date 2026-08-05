"""Sampling, geometry, feasibility, and generator metrics with honest labels."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import linprog, minimize

from pure_math.optimization import DesignModel, QuadratureGraph

from .types import QuadratureCandidate

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class GeometryReport:
    separation: float
    fill_upper_sampled: float
    mesh_ratio_sampled: float
    edge_radius: float
    minimum_edge_length: float
    maximum_degree: int


@dataclass(frozen=True)
class SamplingReport:
    degree: int
    rank: int
    coefficient_dimension: int
    condition: float
    gram_condition: float
    cutoff: float
    exact_rank_certified: bool


@dataclass(frozen=True)
class FeasibilityReport:
    local_margin_min: float
    local_margins: tuple[float, ...]
    global_margin: float
    global_status: str


@dataclass(frozen=True)
class GeneratorReport:
    h0_residual: float
    h1_residual: float
    reversibility_residual: float
    positivity_margin: float
    rate_max: float
    shell_defects: dict[int, float]


@dataclass(frozen=True)
class CandidateReport:
    family: str
    nodes: int
    edges: int
    geometry: GeometryReport
    sampling: tuple[SamplingReport, ...]
    feasibility: FeasibilityReport
    generator: GeneratorReport | None


def to_graph(candidate: QuadratureCandidate) -> QuadratureGraph:
    return QuadratureGraph.build(
        candidate.nodes,
        candidate.weights,
        [tuple(map(int, edge)) for edge in candidate.edges],
    )


def _geodesic(a: FloatArray, b: FloatArray) -> float:
    return math.acos(float(np.clip(a @ b, -1.0, 1.0)))


def _fibonacci_probes(count: int) -> FloatArray:
    index = np.arange(count, dtype=float)
    z = 1.0 - 2.0 * (index + 0.5) / count
    phi = math.pi * (3.0 - math.sqrt(5.0)) * index
    radius = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    return np.column_stack([radius * np.cos(phi), radius * np.sin(phi), z])


def geometry_report(
    candidate: QuadratureCandidate, *, fill_probe_count: int = 8192
) -> GeometryReport:
    x = candidate.nodes
    pair_angles = [
        _geodesic(x[i], x[j])
        for i in range(len(x))
        for j in range(i + 1, len(x))
    ]
    separation = 0.5 * min(pair_angles)
    probes = _fibonacci_probes(fill_probe_count)
    nearest_cosine = np.max(probes @ x.T, axis=1)
    fill_sampled = float(np.max(np.arccos(np.clip(nearest_cosine, -1.0, 1.0))))
    edge_angles = [_geodesic(x[int(i)], x[int(j)]) for i, j in candidate.edges]
    degree = np.zeros(len(x), dtype=int)
    for i, j in candidate.edges:
        degree[int(i)] += 1
        degree[int(j)] += 1
    return GeometryReport(
        separation,
        fill_sampled,
        fill_sampled / separation,
        max(edge_angles),
        min(edge_angles),
        int(np.max(degree)),
    )


def sampling_reports(
    candidate: QuadratureCandidate, degrees: Iterable[int] = (2,)
) -> tuple[SamplingReport, ...]:
    model = DesignModel.build(to_graph(candidate), tuple(degrees))
    output: list[SamplingReport] = []
    for degree in sorted(model.shells):
        shell = model.shell(degree).shell
        output.append(
            SamplingReport(
                degree,
                shell.rank,
                int(shell.raw_samples.shape[1]),
                shell.retained_condition,
                shell.gram_condition,
                shell.cutoff,
                shell.exact_rank_certified,
            )
        )
    return tuple(output)


def _neighbors(candidate: QuadratureCandidate) -> list[list[int]]:
    output: list[list[int]] = [[] for _ in range(candidate.node_count)]
    for i_raw, j_raw in candidate.edges:
        i, j = int(i_raw), int(j_raw)
        output[i].append(j)
        output[j].append(i)
    return output


def local_barycentric_margins(candidate: QuadratureCandidate) -> tuple[float, ...]:
    """Strict row-cone diagnostic.

    Positive means every declared neighbor can receive at least that
    barycentric probability while the loss-scaled tangent mean is zero.
    Zero is boundary feasibility.  Negative is minus the closest attainable
    tangent-mean norm.  This is local only and never certifies shared global
    conductances.
    """

    x = candidate.nodes
    output: list[float] = []
    for i, adjacent in enumerate(_neighbors(candidate)):
        if not adjacent:
            output.append(float("-inf"))
            continue
        columns: list[FloatArray] = []
        for j in adjacent:
            ell = 1.0 - float(x[i] @ x[j])
            if ell <= 1e-13:
                raise ValueError("coincident-node edge invalidates local margin")
            tangent = x[j] - float(x[i] @ x[j]) * x[i]
            columns.append(tangent / ell)
        z = np.asarray(columns).T
        count = z.shape[1]
        c = np.concatenate([np.zeros(count), [-1.0]])
        aeq = np.zeros((4, count + 1))
        aeq[:3, :count] = z
        aeq[3, :count] = 1.0
        beq = np.asarray([0.0, 0.0, 0.0, 1.0])
        aub = np.zeros((count, count + 1))
        aub[:, :count] = -np.eye(count)
        aub[:, count] = 1.0
        strict = linprog(
            c,
            A_ub=aub,
            b_ub=np.zeros(count),
            A_eq=aeq,
            b_eq=beq,
            bounds=[(0.0, 1.0)] * count + [(0.0, 1.0)],
            method="highs",
        )
        if strict.success:
            output.append(float(strict.x[-1]))
            continue
        closest = minimize(
            lambda p: 0.5 * float(np.linalg.norm(z @ p) ** 2),
            np.full(count, 1.0 / count),
            jac=lambda p: z.T @ (z @ p),
            constraints={"type": "eq", "fun": lambda p: float(np.sum(p) - 1.0)},
            bounds=[(0.0, 1.0)] * count,
            method="SLSQP",
            options={"ftol": 1e-13, "maxiter": 400},
        )
        distance = float(np.linalg.norm(z @ closest.x)) if closest.success else float("inf")
        output.append(-distance)
    return tuple(output)


def global_feasibility_margin(
    candidate: QuadratureCandidate, rate_cap: float
) -> tuple[float, str]:
    """LP candidate for a simultaneous positivity/rate margin.

    The margin is VERIFIED_FLOAT only; exact symmetric fixtures are audited
    separately.  A negative/infinite return is a deterministic rejection.
    """

    if not np.isfinite(rate_cap) or rate_cap <= 0:
        raise ValueError("rate_cap must be finite and positive")
    graph = to_graph(candidate)
    m = graph.edge_count
    c = np.concatenate([np.zeros(m), [-1.0]])
    aeq = np.zeros((graph.h1_matrix.shape[0], m + 1))
    aeq[:, :m] = graph.h1_matrix
    scale = np.asarray(
        [candidate.weights[int(i)] * candidate.weights[int(j)] for i, j in candidate.edges]
    )
    positivity = np.zeros((m, m + 1))
    positivity[:, :m] = -np.eye(m)
    positivity[:, m] = scale
    rate = np.zeros((candidate.node_count, m + 1))
    rate[:, :m] = graph.endpoint_incidence
    rate[:, m] = rate_cap * candidate.weights
    aub = np.vstack([positivity, rate])
    bub = np.concatenate([np.zeros(m), rate_cap * candidate.weights])
    result = linprog(
        c,
        A_ub=aub,
        b_ub=bub,
        A_eq=aeq,
        b_eq=graph.h1_rhs,
        bounds=[(0.0, None)] * m + [(0.0, 1.0)],
        method="highs",
    )
    if result.success:
        return float(result.x[-1]), "VERIFIED_FLOAT_CANDIDATE"
    return float("-inf"), f"INFEASIBLE_OR_UNRESOLVED:{result.status}"


def generator_report(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    degrees: Iterable[int] = (2,),
) -> GeneratorReport:
    graph = to_graph(candidate)
    value = np.asarray(gamma, dtype=float)
    if value.shape != (graph.edge_count,):
        raise ValueError("conductance shape mismatch")
    generator = graph.generator(value)
    wmat = np.diag(candidate.weights)
    shells = tuple(sorted(set(int(d) for d in degrees)))
    model = DesignModel.build(graph, shells)
    return GeneratorReport(
        float(np.linalg.norm(generator @ np.ones(candidate.node_count), ord=np.inf)),
        float(np.linalg.norm(generator @ candidate.nodes + 2.0 * candidate.nodes, ord=np.inf)),
        float(np.linalg.norm(wmat @ generator - generator.T @ wmat, ord=np.inf)),
        float(np.min(value)),
        float(np.max(graph.rates(value))),
        {degree: model.defect(value, degree) for degree in shells},
    )


def full_report(
    candidate: QuadratureCandidate,
    *,
    rate_cap: float,
    degrees: Iterable[int] = (2,),
    fill_probe_count: int = 8192,
) -> CandidateReport:
    local = local_barycentric_margins(candidate)
    global_margin, status = global_feasibility_margin(candidate, rate_cap)
    generator = (
        None
        if candidate.seed_conductance is None
        else generator_report(candidate, candidate.seed_conductance, degrees)
    )
    return CandidateReport(
        candidate.family,
        candidate.node_count,
        candidate.edge_count,
        geometry_report(candidate, fill_probe_count=fill_probe_count),
        sampling_reports(candidate, degrees),
        FeasibilityReport(min(local), local, global_margin, status),
        generator,
    )
