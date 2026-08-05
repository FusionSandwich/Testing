"""Fail-closed numerical realizations of the harmonic-defect estimates.

The shell routines deliberately retain their ``n x r`` output.  In
particular, no multiplication by the transpose of the input frame is used:
leakage outside the sampled shell remains part of the reported defect.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg

FloatArray = NDArray[np.float64]


def _matrix(value: ArrayLike, name: str, *, square: bool = False) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 2 or (square and out.shape[0] != out.shape[1]):
        suffix = " square" if square else ""
        raise ValueError(f"{name} must be a{suffix} two-dimensional array")
    if out.size == 0 or not np.all(np.isfinite(out)):
        raise ValueError(f"{name} must be nonempty and finite")
    return out


def _vector(value: ArrayLike, name: str, length: int | None = None) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 1 or (length is not None and out.shape != (length,)):
        suffix = "" if length is None else f" of length {length}"
        raise ValueError(f"{name} must be a vector{suffix}")
    if out.size == 0 or not np.all(np.isfinite(out)):
        raise ValueError(f"{name} must be nonempty and finite")
    return out


def _weights(value: ArrayLike, length: int) -> FloatArray:
    out = _vector(value, "weights", length)
    if np.min(out) <= 0.0:
        raise ValueError("weights must be strictly positive")
    return out


def weighted_norm(value: ArrayLike, weights: ArrayLike) -> float:
    """Return the weighted Euclidean norm of one sampled vector."""

    vector = _vector(value, "value")
    mass = _weights(weights, len(vector))
    return float(np.sqrt(np.dot(mass, vector * vector)))


@dataclass(frozen=True)
class GeneratorReport:
    row_sum_error: float
    detailed_balance_error: float
    minimum_off_diagonal: float
    maximum_weighted_eigenvalue: float
    passed: bool


def validate_reversible_generator(
    generator: ArrayLike,
    weights: ArrayLike,
    *,
    tolerance: float = 5e-12,
) -> GeneratorReport:
    """Validate the positive, conservative, reversible generator convention.

    A failed structural condition raises ``ValueError``.  The returned report
    therefore certifies all four properties within the supplied tolerance.
    """

    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    matrix = _matrix(generator, "generator", square=True)
    n = matrix.shape[0]
    mass = _weights(weights, n)
    scale = max(1.0, float(np.linalg.norm(matrix, ord=np.inf)))
    row_error = float(np.linalg.norm(matrix @ np.ones(n), ord=np.inf))
    balance = mass[:, None] * matrix
    balance_error = float(np.linalg.norm(balance - balance.T, ord=np.inf))
    off_diagonal = matrix.copy()
    np.fill_diagonal(off_diagonal, np.inf)
    minimum_off = float(np.min(off_diagonal))
    root = np.sqrt(mass)
    symmetric = root[:, None] * matrix / root[None, :]
    symmetric_error = float(np.linalg.norm(symmetric - symmetric.T, ord=np.inf))
    if symmetric_error > tolerance * scale:
        raise ValueError("generator is not reversible in the weighted inner product")
    maximum_eigenvalue = float(np.max(linalg.eigvalsh(0.5 * (symmetric + symmetric.T))))
    failures: list[str] = []
    if row_error > tolerance * scale:
        failures.append("row sums")
    if balance_error > tolerance * max(1.0, float(np.linalg.norm(balance, ord=np.inf))):
        failures.append("detailed balance")
    if minimum_off < -tolerance * scale:
        failures.append("off-diagonal positivity")
    if np.max(np.diag(matrix)) > tolerance * scale:
        failures.append("nonpositive diagonal")
    if maximum_eigenvalue > tolerance * scale:
        failures.append("weighted dissipativity")
    if failures:
        raise ValueError("invalid reversible generator: " + ", ".join(failures))
    return GeneratorReport(
        row_error,
        balance_error,
        minimum_off,
        maximum_eigenvalue,
        True,
    )


@dataclass(frozen=True)
class ShellResidual:
    target_lambda: float
    frame: FloatArray
    residual: FloatArray
    weighted_residual: FloatArray
    defect: float
    gram_error: float


def shell_residual(
    generator: ArrayLike,
    weights: ArrayLike,
    quotient_frame: ArrayLike,
    target_lambda: float,
    *,
    orthonormality_tolerance: float = 5e-11,
) -> ShellResidual:
    """Construct the full-output sampled-shell residual and its operator norm."""

    matrix = _matrix(generator, "generator", square=True)
    mass = _weights(weights, matrix.shape[0])
    validate_reversible_generator(matrix, mass)
    frame = _matrix(quotient_frame, "quotient_frame")
    if frame.shape[0] != matrix.shape[0] or frame.shape[1] > frame.shape[0]:
        raise ValueError("quotient_frame has incompatible shape")
    if not np.isfinite(target_lambda) or target_lambda < 0.0:
        raise ValueError("target_lambda must be finite and nonnegative")
    gram = frame.T @ (mass[:, None] * frame)
    gram_error = float(np.linalg.norm(gram - np.eye(frame.shape[1]), ord=2))
    if gram_error > orthonormality_tolerance:
        raise ValueError("quotient_frame is not weighted-orthonormal")
    residual = matrix @ frame + target_lambda * frame
    weighted = np.sqrt(mass)[:, None] * residual
    defect = float(np.linalg.norm(weighted, ord=2))
    if not np.isfinite(defect):
        raise ValueError("shell defect is nonfinite")
    return ShellResidual(
        float(target_lambda),
        frame.copy(),
        residual,
        weighted,
        defect,
        gram_error,
    )


@dataclass(frozen=True)
class ModeErrorReport:
    error: float
    residual_norm: float
    bound: float
    effectivity: float


@dataclass(frozen=True)
class ShellErrorReport:
    """Full sampled-output shell error and its induced operator estimate."""

    error_matrix: FloatArray
    weighted_error_matrix: FloatArray
    error_operator_norm: float
    residual_operator_norm: float
    bound: float
    effectivity: float


def _mode_inputs(
    generator: ArrayLike, weights: ArrayLike, mode: ArrayLike, target_lambda: float
) -> tuple[FloatArray, FloatArray, FloatArray]:
    matrix = _matrix(generator, "generator", square=True)
    mass = _weights(weights, matrix.shape[0])
    validate_reversible_generator(matrix, mass)
    vector = _vector(mode, "mode", matrix.shape[0])
    if not np.isfinite(target_lambda) or target_lambda < 0.0:
        raise ValueError("target_lambda must be finite and nonnegative")
    return matrix, mass, vector


def semigroup_mode_error(
    generator: ArrayLike,
    weights: ArrayLike,
    mode: ArrayLike,
    target_lambda: float,
    time: float,
) -> ModeErrorReport:
    """Compute the exact matrix-exponential error and theorem bound."""

    matrix, mass, vector = _mode_inputs(generator, weights, mode, target_lambda)
    if not np.isfinite(time) or time < 0.0:
        raise ValueError("time must be finite and nonnegative")
    residual = matrix @ vector + target_lambda * vector
    residual_norm = weighted_norm(residual, mass)
    difference = linalg.expm(time * matrix) @ vector - np.exp(-target_lambda * time) * vector
    error = weighted_norm(difference, mass)
    bound = (
        float(time * residual_norm)
        if target_lambda == 0.0
        else float(-np.expm1(-target_lambda * time) * residual_norm / target_lambda)
    )
    effectivity = 1.0 if error == 0.0 and bound == 0.0 else bound / error
    if not np.isfinite(effectivity):
        raise ValueError("effectivity is nonfinite")
    return ModeErrorReport(error, residual_norm, bound, float(effectivity))


def resolvent_mode_error(
    generator: ArrayLike,
    weights: ArrayLike,
    mode: ArrayLike,
    target_lambda: float,
    alpha: float,
) -> ModeErrorReport:
    """Compute the resolvent error and the sharp contraction-based bound."""

    matrix, mass, vector = _mode_inputs(generator, weights, mode, target_lambda)
    if not np.isfinite(alpha) or alpha <= 0.0:
        raise ValueError("alpha must be finite and positive")
    residual = matrix @ vector + target_lambda * vector
    residual_norm = weighted_norm(residual, mass)
    resolved = linalg.solve(alpha * np.eye(len(vector)) - matrix, vector, assume_a="gen")
    difference = resolved - vector / (alpha + target_lambda)
    error = weighted_norm(difference, mass)
    bound = residual_norm / (alpha * (alpha + target_lambda))
    effectivity = 1.0 if error == 0.0 and bound == 0.0 else bound / error
    if not np.isfinite(effectivity):
        raise ValueError("effectivity is nonfinite")
    return ModeErrorReport(error, residual_norm, float(bound), float(effectivity))


def semigroup_shell_error(
    generator: ArrayLike,
    weights: ArrayLike,
    quotient_frame: ArrayLike,
    target_lambda: float,
    time: float,
) -> ShellErrorReport:
    """Evaluate the complete shell without projecting the output back to it."""

    shell = shell_residual(generator, weights, quotient_frame, target_lambda)
    if not np.isfinite(time) or time < 0.0:
        raise ValueError("time must be finite and nonnegative")
    matrix = np.asarray(generator, dtype=float)
    mass = np.asarray(weights, dtype=float)
    error_matrix = (
        linalg.expm(time * matrix) @ shell.frame
        - np.exp(-target_lambda * time) * shell.frame
    )
    weighted_error = np.sqrt(mass)[:, None] * error_matrix
    error_norm = float(np.linalg.norm(weighted_error, ord=2))
    bound = (
        float(time * shell.defect)
        if target_lambda == 0.0
        else float(-np.expm1(-target_lambda * time) * shell.defect / target_lambda)
    )
    effectivity = 1.0 if error_norm == 0.0 and bound == 0.0 else bound / error_norm
    if not np.isfinite(effectivity):
        raise ValueError("shell effectivity is nonfinite")
    return ShellErrorReport(
        error_matrix,
        weighted_error,
        error_norm,
        shell.defect,
        bound,
        float(effectivity),
    )


def resolvent_shell_error(
    generator: ArrayLike,
    weights: ArrayLike,
    quotient_frame: ArrayLike,
    target_lambda: float,
    alpha: float,
) -> ShellErrorReport:
    """Evaluate the complete shell resolvent without output compression."""

    shell = shell_residual(generator, weights, quotient_frame, target_lambda)
    if not np.isfinite(alpha) or alpha <= 0.0:
        raise ValueError("alpha must be finite and positive")
    matrix = np.asarray(generator, dtype=float)
    mass = np.asarray(weights, dtype=float)
    resolved = linalg.solve(
        alpha * np.eye(matrix.shape[0]) - matrix, shell.frame, assume_a="gen"
    )
    error_matrix = resolved - shell.frame / (alpha + target_lambda)
    weighted_error = np.sqrt(mass)[:, None] * error_matrix
    error_norm = float(np.linalg.norm(weighted_error, ord=2))
    bound = shell.defect / (alpha * (alpha + target_lambda))
    effectivity = 1.0 if error_norm == 0.0 and bound == 0.0 else bound / error_norm
    if not np.isfinite(effectivity):
        raise ValueError("shell effectivity is nonfinite")
    return ShellErrorReport(
        error_matrix,
        weighted_error,
        error_norm,
        shell.defect,
        float(bound),
        float(effectivity),
    )


@dataclass(frozen=True)
class BandSamplingReport:
    degrees: tuple[int, ...]
    column_count: int
    rank: int
    smallest_singular_value: float
    largest_singular_value: float
    inverse_stability: float


def band_sampling_guard(
    shell_frames: Mapping[int, ArrayLike],
    weights: ArrayLike,
    *,
    minimum_singular_value: float = 1e-10,
    ambiguity_factor: float = 10.0,
) -> BandSamplingReport:
    """Reject cross-shell aliases and numerically ambiguous injectivity.

    Each frame is interpreted as a coefficient-to-sample synthesis map.  The
    concatenated, mass-weighted map must be injective; checking shells one at a
    time would miss aliases between distinct degrees.
    """

    if not shell_frames:
        raise ValueError("at least one shell frame is required")
    if (
        not np.isfinite(minimum_singular_value)
        or minimum_singular_value <= 0.0
        or not np.isfinite(ambiguity_factor)
        or ambiguity_factor <= 1.0
    ):
        raise ValueError("invalid singular-value guard parameters")
    ordered: list[FloatArray] = []
    row_count: int | None = None
    degrees: list[int] = []
    for degree, raw_frame in sorted(shell_frames.items()):
        if int(degree) != degree or degree < 0:
            raise ValueError("shell degrees must be nonnegative integers")
        frame = _matrix(raw_frame, f"shell_frames[{degree}]")
        if row_count is None:
            row_count = frame.shape[0]
        if frame.shape[0] != row_count:
            raise ValueError("all shell frames must have the same row count")
        ordered.append(frame)
        degrees.append(int(degree))
    assert row_count is not None
    mass = _weights(weights, row_count)
    synthesis = np.concatenate(ordered, axis=1)
    weighted = np.sqrt(mass)[:, None] * synthesis
    singular_values = linalg.svdvals(weighted)
    column_count = synthesis.shape[1]
    if column_count > row_count or len(singular_values) < column_count:
        raise ValueError("band synthesis is not injective: more coefficients than samples")
    smallest = float(singular_values[-1])
    largest = float(singular_values[0])
    threshold = minimum_singular_value * max(1.0, largest)
    if smallest <= threshold:
        raise ValueError("band synthesis is not injective at the declared threshold")
    if smallest <= ambiguity_factor * threshold:
        raise ValueError("band synthesis rank is numerically ambiguous")
    return BandSamplingReport(
        tuple(degrees),
        column_count,
        column_count,
        smallest,
        largest,
        1.0 / smallest,
    )


@dataclass(frozen=True)
class PhysicalDissipativityReport:
    minimum_symmetrizer_eigenvalue: float
    maximum_symmetrizer_eigenvalue: float
    logarithmic_norm: float
    norm_equivalence_factor: float
    dissipative: bool


def physical_symmetrizer_dissipativity(
    operator: ArrayLike,
    symmetrizer: ArrayLike,
    *,
    reference_metric: ArrayLike | None = None,
    tolerance: float = 5e-12,
) -> PhysicalDissipativityReport:
    """Check dissipativity in ``<x,y>_M=x^T M y`` by generalized EVPs.

    The reported extremal eigenvalues and norm-equivalence factor are
    relative to ``reference_metric``.  Omitting it uses the Euclidean
    identity; passing the quadrature matrix ``W`` certifies
    ``m W <= M <= M_upper W`` exactly in the convention of Theorem 3.3.
    """

    matrix = _matrix(operator, "operator", square=True)
    metric = _matrix(symmetrizer, "symmetrizer", square=True)
    if metric.shape != matrix.shape:
        raise ValueError("operator and symmetrizer shapes differ")
    reference = (
        np.eye(matrix.shape[0], dtype=float)
        if reference_metric is None
        else _matrix(reference_metric, "reference_metric", square=True)
    )
    if reference.shape != matrix.shape:
        raise ValueError("operator and reference metric shapes differ")
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    symmetry_error = float(np.linalg.norm(metric - metric.T, ord=np.inf))
    if symmetry_error > tolerance * max(1.0, float(np.linalg.norm(metric, ord=np.inf))):
        raise ValueError("symmetrizer must be symmetric")
    metric = 0.5 * (metric + metric.T)
    reference_symmetry_error = float(
        np.linalg.norm(reference - reference.T, ord=np.inf)
    )
    if reference_symmetry_error > tolerance * max(
        1.0, float(np.linalg.norm(reference, ord=np.inf))
    ):
        raise ValueError("reference metric must be symmetric")
    reference = 0.5 * (reference + reference.T)
    if float(linalg.eigvalsh(metric)[0]) <= 0.0:
        raise ValueError("symmetrizer must be positive definite")
    if float(linalg.eigvalsh(reference)[0]) <= 0.0:
        raise ValueError("reference metric must be positive definite")
    relative_eigenvalues = linalg.eigvalsh(metric, reference)
    minimum = float(relative_eigenvalues[0])
    maximum = float(relative_eigenvalues[-1])
    symmetric_part = 0.5 * (metric @ matrix + matrix.T @ metric)
    logarithmic_norm = float(np.max(linalg.eigvalsh(symmetric_part, metric)))
    scale = max(1.0, float(np.linalg.norm(matrix, ord=2)))
    if logarithmic_norm > tolerance * scale:
        raise ValueError("operator is not dissipative in the physical symmetrizer")
    return PhysicalDissipativityReport(
        minimum,
        maximum,
        logarithmic_norm,
        float(np.sqrt(maximum / minimum)),
        True,
    )
