#!/usr/bin/env python3
"""Exact rational certificate for the FCC coherent-twin generators."""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product

Matrix = tuple[tuple[Q, Q, Q], tuple[Q, Q, Q], tuple[Q, Q, Q]]
Vector = tuple[Q, Q, Q]


def identity() -> Matrix:
    return tuple(
        tuple(Q(1 if row == column else 0) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[column][row] for column in range(3)) for row in range(3))  # type: ignore[return-value]


def multiply(first: Matrix, second: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(first[row][index] * second[index][column] for index in range(3))
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def power(matrix: Matrix, exponent: int) -> Matrix:
    result = identity()
    for _ in range(exponent):
        result = multiply(result, matrix)
    return result


def determinant(matrix: Matrix) -> Q:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def trace(matrix: Matrix) -> Q:
    return sum(matrix[index][index] for index in range(3))


def negate(matrix: Matrix) -> Matrix:
    return tuple(tuple(-entry for entry in row) for row in matrix)  # type: ignore[return-value]


def rotation_sixty(axis_signs: tuple[int, int, int]) -> Matrix:
    a = tuple(Q(sign) for sign in axis_signs)
    result: list[list[Q]] = [[Q(0) for _ in range(3)] for _ in range(3)]
    cross = (
        (Q(0), -a[2], a[1]),
        (a[2], Q(0), -a[0]),
        (-a[1], a[0], Q(0)),
    )
    for row in range(3):
        for column in range(3):
            result[row][column] = (
                Q(1, 2) * Q(1 if row == column else 0)
                + Q(1, 6) * a[row] * a[column]
                + Q(1, 2) * cross[row][column]
            )
    return tuple(tuple(row) for row in result)  # type: ignore[return-value]


def reflection(axis_signs: tuple[int, int, int]) -> Matrix:
    a = tuple(Q(sign) for sign in axis_signs)
    return tuple(
        tuple(
            Q(1 if row == column else 0) - Q(2, 3) * a[row] * a[column]
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def is_signed_permutation(matrix: Matrix) -> bool:
    for row in matrix:
        if sorted(abs(entry) for entry in row) != [Q(0), Q(0), Q(1)]:
            return False
    for column in range(3):
        entries = [abs(matrix[row][column]) for row in range(3)]
        if sorted(entries) != [Q(0), Q(0), Q(1)]:
            return False
    return True


def apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


def preserves_fcc_parity(matrix: Matrix) -> bool:
    for vector in product((0, 1), repeat=3):
        if sum(vector) % 2 != 0:
            continue
        image = apply(matrix, tuple(Q(value) for value in vector))
        if not all(entry.denominator == 1 for entry in image):
            return False
        if sum(int(entry) for entry in image) % 2 != 0:
            return False
    return True


def verify_generator(name: str, axis: tuple[int, int, int], matrix: Matrix) -> None:
    assert multiply(transpose(matrix), matrix) == identity()
    assert determinant(matrix) == 1
    assert power(matrix, 6) == identity()
    assert power(matrix, 3) != identity()

    square = power(matrix, 2)
    assert is_signed_permutation(square)
    assert preserves_fcc_parity(square)
    assert power(matrix, 3) == negate(reflection(axis))

    print(f"{name}: PASS")
    print(f"  determinant: {determinant(matrix)}")
    print("  order divides: 6")
    print("  square is FCC signed-permutation symmetry: yes")
    print("  cube equals minus twin-plane reflection: yes")


def main() -> None:
    axis_one = (1, 1, 1)
    axis_two = (1, -1, -1)
    assert sum(first * second for first, second in zip(axis_one, axis_two)) == -1

    first = rotation_sixty(axis_one)
    second = rotation_sixty(axis_two)
    verify_generator("twin generator T1", axis_one, first)
    verify_generator("twin generator T2", axis_two, second)

    product_matrix = multiply(first, second)
    product_trace = trace(product_matrix)
    assert product_trace == Q(16, 9)
    assert product_trace.denominator != 1

    quaternion_scalar = Q(3, 4) - Q(1, 4) * Q(-1, 3)
    assert quaternion_scalar == Q(5, 6)
    assert 4 * quaternion_scalar * quaternion_scalar - 1 == product_trace

    print("product T1*T2: PASS")
    print("  tetrahedral axis scalar product: -1/3")
    print(f"  quaternion scalar part: {quaternion_scalar}")
    print(f"  exact rotation trace: {product_trace}")
    print("  trace is a rational noninteger: yes")
    print("  product has infinite order: certified by the root-of-unity trace argument")


if __name__ == "__main__":
    main()
