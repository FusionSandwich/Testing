"""Run all deterministic numerical studies for Papers 1 and 2.

The script intentionally uses only public package APIs.  It writes CSV/JSON
results, HDF5 operators, and publication-scale plots under ``results/``.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hts_angular.adaptivity import filtered_harmonic_bootstrap
from hts_angular.graph_generator import fit_graph_generator
from hts_angular.quadrature import (
    PositiveQuadrature,
    balanced_multiresponse_density,
    exact_surface_harmonic_moments,
    farkas_infeasibility_certificate,
    fibonacci_sphere,
    finite_pool_positive_quadrature,
    gauss_legendre_product_sphere,
    minimum_residual_positive_weights,
    moment_conditioning,
    real_spherical_harmonics,
)
from hts_angular.sn2d import (
    BoundaryData2D,
    CartesianGrid2D,
    SN2DProblem,
    circle_quadrature,
    forward_adjoint_identity,
    global_particle_balance,
    solve_source_iteration,
)
from hts_angular.transfer import (
    current_preserving_no_go,
    moment_matrix,
    state_specific_positive_remap,
    universal_positive_transfer,
)
from hts_transport_ops.compression import compress_ballistic_residual
from hts_transport_ops.layer import (
    AngularQuadrature1D,
    Layer,
    isotropic_scattering_matrix,
    response_row_angular_moment,
    response_row_reaction_rate,
    response_row_scalar_flux,
)
from hts_transport_ops.multilayer import compose_operators, global_interface_basis_operator, stable_subdivided_layer_operator
from hts_transport_ops.response_operator import exact_response_operator
from hts_transport_ops.thin_layer import asymptotic_operator, hybrid_operator, select_grazing_states

RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def read_config(name: str) -> dict[str, object]:
    return json.loads((ROOT / "benchmarks" / "configs" / name).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fit_log_slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(y) & (y > 1e-18)
    if np.count_nonzero(mask) < 2:
        return math.nan
    return float(np.polyfit(np.log(x[mask]), np.log(y[mask]), 1)[0])


def thin_layer_from_config(config: dict[str, object], thickness: float, scale: float = 1.0) -> Layer:
    q = AngularQuadrature1D(np.asarray(config["mu"]), np.asarray(config["weights"]))
    total = float(config["total_xs_per_cm"]) * scale
    scatter = float(config["isotropic_scatter_xs_per_cm"]) * scale
    S = isotropic_scattering_matrix(q, np.array([[scatter]]))
    base = Layer(thickness, q, np.array([total]), S, metadata={"length_unit": "cm", "cross_section_unit": "cm^-1"})
    H = np.vstack([
        response_row_reaction_rate(base, [total - scatter]),
        response_row_scalar_flux(base),
        response_row_angular_moment(base, q.mu**2),
    ])
    return Layer(
        thickness, q, np.array([total]), S,
        response_matrix=H,
        response_names=("absorbed_particles", "scalar_flux_track_length", "mu2_track_length"),
        metadata={"length_unit": "cm", "cross_section_unit": "cm^-1", "material": "representative_REBCO_stack"},
    )


def normalized_incidence(layer: Layer) -> tuple[np.ndarray, np.ndarray]:
    mup = layer.mu_state[layer.plus]
    wp = layer.weight_state[layer.plus]
    left = np.exp(5.0 * (mup - 1.0))
    left /= np.sum(wp * mup * left)
    return left, np.zeros(layer.minus.size)


def run_thin_layer() -> dict[str, object]:
    config = read_config("paper1_thin_layer.json")
    hs = np.asarray(config["thicknesses_cm"], dtype=float)
    tol = float(config["hybrid_tolerance"])
    rows: list[dict[str, object]] = []
    errors_by_method: dict[str, list[float]] = {"taylor_1": [], "taylor_2": [], "hybrid_2": []}
    response_errors: dict[str, list[float]] = {key: [] for key in errors_by_method}
    incident_errors: dict[str, list[float]] = {key: [] for key in errors_by_method}
    for h in hs:
        layer = thin_layer_from_config(config, float(h))
        exact = exact_response_operator(layer)
        u, v = normalized_incidence(layer)
        _, _, Jexact = exact.apply(u, v)
        candidates = {
            "taylor_1": asymptotic_operator(layer, 1),
            "taylor_2": asymptotic_operator(layer, 2),
            "hybrid_2": hybrid_operator(layer, 2, tolerance=tol),
        }
        grazing_fraction = float(np.mean(select_grazing_states(layer, 2, tol)))
        for name, candidate in candidates.items():
            full_error = float(np.linalg.norm(candidate.full_matrix - exact.full_matrix))
            response_error = float(np.linalg.norm(candidate.response_matrix - exact.response_matrix) / max(np.linalg.norm(exact.response_matrix), 1e-30))
            _, _, Jcandidate = candidate.apply(u, v)
            incident_error = float(np.linalg.norm(Jcandidate - Jexact) / max(np.linalg.norm(Jexact), 1e-30))
            errors_by_method[name].append(full_error)
            response_errors[name].append(response_error)
            incident_errors[name].append(incident_error)
            rows.append({
                "thickness_cm": h,
                "normal_optical_thickness": float(config["total_xs_per_cm"]) * h,
                "method": name,
                "full_operator_error": full_error,
                "relative_response_matrix_error": response_error,
                "incident_response_error": incident_error,
                "minimum_entry": candidate.minimum_entry(),
                "grazing_fraction": grazing_fraction if name == "hybrid_2" else 0.0,
            })
    write_csv(RESULTS / "paper1_thickness_convergence.csv", rows)
    slopes: dict[str, dict[str, float]] = {}
    # Fit the smallest five thicknesses before mask transitions and roundoff dominate.
    fit_slice = slice(0, 5)
    for name in errors_by_method:
        slopes[name] = {
            "full_operator_order": fit_log_slope(hs[fit_slice], np.asarray(errors_by_method[name])[fit_slice]),
            "response_matrix_order": fit_log_slope(hs[fit_slice], np.asarray(response_errors[name])[fit_slice]),
            "incident_response_order": fit_log_slope(hs[fit_slice], np.asarray(incident_errors[name])[fit_slice]),
        }
    (RESULTS / "paper1_convergence_orders.json").write_text(json.dumps(slopes, indent=2), encoding="utf-8")

    plt.figure(figsize=(7.2, 4.8))
    for name, errors in errors_by_method.items():
        plt.loglog(hs, errors, marker="o", label=name)
    plt.xlabel("Physical thickness h [cm]")
    plt.ylabel("Frobenius error in full response matrix")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "paper1_thickness_convergence.png", dpi=180)
    plt.close()

    # Direction-resolved grazing study.
    hrep = float(config["representative_thickness_cm"])
    layer = thin_layer_from_config(config, hrep)
    exact = exact_response_operator(layer)
    taylor = asymptotic_operator(layer, 2)
    hybrid = hybrid_operator(layer, 2, tolerance=tol)
    direction_rows = []
    nleft = layer.plus.size
    for side, count in (("left", layer.plus.size), ("right", layer.minus.size)):
        for k in range(count):
            u, v = np.zeros(layer.plus.size), np.zeros(layer.minus.size)
            (u if side == "left" else v)[k] = 1.0
            _, _, Je = exact.apply(u, v)
            _, _, Jt = taylor.apply(u, v)
            _, _, Jh = hybrid.apply(u, v)
            state_index = (layer.plus if side == "left" else layer.minus)[k]
            direction_rows.append({
                "side": side,
                "mu": layer.mu_state[state_index],
                "directional_optical_thickness": layer.total_state[state_index] * hrep / abs(layer.mu_state[state_index]),
                "taylor_response_error": float(np.linalg.norm(Jt - Je)),
                "hybrid_response_error": float(np.linalg.norm(Jh - Je)),
            })
    write_csv(RESULTS / "paper1_grazing_direction_study.csv", direction_rows)
    plt.figure(figsize=(7.2, 4.8))
    positive_rows = [row for row in direction_rows if row["side"] == "left"]
    x = np.array([abs(float(row["mu"])) for row in positive_rows])
    plt.loglog(x, [float(row["taylor_response_error"]) for row in positive_rows], marker="o", label="Taylor order 2")
    plt.loglog(x, [float(row["hybrid_response_error"]) for row in positive_rows], marker="s", label="Hybrid")
    plt.xlabel("|mu|")
    plt.ylabel("Absolute response-vector error")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "paper1_grazing_error.png", dpi=180)
    plt.close()

    # Optical-thickness scaling.
    optical_rows = []
    for scale in np.logspace(-2, 2, 13):
        current = thin_layer_from_config(config, hrep, float(scale))
        exact_current = stable_subdivided_layer_operator(current, 1.5)
        try:
            tay = asymptotic_operator(current, 2)
            taylor_error = float(np.linalg.norm(tay.full_matrix - exact_current.full_matrix))
            taylor_status = "assembled"
        except np.linalg.LinAlgError:
            taylor_error = math.nan
            taylor_status = "Schur block numerically singular"
        try:
            hyb = hybrid_operator(current, 2, tolerance=tol)
            hybrid_error = float(np.linalg.norm(hyb.full_matrix - exact_current.full_matrix))
            hybrid_status = "assembled"
        except np.linalg.LinAlgError:
            hybrid_error = math.nan
            hybrid_status = "Schur block numerically singular; use subdivided exact operator"
        optical_rows.append({
            "cross_section_scale": scale,
            "normal_optical_thickness": current.total_xs[0] * hrep,
            "maximum_directional_optical_thickness": current.total_xs[0] * hrep / np.min(np.abs(current.quadrature.mu)),
            "taylor_error": taylor_error,
            "hybrid_error": hybrid_error,
            "taylor_status": taylor_status,
            "hybrid_status": hybrid_status,
            "stable_exact_subdivisions": int(exact_current.metadata.get("subdivision_count", 1)),
            "hybrid_grazing_fraction": float(np.mean(select_grazing_states(current, 2, tol))),
        })
    write_csv(RESULTS / "paper1_optical_scaling.csv", optical_rows)

    # Positive compression with an uncollided ballistic backbone.
    matrix = hybrid.full_matrix
    nport = layer.plus.size
    balance = np.zeros(matrix.shape[0])
    boundary_current = layer.weight_state * np.abs(layer.mu_state)
    balance[:nport] = boundary_current[layer.minus]
    balance[nport : 2 * nport] = boundary_current[layer.plus]
    balance[2 * nport] = 1.0  # first response is particle absorption
    ballistic = np.zeros_like(matrix)
    atten_plus = np.exp(-layer.total_state[layer.plus] * hrep / np.abs(layer.mu_state[layer.plus]))
    atten_minus = np.exp(-layer.total_state[layer.minus] * hrep / np.abs(layer.mu_state[layer.minus]))
    ballistic[nport : 2 * nport, :nport] = np.diag(atten_plus)
    ballistic[:nport, nport:] = np.diag(atten_minus)
    compression = compress_ballistic_residual(matrix, ballistic, balance, rank=4)
    u, v = normalized_incidence(layer)
    incident = np.concatenate([u, v])
    compression_summary = {
        "dense_rows": int(matrix.shape[0]),
        "dense_columns": int(matrix.shape[1]),
        "dense_entries": int(matrix.size),
        "stored_ballistic_nonzeros": int(np.count_nonzero(ballistic)),
        "collided_rank": int(compression.collided.archetypes.shape[1]),
        "compressed_parameter_count": int(np.count_nonzero(ballistic) + compression.collided.archetypes.size + compression.collided.coefficients.size),
        "weighted_frobenius_error": compression.collided.weighted_frobenius_error,
        "max_column_error": compression.collided.max_column_error,
        "incident_output_error": float(np.linalg.norm((compression.approximation - matrix) @ incident)),
        "minimum_entry": float(np.min(compression.approximation)),
        "balance_error": float(np.max(np.abs(balance @ compression.approximation - balance @ matrix))),
    }
    (RESULTS / "paper1_compression_summary.json").write_text(json.dumps(compression_summary, indent=2), encoding="utf-8")

    # Transfer-matrix conditioning threshold study.
    conditioning_rows = []
    for directional_tau in np.logspace(-3, 3, 25):
        conditioning_rows.append({
            "directional_optical_thickness": directional_tau,
            "transfer_matrix_condition_number": float(np.exp(min(2.0 * directional_tau, 709.0))),
            "log_condition_number": 2.0 * directional_tau,
            "double_precision_cancellation_risk": bool(2.0 * directional_tau >= math.log(1.0 / np.finfo(float).eps)),
            "overflow_risk": bool(directional_tau >= 709.0),
        })
    write_csv(RESULTS / "paper1_transfer_conditioning.csv", conditioning_rows)
    return {"convergence_orders": slopes, "compression": compression_summary}


def multilayer_layer(
    name: str,
    h: float,
    total: tuple[float, float],
    coupling: np.ndarray,
    kerma: tuple[float, float],
    fixed_photon_source: float = 0.0,
) -> Layer:
    q = AngularQuadrature1D.gauss_legendre(6)
    S = isotropic_scattering_matrix(q, coupling)
    base = Layer(h, q, np.asarray(total), S)
    H = np.vstack([
        response_row_reaction_rate(base, kerma),
        response_row_scalar_flux(base, [1.0, 0.0]),
        response_row_scalar_flux(base, [0.0, 1.0]),
    ])
    source = np.zeros(base.n_state)
    source[q.n_angle :] = fixed_photon_source
    return Layer(
        h, q, np.asarray(total), S, source=source,
        response_matrix=H,
        response_names=(f"{name}:heating", f"{name}:neutron_flux", f"{name}:photon_flux"),
        channel_names=("neutron", "photon"),
        metadata={"material": name, "length_unit": "cm", "cross_section_unit": "cm^-1", "response_units": ["arbitrary_energy", "cm", "cm"]},
    )


def run_multilayer() -> dict[str, object]:
    specifications = [
        ("Cu", 0.0020, (2.2, 1.1), np.array([[0.80, 0.0], [0.18, 0.35]]), (0.90, 0.55), 0.0),
        ("Ag", 0.0002, (2.8, 1.4), np.array([[0.95, 0.0], [0.22, 0.42]]), (1.15, 0.72), 0.0),
        ("REBCO", 0.0001, (3.5, 1.8), np.array([[1.10, 0.0], [0.35, 0.50]]), (1.45, 0.95), 1e-4),
        ("buffer", 0.00002, (2.6, 1.3), np.array([[0.85, 0.0], [0.20, 0.38]]), (1.05, 0.65), 0.0),
        ("Hastelloy", 0.0050, (2.0, 1.0), np.array([[0.70, 0.0], [0.15, 0.30]]), (0.82, 0.50), 0.0),
    ]
    layers = [multilayer_layer(*spec) for spec in specifications]
    operators = [exact_response_operator(layer) for layer in layers]
    star = compose_operators(operators)
    global_op = global_interface_basis_operator(operators)
    star.save_hdf5(RESULTS / "paper1_multilayer_response_operator.h5")
    rows = []
    for i, name in enumerate(star.response_names):
        rows.append({
            "response_index": i,
            "response_name": name,
            "left_incidence_row_norm": float(np.linalg.norm(star.C_L[i])),
            "right_incidence_row_norm": float(np.linalg.norm(star.C_R[i])),
            "fixed_source_offset": float(star.d[i]),
        })
    write_csv(RESULTS / "paper1_multilayer_responses.csv", rows)
    summary = {
        "layers": len(layers),
        "channels": 2,
        "angles_per_channel": 6,
        "port_dimension": star.n_left_in,
        "responses": star.n_response,
        "total_thickness_cm": float(sum(layer.thickness for layer in layers)),
        "star_vs_global_matrix_max_abs": float(np.max(np.abs(star.full_matrix - global_op.full_matrix))),
        "star_vs_global_offset_max_abs": float(np.max(np.abs(star.offset - global_op.offset))),
        "minimum_boundary_operator_entry": star.minimum_entry(),
        "maximum_interface_condition": float(max(op.metadata.get("condition_E_mm", 0.0) for op in operators)),
    }
    (RESULTS / "paper1_multilayer_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def custom_modes(nodes: np.ndarray, norms: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    x, y, z = nodes.T
    stream = np.exp(10.0 * (x - 1.0))
    adjoint = np.exp(9.0 * (0.65 * x + 0.76 * y - 1.0))
    contributon = stream * adjoint
    grazing = np.exp(-((z / 0.08) ** 2))
    shielding = np.exp(7.0 * (0.82 * x - 0.25 * y + 0.51 * z - 1.0))
    values = np.vstack([stream, adjoint, contributon, grazing, shielding])
    if norms is not None:
        values = values / norms[:, None]
    return values, np.ones(5) if norms is None else norms


def run_quadrature_and_graph() -> dict[str, object]:
    config = read_config("paper2_quadrature.json")
    ref = gauss_legendre_product_sphere(int(config["reference_polar_order"]), int(config["reference_azimuth_order"]), phase=0.25)
    Y, labels = real_spherical_harmonics(ref.nodes, int(config["harmonic_degree"]))
    custom_raw, _ = custom_modes(ref.nodes)
    norms = np.sqrt(np.sum(custom_raw * custom_raw * ref.weights[None, :], axis=1))
    custom, _ = custom_modes(ref.nodes, norms)
    enriched = np.vstack([Y, custom])
    target_harmonic = exact_surface_harmonic_moments(int(config["harmonic_degree"]))
    target_enriched = enriched @ ref.weights
    harmonic_fit = finite_pool_positive_quadrature(ref.nodes, Y, target_harmonic)
    enriched_fit = finite_pool_positive_quadrature(ref.nodes, enriched, target_enriched)
    if harmonic_fit.quadrature is None or enriched_fit.quadrature is None:
        raise RuntimeError("reference moment pool unexpectedly failed")

    density = balanced_multiresponse_density(custom[0], custom[1:4], ref.weights, alpha=float(config["response_density_alpha"]))
    density_checks = {
        "weighted_integral": float(density @ ref.weights),
        "minimum_density": float(np.min(density)),
        "maximum_density": float(np.max(density)),
    }
    fixed_rows = []
    for n in config["fixed_pool_sizes"]:
        pool = fibonacci_sphere(int(n))
        Yp, _ = real_spherical_harmonics(pool.nodes, int(config["harmonic_degree"]))
        custom_p, _ = custom_modes(pool.nodes, norms)
        Fp = np.vstack([Yp, custom_p])
        fit = finite_pool_positive_quadrature(pool.nodes, Fp, target_enriched)
        near = minimum_residual_positive_weights(Fp, target_enriched)
        certificate = None if fit.exact else farkas_infeasibility_certificate(Fp, target_enriched)
        fixed_rows.append({
            "pool_nodes": int(n),
            "exact_feasible": bool(fit.exact),
            "exact_support": fit.quadrature.n_node if fit.quadrature is not None else 0,
            "minimum_residual": near.residual_norm,
            "active_weights": near.active_count,
            "dual_lower_bound": near.dual_lower_bound,
            "primal_dual_gap": near.primal_dual_gap,
            "dual_feasibility_violation": near.dual_feasibility_violation,
            "dual_certified": bool(near.dual_certified),
            "farkas_certified": bool(certificate.certified) if certificate is not None else False,
        })
    write_csv(RESULTS / "paper2_fixed_node_feasibility.csv", fixed_rows)

    plt.figure(figsize=(7.2, 4.8))
    plt.semilogy([row["pool_nodes"] for row in fixed_rows], [max(float(row["minimum_residual"]), 1e-16) for row in fixed_rows], marker="o")
    plt.xlabel("Fixed candidate-node count")
    plt.ylabel("Certified minimum moment residual")
    plt.tight_layout()
    plt.savefig(RESULTS / "paper2_fixed_node_residual.png", dpi=180)
    plt.close()

    conditioning = {
        "harmonic_reference": moment_conditioning(Y, ref.weights),
        "enriched_reference": moment_conditioning(enriched, ref.weights),
        "harmonic_reduced": moment_conditioning(real_spherical_harmonics(harmonic_fit.quadrature.nodes, int(config["harmonic_degree"]))[0], harmonic_fit.quadrature.weights),
    }
    quadrature_summary = {
        "reference_nodes": ref.n_node,
        "harmonic_dimension": int(Y.shape[0]),
        "enriched_dimension": int(enriched.shape[0]),
        "harmonic_positive_support": harmonic_fit.quadrature.n_node,
        "enriched_positive_support": enriched_fit.quadrature.n_node,
        "harmonic_max_residual": float(np.max(np.abs(harmonic_fit.residual))),
        "enriched_max_residual": float(np.max(np.abs(enriched_fit.residual))),
        "density": density_checks,
        "conditioning": conditioning,
    }
    (RESULTS / "paper2_quadrature_summary.json").write_text(json.dumps(quadrature_summary, indent=2), encoding="utf-8")

    graph_rows = []
    for n in config["graph_sizes"]:
        q = fibonacci_sphere(int(n))
        graph = fit_graph_generator(q.nodes, q.weights, maximum_degree=2, k_nearest=int(config["graph_k_nearest"]), regularization=float(config["graph_regularization"]))
        spectral = graph.spectral_diagnostics(2)
        nonconstant = [row for row in spectral if row["ell"] > 0]
        structural = graph.structural_residuals()
        graph_rows.append({
            "nodes": int(n),
            "edges": int(graph.edges.shape[0]),
            "fit_residual_norm": graph.fit_residual_norm,
            "max_harmonic_relative_residual": max(row["weighted_relative_residual"] for row in nonconstant),
            "max_harmonic_absolute_residual": max(row["max_absolute_residual"] for row in nonconstant),
            "constant_residual": structural["constant"],
            "weighted_self_adjoint_residual": structural["weighted_self_adjoint"],
            "largest_eigenvalue": structural["largest_eigenvalue"],
            "semigroup_minimum_t_0p02": float(np.min(graph.semigroup(0.02))),
        })
    write_csv(RESULTS / "paper2_graph_convergence.csv", graph_rows)
    plt.figure(figsize=(7.2, 4.8))
    plt.loglog([row["nodes"] for row in graph_rows], [row["max_harmonic_relative_residual"] for row in graph_rows], marker="o")
    plt.xlabel("Angular nodes")
    plt.ylabel("Maximum weighted harmonic residual")
    plt.tight_layout()
    plt.savefig(RESULTS / "paper2_graph_convergence.png", dpi=180)
    plt.close()

    source = fibonacci_sphere(12)
    target = fibonacci_sphere(8)
    FA = np.vstack([np.ones(source.n_node), source.nodes.T])
    FB = np.vstack([np.ones(target.n_node), target.nodes.T])
    universal = universal_positive_transfer(moment_matrix(source, FA), moment_matrix(target, FB))
    axes = PositiveQuadrature(np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]], float), np.full(6, 4*np.pi/6))
    Faxes = np.vstack([np.ones(axes.n_node), axes.nodes.T])
    state = state_specific_positive_remap(np.ones(source.n_node), moment_matrix(source, FA), moment_matrix(axes, Faxes))
    transfer_summary = {
        "universal_12_to_8_feasible": bool(universal.feasible),
        "strict_convexity_check": bool(current_preserving_no_go(source, target)["universal_positive_mass_current_transfer_possible"]),
        "state_specific_isotropic_12_to_6_feasible": bool(state.feasible),
        "state_specific_residual": state.residual_norm,
    }
    (RESULTS / "paper2_transfer_summary.json").write_text(json.dumps(transfer_summary, indent=2), encoding="utf-8")
    return {"quadrature": quadrature_summary, "graphs": graph_rows, "transfer": transfer_summary}


def solve_benchmark(problem: SN2DProblem):
    """Solve without embedding non-reproducible wall-clock data in results."""
    return solve_source_iteration(problem, tolerance=1e-10, maximum_iterations=5000)


def deterministic_work_units(problem: SN2DProblem, iterations: int) -> int:
    """Return a machine-independent first-order work proxy for comparisons."""
    return int(problem.n_unknown * max(int(iterations), 1))


def line_source_problem(order: int) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(-1.0, 1.0, 18), np.linspace(-1.0, 1.0, 18))
    q = circle_quadrature(order, phase=0.5)
    ng, na, nx, ny = 1, q.n_node, grid.nx, grid.ny
    sigma_t = np.full((ng, nx, ny), 0.35)
    sigma_s = np.zeros((ng, ng, nx, ny))
    source = np.zeros((ng, na, nx, ny))
    source[:, :, nx // 2, ny // 2] = 1.0 / (2.0 * np.pi)
    boundary = BoundaryData2D.zeros(ng, na, grid)
    X, Y = np.meshgrid(grid.x_centers, grid.y_centers, indexing="ij")
    kernels = {}
    for k, (cx, cy) in enumerate(((0.72, 0.0), (0.50, 0.50), (-0.55, 0.62))):
        mask = (X - cx) ** 2 + (Y - cy) ** 2 < 0.10**2
        kernel = np.zeros_like(source)
        kernel[:, :, mask] = 1.0
        kernels[f"detector_{k+1}"] = kernel
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, kernels)


def duct_problem(quadrature: PositiveQuadrature) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 2.0, 31), np.linspace(0.0, 1.0, 16))
    q = quadrature
    ng, na, nx, ny = 1, q.n_node, grid.nx, grid.ny
    X, Y = np.meshgrid(grid.x_centers, grid.y_centers, indexing="ij")
    channel = np.abs(Y - 0.5) < 0.085
    sigma_t = np.where(channel, 0.03, 8.0)[None, :, :]
    sigma_s = np.zeros((1, 1, nx, ny))
    source = np.zeros((1, na, nx, ny))
    boundary = BoundaryData2D.zeros(1, na, grid)
    left = boundary.left.copy()
    positive = q.nodes[:, 0] > 0.0
    left[0, positive, :] = np.exp(30.0 * (q.nodes[positive, 0, None] - 1.0))
    boundary = BoundaryData2D(left, boundary.right, boundary.bottom, boundary.top)
    detector = (X > 1.8) & channel
    kernel = np.zeros_like(source)
    kernel[:, :, detector] = 1.0
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, {"duct_exit": kernel})


def response_enriched_duct_rule(reference: PositiveQuadrature, support_target: int = 10) -> PositiveQuadrature:
    phi = np.arctan2(reference.nodes[:, 1], reference.nodes[:, 0])
    rows = [np.ones(reference.n_node)]
    for k in range(1, 4):
        rows.extend([np.cos(k * phi), np.sin(k * phi)])
    rows.extend([
        np.exp(30.0 * (reference.nodes[:, 0] - 1.0)),
        np.exp(18.0 * (reference.nodes[:, 0] - 1.0) - (reference.nodes[:, 1] / 0.12) ** 2),
    ])
    F = np.vstack(rows)
    target = F @ reference.weights
    fit = finite_pool_positive_quadrature(reference.nodes, F, target)
    if fit.quadrature is None:
        raise RuntimeError("response-enriched duct rule was infeasible on its reference pool")
    return fit.quadrature


def grazing_tape_problem(order: int) -> SN2DProblem:
    x_edges = np.linspace(0.0, 1.0, 31)
    y_edges = np.unique(np.concatenate([np.linspace(0.0, 0.4, 17), [0.19, 0.21]]))
    grid = CartesianGrid2D(x_edges, y_edges)
    q = circle_quadrature(order, phase=0.5)
    ng, na, nx, ny = 1, q.n_node, grid.nx, grid.ny
    X, Y = np.meshgrid(grid.x_centers, grid.y_centers, indexing="ij")
    tape = (Y >= 0.19) & (Y <= 0.21)
    sigma_t = np.where(tape, 8.0, 0.08)[None, :, :]
    sigma_s = np.zeros((1, 1, nx, ny))
    source = np.zeros((1, na, nx, ny))
    boundary = BoundaryData2D.zeros(1, na, grid)
    left = boundary.left.copy()
    beam_y = np.abs(grid.y_centers - 0.2) < 0.035
    positive = q.nodes[:, 0] > 0.0
    angular = np.exp(50.0 * (q.nodes[positive, 0] - 1.0) - (q.nodes[positive, 1] / 0.06) ** 2)
    left[0, positive, :] = angular[:, None] * beam_y[None, :]
    boundary = BoundaryData2D(left, boundary.right, boundary.bottom, boundary.top)
    heating = np.zeros_like(source)
    heating[:, :, tape] = 8.0
    transmitted = np.zeros_like(source)
    transmitted[:, :, -2:, :] = 1.0
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, {"tape_heating": heating, "transmitted": transmitted})


def shielded_photon_problem(order: int) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 2.0, 21), np.linspace(0.0, 1.2, 13))
    q = circle_quadrature(order, phase=0.5)
    ng, na, nx, ny = 1, q.n_node, grid.nx, grid.ny
    X, Y = np.meshgrid(grid.x_centers, grid.y_centers, indexing="ij")
    shield = (X > 0.85) & (X < 1.15) & (np.abs(Y - 0.6) > 0.10)
    sigma_t = np.where(shield, 6.0, 0.15)[None, :, :]
    sigma_s = np.zeros((1, 1, nx, ny))
    source = np.zeros((1, na, nx, ny))
    source_region = (X < 0.2) & (np.abs(Y - 0.6) < 0.10)
    source[:, :, source_region] = 0.3
    boundary = BoundaryData2D.zeros(1, na, grid)
    detector = (X > 1.75) & (np.abs(Y - 0.6) < 0.12)
    kernel = np.zeros_like(source)
    kernel[:, :, detector] = 1.0
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, {"shielded_detector": kernel})


def coupled_problem(order: int) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 1.2, 13), np.linspace(0.0, 0.4, 5))
    q = circle_quadrature(order, phase=0.0)
    ng, na, nx, ny = 2, q.n_node, grid.nx, grid.ny
    X = grid.x_centers[:, None] * np.ones((1, ny))
    sigma_t = np.empty((ng, nx, ny))
    sigma_t[0] = 1.4
    sigma_t[1] = 0.9
    tape = (X > 0.5) & (X < 0.7)
    sigma_t[0] += 0.8 * tape
    sigma_t[1] += 0.5 * tape
    sigma_s = np.zeros((ng, ng, nx, ny))
    sigma_s[0, 0] = 0.45
    sigma_s[0, 1] = 0.30
    sigma_s[1, 1] = 0.22
    source = np.zeros((ng, na, nx, ny))
    boundary = BoundaryData2D.zeros(ng, na, grid)
    left = boundary.left.copy()
    positive = q.nodes[:, 0] > 0.0
    left[0, positive, :] = np.exp(12.0 * (q.nodes[positive, 0, None] - 1.0))
    boundary = BoundaryData2D(left, boundary.right, boundary.bottom, boundary.top)
    kernels = {}
    regions = {
        "copper": (X > 0.42) & (X <= 0.5),
        "rebco": tape,
        "substrate": (X >= 0.7) & (X < 0.9),
    }
    for name, mask in regions.items():
        neutron = np.zeros_like(source); neutron[0, :, mask] = 1.0
        photon = np.zeros_like(source); photon[1, :, mask] = 1.0
        heating = np.zeros_like(source); heating[1, :, mask] = 0.68
        kernels[f"{name}_neutron_flux"] = neutron
        kernels[f"{name}_photon_flux"] = photon
        kernels[f"{name}_photon_heating"] = heating
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, kernels)


def benchmark_family(name: str, builder, orders: list[int], response_names: list[str] | None = None) -> list[dict[str, object]]:
    solutions: dict[int, tuple[object, SN2DProblem]] = {}
    for order in orders:
        problem = builder(order)
        solution = solve_benchmark(problem)
        if not solution.converged:
            raise RuntimeError(f"{name} S{order} did not converge")
        solutions[order] = (solution, problem)
    reference_order = max(orders)
    ref = solutions[reference_order][0]
    names = response_names or list(ref.responses)
    rows = []
    for order in orders:
        solution, problem = solutions[order]
        vector_ref = np.array([ref.responses[key] for key in names])
        vector = np.array([solution.responses[key] for key in names])
        error = float(np.linalg.norm(vector - vector_ref) / max(np.linalg.norm(vector_ref), 1e-30))
        balance = global_particle_balance(problem, solution)
        rows.append({
            "benchmark": name,
            "angular_nodes": order,
            "unknowns": problem.n_unknown,
            "iterations": solution.iterations,
            "deterministic_work_units": deterministic_work_units(problem, solution.iterations),
            "relative_response_error": error,
            "minimum_flux": float(np.min(solution.angular_flux)),
            "particle_balance_relative_residual": balance["relative_residual"],
        })
    return rows


def run_transport_benchmarks() -> dict[str, object]:
    orders = [8, 16, 32, 64]
    all_rows = []
    all_rows += benchmark_family("line_source", line_source_problem, orders)
    all_rows += benchmark_family("grazing_thin_tape", grazing_tape_problem, orders)
    all_rows += benchmark_family("isolated_photon_behind_shield", shielded_photon_problem, orders)
    all_rows += benchmark_family("coupled_neutron_photon_multilayer", coupled_problem, [8, 16, 32, 64])

    # Duct standard rules plus one response-enriched positive rule.
    duct_ref_q = circle_quadrature(64, phase=0.5)
    duct_ref_problem = duct_problem(duct_ref_q)
    duct_ref = solve_benchmark(duct_ref_problem)
    reference = duct_ref.responses["duct_exit"]
    for order in orders:
        problem = duct_problem(circle_quadrature(order, phase=0.5))
        solution = solve_benchmark(problem)
        all_rows.append({
            "benchmark": "narrow_streaming_duct",
            "angular_nodes": order,
            "unknowns": problem.n_unknown,
            "iterations": solution.iterations,
            "deterministic_work_units": deterministic_work_units(problem, solution.iterations),
            "relative_response_error": abs(solution.responses["duct_exit"] - reference) / max(abs(reference), 1e-30),
            "minimum_flux": float(np.min(solution.angular_flux)),
            "particle_balance_relative_residual": global_particle_balance(problem, solution)["relative_residual"],
        })
    enriched = response_enriched_duct_rule(duct_ref_q)
    enriched_problem = duct_problem(enriched)
    enriched_solution = solve_benchmark(enriched_problem)
    all_rows.append({
        "benchmark": "narrow_streaming_duct_response_enriched",
        "angular_nodes": enriched.n_node,
        "unknowns": enriched_problem.n_unknown,
        "iterations": enriched_solution.iterations,
        "deterministic_work_units": deterministic_work_units(enriched_problem, enriched_solution.iterations),
        "relative_response_error": abs(enriched_solution.responses["duct_exit"] - reference) / max(abs(reference), 1e-30),
        "minimum_flux": float(np.min(enriched_solution.angular_flux)),
        "particle_balance_relative_residual": global_particle_balance(enriched_problem, enriched_solution)["relative_residual"],
    })
    write_csv(RESULTS / "paper2_transport_cost_error.csv", all_rows)

    # Ray-effect bootstrap diagnostic at the line-source cell.
    coarse_problem = line_source_problem(8)
    coarse_solution = solve_benchmark(coarse_problem)
    # Use a remote off-axis cell, where the coarse S_N solution contains
    # exact zeros because several ray paths have not yet been represented.
    ix, iy = coarse_problem.grid.nx - 3, coarse_problem.grid.ny // 2
    angular_slice = coarse_solution.angular_flux[0, :, ix, iy]
    smoothed = filtered_harmonic_bootstrap(coarse_problem.quadrature.nodes, coarse_problem.quadrature.weights, angular_slice, 3, filter_strength=0.02)
    bootstrap_summary = {
        "raw_zero_or_tiny_directions": int(np.count_nonzero(np.abs(angular_slice) < 1e-14)),
        "filtered_zero_or_tiny_directions": int(np.count_nonzero(np.abs(smoothed) < 1e-14)),
        "raw_angular_variation": float(np.max(angular_slice) - np.min(angular_slice)),
        "filtered_angular_variation": float(np.max(smoothed) - np.min(smoothed)),
    }

    # One exact discrete forward-adjoint check for the coupled benchmark.
    adj_problem = coupled_problem(16)
    adj_solution = solve_benchmark(adj_problem)
    adjoint_check = forward_adjoint_identity(adj_problem, adj_solution, "rebco_photon_heating")
    summary = {
        "rows": len(all_rows),
        "benchmarks": sorted({str(row["benchmark"]) for row in all_rows}),
        "maximum_particle_balance_relative_residual": max(float(row["particle_balance_relative_residual"]) for row in all_rows),
        "minimum_flux_over_all_runs": min(float(row["minimum_flux"]) for row in all_rows),
        "duct_response_enriched_nodes": enriched.n_node,
        "ray_bootstrap": bootstrap_summary,
        "forward_adjoint_check": adjoint_check,
    }
    (RESULTS / "paper2_transport_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    plt.figure(figsize=(7.2, 4.8))
    for benchmark in sorted({str(row["benchmark"]) for row in all_rows if "response_enriched" not in str(row["benchmark"])}):
        rows = [row for row in all_rows if row["benchmark"] == benchmark and float(row["relative_response_error"]) > 0.0]
        if rows:
            plt.loglog([float(row["deterministic_work_units"]) for row in rows], [float(row["relative_response_error"]) for row in rows], marker="o", label=benchmark)
    plt.xlabel("Deterministic work units [unknowns × iterations]")
    plt.ylabel("Relative response error versus S64")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(RESULTS / "paper2_transport_cost_error.png", dpi=180)
    plt.close()
    return summary


def main() -> None:
    summary = {
        "paper1_thin_layer": run_thin_layer(),
        "paper1_multilayer": run_multilayer(),
        "paper2_quadrature_graph": run_quadrature_and_graph(),
        "paper2_transport": run_transport_benchmarks(),
    }
    (RESULTS / "benchmark_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
