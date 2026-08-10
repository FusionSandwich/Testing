#!/usr/bin/env python3
"""Deterministic audit for the shortened-gap 2:1 ring transition.

This is a regression/audit, not a proof by floating-point rank.  The formulas
are the exact spherical row formulas recorded in
P1E_ADAPTIVE_RING_ROUTE_AUDIT.md.  High precision is used so that the output
can be compared with a separate outward-interval implementation.
"""

from __future__ import annotations

import mpmath as mp


mp.mp.dps = 80


def mask_moments(alpha: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    c = mp.cos(alpha)
    p = (4 * c**2 + 2 * c - 1) / (4 * c * (c + 1))
    q = (2 * c + 1) * (4 * c**2 + 2 * c - 1) / (8 * c**2 * (c + 1))
    beta = mp.mpf("0.5") + mp.cos(2 * alpha) / (2 * c)
    ecos2 = p + (1 - p) * mp.cos(2 * alpha) ** 2
    m1 = 1 - beta
    m2 = 1 - 2 * beta + ecos2
    return p, q, m1, m2


def row_matrix(
    theta: mp.mpf,
    h_minus: mp.mpf,
    h_plus: mp.mpf,
    moments_minus: tuple[mp.mpf, mp.mpf],
    moments_plus: tuple[mp.mpf, mp.mpf],
    ring_delta: mp.mpf,
    jumps: tuple[int, int] = (1, 8),
) -> mp.matrix:
    """Columns are (U_plus,U_minus,H_jump_1,H_jump_2).

    Rows are tangent force, loss-weighted tangent force, and the difference
    of the theta and phi tangent covariances.  Symmetry kills every phi-odd
    row exactly.
    """

    s, c = mp.sin(theta), mp.cos(theta)
    sp, sm = mp.sin(theta + h_plus), mp.sin(theta - h_minus)
    lp, lm = 1 - mp.cos(h_plus), 1 - mp.cos(h_minus)
    m1p, m2p = moments_plus
    m1m, m2m = moments_minus
    a = mp.matrix(3, 4)

    a[0, 0] = mp.sin(h_plus) - c * sp * m1p
    a[0, 1] = -mp.sin(h_minus) - c * sm * m1m
    a[1, 0] = (
        mp.sin(h_plus) * lp
        + (mp.sin(h_plus) * s * sp - c * sp * lp) * m1p
        - c * s * sp**2 * m2p
    )
    a[1, 1] = (
        -mp.sin(h_minus) * lm
        + (-mp.sin(h_minus) * s * sm - c * sm * lm) * m1m
        - c * s * sm**2 * m2m
    )
    a[2, 0] = (
        mp.sin(h_plus) ** 2
        - 2 * mp.sin(h_plus) * c * sp * m1p
        + sp**2 * ((1 + c**2) * m2p - 2 * m1p)
    )
    a[2, 1] = (
        mp.sin(h_minus) ** 2
        + 2 * mp.sin(h_minus) * c * sm * m1m
        + sm**2 * ((1 + c**2) * m2m - 2 * m1m)
    )

    for column, jump in enumerate(jumps, start=2):
        u = 1 - mp.cos(jump * ring_delta)
        a[0, column] = -2 * s * c * u
        a[1, column] = -2 * s**3 * c * u**2
        a[2, column] = 2 * s**2 * (c**2 * u**2 - (2 * u - u**2))
    return a


def solve_transition(
    theta: mp.mpf,
    h: mp.mpf,
    coarse_count: int,
    gap_ratio: mp.mpf,
) -> tuple[mp.mpf, ...]:
    """Solve the two shared transition rows with incoming coarse total one."""

    alpha = mp.pi / coarse_count
    _, _, m1, m2 = mask_moments(alpha)
    diagonal = (m1, m2)
    aligned = (mp.mpf(0), mp.mpf(0))

    coarse = row_matrix(theta, h, gap_ratio * h, aligned, diagonal, 2 * alpha)
    fine_theta = theta + gap_ratio * h
    fine = row_matrix(fine_theta, gap_ratio * h, h, diagonal, aligned, alpha)

    # Unknowns: Q total, outgoing fine total, two coarse H's, two fine H's.
    b = mp.matrix(6, 6)
    rhs = mp.matrix(6, 1)
    for row in range(3):
        b[row, 0] = coarse[row, 0]
        b[row, 2] = coarse[row, 2]
        b[row, 3] = coarse[row, 3]
        rhs[row] = -coarse[row, 1]

        b[row + 3, 0] = fine[row, 1] / 2  # Q column sum is one half.
        b[row + 3, 1] = fine[row, 0]
        b[row + 3, 4] = fine[row, 2]
        b[row + 3, 5] = fine[row, 3]
        rhs[row + 3] = 0
    return tuple(mp.lu_solve(b, rhs))


def residuals(
    theta: mp.mpf,
    h: mp.mpf,
    coarse_count: int,
    gap_ratio: mp.mpf,
    solution: tuple[mp.mpf, ...],
) -> tuple[mp.mpf, ...]:
    alpha = mp.pi / coarse_count
    _, _, m1, m2 = mask_moments(alpha)
    diagonal = (m1, m2)
    aligned = (mp.mpf(0), mp.mpf(0))
    coarse = row_matrix(theta, h, gap_ratio * h, aligned, diagonal, 2 * alpha)
    fine = row_matrix(theta + gap_ratio * h, gap_ratio * h, h, diagonal, aligned, alpha)
    aq, af, hc1, hc8, hf1, hf8 = solution
    rc = coarse * mp.matrix([aq, 1, hc1, hc8])
    rf = fine * mp.matrix([af, aq / 2, hf1, hf8])
    return tuple(rc) + tuple(rf)


def main() -> None:
    print("shortened-gap transition audit")
    print("columns: M h theta/h gap min_coefficient max_scaled_residual")
    global_min = mp.inf
    for coarse_count in (32, 64, 128, 256, 512, 1024, 2048):
        # Put the transition at its ideal dyadic threshold.  The second test
        # moves it by one meridional layer and is the deterministic overshoot
        # mutation.
        for overshoot in (mp.mpf(0), mp.mpf("0.75")):
            h = mp.mpf("1e-7")
            radius = coarse_count / (4 * mp.pi) + overshoot
            theta = radius * h
            a = mp.sin(theta) * mp.pi / (coarse_count * h)
            gap = mp.sqrt(1 - mp.mpf("1.5") * a**2)
            solution = solve_transition(theta, h, coarse_count, gap)
            res = residuals(theta, h, coarse_count, gap, solution)
            minimum = min(solution)
            global_min = min(global_min, minimum)
            scaled = max(
                abs(res[0]) / h,
                abs(res[1]) / h**3,
                abs(res[2]) / h**2,
                abs(res[3]) / h,
                abs(res[4]) / h**3,
                abs(res[5]) / h**2,
            )
            print(
                coarse_count,
                mp.nstr(h, 4),
                mp.nstr(radius, 10),
                mp.nstr(gap, 12),
                mp.nstr(minimum, 12),
                mp.nstr(scaled, 5),
            )
    print("global minimum coefficient", mp.nstr(global_min, 15))
    assert global_min > 0
    print("shortened-gap transition regression audit: PASS")


if __name__ == "__main__":
    main()
