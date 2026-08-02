#!/usr/bin/env python3
"""Exact corrective audit for the Prompt 2 closeout.

This audit is deliberately algebraic.  It uses rational and quadratic-radical
arithmetic only; no floating rank threshold is accepted as proof evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import sympy as sp

Q = sp.Rational
SQRT5 = sp.sqrt(5)


def assert_zero(expr: sp.Expr | sp.MatrixBase, label: str) -> None:
    if isinstance(expr, sp.MatrixBase):
        simplified = expr.applyfunc(sp.simplify)
        if simplified != sp.zeros(*expr.shape):
            raise AssertionError(f"{label}: {simplified}")
    elif sp.simplify(expr) != 0:
        raise AssertionError(f"{label}: {sp.simplify(expr)}")


def regular_simplex_audit() -> None:
    for d in range(2, 11):
        n = d + 1
        gram = sp.Matrix(
            n,
            n,
            lambda i, j: sp.Integer(1) if i == j else -Q(1, d),
        )
        rate = Q(d - 1, d + 1)
        generator = rate * (sp.ones(n) - n * sp.eye(n))
        zero_sum_basis = sp.Matrix.hstack(
            *[
                sp.eye(n)[:, r] - sp.eye(n)[:, n - 1]
                for r in range(n - 1)
            ]
        )
        assert_zero(
            generator * zero_sum_basis + (d - 1) * zero_sum_basis,
            f"simplex d={d} coordinate eigenvalue",
        )

        # For zero-sum y, the theorem's explicit inverse is
        # A_y=d^2/(d^2-1) sum_i y_i x_i x_i^T.  Evaluation at x_k is the
        # squared Gram matrix below.
        sample_map = Q(d * d, d * d - 1) * gram.applyfunc(lambda z: z**2)
        assert_zero(
            sample_map * zero_sum_basis - zero_sum_basis,
            f"simplex d={d} sampling inverse",
        )
        ambient = d * (d + 1) // 2 - 1
        assert ambient - d >= 0
    print("regular-simplex formulas: PASS (d=2,...,10)")


def pentagon_generator() -> tuple[sp.Matrix, sp.Expr, sp.Expr]:
    u = (5 + 3 * SQRT5) / 10
    v = (5 - 3 * SQRT5) / 10
    generator = sp.zeros(5)
    for i in range(5):
        for step, rate in ((1, u), (-1, u), (2, v), (-2, v)):
            generator[i, (i + step) % 5] += rate
        generator[i, i] = -sum(
            generator[i, j] for j in range(5) if j != i
        )
    return generator, u, v


def signed_pentagon_audit() -> None:
    generator, u, v = pentagon_generator()
    assert sp.simplify(u) > 0
    assert sp.simplify(v) < 0

    angles = [2 * sp.pi * m / 5 for m in range(5)]
    one = sp.ones(5, 1)
    x = sp.Matrix([sp.cos(theta) for theta in angles]).applyfunc(sp.simplify)
    y = sp.Matrix([sp.sin(theta) for theta in angles]).applyfunc(sp.simplify)
    cos2 = sp.Matrix([sp.cos(2 * theta) for theta in angles]).applyfunc(
        sp.simplify
    )
    sin2 = sp.Matrix([sp.sin(2 * theta) for theta in angles]).applyfunc(
        sp.simplify
    )

    assert_zero(generator * one, "pentagon L1")
    assert_zero(generator * x + x, "pentagon Lx")
    assert_zero(generator * y + y, "pentagon Ly")
    assert_zero(generator * cos2 + 4 * cos2, "pentagon Lcos2")
    assert_zero(generator * sin2 + 4 * sin2, "pentagon Lsin2")

    sampling = sp.Matrix.hstack(cos2, sin2)
    residual = (generator + 4 * sp.eye(5)) * sampling
    assert sampling.rank() == 2
    assert residual.rank() == 0
    assert 2 - residual.rank() == 2
    assert sampling.rank() - residual.rank() == 2

    # A generator of C5 acts by rotation through 4*pi/5 on Sym_0(2).
    # Negative characteristic discriminant excludes a real invariant line.
    trace = sp.simplify(2 * sp.cos(4 * sp.pi / 5))
    discriminant = sp.simplify(trace**2 - 4)
    assert trace == -(1 + SQRT5) / 2
    assert discriminant == (SQRT5 - 5) / 2
    assert discriminant < 0

    print("signed regular-pentagon counterexample: PASS")
    print(f"  u={u}, v={v}, dim(E_form)=2, dim(E_sample)=2")
    print(f"  C5 conjugation discriminant={discriminant}<0 (real irreducible)")


def centered_product_algebra_audit() -> None:
    lam, nu, mu, c, f, g, gamma = sp.symbols(
        "lam nu mu c f g gamma"
    )
    lhs = (-lam * f * g - nu * f * g + 2 * gamma) + mu * (f * g - c)
    rhs = 2 * gamma + (mu - lam - nu) * f * g - mu * c
    assert_zero(lhs - rhs, "general shifted product residual")

    resonance = sp.simplify(rhs.subs(mu, lam + nu))
    assert_zero(
        resonance - (2 * gamma - (lam + nu) * c),
        "additive product resonance",
    )
    square = sp.simplify(resonance.subs({nu: lam, g: f}) / 2)
    assert_zero(square - (gamma - lam * c), "centered square resonance")
    assert_zero(square.subs(c, 0) - gamma, "uncentered square corollary")
    print("centered product residual identities: PASS")


def boolean_square_audit() -> None:
    states = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    generator = sp.zeros(4)
    for i, (x1, x2) in enumerate(states):
        for flipped in ((-x1, x2), (x1, -x2)):
            generator[i, states.index(flipped)] = 1
        generator[i, i] = -2

    one = sp.ones(4, 1)
    f = sp.Matrix([x1 + x2 for x1, x2 in states])
    centered = sp.Matrix([(x1 + x2) ** 2 - 2 for x1, x2 in states])
    cross = sp.Matrix([2 * x1 * x2 for x1, x2 in states])
    gamma = sp.Matrix(
        [
            Q(1, 2)
            * sum(
                generator[i, j] * (f[j] - f[i]) ** 2
                for j in range(4)
                if j != i
            )
            for i in range(4)
        ]
    )

    assert_zero(generator * one, "Boolean L1")
    assert_zero(generator * f + 2 * f, "Boolean Lf")
    assert centered == cross
    assert centered != sp.zeros(4, 1)
    assert_zero(generator * centered + 4 * centered, "Boolean centered square")
    assert gamma == 4 * one

    t = sp.symbols("t", nonnegative=True)
    variance = 2 * (1 - sp.exp(-4 * t))
    pt_f2 = sp.exp(-4 * t) * centered + 2 * one
    pt_f_sq = sp.exp(-4 * t) * sp.Matrix([value**2 for value in f])
    assert_zero(
        pt_f2 - pt_f_sq - variance * one,
        "Boolean semigroup variance",
    )
    assert sp.simplify(variance.subs(t, 1)) > 0

    print("Boolean centered-square resonance: PASS")
    print("  Lf=-2f, L(f^2-2)=-4(f^2-2), Gamma(f)=4")
    print("  semigroup variance=2(1-exp(-4t))>0 for t>0")


@dataclass(frozen=True)
class S2Row:
    ell: int
    degrees: tuple[int, ...]
    eigenvalues: tuple[int, ...]
    target: int
    resonances: tuple[int, ...]


def s2_low_degree_table_audit() -> list[S2Row]:
    expected = {
        1: ((0, 2), (0, 6), 4),
        2: ((0, 2, 4), (0, 6, 20), 12),
        3: ((0, 2, 4, 6), (0, 6, 20, 42), 24),
        4: ((0, 2, 4, 6, 8), (0, 6, 20, 42, 72), 40),
        5: ((0, 2, 4, 6, 8, 10), (0, 6, 20, 42, 72, 110), 60),
        6: (
            (0, 2, 4, 6, 8, 10, 12),
            (0, 6, 20, 42, 72, 110, 156),
            84,
        ),
    }
    rows: list[S2Row] = []
    for ell in range(1, 7):
        degrees = tuple(range(0, 2 * ell + 1, 2))
        eigenvalues = tuple(k * (k + 1) for k in degrees)
        target = 2 * ell * (ell + 1)
        resonances = tuple(
            k for k in degrees if k * (k + 1) == target
        )
        assert (degrees, eigenvalues, target) == expected[ell]
        assert resonances == ()
        rows.append(S2Row(ell, degrees, eigenvalues, target, resonances))
    print("S^2 low-degree product table: PASS (ell=1,...,6; no additive resonance)")
    return rows


def generalized_pell_audit() -> None:
    hits: list[tuple[int, int, int]] = []
    for dimension in range(2, 13):
        for ell in range(1, 13):
            target = 2 * ell * (ell + dimension - 2)
            for degree in range(0, 2 * ell + 1, 2):
                if degree * (degree + dimension - 2) == target:
                    hits.append((dimension, ell, degree))
    assert hits == [(4, 4, 6), (6, 8, 12), (8, 12, 18), (9, 5, 8)]

    x, y = 1, 1
    prefix: list[tuple[int, int]] = []
    for _ in range(4):
        x, y = 3 * x + 4 * y, 2 * x + 3 * y
        degree, ell = x - 1, y - 1
        assert degree * (degree + 2) == 2 * ell * (ell + 2)
        prefix.append((ell, degree))
    assert prefix[:3] == [(4, 6), (28, 40), (168, 238)]
    print(f"generalized Pell resonance audit: PASS; bounded hits={hits}")


def workflow_regex_self_test() -> None:
    placeholder = re.compile(
        r"(^|[^A-Za-z0-9_])(sorry|admit|sorryAx)([^A-Za-z0-9_]|$)"
    )
    axiom = re.compile(
        r"^[ \t]*(axiom|axioms)([ \t]|$)", re.MULTILINE
    )
    assert placeholder.search("theorem t : True := by sorry")
    assert placeholder.search("#print axioms Foo.sorryAx")
    assert axiom.search("axiom forbidden : Prop")
    assert axiom.search("axioms forbidden1 forbidden2 : Prop")
    assert not axiom.search("#print axioms permittedInspection")
    assert not axiom.search("theorem axiomName : True := by trivial")
    print("workflow axiom/axioms regex self-test: PASS")


def main() -> None:
    print("Prompt 2 corrective closeout exact audit")
    regular_simplex_audit()
    signed_pentagon_audit()
    centered_product_algebra_audit()
    boolean_square_audit()
    s2_low_degree_table_audit()
    generalized_pell_audit()
    workflow_regex_self_test()
    print("Prompt 2 corrective closeout audit: PASS")


if __name__ == "__main__":
    main()
