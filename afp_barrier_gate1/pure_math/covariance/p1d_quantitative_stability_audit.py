#!/usr/bin/env python3
"""Exact and interval-certified regression audit for P1D stability.

The all-orders stability theorem is proved in ``P1D_QUANTITATIVE_STABILITY.md``.
This program is deliberately only its deterministic adversarial audit.  All
finite algebra, graph ranks, and fixture identities are evaluated exactly by
SymPy.  The final extreme-scale pass uses ``mpmath.iv`` outward-rounded
intervals and never makes a rank decision from floating-point data.
"""

from __future__ import annotations

from dataclasses import dataclass

from mpmath import iv
import sympy as sp

import p1a_quadratic_fidelity_audit as p1a
import p1b_sharp_quadratic_defect_audit as p1b


def clean(value):
    return p1a.clean(value)


def assert_zero(value, label: str) -> None:
    p1a.assert_zero(value, label)


def assert_nonnegative(value, label: str) -> None:
    value = clean(value)
    if value.is_nonnegative is not True:
        raise AssertionError(f"{label}: expected exact nonnegative value, got {value}")


def assert_positive(value, label: str) -> None:
    value = clean(value)
    if value.is_positive is not True:
        raise AssertionError(f"{label}: expected exact positive value, got {value}")


def frobenius_sq(matrix: sp.Matrix):
    return clean(sp.trace(matrix.T * matrix))


@dataclass(frozen=True)
class LocalData:
    rates: tuple[sp.Expr, ...]
    epsilon: tuple[sp.Expr, ...]
    variance: tuple[sp.Expr, ...]
    b_sq: tuple[sp.Expr, ...]
    sampling: sp.Matrix
    residual: sp.Matrix
    defect_sq: sp.Expr


def local_data(fixture: p1a.Fixture) -> LocalData:
    """Compute the P1D local data and quotient norm in exact algebra."""

    vertices, weights, rates = fixture.vertices, fixture.weights, fixture.rates
    n, d = len(vertices), vertices[0].rows
    basis = p1a.sym0_orthonormal_basis(d)
    identity = sp.eye(d)
    sampling = sp.Matrix(n, len(basis), lambda i, k:
        clean((vertices[i].T * basis[k] * vertices[i])[0]))
    generator = p1b.generator_from_rates(rates)
    residual = ((generator + 2 * d * sp.eye(n)) * sampling).applyfunc(clean)
    gram_s = (sampling.T * sp.diag(*weights) * sampling).applyfunc(clean)
    gram_r = (residual.T * sp.diag(*weights) * residual).applyfunc(clean)

    column_space = gram_s.columnspace()
    if not column_space:
        raise AssertionError(f"{fixture.name}: impossible zero sampling rank")
    lift = sp.Matrix.hstack(*column_space)
    reduced_s = (lift.T * gram_s * lift).applyfunc(clean)
    reduced_r = (lift.T * gram_r * lift).applyfunc(clean)
    if clean(reduced_s.det()) == 0:
        raise AssertionError(f"{fixture.name}: singular exact deflated sampling Gram")
    pencil = (reduced_s.inv() * reduced_r).applyfunc(clean)
    eigenvalues: list[sp.Expr] = []
    for value, multiplicity in pencil.eigenvals().items():
        eigenvalues.extend([clean(value)] * multiplicity)
    defect_sq = p1a.exact_max(
        eigenvalues, f"{fixture.name}: exact quotient maximum",
        require_nonnegative=True,
    )

    row_rates: list[sp.Expr] = []
    epsilons: list[sp.Expr] = []
    variances: list[sp.Expr] = []
    b_norms: list[sp.Expr] = []
    for i, omega in enumerate(vertices):
        row_rate = clean(sum(rates[i, j] for j in range(n) if i != j))
        assert_positive(row_rate, f"{fixture.name}: row rate {i}")
        covariance = sp.zeros(d)
        epsilon = sp.S.Zero
        variance = sp.S.Zero
        mean_loss = clean(sp.Rational(d - 1, 1) / row_rate)
        for j in range(n):
            if i == j or clean(rates[i, j]) == 0:
                continue
            increment = vertices[j] - omega
            loss = clean(1 - (omega.T * vertices[j])[0])
            covariance += rates[i, j] * increment * increment.T
            epsilon += rates[i, j] * loss ** 2
            variance += rates[i, j] * (loss - mean_loss) ** 2
        covariance = covariance.applyfunc(clean)
        epsilon, variance = clean(epsilon), clean(variance)
        z_row = (omega * omega.T - identity / d).applyfunc(clean)
        m_row = (covariance + 2 * omega * omega.T - 2 * identity).applyfunc(clean)
        b_row = (m_row - sp.Rational(d, d - 1) * epsilon * z_row).applyfunc(clean)
        row_rates.append(row_rate)
        epsilons.append(epsilon)
        variances.append(variance)
        b_norms.append(frobenius_sq(b_row))

    return LocalData(
        tuple(row_rates), tuple(epsilons), tuple(variances), tuple(b_norms),
        sampling, residual, clean(defect_sq),
    )


def audit_master_fixture(d: int, rmax: sp.Expr, delta: sp.Expr) -> None:
    """Audit every requested scalar constant on an exact feasible budget."""

    d, rmax, delta = sp.Integer(d), clean(rmax), clean(delta)
    a0 = clean((d - 1) ** 2 / rmax)
    eta = clean(2 * delta + delta ** 2)
    weights = (sp.Rational(1, 3), sp.Rational(2, 3))
    q = (clean(delta / (1 + delta)), clean(delta / (2 + delta)))
    s = tuple(clean(value / 3) for value in q)
    v = tuple(clean(value - rate) for value, rate in zip(q, s))
    radial_budget = clean(sum(
        weight * (2 * value + value ** 2)
        for weight, value in zip(weights, q)
    ))
    assert_nonnegative(eta - radial_budget, "master radial slack")
    b_energy = clean(
        sp.Rational(1, 2) * d * a0 ** 2 / (d - 1)
        * (eta - radial_budget)
    )
    beta = clean((d - 1) / (d * a0 ** 2))
    master_lhs = clean(radial_budget + beta * b_energy)
    assert_nonnegative(eta - master_lhs, "master energy inequality")

    q2 = clean(sum(w * value ** 2 for w, value in zip(weights, q)))
    s2 = clean(sum(w * value ** 2 for w, value in zip(weights, s)))
    v2 = clean(sum(w * value ** 2 for w, value in zip(weights, v)))
    assert_nonnegative(eta - q2, "normalized epsilon variance")
    assert_nonnegative(eta - s2, "normalized rate variance")
    assert_nonnegative(eta - v2, "normalized loss-variance square")
    assert_nonnegative(
        d * (d - 1) ** 3 * eta / rmax ** 2 - b_energy,
        "anisotropy coefficient",
    )
    variance_energy = clean(a0 * sum(w * value for w, value in zip(weights, v)))
    variance_sq_energy = clean(a0 ** 2 * v2)
    assert_nonnegative(a0 * delta - variance_energy, "weighted V first moment")
    assert_nonnegative(a0 ** 2 * eta - variance_sq_energy,
                       "weighted V second moment")

    # Squared form of the exact pointwise estimate
    # q_i <= sqrt(1+eta/w_i)-1, avoiding any approximate square roots.
    for index, (weight, value) in enumerate(zip(weights, q)):
        assert_nonnegative(
            1 + eta / weight - (1 + value) ** 2,
            f"pointwise w_min dependence {index}",
        )

    # Exact Markov/Chebyshev counts for a threshold chosen from the fixture.
    threshold = clean(q[1] / 2)
    if threshold != 0:
        mass = clean(sum(w for w, value in zip(weights, q) if value >= threshold))
        assert_nonnegative(delta / threshold - mass, "vertex Markov fraction")
        assert_nonnegative(eta / threshold ** 2 - mass, "vertex Chebyshev fraction")


def aligned_cube_tetra_fixture(tiny_mass: sp.Expr) -> p1a.Fixture:
    """The sharp small-mass fixture: aligned cube and tetrahedron shells."""

    equality = next(
        fixture for fixture in p1a.platonic_fixtures()
        if fixture.name == "platonic-cube"
    )
    tiny_mass = clean(tiny_mass)
    signs = [
        tuple(int(clean(vertex[k] * sp.sqrt(3))) for k in range(3))
        for vertex in equality.vertices
    ]
    tetra_indices = [
        i for i, sign in enumerate(signs)
        if sign[0] * sign[1] * sign[2] == 1
    ]
    if len(tetra_indices) != 4:
        raise AssertionError("aligned cube: tetrahedral ray selection changed")
    tetra = [equality.vertices[i] for i in tetra_indices]
    tetra_rates = sp.Matrix(4, 4, lambda i, j:
        sp.Rational(1, 2) if i != j else 0)
    return p1a.Fixture(
        f"aligned-cube-tetra-small-mass-{tiny_mass}",
        equality.vertices + tetra,
        [(1 - tiny_mass) * weight for weight in equality.weights]
        + [tiny_mass / 4] * 4,
        sp.diag(equality.rates, tetra_rates),
        None,
        None,
    )


def audit_small_mass_fixture(tiny_mass: sp.Expr) -> None:
    """A fixed rate-ratio defect hidden behind mass ``tiny_mass``.

    The tetrahedral nodes coincide with four cube nodes, and degree-two
    samples are projective.  The cube and tetrahedral sampling frames are
    therefore exactly aligned.  This makes the fixture sharp, not merely an
    asymptotic example.
    """

    tiny_mass = clean(tiny_mass)
    fixture = aligned_cube_tetra_fixture(tiny_mass)
    data = local_data(fixture)
    assert_zero(data.defect_sq - 4 * (1 + 3 * tiny_mass),
                f"{fixture.name}: exact D2 squared")
    rmax = p1a.exact_max(data.rates, f"{fixture.name}: rmax")
    assert_zero(rmax - 3, f"{fixture.name}: common maximum rate")
    eta = clean(data.defect_sq / 4 - 1)
    assert_zero(eta - 3 * tiny_mass,
                f"{fixture.name}: exact frontier-square excess")

    # The tetrahedral block retains the exact normalized rate defect s=1 on
    # total mass t even as t and the global frontier excess tend to zero.
    for index in range(8, 12):
        assert_zero(data.rates[index] - sp.Rational(3, 2),
                    f"{fixture.name}: tetra row rate {index}")
        assert_zero(data.epsilon[index] - sp.Rational(8, 3),
                    f"{fixture.name}: tetra epsilon {index}")
        assert_zero(data.variance[index],
                    f"{fixture.name}: tetra loss variance {index}")
        assert_zero(data.b_sq[index], f"{fixture.name}: tetra B norm {index}")
    q2 = clean(sum(
        fixture.weights[i]
        * (data.epsilon[i] / sp.Rational(4, 3) - 1) ** 2
        for i in range(12)
    ))
    assert_zero(q2 - tiny_mass, f"{fixture.name}: weighted q square")
    assert_nonnegative(eta - q2, f"{fixture.name}: requested epsilon bound")
    s2 = clean(sum(
        fixture.weights[i] * (3 / data.rates[i] - 1) ** 2
        for i in range(12)
    ))
    assert_zero(s2 - tiny_mass, f"{fixture.name}: weighted rate defect")
    # The stronger nonnegative master summand is exactly t*(2+1)=3t.
    assert_zero(
        sum(fixture.weights[i]
            * (2 * (3 / data.rates[i] - 1)
               + (3 / data.rates[i] - 1) ** 2)
            for i in range(12)) - eta,
        f"{fixture.name}: sharp master budget",
    )


def audit_tetrahedral_alias() -> None:
    tetra = next(
        fixture for fixture in p1a.platonic_fixtures()
        if fixture.name == "platonic-tetrahedron"
    )
    data = local_data(tetra)
    assert data.sampling.rank() == 3
    assert data.sampling.cols == 5
    if len(data.sampling.nullspace()) != 2:
        raise AssertionError("tetrahedron: exact sampling alias dimension changed")
    assert_zero(data.defect_sq - 16, "tetrahedron: exact scalar quotient")
    p1a.assert_matrix_zero(data.residual - 4 * data.sampling,
                           "tetrahedron: quotient scalar action with aliases")


def audit_compass_fixture(kappa: sp.Expr) -> None:
    """Actual reversible S^1 compass generator with rare antipodal edges."""

    kappa = clean(kappa)
    assert_positive(kappa, "compass kappa")
    assert_positive(1 - kappa, "compass probability remainder")
    vertices = [sp.Matrix([1, 0]), sp.Matrix([-1, 0]),
                sp.Matrix([0, 1]), sp.Matrix([0, -1])]
    row_rate = clean(1 / (1 + kappa))
    rates = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            dot = clean((vertices[i].T * vertices[j])[0])
            rates[i, j] = (
                row_rate * kappa if dot == -1
                else row_rate * (1 - kappa) / 2
            )
    fixture = p1a.Fixture(
        f"s1-kappa-compass-{kappa}", vertices,
        [sp.Rational(1, 4)] * 4, rates, None, None,
    )
    data = local_data(fixture)
    for i in range(4):
        assert_zero(data.rates[i] - row_rate,
                    f"{fixture.name}: common rate {i}")
        assert_zero(data.epsilon[i] - (1 + 3 * kappa) / (1 + kappa),
                    f"{fixture.name}: epsilon {i}")
        assert_zero(data.variance[i] - kappa * (1 - kappa) / (1 + kappa),
                    f"{fixture.name}: loss variance {i}")
        assert_zero(data.b_sq[i], f"{fixture.name}: one-dimensional B {i}")
    assert_zero(data.defect_sq - 4 * (1 + 3 * kappa) ** 2 / (1 + kappa) ** 2,
                f"{fixture.name}: exact quotient defect")
    delta = clean((1 + 3 * kappa) / (1 + kappa) ** 2 - 1)
    assert_zero(delta - kappa * (1 - kappa) / (1 + kappa) ** 2,
                f"{fixture.name}: exact frontier excess")

    # Every antipodal transition has p_ij=kappa and loss defect 1-kappa.
    # Thus an O(1) edge defect survives while V_i=O(kappa).
    for i in range(4):
        antipode = 1 - i if i < 2 else 5 - i
        probability = clean(rates[i, antipode] / row_rate)
        assert_zero(probability - kappa,
                    f"{fixture.name}: antipodal probability {i}")
        bad_deviation = clean(2 - (1 + kappa))
        assert_zero(bad_deviation - (1 - kappa),
                    f"{fixture.name}: antipodal loss defect {i}")
        assert_nonnegative(
            data.variance[i] / (kappa * row_rate) - bad_deviation ** 2,
            f"{fixture.name}: kappa edge bound {i}",
        )


def audit_path_fixture(edges: int) -> None:
    """Reflecting reversible Markov path with exact diameter/gap dependence.

    This is a sharpness audit for the *graph propagation lemma*.  It is not
    presented as a closed cyclic spherical embedding or as a new spherical
    generator: the reflecting endpoints are essential and are checked here.
    """

    if edges < 2:
        raise ValueError(edges)
    n = edges + 1
    stationary = [sp.Rational(1, 2 * edges)] + [sp.Rational(1, edges)] * (edges - 1) + [sp.Rational(1, 2 * edges)]
    assert_zero(sum(stationary) - 1, f"path-{edges}: stationary normalization")
    row_sums = [sp.Integer(1)] + [sp.Rational(1, 2) + sp.Rational(1, 2)] * (edges - 1) + [sp.Integer(1)]
    for i, row_sum in enumerate(row_sums):
        assert_zero(row_sum - 1, f"path-{edges}: stochastic row {i}")
    active: list[sp.Expr] = []
    for i in range(edges):
        forward = sp.Integer(1) if i == 0 else sp.Rational(1, 2)
        reverse = sp.Integer(1) if i + 1 == edges else sp.Rational(1, 2)
        active.extend((forward, reverse))
        assert_zero(
            stationary[i] * forward - stationary[i + 1] * reverse,
            f"path-{edges}: detailed balance {i},{i + 1}",
        )
    assert min(active) == sp.Rational(1, 2)
    shell_step = sp.Rational(1, edges ** 2)
    shells = [sp.Rational(2, 5) + i * shell_step for i in range(n)]
    local_errors = [shell_step / 2] * n
    for i in range(edges):
        assert_zero(
            abs(shells[i + 1] - shells[i])
            - local_errors[i] - local_errors[i + 1],
            f"path-{edges}: sharp adjacent propagation {i}",
        )
    assert_zero(
        shells[-1] - shells[0] - edges * shell_step,
        f"path-{edges}: diameter accumulation",
    )
    # The exact reflecting-walk gap records why replacing diameter by a gap
    # must explicitly pay the Poincare constant.
    # Avoid algebraic expansion of cos(pi/1000): positivity follows directly
    # from 0 < pi/(2D) < pi/2, and the displayed expression is exact.
    gap = 2 * sp.sin(sp.pi / (2 * edges)) ** 2
    if gap.is_positive is not True:
        raise AssertionError(f"path-{edges}: exact spectral gap not positive: {gap}")


def audit_singular_tangent_frame(parameter: int) -> None:
    """A quadratic moment residual along a first-order flex."""

    n = sp.Integer(parameter)
    q = clean((n ** 2 - 1) / (n ** 2 + 1))
    s = clean(2 * n / (n ** 2 + 1))
    assert_zero(q ** 2 + s ** 2 - 1, f"singular-frame-{n}: unit direction")
    directions = (
        sp.Matrix([q, s]), sp.Matrix([-q, -s]),
        sp.Matrix([q, -s]), sp.Matrix([-q, s]),
        sp.Matrix([0, 1]), sp.Matrix([0, -1]),
    )
    weights = (sp.Rational(1, 8),) * 4 + (sp.Rational(1, 4),) * 2
    mean = sum((w * y for w, y in zip(weights, directions)), sp.zeros(2, 1))
    covariance = sum(
        (w * y * y.T for w, y in zip(weights, directions)), sp.zeros(2)
    ).applyfunc(clean)
    p1a.assert_matrix_zero(mean.applyfunc(clean),
                           f"singular-frame-{n}: centered")
    covariance_defect = (covariance - sp.eye(2) / 2).applyfunc(clean)
    assert_zero(frobenius_sq(covariance_defect) - s ** 4 / 2,
                f"singular-frame-{n}: quadratic covariance residual")
    reference_distance_sq = clean(1 - q)
    assert_positive(reference_distance_sq,
                    f"singular-frame-{n}: nonzero frame displacement")
    ratio_sq = clean(frobenius_sq(covariance_defect) / reference_distance_sq)
    assert_positive(ratio_sq, f"singular-frame-{n}: residual/distance ratio")

    # At the limiting duplicated frame the covariance derivative has both the
    # rotational kernel and an independent antisymmetric splitting flex.
    jacobian = sp.Matrix([[sp.Rational(1, 4), sp.Rational(1, 4),
                           -sp.Rational(1, 2)]])
    rotation = sp.Matrix([1, 1, 1])
    flex = sp.Matrix([1, -1, 0])
    p1a.assert_matrix_zero(jacobian * rotation,
                           f"singular-frame-{n}: rotation kernel")
    p1a.assert_matrix_zero(jacobian * flex,
                           f"singular-frame-{n}: extra flex kernel")
    if sp.Matrix.hstack(rotation, flex).rank() != 2:
        raise AssertionError("singular tangent-frame flexes lost independence")


def sampling_gap_fixture(parameter: int) -> tuple[p1a.Fixture, sp.Expr]:
    """Four actual S^1 nodes on two rays meeting at angle phi."""

    n = sp.Integer(parameter)
    # cos(phi)=2n/(n^2+1), sin(phi)=(n^2-1)/(n^2+1).  For n>=3,
    # pi/4 < phi < pi/2 and all coordinates remain rational.
    cosine = clean(2 * n / (n ** 2 + 1))
    sine = clean((n ** 2 - 1) / (n ** 2 + 1))
    assert_zero(cosine ** 2 + sine ** 2 - 1,
                f"sampling-gap-{n}: rational unit circle")
    assert_positive(sine - cosine, f"sampling-gap-{n}: phi>pi/4")
    vertices = [
        sp.Matrix([1, 0]), sp.Matrix([-1, 0]),
        sp.Matrix([cosine, sine]), sp.Matrix([-cosine, -sine]),
    ]
    rates = sp.zeros(4)
    for i in (0, 1):
        for j in (2, 3):
            rates[i, j] = rates[j, i] = sp.Rational(1, 2)
    return p1a.Fixture(
        f"actual-s1-sampling-gap-{n}", vertices,
        [sp.Rational(1, 4)] * 4, rates, None, None,
    ), cosine


def audit_sampling_gap(parameter: int) -> None:
    """Actual generator attaining the 1/sqrt(alpha_X) quotient loss."""

    fixture, cosine = sampling_gap_fixture(parameter)
    data = local_data(fixture)
    if data.sampling.rank() != 2:
        raise AssertionError(f"{fixture.name}: exact positive-angle sampling rank")
    if any(rate != 1 for rate in data.rates):
        raise AssertionError(f"{fixture.name}: rmax is not exactly one")
    alpha = clean(cosine ** 2 / 2)
    gram_s = (
        data.sampling.T * sp.diag(*fixture.weights) * data.sampling
    ).applyfunc(clean)
    p1a.assert_exact_multiset(
        gram_s.eigenvals().keys(),
        [alpha, clean((1 - cosine ** 2) / 2)],
        f"{fixture.name}: exact sampling frame eigenvalues",
    )
    assert_positive(clean((1 - cosine ** 2) / 2 - alpha),
                    f"{fixture.name}: alpha is the lower frame bound")

    # On the two ray-constant values, U has the exact matrix [[3,1],[1,3]]:
    # eigenvalue 4 on the constant ray mode and 2 on the contrast mode.
    sample_rays = data.sampling.extract((0, 2), (0, 1))
    residual_rays = data.residual.extract((0, 2), (0, 1))
    quotient = (residual_rays * sample_rays.inv()).applyfunc(clean)
    p1a.assert_matrix_zero(
        quotient - sp.Matrix([[3, 1], [1, 3]]),
        f"{fixture.name}: exact quotient action",
    )
    p1a.assert_exact_multiset(
        quotient.eigenvals().keys(), [2, 4],
        f"{fixture.name}: quotient eigenvalues",
    )
    assert_zero(data.defect_sq - 16, f"{fixture.name}: D2 squared")

    c0 = sp.Integer(2)
    perturbation = (data.residual - c0 * data.sampling).applyfunc(clean)
    hs_sq = clean(sp.trace(
        perturbation.T * sp.diag(*fixture.weights) * perturbation
    ))
    assert_zero(hs_sq - 4 * alpha,
                f"{fixture.name}: exact Hilbert-Schmidt deviation")
    quotient_deviation = (quotient - c0 * sp.eye(2)).applyfunc(clean)
    deviation_norm_sq = p1a.exact_max(
        quotient_deviation.eigenvals().keys(),
        f"{fixture.name}: scalar quotient deviation", require_nonnegative=True,
    ) ** 2
    assert_zero(deviation_norm_sq - 4,
                f"{fixture.name}: nonvanishing quotient deviation")
    assert_zero(deviation_norm_sq - hs_sq / alpha,
                f"{fixture.name}: attained alpha^(-1/2) dependence")


def audit_sampling_alias_endpoint() -> None:
    """At phi=pi/2 the constant ray mode becomes an exact coefficient alias."""

    vertices = [sp.Matrix([1, 0]), sp.Matrix([-1, 0]),
                sp.Matrix([0, 1]), sp.Matrix([0, -1])]
    rates = sp.zeros(4)
    for i in (0, 1):
        for j in (2, 3):
            rates[i, j] = rates[j, i] = sp.Rational(1, 2)
    fixture = p1a.Fixture(
        "actual-s1-sampling-alias-phi-pi-over-two", vertices,
        [sp.Rational(1, 4)] * 4, rates, None, None,
    )
    data = local_data(fixture)
    if data.sampling.rank() != 1 or len(data.sampling.nullspace()) != 1:
        raise AssertionError(f"{fixture.name}: constant coefficient alias lost")
    p1a.assert_matrix_zero(
        data.residual - 2 * data.sampling,
        f"{fixture.name}: scalar action on surviving contrast quotient",
    )


def iv_point(text: str):
    return iv.mpf([text, text])


def assert_iv_nonnegative(value, label: str) -> None:
    """Accept only when outward rounding certifies the whole interval >= 0."""

    if not bool(value.a >= 0):
        raise AssertionError(f"{label}: interval lower endpoint is negative: {value}")


def assert_iv_contains(value, target, label: str) -> None:
    if not (bool(value.a <= target) and bool(target <= value.b)):
        raise AssertionError(f"{label}: {value} does not enclose {target}")


def audit_interval_scale(
    tiny_text: str, kappa_text: str, phi_text: str, d: int, rmax_text: str
) -> None:
    """Outward-rounded stress test; no interval is used for rank selection."""

    delta = iv_point(tiny_text)
    rmax = iv_point(rmax_text)
    dimension = iv_point(str(d))
    one = iv_point("1")
    two = iv_point("2")
    three = iv_point("3")
    eta = two * delta + delta * delta
    q = delta / (one + delta)
    weight = iv_point("0.125")
    assert_iv_nonnegative(
        one + eta / weight - (one + q) * (one + q),
        f"interval t={tiny_text}: pointwise vertex bound",
    )
    a0 = (dimension - one) * (dimension - one) / rmax
    b_constant = dimension * (dimension - one) ** 3 / (rmax * rmax)
    b_energy = b_constant * eta / three
    assert_iv_nonnegative(
        b_constant * eta - b_energy,
        f"interval t={tiny_text}: anisotropy bound",
    )
    variance = a0 * delta / three
    assert_iv_nonnegative(
        a0 * delta - variance,
        f"interval t={tiny_text}: loss-variance bound",
    )
    kappa = iv_point(kappa_text)
    rate = (dimension - one) / iv_point("0.75")
    edge_sq = variance / (two * kappa * rate)
    assert_iv_nonnegative(
        variance / (kappa * rate) - edge_sq,
        f"interval t={tiny_text}: kappa edge bound",
    )
    diameter = iv_point("1000000")
    step = iv.sqrt(edge_sq)
    path_bound = diameter * step / two
    assert_iv_nonnegative(
        diameter * step - path_bound,
        f"interval t={tiny_text}: diameter propagation",
    )
    # Here phi_text is cos(phi), for the actual two-ray S^1 fixture with
    # phi close to pi/2.  Its lower sampling-frame eigenvalue is cos^2(phi)/2,
    # the coefficient-space Hilbert-Schmidt defect is 4*alpha, and the
    # quotient scalar deviation remains exactly 2.
    cos_phi = iv_point(phi_text)
    sin_phi = iv.sqrt(one - cos_phi * cos_phi)
    assert_iv_contains(cos_phi * cos_phi + sin_phi * sin_phi, 1,
                       f"interval t={tiny_text}: two-ray unit vector")
    alpha = cos_phi * cos_phi / two
    hs_sq = iv_point("4") * alpha
    amplified = iv.sqrt(hs_sq / alpha)
    assert_iv_contains(amplified, 2,
                       f"interval t={tiny_text}: alpha amplification")


def main() -> None:
    counts: dict[str, int] = {}

    master_parameters = [
        (2, sp.Rational(7, 3), sp.Rational(0)),
        (3, sp.Rational(11, 4), sp.Rational(1, 10**6)),
        (7, sp.Rational(101, 9), sp.Rational(1, 7)),
        (31, sp.Rational(10**5, 3), sp.Rational(7, 3)),
        (64, sp.Rational(10**12), sp.Rational(10**6)),
    ]
    for parameters in master_parameters:
        audit_master_fixture(*parameters)
    counts["master"] = len(master_parameters)

    small_masses = [sp.Rational(1, 10), sp.Rational(1, 10**3),
                    sp.Rational(1, 10**6)]
    for tiny_mass in small_masses:
        audit_small_mass_fixture(tiny_mass)
    counts["small-w"] = len(small_masses)

    audit_tetrahedral_alias()
    audit_sampling_alias_endpoint()
    counts["alias"] = 2

    kappas = [sp.Rational(1, 4), sp.Rational(1, 10),
              sp.Rational(1, 10**4), sp.Rational(1, 10**9)]
    for kappa in kappas:
        audit_compass_fixture(kappa)
    counts["kappa-compass"] = len(kappas)

    path_lengths = [2, 17, 1000]
    for length in path_lengths:
        audit_path_fixture(length)
    counts["paths"] = len(path_lengths)

    singular_parameters = [2, 10, 10**3, 10**6]
    for parameter in singular_parameters:
        audit_singular_tangent_frame(parameter)
    counts["singular-frame"] = len(singular_parameters)

    sampling_parameters = [3, 10, 10**4, 10**9]
    for parameter in sampling_parameters:
        audit_sampling_gap(parameter)
    counts["sampling-gap"] = len(sampling_parameters)

    iv.dps = 100
    interval_parameters = [
        ("1e-40", "1e-45", "1e-50", 2, "1e40"),
        ("1e-20", "1e-30", "1e-35", 3, "1e-20"),
        ("1e-8", "1e-12", "1e-16", 17,
         "3.1415926535897932384626433832795028841971"),
        ("1", "1e-8", "1e-10", 64, "1e12"),
        ("1e20", "1e-20", "1e-30", 257, "1e-30"),
    ]
    for parameters in interval_parameters:
        audit_interval_scale(*parameters)
    counts["interval"] = len(interval_parameters)

    total = sum(counts.values())
    if total != 30:
        raise AssertionError(f"P1D fixture inventory changed: {counts}")
    print(f"fixtures={total}")
    for label, count in counts.items():
        print(f"{label}-fixtures={count}")
    print("exact master constants and requested bounds: PASS")
    print("small-w cube and tetrahedral alias adversaries: PASS")
    print("kappa conductance and diameter/gap propagation scaling: PASS")
    print("singular tangent-frame and sampling-gap amplification: PASS")
    print("outward-rounded interval stress over extreme scales: PASS")
    print("P1D quantitative stability audit: PASS")


if __name__ == "__main__":
    main()
