"""Variable-node positive spherical quadrature and node-count certificates."""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .quadrature import (
    MomentFitResult,
    PositiveQuadrature,
    exact_surface_harmonic_moments,
    fibonacci_sphere,
    minimum_node_positive_quadrature,
    nonlinear_refine_quadrature,
    real_spherical_harmonics,
    normalize_nodes,
)

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class NodeCountCertificate:
    maximum_degree: int
    node_count: int
    harmonic_gram_lower_bound: int
    exact: bool
    globally_node_minimal: bool
    certificate_type: str
    residual_inf: float
    message: str


@dataclass(frozen=True)
class VariableNodeQuadratureResult:
    quadrature: PositiveQuadrature | None
    exact: bool
    residual: FloatArray
    residual_inf: float
    starts_attempted: int
    best_start: int | None
    minimum_weight: float
    minimum_separation_radians: float
    certificate: NodeCountCertificate


@dataclass(frozen=True)
class FixedPoolMinimumCertificate:
    fit: MomentFitResult
    candidate_count: int
    support: int | None
    exact: bool
    fixed_pool_minimal: bool
    message: str


def harmonic_gram_lower_bound(maximum_degree: int) -> int:
    """Positive-rule lower bound from injectivity on harmonics of half degree.

    If a positive rule is exact through degree ``t``, then evaluation on the
    spherical-harmonic space through degree ``floor(t/2)`` is injective, since
    the squared magnitude of any member lies in the exact product space.
    Therefore ``N >= (floor(t/2)+1)^2`` on :math:`S^2`.
    """
    if int(maximum_degree) != maximum_degree or maximum_degree < 0:
        raise ValueError("maximum_degree must be a nonnegative integer")
    q = int(maximum_degree) // 2
    return (q + 1) ** 2


def regular_tetrahedron_rule() -> PositiveQuadrature:
    nodes = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ]
    ) / math.sqrt(3.0)
    return PositiveQuadrature(nodes, np.full(4, np.pi), {"family": "regular tetrahedron", "degree": 2})


def minimum_separation(nodes: ArrayLike) -> float:
    points = normalize_nodes(nodes)
    if points.shape[0] < 2:
        return math.inf
    dots = np.clip(points @ points.T, -1.0, 1.0)
    np.fill_diagonal(dots, -1.0)
    return float(np.min(np.arccos(np.max(dots, axis=1))))


def node_count_certificate(
    quadrature: PositiveQuadrature,
    maximum_degree: int,
    *,
    tolerance: float = 1e-10,
) -> NodeCountCertificate:
    features, _labels = real_spherical_harmonics(quadrature.nodes, maximum_degree)
    target = exact_surface_harmonic_moments(maximum_degree)
    residual = features @ quadrature.weights - target
    residual_inf = float(np.linalg.norm(residual, ord=np.inf))
    exact = bool(residual_inf <= tolerance)
    lower = harmonic_gram_lower_bound(maximum_degree)
    global_minimal = bool(exact and quadrature.n_node == lower)
    if global_minimal:
        kind = "analytic harmonic-Gram lower bound attained"
        message = f"exact positive rule attains N >= {lower}"
    elif exact:
        kind = "exact construction without matching global lower bound"
        message = f"exact rule uses {quadrature.n_node} nodes; certified lower bound is {lower}"
    else:
        kind = "failed exactness"
        message = f"moment residual {residual_inf:.3e} exceeds tolerance {tolerance:.3e}"
    return NodeCountCertificate(
        maximum_degree=int(maximum_degree),
        node_count=quadrature.n_node,
        harmonic_gram_lower_bound=lower,
        exact=exact,
        globally_node_minimal=global_minimal,
        certificate_type=kind,
        residual_inf=residual_inf,
        message=message,
    )


def variable_node_positive_quadrature(
    maximum_degree: int,
    node_count: int,
    *,
    starts: int = 8,
    seed: int = 0,
    tolerance: float = 1e-10,
    separation_weight: float = 1e-6,
    maximum_evaluations: int = 8000,
) -> VariableNodeQuadratureResult:
    """Deterministic multistart variable-node construction.

    Multistart failure is not interpreted as a continuous infeasibility proof.
    A global node-minimality statement is issued only when an exact positive
    rule attains the analytic harmonic-Gram lower bound.
    """
    if int(node_count) != node_count or node_count < 1:
        raise ValueError("node_count must be a positive integer")
    if int(starts) != starts or starts < 1:
        raise ValueError("starts must be a positive integer")
    if int(seed) != seed:
        raise ValueError("seed must be an integer")
    if not np.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be finite and positive")
    if not np.isfinite(separation_weight) or separation_weight < 0.0:
        raise ValueError("separation_weight must be finite and nonnegative")
    if int(maximum_evaluations) != maximum_evaluations or maximum_evaluations < 1:
        raise ValueError("maximum_evaluations must be a positive integer")
    node_count, starts, seed, maximum_evaluations = (
        int(node_count), int(starts), int(seed), int(maximum_evaluations)
    )
    target = exact_surface_harmonic_moments(maximum_degree)

    def features(nodes: FloatArray) -> FloatArray:
        return real_spherical_harmonics(nodes, maximum_degree)[0]

    initial_rules: list[PositiveQuadrature] = []
    if node_count == 4 and maximum_degree <= 2:
        initial_rules.append(regular_tetrahedron_rule())
    rng = np.random.default_rng(seed)
    while len(initial_rules) < starts:
        phase = float((len(initial_rules) + 0.5) / starts)
        base = fibonacci_sphere(node_count, phase=phase)
        # Deterministic random orthogonal rotations avoid repeatedly optimizing
        # the same azimuthal phase while preserving positivity and mass.
        matrix = rng.normal(size=(3, 3))
        q, _ = np.linalg.qr(matrix)
        if np.linalg.det(q) < 0.0:
            q[:, 0] *= -1.0
        initial_rules.append(PositiveQuadrature(base.nodes @ q, base.weights, {**base.metadata, "start": len(initial_rules)}))
    best_rule: PositiveQuadrature | None = None
    best_residual: FloatArray | None = None
    best_inf = math.inf
    best_start: int | None = None
    for index, initial in enumerate(initial_rules[:starts]):
        if maximum_degree <= 2 and initial.metadata.get("family") == "regular tetrahedron":
            refined = initial
        else:
            refined = nonlinear_refine_quadrature(
                initial,
                features,
                target,
                separation_weight=separation_weight,
                maximum_evaluations=maximum_evaluations,
            )
        residual = features(refined.nodes) @ refined.weights - target
        norm = float(np.linalg.norm(residual, ord=np.inf))
        if norm < best_inf:
            best_rule, best_residual, best_inf, best_start = refined, residual, norm, index
    assert best_residual is not None
    exact = bool(best_rule is not None and best_inf <= tolerance and np.min(best_rule.weights) > 0.0)
    if best_rule is None:
        placeholder = PositiveQuadrature(np.array([[0.0, 0.0, 1.0]]), np.array([4.0 * np.pi]))
        certificate = node_count_certificate(placeholder, maximum_degree, tolerance=tolerance)
        minimum_weight = math.nan
        separation = math.nan
    else:
        certificate = node_count_certificate(best_rule, maximum_degree, tolerance=tolerance)
        minimum_weight = float(np.min(best_rule.weights))
        separation = minimum_separation(best_rule.nodes)
    return VariableNodeQuadratureResult(
        quadrature=best_rule if exact else None,
        exact=exact,
        residual=best_residual,
        residual_inf=best_inf,
        starts_attempted=starts,
        best_start=best_start,
        minimum_weight=minimum_weight,
        minimum_separation_radians=separation,
        certificate=certificate,
    )


def candidate_pool_minimum_certificate(
    nodes: ArrayLike,
    maximum_degree: int,
    *,
    tolerance: float = 1e-9,
    time_limit: float | None = None,
) -> FixedPoolMinimumCertificate:
    points = np.asarray(nodes, dtype=float)
    features, _labels = real_spherical_harmonics(points, maximum_degree)
    target = exact_surface_harmonic_moments(maximum_degree)
    fit = minimum_node_positive_quadrature(
        points,
        features,
        target,
        tolerance=tolerance,
        time_limit=time_limit,
    )
    support = fit.quadrature.n_node if fit.quadrature is not None else None
    exact = bool(fit.exact and fit.quadrature is not None)
    return FixedPoolMinimumCertificate(
        fit=fit,
        candidate_count=points.shape[0],
        support=support,
        exact=exact,
        fixed_pool_minimal=exact,
        message=(
            f"minimum support on the supplied {points.shape[0]}-node pool is {support}"
            if exact
            else f"fixed-pool certification failed: {fit.status}"
        ),
    )


__all__ = [
    "FixedPoolMinimumCertificate",
    "NodeCountCertificate",
    "VariableNodeQuadratureResult",
    "candidate_pool_minimum_certificate",
    "harmonic_gram_lower_bound",
    "minimum_separation",
    "node_count_certificate",
    "regular_tetrahedron_rule",
    "variable_node_positive_quadrature",
]
