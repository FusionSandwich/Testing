"""Positive conservative transfers between angular grids."""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import linprog, lsq_linear

from .quadrature import PositiveQuadrature, farkas_infeasibility_certificate

FloatArray = NDArray[np.float64]


def moment_matrix(quadrature: PositiveQuadrature, feature_values: ArrayLike) -> FloatArray:
    F = np.asarray(feature_values, dtype=float)
    if F.ndim != 2 or F.shape[1] != quadrature.n_node:
        raise ValueError("feature_values must have shape (K,N)")
    return F * quadrature.weights[None, :]


@dataclass(frozen=True)
class TransferResult:
    transfer: FloatArray | None
    feasible: bool
    residual_norm: float
    minimum_entry: float
    column_certificates: tuple[object, ...]
    status: str


def _validated_moment_pair(
    source_moments: ArrayLike, target_moments: ArrayLike
) -> tuple[FloatArray, FloatArray]:
    MA = np.asarray(source_moments, dtype=float)
    MB = np.asarray(target_moments, dtype=float)
    if (
        MA.ndim != 2
        or MB.ndim != 2
        or MA.shape[0] != MB.shape[0]
        or np.any(~np.isfinite(MA))
        or np.any(~np.isfinite(MB))
    ):
        raise ValueError("finite moment matrices must have the same row count")
    return MA, MB


def universal_positive_transfer(
    source_moments: ArrayLike,
    target_moments: ArrayLike,
    tolerance: float = 1e-10,
) -> TransferResult:
    """Find ``T>=0`` satisfying ``M_target T = M_source`` column by column."""
    MA, MB = _validated_moment_pair(source_moments, target_moments)
    if not np.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and nonnegative")
    T = np.zeros((MB.shape[1], MA.shape[1]))
    certificates = []
    statuses = []
    for j in range(MA.shape[1]):
        result = linprog(np.zeros(MB.shape[1]), A_eq=MB, b_eq=MA[:, j], bounds=(0.0, None), method="highs")
        statuses.append(result.message)
        if not result.success:
            certificates.append(farkas_infeasibility_certificate(MB, MA[:, j]))
            return TransferResult(None, False, math.inf, math.nan, tuple(certificates), "; ".join(statuses))
        T[:, j] = np.maximum(result.x, 0.0)
        certificates.append(None)
    residual = MB @ T - MA
    feasible = bool(np.linalg.norm(residual, ord=np.inf) <= tolerance)
    return TransferResult(T, feasible, float(np.linalg.norm(residual)), float(np.min(T)) if T.size else 0.0, tuple(certificates), "; ".join(statuses))


def current_preserving_no_go(source: PositiveQuadrature, target: PositiveQuadrature, tolerance: float = 1e-10) -> dict[str, object]:
    """Check the strict-convexity obstruction for mass+three-current transfer."""
    missing = []
    for node in source.nodes:
        if np.min(np.linalg.norm(target.nodes - node[None, :], axis=1)) > tolerance:
            missing.append(node)
    return {
        "universal_positive_mass_current_transfer_possible": len(missing) == 0,
        "missing_source_directions": np.asarray(missing),
        "reason": "A unit vector is an extreme point of the unit ball, so a positive convex combination of unit target directions equals it only when that direction is present.",
    }


@dataclass(frozen=True)
class StateRemapResult:
    target_state: FloatArray | None
    feasible: bool
    residual_norm: float
    minimum_value: float
    certificate: object | None


def state_specific_positive_remap(
    source_state: ArrayLike,
    source_moments: ArrayLike,
    target_moments: ArrayLike,
    tolerance: float = 1e-10,
) -> StateRemapResult:
    fA = np.asarray(source_state, dtype=float).reshape(-1)
    MA, MB = _validated_moment_pair(source_moments, target_moments)
    if (
        MA.shape[1] != fA.size
        or np.any(~np.isfinite(fA))
        or np.any(fA < 0.0)
        or not np.isfinite(tolerance)
        or tolerance < 0.0
    ):
        raise ValueError("source state must be finite, nonnegative, and align with M_source")
    target = MA @ fA
    result = linprog(np.zeros(MB.shape[1]), A_eq=MB, b_eq=target, bounds=(0.0, None), method="highs")
    if not result.success:
        cert = farkas_infeasibility_certificate(MB, target)
        return StateRemapResult(None, False, math.inf, math.nan, cert)
    fB = np.maximum(result.x, 0.0)
    residual = MB @ fB - target
    return StateRemapResult(fB, np.linalg.norm(residual, ord=np.inf) <= tolerance, float(np.linalg.norm(residual)), float(np.min(fB)) if fB.size else 0.0, None)


def mass_exact_near_transfer(source: PositiveQuadrature, target: PositiveQuadrature) -> TransferResult:
    """Nearest-direction positive transfer preserving the total integral exactly."""
    T = np.zeros((target.n_node, source.n_node))
    for j, node in enumerate(source.nodes):
        i = int(np.argmin(np.linalg.norm(target.nodes - node[None, :], axis=1)))
        T[i, j] = source.weights[j] / target.weights[i]
    MA = source.weights[None, :]
    MB = target.weights[None, :]
    residual = MB @ T - MA
    return TransferResult(T, True, float(np.linalg.norm(residual)), float(np.min(T)) if T.size else 0.0, (), "nearest-node mass-exact fallback")


def minimum_residual_positive_transfer(
    source_moments: ArrayLike,
    target_moments: ArrayLike,
    tolerance: float = 1e-10,
) -> TransferResult:
    MA, MB = _validated_moment_pair(source_moments, target_moments)
    if not np.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and nonnegative")
    T = np.zeros((MB.shape[1], MA.shape[1]))
    messages = []
    for j in range(MA.shape[1]):
        result = lsq_linear(MB, MA[:, j], bounds=(0.0, np.inf), tol=1e-12, lsmr_tol=1e-12)
        T[:, j] = np.maximum(result.x, 0.0)
        messages.append(str(result.status))
    residual = MB @ T - MA
    residual_norm = float(np.linalg.norm(residual))
    feasible = bool(np.linalg.norm(residual, ord=np.inf) <= tolerance)
    return TransferResult(
        T,
        feasible,
        residual_norm,
        float(np.min(T)) if T.size else 0.0,
        (),
        ",".join(messages),
    )


def repeated_transfer_error_bound(single_step_defects: ArrayLike, initial_weighted_l1_norm: float = 1.0) -> float:
    """Additive bound for positive mass-preserving L1-nonexpansive transfers."""
    defects = np.asarray(single_step_defects, dtype=float)
    if np.any(defects < 0.0) or initial_weighted_l1_norm < 0.0:
        raise ValueError("defects and norm must be nonnegative")
    return float(initial_weighted_l1_norm * np.sum(defects))


@dataclass(frozen=True)
class TransferDiagnostics:
    moment_residual: FloatArray
    moment_infinity_norm: float
    minimum_entry: float
    weighted_l1_operator_norm: float
    positive: bool
    mass_preserving: bool
    l1_nonexpansive: bool


def transfer_diagnostics(
    transfer: ArrayLike,
    source: PositiveQuadrature,
    target: PositiveQuadrature,
    source_moments: ArrayLike | None = None,
    target_moments: ArrayLike | None = None,
    tolerance: float = 1e-10,
) -> TransferDiagnostics:
    """Audit positivity, moments, and weighted-L1 stability of a transfer."""

    T = np.asarray(transfer, dtype=float)
    if T.shape != (target.n_node, source.n_node) or np.any(~np.isfinite(T)):
        raise ValueError("transfer must be finite with shape (target_nodes, source_nodes)")
    if not np.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and nonnegative")
    if source_moments is None and target_moments is None:
        MA = source.weights[None, :]
        MB = target.weights[None, :]
    elif source_moments is not None and target_moments is not None:
        MA = np.asarray(source_moments, dtype=float)
        MB = np.asarray(target_moments, dtype=float)
        if (
            MA.ndim != 2
            or MB.ndim != 2
            or MA.shape != (MB.shape[0], source.n_node)
            or MB.shape[1] != target.n_node
            or np.any(~np.isfinite(MA))
            or np.any(~np.isfinite(MB))
        ):
            raise ValueError("moment matrices do not align with quadratures")
    else:
        raise ValueError("provide both source_moments and target_moments or neither")
    residual = MB @ T - MA
    minimum = float(np.min(T, initial=np.inf))
    weighted_column_sums = target.weights @ np.abs(T)
    l1_norm = float(np.max(weighted_column_sums / source.weights, initial=0.0))
    mass_residual = target.weights @ T - source.weights
    return TransferDiagnostics(
        moment_residual=residual,
        moment_infinity_norm=float(np.linalg.norm(residual, ord=np.inf)),
        minimum_entry=minimum,
        weighted_l1_operator_norm=l1_norm,
        positive=minimum >= -tolerance,
        mass_preserving=float(np.linalg.norm(mass_residual, ord=np.inf)) <= tolerance,
        l1_nonexpansive=l1_norm <= 1.0 + tolerance,
    )


def compose_transfers(*transfers: ArrayLike, tolerance: float = 1e-13) -> FloatArray:
    """Compose consecutive positive transfer matrices in application order."""

    if not transfers:
        raise ValueError("at least one transfer is required")
    matrices = [np.asarray(value, dtype=float) for value in transfers]
    for matrix in matrices:
        if matrix.ndim != 2 or np.any(~np.isfinite(matrix)):
            raise ValueError("every transfer must be a finite matrix")
        if np.min(matrix, initial=0.0) < -tolerance:
            raise ValueError("positive transfer composition received a negative entry")
    result = matrices[0]
    for matrix in matrices[1:]:
        if matrix.shape[1] != result.shape[0]:
            raise ValueError("consecutive transfer dimensions do not align")
        result = matrix @ result
    result[np.abs(result) <= tolerance] = 0.0
    return result


def apply_angular_transfer(
    transfer: ArrayLike,
    values: ArrayLike,
    axis: int = -1,
) -> FloatArray:
    """Apply a target-by-source transfer along an arbitrary array axis."""

    T = np.asarray(transfer, dtype=float)
    data = np.asarray(values, dtype=float)
    if T.ndim != 2 or np.any(~np.isfinite(T)) or np.any(~np.isfinite(data)):
        raise ValueError("transfer and values must be finite")
    if data.ndim == 0 or not -data.ndim <= axis < data.ndim:
        raise np.exceptions.AxisError(axis, ndim=data.ndim)
    normalized_axis = int(axis % data.ndim)
    if data.shape[normalized_axis] != T.shape[1]:
        raise ValueError("selected values axis does not match source transfer dimension")
    moved = np.moveaxis(data, normalized_axis, -1)
    mapped = np.einsum("...j,ij->...i", moved, T)
    return np.moveaxis(mapped, -1, normalized_axis)


def transfer_chain_error_bound(
    local_defects: ArrayLike,
    weighted_l1_operator_norms: ArrayLike,
    initial_error: float = 0.0,
) -> float:
    """Bound accumulated error for a sequence of possibly expansive transfers.

    The recurrence is ``e_{k+1} <= ||T_k|| e_k + delta_k``.
    For positive mass-preserving transfers each norm is one, recovering the
    additive defect bound.
    """

    defects = np.asarray(local_defects, dtype=float).reshape(-1)
    norms = np.asarray(weighted_l1_operator_norms, dtype=float).reshape(-1)
    if defects.shape != norms.shape:
        raise ValueError("one operator norm is required for every local defect")
    if (
        np.any(~np.isfinite(defects))
        or np.any(~np.isfinite(norms))
        or np.any(defects < 0.0)
        or np.any(norms < 0.0)
        or not np.isfinite(initial_error)
        or initial_error < 0.0
    ):
        raise ValueError("error-bound inputs must be finite and nonnegative")
    error = float(initial_error)
    for defect, operator_norm in zip(defects, norms, strict=True):
        error = float(operator_norm * error + defect)
    return error
