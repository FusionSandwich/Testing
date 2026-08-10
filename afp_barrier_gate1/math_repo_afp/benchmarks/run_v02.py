#!/usr/bin/env python3
"""Regenerate deterministic validation evidence for the v0.2 research extensions."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hts_angular import (  # noqa: E402
    BoundaryData3D,
    CartesianGrid3D,
    GraphGenerator,
    SN3DProblem,
    axis_quadrature_sphere,
    candidate_pool_minimum_certificate,
    certify_graph_family,
    fibonacci_sphere,
    fit_graph_generator,
    forward_adjoint_identity_3d,
    global_particle_balance_3d,
    node_count_certificate,
    regular_tetrahedron_rule,
    solve_direct_3d,
    solve_source_iteration_3d,
    variable_node_positive_quadrature,
)
from hts_calibration import (  # noqa: E402
    IrradiationDataset,
    campaign_bootstrap,
    fit_positive_gls,
    leave_one_campaign_out,
)
from hts_transport_ops import (  # noqa: E402
    AngularQuadrature1D,
    CurvedPatchModel,
    Layer,
    LocalFrame,
    NuclearDataProvenance,
    OrientedTapeVolume,
    ProcessedMultigroupData,
    canonical_sha256,
    curved_interface_admissibility,
    curved_response_operator,
    cylindrical_tape_patches,
    exact_response_operator,
    isotropic_scattering_matrix,
    load_verified_checkpoint,
    response_row_reaction_rate,
    response_row_scalar_flux,
    run_ordered_cases,
    save_verified_checkpoint,
)

RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def layer_fixture(thickness: float = 8.0e-3) -> Layer:
    quadrature = AngularQuadrature1D.gauss_legendre(4)
    scattering = isotropic_scattering_matrix(quadrature, np.array([[0.18]]))
    base = Layer(
        thickness,
        quadrature,
        np.array([0.7]),
        scattering,
        source=np.linspace(1.0e-4, 4.0e-4, quadrature.n_angle),
    )
    return Layer(
        thickness,
        quadrature,
        base.total_xs,
        scattering,
        source=base.source,
        response_matrix=np.vstack(
            [response_row_scalar_flux(base), response_row_reaction_rate(base, [0.52])]
        ),
        response_names=("track_length", "absorption"),
    )


def geometry_and_curvature() -> dict[str, object]:
    frame = LocalFrame.from_normal([0.3, -0.1, 1.0], origin=[0.02, -0.03, 0.04])
    tape = OrientedTapeVolume(frame, 12.0e-3, 4.0e-3, 80.0e-6)
    normal_chord = tape.chord_length(frame.origin, frame.normal, forward_only=False)
    grazing_direction = frame.to_global_direction([1.0, 0.0, 1.0e-8])
    grazing_direction /= np.linalg.norm(grazing_direction)
    grazing = tape.path_diagnostics(frame.origin, grazing_direction)
    cylinder = cylindrical_tape_patches(0.25, 0.8, 1.7, 5, 17)

    layer = layer_fixture()
    flat_exact = exact_response_operator(layer)
    flat_curved = curved_response_operator(CurvedPatchModel(layer), method="magnus4")
    model = CurvedPatchModel(
        layer,
        principal_curvatures=(8.0, -3.0),
        mu_gradient=0.8 * np.sign(layer.mu_state),
        tangential_leakage=np.linspace(0.01, 0.04, layer.n_state),
    )
    adaptive = curved_response_operator(model, method="adaptive", tolerance=1e-12)
    midpoint = curved_response_operator(model, method="midpoint")
    route = curved_interface_admissibility(model, tangential_scale=0.1)
    vacuum = Layer(
        layer.thickness,
        layer.quadrature,
        np.zeros(layer.n_channel),
        np.zeros((layer.n_state, layer.n_state)),
    )
    curved_vacuum = curved_response_operator(
        CurvedPatchModel(vacuum, principal_curvatures=(8.0, -3.0)),
        method="magnus4",
    ).operator
    flat_vacuum = exact_response_operator(vacuum)
    return {
        "normal_chord_absolute_error": abs(normal_chord - tape.thickness),
        "grazing_finite_chord_m": float(grazing["finite_chord"]),
        "grazing_infinite_slab_path_m": float(grazing["infinite_slab_path"]),
        "grazing_edge_limited": bool(grazing["edge_limited"]),
        "cylindrical_relative_area_error": cylinder.relative_area_error,
        "maximum_patch_normal_rotation": cylinder.maximum_normal_rotation,
        "flat_operator_max_abs_difference": float(
            np.max(np.abs(flat_curved.operator.full_matrix - flat_exact.full_matrix), initial=0.0)
        ),
        "flat_offset_max_abs_difference": float(
            np.max(np.abs(flat_curved.operator.offset - flat_exact.offset), initial=0.0)
        ),
        "curved_vacuum_transmission_max_abs_difference": float(
            np.max(
                np.abs(
                    curved_vacuum.scattering_matrix
                    - flat_vacuum.scattering_matrix
                ),
                initial=0.0,
            )
        ),
        "adaptive_estimated_propagator_error": adaptive.estimated_error,
        "midpoint_vs_adaptive_inf_error": float(
            np.linalg.norm(midpoint.propagator - adaptive.propagator, ord=np.inf)
        ),
        "adaptive_steps": adaptive.accepted_steps,
        "local_interface_accepted": bool(route["accepted"]),
        "curvature_thickness": float(route["curvature_thickness"]),
        "geometric_ratio": float(route["geometric_ratio"]),
    }


def sn3d_fixture() -> SN3DProblem:
    grid = CartesianGrid3D(
        np.array([0.0, 0.2, 0.7, 1.0]),
        np.array([0.0, 0.4, 1.0]),
        np.array([0.0, 0.3, 0.8, 1.0]),
    )
    quadrature = axis_quadrature_sphere()
    shape = grid.shape
    x = grid.x_centers[:, None, None]
    y = grid.y_centers[None, :, None]
    z = grid.z_centers[None, None, :]
    sigma_t = np.empty((2, *shape))
    sigma_t[0] = 0.8 + 0.2 * x + 0.1 * y + 0.05 * z
    sigma_t[1] = 0.65 + 0.1 * x + 0.08 * z
    sigma_s = np.zeros((2, 2, *shape))
    sigma_s[0, 0] = 0.20 + 0.02 * x
    sigma_s[0, 1] = 0.05
    sigma_s[1, 0] = 0.02
    sigma_s[1, 1] = 0.17
    source = np.empty((2, quadrature.n_node, *shape))
    for group in range(2):
        for angle in range(quadrature.n_node):
            source[group, angle] = (
                0.006 * (group + 1) + 0.0004 * angle
            ) * (1.0 + x + 0.5 * y + 0.25 * z)
    return SN3DProblem(
        grid,
        quadrature,
        sigma_t,
        sigma_s,
        source,
        BoundaryData3D.vacuum(2, quadrature.n_node, grid),
        {
            "total_track": np.ones_like(source),
            "photon_weighted": np.broadcast_to(
                np.array([0.0, 1.0])[:, None, None, None, None], source.shape
            ).copy(),
        },
    )


def transport_3d() -> dict[str, object]:
    problem = sn3d_fixture()
    direct = solve_direct_3d(problem, residual_tolerance=1e-11)
    serial = solve_source_iteration_3d(problem, tolerance=2e-13, workers=1)
    parallel = solve_source_iteration_3d(problem, tolerance=2e-13, workers=4)
    adjoint = forward_adjoint_identity_3d(problem, direct, "photon_weighted")
    balance = global_particle_balance_3d(problem, parallel)
    difference = np.max(np.abs(serial.angular_flux - direct.angular_flux), initial=0.0)
    scale = max(np.max(np.abs(direct.angular_flux), initial=0.0), 1e-30)
    return {
        "unknowns": problem.n_unknown,
        "source_iterations": serial.iterations,
        "direct_converged": direct.converged,
        "source_iteration_converged": serial.converged,
        "direct_vs_iteration_relative_max": float(difference / scale),
        "worker_digest_equal": serial.flux_sha256 == parallel.flux_sha256,
        "worker_flux_bitwise_equal": bool(np.array_equal(serial.angular_flux, parallel.angular_flux)),
        "minimum_flux": float(np.min(parallel.angular_flux)),
        "particle_balance_relative_residual": balance["relative_residual"],
        "forward_adjoint_relative_difference": adjoint["relative_difference"],
        "flux_sha256": parallel.flux_sha256,
    }


def nuclear_fixture() -> ProcessedMultigroupData:
    return ProcessedMultigroupData(
        group_edges_eV=np.array([0.5, 2.0, 20.0, 200.0, 2000.0]),
        representative_energy_eV=np.array([1.0, 10.0, 100.0, 1000.0]),
        total_xs_cm1=np.array([0.9, 0.7, 0.45, 0.3]),
        scattering_cm1=np.array(
            [
                [0.16, 0.04, 0.00, 0.00],
                [0.00, 0.13, 0.02, 0.00],
                [0.00, 0.03, 0.08, 0.02],
                [0.00, 0.00, 0.00, 0.05],
            ]
        ),
        reaction_xs_cm1=np.array(
            [[0.12, 0.10, 0.08, 0.05], [0.04, 0.03, 0.02, 0.01]]
        ),
        reaction_q_eV=np.array(
            [[0.2, 1.0, 8.0, 50.0], [-0.1, -0.5, -3.0, -20.0]]
        ),
        reaction_names=("capture", "endothermic"),
        species=("neutron", "neutron", "photon", "photon"),
        channel_names=("n-low", "n-high", "g-low", "g-high"),
        provenance=NuclearDataProvenance(
            "synthetic-closure-fixture",
            "test-1",
            "fixture-builder",
            "1.0",
            293.6,
            evaluated=False,
        ),
        metadata={"fixture": True},
    )


def nuclear_data() -> dict[str, object]:
    data = nuclear_fixture()
    audit = data.require_energy_closure()
    weights = np.array([2.0, 1.0, 3.0, 0.5])
    collapsed = data.collapse_groups(((0, 1), (2, 3)), weights)
    target = np.array(
        [
            np.average(audit.local_deposition_eV_cm1[:2], weights=weights[:2]),
            np.average(audit.local_deposition_eV_cm1[2:], weights=weights[2:]),
        ]
    )
    collapsed_audit = collapsed.require_energy_closure()
    with tempfile.TemporaryDirectory(prefix="rpto-v02-nuclear-") as directory:
        path = Path(directory) / "processed.h5"
        data.save_hdf5(path)
        restored = ProcessedMultigroupData.load_hdf5(path)
    layer = data.to_layer(3.0e-4, AngularQuadrature1D.gauss_legendre(4))
    operator = exact_response_operator(layer)
    _, _, responses = operator.apply(np.ones(layer.plus.size), np.zeros(layer.minus.size))
    return {
        "energy_closure_passed": audit.passed,
        "minimum_local_deposition_eV_cm1": audit.minimum_local_deposition,
        "content_round_trip_digest_equal": restored.content_sha256() == data.content_sha256(),
        "collapsed_group_count": collapsed.n_group,
        "collapsed_heating_max_abs_error": float(
            np.max(np.abs(collapsed_audit.local_deposition_eV_cm1 - target), initial=0.0)
        ),
        "response_count": layer.n_response,
        "minimum_response": float(np.min(responses)),
        "content_sha256": data.content_sha256(),
    }


def calibration_fixture() -> tuple[IrradiationDataset, np.ndarray]:
    campaigns: list[str] = []
    rows: list[list[float]] = []
    noise: list[float] = []
    for campaign_index, campaign in enumerate(("reactor-A", "proton-B", "ion-C", "gamma-D")):
        for local in range(7):
            dose = 0.15 + 0.22 * local + 0.04 * campaign_index
            rows.append([1.0, np.log1p(dose), dose])
            campaigns.append(campaign)
            noise.append(0.003 * np.sin(0.7 * (local + 3 * campaign_index)))
    design = np.asarray(rows)
    coefficients = np.array([0.015, 0.17, -0.095])
    target = np.exp(design @ coefficients + np.asarray(noise))
    sigma = np.full(target.size, 0.012)
    covariance = np.diag(sigma * sigma)
    for start in range(0, target.size, 7):
        covariance[start : start + 7, start : start + 7] += 0.15 * sigma[0] ** 2
    return (
        IrradiationDataset(
            design,
            target,
            tuple(campaigns),
            ("intercept", "benefit", "damage"),
            covariance=covariance,
            metadata={"material": "synthetic-GdBCO-fixture", "target": "Jc/Jc0"},
        ),
        coefficients,
    )


def calibration() -> tuple[dict[str, object], list[dict[str, object]]]:
    dataset, truth = calibration_fixture()
    lower = np.array([-np.inf, 0.0, -np.inf])
    upper = np.array([np.inf, np.inf, 0.0])
    fit = fit_positive_gls(dataset, lower_bounds=lower, upper_bounds=upper)
    validation = leave_one_campaign_out(dataset, lower_bounds=lower, upper_bounds=upper)
    bootstrap = campaign_bootstrap(dataset, 32, seed=41, lower_bounds=lower, upper_bounds=upper)
    rows = [
        {
            "feature": name,
            "truth": float(expected),
            "estimate": float(estimate),
            "standard_uncertainty": float(np.sqrt(max(fit.covariance[index, index], 0.0))),
        }
        for index, (name, expected, estimate) in enumerate(
            zip(fit.feature_names, truth, fit.coefficients, strict=True)
        )
    ]
    return (
        {
            "fit_success": fit.success,
            "coefficient_max_abs_error": float(np.max(np.abs(fit.coefficients - truth))),
            "weighted_residual_norm": fit.weighted_residual_norm,
            "condition_number": fit.condition_number,
            "leave_one_campaign_out_count": len(validation.records),
            "pooled_leave_one_campaign_out_log_rmse": validation.pooled_log_rmse,
            "bootstrap_successful_samples": bootstrap.successful_samples,
            "bootstrap_attempted_samples": bootstrap.attempted_samples,
            "bootstrap_coefficients_sha256": canonical_sha256(bootstrap.coefficients),
        },
        rows,
    )


def quadrature_and_graph() -> tuple[dict[str, object], list[dict[str, object]]]:
    tetrahedron = regular_tetrahedron_rule()
    node_certificate = node_count_certificate(tetrahedron, 2)
    variable = variable_node_positive_quadrature(2, 4, starts=3, seed=19)
    pool = np.vstack([tetrahedron.nodes, axis_quadrature_sphere().nodes])
    fixed = candidate_pool_minimum_certificate(pool, 2, time_limit=10.0)
    graphs = []
    for count in (12, 24, 48):
        quadrature = fibonacci_sphere(count)
        graphs.append(
            fit_graph_generator(
                quadrature.nodes,
                quadrature.weights,
                maximum_degree=2,
                k_nearest=min(12, count - 1),
                regularization=1e-10,
                conductance_floor=1e-14,
            )
        )
    certificate = certify_graph_family(
        graphs,
        maximum_degree=2,
        sample_count=2048,
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
        minimum_fitted_order=0.5,
    )
    broken = [
        GraphGenerator(
            graph.nodes,
            graph.weights,
            np.zeros_like(graph.conductances),
            np.zeros_like(graph.generator),
            np.empty((0, 2), dtype=int),
            graph.fit_residual_norm,
            {"fixture": "disconnected"},
        )
        for graph in graphs
    ]
    no_go = certify_graph_family(
        broken,
        maximum_degree=2,
        sample_count=1024,
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
    )
    rows = [
        {
            "nodes": record.node_count,
            "fill_distance": record.fill_distance,
            "mesh_ratio": record.mesh_ratio,
            "weight_ratio": record.weight_ratio,
            "total_weight": record.total_weight,
            "relative_total_weight_error": record.relative_total_weight_error,
            "relative_weight_scaling_error": record.relative_weight_scaling_error,
            "algebraic_connectivity": record.algebraic_connectivity,
            "structural_residual": record.structural_residual,
            "maximum_harmonic_relative_residual": record.maximum_weighted_relative_residual,
            "mean_harmonic_relative_residual": record.mean_weighted_relative_residual,
        }
        for record in certificate.records
    ]
    return (
        {
            "tetrahedron_residual_inf": node_certificate.residual_inf,
            "tetrahedron_globally_node_minimal": node_certificate.globally_node_minimal,
            "variable_rule_exact": variable.exact,
            "variable_rule_residual_inf": variable.residual_inf,
            "fixed_pool_minimum_support": fixed.support,
            "fixed_pool_exact": fixed.exact,
            "graph_family_passed": certificate.passed,
            "graph_fitted_order": certificate.fitted_order,
            "graph_fitted_prefactor": certificate.fitted_prefactor,
            "graph_minimum_adjacent_order": certificate.minimum_adjacent_order,
            "graph_maximum_envelope_ratio": certificate.maximum_envelope_ratio,
            "graph_fill_distance_interval": certificate.fill_distance_interval,
            "disconnected_family_rejected": not no_go.passed,
            "disconnected_reasons": no_go.reasons,
        },
        rows,
    )


def deterministic_parallel() -> dict[str, object]:
    cases = list(range(20))

    def calculate(value: int) -> dict[str, int]:
        return {"value": value, "cube": value**3}

    serial = run_ordered_cases(cases, calculate, workers=1)
    parallel = run_ordered_cases(cases, calculate, workers=5)
    with tempfile.TemporaryDirectory(prefix="rpto-v02-checkpoint-") as directory:
        path = Path(directory) / "cases.json"
        digest = save_verified_checkpoint(path, parallel)
        restored = load_verified_checkpoint(path)
    return {
        "serial_parallel_digest_equal": serial.digest == parallel.digest,
        "all_cases_succeeded": parallel.succeeded,
        "case_count": len(parallel.results),
        "checkpoint_digest": digest,
        "checkpoint_payload_digest": canonical_sha256(restored),
    }


def main() -> int:
    calibration_summary, calibration_rows = calibration()
    quadrature_summary, graph_rows = quadrature_and_graph()
    summary = {
        "schema": "rpto-v02-benchmark-summary-v1",
        "geometry_and_curvature": geometry_and_curvature(),
        "transport_3d": transport_3d(),
        "nuclear_data": nuclear_data(),
        "calibration": calibration_summary,
        "quadrature_and_graph": quadrature_summary,
        "deterministic_parallel": deterministic_parallel(),
    }
    write_json(RESULTS / "v02_summary.json", summary)
    write_csv(RESULTS / "v02_graph_family.csv", graph_rows)
    write_csv(RESULTS / "v02_calibration_coefficients.csv", calibration_rows)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
