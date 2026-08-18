#!/usr/bin/env python3
"""Exact and brute-force certificate for the FCC truncated-octahedral family.

The FCC lattice is represented as
    L = {(x,y,z) in Z^3 : x+y+z is even}
and is scaled by 1/sqrt(2), so its minimum distance is one.

For t >= 0 define
    S_t = {p in L : ||p||_infinity <= 4t and ||p||_1 <= 6t}.

The script verifies the exact formulas
    n_t = 128 t^3 + 60 t^2 + 12 t + 1,
    b_t = 32 t^2 + 10 t + 1,
    D_t = 6 b_t = 192 t^2 + 60 t + 6,
    E_t = 6 n_t - D_t = 768 t^3 + 168 t^2 + 12 t,
where b_t is the number of missing positive-direction bonds in any one
nearest-neighbor direction and D_t = 6 n_t - E_t.

No floating-point value participates in a pass/fail decision.
"""

from __future__ import annotations

from itertools import combinations

POSITIVE_DIRECTIONS = (
    (1, 1, 0),
    (1, -1, 0),
    (1, 0, 1),
    (1, 0, -1),
    (0, 1, 1),
    (0, 1, -1),
)


def det3(a: tuple[int, int, int],
         b: tuple[int, int, int],
         c: tuple[int, int, int]) -> int:
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def fcc_wulff_set(t: int) -> set[tuple[int, int, int]]:
    if t < 0:
        raise ValueError("t must be nonnegative")
    points: set[tuple[int, int, int]] = set()
    for x in range(-4 * t, 4 * t + 1):
        for y in range(-4 * t, 4 * t + 1):
            remaining = 6 * t - abs(x) - abs(y)
            if remaining < 0:
                continue
            zmax = min(4 * t, remaining)
            for z in range(-zmax, zmax + 1):
                if (x + y + z) % 2 == 0:
                    points.add((x, y, z))
    return points


def translate(p: tuple[int, int, int],
              v: tuple[int, int, int]) -> tuple[int, int, int]:
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])


def exact_formulas(t: int) -> tuple[int, int, int, int]:
    n = 128 * t**3 + 60 * t**2 + 12 * t + 1
    b = 32 * t**2 + 10 * t + 1
    deficit = 6 * b
    edges = 6 * n - deficit
    return n, b, deficit, edges


def brute_force_counts(t: int) -> tuple[int, tuple[int, ...], int, int]:
    points = fcc_wulff_set(t)
    missing = tuple(
        sum(1 for p in points if translate(p, v) not in points)
        for v in POSITIVE_DIRECTIONS
    )
    edges = sum(
        1
        for p in points
        for v in POSITIVE_DIRECTIONS
        if translate(p, v) in points
    )
    deficit = 6 * len(points) - edges
    return len(points), missing, deficit, edges


determinant_sum = sum(
    abs(det3(*triple))
    for triple in combinations(POSITIVE_DIRECTIONS, 3)
)
zonotope_volume = 8 * determinant_sum

assert determinant_sum == 32
assert zonotope_volume == 256
assert 192**3 == 432 * 128**2
assert 6**3 * 2 == 432

print("FCC TRUNCATED-OCTAHEDRAL CERTIFICATE")
print(f"determinant sum = {determinant_sum}")
print(f"integer-coordinate zonotope volume = {zonotope_volume}")
print("limiting coefficient cube = 432")
print("limiting coefficient = 6 * cubert(2)")
print()
print("t  n_t       b_t      D_t      E_t")
for t in range(0, 8):
    n, missing, deficit, edges = brute_force_counts(t)
    en, eb, ed, ee = exact_formulas(t)
    assert n == en
    assert all(value == eb for value in missing)
    assert deficit == ed
    assert edges == ee
    assert deficit == 6 * n - edges
    print(f"{t:1d}  {n:8d}  {eb:7d}  {deficit:7d}  {edges:8d}")

print()
print("Exact formulas:")
print("n_t = 128 t^3 + 60 t^2 + 12 t + 1")
print("b_t = 32 t^2 + 10 t + 1")
print("D_t = 192 t^2 + 60 t + 6")
print("E_t = 768 t^3 + 168 t^2 + 12 t")
print("PASS")
