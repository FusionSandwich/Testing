from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from pure_math.acceleration import (
    complete_transport_audit,
    constrained_defect_correction,
    constrained_error_propagation_operator,
    constrained_low_inverse,
    defect_correction,
    error_propagation_operator,
    field_of_values_bound,
    iteration_count_bound,
    load_generators,
    preconditioned_gmres,
    shellwise_contraction,
    slow_subspace_report,
    spectral_equivalence_bound,
)
from pure_math.acceleration.audit import run_audit
from pure_math.acceleration.fixtures import commuting_shell_fixture
from pure_math.acceleration.transport import load_frozen_operator_data


@pytest.fixture(scope="module")
def transport_payload() -> dict[str, object]:
    return complete_transport_audit()


def test_exact_fixed_point_and_error_operator() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    e = error_propagation_operator(fixture.high, fixture.optimized_low)
    update = exact + np.linalg.solve(
        fixture.optimized_low, fixture.rhs - fixture.high @ exact
    )
    assert np.linalg.norm(update - exact) < 1e-13
    arbitrary = np.linspace(-0.2, 0.5, len(exact))
    next_error = (
        arbitrary
        + np.linalg.solve(
            fixture.optimized_low,
            fixture.rhs - fixture.high @ arbitrary,
        )
        - exact
    )
    assert np.linalg.norm(next_error - e @ (arbitrary - exact)) < 1e-12


def test_shellwise_formula_and_iteration_bound() -> None:
    fixture = commuting_shell_fixture()
    report = shellwise_contraction(fixture.shell_high, fixture.shell_optimized)
    assert np.allclose(report.factors, 1.0 - fixture.shell_high / fixture.shell_optimized)
    assert report.spectral_radius < 0.2
    count = iteration_count_bound(report.spectral_radius, 1.0, 1e-10)
    assert count > 0
    assert report.spectral_radius**count <= 1e-10
    with pytest.raises(ValueError):
        iteration_count_bound(1.0, 1.0, 1e-8)


def test_spd_spectral_equivalence_and_fov() -> None:
    fixture = commuting_shell_fixture()
    spectral = spectral_equivalence_bound(fixture.high, fixture.optimized_low)
    assert spectral.positive
    assert spectral.lower > 0.0
    assert spectral.upper >= spectral.lower
    fov = field_of_values_bound(fixture.high, fixture.optimized_low)
    assert fov.coercivity > 0.0
    assert fov.certified_contractive


def test_defect_correction_converges_and_profiles_setup() -> None:
    fixture = commuting_shell_fixture()
    result = defect_correction(
        fixture.high,
        fixture.rhs,
        fixture.optimized_low,
        rtol=1e-11,
        max_iterations=200,
    )
    assert result.converged
    assert result.low_solves == result.iterations
    assert result.setup_seconds >= 0.0
    assert result.solve_seconds >= 0.0
    assert result.preconditioner_bytes > 0
    assert np.linalg.norm(result.solution - np.linalg.solve(fixture.high, fixture.rhs)) < 1e-9


def test_constrained_correction_preserves_declared_conservation() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    q = np.ones((1, len(exact)))
    perturbation = np.arange(len(exact), dtype=float)
    perturbation -= np.mean(perturbation)
    initial = exact + 0.04 * perturbation
    inverse = constrained_low_inverse(fixture.optimized_low, q)
    assert np.linalg.norm(q @ inverse) < 1e-11
    e = constrained_error_propagation_operator(
        fixture.high, fixture.optimized_low, q
    )
    assert np.linalg.norm(q @ (np.eye(len(exact)) - e)) < 1e-11
    result = constrained_defect_correction(
        fixture.high,
        fixture.rhs,
        fixture.optimized_low,
        q,
        initial=initial,
        rtol=1e-11,
        max_iterations=400,
    )
    assert result.converged
    assert np.linalg.norm(q @ (result.solution - initial)) < 1e-10
    assert np.linalg.norm(result.solution - exact) < 1e-8


def test_constrained_correction_rejects_incompatible_initial_state() -> None:
    fixture = commuting_shell_fixture()
    q = np.ones((1, len(fixture.rhs)))
    with pytest.raises(ValueError, match="conservation-incompatible"):
        constrained_defect_correction(
            fixture.high,
            fixture.rhs,
            fixture.optimized_low,
            q,
            initial=np.zeros_like(fixture.rhs),
        )


def test_gmres_uses_low_operator_only_as_preconditioner() -> None:
    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    for low in (
        None,
        fixture.optimized_low,
        fixture.baseline_low,
        fixture.classical_low,
        fixture.poor_low,
    ):
        result = preconditioned_gmres(
            fixture.high,
            fixture.rhs,
            low_order=low,
            rtol=1e-11,
            restart=4,
            max_iterations=100,
        )
        assert result.converged
        assert np.linalg.norm(result.solution - exact) < 1e-9
        if low is None:
            assert result.low_solves == 0
            assert result.preconditioner_bytes == 0
        else:
            assert result.low_solves > 0
            assert result.preconditioner_bytes > 0


def test_slow_subspace_audit_detects_relevant_contraction() -> None:
    fixture = commuting_shell_fixture()
    basis = np.eye(len(fixture.high))[:, 2:4]
    report = slow_subspace_report(
        fixture.high, fixture.optimized_low, basis
    )
    assert report.dimension == 2
    assert report.contraction_norm < 1.0
    assert report.invariance_leakage < 1e-13


def test_frozen_positive_generators_recompute_invariants() -> None:
    _, _, _, audits, payload = load_generators()
    assert len(payload["scientific_sha256"]) == 64
    for name in (
        "optimized_harmonic_fidelity",
        "moment_monotone_baseline",
        "h2_poor_positive",
    ):
        row = audits[name]
        assert row.positive
        assert row.h0_residual < 2e-10
        assert row.h1_residual < 2e-10
        assert row.reversibility_residual < 2e-10
    assert (
        audits["optimized_harmonic_fidelity"].shell_defects[2]
        < audits["moment_monotone_baseline"].shell_defects[2]
        < audits["h2_poor_positive"].shell_defects[2]
    )


def test_frozen_registry_hash_fails_closed(tmp_path: Path) -> None:
    source = Path(__file__).parents[1] / "acceleration" / "p2d_frozen_operators.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["weights"][0] += 1e-5
    target = tmp_path / "tampered.json"
    target.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ArithmeticError, match="hash mismatch"):
        load_frozen_operator_data(target)


def test_forward_peaked_sweep_has_all_comparators_and_metrics(
    transport_payload: dict[str, object],
) -> None:
    assert transport_payload["status"] == "PASS"
    sweep = transport_payload["forward_peaked_sweep"]
    assert len(sweep["rows"]) == 4
    expected = {
        "none",
        "optimized_harmonic_fidelity",
        "moment_monotone_baseline",
        "classical_modified_fp",
        "h2_poor_positive",
    }
    for row in sweep["rows"]:
        assert set(row["methods"]) == expected
        assert row["methods"]["optimized_harmonic_fidelity"]["iterations"] < row["methods"]["moment_monotone_baseline"]["iterations"]
        assert row["methods"]["optimized_harmonic_fidelity"]["iterations"] < row["methods"]["none"]["iterations"]
        for method in row["methods"].values():
            assert method["converged"]
            assert method["high_order_matvecs"] > 0
            assert method["setup_seconds"] >= 0.0
            assert method["solve_seconds"] >= 0.0
            assert method["python_peak_bytes"] > 0
            assert method["matrix_bytes"] > 0
    assert sweep["summary"]["minimum_iteration_reduction_vs_baseline"] > 0.4


def test_signed_classical_comparator_is_not_promoted(
    transport_payload: dict[str, object],
) -> None:
    sweep = transport_payload["forward_peaked_sweep"]
    assert sweep["summary"]["signed_classical_comparator_is_not_production_eligible"]
    for row in sweep["rows"]:
        assert row["methods"]["classical_modified_fp"]["positivity_expected"] is False


def test_higher_shell_and_ray_adversaries_are_explicit(
    transport_payload: dict[str, object],
) -> None:
    higher = transport_payload["higher_shell_adversary"]
    assert higher["sampled_degree"] == 7
    assert higher["h2_metric_is_controller"] is False
    assert higher["classical_spectral_fp_degree_seven_mismatch"] == 0.0
    ray = transport_payload["ray_dominated_adversary"]
    assert ray["relative_ray_error"] > 1.0
    assert ray["low_operator_can_change_converged_high_order_ray_error"] is False


def test_streaming_energy_boundary_dependence_is_audited(
    transport_payload: dict[str, object],
) -> None:
    decomposition = transport_payload["forward_peaked_sweep"]["mismatch_decomposition"]
    assert decomposition["decomposition_residual"] < 1e-10
    assert decomposition["streaming_mismatch_norm"] == 0.0
    assert decomposition["energy_mismatch_norm"] == 0.0
    assert decomposition["boundary_mismatch_norm"] == 0.0
    multigroup = transport_payload["multigroup_boundary_case"]
    assert multigroup["performance"]["converged"]
    assert multigroup["group_coupling_norm"] > 0.0
    assert multigroup["boundary_block_norm"] > 0.0
    assert multigroup["full_blocks_retained_in_low_operator"] is True


def test_executable_audit() -> None:
    result = run_audit()
    assert result["status"] == "PASS"
    assert result["fixed_point_preserved"] is True
    assert result["conservation_constraint_preserved"] is True
    assert len(result["rows"]) == 4
    assert result["checks"]["higher_shell_failure_exposed"] is True
    assert result["checks"]["forward_peaked_optimized_beats_baseline"] is True
    assert result["checks"]["ray_error_dominates"] is True
