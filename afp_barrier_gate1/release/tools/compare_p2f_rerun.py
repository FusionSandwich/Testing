#!/usr/bin/env python3
"""Compare a P2F rerun to the selected record without hiding float drift."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[2]
SELECTED = PROJECT / "benchmarks" / "p2f" / "P2F_RESULTS.json"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: compare_p2f_rerun.py RERUN.json")
    selected = json.loads(SELECTED.read_text(encoding="utf-8"))
    rerun = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    float_differences: list[tuple[float, float, str, float, float]] = []
    nonfloat_differences: list[str] = []

    def walk(left: object, right: object, path: str) -> None:
        if isinstance(left, dict) and isinstance(right, dict):
            if set(left) != set(right):
                nonfloat_differences.append(f"{path}: key mismatch")
                return
            for key in sorted(left):
                if key == "scientific_sha256":
                    continue
                walk(left[key], right[key], f"{path}.{key}")
            return
        if isinstance(left, list) and isinstance(right, list):
            if len(left) != len(right):
                nonfloat_differences.append(f"{path}: length mismatch")
                return
            for index, (a, b) in enumerate(zip(left, right, strict=True)):
                walk(a, b, f"{path}[{index}]")
            return
        if isinstance(left, float) and isinstance(right, float):
            absolute = abs(left - right)
            relative = absolute / max(abs(left), abs(right), 1e-300)
            if absolute:
                float_differences.append((absolute, relative, path, left, right))
            return
        if left != right:
            nonfloat_differences.append(f"{path}: {left!r} != {right!r}")

    walk(selected, rerun, "root")
    float_differences.sort(reverse=True)
    largest = float_differences[0] if float_differences else (0.0, 0.0, "none", 0.0, 0.0)
    require_same_outcome = (
        selected["summary"]["scientific_outcome"]
        == rerun["summary"]["scientific_outcome"]
        == "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"
    )
    if not require_same_outcome:
        raise SystemExit("P2F classification mismatch")
    print("P2F_RERUN_CLASSIFICATION_MATCH")
    print(f"nonfloat_field_differences={len(nonfloat_differences)}")
    for difference in nonfloat_differences:
        print(f"nonfloat_difference={difference}")
    print(f"differing_float_fields={len(float_differences)}")
    print(f"max_absolute_difference={largest[0]:.17g}")
    print(f"max_relative_difference={largest[1]:.17g}")
    print(f"max_difference_path={largest[2]}")
    print(f"selected_scientific_sha256={selected['scientific_sha256']}")
    print(f"rerun_scientific_sha256={rerun['scientific_sha256']}")


if __name__ == "__main__":
    main()
