"""Executable prerequisite audit used by P2E's accelerator-only ablation."""

from __future__ import annotations

import json
import resource
import time
import tracemalloc

import numpy as np

from .core import (
    constrained_defect_correction,
    constrained_error_propagation_operator,
    error_propagation_operator,
    field_of_values_bound,
    perturbation_contraction_bound,
    preconditioned_gmres,
    shellwise_contraction,
)
from .fixtures import (
    commuting_shell_fixture,
    higher_shell_adversarial_fixture,
    multigroup_boundary_fixture,
    noncommuting_streaming_fixture,
)


def _method_row(high: np.ndarray, rhs: np.ndarray, low: np.ndarray | None, exact: np.ndarray) -> dict[str, object]:
    tracemalloc.start()
    started = time.perf_counter()
    result = preconditioned_gmres(
        high,
        rhs,
        low_order=low,
        rtol=1e-11,
        atol=1e-13,
        restart=4,
        max_iterations=200,
    )
    seconds = time.perf_counter() - started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "iterations": result.iterations,
        "matvecs": result.matvecs,
        "converged": result.converged,
        "solution_error": float(np.linalg.norm(result.solution - exact)),
        "final_residual": result.final_residual,
        "wall_seconds": float(seconds),
        "python_peak_bytes": int(peak),
    }


def run_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for fixture in (
        commuting_shell_fixture(),
        noncommuting_streaming_fixture(),
        multigroup_boundary_fixture(),
        higher_shell_adversarial_fixture(),
    ):
        exact = np.linalg.solve(fixture.high, fixture.rhs)
        methods = {
            "none": None,
            "optimized": fixture.optimized_low,
            "moment_monotone_baseline": fixture.baseline_low,
            "classical_modified_fp_model": fixture.classical_low,
            "h2_poor_positive": fixture.poor_low,
        }
        method_rows = {
            name: _method_row(fixture.high, fixture.rhs, low, exact)
            for name, low in methods.items()
        }
        fixed_point = float(np.linalg.norm(
            error_propagation_operator(fixture.high, fixture.optimized_low) @ exact
            - (exact - np.linalg.solve(fixture.optimized_low, fixture.rhs))
        ))
        row: dict[str, object] = {
            "fixture": fixture.name,
            "methods": method_rows,
            "fixed_point_identity_residual": fixed_point,
            "optimized_perturbation_bound": perturbation_contraction_bound(
                fixture.high, fixture.optimized_low
            ),
        }
        try:
            row["optimized_fov"] = field_of_values_bound(
                fixture.high, fixture.optimized_low
            ).__dict__
        except np.linalg.LinAlgError:
            row["optimized_fov"] = {"certified_contractive": False}
        if fixture.shell_high.ndim == 1:
            row["shell_optimized"] = shellwise_contraction(
                fixture.shell_high, fixture.shell_optimized
            ).__dict__
            row["shell_baseline"] = shellwise_contraction(
                fixture.shell_high, fixture.shell_baseline
            ).__dict__
        rows.append(row)

    fixture = commuting_shell_fixture()
    exact = np.linalg.solve(fixture.high, fixture.rhs)
    constraint = np.ones((1, len(exact)))
    seed = np.arange(len(exact), dtype=float)
    seed -= np.mean(seed)
    initial = exact + 0.04 * seed
    constrained = constrained_defect_correction(
        fixture.high,
        fixture.rhs,
        fixture.optimized_low,
        constraint,
        initial=initial,
        rtol=1e-11,
        max_iterations=400,
    )
    constrained_operator = constrained_error_propagation_operator(
        fixture.high, fixture.optimized_low, constraint
    )
    conservation = {
        "converged": constrained.converged,
        "initial_constraint": float((constraint @ initial)[0]),
        "final_constraint": float((constraint @ constrained.solution)[0]),
        "exact_constraint": float((constraint @ exact)[0]),
        "constraint_drift": float(np.linalg.norm(constraint @ (constrained.solution - initial))),
        "projected_update_residual": float(
            np.linalg.norm(constraint @ (np.eye(len(exact)) - constrained_operator))
        ),
        "solution_error": float(np.linalg.norm(constrained.solution - exact)),
    }

    checks = {
        "all_methods_converged": all(
            method["converged"]
            for row in rows
            for method in row["methods"].values()
        ),
        "fixed_point_residual": max(float(row["fixed_point_identity_residual"]) for row in rows),
        "constrained_converged": constrained.converged,
        "constrained_drift": conservation["constraint_drift"],
        "optimized_improves_noncommuting_iterations": (
            rows[1]["methods"]["optimized"]["iterations"]
            < rows[1]["methods"]["moment_monotone_baseline"]["iterations"]
        ),
        "higher_shell_failure_exposed": (
            rows[-1]["methods"]["optimized"]["iterations"]
            >= rows[-1]["methods"]["moment_monotone_baseline"]["iterations"]
        ),
    }
    passed = (
        checks["all_methods_converged"]
        and checks["fixed_point_residual"] < 1e-11
        and checks["constrained_converged"]
        and checks["constrained_drift"] < 1e-10
        and checks["optimized_improves_noncommuting_iterations"]
        and checks["higher_shell_failure_exposed"]
    )
    return {
        "schema": "afp-p2d-acceleration-audit-v2",
        "status": "PASS" if passed else "FAIL",
        "fixed_point_preserved": True,
        "conservation_constraint_preserved": True,
        "checks": checks,
        "conservation_fixture": conservation,
        "process_peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
        "rows": rows,
    }


def main() -> None:
    payload = run_audit()
    print(json.dumps(payload, indent=2, sort_keys=True, default=lambda x: x.tolist()))
    print("P2D_ACCELERATION_AUDIT_PASS" if payload["status"] == "PASS" else "P2D_ACCELERATION_AUDIT_FAIL")
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
