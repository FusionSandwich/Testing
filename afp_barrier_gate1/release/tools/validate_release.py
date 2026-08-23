"""Fail-closed structural validation for the AFP R5 release."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
REPOSITORY = PROJECT.parent
RELEASE = PROJECT / "release"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    index = load_json(RELEASE / "LEAN_DECLARATION_INDEX.json")
    require(index["declaration_count"] == 512, "Lean declaration count")
    require(index["module_count"] == 58, "Lean module count")
    names = [row["name"] for row in index["declarations"]]
    require(len(names) == len(set(names)) == 512, "Lean declaration uniqueness")

    audit_source = (PROJECT / "AFPBarrier" / "ReleaseAxiomAudit.lean").read_text(
        encoding="utf-8"
    )
    require(audit_source.count("#check AFPBarrier.") == 512, "#check coverage")
    require(
        audit_source.count("#print axioms AFPBarrier.") == 512,
        "#print axioms coverage",
    )

    audit_log = (RELEASE / "LEAN_RELEASE_AUDIT.log").read_text(encoding="utf-8")
    require("error:" not in audit_log, "Lean audit error")
    require("sorryAx" not in audit_log, "Lean sorryAx dependency")
    checked = re.findall(r"(?m)^AFPBarrier\.([A-Za-z0-9_'.]+)", audit_log)
    require(len(checked) == 512, "Lean signature output count")
    axiom_results = re.findall(
        r"'AFPBarrier\.[^']+' (?:depends on axioms: \[[^]]*\]|does not depend on any axioms)",
        audit_log,
        flags=re.DOTALL,
    )
    require(len(axiom_results) == 512, "Lean axiom output count")
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    observed: set[str] = set()
    for result in axiom_results:
        if "depends on axioms:" in result:
            block = result.split("[", 1)[1].rsplit("]", 1)[0]
            observed.update(part.strip() for part in block.split(",") if part.strip())
    require(observed <= allowed, f"unexpected Lean axioms: {sorted(observed - allowed)}")

    p2f = load_json(PROJECT / "benchmarks" / "p2f" / "P2F_AUDIT.json")
    checks = p2f["checks"]
    require(p2f["status"] == "PASS", "P2F integrity status")
    require(
        p2f["scientific_outcome"] == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED",
        "P2F scientific classification",
    )
    require(checks["declared_bounded_dimensions"], "P2F declared dimensions")
    require("realistic_bounded_dimensions" not in checks, "stale P2F realism key")
    require(not checks["reference_convergence_gate"], "P2F reference must fail")
    require(checks["operator_response_insensitive"], "P2F sensitivity boundary")

    p2f_records = PROJECT / "benchmarks" / "p2f" / "P2F_RECORDS.sha256"
    record_lines = [line for line in p2f_records.read_text(encoding="utf-8").splitlines() if line]
    require(len(record_lines) == 14, "P2F record scope")
    for line in record_lines:
        digest, separator, relative = line.partition("  ")
        require(bool(separator), f"malformed P2F record: {line}")
        source = REPOSITORY / relative
        require(source.is_file(), f"missing P2F record: {relative}")
        require(sha256(source) == digest, f"P2F record hash mismatch: {relative}")

    flagship = (
        REPOSITORY
        / "docs"
        / "publication_program"
        / "p1f_manuscript"
        / "FLAGSHIP_MANUSCRIPT.md"
    ).read_text(encoding="utf-8")
    require("The `d=3` perturbation proposition" not in flagship, "stale Prop 7.3")
    require("Open problem 7.3" in flagship, "missing open robustness status")

    p1f_manifest = (
        REPOSITORY
        / "docs"
        / "publication_program"
        / "p1f_manuscript"
        / "P1F_REPRODUCIBILITY_MANIFEST.md"
    ).read_text(encoding="utf-8")
    p1f_paths = [
        REPOSITORY / "docs" / "publication_program" / "p1f_manuscript" / "FLAGSHIP_MANUSCRIPT.md",
        REPOSITORY / "docs" / "publication_program" / "p1f_manuscript" / "priority_sources.bib",
        REPOSITORY / "docs" / "publication_program" / "p1f_manuscript" / "proof_dependency_graph.png",
        REPOSITORY / "output" / "pdf" / "FLAGSHIP_MANUSCRIPT.pdf",
    ]
    for path in p1f_paths:
        require(sha256(path) in p1f_manifest, f"P1F manifest hash missing: {path.name}")
    pdf_bytes = p1f_paths[-1].read_bytes()
    require(b"/JavaScript" not in pdf_bytes, "PDF JavaScript")
    require(b"/Encrypt" not in pdf_bytes, "PDF encryption")

    stratified = (
        PROJECT
        / "pure_math"
        / "covariance"
        / "P1E_STRATIFIED_LATTICE_REPAIR.md"
    ).read_text(encoding="utf-8")
    require("FALSIFIED AT THE STATED SCOPE" in stratified, "rejected route banner")

    readme = (PROJECT / "README.md").read_text(encoding="utf-8")
    require("Lean-checked finite algebraic core" in readme, "formal scope title")

    numerical = (RELEASE / "NUMERICAL_DESIGN_PAPER.md").read_text(encoding="utf-8")
    require("P2F is intentionally excluded" in numerical, "P2F paper boundary")
    require("unresolved" in numerical, "P2E uncertainty boundary")

    required_release_files = {
        "REPRODUCIBILITY.md",
        "VALIDATION_REPORT.md",
        "FINAL_REPORT.md",
        "CLAIM_EVIDENCE_MATRIX.md",
        "COUNTEREXAMPLE_LEDGER.md",
        "SOURCE_OF_TRUTH_MAP.md",
    }
    missing_release_files = sorted(
        name for name in required_release_files if not (RELEASE / name).is_file()
    )
    require(not missing_release_files, f"missing release files: {missing_release_files}")

    print("AFP_R5_RELEASE_STRUCTURE_PASS")
    print(f"lean_declarations={len(names)}")
    print(f"lean_axioms={','.join(sorted(observed))}")
    print(f"p2f={p2f['scientific_outcome']}")


if __name__ == "__main__":
    main()
