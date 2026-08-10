#!/usr/bin/env python3
"""Exact audit of the centroidal-Voronoi P1E blocker.

The accompanying theorem note proves the spherical flux identity.  This
script checks, over exact SymPy arithmetic, the periodic affine-reflection
cell showing that centroidality and excellent mesh quality do not control the
quadratic moment.  Finite computation is used only as a regression test for
the displayed finite identities, not as an all-level proof.
"""

from __future__ import annotations

import sympy as sp


def assert_zero(value, label: str) -> None:
    value = sp.factor(sp.cancel(value))
    if value != 0:
        raise AssertionError(f"{label}: expected zero, got {value}")


def assert_matrix_zero(value: sp.Matrix, label: str) -> None:
    for row in range(value.rows):
        for column in range(value.cols):
            assert_zero(value[row, column], f"{label}[{row},{column}]")


def polygon_area(vertices: list[sp.Matrix]):
    twice = sp.S.Zero
    for p, q in zip(vertices, vertices[1:] + vertices[:1]):
        twice += p[0] * q[1] - p[1] * q[0]
    return sp.Abs(twice) / 2


def audit_reflection_cell() -> None:
    vertices = [
        sp.Matrix([-1, -1]),
        sp.Matrix([2, -1]),
        sp.Matrix([-1, 2]),
    ]
    centroid = sum(vertices, sp.zeros(2, 1)) / 3
    assert_matrix_zero(centroid, "triangle centroid")
    area = polygon_area(vertices)
    assert_zero(area - sp.Rational(9, 2), "triangle area")

    # Reflections of zero across x=-1, y=-1 and x+y=1.
    displacements = [
        sp.Matrix([-2, 0]),
        sp.Matrix([0, -2]),
        sp.Matrix([1, 1]),
    ]
    conductances = [sp.Rational(3, 2), sp.Rational(3, 2), sp.Integer(3)]
    force = sum(
        (weight * delta for weight, delta in zip(conductances, displacements)),
        sp.zeros(2, 1),
    )
    assert_matrix_zero(force, "centroidal finite-volume force")

    covariance = sum(
        (
            weight * delta * delta.T
            for weight, delta in zip(conductances, displacements)
        ),
        sp.zeros(2),
    )
    assert_matrix_zero(
        covariance - sp.Matrix([[9, 3], [3, 9]]),
        "anisotropic second moment",
    )
    anisotropy = covariance - 2 * area * sp.eye(2)
    assert_matrix_zero(anisotropy - sp.Matrix([[0, 3], [3, 0]]),
                       "trace-free anisotropy")

    # Q(x,y)=xy has continuum Laplacian zero, but graph residual 2/3.
    quadratic_flux = sum(
        weight * delta[0] * delta[1]
        for weight, delta in zip(conductances, displacements)
    )
    assert_zero(quadratic_flux / area - sp.Rational(2, 3),
                "unscaled quadratic residual")

    # Scaling cancels exactly: mass h^2, edge-vector product h^2.
    for scale in [sp.Rational(1, 2), sp.Rational(1, 17), sp.Rational(1, 10**9)]:
        scaled_mass = area * scale**2
        scaled_flux = sum(
            weight * (scale * delta[0]) * (scale * delta[1])
            for weight, delta in zip(conductances, displacements)
        )
        assert_zero(scaled_flux / scaled_mass - sp.Rational(2, 3),
                    f"scale-invariant residual h={scale}")

    # Exact mesh constants for the congruent reflection tessellation.
    separation = min(sp.sqrt((delta.T * delta)[0]) for delta in displacements)
    fill = max(sp.sqrt((vertex.T * vertex)[0]) for vertex in vertices)
    assert_zero(separation - sp.sqrt(2), "separation constant")
    assert_zero(fill - sp.sqrt(5), "fill constant")
    if min(conductances) <= 0:
        raise AssertionError("positive face-conductance margin was lost")

    # Enumerate a word ball in the three exact affine reflections.  It
    # contains the full first and second distance shells and certifies the
    # open cutoff window (2, 2 sqrt(2)) used in the theorem note.
    def reflect(point: tuple[int, int], wall: int) -> tuple[int, int]:
        x, y = point
        if wall == 0:
            return -2 - x, y
        if wall == 1:
            return x, -2 - y
        return 1 - y, 1 - x

    orbit = {(0, 0)}
    frontier = {(0, 0)}
    for _ in range(5):
        next_frontier = {
            reflect(point, wall)
            for point in frontier
            for wall in range(3)
        } - orbit
        orbit |= next_frontier
        frontier = next_frontier
    squared_shells = sorted(
        {sp.Integer(x * x + y * y) for x, y in orbit if (x, y) != (0, 0)}
    )
    if squared_shells[:3] != [sp.Integer(2), sp.Integer(4), sp.Integer(8)]:
        raise AssertionError(f"unexpected reflection distance shells: {squared_shells}")

    # The explicit cubic Hermite derivative from the theorem note.
    radius_symbol = sp.symbols("r", real=True)
    short, long = sp.sqrt(2), sp.Integer(2)
    parameter = (radius_symbol - short) / (long - short)
    h00 = 2 * parameter**3 - 3 * parameter**2 + 1
    h10 = parameter**3 - 2 * parameter**2 + parameter
    h01 = -2 * parameter**3 + 3 * parameter**2
    h11 = parameter**3 - parameter**2
    potential_derivative = sp.expand(
        3 * short * h00
        + 10 * (long - short) * h10
        + 3 * h01
        + 10 * (long - short) * h11
    )
    # Recompute directly in a fresh Bernstein parameter; SymPy does not treat
    # the compound expression used for ``parameter`` as a polynomial symbol.
    bernstein_parameter = sp.symbols("t", real=True)
    power_expression = sp.expand(
        3 * short * (2 * bernstein_parameter**3 - 3 * bernstein_parameter**2 + 1)
        + 10 * (long - short)
        * (bernstein_parameter**3 - 2 * bernstein_parameter**2 + bernstein_parameter)
        + 3 * (-2 * bernstein_parameter**3 + 3 * bernstein_parameter**2)
        + 10 * (long - short)
        * (bernstein_parameter**3 - bernstein_parameter**2)
    )
    polynomial = sp.Poly(power_expression, bernstein_parameter)
    coefficients = [polynomial.nth(index) for index in range(4)]
    bernstein = [
        coefficients[0],
        coefficients[0] + coefficients[1] / 3,
        coefficients[0] + 2 * coefficients[1] / 3 + coefficients[2] / 3,
        sum(coefficients),
    ]
    expected_bernstein = [
        3 * sp.sqrt(2),
        (20 - sp.sqrt(2)) / 3,
        (-11 + 10 * sp.sqrt(2)) / 3,
        sp.Integer(3),
    ]
    for index, (observed, expected) in enumerate(zip(bernstein, expected_bernstein)):
        assert_zero(observed - expected, f"Hermite Bernstein coefficient {index}")
        if sp.ask(sp.Q.positive(observed)) is not True:
            raise AssertionError("Hermite radial conductance margin lost positivity")
    hessian_data = [
        (short, 3 * short, sp.Integer(10)),
        (long, sp.Integer(3), sp.Integer(10)),
    ]
    for radius, first, second in hessian_data:
        assert_zero(potential_derivative.subs(radius_symbol, radius) - first,
                    f"Hermite first derivative r={radius}")
        assert_zero(
            sp.diff(potential_derivative, radius_symbol).subs(radius_symbol, radius)
            - second,
            f"Hermite second derivative r={radius}",
        )
        if sp.ask(sp.Q.positive(first / radius)) is not True:
            raise AssertionError("radial-energy transverse Hessian lost positivity")
        if sp.ask(sp.Q.positive(second)) is not True:
            raise AssertionError("radial-energy longitudinal Hessian lost positivity")


def main() -> None:
    audit_reflection_cell()
    print("fixtures=1")
    print("exact affine-reflection centroidal Voronoi cell: PASS")
    print("positive shared force balance and mesh margins: PASS")
    print("open radial cutoff and strict local Hessian margin: PASS")
    print("scale-independent 2/3 quadratic residual blocker: PASS")


if __name__ == "__main__":
    main()
