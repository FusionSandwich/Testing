"""Deterministic exact, ill-conditioned, and infeasible P2A fixtures."""

from __future__ import annotations

from itertools import combinations, product
from math import sqrt

import numpy as np
import sympy as sp

from .certificates import FarkasCertificate
from .model import (
    DesignModel,
    ExactSamplingCertificate,
    QuadratureGraph,
    RankPolicy,
)


def complete_edges(node_count: int) -> list[tuple[int, int]]:
    return list(combinations(range(node_count), 2))


def _exact_degree_two_basis() -> list[sp.Matrix]:
    basis = [
        sp.diag(1, -1, 0) / sp.sqrt(2),
        sp.diag(1, 1, -2) / sp.sqrt(6),
    ]
    for p, q in ((0, 1), (0, 2), (1, 2)):
        matrix = sp.zeros(3)
        matrix[p, q] = matrix[q, p] = 1 / sp.sqrt(2)
        basis.append(matrix)
    for i, left in enumerate(basis):
        if sp.trace(left) != 0:
            raise AssertionError("non-tracefree exact basis")
        for j, right in enumerate(basis):
            target = 1 if i == j else 0
            if sp.simplify(sp.trace(left.T * right) - target) != 0:
                raise AssertionError("non-orthonormal exact basis")
    return basis


def exact_sampling_certificate(
    nodes: list[sp.Matrix], weights: list[sp.Expr],
) -> ExactSamplingCertificate:
    basis = _exact_degree_two_basis()
    samples = sp.Matrix(
        len(nodes), len(basis),
        lambda i, p: sp.simplify((nodes[i].T * basis[p] * nodes[i])[0]),
    )
    return ExactSamplingCertificate.build(samples, weights)


def tetrahedron_fixture() -> tuple[DesignModel, np.ndarray, ExactSamplingCertificate]:
    signs = [v for v in product((1, -1), repeat=3) if v[0] * v[1] * v[2] == 1]
    exact_nodes = [sp.Matrix(v) / sp.sqrt(3) for v in signs]
    nodes = np.asarray(signs, dtype=float) / sqrt(3.0)
    weights = np.full(4, 0.25)
    graph = QuadratureGraph.build(nodes, weights, complete_edges(4))
    certificate = exact_sampling_certificate(exact_nodes, [sp.Rational(1, 4)] * 4)
    model = DesignModel.build(graph, (2,), exact_sampling_certificates={2: certificate})
    return model, np.full(6, 0.125), certificate


def octahedron_fixture() -> tuple[DesignModel, np.ndarray, ExactSamplingCertificate]:
    raw = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    nodes = np.asarray(raw, dtype=float)
    edges = [
        (i, j) for i, j in complete_edges(6)
        if abs(float(nodes[i] @ nodes[j])) < 0.5
    ]
    weights = np.full(6, 1.0 / 6.0)
    graph = QuadratureGraph.build(nodes, weights, edges)
    exact_nodes = [sp.Matrix(v) for v in raw]
    certificate = exact_sampling_certificate(exact_nodes, [sp.Rational(1, 6)] * 6)
    model = DesignModel.build(graph, (2,), exact_sampling_certificates={2: certificate})
    return model, np.full(len(edges), 1.0 / 12.0), certificate


def cube_nodes() -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    signs = list(product((1, -1), repeat=3))
    return np.asarray(signs, dtype=float) / sqrt(3.0), signs


def cube_hamming_edges(signs: list[tuple[int, int, int]], distance: int) -> list[tuple[int, int]]:
    return [
        (i, j) for i, j in complete_edges(len(signs))
        if sum(a != b for a, b in zip(signs[i], signs[j], strict=True)) == distance
    ]


def cube_shell_fixture(distance: int) -> tuple[DesignModel, np.ndarray]:
    if distance not in (1, 2, 3):
        raise ValueError("cube Hamming distance must be 1, 2, or 3")
    nodes, signs = cube_nodes()
    edges = cube_hamming_edges(signs, distance)
    graph = QuadratureGraph.build(nodes, np.full(8, 1.0 / 8.0), edges)
    directed_rate = {1: 1.0, 2: 0.5, 3: 1.0}[distance]
    gamma = np.full(len(edges), directed_rate / 8.0)
    return DesignModel.build(graph), gamma


def locally_strict_globally_infeasible_cube() -> tuple[DesignModel, FarkasCertificate, np.ndarray]:
    nodes, signs = cube_nodes()
    edges = cube_hamming_edges(signs, 1)
    heavy = {(1, 1, 1), (-1, -1, -1)}
    weights = np.asarray([0.2 if sign in heavy else 0.1 for sign in signs])
    graph = QuadratureGraph.build(nodes, weights, edges)
    model = DesignModel.build(graph)
    # Accepted exact field y_x=(x_2,x_3,x_1)/sqrt(3).  In normalized node
    # coordinates this is simply the cyclic permutation of the node.
    field = np.asarray([[node[1], node[2], node[0]] for node in nodes]).reshape(-1)
    certificate = FarkasCertificate(field, None, "exact unequal-mass cube permutation field")
    local_directed_rates = np.ones(len(edges))
    return model, certificate, local_directed_rates


def locally_feasible_globally_infeasible_square() -> tuple[DesignModel, FarkasCertificate]:
    nodes = np.asarray([
        [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
        [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0],
    ])
    weights = np.asarray([1.0, 2.0, 1.0, 2.0]) / 6.0
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    graph = QuadratureGraph.build(nodes, weights, edges)
    model = DesignModel.build(graph)
    signs = np.asarray([-1.0, 1.0, -1.0, 1.0])
    field = (signs[:, None] * nodes).reshape(-1)
    return model, FarkasCertificate(field, None, "exact unequal-mass four-cycle field")


def four_node_antipodal_preference(theta: float) -> tuple[DesignModel, np.ndarray]:
    """Complete equatorial four-node family with variable plain l1 cost."""
    if not 0.0 <= theta <= 1.0:
        raise ValueError("theta must lie in [0,1]")
    nodes = np.asarray([
        [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
        [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0],
    ])
    graph = QuadratureGraph.build(nodes, np.full(4, 0.25), complete_edges(4))
    gamma = np.zeros(6)
    for edge, (i, j) in enumerate(graph.edges):
        dot = float(nodes[i] @ nodes[j])
        gamma[edge] = (1.0 - theta) / 4.0 if dot < -0.5 else theta / 4.0
    return DesignModel.build(graph), gamma


def near_alias_ill_conditioned_fixture(epsilon: float = 2.0**-20) -> tuple[DesignModel, np.ndarray]:
    direction = np.asarray([1.0, epsilon, 0.0])
    direction /= np.linalg.norm(direction)
    nodes = np.asarray([
        [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
        direction, -direction,
        [0.0, 0.0, 1.0], [0.0, 0.0, -1.0],
    ])
    graph = QuadratureGraph.build(
        nodes, np.full(6, 1.0 / 6.0), complete_edges(6), unit_tolerance=1e-14,
    )
    gamma = np.full(15, 1.0 / 18.0)
    return DesignModel.build(graph), gamma


def full_rank_ill_conditioned_fixture(
    parameter: sp.Rational | float = sp.Rational(1, 2**20),
) -> tuple[DesignModel, np.ndarray, ExactSamplingCertificate, sp.Expr]:
    """Ten-node exact full-rank family with determinant ``1152*q*s/625``."""
    t = sp.sympify(parameter)
    q = sp.simplify((1 - t**2) / (1 + t**2))
    s = sp.simplify(2 * t / (1 + t**2))
    positive = [
        sp.Matrix([1, 0, 0]),
        sp.Matrix([0, 1, 0]),
        sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0]),
        sp.Matrix([sp.Rational(3, 5), 0, sp.Rational(4, 5)]),
        sp.Matrix([0, q, s]),
    ]
    exact_nodes = positive + [-node for node in positive]
    nodes = np.asarray([list(map(float, node)) for node in exact_nodes])
    graph = QuadratureGraph.build(
        nodes, np.full(10, 0.1), complete_edges(10), unit_tolerance=1e-14,
    )
    certificate = exact_sampling_certificate(exact_nodes, [sp.Rational(1, 10)] * 10)
    if certificate.rank != 5:
        raise AssertionError("full-rank ill-conditioned fixture lost exact rank five")
    model = DesignModel.build(graph, exact_sampling_certificates={2: certificate})
    gamma = np.full(45, 1.0 / 50.0)
    determinant = sp.simplify(sp.Rational(1152, 625) * q * s)
    return model, gamma, certificate, determinant


def ambiguous_rank_fixture(epsilon: float = 2.0**-33) -> QuadratureGraph:
    direction = np.asarray([1.0, epsilon, 0.0])
    direction /= np.linalg.norm(direction)
    nodes = np.asarray([
        [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
        direction, -direction,
        [0.0, 0.0, 1.0], [0.0, 0.0, -1.0],
    ])
    return QuadratureGraph.build(
        nodes, np.full(6, 1.0 / 6.0), complete_edges(6),
        unit_tolerance=1e-14, reject_zero_edge_columns=False,
    )


def dynamic_weight_ill_conditioned_fixture(epsilon: float = 2.0**-40) -> tuple[DesignModel, np.ndarray]:
    nodes = np.asarray([
        [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0], [0.0, -1.0, 0.0],
        [0.0, 0.0, 1.0], [0.0, 0.0, -1.0],
    ])
    weights = np.asarray([epsilon, epsilon, epsilon, epsilon, 1.0, 1.0])
    graph = QuadratureGraph.build(nodes, weights, complete_edges(6))
    gamma = graph.dense_centered_conductance()
    return DesignModel.build(graph), gamma


def full_rank_icosahedron_graph() -> QuadratureGraph:
    phi = (1.0 + sqrt(5.0)) / 2.0
    raw = []
    for a, b in product((-1.0, 1.0), repeat=2):
        raw.extend(((0.0, a, b * phi), (a, b * phi, 0.0), (b * phi, 0.0, a)))
    nodes = np.asarray(raw)
    nodes /= np.linalg.norm(nodes, axis=1)[:, None]
    return QuadratureGraph.build(nodes, np.full(12, 1.0 / 12.0), complete_edges(12))


def declared_rank_truncation_mutation() -> None:
    graph = full_rank_icosahedron_graph()
    DesignModel.build(graph, rank_policies={2: RankPolicy(declared_rank=3)})
