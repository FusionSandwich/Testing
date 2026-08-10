from __future__ import annotations

import json
from pathlib import Path

from pure_math.p2f_hts.audit import audit_results
from pure_math.p2f_hts.model import build_manifest, run_p2f


def test_p2f_manifest_keeps_neutral_and_afp_physics_separate() -> None:
    manifest = build_manifest()
    assert manifest["physics_firewall"]["neutral"] == "full positive Boltzmann kernel"
    assert manifest["physics_firewall"]["charged"] == "AFP/BFP only"
    assert {row["id"] for row in manifest["incidence_cases"]} == {"normal", "oblique", "grazing"}
    assert {row["material"] for row in manifest["layers"]} >= {
        "Cu", "Ag", "REBCO", "oxide_buffer", "Hastelloy_C276"
    }


def test_p2f_full_run_is_structurally_valid_and_claim_honest() -> None:
    result = run_p2f()
    audit = audit_results(result)
    assert audit["status"] == "PASS"
    assert audit["checks"]["neutral_not_replaced"]
    assert audit["checks"]["pka_tensor_gate"]
    assert audit["scientific_outcome"] in {"BOUNDED_POSITIVE", "BOUNDED_NEGATIVE"}


def test_committed_p2f_result_reaudits() -> None:
    path = Path(__file__).parents[2] / "benchmarks" / "p2f" / "P2F_RESULTS.json"
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert audit_results(payload)["status"] == "PASS"
