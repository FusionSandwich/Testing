"""Protected-stratum and equality-restoration audits.

These routines are deliberately diagnostic unless their inputs carry exact or
outward-rounded certificates.  The mathematical convergence theorem in the
P2C document assumes a uniformly surjective reduced restoration Jacobian; a
small floating singular value is evidence against that hypothesis, never a
proof of it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .inner import moving_gram_data
from .metrics import geometry_report, generator_report, to_graph
from .types import Certification, CertifiedValue, QuadratureCandidate

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class RestorationRankReport:
    rows: int
    columns: int
    numerical_rank: int
    smallest_retained_singular_value: float
    residual_norm: float
    certification: Certification

    @property
    def surjective_candidate(self) -> bool:
        return self.numerical_rank == self.rows


@dataclass(frozen=True)
class ProtectedAudit:
    minimum_weight: float
    half_separation: float
    minimum_edge_length: float
    minimum_sampling_eigenvalue: float
    h1_residual: float
    positivity_margin: float
    rate_maximum: float
    trace_identity_residual: float
    passed: bool
    certification: Certification


def h1_trace_identity(
    candidate: QuadratureCandidate, gamma: ArrayLike
) -> CertifiedValue:
    """Audit sum_e gamma_e |x_i-x_j|^2 = d-1 on normalized S2."""

    value = np.asarray(gamma, dtype=float)
    if value.shape != (candidate.edge_count,):
        raise ValueError("conductance shape mismatch")
    chord_sq = np.asarray([
        float(np.linalg.norm(candidate.nodes[int(i)] - candidate.nodes[int(j)]) ** 2)
        for i, j in candidate.edges
    ])
    lhs = float(value @ chord_sq)
    residual = abs(lhs - 2.0)
    return CertifiedValue(
        residual,
        Certification.VERIFIED_FLOAT,
        note="trace consequence of exact H1; exact fixtures are checked symbolically",
    )


def audit_protected_stratum(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    *,
    degree: int = 2,
    minimum_weight: float = 0.0,
    minimum_separation: float = 0.0,
    minimum_sampling_eigenvalue: float = 0.0,
    minimum_conductance: float = 0.0,
    rate_cap: float = float("inf"),
    tolerance: float = 2e-8,
) -> ProtectedAudit:
    value = np.asarray(gamma, dtype=float)
    if value.shape != (candidate.edge_count,):
        raise ValueError("conductance shape mismatch")
    geometry = geometry_report(candidate, fill_probe_count=1024)
    report = generator_report(candidate, value, degrees=(degree,))
    _, gram, _, _ = moving_gram_data(candidate, value, degree)
    gram_min = float(np.min(np.linalg.eigvalsh(0.5 * (gram + gram.T))))
    trace_residual = h1_trace_identity(candidate, value).value
    scale = max(1.0, rate_cap if np.isfinite(rate_cap) else 1.0)
    passed = bool(
        np.min(candidate.weights) >= minimum_weight - tolerance
        and geometry.separation >= minimum_separation - tolerance
        and gram_min >= minimum_sampling_eigenvalue - tolerance
        and report.h1_residual <= tolerance
        and report.positivity_margin >= minimum_conductance - tolerance
        and report.rate_max <= rate_cap + tolerance * scale
        and trace_residual <= 10.0 * tolerance
    )
    return ProtectedAudit(
        float(np.min(candidate.weights)),
        geometry.separation,
        geometry.minimum_edge_length,
        gram_min,
        report.h1_residual,
        report.positivity_margin,
        report.rate_max,
        trace_residual,
        passed,
        Certification.VERIFIED_FLOAT if passed else Certification.REJECTED,
    )


def numerical_jacobian(
    residual: Callable[[FloatArray], ArrayLike],
    point: ArrayLike,
    *,
    relative_step: float = 2e-7,
) -> FloatArray:
    x = np.asarray(point, dtype=float)
    base = np.asarray(residual(x), dtype=float)
    if x.ndim != 1 or base.ndim != 1:
        raise ValueError("point and residual must be vectors")
    output = np.empty((len(base), len(x)))
    for column in range(len(x)):
        step = relative_step * max(1.0, abs(float(x[column])))
        plus, minus = x.copy(), x.copy()
        plus[column] += step
        minus[column] -= step
        output[:, column] = (
            np.asarray(residual(plus), dtype=float)
            - np.asarray(residual(minus), dtype=float)
        ) / (2.0 * step)
    return output


def minimum_norm_restoration_step(
    jacobian: ArrayLike,
    residual: ArrayLike,
    *,
    singular_floor: float = 1e-10,
) -> tuple[FloatArray, RestorationRankReport]:
    """Solve J delta = -r only when the reduced Jacobian is onto numerically."""

    matrix = np.asarray(jacobian, dtype=float)
    rhs = np.asarray(residual, dtype=float)
    if matrix.ndim != 2 or rhs.shape != (matrix.shape[0],):
        raise ValueError("restoration matrix/residual shape mismatch")
    u, singular, vt = np.linalg.svd(matrix, full_matrices=False)
    scale = max(1.0, float(singular[0]) if singular.size else 1.0)
    kept = singular > singular_floor * scale
    rank = int(np.count_nonzero(kept))
    smallest = float(np.min(singular[kept])) if rank else 0.0
    if rank < matrix.shape[0]:
        report = RestorationRankReport(
            matrix.shape[0], matrix.shape[1], rank, smallest,
            float(np.linalg.norm(rhs)), Certification.REJECTED,
        )
        raise np.linalg.LinAlgError(
            "reduced restoration Jacobian is not surjective; arbitrary node "
            "motion is not certified feasible"
        )
    delta = -vt[kept].T @ ((u[:, kept].T @ rhs) / singular[kept])
    remaining = float(np.linalg.norm(matrix @ delta + rhs))
    return delta, RestorationRankReport(
        matrix.shape[0], matrix.shape[1], rank, smallest, remaining,
        Certification.DIAGNOSTIC,
    )


def h1_equality_residual(
    candidate: QuadratureCandidate, gamma: ArrayLike
) -> FloatArray:
    graph = to_graph(candidate)
    value = np.asarray(gamma, dtype=float)
    return graph.h1_matrix @ value - graph.h1_rhs
