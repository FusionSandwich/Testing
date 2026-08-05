"""Focused P2B harmonic-defect dynamics and transport regressions."""

from __future__ import annotations

import numpy as np
import pytest

from pure_math.dynamics.audit import run_numeric_audit
from pure_math.dynamics.bounds import (
    RESIDUAL_COMPONENTS,
    ResidualLedger,
    iteration_error_bound,
    preconditioned_bound,
)
from pure_math.dynamics.core import (
    band_sampling_guard,
    physical_symmetrizer_dissipativity,
    resolvent_shell_error,
    semigroup_shell_error,
    shell_residual,
    validate_reversible_generator,
)
from pure_math.dynamics.exact_audit import run_exact_audit
from pure_math.dynamics.manufactured import (
    multigroup_manufactured_fixture,
    spatial_manufactured_fixture,
    tetrahedron_h1_exact_fixture,
    two_node_alias_fixture,
    two_node_defect_fixture,
)


def test_two_node_exact_transient_resolvent_and_effectivities() -> None:
    fixture = two_node_defect_fixture()
    time = 0.4
    transient = fixture.transient(time)
    exact_transient = np.exp(-2.0 * time) - np.exp(-6.0 * time)
    assert abs(transient.error - exact_transient) < 2e-14
    assert abs(transient.residual_norm - 4.0) < 2e-14
    assert abs(transient.bound - 4.0 * (1.0 - np.exp(-6.0 * time)) / 6.0) < 2e-14
    assert abs(transient.effectivity - transient.bound / exact_transient) < 2e-14

    alpha = 1.25
    resolvent = fixture.resolvent(alpha)
    exact_resolvent = 4.0 / ((alpha + 2.0) * (alpha + 6.0))
    assert abs(resolvent.error - exact_resolvent) < 2e-14
    assert abs(resolvent.bound - 4.0 / (alpha * (alpha + 6.0))) < 2e-14
    assert abs(resolvent.effectivity - (alpha + 2.0) / alpha) < 2e-14


def test_degree_zero_constant_shell_is_exact() -> None:
    fixture = two_node_defect_fixture()
    constant = np.ones((len(fixture.weights), 1)) / np.sqrt(np.sum(fixture.weights))
    shell = shell_residual(fixture.generator, fixture.weights, constant, 0.0)
    transient = semigroup_shell_error(
        fixture.generator, fixture.weights, constant, 0.0, 0.7
    )
    resolvent = resolvent_shell_error(
        fixture.generator, fixture.weights, constant, 0.0, 1.25
    )
    assert shell.defect < 1e-14
    assert transient.error_operator_norm < 1e-14
    assert transient.bound < 1e-14
    assert resolvent.error_operator_norm < 1e-14
    assert resolvent.bound < 1e-14
    with pytest.raises(ValueError, match="nonnegative"):
        shell_residual(fixture.generator, fixture.weights, constant, -1.0)


def test_sharp_sampling_alias_and_h1_exact_tetrahedron() -> None:
    time = 0.4
    alias = two_node_alias_fixture()
    assert alias.nodes is not None
    quadratic = np.diag([1.0, 0.0, -1.0])
    assert np.allclose(
        np.einsum("ni,ij,nj->n", alias.nodes, quadratic, alias.nodes), alias.mode
    )
    alias_report = alias.transient(time)
    exact_alias_error = 0.5 * (1.0 - np.exp(-6.0 * time))
    assert alias_report.residual_norm == pytest.approx(3.0)
    assert alias_report.error == pytest.approx(exact_alias_error)
    assert alias_report.bound == pytest.approx(exact_alias_error)
    assert alias_report.effectivity == pytest.approx(1.0)
    alias_resolvent = alias.resolvent(1.25)
    assert alias_resolvent.error == pytest.approx(alias_resolvent.bound)
    assert alias_resolvent.effectivity == pytest.approx(1.0)

    tetra = tetrahedron_h1_exact_fixture()
    assert tetra.nodes is not None
    validate_reversible_generator(tetra.generator, tetra.weights)
    assert np.linalg.norm(tetra.generator @ tetra.nodes + 2.0 * tetra.nodes) < 2e-14
    tetra_quadratic = np.zeros((3, 3))
    tetra_quadratic[0, 1] = tetra_quadratic[1, 0] = 3.0 * np.sqrt(2.0) / 4.0
    tetra_quadratic[0, 2] = tetra_quadratic[2, 0] = 3.0 * np.sqrt(2.0) / 4.0
    assert np.trace(tetra_quadratic) == 0.0
    assert np.allclose(
        np.einsum("ni,ij,nj->n", tetra.nodes, tetra_quadratic, tetra.nodes),
        tetra.mode,
    )
    assert np.linalg.norm(tetra.generator @ tetra.mode + 2.0 * tetra.mode) < 2e-14
    tetra_transient = tetra.transient(time)
    assert tetra_transient.residual_norm == pytest.approx(4.0)
    assert tetra_transient.error == pytest.approx(np.exp(-2.0 * time) - np.exp(-6.0 * time))
    alpha = 1.25
    tetra_resolvent = tetra.resolvent(alpha)
    assert tetra_resolvent.error == pytest.approx(4.0 / ((alpha + 2.0) * (alpha + 6.0)))
    assert tetra_resolvent.effectivity == pytest.approx((alpha + 2.0) / alpha)


def test_full_output_shell_residual_keeps_leakage() -> None:
    weights = np.asarray([0.2, 0.3, 0.5])
    conductance = np.asarray(
        [[0.0, 0.1, 0.1], [0.1, 0.0, 0.15], [0.1, 0.15, 0.0]]
    )
    generator = conductance / weights[:, None]
    np.fill_diagonal(generator, -np.sum(generator, axis=1))
    raw = np.asarray([[1.0], [-0.5], [-0.1]])
    frame = raw / np.sqrt((raw.T @ (weights[:, None] * raw)).item())
    shell = shell_residual(generator, weights, frame, 6.0)
    compressed = frame.T @ (weights[:, None] * shell.residual)
    assert shell.residual.shape == (3, 1)
    assert np.linalg.norm(shell.residual - frame @ compressed, 2) > 1e-3
    assert shell.defect > float(np.linalg.norm(compressed, 2))
    transient = semigroup_shell_error(generator, weights, frame, 6.0, 0.25)
    resolvent = resolvent_shell_error(generator, weights, frame, 6.0, 1.5)
    assert transient.error_matrix.shape == (3, 1)
    assert resolvent.error_matrix.shape == (3, 1)
    assert transient.error_operator_norm <= transient.bound + 2e-14
    assert resolvent.error_operator_norm <= resolvent.bound + 2e-14


def test_band_guard_detects_cross_shell_alias_and_ambiguity() -> None:
    weights = np.full(3, 1.0 / 3.0)
    shell0 = np.ones((3, 1))
    shell1 = np.asarray([[1.0], [0.0], [-1.0]])
    report = band_sampling_guard({0: shell0, 1: shell1}, weights)
    assert report.rank == 2 and report.inverse_stability > 0.0
    with pytest.raises(ValueError, match="injective"):
        band_sampling_guard({0: shell0, 1: shell0.copy()}, weights)
    nearly_aliased = shell0 + 2e-10 * shell1
    with pytest.raises(ValueError, match="ambiguous"):
        band_sampling_guard(
            {0: shell0, 1: nearly_aliased},
            weights,
            minimum_singular_value=1e-11,
            ambiguity_factor=100.0,
        )


def test_physical_symmetrizer_and_fail_closed_inputs() -> None:
    fixture = two_node_defect_fixture()
    report = physical_symmetrizer_dissipativity(
        fixture.generator,
        np.diag(fixture.weights),
        reference_metric=np.diag(fixture.weights),
    )
    assert report.dissipative and abs(report.norm_equivalence_factor - 1.0) < 1e-14
    unequal_weights = np.array([0.25, 0.75])
    unequal_metric = np.diag(unequal_weights)
    unequal_generator = np.array([[-1.0, 1.0], [1.0 / 3.0, -1.0 / 3.0]])
    relative = physical_symmetrizer_dissipativity(
        unequal_generator,
        2.0 * unequal_metric,
        reference_metric=unequal_metric,
    )
    assert abs(relative.minimum_symmetrizer_eigenvalue - 2.0) < 1e-14
    assert abs(relative.maximum_symmetrizer_eigenvalue - 2.0) < 1e-14
    assert abs(relative.norm_equivalence_factor - 1.0) < 1e-14
    with pytest.raises(ValueError):
        validate_reversible_generator(fixture.generator, [0.5, 0.0])
    with pytest.raises(ValueError):
        validate_reversible_generator([[np.nan, 0.0], [0.0, 0.0]], [0.5, 0.5])
    with pytest.raises(ValueError):
        validate_reversible_generator([[0.0, -1.0], [0.0, 0.0]], [0.5, 0.5])
    with pytest.raises(ValueError):
        physical_symmetrizer_dissipativity(np.eye(2), np.eye(2))
    with pytest.raises(ValueError):
        physical_symmetrizer_dissipativity(
            np.array([[-1.0, 1.0], [1.0, -1.0]]),
            np.diag([1.0, 100.0]),
            reference_metric=np.eye(2),
        )


def test_exact_noncommuting_spatial_fixture_and_adjoint_estimator() -> None:
    fixture = spatial_manufactured_fixture()
    assert np.linalg.matrix_rank(fixture.commutator) == 4
    assert np.allclose(fixture.source, [0.0, 2.0, 3.0, 10.0])
    assert np.allclose(fixture.computed_solution, [7.0 / 9.0, 7.0 / 3.0, 8.0 / 3.0, 38.0 / 9.0])
    assert np.allclose(fixture.error, [2.0 / 9.0, -1.0 / 3.0, 1.0 / 3.0, -2.0 / 9.0])
    assert np.allclose(
        fixture.residual,
        [14.0 / 9.0, -14.0 / 9.0, 14.0 / 9.0, -14.0 / 9.0],
    )
    assert np.allclose(fixture.comparator_residual, [1.0, -1.0, 1.0, -1.0])
    assert (
        np.linalg.norm(fixture.reference_operator @ fixture.error - fixture.residual)
        < 2e-14
    )
    assert (
        np.linalg.norm(
            fixture.discrete_operator @ fixture.error - fixture.comparator_residual
        )
        < 2e-14
    )
    symmetric_eigenvalues = np.linalg.eigvalsh(
        0.5 * (fixture.reference_operator + fixture.reference_operator.T)
    )
    assert np.allclose(symmetric_eigenvalues, [1.5, 2.5, 5.5, 6.5])
    assert fixture.ledger.component_norms["angular_generator"] == pytest.approx(28.0 / 9.0)
    assert all(
        fixture.ledger.component_norms[name] == 0.0
        for name in RESIDUAL_COMPONENTS
        if name != "angular_generator"
    )
    assert fixture.coercivity == 1.5
    assert fixture.exact_error**2 == pytest.approx(26.0 / 81.0)
    assert fixture.coercive_bound == pytest.approx(56.0 / 27.0)
    assert fixture.effectivity == pytest.approx(28.0 * np.sqrt(26.0) / 39.0)
    assert fixture.response_error == pytest.approx(5.0 / 3.0)
    assert fixture.response_estimator == pytest.approx(fixture.response_error)
    assert np.allclose(
        fixture.adjoint,
        [19.0 / 70.0, -4.0 / 35.0, 11.0 / 35.0, -13.0 / 35.0],
    )
    assert np.allclose(
        fixture.comparator_adjoint,
        [3.0 / 7.0, -4.0 / 21.0, 10.0 / 21.0, -4.0 / 7.0],
    )
    response_ledger = fixture.ledger.response_estimate(fixture.adjoint)
    assert response_ledger["total"] == pytest.approx(fixture.response_error)


def test_six_term_ledger_and_preconditioned_iteration_bounds() -> None:
    components = {
        name: np.asarray([index + 1.0, -(index + 0.5)])
        for index, name in enumerate(RESIDUAL_COMPONENTS)
    }
    ledger = ResidualLedger.build(components, [2.0, 1.0])
    assert np.allclose(ledger.total, sum(components.values()))
    assert ledger.total_norm <= ledger.triangle_norm + 1e-14
    with pytest.raises(ValueError, match="keys mismatch"):
        ResidualLedger.build({"iteration": np.ones(2)})

    fixture = spatial_manufactured_fixture()
    diagonal = np.diag(np.diag(fixture.discrete_operator))
    certificate = preconditioned_bound(
        fixture.discrete_operator, diagonal, fixture.comparator_residual
    )
    assert certificate.contraction == pytest.approx(2.0 / 3.0)
    assert fixture.exact_error <= certificate.residual_error_bound + 1e-14
    assert np.linalg.norm(np.linalg.inv(fixture.discrete_operator), 2) <= (
        certificate.inverse_bound + 1e-14
    )
    assert iteration_error_bound(certificate.contraction, 5, 1.0) == pytest.approx((2.0 / 3.0) ** 5)
    with pytest.raises(ValueError, match="strictly below one"):
        preconditioned_bound(np.asarray([[2.0]]), np.asarray([[1.0]]), np.ones(1))


def test_exact_two_group_angular_and_transfer_mutations() -> None:
    fixture = multigroup_manufactured_fixture()
    assert np.allclose(fixture.discrete_amplitude, [1.0 / 8.0, 3.0 / 16.0])
    assert np.allclose(fixture.target_amplitude, [1.0 / 32.0, 7.0 / 96.0])
    assert np.allclose(fixture.angular_error, [3.0 / 32.0, 11.0 / 96.0])
    assert fixture.low_group_response_error == pytest.approx(11.0 / 96.0)
    # [G,D]_hg = G_hg(D_gg-D_hh), with D=-eta*diag(kappa).
    transfer = np.asarray([[-1.0, 0.0], [1.0, 0.0]])
    diffusion = -np.diag([2.0, 1.0])
    expected = np.asarray(
        [
            [transfer[row, column] * (diffusion[column, column] - diffusion[row, row])
             for column in range(2)]
            for row in range(2)
        ]
    )
    assert np.array_equal(fixture.commutator, expected)
    assert np.linalg.matrix_rank(fixture.commutator) == 1
    assert np.array_equal(fixture.equal_kappa_commutator, np.zeros((2, 2)))
    assert np.allclose(fixture.changed_rate_amplitude, [1.0 / 16.0, 7.0 / 24.0])
    assert np.allclose(fixture.group_rate_error, [-1.0 / 16.0, 5.0 / 48.0])


def test_symbolic_and_numeric_audits_agree() -> None:
    exact = run_exact_audit()
    numeric = run_numeric_audit()
    assert exact["error_squared"] == "26/81"
    assert exact["response"] == "5/3"
    assert exact["commutator_rank"] == "4"
    assert numeric["response_error"] == pytest.approx(numeric["response_estimator"])
    assert numeric["preconditioned_contraction"] == pytest.approx(2.0 / 3.0)
    assert numeric["sharp_alias_effectivity"] == pytest.approx(1.0)
    assert numeric["low_group_response_error"] == pytest.approx(11.0 / 96.0)
    assert numeric["multigroup_commutator_norm"] > 0.0
    assert numeric["equal_kappa_commutator_norm"] == 0.0
