#!/usr/bin/env python3
"""Exact hostile regressions for rejected pre-repair shortened-gap formulas.

These checks distinguish formulas literally printed in the candidate from
the different formulas exercised by ``p1e_short_gap_proof_audit.py``.  They
also retain an exact obstruction to the claimed polar-cap rounding rule and
verify the sampling-quotient factorization that can replace the unsupported
four-cap estimate.
"""

from fractions import Fraction as F

import sympy as sp


def literal_mask_second_moment() -> None:
    """The rejected pre-repair m2 has no removable alpha^-4 value."""

    alpha = sp.symbols("alpha", real=True)
    c = sp.cos(alpha)
    p = (4 * c**2 + 2 * c - 1) / (4 * c * (c + 1))
    beta = sp.Rational(1, 2) + sp.cos(2 * alpha) / (2 * c)

    # Rejected literal formula from the pre-repair candidate.
    printed = 1 - 2 * beta * p + (1 - p) * sp.cos(2 * alpha) ** 2
    # Actual second centered loss moment used by the transition script.
    corrected = 1 - 2 * beta + p + (1 - p) * sp.cos(2 * alpha) ** 2

    assert sp.limit(printed, alpha, 0) == sp.Rational(1, 8)
    assert sp.limit(printed / alpha**4, alpha, 0, dir="+") == sp.oo
    assert sp.limit(corrected / alpha**4, alpha, 0) == sp.Rational(3, 2)
    assert sp.simplify(printed - corrected - 2 * beta * (1 - p) + p) == 0


def exact_mask_bookkeeping() -> None:
    """Retain the mask identities that do survive the hostile audit."""

    c = sp.symbols("c", positive=True)
    p = (4 * c**2 + 2 * c - 1) / (4 * c * (c + 1))
    q = (2 * c + 1) * (4 * c**2 + 2 * c - 1) / (8 * c**2 * (c + 1))
    x2 = 2 * c**2 - 1
    x3 = 4 * c**3 - 3 * c

    assert sp.simplify(p / 2 + 2 * (1 - p) / 4 - sp.Rational(1, 2)) == 0
    assert sp.simplify(2 * q / 4 + 2 * (1 - q) / 4 - sp.Rational(1, 2)) == 0
    assert sp.simplify(p + (1 - p) * x2 - (q * c + (1 - q) * x3)) == 0
    assert sp.simplify(
        p + (1 - p) * x2**2 - (q * c**2 + (1 - q) * x3**2)
    ) == 0


def cap_rounding_counterexample() -> None:
    """M0 does not make the physical longitude grid uniformly fine in h units.

    At a cap radius chosen so the one-step horizontal chord is h/3, the next
    possible unoriented chord is already greater than 0.65 h.  Hence no
    integer longitude jump has length in [0.49 h, 0.51 h].  The argument is
    exact; the rational guards below use only pi < 22/7 and cos x >= 1-x^2/2.
    """

    m0 = 2**40
    pi_hi = F(22, 7)
    x_hi = pi_hi / m0
    cos_lower = 1 - x_hi**2 / 2

    one_step = F(1, 3)
    two_step_lower = F(2, 3) * cos_lower
    assert one_step < F(49, 100)
    assert two_step_lower > F(51, 100)

    # The defining radius lies inside the J=1 cap: sin(theta)=x/(3 sin x)
    # is between 1/3 and 1/2 because 2x/3 < sin x < x for 0<x<=pi/M0.
    assert m0 > 16

    # It also disproves the claimed 2^-35 relative rounding scale.
    nearest_error_lower = min(F(1, 2) - one_step, two_step_lower - F(1, 2))
    assert nearest_error_lower > F(1, 10)
    assert nearest_error_lower > F(1, 2**35)


def direct_sampled_quotient_factorization() -> None:
    """The row form in section 7 gives a direct D2 bound without a frame gap."""

    radial_loss, mass, ell_max = sp.symbols(
        "radial_loss mass ell_max", positive=True
    )
    z = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3), -sp.Rational(1, 3))
    moment = sp.diag(
        radial_loss / mass,
        -radial_loss / (2 * mass),
        -radial_loss / (2 * mass),
    )
    multiplier = 3 * radial_loss / (2 * mass)
    assert sp.simplify(moment - multiplier * z) == sp.zeros(3)

    # R <= ell_max sum(gamma ell) = 2 mass ell_max.
    upper_multiplier = sp.simplify(multiplier.subs(radial_loss, 2 * mass * ell_max))
    assert upper_multiplier == 3 * ell_max


def taylor_domain_mutation() -> None:
    """Jump 8 on a coarse M-ring uses 16*pi/M, not 8*pi/M."""

    m0 = 2**40
    declared_radius = F(8 * 22, 7 * m0)
    coarse_jump_eight_radius = F(16 * 3, m0)  # pi > 3
    assert coarse_jump_eight_radius > declared_radius


def main() -> None:
    literal_mask_second_moment()
    exact_mask_bookkeeping()
    cap_rounding_counterexample()
    direct_sampled_quotient_factorization()
    taylor_domain_mutation()
    print("short-gap hostile referee audit: rejected-mutation regressions PASS")


if __name__ == "__main__":
    main()
