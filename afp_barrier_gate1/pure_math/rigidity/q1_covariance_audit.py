#!/usr/bin/env python3
"""Exact Prompt-3 covariance and sampling-boundary regression.

Status: COMPUTATIONAL.  SymPy is used only for exact algebraic identities and
finite-rank certificates.  This script is not a replacement for the ordinary
proof or the Lean kernel formalization.

The audit deliberately distinguishes a trace-free quadratic *form* from its
sampled function.  On the octahedral nodes the three off-diagonal forms are in
the sampling kernel, while the genuine sampled degree-two exact space is zero.
"""
from __future__ import annotations

import itertools
import json

import sympy as sp


def assert_zero(value: sp.Expr | sp.MatrixBase, label: str) -> None:
    if isinstance(value, sp.MatrixBase):
        if any(sp.simplify(entry) != 0 for entry in value):
            raise AssertionError(f"{label}: nonzero matrix {value}")
        return
    if sp.simplify(value) != 0:
        raise AssertionError(f"{label}: {sp.simplify(value)}")


def sign_vectors(dimension: int) -> list[tuple[int, ...]]:
    return list(itertools.product((-1, 1), repeat=dimension))


def platonic_coordinate_data() -> dict[str, tuple[list[sp.Matrix], sp.Expr]]:
    """Return unnormalised equal-radius vertices and exact adjacent dot ratios."""
    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    invphi = 1 / phi

    tetrahedron = [
        sp.Matrix(v)
        for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    octahedron: list[sp.Matrix] = []
    for axis in range(3):
        for sign in (-1, 1):
            v = [0, 0, 0]
            v[axis] = sign
            octahedron.append(sp.Matrix(v))
    cube = [sp.Matrix(v) for v in sign_vectors(3)]
    icosahedron = [
        sp.Matrix(v)
        for v in (
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1),
        )
    ]
    dodecahedron = [sp.Matrix(v) for v in sign_vectors(3)]
    for zero_axis in range(3):
        # Cyclic coordinate patterns (0, +/-1/phi, +/-phi), together with their
        # coordinate rotations, give the remaining twelve dodecahedral nodes.
        first = (zero_axis + 1) % 3
        second = (zero_axis + 2) % 3
        for s1, s2 in itertools.product((-1, 1), repeat=2):
            v: list[sp.Expr] = [sp.Integer(0), sp.Integer(0), sp.Integer(0)]
            v[zero_axis] = sp.Integer(0)
            v[first] = s1 * invphi
            v[second] = s2 * phi
            dodecahedron.append(sp.Matrix(v))

    return {
        "tetrahedron": (tetrahedron, -sp.Rational(1, 3)),
        "octahedron": (octahedron, sp.Integer(0)),
        "cube": (cube, sp.Rational(1, 3)),
        "icosahedron": (icosahedron, 1 / sqrt5),
        "dodecahedron": (dodecahedron, sqrt5 / 3),
    }


def adjacency_from_dot(vertices: list[sp.Matrix], adjacent_dot: sp.Expr) -> list[set[int]]:
    norm2 = sp.simplify(vertices[0].dot(vertices[0]))
    if norm2 <= 0:
        raise AssertionError("nonpositive common squared radius")
    if any(sp.simplify(v.dot(v) - norm2) != 0 for v in vertices):
        raise AssertionError("coordinate radii differ")
    adjacency = [set() for _ in vertices]
    for i, j in itertools.combinations(range(len(vertices)), 2):
        if sp.simplify(vertices[i].dot(vertices[j]) / norm2 - adjacent_dot) == 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    return adjacency


def platonic_eigenmap_q_regressions() -> dict[str, object]:
    """Check the coordinate eigenmap, not merely the scalar Q formula."""
    expected = {
        "tetrahedron": (4, 3, True),
        "octahedron": (6, 4, True),
        "cube": (8, 3, False),
        "icosahedron": (12, 5, True),
        "dodecahedron": (20, 3, False),
    }
    report: dict[str, object] = {}
    for name, (vertices, cosine) in platonic_coordinate_data().items():
        adjacency = adjacency_from_dot(vertices, cosine)
        n, degree, triangulation = expected[name]
        degrees = {len(row) for row in adjacency}
        if len(vertices) != n or degrees != {degree}:
            raise AssertionError(f"{name}: wrong graph data {len(vertices)=}, {degrees=}")

        ell = sp.simplify(1 - cosine)
        rate = sp.simplify(2 / ell)
        edge_rate = sp.simplify(rate / degree)
        for i, vertex in enumerate(vertices):
            residual = sp.zeros(3, 1)
            for j in adjacency[i]:
                residual += edge_rate * (vertices[j] - vertex)
            assert_zero(residual + 2 * vertex, f"{name}: L Omega + 2 Omega at {i}")
        epsilon = sp.simplify(degree * edge_rate * ell**2)
        quality = sp.simplify(rate * epsilon / 4)
        assert_zero(quality - 1, f"{name}: Q-1")
        report[name] = {
            "vertices": n,
            "degree": degree,
            "cos_edge": str(sp.simplify(cosine)),
            "loss": str(ell),
            "row_rate": str(rate),
            "edge_rate": str(edge_rate),
            "epsilon": str(epsilon),
            "Q": str(quality),
            "coordinate_eigenmap": "exact",
            "sphere_triangulation": triangulation,
        }
    return report


def trace_free_sampling_matrix(nodes: list[sp.Matrix]) -> sp.Matrix:
    """Sample a fixed five-element basis of trace-free symmetric 3x3 forms."""
    basis = [
        sp.diag(1, -1, 0),
        sp.diag(1, 0, -1),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    ]
    return sp.Matrix([[sp.expand((x.T * form * x)[0]) for form in basis] for x in nodes])


def infinity_norm_contraction(matrix: list[list[sp.Rational]], vector: list[sp.Rational]) -> None:
    """Executable finite maximum-principle check with exact rationals."""
    if any(entry < 0 for row in matrix for entry in row):
        raise AssertionError("transition matrix has a negative entry")
    if any(sum(row, sp.Rational(0)) != 1 for row in matrix):
        raise AssertionError("transition matrix is not row stochastic")
    image = [sum((entry * value for entry, value in zip(row, vector)), sp.Rational(0))
             for row in matrix]
    source_norm = max(abs(value) for value in vector)
    image_norm = max(abs(value) for value in image)
    if image_norm > source_norm:
        raise AssertionError("row-stochastic infinity-norm contraction failed")


def weighted_octahedron_symbolic() -> dict[str, object]:
    g12, g13, g23 = sp.symbols("g12 g13 g23", positive=True)
    parameters = (g12, g13, g23)
    g = {(0, 1): g12, (0, 2): g13, (1, 2): g23}
    masses = [g12 + g13, g12 + g23, g13 + g23]
    identity = sp.eye(3)

    octahedral_nodes: list[sp.Matrix] = []
    node_axes: list[int] = []
    for axis in range(3):
        for sign in (-1, 1):
            node = sp.zeros(3, 1)
            node[axis, 0] = sign
            octahedral_nodes.append(node)
            node_axes.append(axis)
    rates = [[sp.Integer(0) for _ in octahedral_nodes] for _ in octahedral_nodes]
    for i, axis in enumerate(node_axes):
        for j, other in enumerate(node_axes):
            if axis != other:
                rates[i][j] = sp.simplify(g[tuple(sorted((axis, other)))] / masses[axis])
    for i, axis in enumerate(node_axes):
        for j, other in enumerate(node_axes):
            if axis != other:
                assert_zero(
                    masses[axis] * rates[i][j] - masses[other] * rates[j][i],
                    f"weighted octahedron detailed balance {i},{j}",
                )
        row_rate = sp.simplify(sum(rates[i]))
        assert_zero(row_rate - 2, f"weighted octahedron row rate {i}")
        generator_value = sum(
            (rates[i][j] * (octahedral_nodes[j] - octahedral_nodes[i])
             for j in range(len(octahedral_nodes))),
            sp.zeros(3, 1),
        )
        assert_zero(generator_value + 2 * octahedral_nodes[i],
                    f"weighted octahedron coordinate eigenmap {i}")
        losses = [sp.simplify(1 - octahedral_nodes[i].dot(octahedral_nodes[j]))
                  for j in range(len(octahedral_nodes))]
        epsilon = sp.simplify(sum(rates[i][j] * losses[j] ** 2
                                  for j in range(len(octahedral_nodes))))
        assert_zero(epsilon - 2, f"weighted octahedron epsilon {i}")
        assert_zero(row_rate * epsilon / 4 - 1, f"weighted octahedron Q {i}")

    tangential: list[sp.Matrix] = []
    covariance: list[sp.Matrix] = []
    residual: list[sp.Matrix] = []
    for axis in range(3):
        tangent = sp.zeros(3)
        for other in range(3):
            if axis == other:
                continue
            tangent[other, other] = sp.simplify(g[tuple(sorted((axis, other)))] / masses[axis])
        omega = sp.zeros(3, 1)
        omega[axis, 0] = 1
        tangent_projector = identity - omega * omega.T
        cov = sp.simplify(2 * omega * omega.T + 2 * tangent)
        res = sp.simplify(3 * (omega * omega.T - identity / 3)
                          + 2 * (tangent - tangent_projector / 2))
        assert_zero(sp.trace(tangent) - 1, f"axis {axis}: trace T")
        assert_zero(tangent * omega, f"axis {axis}: T Omega")
        assert_zero(sp.trace(cov) - 4, f"axis {axis}: trace C")
        assert_zero((omega.T * cov * omega)[0] - 2, f"axis {axis}: radial C")
        assert_zero(sp.trace(res), f"axis {axis}: trace M")

        # Compare the closed decomposition to the covariance obtained directly
        # from the symbolic six-state generator (the negative node has the same
        # radial projector and tangent frame).
        node_index = 2 * axis + 1
        direct_cov = sum(
            (rates[node_index][j]
             * (octahedral_nodes[j] - omega) * (octahedral_nodes[j] - omega).T
             for j in range(len(octahedral_nodes))),
            sp.zeros(3),
        )
        assert_zero(sp.simplify(direct_cov - cov), f"axis {axis}: direct C decomposition")
        direct_residual = sp.simplify(direct_cov + 2 * omega * omega.T - 2 * identity)
        assert_zero(direct_residual - res, f"axis {axis}: direct M decomposition")
        tangential.append(tangent)
        covariance.append(cov)
        residual.append(res)

    axial_differences = [
        sp.factor(tangential[0][1, 1] - tangential[0][2, 2]),
        sp.factor(tangential[1][0, 0] - tangential[1][2, 2]),
        sp.factor(tangential[2][0, 0] - tangential[2][1, 1]),
    ]
    expected_differences = [
        (g12 - g13) / (g12 + g13),
        (g12 - g23) / (g12 + g23),
        (g13 - g23) / (g13 + g23),
    ]
    for index, (actual, expected) in enumerate(zip(axial_differences, expected_differences)):
        assert_zero(actual - expected, f"axis {index}: axial condition")

    # On antipodally even samples, L=2(P-I).  For diagonal trace-free values
    # d=(d1,d2,-d1-d2), a degree-two target would require P d=-2d.
    d1, d2 = sp.symbols("d1 d2")
    diagonal_sample = sp.Matrix([d1, d2, -d1 - d2])
    equations: list[sp.Expr] = []
    for axis in range(3):
        p_value = sum(
            g[tuple(sorted((axis, other)))] * diagonal_sample[other]
            for other in range(3) if other != axis
        ) / masses[axis]
        equations.append(sp.factor(p_value + 2 * diagonal_sample[axis]))
    jacobian = sp.Matrix([[sp.diff(equations[row], variable) for variable in (d1, d2)]
                          for row in range(3)])
    leading_minor = sp.factor(jacobian.extract((0, 1), (0, 1)).det())
    expected_minor = sp.factor(3 * g12 * (g12 + g13 + g23)
                               / ((g12 + g13) * (g12 + g23)))
    assert_zero(leading_minor - expected_minor, "universal sampled-system minor")
    numerator, denominator = sp.fraction(sp.cancel(leading_minor))
    if numerator == 0 or denominator == 0:
        raise AssertionError("sampled-system minor vanished symbolically")
    polynomial = sp.Poly(numerator, *parameters)
    if not polynomial.terms() or any(coefficient <= 0 for _, coefficient in polynomial.terms()):
        raise AssertionError(f"minor positivity certificate failed: {polynomial}")

    # Explicitly retain the sampling kernel: the off-diagonal form columns are
    # zero, while the two diagonal trace-free columns span a two-dimensional
    # sampled image.
    sampling = trace_free_sampling_matrix(octahedral_nodes)
    if sampling.rank() != 2 or any(sampling[:, column] != sp.zeros(6, 1) for column in (2, 3, 4)):
        raise AssertionError(f"octahedral sampling-kernel certificate changed: {sampling}")
    ambient_form_dimension = 5
    exact_form_dimension = ambient_form_dimension - sampling.rank()
    if exact_form_dimension != 3:
        raise AssertionError(f"octahedral exact-form dimension changed: {exact_form_dimension}")

    # Exercise the maximum principle exactly on several positive conductance
    # specializations and adversarial sample vectors.
    specializations = ((1, 2, 5), (1, 1, 1), (1, 7, 3), (11, 2, 1))
    for h12, h13, h23 in specializations:
        rows = [
            [sp.Rational(0), sp.Rational(h12, h12 + h13), sp.Rational(h13, h12 + h13)],
            [sp.Rational(h12, h12 + h23), sp.Rational(0), sp.Rational(h23, h12 + h23)],
            [sp.Rational(h13, h13 + h23), sp.Rational(h23, h13 + h23), sp.Rational(0)],
        ]
        for vector in ([sp.Rational(1), -sp.Rational(1), sp.Rational(0)],
                       [sp.Rational(3, 2), -sp.Rational(2, 3), sp.Rational(7, 5)],
                       [sp.Rational(0), sp.Rational(0), sp.Rational(0)]):
            infinity_norm_contraction(rows, list(vector))

    unequal = {g12: sp.Integer(1), g13: sp.Integer(2), g23: sp.Integer(5)}
    anisotropy = sp.simplify(abs(g12 - g13) / (2 * (g12 + g13)))
    t = sp.symbols("t", positive=True)
    anisotropy_limit = sp.limit((t - 1) / (2 * (t + 1)), t, sp.oo)
    assert_zero(anisotropy_limit - sp.Rational(1, 2), "anisotropy limit")

    return {
        "parameters": [str(parameter) for parameter in parameters],
        "masses": [str(mass) for mass in masses],
        "row_rate": "2",
        "edge_loss": "1",
        "epsilon": "2",
        "Q": "1",
        "coordinate_eigenmap": "exact symbolic",
        "detailed_balance": "w_i a_ij = g_ab = w_j a_ji",
        "axial_all_vertices_iff": "g12 = g13 = g23",
        "axial_differences": [str(value) for value in axial_differences],
        "sampled_system_positive_minor": str(leading_minor),
        "ambient_trace_free_form_dimension": ambient_form_dimension,
        "sampling_rank": sampling.rank(),
        "sampling_kernel_dimension": exact_form_dimension,
        "exact_form_space": "sampling kernel K_X",
        "exact_form_space_dimension": exact_form_dimension,
        "genuine_sampled_degree_two_exact_space": "{0}",
        "genuine_sampled_degree_two_exact_dimension": 0,
        "sampled_certificate": "P f = -2 f and ||P f||_infinity <= ||f||_infinity",
        "unequal_specialization": {
            "parameters": [1, 2, 5],
            "masses": [str(sp.simplify(mass.subs(unequal))) for mass in masses],
            "T_plus_e1": [[str(sp.simplify(tangential[0][i, j].subs(unequal)))
                           for j in range(3)] for i in range(3)],
            "C_plus_e1": [[str(sp.simplify(covariance[0][i, j].subs(unequal)))
                           for j in range(3)] for i in range(3)],
            "M_plus_e1": [[str(sp.simplify(residual[0][i, j].subs(unequal)))
                           for j in range(3)] for i in range(3)],
        },
        "axis1_anisotropy": str(anisotropy),
        "anisotropy_limit": str(anisotropy_limit),
    }


def main() -> None:
    report = {
        "status_label": "COMPUTATIONAL",
        "platonic_coordinate_eigenmaps": platonic_eigenmap_q_regressions(),
        "weighted_octahedron": weighted_octahedron_symbolic(),
        "permanent_rejections": {
            "Q=1 forces axial covariance": "REJECTED",
            "form-space dimension is sampled-space dimension": "REJECTED",
            "unrestricted three-Platonic classification": "REJECTED by cube and dodecahedron",
        },
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
