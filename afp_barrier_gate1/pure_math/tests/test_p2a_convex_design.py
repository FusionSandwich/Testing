"""P2A convex-design regressions (CVXPY 1.7.3 / SciPy 1.16.1 API floor)."""

from __future__ import annotations

import numpy as np
import pytest

from pure_math.optimization.audit import (
    certificate_and_failure_audit,
    conditioning_and_cost_audit,
    formulation_audit,
    octa_reconstruction,
)
from pure_math.optimization.fixtures import (
    ambiguous_rank_fixture,
    declared_rank_truncation_mutation,
    dynamic_weight_ill_conditioned_fixture,
    locally_feasible_globally_infeasible_square,
    octahedron_fixture,
    tetrahedron_fixture,
    four_node_antipodal_preference,
)
from pure_math.optimization.model import (
    AmbiguousSamplingRank,
    DesignModel,
    RankPolicy,
    degree_two_basis,
)
from pure_math.optimization.programs import (
    DesignRequest,
    ResponseTerm,
    SolverConfig,
    classify_request_cone,
    prune_and_reoptimize,
    solve_design,
)


def test_degree_two_basis_is_frobenius_orthonormal_tracefree() -> None:
    basis = degree_two_basis()
    assert basis.shape == (5, 3, 3)
    assert np.max(np.abs(np.trace(basis, axis1=1, axis2=2))) < 1e-15
    gram = np.asarray([[np.sum(left * right) for right in basis] for left in basis])
    assert np.max(np.abs(gram - np.eye(5))) < 1e-15


def test_exact_alias_certificates_tetra_and_octa() -> None:
    tetra, _, tetra_certificate = tetrahedron_fixture()
    octa, _, octa_certificate = octahedron_fixture()
    assert (tetra_certificate.rank, len(tetra_certificate.nullspace)) == (3, 2)
    assert (octa_certificate.rank, len(octa_certificate.nullspace)) == (2, 3)
    assert tetra.shell(2).shell.exact_rank_certified
    assert octa.shell(2).shell.exact_rank_certified
    assert tetra.condition_report()["shells"][2]["orthonormality_error"] < 1e-14
    assert octa.condition_report()["shells"][2]["orthonormality_error"] < 1e-14


def test_affine_quotient_matches_direct_normalized_generator() -> None:
    model, gamma, _ = tetrahedron_fixture()
    shell = model.shell(2).shell
    direct = model.graph.symmetric_generator(gamma) @ shell.quotient_frame + 6.0 * shell.quotient_frame
    assert np.max(np.abs(model.residual(gamma) - direct)) < 2e-14
    assert abs(model.defect(gamma) - 4.0) < 2e-14
    physical = model.shell(2).shell.raw_samples[:, 2]
    unit_mode = model.shell(2).shell.quotient_mode_from_samples(model.graph, physical)
    tiny_mode = model.shell(2).shell.quotient_mode_from_samples(model.graph, 1e-12 * physical)
    subnormal_mode = model.shell(2).shell.quotient_mode_from_samples(model.graph, 1e-200 * physical)
    assert np.max(np.abs(unit_mode - tiny_mode)) < 1e-14
    assert np.max(np.abs(unit_mode - subnormal_mode)) < 1e-14


def test_full_output_residual_detects_leakage_lost_by_compression() -> None:
    # Unequal masses destroy invariance of the sampled H2 range.  The full
    # residual has a substantial component orthogonal to that input range;
    # U.T @ T is therefore a provably smaller, invalid compressed defect.
    model, gamma = dynamic_weight_ill_conditioned_fixture(0.1)
    frame = model.shell(2).shell.quotient_frame
    residual = model.residual(gamma)
    leakage = (np.eye(model.graph.node_count) - frame @ frame.T) @ residual
    full_norm = float(np.linalg.norm(residual, 2))
    compressed_norm = float(np.linalg.norm(frame.T @ residual, 2))
    assert np.linalg.norm(leakage, 2) > 0.9
    assert full_norm - compressed_norm > 0.08


def test_declared_rank_and_ambiguous_rank_fail_closed() -> None:
    with pytest.raises(AmbiguousSamplingRank):
        DesignModel.build(ambiguous_rank_fixture())
    with pytest.raises(AmbiguousSamplingRank):
        declared_rank_truncation_mutation()
    graph = tetrahedron_fixture()[0].graph
    # A separated declared rank is allowed but is still labeled declared,
    # never exact.
    model = DesignModel.build(graph, rank_policies={2: RankPolicy(declared_rank=3)})
    assert model.shell(2).shell.rank_declared
    assert not model.shell(2).shell.exact_rank_certified


def test_all_seven_formulations_and_duals_clarabel() -> None:
    record = formulation_audit("CLARABEL")
    cones = {row["cone"] for row in record["programs"]}
    assert {"SDP", "SOCP", "QP", "LP"} <= cones
    assert len(record["programs"]) >= 12


def test_primal_cone_slacks_are_reconstructed() -> None:
    model, _, _ = tetrahedron_fixture()
    spectral = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL")
    )
    rank = model.shell(2).shell.rank
    selected = solve_design(
        model,
        DesignRequest.minimax_modes(1.5, np.eye(rank)),
        SolverConfig("CLARABEL"),
    )
    assert spectral.verification.passed and selected.verification.passed
    assert spectral.verification.metrics["primal_psd_block_count"] == 1
    assert spectral.verification.metrics["primal_psd_min_eigenvalue"] > -5e-6
    assert selected.verification.metrics["primal_soc_block_count"] == rank
    assert selected.verification.metrics["primal_soc_min_margin"] > -5e-6


def test_rate_cap_verification_is_in_directed_rate_units() -> None:
    from pure_math.optimization.certificates import VerificationTolerance, _primal_report

    model, exact_gamma = dynamic_weight_ill_conditioned_fixture()
    # Compile once to obtain the frozen affine/cone handles, then replace the
    # inaccurate solver candidate by an analytically exact dense generator.
    candidate = solve_design(
        model, DesignRequest.minimum_defect(2.0), SolverConfig("CLARABEL"),
        verify=False,
    )
    mutated = exact_gamma.copy()
    mutated[0] += 1e-10
    candidate.gamma = mutated
    candidate.epigraph = 10.0
    candidate.objective = model.defect(mutated)
    raw_excess = np.max(
        model.graph.endpoint_incidence @ mutated - 2.0 * model.graph.weights
    )
    assert 0.0 < raw_excess < 3e-6  # the rejected, mass-unscaled old check
    passed, metrics, failures = _primal_report(
        model, candidate, VerificationTolerance()
    )
    assert not passed
    assert metrics["rate_violation"] > 100.0
    assert "rate cap" in failures


def test_public_result_verifier_rejects_nonfinite_fields() -> None:
    from pure_math.optimization.certificates import verify_result

    model, _, _ = tetrahedron_fixture()
    result = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL"),
        verify=False,
    )
    result.gamma = np.full(model.graph.edge_count, np.nan)
    report = verify_result(model, result)
    assert not report.passed
    assert "nonfinite or malformed primal conductance" in report.failures


def test_scalar_lp_verifier_rejects_negative_dual_cancellation() -> None:
    from pure_math.optimization.certificates import verify_result

    model, _, _ = tetrahedron_fixture()
    rank = model.shell(2).shell.rank
    term = ResponseTerm.build(
        2, np.asarray([[1.0, 0.0, 0.0, 0.0]]),
        np.eye(rank)[:, :1], np.zeros((1, 1)),
    )
    result = solve_design(
        model,
        DesignRequest.response_weighted(
            1.5, [term, term], metric="scalar_max"
        ),
        SolverConfig("CLARABEL"),
        verify=False,
    )
    # Identical affine rows let this signed shift preserve every aggregate
    # stationarity/normalization equation.  Only the componentwise dual-cone
    # check can reject it.
    result.duals["upper"][0] = np.asarray(result.duals["upper"][0]) - 2.0
    result.duals["upper"][1] = np.asarray(result.duals["upper"][1]) + 2.0
    report = verify_result(model, result)
    assert not report.passed
    assert "LP dual cone" in report.failures


def test_psd_verifier_rejects_skew_dual_mutation() -> None:
    from pure_math.optimization.certificates import verify_result

    model, _, _ = tetrahedron_fixture()
    result = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL"),
        verify=False,
    )
    result.duals["psd"][0][0, 1] += 100.0
    result.duals["psd"][0][1, 0] -= 100.0
    report = verify_result(model, result)
    assert not report.passed
    assert "PSD dual symmetry" in report.failures


def test_result_verifier_binds_declared_request_and_dual_shapes() -> None:
    from pure_math.optimization.certificates import verify_result

    model, _, _ = tetrahedron_fixture()
    relabeled = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL"),
        verify=False,
    )
    relabeled.request = DesignRequest.minimum_defect(0.1)
    report = verify_result(model, relabeled)
    assert not report.passed
    assert "fixed-rate binding mismatch" in report.failures

    malformed = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL"),
        verify=False,
    )
    malformed.duals["positivity"] = np.zeros(model.graph.edge_count - 1)
    report = verify_result(model, malformed)
    assert not report.passed
    assert any("malformed primal/dual data" in item for item in report.failures)

    malformed_psd = solve_design(
        model, DesignRequest.minimum_defect(1.5), SolverConfig("CLARABEL"),
        verify=False,
    )
    malformed_psd.duals["psd"] = [np.eye(3)]
    report = verify_result(model, malformed_psd)
    assert not report.passed
    assert any("malformed primal/dual data" in item for item in report.failures)


def test_result_verifier_binds_response_targets_and_weights() -> None:
    from pure_math.optimization.certificates import verify_result

    model, _, _ = tetrahedron_fixture()
    rank = model.shell(2).shell.rank
    zero = ResponseTerm.build(
        2, np.eye(model.graph.node_count), np.eye(rank),
        np.zeros((model.graph.node_count, rank)), weight=1.0,
    )
    result = solve_design(
        model,
        DesignRequest.response_weighted(1.5, [zero], metric="frobenius"),
        SolverConfig("CLARABEL"), verify=False,
    )
    changed = ResponseTerm.build(
        2, np.eye(model.graph.node_count), np.eye(rank),
        np.full((model.graph.node_count, rank), 1000.0), weight=999.0,
    )
    result.request = DesignRequest.response_weighted(
        1.5, [changed], metric="frobenius"
    )
    assert not verify_result(model, result).passed


def test_response_affine_target_is_not_dropped() -> None:
    model, _, _ = tetrahedron_fixture()
    rank = model.shell(2).shell.rank
    term_zero = ResponseTerm.build(2, np.eye(4), np.eye(rank), np.zeros((4, rank)))
    term_target = ResponseTerm.build(2, np.eye(4), np.eye(rank), np.full((4, rank), 0.25))
    zero = solve_design(
        model, DesignRequest.response_weighted(1.5, [term_zero], metric="frobenius"),
        SolverConfig("CLARABEL"),
    )
    target = solve_design(
        model, DesignRequest.response_weighted(1.5, [term_target], metric="frobenius"),
        SolverConfig("CLARABEL"),
    )
    assert zero.verification.passed and target.verification.passed
    assert abs(float(zero.objective) - float(target.objective)) > 1e-3


def test_farkas_conic_pruning_and_mutations() -> None:
    record = certificate_and_failure_audit("CLARABEL")
    assert abs(record["conic_separation"] - 0.1) < 1e-12
    assert abs(record["square_farkas_work"] + 2.0 / 3.0) < 1e-12
    assert abs(record["cube_farkas_work"] + 0.4) < 1e-12
    assert record["prune_attempts"] == 6


def test_pruning_preserves_custom_sampling_quotient() -> None:
    base, _ = four_node_antipodal_preference(0.5)
    samples = np.asarray([[1.0], [-2.0], [3.0], [-4.0]])
    model = DesignModel.build(base.graph, sample_overrides={2: samples})
    frame = model.shell(2).shell.quotient_frame.copy()
    pruned = prune_and_reoptimize(
        model,
        DesignRequest.minimum_defect(2.0),
        SolverConfig("CLARABEL"),
        objective_absolute_allowance=10.0,
    )
    assert pruned.model.graph.edge_count < model.graph.edge_count
    assert pruned.model.shell(2).shell.rank == 1
    assert np.array_equal(pruned.model.shell(2).shell.quotient_frame, frame)


def test_pruning_remaps_edge_groups() -> None:
    model, _ = four_node_antipodal_preference(0.5)
    request = DesignRequest.frobenius_shell(
        2.0,
        edge_groups=((0, 1, 2), (3, 4, 5)),
        group_penalty_weight=0.2,
    )
    pruned = prune_and_reoptimize(
        model, request, SolverConfig("CLARABEL"),
        objective_absolute_allowance=100.0,
    )
    assert pruned.result.verification.passed
    assert pruned.model.graph.edge_count < model.graph.edge_count
    assert all(
        0 <= edge < pruned.model.graph.edge_count
        for group in pruned.result.request.edge_groups for edge in group
    )
    assert all(np.isfinite(attempt.candidate_score) for attempt in pruned.attempts)
    assert all(attempt.support_before for attempt in pruned.attempts)


def test_nonfinite_request_data_fail_before_compilation() -> None:
    model, _, _ = tetrahedron_fixture()
    rank = model.shell(2).shell.rank
    bad_requests = [
        DesignRequest.multi_shell(1.5, {2: np.nan}),
        DesignRequest.minimax_modes(1.5, np.full((rank, 1), np.nan)),
        DesignRequest.minimax_scalar_responses(
            1.5, np.eye(rank), np.full((model.graph.node_count, rank), np.nan)
        ),
        DesignRequest.response_weighted(
            1.5,
            [ResponseTerm.build(
                2, np.eye(model.graph.node_count), np.eye(rank),
                np.full((model.graph.node_count, rank), np.nan),
            )],
        ),
        DesignRequest.frobenius_shell(1.5, group_penalty_weight=np.nan),
        DesignRequest.frobenius_shell(1.5, group_penalty_weight=0.2),
    ]
    for request in bad_requests:
        with pytest.raises(ValueError):
            classify_request_cone(model, request)


def test_conditioning_cost_and_fixedness_regressions() -> None:
    record = conditioning_and_cost_audit()
    assert record["full_rank"] == 5
    assert record["full_rank_gram_condition"] > 1e11
    assert record["near_alias_gram_condition"] > 1e11
    assert record["weight_dynamic_range"] > 1e11
    assert record["four_node_l1_endpoints"] == [0.5, 1.0]


def test_octa_exact_reconstruction() -> None:
    record = octa_reconstruction("CLARABEL")
    assert record["rank"] == 2 and record["nullity"] == 3
    assert abs(float(record["objective"]) - 3.0) < 3e-5


def test_local_feasibility_does_not_imply_global_reversibility() -> None:
    model, certificate = locally_feasible_globally_infeasible_square()
    from pure_math.optimization.certificates import verify_farkas_certificate

    report = verify_farkas_certificate(model, certificate)
    assert report.passed
    assert abs(float(report.metrics["rhs_work"]) + 2.0 / 3.0) < 1e-12


def test_cone_classifier_does_not_solve() -> None:
    model, _, _ = tetrahedron_fixture()
    rank = model.shell(2).shell.rank
    assert classify_request_cone(model, DesignRequest.minimum_defect(1.5)) == "SDP"
    assert classify_request_cone(model, DesignRequest.frobenius_shell(1.5)) == "QP"
    assert classify_request_cone(model, DesignRequest.minimax_modes(1.5, np.eye(rank))) == "SOCP"
