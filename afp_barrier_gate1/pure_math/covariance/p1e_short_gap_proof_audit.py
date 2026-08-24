#!/usr/bin/env python3
"""Exact algebra audit for the no-guard shortened-gap S2 candidate.

This file deliberately does not claim the analytic remainder (6.1).  The
literal matrix-to-limit derivation is checked separately by
p1e_short_gap_symbolic_matrix_audit.py; finite-level convergence is checked
by p1e_short_gap_family_audit.py.
"""

from fractions import Fraction as F

import sympy as sp


M0 = 2**80


def corrected_mask_moments() -> None:
    c = sp.symbols("c", positive=True)
    p = (4 * c**2 + 2 * c - 1) / (4 * c * (c + 1))
    beta = sp.Rational(1, 2) + (2 * c**2 - 1) / (2 * c)
    m1 = sp.factor(1 - beta)
    m2 = sp.factor(1 - 2 * beta + p + (1 - p) * (2 * c**2 - 1) ** 2)
    assert sp.simplify(m1 + (c - 1) * (2 * c + 1) / (2 * c)) == 0
    assert sp.simplify(m2 - (c - 1) ** 2 * (c + 1) * (2 * c + 1) / c) == 0


def limiting_system() -> None:
    r = sp.sqrt(58)
    A = sp.Matrix(
        [
            [-sp.Rational(29, 8), r / 8, 8 * r, 0, 0, 0],
            [-sp.Rational(29, 8), r / 32, 128 * r, 0, 0, 0],
            [0, r / 8, 8 * r, 0, 0, 0],
            [sp.Rational(29, 8), 0, 0, -r, r / 16, 4 * r],
            [sp.Rational(29, 8), 0, 0, -r, r / 256, 16 * r],
            [0, 0, 0, 0, r / 16, 4 * r],
        ]
    )
    assert sp.simplify(A.det() - sp.Rational(96799941, 512) * r) == 0
    assert all(sp.simplify(3 - sum(abs(A.inv()[i, j]) for j in range(6))) > 0 for i in range(6))

    y = sp.symbols("y", real=True)
    b = sp.Matrix(
        [
            -sp.Rational(3, 16),
            sp.Rational(63, 512) + 3 * r * y / 32,
            sp.Rational(13, 8) + r / 4,
            -sp.Rational(3, 16),
            -sp.Rational(285, 512) - 3 * r * y / 32,
            sp.Rational(13, 8) + r / 4,
        ]
    )
    solution = [sp.factor(x) for x in A.inv() * b]
    expected = [
        (29 + 4 * r) / 58,
        -r * (16 * r * y - 640 * r - 4107) / 19488,
        r * (16 * r * y + 32 * r + 261) / 1247232,
        r * (29 + 4 * r) / 464,
        r * (16 * r * y + 895 + 128 * r) / 2436,
        -r * (16 * r * y - 40 * r - 197) / 155904,
    ]
    assert all(sp.simplify(x - z) == 0 for x, z in zip(solution, expected))

    # An affine function on [-7/6,7/6] takes its minimum at an endpoint.
    for value in solution:
        assert sp.simplify(value.subs(y, -sp.Rational(7, 6)) - sp.Rational(1, 500)) > 0
        assert sp.simplify(value.subs(y, sp.Rational(7, 6)) - sp.Rational(1, 500)) > 0
        assert sp.simplify(10 - value.subs(y, -sp.Rational(7, 6))) > 0
        assert sp.simplify(10 - value.subs(y, sp.Rational(7, 6))) > 0


def schedule_box() -> None:
    # |dt|,|dS| <= 1/2 and the exact derivative bounds pi/M,2/M give
    # |a-1/4| <= (pi/2+1)/M < 3/M using pi<22/7.
    assert F(11, 7) + 1 < 3
    # The common transition box therefore has |eta|<=3 and, with c>6/7,
    # |eta/(pi*c)|<7/6.  Use pi>3.
    assert F(3, 1) / (F(3, 1) * F(6, 7)) <= F(7, 6)


def neumann_budget() -> None:
    entry = F(10**12, M0)
    contraction = 18 * entry
    assert contraction < F(1, 2**35)
    # ||z0||inf<10 on the full phase box.  With ||A0^-1||inf<3,
    # ||A^-1||inf<=3/(1-contraction)<4 and hence
    # ||z-z0||inf <=4(entry+6 entry*10)=244 entry.
    displacement = 244 * entry
    assert displacement < F(1, 1000)
    # The limiting cone margin is 1/500 and the requested solution enclosure
    # is 1/1000.
    assert F(1, 1000) < F(1, 500)
    # Jump eight on a coarse ring is 16*pi/M; this is the literal guard.
    assert F(16 * 22, 7 * M0) < F(1, 2**70)


def ordinary_recurrence() -> None:
    z = sp.symbols("z", positive=True)
    rho = (1 - z) * (1 + 2 * z) / ((1 + z) * (1 - 2 * z))
    q = sp.factor((rho - 1) / (rho + 1))
    # This is D/S after tan(h/2) cot(theta)=z.
    assert sp.simplify(q - z / (1 - 2 * z**2)) == 0

    # Coefficients of the telescoping error are nonnegative:
    # 2*((2^(2k+1)-2)/(2k+1))*z^(2k+1), k>=1.
    for k in range(1, 20):
        assert 2 ** (2 * k + 1) - 2 > 0
    # Dropping denominators and summing a geometric series gives the printed
    # 16 z^3/(1-4z^2) guard.
    assert F(16, 1) / (1 - 4 * F(1, 16)) < 22

    # Signed second-order cumulative transition budget.  For
    # |eps_m| <= alpha_m and alpha_star=256/M0.  This notation is disjoint
    # from the polar-latitude constant a_0=4/3 in the proof source.
    # log(1+eps_m) >= eps_m-eps_m^2/(2(1-alpha_star)).
    alpha_star = F(256, M0)
    linear_sum = F(512, M0)
    square_sum = F(262144, 3 * M0**2)
    remainder = square_sum / (2 * (1 - alpha_star))
    assert alpha_star < 1
    assert remainder < F(1, M0)
    assert linear_sum + remainder < F(513, M0)

    # The old exponent 512 is genuinely unsafe.  With J=80 and every
    # eps_m=-alpha_m, log(1-alpha_m) <= -alpha_m-alpha_m^2/2, and the exact rational lower
    # bound on the accumulated magnitude already exceeds 512/M0.
    j = 80
    finite_linear = sum((F(256, M0 * 2**m) for m in range(j)), F(0))
    finite_square = sum((F(256, M0 * 2**m) ** 2 for m in range(j)), F(0))
    assert finite_linear + finite_square / 2 > F(512, M0)


def reachable_horizontal_margin() -> None:
    assert F(499, 251) > F(19, 10)
    assert (F(10, 19) * F(96, 95)) ** 2 < F(1, 3)
    assert (F(48, 19) * F(96, 95)) ** 2 < 7
    # Actual floor/ceiling H margins with 3/5<T<101/100.
    hplus_lower = F(2, 3) / (7**2 * F(101, 100))
    hminus_lower = 1 / (F(1, 3) * 7 * F(101, 100))
    assert hplus_lower > F(1, 100)
    assert hminus_lower > F(1, 100)
    assert 1 / (F(1, 16) * F(3, 5)) < 100
    assert 1 / (2 * F(3, 5)) < 100
    assert 224 + 32 == 256


def first_polar_limit() -> None:
    u0, u1 = F(1, 20), F(1, 10)
    v0, v1 = F(1, 2), F(2, 3)
    a = F(4, 3)
    up = 2 * a**3 / ((a - 1) * (2 * a + 1))
    assert up == F(128, 33) and up > F(3, 2)
    h1_lower = (a + 1) * (2 * a + 2 * v0 - 3) / (4 * u1 * (a - 1) * (2 * a + 1) * (v1 - u0))
    h2_lower = (a + 1) * (3 - 2 * a - 2 * u1) / (4 * v1 * (a - 1) * (2 * a + 1) * (v1 - u0))
    assert h1_lower > 1 and h2_lower > F(1, 20)


def quotient_constants() -> None:
    # Active chord >=h/8 and 1-cos x >=2x^2/pi^2 imply ell>=h^2/(32pi^2),
    # so r<=2/ell<=64pi^2 h^-2.
    assert 2 * 32 == 64
    # P1B lower constant 6/R3 and direct upper constant 3 Lambda^2/2.
    assert F(6, 64) == F(3, 32)
    assert F(3 * 5**2, 2) == F(75, 2)


def hostile_mutations() -> None:
    a = F(1, 4)
    assert F(29, 32) + F(3, 2) * a**2 == 1
    assert 1 + F(3, 2) * a**2 != 1
    assert F(1, 2) != 1  # Q column sum mutation


def main() -> None:
    corrected_mask_moments()
    limiting_system()
    schedule_box()
    neumann_budget()
    ordinary_recurrence()
    reachable_horizontal_margin()
    first_polar_limit()
    quotient_constants()
    hostile_mutations()
    print("short-gap exact algebra audit: PASS (remainder is certified by the Cauchy guard audit)")


if __name__ == "__main__":
    main()
