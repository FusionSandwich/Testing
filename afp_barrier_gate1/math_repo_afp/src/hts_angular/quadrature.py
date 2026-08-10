"""Positive spherical quadrature as a finite moment-cone problem."""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Callable, Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.linalg import null_space
from scipy.optimize import Bounds, LinearConstraint, least_squares, linprog, lsq_linear, milp
from scipy.special import sph_harm_y

FloatArray = NDArray[np.float64]


def normalize_nodes(nodes: ArrayLike) -> FloatArray:
    points = np.asarray(nodes, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("sphere nodes must have shape (N,3)")
    lengths = np.linalg.norm(points, axis=1)
    if np.any(lengths <= 0.0) or np.any(~np.isfinite(points)):
        raise ValueError("sphere nodes must be finite and nonzero")
    return points / lengths[:, None]


@dataclass(frozen=True)
class PositiveQuadrature:
    nodes: FloatArray
    weights: FloatArray
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        nodes = normalize_nodes(self.nodes)
        weights = np.asarray(self.weights, dtype=float).reshape(-1)
        if weights.shape != (nodes.shape[0],) or np.any(~np.isfinite(weights)):
            raise ValueError("weights have the wrong shape or nonfinite entries")
        if np.any(weights <= 0.0):
            raise ValueError("quadrature support weights must be strictly positive")
        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "metadata", dict(self.metadata))

    @property
    def n_node(self) -> int:
        return int(self.weights.size)

    @property
    def total_mass(self) -> float:
        return float(np.sum(self.weights))

    def integrate(self, values: ArrayLike) -> FloatArray:
        f = np.asarray(values, dtype=float)
        if f.shape[-1] != self.n_node:
            raise ValueError("last value dimension must equal the node count")
        return np.tensordot(f, self.weights, axes=([-1], [0]))


def fibonacci_sphere(n: int, phase: float = 0.5) -> PositiveQuadrature:
    if n < 1:
        raise ValueError("n must be positive")
    k = np.arange(n, dtype=float)
    z = 1.0 - 2.0 * (k + phase) / n
    golden = np.pi * (3.0 - np.sqrt(5.0))
    phi = golden * k
    radius = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    nodes = np.column_stack([radius * np.cos(phi), radius * np.sin(phi), z])
    return PositiveQuadrature(nodes, np.full(n, 4.0 * np.pi / n), {"family": "Fibonacci", "phase": phase})


def gauss_legendre_product_sphere(n_polar: int, n_azimuth: int, phase: float = 0.0) -> PositiveQuadrature:
    if n_polar < 1 or n_azimuth < 1:
        raise ValueError("orders must be positive")
    z, wz = np.polynomial.legendre.leggauss(n_polar)
    phi = 2.0 * np.pi * (np.arange(n_azimuth) + phase) / n_azimuth
    nodes, weights = [], []
    for zi, wi in zip(z, wz, strict=True):
        radius = np.sqrt(max(0.0, 1.0 - zi * zi))
        for angle in phi:
            nodes.append([radius * np.cos(angle), radius * np.sin(angle), zi])
            weights.append(wi * 2.0 * np.pi / n_azimuth)
    return PositiveQuadrature(np.asarray(nodes), np.asarray(weights), {"family": "Gauss-Legendre product"})


def spherical_coordinates(nodes: ArrayLike) -> tuple[FloatArray, FloatArray]:
    points = normalize_nodes(nodes)
    polar = np.arccos(np.clip(points[:, 2], -1.0, 1.0))
    azimuth = np.mod(np.arctan2(points[:, 1], points[:, 0]), 2.0 * np.pi)
    return polar, azimuth


def real_spherical_harmonics(nodes: ArrayLike, maximum_degree: int) -> tuple[FloatArray, tuple[tuple[int, int], ...]]:
    """Orthonormal real spherical harmonics, returned as ``(K,N)``."""
    if maximum_degree < 0:
        raise ValueError("maximum_degree must be nonnegative")
    polar, azimuth = spherical_coordinates(nodes)
    rows, labels = [], []
    for ell in range(maximum_degree + 1):
        for m in range(-ell, ell + 1):
            if m < 0:
                complex_y = sph_harm_y(ell, -m, polar, azimuth)
                row = np.sqrt(2.0) * ((-1) ** m) * complex_y.imag
            elif m == 0:
                row = sph_harm_y(ell, 0, polar, azimuth).real
            else:
                complex_y = sph_harm_y(ell, m, polar, azimuth)
                row = np.sqrt(2.0) * ((-1) ** m) * complex_y.real
            rows.append(np.asarray(row, dtype=float))
            labels.append((ell, m))
    return np.vstack(rows), tuple(labels)


def exact_surface_harmonic_moments(maximum_degree: int) -> FloatArray:
    out = np.zeros((maximum_degree + 1) ** 2)
    out[0] = np.sqrt(4.0 * np.pi)
    return out


def balanced_multiresponse_density(
    forward: ArrayLike,
    adjoints: ArrayLike,
    base_weights: ArrayLike,
    alpha: float = 0.85,
    power: float = 1.0,
    floor_fraction: float = 1e-12,
) -> FloatArray:
    """Construct a non-dominating response-weighted probability density.

    Every response contribution is normalized by its own weighted integral
    before averaging, so one large-magnitude response cannot dominate.
    """
    f = np.asarray(forward, dtype=float).reshape(-1)
    z = np.asarray(adjoints, dtype=float)
    if z.ndim == 1:
        z = z[None, :]
    w = np.asarray(base_weights, dtype=float).reshape(-1)
    if z.shape[1] != f.size or w.shape != f.shape or np.any(w <= 0.0):
        raise ValueError("forward, adjoints, and positive weights must align")
    if not 0.0 <= alpha < 1.0 or power <= 0.0:
        raise ValueError("alpha must be in [0,1) and power positive")
    terms = np.abs(z * f[None, :]) ** power
    normalizers = terms @ w
    normalized = np.divide(terms, normalizers[:, None], out=np.zeros_like(terms), where=normalizers[:, None] > 0.0)
    response_density = normalized.mean(axis=0) if normalized.shape[0] else np.zeros_like(f)
    uniform = np.full_like(f, 1.0 / np.sum(w))
    density = (1.0 - alpha) * uniform + alpha * response_density
    density = np.maximum(density, floor_fraction / np.sum(w))
    density /= density @ w
    return density


def _validate_moments(feature_matrix: ArrayLike, target: ArrayLike) -> tuple[FloatArray, FloatArray]:
    A = np.asarray(feature_matrix, dtype=float)
    b = np.asarray(target, dtype=float).reshape(-1)
    if A.ndim != 2 or b.shape != (A.shape[0],):
        raise ValueError("feature matrix must be KxN and target must have K entries")
    if np.any(~np.isfinite(A)) or np.any(~np.isfinite(b)):
        raise ValueError("moment data must be finite")
    return A, b


def caratheodory_support_reduction(
    nodes: ArrayLike,
    weights: ArrayLike,
    feature_matrix: ArrayLike,
    tolerance: float = 1e-12,
) -> PositiveQuadrature:
    """Reduce an already exact positive rule to at most ``rank(A)`` nodes."""
    points = normalize_nodes(nodes)
    w = np.asarray(weights, dtype=float).reshape(-1).copy()
    A = np.asarray(feature_matrix, dtype=float)
    if A.shape[1] != w.size or points.shape[0] != w.size or np.any(w < 0.0):
        raise ValueError("input rule and feature matrix do not align")
    active = np.flatnonzero(w > tolerance)
    rank = np.linalg.matrix_rank(A[:, active], tol=tolerance)
    while active.size > rank:
        Z = null_space(A[:, active])
        if Z.size == 0:
            break
        z = Z[:, 0]
        positive = z > tolerance
        negative = z < -tolerance
        candidates: list[tuple[float, int]] = []
        if np.any(positive):
            theta = np.min(w[active[positive]] / z[positive])
            candidates.append((theta, -1))  # w - theta z
        if np.any(negative):
            theta = np.min(w[active[negative]] / (-z[negative]))
            candidates.append((theta, +1))  # w + theta z
        if not candidates:
            break
        theta, sign = min(candidates, key=lambda pair: pair[0])
        w[active] += sign * theta * z
        w[np.abs(w) <= tolerance] = 0.0
        if np.any(w < -100 * tolerance):
            raise RuntimeError("support-reduction step lost positivity")
        w = np.maximum(w, 0.0)
        active = np.flatnonzero(w > tolerance)
        rank = np.linalg.matrix_rank(A[:, active], tol=tolerance)
    return PositiveQuadrature(points[active], w[active], {"construction": "Caratheodory support reduction", "rank": int(rank)})


@dataclass(frozen=True)
class MomentFitResult:
    quadrature: PositiveQuadrature | None
    residual: FloatArray
    residual_norm: float
    exact: bool
    status: str
    full_weights: FloatArray


def finite_pool_positive_quadrature(
    nodes: ArrayLike,
    feature_matrix: ArrayLike,
    target: ArrayLike,
    tolerance: float = 1e-9,
    objective: ArrayLike | None = None,
) -> MomentFitResult:
    points = normalize_nodes(nodes)
    A, b = _validate_moments(feature_matrix, target)
    if A.shape[1] != points.shape[0]:
        raise ValueError("feature columns must correspond to nodes")
    if objective is None:
        # A deterministic, tiny generic objective encourages a basic sparse
        # solution without materially changing feasibility.
        c = np.linspace(0.0, 1.0, points.shape[0]) * 1e-12
    else:
        c = np.asarray(objective, dtype=float).reshape(-1)
        if c.shape != (points.shape[0],):
            raise ValueError("objective has the wrong length")
    result = linprog(c, A_eq=A, b_eq=b, bounds=(0.0, None), method="highs")
    if not result.success:
        return MomentFitResult(None, np.full_like(b, np.nan), math.inf, False, result.message, np.zeros(points.shape[0]))
    weights = np.maximum(np.asarray(result.x, dtype=float), 0.0)
    threshold = max(tolerance * 1e-3, 1e-13)
    active = weights > threshold
    # A basic LP solution is sparse, but HiGHS can leave tiny numerical weights.
    # Add discarded entries back in descending order until the *returned* rule,
    # rather than the unfiltered vector, satisfies the requested tolerance.
    omitted = np.flatnonzero(~active & (weights > 0.0))
    if np.any(active):
        sparse_residual = A[:, active] @ weights[active] - b
        for index in omitted[np.argsort(weights[omitted])[::-1]]:
            if np.linalg.norm(sparse_residual, ord=np.inf) <= tolerance:
                break
            active[index] = True
            sparse_residual = A[:, active] @ weights[active] - b
    else:
        sparse_residual = -b.copy()
    quadrature = None
    if np.any(active):
        quadrature = PositiveQuadrature(
            points[active],
            weights[active],
            {
                "construction": "finite-pool positive moment LP",
                "support": int(np.count_nonzero(active)),
            },
        )
    residual = sparse_residual
    exact = bool(quadrature is not None and np.linalg.norm(residual, ord=np.inf) <= tolerance)
    return MomentFitResult(
        quadrature,
        residual,
        float(np.linalg.norm(residual)),
        exact,
        result.message,
        weights,
    )


@dataclass(frozen=True)
class MinimumResidualResult:
    weights: FloatArray
    residual: FloatArray
    residual_norm: float
    kkt_dual: FloatArray
    dual_feasibility_violation: float
    complementarity: float
    dual_lower_bound: float
    primal_dual_gap: float
    dual_certified: bool
    active_count: int


def minimum_residual_positive_weights(
    feature_matrix: ArrayLike,
    target: ArrayLike,
    tolerance: float = 1e-12,
) -> MinimumResidualResult:
    A, b = _validate_moments(feature_matrix, target)
    result = lsq_linear(A, b, bounds=(0.0, np.inf), tol=tolerance, lsmr_tol=tolerance, max_iter=10000)
    w = np.maximum(result.x, 0.0)
    residual = A @ w - b
    dual = residual.copy()
    Atdual = A.T @ dual
    violation = float(max(0.0, -np.min(Atdual, initial=0.0)))
    complementarity = float(np.max(np.abs(w * Atdual), initial=0.0))
    norm_dual = float(np.linalg.norm(dual))
    primal = float(np.linalg.norm(residual))
    feasibility_scale = max(np.linalg.norm(A, 2) * norm_dual, np.finfo(float).tiny)
    dual_certified = bool(violation <= 1e-8 * feasibility_scale and complementarity <= 1e-8 * max(1.0, primal * np.linalg.norm(w)))
    # Near an exactly feasible rule the residual direction is dominated by
    # floating-point noise and must not be normalized into a spurious large
    # lower bound.  Otherwise the KKT residual is a rigorous separating
    # direction when its cone feasibility and complementarity are certified.
    exact_scale = 1e-11 * (1.0 + np.linalg.norm(b))
    if norm_dual == 0.0 or primal <= exact_scale or not dual_certified:
        lower = 0.0
    else:
        lower = min(primal, max(0.0, float(-b @ dual / norm_dual)))
    return MinimumResidualResult(
        weights=w,
        residual=residual,
        residual_norm=primal,
        kkt_dual=dual,
        dual_feasibility_violation=violation,
        complementarity=complementarity,
        dual_lower_bound=lower,
        primal_dual_gap=max(0.0, primal - lower),
        dual_certified=dual_certified and primal > exact_scale,
        active_count=int(np.count_nonzero(w > 1e-11)),
    )


@dataclass(frozen=True)
class FarkasCertificate:
    vector: FloatArray | None
    certified: bool
    minimum_cone_pairing: float
    target_pairing: float
    status: str


def farkas_infeasibility_certificate(feature_matrix: ArrayLike, target: ArrayLike, tolerance: float = 1e-10) -> FarkasCertificate:
    """Seek ``y`` with ``A.T y >= 0`` and ``b.T y <= -1``."""
    A, b = _validate_moments(feature_matrix, target)
    K = A.shape[0]
    inequalities = np.vstack([-A.T, b[None, :]])
    rhs = np.concatenate([np.zeros(A.shape[1]), [-1.0]])
    result = linprog(np.zeros(K), A_ub=inequalities, b_ub=rhs, bounds=[(None, None)] * K, method="highs")
    if not result.success:
        return FarkasCertificate(None, False, math.nan, math.nan, result.message)
    y = np.asarray(result.x)
    minimum = float(np.min(A.T @ y, initial=np.inf))
    pairing = float(b @ y)
    certified = minimum >= -tolerance and pairing < -tolerance
    return FarkasCertificate(y, certified, minimum, pairing, result.message)


def moment_conditioning(feature_matrix: ArrayLike, weights: ArrayLike | None = None) -> dict[str, float]:
    A = np.asarray(feature_matrix, dtype=float)
    if weights is not None:
        w = np.asarray(weights, dtype=float).reshape(-1)
        if w.shape != (A.shape[1],) or np.any(w <= 0.0):
            raise ValueError("weights must be positive and correspond to columns")
        A = A * np.sqrt(w)[None, :]
    singular = np.linalg.svd(A, compute_uv=False)
    positive = singular[singular > np.finfo(float).eps * max(A.shape) * singular[0]] if singular.size else singular
    return {
        "rank": float(positive.size),
        "sigma_max": float(singular[0]) if singular.size else 0.0,
        "sigma_min_nonzero": float(positive[-1]) if positive.size else 0.0,
        "condition_nonzero": float(positive[0] / positive[-1]) if positive.size else math.inf,
    }


def nonlinear_refine_quadrature(
    initial: PositiveQuadrature,
    feature_function: Callable[[FloatArray], FloatArray],
    target: ArrayLike,
    separation_weight: float = 1e-5,
    maximum_evaluations: int = 4000,
) -> PositiveQuadrature:
    """Refine nodes and positive weights using angular coordinates and softmax.

    This is a local nonlinear refinement, not the existence certificate.  The
    finite-pool LP should be used before and after it for certification.
    """
    target_vec = np.asarray(target, dtype=float).reshape(-1)
    polar, azimuth = spherical_coordinates(initial.nodes)
    logits = np.log(initial.weights / np.sum(initial.weights))
    x0 = np.concatenate([polar, azimuth, logits])
    n = initial.n_node
    total = initial.total_mass

    def unpack(x: FloatArray) -> tuple[FloatArray, FloatArray]:
        th = x[:n]
        ph = x[n : 2 * n]
        r = np.sin(th)
        nodes = np.column_stack([r * np.cos(ph), r * np.sin(ph), np.cos(th)])
        q = x[2 * n :]
        q = q - np.max(q)
        weights = total * np.exp(q) / np.sum(np.exp(q))
        return nodes, weights

    def residual(x: FloatArray) -> FloatArray:
        nodes, weights = unpack(x)
        F = np.asarray(feature_function(nodes), dtype=float)
        moment = F @ weights - target_vec
        if separation_weight <= 0.0 or n < 2:
            return moment
        dots = nodes @ nodes.T
        upper = dots[np.triu_indices(n, 1)]
        # Penalize only near-coincident nodes (dot > 0.95).
        sep = np.sqrt(separation_weight) * np.maximum(upper - 0.95, 0.0)
        return np.concatenate([moment, sep])

    result = least_squares(residual, x0, max_nfev=maximum_evaluations, xtol=1e-13, ftol=1e-13, gtol=1e-13)
    nodes, weights = unpack(result.x)
    return PositiveQuadrature(nodes, weights, {**initial.metadata, "nonlinear_refined": bool(result.success), "cost": float(result.cost)})


def node_count_bounds(maximum_harmonic_degree: int, feature_dimension: int) -> dict[str, int]:
    """General Tchakaloff upper bound and a harmonic product-space lower bound."""
    if maximum_harmonic_degree < 0 or feature_dimension < 1:
        raise ValueError("invalid dimensions")
    half_dimension = (maximum_harmonic_degree // 2 + 1) ** 2
    return {"tchakaloff_upper": int(feature_dimension), "harmonic_gram_lower": int(half_dimension)}


@dataclass(frozen=True)
class ResponseMomentCertificate:
    """Certified response-error contribution from moment residuals.

    ``coefficients[m]`` contains the expansion coefficients of response
    integrand ``m`` in the constrained feature basis.  Any component outside
    that basis must be supplied separately through
    ``unresolved_integral_bounds``.
    """

    per_response_bound: FloatArray
    moment_contribution: FloatArray
    unresolved_contribution: FloatArray
    maximum_bound: float


def response_error_from_moment_residual(
    moment_residual: ArrayLike,
    response_coefficients: ArrayLike,
    unresolved_integral_bounds: ArrayLike | float = 0.0,
) -> ResponseMomentCertificate:
    """Bound response errors induced by a certified quadrature moment defect.

    If ``g_m = sum_k c[m,k] f_k + r_m`` and the quadrature moment residual is
    ``delta_k``, then

    ``|I(g_m)-Q(g_m)| <= |c_m dot delta| + |I(r_m)-Q(r_m)|``.

    The second term is supplied as a nonnegative externally justified bound.
    """

    residual = np.asarray(moment_residual, dtype=float).reshape(-1)
    coefficients = np.asarray(response_coefficients, dtype=float)
    if coefficients.ndim == 1:
        coefficients = coefficients[None, :]
    if coefficients.ndim != 2 or coefficients.shape[1] != residual.size:
        raise ValueError("response_coefficients must have one column per moment")
    unresolved = np.asarray(unresolved_integral_bounds, dtype=float)
    if unresolved.ndim == 0:
        unresolved = np.full(coefficients.shape[0], float(unresolved))
    else:
        unresolved = unresolved.reshape(-1)
    if unresolved.shape != (coefficients.shape[0],):
        raise ValueError("one unresolved bound is required per response")
    if (
        np.any(~np.isfinite(residual))
        or np.any(~np.isfinite(coefficients))
        or np.any(~np.isfinite(unresolved))
        or np.any(unresolved < 0.0)
    ):
        raise ValueError("certificate inputs must be finite and bounds nonnegative")
    moment = np.abs(coefficients @ residual)
    total = moment + unresolved
    return ResponseMomentCertificate(
        per_response_bound=total,
        moment_contribution=moment,
        unresolved_contribution=unresolved,
        maximum_bound=float(np.max(total, initial=0.0)),
    )


def finite_pool_symmetric_quadrature(
    nodes: ArrayLike,
    feature_matrix: ArrayLike,
    target: ArrayLike,
    orbits: Sequence[Sequence[int]],
    tolerance: float = 1e-9,
    objective: ArrayLike | None = None,
) -> MomentFitResult:
    """Fit a positive rule with exactly equal weights within symmetry orbits.

    The orbit constraints are imposed before the LP: one nonnegative variable
    is used for the common per-node weight of each orbit.  Therefore any
    returned rule satisfies the requested symmetry exactly up to floating-point
    representation, rather than through a post-hoc average that could destroy
    moment exactness.
    """

    points = normalize_nodes(nodes)
    A, b = _validate_moments(feature_matrix, target)
    if A.shape[1] != points.shape[0]:
        raise ValueError("feature columns must correspond to nodes")
    normalized_orbits: list[np.ndarray] = []
    seen: set[int] = set()
    for orbit in orbits:
        indices = np.asarray(tuple(orbit), dtype=int).reshape(-1)
        if indices.size == 0 or np.any(indices < 0) or np.any(indices >= points.shape[0]):
            raise ValueError("every orbit must contain valid node indices")
        if np.unique(indices).size != indices.size or any(int(i) in seen for i in indices):
            raise ValueError("symmetry orbits must be disjoint")
        seen.update(int(i) for i in indices)
        normalized_orbits.append(indices)
    if seen != set(range(points.shape[0])):
        raise ValueError("symmetry orbits must partition the candidate pool")
    orbit_matrix = np.column_stack([np.sum(A[:, orbit], axis=1) for orbit in normalized_orbits])
    if objective is None:
        c = np.linspace(0.0, 1.0, len(normalized_orbits)) * 1e-12
    else:
        c = np.asarray(objective, dtype=float).reshape(-1)
        if c.shape != (len(normalized_orbits),):
            raise ValueError("objective must have one entry per orbit")
    result = linprog(c, A_eq=orbit_matrix, b_eq=b, bounds=(0.0, None), method="highs")
    if not result.success:
        return MomentFitResult(
            None,
            np.full_like(b, np.nan),
            math.inf,
            False,
            result.message,
            np.zeros(points.shape[0]),
        )
    orbit_weights = np.maximum(np.asarray(result.x, dtype=float), 0.0)
    full = np.zeros(points.shape[0], dtype=float)
    for value, orbit in zip(orbit_weights, normalized_orbits, strict=True):
        full[orbit] = value
    active = full > max(tolerance * 1e-3, 1e-13)
    residual = A[:, active] @ full[active] - b if np.any(active) else -b.copy()
    exact = bool(np.any(active) and np.linalg.norm(residual, ord=np.inf) <= tolerance)
    quadrature = (
        PositiveQuadrature(
            points[active],
            full[active],
            {
                "construction": "finite-pool positive orbit LP",
                "active_orbits": int(np.count_nonzero(orbit_weights > 0.0)),
                "support": int(np.count_nonzero(active)),
            },
        )
        if exact
        else None
    )
    return MomentFitResult(
        quadrature,
        residual,
        float(np.linalg.norm(residual)),
        exact,
        result.message,
        full,
    )


def _weight_upper_bounds(A: FloatArray, b: FloatArray) -> FloatArray:
    """Derive finite valid weight bounds from a sign-definite moment row."""

    candidates: list[FloatArray] = []
    for row, target_value in zip(A, b, strict=True):
        if target_value > 0.0 and np.all(row > 0.0):
            candidates.append(target_value / row)
        elif target_value < 0.0 and np.all(row < 0.0):
            candidates.append(target_value / row)
    if not candidates:
        raise ValueError(
            "minimum-node MILP needs max_weight or a sign-definite normalization moment"
        )
    stacked = np.vstack(candidates)
    return np.min(stacked, axis=0) * (1.0 + 1e-12)


def minimum_node_positive_quadrature(
    nodes: ArrayLike,
    feature_matrix: ArrayLike,
    target: ArrayLike,
    tolerance: float = 1e-9,
    max_weight: ArrayLike | float | None = None,
    time_limit: float | None = None,
) -> MomentFitResult:
    """Certify a minimum-support positive rule on a fixed candidate pool.

    This mixed-integer formulation minimizes the number of active candidate
    nodes.  It is a *fixed-pool* minimum, not a global variable-node lower
    bound.  The returned continuous weights are recertified by an LP restricted
    to the selected support.
    """

    points = normalize_nodes(nodes)
    A, b = _validate_moments(feature_matrix, target)
    if A.shape[1] != points.shape[0]:
        raise ValueError("feature columns must correspond to nodes")
    n = points.shape[0]
    if max_weight is None:
        upper = _weight_upper_bounds(A, b)
    else:
        value = np.asarray(max_weight, dtype=float)
        if value.ndim == 0:
            upper = np.full(n, float(value))
        else:
            upper = value.reshape(-1)
        if upper.shape != (n,) or np.any(~np.isfinite(upper)) or np.any(upper <= 0.0):
            raise ValueError("max_weight must be finite and positive")
    objective = np.concatenate([np.zeros(n), np.ones(n)])
    integrality = np.concatenate([np.zeros(n, dtype=int), np.ones(n, dtype=int)])
    lower_bounds = np.zeros(2 * n)
    upper_bounds = np.concatenate([upper, np.ones(n)])
    equality = LinearConstraint(
        np.hstack([A, np.zeros((A.shape[0], n))]), b, b
    )
    linking = LinearConstraint(
        np.hstack([np.eye(n), -np.diag(upper)]),
        -np.full(n, np.inf),
        np.zeros(n),
    )
    options: dict[str, float] = {}
    if time_limit is not None:
        if not np.isfinite(time_limit) or time_limit <= 0.0:
            raise ValueError("time_limit must be finite and positive")
        options["time_limit"] = float(time_limit)
    result = milp(
        c=objective,
        integrality=integrality,
        bounds=Bounds(lower_bounds, upper_bounds),
        constraints=[equality, linking],
        options=options or None,
    )
    if not result.success or result.x is None:
        return MomentFitResult(
            None,
            np.full_like(b, np.nan),
            math.inf,
            False,
            result.message,
            np.zeros(n),
        )
    selected = np.asarray(result.x[n:] > 0.5)
    if not np.any(selected):
        return MomentFitResult(None, -b.copy(), float(np.linalg.norm(b)), False, result.message, np.zeros(n))
    # Re-solve continuously on the certified support to remove MILP feasibility
    # tolerances and obtain a high-accuracy moment certificate.
    restricted = finite_pool_positive_quadrature(
        points[selected], A[:, selected], b, tolerance=tolerance
    )
    full = np.zeros(n)
    if restricted.quadrature is None:
        return MomentFitResult(
            None,
            restricted.residual,
            restricted.residual_norm,
            False,
            f"MILP selected {int(np.count_nonzero(selected))} nodes; LP recertification failed: {restricted.status}",
            full,
        )
    selected_indices = np.flatnonzero(selected)
    # The restricted LP can prune additional numerical-zero columns.  Match its
    # nodes back to the selected pool deterministically.
    used = np.zeros(selected_indices.size, dtype=bool)
    for node, weight in zip(
        restricted.quadrature.nodes, restricted.quadrature.weights, strict=True
    ):
        distances = np.linalg.norm(points[selected] - node[None, :], axis=1)
        distances[used] = np.inf
        local = int(np.argmin(distances))
        if distances[local] > 1e-10:
            raise RuntimeError("failed to map recertified MILP support to candidate nodes")
        full[selected_indices[local]] = weight
        used[local] = True
    active = full > 0.0
    residual = A[:, active] @ full[active] - b
    exact = bool(np.linalg.norm(residual, ord=np.inf) <= tolerance)
    quadrature = PositiveQuadrature(
        points[active],
        full[active],
        {
            "construction": "minimum-support fixed-pool MILP plus LP recertification",
            "minimum_fixed_pool_support": int(np.count_nonzero(selected)),
            "returned_support": int(np.count_nonzero(active)),
            "milp_objective": float(result.fun),
        },
    )
    return MomentFitResult(
        quadrature,
        residual,
        float(np.linalg.norm(residual)),
        exact,
        result.message,
        full,
    )
