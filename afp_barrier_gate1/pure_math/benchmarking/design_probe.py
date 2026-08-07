"""Pre-registration P2E operator-design probe on training-only fixtures.

This module is not publication evidence.  It compares the published-style
minimum-Euclidean-norm shared-conductance construction on the declared local
(Voronoi/weak-Delaunay) graph against the accepted P2A inner optimizer on an
augmented graph, always on identical nodes and masses.  Its sole purpose is
to select a frozen benchmark candidate before the immutable P2E manifest is
committed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import hashlib
import json
import math
import resource
import time
from typing import Callable

import numpy as np

from pure_math.codesign.families import (
    ahrens_beylkin_icosahedral_fixture,
    complete_edges,
    knn_edges,
    lebedev_14,
    product_rule,
    weak_delaunay_edges,
)
from pure_math.codesign.inner import solve_global_inner
from pure_math.codesign.metrics import apply_generator, generator_report, to_graph
from pure_math.codesign.rotations import signed_permutation_rotations
from pure_math.codesign.types import QuadratureCandidate, canonical_array_sha256


@dataclass(frozen=True)
class ProbeRow:
    family: str
    node_count: int
    baseline_edge_count: int
    optimized_edge_count: int
    baseline_status: str
    baseline_h1_residual: float | None
    baseline_min_conductance: float | None
    baseline_rate: float | None
    baseline_d2: float | None
    baseline_d3: float | None
    baseline_d4: float | None
    optimized_status: str
    optimized_rate_cap: float | None
    optimized_rate: float | None
    optimized_d2: float | None
    optimized_d3: float | None
    optimized_d4: float | None
    d2_ratio: float | None
    d3_ratio: float | None
    d4_ratio: float | None
    baseline_rotation_spread: float | None
    optimized_rotation_spread: float | None
    nodes_weights_sha256: str
    baseline_gamma_sha256: str | None
    optimized_gamma_sha256: str | None
    solve_seconds: float
    process_peak_rss_bytes: int
    note: str


def _pseudoinverse_baseline(candidate: QuadratureCandidate) -> tuple[np.ndarray, float]:
    graph = to_graph(candidate)
    matrix = np.asarray(graph.h1_matrix, dtype=float)
    rhs = np.asarray(graph.h1_rhs, dtype=float)
    gamma = np.linalg.pinv(matrix, rcond=1e-13) @ rhs
    residual = float(np.linalg.norm(matrix @ gamma - rhs, ord=np.inf))
    scale = max(1.0, float(np.linalg.norm(rhs, ord=np.inf)))
    if residual > 2e-10 * scale:
        raise RuntimeError(f"pseudoinverse moment residual {residual:.3e}")
    if float(np.min(gamma)) < -2e-10 * max(1.0, float(np.max(np.abs(gamma)))):
        raise RuntimeError(
            f"published-style pseudoinverse is nonmonotone: min={np.min(gamma):.3e}"
        )
    gamma = np.maximum(gamma, 0.0)
    return gamma, residual


def _candidate_with_edges(
    base: QuadratureCandidate,
    edges: list[tuple[int, int]],
    label: str,
) -> QuadratureCandidate:
    return QuadratureCandidate.build(
        f"{base.family}:{label}",
        base.nodes,
        base.weights,
        edges,
        metadata={**base.metadata, "p2e_probe_graph": label},
    )


def _probe_value(
    candidate: QuadratureCandidate,
    gamma: np.ndarray,
    direction: np.ndarray,
) -> float:
    # A directional H2 collision response.  It is not a streaming-ray metric.
    direction = direction / np.linalg.norm(direction)
    values = (candidate.nodes @ direction) ** 2 - 1.0 / 3.0
    action = apply_generator(candidate, gamma, values)
    return float(np.dot(candidate.weights * values, action))


def _rotation_spread(candidate: QuadratureCandidate, gamma: np.ndarray) -> float:
    values = []
    for rotation in signed_permutation_rotations():
        values.append(_probe_value(candidate, gamma, rotation @ np.array([0.0, 0.0, 1.0])))
    return float(max(values) - min(values))


def _families() -> tuple[tuple[str, Callable[[], QuadratureCandidate]], ...]:
    return (
        ("lebedev14", lambda: lebedev_14(graph="weak_delaunay")),
        ("icosahedral12", lambda: ahrens_beylkin_icosahedral_fixture(graph="weak_delaunay")),
        ("product_3x8", lambda: product_rule(3, 8, graph="weak_delaunay")),
        ("product_4x8", lambda: product_rule(4, 8, graph="weak_delaunay")),
        ("product_4x12", lambda: product_rule(4, 12, graph="weak_delaunay")),
    )


def _finite(value: float | None) -> float | None:
    if value is None:
        return None
    if not math.isfinite(value):
        return None
    return float(value)


def run_probe() -> dict[str, object]:
    rows: list[ProbeRow] = []
    for label, factory in _families():
        started = time.perf_counter()
        base = factory()
        base_hash = canonical_array_sha256({"nodes": base.nodes, "weights": base.weights})
        baseline_status = "VERIFIED_FLOAT"
        baseline_gamma: np.ndarray | None = None
        baseline_h1: float | None = None
        baseline_report = None
        baseline_rotation: float | None = None
        note_parts: list[str] = []
        try:
            baseline_gamma, baseline_h1 = _pseudoinverse_baseline(base)
            baseline_report = generator_report(base, baseline_gamma, (2, 3, 4))
            baseline_rotation = _rotation_spread(base, baseline_gamma)
        except Exception as error:  # deterministic diagnostic row, not silent fallback
            baseline_status = f"REJECTED:{type(error).__name__}"
            note_parts.append(str(error))

        local_edges = {tuple(map(int, edge)) for edge in base.edges}
        target_neighbors = min(10, base.node_count - 1)
        augmented_edges = sorted(local_edges | set(knn_edges(base.nodes, target_neighbors)))
        if len(augmented_edges) == len(local_edges) and base.node_count <= 36:
            augmented_edges = complete_edges(base.node_count)
        augmented = _candidate_with_edges(base, augmented_edges, "augmented")

        optimized_status = "NOT_RUN:NO_VALID_BASELINE"
        optimized_report = None
        optimized_gamma: np.ndarray | None = None
        optimized_rotation: float | None = None
        rate_cap: float | None = None
        if baseline_report is not None:
            # The cap is frozen from the baseline before optimization.  It is
            # deliberately not selected from the optimized result.
            rate_cap = max(4.0, 1.75 * baseline_report.rate_max)
            try:
                record = solve_global_inner(
                    augmented, rate_cap, degree=2, solver="CLARABEL"
                )
                optimized_gamma = np.asarray(record.result.gamma, dtype=float)
                optimized_report = generator_report(augmented, optimized_gamma, (2, 3, 4))
                optimized_rotation = _rotation_spread(augmented, optimized_gamma)
                optimized_status = "VERIFIED_FLOAT_P2A_INNER"
            except Exception as error:
                optimized_status = f"REJECTED:{type(error).__name__}"
                note_parts.append(str(error))

        elapsed = time.perf_counter() - started
        def shell(report: object | None, degree: int) -> float | None:
            return None if report is None else float(report.shell_defects[degree])
        baseline_d2 = shell(baseline_report, 2)
        optimized_d2 = shell(optimized_report, 2)
        baseline_d3 = shell(baseline_report, 3)
        optimized_d3 = shell(optimized_report, 3)
        baseline_d4 = shell(baseline_report, 4)
        optimized_d4 = shell(optimized_report, 4)
        ratio = lambda a, b: None if a is None or b is None or b <= 0 else float(a / b)
        rows.append(
            ProbeRow(
                label,
                base.node_count,
                base.edge_count,
                augmented.edge_count,
                baseline_status,
                _finite(baseline_h1),
                None if baseline_gamma is None else _finite(float(np.min(baseline_gamma))),
                None if baseline_report is None else _finite(baseline_report.rate_max),
                _finite(baseline_d2),
                _finite(baseline_d3),
                _finite(baseline_d4),
                optimized_status,
                _finite(rate_cap),
                None if optimized_report is None else _finite(optimized_report.rate_max),
                _finite(optimized_d2),
                _finite(optimized_d3),
                _finite(optimized_d4),
                ratio(optimized_d2, baseline_d2),
                ratio(optimized_d3, baseline_d3),
                ratio(optimized_d4, baseline_d4),
                _finite(baseline_rotation),
                _finite(optimized_rotation),
                base_hash,
                None if baseline_gamma is None else canonical_array_sha256({"gamma": baseline_gamma}),
                None if optimized_gamma is None else canonical_array_sha256({"gamma": optimized_gamma}),
                float(elapsed),
                int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
                " | ".join(note_parts),
            )
        )

    valid = [
        row for row in rows
        if row.d2_ratio is not None
        and row.optimized_status == "VERIFIED_FLOAT_P2A_INNER"
        and row.baseline_status == "VERIFIED_FLOAT"
    ]
    selected = None if not valid else min(
        valid,
        key=lambda row: (
            row.d2_ratio,
            row.optimized_rotation_spread or math.inf,
            row.node_count,
            row.family,
        ),
    ).family
    payload = {
        "schema": "afp-p2e-training-design-probe-v1",
        "scope": "TRAINING_ONLY_NOT_HELD_OUT_NOT_PUBLICATION_EVIDENCE",
        "selected_training_candidate": selected,
        "selection_rule": "minimum D2 ratio, then rotation spread, node count, family name",
        "rows": [asdict(row) for row in rows],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()
    payload = run_probe()
    rendered = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        from pathlib import Path
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if payload["selected_training_candidate"] is None:
        raise SystemExit("P2E_DESIGN_PROBE_NO_ADMISSIBLE_CANDIDATE")
    print("P2E_DESIGN_PROBE_PASS")


if __name__ == "__main__":
    main()
