#!/usr/bin/env python3
"""Exact low-index cubic coincidence-rotation classifier."""

from __future__ import annotations

from fractions import Fraction as Q
from functools import reduce
from itertools import permutations, product
from math import gcd, isqrt

Matrix = tuple[tuple[Q, Q, Q], tuple[Q, Q, Q], tuple[Q, Q, Q]]
Quaternion = tuple[int, int, int, int]


def determinant(matrix: Matrix) -> Q:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def multiply(first: Matrix, second: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(first[row][index] * second[index][column] for index in range(3))
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def rotation_matrix(q: Quaternion) -> Matrix:
    w, x, y, z = q
    norm = sum(value * value for value in q)
    return (
        (
            Q(w * w + x * x - y * y - z * z, norm),
            Q(2 * (x * y - w * z), norm),
            Q(2 * (x * z + w * y), norm),
        ),
        (
            Q(2 * (x * y + w * z), norm),
            Q(w * w - x * x + y * y - z * z, norm),
            Q(2 * (y * z - w * x), norm),
        ),
        (
            Q(2 * (x * z - w * y), norm),
            Q(2 * (y * z + w * x), norm),
            Q(w * w - x * x - y * y + z * z, norm),
        ),
    )


def proper_cubic_group() -> tuple[Matrix, ...]:
    group: list[Matrix] = []
    for permutation in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            matrix = [[Q(0) for _ in range(3)] for _ in range(3)]
            for row, column in enumerate(permutation):
                matrix[row][column] = Q(signs[row])
            result: Matrix = tuple(tuple(row) for row in matrix)  # type: ignore[assignment]
            if determinant(result) == 1:
                group.append(result)
    assert len(group) == 24
    return tuple(group)


CUBIC = proper_cubic_group()


def matrix_key(matrix: Matrix) -> tuple[Q, ...]:
    return tuple(value for row in matrix for value in row)


def double_coset_key(matrix: Matrix) -> tuple[Q, ...]:
    return min(
        matrix_key(multiply(multiply(left, matrix), right))
        for left in CUBIC
        for right in CUBIC
    )


def primitive_quaternions_of_norm(norm: int) -> list[Quaternion]:
    bound = isqrt(norm)
    result: list[Quaternion] = []
    for q in product(range(-bound, bound + 1), repeat=4):
        if sum(value * value for value in q) != norm:
            continue
        if reduce(gcd, map(abs, q)) != 1:
            continue
        result.append(q)
    return result


def classify(norms: tuple[int, ...]) -> tuple[dict[tuple[Q, ...], tuple[Quaternion, Matrix]], int]:
    rotations: dict[tuple[Q, ...], tuple[Quaternion, Matrix]] = {}
    quaternion_count = 0
    for norm in norms:
        quaternions = primitive_quaternions_of_norm(norm)
        quaternion_count += len(quaternions)
        for q in quaternions:
            matrix = rotation_matrix(q)
            rotations.setdefault(matrix_key(matrix), (q, matrix))

    classes: dict[tuple[Q, ...], tuple[Quaternion, Matrix]] = {}
    for q, matrix in rotations.values():
        classes.setdefault(double_coset_key(matrix), (q, matrix))
    return classes, quaternion_count


def find_equivalence(source: Matrix, target: Matrix) -> tuple[Matrix, Matrix]:
    for left in CUBIC:
        for right in CUBIC:
            if multiply(multiply(left, source), right) == target:
                return left, right
    raise AssertionError("matrices are not cubic-double-coset equivalent")


def matrix_text(matrix: Matrix) -> str:
    return "[" + "; ".join(",".join(str(value) for value in row) for row in matrix) + "]"


def main() -> None:
    for parity in product((0, 1), repeat=4):
        if parity == (0, 0, 0, 0):
            continue
        residue = sum(value * value for value in parity) % 8
        assert residue != 0

    index3, count3 = classify((3, 6, 12))
    index5, count5 = classify((5, 10, 20))
    assert len(index3) == 1
    assert len(index5) == 1

    twin = rotation_matrix((3, 1, 1, 1))
    sigma5 = rotation_matrix((2, 0, 0, 1))
    assert double_coset_key(twin) == next(iter(index3))
    assert double_coset_key(sigma5) == next(iter(index5))

    norm20 = rotation_matrix((3, 3, 1, 1))
    left, right = find_equivalence(norm20, sigma5)
    assert multiply(multiply(left, norm20), right) == sigma5

    assert twin == (
        (Q(2, 3), Q(-1, 3), Q(2, 3)),
        (Q(2, 3), Q(2, 3), Q(-1, 3)),
        (Q(-1, 3), Q(2, 3), Q(2, 3)),
    )
    assert sigma5 == (
        (Q(3, 5), Q(-4, 5), Q(0)),
        (Q(4, 5), Q(3, 5), Q(0)),
        (Q(0), Q(0), Q(1)),
    )

    print("LOW-INDEX CUBIC CSL DOUBLE-COSET CERTIFICATE")
    print("status: PASS")
    print("proper cubic rotation group size: 24")
    print("primitive norm valuation bound: v2(N(q)) <= 2")
    print("reduced index 3:")
    print("  exhaustive norms: 3, 6, 12")
    print(f"  primitive quaternions enumerated: {count3}")
    print("  cubic double-coset classes: 1")
    print("  representative quaternion: (3,1,1,1)")
    print("  representative rotation: 60-degree coherent [111] twin")
    print("reduced index 5:")
    print("  exhaustive norms: 5, 10, 20")
    print(f"  primitive quaternions enumerated: {count5}")
    print("  cubic double-coset classes: 1")
    print("  standard representative quaternion: (2,0,0,1)")
    print("  standard rotation: (1/5)*[[3,-4,0],[4,3,0],[0,0,5]]")
    print("  norm-20 representative (3,3,1,1) is explicitly cubic-equivalent")
    print("  left cubic symmetry: " + matrix_text(left))
    print("  right cubic symmetry: " + matrix_text(right))
    print("selector consequence:")
    print("  the only reduced indices below 7 are the coherent Sigma-3 class")
    print("  and the Sigma-5 [001] class")


if __name__ == "__main__":
    main()
