#!/usr/bin/env python3
"""Rational Cauchy majorant for the literal normalized transition program.

Together with p1e_short_gap_symbolic_matrix_audit.py, this certifies the
continuous all-orders box.  The symbolic audit checks that the literal row
program has the stated removable value; this audit bounds every semantic
primitive in that program on a complex disk and applies Cauchy's estimate.
No floating point or sampled parameter grid is used.
"""

from fractions import Fraction as F


def main() -> None:
    radius = F(1, 10_000)
    x0 = F(1, 2**80)
    pi_lo, pi_hi = F(3), F(22, 7)
    a_lo, a_hi = F(249, 1000), F(251, 1000)
    c_lo = F(6, 7)

    # On |x|<=R, |eta|<=3: a=1/4+eta*x and r=pi*x/a.
    assert F(1, 4) - 3 * radius > a_lo
    assert F(1, 4) + 3 * radius < a_hi
    r_bound = pi_hi * radius / a_lo
    alpha_bound = pi_hi * radius
    assert r_bound < F(1, 700)
    assert alpha_bound < F(1, 3000)
    assert 16 * alpha_bound < F(1, 180)  # coarse jump eight

    # For |z|<=1/180, exp(|z|)<=1/(1-|z|)<2.  Therefore
    # |sin z|<=2|z|, |cos z|<=2, |1-cos z|<=|z|^2,
    # and the entire quotients |sinc z|,|cosc z| are <=2.
    assert F(1, 1) / (1 - F(1, 180)) < 2
    assert 1 - alpha_bound**2 > F(9, 10)  # |cos(alpha)| denominator

    # Cancellation-free mask forms (2.4):
    # |m1|<=3 alpha^2, |m2|<=17 alpha^4.  Since alpha=a*r,
    # M1=|m1/r^2| and M2=|m2/r^4| are both <1.
    assert F(5, 1) / (2 * F(9, 10)) < 3
    assert F(3 * 5, 1) / F(9, 10) < 17
    assert 3 * a_hi**2 < 1
    assert 17 * a_hi**4 < 1

    # Neighbor sine ratios and fine cosine in the dimensionless guarded
    # formulas: v<=3, cf<=3, and the fine outgoing neighbor ratio<=7.
    assert 2 + 2 * r_bound < 3
    assert 3 * 2 + 3 * 2 * r_bound < 7

    # Literal radial columns after row-power division.  With lambda<=1,
    # |c0|,|base|<=3, |neighbor|<=7, M1,M2<=1 and sinc,cosc<=2,
    # the force/loss/isotropy coefficients are bounded by 3,45,103.
    force_radial = 2 + 3 * 7 * r_bound
    loss_radial = 2 + 7 * (2 * 3 + 3 * r_bound) + 3 * 3 * 7**2 * r_bound
    iso_radial = 4 + 4 * 3 * 7 * r_bound + 7**2 * (10 * r_bound**2 + 2)
    assert force_radial < 3
    assert loss_radial < 45
    assert iso_radial < 103

    # For u=1-cos(jump*delta), U=|u/r^2|<=17.  Substitute U in the
    # three literal horizontal columns.  The loss row is the largest.
    U = F(17)
    c_ratio = F(7, 2)  # |cf/c| <= 3/(6/7) < 7/2
    horizontal_force = 2 * 3 * c_ratio * U
    horizontal_loss = 2 * 3**3 * c_ratio * U**2
    horizontal_iso = 2 * 3**2 * (2 * U + 10 * r_bound**2 * U**2)
    assert horizontal_force < 400
    assert horizontal_loss < 55_000
    assert horizontal_iso < 700

    # All fixed row multipliers in (4.3) are <16.  Hence every A entry is
    # <10^6 on the disk.
    A_disk = F(1_000_000)
    assert 16 * max(F(103), horizontal_force, horizontal_loss, horizontal_iso) < A_disk

    # The force/loss RHS before division by c*r is a sum of two radial
    # coefficients with factors <=1/g<2.  On |x|=R,
    # 1/|c*r|=|a|/(|c|*pi*R)<1000.  The isotropy RHS has no such
    # removable quotient and is bounded directly.
    inv_cr_boundary = a_hi / (c_lo * pi_lo * radius)
    assert inv_cr_boundary < 1000
    rhs_force = 3 * 3 * inv_cr_boundary * 16
    rhs_loss = 45 * 3 * inv_cr_boundary * 16
    rhs_iso = 103 * 3 * 16
    b_disk = F(10_000_000)
    assert max(rhs_force, rhs_loss, rhs_iso) < b_disk

    # The RHS quotients are removable (verified exactly by the symbolic
    # audit).  Maximum modulus bounds their disk values by the boundary
    # estimates above.  Cauchy's derivative estimate at 0<=x<=2^-80 uses
    # distance R-x > R/2.
    assert x0 < radius / 2
    derivative_A = 2 * A_disk / radius
    derivative_b = 2 * b_disk / radius
    assert derivative_A < 10**12
    assert derivative_b < 10**12
    print("short-gap rational Cauchy all-orders guard: PASS")
    print("entrywise |A-A0|/x <=", derivative_A)
    print("entrywise |b-b0|/x <=", derivative_b)


if __name__ == "__main__":
    main()
