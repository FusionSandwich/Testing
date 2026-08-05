"""Deterministic executable audit for the P2C co-design package."""

from __future__ import annotations

import argparse
import json

import numpy as np

from .adaptive import antipodal_response_proposal, enriched_response_identity
from .convergence import benchmark_reflected_ring_family, fitted_log_slope
from .families import (
    FAMILY_DESCRIPTORS,
    ahrens_beylkin_icosahedral_fixture,
    delaunay_candidate,
    lebedev_14,
    level_symmetric_from_orbits,
    maximal_net_candidate,
    product_rule,
    spherical_design_candidate,
)
from .fixtures import (
    icosahedral_complete_fixture,
    octahedral_complete_fixture,
    singular_sampling_fixture,
)
from .graph_updates import add_edges, verify_zero_extension
from .inner import verify_moving_gram_epigraph
from .metrics import full_report
from .rotations import (
    collision_rotation_spread,
    joint_collision_covariance_defect,
    signed_permutation_rotations,
)
from .types import QuadratureCandidate


def _with_dense_seed(candidate: QuadratureCandidate) -> QuadratureCandidate:
    from .inner import dense_centered_initializer

    gamma = dense_centered_initializer(candidate)
    return QuadratureCandidate.build(
        candidate.family,
        candidate.nodes,
        candidate.weights,
        [tuple(map(int, edge)) for edge in candidate.edges],
        seed_conductance=gamma,
        metadata={**candidate.metadata, "audit_seed": "dense-centered"},
    )


def family_candidates() -> tuple[QuadratureCandidate, ...]:
    product = _with_dense_seed(product_rule(2, 4, graph="complete"))
    level = _with_dense_seed(level_symmetric_from_orbits(
        [(1.0, 1.0, 1.0)], [1.0], graph="complete"
    ))
    lebedev = _with_dense_seed(lebedev_14(graph="complete"))
    ab = icosahedral_complete_fixture()
    design_base = ahrens_beylkin_icosahedral_fixture(graph="complete")
    design = QuadratureCandidate.build(
        "spherical_design",
        design_base.nodes,
        design_base.weights,
        [tuple(map(int, edge)) for edge in design_base.edges],
        seed_conductance=design_base.seed_conductance,
        metadata={"declared_strength": 5, "fixture": "icosahedral orbit"},
    )
    net = maximal_net_candidate(12, graph="weak_delaunay")
    delaunay = delaunay_candidate(design_base.nodes, design_base.weights)
    local_base = octahedral_complete_fixture()
    local = antipodal_response_proposal(
        local_base,
        np.arange(local_base.node_count, 0, -1, dtype=float),
        bulk_fraction=0.4,
    ).proposal
    return product, level, lebedev, ab, design, net, delaunay, local


def run_audit(*, quick: bool) -> dict[str, object]:
    candidates = family_candidates()
    names = {descriptor.name for descriptor in FAMILY_DESCRIPTORS}
    observed = {candidate.family for candidate in candidates}
    if names != observed:
        raise AssertionError(f"family coverage mismatch: expected={names}, observed={observed}")

    family_rows: list[dict[str, object]] = []
    for candidate in candidates:
        report = full_report(
            candidate,
            rate_cap=20.0,
            degrees=(2,),
            fill_probe_count=384 if quick else 2048,
        )
        family_rows.append({
            "family": report.family,
            "N": report.nodes,
            "E": report.edges,
            "positive_mass": float(np.min(candidate.weights)),
            "sampling_condition2": report.sampling[0].condition,
            "sampling_rank2": report.sampling[0].rank,
            "local_margin": report.feasibility.local_margin_min,
            "global_margin": report.feasibility.global_margin,
            "global_status": report.feasibility.global_status,
            "seed_H1_residual": (
                None if report.generator is None else report.generator.h1_residual
            ),
        })

    singular = singular_sampling_fixture()
    moving = verify_moving_gram_epigraph(
        singular,
        singular.seed_conductance,
        degree=2,
        delta=6.0,
        tolerance=2e-8,
    )
    if not moving.passed or abs(moving.generalized_defect - 6.0) > 2e-8:
        raise AssertionError("singular moving-Gram epigraph regression failed")

    old = QuadratureCandidate.build(
        "edge_subset",
        singular.nodes,
        singular.weights,
        [(0, 1)],
        seed_conductance=[0.5],
    )
    enlarged = add_edges(old, [])
    if not verify_zero_extension(
        old, enlarged, old.seed_conductance, enlarged.seed_conductance
    ):
        raise AssertionError("zero-extension theorem regression failed")

    symmetric = icosahedral_complete_fixture()
    rotations = signed_permutation_rotations()
    coefficients = np.asarray([1.0, -0.5, 0.25, 0.0, 0.75])
    spread = collision_rotation_spread(
        symmetric, symmetric.seed_conductance, coefficients, rotations
    )
    covariance = joint_collision_covariance_defect(
        symmetric, symmetric.seed_conductance, coefficients, rotations
    )
    if spread.absolute_spread > 2e-9 or covariance > 2e-9:
        raise AssertionError("isotropic dense-generator rotation audit failed")

    operator = np.asarray([[3.0, -0.5], [-0.5, 2.0]])
    enriched = enriched_response_identity(
        operator,
        np.asarray([1.0, -0.25]),
        np.asarray([0.5, 2.0]),
        np.asarray([0.1, -0.2]),
    )
    if not enriched.passed:
        raise AssertionError("enriched discrete response identity failed")

    levels = ((16, 1), (24, 1)) if quick else ((16, 1), (24, 1), (32, 1))
    convergence = benchmark_reflected_ring_family(
        levels, optimize_indices=()
    )
    slope = fitted_log_slope(convergence)

    return {
        "families": family_rows,
        "moving_gram_singular": {
            "rank_compatible_residual": moving.kernel_compatibility_residual,
            "defect": moving.generalized_defect,
            "minimum_block_eigenvalue": moving.minimum_block_eigenvalue,
        },
        "rotation": {
            "collision_fixed_spread": spread.absolute_spread,
            "joint_covariance_defect": covariance,
            "scope": spread.scope,
        },
        "adaptive": {
            "identity_residual": enriched.identity_residual,
            "indicator_bound": enriched.indicator_sum,
            "scope": enriched.scope,
        },
        "convergence": [row.serializable() for row in convergence],
        "finite_slope_supplement_only": slope,
        "theorem_source": "accepted P1B lower frontier plus P1E construction",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    report = run_audit(quick=args.quick)
    print(json.dumps(report, sort_keys=True))
    print("P2C_CODESIGN_AUDIT_PASS")


if __name__ == "__main__":
    main()
