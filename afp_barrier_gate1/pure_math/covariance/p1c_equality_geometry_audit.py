#!/usr/bin/env python3
"""Exact P1C equality-geometry and sampling-alias audit.

The all-dimensional proofs are given in ``P1C_EQUALITY_GEOMETRY.md``.  This
file is deterministic exact regression evidence: every calculation is over
``QQ`` or ``QQ(sqrt(5))`` through SymPy, and no floating rank threshold is
used.  Finite fixtures are not promoted into all-orders proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import sympy as sp

import p1a_quadratic_fidelity_audit as p1a
import p1b_sharp_quadratic_defect_audit as p1b


def clean(value):
    return p1a.clean(value)


def assert_zero(value, label: str) -> None:
    p1a.assert_zero(value, label)


def assert_matrix_zero(matrix: sp.Matrix, label: str) -> None:
    p1a.assert_matrix_zero(matrix, label)


def frobenius(left: sp.Matrix, right: sp.Matrix):
    return p1a.frobenius(left, right)


def generator_from_rates(rates: sp.Matrix) -> sp.Matrix:
    return p1b.generator_from_rates(rates)


def family_fixture(kind: str, d: int) -> p1a.Fixture:
    if d < 2:
        raise ValueError("the positive spherical families require d>=2")
    if kind == "simplex":
        vertices = p1a.regular_simplex(d)
        return p1a.uniform_fixture(
            f"simplex-d{d}", vertices,
            p1a.complete_rates(d + 1, sp.Rational(d - 1, d + 1)),
            sp.Integer(d + 1), d,
        )
    if kind == "cross-polytope":
        vertices = p1a.cross_polytope(d)
        rates = sp.Matrix(2 * d, 2 * d, lambda i, j:
            sp.Rational(1, 2)
            if i != j and clean((vertices[i].T * vertices[j])[0]) == 0 else 0)
        return p1a.uniform_fixture(
            f"cross-polytope-d{d}", vertices, rates,
            sp.Integer(d), d - 1,
        )
    if kind == "hypercube":
        vertices = p1a.hypercube(d)
        signs = [tuple(int(clean(v[p] * sp.sqrt(d))) for p in range(d))
                 for v in vertices]
        rates = sp.Matrix(2 ** d, 2 ** d, lambda i, j:
            sp.Rational(d - 1, 2)
            if sum(left != right for left, right in zip(signs[i], signs[j])) == 1
            else 0)
        return p1a.uniform_fixture(
            f"hypercube-d{d}", vertices, rates,
            sp.Integer(2), d * (d - 1) // 2,
        )
    raise ValueError(kind)


@dataclass(frozen=True)
class EqualityState:
    name: str
    d: int
    nodes: int
    weight: sp.Expr
    active_rate: sp.Expr
    active_conductance: sp.Expr
    row_rate: sp.Expr
    loss: sp.Expr
    epsilon: sp.Expr
    scalar: sp.Expr
    rank_s: int
    dim_kernel: int
    e2: int


def audit_equality_fixture(fixture: p1a.Fixture) -> EqualityState:
    """Audit the full local block theorem and sampled quotient exactly."""

    vertices, weights, rates = fixture.vertices, fixture.weights, fixture.rates
    n, d = len(vertices), vertices[0].rows
    identity = sp.eye(d)
    basis = p1a.sym0_orthonormal_basis(d)
    sampling = sp.Matrix(n, len(basis), lambda i, k:
        clean((vertices[i].T * basis[k] * vertices[i])[0]))
    generator = generator_from_rates(rates)
    residual = ((generator + 2 * d * sp.eye(n)) * sampling).applyfunc(clean)

    active_rates = {
        clean(rates[i, j]) for i in range(n) for j in range(n)
        if i != j and clean(rates[i, j]) != 0
    }
    if len(active_rates) != 1:
        raise AssertionError(f"{fixture.name}: expected one active rate: {active_rates}")
    active_rate = active_rates.pop()
    active_conductances = {
        clean(weights[i] * rates[i, j]) for i in range(n) for j in range(n)
        if i != j and clean(rates[i, j]) != 0
    }
    if len(active_conductances) != 1:
        raise AssertionError(
            f"{fixture.name}: expected one active conductance: {active_conductances}"
        )
    active_conductance = active_conductances.pop()

    common_row_rate = None
    common_loss = None
    common_epsilon = None
    common_scalar = None
    for i, omega in enumerate(vertices):
        projector = (identity - omega * omega.T).applyfunc(clean)
        row_rate = clean(sum(rates[i, j] for j in range(n) if j != i))
        active = [j for j in range(n) if j != i and clean(rates[i, j]) != 0]
        losses = [clean(1 - (omega.T * vertices[j])[0]) for j in active]
        if len(set(losses)) != 1:
            raise AssertionError(f"{fixture.name}: row {i} is not one-shell: {losses}")
        ell = losses[0]
        epsilon = clean(sum(rates[i, j] * ell ** 2 for j in active))

        tangent_mean = sp.zeros(d, 1)
        radial_tangent = sp.zeros(d, 1)
        tangent_second = sp.zeros(d)
        covariance = sp.zeros(d)
        for j in active:
            delta = vertices[j] - omega
            tangent = (projector * vertices[j]).applyfunc(clean)
            assert_matrix_zero(
                delta - (-ell * omega + tangent),
                f"{fixture.name}: radial-tangent increment {i},{j}",
            )
            assert_zero((omega.T * tangent)[0],
                        f"{fixture.name}: tangent orthogonality {i},{j}")
            assert_zero(
                (tangent.T * tangent)[0] - ell * (2 - ell),
                f"{fixture.name}: tangent norm {i},{j}",
            )
            tangent_mean += rates[i, j] * tangent
            radial_tangent += rates[i, j] * ell * tangent
            tangent_second += rates[i, j] * tangent * tangent.T
            covariance += rates[i, j] * delta * delta.T

        tangent_mean = tangent_mean.applyfunc(clean)
        radial_tangent = radial_tangent.applyfunc(clean)
        tangent_second = tangent_second.applyfunc(clean)
        covariance = covariance.applyfunc(clean)
        assert_matrix_zero(tangent_mean, f"{fixture.name}: tangent first moment {i}")
        assert_matrix_zero(radial_tangent,
                           f"{fixture.name}: radial-tangent covariance {i}")
        assert_matrix_zero(
            tangent_second - (2 - ell) * projector,
            f"{fixture.name}: isotropic tangent covariance {i}",
        )
        block_covariance = (
            epsilon * omega * omega.T
            - omega * radial_tangent.T - radial_tangent * omega.T
            + tangent_second
        ).applyfunc(clean)
        assert_matrix_zero(covariance - block_covariance,
                           f"{fixture.name}: covariance block split {i}")

        z_row = (omega * omega.T - identity / d).applyfunc(clean)
        matrix_m = (covariance + 2 * omega * omega.T - 2 * identity).applyfunc(clean)
        matrix_b = (
            matrix_m - sp.Rational(d, d - 1) * epsilon * z_row
        ).applyfunc(clean)
        block_b = (
            -omega * radial_tangent.T - radial_tangent * omega.T
            + tangent_second - (2 - epsilon / (d - 1)) * projector
        ).applyfunc(clean)
        assert_matrix_zero(matrix_b - block_b,
                           f"{fixture.name}: B block split {i}")
        assert_zero(
            frobenius(matrix_b, matrix_b)
            - 2 * (radial_tangent.T * radial_tangent)[0]
            - frobenius(
                tangent_second - (2 - epsilon / (d - 1)) * projector,
                tangent_second - (2 - epsilon / (d - 1)) * projector,
            ),
            f"{fixture.name}: orthogonal B block norm {i}",
        )
        assert_matrix_zero(matrix_b, f"{fixture.name}: B=0 {i}")

        scalar = clean(d * ell)
        assert_matrix_zero(matrix_m - scalar * z_row,
                           f"{fixture.name}: scalar residual row {i}")
        assert_zero(row_rate * ell - (d - 1),
                    f"{fixture.name}: rate-loss normalization {i}")
        assert_zero(epsilon - (d - 1) * ell,
                    f"{fixture.name}: epsilon normalization {i}")

        if clean(ell - 2) != 0:
            scale_sq = clean(ell * (2 - ell))
            if scale_sq.is_positive is not True:
                raise AssertionError(f"{fixture.name}: nonpositive tangent scale")
            probability_mean = sp.zeros(d, 1)
            probability_second = sp.zeros(d)
            for j in active:
                tangent = (projector * vertices[j]).applyfunc(clean)
                unit = (tangent / sp.sqrt(scale_sq)).applyfunc(clean)
                probability = clean(rates[i, j] / row_rate)
                assert_zero((unit.T * unit)[0] - 1,
                            f"{fixture.name}: unit tangent {i},{j}")
                probability_mean += probability * unit
                probability_second += probability * unit * unit.T
            assert_matrix_zero(probability_mean.applyfunc(clean),
                               f"{fixture.name}: centered tight frame {i}")
            assert_matrix_zero(
                probability_second.applyfunc(clean) - projector / (d - 1),
                f"{fixture.name}: weighted UNTF {i}",
            )

        for label, observed in (
            ("row rate", row_rate), ("loss", ell),
            ("epsilon", epsilon), ("scalar", scalar),
        ):
            target = {
                "row rate": common_row_rate,
                "loss": common_loss,
                "epsilon": common_epsilon,
                "scalar": common_scalar,
            }[label]
            if target is not None:
                assert_zero(observed - target, f"{fixture.name}: common {label}")
        common_row_rate = row_rate
        common_loss = ell
        common_epsilon = epsilon
        common_scalar = scalar

    assert_matrix_zero(residual - common_scalar * sampling,
                       f"{fixture.name}: R=cS")
    rank_s = sampling.rank()
    rank_r = residual.rank()
    e2 = rank_s - rank_r
    if rank_s != fixture.expected_rank:
        raise AssertionError(
            f"{fixture.name}: exact sampling rank {rank_s} != {fixture.expected_rank}"
        )
    if e2 != 0:
        raise AssertionError(f"{fixture.name}: equality must have e2=0, got {e2}")
    assert_zero(common_scalar * common_row_rate - d * (d - 1),
                f"{fixture.name}: exact frontier product")
    return EqualityState(
        fixture.name, d, n, clean(weights[0]), active_rate,
        active_conductance, common_row_rate, common_loss, common_epsilon,
        common_scalar, rank_s, len(basis) - rank_s, e2,
    )


def audit_symbolic_family_formulas() -> None:
    d = sp.symbols("d", integer=True, positive=True)
    families = {
        "simplex": {
            "n": d + 1, "degree": d,
            "a": (d - 1) / (d + 1), "ell": (d + 1) / d,
            "scalar": d + 1,
        },
        "cross-polytope": {
            "n": 2 * d, "degree": 2 * (d - 1),
            "a": sp.Rational(1, 2), "ell": 1, "scalar": d,
        },
        "hypercube": {
            "n": 2 ** d, "degree": d,
            "a": (d - 1) / 2, "ell": 2 / d, "scalar": 2,
        },
    }
    for name, row in families.items():
        rate = clean(row["degree"] * row["a"])
        epsilon = clean(rate * row["ell"] ** 2)
        assert_zero(rate * row["ell"] - (d - 1),
                    f"{name}: all-d first moment")
        assert_zero(epsilon - (d - 1) * row["ell"],
                    f"{name}: all-d epsilon")
        assert_zero(row["scalar"] - d * row["ell"],
                    f"{name}: all-d scalar")
        assert_zero(row["scalar"] * rate - d * (d - 1),
                    f"{name}: all-d product")
        assert_zero(row["a"] / row["n"] - row["a"] * (1 / row["n"]),
                    f"{name}: all-d conductance")


def raw_sym0_basis_3() -> list[sp.Matrix]:
    basis = [sp.diag(1, -1, 0), sp.diag(-1, -1, 2)]
    for p, q in ((0, 1), (0, 2), (1, 2)):
        matrix = sp.zeros(3)
        matrix[p, q] = matrix[q, p] = sp.Rational(1, 2)
        basis.append(matrix)
    return basis


def raw_sampling(vertices: list[sp.Matrix]) -> sp.Matrix:
    basis = raw_sym0_basis_3()
    return sp.Matrix(len(vertices), 5, lambda i, k:
        clean((vertices[i].T * basis[k] * vertices[i])[0]))


def audit_platonic_kernel_certificates() -> None:
    fixtures = {fixture.name: fixture for fixture in p1a.platonic_fixtures()}

    # Use the publication coordinates in which the alias spaces have their
    # displayed diagonal/off-diagonal descriptions.  The P1A simplex helper
    # uses an orthogonally rotated tetrahedron, which of course has the same
    # rank but not the same coordinate subspace.
    tetra_vertices = [
        sp.Matrix(signs) / sp.sqrt(3) for signs in
        ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    tetra = raw_sampling(tetra_vertices)
    cube = raw_sampling(fixtures["platonic-cube"].vertices)
    octa = raw_sampling(fixtures["platonic-octahedron"].vertices)
    assert_matrix_zero(tetra[:, :2], "tetrahedron diagonal aliases")
    assert_matrix_zero(cube[:, :2], "cube diagonal aliases")
    assert_zero(tetra.extract((0, 1, 2), (2, 3, 4)).det() + sp.Rational(4, 27),
                "tetrahedron exact rank minor")
    # The P1A cube ordering gives the opposite orientation of the documented
    # row certificate; only nonvanishing, not its sign, is intrinsic.
    cube_minor = clean(cube.extract((0, 1, 2), (2, 3, 4)).det())
    assert_zero(cube_minor ** 2 - sp.Rational(16, 729),
                "cube exact rank minor squared")
    assert_matrix_zero(octa[:, 2:], "octahedron off-diagonal aliases")
    assert_zero(octa.extract((0, 2), (0, 1)).det() ** 2 - 4,
                "octahedron exact rank minor squared")

    phi = (1 + sp.sqrt(5)) / 2
    rho = sp.sqrt(phi + 2)
    ico = [
        sp.Matrix(v) / rho for v in (
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1),
        )
    ]
    ico_minor = clean(raw_sampling(ico).extract((0, 1, 4, 5, 8), range(5)).det())
    assert_zero(ico_minor + 16 * sp.sqrt(5) / 125,
                "icosahedron exact Q(sqrt(5)) minor")

    dodeca_rows = [
        sp.Matrix(v) / sp.sqrt(3) for v in (
            (-1, -1, -1), (-1, -1, 1), (-1, 1, -1),
            (0, -1 / phi, -phi), (-1 / phi, -phi, 0),
        )
    ]
    dodeca_minor = clean(raw_sampling(dodeca_rows).det())
    assert_zero(dodeca_minor - sp.Rational(16, 81),
                "dodecahedron exact Q(sqrt(5)) minor")


def antipodal_equality_fixture(d: int = 3) -> p1a.Fixture:
    e1 = sp.eye(d)[:, 0]
    rate = sp.Rational(d - 1, 2)
    return p1a.uniform_fixture(
        f"antipodal-equality-d{d}", [e1, -e1],
        sp.Matrix([[0, rate], [rate, 0]]),
        sp.Integer(2 * d), 1,
    )


def blown_up_tetrahedron_fixture() -> p1a.Fixture:
    base = p1a.regular_simplex(3)
    vertices = [base[i] for i in range(4) for _ in range(2)]
    weights = [sp.Rational(1, 8)] * 8
    rates = sp.Matrix(8, 8, lambda left, right:
        sp.Rational(1, 4)
        if left // 2 != right // 2 else 0)
    return p1a.Fixture(
        "connected-twofold-tetrahedron-blowup", vertices, weights, rates,
        sp.Integer(4), 3,
    )


def long_chord_icosahedron_fixture() -> p1a.Fixture:
    """The connected non-1-skeleton shell with adjacent dot -1/sqrt(5)."""

    vertices = p1a.golden_vertices("icosahedron")
    alpha = -sp.sqrt(5) / 5
    rate = (5 - sp.sqrt(5)) / 10
    rates = sp.Matrix(12, 12, lambda i, j:
        rate if i != j and clean((vertices[i].T * vertices[j])[0] - alpha) == 0
        else 0)
    return p1a.uniform_fixture(
        "icosahedron-long-chord-shell", vertices, rates,
        3 + 3 * sp.sqrt(5) / 5, 5,
    )


def audit_antipodal_and_global_classification_guards() -> list[EqualityState]:
    antipodal = audit_equality_fixture(antipodal_equality_fixture())
    assert_zero(antipodal.loss - 2, "antipodal shell loss")
    # Here ell(2-ell)=0: all tangent increments vanish, so division by the
    # tangent length and the unit-norm frame statement are deliberately barred.
    blowup = audit_equality_fixture(blown_up_tetrahedron_fixture())
    if blowup.nodes != 8 or blowup.dim_kernel != 2:
        raise AssertionError(f"connected blowup alias regression: {blowup}")
    long_ico_fixture = long_chord_icosahedron_fixture()
    long_ico = audit_equality_fixture(long_ico_fixture)
    if len(generator_from_rates(long_ico_fixture.rates).nullspace()) != 1:
        raise AssertionError("long-chord icosahedral equality graph is disconnected")
    assert_zero(long_ico.loss - (1 + sp.sqrt(5) / 5),
                "long-chord icosahedral shell")

    # A centered weighted unit tight frame in R^2 that is not a regular square.
    weights = [sp.Rational(1, 5), sp.Rational(1, 5),
               sp.Rational(3, 10), sp.Rational(3, 10)]
    directions = [
        sp.Matrix([sp.sqrt(3) / 2, sp.Rational(1, 2)]),
        sp.Matrix([sp.sqrt(3) / 2, -sp.Rational(1, 2)]),
        sp.Matrix([-1 / sp.sqrt(3), sp.sqrt(sp.Rational(2, 3))]),
        sp.Matrix([-1 / sp.sqrt(3), -sp.sqrt(sp.Rational(2, 3))]),
    ]
    mean = sum((weights[k] * directions[k] for k in range(4)), sp.zeros(2, 1))
    second = sum(
        (weights[k] * directions[k] * directions[k].T for k in range(4)),
        sp.zeros(2),
    )
    assert_matrix_zero(mean.applyfunc(clean), "nonregular weighted frame mean")
    assert_matrix_zero((second - sp.eye(2) / 2).applyfunc(clean),
                       "nonregular weighted frame covariance")
    if len(set(weights)) == 1:
        raise AssertionError("weighted-frame mutation unexpectedly became uniform")

    # Kolmogorov cycle products are the exact missing reversibility condition.
    forward = [sp.Rational(2, 3), sp.Rational(3, 5), sp.Rational(5, 7)]
    reverse = [sp.Rational(1, 3), sp.Rational(3, 7), sp.Rational(2, 1)]
    assert_zero(sp.prod(forward) - sp.prod(reverse),
                "cycle reversibility product")
    mutated = list(reverse)
    mutated[-1] += 1
    if clean(sp.prod(forward) - sp.prod(mutated)) == 0:
        raise AssertionError("cycle-reversibility mutation escaped")
    return [antipodal, blowup, long_ico]


def mutation_tests(states: list[EqualityState]) -> None:
    for state in states:
        if state.e2 != 0:
            raise AssertionError(f"form/sample alias conflation: {state}")
        assert_zero(state.scalar * state.row_rate - state.d * (state.d - 1),
                    f"{state.name}: frontier mutation")
    tetra = next(row for row in states if row.name == "platonic-tetrahedron")
    octa = next(row for row in states if row.name == "platonic-octahedron")
    cube = next(row for row in states if row.name == "platonic-cube")
    if (tetra.dim_kernel, octa.dim_kernel, cube.dim_kernel) != (2, 3, 2):
        raise AssertionError("tetra/octa/cube alias dimensions changed")
    if any(row.e2 != 0 for row in (tetra, octa, cube)):
        raise AssertionError("algebraic aliases were misreported as sampled modes")


def main() -> None:
    audit_symbolic_family_formulas()
    states: list[EqualityState] = []
    for d in (2, 3, 4, 5):
        for kind in ("simplex", "cross-polytope", "hypercube"):
            states.append(audit_equality_fixture(family_fixture(kind, d)))
    states.extend(audit_equality_fixture(fixture)
                  for fixture in p1a.platonic_fixtures())
    audit_platonic_kernel_certificates()
    states.extend(audit_antipodal_and_global_classification_guards())
    mutation_tests(states)

    for row in states:
        print(
            f"{row.name}: d={row.d} N={row.nodes} w={row.weight} "
            f"gamma={row.active_conductance} a={row.active_rate} "
            f"r={row.row_rate} ell={row.loss} epsilon={row.epsilon} "
            f"M/Z=D2={row.scalar} rankS={row.rank_s} "
            f"dimK={row.dim_kernel} e2={row.e2} D2*r={clean(row.scalar * row.row_rate)}"
        )
    print(f"equality-fixtures={len(states)}")
    print("all-dimensional family identities: EXACT_SYMBOLIC")
    print("local radial-tangent block theorem: PASS")
    print("nonantipodal weighted tight-frame equivalence: PASS")
    print("antipodal zero-frame exception: PASS")
    print("Platonic algebraic rank and alias certificates: PASS")
    print("connected blowup classification adversary: PASS")
    print("sampling aliases are not sampled H2 modes: PASS")
    print("P1C exact equality-geometry audit: PASS")


if __name__ == "__main__":
    main()
