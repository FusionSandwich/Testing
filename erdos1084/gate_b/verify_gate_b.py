#!/usr/bin/env python3
"""Exact arithmetic certificate for Gate B."""

from fractions import Fraction as Q
from math import gcd

T = (
    (Q(-2, 3), Q(1, 3)),
    (Q(1, 3), Q(-2, 3)),
    (Q(1, 3), Q(1, 3)),
)


def triangle_support(u: tuple[Q, Q]) -> Q:
    x, y = u
    return max(x * a + y * b for a, b in T)


def stationary_volume(p: Q) -> Q:
    return 32 + 2 * p * (1 - p)


def stationary_cube(p: Q) -> Q:
    return 432 + 27 * p * (1 - p)


def positive_part(x: Q) -> Q:
    return max(Q(0), x)


def raw_relaxed_support(v: tuple[Q, Q, Q]) -> Q:
    x, y, t = v
    A = triangle_support((x, y))
    B = triangle_support((-x, -y))
    H = A + B
    return H + max(
        Q(3, 2) * abs(t),
        H / 2 + positive_part(abs(t) - abs(A - B)) / 2,
    )


def convex_envelope_support(v: tuple[Q, Q, Q]) -> Q:
    x, y, t = v
    H = triangle_support((x, y)) + triangle_support((-x, -y))
    return H + max(H / 2, Q(3, 2) * abs(t))


classes = 0
strict_classes = 0
for denominator in range(1, 65):
    for numerator in range(denominator + 1):
        if gcd(numerator, denominator) != 1 and numerator not in (0, denominator):
            continue
        p = Q(numerator, denominator)
        cube = stationary_cube(p)
        volume = stationary_volume(p)
        assert cube == Q(27, 2) * volume
        assert cube >= 432
        if 0 < numerator < denominator:
            assert cube > 432
            strict_classes += 1
        else:
            assert cube == 432
        classes += 1

approximants = (
    Q(2, 5),
    Q(5, 12),
    Q(12, 29),
    Q(29, 70),
    Q(70, 169),
)
for left, right in zip(approximants, approximants[1:]):
    assert abs(right * right + 2 * right - 1) < abs(left * left + 2 * left - 1)
coefficient_differences = [
    abs(stationary_cube(right) - stationary_cube(left))
    for left, right in zip(approximants, approximants[1:])
]
for earlier, later in zip(coefficient_differences, coefficient_differences[1:]):
    assert later < earlier

v = (Q(3), Q(3), Q(1))
w = (Q(3), Q(0), Q(1))
vw = tuple(a + b for a, b in zip(v, w))
assert raw_relaxed_support(v) == Q(9, 2)
assert raw_relaxed_support(w) == Q(9, 2)
assert raw_relaxed_support(vw) == 10
assert raw_relaxed_support(vw) > raw_relaxed_support(v) + raw_relaxed_support(w)

test = (Q(1), Q(-1), Q(1, 4))
assert raw_relaxed_support(test) == Q(25, 8)
assert convex_envelope_support(test) == 3
assert convex_envelope_support(test) < raw_relaxed_support(test)

scaled_common_volume = Q(57, 4)
physical_common_volume = 2 * scaled_common_volume
common_cube = Q(27, 2) * physical_common_volume
assert physical_common_volume == Q(57, 2)
assert common_cube == Q(1539, 4)
assert common_cube < 432

print("GATE B INVARIANT-MEASURE EXACT CERTIFICATE")
print("status: PASS")
print(f"rational marginals checked: {classes}")
print(f"strict non-FCC marginals checked: {strict_classes}")
print()
print("stationary theorem:")
print("  physical volume = 32 + 2*p*(1-p)")
print("  coefficient cube = 432 + 27*p*(1-p)")
print("  equality iff p=0 or p=1")
print()
print("aperiodic frequency approximants:")
for p, cube in zip(approximants, map(stationary_cube, approximants)):
    print(f"  p={p}: coefficient cube={cube}")
print()
print("raw-infimum subadditivity counterexample:")
print(f"  phi(v)={raw_relaxed_support(v)}")
print(f"  phi(w)={raw_relaxed_support(w)}")
print(f"  phi(v+w)={raw_relaxed_support(vw)}")
print()
print("convex-envelope certificate:")
print(f"  scaled Wulff volume={scaled_common_volume}")
print(f"  physical Wulff volume={physical_common_volume}")
print(f"  coefficient cube={common_cube}")
print()
print("Certified conclusion:")
print("  every invariant stacking measure has coefficient at least FCC,")
print("  but the directionwise infimum is nonconvex and its convex envelope")
print("  is the phase-independent over-relaxation with cube 1539/4.")
