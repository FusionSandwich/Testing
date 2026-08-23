#!/usr/bin/env python3
"""Validate the corrected flagship source, citations, and selected PDF binding."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]
MANUSCRIPT = REPOSITORY / "docs" / "publication_program" / "p1f_manuscript"
SOURCE = MANUSCRIPT / "FLAGSHIP_MANUSCRIPT.md"
BIBLIOGRAPHY = MANUSCRIPT / "priority_sources.bib"
RECORD = MANUSCRIPT / "P1F_REPRODUCIBILITY_MANIFEST.md"
FIGURE = MANUSCRIPT / "proof_dependency_graph.png"
PDF = REPOSITORY / "output" / "pdf" / "FLAGSHIP_MANUSCRIPT.pdf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    bibliography = BIBLIOGRAPHY.read_text(encoding="utf-8")
    record = RECORD.read_text(encoding="utf-8")
    cited = set(re.findall(r"@([A-Za-z0-9_:.+-]+)", source))
    entries = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography, re.MULTILINE))
    require(cited == entries, f"citation mismatch: cited={len(cited)} entries={len(entries)}")

    required_keys = {
        "P1A-QUOT",
        "P1A-2DEF",
        "P1B-SHARP",
        "P1B-EQUALITY",
        "P1C-LOCAL",
        "P1C-GLOBAL",
        "P1D-MASTER",
        "P1D-QUOTIENT",
        "P1E-POLYGON",
        "P1E-RING",
        "P1E-ROW",
        "F-CONSTRUCT",
    }
    require(all(key in source for key in required_keys), "claim-registry key missing")
    require("Open problem 7.3" in source, "robustness problem not open")
    require("The `d=3` perturbation proposition" not in source, "stale proposition wording")
    require("P1E_SHORT_GAP_S2_CANDIDATE_THEOREM" not in source, "candidate leak")
    for path in (SOURCE, BIBLIOGRAPHY, FIGURE, PDF):
        require(sha256(path) in record, f"unbound artifact: {path.name}")
    pdf = PDF.read_bytes()
    require(pdf.startswith(b"%PDF-"), "invalid PDF header")
    require(len(pdf) > 100_000, "unexpectedly small PDF")
    require(b"/JavaScript" not in pdf, "PDF JavaScript")
    require(b"/Encrypt" not in pdf, "PDF encryption")

    print("AFP_R6_FLAGSHIP_SOURCE_PASS")
    print(f"citations={len(cited)}")
    print(f"source_sha256={sha256(SOURCE)}")
    print(f"figure_sha256={sha256(FIGURE)}")
    print(f"pdf_sha256={sha256(PDF)}")


if __name__ == "__main__":
    main()
