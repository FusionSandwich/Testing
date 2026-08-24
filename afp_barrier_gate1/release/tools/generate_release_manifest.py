"""Generate deterministic SHA-256 manifests for the AFP R8 release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[2]
REPOSITORY = PROJECT.parent
RELEASE = PROJECT / "release"
TEXT_MANIFEST = RELEASE / "RELEASE_MANIFEST.sha256"
JSON_MANIFEST = RELEASE / "RELEASE_MANIFEST.json"

EXCLUDED_NAMES = {
    TEXT_MANIFEST.name,
    JSON_MANIFEST.name,
}

OUTSIDE_RELEASE = [
    PROJECT / "AFPBarrier" / "ReleaseAxiomAudit.lean",
    PROJECT / "AFPBarrier" / "AxiomAudit.lean",
    PROJECT / "README.md",
    PROJECT / "GATE3.md",
    PROJECT / "GATE6.md",
    PROJECT / "docs" / "P4_THEOREM_TO_FILE_MAP.md",
    PROJECT / "gate6" / "MULTIGROUP_REPORT.md",
    PROJECT / "pure_math" / "covariance" / "P1E_COXETER_HARMONIC_CONSTRUCTION.md",
    PROJECT / "pure_math" / "covariance" / "P1E_STRATIFIED_LATTICE_REPAIR.md",
    PROJECT / "pure_math" / "covariance" / "P1E_STRUCTURED_STRESS_CONSTRUCTION.md",
    PROJECT / "pure_math" / "p2f_hts" / "audit.py",
    PROJECT / "pure_math" / "p2f_hts" / "model.py",
    PROJECT / "benchmarks" / "p2f" / "P2F_MANIFEST.json",
    PROJECT / "benchmarks" / "p2f" / "P2F_RESULTS.json",
    PROJECT / "benchmarks" / "p2f" / "P2F_AUDIT.json",
    PROJECT / "benchmarks" / "p2f" / "P2F_RECORDS.sha256",
    REPOSITORY / "docs" / "publication_program" / "THEOREM_REGISTRY.md",
    REPOSITORY / "docs" / "publication_program" / "P1E_SHORT_GAP_S2_CONSTRUCTION.md",
    REPOSITORY / "docs" / "publication_program" / "P2F_HTS_LAYERED_CASE.md",
    REPOSITORY
    / "docs"
    / "consolidation"
    / "audit"
    / "2026-08-10"
    / "workflow_artifacts"
    / "README.md",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "FLAGSHIP_MANUSCRIPT.md",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "P1F_REPRODUCIBILITY_MANIFEST.md",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "build_flagship_paper.py",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "table_layout.lua",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "priority_sources.bib",
    REPOSITORY
    / "docs"
    / "publication_program"
    / "p1f_manuscript"
    / "proof_dependency_graph.png",
    REPOSITORY / "output" / "pdf" / "FLAGSHIP_MANUSCRIPT.pdf",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    files = [
        path
        for path in RELEASE.rglob("*")
        if path.is_file()
        and path.name not in EXCLUDED_NAMES
        and "tmp" not in path.relative_to(RELEASE).parts
        and "__pycache__" not in path.parts
    ]
    files.extend(OUTSIDE_RELEASE)
    files = sorted(set(files), key=lambda path: path.relative_to(REPOSITORY).as_posix())
    missing = [path for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)

    records = []
    for path in files:
        records.append(
            {
                "path": path.relative_to(REPOSITORY).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    TEXT_MANIFEST.write_text(
        "".join(f"{row['sha256']}  {row['path']}\n" for row in records),
        encoding="utf-8",
        newline="\n",
    )
    JSON_MANIFEST.write_text(
        json.dumps(
            {
                "schema": "afp-r8-release-manifest-v1",
                "self_excluded": [TEXT_MANIFEST.name, JSON_MANIFEST.name],
                "file_count": len(records),
                "files": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"generated release manifest for {len(records)} files")


if __name__ == "__main__":
    main()
