#!/usr/bin/env python3
"""Exact P1A sampling-quotient and two-defect regression audit.

All asserted identities are evaluated in SymPy exact algebra.  Floating
values are used only to propose candidates when selecting a golden-ratio
adjacency or a maximum from a finite algebraic list.  Every such ordering is
then certified by exact symbolic nonnegative differences.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import sympy as sp


def clean(x):
    return sp.simplify(sp.radsimp(sp.cancel(x)))


def assert_zero(x, label: str) -> None:
    value = clean(x)
    if value != 0:
        raise AssertionError(f"{label}: expected zero, got {value}")


def assert_matrix_zero(matrix: sp.Matrix, label: str) -> None:
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            assert_zero(matrix[row, col], f"{label}[{row},{col}]")


def exact_max(values, label: str, *, require_nonnegative: bool = False):
    """Select numerically, then certify the finite algebraic maximum exactly."""
    candidates = [clean(value) for value in values]
    if not candidates:
        raise AssertionError(f"{label}: empty maximum")
    for value in candidates:
        if value.is_real is not True:
            raise AssertionError(f"{label}: value is not certified real: {value}")
        if require_nonnegative and value.is_nonnegative is not True:
            raise AssertionError(
                f"{label}: value is not certified nonnegative: {value}"
            )
    candidate = max(candidates, key=lambda value: float(sp.N(value, 80)))
    for value in candidates:
        gap = clean(candidate - value)
        if gap != 0 and gap.is_nonnegative is not True:
            raise AssertionError(
                f"{label}: maximum ordering not certified: {candidate} - {value} = {gap}"
            )
    return candidate


def assert_exact_multiset(actual, expected, label: str) -> None:
    """Compare finite algebraic multisets without a floating ordering."""
    remaining = [clean(value) for value in expected]
    for observed in (clean(value) for value in actual):
        for index, target in enumerate(remaining):
            if clean(observed - target) == 0:
                remaining.pop(index)
                break
        else:
            raise AssertionError(f"{label}: unexpected value {observed}")
    if remaining:
        raise AssertionError(f"{label}: missing values {remaining}")


def frobenius(a: sp.Matrix, b: sp.Matrix):
    return clean(sp.trace(a.T * b))


def sym0_orthonormal_basis(d: int) -> list[sp.Matrix]:
    """A Frobenius-orthonormal basis of real symmetric trace-free matrices."""
    basis: list[sp.Matrix] = []
    for k in range(1, d):
        entry = [sp.S.Zero] * d
        scale = sp.sqrt(sp.Integer(k) * (k + 1))
        for p in range(k):
            entry[p] = 1 / scale
        entry[k] = -sp.Integer(k) / scale
        basis.append(sp.diag(*entry))
    for p in range(d):
        for q in range(p + 1, d):
            matrix = sp.zeros(d)
            matrix[p, q] = matrix[q, p] = 1 / sp.sqrt(2)
            basis.append(matrix)
    expected = d * (d + 1) // 2 - 1
    assert len(basis) == expected
    for p, left in enumerate(basis):
        for q, right in enumerate(basis):
            assert_zero(
                frobenius(left, right) - (1 if p == q else 0),
                "orthonormal coefficient basis",
            )
    return basis


def regular_simplex(d: int) -> list[sp.Matrix]:
    """The d+1 regular-simplex vertices in exact R^d coordinates."""
    columns = []
    for k in range(1, d + 1):
        col = [sp.S.Zero] * (d + 1)
        scale = sp.sqrt(sp.Integer(k) * (k + 1))
        for p in range(k):
            col[p] = 1 / scale
        col[k] = -sp.Integer(k) / scale
        columns.append(sp.Matrix(col))
    u = sp.Matrix.hstack(*columns)
    center = sp.ones(d + 1, 1) / sp.Integer(d + 1)
    scale = sp.sqrt(sp.Rational(d + 1, d))
    return [sp.simplify(scale * u.T * (sp.eye(d + 1)[:, i] - center))
            for i in range(d + 1)]


def cross_polytope(d: int) -> list[sp.Matrix]:
    vertices = []
    for p in range(d):
        e = sp.eye(d)[:, p]
        vertices.extend([e, -e])
    return vertices


def hypercube(d: int) -> list[sp.Matrix]:
    scale = sp.sqrt(d)
    return [sp.Matrix(signs) / scale for signs in product((-1, 1), repeat=d)]


def golden_vertices(kind: str) -> list[sp.Matrix]:
    phi = (1 + sp.sqrt(5)) / 2
    out: list[sp.Matrix] = []
    if kind == "icosahedron":
        for a, b in product((-1, 1), repeat=2):
            out.extend([
                sp.Matrix([0, a, b * phi]),
                sp.Matrix([a, b * phi, 0]),
                sp.Matrix([b * phi, 0, a]),
            ])
    elif kind == "dodecahedron":
        out.extend(sp.Matrix(v) for v in product((-1, 1), repeat=3))
        inv = 1 / phi
        for a, b in product((-1, 1), repeat=2):
            out.extend([
                sp.Matrix([0, a * inv, b * phi]),
                sp.Matrix([a * inv, b * phi, 0]),
                sp.Matrix([b * phi, 0, a * inv]),
            ])
    else:
        raise ValueError(kind)
    # Remove no points: the coordinate recipes produce distinct vertices.
    norm = sp.sqrt(frobenius(out[0], out[0]))
    normalized = [sp.simplify(v / norm) for v in out]
    assert len({tuple(map(str, v)) for v in normalized}) == len(normalized)
    return normalized


def shortest_edge_rates(vertices: list[sp.Matrix], eigenvalue: int) -> sp.Matrix:
    n = len(vertices)
    dots = {
        (i, j): clean((vertices[i].T * vertices[j])[0])
        for i in range(n) for j in range(i + 1, n)
    }
    maximum = max(dots.values(), key=lambda x: float(sp.N(x, 30)))
    adjacency = [[False] * n for _ in range(n)]
    for (i, j), dot in dots.items():
        if clean(dot - maximum) == 0:
            adjacency[i][j] = adjacency[j][i] = True
    # The floating comparison above is only a selector.  Certify its answer
    # in the exact algebraic number field before using the adjacency.
    for (i, j), dot in dots.items():
        gap = clean(maximum - dot)
        if adjacency[i][j]:
            assert_zero(gap, "selected golden-shell edge dot")
        elif gap.is_positive is not True:
            raise AssertionError(
                f"golden-shell nonedge lacks exact strict certificate: {i},{j}: {gap}"
            )
    degrees = [sum(row) for row in adjacency]
    if len(set(degrees)) != 1:
        raise AssertionError(f"shortest-edge graph is not regular: {degrees}")
    loss = clean(1 - maximum)
    rate = clean(sp.Integer(eigenvalue) / (degrees[0] * loss))
    return sp.Matrix(n, n, lambda i, j: rate if adjacency[i][j] else 0)


@dataclass
class Fixture:
    name: str
    vertices: list[sp.Matrix]
    weights: list[sp.Expr]
    rates: sp.Matrix
    expected_scalar: sp.Expr | None = None
    expected_rank: int | None = None


def uniform_fixture(
    name: str,
    vertices: list[sp.Matrix],
    rates: sp.Matrix,
    expected_scalar=None,
    expected_rank=None,
) -> Fixture:
    n = len(vertices)
    return Fixture(
        name,
        vertices,
        [sp.Rational(1, n)] * n,
        rates,
        expected_scalar,
        expected_rank,
    )


def complete_rates(n: int, rate) -> sp.Matrix:
    return sp.Matrix(n, n, lambda i, j: rate if i != j else 0)


def family_fixtures() -> list[Fixture]:
    fixtures: list[Fixture] = []
    for d in (2, 3, 4):
        simplex = regular_simplex(d)
        fixtures.append(uniform_fixture(
            f"simplex-d{d}", simplex,
            complete_rates(d + 1, sp.Rational(d - 1, d + 1)),
            sp.Integer(d + 1), d,
        ))

        cross = cross_polytope(d)
        n = len(cross)
        rates = sp.Matrix(n, n, lambda i, j:
            sp.Rational(1, 2)
            if i != j and clean((cross[i].T * cross[j])[0]) == 0 else 0)
        fixtures.append(uniform_fixture(
            f"cross-polytope-d{d}", cross, rates, sp.Integer(d), d - 1,
        ))

        cube = hypercube(d)
        n = len(cube)
        rates = sp.zeros(n)
        signs = [tuple(int(clean(v[p] * sp.sqrt(d))) for p in range(d)) for v in cube]
        for i in range(n):
            for j in range(n):
                if sum(a != b for a, b in zip(signs[i], signs[j])) == 1:
                    rates[i, j] = sp.Rational(d - 1, 2)
        fixtures.append(uniform_fixture(
            f"hypercube-d{d}", cube, rates, sp.Integer(2), d * (d - 1) // 2,
        ))
    return fixtures


def platonic_fixtures() -> list[Fixture]:
    tetra = regular_simplex(3)
    octa = cross_polytope(3)
    cube = hypercube(3)
    result = [
        uniform_fixture("platonic-tetrahedron", tetra,
                        complete_rates(4, sp.Rational(1, 2)), 4, 3),
    ]
    octa_rates = sp.Matrix(6, 6, lambda i, j:
        sp.Rational(1, 2)
        if i != j and clean((octa[i].T * octa[j])[0]) == 0 else 0)
    result.append(uniform_fixture("platonic-octahedron", octa, octa_rates, 3, 2))
    cube_rates = sp.zeros(8)
    cube_signs = [tuple(int(clean(v[p] * sp.sqrt(3))) for p in range(3)) for v in cube]
    for i in range(8):
        for j in range(8):
            if sum(a != b for a, b in zip(cube_signs[i], cube_signs[j])) == 1:
                cube_rates[i, j] = 1
    result.append(uniform_fixture("platonic-cube", cube, cube_rates, 2, 3))
    ico = golden_vertices("icosahedron")
    result.append(uniform_fixture(
        "platonic-icosahedron", ico, shortest_edge_rates(ico, 2),
        3 - 3 * sp.sqrt(5) / 5, 5,
    ))
    dod = golden_vertices("dodecahedron")
    result.append(uniform_fixture(
        "platonic-dodecahedron", dod, shortest_edge_rates(dod, 2),
        3 - sp.sqrt(5), 5,
    ))
    return result


def adversarial_fixtures() -> list[Fixture]:
    e1, e2 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
    antipodal = uniform_fixture(
        "aliased-antipodal-pair", [e1, -e1],
        sp.Matrix([[0, sp.Rational(1, 2)], [sp.Rational(1, 2), 0]]),
        4, 1,
    )
    vertices = [e1, e1, -e1, e2, -e2]
    weights = [sp.Rational(1, 12), sp.Rational(1, 12), sp.Rational(1, 6),
               sp.Rational(1, 3), sp.Rational(1, 3)]
    rates = sp.Matrix(5, 5, lambda i, j: weights[j] if i != j else 0)
    repeated = Fixture("weighted-repeated-alias", vertices, weights, rates,
                       None, 1)
    # The accepted exact spherical hexagonal prism: its sampling is
    # injective but its genuinely sampled exact space has dimension two.
    cosines = [1, sp.Rational(1, 2), -sp.Rational(1, 2), -1,
               -sp.Rational(1, 2), sp.Rational(1, 2)]
    sines = [0, sp.sqrt(3) / 2, sp.sqrt(3) / 2, 0,
             -sp.sqrt(3) / 2, -sp.sqrt(3) / 2]
    prism_vertices = [
        sp.Matrix([2 * cosines[k], 2 * sines[k], sigma]) / sp.sqrt(5)
        for sigma in (-1, 1) for k in range(6)
    ]
    prism_rates = sp.zeros(12)
    for layer in range(2):
        for k in range(6):
            i = 6 * layer + k
            prism_rates[i, 6 * layer + (k - 1) % 6] = 2
            prism_rates[i, 6 * layer + (k + 1) % 6] = 2
            prism_rates[i, 6 * (1 - layer) + k] = 1
    prism = uniform_fixture("exact-spherical-hexagonal-prism", prism_vertices,
                            prism_rates, None, 5)

    # A positive full cube row where the loss variance and B_i are both
    # strictly nonzero.  Each nonempty coordinate-flip subset has its own
    # positive rate.
    cube = hypercube(3)
    cube_signs = [tuple(int(clean(v[p] * sp.sqrt(3))) for p in range(3))
                  for v in cube]
    flip_rates = {
        (0,): sp.Rational(3, 4),
        (1,): sp.Rational(19, 24),
        (2,): sp.Rational(5, 6),
        (0, 1): sp.Rational(1, 8),
        (0, 2): sp.Rational(1, 12),
        (1, 2): sp.Rational(1, 24),
        (0, 1, 2): sp.Rational(1, 24),
    }
    cube_full_rates = sp.zeros(8)
    for i, left in enumerate(cube_signs):
        for j, right in enumerate(cube_signs):
            changed = tuple(k for k in range(3) if left[k] != right[k])
            if changed:
                cube_full_rates[i, j] = flip_rates[changed]
    anisotropic = uniform_fixture(
        "positive-cube-both-defects", cube, cube_full_rates, None, 3
    )
    # A lower-dimensional equatorial cycle: both K_X and E_sample are
    # nonzero, so all three dimension terms are exercised simultaneously.
    equator_vertices = [
        sp.Matrix([cosines[k], sines[k], 0]) for k in range(6)
    ]
    equator_rates = sp.zeros(6)
    for k in range(6):
        equator_rates[k, (k - 1) % 6] = 2
        equator_rates[k, (k + 1) % 6] = 2
    equator = uniform_fixture(
        "degenerate-equatorial-hexagon", equator_vertices, equator_rates,
        None, 3,
    )
    return [antipodal, repeated, prism, anisotropic, equator]


def audit_fixture(fixture: Fixture) -> dict[str, object]:
    vertices, weights, rates = fixture.vertices, fixture.weights, fixture.rates
    n, d = len(vertices), vertices[0].rows
    basis = sym0_orthonormal_basis(d)
    m = len(basis)
    identity = sp.eye(d)
    weight_matrix = sp.diag(*weights)

    assert_zero(sum(weights) - 1, f"{fixture.name}: weight normalization")
    for i, weight in enumerate(weights):
        if clean(weight).is_positive is not True:
            raise AssertionError(
                f"{fixture.name}: nonpositive or uncertified weight {i}: {weight}"
            )
    for i, omega in enumerate(vertices):
        assert_zero((omega.T * omega)[0] - 1, f"{fixture.name}: unit vertex {i}")
    for i in range(n):
        for j in range(n):
            rate = clean(rates[i, j])
            gamma = clean(weights[i] * rate)
            if i == j:
                assert_zero(rate, f"{fixture.name}: diagonal rate {i}")
            if i != j and rate.is_nonnegative is not True:
                raise AssertionError(
                    f"{fixture.name}: negative or uncertified rate {i},{j}: {rate}"
                )
            if gamma.is_nonnegative is not True:
                raise AssertionError(
                    f"{fixture.name}: negative or uncertified conductance {i},{j}: {gamma}"
                )
            assert_zero(
                gamma - weights[j] * rates[j, i],
                f"{fixture.name}: detailed balance {i},{j}",
            )

    generator = sp.Matrix(n, n, lambda i, j:
        rates[i, j] if i != j else -sum(rates[i, k] for k in range(n) if k != i))
    omega_matrix = sp.Matrix.hstack(*vertices).T
    assert_matrix_zero(
        generator * omega_matrix + (d - 1) * omega_matrix,
        f"{fixture.name}: negative generator eigenmap",
    )
    # The opposite sign must not satisfy the declared eigenmap.
    if generator * omega_matrix - (d - 1) * omega_matrix == sp.zeros(n, d):
        raise AssertionError(f"{fixture.name}: generator sign mutation escaped")

    sampling = sp.Matrix(n, m, lambda i, p:
        clean((vertices[i].T * basis[p] * vertices[i])[0]))
    target = generator + 2 * d * sp.eye(n)
    residual = target * sampling
    covariances: list[sp.Matrix] = []
    z_rows: list[sp.Matrix] = []
    m_rows: list[sp.Matrix] = []
    b_rows: list[sp.Matrix] = []
    epsilons: list[sp.Expr] = []
    variances: list[sp.Expr] = []

    for i, omega in enumerate(vertices):
        rate_sum = clean(sum(rates[i, j] for j in range(n) if j != i))
        if not bool(rate_sum > 0):
            raise AssertionError(f"{fixture.name}: nonpositive row rate {i}: {rate_sum}")
        losses = [clean(1 - (omega.T * vertices[j])[0]) for j in range(n)]
        first = clean(sum(rates[i, j] * losses[j] for j in range(n) if j != i))
        assert_zero(first - (d - 1), f"{fixture.name}: first loss moment {i}")
        covariance = sp.zeros(d)
        for j in range(n):
            if i == j:
                continue
            delta = vertices[j] - omega
            covariance += rates[i, j] * delta * delta.T
        covariance = covariance.applyfunc(clean)
        epsilon = clean(sum(rates[i, j] * losses[j] ** 2
                            for j in range(n) if j != i))
        z = (omega * omega.T - identity / sp.Integer(d)).applyfunc(clean)
        unprojected = covariance + 2 * omega * omega.T
        matrix_m = (unprojected - sp.trace(unprojected) * identity / d).applyfunc(clean)
        matrix_b = (matrix_m - sp.Rational(d, d - 1) * epsilon * z).applyfunc(clean)
        covariances.append(covariance)
        z_rows.append(z)
        m_rows.append(matrix_m)
        b_rows.append(matrix_b)
        epsilons.append(epsilon)

        assert_zero(sp.trace(covariance) - 2 * (d - 1),
                    f"{fixture.name}: covariance trace {i}")
        assert_zero((omega.T * covariance * omega)[0] - epsilon,
                    f"{fixture.name}: radial covariance {i}")
        assert_zero(frobenius(matrix_m, z) - epsilon,
                    f"{fixture.name}: M-Z pairing {i}")
        assert_zero(frobenius(z, z) - sp.Rational(d - 1, d),
                    f"{fixture.name}: Z norm {i}")
        assert_zero(frobenius(matrix_b, z), f"{fixture.name}: B-Z orthogonality {i}")
        assert_zero(
            frobenius(matrix_m, matrix_m)
            - sp.Rational(d, d - 1) * epsilon ** 2
            - frobenius(matrix_b, matrix_b),
            f"{fixture.name}: Pythagorean identity {i}",
        )
        variance = clean(sum(
            rates[i, j] * (losses[j] - sp.Rational(d - 1, 1) / rate_sum) ** 2
            for j in range(n) if j != i
        ))
        variances.append(variance)
        assert_zero(
            epsilon - sp.Rational((d - 1) ** 2, 1) / rate_sum - variance,
            f"{fixture.name}: loss variance identity {i}",
        )
        for p, coefficient in enumerate(basis):
            assert_zero(
                residual[i, p] - frobenius(coefficient, matrix_m),
                f"{fixture.name}: residual row pairing {i},{p}",
            )
            assert_zero(
                sampling[i, p] - frobenius(coefficient, z),
                f"{fixture.name}: sampling row pairing {i},{p}",
            )

    # Kernel factorization is tested on an exact nullspace basis.
    for column, alias in enumerate(sampling.nullspace()):
        assert_matrix_zero(residual * alias, f"{fixture.name}: quotient alias {column}")

    z_coordinates = sp.Matrix(n, m, lambda i, p: frobenius(basis[p], z_rows[i]))
    m_coordinates = sp.Matrix(n, m, lambda i, p: frobenius(basis[p], m_rows[i]))
    assert_matrix_zero(sampling - z_coordinates, f"{fixture.name}: S row representers")
    assert_matrix_zero(residual - m_coordinates, f"{fixture.name}: R row representers")
    gram_s = (sampling.T * weight_matrix * sampling).applyfunc(clean)
    gram_r = (residual.T * weight_matrix * residual).applyfunc(clean)
    assert_matrix_zero(
        gram_s - z_coordinates.T * weight_matrix * z_coordinates,
        f"{fixture.name}: weighted sampling Gram",
    )
    assert_matrix_zero(
        gram_r - m_coordinates.T * weight_matrix * m_coordinates,
        f"{fixture.name}: weighted residual Gram",
    )
    b_coordinates = sp.Matrix(n, m, lambda i, p:
        frobenius(basis[p], b_rows[i]))
    radial_gram = sp.zeros(m)
    mixed_gram = sp.zeros(m)
    anisotropy_gram = sp.zeros(m)
    for i in range(n):
        z_col = z_coordinates[i, :].T
        b_col = b_coordinates[i, :].T
        coefficient = clean(sp.Rational(d, d - 1) * epsilons[i])
        radial_gram += weights[i] * coefficient ** 2 * z_col * z_col.T
        mixed_gram += weights[i] * coefficient * (
            z_col * b_col.T + b_col * z_col.T
        )
        anisotropy_gram += weights[i] * b_col * b_col.T
    radial_gram = radial_gram.applyfunc(clean)
    mixed_gram = mixed_gram.applyfunc(clean)
    anisotropy_gram = anisotropy_gram.applyfunc(clean)
    assert_matrix_zero(
        gram_r - radial_gram - mixed_gram - anisotropy_gram,
        f"{fixture.name}: expanded two-defect Gram",
    )
    assert_matrix_zero(
        gram_r - sampling.T * weight_matrix * target ** 2 * sampling,
        f"{fixture.name}: self-adjoint T squared Gram",
    )
    assert_matrix_zero(
        weight_matrix * generator - generator.T * weight_matrix,
        f"{fixture.name}: weighted self-adjointness",
    )
    assert_zero(sp.trace(gram_s) - sp.Rational(d - 1, d),
                f"{fixture.name}: sampling Gram trace")
    global_two_defect = clean(sum(
        weights[i] * (
            sp.Rational(d, d - 1) * epsilons[i] ** 2
            + frobenius(b_rows[i], b_rows[i])
        ) for i in range(n)
    ))
    assert_zero(sp.trace(gram_r) - global_two_defect,
                f"{fixture.name}: residual Gram two-defect trace")
    for i in range(n):
        row_formula = (2 * d - sum(rates[i, j] for j in range(n) if j != i)) * z_rows[i]
        row_formula += sum(
            (rates[i, j] * z_rows[j] for j in range(n) if j != i),
            sp.zeros(d),
        )
        assert_matrix_zero(m_rows[i] - row_formula,
                           f"{fixture.name}: operator row tensor {i}")

    rank_s, rank_r = sampling.rank(), residual.rank()
    if fixture.expected_rank is not None and rank_s != fixture.expected_rank:
        raise AssertionError(
            f"{fixture.name}: rank S expected {fixture.expected_rank}, observed {rank_s}"
        )
    if rank_r > rank_s:
        raise AssertionError(f"{fixture.name}: residual rank exceeds sampling rank")
    form_basis = residual.nullspace()
    sampled_exact_rank = (sampling * sp.Matrix.hstack(*form_basis)).rank() if form_basis else 0
    if sampled_exact_rank != rank_s - rank_r:
        raise AssertionError(
            f"{fixture.name}: sampled exact rank {sampled_exact_rank} != {rank_s-rank_r}"
        )
    if len(form_basis) != m - rank_r or len(sampling.nullspace()) != m - rank_s:
        raise AssertionError(f"{fixture.name}: rank-nullity mutation")

    # Deflate the singular pencil to range(G_S)=K_X^perp.
    complement = gram_s.columnspace()
    if not complement:
        raise AssertionError(f"{fixture.name}: impossible zero degree-two sample")
    lift = sp.Matrix.hstack(*complement)
    reduced_s = (lift.T * gram_s * lift).applyfunc(clean)
    reduced_r = (lift.T * gram_r * lift).applyfunc(clean)
    if clean(reduced_s.det()) == 0:
        raise AssertionError(f"{fixture.name}: singular deflated sampling Gram")
    generalized = (reduced_s.inv() * reduced_r).applyfunc(clean)
    eigenvalues = []
    for value, multiplicity in generalized.eigenvals().items():
        eigenvalues.extend([clean(value)] * multiplicity)
    if len(eigenvalues) != rank_s:
        raise AssertionError(f"{fixture.name}: generalized eigenvalue count")
    max_eigenvalue = exact_max(
        eigenvalues, f"{fixture.name}: generalized maximum",
        require_nonnegative=True,
    )
    defect = clean(sp.sqrt(max_eigenvalue))
    frobenius_eigenvalues = []
    for value, multiplicity in gram_r.eigenvals().items():
        frobenius_eigenvalues.extend([clean(value)] * multiplicity)
    wrong_frobenius_defect_sq = exact_max(
        frobenius_eigenvalues, f"{fixture.name}: Frobenius maximum",
        require_nonnegative=True,
    )
    mixed_max_abs = exact_max(
        (clean(abs(entry)) for entry in mixed_gram),
        f"{fixture.name}: mixed Gram absolute maximum",
        require_nonnegative=True,
    )

    if fixture.expected_scalar is not None:
        scalar = clean(fixture.expected_scalar)
        assert_matrix_zero(residual - scalar * sampling,
                           f"{fixture.name}: expected scalar residual")
        assert_zero(defect - abs(scalar), f"{fixture.name}: defect")
        for i in range(n):
            assert_matrix_zero(m_rows[i] - scalar * z_rows[i],
                               f"{fixture.name}: M scalar Z {i}")
            assert_matrix_zero(b_rows[i], f"{fixture.name}: zero anisotropy {i}")

    return {
        "name": fixture.name,
        "d": d,
        "nodes": n,
        "rank_s": rank_s,
        "rank_r": rank_r,
        "dim_kernel": m - rank_s,
        "dim_form": m - rank_r,
        "dim_sampled_exact": sampled_exact_rank,
        "defect": defect,
        "epsilon_0": epsilons[0],
        "variance_0": variances[0],
        "b_norm_0": frobenius(b_rows[0], b_rows[0]),
        "generalized_eigenvalues": tuple(eigenvalues),
        "wrong_frobenius_defect_sq": clean(wrong_frobenius_defect_sq),
        "mixed_gram_max_abs": clean(mixed_max_abs),
        "joint_sampling_residual_rank": sampling.row_join(residual).rank(),
    }


def mutation_tests(fixtures: list[Fixture]) -> None:
    tetra = next(f for f in fixtures if f.name == "platonic-tetrahedron")
    d = 3
    basis = sym0_orthonormal_basis(d)
    sampling = sp.Matrix(len(tetra.vertices), len(basis), lambda i, p:
        clean((tetra.vertices[i].T * basis[p] * tetra.vertices[i])[0]))
    generator = sp.Matrix(4, 4, lambda i, j:
        tetra.rates[i, j] if i != j
        else -sum(tetra.rates[i, k] for k in range(4) if k != i))
    correct = (generator + 2 * d * sp.eye(4)) * sampling
    wrong_sign = (generator - 2 * d * sp.eye(4)) * sampling
    if correct == wrong_sign:
        raise AssertionError("target-sign mutation was not detected")
    wrong_generator_convention = (-generator + 2 * d * sp.eye(4)) * sampling
    assert_matrix_zero(wrong_generator_convention - 8 * sampling,
                       "positive-Laplacian sign mutation fixture")
    if correct == wrong_generator_convention:
        raise AssertionError("positive-Laplacian generator mutation was not detected")

    weighted = next(f for f in fixtures if f.name == "weighted-repeated-alias")
    basis2 = sym0_orthonormal_basis(2)
    sample2 = sp.Matrix(5, 2, lambda i, p:
        clean((weighted.vertices[i].T * basis2[p] * weighted.vertices[i])[0]))
    test_function = sp.Matrix([1, 2, 3, 4, 5])
    weighted_adjoint = sample2.T * sp.diag(*weighted.weights) * test_function
    wrong_adjoint = sample2.T * test_function
    if weighted_adjoint == wrong_adjoint:
        raise AssertionError("unweighted-adjoint mutation was not detected")
    weighted_generator = sp.Matrix(5, 5, lambda i, j:
        weighted.rates[i, j] if i != j
        else -sum(weighted.rates[i, k] for k in range(5) if k != i))
    weighted_target = weighted_generator + 4 * sp.eye(5)
    weighted_residual = weighted_target * sample2
    weight_matrix = sp.diag(*weighted.weights)
    gs = (sample2.T * weight_matrix * sample2).applyfunc(clean)
    gr = (weighted_residual.T * weight_matrix * weighted_residual).applyfunc(clean)
    cross = (sample2.T * weight_matrix * weighted_residual).applyfunc(clean)
    assert_zero(gs[0, 0] - sp.Rational(1, 2), "weighted alias G_S")
    assert_zero(gr[0, 0] - sp.Rational(44, 9), "weighted alias G_R")
    assert_zero(cross[0, 0] - sp.Rational(14, 9), "weighted alias S*R")
    assert_zero(gr[0, 0] / gs[0, 0] - sp.Rational(88, 9),
                "weighted alias quotient defect squared")
    compressed_square = clean((cross[0, 0] / gs[0, 0]) ** 2)
    if clean(compressed_square - sp.Rational(88, 9)) == 0:
        raise AssertionError("non-invariant compression-square mutation escaped")
    wrong_gs = sample2.T * sample2
    wrong_gr = weighted_residual.T * weighted_residual
    wrong_quotient = clean(wrong_gr[0, 0] / wrong_gs[0, 0])
    assert_zero(wrong_quotient - sp.Rational(392, 45),
                "unweighted quotient mutation value")

    antipodal = next(f for f in fixtures if f.name == "aliased-antipodal-pair")
    result = audit_fixture(antipodal)
    if result["dim_form"] == result["dim_sampled_exact"]:
        raise AssertionError("form/sample-space conflation mutation was not detected")
    spectral_parameter = sp.symbols("lambda")
    antipodal_basis = sym0_orthonormal_basis(2)
    antipodal_s = sp.Matrix(2, 2, lambda i, p:
        clean((antipodal.vertices[i].T * antipodal_basis[p] * antipodal.vertices[i])[0]))
    antipodal_l = sp.Matrix([[-sp.Rational(1, 2), sp.Rational(1, 2)],
                             [sp.Rational(1, 2), -sp.Rational(1, 2)]])
    antipodal_r = (antipodal_l + 4 * sp.eye(2)) * antipodal_s
    antipodal_w = sp.eye(2) / 2
    singular_gs = antipodal_s.T * antipodal_w * antipodal_s
    singular_gr = antipodal_r.T * antipodal_w * antipodal_r
    assert_zero((singular_gr - spectral_parameter * singular_gs).det(),
                "raw singular pencil determinant")
    prism = audit_fixture(next(
        f for f in fixtures if f.name == "exact-spherical-hexagonal-prism"
    ))
    if (prism["rank_s"], prism["rank_r"], prism["dim_kernel"],
            prism["dim_form"], prism["dim_sampled_exact"]) != (5, 3, 0, 2, 2):
        raise AssertionError(f"prism three-space regression failed: {prism}")
    assert_exact_multiset(
        prism["generalized_eigenvalues"], (0, 0, 4, 4, 36),
        "prism quotient spectrum",
    )
    assert_zero(prism["defect"] - 6, "prism sampled defect")
    assert_zero(prism["wrong_frobenius_defect_sq"] - sp.Rational(24, 25),
                "prism wrong Frobenius denominator mutation")
    assert_zero(prism["mixed_gram_max_abs"] - sp.Rational(288, 625),
                "prism mixed Gram operator")
    weighted_result = audit_fixture(weighted)
    if weighted_result["joint_sampling_residual_rank"] != 2:
        raise AssertionError(
            f"weighted sampled range unexpectedly invariant: {weighted_result}"
        )
    both = audit_fixture(next(
        f for f in fixtures if f.name == "positive-cube-both-defects"
    ))
    assert_zero(both["epsilon_0"] - sp.Rational(5, 3),
                "both-defects epsilon")
    assert_zero(both["variance_0"] - sp.Rational(1, 6),
                "both-defects loss variance")
    assert_zero(both["b_norm_0"] - sp.Rational(1, 81),
                "both-defects anisotropy norm")
    assert_zero(both["defect"] - sp.Rational(8, 3),
                "both-defects quotient defect")
    equator = audit_fixture(next(
        f for f in fixtures if f.name == "degenerate-equatorial-hexagon"
    ))
    if (equator["rank_s"], equator["rank_r"], equator["dim_kernel"],
            equator["dim_form"], equator["dim_sampled_exact"]) != (3, 1, 2, 4, 2):
        raise AssertionError(f"equatorial three-space regression failed: {equator}")

    # Nonorthogonal raw coefficient basis: S^TWS is the bilinear Gram,
    # whereas the operator coordinate matrix contains the inverse basis Gram.
    raw_basis = [
        sp.diag(1, -1, 0),
        sp.diag(-1, -1, 2),
    ]
    for p, q in ((0, 1), (0, 2), (1, 2)):
        matrix = sp.zeros(3)
        matrix[p, q] = matrix[q, p] = sp.Rational(1, 2)
        raw_basis.append(matrix)
    basis_gram = sp.Matrix(5, 5, lambda i, j:
        frobenius(raw_basis[i], raw_basis[j]))
    assert_matrix_zero(
        basis_gram - sp.diag(2, 6, sp.Rational(1, 2),
                             sp.Rational(1, 2), sp.Rational(1, 2)),
        "raw coefficient basis Gram",
    )
    cube_fixture = next(f for f in fixtures if f.name == "positive-cube-both-defects")
    raw_s = sp.Matrix(8, 5, lambda i, p:
        clean((cube_fixture.vertices[i].T * raw_basis[p] * cube_fixture.vertices[i])[0]))
    raw_l = sp.Matrix(8, 8, lambda i, j:
        cube_fixture.rates[i, j] if i != j
        else -sum(cube_fixture.rates[i, k] for k in range(8) if k != i))
    raw_r = (raw_l + 6 * sp.eye(8)) * raw_s
    raw_w = sp.eye(8) / 8
    raw_gs = (raw_s.T * raw_w * raw_s).applyfunc(clean)
    raw_gr = (raw_r.T * raw_w * raw_r).applyfunc(clean)
    assert_matrix_zero(
        raw_gs - sp.diag(0, 0, sp.Rational(1, 9),
                         sp.Rational(1, 9), sp.Rational(1, 9)),
        "raw sampling bilinear Gram",
    )
    assert_matrix_zero(
        raw_gr - sp.diag(0, 0, sp.Rational(64, 81),
                         sp.Rational(25, 36), sp.Rational(49, 81)),
        "raw residual bilinear Gram",
    )
    operator_gs = (basis_gram.inv() * raw_gs).applyfunc(clean)
    if operator_gs == raw_gs:
        raise AssertionError("nonorthogonal-basis Gram/operator mutation escaped")
    raw_lift = sp.Matrix.hstack(*raw_gs.columnspace())
    raw_pencil = (
        (raw_lift.T * raw_gs * raw_lift).inv()
        * (raw_lift.T * raw_gr * raw_lift)
    ).applyfunc(clean)
    raw_spectrum = [
        clean(value) for value, multiplicity in raw_pencil.eigenvals().items()
        for _ in range(multiplicity)
    ]
    assert_exact_multiset(
        raw_spectrum,
        (sp.Rational(49, 9), sp.Rational(25, 4), sp.Rational(64, 9)),
        "nonorthogonal generalized spectrum",
    )


def main() -> None:
    fixtures = family_fixtures() + platonic_fixtures() + adversarial_fixtures()
    required_names = {
        *(f"simplex-d{d}" for d in (2, 3, 4)),
        *(f"cross-polytope-d{d}" for d in (2, 3, 4)),
        *(f"hypercube-d{d}" for d in (2, 3, 4)),
        "platonic-tetrahedron", "platonic-octahedron", "platonic-cube",
        "platonic-icosahedron", "platonic-dodecahedron",
        "aliased-antipodal-pair", "weighted-repeated-alias",
        "exact-spherical-hexagonal-prism", "positive-cube-both-defects",
        "degenerate-equatorial-hexagon",
    }
    observed_names = {fixture.name for fixture in fixtures}
    if len(fixtures) != 19 or observed_names != required_names:
        raise AssertionError(
            f"fixture inventory changed: count={len(fixtures)} names={sorted(observed_names)}"
        )
    results = [audit_fixture(fixture) for fixture in fixtures]
    mutation_tests(fixtures)
    for row in results:
        print(
            "{name}: d={d} N={nodes} rank(S/R)={rank_s}/{rank_r} "
            "dim(K/form/sample)={dim_kernel}/{dim_form}/{dim_sampled_exact} "
            "epsilon0={epsilon_0} D2={defect}".format(**row)
        )
    print(f"fixtures={len(results)}")
    print("weighted-adjoint mutation: REJECTED")
    print("generator-sign mutation: REJECTED")
    print("non-invariant-compression mutation: REJECTED")
    print("sampling-quotient conflation mutation: REJECTED")
    print("P1A exact quadratic-fidelity audit: PASS")


if __name__ == "__main__":
    main()
