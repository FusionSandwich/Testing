#!/usr/bin/env python3
"""Exact fixtures for rejected algebraic/product P1E routes.

The accompanying proof, not this finite script, gives the all-level
obstructions.  These fixtures check the Pell double-cap collapse, the affine
rigidity of separable constant-norm composition maps, and the exact spectral
radial-normalization identity.  All decisions use integers or SymPy exact
algebra.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def assert_zero(value, label: str) -> None:
    value = sp.simplify(value)
    if value != 0:
        raise AssertionError(f"{label}: expected zero, got {value}")


def assert_matrix_zero(value: sp.Matrix, label: str) -> None:
    for row, column in product(range(value.rows), range(value.cols)):
        assert_zero(value[row, column], f"{label}[{row},{column}]")


def audit_pell_double_ball(levels: int = 8) -> int:
    """Check N^2-5a^2=1 and the exact north/south separation."""

    number, radial = 1, 0
    fixtures = 0
    for _ in range(levels):
        # Multiply N+a*sqrt(5) by the fundamental positive unit 9+4*sqrt(5).
        number, radial = 9 * number + 20 * radial, 4 * number + 9 * radial
        assert number * number - 5 * radial * radial == 1
        norm_sq = sp.Rational(5 * radial * radial, number * number)
        assert_zero(norm_sq - (1 - sp.Rational(1, number * number)),
                    "Pell cap radius")
        separation = sp.simplify(2 * (1 - norm_sq) / (1 + norm_sq))
        assert_zero(separation - sp.Rational(2, 2 * number * number - 1),
                    "Pell north/south separation")
        fixtures += 1
    return fixtures


def audit_composition_rigidity(total: int = 7, dimension: int = 3) -> int:
    """The only g with sum_a g(k_a) constant is affine on {0,...,N}."""

    rows = []
    reference = None
    for composition in compositions(total, dimension):
        row = [sp.Integer(0)] * (total + 1)
        for entry in composition:
            row[entry] += 1
        if reference is None:
            reference = row
        else:
            rows.append([left - right for left, right in zip(row, reference)])
    matrix = sp.Matrix(rows)
    nullspace = matrix.nullspace()
    if len(nullspace) != 2:
        raise AssertionError(f"composition nullity is {len(nullspace)}, expected 2")
    constant = sp.ones(total + 1, 1)
    affine = sp.Matrix(range(total + 1))
    assert_matrix_zero(matrix * constant, "composition constant sequence")
    assert_matrix_zero(matrix * affine, "composition affine sequence")
    if sp.Matrix.hstack(constant, affine).rank() != 2:
        raise AssertionError("constant and affine sequences lost independence")
    return 1


def audit_spectral_radial_normalization() -> int:
    """Exact nonconstant-row-norm fixture for the lemma in Section 5."""

    conductance = sp.ones(3) - sp.eye(3)
    f = sp.Matrix([
        [1, 1],
        [-1, 1],
        [0, -2],
    ])
    degree = sp.diag(*[sum(conductance[row, column] for column in range(3))
                       for row in range(3)])
    laplacian = conductance - degree
    assert_matrix_zero(laplacian * f + 3 * f, "common vector eigenmap")

    scales = [sp.sqrt((f.row(row) * f.row(row).T)[0]) for row in range(3)]
    if scales[0] == scales[2]:
        raise AssertionError("fixture accidentally has constant row norm")
    omega = sp.Matrix.vstack(*(f.row(row) / scales[row] for row in range(3)))
    transformed = sp.zeros(3)
    for row in range(3):
        for column in range(3):
            if row != column:
                transformed[row, column] = scales[row] * scales[column]

    for row in range(3):
        force = sp.zeros(2, 1)
        for column in range(3):
            force += transformed[row, column] * (
                omega.row(column).T - omega.row(row).T
            )
        tangent_test = sp.Matrix([-omega[row, 1], omega[row, 0]])
        assert_zero((tangent_test.T * force)[0],
                    f"radially normalized force row {row}")
        mass = sum(
            transformed[row, column]
            * (1 - (omega.row(row) * omega.row(column).T)[0])
            for column in range(3)
        )
        assert_matrix_zero(force + mass * omega.row(row).T,
                           f"radial contraction row {row}")
    return 1


def main() -> None:
    pell = audit_pell_double_ball()
    composition = audit_composition_rigidity()
    spectral = audit_spectral_radial_normalization()
    print(f"pell-double-ball-fixtures={pell}")
    print(f"composition-rigidity-fixtures={composition}")
    print(f"spectral-radial-normalization-fixtures={spectral}")
    print("P1E algebraic/product exact identities and blockers: PASS")
    print("P1E algebraic/product all-level construction: BLOCKED")


if __name__ == "__main__":
    main()
