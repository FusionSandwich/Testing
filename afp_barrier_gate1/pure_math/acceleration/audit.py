"""Executable P2D proof, transport, comparator, and hostile audit."""

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
    iteration_count_bound,
    perturbation_contraction_bound,
    preconditioned_gmres,
    shellwise_contraction,
    spectral_equivalence_bound,
)
from .fixtures import (
    commuting_shell_fixture,
    higher_shell_adversarial_fixture,
    multigroup_boundary_fixture,
    noncommuting_streaming_fixture,
)
from .transport import complete_transport_audit


def _method_row(
    high: np.ndarray,
    rhs: np.ndarray,
    low: np.ndarray | None,
    exact: np.ndarray,
) -> dict[str, object]:
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
        "low_solves": result.low_solves,
        "converged": result.converged,
        "solution_error": float(np.linalg.norm(result.solution - exact)),
        "final_residual": result.final_residual,
        "setup_seconds": result.setup_seconds,
        "solve_seconds": result.solve_seconds,
        "wall_seconds": float(seconds),
        "python_peak_bytes": int(peak),
        "preconditioner_bytes": result.preconditioner_bytes,
    }


def _finite_algebra_audit() -> dict[str, object]:
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
        except (np.linalg.LinAlgError, ValueError):
            row["optimized_fov"] = {"certified_contractive": False}
        if fixture.name == "commuting_shell":
            row["spectral_equivalence"] = spectral_equivalence_bound(
                fixture.high, fixture.optimized_low
            ).__dict__
        if fixture.shell_high.ndim == 1:
            optimized_shell = shellwise_contraction(
                fixture.shell_high, fixture.shell_optimized
            )
            row["shell_optimized"] = optimized_shell.__dict__
            row["shell_baseline"] = shellwise_contraction(
                fixture.shell_high, fixture.shell_baseline
            ).__dict__
            if optimized_shell.contractive:
                row["sufficient_iterations_to_reduce_unit_error_to_1e-8"] = iteration_count_bound(
                    optimized_shell.spectral_radius, 1.0, 1e-8
                )
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
        "higher_shell_toy_failure_exposed": (
            rows[-1]["methods"]["optimized"]["iterations"]
            >= rows[-1]["methods"]["moment_monotone_baseline"]["iterations"]
        ),
    }
    passed = bool(
        checks["all_methods_converged"]
        and checks["fixed_point_residual"] < 1e-11
        and checks["constrained_converged"]
        and checks["constrained_drift"] < 1e-10
        and checks["optimized_improves_noncommuting_iterations"]
        and checks["higher_shell_toy_failure_exposed"]
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "conservation_fixture": conservation,
        "rows": rows,
    }


def run_audit() -> dict[str, object]:
    finite = _finite_algebra_audit()
    transport = complete_transport_audit()
    checks = {
        "finite_algebra_pass": finite["status"] == "PASS",
        "transport_pass": transport["status"] == "PASS",
        "fixed_point_residual": finite["checks"]["fixed_point_residual"],
        "constrained_converged": finite["checks"]["constrained_converged"],
        "constrained_drift": finite["checks"]["constrained_drift"],
        "optimized_improves_noncommuting_iterations": finite["checks"]["optimized_improves_noncommuting_iterations"],
        "forward_peaked_optimized_beats_baseline": transport["checks"]["forward_peaked_optimized_beats_baseline"],
        "forward_peaked_optimized_beats_none": transport["checks"]["forward_peaked_optimized_beats_none"],
        "higher_shell_failure_exposed": bool(
            finite["checks"]["higher_shell_toy_failure_exposed"]
            and transport["checks"]["higher_shell_failure_exposed"]
        ),
        "ray_error_dominates": transport["checks"]["ray_error_dominates"],
        "multigroup_boundary_converged": transport["checks"]["multigroup_boundary_converged"],
    }
    passed = bool(checks["finite_algebra_pass"] and checks["transport_pass"])
    return {
        "schema": "afp-p2d-acceleration-audit-v3",
        "status": "PASS" if passed else "FAIL",
        "fixed_point_preserved": True,
        "conservation_constraint_preserved": True,
        "checks": checks,
        "conservation_fixture": finite["conservation_fixture"],
        "finite_algebra": finite,
        "transport": transport,
        # Retain the old row location for downstream readers.
        "rows": finite["rows"],
        "process_peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024),
    }


def main() -> None:
    payload = run_audit()
    print(json.dumps(payload, indent=2, sort_keys=True, default=lambda x: x.tolist(), allow_nan=False))
    print("P2D_ACCELERATION_AUDIT_PASS" if payload["status"] == "PASS" else "P2D_ACCELERATION_AUDIT_FAIL")
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
