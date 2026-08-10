"""The seven preregistered P2E benchmark families.

Physical cases are bounded verification models.  The electron case reproduces
the published 10 MeV-water geometry and multigroup structure, but its frozen
coefficient table is a documented verification surrogate rather than a claim
of reproducing Radiant or evaluated material data.  P2F supplies the separate
HTS engineering-scope firewall.
"""
from __future__ import annotations

import math
import time
import tracemalloc
from typing import Any, Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy import linalg

from pure_math.acceleration.core import preconditioned_gmres
from pure_math.acceleration.transport import (
    audit_generator,
    real_harmonic_samples,
    sampled_shell_defect,
    weighted_harmonic_frame,
    weighted_spectral_operator,
)

from .metrics import (
    aggregate_error,
    dataclass_dict,
    equal_cost_record,
    response_error,
    response_from_angular,
    rotation_spread,
)
from .operators import FrozenOperators
from .slab import (
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




def _oblique_direction(normal: ArrayLike, polar_degrees: float, azimuth_degrees: float = 0.0) -> FloatArray:
    n = np.asarray(normal, dtype=float)
    n /= np.linalg.norm(n)
    helper = np.asarray([0.0, 0.0, 1.0]) if abs(n[2]) < 0.9 else np.asarray([0.0, 1.0, 0.0])
    tangent1 = np.cross(helper, n)
    tangent1 /= np.linalg.norm(tangent1)
    tangent2 = np.cross(n, tangent1)
    theta = math.radians(polar_degrees)
    phi = math.radians(azimuth_degrees)
    direction = math.cos(theta) * n + math.sin(theta) * (math.cos(phi) * tangent1 + math.sin(phi) * tangent2)
    return direction / np.linalg.norm(direction)

def _operator_record(ops: FrozenOperators, name: str) -> dict[str, Any]:
    audit = audit_generator(name, ops.nodes, ops.weights, ops.matrices[name], degrees=(2, 3, 4, 5, 6))
    return {
        "conservation_residual": audit.h0_residual,
        "h0_residual": audit.h0_residual,
        "h1_residual": audit.h1_residual,
        "reversibility_residual": audit.reversibility_residual,
        "minimum_offdiagonal": audit.minimum_offdiagonal,
        "positive_generator": audit.positive,
        "rate_max": audit.rate_max,
        "stiffness": audit.rate_max,
        "shell_defects": {str(k): float(v) for k, v in audit.shell_defects.items()},
    }


def _spectral_reference(nodes: FloatArray, weights: FloatArray) -> FloatArray:
    frame = weighted_harmonic_frame(nodes, weights, maximum_degree=20)
    degree = frame.degrees.astype(float)
    return weighted_spectral_operator(frame, -degree * (degree + 1.0))


def _mode_function(nodes: FloatArray, degree: int, order_index: int) -> FloatArray:
    samples = np.ones((len(nodes), 1)) if degree == 0 else real_harmonic_samples(nodes, degree)
    return samples[:, order_index % samples.shape[1]]


def _angular_method(
    ops: FrozenOperators,
    name: str,
    initial: FloatArray,
    time_value: float,
    diffusion: float,
    normal: FloatArray,
    reference_response: Any,
    *,
    reference_value: FloatArray | None = None,
    linear_response: FloatArray | None = None,
) -> dict[str, Any]:
    started = time.perf_counter()
    tracemalloc.start()
    try:
        value = linalg.expm(time_value * diffusion * ops.matrices[name]) @ initial
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    response = response_from_angular(value, ops.nodes, ops.weights, normal)
    error = response_error(response, reference_response)
    row = _operator_record(ops, name)
    l2_error = None
    linear_value = None
    linear_error = None
    if reference_value is not None:
        l2_error = float(np.sqrt(np.sum(ops.weights * (value - reference_value) ** 2)))
    if linear_response is not None and reference_value is not None:
        q = np.asarray(linear_response, dtype=float)
        qnorm = float(np.sqrt(np.sum(ops.weights * q * q)))
        if qnorm <= 0:
            raise ValueError("linear response must be nonzero")
        q = q / qnorm
        linear_value = float(np.sum(ops.weights * q * value))
        linear_reference = float(np.sum(ops.weights * q * reference_value))
        linear_error = abs(linear_value - linear_reference)
    row.update(
        {
            "minimum_flux": float(np.min(value)),
            "input_nonnegative": bool(np.min(initial) >= -2e-11),
            "positivity_applicable": bool(np.min(initial) >= -2e-11),
            "positivity": bool(row["positive_generator"] and (np.min(initial) < -2e-11 or np.min(value) >= -2e-11)),
            "mass_error": abs(float(ops.weights @ value) - float(ops.weights @ initial)),
            "scalar_error": error.scalar,
            "current_error": error.current,
            "tensor_error": error.tensor,
            "q_normal_error": error.q_normal,
            "response_error": float(linear_error if linear_error is not None else error.response),
            "aggregate_error": float(
                l2_error / max(float(np.sqrt(np.sum(ops.weights * np.asarray(reference_value) ** 2))), 1e-14)
                if l2_error is not None and reference_value is not None
                else aggregate_error(error, reference_response)
            ),
            "angular_l2_error": l2_error,
            "linear_response_value": linear_value,
            "response": dataclass_dict(response),
            "iterations": 1,
            "matvecs": 1,
            "linear_solves": 0,
            "runtime_seconds": float(elapsed),
            "memory_bytes": int(peak),
        }
    )
    return row


def individual_modes_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    settings = {
        "training": (2, 1, 0.11, 0.70),
        "validation": (3, 4, 0.09, 0.55),
        "heldout": (4, 6, 0.075, 0.63),
    }
    degree, order, t, diffusion = settings[partition]
    initial = _mode_function(ops.nodes, degree, order)
    decay = math.exp(-diffusion * degree * (degree + 1) * t)
    reference_value = decay * initial
    normal = np.asarray([0.37, -0.29, 0.882])
    normal /= np.linalg.norm(normal)
    reference = response_from_angular(reference_value, ops.nodes, ops.weights, normal)
    methods = {
        name: _angular_method(
            ops, name, initial, t, diffusion, normal, reference,
            reference_value=reference_value, linear_response=initial,
        )
        for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
    }
    return _finalize_case(
        ops,
        "P2E-01",
        "individual_Ylm_decay",
        partition,
        methods,
        reference,
        {"type": "analytic_harmonic_decay", "uncertainty": 0.0, "degree": degree, "order_index": order},
    )


def random_bandlimited_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    seeds = {"training": 1027, "validation": 8102, "heldout": 20260807}
    maximum = {"training": 4, "validation": 5, "heldout": 6}[partition]
    rng = np.random.default_rng(seeds[partition])
    t, diffusion = 0.065, 0.48
    initial = np.zeros(len(ops.nodes))
    reference_value = np.zeros(len(ops.nodes))
    coefficient_digest: list[float] = []
    for degree in range(maximum + 1):
        samples = np.ones((len(ops.nodes), 1)) if degree == 0 else real_harmonic_samples(ops.nodes, degree)
        coefficients = rng.normal(size=samples.shape[1]) / (1.0 + degree) ** 1.5
        coefficient_digest.extend(map(float, coefficients))
        initial += samples @ coefficients
        reference_value += math.exp(-diffusion * degree * (degree + 1) * t) * (samples @ coefficients)
    shift = max(0.0, -float(np.min(initial)) + 0.05)
    initial += shift
    reference_value += shift
    normal = np.asarray([-0.41, 0.73, 0.547])
    normal /= np.linalg.norm(normal)
    reference = response_from_angular(reference_value, ops.nodes, ops.weights, normal)
    methods = {
        name: _angular_method(
            ops, name, initial, t, diffusion, normal, reference,
            reference_value=reference_value, linear_response=initial,
        )
        for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
    }
    return _finalize_case(
        ops,
        "P2E-02",
        "random_band_limited_data",
        partition,
        methods,
        reference,
        {
            "type": "analytic_shell_decay",
            "uncertainty": 0.0,
            "seed": seeds[partition],
            "maximum_degree": maximum,
            "coefficient_l2": float(np.linalg.norm(coefficient_digest)),
        },
    )


def _fine_angular_reference(
    n_mu: int,
    n_phi: int,
    beam_direction: FloatArray,
    concentration: float,
    t: float,
    diffusion: float,
    normal: FloatArray,
) -> tuple[Any, FloatArray, FloatArray, FloatArray]:
    nodes, weights = product_quadrature(n_mu, n_phi)
    initial = normalized_beam(nodes, weights, beam_direction, concentration)
    operator = _spectral_reference(nodes, weights)
    value = linalg.expm(t * diffusion * operator) @ initial
    return response_from_angular(value, nodes, weights, normal), nodes, weights, value


def narrow_beam_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    parameters = {
        "training": (28.0, 0.060, np.asarray([0.2, 0.1, 0.9747])),
        "validation": (45.0, 0.045, np.asarray([-0.31, 0.44, 0.842])),
        "heldout": (70.0, 0.037, np.asarray([0.521, -0.173, 0.836])),
    }
    concentration, t, beam = parameters[partition]
    beam /= np.linalg.norm(beam)
    normal = np.asarray([0.13, 0.71, 0.692])
    normal /= np.linalg.norm(normal)
    diffusion = 0.34
    fine, _, _, _ = _fine_angular_reference(7, 14, beam, concentration, t, diffusion, normal)
    medium, _, _, _ = _fine_angular_reference(6, 12, beam, concentration, t, diffusion, normal)
    uncertainty = abs(fine.response - medium.response)
    initial = normalized_beam(ops.nodes, ops.weights, beam, concentration)
    methods = {
        name: _angular_method(ops, name, initial, t, diffusion, normal, fine)
        for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity")
    }
    rotations = [
        np.asarray([0.0, 0.0, 1.0]),
        np.asarray([1.0, 1.0, 1.0]) / math.sqrt(3.0),
        np.asarray([0.63, -0.41, 0.659]),
        np.asarray([-0.28, 0.86, 0.426]),
    ]
    for name in methods:
        values: list[float] = []
        for direction in rotations:
            direction /= np.linalg.norm(direction)
            init = normalized_beam(ops.nodes, ops.weights, direction, concentration)
            out = linalg.expm(t * diffusion * ops.matrices[name]) @ init
            values.append(response_from_angular(out, ops.nodes, ops.weights, normal).response)
        methods[name]["rotation_responses"] = values
        methods[name]["rotation_spread"] = rotation_spread(values)
    return _finalize_case(
        ops,
        "P2E-03",
        "narrow_beam_angular_diffusion",
        partition,
        methods,
        fine,
        {
            "type": "fine_sampled_spectral_Laplace_Beltrami",
            "directions": 98,
            "medium_directions": 72,
            "uncertainty": float(uncertainty),
        },
    )


def _charged_multigroup(
    nodes: FloatArray,
    weights: FloatArray,
    generator: FloatArray,
    mesh: Mesh,
    normal: FloatArray,
    beam_direction: FloatArray,
    energies: FloatArray,
    diffusion: FloatArray,
    removal: FloatArray,
    absorption: FloatArray,
    stopping: FloatArray,
    *,
    concentration: float,
    lateral_width_cm: float | None = None,
    lateral_factor: float = 0.0,
) -> dict[str, Any]:
    cells, directions = mesh.cell_count, len(weights)
    group_fluxes: list[FloatArray] = []
    deposition = np.zeros(cells)
    source = np.zeros((cells, directions))
    inflow = normalized_beam(nodes, weights, beam_direction, concentration)
    total_runtime = 0.0
    peak = 0
    min_flux = float("inf")
    maximum_balance = 0.0
    linear_solves = 0
    final_solution = None
    for group, energy in enumerate(energies):
        blocks = np.repeat(
            (absorption[group] + removal[group]) * np.eye(directions)[None, :, :]
            - diffusion[group] * generator[None, :, :],
            cells,
            axis=0,
        )
        result = solve_steady_slab(
            mesh,
            nodes,
            weights,
            normal,
            blocks,
            np.full(cells, absorption[group] + removal[group]),
            source,
            inflow_left=inflow if group == 0 else None,
            lateral_width_cm=lateral_width_cm,
            lateral_factor=lateral_factor,
        )
        final_solution = result
        group_fluxes.append(result.angular_flux)
        total_runtime += result.solve_seconds
        peak = max(peak, result.peak_memory_bytes)
        min_flux = min(min_flux, result.minimum_flux)
        maximum_balance = max(maximum_balance, result.balance_residual)
        linear_solves += 1
        deposition += mesh.widths * stopping[group] * result.scalar_flux
        if group + 1 < len(energies):
            isotropic = result.scalar_flux[:, None] * np.ones((1, directions))
            source = removal[group] * (0.88 * result.angular_flux + 0.12 * isotropic)
    assert final_solution is not None
    total_flux = np.sum(np.stack(group_fluxes), axis=0)
    scalar, current, tensor, qn = angular_moments(total_flux, nodes, weights, normal)
    return {
        "angular_flux_groups": group_fluxes,
        "total_angular_flux": total_flux,
        "scalar": scalar,
        "current": current,
        "tensor": tensor,
        "q_normal": qn,
        "deposition": deposition,
        "total_deposition": float(np.sum(deposition)),
        "minimum_flux": float(min_flux),
        "balance_residual": float(maximum_balance),
        "left_outflow": final_solution.left_outflow,
        "right_outflow": final_solution.right_outflow,
        "lateral_escape": final_solution.lateral_escape,
        "runtime_seconds": float(total_runtime),
        "memory_bytes": int(peak),
        "linear_solves": int(linear_solves),
        "matrix_nonzeros": int(final_solution.matrix_nonzeros),
    }


def _charged_response(result: dict[str, Any], mesh: Mesh, layer: int | None = None, *, response_kind: str = "q_normal") -> dict[str, Any]:
    if layer is None:
        mask = np.ones(mesh.cell_count, dtype=bool)
    else:
        mask = mesh.layer_index == layer
    weight = mesh.widths[mask]
    scalar = float(np.sum(weight * result["scalar"][mask]))
    current = np.sum(weight[:, None] * result["current"][mask], axis=0)
    tensor = np.sum(weight[:, None, None] * result["tensor"][mask], axis=0)
    qn = float(np.sum(weight * result["q_normal"][mask]))
    deposition = float(np.sum(result["deposition"][mask]))
    if response_kind == "q_normal":
        response = qn
    elif response_kind == "deposition":
        response = deposition
    elif response_kind == "tensor_normalized":
        response = qn / max(abs(scalar), 1e-14)
    else:
        raise ValueError(f"unsupported response_kind {response_kind!r}")
    return {
        "scalar": scalar,
        "current": current,
        "tensor": tensor,
        "q_normal": qn,
        "deposition": deposition,
        "response": float(response),
        "response_kind": response_kind,
    }


def _charged_error(value: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    return {
        "scalar": abs(value["scalar"] - reference["scalar"]),
        "current": float(np.linalg.norm(value["current"] - reference["current"])),
        "tensor": float(np.linalg.norm(value["tensor"] - reference["tensor"], ord="fro")),
        "q_normal": abs(value["q_normal"] - reference["q_normal"]),
        "deposition": abs(value["deposition"] - reference["deposition"]),
        "response": abs(value["response"] - reference["response"]),
    }


def _charged_case_methods(
    ops: FrozenOperators,
    mesh: Mesh,
    normal: FloatArray,
    beam: FloatArray,
    energies: FloatArray,
    diffusion: FloatArray,
    removal: FloatArray,
    absorption: FloatArray,
    stopping: FloatArray,
    reference: dict[str, Any],
    *,
    concentration: float,
    response_layer: int | None,
    lateral_width_cm: float | None = None,
    lateral_factor: float = 0.0,
    response_kind: str = "q_normal",
) -> dict[str, Any]:
    methods: dict[str, Any] = {}
    for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity"):
        result = _charged_multigroup(
            ops.nodes,
            ops.weights,
            ops.matrices[name],
            mesh,
            normal,
            beam,
            energies,
            diffusion,
            removal,
            absorption,
            stopping,
            concentration=concentration,
            lateral_width_cm=lateral_width_cm,
            lateral_factor=lateral_factor,
        )
        response = _charged_response(result, mesh, response_layer, response_kind=response_kind)
        error = _charged_error(response, reference)
        audit = _operator_record(ops, name)
        scale = max(abs(reference["response"]), 1e-12)
        audit.update(
            {
                "minimum_flux": result["minimum_flux"],
                "input_nonnegative": True,
                "positivity_applicable": True,
                "positivity": result["minimum_flux"] >= -2e-10,
                "transport_balance_residual": result["balance_residual"],
                "scalar_error": error["scalar"],
                "current_error": error["current"],
                "tensor_error": error["tensor"],
                "q_normal_error": error["q_normal"],
                "response_error": error["response"],
                "deposition_error": error["deposition"],
                "aggregate_error": float(
                    np.linalg.norm(
                        [
                            error["scalar"] / max(abs(reference["scalar"]), 1e-12),
                            error["current"] / max(np.linalg.norm(reference["current"]), 1e-12),
                            error["tensor"] / max(np.linalg.norm(reference["tensor"]), 1e-12),
                            error["q_normal"] / max(abs(reference["q_normal"]), 1e-12),
                            error["response"] / scale,
                        ]
                    )
                    / math.sqrt(5.0)
                ),
                "response": _json_response(response),
                "iterations": result["linear_solves"],
                "matvecs": 0,
                "linear_solves": result["linear_solves"],
                "runtime_seconds": result["runtime_seconds"],
                "memory_bytes": result["memory_bytes"],
                "matrix_nonzeros": result["matrix_nonzeros"],
                "left_outflow": result["left_outflow"],
                "right_outflow": result["right_outflow"],
                "lateral_escape": result["lateral_escape"],
            }
        )
        methods[name] = audit
    return methods


def _json_response(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "scalar": float(row["scalar"]),
        "current": np.asarray(row["current"]).tolist(),
        "tensor": np.asarray(row["tensor"]).tolist(),
        "q_normal": float(row["q_normal"]),
        "deposition": float(row["deposition"]),
        "response": float(row["response"]),
        "response_kind": str(row.get("response_kind", "unspecified")),
    }


def electron_deposition_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    # Published geometry: pure 10 MeV electrons in a 5 cm water slab, 40
    # logarithmic groups down to 1 keV.  Coefficients below are frozen
    # verification surrogates and are not represented as Radiant cross sections.
    cells = {"training": 24, "validation": 32, "heldout": 40}[partition]
    mesh = build_mesh([Layer("water", 5.0, cells, "liquid_water")])
    normal = np.asarray([0.0, 0.0, 1.0])
    beam = np.asarray([0.0, 0.0, 1.0])
    energies = np.geomspace(10.0, 0.001, 40)
    diffusion = 0.025 + 0.19 / np.sqrt(energies + 0.03)
    removal = 0.22 + 0.34 / np.sqrt(energies + 0.02)
    absorption = 0.015 + 0.012 / np.sqrt(energies + 0.02)
    stopping = 0.16 + 0.07 * np.log1p(1.0 / energies)
    fine_nodes, fine_weights = product_quadrature(6, 12)
    medium_nodes, medium_weights = product_quadrature(5, 10)
    fine_result = _charged_multigroup(
        fine_nodes,
        fine_weights,
        _spectral_reference(fine_nodes, fine_weights),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=180.0,
    )
    medium_result = _charged_multigroup(
        medium_nodes,
        medium_weights,
        _spectral_reference(medium_nodes, medium_weights),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=180.0,
    )
    reference = _charged_response(fine_result, mesh, None, response_kind="deposition")
    medium = _charged_response(medium_result, mesh, None, response_kind="deposition")
    uncertainty = abs(reference["response"] - medium["response"])
    methods = _charged_case_methods(
        ops,
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        reference,
        concentration=180.0,
        response_layer=None,
        response_kind="deposition",
    )
    return _finalize_case(
        ops,
        "P2E-04",
        "published_geometry_10MeV_electron_water_deposition",
        partition,
        methods,
        _json_response(reference),
        {
            "type": "fine_angular_spectral_reference",
            "fine_directions": 72,
            "medium_directions": 50,
            "uncertainty": float(uncertainty),
            "geometry_provenance": "Bienvenue et al. 2025: 10 MeV electron, water, 5 cm, 40 log groups, 1 keV cutoff",
            "coefficient_scope": "frozen positive verification surrogate; not Radiant/evaluated cross sections",
        },
    )


def neutron_bfp_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    cells = {"training": 24, "validation": 36, "heldout": 48}[partition]
    concentration = {"training": 18.0, "validation": 28.0, "heldout": 42.0}[partition]
    mesh = build_mesh([Layer("fast_medium", 8.0, cells, "forward_elastic_medium")])
    normals = {
        "training": np.asarray([0.43, -0.21, 0.878]),
        "validation": np.asarray([-0.36, 0.57, 0.738]),
        "heldout": np.asarray([0.61, -0.44, 0.659]),
    }
    normal = normals[partition] / np.linalg.norm(normals[partition])
    beam = _oblique_direction(normal, 18.0, 31.0)
    sigma_s, sigma_a = 0.82, 0.035

    def solve_full(nodes: FloatArray, weights: FloatArray) -> dict[str, Any]:
        kernel = reversible_positive_kernel(nodes, weights, concentration)
        block = sigma_a * np.eye(len(weights)) + sigma_s * (np.eye(len(weights)) - kernel)
        result = solve_steady_slab(
            mesh,
            nodes,
            weights,
            normal,
            np.repeat(block[None, :, :], mesh.cell_count, axis=0),
            np.full(mesh.cell_count, sigma_a),
            np.zeros((mesh.cell_count, len(weights))),
            inflow_left=normalized_beam(nodes, weights, beam, 100.0),
        )
        return {
            "result": result,
            "response": _charged_response(
                {
                    "scalar": result.scalar_flux,
                    "current": result.current,
                    "tensor": result.tensor,
                    "q_normal": result.q_normal,
                    "deposition": mesh.widths * sigma_a * result.scalar_flux,
                },
                mesh,
                None,
                response_kind="q_normal",
            ),
            "kernel": kernel,
        }

    fn, fw = product_quadrature(6, 12)
    mn, mw = product_quadrature(5, 10)
    fine = solve_full(fn, fw)
    medium = solve_full(mn, mw)
    reference = fine["response"]
    uncertainty = abs(reference["response"] - medium["response"]["response"])

    methods: dict[str, Any] = {}
    # Match the full-kernel first moment on the production nodes.
    kernel32 = reversible_positive_kernel(ops.nodes, ops.weights, concentration)
    cosine = ops.nodes @ ops.nodes.T
    first = float(np.sum(ops.weights[:, None] * ops.weights[None, :] * kernel32 * cosine))
    diffusion_scale = 0.5 * sigma_s * max(0.0, 1.0 - first)
    for name in ("moment_monotone_baseline", "optimized_harmonic_fidelity"):
        block = sigma_a * np.eye(len(ops.weights)) - diffusion_scale * ops.matrices[name]
        result = solve_steady_slab(
            mesh,
            ops.nodes,
            ops.weights,
            normal,
            np.repeat(block[None, :, :], mesh.cell_count, axis=0),
            np.full(mesh.cell_count, sigma_a),
            np.zeros((mesh.cell_count, len(ops.weights))),
            inflow_left=normalized_beam(ops.nodes, ops.weights, beam, 100.0),
        )
        response = _charged_response(
            {
                "scalar": result.scalar_flux,
                "current": result.current,
                "tensor": result.tensor,
                "q_normal": result.q_normal,
                "deposition": mesh.widths * sigma_a * result.scalar_flux,
            },
            mesh,
            None,
        )
        error = _charged_error(response, reference)
        row = _operator_record(ops, name)
        row.update(
            {
                "minimum_flux": result.minimum_flux,
                "input_nonnegative": True,
                "positivity_applicable": True,
                "positivity": result.minimum_flux >= -2e-10,
                "transport_balance_residual": result.balance_residual,
                "scalar_error": error["scalar"],
                "current_error": error["current"],
                "tensor_error": error["tensor"],
                "q_normal_error": error["q_normal"],
                "response_error": error["response"],
                "aggregate_error": error["response"] / max(abs(reference["response"]), 1e-12),
                "response": _json_response(response),
                "iterations": 1,
                "matvecs": 0,
                "linear_solves": 1,
                "runtime_seconds": result.solve_seconds,
                "memory_bytes": result.peak_memory_bytes,
                "matrix_nonzeros": result.matrix_nonzeros,
                "matched_first_moment": first,
                "diffusion_scale": diffusion_scale,
            }
        )
        methods[name] = row
    return _finalize_case(
        ops,
        "P2E-05",
        "justified_forward_elastic_neutron_BFP",
        partition,
        methods,
        _json_response(reference),
        {
            "type": "full_positive_reversible_Boltzmann_kernel_fine_angular",
            "fine_directions": 72,
            "medium_directions": 50,
            "uncertainty": float(uncertainty),
            "kernel_concentration": concentration,
            "approximation_scope": "first-moment-matched forward-peaked BFP verification",
        },
    )


def proton_layered_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    refinement = {"training": 1, "validation": 2, "heldout": 3}[partition]
    mesh = build_mesh(
        [
            Layer("Al", 0.050, 4 * refinement, "Al"),
            Layer("Cu", 0.030, 4 * refinement, "Cu"),
            Layer("water", 0.080, 6 * refinement, "water"),
        ]
    )
    normals = {
        "training": np.asarray([0.29, 0.41, 0.865]),
        "validation": np.asarray([-0.47, 0.22, 0.855]),
        "heldout": np.asarray([0.37, -0.56, 0.741]),
    }
    normal = normals[partition] / np.linalg.norm(normals[partition])
    beam = _oblique_direction(normal, 25.0, 17.0)
    energies = np.geomspace(50.0, 1.0, 10)
    diffusion = 0.18 + 0.35 / np.sqrt(energies)
    removal = 0.35 + 0.65 / np.sqrt(energies)
    absorption = 0.01 + 0.025 / np.sqrt(energies)
    stopping = 0.30 + 0.42 / np.sqrt(energies)
    fn, fw = product_quadrature(6, 12)
    mn, mw = product_quadrature(5, 10)
    fine_result = _charged_multigroup(
        fn,
        fw,
        _spectral_reference(fn, fw),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=120.0,
    )
    medium_result = _charged_multigroup(
        mn,
        mw,
        _spectral_reference(mn, mw),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=120.0,
    )
    reference = _charged_response(fine_result, mesh, 1, response_kind="q_normal")
    medium = _charged_response(medium_result, mesh, 1, response_kind="q_normal")
    uncertainty = abs(reference["response"] - medium["response"])
    methods = _charged_case_methods(
        ops,
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        reference,
        concentration=120.0,
        response_layer=1,
        response_kind="q_normal",
    )
    return _finalize_case(
        ops,
        "P2E-06",
        "proton_multiple_scattering_layered_target",
        partition,
        methods,
        _json_response(reference),
        {
            "type": "fine_angular_spectral_BFP_reference",
            "fine_directions": 72,
            "medium_directions": 50,
            "uncertainty": float(uncertainty),
            "response_layer": "Cu",
        },
    )


def hts_oblique_case(ops: FrozenOperators, partition: str) -> dict[str, Any]:
    refinement = {"training": 1, "validation": 2, "heldout": 3}[partition]
    mesh = build_mesh(
        [
            Layer("Cu_front", 20e-4, 2 * refinement, "Cu"),
            Layer("Ag", 2e-4, 1 * refinement, "Ag"),
            Layer("REBCO", 1.2e-4, 2 * refinement, "REBCO"),
            Layer("buffer", 0.5e-4, 1 * refinement, "oxide_buffer"),
            Layer("Hastelloy", 50e-4, 4 * refinement, "Hastelloy_C276"),
            Layer("Cu_back", 20e-4, 2 * refinement, "Cu"),
        ]
    )
    normals = {
        "training": np.asarray([0.25, 0.48, 0.841]),
        "validation": np.asarray([-0.42, 0.31, 0.853]),
        "heldout": np.asarray([0.53, -0.36, 0.768]),
    }
    normal = normals[partition] / np.linalg.norm(normals[partition])
    beam = _oblique_direction(normal, 60.0, 23.0)
    energies = np.geomspace(20.0, 0.25, 8)
    diffusion = 1.2 + 2.2 / np.sqrt(energies)
    removal = 0.22 + 0.55 / np.sqrt(energies)
    absorption = 0.01 + 0.02 / np.sqrt(energies)
    stopping = 1.1 + 1.8 / np.sqrt(energies)
    fn, fw = product_quadrature(6, 12)
    mn, mw = product_quadrature(5, 10)
    fine_result = _charged_multigroup(
        fn,
        fw,
        _spectral_reference(fn, fw),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=150.0,
        lateral_width_cm=0.4,
        lateral_factor=0.35,
    )
    medium_result = _charged_multigroup(
        mn,
        mw,
        _spectral_reference(mn, mw),
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        concentration=150.0,
        lateral_width_cm=0.4,
        lateral_factor=0.35,
    )
    reference = _charged_response(fine_result, mesh, 2, response_kind="q_normal")
    medium = _charged_response(medium_result, mesh, 2, response_kind="q_normal")
    uncertainty = abs(reference["response"] - medium["response"])
    methods = _charged_case_methods(
        ops,
        mesh,
        normal,
        beam,
        energies,
        diffusion,
        removal,
        absorption,
        stopping,
        reference,
        concentration=150.0,
        response_layer=2,
        lateral_width_cm=0.4,
        lateral_factor=0.35,
        response_kind="q_normal",
    )
    # Collision/orientation spread at fixed quadrature.  The full P2F case adds
    # neutral and secondary fields and a dedicated grazing engineering audit.
    angles = [0.0, 27.0, 60.0, 82.0]
    for name in methods:
        responses: list[float] = []
        for angle in angles:
            theta = math.radians(angle)
            direction = _oblique_direction(normal, angle, 23.0)
            compact = _charged_multigroup(
                ops.nodes,
                ops.weights,
                ops.matrices[name],
                mesh,
                normal,
                direction,
                energies[:3],
                diffusion[:3],
                removal[:3],
                absorption[:3],
                stopping[:3],
                concentration=120.0,
                lateral_width_cm=0.4,
                lateral_factor=0.35,
            )
            responses.append(_charged_response(compact, mesh, 2, response_kind="q_normal")["response"])
        methods[name]["rotation_responses"] = list(map(float, responses))
        methods[name]["rotation_spread"] = rotation_spread(responses)
    return _finalize_case(
        ops,
        "P2E-07",
        "oblique_HTS_tape_stack",
        partition,
        methods,
        _json_response(reference),
        {
            "type": "fine_angular_spectral_BFP_reference",
            "fine_directions": 72,
            "medium_directions": 50,
            "uncertainty": float(uncertainty),
            "response_layer": "REBCO",
            "scope": "charged-particle layered benchmark; full neutral/secondary P2F model is separate",
        },
    )


def accelerator_ablation(ops: FrozenOperators) -> dict[str, Any]:
    # A common high-order matrix and source; only the preconditioner changes.
    frame = weighted_harmonic_frame(ops.nodes, ops.weights, maximum_degree=15)
    degree = frame.degrees.astype(float)
    high_collision = weighted_spectral_operator(frame, 0.04 + 0.32 * degree * (degree + 1.0))
    normal = np.asarray([0.31, -0.27, 0.912])
    normal /= np.linalg.norm(normal)
    streaming = np.diag(0.18 + 0.12 * np.abs(ops.nodes @ normal))
    high = streaming + high_collision
    rhs = normalized_beam(ops.nodes, ops.weights, np.asarray([0.2, 0.4, 0.894]), 45.0)
    truth = np.linalg.solve(high, rhs)
    output: dict[str, Any] = {}
    for name in (
        "none",
        "moment_monotone_baseline",
        "optimized_harmonic_fidelity",
        "h2_poor_positive",
    ):
        low = None if name == "none" else streaming + 0.04 * np.eye(len(ops.weights)) - 0.32 * ops.matrices[name]
        result = preconditioned_gmres(high, rhs, low_order=low, rtol=1e-11, atol=1e-13, restart=20, max_iterations=1000)
        output[name] = {
            "iterations": result.iterations,
            "matvecs": result.matvecs,
            "low_order_solves": result.low_solves,
            "setup_seconds": result.setup_seconds,
            "solve_seconds": result.solve_seconds,
            "memory_bytes": result.preconditioner_bytes,
            "converged": result.converged,
            "fixed_point_error": float(np.linalg.norm(result.solution - truth)),
            "production_operator_unchanged": True,
        }
    return output


def run_case(case_id: str, ops: FrozenOperators, partition: str) -> dict[str, Any]:
    functions = {
        "P2E-01": individual_modes_case,
        "P2E-02": random_bandlimited_case,
        "P2E-03": narrow_beam_case,
        "P2E-04": electron_deposition_case,
        "P2E-05": neutron_bfp_case,
        "P2E-06": proton_layered_case,
        "P2E-07": hts_oblique_case,
    }
    return functions[case_id](ops, partition)


def _finalize_case(
    ops: FrozenOperators,
    case_id: str,
    category: str,
    partition: str,
    methods: dict[str, Any],
    reference: Any,
    reference_record: dict[str, Any],
) -> dict[str, Any]:
    baseline = methods["moment_monotone_baseline"]
    optimized = methods["optimized_harmonic_fidelity"]
    equal = equal_cost_record(
        float(baseline["aggregate_error"]),
        float(optimized["aggregate_error"]),
        float(baseline["runtime_seconds"]),
        float(optimized["runtime_seconds"]),
        len(ops.nodes),
    )
    return {
        "id": case_id,
        "category": category,
        "partition": partition,
        "direction_count": int(len(ops.nodes)),
        "same_nodes": True,
        "same_spatial_energy_discretization": True,
        "reference": reference_record,
        "reference_response": dataclass_dict(reference),
        "methods": methods,
        "equal_cost_equal_error": equal,
        "optimized_to_baseline_response_error_ratio": float(
            optimized["response_error"] / max(float(baseline["response_error"]), 1e-30)
        ),
        "optimized_to_baseline_aggregate_error_ratio": float(
            optimized["aggregate_error"] / max(float(baseline["aggregate_error"]), 1e-30)
        ),
    }
