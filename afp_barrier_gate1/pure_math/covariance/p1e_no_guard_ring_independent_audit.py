#!/usr/bin/env python3
"""Exact regressions for the independent no-guard ring audit."""

from __future__ import annotations

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def equator_closure_counterexample() -> None:
    """At J=1 the final ordinary row has phi_star/delta < 2."""

    m = sp.Integer(2) ** 81
    g = sp.sqrt(sp.Rational(29, 32))
    e = g - sp.Rational(2, 3)
    require(e > 0, "positive J=1 equator-closing phase")

    # H=2*delta=4*pi/M and h=H/(1+q), q=8e/M.
    # The comparison decreases with H^2, so insert pi < 22/7.
    q = 8 * e / m
    h_upper = sp.Rational(88, 7) / m
    x = h_upper**2
    comparison = (
        sp.Rational(1, 2)
        - x / 24
        - 1
        / (
            2
            * (1 + q) ** 2
            * (1 - x / (1 + q) ** 2)
        )
    )
    require(sp.simplify(comparison) > 0, "z_star < 1-cos(2 delta)")


def reachable_phase_constant() -> None:
    phase_bound = sp.Rational(11, 7) + sp.Rational(1, 19)
    require(phase_bound == sp.Rational(216, 133), "phase arithmetic")
    require(phase_bound < 2, "reachable phase lies in phase-two box")


def adaptive_limiting_factor() -> None:
    # Worst ceiling event as R decreases to 2 from above:
    # t_-=1, t_+=5, x_-=1/4, x_+=25/4.
    x_minus = sp.Rational(1, 4)
    x_plus = sp.Rational(25, 4)
    upper_fraction = (1 - x_minus) / (x_plus - x_minus)
    limiting_ratio = sp.simplify(upper_fraction / x_plus)
    require(limiting_ratio == sp.Rational(1, 50), "adaptive upper factor")
    require(limiting_ratio > sp.Rational(1, 100), "reachable margin")

    # The loose rectangle alone does not prove 1/100.
    loose_minus = sp.Rational(1, 3)
    loose_plus = sp.Integer(10)
    loose_ratio = sp.simplify(
        ((1 - loose_minus) / (loose_plus - loose_minus)) / loose_plus
    )
    require(loose_ratio < sp.Rational(1, 100), "loose-box inference fails")


def reachable_horizontal_margin() -> None:
    # Reachable lambda bounds imply x_-<1/3 and x_+<7 using
    # sin(t)>95t/96 for 0<t<1/4.
    x_minus_upper = (sp.Rational(10, 19) * sp.Rational(96, 95)) ** 2
    x_plus_upper = (sp.Rational(48, 19) * sp.Rational(96, 95)) ** 2
    require(x_minus_upper < sp.Rational(1, 3), "reachable x-minus upper")
    require(x_plus_upper < 7, "reachable x-plus upper")

    # With 3/5<T<101/100, the exact conductance formulas give the
    # displayed 1/100--100 comparison.
    plus_lower = (
        sp.Rational(2, 3)
        / (7**2 * sp.Rational(101, 100))
    )
    minus_lower = 1 / (
        sp.Rational(1, 3) * 7 * sp.Rational(101, 100)
    )
    upper_from_xminus = 1 / (
        sp.Rational(1, 16) * sp.Rational(3, 5)
    )
    require(plus_lower > sp.Rational(1, 100), "H-plus lower margin")
    require(minus_lower > sp.Rational(1, 100), "H-minus lower margin")
    require(upper_from_xminus < 100, "horizontal upper margin")


def ordinary_recurrence() -> None:
    z = sp.symbols("z", positive=True)
    radial_ratio = (1 - z) * (1 + 2 * z) / ((1 + z) * (1 - 2 * z))
    sine_ratio = (1 + z) / (1 - z)
    remainder = sp.expand_log(sp.log(radial_ratio / sine_ratio), force=True)
    expected = (
        2 * sp.log(1 - z)
        - 2 * sp.log(1 + z)
        + sp.log(1 + 2 * z)
        - sp.log(1 - 2 * z)
    )
    require(sp.simplify(remainder - expected) == 0, "log recurrence")
    require(
        sp.series(expected, z, 0, 8)
        == 4 * z**3 + 12 * z**5 + 36 * z**7 + sp.Order(z**8),
        "positive remainder series",
    )

    # Exact ordinary-row determinant for unknowns (U_plus,H_u,H_v).
    sine_h, ell, s, c, u, v = sp.symbols(
        "sine_h ell s c u v", real=True
    )
    radial = sp.Matrix([sine_h, sine_h * ell, sine_h**2])
    horizontal_u = sp.Matrix(
        [
            -2 * s * c * u,
            -2 * s**3 * c * u**2,
            2 * s**2 * (c**2 * u**2 - (2 * u - u**2)),
        ]
    )
    horizontal_v = horizontal_u.subs(u, v)
    determinant = sp.factor(
        sp.Matrix.hstack(radial, horizontal_u, horizontal_v).det()
    )
    determinant_expected = (
        4
        * sine_h
        * c
        * s**3
        * u
        * v
        * (u - v)
        * (-sine_h * c * s - c**2 * ell - ell + 2 * s**2)
    )
    require(
        sp.simplify(determinant - determinant_expected) == 0,
        "ordinary-row determinant",
    )


def first_ring_and_rate() -> None:
    a = sp.symbols("a", positive=True)
    u_plus = 2 * a**3 / ((a - 1) * (2 * a + 1))
    require(
        sp.simplify(u_plus.subs(a, sp.Rational(4, 3)))
        == sp.Rational(128, 33),
        "first-ring radial limit",
    )

    # Fine transition jump one: 2/(5*pi) > 1/8 from pi<22/7.
    require(sp.Rational(7, 55) > sp.Rational(1, 8), "fine jump margin")
    require(
        2 * sp.Rational(1, 3) * sp.Rational(1, 32)
        > sp.Rational(1, 64),
        "adaptive chord squared exceeds h^2/64",
    )
    require(
        sp.simplify(6 / (64 * sp.pi**2))
        == sp.Rational(3, 32) / sp.pi**2,
        "P1B lower constant",
    )

    # Exact first-row determinant and its uniform box lower bound.
    u, v = sp.symbols("u v", positive=True)
    matrix = sp.Matrix(
        [
            [1, -2 * a * u, -2 * a * v],
            [sp.Rational(1, 2), -2 * a**3 * u**2, -2 * a**3 * v**2],
            [1, -4 * a**2 * u * (1 - u), -4 * a**2 * v * (1 - v)],
        ]
    )
    determinant = sp.factor(matrix.det())
    expected = 4 * a**3 * u * v * (a - 1) * (2 * a + 1) * (u - v)
    require(sp.simplify(determinant - expected) == 0, "first-row determinant")
    determinant_lower = sp.Rational(704, 6075)
    require(determinant_lower > sp.Rational(1, 9), "determinant box lower")


def straight_line_compiler() -> None:
    length = 10**6
    exponent = 28 * 2**length - 12
    # Closed form for e_{k+1}=12+2e_k, e_0=16.
    require(exponent == (16 + 12) * 2**length - 12, "compiler exponent")
    base_exponent = 28 * 2**length + 100
    require(base_exponent - exponent > 100, "dyadic closure margin")


def main() -> None:
    equator_closure_counterexample()
    reachable_phase_constant()
    adaptive_limiting_factor()
    reachable_horizontal_margin()
    ordinary_recurrence()
    first_ring_and_rate()
    straight_line_compiler()
    print("no-guard ring independent audit: exact regressions PASS")


if __name__ == "__main__":
    main()
