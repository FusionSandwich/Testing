"""Build the frozen P2E operator registry using training-only diagnostics.

The output of this module is intended to be committed verbatim in the later
immutable preregistration commit.  It never imports or evaluates any held-out
benchmark response.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import resource
import time
from typing import Any, Iterable

import numpy as np

from pure_math.codesign.families import knn_edges, product_rule
from pure_math.codesign.inner import build_inner_model, solve_global_inner
from pure_math.codesign.metrics import generator_report, to_graph
from pure_math.codesign.types import QuadratureCandidate, canonical_array_sha256
from pure_math.optimization import DesignRequest, SolverConfig, solve_design


@dataclass(frozen=True)
class FrozenMethodSummary:
    name: str
    role: str
    graph_label: str
    node_count: int
    edge_count: int
    rate_cap: float | None
    rate_max: float
    shell_defects: dict[str, float]
    training_rotation_spread: float
    minimum_conductance: float
    maximum_conductance: float
    gamma_sha256: str
    solver: str
    solver_status: str
    certificate_level: str
    primal_passed: bool
    dual_passed: bool | None
    objective_interval: list[float] | None
    positivity_expected: bool
    note: str


def _strict_json(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _pseudoinverse(candidate: QuadratureCandidate) -> np.ndarray:
    graph = to_graph(candidate)
    matrix = np.asarray(graph.h1_matrix, dtype=float)
    rhs = np.asarray(graph.h1_rhs, dtype=float)
    gamma = np.linalg.pinv(matrix, rcond=1e-13) @ rhs
    residual = float(np.linalg.norm(matrix @ gamma - rhs, ord=np.inf))
    if residual > 2e-10 * max(1.0, float(np.linalg.norm(rhs, ord=np.inf))):
        raise RuntimeError(f"baseline H1 residual {residual:.3e}")
    if float(np.min(gamma)) < -2e-10 * max(1.0, float(np.max(np.abs(gamma)))):
        raise RuntimeError(f"baseline nonmonotone: min={np.min(gamma):.3e}")
    return np.maximum(gamma, 0.0)


def _with_edges(base: QuadratureCandidate, edges: Iterable[tuple[int, int]], label: str) -> QuadratureCandidate:
    return QuadratureCandidate.build(
        f"{base.family}:{label}", base.nodes, base.weights, tuple(edges),
        metadata={**base.metadata, "p2e_graph": label},
    )


def _augmented(base: QuadratureCandidate, neighbors: int = 10) -> QuadratureCandidate:
    local = {tuple(map(int, edge)) for edge in base.edges}
    extra = set(knn_edges(base.nodes, min(neighbors, base.node_count - 1)))
    return _with_edges(base, sorted(local | extra), f"weak_delaunay_plus_knn{neighbors}")


def _fibonacci_directions(count: int, phase: float = 0.0) -> np.ndarray:
    if count <= 0:
        raise ValueError("count must be positive")
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    output = []
    for index in range(count):
        z = 1.0 - 2.0 * (index + 0.5) / count
        phi = 2.0 * math.pi * ((index / golden + phase) % 1.0)
        radius = math.sqrt(max(0.0, 1.0 - z * z))
        output.append((radius * math.cos(phi), radius * math.sin(phi), z))
    return np.asarray(output, dtype=float)


def _directional_h2_defect(candidate: QuadratureCandidate, gamma: np.ndarray, direction: np.ndarray) -> float:
    graph = to_graph(candidate)
    direction = np.asarray(direction, dtype=float)
    direction /= np.linalg.norm(direction)
    samples = (candidate.nodes @ direction) ** 2 - 1.0 / 3.0
    residual = graph.generator(gamma) @ samples + 6.0 * samples
    denominator = float(np.sqrt(np.sum(candidate.weights * samples**2)))
    return float(np.sqrt(np.sum(candidate.weights * residual**2)) / denominator)


def _training_rotation_spread(candidate: QuadratureCandidate, gamma: np.ndarray) -> float:
    values = [_directional_h2_defect(candidate, gamma, direction) for direction in _fibonacci_directions(48, 0.137)]
    return float(max(values) - min(values))


def _rotation_modes(candidate: QuadratureCandidate) -> np.ndarray:
    model = build_inner_model(candidate, (2,))
    shell = model.shells[2].shell
    graph = model.graph
    columns = []
    for direction in _fibonacci_directions(24, 0.3819660112501051):
        samples = (candidate.nodes @ direction) ** 2 - 1.0 / 3.0
        columns.append(shell.quotient_mode_from_samples(graph, samples))
    return np.column_stack(columns)


def _verified_result(model: Any, request: DesignRequest, *, solver: str = "CLARABEL") -> Any:
    result = solve_design(model, request, SolverConfig(solver=solver))
    if not result.feasible_candidate or result.verification is None or not result.verification.passed:
        failures = [] if result.verification is None else result.verification.failures
        raise RuntimeError(f"unverified {request.kind} result: status={result.status}, failures={failures}")
    return result


def _summary(
    name: str,
    role: str,
    graph_label: str,
    candidate: QuadratureCandidate,
    gamma: np.ndarray,
    *,
    rate_cap: float | None,
    result: Any | None,
    note: str = "",
    construction: str | None = None,
    positivity_expected: bool = True,
) -> FrozenMethodSummary:
    report = generator_report(candidate, gamma, (2, 3, 4, 5, 6))
    if result is None:
        if construction is None:
            construction = "NUMPY_PINV"
        solver = construction
        status = "verified_float"
        certificate_level = "independent_moment_reversibility_rate_and_positivity_recompute"
        primal = True
        dual = None
        interval = None
    else:
        verification = result.verification
        solver = result.solver
        status = result.status
        certificate_level = verification.certificate_level
        primal = bool(verification.primal_passed)
        dual = verification.dual_passed
        interval = None if verification.objective_interval is None else [
            float(verification.objective_interval[0]), float(verification.objective_interval[1])
        ]
    return FrozenMethodSummary(
        name=name,
        role=role,
        graph_label=graph_label,
        node_count=candidate.node_count,
        edge_count=candidate.edge_count,
        rate_cap=None if rate_cap is None else float(rate_cap),
        rate_max=float(report.rate_max),
        shell_defects={str(k): float(v) for k, v in report.shell_defects.items()},
        training_rotation_spread=_training_rotation_spread(candidate, gamma),
        minimum_conductance=float(np.min(gamma)),
        maximum_conductance=float(np.max(gamma)),
        gamma_sha256=canonical_array_sha256({"gamma": gamma}),
        solver=solver,
        solver_status=status,
        certificate_level=certificate_level,
        primal_passed=primal,
        dual_passed=dual,
        objective_interval=interval,
        positivity_expected=bool(positivity_expected),
        note=note,
    )


def _method_payload(summary: FrozenMethodSummary, candidate: QuadratureCandidate, gamma: np.ndarray) -> dict[str, object]:
    return {
        "summary": asdict(summary),
        "family": candidate.family,
        "nodes": np.asarray(candidate.nodes, dtype=float).tolist(),
        "weights": np.asarray(candidate.weights, dtype=float).tolist(),
        "edges": np.asarray(candidate.edges, dtype=int).tolist(),
        "gamma": np.asarray(gamma, dtype=float).tolist(),
        "candidate_sha256": canonical_array_sha256({
            "nodes": candidate.nodes,
            "weights": candidate.weights,
            "edges": candidate.edges,
        }),
    }


def build_registry() -> dict[str, object]:
    started = time.perf_counter()
    base = product_rule(4, 8, graph="weak_delaunay")
    augmented = _augmented(base, 10)
    baseline_gamma = _pseudoinverse(base)
    baseline_report = generator_report(base, baseline_gamma, (2, 3, 4))
    rate_cap = max(4.0, 1.75 * baseline_report.rate_max)

    h2_record = solve_global_inner(augmented, rate_cap, degree=2, solver="CLARABEL")
    h2_result = h2_record.result
    assert h2_result.gamma is not None
    h2_gamma = np.asarray(h2_result.gamma, dtype=float)

    rotation_model = build_inner_model(augmented, (2,))
    rotation_result = _verified_result(
        rotation_model,
        DesignRequest.minimax_modes(rate_cap, _rotation_modes(augmented), degree=2),
    )
    assert rotation_result.gamma is not None
    rotation_gamma = np.asarray(rotation_result.gamma, dtype=float)

    no_h2_model = build_inner_model(augmented, (3, 4))
    no_h2_result = _verified_result(
        no_h2_model,
        DesignRequest.multi_shell(rate_cap, {3: 1.0, 4: 0.25}, metric="frobenius"),
    )
    assert no_h2_result.gamma is not None
    no_h2_gamma = np.asarray(no_h2_result.gamma, dtype=float)

    no_rate_cap = 100.0 * baseline_report.rate_max
    no_rate_record = solve_global_inner(augmented, no_rate_cap, degree=2, solver="CLARABEL")
    no_rate_result = no_rate_record.result
    assert no_rate_result.gamma is not None
    no_rate_gamma = np.asarray(no_rate_result.gamma, dtype=float)

    local_model = build_inner_model(base, (2,))
    local_result = _verified_result(local_model, DesignRequest.minimum_defect(rate_cap, degree=2))
    assert local_result.gamma is not None
    local_gamma = np.asarray(local_result.gamma, dtype=float)

    # Training-only blend between the all-shell H2 norm and the selected-mode
    # rotation objective.  Both endpoints are positive, exact, reversible,
    # and rate-capped, so every grid point inherits those properties.
    baseline_d2 = float(baseline_report.shell_defects[2])
    baseline_d3 = float(baseline_report.shell_defects[3])
    baseline_rotation = max(_training_rotation_spread(base, baseline_gamma), 1e-12)
    blend_rows: list[dict[str, float]] = []
    for alpha in np.linspace(0.0, 1.0, 17):
        gamma = (1.0 - alpha) * h2_gamma + alpha * rotation_gamma
        report = generator_report(augmented, gamma, (2, 3, 4))
        rotation = _training_rotation_spread(augmented, gamma)
        score = (
            float(report.shell_defects[2]) / baseline_d2
            + 0.20 * rotation / baseline_rotation
            + 0.05 * float(report.shell_defects[3]) / float(baseline_report.shell_defects[3])
            + 0.01 * float(report.rate_max) / float(baseline_report.rate_max)
        )
        blend_rows.append({
            "alpha": float(alpha), "score": float(score),
            "d2": float(report.shell_defects[2]),
            "d3": float(report.shell_defects[3]),
            "rotation_spread": float(rotation),
            "rate_max": float(report.rate_max),
        })
    selected_blend = min(blend_rows, key=lambda row: (row["score"], row["alpha"]))
    alpha = selected_blend["alpha"]
    primary_gamma = (1.0 - alpha) * h2_gamma + alpha * rotation_gamma

    methods: dict[str, dict[str, object]] = {}
    methods["monotone_afp_baseline"] = _method_payload(
        _summary(
            "monotone_afp_baseline", "production_baseline",
            "weak_delaunay_minimum_norm_pseudoinverse", base, baseline_gamma,
            rate_cap=None, result=None,
            note="published-style shared-conductance pseudoinverse baseline",
        ), base, baseline_gamma,
    )
    methods["harmonic_fidelity"] = _method_payload(
        _summary(
            "harmonic_fidelity", "production_new_method",
            "weak_delaunay_plus_knn10", augmented, primary_gamma,
            rate_cap=rate_cap, result=None,
            construction="VERIFIED_CONVEX_COMBINATION_OF_TWO_P2A_FEASIBLE_ENDPOINTS",
            note=(
                f"training-only convex blend alpha={alpha:.6f} of H2 spectral and rotation-minimax endpoints; "
                "feasibility is inherited by convexity, but no dual-optimality certificate is claimed for the blended training objective"
            ),
        ), augmented, primary_gamma,
    )
    methods["remove_rotation_penalty"] = _method_payload(
        _summary(
            "remove_rotation_penalty", "ablation",
            "weak_delaunay_plus_knn10", augmented, h2_gamma,
            rate_cap=rate_cap, result=h2_result,
            note="full sampled H2 norm only; no selected-orientation term",
        ), augmented, h2_gamma,
    )
    methods["remove_h2_objective"] = _method_payload(
        _summary(
            "remove_h2_objective", "ablation",
            "weak_delaunay_plus_knn10", augmented, no_h2_gamma,
            rate_cap=rate_cap, result=no_h2_result,
            note="H3/H4 Frobenius objective only",
        ), augmented, no_h2_gamma,
    )
    methods["remove_rate_cap"] = _method_payload(
        _summary(
            "remove_rate_cap", "ablation",
            "weak_delaunay_plus_knn10", augmented, no_rate_gamma,
            rate_cap=no_rate_cap, result=no_rate_result,
            note="operationally inactive cap set to 100 times baseline rate",
        ), augmented, no_rate_gamma,
    )
    methods["alter_graph_locality"] = _method_payload(
        _summary(
            "alter_graph_locality", "ablation",
            "weak_delaunay_only", base, local_gamma,
            rate_cap=rate_cap, result=local_result,
            note="same nodes; local graph retained without augmentation",
        ), base, local_gamma,
    )

    # Different quadrature is frozen as a separate co-design ablation and is
    # never mixed into same-node operator-quality tables.
    alt_base = product_rule(3, 8, graph="weak_delaunay")
    alt_augmented = _augmented(alt_base, 10)
    alt_baseline = _pseudoinverse(alt_base)
    alt_rate = max(4.0, 1.75 * generator_report(alt_base, alt_baseline, (2,)).rate_max)
    alt_record = solve_global_inner(alt_augmented, alt_rate, degree=2, solver="CLARABEL")
    assert alt_record.result.gamma is not None
    alt_gamma = np.asarray(alt_record.result.gamma, dtype=float)
    alt_baseline_payload = _method_payload(
        _summary(
            "baseline_product_3x8", "separate_co_design_baseline",
            "product_3x8_weak_delaunay_minimum_norm_pseudoinverse", alt_base, alt_baseline,
            rate_cap=None, result=None,
            note="different-node baseline; excluded from same-node operator-quality tables",
        ), alt_base, alt_baseline,
    )
    alt_harmonic_payload = _method_payload(
        _summary(
            "harmonic_product_3x8", "separate_co_design_harmonic",
            "product_3x8_weak_delaunay_plus_knn10", alt_augmented, alt_gamma,
            rate_cap=alt_rate, result=alt_record.result,
            note="different-node comparison; excluded from same-node operator-quality tables",
        ), alt_augmented, alt_gamma,
    )
    co_design_levels = {
        "baseline_product_3x8": alt_baseline_payload,
        "harmonic_product_3x8": alt_harmonic_payload,
        "baseline_product_4x8": methods["monotone_afp_baseline"],
        "harmonic_product_4x8": methods["harmonic_fidelity"],
    }

    registry: dict[str, object] = {
        "schema": "afp-p2e-frozen-operator-registry-v1",
        "scope": "TRAINING_SELECTED_PRE_HELD_OUT",
        "literal_parent_sha": "b34c29b1b04f5293eaa4007b39d189efa03c51f5",
        "training_probe_sha256": "c5f9f615505eaa5674f76fa22295b5c0dd09b1ac049dadcc755385f62d3f8683",
        "selected_family": "product_4x8",
        "fixed_node_count": base.node_count,
        "fixed_nodes_weights_sha256": canonical_array_sha256({"nodes": base.nodes, "weights": base.weights}),
        "rate_cap_rule": "max(4,1.75*baseline_rate)",
        "rate_cap": float(rate_cap),
        "primary_blend_selection": {
            "grid": blend_rows,
            "selected": selected_blend,
            "weights": {"d2_ratio": 1.0, "rotation_ratio": 0.20, "d3_ratio": 0.05, "rate_ratio": 0.01},
            "data_scope": "TRAINING_SHELL_AND_COLLISION_ROTATION_ONLY",
        },
        "methods": methods,
        "co_design_levels": co_design_levels,
        "signed_variant_rule": {
            "name": "signed_higher_accuracy",
            "construction": "weighted spherical-harmonic collocation through l=6 on fixed product_4x8 nodes",
            "positivity_expected": False,
            "production_eligibility": False,
        },
        "accelerator_only_rule": {
            "production_operator": "monotone_afp_baseline",
            "preconditioner": "harmonic_fidelity",
            "fixed_point_unchanged": True,
            "scope": "P2E_COMPUTATIONAL_ABLATION_NOT_P2D_COMPLETION",
        },
        "elapsed_seconds": float(time.perf_counter() - started),
        "process_peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
    }
    digest_payload = dict(registry)
    registry["registry_sha256"] = hashlib.sha256(_strict_json(digest_payload).encode("utf-8")).hexdigest()
    return registry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    registry = build_registry()
    rendered = json.dumps(registry, indent=2, sort_keys=True, allow_nan=False) + "\n"
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("P2E_OPERATOR_FREEZE_PASS")


if __name__ == "__main__":
    main()
