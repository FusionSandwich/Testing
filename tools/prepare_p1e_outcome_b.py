#!/usr/bin/env python3
"""Prepare the authoritative live sources for the Outcome B migration.

The preparation is deterministic and idempotent. It aligns strict migration
matchers with the authoritative-parent wording, strengthens publication-marker
checks, and corrects two accepted-surface scope summaries that sit outside the
main migration table. Historical rejected-route documents are not rewritten.
"""

from __future__ import annotations

import argparse
from pathlib import Path


CHANGED: list[str] = []


def replace_once_or_present(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"ALREADY_PREPARED {label}")
    elif old in text:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"{label}: expected one occurrence, found {count}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        CHANGED.append(path.as_posix())
        print(f"PREPARED {label}")
    else:
        raise AssertionError(f"{label}: neither source nor prepared text found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()

    migration = root / "tools/apply_p1e_outcome_b.py"
    replace_once_or_present(
        migration,
        "a global six-moment right inverse is proved.",
        "a global six-moment right inverse with quantitative norm is later proved.",
        "P1E approach-registry matcher",
    )

    old_value_pattern = (
        '        r"The accepted `d=3` perturbation constants apply only to support-preserving\\n'
        'latitude perturbations with fixed combinatorial data\\. No exact-head workflow\\n'
        'status is inferred from these mathematical constants\\.",'
    )
    new_value_pattern = (
        '        r"The `d=3` perturbation constants apply only to support-preserving reflected\\n'
        'latitude perturbations with fixed combinatorial data\\. No exact-head workflow\\n'
        'execution, artifact digest, or frozen P1E commit is recorded in this value\\n'
        'table\\.",'
    )
    replace_once_or_present(
        migration,
        old_value_pattern,
        new_value_pattern,
        "value-registry matcher",
    )

    replace_once_or_present(
        migration,
        '    if "historical arithmetic regression; not a construction certificate" in text:\n',
        '    if "historical_exponent_recurrence" in text:\n',
        "independent-audit idempotence sentinel",
    )

    sampling_report = root / "docs/publication_program/p1f_manuscript/SAMPLING_ALIAS_EQUALITY_HOSTILE_REFEREE_REPORT.md"
    replace_once_or_present(
        sampling_report,
        "6. Robustness fixes support, counts, phases, masks, horizontal jumps and\n"
        "   reflection; arbitrary motion is not claimed.",
        "6. At each fixed level, the frozen-support reflected latitude perturbations\n"
        "   have an existential level-dependent persistence radius. Counts, phases,\n"
        "   masks, horizontal jumps, support, and reflection remain fixed; no radius\n"
        "   uniform in the level, mesh-power law, perturbed all-level constants, or\n"
        "   arbitrary motion is claimed.",
        "sampling-alias persistence boundary",
    )

    boundary_matrix = root / "docs/publication_program/PAPER_BOUNDARY_MATRIX.md"
    replace_once_or_present(
        boundary_matrix,
        "| structured robustness | construction stability boundary | mesh diagnostic | none | fixed counts, phases, masks, horizontal jumps, reflection and a common rotation | independent longitude or arbitrary node motion is outside the theorem | I |",
        "| fixed-level local persistence | construction stability boundary | mesh diagnostic | none | for each fixed `J`, frozen counts, phases, masks, horizontal jumps, support, reflection and a common rotation; existential `delta_J` | no radius uniform in `J`, no mesh-power law or perturbed all-level constants; independent longitude and arbitrary node motion are outside the theorem | I |",
        "paper-boundary persistence row",
    )

    verifier = root / "afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py"
    old_marker_loop = (
        "    for relative, markers in requirements.items():\n"
        "        text = read_text(root, relative)\n"
        "        for marker in markers:\n"
        "            if marker not in text:\n"
        "                raise AssertionError(f\"missing marker in {relative}: {marker!r}\")\n"
    )
    new_marker_loop = (
        "    for relative, markers in requirements.items():\n"
        "        text = read_text(root, relative)\n"
        "        normalized_text = \" \".join(text.split()).casefold()\n"
        "        for marker in markers:\n"
        "            normalized_marker = \" \".join(marker.split()).casefold()\n"
        "            if marker not in text and normalized_marker not in normalized_text:\n"
        "                raise AssertionError(f\"missing marker in {relative}: {marker!r}\")\n"
    )
    replace_once_or_present(
        verifier,
        old_marker_loop,
        new_marker_loop,
        "publication-marker normalization",
    )

    old_requirements_tail = (
        '        "docs/publication_program/P1E_PROP73_APPROACH_REGISTRY.md": (\n'
        '            "OUTCOME B SELECTED",\n'
        '            "literal expression DAG absent",\n'
        '            "fixed-level continuity",\n'
        '        ),\n'
        '    }\n'
    )
    new_requirements_tail = (
        '        "docs/publication_program/P1E_PROP73_APPROACH_REGISTRY.md": (\n'
        '            "OUTCOME B SELECTED",\n'
        '            "literal expression DAG absent",\n'
        '            "fixed-level continuity",\n'
        '        ),\n'
        '        "docs/publication_program/p1f_manuscript/SAMPLING_ALIAS_EQUALITY_HOSTILE_REFEREE_REPORT.md": (\n'
        '            "existential level-dependent persistence radius",\n'
        '            "no radius uniform in the level",\n'
        '        ),\n'
        '        "docs/publication_program/PAPER_BOUNDARY_MATRIX.md": (\n'
        '            "| fixed-level local persistence |",\n'
        '            "existential `delta_J`",\n'
        '            "no radius uniform in `J`",\n'
        '        ),\n'
        '    }\n'
    )
    replace_once_or_present(
        verifier,
        old_requirements_tail,
        new_requirements_tail,
        "accepted-surface persistence markers",
    )

    finalizer = root / "tools/finalize_p1e_repair.py"
    replace_once_or_present(
        finalizer,
        '    "tools/apply_p1e_outcome_b.py",\n',
        '    "tools/prepare_p1e_outcome_b.py",\n    "tools/apply_p1e_outcome_b.py",\n',
        "preparation-helper reproducibility hash",
    )

    print(f"PREPARATION_CHANGED_COUNT {len(CHANGED)}")
    if args.check and CHANGED:
        raise SystemExit("Outcome B preparation is not yet applied")


if __name__ == "__main__":
    main()
