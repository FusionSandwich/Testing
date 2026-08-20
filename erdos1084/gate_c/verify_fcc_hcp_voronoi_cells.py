#!/usr/bin/env python3
"""Exact FCC/HCP contact-cell certificate for Target-B compactness."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product

Point = tuple[Q, Q, Q]


def det(a: Point, b: Point, c: Point) -> Q:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def solve3(rows: list[Point], rhs: list[Q]) -> Point | None:
    denominator = det(rows[0], rows[1], rows[2])
    if denominator == 0:
        return None
    answers: list[Q] = []
    for column in range(3):
        matrix = [list(row) for row in rows]
        for index in range(3):
            matrix[index][column] = rhs[index]
        answers.append(
            det(tuple(matrix[0]), tuple(matrix[1]), tuple(matrix[2]))
            / denominator
        )
    return answers[0], answers[1], answers[2]


def verify_cell(
    name: str,
    normals: list[Point],
    vertices: list[Point],
    metric: Point,
    triangles: list[tuple[int, int, int]],
    rational_volume: Q,
    physical_volume_text: str,
) -> None:
    rhs = Q(2)

    def dot(first: Point, second: Point) -> Q:
        return sum(metric[index] * first[index] * second[index] for index in range(3))

    def norm_sq(point: Point) -> Q:
        return dot(point, point)

    assert len(normals) == 12
    assert all(norm_sq(normal) == 4 for normal in normals)
    assert all(
        all(dot(normal, vertex) <= rhs for normal in normals)
        for vertex in vertices
    )

    regenerated: set[Point] = set()
    for indices in combinations(range(len(normals)), 3):
        rows = [
            tuple(metric[column] * normals[index][column] for column in range(3))
            for index in indices
        ]
        point = solve3(rows, [rhs, rhs, rhs])
        if point is not None and all(dot(normal, point) <= rhs for normal in normals):
            regenerated.add(point)

    assert regenerated == set(vertices)
    assert len(vertices) == 14
    assert max(norm_sq(vertex) for vertex in vertices) == 2

    facet_triangles: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
    for triangle in triangles:
        triangle_vertices = [vertices[index] for index in triangle]
        supports = [
            index
            for index, normal in enumerate(normals)
            if all(dot(normal, vertex) == rhs for vertex in triangle_vertices)
        ]
        assert len(supports) == 1
        facet_triangles[supports[0]].append(triangle)

    assert set(facet_triangles) == set(range(12))
    for facet_index, two_triangles in facet_triangles.items():
        assert len(two_triangles) == 2
        facet_vertices = {
            index
            for index, vertex in enumerate(vertices)
            if dot(normals[facet_index], vertex) == rhs
        }
        assert len(facet_vertices) == 4
        assert set().union(*(set(triangle) for triangle in two_triangles)) == facet_vertices
        assert len(set(two_triangles[0]) & set(two_triangles[1])) == 2

    volume = sum(
        abs(det(vertices[first], vertices[second], vertices[third]))
        for first, second, third in triangles
    ) / 6
    assert volume == rational_volume

    print(f"{name}: PASS")
    print(f"  contact halfspaces: {len(normals)}")
    print(f"  vertices: {len(vertices)}")
    print(f"  facets: {len(facet_triangles)}")
    print(f"  maximum physical squared radius: {max(norm_sq(v) for v in vertices)}")
    print(f"  rational-coordinate volume: {volume}")
    print(f"  physical volume: {physical_volume_text}")


fcc_normals: list[Point] = []
for zero_coordinate in range(3):
    nonzero = [index for index in range(3) if index != zero_coordinate]
    for first_sign, second_sign in product((-1, 1), repeat=2):
        vector = [Q(0), Q(0), Q(0)]
        vector[nonzero[0]] = Q(first_sign)
        vector[nonzero[1]] = Q(second_sign)
        fcc_normals.append(tuple(vector))

fcc_vertices: list[Point] = [
    (Q(1), Q(0), Q(0)),
    (Q(-1), Q(0), Q(0)),
    (Q(0), Q(1), Q(0)),
    (Q(0), Q(-1), Q(0)),
    (Q(0), Q(0), Q(1)),
    (Q(0), Q(0), Q(-1)),
]
fcc_vertices += [
    tuple(Q(sign, 2) for sign in signs)
    for signs in product((-1, 1), repeat=3)
]

fcc_triangles = [
    (10, 6, 5), (10, 6, 3), (7, 6, 3), (7, 6, 1),
    (11, 10, 3), (11, 10, 0), (11, 7, 3), (11, 7, 4),
    (12, 10, 0), (12, 10, 5), (8, 6, 1), (8, 6, 5),
    (8, 12, 5), (8, 12, 2), (13, 11, 4), (13, 11, 0),
    (13, 12, 0), (13, 12, 2), (9, 7, 4), (9, 7, 1),
    (9, 8, 1), (9, 8, 2), (9, 13, 4), (9, 13, 2),
]

verify_cell(
    "FCC contact Voronoi cell",
    fcc_normals,
    fcc_vertices,
    (Q(2), Q(2), Q(2)),
    fcc_triangles,
    Q(2),
    "2 * (2*sqrt(2)) = 4*sqrt(2)",
)

hcp_normals: list[Point] = [
    (Q(2), Q(0), Q(0)), (Q(-2), Q(0), Q(0)),
    (Q(1), Q(1), Q(0)), (Q(-1), Q(-1), Q(0)),
    (Q(-1), Q(1), Q(0)), (Q(1), Q(-1), Q(0)),
    (Q(1), Q(1, 3), Q(2, 3)),
    (Q(-1), Q(1, 3), Q(2, 3)),
    (Q(0), Q(-2, 3), Q(2, 3)),
    (Q(1), Q(1, 3), Q(-2, 3)),
    (Q(-1), Q(1, 3), Q(-2, 3)),
    (Q(0), Q(-2, 3), Q(-2, 3)),
]

hcp_vertices: list[Point] = [
    (Q(0), Q(0), Q(1, 2)), (Q(0), Q(0), Q(-1, 2)),
    (Q(1), Q(-1, 3), Q(1, 3)), (Q(1), Q(-1, 3), Q(-1, 3)),
    (Q(-1), Q(-1, 3), Q(1, 3)), (Q(-1), Q(-1, 3), Q(-1, 3)),
    (Q(0), Q(2, 3), Q(1, 3)), (Q(0), Q(2, 3), Q(-1, 3)),
    (Q(1), Q(1, 3), Q(1, 6)), (Q(1), Q(1, 3), Q(-1, 6)),
    (Q(-1), Q(1, 3), Q(1, 6)), (Q(-1), Q(1, 3), Q(-1, 6)),
    (Q(0), Q(-2, 3), Q(1, 6)), (Q(0), Q(-2, 3), Q(-1, 6)),
]

hcp_triangles = [
    (10, 0, 6), (10, 0, 4), (12, 0, 4), (12, 0, 2),
    (5, 10, 4), (5, 10, 11), (5, 12, 4), (5, 12, 13),
    (8, 0, 6), (8, 0, 2), (3, 5, 13), (3, 5, 1),
    (3, 12, 2), (3, 12, 13), (3, 8, 2), (3, 8, 9),
    (7, 5, 11), (7, 5, 1), (7, 3, 1), (7, 3, 9),
    (7, 10, 6), (7, 10, 11), (7, 8, 6), (7, 8, 9),
]

verify_cell(
    "HCP contact Voronoi cell",
    hcp_normals,
    hcp_vertices,
    (Q(1), Q(3), Q(6)),
    hcp_triangles,
    Q(4, 3),
    "(4/3) * (3*sqrt(2)) = 4*sqrt(2)",
)
