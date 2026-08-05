#!/usr/bin/env python3
"""Exact rational finite-h enclosure for the separate first polar row."""

from fractions import Fraction as F

import sympy as sp


def literal_matrix() -> None:
    h, u, v = sp.symbols("h u v", positive=True)
    a = sp.Rational(4, 3)
    s, c = sp.sin(a * h), sp.cos(a * h)
    values = (u, v)
    A = sp.zeros(3, 3)
    A[:, 0] = sp.Matrix(
        [sp.sin(h) / h, sp.sin(h) * (1 - sp.cos(h)) / h**3, sp.sin(h) ** 2 / h**2]
    )
    for column, loss in enumerate(values, 1):
        A[0, column] = -2 * s * c * loss / h
        A[1, column] = -2 * s**3 * c * loss**2 / h**3
        A[2, column] = 2 * s**2 * (c**2 * loss**2 - (2 * loss - loss**2)) / h**2
    b = sp.Matrix(
        [sp.sin(a * h) / h, sp.sin(a * h) * (1 - sp.cos(a * h)) / h**3, -sp.sin(a * h) ** 2 / h**2]
    )
    A0 = A.applyfunc(lambda value: sp.simplify(sp.limit(value, h, 0)))
    b0 = b.applyfunc(lambda value: sp.simplify(sp.limit(value, h, 0)))
    assert sp.factor(A0.det()) == 4 * a**3 * u * v * (a - 1) * (2 * a + 1) * (u - v)
    solution = A0.inv() * b0
    expected = sp.Matrix(
        [
            2 * a**3 / ((a - 1) * (2 * a + 1)),
            -(a + 1) * (2 * a + 2 * v - 3) / (4 * u * (a - 1) * (2 * a + 1) * (u - v)),
            (a + 1) * (2 * a + 2 * u - 3) / (4 * v * (a - 1) * (2 * a + 1) * (u - v)),
        ]
    )
    assert all(sp.simplify(x - y) == 0 for x, y in zip(solution, expected))


def main() -> None:
    literal_matrix()
    a = F(4, 3)
    u_lo, u_hi = F(1, 20), F(1, 10)
    v_lo, v_hi = F(1, 2), F(2, 3)
    radius = F(1, 100)
    h_actual = F(44, 7 * 2**80)  # 2*pi/M0 with pi<22/7

    # Rounding is much smaller than 1/1000.  Taylor bounds on the two
    # enclosing angle intervals imply the u,v boxes used by literal_matrix.
    assert F(22, 7 * 2**80) < F(1, 1000)
    d1_lo, d1_hi = F(3, 8) - F(1, 1000), F(3, 8) + F(1, 1000)
    d2_lo, d2_hi = F(9, 8) - F(1, 1000), F(9, 8) + F(1, 1000)
    assert d1_lo**2 / 2 - d1_hi**4 / 24 > u_lo
    assert d1_hi**2 / 2 < u_hi
    assert d2_lo**2 / 2 - d2_hi**4 / 24 > v_lo
    assert d2_hi**2 / 2 < v_hi

    # On |h|<=1/100, every argument is <1/70.  The entire sinc/cosc
    # quotients and cosine are bounded by 2 using exp(|z|)<2.
    assert a * radius < F(1, 70)
    assert 1 / (1 - F(1, 70)) < 2

    # Literal normalized 3x3 entries, row by row, are bounded as follows:
    # force: S(h), -2a S(ah)cos(ah)u;
    # loss: .5 S(h)C(h), -2a^3 S(ah)^3 cos(ah)u^2;
    # isotropy: S(h)^2 and
    #   2a^2 S(ah)^2[cos(ah)^2u^2-(2u-u^2)].
    force_bound = max(F(2), 2 * a * 2 * 2)
    loss_bound = max(F(2), 2 * a**3 * 2**3 * 2)
    iso_bound = max(F(4), 2 * a**2 * 2**2 * (4 + 3))
    matrix_disk = max(force_bound, loss_bound, iso_bound)
    assert matrix_disk < 110
    rhs_disk = max(2 * a, 2 * a**3, 4 * a**2)
    assert rhs_disk < 8

    derivative_A = 2 * F(110) / radius
    derivative_b = 2 * F(8) / radius
    assert derivative_A == 22_000
    assert derivative_b == 1_600

    # Exact determinant of the h=0 matrix is
    # 4 a^3 u v (a-1)(2a+1)(u-v).  Its absolute value on the box is
    # at least the following rational number.  Direct inspection of the
    # printed adjugate bounds every entry by 512, hence ||A0^-1||inf<2e4.
    det_lower = 4 * a**3 * u_lo * v_lo * (a - 1) * (2 * a + 1) * (v_lo - u_hi)
    assert det_lower == F(704, 6075)
    assert 3 * 512 / det_lower < 20_000

    operator_perturbation = 20_000 * 3 * derivative_A * h_actual
    assert operator_perturbation < F(1, 10**12)
    inverse_finite = F(20_000, 1) / (1 - operator_perturbation)
    # ||z0||inf<64 on the box.  Apply the resolvent identity literally.
    displacement = inverse_finite * (derivative_b * h_actual + 3 * derivative_A * h_actual * 64)
    assert displacement < F(1, 10**6)
    assert displacement < F(1, 20)
    print("short-gap first-polar-row Cauchy guard: PASS")


if __name__ == "__main__":
    main()
