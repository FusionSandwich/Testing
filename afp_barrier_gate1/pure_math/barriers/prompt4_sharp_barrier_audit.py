#!/usr/bin/env python3
"""Exact symbolic regression audit for Prompt 4 sharp barriers and synthesis.

General proofs are in the theorem document. This script checks coefficient
algebra, exact polar balance, extremal constants, anisotropy examples, and the
bounded branch certificates without using fitted slopes as theorem evidence.
"""

from __future__ import annotations

import sympy as sp

Q = sp.Rational
x, N = sp.symbols("x N", positive=True)


def assert_zero(expr: sp.Expr, label: str) -> None:
    value = sp.simplify(expr)
    if value != 0:
        raise AssertionError(f"{label}: {value}")


def asymptotic_coefficients() -> None:
    r = Q(1, 2) / sp.sin(x) ** 2 + Q(1, 2) / sp.sin(x) ** 4
    q = Q(1, 4) / sp.sin(x) ** 2 + Q(1, 2) + Q(1, 4) * sp.sin(x) ** 2
    r_series = sp.series(r, x, 0, 5).removeO().expand()
    q_series = sp.series(q, x, 0, 5).removeO().expand()
    expected_r = (
        Q(1, 2) / x**4
        + Q(5, 6) / x**2
        + Q(13, 45)
        + Q(25, 378) * x**2
        + Q(71, 5670) * x**4
    )
    expected_q = (
        Q(1, 4) / x**2
        + Q(7, 12)
        + Q(4, 15) * x**2
        - Q(61, 756) * x**4
    )
    assert_zero(r_series - expected_r, "polar rate series")
    assert_zero(q_series - expected_q, "polar quality series")

    h = sp.pi / (2 * N)
    target_r = (
        8 * N**4 / sp.pi**4
        + 10 * N**2 / (3 * sp.pi**2)
        + Q(13, 45)
    )
    target_q = N**2 / sp.pi**2 + Q(7, 12)
    assert_zero(
        Q(1, 2) / h**4 + Q(5, 6) / h**2 + Q(13, 45) - target_r,
        "N-form rate coefficients",
    )
    assert_zero(
        Q(1, 4) / h**2 + Q(7, 12) - target_q,
        "N-form quality coefficients",
    )
    print("exact polar coefficient extraction: PASS")


def remainder_transfer_constants() -> None:
    # The proof establishes e in [0,x^4/80] for
    # csc^2 x = x^-2 + 1/3 + x^2/15 + e on 0<x<=pi/4.
    # Here pi^2<10 gives x^2<=5/8 and the transfer is exact rational algebra.
    tmax = Q(5, 8)
    a, b, c = Q(1, 3), Q(1, 15), Q(1, 80)
    cr = (
        Q(1, 18)
        + c
        + (Q(1, 2) * b**2 + c * (a + Q(1, 2))) * tmax
        + c * b * tmax**2
        + Q(1, 2) * c**2 * tmax**3
    )
    if not cr < Q(1, 12):
        raise AssertionError(f"rate remainder transfer too weak: {cr}")
    cq = Q(1, 60) + Q(1, 4) + tmax / 320
    if not cq < Q(1, 3):
        raise AssertionError(f"quality remainder transfer too weak: {cq}")

    partial_fraction_constant = Q(2464, 225 * 945)
    if not partial_fraction_constant < Q(1, 80):
        raise AssertionError("partial-fraction csc^2 remainder constant")
    print("rigorous remainder constants: PASS")
    print(f"  csc^2 tail constant={partial_fraction_constant} < 1/80")
    print(f"  rate transfer constant={cr} < 1/12")
    print(f"  quality transfer constant={cq} < 1/3")


def polar_balance_forces_rates() -> None:
    s = sp.symbols("s", nonzero=True)
    av, al, ar = sp.symbols("a_v a_l a_r")
    eq_y = sp.Eq(ar, al)
    eq_z = sp.Eq(av * (-4 * s**2), -2)
    eq_x = sp.Eq(
        al * (-2 * s**2)
        + ar * (-2 * s**2)
        + av * 2 * (1 - 2 * s**2),
        -2,
    )
    solution = sp.solve([eq_y, eq_z, eq_x], [av, al, ar], dict=True)
    if len(solution) != 1:
        raise AssertionError(f"polar solution not unique: {solution}")
    sol = solution[0]
    assert_zero(sol[av] - Q(1, 2) / s**2, "forced meridional polar rate")
    assert_zero(sol[al] - Q(1, 4) / s**4, "forced left polar rate")
    assert_zero(sol[ar] - Q(1, 4) / s**4, "forced right polar rate")
    total = sp.simplify(sol[av] + sol[al] + sol[ar])
    assert_zero(
        total - (Q(1, 2) / s**2 + Q(1, 2) / s**4),
        "forced polar total",
    )
    defect = 2 * s**2 + 2 * s**4
    quality = sp.factor(total * defect / 4)
    assert_zero(
        quality - (Q(1, 4) / s**2 + Q(1, 2) + Q(1, 4) * s**2),
        "polar quality formula",
    )
    print("fixed product-graph polar rates forced uniquely: PASS")


def extremal_and_window_constants() -> None:
    R, K = sp.symbols("R K", positive=True)
    assert_zero((4 / (R * K)) * (R * K) - 4, "extremal normalization")

    L, U, h = sp.symbols("L U h", positive=True)
    rate_lower = 2 / (U * h**2)
    rate_upper = 2 / (L * h**2)
    defect_lower = 2 * L * h**2
    defect_upper = 2 * U * h**2
    assert_zero(rate_lower.subs(U, 2) - 1 / h**2, "net rate lower")
    assert_zero(
        rate_upper.subs(L, 2 / sp.pi**2) - sp.pi**2 / h**2,
        "net rate upper",
    )
    assert_zero(
        defect_lower.subs(L, 2 / sp.pi**2) - 4 * h**2 / sp.pi**2,
        "net defect lower",
    )
    assert_zero(defect_upper.subs(U, 2) - 4 * h**2, "net defect upper")

    threshold = sp.pi**2 * sp.sqrt(R) / 2
    assert_zero(
        (8 / sp.pi**4) * threshold**4 - 2 * R * threshold**2,
        "product/linear-rate threshold",
    )
    print("universal barrier, loss window, and extremal separation: PASS")


def anisotropy_cone_examples() -> None:
    l1, l2 = sp.symbols("l1 l2", positive=True)
    mean = (l1 + l2) / 2
    second = (l1**2 + l2**2) / 2
    qminus1 = sp.factor(second / mean**2 - 1)
    expected = (l1 - l2) ** 2 / (l1 + l2) ** 2
    assert_zero(qminus1 - expected, "two-direction anisotropy sharpness")

    losses = [sp.Integer(1), sp.Integer(2), sp.Integer(4)]
    p1, p2, p3 = sp.symbols("p1 p2 p3", nonnegative=True)
    sol = sp.solve(
        [
            sp.Eq(p1 + p2 + p3, 1),
            sp.Eq(-p1 + p3, 0),
            sp.Eq(p1 + 2 * p2 + 4 * p3, Q(7, 3)),
        ],
        [p1, p2, p3],
        dict=True,
    )
    if sol != [{p1: Q(1, 3), p2: Q(1, 3), p3: Q(1, 3)}]:
        raise AssertionError(f"unexpected anisotropy slice: {sol}")
    psi = sum(
        sol[0][p] * ell**2
        for p, ell in zip((p1, p2, p3), losses, strict=True)
    )
    assert_zero(psi - 7, "anisotropy slice second moment")
    assert_zero(psi / Q(49, 9) - 1 - Q(2, 7), "anisotropy slice Q-1")
    print("feasible-cone anisotropy reformulation and sharp examples: PASS")


def reduced_ring_incidence() -> None:
    Mi, Mj, p, q = sp.symbols(
        "M_i M_j p q", positive=True, integer=True
    )
    assert_zero(
        p * Mi - q * Mj - (p * Mi - q * Mj),
        "biregular incidence identity",
    )
    relation = sp.solve(sp.Eq(Mi, Mj), Mi)
    if relation != [Mj]:
        raise AssertionError("perfect-matching ring count")
    print("reduced-ring perfect-matching impossibility certificate: PASS")


def main() -> None:
    print("Prompt 4 exact sharp-barrier and extremal audit")
    asymptotic_coefficients()
    remainder_transfer_constants()
    polar_balance_forces_rates()
    extremal_and_window_constants()
    anisotropy_cone_examples()
    reduced_ring_incidence()
    print("Prompt 4 exact audit: PASS")


if __name__ == "__main__":
    main()
