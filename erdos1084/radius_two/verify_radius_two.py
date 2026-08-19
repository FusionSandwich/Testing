#!/usr/bin/env python3
"""Integer/rational certificate for the radius-two `5/3` contact bound.

No floating-point value participates in a pass/fail decision. Radical values are
bounded by rational decimal intervals obtained from integer square roots.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

DIGITS = 70


def sqrt_fraction_bounds(q: Fraction, digits: int = DIGITS) -> tuple[Fraction, Fraction]:
    if q < 0:
        raise ValueError("negative radicand")
    scale = 10**digits
    n = (q.numerator * scale * scale) // q.denominator
    m = isqrt(n)
    lo = Fraction(m, scale)
    if lo * lo == q:
        return lo, lo
    return lo, Fraction(m + 1, scale)


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("invalid interval")

    @staticmethod
    def exact(q: Fraction | int) -> "Interval":
        q = Fraction(q)
        return Interval(q, q)

    def __add__(self, other: "Interval | Fraction | int") -> "Interval":
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: "Interval | Fraction | int") -> "Interval":
        return self + (-as_interval(other))

    def __rsub__(self, other: "Interval | Fraction | int") -> "Interval":
        return as_interval(other) - self

    def __mul__(self, other: "Interval | Fraction | int") -> "Interval":
        other = as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other: "Interval | Fraction | int") -> "Interval":
        return self * as_interval(other).reciprocal()

    def square(self) -> "Interval":
        if self.lo >= 0:
            return Interval(self.lo * self.lo, self.hi * self.hi)
        if self.hi <= 0:
            return Interval(self.hi * self.hi, self.lo * self.lo)
        return Interval(Fraction(0), max(self.lo * self.lo, self.hi * self.hi))

    def sqrt(self) -> "Interval":
        if self.lo < 0:
            raise ValueError("negative interval radicand")
        lo, _ = sqrt_fraction_bounds(self.lo)
        _, hi = sqrt_fraction_bounds(self.hi)
        return Interval(lo, hi)


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval.exact(value)


def decimal_floor(q: Fraction, digits: int) -> str:
    sign = "-" if q < 0 else ""
    q = abs(q)
    scale = 10**digits
    m = q.numerator * scale // q.denominator
    whole, frac = divmod(m, scale)
    return f"{sign}{whole}.{frac:0{digits}d}"


def decimal_ceil(q: Fraction, digits: int) -> str:
    if q < 0:
        return "-" + decimal_floor(-q, digits)
    scale = 10**digits
    m = (q.numerator * scale + q.denominator - 1) // q.denominator
    whole, frac = divmod(m, scale)
    return f"{whole}.{frac:0{digits}d}"


def show(interval: Interval, digits: int = 36) -> str:
    return (
        f"[{decimal_floor(interval.lo, digits)}, "
        f"{decimal_ceil(interval.hi, digits)}]"
    )


sqrt3 = Interval(*sqrt_fraction_bounds(Fraction(3)))
three_twentieths = Fraction(3, 20)

assert 3 * 11**2 - 19**2 == 2
assert 3 * 47400**2 - 82099**2 == 34199
assert 24 * sqrt3.hi < 73

charges: dict[int, Interval] = {}
H_values: dict[int, Interval] = {}

for degree in range(1, 12):
    x = 1 - degree * (1 - sqrt3 / 2)
    radicand = 1 - x.square()
    assert radicand.lo > 0
    H = 1 + sqrt3 * x / 2 - radicand.sqrt() / 2
    charge = H / (12 - degree)
    assert charge.hi < three_twentieths
    H_values[degree] = H
    charges[degree] = charge

max_degree = max(charges, key=lambda degree: charges[degree].hi)
assert max_degree == 11

optimized_coefficient = Interval(
    Fraction(1, 4) / charges[max_degree].hi,
    Fraction(1, 4) / charges[max_degree].lo,
)
assert optimized_coefficient.lo > Fraction(5, 3)

print("RADIUS-TWO EXACT CERTIFICATE")
print(f"radical digits: {DIGITS}")
print(f"sqrt(3) in {show(sqrt3, 40)}")
print(f"11-sphere non-saturation square margin: {3 * 11**2 - 19**2}")
print(f"lower-endpoint square margin: {3 * 47400**2 - 82099**2}")
print()
print("degree  H_d interval                              H_d/(12-d) interval                       gap below 3/20")
for degree in range(1, 12):
    gap = three_twentieths - charges[degree].hi
    print(
        f"{degree:2d}  {show(H_values[degree], 36)}  "
        f"{show(charges[degree], 36)}  {decimal_floor(gap, 36)}"
    )
print()
print(f"unique largest certified charge degree: {max_degree}")
print(f"optimized radius-two coefficient in {show(optimized_coefficient, 36)}")
print("clean exact coefficient: 5/3")
print("PASS")
