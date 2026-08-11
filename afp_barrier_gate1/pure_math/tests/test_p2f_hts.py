from __future__ import annotations

import copy
import json
from pathlib import Path

from pure_math.p2f_hts.audit import (
    _classify_scientific_outcome as audit_classify_scientific_outcome,
    _hash as audit_hash,
    audit_results,
)
from pure_math.p2f_hts.model import (
    _classify_scientific_outcome as model_classify_scientific_outcome,
    build_manifest,
    run_p2f,
)


def test_p2f_manifest_keeps_neutral_and_afp_physics_separate() -> None:
    manifest = build_manifest()
    assert manifest["physics_firewall"]["neutral"] == "full positive Boltzmann kernel"
    assert manifest["physics_firewall"]["charged"] == "AFP/BFP only"
    assert {row["id"] for row in manifest["incidence_cases"]} == {"normal", "oblique", "grazing"}
    assert {row["material"] for row in manifest["layers"]} >= {
        "Cu", "Ag", "REBCO", "oxide_buffer", "Hastelloy_C276"
    }
    assert {row["nodes"] for row in manifest["angular_reference_sweep"]} == {50, 72, 98, 128}


def test_reference_failure_preempts_nominal_pairwise_improvement() -> None:
    kwargs = {
        "resolved_improvements": 1,
        "resolved_degradations": 0,
        "reference_converged": False,
        "operator_response_insensitive": False,
    }
    assert model_classify_scientific_outcome(**kwargs) == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"
    assert audit_classify_scientific_outcome(**kwargs) == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"


def test_p2f_full_run_is_structurally_valid_and_claim_honest() -> None:
    result = run_p2f()
    audit = audit_results(result)
    assert audit["status"] == "PASS"
    assert audit["checks"]["neutral_not_replaced"]
    assert audit["checks"]["pka_tensor_gate"]
    assert audit["checks"]["resolved_difference_count"] == 0
    assert audit["checks"]["resolved_improvement_count"] == 0
    assert audit["checks"]["resolved_degradation_count"] == 0
    assert audit["checks"]["operator_response_insensitive"]
    assert not audit["checks"]["grazing_reference_converged"]
    assert audit["checks"]["reference_linkage"]
    assert audit["scientific_outcome"] == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"

    threshold_tamper = copy.deepcopy(result)
    threshold_tamper["manifest"]["reference_convergence_relative_span_limit"] = 1.0
    threshold_scientific = dict(threshold_tamper)
    threshold_scientific.pop("scientific_sha256")
    threshold_tamper["scientific_sha256"] = audit_hash(threshold_scientific)
    threshold_audit = audit_results(threshold_tamper)
    assert threshold_audit["status"] == "FAIL"
    assert not threshold_audit["checks"]["reference_manifest"]

    comparison_tamper = copy.deepcopy(result)
    comparison_tamper["cases"][0]["comparisons"]["total_heating"]["baseline_absolute_error"] += 1.0
    comparison_scientific = dict(comparison_tamper)
    comparison_scientific.pop("scientific_sha256")
    comparison_tamper["scientific_sha256"] = audit_hash(comparison_scientific)
    comparison_audit = audit_results(comparison_tamper)
    assert comparison_audit["status"] == "FAIL"
    assert not comparison_audit["checks"]["comparison_consistency"]


def test_committed_p2f_result_reaudits() -> None:
    path = Path(__file__).parents[2] / "benchmarks" / "p2f" / "P2F_RESULTS.json"
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        audit = audit_results(payload)
        assert audit["status"] == "PASS"
        assert audit["scientific_outcome"] == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"
