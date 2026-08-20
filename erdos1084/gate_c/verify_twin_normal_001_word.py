#!/usr/bin/env python3
"""Exact rational certificate for a seven-letter FCC twin normal approximation."""

from __future__ import annotations

from fractions import Fraction as Q

Matrix = tuple[tuple[Q, Q, Q], tuple[Q, Q, Q], tuple[Q, Q, Q]]
Vector = tuple[Q, Q, Q]


def multiply(first: Matrix, second: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(first[row][index] * second[index][column] for index in range(3))
            for column in range(3)
        )
        for row in range(3)
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[column][row] for column in range(3)) for row in range(3))  # type: ignore[return-value]


def identity() -> Matrix:
    return (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
    )


def product(word: list[Matrix]) -> Matrix:
    result = identity()
    for matrix in word:
        result = multiply(result, matrix)
    return result


def apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


T1: Matrix = (
    (Q(2, 3), Q(-1, 3), Q(2, 3)),
    (Q(2, 3), Q(2, 3), Q(-1, 3)),
    (Q(-1, 3), Q(2, 3), Q(2, 3)),
)
T2: Matrix = (
    (Q(2, 3), Q(1, 3), Q(-2, 3)),
    (Q(-2, 3), Q(2, 3), Q(-1, 3)),
    (Q(1, 3), Q(2, 3), Q(2, 3)),
)

names = ["T2^-1", "T1", "T2^-1", "T1^-1", "T2", "T1^-1", "T2"]
word = [transpose(T2), T1, transpose(T2), transpose(T1), T2, transpose(T1), T2]
image = apply(product(word), (Q(1), Q(1), Q(1)))
expected = (Q(-125, 2187), Q(-229, 2187), Q(3779, 2187))
assert image == expected
assert sum(entry * entry for entry in image) == 3

transverse_sq = (image[0] ** 2 + image[1] ** 2) / 3
assert transverse_sq == Q(68066, 14348907)
assert transverse_sq < Q(1, 200)

print("FCC twin-word normal approximation: PASS")
print("  word length: 7")
print("  word: " + " ".join(names))
print("  reference normal numerator: (1,1,1)")
print("  image numerator: (-125,-229,3779)/2187")
print("  image numerator squared norm: 3")
print("  target normal: [001]")
print("  exact squared transverse error: 68066/14348907")
print("  certified bound: squared transverse error < 1/200")
