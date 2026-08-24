"""Fail-closed structural validation for the AFP R7 release."""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
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
    require("Corollary 6.3" not in flagship, "unauditable Corollary 6.3 survived")
    require(
        "Conditional transfers from the defect budget (discussion)" in flagship,
        "missing demoted stability-transfer discussion",
    )
    require(
        "computer-assisted exact-rational theorem" in flagship,
        "Theorem 7.2 certificate boundary is not explicit",
    )
    require(
        "For every integer $J\\ge1$" in flagship,
        "Theorem 7.2 discrete sequence is not explicit",
    )
    require("e^{-513/M_0}" in flagship, "corrected transition-product lower bound")
    require(
        "exact weighted decomposition of the frontier excess" not in flagship.lower(),
        "false frontier-excess decomposition wording",
    )

    supplement = (
        REPOSITORY / "docs" / "publication_program" / "P1E_SHORT_GAP_S2_CONSTRUCTION.md"
    ).read_text(encoding="utf-8")
    require("\\gamma_{ij}={\\Gamma_{ij}\\over W}" in supplement, "P1E Gamma/W normalization")
    require("e^{-513/M_0}" in supplement, "P1E corrected transition-product bound")

    certificate_dir = RELEASE / "certificates" / "theorem_7_2"
    certificate = load_json(certificate_dir / "certificate.json")
    require(
        certificate["classification"] == "COMPUTER_ASSISTED_EXACT_RATIONAL",
        "Theorem 7.2 certificate classification",
    )
    require(
        certificate["schema"] == "afp-theorem-7.2-exact-rational-certificate-v2",
        "Theorem 7.2 certificate schema",
    )
    require(
        certificate["claim_boundary"]["whole_theorem_machine_verified"] is False,
        "whole-theorem certificate overclaim",
    )
    verifier = certificate_dir / "verify_certificate.py"
    verified = subprocess.run(
        [sys.executable, str(verifier), str(certificate_dir / "certificate.json")],
        cwd=REPOSITORY,
        check=False,
        capture_output=True,
        text=True,
    )
    require(verified.returncode == 0, f"Theorem 7.2 verifier failed: {verified.stderr}")
    require(
        "Theorem 7.2 exact-rational certificate: PASS" in verified.stdout,
        "Theorem 7.2 verifier pass marker",
    )
    require(
        "hostile_mutations=3/3 rejected" in verified.stdout,
        "Theorem 7.2 mutation-test marker",
    )

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
        "HOSTILE_AI_REVIEW_R7_RESPONSE.md",
    }
    missing_release_files = sorted(
        name for name in required_release_files if not (RELEASE / name).is_file()
    )
    require(not missing_release_files, f"missing release files: {missing_release_files}")

    response = (RELEASE / "HOSTILE_AI_REVIEW_R7_RESPONSE.md").read_text(encoding="utf-8")
    require("internal AI adversarial review" in response, "review identity boundary")
    require("not identifiable external human peer review" in response, "human-review firewall")
    require("Blocker 1" in response and "Blocker 4" in response, "four-blocker response")

    print("AFP_R7_RELEASE_STRUCTURE_PASS")
    print(f"lean_declarations={len(names)}")
    print(f"lean_axioms={','.join(sorted(observed))}")
    print(f"p2f={p2f['scientific_outcome']}")
    print("theorem_7_2=COMPUTER_ASSISTED_EXACT_RATIONAL")


if __name__ == "__main__":
    main()
