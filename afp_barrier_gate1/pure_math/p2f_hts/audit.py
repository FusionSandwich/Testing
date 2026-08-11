"""Fail-closed structural and scientific-claim audit for P2F HTS results."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


EXPECTED_LAYERS = {
    "Cu_front", "Ag_cap", "REBCO", "oxide_buffer", "Hastelloy_C276", "Cu_back"
}
EXPECTED_RESPONSES = {
    "REBCO_charged_heating",
    "REBCO_charged_q_normal",
    "REBCO_charged_scalar",
    "total_heating",
    "charged_escape",
    "substrate_total_PKA_source",
}
EXPECTED_REFERENCE_NODES = {"50", "72", "98", "128"}


def _hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _relative_difference(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0e-300)
    return abs(left - right) / scale


def _classify_scientific_outcome(
    *,
    resolved_improvements: int,
    resolved_degradations: int,
    reference_converged: bool,
    operator_response_insensitive: bool,
) -> str:
    if not reference_converged:
        return "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"
    if resolved_improvements and resolved_degradations:
        return "MIXED_RESOLVED_RESPONSE_CHANGES"
    if resolved_improvements:
        return "RESOLVED_IMPROVEMENT_PRESENT"
    if resolved_degradations:
        return "RESOLVED_DEGRADATION_PRESENT"
    if operator_response_insensitive:
        return "INCONCLUSIVE_OPERATOR_INSENSITIVE"
    return "INCONCLUSIVE_BELOW_REFERENCE_RESOLUTION"


def audit_results(payload: dict[str, Any]) -> dict[str, Any]:
    claimed = str(payload["scientific_sha256"])
    scientific = dict(payload)
    scientific.pop("scientific_sha256")
    checks: dict[str, Any] = {
        "scientific_hash": _hash(scientific) == claimed,
        "schema": payload.get("schema") == "afp-p2f-hts-results-v2",
    }

    manifest = payload["manifest"]
    checks["manifest_schema"] = manifest.get("schema") == "afp-p2f-hts-manifest-v2"
    layers = manifest["layers"]
    checks["layer_inventory"] = {row["name"] for row in layers} == EXPECTED_LAYERS
    thickness = {row["name"]: float(row["thickness_um"]) for row in layers}
    checks["realistic_bounded_dimensions"] = (
        10.0 <= thickness["Cu_front"] <= 50.0
        and 0.5 <= thickness["Ag_cap"] <= 5.0
        and 0.5 <= thickness["REBCO"] <= 3.0
        and 0.05 <= thickness["oxide_buffer"] <= 1.0
        and 30.0 <= thickness["Hastelloy_C276"] <= 100.0
        and 10.0 <= thickness["Cu_back"] <= 50.0
    )
    incidence = {row["id"]: float(row["polar_degrees"]) for row in manifest["incidence_cases"]}
    checks["incidence_inventory"] = set(incidence) == {"normal", "oblique", "grazing"}
    checks["grazing_case"] = incidence.get("grazing", 0.0) >= 80.0
    reference_specs = manifest["angular_reference_sweep"]
    checks["reference_manifest"] = (
        {str(int(row["nodes"])) for row in reference_specs} == EXPECTED_REFERENCE_NODES
        and all(int(row["n_mu"]) * int(row["n_phi"]) == int(row["nodes"]) for row in reference_specs)
        and int(manifest["production_nodes"]) == 32
        and int(manifest["nominal_reference_nodes"]) == 72
        and int(manifest["medium_reference_nodes"]) == 50
        and math.isclose(float(manifest["reference_convergence_relative_span_limit"]), 0.05)
        and math.isclose(float(manifest["operator_response_relative_difference_tolerance"]), 1.0e-10)
        and int(manifest["record_float_significant_digits"]) == 12
        and math.isclose(float(manifest["record_zero_threshold"]), 1.0e-18)
        and manifest["record_blas_core"] == "Haswell"
    )
    firewall = manifest["physics_firewall"]
    checks["physics_firewall"] = (
        firewall["neutral"] == "full positive Boltzmann kernel"
        and firewall["charged"] == "AFP/BFP only"
        and "DPA" in firewall["excluded"]
        and "Jc" in firewall["excluded"]
    )

    cases = payload["cases"]
    checks["case_inventory"] = [case["id"] for case in cases] == ["normal", "oblique", "grazing"]
    checks["same_discretization"] = all(
        case["same_nodes_between_methods"]
        and case["same_spatial_energy_discretization"]
        for case in cases
    )
    checks["neutral_not_replaced"] = all(
        case["neutral_operator_identical_between_methods"]
        and all(
            result["neutral"]["operator"]
            == "full positive reversible Boltzmann kernels; never replaced by AFP"
            for result in case["methods"].values()
        )
        for case in cases
    )
    minimum_flux = min(
        float(field["minimum_flux"])
        for case in cases
        for result in case["methods"].values()
        for field in (result["neutral"], result["charged"])
    )
    maximum_balance = max(
        float(field["maximum_balance_residual"])
        for case in cases
        for result in case["methods"].values()
        for field in (result["neutral"], result["charged"])
    )
    checks["minimum_flux"] = minimum_flux
    checks["maximum_balance_residual"] = maximum_balance
    checks["positivity_gate"] = minimum_flux >= -2.0e-10
    checks["balance_gate"] = maximum_balance <= 5.0e-8
    checks["response_inventory"] = all(
        set(case["nominal_reference"]["responses"]) == EXPECTED_RESPONSES
        and set(case["comparisons"]) == EXPECTED_RESPONSES
        for case in cases
    )
    checks["reference_uncertainty_separated"] = all(
        abs(
            float(row["reference_uncertainty"]["conservative_sum"])
            - float(row["reference_uncertainty"]["angular_component"])
            - float(row["reference_uncertainty"]["spatial_component"])
        ) <= 1e-14
        for case in cases
        for row in case["comparisons"].values()
    )
    checks["layer_outputs"] = all(
        set(result["layers"]) == EXPECTED_LAYERS
        and set(result["species_resolved_pka"]) == EXPECTED_LAYERS
        and bool(result["charged_interface_crossing"])
        for case in cases
        for result in case["methods"].values()
    )

    tensors_valid = True
    for case in cases:
        for result in case["methods"].values():
            for layer_species in result["species_resolved_pka"].values():
                for row in layer_species.values():
                    tensor = np.asarray(row["directional_tensor"], dtype=float)
                    tensors_valid = tensors_valid and (
                        tensor.shape == (3, 3)
                        and np.linalg.norm(tensor - tensor.T, ord=np.inf) <= 1e-12
                        and float(np.min(np.linalg.eigvalsh(0.5 * (tensor + tensor.T)))) >= -1e-12
                        and float(row["total_source"]) >= 0.0
                    )
    checks["pka_tensor_gate"] = tensors_valid

    audits = payload["production_operator_audits"]
    checks["operator_invariants"] = all(
        bool(row["positive"])
        and float(row["h0_residual"]) <= 5e-9
        and float(row["h1_residual"]) <= 5e-7
        and float(row["reversibility_residual"]) <= 5e-9
        for row in audits.values()
    )

    span_limit = float(manifest["reference_convergence_relative_span_limit"])
    reference_consistent = True
    reference_inventory = True
    for case in cases:
        sweep = case["angular_reference_sweep"]
        reference_inventory = reference_inventory and set(sweep) == EXPECTED_REFERENCE_NODES
        stored = case["reference_convergence"]
        case_gate = True
        for response in EXPECTED_RESPONSES:
            values = [float(sweep[key]["responses"][response]) for key in ("50", "72", "98", "128")]
            scale = max(max(abs(value) for value in values), 1.0e-300)
            relative_span = (max(values) - min(values)) / scale
            converged = relative_span <= span_limit
            stored_row = stored["responses"][response]
            reference_consistent = reference_consistent and math.isclose(
                float(stored_row["relative_span"]), relative_span, rel_tol=5e-9, abs_tol=1e-13
            ) and bool(stored_row["converged"]) == converged
            case_gate = case_gate and converged
        reference_consistent = reference_consistent and (
            bool(stored["all_responses_converged"]) == case_gate
            and math.isclose(float(stored["relative_span_limit"]), span_limit)
        )
    checks["reference_sweep_inventory"] = reference_inventory
    checks["reference_convergence_consistency"] = reference_consistent
    reference_convergence_gate = all(
        bool(case["reference_convergence"]["all_responses_converged"])
        for case in cases
    )
    checks["reference_convergence_gate"] = reference_convergence_gate
    grazing = next(case for case in cases if case["id"] == "grazing")
    checks["grazing_reference_converged"] = bool(
        grazing["reference_convergence"]["all_responses_converged"]
    )

    comparison_rows = [row for case in cases for row in case["comparisons"].values()]
    comparison_consistent = True
    reference_linkage = True
    for case in cases:
        sweep = case["angular_reference_sweep"]
        for response in EXPECTED_RESPONSES:
            nominal_response = float(case["nominal_reference"]["responses"][response])
            medium_response = float(case["medium_angular_reference"]["responses"][response])
            spatial_response = float(case["coarse_spatial_reference"]["responses"][response])
            reference_linkage = reference_linkage and (
                math.isclose(nominal_response, float(sweep["72"]["responses"][response]), rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(medium_response, float(sweep["50"]["responses"][response]), rel_tol=5e-9, abs_tol=1e-13)
            )

            row = case["comparisons"][response]
            baseline_response = float(row["baseline_response"])
            optimized_response = float(row["optimized_response"])
            absolute_difference = abs(baseline_response - optimized_response)
            relative_difference = _relative_difference(baseline_response, optimized_response)
            baseline_error = abs(baseline_response - nominal_response)
            optimized_error = abs(optimized_response - nominal_response)
            angular_component = abs(nominal_response - medium_response)
            spatial_component = abs(nominal_response - spatial_response)
            conservative_sum = angular_component + spatial_component
            stored_uncertainty = row["reference_uncertainty"]
            response_reference_converged = bool(
                case["reference_convergence"]["responses"][response]["converged"]
            )
            resolved = response_reference_converged and (
                abs(baseline_error - optimized_error) > conservative_sum
            )
            comparison_consistent = comparison_consistent and (
                math.isclose(float(row["method_absolute_difference"]), absolute_difference, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(row["method_relative_difference"]), relative_difference, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(row["baseline_absolute_error"]), baseline_error, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(row["optimized_absolute_error"]), optimized_error, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(stored_uncertainty["angular_component"]), angular_component, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(stored_uncertainty["spatial_component"]), spatial_component, rel_tol=5e-9, abs_tol=1e-13)
                and math.isclose(float(stored_uncertainty["conservative_sum"]), conservative_sum, rel_tol=5e-9, abs_tol=1e-13)
                and bool(stored_uncertainty["nominal_reference_converged"]) == response_reference_converged
                and bool(row["difference_resolved_by_reference"]) == resolved
                and bool(row["resolved_improvement"]) == bool(resolved and optimized_error < baseline_error)
                and bool(row["resolved_degradation"]) == bool(resolved and optimized_error > baseline_error)
            )
    checks["reference_linkage"] = reference_linkage
    checks["comparison_consistency"] = comparison_consistent

    resolved_improvements = sum(int(row["resolved_improvement"]) for row in comparison_rows)
    resolved_degradations = sum(int(row["resolved_degradation"]) for row in comparison_rows)
    resolved_differences = sum(int(row["difference_resolved_by_reference"]) for row in comparison_rows)
    maximum_method_relative_difference = max(float(row["method_relative_difference"]) for row in comparison_rows)
    operator_tolerance = float(manifest["operator_response_relative_difference_tolerance"])
    operator_response_insensitive = maximum_method_relative_difference <= operator_tolerance
    expected_outcome = _classify_scientific_outcome(
        resolved_improvements=resolved_improvements,
        resolved_degradations=resolved_degradations,
        reference_converged=reference_convergence_gate,
        operator_response_insensitive=operator_response_insensitive,
    )

    checks["resolved_improvement_count"] = resolved_improvements
    checks["resolved_degradation_count"] = resolved_degradations
    checks["resolved_difference_count"] = resolved_differences
    checks["operator_response_max_relative_difference"] = maximum_method_relative_difference
    checks["operator_response_insensitive"] = operator_response_insensitive
    summary = payload["summary"]
    checks["outcome_consistency"] = (
        int(summary["resolved_improvement_count"]) == resolved_improvements
        and int(summary["resolved_degradation_count"]) == resolved_degradations
        and int(summary["resolved_difference_count"]) == resolved_differences
        and int(summary["response_comparison_count"]) == len(comparison_rows)
        and bool(summary["reference_convergence_gate"]) == reference_convergence_gate
        and math.isclose(
            float(summary["operator_response_max_relative_difference"]),
            maximum_method_relative_difference,
            rel_tol=5e-9,
            abs_tol=1e-13,
        )
        and bool(summary["operator_response_insensitive"]) == operator_response_insensitive
        and summary["scientific_outcome"] == expected_outcome
    )

    integrity_keys = [
        "scientific_hash", "schema", "manifest_schema", "layer_inventory",
        "realistic_bounded_dimensions", "incidence_inventory", "grazing_case",
        "reference_manifest", "physics_firewall", "case_inventory",
        "same_discretization", "neutral_not_replaced", "positivity_gate", "balance_gate",
        "response_inventory", "reference_uncertainty_separated", "layer_outputs",
        "pka_tensor_gate", "operator_invariants", "reference_sweep_inventory",
        "reference_convergence_consistency", "reference_linkage",
        "comparison_consistency", "outcome_consistency",
    ]
    passed = all(bool(checks[key]) for key in integrity_keys)

    if expected_outcome == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED":
        claim_boundary = (
            "Integrity PASS does not imply a transport-performance conclusion. The angular "
            "reference sweep fails the declared convergence gate, and no baseline/optimized "
            "difference is resolved; the P2F transfer experiment is inconclusive."
        )
    elif expected_outcome == "INCONCLUSIVE_OPERATOR_INSENSITIVE":
        claim_boundary = (
            "Integrity PASS does not imply physical superiority. The selected responses are "
            "insensitive to the operator replacement at the declared tolerance."
        )
    else:
        claim_boundary = (
            "Integrity PASS validates the record and classification logic only. Any response "
            "claim is limited to differences resolved by a converged declared reference."
        )

    return {
        "schema": "afp-p2f-hts-audit-v2",
        "status": "PASS" if passed else "FAIL",
        "scientific_outcome": expected_outcome,
        "checks": checks,
        "claim_boundary": claim_boundary,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.results).read_text(encoding="utf-8"))
    audit = audit_results(payload)
    Path(args.output).write_text(
        json.dumps(audit, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(audit["status"])
    print(audit["scientific_outcome"])
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
