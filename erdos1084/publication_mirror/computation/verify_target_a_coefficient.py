#!/usr/bin/env python3
"""Exact arithmetic certificate for the universal Erdős 1084 coefficient 2.0465.

All pass/fail decisions are rational or quadratic-field identities. Decimal output
is diagnostic only. Published geometric inputs are not re-proved here.
"""
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
        return Quad(self.a * other.a + self.m * self.b * other.b,
                    self.a * other.b + self.b * other.a, self.m)

    def scale(self, q: Q) -> "Quad":
        return Quad(self.a * q, self.b * q, self.m)

    def pow(self, n: int) -> "Quad":
        out = Quad(Q(1), Q(0), self.m)
        base = self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n >>= 1
        return out


S3 = Quad(Q(0), Q(1), 3)
one = Quad(Q(1), Q(0), 3)
r_star = Quad(Q(40), Q(22), 3).scale(Q(1, 37))
q = one - S3.scale(Q(1, 2))
local_factor = Quad(Q(103), Q(-117, 2), 3)
reciprocal = Quad(Q(10), Q(-11, 2), 3)

assert r_star * reciprocal == one
assert r_star.pow(2) * q * local_factor == one
assert 3 * 11**2 > 17**2
assert 206**2 > 3 * 117**2

sqrt3_upper = Q(1732050808, 10**9)
assert 3 < sqrt3_upper**2


def atan_partial(x: Q, terms: int) -> Q:
    return sum((Q(1) if j % 2 == 0 else Q(-1)) * x ** (2*j+1) / (2*j+1)
               for j in range(terms))


pi_machin_upper = 16 * atan_partial(Q(1, 5), 5) - 4 * atan_partial(Q(1, 239), 2)
pi_upper = Q(3141593, 10**6)
assert pi_machin_upper < pi_upper

local_lower = 103 - Q(117, 2) * sqrt3_upper
assert local_lower == Q(418756933, 250000000)
clean = Q(4093, 2000)
margin = 18 * local_lower**3 - clean**3 * pi_upper**2
assert margin > 0
assert margin == Q(83319151211028177098003,
                   125000000000000000000000000)

getcontext().prec = 60
D = Decimal
sqrt3 = D(3).sqrt()
pi_diag = D("3.14159265358979323846264338327950288419716939937510582097494")
local_diag = D(103) - D(117) * sqrt3 / D(2)
cube_diag = D(18) * local_diag**3 / pi_diag**2
c_diag = cube_diag ** (D(1)/D(3))
r_diag = (D(40)+D(22)*sqrt3)/D(37)

print("ERDOS 1084 UNIVERSAL TARGET-A COEFFICIENT CERTIFICATE")
print("status: PASS")
print("finite-density input: external Bezdek--Langi theorem for lambda>=1")
print("optimized radius identity: r_*^2 q L = 1")
print("reciprocal identity: 1/r_* = 10 - 11 sqrt(3)/2")
print(f"sqrt(3) upper: {sqrt3_upper}")
print(f"pi upper from Machin certificate: {pi_machin_upper}")
print(f"declared pi upper: {pi_upper}")
print(f"local factor lower: {local_lower}")
print(f"clean coefficient: {clean}")
print(f"positive exact cube margin: {margin}")
print(f"diagnostic optimized radius: {r_diag}")
print(f"diagnostic exact coefficient: {c_diag}")
print("conclusion: c_K > 2.0465")
