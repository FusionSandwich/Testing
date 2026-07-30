#!/usr/bin/env python3
"""Exact symbolic audit of the N=2 GLC angular Fokker--Planck stencil.

This is intentionally small and exact. It verifies the same coordinate,
defect, and stiffness identities used in the floating-point family audit,
without numerical tolerances.
"""

from sympy import Matrix, Rational, sqrt, simplify

mu = [-1 / sqrt(3), 1 / sqrt(3)]
w = [Rational(1), Rational(1)]
rho = [sqrt(Rational(2, 3)), sqrt(Rational(2, 3))]

beta = -2 * w[0] * mu[0]
a01 = simplify(beta / (w[0] * (mu[1] - mu[0])))
a10 = simplify(beta / (w[1] * (mu[1] - mu[0])))
assert a01 == 1 and a10 == 1

c = Rational(0)
K = simplify(2 * rho[0] ** 2 + rho[0] * c)
dphi_base = Rational(1)
q = simplify(K / (2 * rho[0] ** 2 * dphi_base))
assert K == Rational(4, 3)
assert q == 1

p = Matrix([rho[0], 0, mu[0]])
p_lat = Matrix([rho[1], 0, mu[1]])
p_az_plus = Matrix([0, rho[0], mu[0]])
p_az_minus = Matrix([0, -rho[0], mu[0]])

Lp = simplify(a01 * (p_lat - p) + q * (p_az_plus - p) + q * (p_az_minus - p))
assert all(simplify(Lp[k] + 2 * p[k]) == 0 for k in range(3))

def chord_defect(other: Matrix):
    return simplify(1 - p.dot(other))

d_lat = chord_defect(p_lat)
d_az_plus = chord_defect(p_az_plus)
d_az_minus = chord_defect(p_az_minus)
defect = simplify(a01 * d_lat**2 + q * d_az_plus**2 + q * d_az_minus**2)
rate = simplify(a01 + 2 * q)
assert d_lat == Rational(2, 3)
assert d_az_plus == Rational(2, 3)
assert d_az_minus == Rational(2, 3)
assert defect == Rational(4, 3)
assert rate == 3
assert simplify(rate * defect) == 4

print("N=2 exact symbolic audit: PASS")
print(f"latitude_rate={a01}, K={K}, azimuth_rate={q}, defect={defect}, rate={rate}")
