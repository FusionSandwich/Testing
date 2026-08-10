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
        return float(f"{finite:.12g}")
    return value


def build_manifest() -> dict[str, Any]:
    return {
        "schema": "afp-p2f-hts-manifest-v1",
        "stack_provenance": (
            "bounded coated-conductor verification stack chosen within the HTS irradiation "
            "roadmap ranges; dimensions are representative, not a manufacturer certificate"
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
        "fine_reference_nodes": 72,
        "medium_reference_nodes": 50,
        "record_float_significant_digits": 12,
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
    fine_nodes, fine_weights = product_quadrature(6, 12)
    medium_nodes, medium_weights = product_quadrature(5, 10)
    fine_generator = _positive_reference_generator(fine_nodes, fine_weights)
    medium_generator = _positive_reference_generator(medium_nodes, medium_weights)
    manifest = build_manifest()
    cases: list[dict[str, Any]] = []
    for incidence in manifest["incidence_cases"]:
        polar = float(incidence["polar_degrees"])
        azimuth = float(incidence["azimuth_degrees"])
        fine = _run_one(fine_mesh, fine_nodes, fine_weights, fine_generator, polar, azimuth)
        medium = _run_one(fine_mesh, medium_nodes, medium_weights, medium_generator, polar, azimuth)
        spatial = _run_one(mesh, fine_nodes, fine_weights, fine_generator, polar, azimuth)
        methods = {
            name: _run_one(mesh, ops.nodes, ops.weights, ops.matrices[name], polar, azimuth)
            for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
        }
        uncertainty = {}
        for key in fine["responses"]:
            angular_component = abs(float(fine["responses"][key]) - float(medium["responses"][key]))
            spatial_component = abs(float(fine["responses"][key]) - float(spatial["responses"][key]))
            uncertainty[key] = {
                "angular_component": angular_component,
                "spatial_component": spatial_component,
                "conservative_sum": angular_component + spatial_component,
            }
        errors: dict[str, Any] = {}
        for name, result in methods.items():
            errors[name] = {
                key: abs(float(result["responses"][key]) - float(fine["responses"][key]))
                for key in fine["responses"]
            }
        comparisons: dict[str, Any] = {}
        for key in fine["responses"]:
            baseline_error = errors["moment_monotone_baseline"][key]
            optimized_error = errors["optimized_harmonic_fidelity"][key]
            delta = baseline_error - optimized_error
            resolved = abs(delta) > uncertainty[key]["conservative_sum"]
            comparisons[key] = {
                "baseline_absolute_error": baseline_error,
                "optimized_absolute_error": optimized_error,
                "reference_uncertainty": uncertainty[key],
                "optimized_improves": optimized_error < baseline_error,
                "difference_resolved_by_reference": resolved,
                "resolved_improvement": bool(resolved and optimized_error < baseline_error),
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
                "fine_reference": fine,
                "medium_angular_reference": medium,
                "coarse_spatial_reference": spatial,
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
    resolved_improvements = sum(
        int(row["resolved_improvement"])
        for case in cases
        for row in case["comparisons"].values()
    )
    result = {
        "schema": "afp-p2f-hts-results-v1",
        "manifest": manifest,
        "operator_registry_sha256": ops.registry["scientific_sha256"],
        "production_operator_audits": production_audits,
        "cases": cases,
        "summary": {
            "resolved_improvement_count": int(resolved_improvements),
            "response_comparison_count": int(sum(len(case["comparisons"]) for case in cases)),
            "scientific_outcome": (
                "BOUNDED_POSITIVE" if resolved_improvements > 0 else "BOUNDED_NEGATIVE"
            ),
            "claim_rule": (
                "Only resolved improvements may support an AFP response-benefit claim; "
                "all other differences are below reference resolution or unfavorable."
            ),
        },
    }
    result = _canonicalize_floats(result)
    result["scientific_sha256"] = _scientific_hash(result)
    return result
