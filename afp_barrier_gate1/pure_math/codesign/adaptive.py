"""Adjoint-weighted refinement against an enriched discrete reference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .families import locally_adapted_antipodal
from .types import QuadratureCandidate

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class EnrichedResponseReport:
    response_error: float
    adjoint_residual_pairing: float
    identity_residual: float
    indicators: FloatArray
    indicator_sum: float
    passed: bool
    scope: str = "ENRICHED_DISCRETE_REFERENCE_ONLY"


def enriched_response_identity(
    operator: ArrayLike,
    source: ArrayLike,
    response: ArrayLike,
    prolonged_coarse_solution: ArrayLike,
    *,
    tolerance: float = 2e-10,
) -> EnrichedResponseReport:
    """Audit c*(u-Iu_H)=z*(q-A Iu_H) without Galerkin assumptions."""

    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    matrix = np.asarray(operator, dtype=float)
    q = np.asarray(source, dtype=float)
    c = np.asarray(response, dtype=float)
    coarse = np.asarray(prolonged_coarse_solution, dtype=float)
    if (
        matrix.ndim != 2
        or matrix.shape[0] != matrix.shape[1]
        or q.shape != c.shape
        or q.shape != coarse.shape
        or q.shape != (matrix.shape[0],)
        or not all(
            np.all(np.isfinite(value))
            for value in (matrix, q, c, coarse)
        )
    ):
        raise ValueError(
            "enriched identity arrays must be finite with compatible shapes"
        )
    solution = np.linalg.solve(matrix, q)
    adjoint = np.linalg.solve(matrix.T, c)
    residual = q - matrix @ coarse
    error = float(c @ (solution - coarse))
    pairing = float(adjoint @ residual)
    indicators = np.abs(adjoint * residual)
    identity_residual = abs(error - pairing)
    scale = max(1.0, abs(error), abs(pairing))
    return EnrichedResponseReport(
        error,
        pairing,
        identity_residual,
        indicators,
        float(np.sum(indicators)),
        identity_residual <= tolerance * scale
        and abs(error) <= float(np.sum(indicators)) + tolerance * scale,
    )


def deterministic_mark(
    indicators: ArrayLike, *, bulk_fraction: float = 0.5
) -> tuple[int, ...]:
    value = np.asarray(indicators, dtype=float)
    if (
        value.ndim != 1
        or len(value) == 0
        or not np.all(np.isfinite(value))
        or np.min(value) < 0
    ):
        raise ValueError("indicators must be a finite nonnegative vector")
    if not 0 < bulk_fraction <= 1:
        raise ValueError("bulk fraction must lie in (0,1]")
    total = float(np.sum(value))
    if total == 0.0:
        return ()
    order = sorted(range(len(value)), key=lambda i: (-value[i], i))
    target = bulk_fraction * total
    selected: list[int] = []
    running = 0.0
    for index in order:
        selected.append(index)
        running += float(value[index])
        if running >= target:
            break
    return tuple(selected)


@dataclass(frozen=True)
class AdaptiveProposal:
    incumbent: QuadratureCandidate
    proposal: QuadratureCandidate
    marked: tuple[int, ...]
    retained_until_verified: bool = True


def antipodal_response_proposal(
    candidate: QuadratureCandidate,
    indicators: ArrayLike,
    *,
    bulk_fraction: float,
    transferred_mass_fraction: float = 0.2,
) -> AdaptiveProposal:
    """Refine the leading marked antipodal pair and preserve mass/centering.

    Exact quadrature moments beyond degree one and global generator
    feasibility are deliberately rechecked by downstream gates.
    """

    indicator_vector = np.asarray(indicators, dtype=float)
    if indicator_vector.shape != (candidate.node_count,):
        raise ValueError("adaptive indicators need one entry per node")
    marked = deterministic_mark(
        indicator_vector, bulk_fraction=bulk_fraction
    )
    if not marked:
        raise ValueError("zero indicators define no refinement proposal")
    index = marked[0]
    x = candidate.nodes[index]
    tangent = np.asarray([x[1] - x[2], x[2] - x[0], x[0] - x[1]])
    tangent -= float(tangent @ x) * x
    if np.linalg.norm(tangent) < 1e-12:
        axis = np.eye(3)[int(np.argmin(np.abs(x)))]
        tangent = axis - float(axis @ x) * x
    direction = x + 0.35 * tangent / np.linalg.norm(tangent)
    direction /= np.linalg.norm(direction)
    antipode = int(np.argmin(np.linalg.norm(candidate.nodes + x, axis=1)))
    transfer = transferred_mass_fraction * min(
        candidate.weights[index], candidate.weights[antipode]
    )
    proposal = locally_adapted_antipodal(
        candidate, index, direction, float(transfer)
    )
    return AdaptiveProposal(candidate, proposal, marked)
