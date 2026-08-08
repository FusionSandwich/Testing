from __future__ import annotations

import numpy as np

from pure_math.benchmarking.cases import individual_modes_case, random_bandlimited_case
from pure_math.benchmarking.manifest import load_manifest
from pure_math.benchmarking.operators import load_frozen_operators
from pure_math.benchmarking.slab import (
    Layer,
    build_mesh,
    normalized_beam,
    product_quadrature,
    reversible_positive_kernel,
    solve_steady_slab,
)


def test_manifest_and_registry_are_hash_bound() -> None:
    manifest = load_manifest()
    operators = load_frozen_operators()
    assert manifest["operator_registry_sha256"] == operators.registry["scientific_sha256"]
    assert manifest["parent_p2d_sha"] == "d46979d2aa52d502915eea2355a64cb788aae4f6"
    assert len(operators.nodes) == 32
    assert np.min(operators.weights) > 0
    assert abs(np.sum(operators.weights) - 1.0) < 2e-13


def test_production_operator_is_positive_exact_and_h2_better() -> None:
    operators = load_frozen_operators()
    baseline = operators.audit("moment_monotone_baseline")
    optimized = operators.audit("optimized_harmonic_fidelity")
    assert baseline["positive"] and optimized["positive"]
    assert optimized["h0_residual"] < 5e-10
    assert optimized["h1_residual"] < 5e-9
    assert optimized["shell_defects"][2] < 0.75 * baseline["shell_defects"][2]
    assert optimized["rate_max"] <= operators.registry["production_rate_cap"] + 5e-8


def test_positive_reversible_boltzmann_kernel() -> None:
    nodes, weights = product_quadrature(4, 8)
    kernel = reversible_positive_kernel(nodes, weights, 24.0)
    assert np.min(kernel) >= -1e-14
    assert np.linalg.norm(kernel @ np.ones(len(weights)) - 1.0, ord=np.inf) < 2e-10
    assert np.linalg.norm(weights[:, None] * kernel - kernel.T * weights[None, :], ord=np.inf) < 2e-10


def test_small_upwind_slab_is_positive_and_balanced() -> None:
    nodes, weights = product_quadrature(3, 6)
    mesh = build_mesh([Layer("test", 1.0, 8, "test")])
    kernel = reversible_positive_kernel(nodes, weights, 5.0)
    block = 0.08 * np.eye(len(weights)) + 0.7 * (np.eye(len(weights)) - kernel)
    result = solve_steady_slab(
        mesh,
        nodes,
        weights,
        np.asarray([0.0, 0.0, 1.0]),
        np.repeat(block[None, :, :], mesh.cell_count, axis=0),
        np.full(mesh.cell_count, 0.08),
        np.zeros((mesh.cell_count, len(weights))),
        inflow_left=normalized_beam(nodes, weights, np.asarray([0.0, 0.0, 1.0]), 30.0),
    )
    assert result.minimum_flux >= -2e-10
    assert result.balance_residual < 5e-8


def test_training_analytic_cases_have_complete_same_node_records() -> None:
    operators = load_frozen_operators()
    for case in (
        individual_modes_case(operators, "training"),
        random_bandlimited_case(operators, "training"),
    ):
        assert case["same_nodes"]
        assert case["same_spatial_energy_discretization"]
        assert set(case["methods"]) == {
            "moment_monotone_baseline",
            "optimized_harmonic_fidelity",
        }
        for row in case["methods"].values():
            assert row["positivity"]
            assert row["h0_residual"] < 5e-10
            assert row["h1_residual"] < 5e-9
            assert row["memory_bytes"] >= 0
