#!/usr/bin/env python3
"""Deterministic numerical and certificate audit for all P2A formulations."""

from __future__ import annotations

import argparse
import json

import numpy as np

from .certificates import (
    ConicInfeasibilityCertificate,
    verify_conic_infeasibility_certificate,
    verify_farkas_certificate,
)
from .fixtures import (
    ambiguous_rank_fixture,
    cube_shell_fixture,
    declared_rank_truncation_mutation,
    dynamic_weight_ill_conditioned_fixture,
    four_node_antipodal_preference,
    full_rank_ill_conditioned_fixture,
    locally_feasible_globally_infeasible_square,
    locally_strict_globally_infeasible_cube,
    near_alias_ill_conditioned_fixture,
    octahedron_fixture,
    tetrahedron_fixture,
)
from .model import AmbiguousSamplingRank, DesignModel
from .programs import (
    DesignRequest,
    ResponseTerm,
    SolverConfig,
    classify_request_cone,
    prune_and_reoptimize,
    solve_design,
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def checked_solve(model: DesignModel, request: DesignRequest, config: SolverConfig):
    result = solve_design(model, request, config)
    require(result.feasible_candidate, f"{request.kind}/{request.metric}: no candidate: {result.status}")
    require(result.verification is not None and result.verification.passed, f"{request.kind}/{request.metric}: {result.verification}")
    require(result.verification.certificate_level == "tolerance_diagnostic", "numeric certificate mislabeled exact")
    return result


def formulation_audit(solver: str) -> dict[str, object]:
    tetra, exact_gamma, exact_sampling = tetrahedron_fixture()
    # Add H3 only for the multi-shell tests; retain the exact H2 certificate.
    model = DesignModel.build(
        tetra.graph, (2, 3), exact_sampling_certificates={2: exact_sampling}
    )
    config = SolverConfig(solver)
    rank = model.shell(2).shell.rank
    modes = np.eye(rank)
    scalar_outputs = np.zeros((model.graph.node_count, rank))
    scalar_outputs[0, :] = 1.0

    requests = [
        DesignRequest.minimum_defect(1.5),
        DesignRequest.minimum_rate(4.0),
        DesignRequest.frobenius_shell(1.5),
        DesignRequest.minimax_modes(1.5, modes),
        DesignRequest.minimax_scalar_responses(1.5, modes, scalar_outputs),
        DesignRequest.multi_shell(1.5, {2: 1.0, 3: 0.1}, metric="frobenius"),
        DesignRequest.multi_shell(1.5, {2: 1.0, 3: 0.1}, metric="spectral_max"),
    ]
    response_terms = [
        ResponseTerm.build(2, np.eye(4), np.eye(rank), np.zeros((4, rank)), weight=0.5),
        ResponseTerm.build(2, np.eye(4)[:2], np.eye(rank)[:, :1], np.full((2, 1), 0.125), weight=2.0),
    ]
    requests.extend([
        DesignRequest.response_weighted(1.5, response_terms, metric="frobenius"),
        DesignRequest.response_weighted(1.5, response_terms, metric="spectral_max"),
        DesignRequest.response_weighted(1.5, response_terms, metric="column_max"),
    ])
    scalar_terms = [
        ResponseTerm.build(2, np.ones((1, 4)) / 2.0, np.eye(rank)[:, :1], np.zeros((1, 1))),
        ResponseTerm.build(2, np.asarray([[1.0, 0.0, 0.0, 0.0]]), np.eye(rank)[:, 1:2], np.asarray([[0.2]]), weight=2.0),
    ]
    requests.append(DesignRequest.response_weighted(1.5, scalar_terms, metric="scalar_max"))
    group_request = DesignRequest.frobenius_shell(
        1.5, edge_groups=((0, 1, 2), (3, 4, 5)), group_penalty_weight=0.2,
    )
    requests.append(group_request)

    records = []
    for request in requests:
        result = checked_solve(model, request, config)
        records.append({
            "kind": request.kind,
            "metric": request.metric,
            "cone": classify_request_cone(model, request),
            "objective": float(result.objective),
            "gap": float(result.verification.metrics["primal_dual_gap"]),
        })

    spectral = records[0]
    minimum_rate = records[1]
    require(abs(spectral["objective"] - 4.0) < 2e-5, "tetra minimum defect reconstruction")
    require(abs(minimum_rate["objective"] - 1.5) < 2e-5, "tetra minimum rate reconstruction")
    require(abs(spectral["objective"] * 1.5 - 6.0) < 3e-5, "Paper-I lower-bound equality")
    require(np.max(np.abs(np.asarray(checked_solve(model, DesignRequest.minimum_defect(1.5), config).gamma) - exact_gamma)) < 2e-6, "tetra gamma reconstruction")
    return {"solver": solver, "programs": records}


def certificate_and_failure_audit(solver: str) -> dict[str, object]:
    tetra, _, _ = tetrahedron_fixture()
    u = tetra.shell(2).shell.quotient_frame
    p = u @ u.T
    zmat = np.block([[p, -u], [-u.T, np.eye(3)]]) / 6.0
    conic = ConicInfeasibilityCertificate(
        np.zeros(12), np.full(4, 4.0 / 3.0), np.zeros(6), zmat,
        1.5, 3.9, label="tetra exact-form caps R=3/2, delta=39/10",
    )
    conic_report = verify_conic_infeasibility_certificate(tetra, conic)
    require(conic_report.passed, f"conic infeasibility certificate: {conic_report.failures}")
    require(abs(float(conic_report.metrics["strict_separation"]) - 0.1) < 2e-12, "conic separation")
    bad_conic = ConicInfeasibilityCertificate(
        conic.equality_field, np.full(4, 1.0 / 3.0), conic.positivity_field,
        conic.psd_field, conic.rate_cap, conic.defect_cap,
    )
    require(not verify_conic_infeasibility_certificate(tetra, bad_conic).passed, "wrong rate-dual normalization mutation escaped")
    nan_conic = ConicInfeasibilityCertificate(
        np.full(12, np.nan), conic.rate_field, conic.positivity_field,
        conic.psd_field, conic.rate_cap, conic.defect_cap,
    )
    require(not verify_conic_infeasibility_certificate(tetra, nan_conic).passed, "NaN conic ray escaped")
    skew_conic = ConicInfeasibilityCertificate(
        conic.equality_field, conic.rate_field, conic.positivity_field,
        conic.psd_field + np.triu(np.ones_like(conic.psd_field), 1),
        conic.rate_cap, conic.defect_cap,
    )
    require(not verify_conic_infeasibility_certificate(tetra, skew_conic).passed, "nonsymmetric conic ray escaped")

    square, square_cert = locally_feasible_globally_infeasible_square()
    square_report = verify_farkas_certificate(square, square_cert)
    require(square_report.passed, "four-cycle exact Farkas certificate")
    require(abs(float(square_report.metrics["rhs_work"]) + 2.0 / 3.0) < 2e-12, "four-cycle Farkas work")
    cube, cube_cert, local_rates = locally_strict_globally_infeasible_cube()
    cube_report = verify_farkas_certificate(cube, cube_cert)
    require(cube_report.passed, "cube exact Farkas certificate")
    require(abs(float(cube_report.metrics["rhs_work"]) + 0.4) < 2e-12, "cube Farkas work")
    require(not verify_farkas_certificate(cube, type(cube_cert)(-cube_cert.equality_field)).passed, "reversed Farkas sign mutation escaped")
    require(
        not verify_farkas_certificate(
            cube, type(cube_cert)(np.full_like(cube_cert.equality_field, np.nan))
        ).passed,
        "NaN Farkas ray escaped",
    )
    # Every cube row has the displayed strict local rate-one solution.
    for i, node in enumerate(cube.graph.nodes):
        incident = [e for e, edge in enumerate(cube.graph.edges) if i in edge]
        local = np.zeros(3)
        for edge in incident:
            a, b = map(int, cube.graph.edges[edge])
            j = b if a == i else a
            local += local_rates[edge] * (cube.graph.nodes[j] - node)
        require(np.linalg.norm(local + 2 * node) < 2e-12, "cube local positive row")

    prune = prune_and_reoptimize(
        tetra, DesignRequest.minimum_defect(1.5), SolverConfig(solver)
    )
    require(len(prune.kept_original_edges) == 6, "tetra unique support was incorrectly pruned")
    require(all(attempt.farkas_verified for attempt in prune.attempts), "prune failure lacks Farkas certificate")
    return {
        "conic_separation": conic_report.metrics["strict_separation"],
        "square_farkas_work": square_report.metrics["rhs_work"],
        "cube_farkas_work": cube_report.metrics["rhs_work"],
        "prune_attempts": len(prune.attempts),
    }


def conditioning_and_cost_audit() -> dict[str, object]:
    full, gamma, certificate, determinant = full_rank_ill_conditioned_fixture()
    report = full.condition_report()
    shell = report["shells"][2]
    require(certificate.rank == 5 and shell["rank"] == 5, "exact full rank condition fixture")
    require(shell["exact_rank_certified"], "full-rank condition fixture lacks exact rank")
    require(shell["condition_sampling_gram"] > 1e11, "condition degradation too weak")
    require(np.linalg.norm(full.graph.h1_matrix @ gamma - full.graph.h1_rhs, ord=np.inf) < 2e-12, "ill-conditioned full-rank H1")

    near, near_gamma = near_alias_ill_conditioned_fixture()
    require(near.condition_report()["shells"][2]["condition_sampling_gram"] > 1e11, "near-alias condition report")
    require(np.linalg.norm(near.graph.h1_matrix @ near_gamma - near.graph.h1_rhs, ord=np.inf) < 2e-12, "near-alias H1")
    dynamic, dynamic_gamma = dynamic_weight_ill_conditioned_fixture()
    require(dynamic.condition_report()["weight_dynamic_range"] > 1e11, "weight dynamic range report")
    require(np.linalg.norm(dynamic.graph.h1_matrix @ dynamic_gamma - dynamic.graph.h1_rhs, ord=np.inf) < 2e-12, "dynamic-weight H1")

    try:
        DesignModel.build(ambiguous_rank_fixture())
    except AmbiguousSamplingRank:
        pass
    else:
        raise AssertionError("ambiguous sampling rank mutation was accepted")
    try:
        declared_rank_truncation_mutation()
    except AmbiguousSamplingRank:
        pass
    else:
        raise AssertionError("declared full-rank truncation mutation was accepted")

    cube1, gamma1 = cube_shell_fixture(1)
    cube2, gamma2 = cube_shell_fixture(2)
    require(abs(float(np.sum(gamma1)) - 1.5) < 1e-13, "cube distance-one l1")
    require(abs(float(np.sum(gamma2)) - 0.75) < 1e-13, "cube distance-two l1")
    require(abs(float(cube1.graph.losses @ gamma1) - 1.0) < 1e-13, "cube fixed loss cost 1")
    require(abs(float(cube2.graph.losses @ gamma2) - 1.0) < 1e-13, "cube fixed loss cost 2")
    require(cube1.affine_cost_certificate(np.ones(cube1.graph.edge_count))["affine_fixed"], "one-shell plain l1 should be fixed")
    require(cube2.affine_cost_certificate(np.ones(cube2.graph.edge_count))["affine_fixed"], "second one-shell plain l1 should be fixed")
    require(cube1.affine_cost_certificate(cube1.graph.losses)["affine_fixed"], "loss l1 fixedness witness missed")

    four0, g0 = four_node_antipodal_preference(0.0)
    four1, g1 = four_node_antipodal_preference(1.0)
    require(abs(np.sum(g0) - 0.5) < 1e-13 and abs(np.sum(g1) - 1.0) < 1e-13, "four-node variable conductance")
    require(abs(four0.graph.losses @ g0 - 1.0) < 1e-13 and abs(four1.graph.losses @ g1 - 1.0) < 1e-13, "four-node fixed loss")
    require(not four0.affine_cost_certificate(np.ones(four0.graph.edge_count))["affine_fixed"], "mixed-loss complete graph plain l1 incorrectly fixed")
    return {
        "full_rank": shell["rank"],
        "full_rank_gram_condition": shell["condition_sampling_gram"],
        "selected_minor_determinant": str(determinant),
        "near_alias_gram_condition": near.condition_report()["shells"][2]["condition_sampling_gram"],
        "weight_dynamic_range": dynamic.condition_report()["weight_dynamic_range"],
        "four_node_l1_endpoints": [float(np.sum(g0)), float(np.sum(g1))],
    }


def octa_reconstruction(solver: str) -> dict[str, object]:
    model, exact_gamma, certificate = octahedron_fixture()
    result = checked_solve(model, DesignRequest.minimum_defect(2.0), SolverConfig(solver))
    require(abs(float(result.objective) - 3.0) < 3e-5, "octa defect reconstruction")
    require(np.max(np.abs(np.asarray(result.gamma) - exact_gamma)) < 3e-6, "octa conductance reconstruction")
    require(certificate.rank == 2 and len(certificate.nullspace) == 3, "octa exact aliases")
    return {"objective": result.objective, "rank": certificate.rank, "nullity": len(certificate.nullspace)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"), default="CLARABEL")
    args = parser.parse_args()
    record = {
        "formulations": formulation_audit(args.solver),
        "certificates": certificate_and_failure_audit(args.solver),
        "conditioning_and_cost": conditioning_and_cost_audit(),
        "octahedron": octa_reconstruction(args.solver),
    }
    print(json.dumps(record, indent=2, sort_keys=True))
    print(f"P2A convex design audit ({args.solver}): PASS")


if __name__ == "__main__":
    main()
