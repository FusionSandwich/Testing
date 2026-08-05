"""Deterministic positive-mass node families and permitted graph builders."""

from __future__ import annotations

from itertools import permutations, product
import math
from typing import Iterable, Sequence

import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.typing import ArrayLike, NDArray
from scipy.spatial import ConvexHull, QhullError

from pure_math.optimization import real_harmonic_samples

from .types import FamilyDescriptor, QuadratureCandidate

FloatArray = NDArray[np.float64]


FAMILY_DESCRIPTORS: tuple[FamilyDescriptor, ...] = (
    FamilyDescriptor(
        "product",
        "Gauss--Legendre polar mass times uniform azimuth mass",
        ("grid", "weak_delaunay", "knn", "complete"),
        "audit the declared tensor-product polynomial/harmonic degree",
        "Gauss--Legendre weights are individually positive",
        "polar clustering and longitude seams can amplify ray effects",
    ),
    FamilyDescriptor(
        "level_symmetric",
        "positive tabulated orbit masses divided over each signed-permutation orbit",
        ("orbit_distance", "weak_delaunay", "complete"),
        "audit each imported rule and convention separately",
        "reject any nonpositive tabulated orbit mass",
        "a level-symmetric table is data, not an all-orders construction",
    ),
    FamilyDescriptor(
        "lebedev",
        "positive octahedral orbit masses divided over orbit nodes",
        ("orbit_distance", "weak_delaunay", "complete"),
        "exact/outward audit of the advertised degree for each rule",
        "admit individual rules only after a strict positivity audit",
        "not every rule/source may share the same normalization or positivity",
    ),
    FamilyDescriptor(
        "ahrens_beylkin",
        "icosahedral generator-orbit masses divided over orbit nodes",
        ("orbit_distance", "weak_delaunay", "complete"),
        "audit invariant-subspace exactness in the published convention",
        "Newton output is admitted only after an independent positive-mass audit",
        "rotational quadrature exactness does not prove generator feasibility",
    ),
    FamilyDescriptor(
        "spherical_design",
        "equal positive mass 1/N",
        ("weak_delaunay", "knn", "complete"),
        "exact moments through the declared design strength",
        "automatic for a nonempty equal-weight design",
        "design exactness alone does not solve shared-edge compatibility",
    ),
    FamilyDescriptor(
        "maximal_net",
        "positive Voronoi masses when certified; equal diagnostic masses otherwise",
        ("weak_delaunay", "radius", "knn", "complete"),
        "no polynomial exactness unless moment restoration is certified",
        "all computed cell masses must have outward-positive lower bounds",
        "deterministic greedy nets are quadrature candidates, not exact designs",
    ),
    FamilyDescriptor(
        "delaunay",
        "positive supplied or certified spherical-Voronoi masses",
        ("weak_delaunay", "complete"),
        "audit supplied moments and sampling rank",
        "reject zero/negative cells and duplicate nodes",
        "degenerate facets require the weak graph or an intrinsic tie rule",
    ),
    FamilyDescriptor(
        "locally_adapted",
        "positive surface masses with exact moment restoration",
        ("weak_delaunay_plus_certified_edges", "complete"),
        "recheck every moment and sampling-rank certificate after refinement",
        "reject the proposal if restoration loses positivity",
        "node insertion is not automatically generator-feasible",
    ),
)


def complete_edges(node_count: int) -> list[tuple[int, int]]:
    if node_count < 2:
        raise ValueError("complete graph needs at least two nodes")
    return [(i, j) for i in range(node_count) for j in range(i + 1, node_count)]


def knn_edges(nodes: ArrayLike, neighbors: int) -> list[tuple[int, int]]:
    x = np.asarray(nodes, dtype=float)
    if x.ndim != 2 or x.shape[1] != 3:
        raise ValueError("nodes must have shape (N,3)")
    if not 1 <= neighbors < len(x):
        raise ValueError("neighbors must lie in 1..N-1")
    gram = np.clip(x @ x.T, -1.0, 1.0)
    np.fill_diagonal(gram, -np.inf)
    edges: set[tuple[int, int]] = set()
    for i in range(len(x)):
        order = sorted(range(len(x)), key=lambda j: (-gram[i, j], j))
        for j in order[:neighbors]:
            edges.add((i, j) if i < j else (j, i))
    return sorted(edges)


def radius_edges(nodes: ArrayLike, radius: float) -> list[tuple[int, int]]:
    x = np.asarray(nodes, dtype=float)
    if not 0 < radius < math.pi:
        raise ValueError("geodesic radius must be in (0,pi)")
    threshold = math.cos(radius)
    return [
        (i, j)
        for i in range(len(x))
        for j in range(i + 1, len(x))
        if float(x[i] @ x[j]) >= threshold
    ]


def weak_delaunay_edges(
    nodes: ArrayLike, *, facet_tolerance: float = 2e-10
) -> list[tuple[int, int]]:
    """Return all pairs on every supporting convex-hull facet.

    Coplanar triangular pieces with the same supporting plane are grouped, so
    a degenerate spherical Delaunay face contributes all of its legal weak
    edges instead of a coordinate-dependent diagonal.
    """

    x = np.asarray(nodes, dtype=float)
    if not np.isfinite(facet_tolerance) or facet_tolerance <= 0:
        raise ValueError("facet_tolerance must be finite and positive")
    if x.ndim != 2 or x.shape[1] != 3:
        raise ValueError("nodes must have shape (N,3)")
    if len(x) < 4:
        return complete_edges(len(x))
    try:
        hull = ConvexHull(x)
    except QhullError as error:
        raise ValueError(
            "weak spherical Delaunay requires a full-dimensional node hull"
        ) from error
    groups: list[tuple[np.ndarray, float, set[int]]] = []
    for simplex, equation in zip(hull.simplices, hull.equations, strict=True):
        normal = np.asarray(equation[:3], dtype=float)
        offset = float(equation[3])
        norm = float(np.linalg.norm(normal))
        normal, offset = normal / norm, offset / norm
        matched = False
        for old_normal, old_offset, vertices in groups:
            if (
                np.linalg.norm(normal - old_normal) <= facet_tolerance
                and abs(offset - old_offset) <= facet_tolerance
            ):
                vertices.update(map(int, simplex))
                matched = True
                break
        if not matched:
            groups.append((normal, offset, set(map(int, simplex))))
    edges: set[tuple[int, int]] = set()
    for _, _, vertices in groups:
        ordered = sorted(vertices)
        edges.update(
            (ordered[a], ordered[b])
            for a in range(len(ordered))
            for b in range(a + 1, len(ordered))
        )
    return sorted(edges)


def product_rule(n_mu: int, n_phi: int, *, graph: str = "grid") -> QuadratureCandidate:
    if n_mu < 2 or n_phi < 3:
        raise ValueError("product rule requires n_mu>=2 and n_phi>=3")
    mu, polar_weight = leggauss(n_mu)
    nodes: list[list[float]] = []
    weights: list[float] = []
    for a in range(n_mu):
        radius = math.sqrt(max(0.0, 1.0 - float(mu[a]) ** 2))
        for b in range(n_phi):
            phi = 2.0 * math.pi * b / n_phi
            nodes.append([radius * math.cos(phi), radius * math.sin(phi), float(mu[a])])
            weights.append(float(polar_weight[a]) / (2.0 * n_phi))
    if graph == "grid":
        edges: set[tuple[int, int]] = set()
        for a in range(n_mu):
            for b in range(n_phi):
                i = a * n_phi + b
                j = a * n_phi + (b + 1) % n_phi
                edges.add((i, j) if i < j else (j, i))
                if a + 1 < n_mu:
                    edges.add((i, (a + 1) * n_phi + b))
        selected = sorted(edges)
    elif graph == "weak_delaunay":
        selected = weak_delaunay_edges(nodes)
    elif graph == "complete":
        selected = complete_edges(len(nodes))
    else:
        raise ValueError("unsupported product graph")
    return QuadratureCandidate.build(
        "product", nodes, weights, selected,
        metadata={"n_mu": n_mu, "n_phi": n_phi, "graph_rule": graph},
    )


def _signed_permutation_orbit(generator: ArrayLike) -> FloatArray:
    point = np.asarray(generator, dtype=float)
    point = point / np.linalg.norm(point)
    output: dict[tuple[float, float, float], np.ndarray] = {}
    for perm in permutations(range(3)):
        permuted = point[list(perm)]
        for signs in product((-1.0, 1.0), repeat=3):
            value = permuted * np.asarray(signs)
            key = tuple(float(v) for v in np.round(value, 14))
            output[key] = value
    return np.asarray([output[key] for key in sorted(output)])


def level_symmetric_from_orbits(
    generators: Sequence[ArrayLike],
    orbit_masses: Sequence[float],
    *,
    graph: str = "weak_delaunay",
) -> QuadratureCandidate:
    if len(generators) != len(orbit_masses) or not generators:
        raise ValueError("one positive mass is needed per generator orbit")
    if min(orbit_masses) <= 0 or abs(sum(orbit_masses) - 1.0) > 5e-12:
        raise ValueError("orbit masses must be positive and sum to one")
    nodes: list[np.ndarray] = []
    weights: list[float] = []
    orbit_sizes: list[int] = []
    for generator, mass in zip(generators, orbit_masses, strict=True):
        orbit = _signed_permutation_orbit(generator)
        orbit_sizes.append(len(orbit))
        nodes.extend(orbit)
        weights.extend([float(mass) / len(orbit)] * len(orbit))
    x = np.asarray(nodes)
    if graph == "weak_delaunay":
        selected = weak_delaunay_edges(x)
    elif graph == "complete":
        selected = complete_edges(len(x))
    else:
        raise ValueError("unsupported level-symmetric graph")
    return QuadratureCandidate.build(
        "level_symmetric", x, weights, selected,
        metadata={"orbit_sizes": orbit_sizes, "graph_rule": graph},
    )


def lebedev_6(*, graph: str = "weak_delaunay") -> QuadratureCandidate:
    nodes = np.vstack([np.eye(3), -np.eye(3)])
    if graph == "weak_delaunay":
        edges = weak_delaunay_edges(nodes)
    elif graph == "complete":
        edges = complete_edges(6)
    else:
        raise ValueError("unsupported Lebedev-6 graph")
    return QuadratureCandidate.build(
        "lebedev", nodes, np.full(6, 1.0 / 6.0), edges,
        metadata={
            "rule": "octahedral-6",
            "advertised_degree": 3,
            "exactness_certification": "EXACT_SYMPY_MONOMIAL_AUDIT",
            "graph_rule": graph,
        },
    )


def lebedev_14(*, graph: str = "weak_delaunay") -> QuadratureCandidate:
    axes = np.vstack([np.eye(3), -np.eye(3)])
    cube = np.asarray(list(product((-1.0, 1.0), repeat=3))) / math.sqrt(3.0)
    nodes = np.vstack([axes, cube])
    weights = np.concatenate([np.full(6, 1.0 / 15.0), np.full(8, 3.0 / 40.0)])
    if graph == "weak_delaunay":
        edges = weak_delaunay_edges(nodes)
    elif graph == "complete":
        edges = complete_edges(14)
    else:
        raise ValueError("unsupported Lebedev-14 graph")
    return QuadratureCandidate.build(
        "lebedev", nodes, weights, edges,
        metadata={
            "rule": "octahedral-14",
            "advertised_degree": 5,
            "exactness_certification": "EXACT_SYMPY_MONOMIAL_AUDIT",
            "graph_rule": graph,
        },
    )


def ahrens_beylkin_icosahedral_fixture(
    *, graph: str = "weak_delaunay"
) -> QuadratureCandidate:
    """The vertex orbit is an audit fixture, not the full AB rule generator."""

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    nodes = []
    for a, b in ((1.0, phi),):
        for s in (-1.0, 1.0):
            for t in (-1.0, 1.0):
                nodes.extend(([0.0, s * a, t * b], [s * a, t * b, 0.0], [t * b, 0.0, s * a]))
    x = np.asarray(nodes)
    x /= np.linalg.norm(x, axis=1)[:, None]
    if graph == "weak_delaunay":
        edges = weak_delaunay_edges(x)
    elif graph == "complete":
        edges = complete_edges(12)
    else:
        raise ValueError("unsupported icosahedral-fixture graph")
    return QuadratureCandidate.build(
        "ahrens_beylkin", x, np.full(12, 1.0 / 12.0), edges,
        metadata={"rule": "icosahedral-vertex-orbit-fixture", "graph_rule": graph},
    )


def spherical_design_candidate(
    nodes: ArrayLike,
    strength: int,
    *,
    graph: str = "weak_delaunay",
    moment_tolerance: float = 2e-11,
) -> QuadratureCandidate:
    x = np.asarray(nodes, dtype=float)
    if strength < 1:
        raise ValueError("design strength must be positive")
    if not np.isfinite(moment_tolerance) or moment_tolerance <= 0:
        raise ValueError("moment_tolerance must be finite and positive")
    weights = np.full(len(x), 1.0 / len(x))
    moment_residual = max(
        float(np.linalg.norm(
            weights @ real_harmonic_samples(x, degree),
            ord=np.inf,
        ))
        for degree in range(1, int(strength) + 1)
    )
    if moment_residual > moment_tolerance:
        raise ValueError(
            f"nodes fail the declared t-design moment audit: "
            f"{moment_residual:.3e} > {moment_tolerance:.3e}"
        )
    if graph == "weak_delaunay":
        selected = weak_delaunay_edges(x)
    elif graph == "complete":
        selected = complete_edges(len(x))
    elif graph == "knn":
        selected = knn_edges(x, min(6, len(x) - 1))
    else:
        raise ValueError("unsupported spherical-design graph")
    return QuadratureCandidate.build(
        "spherical_design", x, weights, selected,
        metadata={
            "declared_strength": int(strength),
            "graph_rule": graph,
            "strength_certification": "VERIFIED_FLOAT_MOMENT_RESIDUAL",
            "moment_residual": moment_residual,
        },
    )


def fibonacci_nodes(count: int) -> FloatArray:
    if count < 2:
        raise ValueError("count must be at least two")
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    index = np.arange(count, dtype=float)
    z = 1.0 - 2.0 * (index + 0.5) / count
    phi = 2.0 * math.pi * index / golden
    radius = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    return np.column_stack([radius * np.cos(phi), radius * np.sin(phi), z])


def maximal_net_candidate(
    count: int, *, pool_multiplier: int = 24, graph: str = "weak_delaunay"
) -> QuadratureCandidate:
    """Deterministic farthest-point diagnostic net with positive equal masses."""

    if count < 4 or pool_multiplier < 2:
        raise ValueError("invalid net parameters")
    pool = fibonacci_nodes(count * pool_multiplier)
    chosen = [int(np.argmax(pool[:, 2]))]
    best_dot = pool @ pool[chosen[0]]
    for _ in range(1, count):
        candidate = int(np.argmin(best_dot))
        chosen.append(candidate)
        best_dot = np.maximum(best_dot, pool @ pool[candidate])
    x = pool[np.asarray(chosen)]
    if graph == "weak_delaunay":
        selected = weak_delaunay_edges(x)
    elif graph == "complete":
        selected = complete_edges(len(x))
    elif graph == "knn":
        selected = knn_edges(x, min(6, len(x) - 1))
    else:
        raise ValueError("unsupported maximal-net graph")
    return QuadratureCandidate.build(
        "maximal_net", x, np.full(count, 1.0 / count), selected,
        metadata={
            "pool_multiplier": pool_multiplier,
            "graph_rule": graph,
            "mass_certification": "DIAGNOSTIC_EQUAL_MASS",
        },
    )


def delaunay_candidate(
    nodes: ArrayLike, weights: ArrayLike
) -> QuadratureCandidate:
    x = np.asarray(nodes, dtype=float)
    return QuadratureCandidate.build(
        "delaunay", x, weights, weak_delaunay_edges(x),
        metadata={"graph_rule": "weak_delaunay"},
    )


def locally_adapted_antipodal(
    candidate: QuadratureCandidate,
    pair_index: int,
    direction: ArrayLike,
    transferred_mass: float,
) -> QuadratureCandidate:
    """Insert an antipodal pair while preserving total mass and centering.

    The proposal is still rejected later unless moment, sampling, and inner
    generator certificates all pass.
    """

    x, w = candidate.nodes.copy(), candidate.weights.copy()
    if not 0 <= pair_index < len(x):
        raise ValueError("pair index is outside the candidate")
    antipode = int(np.argmin(np.linalg.norm(x + x[pair_index], axis=1)))
    if np.linalg.norm(x[antipode] + x[pair_index]) > 2e-10:
        raise ValueError("selected node has no certified antipode")
    if not 0 < transferred_mass < min(w[pair_index], w[antipode]):
        raise ValueError("transferred mass must leave both old masses positive")
    new = np.asarray(direction, dtype=float)
    new /= np.linalg.norm(new)
    x_new = np.vstack([x, new, -new])
    w[pair_index] -= transferred_mass
    w[antipode] -= transferred_mass
    w_new = np.concatenate([w, [transferred_mass, transferred_mass]])
    return QuadratureCandidate.build(
        "locally_adapted", x_new, w_new, weak_delaunay_edges(x_new),
        metadata={
            "parent_family": candidate.family,
            "refined_pair": (pair_index, antipode),
            "transferred_mass": transferred_mass,
        },
    )


def reflected_ring_candidate(M0: int, J: int) -> QuadratureCandidate:
    """Adapt the accepted P1E reflected-ring regression family to P2A."""

    from pure_math.covariance import p1e_short_gap_family_audit as p1e

    family = p1e.build_orbits(int(M0), int(J))
    graph = p1e.expand(family)
    x = np.asarray(graph["nodes"], dtype=float)
    weights = np.asarray(graph["weights"], dtype=float)
    mu = np.asarray(graph["mu"], dtype=float)
    total_mass = float(np.sum(mu))
    weighted_edges = [
        (int(row[0]), int(row[1]), float(row[2]) / total_mass)
        for row in np.asarray(graph["edges"])
    ]
    return QuadratureCandidate.build(
        "p1e_reflected_ring", x, weights, weighted_edges,
        metadata={
            "M0": int(M0),
            "J": int(J),
            "h": float(graph["h"]),
            "rate_cap_constant": 64.0 * math.pi**2,
            "defect_upper_constant": 75.0 / 2.0,
            "source": "accepted P1E reflected-ring construction",
        },
    )
