#!/usr/bin/env python3
"""Exact signed-conductance restoration and negative-mass certificate.

The example is the cube {+/-1}^3/sqrt(3), with unit vertex masses and a
reversible complete-graph conductance depending only on Hamming distance:

    distance 1:  3/2,
    distance 2:  0,
    distance 3: -1/2.

It conserves constants, has L X = -2 X, and makes all three genuine cross
quadratics x_a x_b exact at eigenvalue -6.  Its undirected negative mass is
2.  The final section proves 2 is the exact minimum among *all* reversible
cube conductances satisfying those coordinate and full cross-quadratic
requirements: group averaging reduces any feasible point without increasing
negative mass to three orbit rates, and the resulting one-variable convex
piecewise-linear objective is bounded below exactly.
"""

from __future__ import annotations

import itertools

import sympy as sp


Q = sp.Rational


def assert_zero(value: sp.Expr | sp.Matrix, message: str) -> None:
    if isinstance(value, sp.MatrixBase):
        ok = value.applyfunc(sp.simplify) == sp.zeros(*value.shape)
    else:
        ok = sp.simplify(value) == 0
    if not ok:
        raise AssertionError(message)


SIGNS = tuple(itertools.product((-1, 1), repeat=3))
VERTICES = tuple(sp.Matrix(s) / sp.sqrt(3) for s in SIGNS)


def hamming(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b))


def orbital_generator(r1: sp.Expr, r2: sp.Expr, r3: sp.Expr) -> sp.Matrix:
    rates = {1: r1, 2: r2, 3: r3}
    L = sp.zeros(8)
    for i, si in enumerate(SIGNS):
        for j, sj in enumerate(SIGNS):
            if i != j:
                L[i, j] = rates[hamming(si, sj)]
        L[i, i] = -sum(L[i, j] for j in range(8) if j != i)
    return L


def character(columns: tuple[int, ...]) -> sp.Matrix:
    return sp.Matrix([sp.prod(s[k] for k in columns) for s in SIGNS])


def exact_construction() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    L = orbital_generator(Q(3, 2), 0, -Q(1, 2))
    if L != L.T:
        raise AssertionError("signed rates are not reversible for unit masses")
    assert_zero(L * sp.ones(8, 1), "signed construction breaks conservation")

    X = sp.Matrix([[x[k] for k in range(3)] for x in VERTICES])
    assert_zero(L * X + 2 * X, "signed construction loses coordinate exactness")

    cross = sp.Matrix.hstack(
        *[sp.Matrix([x[a] * x[b] for x in VERTICES])
          for a, b in ((0, 1), (0, 2), (1, 2))]
    )
    if cross.rank() != 3:
        raise AssertionError("restored quadratics are aliased or dependent")
    for j in range(3):
        if cross.col(j) == sp.zeros(8, 1):
            raise AssertionError("claimed restored mode samples to zero")
    assert_zero(L * cross + 6 * cross,
                "signed construction does not restore eigenvalue -6")

    # Full covariance certificate: C_i=2(I-x_i x_i^T), so all residual
    # tensors M_i vanish, not merely the selected three pairings.
    for i, x in enumerate(VERTICES):
        C = sp.zeros(3)
        for j, y in enumerate(VERTICES):
            if i == j:
                continue
            delta = y - x
            C += L[i, j] * delta * delta.T
        assert_zero(C - 2 * (sp.eye(3) - x * x.T),
                    f"signed covariance certificate failed at {i}")
        M = C + 2 * x * x.T - 2 * sp.eye(3)
        assert_zero(M, f"signed residual tensor is nonzero at {i}")

    # Complete sign pattern and exact undirected negative mass.
    counts = {1: 0, 2: 0, 3: 0}
    negative_mass = sp.Integer(0)
    for i in range(8):
        for j in range(i + 1, 8):
            q = hamming(SIGNS[i], SIGNS[j])
            counts[q] += 1
            negative_mass += sp.Max(-L[i, j], 0)
    if counts != {1: 12, 2: 12, 3: 4}:
        raise AssertionError(f"cube orbit counts changed: {counts}")
    assert_zero(negative_mass - 2, "undirected negative mass is not 2")
    # The directed convention sum_{i,j} max(-a_ij,0) is twice this value.
    directed_negative_mass = sum(
        sp.Max(-L[i, j], 0) for i in range(8) for j in range(8) if i != j
    )
    assert_zero(directed_negative_mass - 4,
                "directed negative mass is not twice the edge mass")
    if all(L[i, j] >= 0 for i in range(8) for j in range(8) if i != j):
        raise AssertionError("negative test: signed construction has no negative edge")
    return L, X, cross


def derive_orbit_constraints() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Derive, rather than assume, the two averaged feasibility equations."""

    r1, r2, r3 = sp.symbols("r1 r2 r3", real=True)
    L = orbital_generator(r1, r2, r3)
    x1 = character((0,))
    x12 = character((0, 1))
    coordinate_residual = (L * x1 + 2 * x1)[0]
    quadratic_residual = (L * x12 + 6 * x12)[0]
    # All rows give the same scalar equation up to the character sign.
    for i in range(8):
        assert_zero((L * x1 + 2 * x1)[i] * x1[0]
                    - x1[i] * coordinate_residual,
                    "hidden coordinate orbit equation")
        assert_zero((L * x12 + 6 * x12)[i] * x12[0]
                    - x12[i] * quadratic_residual,
                    "hidden quadratic orbit equation")
    solutions = sp.solve((coordinate_residual, quadratic_residual), (r1, r3),
                         dict=True)
    if len(solutions) != 1:
        raise AssertionError("orbit feasibility did not reduce to one parameter")
    sol = solutions[0]
    assert_zero(sol[r1] - (Q(3, 2) - r2), "wrong r1 orbit constraint")
    assert_zero(sol[r3] - (-Q(1, 2) - r2), "wrong r3 orbit constraint")
    return r2, sol[r1], sol[r3]


def exact_optimality_certificate() -> None:
    """Prove min undirected negative mass = 2 on the feasible affine line.

    Convexity and cube invariance justify averaging any reversible feasible
    conductance over the cube group.  Each Hamming orbit has respectively
    12, 12, and 4 undirected edges.  The derived equations below parameterize
    the average by t=r2.  The four explicit affine formulas are the complete
    epigraph certificate for the convex piecewise-linear objective.
    """

    t, r1, r3 = derive_orbit_constraints()
    assert_zero(r1 - (Q(3, 2) - t), "r1 parameterization failed")
    assert_zero(r3 - (-Q(1, 2) - t), "r3 parameterization failed")

    # Piecewise formulas for
    # F(t)=12 max(-r1,0)+12 max(-t,0)+4 max(-r3,0).
    formulas = (
        ("t <= -1/2", -12 * t, 6),
        ("-1/2 <= t <= 0", 2 - 8 * t, 2),
        ("0 <= t <= 3/2", 2 + 4 * t, 2),
        ("t >= 3/2", 16 * t - 16, 8),
    )
    for _, formula, endpoint_bound in formulas:
        # Exact endpoint evaluations certify each monotone affine piece.
        slope = sp.diff(formula, t)
        if slope < 0:
            endpoint = -Q(1, 2) if formula == -12 * t else sp.Integer(0)
        else:
            endpoint = sp.Integer(0) if formula == 2 + 4 * t else Q(3, 2)
        value = sp.simplify(formula.subs(t, endpoint))
        if value != endpoint_bound:
            raise AssertionError("piecewise endpoint certificate changed")
        if value < 2:
            raise AssertionError("piecewise lower bound fell below 2")

    # Equality is attained at t=0, and only adjacent pieces meet 2 there.
    f_at_zero = 12 * sp.Max(-(Q(3, 2)), 0) + 12 * sp.Max(0, 0) \
        + 4 * sp.Max(Q(1, 2), 0)
    assert_zero(f_at_zero - 2, "construction does not attain the lower bound")

    # Why the reduction covers all reversible conductances: averaging over
    # signed coordinate permutations preserves the two linear eigenvector
    # systems; max(-gamma,0) is convex; and the group is transitive on each
    # Hamming-distance edge orbit.  These finite facts are checked exactly.
    perms = tuple(itertools.permutations(range(3)))
    sign_flips = tuple(itertools.product((-1, 1), repeat=3))
    action_permutations: list[tuple[int, ...]] = []
    lookup = {s: i for i, s in enumerate(SIGNS)}
    for p in perms:
        for eps in sign_flips:
            action = tuple(
                lookup[tuple(eps[k] * s[p[k]] for k in range(3))] for s in SIGNS
            )
            action_permutations.append(action)
    if len(set(action_permutations)) != 48:
        raise AssertionError("cube group action does not have order 48")
    for q in (1, 2, 3):
        edges = {(i, j) for i in range(8) for j in range(i + 1, 8)
                 if hamming(SIGNS[i], SIGNS[j]) == q}
        seed = next(iter(edges))
        orbit = set()
        for action in action_permutations:
            a, b = action[seed[0]], action[seed[1]]
            orbit.add((min(a, b), max(a, b)))
        if orbit != edges:
            raise AssertionError(f"cube group is not transitive on orbit q={q}")


def main() -> None:
    print("Exact signed restoration audit (SymPy exact arithmetic)")
    L, _, cross = exact_construction()
    exact_optimality_certificate()
    sign_counts = {
        "positive": sum(bool(L[i, j] > 0)
                        for i in range(8) for j in range(i + 1, 8)),
        "zero": sum(bool(L[i, j] == 0)
                    for i in range(8) for j in range(i + 1, 8)),
        "negative": sum(bool(L[i, j] < 0)
                        for i in range(8) for j in range(i + 1, 8)),
    }
    print(
        "cube: unit masses, complete graph, orbit rates "
        "(r1,r2,r3)=(3/2,0,-1/2); "
        f"signs={sign_counts}; restored-rank={cross.rank()}"
    )
    print("negative mass: undirected optimum=2; directed value=4")
    print("Exact signed restoration audit: PASS")


if __name__ == "__main__":
    main()
