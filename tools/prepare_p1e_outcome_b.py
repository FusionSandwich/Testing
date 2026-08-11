#!/usr/bin/env python3
"""Normalize live-source wording before applying the Outcome B migration.

The preparation is deterministic and idempotent. It repairs strict migration
matchers to the exact authoritative-parent wording and makes publication-marker
checks insensitive to line wrapping and capitalization. It does not alter any
mathematical statement by itself.
"""

from __future__ import annotations

import argparse
from pathlib import Path


CHANGED: list[str] = []


def replace_once_or_present(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old in text:
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"{label}: expected one occurrence, found {count}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        CHANGED.append(path.as_posix())
        print(f"PREPARED {label}")
    elif new in text:
        print(f"ALREADY_PREPARED {label}")
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

    print(f"PREPARATION_CHANGED_COUNT {len(CHANGED)}")
    if args.check and CHANGED:
        raise SystemExit("Outcome B preparation is not yet applied")


if __name__ == "__main__":
    main()
