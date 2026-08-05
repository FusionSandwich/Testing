"""Exact fixed-candidate inner design and moving-Gram certificates."""

from __future__ import annotations

from dataclasses import dataclass
import time
import tracemalloc
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from pure_math.optimization import (
    DesignModel,
    DesignRequest,
    DesignResult,
    RankPolicy,
    SolverConfig,
    real_harmonic_samples,
    solve_design,
)

from .metrics import apply_generator, to_graph
from .types import QuadratureCandidate

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class GramEpigraphReport:
    degree: int
    delta: float
    minimum_block_eigenvalue: float
    kernel_compatibility_residual: float
    generalized_defect: float
    sampling_rank: int
    sampling_cutoff: float
    smallest_retained_singular: float
    largest_discarded_singular: float
    passed: bool


@dataclass(frozen=True)
class InnerRecord:
    result: DesignResult
    elapsed_seconds: float
    python_tracemalloc_peak_bytes: int
    node_count: int
    edge_count: int
    rate_cap: float


def moving_gram_data(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    degree: int,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Return samples, Gram, full residual, and residual Gram."""

    conductance = np.asarray(gamma, dtype=float)
    if conductance.shape != (candidate.edge_count,):
        raise ValueError("conductance has the wrong shape")
    samples = real_harmonic_samples(candidate.nodes, int(degree))
    weight = np.diag(candidate.weights)
    residual = (
        apply_generator(candidate, conductance, samples)
        + degree * (degree + 1) * samples
    )
    gram = samples.T @ weight @ samples
    residual_gram = residual.T @ weight @ residual
    return samples, gram, residual, residual_gram


def generalized_defect(
    gram: FloatArray,
    z_residual: FloatArray,
    *,
    rank_policy: RankPolicy | None = None,
) -> tuple[float, float, int, float, float, float]:
    """Use the frozen P2A singular-value rank policy on a Gram matrix."""

    symmetric = 0.5 * (gram + gram.T)
    eigenvalues, vectors = np.linalg.eigh(symmetric)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    if float(np.min(eigenvalues)) < -1e-12 * scale:
        raise ValueError("sampling Gram is not positive semidefinite")
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = np.maximum(eigenvalues[order], 0.0)
    vectors = vectors[:, order]
    singular = np.sqrt(eigenvalues)
    policy = rank_policy or RankPolicy()
    rank = policy.classify(singular, gram.shape[0])
    kept_vectors = vectors[:, :rank]
    kept_values = eigenvalues[:rank]
    kernel = vectors[:, rank:]
    kernel_residual = (
        0.0
        if kernel.size == 0
        else float(np.linalg.norm(z_residual @ kernel, ord=2))
    )
    frame = kept_vectors / np.sqrt(kept_values)[None, :]
    reduced_residual = z_residual @ frame
    discarded = 0.0 if rank >= len(singular) else float(singular[rank])
    return (
        float(np.linalg.norm(reduced_residual, ord=2)),
        kernel_residual,
        rank,
        policy.threshold(float(singular[0])),
        float(singular[rank - 1]),
        discarded,
    )

def math_sqrt_nonnegative(value: float) -> float:
    if not np.isfinite(value):
        raise ArithmeticError("generalized residual Gram value is nonfinite")
    if value < -1e-10:
        raise ArithmeticError("generalized residual Gram has a negative eigenvalue")
    return float(np.sqrt(max(0.0, value)))


def moving_gram_block(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    degree: int,
    delta: float,
) -> FloatArray:
    """Raw coefficient-space LMI, valid even on a singular sampling Gram."""

    if delta < 0 or not np.isfinite(delta):
        raise ValueError("delta must be finite and nonnegative")
    _, gram, residual, _ = moving_gram_data(candidate, gamma, degree)
    root_w = np.sqrt(candidate.weights)
    z = root_w[:, None] * residual
    return np.block([
        [delta * gram, z.T],
        [z, delta * np.eye(candidate.node_count)],
    ])


def verify_moving_gram_epigraph(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    degree: int,
    delta: float,
    *,
    tolerance: float = 2e-8,
) -> GramEpigraphReport:
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    _, gram, residual, _ = moving_gram_data(candidate, gamma, degree)
    z_residual = np.sqrt(candidate.weights)[:, None] * residual
    (
        defect,
        compatibility,
        sampling_rank,
        sampling_cutoff,
        smallest_retained,
        largest_discarded,
    ) = generalized_defect(gram, z_residual)
    block = moving_gram_block(candidate, gamma, degree, delta)
    minimum = float(np.min(np.linalg.eigvalsh(0.5 * (block + block.T))))
    scale = max(1.0, float(np.linalg.norm(block, ord=2)))
    passed = (
        minimum >= -tolerance * scale
        and defect <= delta + tolerance * max(1.0, delta)
        and compatibility <= tolerance * max(
            1.0, float(np.linalg.norm(z_residual, ord=2))
        )
    )
    return GramEpigraphReport(
        int(degree),
        float(delta),
        minimum,
        compatibility,
        defect,
        sampling_rank,
        sampling_cutoff,
        smallest_retained,
        largest_discarded,
        bool(passed),
    )


def dense_centered_initializer(candidate: QuadratureCandidate) -> FloatArray:
    """Exact formula 2 w_i w_j on a complete centered S2 quadrature."""

    graph = to_graph(candidate)
    return graph.dense_centered_conductance()


def build_inner_model(
    candidate: QuadratureCandidate,
    degrees: Iterable[int] = (2,),
) -> DesignModel:
    return DesignModel.build(to_graph(candidate), tuple(degrees))


def solve_global_inner(
    candidate: QuadratureCandidate,
    rate_cap: float,
    *,
    degree: int = 2,
    solver: str = "CLARABEL",
) -> InnerRecord:
    """Globally solve P2A on fixed nodes/masses/graph and verify the candidate."""

    model = build_inner_model(candidate, (degree,))
    request = DesignRequest.minimum_defect(float(rate_cap), degree=degree)
    owns_trace = not tracemalloc.is_tracing()
    if owns_trace:
        tracemalloc.start()
    start = time.perf_counter()
    try:
        result = solve_design(model, request, SolverConfig(solver=solver))
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
    finally:
        if owns_trace:
            tracemalloc.stop()
    if (
        not result.feasible_candidate
        or result.verification is None
        or not result.verification.passed
    ):
        failures = [] if result.verification is None else result.verification.failures
        raise RuntimeError(
            f"inner design did not independently verify: status={result.status}, "
            f"failures={failures}"
        )
    return InnerRecord(
        result, float(elapsed), int(peak), candidate.node_count,
        candidate.edge_count, float(rate_cap)
    )
