"""Deterministic training, validation, and held-out P2E execution."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import resource
import time
from typing import Any

import numpy as np
import scipy

from .ablations import run_ablations
from .cases import accelerator_ablation, run_case
from .manifest import load_manifest, scientific_hash
from .operators import load_frozen_operators


def _strict_dump(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _aggregate(cases: list[dict[str, Any]]) -> dict[str, Any]:
    response_ratios = np.asarray(
        [case["optimized_to_baseline_response_error_ratio"] for case in cases], dtype=float
    )
    aggregate_ratios = np.asarray(
        [case["optimized_to_baseline_aggregate_error_ratio"] for case in cases], dtype=float
    )
    angular = response_ratios[:3]
    physical = response_ratios[3:]
    return {
        "case_count": len(cases),
        "response_error_geometric_mean_ratio": float(np.exp(np.mean(np.log(np.maximum(response_ratios, 1e-300))))),
        "aggregate_error_geometric_mean_ratio": float(np.exp(np.mean(np.log(np.maximum(aggregate_ratios, 1e-300))))),
        "response_error_median_ratio": float(np.median(response_ratios)),
        "response_cases_improved": int(np.sum(response_ratios < 1.0)),
        "response_cases_improved_by_5pct": int(np.sum(response_ratios <= 0.95)),
        "angular_geometric_mean_ratio": float(np.exp(np.mean(np.log(np.maximum(angular, 1e-300))))),
        "physical_geometric_mean_ratio": float(np.exp(np.mean(np.log(np.maximum(physical, 1e-300))))),
        "worst_response_ratio": float(np.max(response_ratios)),
        "best_response_ratio": float(np.min(response_ratios)),
    }


def run_partition(
    partition: str,
    output: str | Path,
    *,
    case_ids: list[str] | None = None,
) -> dict[str, Any]:
    manifest = load_manifest()
    if partition not in {"training", "validation", "heldout"}:
        raise ValueError("partition must be training, validation, or heldout")
    expected = list(manifest["partitions"][partition])
    selected = expected if case_ids is None else list(case_ids)
    if any(case not in expected for case in selected):
        raise ValueError("requested case is not in the selected partition")
    ops = load_frozen_operators()
    started = time.perf_counter()
    cases = [run_case(case, ops, partition) for case in selected]
    accelerator = accelerator_ablation(ops)
    ablations = run_ablations(ops, partition)
    payload: dict[str, Any] = {
        "schema": "afp-p2e-benchmark-results-v1",
        "partition": partition,
        "manifest_sha256": manifest["scientific_sha256"],
        "operator_registry_sha256": ops.registry["scientific_sha256"],
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "cases": cases,
        "accelerator_only_ablation": accelerator,
        "ablations": ablations,
        "aggregate": _aggregate(cases),
        "elapsed_seconds": float(time.perf_counter() - started),
        "process_peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
    }
    scientific = dict(payload)
    scientific.pop("elapsed_seconds")
    scientific.pop("process_peak_rss_bytes")
    scientific["software"] = {"model": "frozen by manifest"}
    payload["scientific_sha256"] = scientific_hash(scientific)
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    _strict_dump(target, payload)
    return payload


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("partition", choices=("training", "validation", "heldout"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    payload = run_partition(args.partition, args.output)
    print(json.dumps(payload["aggregate"], indent=2, sort_keys=True))
    print(f"P2E_{args.partition.upper()}_PASS")


if __name__ == "__main__":
    main()
