#!/usr/bin/env python3
"""Exact regression for the cotangent/tight-frame separation in the P1E cone audit.

This is a deterministic rational fixture, not evidence for an all-level
construction.  It falsifies the transfer ``positive cotangent equilibrium
implies a tight local covariance``.
"""

from fractions import Fraction as F


Vec = tuple[F, F]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1])


def dot(a: Vec, b: Vec) -> F:
    return a[0] * b[0] + a[1] * b[1]


def det(a: Vec, b: Vec) -> F:
    return a[0] * b[1] - a[1] * b[0]


def cot_at(p: Vec, a: Vec, b: Vec) -> F:
    x = sub(a, p)
    y = sub(b, p)
    return dot(x, y) / abs(det(x, y))


def half_cotangent_weights(points: list[Vec]) -> list[F]:
    zero = (F(0), F(0))
    weights: list[F] = []
    for k, u in enumerate(points):
        previous = points[k - 1]
        following = points[(k + 1) % len(points)]
        weights.append(
            F(1, 2)
            * (cot_at(previous, zero, u) + cot_at(following, u, zero))
        )
    return weights


def audit() -> None:
    points: list[Vec] = [
        (F(2), F(0)),
        (F(1), F(1)),
        (F(-3, 10), F(7, 5)),
        (F(-1), F(-1, 5)),
        (F(1, 5), F(-1)),
    ]
    expected = [F(4, 25), F(53, 68), F(762, 1241), F(349, 292), F(7, 5)]
    weights = half_cotangent_weights(points)

    assert weights == expected
    assert all(weight > 0 for weight in weights)
    assert all(det(points[k], points[(k + 1) % len(points)]) > 0 for k in range(5))

    force = [sum(weight * point[j] for weight, point in zip(weights, points)) for j in range(2)]
    assert force == [F(0), F(0)]

    covariance = [
        [sum(weight * point[i] * point[j] for weight, point in zip(weights, points)) for j in range(2)]
        for i in range(2)
    ]
    assert covariance == [
        [F(422852, 155125), F(29819, 62050)],
        [F(29819, 62050), F(8515, 2482)],
    ]
    assert covariance[0][0] - covariance[1][1] == F(-12863, 18250)
    assert covariance[0][1] == F(29819, 62050)


if __name__ == "__main__":
    audit()
    print("P1E icosahedral-cone exact cotangent audit: PASS")
