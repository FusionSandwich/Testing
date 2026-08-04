#!/usr/bin/env python3
"""Exact P1B audit for the sharp genuinely sampled quadratic-defect bound.

The general theorem is proved in P1B_SHARP_QUADRATIC_DEFECT_BOUND.md.  This
script is deterministic regression and adversarial evidence.  It imports the
accepted P1A exact fixtures and recomputes all P1B quantities in SymPy exact
algebra; no finite fixture is used as a substitute for the all-dimensional
proof.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

import p1a_quadratic_fidelity_audit as p1a


def clean(value):
    return p1a.clean(value)


def assert_zero(value, label: str) -> None:
    p1a.assert_zero(value, label)


def assert_matrix_zero(matrix: sp.Matrix, label: str) -> None:
    p1a.assert_matrix_zero(matrix, label)


def assert_nonnegative(value, label: str) -> None:
    value = clean(value)
    if value.is_nonnegative is not True:
        raise AssertionError(f"{label}: expected certified nonnegative, got {value}")


def sym0_basis(d: int) -> list[sp.Matrix]:
    return p1a.sym0_orthonormal_basis(d)


def generator_from_rates(rates: sp.Matrix) -> sp.Matrix:
    n = rates.rows
    return sp.Matrix(
        n,
        n,
        lambda i, j: rates[i, j]
        if i != j
        else -sum(rates[i, k] for k in range(n) if k != i),
    )


def nearly_singular_fixture(n: int) -> p1a.Fixture:
    """Two antipodal pairs in S^1 with rationally close axes.

    The two rank-one trace-free sampling directions are independent for every
    finite n>=2, but their Gram determinant tends to zero as n tends to
    infinity.  The complete centered generator is positive and reversible.
    """

    if n < 2:
        raise ValueError(n)
    q = sp.Rational(n * n - 1, n * n + 1)
    s = sp.Rational(2 * n, n * n + 1)
    e1 = sp.Matrix([1, 0])
    v = sp.Matrix([q, s])
    vertices = [e1, -e1, v, -v]
    weights = [sp.Rational(1, 4)] * 4
    # Complete centered generator on S^1: a_ij=w_j for i != j.
    rates = sp.Matrix(4, 4, lambda i, j: weights[j] if i != j else 0)
    return p1a.Fixture(f"nearly-singular-antipodal-pairs-n{n}", vertices, weights, rates)


def disconnected_equality_fixture() -> p1a.Fixture:
    """Two disconnected antipodal components in S^1.

    Connectivity is deliberately absent.  Each component has the unique rate
    that realizes L Omega=-Omega, and the sharp product equality still holds.
    """

    e1, e2 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
    vertices = [e1, -e1, e2, -e2]
    weights = [sp.Rational(1, 4)] * 4
    rates = sp.zeros(4)
    rates[0, 1] = rates[1, 0] = sp.Rational(1, 2)
    rates[2, 3] = rates[3, 2] = sp.Rational(1, 2)
    return p1a.Fixture("disconnected-antipodal-equality", vertices, weights, rates)


def exact_rademacher_average(
    sampling: sp.Matrix, residual: sp.Matrix, weights: list[sp.Expr]
) -> tuple[sp.Expr, sp.Expr]:
    """Average weighted energies over every Rademacher coefficient vector."""

    m = sampling.cols
    W = sp.diag(*weights)
    sample_total = sp.S.Zero
    residual_total = sp.S.Zero
    count = sp.Integer(2) ** m
    for signs in product((-1, 1), repeat=m):
        x = sp.Matrix(signs)
        sample_total += (x.T * sampling.T * W * sampling * x)[0]
        residual_total += (x.T * residual.T * W * residual * x)[0]
    return clean(sample_total / count), clean(residual_total / count)


def audit_p1b_fixture(fixture: p1a.Fixture) -> dict[str, object]:
    base = p1a.audit_fixture(fixture)
    vertices, weights, rates = fixture.vertices, fixture.weights, fixture.rates
    n, d = len(vertices), vertices[0].rows
    basis = sym0_basis(d)
    m = len(basis)
    W = sp.diag(*weights)
    L = generator_from_rates(rates)
    sampling = sp.Matrix(
        n,
        m,
        lambda i, p: clean((vertices[i].T * basis[p] * vertices[i])[0]),
    )
    residual = ((L + 2 * d * sp.eye(n)) * sampling).applyfunc(clean)
    gram_s = (sampling.T * W * sampling).applyfunc(clean)
    gram_r = (residual.T * W * residual).applyfunc(clean)

    assert_zero(sum(weights) - 1, f"{fixture.name}: normalized weights")
    assert_zero(sp.trace(gram_s) - sp.Rational(d - 1, d),
                f"{fixture.name}: sampling trace")

    identity = sp.eye(d)
    epsilons: list[sp.Expr] = []
    b_norms: list[sp.Expr] = []
    row_rates: list[sp.Expr] = []
    variances: list[sp.Expr] = []
    z_rows: list[sp.Matrix] = []
    m_rows: list[sp.Matrix] = []

    for i, omega in enumerate(vertices):
        r_i = clean(sum(rates[i, j] for j in range(n) if j != i))
        if r_i.is_positive is not True:
            raise AssertionError(f"{fixture.name}: row rate {i} not positive: {r_i}")
        row_rates.append(r_i)
        losses = [clean(1 - (omega.T * vertices[j])[0]) for j in range(n)]
        covariance = sp.zeros(d)
        for j in range(n):
            if i != j:
                delta = vertices[j] - omega
                covariance += rates[i, j] * delta * delta.T
        covariance = covariance.applyfunc(clean)
        epsilon = clean(sum(
            rates[i, j] * losses[j] ** 2 for j in range(n) if j != i
        ))
        variance = clean(sum(
            rates[i, j]
            * (losses[j] - sp.Rational(d - 1, 1) / r_i) ** 2
            for j in range(n) if j != i
        ))
        z = (omega * omega.T - identity / sp.Integer(d)).applyfunc(clean)
        unprojected = covariance + 2 * omega * omega.T
        matrix_m = (
            unprojected - sp.trace(unprojected) * identity / sp.Integer(d)
        ).applyfunc(clean)
        matrix_b = (
            matrix_m - sp.Rational(d, d - 1) * epsilon * z
        ).applyfunc(clean)
        epsilons.append(epsilon)
        variances.append(variance)
        b_norms.append(clean(p1a.frobenius(matrix_b, matrix_b)))
        z_rows.append(z)
        m_rows.append(matrix_m)

    energy_epsilon = clean(sum(
        weights[i] * epsilons[i] ** 2 for i in range(n)
    ))
    energy_b = clean(sum(weights[i] * b_norms[i] for i in range(n)))
    trace_r_expected = clean(
        sp.Rational(d, d - 1) * energy_epsilon + energy_b
    )
    assert_zero(sp.trace(gram_r) - trace_r_expected,
                f"{fixture.name}: residual two-defect trace")

    complement = gram_s.columnspace()
    if not complement:
        raise AssertionError(f"{fixture.name}: impossible zero sampling rank")
    lift = sp.Matrix.hstack(*complement)
    reduced_s = (lift.T * gram_s * lift).applyfunc(clean)
    reduced_r = (lift.T * gram_r * lift).applyfunc(clean)
    if clean(reduced_s.det()) == 0:
        raise AssertionError(f"{fixture.name}: singular deflated Gram")
    generalized = (reduced_s.inv() * reduced_r).applyfunc(clean)
    eigenvalues: list[sp.Expr] = []
    for value, multiplicity in generalized.eigenvals().items():
        eigenvalues.extend([clean(value)] * multiplicity)
    defect_sq = p1a.exact_max(
        eigenvalues, f"{fixture.name}: quotient maximum", require_nonnegative=True
    )
    defect = clean(sp.sqrt(defect_sq))

    strong_rhs = clean(
        sp.Rational(d * d, (d - 1) ** 2) * energy_epsilon
        + sp.Rational(d, d - 1) * energy_b
    )
    trace_ratio = clean(sp.trace(gram_r) / sp.trace(gram_s))
    assert_zero(strong_rhs - trace_ratio,
                f"{fixture.name}: exact strong coefficient")
    assert_nonnegative(defect_sq - strong_rhs,
                       f"{fixture.name}: strong two-defect bound")

    radial_rhs_sq = clean(
        sp.Rational(d * d, (d - 1) ** 2) * energy_epsilon
    )
    assert_nonnegative(defect_sq - radial_rhs_sq,
                       f"{fixture.name}: radial defect bound")

    rmax = p1a.exact_max(row_rates, f"{fixture.name}: rmax", require_nonnegative=True)
    epsilon_floor = clean(sp.Rational((d - 1) ** 4, 1) / rmax ** 2)
    assert_nonnegative(energy_epsilon - epsilon_floor,
                       f"{fixture.name}: epsilon RMS floor")
    product_gap = clean(defect * rmax - d * (d - 1))
    assert_nonnegative(product_gap, f"{fixture.name}: sharp product")

    trace_gap = clean(defect_sq - strong_rhs)
    generalized_saturated = all(clean(value - defect_sq) == 0 for value in eigenvalues)
    if (trace_gap == 0) != generalized_saturated:
        raise AssertionError(
            f"{fixture.name}: generalized trace equality mismatch: "
            f"gap={trace_gap}, spectrum={eigenvalues}"
        )
    radial_gap = clean(defect_sq - radial_rhs_sq)
    all_b_zero = all(value == 0 for value in b_norms)
    if (radial_gap == 0) != (generalized_saturated and all_b_zero):
        raise AssertionError(
            f"{fixture.name}: radial equality mismatch: {radial_gap}, "
            f"sat={generalized_saturated}, B={b_norms}"
        )

    rms_gap = clean(energy_epsilon - epsilon_floor)
    rate_variance_equal = all(
        clean(row_rates[i] - rmax) == 0 and variances[i] == 0
        for i in range(n)
    )
    if (rms_gap == 0) != rate_variance_equal:
        raise AssertionError(
            f"{fixture.name}: RMS equality mismatch: {rms_gap}, "
            f"rates={row_rates}, variances={variances}"
        )

    final_equal = product_gap == 0
    local_equal = rate_variance_equal and all_b_zero
    if final_equal != local_equal:
        raise AssertionError(
            f"{fixture.name}: final equality mismatch: gap={product_gap}, "
            f"rates/variance={rate_variance_equal}, B={all_b_zero}"
        )

    cstar = clean(sp.Rational(d * (d - 1), 1) / rmax)
    scalar_rows = all(
        all(
            clean(m_rows[i][p, q] - cstar * z_rows[i][p, q]) == 0
            for p in range(d) for q in range(d)
        )
        for i in range(n)
    )
    scalar_map = residual == (cstar * sampling).applyfunc(clean)
    if final_equal != scalar_rows or final_equal != scalar_map:
        raise AssertionError(
            f"{fixture.name}: scalar residual equality mismatch: "
            f"final={final_equal}, rows={scalar_rows}, map={scalar_map}"
        )

    if m <= 6:
        sample_average, residual_average = exact_rademacher_average(
            sampling, residual, weights
        )
        assert_zero(sample_average - sp.trace(gram_s),
                    f"{fixture.name}: random sampling trace")
        assert_zero(residual_average - sp.trace(gram_r),
                    f"{fixture.name}: random residual trace")

    return {
        **base,
        "trace_gap": trace_gap,
        "radial_gap": radial_gap,
        "rms_gap": rms_gap,
        "product_gap": product_gap,
        "strong_rhs": strong_rhs,
        "defect_sq": defect_sq,
        "rmax": rmax,
        "final_equal": final_equal,
        "generalized_saturated": generalized_saturated,
        "gram_s_det": clean(gram_s.det()) if gram_s.rows == gram_s.cols else None,
    }


def mutation_tests(results: list[dict[str, object]]) -> None:
    both = next(row for row in results if row["name"] == "positive-cube-both-defects")
    if clean(both["strong_rhs"] - (
        sp.Rational(9, 4) * sp.Rational(25, 9)
        + sp.Rational(3, 2) * sp.Rational(1, 81)
    )) != 0:
        raise AssertionError("anisotropy coefficient mutation escaped")

    repeated = next(row for row in results if row["name"] == "weighted-repeated-alias")
    if repeated["trace_gap"] != 0 or repeated["final_equal"]:
        raise AssertionError(
            "trace saturation was incorrectly conflated with final equality"
        )

    near = [row for row in results if str(row["name"]).startswith("nearly-singular")]
    determinants = [clean(row["gram_s_det"]) for row in near]
    for determinant in determinants:
        if determinant.is_positive is not True:
            raise AssertionError(f"near-singular Gram not positive: {determinant}")
    for left, right in zip(determinants, determinants[1:]):
        if clean(left - right).is_positive is not True:
            raise AssertionError(
                f"near-singular determinants do not decrease: {left}, {right}"
            )
    if not all(row["final_equal"] for row in near):
        raise AssertionError("near-singular exact equality family lost sharpness")


def main() -> None:
    fixtures = (
        p1a.family_fixtures()
        + p1a.platonic_fixtures()
        + p1a.adversarial_fixtures()
        + [disconnected_equality_fixture()]
        + [nearly_singular_fixture(n) for n in (2, 10, 100, 1000)]
    )
    names = [fixture.name for fixture in fixtures]
    if len(fixtures) != 24 or len(set(names)) != 24:
        raise AssertionError(f"P1B fixture inventory changed: {names}")
    results = [audit_p1b_fixture(fixture) for fixture in fixtures]
    mutation_tests(results)
    equality_count = sum(bool(row["final_equal"]) for row in results)
    for row in results:
        print(
            "{name}: d={d} N={nodes} rank(S/R)={rank_s}/{rank_r} "
            "D2={defect} rmax={rmax} product-gap={product_gap} "
            "trace-gap={trace_gap} equality={final_equal}".format(**row)
        )
    print(f"fixtures={len(results)}")
    print(f"equality-fixtures={equality_count}")
    print("zero-sampling-rank under stated hypotheses: IMPOSSIBLE")
    print("strong two-defect coefficient audit: EXACT")
    print("weighted-normalization mutation: REJECTED")
    print("near-singular quotient audit: PASS")
    print("P1B sharp quadratic-defect audit: PASS")


if __name__ == "__main__":
    main()
