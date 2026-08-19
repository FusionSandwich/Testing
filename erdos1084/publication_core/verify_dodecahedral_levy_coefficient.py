#!/usr/bin/env python3
"""Exact certificate for the publication-core Erdős 1084 coefficient."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as Q


@dataclass(frozen=True)
class Quad:
    a: Q
    b: Q
    m: int

    def __add__(self, other: "Quad") -> "Quad":
        assert self.m == other.m
        return Quad(self.a + other.a, self.b + other.b, self.m)

    def __sub__(self, other: "Quad") -> "Quad":
        assert self.m == other.m
        return Quad(self.a - other.a, self.b - other.b, self.m)

    def __mul__(self, other: "Quad") -> "Quad":
        assert self.m == other.m
        return Quad(
            self.a * other.a + self.m * self.b * other.b,
            self.a * other.b + self.b * other.a,
            self.m,
        )

    def scale(self, q: Q) -> "Quad":
        return Quad(q * self.a, q * self.b, self.m)

    def pow(self, n: int) -> "Quad":
        assert n >= 0
        result = Quad(Q(1), Q(0), self.m)
        base = self
        k = n
        while k:
            if k & 1:
                result = result * base
            base = base * base
            k >>= 1
        return result


S3 = Quad(Q(0), Q(1), 3)
one3 = Quad(Q(1), Q(0), 3)
r_star = Quad(Q(40), Q(22), 3).scale(Q(1, 37))
q = one3 - S3.scale(Q(1, 2))
local_factor = Quad(Q(103), Q(-117, 2), 3)
assert r_star.pow(2) * q * local_factor == one3
assert r_star * Quad(Q(10), Q(-11, 2), 3) == one3

num_inradius = Quad(Q(250), Q(110), 5)
face_area_square_factor = Quad(Q(25), Q(10), 5)
claimed_density_square = Quad(Q(65, 2250), Q(29, 2250), 5)
left = claimed_density_square * face_area_square_factor.scale(Q(160000))
right = num_inradius.pow(2).scale(Q(16, 9))
assert left == right

sqrt3_upper = Q(1732050808, 10**9)
sqrt5_upper = Q(2236068, 10**6)
pi_upper = Q(3141593, 10**6)
assert 3 < sqrt3_upper**2
assert 5 < sqrt5_upper**2


def atan_partial(x: Q, terms: int) -> Q:
    return sum(
        (Q(1) if j % 2 == 0 else Q(-1))
        * x ** (2 * j + 1)
        / (2 * j + 1)
        for j in range(terms)
    )


pi_upper_from_machin = (
    16 * atan_partial(Q(1, 5), 5)
    - 4 * atan_partial(Q(1, 239), 2)
)
assert pi_upper_from_machin < pi_upper

local_lower = 103 - Q(117, 2) * sqrt3_upper
assert local_lower == Q(418756933, 250000000)
clean = Q(20207, 10000)
margin = (
    2250 * local_lower**3
    - clean**3 * pi_upper**2 * (65 + 29 * sqrt5_upper)
)
assert margin == Q(
    89330358943299520481455108949,
    250000000000000000000000000000,
)
assert margin > 0

published_density = Q(7547, 10000)
margin_from_published_decimal = local_lower**3 - clean**3 * published_density**2
assert margin_from_published_decimal > 0

surface_scale = Q(120637, 100000)
assert surface_scale**3 * published_density**2 < 1
assert clean < surface_scale * local_lower

getcontext().prec = 60
D = Decimal
sqrt3 = D(3).sqrt()
sqrt5 = D(5).sqrt()
pi_diag = D("3.14159265358979323846264338327950288419716939937510582097494")
L_diag = D(103) - D(117) * sqrt3 / D(2)
delta_diag = pi_diag * ((D(65) + D(29) * sqrt5) / D(2250)).sqrt()
cube_diag = D(2250) * L_diag**3 / (pi_diag**2 * (D(65) + D(29) * sqrt5))
c_diag = cube_diag ** (D(1) / D(3))

print("DODECAHEDRAL-LEVY CONTACT COEFFICIENT CERTIFICATE")
print("status: PASS")
print("optimized radius identity: r_*^2 q L = 1")
print("reciprocal identity: 1/r_* = 10 - 11 sqrt(3)/2")
print("dodecahedral identity: delta_Q^2/pi^2 = (65+29 sqrt(5))/2250")
print(f"sqrt(3) upper: {sqrt3_upper}")
print(f"sqrt(5) upper: {sqrt5_upper}")
print(f"pi upper from Machin certificate: {pi_upper_from_machin}")
print(f"declared pi upper: {pi_upper}")
print(f"local factor lower: {local_lower}")
print(f"surface scale: {surface_scale}")
print(f"clean coefficient: {clean}")
print(f"positive exact cube margin: {margin}")
print(f"published-0.7547 cube margin: {margin_from_published_decimal}")
print(f"diagnostic delta_Q: {delta_diag}")
print(f"diagnostic exact coefficient: {c_diag}")
print("conclusion: c_Q > 2.0207")
