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
    SolverConfig,
    real_harmonic_samples,
    solve_design,
)

from .metrics import to_graph
from .types import QuadratureCandidate

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class GramEpigraphReport:
    degree: int
    delta: float
    minimum_block_eigenvalue: float
    kernel_compatibility_residual: float
    generalized_defect: float
    passed: bool


@dataclass(frozen=True)
class InnerRecord:
    result: DesignResult
    elapsed_seconds: float
    peak_memory_bytes: int
    node_count: int
    edge_count: int
    rate_cap: float


def moving_gram_data(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    degree: int,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Return samples, Gram, full residual, and residual Gram."""

    graph = to_graph(candidate)
    conductance = np.asarray(gamma, dtype=float)
    if conductance.shape != (graph.edge_count,):
        raise ValueError("conductance has the wrong shape")
    samples = real_harmonic_samples(candidate.nodes, int(degree))
    weight = np.diag(candidate.weights)
    residual = (graph.generator(conductance) + degree * (degree + 1) * np.eye(candidate.node_count)) @ samples
    gram = samples.T @ weight @ samples
    residual_gram = residual.T @ weight @ residual
    return samples, gram, residual, residual_gram


def generalized_defect(
    gram: FloatArray,
    residual_gram: FloatArray,
    *,
    rank_tolerance: float = 1e-11,
) -> tuple[float, float]:
    eigenvalues, vectors = np.linalg.eigh(0.5 * (gram + gram.T))
    cutoff = max(rank_tolerance, rank_tolerance * float(np.max(eigenvalues)))
    kept = eigenvalues > cutoff
    if not np.any(kept):
        raise ValueError("sampling Gram has zero retained rank")
    kernel = vectors[:, ~kept]
    kernel_residual = (
        0.0
        if kernel.size == 0
        else float(np.linalg.norm(residual_gram @ kernel, ord=2))
    )
    frame = vectors[:, kept] / np.sqrt(eigenvalues[kept])[None, :]
    reduced = frame.T @ residual_gram @ frame
    largest = float(np.max(np.linalg.eigvalsh(0.5 * (reduced + reduced.T))))
    return math_sqrt_nonnegative(largest), kernel_residual


def math_sqrt_nonnegative(value: float) -> float:
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
    _, gram, _, residual_gram = moving_gram_data(candidate, gamma, degree)
    defect, compatibility = generalized_defect(gram, residual_gram)
    block = moving_gram_block(candidate, gamma, degree, delta)
    minimum = float(np.min(np.linalg.eigvalsh(0.5 * (block + block.T))))
    scale = max(1.0, float(np.linalg.norm(block, ord=2)))
    passed = minimum >= -tolerance * scale and defect <= delta + tolerance * max(1.0, delta)
    return GramEpigraphReport(
        int(degree), float(delta), minimum, compatibility, defect, bool(passed)
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
    tracemalloc.start()
    start = time.perf_counter()
    try:
        result = solve_design(model, request, SolverConfig(solver=solver))
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
    finally:
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
