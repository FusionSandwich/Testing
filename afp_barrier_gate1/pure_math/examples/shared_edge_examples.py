from fractions import Fraction as Q
from itertools import product
from typing import Dict, List, Sequence, Tuple

Vec3 = Tuple[Q, Q, Q]


def add(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x + y for x, y in zip(a, b, strict=True))  # type: ignore[return-value]


def sub(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x - y for x, y in zip(a, b, strict=True))  # type: ignore[return-value]


def scale(c: Q, a: Vec3) -> Vec3:
    return tuple(c * x for x in a)  # type: ignore[return-value]


def dot(a: Vec3, b: Vec3) -> Q:
    return sum((x * y for x, y in zip(a, b, strict=True)), Q(0))


def strain(vertices: Sequence[Vec3], edge: Tuple[int, int], y: Sequence[Vec3]) -> Q:
    p, q = edge
    return dot(sub(y[p], y[q]), sub(vertices[q], vertices[p]))


def run() -> None:
    vertices: List[Vec3] = [
        tuple(Q(x) for x in s) for s in product((1, -1), repeat=3)
    ]  # type: ignore[list-item]
    edges = [
        (i, j)
        for i, x in enumerate(vertices)
        for j, z in enumerate(vertices[i + 1 :], i + 1)
        if sum(a != b for a, b in zip(x, z, strict=True)) == 1
    ]
    assert len(vertices) == 8 and len(edges) == 12
    index: Dict[Vec3, int] = {v: i for i, v in enumerate(vertices)}

    # Every row is locally exact with three unit rates.
    for i, x in enumerate(vertices):
        total: Vec3 = (Q(0), Q(0), Q(0))
        for p, q in edges:
            if p == i:
                total = add(total, sub(vertices[q], x))
            elif q == i:
                total = add(total, sub(vertices[p], x))
        assert total == scale(Q(-2), x)

    # Centered nonconstant masses and an exact infeasibility certificate.
    masses = [Q(1) for _ in vertices]
    plus = index[(Q(1), Q(1), Q(1))]
    minus = index[(Q(-1), Q(-1), Q(-1))]
    adjacent = index[(Q(1), Q(1), Q(-1))]
    masses[plus] = masses[minus] = Q(2)
    center: Vec3 = (Q(0), Q(0), Q(0))
    for w, x in zip(masses, vertices, strict=True):
        center = add(center, scale(w, x))
    assert center == (Q(0), Q(0), Q(0))
    y: List[Vec3] = [(Q(0), Q(0), Q(0)) for _ in vertices]
    y[plus] = y[adjacent] = (Q(0), Q(0), Q(1))
    assert all(strain(vertices, edge, y) == 0 for edge in edges)
    assert sum(
        (dot(scale(-2 * w, x), yi) for w, x, yi in zip(masses, vertices, y, strict=True)),
        Q(0),
    ) == -2

    # Strict global cube and exact conductance-sum primal/dual certificates.
    assert sum((Q(1) for _ in edges), Q(0)) == 12
    y_opt = [scale(Q(-1, 4), x) for x in vertices]
    assert all(strain(vertices, edge, y_opt) == 1 for edge in edges)
    assert sum(
        (dot(scale(Q(-2), x), yi) for x, yi in zip(vertices, y_opt, strict=True)),
        Q(0),
    ) == 12
