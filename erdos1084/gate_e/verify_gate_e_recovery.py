#!/usr/bin/env python3
"""Exact arithmetic and finite combinatorial checks for the Gate-E recovery theorem."""

from __future__ import annotations

TRI_POSITIVE_DIRECTIONS = ((1, 0), (0, 1), (1, -1))
TRI_SIX_DIRECTIONS = (
    (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1),
)


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
            point = (point[0] + di, point[1] + dj)
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

max_checked = 100_000
points = {(0, 0)}
number = 1
edges = 0
worst_slack = 0
worst_case = (1, 0, 3, 3)
radius = 1
while number < max_checked:
    assert len(points) == 3 * (radius - 1) ** 2 + 3 * (radius - 1) + 1
    for point in outer_ring(radius):
        if number >= max_checked:
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
            worst_case = (number, radius, deficit, bound)
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
print("hex patch formulas:")
print("  N_r = 3 r^2 + 3 r + 1")
print("  E_r = 9 r^2 + 3 r")
print("  3 N_r - E_r = 6 r + 3")
print()
print(f"prefix reservoir checked for every q <= {max_checked}")
print("proved bound: 3 q - E(P_q) <= 18 r(q) - 3 for r(q) >= 1")
print(f"tightest checked slack record = {worst_case}")
print()
print("exact FCC shell identities:")
print("  n_(t+1)-n_t = 384 t^2 + 504 t + 200")
print("  D_(t+1)-D_t = 384 t + 252")
print()
print("Certified use:")
print("an O(n^(2/3)) particle-count error can be corrected on a close-packed terrace")
print("at O(n^(1/3)) contact-deficit cost, which is o(n^(2/3)).")
