#!/usr/bin/env python3
"""Exact regression and adversarial audit for Prompt 3 spherical Q=1 rigidity.

The ordinary proofs live in the Prompt 3 theorem document. This script uses
only exact SymPy arithmetic for the finite polyhedral, Euler, variance, and
counterfamily checks. Floating-point rank or geometry thresholds are not used
as proof evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product

import sympy as sp

Q = sp.Rational
SQRT5 = sp.sqrt(5)
PHI = (1 + SQRT5) / 2
INV_PHI = 1 / PHI


def simp(value: sp.Expr | int) -> sp.Expr:
    """Canonical exact simplification in Q(sqrt(5)) and rational subfields."""

    return sp.factor(sp.radsimp(sp.simplify(sp.sympify(value))))


def dot(x: tuple[sp.Expr, ...], y: tuple[sp.Expr, ...]) -> sp.Expr:
    return simp(sum(a * b for a, b in zip(x, y, strict=True)))


@dataclass(frozen=True)
class PolyhedronAudit:
    name: str
    vertices: int
    edges: int
    degree: int
    triangles: int
    adjacent_dot: sp.Expr
    edge_rate: sp.Expr
    row_rate: sp.Expr
    defect: sp.Expr
    quality: sp.Expr
    is_triangular_sphere: bool


def platonic_raw_data() -> dict[str, tuple[list[tuple[sp.Expr, ...]], sp.Expr]]:
    tetrahedron = [
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    ]
    octahedron = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    cube = list(product((-1, 1), repeat=3))
    icosahedron = [
        (0, 1, PHI),
        (0, -1, PHI),
        (0, 1, -PHI),
        (0, -1, -PHI),
        (1, PHI, 0),
        (-1, PHI, 0),
        (1, -PHI, 0),
        (-1, -PHI, 0),
        (PHI, 0, 1),
        (-PHI, 0, 1),
        (PHI, 0, -1),
        (-PHI, 0, -1),
    ]
    dodecahedron: list[tuple[sp.Expr, ...]] = list(product((-1, 1), repeat=3))
    for a in (-1, 1):
        for b in (-1, 1):
            dodecahedron.extend(
                [
                    (0, a * INV_PHI, b * PHI),
                    (a * INV_PHI, b * PHI, 0),
                    (a * PHI, 0, b * INV_PHI),
                ]
            )
    return {
        "tetrahedron": (tetrahedron, sp.Integer(-1)),
        "octahedron": (octahedron, sp.Integer(0)),
        "cube": (cube, sp.Integer(1)),
        "icosahedron": (icosahedron, PHI),
        "dodecahedron": (dodecahedron, SQRT5),
    }


def adjacency(raw: list[tuple[sp.Expr, ...]], adjacent_raw_dot: sp.Expr) -> list[list[int]]:
    n = len(raw)
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if simp(dot(raw[i], raw[j]) - adjacent_raw_dot) == 0:
                graph[i][j] = graph[j][i] = 1
    return graph


def triangle_count(graph: list[list[int]]) -> int:
    n = len(graph)
    return sum(
        graph[i][j] * graph[j][k] * graph[k][i]
        for i, j, k in combinations(range(n), 3)
    )


def common_neighbor_count(graph: list[list[int]], i: int, j: int) -> int:
    return sum(graph[i][k] * graph[j][k] for k in range(len(graph)))


def audit_polyhedron(
    name: str,
    raw: list[tuple[sp.Expr, ...]],
    adjacent_raw_dot: sp.Expr,
) -> PolyhedronAudit:
    n = len(raw)
    norm2 = simp(dot(raw[0], raw[0]))
    assert all(simp(dot(v, v) - norm2) == 0 for v in raw)
    graph = adjacency(raw, adjacent_raw_dot)
    degrees = [sum(row) for row in graph]
    assert len(set(degrees)) == 1
    degree = degrees[0]
    edges = sum(degrees) // 2
    triangles = triangle_count(graph)
    alpha = simp(adjacent_raw_dot / norm2)
    loss = simp(1 - alpha)
    edge_rate = simp(Q(2, degree) / loss)
    row_rate = simp(degree * edge_rate)
    defect = simp(degree * edge_rate * loss**2)
    quality = simp(row_rate * defect / 4)
    assert quality == 1

    for i, vertex in enumerate(raw):
        neighbor_sum = tuple(
            simp(sum(graph[i][j] * raw[j][k] for j in range(n)))
            for k in range(3)
        )
        generated = tuple(
            simp(edge_rate * (neighbor_sum[k] - degree * vertex[k]))
            for k in range(3)
        )
        assert generated == tuple(simp(-2 * coordinate) for coordinate in vertex)

    is_triangular_sphere = (
        3 * triangles == 2 * edges and n - edges + triangles == 2
    )
    if is_triangular_sphere:
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j]:
                    assert common_neighbor_count(graph, i, j) == 2

    return PolyhedronAudit(
        name=name,
        vertices=n,
        edges=edges,
        degree=degree,
        triangles=triangles,
        adjacent_dot=alpha,
        edge_rate=edge_rate,
        row_rate=row_rate,
        defect=defect,
        quality=quality,
        is_triangular_sphere=is_triangular_sphere,
    )


def platonic_q_one_audit() -> dict[str, PolyhedronAudit]:
    audits = {
        name: audit_polyhedron(name, raw, adjacent_raw_dot)
        for name, (raw, adjacent_raw_dot) in platonic_raw_data().items()
    }
    expected = {
        "tetrahedron": (4, 6, 3, 4, Q(-1, 3), Q(3, 2)),
        "octahedron": (6, 12, 4, 8, sp.Integer(0), sp.Integer(2)),
        "cube": (8, 12, 3, 0, Q(1, 3), sp.Integer(3)),
        "icosahedron": (12, 30, 5, 20, SQRT5 / 5, (5 + SQRT5) / 2),
        "dodecahedron": (20, 30, 3, 0, SQRT5 / 3, (9 + 3 * SQRT5) / 2),
    }
    for name, audit in audits.items():
        v, e, q, t, c, rate = expected[name]
        assert (audit.vertices, audit.edges, audit.degree, audit.triangles) == (v, e, q, t)
        assert simp(audit.adjacent_dot - c) == 0
        assert simp(audit.row_rate - rate) == 0
        assert audit.quality == 1
        print(
            f"{name:12s}: V={v:2d} E={e:2d} degree={q} triangles={t:2d} "
            f"dot={simp(c)} rate={simp(rate)} defect={audit.defect} Q=1"
        )

    assert audits["tetrahedron"].is_triangular_sphere
    assert audits["octahedron"].is_triangular_sphere
    assert audits["icosahedron"].is_triangular_sphere
    assert not audits["cube"].is_triangular_sphere
    assert not audits["dodecahedron"].is_triangular_sphere
    print("Platonic Q=1 and triangulation-boundary audit: PASS")
    return audits


def regular_triangulation_arithmetic_audit() -> None:
    expected = {
        3: (4, 6, 4, Q(-1, 3), Q(3, 2)),
        4: (6, 12, 8, sp.Integer(0), sp.Integer(2)),
        5: (12, 30, 20, SQRT5 / 5, (5 + SQRT5) / 2),
    }
    for q, (vertices, edges, faces, expected_c, expected_rate) in expected.items():
        cos_alpha = sp.expand_trig(sp.cos(2 * sp.pi / q))
        c = simp(cos_alpha / (1 - cos_alpha))
        rate = simp(2 / (1 - c))
        assert simp(c - expected_c) == 0
        assert simp(rate - expected_rate) == 0
        assert (6 - q) * vertices == 12
        assert q * vertices == 2 * edges
        assert 3 * faces == 2 * edges
        assert vertices - edges + faces == 2
        gram_det = simp((1 - c) ** 2 * (1 + 2 * c))
        assert gram_det > 0
        print(
            f"q={q}: (V,E,F)=({vertices},{edges},{faces}), "
            f"edge dot={c}, common row rate={rate}"
        )
    print("regular spherical-triangulation arithmetic: PASS")


def graph_certificate_audit(audits: dict[str, PolyhedronAudit]) -> None:
    data = platonic_raw_data()
    tet = adjacency(*data["tetrahedron"])
    assert all(tet[i][j] == 1 for i in range(4) for j in range(4) if i != j)

    oct_graph = adjacency(*data["octahedron"])
    complement_edges = [
        (i, j)
        for i in range(6)
        for j in range(i + 1, 6)
        if not oct_graph[i][j]
    ]
    assert len(complement_edges) == 3
    assert sorted(v for edge in complement_edges for v in edge) == list(range(6))

    ico = adjacency(*data["icosahedron"])
    assert all(sum(row) == 5 for row in ico)
    assert triangle_count(ico) == 20
    assert all(
        common_neighbor_count(ico, i, j) == 2
        for i in range(12)
        for j in range(i + 1, 12)
        if ico[i][j]
    )
    for i in range(12):
        link = [j for j in range(12) if ico[i][j]]
        assert len(link) == 5
        link_edges = sum(ico[u][v] for u, v in combinations(link, 2))
        assert link_edges == 5
        assert all(sum(ico[u][v] for v in link) == 2 for u in link)

    assert audits["icosahedron"].vertices == 12
    print("tetrahedral, octahedral, and icosahedral graph certificates: PASS")


def normalized_quality_variance_audit() -> None:
    examples = [
        ([Q(1, 3), Q(2, 3)], [Q(1, 2), Q(5, 4)]),
        ([Q(1, 6), Q(1, 3), Q(1, 2)], [Q(1, 4), Q(1), Q(7, 4)]),
        ([Q(1, 4)] * 4, [Q(1, 3), Q(2, 3), Q(4, 3), Q(5, 3)]),
    ]
    for weights, losses in examples:
        assert sum(weights) == 1
        mean = simp(sum(p * ell for p, ell in zip(weights, losses, strict=True)))
        second = simp(sum(p * ell**2 for p, ell in zip(weights, losses, strict=True)))
        left = simp(second / mean**2 - 1)
        right = simp(
            sum(
                p * (ell / mean - 1) ** 2
                for p, ell in zip(weights, losses, strict=True)
            )
        )
        assert simp(left - right) == 0
        assert right >= 0
    print("normalized Q-1 weighted-variance identity: PASS")


def near_rigidity_constant_audit() -> None:
    eps = Q(1, 100)
    p_min = Q(1, 4)
    delta = sp.sqrt(eps / p_min)
    kappa = simp((1 + delta) / (1 - delta))
    assert delta == Q(1, 5)
    assert kappa == Q(3, 2)

    diameter = 4
    root_center = sp.Integer(1)
    centers = [simp(root_center * kappa**r) for r in range(diameter + 1)]
    for left, right in zip(centers[:-1], centers[1:], strict=True):
        assert simp((1 - delta) * right - (1 + delta) * left) == 0
        shared_loss = simp((1 + delta) * left)
        assert (1 - delta) * left <= shared_loss <= (1 + delta) * left
        assert (1 - delta) * right <= shared_loss <= (1 + delta) * right

    lower = simp((1 - delta) * kappa ** (-diameter) * root_center)
    upper = simp((1 + delta) * kappa**diameter * root_center)
    ratio_bound = simp(kappa ** (2 * diameter + 1))
    assert simp(upper / lower - ratio_bound) == 0

    eta, r_min, a_min = Q(1, 1000), Q(1, 2), Q(1, 5)
    delta_add = sp.sqrt(eta / (r_min * a_min))
    assert delta_add == Q(1, 10)
    assert (2 * diameter + 1) * delta_add == Q(9, 10)
    assert 2 * (2 * diameter + 1) * delta_add == Q(9, 5)
    print(
        "near-rigidity constants: PASS "
        f"(delta={delta}, kappa={kappa}, D={diameter}, Delta={delta_add})"
    )


def rare_edge_counterfamily_audit() -> None:
    t = sp.symbols("t", positive=True)
    p = t**4
    outlier = 1 + 1 / t
    bulk = 1 - t**3 / (1 - t**4)
    mean = simp(p * outlier + (1 - p) * bulk)
    variance = simp(p * (outlier - 1) ** 2 + (1 - p) * (bulk - 1) ** 2)
    assert mean == 1
    assert simp(variance - t**2 / (1 - t**4)) == 0
    assert sp.limit(variance, t, 0, dir="+") == 0
    assert sp.limit(outlier, t, 0, dir="+") == sp.oo
    for value in (Q(1, 2), Q(1, 3), Q(1, 5), Q(1, 10)):
        assert simp(variance.subs(t, value)) > 0
        assert simp(bulk.subs(t, value)) > 0
    print("rare-active-edge counterfamily without p_min: PASS")


def conductance_floor_transfer_audit() -> None:
    gamma_min = Q(1, 7)
    w_max = Q(5, 3)
    r_max = Q(11, 4)
    a_min = simp(gamma_min / w_max)
    p_min = simp(gamma_min / (w_max * r_max))
    assert a_min == Q(3, 35)
    assert p_min == Q(12, 385)
    assert simp(a_min / r_max - p_min) == 0
    print("shared-conductance floor transfer: PASS")


def main() -> None:
    print("Prompt 3 exact spherical Q=1 rigidity audit")
    audits = platonic_q_one_audit()
    regular_triangulation_arithmetic_audit()
    graph_certificate_audit(audits)
    normalized_quality_variance_audit()
    near_rigidity_constant_audit()
    rare_edge_counterfamily_audit()
    conductance_floor_transfer_audit()
    print("Prompt 3 exact audit: PASS")


if __name__ == "__main__":
    main()
