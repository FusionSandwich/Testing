#!/usr/bin/env python3
"""Exact D3 counterexample to an omitted invariance hypothesis.

The state space is {0,1} x Z/3Z.  Each layer is a three-cycle with unit
rates, and corresponding vertices in the two layers are joined at unit rate.
The diagonal D3 action on the Z/3Z coordinate commutes with the positive,
reversible generator.  The zero-sum standard module U0 supported on layer zero
is irreducible, but L(U0) has a nonzero component on layer one.  Thus
equivariance alone does not make a selected irreducible copy invariant.
"""

from __future__ import annotations

import sympy as sp


STATES = tuple((layer, k) for layer in (0, 1) for k in range(3))
INDEX = {state: i for i, state in enumerate(STATES)}


def assert_zero(value: sp.Expr | sp.Matrix, message: str) -> None:
    if isinstance(value, sp.MatrixBase):
        ok = value.applyfunc(sp.simplify) == sp.zeros(*value.shape)
    else:
        ok = sp.simplify(value) == 0
    if not ok:
        raise AssertionError(message)


def prism_generator() -> sp.Matrix:
    L = sp.zeros(6)
    for layer, k in STATES:
        i = INDEX[(layer, k)]
        neighbors = (
            (layer, (k + 1) % 3),
            (layer, (k - 1) % 3),
            (1 - layer, k),
        )
        for neighbor in neighbors:
            L[i, INDEX[neighbor]] = 1
        L[i, i] = -3
    return L


def d3_actions() -> tuple[tuple[int, ...], ...]:
    """The six affine maps k |-> sign*k+shift on both layers."""

    return tuple(
        tuple(INDEX[(layer, (sign * k + shift) % 3)] for layer, k in STATES)
        for sign in (1, -1)
        for shift in range(3)
    )


def permutation_matrix(action: tuple[int, ...]) -> sp.Matrix:
    P = sp.zeros(6)
    for i, image in enumerate(action):
        P[image, i] = 1
    return P


def exact_counterexample() -> None:
    L = prism_generator()
    if L != L.T:
        raise AssertionError("D3 generator is not reversible for unit masses")
    assert_zero(L * sp.ones(6, 1), "D3 generator is not conservative")
    for i in range(6):
        for j in range(6):
            if i != j and not bool(L[i, j] >= 0):
                raise AssertionError("D3 generator has a negative off-diagonal rate")
    edges = {(i, j) for i in range(6) for j in range(i + 1, 6) if L[i, j] > 0}
    if len(edges) != 9:
        raise AssertionError("D3 triangular-prism edge count changed")

    seen = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for j in range(6):
            if L[i, j] > 0 and j not in seen:
                seen.add(j)
                pending.append(j)
    if len(seen) != 6:
        raise AssertionError("D3 generator graph is disconnected")

    actions = d3_actions()
    if len(set(actions)) != 6:
        raise AssertionError("D3 action is not faithful")
    matrices = tuple(permutation_matrix(action) for action in actions)
    for P in matrices:
        assert_zero(P.T * P - sp.eye(6), "D3 action is not by permutations")
        assert_zero(P * L - L * P, "D3 action does not commute with L")
        assert_zero(P * sp.ones(6, 1) - sp.ones(6, 1),
                    "D3 action does not preserve unit masses")

    # U0 is the two-dimensional zero-sum module on layer zero.
    U0 = sp.Matrix.hstack(
        sp.Matrix((1, -1, 0, 0, 0, 0)),
        sp.Matrix((0, 1, -1, 0, 0, 0)),
    )
    if U0.rank() != 2:
        raise AssertionError("U0 does not have dimension two")
    assert_zero(sp.ones(1, 6) * U0, "U0 is not zero-sum")
    for P in matrices:
        if sp.Matrix.hstack(U0, P * U0).rank() != 2:
            raise AssertionError("U0 is not D3-invariant")

    # Rotation by one step has no real eigenline: its exact restriction has
    # characteristic polynomial t^2+t+1 with discriminant -3.  Any nonzero
    # proper real D3-submodule would be such a rotation-invariant line.
    rotation = permutation_matrix(actions[1])  # sign=+1, shift=1
    restriction = (U0.T * U0).inv() * U0.T * rotation * U0
    expected_restriction = sp.Matrix(((0, -1), (1, -1)))
    assert_zero(restriction - expected_restriction,
                "D3 rotation restriction changed")
    if restriction.trace() != -1 or restriction.det() != 1:
        raise AssertionError("D3 rotation characteristic polynomial changed")
    discriminant = restriction.trace() ** 2 - 4 * restriction.det()
    if discriminant != -3 or not bool(discriminant < 0):
        raise AssertionError("U0 irreducibility certificate failed")

    # For v in U0, the ring contribution is -3v and the vertical edge adds
    # -v on layer zero and +v on layer one: L(v,0)=(-4v,v).
    top = U0[:3, :]
    expected_image = sp.Matrix.vstack(-4 * top, top)
    assert_zero(L * U0 - expected_image, "exact L(U0)=(-4U0,U0) formula failed")
    lower_component = (L * U0)[3:6, :]
    if lower_component.rank() != 2:
        raise AssertionError("L(U0) has no certified component on layer one")
    if sp.Matrix.hstack(U0, L * U0).rank() == 2:
        raise AssertionError("negative test: U0 was incorrectly L-invariant")


def main() -> None:
    exact_counterexample()
    print("Exact D3 invariance counterexample: PASS")
    print("positive symmetric conservative connected triangular prism")
    print("U0: dim=2, irreducible (rotation discriminant=-3), not L-invariant")


if __name__ == "__main__":
    main()
