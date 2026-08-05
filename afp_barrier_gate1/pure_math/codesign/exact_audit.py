"""Symbolic finite-algebra audit for P2C.

This module proves only the stable rational/algebraic identities it evaluates:
normalization, centering, the dense complete-graph H0/H1 construction, its
Lebedev-14 H2 defect, and the Paper-I constant sandwich.  It does not pretend
to formalize compactness, SDP duality, or asymptotic design existence.
"""

from __future__ import annotations

import json

import sympy as sp


def _lebedev14_exact() -> tuple[sp.Matrix, list[sp.Expr]]:
    axes = [
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ]
    r = 1 / sp.sqrt(3)
    cube = [(sx * r, sy * r, sz * r)
            for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    nodes = sp.Matrix(axes + cube)
    weights = [sp.Rational(1, 15)] * 6 + [sp.Rational(3, 40)] * 8
    return nodes, weights


def _dense_generator(nodes: sp.Matrix, weights: list[sp.Expr]) -> sp.Matrix:
    n = nodes.rows
    return sp.Matrix(
        n, n,
        lambda i, j: (
            2 * weights[j] if i != j
            else -2 * (1 - weights[i])
        ),
    )


def exact_audit() -> dict[str, str]:
    nodes, weights = _lebedev14_exact()
    n = nodes.rows
    one = sp.ones(n, 1)
    wrow = sp.Matrix(1, n, weights)
    generator = _dense_generator(nodes, weights)

    assert sp.simplify(sum(weights)) == 1
    assert all(sp.simplify((nodes.row(i) * nodes.row(i).T)[0] - 1) == 0
               for i in range(n))
    assert wrow * nodes == sp.zeros(1, 3)
    assert generator * one == sp.zeros(n, 1)
    assert generator * nodes == -2 * nodes
    assert sp.diag(*weights) * generator == generator.T * sp.diag(*weights)

    x, y, z = nodes[:, 0], nodes[:, 1], nodes[:, 2]
    shell = sp.Matrix.hstack(
        x.multiply_elementwise(y),
        y.multiply_elementwise(z),
        z.multiply_elementwise(x),
        x.multiply_elementwise(x) - y.multiply_elementwise(y),
        2 * z.multiply_elementwise(z)
        - x.multiply_elementwise(x)
        - y.multiply_elementwise(y),
    )
    gram = sp.simplify(shell.T * sp.diag(*weights) * shell)
    assert gram.det() != 0
    residual = sp.simplify((generator + 6 * sp.eye(n)) * shell)
    assert residual == 4 * shell
    assert sp.simplify(residual.T * sp.diag(*weights) * residual - 16 * gram) == sp.zeros(5)

    conductance_trace = sp.Integer(0)
    maximum_rate = sp.Integer(0)
    for i in range(n):
        rate = sp.Integer(0)
        for j in range(n):
            if i == j:
                continue
            c = 2 * weights[i] * weights[j]
            rate += c / weights[i]
            chord = nodes.row(i) - nodes.row(j)
            if i < j:
                conductance_trace += c * (chord * chord.T)[0]
        maximum_rate = sp.Max(maximum_rate, sp.simplify(rate))
    assert sp.simplify(conductance_trace) == 2
    assert sp.simplify(maximum_rate - sp.Rational(28, 15)) == 0

    h = sp.symbols("h", positive=True)
    lower = sp.Rational(3, 32) / sp.pi**2 * h**2
    rate_cap = 64 * sp.pi**2 / h**2
    upper = sp.Rational(75, 2) * h**2
    assert sp.simplify(lower * rate_cap) == 6
    assert sp.simplify(upper / h**2) == sp.Rational(75, 2)

    return {
        "mass": "1",
        "centering": "exact",
        "H0": "exact",
        "H1": "exact eigenvalue -2",
        "reversibility": "exact",
        "H2_dense_defect": "4",
        "trace_identity": "2",
        "maximum_rate": "28/15",
        "paper_I_lower_times_rate_cap": "6",
    }


def main() -> None:
    result = exact_audit()
    print(json.dumps(result, sort_keys=True))
    print("P2C_EXACT_AUDIT_PASS")


if __name__ == "__main__":
    main()
