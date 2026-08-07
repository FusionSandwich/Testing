from __future__ import annotations

import numpy as np
import pytest

from pure_math.benchmarking.harness import _operator_invariants, run_benchmarks
from pure_math.benchmarking.manifest_builder import build_manifest
from pure_math.benchmarking.transport import layered_slab
from pure_math.benchmarking.harness import FrozenOperator
from pure_math.codesign.families import complete_edges, product_rule
from pure_math.optimization import QuadratureGraph


def _dense_exact_operator() -> FrozenOperator:
    candidate = product_rule(2, 4, graph="complete")
    graph = QuadratureGraph.build(
        candidate.nodes,
        candidate.weights,
        complete_edges(candidate.node_count),
    )
    gamma = np.asarray(
        [2.0 * candidate.weights[i] * candidate.weights[j] for i, j in graph.edges],
        dtype=float,
    )
    matrix = graph.generator(gamma)
    return FrozenOperator(
        "dense_control",
        "test",
        candidate.nodes,
        candidate.weights,
        matrix,
        float(np.max(-np.diag(matrix))),
        {},
        0.0,
        True,
        "test",
    )


def test_manifest_contains_all_mandatory_cases_and_ablations() -> None:
    manifest = build_manifest(
        {
            "schema": "afp-p2e-frozen-operator-registry-v1",
            "registry_sha256": "registry-test",
        },
        status="DEVELOPMENT_TRAINING_VALIDATION",
    )
    heldout = [case for case in manifest["cases"] if case["partition"] == "heldout"]
    categories = {case["category"] for case in heldout}
    assert categories == {
        "exact_Ylm_decay",
        "random_band_limited",
        "narrow_beam",
        "published_electron_depth_dose",
        "justified_neutron_BFP",
        "proton_multiple_scattering",
        "HTS_oblique_stack",
    }
    assert len(manifest["ablation_inventory"]) == 7
    assert manifest["partitions"]["heldout"]
    assert manifest["fixed_node_method_order"][0:2] == [
        "monotone_afp_baseline",
        "harmonic_fidelity",
    ]


def test_heldout_execution_is_fail_closed_before_preregistration() -> None:
    manifest = build_manifest(
        {
            "schema": "afp-p2e-frozen-operator-registry-v1",
            "registry_sha256": "registry-test",
        },
        status="DEVELOPMENT_TRAINING_VALIDATION",
    )
    with pytest.raises(ValueError, match="immutable preregistration"):
        run_benchmarks(
            {
                "schema": "afp-p2e-frozen-operator-registry-v1",
                "registry_sha256": "registry-test",
                "methods": {},
            },
            manifest,
            "heldout",
        )


def test_dense_exact_control_preserves_h0_h1_and_conservation() -> None:
    operator = _dense_exact_operator()
    invariants = _operator_invariants(operator)
    assert invariants["conservation_residual"] < 2e-13
    assert invariants["h0_residual"] < 2e-13
    assert invariants["h1_residual"] < 2e-13
    assert invariants["minimum_offdiagonal"] >= 0.0


def test_layered_vacuum_current_ledger() -> None:
    operator = _dense_exact_operator()
    profile = layered_slab(
        operator.nodes,
        operator.weights,
        operator.matrix,
        {
            "axis": [0.0, 0.0, 1.0],
            "normal": [0.0, 0.0, 1.0],
            "concentration": 12.0,
            "energy_mev": 1.0,
            "layers": [
                {
                    "material": "vacuum",
                    "thickness_cm": 0.5,
                    "cells": 3,
                    "absorption": 0.0,
                    "angular_diffusion": 0.0,
                    "stopping_mev_per_cm": 0.0,
                }
            ],
        },
        direct=True,
    )
    assert profile.converged
    assert profile.particle_balance_error < 2e-12
    assert min(profile.response) >= -2e-12


def test_preregistered_manifest_digest_changes_with_status() -> None:
    registry = {
        "schema": "afp-p2e-frozen-operator-registry-v1",
        "registry_sha256": "registry-test",
    }
    development = build_manifest(registry, status="DEVELOPMENT_TRAINING_VALIDATION")
    frozen = build_manifest(registry, status="IMMUTABLE_PREREGISTERED")
    assert development["manifest_sha256"] != frozen["manifest_sha256"]
    assert frozen["status"] == "IMMUTABLE_PREREGISTERED"
