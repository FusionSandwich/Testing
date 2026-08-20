#!/usr/bin/env python3
"""Exact Matrix-Tree certificate for icosahedral spanning-tree developments."""

from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction as Q

VERTICES = tuple(range(12))
EDGES = (
    (0, 1), (0, 5), (0, 7), (0, 8), (0, 11),
    (1, 2), (1, 5), (1, 6), (1, 8),
    (2, 3), (2, 6), (2, 8), (2, 9),
    (3, 4), (3, 6), (3, 9), (3, 10),
    (4, 5), (4, 6), (4, 10), (4, 11),
    (5, 6), (5, 11),
    (7, 8), (7, 9), (7, 10), (7, 11),
    (8, 9), (9, 10), (10, 11),
)


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    if size == 0:
        return 1
    sign = 1
    previous_pivot = 1
    for column in range(size - 1):
        if work[column][column] == 0:
            pivot_row = next(
                (row for row in range(column + 1, size) if work[row][column] != 0),
                None,
            )
            if pivot_row is None:
                return 0
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for next_column in range(column + 1, size):
                numerator = (
                    work[row][next_column] * pivot
                    - work[row][column] * work[column][next_column]
                )
                if numerator % previous_pivot != 0:
                    raise AssertionError("Bareiss division was not exact")
                work[row][next_column] = numerator // previous_pivot
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def spanning_tree_count(
    vertices: set[int], weighted_edges: Counter[tuple[int, int]]
) -> int:
    ordered = sorted(vertices)
    index = {vertex: position for position, vertex in enumerate(ordered)}
    size = len(ordered)
    laplacian = [[0 for _ in range(size)] for _ in range(size)]
    for (first, second), multiplicity in weighted_edges.items():
        if first == second:
            continue
        i, j = index[first], index[second]
        laplacian[i][i] += multiplicity
        laplacian[j][j] += multiplicity
        laplacian[i][j] -= multiplicity
        laplacian[j][i] -= multiplicity
    cofactor = [row[:-1] for row in laplacian[:-1]]
    return bareiss_determinant(cofactor)


def is_connected() -> bool:
    adjacency = {vertex: set() for vertex in VERTICES}
    for first, second in EDGES:
        adjacency[first].add(second)
        adjacency[second].add(first)
    reached = {VERTICES[0]}
    queue: deque[int] = deque([VERTICES[0]])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    return reached == set(VERTICES)


def contracted_multigraph(
    contracted_edge: tuple[int, int]
) -> tuple[set[int], Counter[tuple[int, int]]]:
    first, second = contracted_edge
    representative = min(first, second)
    removed = max(first, second)
    image = {
        vertex: representative if vertex == removed else vertex
        for vertex in VERTICES
    }
    weighted: Counter[tuple[int, int]] = Counter()
    for left, right in EDGES:
        mapped_left, mapped_right = image[left], image[right]
        if mapped_left == mapped_right:
            continue
        weighted[tuple(sorted((mapped_left, mapped_right)))] += 1
    return set(image.values()), weighted


def main() -> None:
    canonical_edges = [tuple(sorted(edge)) for edge in EDGES]
    assert len(VERTICES) == 12
    assert len(EDGES) == 30
    assert len(set(canonical_edges)) == 30
    assert is_connected()

    degrees = Counter()
    for first, second in EDGES:
        degrees[first] += 1
        degrees[second] += 1
    assert set(degrees.values()) == {5}

    total_trees = spanning_tree_count(set(VERTICES), Counter(canonical_edges))
    assert total_trees == 5_184_000

    containing_counts: dict[tuple[int, int], int] = {}
    for edge in EDGES:
        vertices, weighted = contracted_multigraph(edge)
        containing_counts[tuple(sorted(edge))] = spanning_tree_count(vertices, weighted)

    assert set(containing_counts.values()) == {1_900_800}
    per_edge = next(iter(containing_counts.values()))
    marginal = Q(per_edge, total_trees)
    assert marginal == Q(11, 30)
    assert sum(containing_counts.values()) == total_trees * 11

    print("ICOSAHEDRAL SPANNING-TREE DEVELOPMENT CERTIFICATE")
    print("status: PASS")
    print(f"vertices: {len(VERTICES)}")
    print(f"edges / radial interfaces: {len(EDGES)}")
    print("vertex degree: 5")
    print("branch interfaces in one primal spanning tree: 11")
    print("uncut dual adjacency edges: 19")
    print(f"exact primal spanning-tree count: {total_trees}")
    print(f"trees containing each fixed edge: {per_edge}")
    print(f"uniform branch marginal: {marginal}")
    print("incidence identity: 30*1900800 = 11*5184000")
    print("selector consequence:")
    print("  physical interface ratio >= 11/30 on every equal-jump radial face")
    print("  implies the sharp FCC bound for the averaged spanning-tree development family")


if __name__ == "__main__":
    main()
