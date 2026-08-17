#!/usr/bin/env python3
"""Exact compact certificate for the continuous `1673/1000` envelope."""

from fractions import Fraction
from math import isqrt

DIGITS = 80


class Q3:
    """Exact element `a + b*sqrt(3)` with rational coefficients."""

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        other = other if isinstance(other, Q3) else Q3(other)
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q3) else Q3(-other))

    def __rsub__(self, other):
        return Q3(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Q3) else Q3(other)
        return Q3(
            self.a * other.a + 3 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Fraction(other)
        return Q3(self.a / other, self.b / other)

    def __eq__(self, other):
        other = other if isinstance(other, Q3) else Q3(other)
        return self.a == other.a and self.b == other.b


S = Q3(0, 1)
L = (11 * S - 20) / 2
U = S / 2
Q = lambda x: (1000 * S - 654) + (673 * S - 2000) * x
P = lambda x: (
    (2692000 * S - 8157716) * (x * x)
    + (4880284 * S - 6654000) * x
    + 1308000 * S
    - 628787
)

assert S * S == 3
assert Q(U) == Q3(Fraction(711, 2))
assert P(U) == 573352
assert P(L) == 4 * Q3(-574502107, 331688980)
assert 2692000 * 2 - 8157716 < 0
assert 3 * 331688980**2 - 574502107**2 == 67412881751
assert 3 * 440**2 - 759**2 == 4719


def sqrt_bounds(q: Fraction) -> tuple[Fraction, Fraction]:
    scale = 10**DIGITS
    n = q.numerator * scale * scale // q.denominator
    m = isqrt(n)
    lo = Fraction(m, scale)
    hi = lo if lo * lo == q else Fraction(m + 1, scale)
    return lo, hi


def add_interval(a, b):
    return a[0] + b[0], a[1] + b[1]


def scale_interval(c, a):
    return (c * a[0], c * a[1]) if c >= 0 else (c * a[1], c * a[0])


def sqrt_interval(a):
    return sqrt_bounds(a[0])[0], sqrt_bounds(a[1])[1]


def floor_dec(q: Fraction, digits: int) -> str:
    sign = "-" if q < 0 else ""
    q = abs(q)
    scale = 10**digits
    m = q.numerator * scale // q.denominator
    whole, frac = divmod(m, scale)
    return f"{sign}{whole}.{frac:0{digits}d}"


def ceil_dec(q: Fraction, digits: int) -> str:
    if q < 0:
        return "-" + floor_dec(-q, digits)
    scale = 10**digits
    m = (q.numerator * scale + q.denominator - 1) // q.denominator
    whole, frac = divmod(m, scale)
    return f"{whole}.{frac:0{digits}d}"


sqrt3 = sqrt_bounds(Fraction(3))
radicand = add_interval(
    (Fraction(-759), Fraction(-759)),
    scale_interval(Fraction(440), sqrt3),
)
assert radicand[0] > 0
nested = sqrt_interval(radicand)
denominator = add_interval(
    (Fraction(37), Fraction(37)),
    scale_interval(Fraction(-20), sqrt3),
)
denominator = add_interval(denominator, scale_interval(Fraction(-1), nested))
assert denominator[0] > 0
c2_star = Fraction(1, denominator[1]), Fraction(1, denominator[0])
clean = Fraction(1673, 1000)
assert c2_star[0] > clean

print("RADIUS-TWO 1673/1000 CERTIFICATE")
print("status: PASS")
print("Q(U) = 711/2")
print("P(U) = 573352")
print("P(L) = 4*(331688980*sqrt(3)-574502107)")
print("lower-endpoint square margin = 67412881751")
print("nested-radicand square margin = 4719")
print(
    "c2_star in "
    f"[{floor_dec(c2_star[0], 42)}, {ceil_dec(c2_star[1], 42)}]"
)
print(f"gap above 1673/1000 > {floor_dec(c2_star[0] - clean, 42)}")
print("PASS")
