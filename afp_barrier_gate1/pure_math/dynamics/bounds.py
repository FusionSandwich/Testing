"""Residual ledgers and certified preconditioned iteration bounds."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg

FloatArray = NDArray[np.float64]

RESIDUAL_COMPONENTS = (
    "physical_bfp",
    "angular_generator",
    "angular_sampling",
    "spatial_discretization",
    "energy_group",
    "iteration",
)


def _finite_vector(value: ArrayLike, name: str, length: int | None = None) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 1 or out.size == 0 or (length is not None and len(out) != length):
        raise ValueError(f"{name} must be a nonempty vector of the required length")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains a nonfinite entry")
    return out


def _positive_weights(value: ArrayLike, length: int) -> FloatArray:
    out = _finite_vector(value, "weights", length)
    if np.min(out) <= 0.0:
        raise ValueError("weights must be strictly positive")
    return out


@dataclass(frozen=True)
class ResidualLedger:
    """An exact, named six-way residual decomposition.

    The total is the algebraic sum.  The certified triangle bound uses the sum
    of component norms and therefore never benefits from accidental numerical
    cancellation between modeling errors.
    """

    components: Mapping[str, FloatArray]
    total: FloatArray
    component_norms: Mapping[str, float]
    total_norm: float
    triangle_norm: float

    @classmethod
    def build(
        cls, components: Mapping[str, ArrayLike], weights: ArrayLike | None = None
    ) -> "ResidualLedger":
        if set(components) != set(RESIDUAL_COMPONENTS):
            missing = sorted(set(RESIDUAL_COMPONENTS) - set(components))
            extra = sorted(set(components) - set(RESIDUAL_COMPONENTS))
            raise ValueError(f"residual ledger keys mismatch; missing={missing}, extra={extra}")
        first = _finite_vector(components[RESIDUAL_COMPONENTS[0]], RESIDUAL_COMPONENTS[0])
        arrays: dict[str, FloatArray] = {RESIDUAL_COMPONENTS[0]: first.copy()}
        for name in RESIDUAL_COMPONENTS[1:]:
            arrays[name] = _finite_vector(components[name], name, len(first)).copy()
        mass = np.ones(len(first)) if weights is None else _positive_weights(weights, len(first))

        def norm(vector: FloatArray) -> float:
            return float(np.sqrt(np.dot(mass, vector * vector)))

        total = sum((arrays[name] for name in RESIDUAL_COMPONENTS), np.zeros(len(first)))
        norms = {name: norm(arrays[name]) for name in RESIDUAL_COMPONENTS}
        return cls(arrays, total, norms, norm(total), float(sum(norms.values())))

    def coercive_error_bound(self, coercivity: float, *, cancellation_safe: bool = True) -> float:
        if not np.isfinite(coercivity) or coercivity <= 0.0:
            raise ValueError("coercivity must be finite and positive")
        numerator = self.triangle_norm if cancellation_safe else self.total_norm
        return numerator / coercivity

    def response_estimate(self, adjoint: ArrayLike, weights: ArrayLike | None = None) -> dict[str, float]:
        vector = _finite_vector(adjoint, "adjoint", len(self.total))
        mass = np.ones(len(vector)) if weights is None else _positive_weights(weights, len(vector))
        estimates = {
            name: float(np.dot(mass * vector, self.components[name]))
            for name in RESIDUAL_COMPONENTS
        }
        estimates["total"] = float(sum(estimates.values()))
        return estimates


@dataclass(frozen=True)
class PreconditionedBound:
    contraction: float
    inverse_bound: float
    residual_error_bound: float


def preconditioned_bound(
    operator: ArrayLike,
    preconditioner: ArrayLike,
    residual: ArrayLike,
) -> PreconditionedBound:
    """Certify ``K^{-1}`` and error bounds from ``||I-M^{-1}K||_2<1``.

    ``residual_error_bound`` applies to an iterate with algebraic residual
    ``r=b-Kx`` and equals ``||M^{-1}r||/(1-q)``.
    """

    matrix = np.asarray(operator, dtype=float)
    metric = np.asarray(preconditioner, dtype=float)
    if (
        matrix.ndim != 2
        or matrix.shape[0] != matrix.shape[1]
        or metric.shape != matrix.shape
        or not np.all(np.isfinite(matrix))
        or not np.all(np.isfinite(metric))
    ):
        raise ValueError("operator and preconditioner must be finite square matrices of equal shape")
    vector = _finite_vector(residual, "residual", matrix.shape[0])
    try:
        preconditioned_operator = linalg.solve(metric, matrix, assume_a="gen")
        preconditioned_residual = linalg.solve(metric, vector, assume_a="gen")
        inverse_metric_norm = float(np.linalg.norm(linalg.solve(metric, np.eye(len(vector))), 2))
    except linalg.LinAlgError as exc:
        raise ValueError("preconditioner is singular") from exc
    contraction = float(np.linalg.norm(np.eye(len(vector)) - preconditioned_operator, 2))
    if not np.isfinite(contraction) or contraction >= 1.0:
        raise ValueError("preconditioned contraction is not strictly below one")
    denominator = 1.0 - contraction
    return PreconditionedBound(
        contraction,
        inverse_metric_norm / denominator,
        float(np.linalg.norm(preconditioned_residual, 2) / denominator),
    )


def iteration_error_bound(contraction: float, iterations: int, initial_error: float) -> float:
    if not np.isfinite(contraction) or not 0.0 <= contraction < 1.0:
        raise ValueError("contraction must lie in [0,1)")
    if isinstance(iterations, bool) or int(iterations) != iterations or iterations < 0:
        raise ValueError("iterations must be a nonnegative integer")
    if not np.isfinite(initial_error) or initial_error < 0.0:
        raise ValueError("initial_error must be finite and nonnegative")
    return float(contraction**int(iterations) * initial_error)
