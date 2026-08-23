"""Finite, physically bounded P2F HTS coated-conductor verification model.

The neutral field always uses a full positive Boltzmann kernel.  AFP generators
are used only for the separately transported charged-secondary BFP component.
The frozen coefficients are verification surrogates, not evaluated nuclear
data, and no output is interpreted as DPA, retained damage, or a change in Jc.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any

import numpy as np
from numpy.typing import NDArray

from pure_math.acceleration.transport import audit_generator
from pure_math.benchmarking.operators import FrozenOperators, load_frozen_operators
from pure_math.benchmarking.slab import (
    Layer,
    Mesh,
    angular_moments,
    build_mesh,
    normalized_beam,
    product_quadrature,
    reversible_positive_kernel,
    solve_steady_slab,
)

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class Material:
    neutral_scatter: tuple[float, ...]
    neutral_loss: tuple[float, ...]
    neutral_downscatter: tuple[float, ...]
    charged_yield: tuple[float, ...]
    pka_fraction: tuple[float, ...]
    charged_diffusion: tuple[float, ...]
    charged_removal: tuple[float, ...]
    charged_absorption: tuple[float, ...]
    stopping: tuple[float, ...]
    species: tuple[tuple[str, float], ...]


NEUTRAL_ENERGIES_MEV = np.asarray([14.0, 2.0, 0.025], dtype=float)
CHARGED_ENERGIES_MEV = np.asarray([2.0, 0.50, 0.10], dtype=float)


def _material(scale: float, species: tuple[tuple[str, float], ...]) -> Material:
    total = sum(value for _name, value in species)
    normalized = tuple((name, value / total) for name, value in species)
    return Material(
        neutral_scatter=tuple(scale * x for x in (5.0, 3.0, 1.2)),
        neutral_loss=tuple(scale * x for x in (0.24, 0.42, 0.85)),
        neutral_downscatter=tuple(scale * x for x in (0.14, 0.18, 0.0)),
        charged_yield=tuple(scale * x for x in (0.060, 0.085, 0.12)),
        pka_fraction=tuple(x for x in (0.32, 0.46, 0.58)),
        charged_diffusion=tuple(scale * x for x in (9.0, 15.0, 24.0)),
        charged_removal=tuple(scale * x for x in (2.4, 4.2, 7.5)),
        charged_absorption=tuple(scale * x for x in (0.18, 0.35, 0.72)),
        stopping=tuple(scale * x for x in (0.55, 1.10, 2.30)),
        species=normalized,
    )


MATERIALS: dict[str, Material] = {
    "Cu": _material(1.00, (("Cu", 1.0),)),
    "Ag": _material(0.82, (("Ag", 1.0),)),
    "REBCO": _material(1.18, (("Y", 1.0), ("Ba", 2.0), ("Cu", 3.0), ("O", 7.0))),
    "oxide_buffer": _material(0.72, (("Mg", 1.0), ("O", 1.0))),
    "Hastelloy_C276": _material(
        1.08,
        (("Ni", 0.57), ("Cr", 0.16), ("Mo", 0.16), ("Fe", 0.06), ("W", 0.04), ("Co", 0.01)),
    ),
}


def tape_layers(refinement: int = 1) -> tuple[Layer, ...]:
    if refinement < 1:
        raise ValueError("refinement must be positive")
    return (
        Layer("Cu_front", 20.0e-4, 2 * refinement, "Cu"),
        Layer("Ag_cap", 2.0e-4, 1 * refinement, "Ag"),
        Layer("REBCO", 1.0e-4, 2 * refinement, "REBCO"),
        Layer("oxide_buffer", 0.2e-4, 1 * refinement, "oxide_buffer"),
        Layer("Hastelloy_C276", 50.0e-4, 5 * refinement, "Hastelloy_C276"),
        Layer("Cu_back", 20.0e-4, 2 * refinement, "Cu"),
    )


def _beam(normal: FloatArray, polar_degrees: float, azimuth_degrees: float) -> FloatArray:
    theta = math.radians(polar_degrees)
    phi = math.radians(azimuth_degrees)
    tangent1 = np.asarray([1.0, 0.0, 0.0])
    tangent2 = np.asarray([0.0, 1.0, 0.0])
    value = math.cos(theta) * normal + math.sin(theta) * (
        math.cos(phi) * tangent1 + math.sin(phi) * tangent2
    )
    return value / np.linalg.norm(value)


def _positive_reference_generator(nodes: FloatArray, weights: FloatArray) -> FloatArray:
    kernel = reversible_positive_kernel(nodes, weights, concentration=28.0)
    seed = kernel - np.eye(len(weights))
    target = -2.0 * nodes
    image = seed @ nodes
    numerator = float(np.sum(weights[:, None] * image * target))
    denominator = float(np.sum(weights[:, None] * image * image))
    rate = numerator / max(denominator, 1e-30)
    if rate <= 0:
        raise ArithmeticError("reference generator calibration failed")
    return rate * seed


def _cell_material(mesh: Mesh) -> list[Material]:
    return [MATERIALS[mesh.layers[int(index)].material] for index in mesh.layer_index]


def _neutral_transport(
    mesh: Mesh,
    nodes: FloatArray,
    weights: FloatArray,
    normal: FloatArray,
    beam: FloatArray,
    grazing: bool,
) -> dict[str, Any]:
    cells, directions = mesh.cell_count, len(weights)
    materials = _cell_material(mesh)
    group_flux: list[FloatArray] = []
    secondary_source = np.zeros((cells, directions), dtype=float)
    pka_group_source = np.zeros((len(NEUTRAL_ENERGIES_MEV), cells, directions), dtype=float)
    heating = np.zeros(cells, dtype=float)
    source = np.zeros((cells, directions), dtype=float)
    balances: list[float] = []
    minimum = math.inf
    nnz = 0
    outflow = 0.0
    for group, energy in enumerate(NEUTRAL_ENERGIES_MEV):
        concentration = (16.0, 7.0, 2.5)[group]
        kernel = reversible_positive_kernel(nodes, weights, concentration)
        blocks = np.empty((cells, directions, directions), dtype=float)
        loss = np.empty(cells, dtype=float)
        for cell, material in enumerate(materials):
            sigma_s = material.neutral_scatter[group]
            sigma_l = material.neutral_loss[group]
            blocks[cell] = sigma_l * np.eye(directions) + sigma_s * (np.eye(directions) - kernel)
            loss[cell] = sigma_l
        result = solve_steady_slab(
            mesh,
            nodes,
            weights,
            normal,
            blocks,
            loss,
            source,
            inflow_left=(normalized_beam(nodes, weights, beam, 110.0) if group == 0 else None),
            lateral_width_cm=(0.4 if grazing else None),
            lateral_factor=(0.35 if grazing else 0.0),
        )
        flux = result.angular_flux
        group_flux.append(flux)
        balances.append(result.balance_residual)
        minimum = min(minimum, result.minimum_flux)
        nnz = max(nnz, result.matrix_nonzeros)
        outflow += result.left_outflow + result.right_outflow + result.lateral_escape
        for cell, material in enumerate(materials):
            reaction = material.charged_yield[group] * flux[cell]
            isotropic = float(weights @ reaction) * np.ones(directions)
            secondary_source[cell] += 0.70 * reaction + 0.30 * isotropic
            pka_group_source[group, cell] = material.pka_fraction[group] * material.neutral_loss[group] * flux[cell]
            heating[cell] += (
                mesh.widths[cell]
                * material.neutral_loss[group]
                * float(weights @ flux[cell])
                * float(energy)
                * 0.12
            )
        if group + 1 < len(NEUTRAL_ENERGIES_MEV):
            source = np.zeros_like(source)
            for cell, material in enumerate(materials):
                scatter = material.neutral_downscatter[group] * flux[cell]
                source[cell] = 0.55 * scatter + 0.45 * float(weights @ scatter)
    total = np.sum(np.stack(group_flux), axis=0)
    scalar, current, tensor, qn = angular_moments(total, nodes, weights, normal)
    return {
        "groups": group_flux,
        "total": total,
        "scalar": scalar,
        "current": current,
        "tensor": tensor,
        "q_normal": qn,
        "secondary_source": secondary_source,
        "pka_group_source": pka_group_source,
        "heating": heating,
        "minimum_flux": float(minimum),
        "maximum_balance_residual": float(max(balances)),
        "matrix_nonzeros": int(nnz),
        "total_escape": float(outflow),
    }


def _charged_transport(
    mesh: Mesh,
    nodes: FloatArray,
    weights: FloatArray,
    normal: FloatArray,
    generator: FloatArray,
    external_source: FloatArray,
    grazing: bool,
) -> dict[str, Any]:
    cells, directions = mesh.cell_count, len(weights)
    materials = _cell_material(mesh)
    source = np.asarray(external_source, dtype=float)
    group_flux: list[FloatArray] = []
    deposition = np.zeros(cells, dtype=float)
    balances: list[float] = []
    minimum = math.inf
    nnz = 0
    escapes = []
    for group, energy in enumerate(CHARGED_ENERGIES_MEV):
        blocks = np.empty((cells, directions, directions), dtype=float)
        loss = np.empty(cells, dtype=float)
        for cell, material in enumerate(materials):
            absorption = material.charged_absorption[group]
            removal = material.charged_removal[group]
            diffusion = material.charged_diffusion[group]
            blocks[cell] = (absorption + removal) * np.eye(directions) - diffusion * generator
            loss[cell] = absorption + removal
        result = solve_steady_slab(
            mesh,
            nodes,
            weights,
            normal,
            blocks,
            loss,
            source,
            lateral_width_cm=(0.4 if grazing else None),
            lateral_factor=(0.35 if grazing else 0.0),
        )
        flux = result.angular_flux
        group_flux.append(flux)
        balances.append(result.balance_residual)
        minimum = min(minimum, result.minimum_flux)
        nnz = max(nnz, result.matrix_nonzeros)
        escapes.append(result.left_outflow + result.right_outflow + result.lateral_escape)
        for cell, material in enumerate(materials):
            deposition[cell] += (
                mesh.widths[cell]
                * material.stopping[group]
                * float(weights @ flux[cell])
                * float(energy)
            )
        if group + 1 < len(CHARGED_ENERGIES_MEV):
            source = np.zeros_like(source)
            for cell, material in enumerate(materials):
                scatter = material.charged_removal[group] * flux[cell]
                source[cell] = 0.82 * scatter + 0.18 * float(weights @ scatter)
    total = np.sum(np.stack(group_flux), axis=0)
    scalar, current, tensor, qn = angular_moments(total, nodes, weights, normal)
    return {
        "groups": group_flux,
        "total": total,
        "scalar": scalar,
        "current": current,
        "tensor": tensor,
        "q_normal": qn,
        "deposition": deposition,
        "minimum_flux": float(minimum),
        "maximum_balance_residual": float(max(balances)),
        "matrix_nonzeros": int(nnz),
        "escape_by_group": list(map(float, escapes)),
        "total_escape": float(sum(escapes)),
    }


def _layer_crossings(mesh: Mesh, angular: FloatArray, nodes: FloatArray, weights: FloatArray, normal: FloatArray) -> dict[str, float]:
    mu = nodes @ normal
    output: dict[str, float] = {}
    for layer in range(len(mesh.layers) - 1):
        left_cells = np.where(mesh.layer_index == layer)[0]
        right_cells = np.where(mesh.layer_index == layer + 1)[0]
        left, right = int(left_cells[-1]), int(right_cells[0])
        value = float(np.sum(weights[mu > 0] * mu[mu > 0] * angular[left, mu > 0]))
        value += float(np.sum(weights[mu < 0] * (-mu[mu < 0]) * angular[right, mu < 0]))
        output[f"{mesh.layers[layer].name}->{mesh.layers[layer + 1].name}"] = value
    return output


def _integrate_layers(
    mesh: Mesh,
    neutral: dict[str, Any],
    charged: dict[str, Any],
    nodes: FloatArray,
    weights: FloatArray,
    normal: FloatArray,
) -> tuple[dict[str, Any], dict[str, Any]]:
    layers: dict[str, Any] = {}
    species: dict[str, Any] = {}
    for index, layer in enumerate(mesh.layers):
        mask = mesh.layer_index == index
        width = mesh.widths[mask]
        neutral_scalar = float(np.sum(width * neutral["scalar"][mask]))
        charged_scalar = float(np.sum(width * charged["scalar"][mask]))
        neutral_current = np.sum(width[:, None] * neutral["current"][mask], axis=0)
        charged_current = np.sum(width[:, None] * charged["current"][mask], axis=0)
        neutral_tensor = np.sum(width[:, None, None] * neutral["tensor"][mask], axis=0)
        charged_tensor = np.sum(width[:, None, None] * charged["tensor"][mask], axis=0)
        layer_pka: dict[str, Any] = {}
        material = MATERIALS[layer.material]
        for species_name, fraction in material.species:
            spectrum = []
            tensor = np.zeros((3, 3), dtype=float)
            for group in range(len(NEUTRAL_ENERGIES_MEV)):
                field = neutral["pka_group_source"][group, mask]
                total = float(np.sum(width[:, None] * weights[None, :] * field)) * fraction
                spectrum.append(total)
                tensor += fraction * np.einsum(
                    "c,d,cd,di,dj->ij", width, weights, field, nodes, nodes
                )
            layer_pka[species_name] = {
                "group_source": list(map(float, spectrum)),
                "total_source": float(sum(spectrum)),
                "directional_tensor": tensor.tolist(),
            }
        species[layer.name] = layer_pka
        layers[layer.name] = {
            "material": layer.material,
            "thickness_um": 1.0e4 * layer.thickness_cm,
            "neutral_scalar_flux_integral": neutral_scalar,
            "charged_scalar_flux_integral": charged_scalar,
            "neutral_current_integral": neutral_current.tolist(),
            "charged_current_integral": charged_current.tolist(),
            "neutral_traceless_second_moment": neutral_tensor.tolist(),
            "charged_traceless_second_moment": charged_tensor.tolist(),
            "neutral_q_normal": float(normal @ neutral_tensor @ normal),
            "charged_q_normal": float(normal @ charged_tensor @ normal),
            "neutral_heating_proxy": float(np.sum(neutral["heating"][mask])),
            "charged_heating_proxy": float(np.sum(charged["deposition"][mask])),
        }
    return layers, species


def _run_one(
    mesh: Mesh,
    nodes: FloatArray,
    weights: FloatArray,
    generator: FloatArray,
    polar_degrees: float,
    azimuth_degrees: float,
) -> dict[str, Any]:
    normal = np.asarray([0.0, 0.0, 1.0])
    beam = _beam(normal, polar_degrees, azimuth_degrees)
    grazing = polar_degrees >= 80.0
    neutral = _neutral_transport(mesh, nodes, weights, normal, beam, grazing)
    charged = _charged_transport(
        mesh,
        nodes,
        weights,
        normal,
        generator,
        neutral["secondary_source"],
        grazing,
    )
    layers, species = _integrate_layers(mesh, neutral, charged, nodes, weights, normal)
    responses = {
        "REBCO_charged_heating": layers["REBCO"]["charged_heating_proxy"],
        "REBCO_charged_q_normal": layers["REBCO"]["charged_q_normal"],
        "REBCO_charged_scalar": layers["REBCO"]["charged_scalar_flux_integral"],
        "total_heating": float(sum(x["neutral_heating_proxy"] + x["charged_heating_proxy"] for x in layers.values())),
        "charged_escape": charged["total_escape"],
        "substrate_total_PKA_source": float(
            sum(x["total_source"] for x in species["Hastelloy_C276"].values())
        ),
    }
    return {
        "layers": layers,
        "species_resolved_pka": species,
        "charged_interface_crossing": _layer_crossings(mesh, charged["total"], nodes, weights, normal),
        "responses": responses,
        "neutral": {
            "operator": "full positive reversible Boltzmann kernels; never replaced by AFP",
            "minimum_flux": neutral["minimum_flux"],
            "maximum_balance_residual": neutral["maximum_balance_residual"],
            "matrix_nonzeros": neutral["matrix_nonzeros"],
            "total_escape": neutral["total_escape"],
        },
        "charged": {
            "operator": "BFP angular diffusion using the declared generator only",
            "minimum_flux": charged["minimum_flux"],
            "maximum_balance_residual": charged["maximum_balance_residual"],
            "matrix_nonzeros": charged["matrix_nonzeros"],
            "escape_by_group": charged["escape_by_group"],
            "total_escape": charged["total_escape"],
        },
    }


def _scientific_hash(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonicalize_floats(value: Any) -> Any:
    """Remove insignificant BLAS/NumPy serialization drift from evidence.

    Twelve significant decimal digits remain substantially tighter than every
    declared P2F reference-uncertainty gate.  Canonicalizing only after all
    calculations keeps the computation unchanged while making the committed
    record reproducible across the pinned NumPy wheel and compatible patch
    releases.
    """
    if isinstance(value, dict):
        return {key: _canonicalize_floats(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_canonicalize_floats(item) for item in value]
    if isinstance(value, tuple):
        return [_canonicalize_floats(item) for item in value]
    if isinstance(value, (float, np.floating)):
        finite = float(value)
        if not math.isfinite(finite):
            raise ValueError("P2F records must not contain non-finite values")
        if abs(finite) < 1.0e-18:
            return 0.0
        return float(f"{finite:.12g}")
    return value


def _relative_difference(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0e-300)
    return abs(left - right) / scale


def _classify_scientific_outcome(
    *,
    resolved_improvements: int,
    resolved_degradations: int,
    reference_converged: bool,
    operator_response_insensitive: bool,
) -> str:
    if not reference_converged:
        return "INCONCLUSIVE_REFERENCE_NOT_CONVERGED"
    if resolved_improvements and resolved_degradations:
        return "MIXED_RESOLVED_RESPONSE_CHANGES"
    if resolved_improvements:
        return "RESOLVED_IMPROVEMENT_PRESENT"
    if resolved_degradations:
        return "RESOLVED_DEGRADATION_PRESENT"
    if operator_response_insensitive:
        return "INCONCLUSIVE_OPERATOR_INSENSITIVE"
    return "INCONCLUSIVE_BELOW_REFERENCE_RESOLUTION"


def build_manifest() -> dict[str, Any]:
    return {
        "schema": "afp-p2f-hts-manifest-v2",
        "stack_provenance": (
            "synthetic bounded coated-conductor verification stack; dimensions are test "
            "inputs, not validated device or manufacturer data"
        ),
        "layers": [
            {"name": layer.name, "material": layer.material, "thickness_um": 1.0e4 * layer.thickness_cm}
            for layer in tape_layers()
        ],
        "incidence_cases": [
            {"id": "normal", "polar_degrees": 0.0, "azimuth_degrees": 0.0},
            {"id": "oblique", "polar_degrees": 60.0, "azimuth_degrees": 23.0},
            {"id": "grazing", "polar_degrees": 84.0, "azimuth_degrees": 23.0},
        ],
        "neutral_energy_MeV": NEUTRAL_ENERGIES_MEV.tolist(),
        "charged_energy_MeV": CHARGED_ENERGIES_MEV.tolist(),
        "production_nodes": 32,
        "nominal_reference_nodes": 72,
        "medium_reference_nodes": 50,
        "angular_reference_sweep": [
            {"n_mu": 5, "n_phi": 10, "nodes": 50},
            {"n_mu": 6, "n_phi": 12, "nodes": 72},
            {"n_mu": 7, "n_phi": 14, "nodes": 98},
            {"n_mu": 8, "n_phi": 16, "nodes": 128},
        ],
        "reference_convergence_relative_span_limit": 0.05,
        "operator_response_relative_difference_tolerance": 1.0e-10,
        "record_float_significant_digits": 12,
        "record_zero_threshold": 1.0e-18,
        "record_blas_core": "Haswell",
        "physics_firewall": {
            "neutral": "full positive Boltzmann kernel",
            "charged": "AFP/BFP only",
            "nuclear_data": "frozen positive verification surrogates; not evaluated data",
            "excluded": [
                "DPA", "retained defects", "annealing", "Jc", "Tc", "H/He production",
                "full PKA energy spectra", "Monte Carlo replacement",
            ],
        },
    }


def run_p2f() -> dict[str, Any]:
    ops: FrozenOperators = load_frozen_operators()
    mesh = build_mesh(tape_layers(refinement=1))
    fine_mesh = build_mesh(tape_layers(refinement=2))
    manifest = build_manifest()

    reference_operators: dict[str, tuple[int, int, FloatArray, FloatArray, FloatArray]] = {}
    for spec in manifest["angular_reference_sweep"]:
        n_mu = int(spec["n_mu"])
        n_phi = int(spec["n_phi"])
        nodes, weights = product_quadrature(n_mu, n_phi)
        reference_operators[str(len(weights))] = (
            n_mu,
            n_phi,
            nodes,
            weights,
            _positive_reference_generator(nodes, weights),
        )

    cases: list[dict[str, Any]] = []
    for incidence in manifest["incidence_cases"]:
        polar = float(incidence["polar_degrees"])
        azimuth = float(incidence["azimuth_degrees"])
        reference_runs: dict[str, dict[str, Any]] = {}
        reference_sweep: dict[str, Any] = {}
        for node_key, (n_mu, n_phi, nodes, weights, generator) in reference_operators.items():
            reference = _run_one(fine_mesh, nodes, weights, generator, polar, azimuth)
            reference_runs[node_key] = reference
            reference_sweep[node_key] = {
                "n_mu": n_mu,
                "n_phi": n_phi,
                "responses": reference["responses"],
            }

        fine = reference_runs["72"]
        medium = reference_runs["50"]
        fine_nodes = reference_operators["72"][2]
        fine_weights = reference_operators["72"][3]
        fine_generator = reference_operators["72"][4]
        spatial = _run_one(mesh, fine_nodes, fine_weights, fine_generator, polar, azimuth)
        methods = {
            name: _run_one(mesh, ops.nodes, ops.weights, ops.matrices[name], polar, azimuth)
            for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
        }

        convergence_by_response: dict[str, Any] = {}
        span_limit = float(manifest["reference_convergence_relative_span_limit"])
        for key in fine["responses"]:
            values = [float(reference_sweep[node_key]["responses"][key]) for node_key in ("50", "72", "98", "128")]
            scale = max(max(abs(value) for value in values), 1.0e-300)
            relative_span = (max(values) - min(values)) / scale
            convergence_by_response[key] = {
                "relative_span": relative_span,
                "converged": bool(relative_span <= span_limit),
            }
        reference_converged = all(row["converged"] for row in convergence_by_response.values())

        uncertainty: dict[str, Any] = {}
        for key in fine["responses"]:
            angular_component = abs(float(fine["responses"][key]) - float(medium["responses"][key]))
            spatial_component = abs(float(fine["responses"][key]) - float(spatial["responses"][key]))
            uncertainty[key] = {
                "angular_component": angular_component,
                "spatial_component": spatial_component,
                "conservative_sum": angular_component + spatial_component,
                "nominal_reference_converged": bool(convergence_by_response[key]["converged"]),
            }

        errors: dict[str, Any] = {}
        for name, result in methods.items():
            errors[name] = {
                key: abs(float(result["responses"][key]) - float(fine["responses"][key]))
                for key in fine["responses"]
            }

        comparisons: dict[str, Any] = {}
        for key in fine["responses"]:
            baseline_response = float(methods["moment_monotone_baseline"]["responses"][key])
            optimized_response = float(methods["optimized_harmonic_fidelity"]["responses"][key])
            baseline_error = float(errors["moment_monotone_baseline"][key])
            optimized_error = float(errors["optimized_harmonic_fidelity"][key])
            delta = baseline_error - optimized_error
            response_reference_converged = bool(convergence_by_response[key]["converged"])
            resolved = response_reference_converged and (
                abs(delta) > float(uncertainty[key]["conservative_sum"])
            )
            comparisons[key] = {
                "baseline_response": baseline_response,
                "optimized_response": optimized_response,
                "method_absolute_difference": abs(baseline_response - optimized_response),
                "method_relative_difference": _relative_difference(baseline_response, optimized_response),
                "baseline_absolute_error": baseline_error,
                "optimized_absolute_error": optimized_error,
                "reference_uncertainty": uncertainty[key],
                "optimized_improves": optimized_error < baseline_error,
                "difference_resolved_by_reference": resolved,
                "resolved_improvement": bool(resolved and optimized_error < baseline_error),
                "resolved_degradation": bool(resolved and optimized_error > baseline_error),
                "H2_prediction": "optimized error should be smaller because its sampled H2 defect is smaller",
                "observed_direction_matches_H2_prediction": bool(optimized_error < baseline_error),
                "requires_higher_shell_or_transport_information": bool(
                    not (resolved and optimized_error < baseline_error)
                ),
            }

        neutral_hashes = {
            name: _scientific_hash(result["neutral"])
            for name, result in methods.items()
        }
        cases.append(
            {
                "id": incidence["id"],
                "polar_degrees": polar,
                "azimuth_degrees": azimuth,
                "same_nodes_between_methods": True,
                "same_spatial_energy_discretization": True,
                "neutral_operator_identical_between_methods": len(set(neutral_hashes.values())) == 1,
                "nominal_reference": fine,
                "medium_angular_reference": medium,
                "coarse_spatial_reference": spatial,
                "angular_reference_sweep": reference_sweep,
                "reference_convergence": {
                    "relative_span_limit": span_limit,
                    "responses": convergence_by_response,
                    "all_responses_converged": reference_converged,
                },
                "methods": methods,
                "comparisons": comparisons,
            }
        )

    production_audits = {
        name: {
            "h0_residual": report.h0_residual,
            "h1_residual": report.h1_residual,
            "reversibility_residual": report.reversibility_residual,
            "minimum_offdiagonal": report.minimum_offdiagonal,
            "rate_max": report.rate_max,
            "shell_defects": {str(k): float(v) for k, v in report.shell_defects.items()},
            "positive": report.positive,
        }
        for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
        for report in [audit_generator(name, ops.nodes, ops.weights, ops.matrices[name], degrees=(2, 3, 4, 5, 6))]
    }

    comparisons = [row for case in cases for row in case["comparisons"].values()]
    resolved_improvements = sum(int(row["resolved_improvement"]) for row in comparisons)
    resolved_degradations = sum(int(row["resolved_degradation"]) for row in comparisons)
    resolved_differences = sum(int(row["difference_resolved_by_reference"]) for row in comparisons)
    max_method_relative_difference = max(float(row["method_relative_difference"]) for row in comparisons)
    reference_converged = all(bool(case["reference_convergence"]["all_responses_converged"]) for case in cases)
    operator_tolerance = float(manifest["operator_response_relative_difference_tolerance"])
    operator_response_insensitive = max_method_relative_difference <= operator_tolerance
    scientific_outcome = _classify_scientific_outcome(
        resolved_improvements=resolved_improvements,
        resolved_degradations=resolved_degradations,
        reference_converged=reference_converged,
        operator_response_insensitive=operator_response_insensitive,
    )

    result = {
        "schema": "afp-p2f-hts-results-v2",
        "manifest": manifest,
        "operator_registry_sha256": ops.registry["scientific_sha256"],
        "production_operator_audits": production_audits,
        "cases": cases,
        "summary": {
            "resolved_improvement_count": int(resolved_improvements),
            "resolved_degradation_count": int(resolved_degradations),
            "resolved_difference_count": int(resolved_differences),
            "response_comparison_count": int(len(comparisons)),
            "reference_convergence_gate": bool(reference_converged),
            "operator_response_max_relative_difference": max_method_relative_difference,
            "operator_response_insensitive": bool(operator_response_insensitive),
            "scientific_outcome": scientific_outcome,
            "claim_rule": (
                "No AFP response-performance claim is permitted unless the declared reference "
                "convergence gate passes and a baseline/optimized error difference is resolved. "
                "A structurally valid run may therefore have an inconclusive scientific outcome."
            ),
        },
    }
    result = _canonicalize_floats(result)
    result["scientific_sha256"] = _scientific_hash(result)
    return result
