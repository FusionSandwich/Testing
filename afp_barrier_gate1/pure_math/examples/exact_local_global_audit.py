#!/usr/bin/env python3
"""Exact symbolic regression certificates for the local/global theorem package."""

from __future__ import annotations

import json
import sympy as sp


def zero(value: sp.Expr | sp.Matrix, label: str) -> None:
    entries = list(value) if isinstance(value, sp.MatrixBase) else [value]
    residual = [sp.simplify(x) for x in entries]
    if any(x != 0 for x in residual):
        raise AssertionError(f"{label}: {residual}")


def row_from_beta(beta: sp.Matrix, theta: tuple[sp.Expr, ...]) -> sp.Matrix:
    scale = sum((beta[j] * sp.tan(theta[j] / 2) for j in range(len(theta))), sp.S.Zero)
    return sp.Matrix([
        sp.simplify(2 * beta[j] / (sp.sin(theta[j]) * scale))
        for j in range(len(theta))
    ])


def check_local(u: sp.Matrix, beta: sp.Matrix, theta: tuple[sp.Expr, ...], rate=None):
    zero(sum(beta, sp.S.Zero) - 1, "beta normalization")
    zero(u * beta, "tangent dependence")
    a = row_from_beta(beta, theta)
    sine = sp.Matrix([sp.sin(x) for x in theta])
    loss = sp.Matrix([1 - sp.cos(x) for x in theta])
    zero(u * sp.matrix_multiply_elementwise(a, sine), "row tangent balance")
    zero(a.dot(loss) - 2, "row normal balance")
    if rate is not None:
        zero(sum(a, sp.S.Zero) - rate, "row rate")
    return a


def edge_column(nodes, edge):
    i, j = edge
    blocks = [sp.zeros(3, 1) for _ in nodes]
    blocks[i] = nodes[j] - nodes[i]
    blocks[j] = nodes[i] - nodes[j]
    return sp.Matrix.vstack(*blocks)


def main() -> None:
    e1, e2 = sp.Matrix([1, 0]), sp.Matrix([0, 1])

    # Boundary hull: the third indexed point is forced to coefficient zero.
    boundary_u = sp.Matrix.hstack(e1, -e1, e2)
    boundary_beta = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), 0])
    boundary_row = check_local(boundary_u, boundary_beta, (sp.pi / 3,) * 3)
    zero(boundary_row - sp.Matrix([2, 2, 0]), "boundary row")

    # Full-dimensional strict hull.
    tri_u = sp.Matrix([
        [1, sp.Rational(-1, 2), sp.Rational(-1, 2)],
        [0, sp.sqrt(3) / 2, -sp.sqrt(3) / 2],
    ])
    tri_beta = sp.Matrix([sp.Rational(1, 3)] * 3)
    tri_row = check_local(tri_u, tri_beta, (sp.pi / 3,) * 3, rate=4)
    zero(tri_row - sp.Matrix([sp.Rational(4, 3)] * 3), "triangle row")

    # Repeated indexed tangent direction with a different angle on one copy.
    repeated_u = sp.Matrix.hstack(e1, -e1, e2, -e2, e1)
    repeated_beta = sp.Matrix([
        sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 6),
        sp.Rational(1, 6), sp.Rational(1, 6),
    ])
    repeated_row = check_local(
        repeated_u, repeated_beta, (sp.pi / 4,) + (sp.pi / 3,) * 4
    )

    # Mixed boundary row: the antipode receives the remaining normal mass.
    mixed = sp.Matrix([1, 1, 0])
    zero(boundary_u * sp.matrix_multiply_elementwise(
        mixed, sp.Matrix([sp.sqrt(3) / 2] * 3)), "mixed tangent")
    zero(mixed.dot(sp.Matrix([sp.Rational(1, 2)] * 3)) + 2 * sp.Rational(1, 2) - 2,
         "mixed normal")

    # Centered unequal-mass square: local rows exist but shared conductance does not.
    nodes = (
        sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]),
        sp.Matrix([-1, 0, 0]), sp.Matrix([0, -1, 0]),
    )
    edges = ((0, 1), (1, 2), (2, 3), (3, 0))
    matrix = sp.Matrix.hstack(*(edge_column(nodes, e) for e in edges))
    masses = (1, 2, 1, 2)
    zero(sum((masses[i] * nodes[i] for i in range(4)), sp.zeros(3, 1)), "centering")
    rhs = sp.Matrix.vstack(*(-2 * masses[i] * nodes[i] for i in range(4)))
    signs = (-1, 1, -1, 1)
    witness = sp.Matrix.vstack(*(signs[i] * nodes[i] for i in range(4)))
    edge_work = matrix.T * witness
    dual_work = (rhs.T * witness)[0]
    zero(edge_work, "Farkas edge work")
    zero(dual_work + 4, "Farkas negative work")
    for i in range(4):
        js = ((i - 1) % 4, (i + 1) % 4)
        local = sum((nodes[j] - nodes[i] for j in js), sp.zeros(3, 1))
        zero(local + 2 * nodes[i], f"local row {i}")

    # Equal-mass symmetric square is globally strict.
    equal_rhs = sp.Matrix.vstack(*(-2 * x for x in nodes))
    zero(matrix * sp.ones(4, 1) - equal_rhs, "symmetric shared solution")

    print(json.dumps({
        "arithmetic": "exact symbolic",
        "local": {
            "boundary_row": [str(x) for x in boundary_row],
            "strict_triangle_row": [str(x) for x in tri_row],
            "repeated_row": [str(sp.simplify(x)) for x in repeated_row],
            "mixed_antipodal_row": ["1", "1", "0", "1/2"],
        },
        "global": {
            "edge_work": [str(x) for x in edge_work],
            "dual_work": str(dual_work),
            "symmetric_conductance": ["1"] * 4,
        },
        "role": "regression certificates, not general-theorem evidence",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
