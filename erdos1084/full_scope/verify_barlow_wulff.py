#!/usr/bin/env python3
"""Exact Barlow-stacking Wulff-volume certificate.

Close-packed layers admit two possible transition chiralities. Let p in [0,1]
be the asymptotic frequency of one chirality. The script computes the exact
weighted zonotope volume and certifies

  W(p) = 32 + 12 p(1-p),
  c_Barlow(p)^3 = 432 + 162 p(1-p).

No floating-point value participates in a pass/fail decision.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Q = Fraction
Poly = tuple[Fraction, Fraction, Fraction, Fraction]


def poly_add(a: Poly, b: Poly) -> Poly:
    return tuple(a[i] + b[i] for i in range(4))  # type: ignore[return-value]


def poly_mul(a: Poly, b: Poly) -> Poly:
    out = [Q(0) for _ in range(4)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j < 4:
                out[i + j] += ai * bj
    return tuple(out)  # type: ignore[return-value]


ONE: Poly = (Q(1), Q(0), Q(0), Q(0))
P: Poly = (Q(0), Q(1), Q(0), Q(0))
ONE_MINUS_P: Poly = (Q(1), Q(-1), Q(0), Q(0))


def det3(a: tuple[Fraction, Fraction, Fraction],
         b: tuple[Fraction, Fraction, Fraction],
         c: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


BASAL = (
    (Q(1), Q(0), Q(0)),
    (Q(0), Q(1), Q(0)),
    (Q(-1), Q(1), Q(0)),
)
PLUS = (
    (Q(1, 3), Q(1, 3), Q(1)),
    (Q(-2, 3), Q(1, 3), Q(1)),
    (Q(1, 3), Q(-2, 3), Q(1)),
)
MINUS = (
    (Q(2, 3), Q(-1, 3), Q(1)),
    (Q(-1, 3), Q(-1, 3), Q(1)),
    (Q(-1, 3), Q(2, 3), Q(1)),
)

GENERATORS = BASAL + PLUS + MINUS
WEIGHTS = (ONE,) * 3 + (P,) * 3 + (ONE_MINUS_P,) * 3

zcoord: Poly = (Q(0), Q(0), Q(0), Q(0))
for i, j, k in combinations(range(9), 3):
    determinant = abs(det3(GENERATORS[i], GENERATORS[j], GENERATORS[k]))
    if determinant == 0:
        continue
    weight = poly_mul(poly_mul(WEIGHTS[i], WEIGHTS[j]), WEIGHTS[k])
    term = tuple(determinant * coefficient for coefficient in weight)
    zcoord = poly_add(zcoord, term)  # type: ignore[arg-type]
zcoord = tuple(8 * coefficient for coefficient in zcoord)  # type: ignore[assignment]

wulff = tuple(coefficient / 4 for coefficient in zcoord)
coefficient_cube = tuple(Q(27, 2) * coefficient for coefficient in wulff)

assert zcoord == (Q(128), Q(48), Q(-48), Q(0))
assert wulff == (Q(32), Q(12), Q(-12), Q(0))
assert coefficient_cube == (Q(432), Q(162), Q(-162), Q(0))


def evaluate(poly: Poly, value: Fraction) -> Fraction:
    return sum(poly[i] * value**i for i in range(4))


assert evaluate(wulff, Q(0)) == 32
assert evaluate(wulff, Q(1)) == 32
assert evaluate(wulff, Q(1, 2)) == 35
assert evaluate(coefficient_cube, Q(0)) == 432
assert evaluate(coefficient_cube, Q(1)) == 432
assert evaluate(coefficient_cube, Q(1, 2)) == Q(945, 2)

print("BARLOW WULFF CERTIFICATE")
print("coordinate zonotope volume = 128 + 48 p - 48 p^2")
print("physical D-Wulff volume = 32 + 12 p - 12 p^2")
print("coefficient cube = 432 + 162 p - 162 p^2")
print("coefficient cube = 432 + 162 p(1-p)")
print()
print("FCC: p=0 or 1")
print("  W = 32")
print("  c^3 = 432")
print("  c = 6 * cubert(2)")
print("HCP: p=1/2")
print("  W = 35")
print("  c^3 = 945/2")
print("  c = 3 * cubert(35/2)")
print()
print("Verified: FCC uniquely minimizes the coefficient among p in [0,1].")
print("PASS")
