#!/usr/bin/env python3
"""Hostile exact audit of the short-gap Cauchy guards.

This audit is independent of the finite-level regressions.  It checks the
algebra behind the cancellation-free transition columns, the removable RHS
quotients, and the first-polar-row inverse budget.  Rational inequalities are
used for every numerical constant.
"""

from fractions import Fraction as F

import sympy as sp


def transition_column_factorization() -> None:
    """Verify (4.8)--(4.9) against the literal row equations."""

    r, lam, base, c0, neigh, m1n, m2n = sp.symbols(
        "r lam base c0 neigh m1n m2n", nonzero=True
    )
    s = sp.symbols("s", nonzero=True)
    z = lam * s * r
    gap_sin = sp.sin(z)
    gap_loss = 1 - sp.cos(z)
    m1 = r**2 * m1n
    m2 = r**4 * m2n
    bs = base * s
    ns = neigh * s

    literal_out = sp.Matrix(
        [
            gap_sin - c0 * ns * m1,
            gap_sin * gap_loss
            + (gap_sin * bs * ns - c0 * ns * gap_loss) * m1
            - c0 * bs * ns**2 * m2,
            gap_sin**2
            - 2 * gap_sin * c0 * ns * m1
            + ns**2 * ((1 + c0**2) * m2 - 2 * m1),
        ]
    )
    literal_in = sp.Matrix(
        [
            -gap_sin - c0 * ns * m1,
            -gap_sin * gap_loss
            + (-gap_sin * bs * ns - c0 * ns * gap_loss) * m1
            - c0 * bs * ns**2 * m2,
            gap_sin**2
            + 2 * gap_sin * c0 * ns * m1
            + ns**2 * ((1 + c0**2) * m2 - 2 * m1),
        ]
    )
    scales = sp.diag(1 / (s * r), 1 / (s**3 * r**3), 1 / (s**2 * r**2))
    out = sp.simplify(scales * literal_out)
    incoming = sp.simplify(scales * literal_in)

    sinc = sp.sin(z) / z
    cosc = 2 * (1 - sp.cos(z)) / z**2
    expected_out = sp.Matrix(
        [
            lam * sinc - c0 * neigh * r * m1n,
            lam**3 * sinc * cosc / 2
            + neigh
            * (lam * base * sinc * m1n - c0 * lam**2 * cosc * r * m1n / 2)
            - c0 * base * neigh**2 * r * m2n,
            lam**2 * sinc**2
            - 2 * lam * c0 * neigh * sinc * r * m1n
            + neigh**2 * ((1 + c0**2) * r**2 * m2n - 2 * m1n),
        ]
    )
    expected_in = sp.Matrix(
        [
            -lam * sinc - c0 * neigh * r * m1n,
            -lam**3 * sinc * cosc / 2
            + neigh
            * (-lam * base * sinc * m1n - c0 * lam**2 * cosc * r * m1n / 2)
            - c0 * base * neigh**2 * r * m2n,
            lam**2 * sinc**2
            + 2 * lam * c0 * neigh * sinc * r * m1n
            + neigh**2 * ((1 + c0**2) * r**2 * m2n - 2 * m1n),
        ]
    )
    assert all(sp.simplify(a - b) == 0 for a, b in zip(out, expected_out))
    assert all(sp.simplify(a - b) == 0 for a, b in zip(incoming, expected_in))

    u = sp.symbols("u")
    literal_horizontal = sp.Matrix(
        [
            -2 * bs * c0 * u,
            -2 * bs**3 * c0 * u**2,
            2 * bs**2 * (c0**2 * u**2 - (2 * u - u**2)),
        ]
    )
    U = sp.symbols("U")
    c = sp.symbols("c", nonzero=True)
    normalized = sp.diag(
        1 / (s * c * r**2), 1 / (s**3 * c * r**4), 1 / (s**2 * r**2)
    ) * literal_horizontal.subs(u, r**2 * U)
    expected_horizontal = sp.Matrix(
        [
            -2 * base * c0 * U / c,
            -2 * base**3 * c0 * U**2 / c,
            2 * base**2 * (-2 * U + r**2 * (1 + c0**2) * U**2),
        ]
    )
    assert all(
        sp.simplify(a - b) == 0 for a, b in zip(normalized, expected_horizontal)
    )


def transition_disk_budget() -> None:
    """Recheck every semantic disk constant, including all RHS rows."""

    radius = F(1, 10_000)
    x_actual = F(1, 2**80)
    a_lo, a_hi = F(249, 1000), F(251, 1000)
    c_lo = F(6, 7)
    pi_lo, pi_hi = F(3), F(22, 7)

    assert F(1, 4) - 3 * radius > a_lo
    assert F(1, 4) + 3 * radius < a_hi
    rmax = pi_hi * radius / a_lo
    alphamax = pi_hi * radius
    assert rmax < F(1, 700)
    assert 16 * alphamax < F(1, 180)
    assert 1 - alphamax**2 > F(9, 10)

    # Cancellation-free mask bounds.  For complex alpha,
    # |1-cos(alpha)|<=|alpha|^2, |cos(alpha)|>=1-|alpha|^2.
    assert F(5, 2) / F(9, 10) < 3
    assert 15 / F(9, 10) < 17
    assert 3 * a_hi**2 < 1
    assert 17 * a_hi**4 < 1

    # The cancellation-free sine ratios are
    # n_c+=cos(gsr)+c*g*r*sinc(gsr),
    # n_c-=cos(sr)-c*r*sinc(sr), and
    # n_f+=cos((g+1)sr)+c*(g+1)r*sinc((g+1)sr).
    # With |cos|,|sinc|<=2 and g<1 these are bounded by 3,3,3.
    assert 2 + 2 * rmax < 3
    assert 2 + 4 * rmax < 3
    # The submitted value 7 is therefore conservative.
    neigh = F(7)
    base = F(3)
    cosine = F(3)
    m1n = m2n = F(1)
    sinc = cosc = F(2)

    force = sinc + cosine * neigh * rmax * m1n
    loss = (
        sinc * cosc / 2
        + neigh * (base * sinc * m1n + cosine * cosc * rmax * m1n / 2)
        + cosine * base * neigh**2 * rmax * m2n
    )
    isotropy = (
        sinc**2
        + 2 * cosine * neigh * sinc * rmax * m1n
        + neigh**2 * ((1 + cosine**2) * rmax**2 * m2n + 2 * m1n)
    )
    assert force < 3
    assert loss < 45
    assert isotropy < 103

    # Coarse jump eight is the largest horizontal argument: 16*pi*x.
    # Hence U=|(1-cos z)/r^2| <= (16|a|)^2 < 17.
    U = F(17)
    assert (16 * a_hi) ** 2 < U
    c_ratio = F(7, 2)
    horizontal = (
        2 * base * c_ratio * U,
        2 * base**3 * c_ratio * U**2,
        2 * base**2 * (2 * U + (1 + cosine**2) * rmax**2 * U**2),
    )
    assert horizontal[0] < 400
    assert horizontal[1] < 55_000
    assert horizontal[2] < 700

    # Transition matrix columns include at most the E multiplier 2*sqrt(58)<16.
    assert 16 * max(force, loss, isotropy, *horizontal) < 1_000_000

    # Only force and loss RHS rows have a 1/(c*r) quotient.  On |x|=R,
    # this reciprocal is at most the following number.  Each baseline uses
    # two radial columns whose coefficient sum is <3.
    inv_cr = a_hi / (c_lo * pi_lo * radius)
    assert inv_cr < 1000
    rhs_force = 16 * 3 * force * inv_cr
    rhs_loss = 16 * 3 * loss * inv_cr
    # Isotropy is divided by h^2, not h^2*cot(theta), so it has no pole.
    rhs_iso = 16 * 3 * isotropy
    assert max(rhs_force, rhs_loss, rhs_iso) < 10_000_000

    # The exact zero of each force/loss numerator at x=0 is supplied by the
    # literal symbolic limit audit.  All other possible denominators are
    # guarded by a, c, and cos(alpha), so the quotients are holomorphic after
    # filling in that value.  Maximum modulus and Cauchy then give:
    assert x_actual < radius / 2
    dA = F(2_000_000) / radius
    db = F(20_000_000) / radius
    assert dA == 20_000_000_000
    assert db == 200_000_000_000
    assert dA < 10**12 and db < 10**12


def polar_inverse_budget() -> None:
    """Prove the first-row adjugate and limiting-solution bounds rationally."""

    a = F(4, 3)
    ulo, uhi = F(1, 20), F(1, 10)
    vlo, vhi = F(1, 2), F(2, 3)

    # At h=0 the three U-column entries are <=1.  Every horizontal entry is
    # bounded by 3: force <=2*a, loss <=2*a^3, and isotropy
    # 4*a^2*t(1-t)<=a^2 for 0<t<1.  Thus each 2x2 adjugate entry is <18.
    assert 2 * a < 3
    assert 2 * a**3 < 5  # the loss also carries t^2<=4/9, giving <3 below
    assert 2 * a**3 * vhi**2 < 3
    assert a**2 < 3
    adj_entry = F(18)
    det_lower = 4 * a**3 * ulo * vlo * (a - 1) * (2 * a + 1) * (vlo - uhi)
    assert det_lower == F(704, 6075)
    inverse_inf = 3 * adj_entry / det_lower
    assert inverse_inf < 500
    assert inverse_inf < 20_000

    # Direct rational bounds for the limiting solution printed in (8.5)--(8.6).
    up = 2 * a**3 / ((a - 1) * (2 * a + 1))
    h1_upper = (a + 1) * (2 * a + 2 * vhi - 3) / (
        4 * ulo * (a - 1) * (2 * a + 1) * (vlo - uhi)
    )
    h2_upper = (a + 1) * (3 - 2 * a - 2 * ulo) / (
        4 * vlo * (a - 1) * (2 * a + 1) * (vlo - uhi)
    )
    assert max(up, h1_upper, h2_upper) < 64

    # Recheck the Cauchy/resolvent arithmetic with the submitted loose inverse.
    h_actual = F(44, 7 * 2**80)
    dA, db = F(22_000), F(1_600)
    contraction = 20_000 * 3 * dA * h_actual
    assert contraction < F(1, 10**12)
    inverse_finite = F(20_000) / (1 - contraction)
    displacement = inverse_finite * (db * h_actual + 3 * dA * h_actual * 64)
    assert displacement < F(1, 10**6)


def main() -> None:
    transition_column_factorization()
    transition_disk_budget()
    polar_inverse_budget()
    print("short-gap hostile Cauchy/first-row audit: ACCEPT")


if __name__ == "__main__":
    main()
