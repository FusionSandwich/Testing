"""Sampling, geometry, feasibility, and generator metrics with honest labels."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import linprog, minimize

from pure_math.optimization import QuadratureGraph, RankPolicy, real_harmonic_samples

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


def apply_generator(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    values: ArrayLike,
) -> FloatArray:
    """Apply L edgewise in O(N+E) storage without an N-by-N matrix."""

    conductance = np.asarray(gamma, dtype=float)
    field = np.asarray(values, dtype=float)
    vector = field.ndim == 1
    if (
        conductance.shape != (candidate.edge_count,)
        or not np.all(np.isfinite(conductance))
        or field.ndim not in (1, 2)
        or field.shape[0] != candidate.node_count
        or not np.all(np.isfinite(field))
    ):
        raise ValueError("invalid conductance or field for generator action")
    matrix = field[:, None] if vector else field
    output = np.zeros_like(matrix, dtype=float)
    i, j = candidate.edges[:, 0], candidate.edges[:, 1]
    flux = conductance[:, None] * (matrix[j] - matrix[i])
    np.add.at(output, i, flux)
    np.add.at(output, j, -flux)
    output /= candidate.weights[:, None]
    return output[:, 0] if vector else output


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


def _matrix_free_shell(
    candidate: QuadratureCandidate, degree: int
) -> tuple[FloatArray, FloatArray, int, float]:
    samples = real_harmonic_samples(candidate.nodes, int(degree))
    root_w = np.sqrt(candidate.weights)
    weighted = root_w[:, None] * samples
    u, singular, _ = np.linalg.svd(weighted, full_matrices=False)
    policy = RankPolicy()
    rank = policy.classify(singular, samples.shape[1])
    cutoff = policy.threshold(float(singular[0]))
    modes = u[:, :rank] / root_w[:, None]
    return samples, modes, rank, cutoff


def sampling_reports(
    candidate: QuadratureCandidate, degrees: Iterable[int] = (2,)
) -> tuple[SamplingReport, ...]:
    output: list[SamplingReport] = []
    for degree in sorted(set(map(int, degrees))):
        samples = real_harmonic_samples(candidate.nodes, degree)
        singular = np.linalg.svd(
            np.sqrt(candidate.weights)[:, None] * samples,
            compute_uv=False,
        )
        policy = RankPolicy()
        rank = policy.classify(singular, samples.shape[1])
        condition = float(singular[0] / singular[rank - 1])
        output.append(
            SamplingReport(
                degree,
                rank,
                int(samples.shape[1]),
                condition,
                condition**2,
                policy.threshold(float(singular[0])),
                False,
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
    value = np.asarray(gamma, dtype=float)
    if value.shape != (candidate.edge_count,):
        raise ValueError("conductance shape mismatch")
    if not np.all(np.isfinite(value)) or np.min(value) < 0:
        raise ValueError("conductance must be finite and nonnegative")
    i = candidate.edges[:, 0]
    j = candidate.edges[:, 1]
    endpoint_sum = np.zeros(candidate.node_count)
    np.add.at(endpoint_sum, i, value)
    np.add.at(endpoint_sum, j, value)
    rates = endpoint_sum / candidate.weights
    detailed_balance = float(np.max(np.abs(
        candidate.weights[i] * (value / candidate.weights[i])
        - candidate.weights[j] * (value / candidate.weights[j])
    )))
    shell_defects: dict[int, float] = {}
    for degree in sorted(set(map(int, degrees))):
        _, modes, _, _ = _matrix_free_shell(candidate, degree)
        residual = (
            apply_generator(candidate, value, modes)
            + degree * (degree + 1) * modes
        )
        shell_defects[degree] = float(np.linalg.norm(
            np.sqrt(candidate.weights)[:, None] * residual,
            ord=2,
        ))
    return GeneratorReport(
        float(np.linalg.norm(
            apply_generator(candidate, value, np.ones(candidate.node_count)),
            ord=np.inf,
        )),
        float(np.linalg.norm(
            apply_generator(candidate, value, candidate.nodes)
            + 2.0 * candidate.nodes,
            ord=np.inf,
        )),
        detailed_balance,
        float(np.min(value)),
        float(np.max(rates)),
        shell_defects,
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
