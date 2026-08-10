"""Fixed-point-preserving low-order acceleration for Paper-II P2D/P2E.

The high-order matrix is never replaced.  A low-order matrix is used only in
residual correction or as a left preconditioner.  Every public routine checks
finite shapes and returns independently recomputed high-order residuals.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import time

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
    metric_condition: float = 1.0


@dataclass(frozen=True)
class SpectralEquivalenceReport:
    lower: float
    upper: float
    condition_bound: float
    positive: bool
    metric_condition: float


@dataclass(frozen=True)
class SlowSubspaceReport:
    dimension: int
    contraction_norm: float
    invariance_leakage: float
    mismatch_norm: float
    low_inverse_norm: float
    certified_contractive_on_basis: bool


@dataclass(frozen=True)
class TransportMismatchReport:
    total_mismatch_norm: float
    angular_mismatch_norm: float
    streaming_mismatch_norm: float
    energy_mismatch_norm: float
    boundary_mismatch_norm: float
    decomposition_residual: float


@dataclass(frozen=True)
class IterationResult:
    solution: FloatArray
    residual_history: tuple[float, ...]
    iterations: int
    matvecs: int
    converged: bool
    final_residual: float
    setup_seconds: float = 0.0
    solve_seconds: float = 0.0
    low_solves: int = 0
    preconditioner_bytes: int = 0


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


def _metric_similarity(matrix: FloatArray, metric: ArrayLike | None) -> tuple[FloatArray, float]:
    """Return the Euclidean representative of an operator in an SPD metric."""

    if metric is None:
        return matrix, 1.0
    m = _matrix(metric, "metric")
    if m.shape != matrix.shape or np.linalg.norm(m - m.T, ord=np.inf) > 1e-11:
        raise ValueError("metric must be symmetric and match the operator")
    eigenvalues = np.linalg.eigvalsh(m)
    if float(np.min(eigenvalues)) <= 0.0:
        raise ValueError("metric must be positive definite")
    root = linalg.cholesky(m, lower=False)
    transformed = root @ matrix @ linalg.solve(root, np.eye(len(root)), assume_a="gen")
    return transformed, float(np.max(eigenvalues) / np.min(eigenvalues))


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
    if (
        high.ndim != 1
        or low.shape != high.shape
        or not np.all(np.isfinite(high))
        or not np.all(np.isfinite(low))
    ):
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
    metric: ArrayLike | None = None,
) -> FieldOfValuesReport:
    """Field-of-values contraction bound in Euclidean or an SPD metric.

    For ``B=A_L^{-1}A_H``, if the Hermitian part in the declared metric has
    lower bound ``alpha>0`` and ``||B||<=beta``, then

    ``||I-omega B|| <= sqrt(1-2 omega alpha+omega^2 beta^2)``.

    The default ``omega=alpha/beta^2`` minimizes this displayed bound.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    bmat = linalg.solve(al, ah, assume_a="gen")
    representative, metric_condition = _metric_similarity(bmat, metric)
    hermitian = 0.5 * (representative + representative.T)
    alpha = float(np.min(np.linalg.eigvalsh(hermitian)))
    beta = float(np.linalg.norm(representative, ord=2))
    chosen = (
        alpha / beta**2
        if omega is None and beta > 0.0
        else float(1.0 if omega is None else omega)
    )
    if not np.isfinite(chosen):
        raise ValueError("omega must be finite")
    radicand = 1.0 - 2.0 * chosen * alpha + chosen**2 * beta**2
    bound = math.sqrt(max(0.0, radicand))
    return FieldOfValuesReport(
        alpha,
        beta,
        chosen,
        bound,
        bool(alpha > 0.0 and bound < 1.0),
        metric_condition,
    )


def spectral_equivalence_bound(
    high_order: ArrayLike,
    low_order: ArrayLike,
    *,
    metric: ArrayLike | None = None,
) -> SpectralEquivalenceReport:
    """Generalized Rayleigh bounds for symmetric positive representatives.

    This is a sufficient-condition utility.  It rejects nonsymmetric or
    nonpositive transformed operators rather than silently applying an SPD
    theorem to a streaming-dominated nonsymmetric system.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    ahat, metric_condition = _metric_similarity(ah, metric)
    lhat, _ = _metric_similarity(al, metric)
    if (
        np.linalg.norm(ahat - ahat.T, ord=np.inf) > 2e-10
        or np.linalg.norm(lhat - lhat.T, ord=np.inf) > 2e-10
    ):
        raise ValueError("spectral equivalence requires symmetric metric representatives")
    low_eigen = np.linalg.eigvalsh(0.5 * (lhat + lhat.T))
    if float(np.min(low_eigen)) <= 0.0:
        raise ValueError("low-order representative is not positive definite")
    values = linalg.eigvalsh(0.5 * (ahat + ahat.T), 0.5 * (lhat + lhat.T))
    lower = float(np.min(values))
    upper = float(np.max(values))
    positive = bool(lower > 0.0)
    condition = float(upper / lower) if positive else float("inf")
    return SpectralEquivalenceReport(lower, upper, condition, positive, metric_condition)


def perturbation_contraction_bound(high_order: ArrayLike, low_order: ArrayLike) -> float:
    """Return ``||A_L^{-1}||_2 ||A_L-A_H||_2``."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    if ah.shape != al.shape:
        raise ValueError("matrix shapes differ")
    inverse_norm = 1.0 / float(np.min(np.linalg.svd(al, compute_uv=False)))
    return inverse_norm * float(np.linalg.norm(al - ah, ord=2))


def iteration_count_bound(contraction: float, initial_error: float, tolerance: float) -> int:
    """Return a sufficient stationary-iteration count from ``||E||<=rho<1``."""

    if not all(np.isfinite(v) for v in (contraction, initial_error, tolerance)):
        raise ValueError("iteration-count inputs must be finite")
    if not 0.0 <= contraction < 1.0 or initial_error < 0.0 or tolerance <= 0.0:
        raise ValueError("need 0<=contraction<1, initial_error>=0, tolerance>0")
    if initial_error <= tolerance or contraction == 0.0:
        return 0 if initial_error <= tolerance else 1
    return int(math.ceil(math.log(tolerance / initial_error) / math.log(contraction)))


def slow_subspace_report(
    high_order: ArrayLike,
    low_order: ArrayLike,
    basis: ArrayLike,
    *,
    omega: float = 1.0,
) -> SlowSubspaceReport:
    """Audit the actual correction on a declared relevant slow subspace.

    ``basis`` is orthonormalized before evaluation.  The report distinguishes
    the restricted action ``||EV||`` from leakage outside ``span(V)``; this
    prevents an isolated angular eigenvalue claim from masquerading as a full
    transport acceleration result.
    """

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    raw = np.asarray(basis, dtype=float)
    if raw.ndim == 1:
        raw = raw[:, None]
    if raw.ndim != 2 or raw.shape[0] != len(ah) or not np.all(np.isfinite(raw)):
        raise ValueError("basis must be finite with one row per unknown")
    q, r = np.linalg.qr(raw, mode="reduced")
    rank = int(np.linalg.matrix_rank(r))
    if rank == 0:
        raise ValueError("basis has zero rank")
    q = q[:, :rank]
    error = error_propagation_operator(ah, al, omega=omega)
    action = error @ q
    projected = q @ (q.T @ action)
    contraction = float(np.linalg.norm(action, ord=2))
    leakage = float(np.linalg.norm(action - projected, ord=2))
    mismatch = float(np.linalg.norm((al - ah) @ q, ord=2))
    low_inverse = 1.0 / float(np.min(np.linalg.svd(al, compute_uv=False)))
    return SlowSubspaceReport(
        rank,
        contraction,
        leakage,
        mismatch,
        low_inverse,
        bool(contraction < 1.0),
    )


def transport_mismatch_decomposition(
    high_order: ArrayLike,
    low_order: ArrayLike,
    *,
    angular_high: ArrayLike,
    angular_low: ArrayLike,
    streaming_high: ArrayLike,
    streaming_low: ArrayLike,
    energy_high: ArrayLike,
    energy_low: ArrayLike,
    boundary_high: ArrayLike,
    boundary_low: ArrayLike,
) -> TransportMismatchReport:
    """Check an explicit angular/streaming/energy/boundary decomposition."""

    ah = _matrix(high_order, "high_order")
    al = _matrix(low_order, "low_order")
    pieces = []
    names = (
        (angular_high, angular_low, "angular"),
        (streaming_high, streaming_low, "streaming"),
        (energy_high, energy_low, "energy"),
        (boundary_high, boundary_low, "boundary"),
    )
    norms: dict[str, float] = {}
    for high, low, name in names:
        h = _matrix(high, f"{name}_high")
        l = _matrix(low, f"{name}_low")
        if h.shape != ah.shape or l.shape != ah.shape:
            raise ValueError("all decomposition pieces must match the full operator")
        difference = l - h
        pieces.append(difference)
        norms[name] = float(np.linalg.norm(difference, ord=2))
    residual = (al - ah) - sum(pieces, np.zeros_like(ah))
    return TransportMismatchReport(
        float(np.linalg.norm(al - ah, ord=2)),
        norms["angular"],
        norms["streaming"],
        norms["energy"],
        norms["boundary"],
        float(np.linalg.norm(residual, ord=2)),
    )


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
    correction = inverse - inverse @ q.T @ linalg.solve(
        schur, q @ inverse, assume_a="gen"
    )
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
    setup_start = time.perf_counter()
    projector = constrained_low_inverse(al, q)
    setup_seconds = time.perf_counter() - setup_start
    exact = linalg.solve(ah, b, assume_a="gen")
    compatibility = float(np.linalg.norm(q @ (x - exact), ord=np.inf))
    if compatibility > 2e-10 * max(1.0, float(np.linalg.norm(q @ exact, ord=np.inf))):
        raise ValueError(f"initial iterate is conservation-incompatible: {compatibility:.3e}")
    scale = max(float(np.linalg.norm(b)), 1.0)
    history: list[float] = []
    matvecs = 0
    low_solves = 0
    invariant = q @ x
    solve_start = time.perf_counter()
    for _ in range(max_iterations + 1):
        residual = b - ah @ x
        matvecs += 1
        norm = float(np.linalg.norm(residual))
        history.append(norm)
        if norm <= atol + rtol * scale:
            return IterationResult(
                x,
                tuple(history),
                len(history) - 1,
                matvecs,
                True,
                norm,
                setup_seconds,
                time.perf_counter() - solve_start,
                low_solves,
                int(projector.nbytes),
            )
        if len(history) > max_iterations:
            break
        x = x + float(omega) * (projector @ residual)
        low_solves += 1
        drift = float(np.linalg.norm(q @ x - invariant, ord=np.inf))
        if drift > 5e-10 * max(1.0, float(np.linalg.norm(invariant, ord=np.inf))):
            raise ArithmeticError(f"conservation drift {drift:.3e}")
    return IterationResult(
        x,
        tuple(history),
        max_iterations,
        matvecs,
        False,
        history[-1],
        setup_seconds,
        time.perf_counter() - solve_start,
        low_solves,
        int(projector.nbytes),
    )


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
    setup_start = time.perf_counter()
    lu, piv = linalg.lu_factor(al)
    setup_seconds = time.perf_counter() - setup_start
    scale = max(float(np.linalg.norm(b)), 1.0)
    history: list[float] = []
    matvecs = 0
    low_solves = 0
    solve_start = time.perf_counter()
    for _ in range(max_iterations + 1):
        residual = b - ah @ x
        matvecs += 1
        norm = float(np.linalg.norm(residual))
        history.append(norm)
        if norm <= atol + rtol * scale:
            return IterationResult(
                x,
                tuple(history),
                len(history) - 1,
                matvecs,
                True,
                norm,
                setup_seconds,
                time.perf_counter() - solve_start,
                low_solves,
                int(lu.nbytes + piv.nbytes),
            )
        if len(history) > max_iterations:
            break
        correction = linalg.lu_solve((lu, piv), residual)
        low_solves += 1
        x = x + float(omega) * correction
    return IterationResult(
        x,
        tuple(history),
        max_iterations,
        matvecs,
        False,
        history[-1],
        setup_seconds,
        time.perf_counter() - solve_start,
        low_solves,
        int(lu.nbytes + piv.nbytes),
    )


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
    """GMRES using ``A_L`` only as a cached left preconditioner.

    The returned final residual is recomputed in the original high-order
    system, so a preconditioned callback norm cannot hide a bad fixed point.
    Setup and solve time, low solves, and factor storage are recorded
    separately.
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
    setup_seconds = 0.0
    low_solves = 0
    preconditioner_bytes = 0
    if low_order is not None:
        al = _matrix(low_order, "low_order")
        if al.shape != ah.shape:
            raise ValueError("matrix shapes differ")
        setup_start = time.perf_counter()
        lu, piv = linalg.lu_factor(al)
        setup_seconds = time.perf_counter() - setup_start
        preconditioner_bytes = int(lu.nbytes + piv.nbytes)

        def precondition(v: FloatArray) -> FloatArray:
            nonlocal low_solves
            low_solves += 1
            return linalg.lu_solve((lu, piv), v)

        preconditioner = LinearOperator(al.shape, matvec=precondition, dtype=float)

    callback_count = 0

    def callback(_value: object) -> None:
        nonlocal callback_count
        callback_count += 1

    solve_start = time.perf_counter()
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
    solve_seconds = time.perf_counter() - solve_start
    solution = np.asarray(solution, dtype=float)
    final = float(np.linalg.norm(b - ah @ solution))
    matvecs += 1
    scale = max(float(np.linalg.norm(b)), 1.0)
    converged = bool(info == 0 and final <= atol + rtol * scale * 5.0)
    initial_residual = float(
        np.linalg.norm(b - ah @ (np.zeros_like(b) if x0 is None else x0))
    )
    return IterationResult(
        solution,
        (initial_residual, final),
        callback_count,
        matvecs,
        converged,
        final,
        setup_seconds,
        solve_seconds,
        low_solves,
        preconditioner_bytes,
    )
