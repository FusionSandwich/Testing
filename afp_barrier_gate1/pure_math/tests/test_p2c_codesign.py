from __future__ import annotations

import math

import numpy as np
import pytest

from pure_math.codesign.adaptive import deterministic_mark, enriched_response_identity
from pure_math.codesign.convergence import (
    PAPER_I_LOWER_CONSTANT,
    PAPER_I_RATE_CONSTANT,
    PAPER_I_UPPER_CONSTANT,
    certified_pair_slope_interval,
    paper_i_sandwich,
)
from pure_math.codesign.exact_audit import exact_audit
from pure_math.codesign.families import (
    FAMILY_DESCRIPTORS,
    ahrens_beylkin_icosahedral_fixture,
    complete_edges,
    lebedev_6,
    lebedev_14,
    level_symmetric_from_orbits,
    maximal_net_candidate,
    product_rule,
    spherical_design_candidate,
    weak_delaunay_edges,
)
from pure_math.codesign.feasibility import (
    audit_protected_stratum,
    h1_trace_identity,
    minimum_norm_restoration_step,
)
from pure_math.codesign.fixtures import (
    icosahedral_complete_fixture,
    octahedral_complete_fixture,
    singular_sampling_fixture,
)
from pure_math.codesign.graph_updates import (
    GraphEvaluation,
    ObjectiveInterval,
    add_edges,
    certified_graph_decision,
    verify_zero_extension,
)
from pure_math.codesign.inner import (
    moving_gram_block,
    verify_moving_gram_epigraph,
)
from pure_math.codesign.metrics import generator_report, sampling_reports
from pure_math.codesign.outer import (
    ObjectiveTerms,
    ObjectiveWeights,
    OuterEvaluation,
    certified_proximal_step,
)
from pure_math.codesign.rotations import (
    audit_rotation_interpolation,
    collision_rotation_spread,
    joint_collision_covariance_defect,
    signed_permutation_rotations,
)
from pure_math.codesign.types import QuadratureCandidate


def test_all_requested_family_descriptors_are_explicit() -> None:
    assert {item.name for item in FAMILY_DESCRIPTORS} == {
        "product",
        "level_symmetric",
        "lebedev",
        "ahrens_beylkin",
        "spherical_design",
        "maximal_net",
        "delaunay",
        "locally_adapted",
    }
    assert all(item.mass_rule and item.admitted_graphs and item.warning
               for item in FAMILY_DESCRIPTORS)


@pytest.mark.parametrize(
    "candidate",
    [
        product_rule(2, 4, graph="complete"),
        level_symmetric_from_orbits([(1, 1, 1)], [1.0], graph="complete"),
        lebedev_14(graph="complete"),
        ahrens_beylkin_icosahedral_fixture(graph="complete"),
        maximal_net_candidate(10),
    ],
)
def test_family_candidates_have_strict_positive_normalized_masses(candidate) -> None:
    assert np.min(candidate.weights) > 0
    assert abs(float(np.sum(candidate.weights)) - 1.0) < 2e-12
    assert np.max(np.abs(np.linalg.norm(candidate.nodes, axis=1) - 1.0)) < 2e-11


def test_weak_delaunay_is_intrinsic_on_octahedral_degeneracy() -> None:
    candidate = lebedev_6(graph="weak_delaunay")
    rotated = candidate.rotated(
        np.asarray([
            [0.36, -0.48, 0.8],
            [0.8, 0.60, 0.0],
            [-0.48, 0.64, 0.60],
        ])
    )
    assert weak_delaunay_edges(candidate.nodes) == weak_delaunay_edges(rotated.nodes)


def test_dense_centered_complete_graph_is_exact_h0_h1_and_reversible() -> None:
    candidate = icosahedral_complete_fixture()
    report = generator_report(candidate, candidate.seed_conductance, (2,))
    assert report.h0_residual < 2e-13
    assert report.h1_residual < 2e-12
    assert report.reversibility_residual < 2e-13
    assert report.positivity_margin > 0
    assert abs(report.shell_defects[2] - 4.0) < 2e-10
    assert h1_trace_identity(candidate, candidate.seed_conductance).value < 2e-12


def test_raw_moving_gram_lmi_handles_a_sampling_kernel() -> None:
    candidate = singular_sampling_fixture()
    accepted = verify_moving_gram_epigraph(
        candidate, candidate.seed_conductance, 2, 6.0
    )
    rejected = verify_moving_gram_epigraph(
        candidate, candidate.seed_conductance, 2, 5.5
    )
    assert accepted.passed
    assert abs(accepted.generalized_defect - 6.0) < 2e-10
    assert not rejected.passed
    block = moving_gram_block(
        candidate, candidate.seed_conductance, 2, 6.0
    )
    assert block.shape[0] == candidate.node_count + 5


def test_sampling_condition_is_one_for_icosahedral_five_design() -> None:
    candidate = icosahedral_complete_fixture()
    report = sampling_reports(candidate, (2,))[0]
    assert report.rank == 5
    assert abs(report.condition - 1.0) < 2e-10


def test_edge_addition_zero_extension_preserves_all_fixed_quantities() -> None:
    weak = lebedev_6(graph="weak_delaunay")
    gamma = np.linspace(0.01, 0.01 * weak.edge_count, weak.edge_count)
    seeded = QuadratureCandidate.build(
        weak.family,
        weak.nodes,
        weak.weights,
        [tuple(map(int, edge)) for edge in weak.edges],
        seed_conductance=gamma,
    )
    extra = sorted(set(complete_edges(6)) - set(map(tuple, seeded.edges)))
    enlarged = add_edges(seeded, extra)
    assert enlarged.edge_count == 15
    assert verify_zero_extension(
        seeded, enlarged, seeded.seed_conductance, enlarged.seed_conductance
    )


def test_certified_graph_decision_is_fail_closed() -> None:
    old_candidate = octahedral_complete_fixture()
    new_candidate = old_candidate
    old = GraphEvaluation(
        old_candidate, ObjectiveInterval(1.0, 1.01), True, True, "old"
    )
    new = GraphEvaluation(
        new_candidate, ObjectiveInterval(0.80, 0.81), True, True, "new"
    )
    assert certified_graph_decision(
        old, new, edge_penalty=0.0, strict_decrease=0.01
    ).accepted
    uncertified = GraphEvaluation(
        new_candidate, ObjectiveInterval(0.1, 0.2), True, False, "solver-only"
    )
    assert not certified_graph_decision(old, uncertified).accepted


def test_collision_probe_and_joint_covariance_are_separately_scoped() -> None:
    candidate = icosahedral_complete_fixture()
    rotations = signed_permutation_rotations()
    probe = np.asarray([1.0, -0.5, 0.25, 0.0, 0.75])
    spread = collision_rotation_spread(
        candidate, candidate.seed_conductance, probe, rotations
    )
    joint = joint_collision_covariance_defect(
        candidate, candidate.seed_conductance, probe, rotations
    )
    assert spread.scope.startswith("COLLISION_ONLY")
    assert spread.absolute_spread < 2e-10
    assert joint < 2e-10


def test_identity_interpolation_audit_is_separate_streaming_remedy() -> None:
    candidate = octahedral_complete_fixture()
    report = audit_rotation_interpolation(np.eye(6), candidate, candidate)
    assert report.passed
    assert report.scope == "SEPARATE_STREAMING_REMEDY"


def test_enriched_response_identity_and_marking() -> None:
    operator = np.asarray([[3.0, -0.5], [-0.5, 2.0]])
    report = enriched_response_identity(
        operator, [1.0, -0.25], [0.5, 2.0], [0.1, -0.2]
    )
    assert report.passed
    assert abs(report.response_error) <= report.indicator_sum + 2e-12
    assert deterministic_mark([4.0, 2.0, 1.0], bulk_fraction=0.5) == (0,)


def test_restoration_rejects_a_nonsurjective_reduced_jacobian() -> None:
    with pytest.raises(np.linalg.LinAlgError):
        minimum_norm_restoration_step(
            np.asarray([[1.0], [0.0]]), np.asarray([1.0, 1.0])
        )
    delta, report = minimum_norm_restoration_step(
        np.asarray([[1.0, 0.0], [0.0, 2.0]]), np.asarray([1.0, -2.0])
    )
    assert report.surjective_candidate
    assert np.linalg.norm(np.asarray([[1.0, 0.0], [0.0, 2.0]]) @ delta
                          + np.asarray([1.0, -2.0])) < 1e-12


def test_protected_audit_accepts_exact_symmetric_fixture() -> None:
    candidate = octahedral_complete_fixture()
    report = audit_protected_stratum(
        candidate,
        candidate.seed_conductance,
        minimum_weight=0.1,
        minimum_separation=0.4,
        minimum_sampling_eigenvalue=-1e-12,
        minimum_conductance=0.01,
        rate_cap=2.0,
    )
    assert report.passed


def test_finite_proximal_controller_certifies_descent_without_global_claim() -> None:
    current = octahedral_complete_fixture()
    proposal = current.rotated(np.eye(3))

    def evaluator(candidate):
        value = 2.0 if "joint_rotation" not in candidate.metadata else 1.8
        terms = ObjectiveTerms(value, 0.0)
        return OuterEvaluation(
            candidate,
            terms,
            value,
            True,
            True,
            "VERIFIED_FLOAT",
        )

    step = certified_proximal_step(
        current, [proposal], evaluator, alpha=1.0
    )
    assert step.accepted
    assert step.after.objective <= step.before.objective


def test_paper_i_all_orders_constants_form_exact_frontier_sandwich() -> None:
    h = 0.125
    theorem = paper_i_sandwich(h)
    assert math.isclose(
        PAPER_I_LOWER_CONSTANT * PAPER_I_RATE_CONSTANT, 6.0,
        rel_tol=1e-14,
    )
    assert theorem.lower > 0
    assert theorem.upper == PAPER_I_UPPER_CONSTANT * h * h
    interval = certified_pair_slope_interval(
        0.2, 0.1, (0.039, 0.041), (0.0098, 0.0102)
    )
    assert interval[0] <= 2.0 <= interval[1]


def test_symbolic_audit() -> None:
    result = exact_audit()
    assert result["H1"] == "exact eigenvalue -2"
    assert result["H2_dense_defect"] == "4"
    assert result["paper_I_lower_times_rate_cap"] == "6"
