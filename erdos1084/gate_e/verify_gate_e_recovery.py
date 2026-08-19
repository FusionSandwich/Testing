#!/usr/bin/env python3
"""Exact arithmetic and finite combinatorial checks for the Gate-E recovery theorem.

The authoritative all-n proof uses an exact-cardinality FCC correction cluster. The triangular
terrace calculation is retained as an auxiliary sharper local construction.
"""

from __future__ import annotations

FCC_DIRECTIONS = (
    (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
    (0, 1, 1), (0, 1, -1),
    (-1, -1, 0), (-1, 1, 0), (-1, 0, -1), (-1, 0, 1),
    (0, -1, -1), (0, -1, 1),
)
TRI_POSITIVE_DIRECTIONS = ((1, 0), (0, 1), (1, -1))
TRI_SIX_DIRECTIONS = (
    (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1),
)


def add3(p: tuple[int, int, int], v: tuple[int, int, int]) -> tuple[int, int, int]:
    return p[0] + v[0], p[1] + v[1], p[2] + v[2]


def parity_box(m: int) -> set[tuple[int, int, int]]:
    return {
        (x, y, z)
        for x in range(m)
        for y in range(m)
        for z in range(m)
        if (x + y + z) % 2 == 0
    }


def parity_box_number(m: int) -> int:
    return (m**3 + (m % 2)) // 2


def contact_deficit_3d(points: set[tuple[int, int, int]]) -> int:
    degree_sum = sum(add3(p, v) in points for p in points for v in FCC_DIRECTIONS)
    assert degree_sum % 2 == 0
    return 6 * len(points) - degree_sum // 2


def hex_points(radius: int) -> set[tuple[int, int]]:
    if radius < 0:
        return set()
    return {
        (i, j)
        for i in range(-radius, radius + 1)
        for j in range(-radius, radius + 1)
        if max(abs(i), abs(j), abs(i + j)) <= radius
    }


def outer_ring(radius: int) -> list[tuple[int, int]]:
    if radius == 0:
        return [(0, 0)]
    directions = ((0, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1))
    point = (radius, 0)
    ring: list[tuple[int, int]] = []
    for di, dj in directions:
        for _ in range(radius):
            ring.append(point)
            point = point[0] + di, point[1] + dj
    assert point == (radius, 0)
    return ring


def triangular_edges(points: set[tuple[int, int]]) -> int:
    return sum(
        (i + di, j + dj) in points
        for i, j in points
        for di, dj in TRI_POSITIVE_DIRECTIONS
    )


assert 256 // 2 == 128
assert 6 * 32 == 192
assert 192**3 == 432 * 128**2
assert 6**3 * 2 == 432

max_box_checked = 30
worst_box_ratio_record = None
for m in range(1, max_box_checked + 1):
    box = parity_box(m)
    assert len(box) == parity_box_number(m)
    deficit = contact_deficit_3d(box)
    assert deficit <= 36 * m * m
    shell_gap = parity_box_number(m + 1) - parity_box_number(m)
    assert shell_gap <= 2 * m * m + 2 * m + 1
    correction_bound = 36 * m * m + 6 * shell_gap
    assert correction_bound <= 48 * m * m + 12 * m + 6
    record = (m, len(box), deficit, shell_gap, correction_bound)
    if worst_box_ratio_record is None or deficit * worst_box_ratio_record[1] > worst_box_ratio_record[2] * len(box):
        worst_box_ratio_record = record

for radius in range(0, 101):
    patch = hex_points(radius)
    number = 3 * radius * radius + 3 * radius + 1
    edges = 9 * radius * radius + 3 * radius
    deficit = 6 * radius + 3
    assert len(patch) == number
    assert triangular_edges(patch) == edges
    assert 3 * number - edges == deficit
    if radius > 0:
        assert set(outer_ring(radius)) == patch - hex_points(radius - 1)

max_prefix_checked = 100_000
points = {(0, 0)}
number = 1
edges = 0
worst_slack = 0
worst_case = (1, 0, 3, 3)
radius = 1
while number < max_prefix_checked:
    assert len(points) == 3 * (radius - 1) ** 2 + 3 * (radius - 1) + 1
    for point in outer_ring(radius):
        if number >= max_prefix_checked:
            break
        neighbors = sum(
            (point[0] + di, point[1] + dj) in points
            for di, dj in TRI_SIX_DIRECTIONS
        )
        edges += neighbors
        points.add(point)
        number += 1
        deficit = 3 * number - edges
        bound = 18 * radius - 3
        assert deficit <= bound
        slack = bound - deficit
        if slack < worst_slack:
            worst_slack = slack
            worst_case = number, radius, deficit, bound
    radius += 1
assert triangular_edges(points) == edges


def fcc_number(t: int) -> int:
    return 128 * t**3 + 60 * t**2 + 12 * t + 1


def fcc_deficit(t: int) -> int:
    return 192 * t**2 + 60 * t + 6


for t in range(0, 100):
    assert fcc_number(t + 1) - fcc_number(t) == 384 * t**2 + 504 * t + 200
    assert fcc_deficit(t + 1) - fcc_deficit(t) == 384 * t + 252

print("GATE-E EXACT-MASS RECOVERY CERTIFICATE")
print("status: PASS")
print("FCC lattice density coefficient = 128")
print("FCC missing-bond coefficient per six directions = 192")
print("limiting coefficient cube = 432")
print("limiting coefficient = 6 * cubert(2)")
print()
print("FCC correction-cluster box formulas:")
print("  |B_m| = ceil(m^3/2)")
print("  |B_(m+1) \\ B_m| <= 2 m^2 + 2 m + 1")
print("  D(B_m) <= 36 m^2")
print("  exact-q correction bound <= 48 m^2 + 12 m + 6 = O(q^(2/3))")
print(f"  brute-force boxes checked through m = {max_box_checked}")
print(f"  diagnostic box record = {worst_box_ratio_record}")
print()
print("auxiliary triangular terrace formulas:")
print("  N_r = 3 r^2 + 3 r + 1")
print("  E_r = 9 r^2 + 3 r")
print("  3 N_r - E_r = 6 r + 3")
print(f"  prefixes checked through q = {max_prefix_checked}")
print(f"  tightest checked slack record = {worst_case}")
print()
print("exact FCC shell identities:")
print("  n_(t+1)-n_t = 384 t^2 + 504 t + 200")
print("  D_(t+1)-D_t = 384 t + 252")
print()
print("Certified use:")
print("an O(n^(2/3)) particle-count discrepancy can be filled by a separate exact-q FCC cluster")
print("at O(n^(4/9)) deficit cost, which is o(n^(2/3)); first-contact translation joins it.")
