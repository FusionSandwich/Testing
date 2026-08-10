"""Fail-closed P2E result and ablation audit."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from .manifest import load_manifest
from .operators import load_frozen_operators


def audit_results(payload: dict[str, Any]) -> dict[str, Any]:
    manifest = load_manifest()
    ops = load_frozen_operators()
    partition = str(payload["partition"])
    expected = list(manifest["partitions"][partition])
    identifiers = [row["id"] for row in payload["cases"]]
    checks: dict[str, Any] = {
        "manifest_match": payload["manifest_sha256"] == manifest["scientific_sha256"],
        "registry_match": payload["operator_registry_sha256"] == ops.registry["scientific_sha256"],
        "case_inventory": identifiers == expected,
        "same_node_comparisons": all(row["same_nodes"] for row in payload["cases"]),
        "same_space_energy": all(row["same_spatial_energy_discretization"] for row in payload["cases"]),
    }
    maximum_h0 = 0.0
    maximum_h1 = 0.0
    minimum_flux = float("inf")
    maximum_balance = 0.0
    complete_fields = True
    for case in payload["cases"]:
        if "uncertainty" not in case["reference"]:
            complete_fields = False
        if set(case["methods"]) != {"moment_monotone_baseline", "optimized_harmonic_fidelity"}:
            complete_fields = False
        for row in case["methods"].values():
            maximum_h0 = max(maximum_h0, float(row["h0_residual"]))
            maximum_h1 = max(maximum_h1, float(row["h1_residual"]))
            if bool(row.get("positivity_applicable", True)):
                minimum_flux = min(minimum_flux, float(row["minimum_flux"]))
            maximum_balance = max(maximum_balance, float(row.get("transport_balance_residual", row.get("mass_error", 0.0))))
            required = {
                "shell_defects",
                "scalar_error",
                "current_error",
                "tensor_error",
                "q_normal_error",
                "response_error",
                "runtime_seconds",
                "memory_bytes",
                "iterations",
                "matvecs",
            }
            complete_fields = complete_fields and required.issubset(row)
        complete_fields = complete_fields and {
            "equal_direction_count",
            "equal_wall_time",
            "wall_time_at_equal_response_error",
        }.issubset(case["equal_cost_equal_error"])
    checks.update(
        {
            "complete_required_fields": complete_fields,
            "maximum_h0_residual": maximum_h0,
            "maximum_h1_residual": maximum_h1,
            "minimum_flux": minimum_flux,
            "maximum_balance_residual": maximum_balance,
            "invariant_gate": maximum_h0 <= 5e-8 and maximum_h1 <= 5e-7,
            "positivity_gate": minimum_flux >= -2e-9,
            "balance_gate": maximum_balance <= 5e-6,
        }
    )
    ablations = payload.get("ablations", {})
    same_node_ablation_names = set(ablations.get("same_node_operator_ablations", {}))
    checks["ablation_inventory"] = same_node_ablation_names == {
        "production", "remove_H2_objective", "remove_rate_cap",
        "remove_rotation_penalty", "alter_graph_locality",
        "signed_higher_accuracy",
    }
    checks["quadrature_ablation_separate"] = set(ablations.get("co_design_ablation", {})) == {"alter_quadrature"}
    checks["signed_scope_honest"] = not ablations["same_node_operator_ablations"]["signed_higher_accuracy"]["positivity_expected"]
    acceleration = payload["accelerator_only_ablation"]
    checks["accelerator_inventory"] = set(acceleration) == {
        "none",
        "moment_monotone_baseline",
        "optimized_harmonic_fidelity",
        "h2_poor_positive",
    }
    checks["accelerator_fixed_point"] = all(
        row["production_operator_unchanged"]
        and row["converged"]
        and row["fixed_point_error"] < 5e-8
        for row in acceleration.values()
    )
    baseline_iterations = int(acceleration["moment_monotone_baseline"]["iterations"])
    optimized_iterations = int(acceleration["optimized_harmonic_fidelity"]["iterations"])
    acceleration_reduction = (
        (baseline_iterations - optimized_iterations) / baseline_iterations
        if baseline_iterations > 0
        else float("-inf")
    )
    checks["acceleration_iteration_reduction"] = float(acceleration_reduction)
    checks["acceleration_value_gate"] = (
        baseline_iterations > 0
        and acceleration_reduction
        >= float(manifest["success_criteria"]["acceleration_iteration_reduction_min"])
    )
    checks["equal_wall_time_claim_honest"] = all(
        not bool(case["equal_cost_equal_error"]["equal_wall_time"].get(
            "is_true_equal_time_allocation_experiment", False
        ))
        for case in payload["cases"]
    )
    if partition == "heldout":
        criteria = manifest["success_criteria"]
        aggregate = payload["aggregate"]
        checks["angular_value_gate"] = aggregate["angular_geometric_mean_ratio"] <= criteria["angular_geometric_mean_ratio_max"]
        checks["physical_value_gate"] = aggregate["response_cases_improved_by_5pct"] >= criteria["minimum_total_cases_improved_by_5pct"]
        checks["median_value_gate"] = aggregate["response_error_median_ratio"] <= criteria["median_response_ratio_max"]
        checks["worst_degradation_gate"] = aggregate["worst_response_ratio"] <= criteria["worst_response_ratio_max"]
        uncertainty_rows = []
        for case in payload["cases"]:
            baseline_error = float(case["methods"]["moment_monotone_baseline"]["response_error"])
            optimized_error = float(case["methods"]["optimized_harmonic_fidelity"]["response_error"])
            uncertainty = float(case["reference"]["uncertainty"])
            difference = optimized_error - baseline_error
            uncertainty_rows.append(
                {
                    "id": str(case["id"]),
                    "optimized_minus_baseline_absolute_error": difference,
                    "reference_uncertainty": uncertainty,
                    "resolved_relative_to_reference_uncertainty": abs(difference) > uncertainty,
                }
            )
        checks["uncertainty_interpretation"] = uncertainty_rows
        checks["reference_resolved_case_count"] = sum(
            bool(row["resolved_relative_to_reference_uncertainty"])
            for row in uncertainty_rows
        )
    passed = all(
        bool(value)
        for key, value in checks.items()
        if key.endswith("gate") or key in {
            "manifest_match",
            "registry_match",
            "case_inventory",
            "same_node_comparisons",
            "same_space_energy",
            "complete_required_fields",
            "ablation_inventory",
            "quadrature_ablation_separate",
            "signed_scope_honest",
            "accelerator_inventory",
            "accelerator_fixed_point",
            "equal_wall_time_claim_honest",
        }
    )
    return {
        "schema": "afp-p2e-result-audit-v1",
        "partition": partition,
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "aggregate": payload["aggregate"],
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = json.loads(Path(args.results).read_text(encoding="utf-8"))
    audit = audit_results(payload)
    text = json.dumps(audit, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    print("P2E_RESULT_AUDIT_PASS" if audit["status"] == "PASS" else "P2E_RESULT_AUDIT_FAIL")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
