#!/usr/bin/env python3
"""Derive the normalized transition limit from the literal exact formulas.

This is intentionally slower than the rational constant audit.  It prevents
the displayed 6x6 matrix from drifting away from the row formula, affine
reparameterization, row scaling, Q column factor, or fixed-gap phase term.
It proves the removable limit exactly in SymPy; it does not prove the uniform
O(1/M) remainder enclosure.
"""

import sympy as sp


def radial(s, c, sn, gap, m1, m2, outgoing):
    loss = 1 - sp.cos(gap)
    if outgoing:
        return sp.Matrix(
            [
                sp.sin(gap) - c * sn * m1,
                sp.sin(gap) * loss
                + (sp.sin(gap) * s * sn - c * sn * loss) * m1
                - c * s * sn**2 * m2,
                sp.sin(gap) ** 2
                - 2 * sp.sin(gap) * c * sn * m1
                + sn**2 * ((1 + c**2) * m2 - 2 * m1),
            ]
        )
    return sp.Matrix(
        [
            -sp.sin(gap) - c * sn * m1,
            -sp.sin(gap) * loss
            + (-sp.sin(gap) * s * sn - c * sn * loss) * m1
            - c * s * sn**2 * m2,
            sp.sin(gap) ** 2
            + 2 * sp.sin(gap) * c * sn * m1
            + sn**2 * ((1 + c**2) * m2 - 2 * m1),
        ]
    )


def horizontal(s, c, delta, jump):
    u = 1 - sp.cos(jump * delta)
    return sp.Matrix(
        [-2 * s * c * u, -2 * s**3 * c * u**2, 2 * s**2 * (c**2 * u**2 - (2 * u - u**2))]
    )


def main() -> None:
    t, eta, c, s = sp.symbols("t eta c s", real=True, positive=True)
    a = sp.Rational(1, 4) + eta * t
    gap_ratio = sp.sqrt(sp.Rational(29, 32))
    alpha = sp.pi * t
    h = sp.pi * s * t / a
    ca = sp.cos(alpha)
    p = (4 * ca**2 + 2 * ca - 1) / (4 * ca * (ca + 1))
    beta = sp.Rational(1, 2) + sp.cos(2 * alpha) / (2 * ca)
    m1 = 1 - beta
    m2 = 1 - 2 * beta + p + (1 - p) * sp.cos(2 * alpha) ** 2

    sg, cg = sp.sin(gap_ratio * h), sp.cos(gap_ratio * h)
    sf, cf = s * cg + c * sg, c * cg - s * sg
    sh, ch = sp.sin(h), sp.cos(h)
    sm = s * ch - c * sh
    sfp = sf * ch + cf * sh

    coarse_out = radial(s, c, sf, gap_ratio * h, m1, m2, True)
    coarse_in = radial(s, c, sm, h, 0, 0, False)
    fine_in = radial(sf, cf, s, gap_ratio * h, m1, m2, False)
    fine_out = radial(sf, cf, sfp, h, 0, 0, True)

    raw = sp.zeros(6, 6)
    kappa = h * c / s
    for row in range(3):
        raw[row, 0] = coarse_out[row] * kappa
        raw[row, 1] = horizontal(s, c, 2 * alpha, 1)[row]
        raw[row, 2] = horizontal(s, c, 2 * alpha, 8)[row]
        raw[row + 3, 0] = fine_in[row] * kappa / 2
        raw[row + 3, 3] = fine_out[row] * kappa
        raw[row + 3, 4] = horizontal(sf, cf, alpha, 1)[row]
        raw[row + 3, 5] = horizontal(sf, cf, alpha, 8)[row]

    scales = [1 / (h**2 * c / s), 1 / (h**4 * c / s), 1 / h**2] * 2
    multipliers = [-sp.sqrt(58) / 2, -sp.sqrt(58), -sp.sqrt(58) / 4,
                   -sp.sqrt(58), -2 * sp.sqrt(58), -sp.sqrt(58) / 2]
    normalized = sp.Matrix(6, 6, lambda i, j: raw[i, j] * scales[i] * multipliers[i])
    expected = sp.Matrix(
        [
            [-sp.Rational(29, 8), sp.sqrt(58) / 8, 8 * sp.sqrt(58), 0, 0, 0],
            [-sp.Rational(29, 8), sp.sqrt(58) / 32, 128 * sp.sqrt(58), 0, 0, 0],
            [0, sp.sqrt(58) / 8, 8 * sp.sqrt(58), 0, 0, 0],
            [sp.Rational(29, 8), 0, 0, -sp.sqrt(58), sp.sqrt(58) / 16, 4 * sp.sqrt(58)],
            [sp.Rational(29, 8), 0, 0, -sp.sqrt(58), sp.sqrt(58) / 256, 16 * sp.sqrt(58)],
            [0, 0, 0, 0, sp.sqrt(58) / 16, 4 * sp.sqrt(58)],
        ]
    )
    for i in range(6):
        for j in range(6):
            assert sp.simplify(sp.limit(normalized[i, j], t, 0) - expected[i, j]) == 0

    row_scale = sp.diag(*scales)
    row_mult = sp.diag(*multipliers)
    bc = -row_mult[:3, :3] * row_scale[:3, :3] * (coarse_out / gap_ratio + coarse_in)
    bf = -row_mult[3:, 3:] * row_scale[3:, 3:] * (fine_in / (2 * gap_ratio) + fine_out / 2)
    rhs = list(bc) + list(bf)
    y = eta / (sp.pi * c)
    expected_rhs = [
        -sp.Rational(3, 16),
        sp.Rational(63, 512) + 3 * sp.sqrt(58) * y / 32,
        sp.Rational(13, 8) + sp.sqrt(58) / 4,
        -sp.Rational(3, 16),
        -sp.Rational(285, 512) - 3 * sp.sqrt(58) * y / 32,
        sp.Rational(13, 8) + sp.sqrt(58) / 4,
    ]
    for actual, wanted in zip(rhs, expected_rhs):
        assert sp.simplify(sp.limit(actual, t, 0) - wanted) == 0
    print("short-gap literal symbolic matrix-to-limit audit: PASS")


if __name__ == "__main__":
    main()
