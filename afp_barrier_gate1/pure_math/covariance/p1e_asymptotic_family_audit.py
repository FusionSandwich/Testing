#!/usr/bin/env python3
"""Deterministic exact/interval audit for the P1E construction.

The all-level geometric argument belongs to the accompanying P1E theorem.
This file checks its finite shared-stress algebra, the closed-form polygon
specialization, and the counterexamples which prevent several tempting
shortcuts.  Exact decisions use SymPy algebra.  Extreme-scale trigonometric
checks use outward-rounded ``mpmath.iv`` intervals.  No computed finite mesh
is promoted to an all-dimensional existence proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from mpmath import iv
import sympy as sp

import p1a_quadratic_fidelity_audit as p1a
import p1b_sharp_quadratic_defect_audit as p1b


def clean(value):
    return p1a.clean(value)


def assert_zero(value, label: str) -> None:
    p1a.assert_zero(value, label)


def assert_matrix_zero(matrix: sp.Matrix, label: str) -> None:
    p1a.assert_matrix_zero(matrix, label)


def assert_positive(value, label: str) -> None:
    value = clean(value)
    if value.is_positive is not True:
        raise AssertionError(f"{label}: expected exact positivity, got {value}")


def assert_nonnegative(value, label: str) -> None:
    value = clean(value)
    if value.is_nonnegative is not True:
        raise AssertionError(f"{label}: expected exact nonnegativity, got {value}")


def frobenius_sq(matrix: sp.Matrix):
    return clean(sp.trace(matrix.T * matrix))


@dataclass(frozen=True)
class StressCorrection:
    """Exact weighted minimum-energy correction on undirected edges."""

    tangent_operator: sp.Matrix
    baseline: sp.Matrix
    correction: sp.Matrix
    stress: sp.Matrix
    independent_rows: tuple[int, ...]
    multiplier: sp.Matrix


@dataclass(frozen=True)
class GeneratorData:
    """Normalized reversible generator and its quadratic row data."""

    masses: tuple[sp.Expr, ...]
    weights: tuple[sp.Expr, ...]
    rates: sp.Matrix
    generator: sp.Matrix
    row_rates: tuple[sp.Expr, ...]
    epsilon: tuple[sp.Expr, ...]
    moment_rows: tuple[sp.Matrix, ...]
    sampling: sp.Matrix
    residual: sp.Matrix
    defect_sq: sp.Expr


def tangent_operator(
    vertices: Sequence[sp.Matrix], edges: Sequence[tuple[int, int]]
) -> sp.Matrix:
    """Return ``T`` with ``(T gamma)_i=sum_j gamma_ij P_i x_j``.

    Each undirected edge has one column, so every output stress is shared by
    construction.  Keeping all ambient tangent coordinates makes the routine
    coordinate free at the algebraic level; exact row deflation below removes
    the radial and global-equilibrium dependencies.
    """

    if not vertices:
        raise ValueError("a stress graph needs at least one vertex")
    d = vertices[0].rows
    for index, vertex in enumerate(vertices):
        if vertex.cols != 1 or vertex.rows != d:
            raise ValueError("all vertices must be ambient column vectors")
        assert_zero((vertex.T * vertex)[0] - 1, f"unit vertex {index}")
    operator = sp.zeros(len(vertices) * d, len(edges))
    for edge_index, (i, j) in enumerate(edges):
        if i == j or not (0 <= i < len(vertices) and 0 <= j < len(vertices)):
            raise ValueError(f"invalid undirected edge {(i, j)}")
        for source, target in ((i, j), (j, i)):
            omega = vertices[source]
            projector = sp.eye(d) - omega * omega.T
            tangent = (projector * vertices[target]).applyfunc(clean)
            operator[source * d:(source + 1) * d, edge_index] = tangent
    return operator.applyfunc(clean)


def minimum_energy_shared_correction(
    vertices: Sequence[sp.Matrix],
    edges: Sequence[tuple[int, int]],
    baseline: Sequence[sp.Expr],
) -> StressCorrection:
    """Solve the exact shared-edge correction problem.

    This minimizes ``z.T * diag(baseline)^-1 * z / 2`` subject to
    ``T z = -T baseline``.  Independent constraint rows are selected by exact
    RREF, never a floating rank threshold.  Positivity is intentionally not
    assumed: it is a separate interior-margin property checked by each
    construction fixture.
    """

    operator = tangent_operator(vertices, edges)
    gamma0 = sp.Matrix([clean(value) for value in baseline])
    if gamma0.rows != len(edges):
        raise ValueError("one baseline conductance is required per edge")
    for edge_index, value in enumerate(gamma0):
        assert_positive(value, f"baseline conductance {edge_index}")

    # Pivot columns of T^T are independent rows of T.
    independent_rows = tuple(int(i) for i in operator.T.rref()[1])
    if not independent_rows:
        correction = sp.zeros(len(edges), 1)
        return StressCorrection(
            operator, gamma0, correction, gamma0, (), sp.zeros(0, 1)
        )
    constraints = operator[list(independent_rows), :]
    right_hand_side = -(operator * gamma0)[list(independent_rows), :]
    metric = sp.diag(*gamma0)
    schur = (constraints * metric * constraints.T).applyfunc(clean)
    if clean(schur.det()) == 0:
        raise AssertionError("exact row deflation did not produce a nonsingular Schur matrix")
    multiplier = (schur.inv() * right_hand_side).applyfunc(clean)
    correction = (metric * constraints.T * multiplier).applyfunc(clean)
    stress = (gamma0 + correction).applyfunc(clean)

    assert_matrix_zero(operator * stress, "corrected tangent equilibrium")
    assert_matrix_zero(
        correction - metric * constraints.T * multiplier,
        "minimum-energy KKT equation",
    )
    inverse_metric = sp.diag(*(clean(1 / value) for value in gamma0))
    for index, null_direction in enumerate(operator.nullspace()):
        assert_zero(
            (null_direction.T * inverse_metric * correction)[0],
            f"minimum-energy nullspace orthogonality {index}",
        )
    return StressCorrection(
        operator, gamma0, correction, stress, independent_rows, multiplier
    )


def quotient_defect_sq(sampling: sp.Matrix, residual: sp.Matrix, weights):
    """Compute the exact sampling-kernel-deflated generalized norm."""

    gram_s = (sampling.T * sp.diag(*weights) * sampling).applyfunc(clean)
    gram_r = (residual.T * sp.diag(*weights) * residual).applyfunc(clean)
    sampled = gram_s.columnspace()
    if not sampled:
        raise AssertionError("unit-node degree-two sampling unexpectedly has rank zero")
    lift = sp.Matrix.hstack(*sampled)
    reduced_s = (lift.T * gram_s * lift).applyfunc(clean)
    reduced_r = (lift.T * gram_r * lift).applyfunc(clean)
    if clean(reduced_s.det()) == 0:
        raise AssertionError("exact quotient deflation left a singular sampling Gram")
    pencil = (reduced_s.inv() * reduced_r).applyfunc(clean)
    eigenvalues: list[sp.Expr] = []
    for value, multiplicity in pencil.eigenvals().items():
        eigenvalues.extend([clean(value)] * multiplicity)
    return p1a.exact_max(
        eigenvalues, "P1E exact quotient maximum", require_nonnegative=True
    )


def generator_from_shared_stress(
    vertices: Sequence[sp.Matrix],
    edges: Sequence[tuple[int, int]],
    stress: Sequence[sp.Expr],
) -> GeneratorData:
    """Normalize a positive equilibrium stress and audit all finite identities."""

    count, d = len(vertices), vertices[0].rows
    tangent_dimension = d - 1
    if tangent_dimension < 1:
        raise ValueError("the spherical construction requires d>=2")
    gamma = tuple(clean(value) for value in stress)
    for edge_index, value in enumerate(gamma):
        assert_positive(value, f"corrected conductance {edge_index}")
    operator = tangent_operator(vertices, edges)
    assert_matrix_zero(operator * sp.Matrix(gamma), "input stress equilibrium")

    incident: list[list[tuple[int, sp.Expr]]] = [[] for _ in vertices]
    for (i, j), value in zip(edges, gamma):
        incident[i].append((j, value))
        incident[j].append((i, value))

    masses: list[sp.Expr] = []
    for i, omega in enumerate(vertices):
        loss_sum = sum(
            value * clean(1 - (omega.T * vertices[j])[0])
            for j, value in incident[i]
        )
        mass = clean(loss_sum / tangent_dimension)
        assert_positive(mass, f"unnormalized mass {i}")
        masses.append(mass)
    total_mass = clean(sum(masses))
    weights = tuple(clean(value / total_mass) for value in masses)
    assert_zero(sum(weights) - 1, "normalized mass sum")

    rates = sp.zeros(count)
    normalized_conductance = sp.zeros(count)
    for (i, j), value in zip(edges, gamma):
        rates[i, j] = clean(value / masses[i])
        rates[j, i] = clean(value / masses[j])
        normalized_conductance[i, j] = normalized_conductance[j, i] = clean(
            value / total_mass
        )
        assert_zero(
            weights[i] * rates[i, j] - weights[j] * rates[j, i],
            f"detailed balance edge {i},{j}",
        )
    generator = p1b.generator_from_rates(rates)
    ones = sp.ones(count, 1)
    node_matrix = sp.Matrix.vstack(*(omega.T for omega in vertices))
    assert_matrix_zero(generator * ones, "H0 reproduction")
    assert_matrix_zero(
        generator * node_matrix + tangent_dimension * node_matrix,
        "H1 reproduction",
    )

    basis = p1a.sym0_orthonormal_basis(d)
    sampling = sp.Matrix(
        count,
        len(basis),
        lambda i, k: clean((vertices[i].T * basis[k] * vertices[i])[0]),
    )
    residual = ((generator + 2 * d * sp.eye(count)) * sampling).applyfunc(clean)

    identity = sp.eye(d)
    row_rates: list[sp.Expr] = []
    epsilons: list[sp.Expr] = []
    moment_rows: list[sp.Matrix] = []
    for i, omega in enumerate(vertices):
        covariance = sp.zeros(d)
        epsilon = sp.S.Zero
        row_rate = sp.S.Zero
        unnormalized_moment = sp.zeros(d)
        projector = identity - omega * omega.T
        for j, value in incident[i]:
            delta = vertices[j] - omega
            loss = clean(1 - (omega.T * vertices[j])[0])
            rate = clean(value / masses[i])
            row_rate += rate
            epsilon += rate * loss ** 2
            covariance += rate * delta * delta.T
            unnormalized_moment += value * (
                delta * delta.T - clean(2 * loss / tangent_dimension) * projector
            )
        covariance = covariance.applyfunc(clean)
        epsilon, row_rate = clean(epsilon), clean(row_rate)
        row_representer = (
            covariance + 2 * omega * omega.T - 2 * identity
        ).applyfunc(clean)
        assert_matrix_zero(
            row_representer - (unnormalized_moment / masses[i]).applyfunc(clean),
            f"shared-stress quadratic moment row {i}",
        )
        for k, coefficient in enumerate(basis):
            assert_zero(
                residual[i, k] - sp.trace(row_representer.T * coefficient),
                f"residual row-representer identity {i},{k}",
            )
        row_rates.append(row_rate)
        epsilons.append(epsilon)
        moment_rows.append(row_representer)

    defect_sq = quotient_defect_sq(sampling, residual, weights)
    return GeneratorData(
        tuple(masses), weights, rates, generator, tuple(row_rates),
        tuple(epsilons), tuple(moment_rows), sampling, residual, defect_sq,
    )


def audit_correction_fixture(
    name: str,
    vertices: Sequence[sp.Matrix],
    edges: Sequence[tuple[int, int]],
    baseline: Sequence[sp.Expr],
    expected_stress: sp.Expr,
    expected_rate: sp.Expr,
    expected_scalar: sp.Expr,
) -> None:
    correction = minimum_energy_shared_correction(vertices, edges, baseline)
    if correction.tangent_operator * correction.baseline == sp.zeros(
        correction.tangent_operator.rows, 1
    ):
        raise AssertionError(f"{name}: baseline was accidentally already equilibrated")
    for edge_index, value in enumerate(correction.stress):
        assert_zero(value - expected_stress, f"{name}: corrected stress {edge_index}")
    data = generator_from_shared_stress(vertices, edges, correction.stress)
    assert_zero(data.defect_sq - expected_scalar ** 2, f"{name}: quotient defect")
    for i, row_rate in enumerate(data.row_rates):
        assert_zero(row_rate - expected_rate, f"{name}: row rate {i}")
        assert_zero(
            data.epsilon[i] - sp.Rational(vertices[0].rows - 1, vertices[0].rows)
            * expected_scalar,
            f"{name}: epsilon {i}",
        )
    assert_zero(
        expected_scalar * expected_rate
        - vertices[0].rows * (vertices[0].rows - 1),
        f"{name}: sharp rate-defect product",
    )
    for i, moment in enumerate(data.moment_rows):
        d = vertices[0].rows
        z_row = vertices[i] * vertices[i].T - sp.eye(d) / d
        assert_matrix_zero(
            moment - expected_scalar * z_row,
            f"{name}: scalar quadratic row {i}",
        )


def audit_shared_corrections() -> None:
    square = [
        sp.Matrix([1, 0]), sp.Matrix([0, 1]),
        sp.Matrix([-1, 0]), sp.Matrix([0, -1]),
    ]
    square_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    audit_correction_fixture(
        "square",
        square,
        square_edges,
        [1, sp.Rational(6, 5), sp.Rational(4, 5), 1],
        sp.Rational(48, 49),
        sp.Integer(1),
        sp.Integer(2),
    )

    tetrahedron = p1a.regular_simplex(3)
    tetrahedron_edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    audit_correction_fixture(
        "tetrahedron",
        tetrahedron,
        tetrahedron_edges,
        [1, sp.Rational(11, 10), sp.Rational(9, 10),
         sp.Rational(6, 5), sp.Rational(4, 5), 1],
        sp.Rational(2376, 2417),
        sp.Rational(3, 2),
        sp.Integer(4),
    )


def audit_sampling_kernel_fixture() -> None:
    """An antipodal exact generator with a nontrivial quadratic alias."""

    vertices = [sp.Matrix([1, 0]), sp.Matrix([-1, 0])]
    edges = [(0, 1)]
    baseline = [sp.Rational(7, 3)]
    correction = minimum_energy_shared_correction(vertices, edges, baseline)
    assert_matrix_zero(correction.correction, "antipodal zero tangent correction")
    data = generator_from_shared_stress(vertices, edges, correction.stress)
    if data.sampling.rank() != 1 or data.sampling.cols != 2:
        raise AssertionError("antipodal fixture lost its exact sampling kernel")
    assert_matrix_zero(data.residual - 4 * data.sampling,
                       "antipodal scalar quotient residual")
    assert_zero(data.defect_sq - 16, "antipodal kernel-correct quotient defect")
    for rate in data.row_rates:
        assert_zero(rate - sp.Rational(1, 2), "antipodal row rate")


def balanced_coset_law(theta: sp.Rational):
    """Exact four-point law on ``theta + Z`` with zero first/cubic moments.

    The proof uses flux weights.  Negative and positive squared-length
    intervals overlap; the two conditional flux distributions are chosen to
    have the same squared-length mean.  Dividing flux by length then kills
    both the ordinary first moment and the cubic moment with strictly positive
    weights.  This is the finite connector used by the Coxeter crystal
    compiler; no floating feasibility solve is involved.
    """

    if not (-sp.Rational(1, 2) <= theta < sp.Rational(1, 2)):
        raise ValueError("the coset representative must lie in [-1/2,1/2)")
    radius, span = sp.Integer(2), sp.Integer(2)
    a = clean(radius - theta)
    b = clean(radius + span - theta)
    p = clean(radius + theta)
    q = clean(radius + span + theta)
    lower_square = p ** 2 if theta >= 0 else a ** 2
    upper_square = b ** 2 if theta >= 0 else q ** 2
    shared_square = clean((lower_square + upper_square) / 2)
    negative_flux = (
        clean((b ** 2 - shared_square) / (b ** 2 - a ** 2)),
        clean((shared_square - a ** 2) / (b ** 2 - a ** 2)),
    )
    positive_flux = (
        clean((q ** 2 - shared_square) / (q ** 2 - p ** 2)),
        clean((shared_square - p ** 2) / (q ** 2 - p ** 2)),
    )
    points = (-a, -b, p, q)
    raw_weights = (
        clean(negative_flux[0] / a),
        clean(negative_flux[1] / b),
        clean(positive_flux[0] / p),
        clean(positive_flux[1] / q),
    )
    normalizer = clean(sum(raw_weights))
    weights = tuple(clean(weight / normalizer) for weight in raw_weights)
    assert_zero(sum(weights) - 1, "coset connector probability mass")
    for index, weight in enumerate(weights):
        assert_positive(weight, f"coset connector weight {index}")
        assert_nonnegative(
            weight - sp.Rational(1, 56),
            f"coset connector uniform weight floor {index}",
        )
    assert_zero(sum(weight * point for weight, point in zip(weights, points)),
                "coset connector first moment")
    assert_zero(sum(weight * point ** 3 for weight, point in zip(weights, points)),
                "coset connector cubic moment")
    second = clean(
        sum(weight * point ** 2 for weight, point in zip(weights, points))
    )
    assert_nonnegative(second - sp.Rational(9, 4),
                       "coset connector second-moment floor")
    assert_nonnegative(sp.Rational(81, 4) - second,
                       "coset connector second-moment ceiling")
    return points, weights


def audit_crystal_connector(theta: sp.Rational) -> None:
    """One-dimensional shared connector and its exact optical gap."""

    points, weights = balanced_coset_law(theta)
    total = clean(sum(weights))
    optical = sp.Matrix([[total, -total], [-total, total]])
    assert_matrix_zero(optical * sp.ones(2, 1), "connector acoustic kernel")
    eigenvalues = optical.eigenvals()
    if clean(eigenvalues.get(sp.S.Zero, 0) - 1) != 0:
        raise AssertionError("connector optical matrix has the wrong kernel")
    assert_positive(clean(2 * total), "connector optical eigenvalue")
    # Reversing an undirected edge negates every displacement but leaves the
    # same positive weight and second moment.
    assert_zero(sum(w * (-z) for w, z in zip(weights, points)),
                "reversed connector first moment")
    assert_zero(sum(w * (-z) ** 3 for w, z in zip(weights, points)),
                "reversed connector cubic moment")


def audit_tensor_crystal_connector() -> None:
    """Tensor products kill every component of the full cubic tensor."""

    laws = [balanced_coset_law(sp.Rational(1, 3)),
            balanced_coset_law(-sp.Rational(2, 5))]
    points: list[sp.Matrix] = []
    weights: list[sp.Expr] = []
    for i, zi in enumerate(laws[0][0]):
        for j, zj in enumerate(laws[1][0]):
            points.append(sp.Matrix([zi, zj]))
            weights.append(clean(laws[0][1][i] * laws[1][1][j]))
    mean = sum((w * z for w, z in zip(weights, points)), sp.zeros(2, 1))
    assert_matrix_zero(mean, "tensor connector first moment")
    for a in range(2):
        for b in range(2):
            for c in range(2):
                assert_zero(
                    sum(w * z[a] * z[b] * z[c]
                        for w, z in zip(weights, points)),
                    f"tensor connector cubic moment {a}{b}{c}",
                )
    covariance = sum(
        (w * z * z.T for w, z in zip(weights, points)), sp.zeros(2)
    ).applyfunc(clean)
    assert_zero(covariance[0, 1], "tensor connector cross covariance")
    assert_positive(covariance[0, 0], "tensor connector first variance")
    assert_positive(covariance[1, 1], "tensor connector second variance")
    assert_positive(clean(covariance.det()), "tensor connector SPD determinant")


def audit_parabolic_nonperiodicity_blocker() -> None:
    """Exact residue mutation rejecting the raw K_N Bloch compiler.

    For block sizes |Z|=2, |B|=3, write a=k1-k2 and let p,q be
    two independent B-block differences.  Integer solvability is exactly
    p+q+abs(a) == N (mod 3).  A putative period (A,P,Q) would force
    P+Q+abs(a+A)-abs(a) == 0 (mod 3) for every a.  The theorem note
    proves from the positive, negative, and crossing ranges that this implies
    A=0, so the period group cannot have full rank.  The bounded loop
    below is a mutation regression for that all-integer proof, not its
    substitute.
    """

    modulus = 3
    for shift in range(-12, 13):
        if shift == 0:
            continue
        for tangential_sum in range(modulus):
            preserved = all(
                (
                    tangential_sum
                    + abs(a + shift)
                    - abs(a)
                ) % modulus == 0
                for a in range(-24, 25)
            )
            if preserved:
                raise AssertionError(
                    "raw parabolic residue unexpectedly admitted a normal period "
                    f"A={shift}, P+Q={tangential_sum}"
                )

    # A normal-zero translation preserves the condition exactly iff P+Q=0.
    for tangential_sum in range(modulus):
        preserved = all(
            (tangential_sum + abs(a) - abs(a)) % modulus == 0
            for a in range(-24, 25)
        )
        if preserved != (tangential_sum == 0):
            raise AssertionError("normal-zero parabolic period classification failed")


def audit_polygon_symbolic() -> None:
    """Polynomial proof of the regular-polygon row identities for every N."""

    c, s = sp.symbols("c s", real=True, positive=True)
    # cos(2h), sin(2h), with only the relation c^2+s^2=1 used.
    cosine = c ** 2 - s ** 2
    sine = 2 * c * s
    omega = sp.Matrix([1, 0])
    neighbors = [sp.Matrix([cosine, sine]), sp.Matrix([cosine, -sine])]
    rate = 1 / (4 * s ** 2)

    def reduce_unit(value):
        return sp.factor(sp.together(value).subs(c ** 2, 1 - s ** 2))

    h1 = rate * sum((neighbor - omega for neighbor in neighbors), sp.zeros(2, 1))
    for coordinate in range(2):
        assert_zero(reduce_unit(h1[coordinate] + omega[coordinate]),
                    f"all-N polygon H1 coordinate {coordinate}")
    loss = reduce_unit(1 - (omega.T * neighbors[0])[0])
    assert_zero(loss - 2 * s ** 2, "all-N polygon chordal loss")
    row_rate = clean(2 * rate)
    epsilon = reduce_unit(2 * rate * loss ** 2)
    assert_zero(row_rate - 1 / (2 * s ** 2), "all-N polygon rate")
    assert_zero(epsilon - 2 * s ** 2, "all-N polygon epsilon")
    covariance = sum(
        (rate * (neighbor - omega) * (neighbor - omega).T for neighbor in neighbors),
        sp.zeros(2),
    )
    covariance = covariance.applyfunc(reduce_unit)
    moment = (covariance + 2 * omega * omega.T - 2 * sp.eye(2)).applyfunc(reduce_unit)
    z_row = omega * omega.T - sp.eye(2) / 2
    assert_matrix_zero(
        (moment - 4 * s ** 2 * z_row).applyfunc(reduce_unit),
        "all-N polygon scalar row",
    )
    assert_zero(4 * s ** 2 * row_rate - 2, "all-N polygon sharp product")


def audit_polygon_level(number_of_vertices: int) -> None:
    """Exact whole-generator check at algebraic representative levels."""

    number = sp.Integer(number_of_vertices)
    h = sp.pi / number
    vertices = [
        sp.Matrix([
            sp.cos(2 * sp.pi * k / number),
            sp.sin(2 * sp.pi * k / number),
        ])
        for k in range(number_of_vertices)
    ]
    edges = [(k, (k + 1) % number_of_vertices) for k in range(number_of_vertices)]
    stress = [sp.Integer(1)] * number_of_vertices
    data = generator_from_shared_stress(vertices, edges, stress)
    scalar = clean(4 * sp.sin(h) ** 2)
    assert_zero(data.defect_sq - scalar ** 2,
                f"polygon N={number_of_vertices}: exact quotient defect")
    assert_matrix_zero(
        data.residual - scalar * data.sampling,
        f"polygon N={number_of_vertices}: scalar residual",
    )
    assert_nonnegative(4 * h ** 2 - scalar,
                       f"polygon N={number_of_vertices}: D2 upper bound")
    rate = data.row_rates[0]
    for observed in data.row_rates:
        assert_zero(observed - rate, f"polygon N={number_of_vertices}: common rate")
    assert_zero(scalar * rate - 2, f"polygon N={number_of_vertices}: frontier")


def audit_cycle_ratio_blocker() -> None:
    """Exact H1 rows whose Kolmogorov cycle ratio is 21/4."""

    e = [sp.eye(3)[:, k] for k in range(3)]
    vertices = [e[0], -e[0], e[1], -e[1], e[2], -e[2]]
    c = sp.Matrix([
        [0, sp.Rational(9, 10), sp.Rational(1, 10)],
        [sp.Rational(4, 5), 0, sp.Rational(1, 5)],
        [sp.Rational(7, 10), sp.Rational(3, 10), 0],
    ])
    rates = sp.zeros(6)
    for source_axis in range(3):
        for source_sign in range(2):
            source = 2 * source_axis + source_sign
            for target_axis in range(3):
                if source_axis == target_axis:
                    continue
                for target_sign in range(2):
                    rates[source, 2 * target_axis + target_sign] = c[
                        source_axis, target_axis
                    ]
    generator = p1b.generator_from_rates(rates)
    node_matrix = sp.Matrix.vstack(*(omega.T for omega in vertices))
    assert_matrix_zero(generator * node_matrix + 2 * node_matrix,
                       "21/4 blocker exact H1")
    ratio = clean(c[0, 1] * c[1, 2] * c[2, 0]
                  / (c[1, 0] * c[2, 1] * c[0, 2]))
    assert_zero(ratio - sp.Rational(21, 4), "Kolmogorov cycle ratio")
    if ratio == 1:
        raise AssertionError("21/4 blocker accidentally became reversible")


def audit_delaunay_star_blocker() -> None:
    directions = [sp.Matrix([1, 0]), sp.Matrix([0, 1]), sp.Matrix([-1, -1])]
    covariance = sum(
        (2 * direction * direction.T for direction in directions), sp.zeros(2)
    )
    expected = sp.Matrix([[4, 2], [2, 4]])
    assert_matrix_zero(covariance - expected, "Delaunay tangent-star covariance")
    # Dividing by the limiting mass two gives the matrix in the theorem.
    normalized = covariance / 2
    anisotropy = normalized - 2 * sp.eye(2)
    assert_zero(frobenius_sq(anisotropy) - 2,
                "Delaunay tangent-star anisotropy floor")


def audit_cubed_sphere_seam_blocker() -> None:
    """Natural cubed-sphere tight rows force a binomial shared stress."""

    t = sp.symbols("t", real=True)
    y = sp.Matrix([1, 1, t])
    scale_sq = clean((y.T * y)[0])
    projector = (sp.eye(3) - y * y.T / scale_sq).applyfunc(clean)
    e1, e2, e3 = (sp.eye(3)[:, k] for k in range(3))
    seam = (projector * e3).applyfunc(clean)
    inward_a = (projector * (-e2)).applyfunc(clean)
    inward_b = (projector * (-e1)).applyfunc(clean)
    cross_normal = (e1 - e2) / 2
    assert_matrix_zero(
        inward_a - cross_normal - t * seam / 2,
        "cubed seam first inward decomposition",
    )
    assert_matrix_zero(
        inward_b + cross_normal - t * seam / 2,
        "cubed seam second inward decomposition",
    )
    plus = clean((1 - t) / 2)
    minus = clean((1 + t) / 2)
    force = (inward_a + inward_b + (plus - minus) * seam).applyfunc(clean)
    assert_matrix_zero(force, "cubed seam local tangent balance")
    covariance = (
        inward_a * inward_a.T
        + inward_b * inward_b.T
        + (plus + minus) * seam * seam.T
    ).applyfunc(clean)
    assert_matrix_zero(
        covariance - projector,
        "cubed seam local tangent tight frame",
    )

    number = 12
    profile = [sp.Integer(1)]
    for k in range(number):
        profile.append(clean(profile[-1] * sp.Rational(number - k, k + 1)))
    for k, value in enumerate(profile):
        assert_zero(value - sp.binomial(number, k),
                    f"cubed seam binomial sharedness k={k}")
    assert_nonnegative(
        max(profile) - sp.Rational(2 ** number, number + 1),
        "cubed seam exponential margin loss",
    )

    # The signed d=4 cube-corner rays are a regular-simplex tight frame.
    dimension = 4
    corner = sp.ones(dimension, 1) / sp.sqrt(dimension)
    corner_projector = sp.eye(dimension) - corner * corner.T
    rays = [-(corner_projector * sp.eye(dimension)[:, k])
            for k in range(dimension)]
    assert_matrix_zero(sum(rays, sp.zeros(dimension, 1)),
                       "cubed corner tangent balance")
    corner_covariance = sum(
        (ray * ray.T for ray in rays), sp.zeros(dimension)
    )
    assert_matrix_zero(corner_covariance - corner_projector,
                       "cubed corner simplex tight frame")


def audit_alternating_gap_blocker() -> None:
    s, rho = sp.symbols("s rho", positive=True, real=True)
    alpha, beta = s * (1 + rho), s * (1 - rho)
    a_term = 4 * (
        1 - sp.cos(rho * s) * sp.cos(alpha / 2) * sp.cos(beta / 2)
    )
    b_term = -4 * sp.cos(alpha / 2) * sp.cos(beta / 2) * sp.sin(rho * s)
    assert_zero(sp.limit(a_term / s, s, 0), "alternating-gap radial limit")
    assert_zero(sp.limit(b_term / s, s, 0) + 4 * rho,
                "alternating-gap first-order tensor limit")
    limit_sq = clean(sp.limit((a_term ** 2 + b_term ** 2) / s ** 2, s, 0))
    assert_zero(limit_sq - 16 * rho ** 2, "alternating-gap defect limit")


def audit_positive_filter_blocker() -> None:
    """Exact mutations of the positive-filter amplification inequality."""

    n, tau = sp.Integer(2), sp.Rational(1, 10)
    beta = clean(1 - n * tau)
    filters = [
        (sp.Rational(0), sp.Rational(1)),
        (sp.Rational(1, 2), sp.Rational(0), sp.Rational(1, 2)),
        (sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(1, 3)),
        (sp.Rational(1, 10), 0, 0, 0, 0, sp.Rational(9, 10)),
    ]
    for filter_index, coefficients in enumerate(filters):
        assert_zero(sum(coefficients) - 1, f"filter {filter_index}: Markov mass")
        phi = clean(sum(q * beta ** k for k, q in enumerate(coefficients)))
        first_moment = clean(sum(k * q for k, q in enumerate(coefficients)))
        amplification = clean(n * tau * first_moment / (1 - phi))
        assert_nonnegative(amplification - 1,
                           f"filter {filter_index}: inherited defect amplification")
        # Termwise Bernoulli is the exact finite certificate used above.
        for k, q in enumerate(coefficients):
            if q:
                assert_nonnegative(
                    k * (1 - beta) - (1 - beta ** k),
                    f"filter {filter_index}: Bernoulli term {k}",
                )


def iv_point(text: str):
    return iv.mpf([text, text])


def assert_iv_nonnegative(value, label: str) -> None:
    if not bool(value.a >= 0):
        raise AssertionError(f"{label}: interval lower endpoint is negative: {value}")


def audit_polygon_interval(number_text: str) -> None:
    number = iv_point(number_text)
    h = iv.pi / number
    scalar = 4 * iv.sin(h) ** 2
    assert_iv_nonnegative(4 * h ** 2 - scalar,
                          f"interval polygon N={number_text}: D2<=4h^2")
    scaled_rate = h ** 2 / (2 * iv.sin(h) ** 2)
    assert_iv_nonnegative(
        iv.pi ** 2 / 8 - scaled_rate,
        f"interval polygon N={number_text}: rate bound",
    )
    product = scalar / (2 * iv.sin(h) ** 2)
    if not (bool(product.a <= 2) and bool(2 <= product.b)):
        raise AssertionError(
            f"interval polygon N={number_text}: sharp product not enclosed: {product}"
        )


def audit_alternating_interval(scale_text: str, rho_text: str) -> None:
    scale, rho = iv_point(scale_text), iv_point(rho_text)
    alpha, beta = scale * (1 + rho), scale * (1 - rho)
    a_term = 4 * (
        1 - iv.cos(rho * scale) * iv.cos(alpha / 2) * iv.cos(beta / 2)
    )
    b_term = -4 * iv.cos(alpha / 2) * iv.cos(beta / 2) * iv.sin(rho * scale)
    scaled_defect = iv.sqrt(a_term ** 2 + b_term ** 2) / scale
    assert_iv_nonnegative(
        scaled_defect - 3 * rho,
        f"interval alternating s={scale_text},rho={rho_text}: lower first-order floor",
    )
    assert_iv_nonnegative(
        5 * rho - scaled_defect,
        f"interval alternating s={scale_text},rho={rho_text}: upper enclosure",
    )


def main() -> None:
    counts: dict[str, int] = {}

    audit_shared_corrections()
    audit_sampling_kernel_fixture()
    counts["shared-correction"] = 3

    audit_crystal_connector(sp.Rational(0))
    audit_crystal_connector(sp.Rational(2, 7))
    audit_tensor_crystal_connector()
    counts["crystal-compiler"] = 3

    audit_polygon_symbolic()
    polygon_levels = [5, 6, 8, 10, 12]
    for number in polygon_levels:
        audit_polygon_level(number)
    counts["polygon"] = 1 + len(polygon_levels)

    audit_cycle_ratio_blocker()
    audit_delaunay_star_blocker()
    audit_cubed_sphere_seam_blocker()
    audit_alternating_gap_blocker()
    audit_positive_filter_blocker()
    audit_parabolic_nonperiodicity_blocker()
    counts["blocker"] = 6

    iv.dps = 160
    polygon_intervals = ["5", "100", "1e6", "1e20"]
    for number in polygon_intervals:
        audit_polygon_interval(number)
    alternating_intervals = [
        ("1e-4", "0.1"), ("1e-12", "0.5"), ("1e-40", "0.99")
    ]
    for parameters in alternating_intervals:
        audit_alternating_interval(*parameters)
    counts["interval"] = len(polygon_intervals) + len(alternating_intervals)

    total = sum(counts.values())
    if total != 25:
        raise AssertionError(f"P1E fixture inventory changed: {counts}")
    print(f"fixtures={total}")
    for label, count in counts.items():
        print(f"{label}-fixtures={count}")
    print("exact weighted minimum-energy shared correction: PASS")
    print("exact H0/H1, reversibility, moment rows, rate and quotient checks: PASS")
    print("noninjective antipodal sampling quotient: PASS")
    print("positive crystal connector first/cubic moments and optical gap: PASS")
    print("closed-form all-level polygon identities: PASS")
    print("21/4, Delaunay-star, cubed-seam, alternating-gap, filter and raw-K_N blockers: PASS")
    print("outward-rounded extreme-scale interval tests: PASS")
    print("P1E asymptotic-family deterministic audit: PASS")


if __name__ == "__main__":
    main()
