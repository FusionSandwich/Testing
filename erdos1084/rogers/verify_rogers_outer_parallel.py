#!/usr/bin/env python3
"""Exact certificate for the corrected Rogers outer-parallel coefficient."""

from fractions import Fraction as Q


def atan_partial(x: Q, terms: int) -> Q:
    return sum(
        (Q(1) if j % 2 == 0 else Q(-1))
        * x ** (2 * j + 1)
        / (2 * j + 1)
        for j in range(terms)
    )


sqrt2_upper = Q(707107, 500000)
sqrt3_upper = Q(1732050808, 10**9)
assert 2 < sqrt2_upper**2
assert 3 < sqrt3_upper**2

pi_upper_from_machin = (
    16 * atan_partial(Q(1, 5), 5)
    - 4 * atan_partial(Q(1, 239), 2)
)
pi_upper = Q(3141593, 10**6)
assert pi_upper_from_machin < pi_upper

atan_lower_factor = Q(1, 4) - Q(1, 96) + Q(1, 1280) - Q(1, 14336)
assert atan_lower_factor == Q(51673, 215040)

rogers_sigma_upper = sqrt2_upper * pi_upper / 2 - 6 * atan_lower_factor
assert rogers_sigma_upper == Q(5457713997657, 7000000000000)

local_lower = 103 - Q(117, 2) * sqrt3_upper
assert local_lower == Q(418756933, 250000000)

clean = Q(19773, 10000)
margin = local_lower**3 - clean**3 * rogers_sigma_upper**2
assert margin == Q(
    12110011383910062757202469348733867,
    49000000000000000000000000000000000000,
)
assert margin > 0

surface_scale = Q(59023, 50000)
assert surface_scale**3 * rogers_sigma_upper**2 < 1
assert clean < surface_scale * local_lower

print("ROGERS OUTER-PARALLEL COEFFICIENT CERTIFICATE")
print("status: PASS")
print(f"Rogers sigma_3 upper: {rogers_sigma_upper}")
print(f"surface scale: {surface_scale}")
print(f"local factor lower: {local_lower}")
print(f"clean coefficient: {clean}")
print(f"positive cubed margin: {margin}")
print("conclusion: corrected universal coefficient > 1.9773")
