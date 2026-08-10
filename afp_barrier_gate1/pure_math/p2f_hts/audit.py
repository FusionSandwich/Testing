"""Fail-closed structural and claim audit for P2F HTS results."""
from __future__ import annotations

import argparse
import hashlib
import json
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


def _hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def audit_results(payload: dict[str, Any]) -> dict[str, Any]:
    claimed = str(payload["scientific_sha256"])
    scientific = dict(payload)
    scientific.pop("scientific_sha256")
    checks: dict[str, Any] = {
        "scientific_hash": _hash(scientific) == claimed,
        "schema": payload.get("schema") == "afp-p2f-hts-results-v1",
    }
    manifest = payload["manifest"]
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
        set(case["fine_reference"]["responses"]) == EXPECTED_RESPONSES
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
    resolved = sum(
        int(row["resolved_improvement"])
        for case in cases
        for row in case["comparisons"].values()
    )
    checks["resolved_improvement_count"] = resolved
    checks["outcome_consistency"] = (
        int(payload["summary"]["resolved_improvement_count"]) == resolved
        and payload["summary"]["scientific_outcome"]
        == ("BOUNDED_POSITIVE" if resolved else "BOUNDED_NEGATIVE")
    )
    integrity_keys = [
        "scientific_hash", "schema", "layer_inventory", "realistic_bounded_dimensions",
        "incidence_inventory", "grazing_case", "physics_firewall", "case_inventory",
        "same_discretization", "neutral_not_replaced", "positivity_gate", "balance_gate",
        "response_inventory", "reference_uncertainty_separated", "layer_outputs",
        "pka_tensor_gate", "operator_invariants", "outcome_consistency",
    ]
    passed = all(bool(checks[key]) for key in integrity_keys)
    return {
        "schema": "afp-p2f-hts-audit-v1",
        "status": "PASS" if passed else "FAIL",
        "scientific_outcome": payload["summary"]["scientific_outcome"],
        "checks": checks,
        "claim_boundary": (
            "Integrity PASS does not imply physical superiority. A BOUNDED_NEGATIVE outcome "
            "forbids an HTS response-benefit claim."
        ),
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
