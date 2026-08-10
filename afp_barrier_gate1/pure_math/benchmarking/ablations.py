"""Frozen P2E ablations, with quadrature changes kept in a separate study."""
from __future__ import annotations

import math
import time
import tracemalloc
from typing import Any

import numpy as np
from scipy import linalg

from pure_math.acceleration.transport import generator_from_edges

from .cases import _fine_angular_reference, accelerator_ablation
from .metrics import response_error, response_from_angular
from .operators import FrozenOperators
from .slab import normalized_beam


def run_ablations(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    directions = {
        "training": np.asarray([0.34, 0.52, 0.783]),
        "validation": np.asarray([-0.57, 0.31, 0.761]),
        "heldout": np.asarray([0.47, -0.68, 0.563]),
    }
    beam = directions[partition]
    beam /= np.linalg.norm(beam)
    normal = np.asarray([0.29, 0.63, 0.721])
    normal /= np.linalg.norm(normal)
    concentration = {"training": 38.0, "validation": 54.0, "heldout": 76.0}[partition]
    t, diffusion = 0.052, 0.41
    reference, _, _, _ = _fine_angular_reference(7, 14, beam, concentration, t, diffusion, normal)
    rows: dict[str, Any] = {}
    mapping = {
        "production": "optimized_harmonic_fidelity",
        "remove_H2_objective": "no_h2_objective",
        "remove_rate_cap": "remove_rate_cap",
        "remove_rotation_penalty": "remove_rotation_penalty",
        "alter_graph_locality": "alter_graph_locality",
        "signed_higher_accuracy": "signed_higher_accuracy",
    }
    for label, name in mapping.items():
        initial = normalized_beam(ops.nodes, ops.weights, beam, concentration)
        tracemalloc.start()
        started = time.perf_counter()
        try:
            value = linalg.expm(t * diffusion * ops.matrices[name]) @ initial
            elapsed = time.perf_counter() - started
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        response = response_from_angular(value, ops.nodes, ops.weights, normal)
        error = response_error(response, reference)
        offdiag = ops.matrices[name].copy()
        np.fill_diagonal(offdiag, np.inf)
        rows[label] = {
            "method": name,
            "same_nodes_as_production": True,
            "response_error": error.response,
            "tensor_error": error.tensor,
            "q_normal_error": error.q_normal,
            "minimum_solution": float(np.min(value)),
            "minimum_offdiagonal": float(np.min(offdiag)),
            "positivity_expected": name != "signed_higher_accuracy",
            "runtime_seconds": float(elapsed),
            "memory_bytes": int(peak),
        }

    # Different quadrature is deliberately separated from operator-quality rows.
    alt = ops.registry["co_design_only"]["alternate_product_3x8"]
    nodes = np.asarray(alt["nodes"], dtype=float)
    weights = np.asarray(alt["weights"], dtype=float)
    matrix = generator_from_edges(weights, np.asarray(alt["edges"], dtype=np.int64), np.asarray(alt["gamma"], dtype=float))
    initial = normalized_beam(nodes, weights, beam, concentration)
    started = time.perf_counter()
    value = linalg.expm(t * diffusion * matrix) @ initial
    response = response_from_angular(value, nodes, weights, normal)
    error = response_error(response, reference)
    co_design = {
        "alter_quadrature": {
            "node_family": "product_3x8",
            "directions": int(len(weights)),
            "response_error": error.response,
            "tensor_error": error.tensor,
            "q_normal_error": error.q_normal,
            "runtime_seconds": float(time.perf_counter() - started),
            "comparison_scope": "separate co-design study; not a same-node operator-quality comparison",
        }
    }
    return {
        "same_node_operator_ablations": rows,
        "co_design_ablation": co_design,
        "accelerator_only_unchanged_production_operator": accelerator_ablation(ops),
        "reference": {
            "type": "fine sampled spectral Laplace-Beltrami",
            "directions": 98,
            "response": reference.response,
        },
    }
