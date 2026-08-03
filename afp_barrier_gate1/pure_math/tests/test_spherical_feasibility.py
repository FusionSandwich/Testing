#!/usr/bin/env python3
"""Exact-arithmetic regressions for the P0/M1 spherical theorem package.

The tests use only fractions. They falsify sign conventions, antipodal budget
handling, boundary/relative-interior distinctions, and the global shared-edge
matrix. They are not substitutes for the general proofs in the stage theorem.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from typing import Dict, List, Sequence, Tuple

Vec2 = Tuple[F, F]
Vec3 = Tuple[F, F, F]


def add2(a: Vec2, b: Vec2) -> Vec2:
    return (a[0] + b[0], a[1] + b[1])


def scale2(c: F, a: Vec2) -> Vec2:
    return (c * a[0], c * a[1])


def weighted_sum2(weights: Sequence[F], vectors: Sequence[Vec2]) -> Vec2:
    out = (F(0), F(0))
    for w, v in zip(weights, vectors, strict=True):
        out = add2(out, scale2(w, v))
    return out


def dot3(a: Vec3, b: Vec3) -> F:
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


def add3(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x + y for x, y in zip(a, b, strict=True))  # type: ignore[return-value]


def sub3(a: Vec3, b: Vec3) -> Vec3:
    return tuple(x - y for x, y in zip(a, b, strict=True))  # type: ignore[return-value]


def scale3(c: F, a: Vec3) -> Vec3:
    return tuple(c * x for x in a)  # type: ignore[return-value]


def local_convex_and_rate_examples() -> None:
    e1: Vec2 = (F(1), F(0))
    me1: Vec2 = (F(-1), F(0))
    e2: Vec2 = (F(0), F(1))
    me2: Vec2 = (F(0), F(-1))

    # Outside: every convex combination of e1,e2 has coordinate sum one.
    assert all(x + y == 1 for x, y in (e1, e2))

    # Relative boundary in the full-dimensional triangle conv{e1,-e1,e2}.
    boundary = [e1, me1, e2]
    lam_boundary = [F(1, 2), F(1, 2), F(0)]
    assert sum(lam_boundary) == 1
    assert weighted_sum2(lam_boundary, boundary) == (0, 0)
    assert min(lam_boundary) == 0

    # Relative interior of the square; all coefficients are strictly positive.
    interior = [e1, me1, e2, me2]
    lam_interior = [F(1, 4)] * 4
    assert sum(lam_interior) == 1
    assert weighted_sum2(lam_interior, interior) == (0, 0)
    assert min(lam_interior) > 0

    # Repeated/redundant directions: two distinct all-positive dependences.
    repeated = [e1, e1, me1, me1, e2, me2]
    lam_a = [F(1, 8), F(1, 8), F(1, 8), F(1, 8), F(1, 4), F(1, 4)]
    lam_b = [F(1, 16), F(3, 16), F(3, 16), F(1, 16), F(1, 4), F(1, 4)]
    for lam in (lam_a, lam_b):
        assert sum(lam) == 1
        assert min(lam) > 0
        assert weighted_sum2(lam, repeated) == (0, 0)
    assert lam_a != lam_b

    # Rational angular data: cos(theta)=3/5, sin(theta)=4/5,
    # loss=2/5, q=loss/sin=1/2. Formula a_j=2 lambda_j/(sin*Q).
    sin_theta = F(4, 5)
    loss = F(2, 5)
    q = loss / sin_theta
    assert q == F(1, 2)

    def rates(lam: Sequence[F]) -> List[F]:
        Q = sum((x * q for x in lam), F(0))
        return [F(2) * x / (sin_theta * Q) for x in lam]

    a_boundary = rates(lam_boundary)
    assert a_boundary == [F(5, 2), F(5, 2), F(0)]
    assert weighted_sum2([a * sin_theta for a in a_boundary], boundary) == (0, 0)
    assert sum((a * loss for a in a_boundary), F(0)) == 2

    a_interior = rates(lam_interior)
    assert a_interior == [F(5, 4)] * 4
    assert weighted_sum2([a * sin_theta for a in a_interior], interior) == (0, 0)
    assert sum((a * loss for a in a_interior), F(0)) == 2


def perturbation_boundary_crossing() -> None:
    e1: Vec2 = (F(1), F(0))
    e2: Vec2 = (F(0), F(1))

    # Rational unit-circle parametrization near -e1.
    def u(r: F) -> Vec2:
        den = r * r + 1
        return ((r * r - 1) / den, F(2) * r / den)

    up = u(F(1, 3))
    uz = u(F(0))
    um = u(F(-1, 3))
    assert up == (F(-4, 5), F(3, 5))
    assert uz == (F(-1), F(0))
    assert um == (F(-4, 5), F(-3, 5))

    # r>0 is outside; r=0 is boundary; r<0 has an all-positive certificate.
    assert up[1] > 0
    assert weighted_sum2([F(1, 2), F(1, 2), F(0)], [e1, uz, e2]) == (0, 0)
    lam = [F(1, 3), F(5, 12), F(1, 4)]
    assert min(lam) > 0
    assert sum(lam) == 1
    assert weighted_sum2(lam, [e1, um, e2]) == (0, 0)


def antipodal_budget_examples() -> None:
    # Antipodal-only: no tangent direction is introduced; rates sum to one.
    antipodal_only = [F(1, 3)] * 3
    assert min(antipodal_only) > 0
    assert sum(antipodal_only) == 1
    assert sum((F(2) * a for a in antipodal_only), F(0)) == 2

    loss = F(2, 5)

    # Mixed boundary: the third nonantipodal edge is zero. Each block spends
    # one unit of the normal budget.
    nonant_boundary = [F(5, 4), F(5, 4), F(0)]
    antipodal_rate = F(1, 2)
    assert sum((a * loss for a in nonant_boundary), F(0)) == 1
    assert F(2) * antipodal_rate == 1

    # Mixed strict: four surrounding nonantipodal directions plus an antipode.
    nonant_strict = [F(5, 16)] * 4
    antipodal_strict = F(3, 4)
    assert min(nonant_strict) > 0 and antipodal_strict > 0
    assert sum((a * loss for a in nonant_strict), F(0)) == F(1, 2)
    assert F(2) * antipodal_strict == F(3, 2)
    assert sum((a * loss for a in nonant_strict), F(0)) + F(2) * antipodal_strict == 2


def cube_global_examples() -> None:
    # Actual nodes are x/sqrt(3); scaled coordinates keep every check rational.
    vertices: List[Vec3] = [tuple(F(v) for v in x) for x in product((1, -1), repeat=3)]  # type: ignore[list-item]
    index: Dict[Vec3, int] = {x: i for i, x in enumerate(vertices)}
    edges: List[Tuple[int, int]] = []
    for i, x in enumerate(vertices):
        for k in range(3):
            y = list(x)
            y[k] = -y[k]
            j = index[tuple(y)]  # type: ignore[arg-type]
            if i < j:
                edges.append((i, j))
    assert len(edges) == 12

    neighbors: List[List[int]] = [[] for _ in vertices]
    for i, j in edges:
        neighbors[i].append(j)
        neighbors[j].append(i)

    # Every local row is uniquely positive, with rate one on all three edges.
    for i, x in enumerate(vertices):
        assert len(neighbors[i]) == 3
        lhs = (F(0), F(0), F(0))
        for j in neighbors[i]:
            lhs = add3(lhs, sub3(vertices[j], x))
            assert dot3(x, vertices[j]) == 1  # actual dot product is 1/3
        assert lhs == scale3(F(-2), x)

    # Strict symmetric global example: all masses and conductances are one.
    gamma = [F(1)] * len(edges)
    balance = [(F(0), F(0), F(0)) for _ in vertices]
    for g, (i, j) in zip(gamma, edges, strict=True):
        d = sub3(vertices[j], vertices[i])
        balance[i] = add3(balance[i], scale3(g, d))
        balance[j] = add3(balance[j], scale3(-g, d))
    for i, x in enumerate(vertices):
        assert balance[i] == scale3(F(-2), x)

    # Total-outgoing-rate LP: c_e=2 and y_i=-(3/2)Omega_i saturates every edge.
    alpha = F(-3, 2)
    for i, j in edges:
        dx = sub3(vertices[j], vertices[i])
        aty = dot3(scale3(alpha, sub3(vertices[i], vertices[j])), dx) / 3
        assert aty == 2
    primal_objective = sum((F(2) * g for g in gamma), F(0))
    dual_objective = sum((F(-2) * dot3(x, scale3(alpha, x)) / 3 for x in vertices), F(0))
    assert primal_objective == dual_objective == 24

    # Weighted-centered but globally incompatible cube: the +++/--- antipodal
    # pair has mass two, all other vertices mass one.
    heavy = {(F(1), F(1), F(1)), (F(-1), F(-1), F(-1))}
    w = [F(2) if x in heavy else F(1) for x in vertices]
    center = (F(0), F(0), F(0))
    for wi, x in zip(w, vertices, strict=True):
        center = add3(center, scale3(wi, x))
    assert center == (0, 0, 0)

    # Exact Farkas field y_x=(x2,x3,x1)/sqrt(3). Every edge work is zero and
    # b.y=-4, proving global infeasibility despite local strict feasibility.
    def perm(x: Vec3) -> Vec3:
        return (x[1], x[2], x[0])

    for i, j in edges:
        aty = dot3(sub3(perm(vertices[i]), perm(vertices[j])), sub3(vertices[j], vertices[i])) / 3
        assert aty == 0
    dual_work = sum((F(-2) * wi * dot3(x, perm(x)) / 3 for wi, x in zip(w, vertices, strict=True)), F(0))
    assert dual_work == -4

    # Unique local rates a_ij=1 would force gamma_ij=w_i=w_j on every edge.
    assert any(w[i] != w[j] for i, j in edges)


def main() -> None:
    local_convex_and_rate_examples()
    perturbation_boundary_crossing()
    antipodal_budget_examples()
    cube_global_examples()
    print("exact spherical feasibility regressions: PASS")


if __name__ == "__main__":
    main()
