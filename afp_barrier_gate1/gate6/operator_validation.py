"""Reusable invariant checks for Gate 6 angular transport operators.

The audit scripts intentionally remain executable research records.  This module
provides a smaller implementation contract that unit tests and future Radiant
adapters can call directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


class OperatorValidationError(ValueError):
    """Raised when an angular operator violates a required invariant."""


@dataclass(frozen=True)
class OperatorValidationMetrics:
    directions: int
    edges: int
    minimum_weight: float
    minimum_conductance: float
    minimum_rate: float
    maximum_rate: float
    direction_norm_error: float
    total_weight_error: float
    weighted_centroid_error: float
    reconstructed_rate_error: float
    symmetric_matrix_error: float
    symmetric_diagonal_error: float
    symmetric_edge_error: float
    constant_residual: float
    coordinate_residual: float


def _as_float_array(value: Any, name: str, ndim: int) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if array.ndim != ndim:
        raise OperatorValidationError(
            f"{name} must have {ndim} dimensions, got shape {array.shape}"
        )
    if not np.all(np.isfinite(array)):
        raise OperatorValidationError(f"{name} contains NaN or infinity")
    return array


def _apply_generator(operator: Any, values: np.ndarray) -> np.ndarray:
    """Apply the shared-edge generator to one or more columns."""

    data = np.asarray(values, dtype=float)
    squeeze = False
    if data.ndim == 1:
        data = data[:, None]
        squeeze = True
    if data.ndim != 2:
        raise OperatorValidationError("generator input must be one- or two-dimensional")

    result = np.zeros_like(data)
    difference = data[operator.edge_j] - data[operator.edge_i]
    np.add.at(
        result,
        operator.edge_i,
        operator.gamma[:, None] / operator.weights[operator.edge_i, None]
        * difference,
    )
    np.add.at(
        result,
        operator.edge_j,
        -operator.gamma[:, None] / operator.weights[operator.edge_j, None]
        * difference,
    )
    return result[:, 0] if squeeze else result


def validate_operator(
    operator: Any,
    *,
    expected_total_weight: float = 4.0 * np.pi,
    positivity_tolerance: float = 1.0e-14,
    algebra_tolerance: float = 5.0e-10,
    coordinate_tolerance: float = 5.0e-8,
    dense_limit: int = 2_000,
) -> OperatorValidationMetrics:
    """Validate the implementation contract of a reversible AFP operator.

    Required fields are the ones produced by `AngularOperator` in
    `angular_diffusion_transport_audit.py`: directions, weights, edge_i,
    edge_j, gamma, rate, and symmetric_matrix.
    """

    directions = _as_float_array(operator.directions, "directions", 2)
    weights = _as_float_array(operator.weights, "weights", 1)
    edge_i = np.asarray(operator.edge_i, dtype=int)
    edge_j = np.asarray(operator.edge_j, dtype=int)
    gamma = _as_float_array(operator.gamma, "gamma", 1)
    rate = _as_float_array(operator.rate, "rate", 1)
    symmetric = _as_float_array(operator.symmetric_matrix, "symmetric_matrix", 2)

    count = len(directions)
    if directions.shape != (count, 3):
        raise OperatorValidationError(
            f"directions must have shape (K, 3), got {directions.shape}"
        )
    if weights.shape != (count,) or rate.shape != (count,):
        raise OperatorValidationError("weights and rate must have one value per direction")
    if symmetric.shape != (count, count):
        raise OperatorValidationError(
            f"symmetric_matrix must have shape {(count, count)}, got {symmetric.shape}"
        )
    if edge_i.ndim != 1 or edge_j.ndim != 1:
        raise OperatorValidationError("edge indices must be one-dimensional")
    if not (len(edge_i) == len(edge_j) == len(gamma)):
        raise OperatorValidationError("edge_i, edge_j, and gamma lengths differ")
    if len(edge_i) == 0:
        raise OperatorValidationError("operator has no active edges")
    if np.min(edge_i) < 0 or np.min(edge_j) < 0:
        raise OperatorValidationError("edge index is negative")
    if np.max(edge_i) >= count or np.max(edge_j) >= count:
        raise OperatorValidationError("edge index exceeds direction count")
    if np.any(edge_i == edge_j):
        raise OperatorValidationError("self edges are not permitted")

    minimum_weight = float(np.min(weights))
    minimum_conductance = float(np.min(gamma))
    minimum_rate = float(np.min(rate))
    maximum_rate = float(np.max(rate))
    if minimum_weight <= positivity_tolerance:
        raise OperatorValidationError(
            f"nonpositive or tiny quadrature weight: {minimum_weight:.3e}"
        )
    if minimum_conductance <= positivity_tolerance:
        raise OperatorValidationError(
            f"nonpositive or tiny edge conductance: {minimum_conductance:.3e}"
        )
    if minimum_rate <= positivity_tolerance:
        raise OperatorValidationError(
            f"nonpositive or tiny outgoing rate: {minimum_rate:.3e}"
        )

    direction_norm_error = float(
        np.max(np.abs(np.linalg.norm(directions, axis=1) - 1.0))
    )
    total_weight_error = abs(float(np.sum(weights)) - expected_total_weight)
    weighted_centroid_error = float(
        np.max(np.abs(np.sum(weights[:, None] * directions, axis=0)))
    )

    reconstructed_rate = np.zeros(count, dtype=float)
    np.add.at(reconstructed_rate, edge_i, gamma / weights[edge_i])
    np.add.at(reconstructed_rate, edge_j, gamma / weights[edge_j])
    reconstructed_rate_error = float(np.max(np.abs(reconstructed_rate - rate)))

    symmetric_matrix_error = float(np.max(np.abs(symmetric - symmetric.T)))
    symmetric_diagonal_error = float(np.max(np.abs(np.diag(symmetric) + rate)))
    symmetric_edge_error = 0.0
    if count <= dense_limit:
        expected = np.zeros_like(symmetric)
        edge_values = gamma / np.sqrt(weights[edge_i] * weights[edge_j])
        np.add.at(expected, (edge_i, edge_j), edge_values)
        np.add.at(expected, (edge_j, edge_i), edge_values)
        expected[np.diag_indices_from(expected)] = -rate
        symmetric_edge_error = float(np.max(np.abs(expected - symmetric)))

    constant_residual = float(
        np.max(np.abs(_apply_generator(operator, np.ones(count, dtype=float))))
    )
    coordinate_residual = float(
        np.max(np.abs(_apply_generator(operator, directions) + 2.0 * directions))
    )

    checks = {
        "direction normalization": (direction_norm_error, algebra_tolerance),
        "total quadrature weight": (total_weight_error, algebra_tolerance),
        "weighted centroid": (weighted_centroid_error, algebra_tolerance),
        "reconstructed rate": (reconstructed_rate_error, algebra_tolerance),
        "weighted-symmetric matrix": (symmetric_matrix_error, algebra_tolerance),
        "symmetric diagonal": (symmetric_diagonal_error, algebra_tolerance),
        "symmetric edge assembly": (symmetric_edge_error, algebra_tolerance),
        "constant mode": (constant_residual, algebra_tolerance),
        "coordinate modes": (coordinate_residual, coordinate_tolerance),
    }
    failures = [
        f"{name} error {value:.3e} exceeds {limit:.3e}"
        for name, (value, limit) in checks.items()
        if value > limit
    ]
    if failures:
        raise OperatorValidationError("; ".join(failures))

    return OperatorValidationMetrics(
        directions=count,
        edges=len(gamma),
        minimum_weight=minimum_weight,
        minimum_conductance=minimum_conductance,
        minimum_rate=minimum_rate,
        maximum_rate=maximum_rate,
        direction_norm_error=direction_norm_error,
        total_weight_error=total_weight_error,
        weighted_centroid_error=weighted_centroid_error,
        reconstructed_rate_error=reconstructed_rate_error,
        symmetric_matrix_error=symmetric_matrix_error,
        symmetric_diagonal_error=symmetric_diagonal_error,
        symmetric_edge_error=symmetric_edge_error,
        constant_residual=constant_residual,
        coordinate_residual=coordinate_residual,
    )


def positivity_step_limit(operator: Any) -> float:
    """Return the sharp rowwise forward-Euler positivity limit."""

    rate = np.asarray(operator.rate, dtype=float)
    if rate.ndim != 1 or len(rate) == 0 or not np.all(np.isfinite(rate)):
        raise OperatorValidationError("invalid rate vector")
    maximum_rate = float(np.max(rate))
    if maximum_rate <= 0.0:
        raise OperatorValidationError("maximum rate must be positive")
    return 1.0 / maximum_rate
