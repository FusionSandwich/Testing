"""Fixed-point-preserving low-order acceleration for Paper-II P2D/P2E.

The high-order matrix is never replaced.  A low-order matrix is used only in
residual correction or as a left preconditioner.  Every public routine checks
finite shapes and returns independently recomputed residual histories.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg
from scipy.sparse.linalg import LinearOperator, gmres

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ShellContraction:
    high: FloatArray
    low: FloatArray
    factors: FloatArray
    spectral_radius: float
    contractive: bool


@dataclass(frozen=True)
class FieldOfValuesReport:
    coercivity: float
    operator_norm: float
    omega: float
    norm_bound: float
    certified_contractive: bool


@dataclass(frozen=True)
class IterationResult:
    solution: FloatArray
    residual_history: tuple[float, ...]
    iterations: int
    matvecs: int
    converged: bool
    final_residual: float


def _matrix(value: ArrayLike, name: str) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.ndim != 2 or out.shape[0] != out.shape[1]:
        raise ValueError(f"{name} must be square")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains a nonfinite entry")
    return out


def _vector(value: ArrayLike, size: int, name: str) -> FloatArray:
    out = np.asarray(value, dtype=float)
    if out.shape != (size,) or not np.all(np.isfinite(out)):
        raise ValueError(f"{name} must be a finite vector of length {size}")
    return out


def error_propagation_operator(
    high_order: ArrayLike,
    low_order: ArrayLike,
    *,
    omega: float = 1.0,
) -> FloatArray:
    """Return ``I - omega A_L^{-1} A_H`` for residual correction.

    If ``A_H x=b`` is solved exactly, its solution is a fixed point of the
    correction for every nonsingular ``A_L`` and every finite ``omega``.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("high_order and low_order must have identical shapes")
    if not np.isfinite(omega):
        raise ValueError("omega must be finite")
    return np.eye(len(ah)) - float(omega) * linalg.solve(al, ah, assume_a="gen")


def shellwise_contraction(
    high_shell_values: ArrayLike,
    low_shell_values: ArrayLike,
    *,
    omega: float = 1.0,
) -> ShellContraction:
    """Exact contraction factors for a simultaneously diagonal shell model."""

    high = np.asarray(high_shell_values, dtype=float)
    low = np.asarray(low_shell_values, dtype=float)
    if high.ndim != 1 or low.shape != high.shape or not np.all(np.isfinite(high)) or not np.all(np.isfinite(low)):
        raise ValueError("shell arrays must be finite one-dimensional arrays of equal shape")
    if np.min(np.abs(low)) <= 0.0 or not np.isfinite(omega):
        raise ValueError("low shell values must be nonzero and omega finite")
    factors = 1.0 - float(omega) * high / low
    radius = float(np.max(np.abs(factors))) if factors.size else 0.0
    return ShellContraction(high.copy(), low.copy(), factors, radius, bool(radius < 1.0))


def field_of_values_bound(
    high_order: ArrayLike,
    low_order: ArrayLike,
    *,
    omega: float | None = None,
) -> FieldOfValuesReport:
    """Euclidean field-of-values bound for left residual correction.

    For ``B=A_L^{-1}A_H``, if the Hermitian part has lower bound ``alpha>0``
    and ``||B||<=beta``, then

    ``||I-omega B|| <= sqrt(1-2 omega alpha+omega^2 beta^2)``.

    The default ``omega=alpha/beta^2`` minimizes this displayed bound.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    bmat = linalg.solve(al, ah, assume_a="gen")
    hermitian = 0.5 * (bmat + bmat.T)
    alpha = float(np.min(np.linalg.eigvalsh(hermitian)))
    beta = float(np.linalg.norm(bmat, ord=2))
    chosen = (alpha / beta**2) if omega is None and beta > 0.0 else float(1.0 if omega is None else omega)
    radicand = 1.0 - 2.0 * chosen * alpha + chosen**2 * beta**2
    bound = math.sqrt(max(0.0, radicand))
    return FieldOfValuesReport(alpha, beta, chosen, bound, bool(alpha > 0.0 and bound < 1.0))


def perturbation_contraction_bound(high_order: ArrayLike, low_order: ArrayLike) -> float:
    """Return ``||A_L^{-1}||_2 ||A_L-A_H||_2``."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    inverse_norm = 1.0 / float(np.min(np.linalg.svd(al, compute_uv=False)))
    return inverse_norm * float(np.linalg.norm(al - ah, ord=2))


def invariant_residuals(
    high_order: ArrayLike,
    low_order: ArrayLike,
    left_invariants: ArrayLike,
) -> dict[str, float]:
    """Check left conservation invariants for high and low operators."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    q = np.asarray(left_invariants, dtype=float)
    if q.ndim == 1:
        q = q[None, :]
    if q.ndim != 2 or q.shape[1] != len(ah) or not np.all(np.isfinite(q)):
        raise ValueError("left_invariants must have one column per unknown")
    return {
        "high": float(np.linalg.norm(q @ ah, ord=np.inf)),
        "low": float(np.linalg.norm(q @ al, ord=np.inf)),
        "mismatch": float(np.linalg.norm(q @ (ah - al), ord=np.inf)),
    }



def constrained_low_inverse(
    low_order: ArrayLike,
    constraints: ArrayLike,
) -> FloatArray:
    """Return the exact low-order correction map constrained by ``Q delta=0``.

    For full-row-rank ``Q`` and nonsingular ``A_L``, the returned matrix is

    ``P_L=A_L^{-1}-A_L^{-1}Q^T(QA_L^{-1}Q^T)^{-1}QA_L^{-1}``.

    Thus ``Q P_L=0``.  A compatible initial iterate retains its declared
    conservation values under every residual correction.
    """

    al = _matrix(low_order, "low_order")
    q = np.asarray(constraints, dtype=float)
    if q.ndim == 1:
        q = q[None, :]
    if q.ndim != 2 or q.shape[1] != len(al) or not np.all(np.isfinite(q)):
        raise ValueError("constraints must be finite with one column per unknown")
    if q.shape[0] == 0:
        return linalg.inv(al)
    if np.linalg.matrix_rank(q) != q.shape[0]:
        raise ValueError("constraints must have full row rank")
    inverse = linalg.solve(al, np.eye(len(al)), assume_a="gen")
    schur = q @ inverse @ q.T
    if np.linalg.matrix_rank(schur) != len(schur):
        raise ValueError("constrained low-order Schur complement is singular")
    correction = inverse - inverse @ q.T @ linalg.solve(schur, q @ inverse, assume_a="gen")
    residual = float(np.linalg.norm(q @ correction, ord=np.inf))
    if residual > 5e-11 * max(1.0, float(np.linalg.norm(correction, ord=np.inf))):
        raise ArithmeticError(f"constraint projection residual {residual:.3e}")
    return correction


def constrained_error_propagation_operator(
    high_order: ArrayLike,
    low_order: ArrayLike,
    constraints: ArrayLike,
    *,
    omega: float = 1.0,
) -> FloatArray:
    """Return ``I-omega P_L A_H`` with ``Q P_L=0``."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    if not np.isfinite(omega):
        raise ValueError("omega must be finite")
    return np.eye(len(ah)) - float(omega) * constrained_low_inverse(al, constraints) @ ah


def constrained_defect_correction(
    high_order: ArrayLike,
    rhs: ArrayLike,
    low_order: ArrayLike,
    constraints: ArrayLike,
    *,
    initial: ArrayLike,
    omega: float = 1.0,
    rtol: float = 1e-10,
    atol: float = 1e-13,
    max_iterations: int = 1000,
) -> IterationResult:
    """Residual correction whose every update satisfies ``Q delta=0``.

    Convergence to the high-order solution is possible only when the initial
    iterate and exact solution have the same constraint values.  The routine
    checks that compatibility instead of silently projecting to the wrong
    fixed point.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    b = _vector(rhs, len(ah), "rhs")
    x = _vector(initial, len(ah), "initial").copy()
    q = np.asarray(constraints, dtype=float)
    if q.ndim == 1:
        q = q[None, :]
    projector = constrained_low_inverse(al, q)
    exact = linalg.solve(ah, b, assume_a="gen")
    compatibility = float(np.linalg.norm(q @ (x - exact), ord=np.inf))
    if compatibility > 2e-10 * max(1.0, float(np.linalg.norm(q @ exact, ord=np.inf))):
        raise ValueError(f"initial iterate is conservation-incompatible: {compatibility:.3e}")
    scale = max(float(np.linalg.norm(b)), 1.0)
    history: list[float] = []
    matvecs = 0
    invariant = q @ x
    for _ in range(max_iterations + 1):
        residual = b - ah @ x
        matvecs += 1
        norm = float(np.linalg.norm(residual))
        history.append(norm)
        if norm <= atol + rtol * scale:
            return IterationResult(x, tuple(history), len(history) - 1, matvecs, True, norm)
        if len(history) > max_iterations:
            break
        x = x + float(omega) * (projector @ residual)
        drift = float(np.linalg.norm(q @ x - invariant, ord=np.inf))
        if drift > 5e-10 * max(1.0, float(np.linalg.norm(invariant, ord=np.inf))):
            raise ArithmeticError(f"conservation drift {drift:.3e}")
    return IterationResult(x, tuple(history), max_iterations, matvecs, False, history[-1])

def defect_correction(
    high_order: ArrayLike,
    rhs: ArrayLike,
    low_order: ArrayLike,
    *,
    initial: ArrayLike | None = None,
    omega: float = 1.0,
    rtol: float = 1e-10,
    atol: float = 1e-13,
    max_iterations: int = 1000,
) -> IterationResult:
    """Stationary residual correction with exact fixed point preservation."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    b = _vector(rhs, len(ah), "rhs")
    x = np.zeros_like(b) if initial is None else _vector(initial, len(ah), "initial").copy()
    if not np.isfinite(omega) or rtol <= 0.0 or atol < 0.0 or max_iterations < 0:
        raise ValueError("invalid iteration controls")
    scale = max(float(np.linalg.norm(b)), 1.0)
    history: list[float] = []
    matvecs = 0
    for _ in range(max_iterations + 1):
        residual = b - ah @ x
        matvecs += 1
        norm = float(np.linalg.norm(residual))
        history.append(norm)
        if norm <= atol + rtol * scale:
            return IterationResult(x, tuple(history), len(history) - 1, matvecs, True, norm)
        if len(history) > max_iterations:
            break
        correction = linalg.solve(al, residual, assume_a="gen")
        x = x + float(omega) * correction
    return IterationResult(x, tuple(history), max_iterations, matvecs, False, history[-1])


def preconditioned_gmres(
    high_order: ArrayLike,
    rhs: ArrayLike,
    *,
    low_order: ArrayLike | None = None,
    initial: ArrayLike | None = None,
    rtol: float = 1e-10,
    atol: float = 1e-13,
    restart: int | None = None,
    max_iterations: int | None = None,
) -> IterationResult:
    """GMRES using ``A_L`` only as a left preconditioner.

    The returned residual history is recomputed in the original high-order
    system, so a preconditioned callback norm cannot hide a bad fixed point.
    """

    ah = _matrix(high_order, "high_order")
    b = _vector(rhs, len(ah), "rhs")
    x0 = None if initial is None else _vector(initial, len(ah), "initial")
    if rtol <= 0.0 or atol < 0.0:
        raise ValueError("invalid tolerances")
    matvecs = 0

    def action(v: FloatArray) -> FloatArray:
        nonlocal matvecs
        matvecs += 1
        return ah @ v

    operator = LinearOperator(ah.shape, matvec=action, dtype=float)
    preconditioner: LinearOperator | None = None
    if low_order is not None:
        al = _matrix(low_order, "low_order")
        if al.shape != ah.shape:
            raise ValueError("matrix shapes differ")
        preconditioner = LinearOperator(
            al.shape,
            matvec=lambda v: linalg.solve(al, v, assume_a="gen"),
            dtype=float,
        )

    callback_count = 0

    def callback(_value: object) -> None:
        nonlocal callback_count
        callback_count += 1

    solution, info = gmres(
        operator,
        b,
        x0=x0,
        M=preconditioner,
        rtol=float(rtol),
        atol=float(atol),
        restart=restart,
        maxiter=max_iterations,
        callback=callback,
        callback_type="pr_norm",
    )
    solution = np.asarray(solution, dtype=float)
    final = float(np.linalg.norm(b - ah @ solution))
    matvecs += 1
    scale = max(float(np.linalg.norm(b)), 1.0)
    converged = bool(info == 0 and final <= atol + rtol * scale * 5.0)
    # SciPy exposes only the preconditioned callback history.  We retain a
    # deterministic two-point original-system history and the true count.
    initial_residual = float(np.linalg.norm(b - ah @ (np.zeros_like(b) if x0 is None else x0)))
    return IterationResult(
        solution,
        (initial_residual, final),
        callback_count,
        matvecs,
        converged,
        final,
    )
