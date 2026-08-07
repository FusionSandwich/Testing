"""Deterministic one-dimensional BFP transport kernels for P2E.

These routines isolate spatial/energy machinery from the angular-generator
comparison.  They are deliberately small enough for exact-head CI, but they
retain a conservative upwind streaming ledger, explicit angular diffusion,
energy-group transfer, source normalization, iterative-work counters, and an
independent direct-solve reference route.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import LinearOperator, gmres, spilu, spsolve

FloatArray = np.ndarray


@dataclass(frozen=True)
class SlabSolve:
    state: FloatArray
    iterations: int
    matvecs: int
    converged: bool
    residual: float


@dataclass(frozen=True)
class TransportProfile:
    state: FloatArray
    scalar: FloatArray
    current: FloatArray
    tensor: FloatArray
    response: FloatArray
    response_labels: tuple[str, ...]
    particle_balance_error: float
    iterations: int
    matvecs: int
    converged: bool
    minimum_state: float
    extra: dict[str, Any]


def assemble_steady_slab(
    mu: FloatArray,
    generator: FloatArray,
    cell_widths: FloatArray,
    absorption: FloatArray,
    angular_diffusion: FloatArray,
    source: FloatArray,
    *,
    left_inflow: FloatArray | None = None,
    right_inflow: FloatArray | None = None,
) -> tuple[sparse.csr_matrix, FloatArray]:
    direction = np.asarray(mu, dtype=float)
    lmat = np.asarray(generator, dtype=float)
    dx = np.asarray(cell_widths, dtype=float)
    sigma = np.asarray(absorption, dtype=float)
    diffusion = np.asarray(angular_diffusion, dtype=float)
    q = np.asarray(source, dtype=float)
    cells, directions = q.shape
    if direction.shape != (directions,) or lmat.shape != (directions, directions):
        raise ValueError("angular shapes are inconsistent")
    if dx.shape != (cells,) or sigma.shape != (cells,) or diffusion.shape != (cells,):
        raise ValueError("cell coefficient shapes are inconsistent")
    if np.min(dx) <= 0.0 or np.min(sigma) < 0.0 or np.min(diffusion) < 0.0:
        raise ValueError("cell widths must be positive and coefficients nonnegative")
    left = np.zeros(directions) if left_inflow is None else np.asarray(left_inflow, dtype=float)
    right = np.zeros(directions) if right_inflow is None else np.asarray(right_inflow, dtype=float)
    if left.shape != (directions,) or right.shape != (directions,):
        raise ValueError("boundary inflow has wrong shape")

    matrix = sparse.lil_matrix((cells * directions, cells * directions), dtype=float)
    rhs = q.reshape(-1).copy()
    for cell in range(cells):
        base = cell * directions
        block = sigma[cell] * np.eye(directions) - diffusion[cell] * lmat
        matrix[base : base + directions, base : base + directions] += block
        for angle, cosine in enumerate(direction):
            row = base + angle
            if cosine > 0.0:
                coefficient = cosine / dx[cell]
                matrix[row, row] += coefficient
                if cell == 0:
                    rhs[row] += coefficient * left[angle]
                else:
                    matrix[row, (cell - 1) * directions + angle] -= coefficient
            elif cosine < 0.0:
                coefficient = -cosine / dx[cell]
                matrix[row, row] += coefficient
                if cell == cells - 1:
                    rhs[row] += coefficient * right[angle]
                else:
                    matrix[row, (cell + 1) * directions + angle] -= coefficient
    return matrix.tocsr(), rhs


def solve_steady_slab(
    mu: FloatArray,
    generator: FloatArray,
    cell_widths: FloatArray,
    absorption: FloatArray,
    angular_diffusion: FloatArray,
    source: FloatArray,
    *,
    left_inflow: FloatArray | None = None,
    right_inflow: FloatArray | None = None,
    direct: bool = False,
    rtol: float = 3e-8,
    max_iterations: int = 700,
) -> SlabSolve:
    matrix, rhs = assemble_steady_slab(
        mu,
        generator,
        cell_widths,
        absorption,
        angular_diffusion,
        source,
        left_inflow=left_inflow,
        right_inflow=right_inflow,
    )
    shape = np.asarray(source).shape
    if direct:
        solution = np.asarray(spsolve(matrix, rhs), dtype=float)
        residual = float(np.linalg.norm(rhs - matrix @ solution))
        return SlabSolve(solution.reshape(shape), 1, 1, True, residual)

    matvecs = 0

    def action(value: FloatArray) -> FloatArray:
        nonlocal matvecs
        matvecs += 1
        return matrix @ value

    operator = LinearOperator(matrix.shape, matvec=action, dtype=float)
    preconditioner: LinearOperator | None = None
    try:
        ilu = spilu(matrix.tocsc(), drop_tol=2e-4, fill_factor=8.0)
        preconditioner = LinearOperator(matrix.shape, matvec=ilu.solve, dtype=float)
    except RuntimeError:
        preconditioner = None

    iterations = 0

    def callback(_: object) -> None:
        nonlocal iterations
        iterations += 1

    solution, info = gmres(
        operator,
        rhs,
        M=preconditioner,
        restart=40,
        maxiter=max_iterations,
        rtol=rtol,
        atol=1e-12,
        callback=callback,
        callback_type="pr_norm",
    )
    solution = np.asarray(solution, dtype=float)
    residual = float(np.linalg.norm(rhs - matrix @ solution))
    matvecs += 1
    tolerance = 1e-12 + 10.0 * rtol * max(float(np.linalg.norm(rhs)), 1.0)
    return SlabSolve(
        solution.reshape(shape),
        iterations,
        matvecs,
        bool(info == 0 and residual <= tolerance),
        residual,
    )


def normalized_beam(
    nodes: FloatArray,
    weights: FloatArray,
    normal: FloatArray,
    axis: FloatArray,
    concentration: float,
) -> tuple[FloatArray, float]:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    n = np.asarray(normal, dtype=float)
    n /= np.linalg.norm(n)
    direction = np.asarray(axis, dtype=float)
    direction /= np.linalg.norm(direction)
    if concentration <= 0.0:
        raise ValueError("beam concentration must be positive")
    value = np.exp(np.clip(concentration * (x @ direction - 1.0), -700.0, 0.0))
    mu = x @ n
    value[mu <= 0.0] = 0.0
    incoming = float(np.sum(w * np.maximum(mu, 0.0) * value))
    if incoming <= 0.0:
        raise ValueError("quadrature does not resolve the incident beam")
    return value / incoming, incoming


def layer_moments(
    nodes: FloatArray,
    weights: FloatArray,
    state: FloatArray,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    psi = np.asarray(state, dtype=float)
    scalar = psi @ w
    current = np.einsum("ci,i,ij->cj", psi, w, x)
    tensor = np.einsum("ci,i,ij,ik->cjk", psi, w, x, x)
    tensor -= scalar[:, None, None] * np.eye(3)[None, :, :] / 3.0
    return scalar, current, tensor


def boundary_currents(
    mu: FloatArray,
    weights: FloatArray,
    state: FloatArray,
) -> dict[str, float]:
    cosine = np.asarray(mu, dtype=float)
    w = np.asarray(weights, dtype=float)
    psi = np.asarray(state, dtype=float)
    positive = cosine > 0.0
    negative = cosine < 0.0
    return {
        "left_escape": float(np.sum(w[negative] * (-cosine[negative]) * psi[0, negative])),
        "right_escape": float(np.sum(w[positive] * cosine[positive] * psi[-1, positive])),
    }


def _electron_coefficients(energy_mev: float, specification: Mapping[str, Any]) -> tuple[float, float, float]:
    model = specification["surrogate_coefficients"]
    transfer = float(model["transfer_fraction"]) if energy_mev > float(specification["cutoff_mev"]) else 0.0
    absorption = float(model["absorption_base"]) + float(model["absorption_scale"]) / (
        energy_mev + float(model["absorption_shift"])
    ) ** float(model["absorption_exponent"])
    diffusion = float(model["diffusion_base"]) + float(model["diffusion_scale"]) / (
        np.sqrt(energy_mev) + float(model["diffusion_shift"])
    )
    return transfer, absorption, diffusion


def electron_depth_dose(
    nodes: FloatArray,
    weights: FloatArray,
    generator: FloatArray,
    specification: Mapping[str, Any],
    *,
    direct: bool,
) -> TransportProfile:
    cells = int(specification["spatial_cells"])
    groups = int(specification["energy_groups"])
    slab_cm = float(specification["slab_cm"])
    top = float(specification["top_energy_mev"])
    cutoff = float(specification["cutoff_mev"])
    source_kind = str(specification["source_kind"])
    normal = np.asarray(specification.get("normal", [1.0, 0.0, 0.0]), dtype=float)
    normal /= np.linalg.norm(normal)
    mu = np.asarray(nodes, dtype=float) @ normal
    widths = np.full(cells, slab_cm / cells)
    energies = np.geomspace(top, cutoff, groups)
    previous = np.zeros((cells, len(weights)))
    accumulated = np.zeros_like(previous)
    deposition = np.zeros(cells)
    external_source = 0.0
    absorption_total = 0.0
    escape_total = 0.0
    iterations = 0
    matvecs = 0
    minimum_state = float("inf")

    for group, energy in enumerate(energies):
        transfer, true_absorption, diffusion_value = _electron_coefficients(float(energy), specification)
        if group + 1 == groups:
            transfer = 0.0
        absorption = np.full(cells, true_absorption + transfer)
        diffusion = np.full(cells, diffusion_value)
        source = transfer * previous
        left = np.zeros(len(weights))
        if group == 0 and source_kind == "isotropic_internal":
            source = source.copy()
            lower = int(round(float(specification["source_start_cm"]) / slab_cm * cells))
            upper = int(round(float(specification["source_end_cm"]) / slab_cm * cells))
            lower = max(0, min(cells - 1, lower))
            upper = max(lower + 1, min(cells, upper))
            source[lower:upper] += 1.0
            external_source += float(np.sum(widths[lower:upper]))
        elif group == 0 and source_kind == "normal_beam":
            left, _ = normalized_beam(
                nodes,
                weights,
                normal,
                np.asarray(specification.get("axis", normal), dtype=float),
                float(specification.get("concentration", 60.0)),
            )
            external_source += 1.0
        elif group == 0:
            raise ValueError(f"unsupported electron source_kind {source_kind!r}")

        solve = solve_steady_slab(
            mu,
            generator,
            widths,
            absorption,
            diffusion,
            source,
            left_inflow=left,
            direct=direct,
            rtol=float(specification.get("rtol", 3e-8)),
            max_iterations=int(specification.get("max_iterations", 700)),
        )
        if not solve.converged:
            raise RuntimeError(f"electron group {group} failed: residual={solve.residual:.3e}")
        state = solve.state
        minimum_state = min(minimum_state, float(np.min(state)))
        scalar, _, _ = layer_moments(nodes, weights, state)
        energy_width = float(energy) if group + 1 == groups else float(energy - energies[group + 1])
        deposition += true_absorption * scalar * widths * energy_width
        accumulated += state * energy_width
        absorption_total += float(np.sum(true_absorption * scalar * widths))
        currents = boundary_currents(mu, weights, state)
        escape_total += currents["left_escape"] + currents["right_escape"]
        iterations += solve.iterations
        matvecs += solve.matvecs
        previous = state

    scalar, current, tensor = layer_moments(nodes, weights, accumulated)
    balance = abs(external_source - absorption_total - escape_total) / max(abs(external_source), 1e-14)
    labels = tuple(f"depth_cell_{index}" for index in range(cells))
    return TransportProfile(
        accumulated,
        scalar,
        current,
        tensor,
        deposition,
        labels,
        balance,
        iterations,
        matvecs,
        True,
        minimum_state,
        {
            "published_geometry": {
                "slab_cm": slab_cm,
                "spatial_cells": cells,
                "energy_groups": groups,
                "top_energy_mev": top,
                "cutoff_mev": cutoff,
                "source_kind": source_kind,
            },
            "scope": "published geometry and discretization with preregistered analytic surrogate coefficients; not a Radiant cross-section-table reproduction",
        },
    )


def layered_slab(
    nodes: FloatArray,
    weights: FloatArray,
    generator: FloatArray,
    specification: Mapping[str, Any],
    *,
    direct: bool,
    coefficient_scale: float = 1.0,
) -> TransportProfile:
    normal = np.asarray(specification.get("normal", [0.0, 0.0, 1.0]), dtype=float)
    normal /= np.linalg.norm(normal)
    axis = np.asarray(specification["axis"], dtype=float)
    axis /= np.linalg.norm(axis)
    x = np.asarray(nodes, dtype=float)
    mu = x @ normal

    widths: list[float] = []
    absorption: list[float] = []
    diffusion: list[float] = []
    stopping: list[float] = []
    labels: list[str] = []
    for layer in specification["layers"]:
        cells = int(layer.get("cells", 1))
        width = float(layer["thickness_cm"]) / cells
        for cell in range(cells):
            widths.append(width)
            absorption.append(coefficient_scale * float(layer.get("absorption", 0.0)))
            diffusion.append(coefficient_scale * float(layer["angular_diffusion"]))
            stopping.append(coefficient_scale * float(layer.get("stopping_mev_per_cm", 0.0)))
            labels.append(f"{layer['material']}:{cell}")
    widths_array = np.asarray(widths)
    absorption_array = np.asarray(absorption)
    diffusion_array = np.asarray(diffusion)
    stopping_array = np.asarray(stopping)
    source = np.zeros((len(widths), len(weights)))
    left, _ = normalized_beam(
        nodes,
        weights,
        normal,
        axis,
        float(specification.get("concentration", 60.0)),
    )
    solve = solve_steady_slab(
        mu,
        generator,
        widths_array,
        absorption_array,
        diffusion_array,
        source,
        left_inflow=left,
        direct=direct,
        rtol=float(specification.get("rtol", 2e-9)),
        max_iterations=int(specification.get("max_iterations", 800)),
    )
    if not solve.converged:
        raise RuntimeError(f"layered solve failed: residual={solve.residual:.3e}")
    scalar, current, tensor = layer_moments(nodes, weights, solve.state)
    energy = float(specification.get("energy_mev", 1.0))
    absorption_response = energy * absorption_array * scalar * widths_array
    stopping_response = stopping_array * scalar * widths_array
    deposition = absorption_response + stopping_response
    currents = boundary_currents(mu, weights, solve.state)
    particle_absorption = float(np.sum(absorption_array * scalar * widths_array))
    balance = abs(1.0 - particle_absorption - currents["left_escape"] - currents["right_escape"])
    qn = np.einsum(
        "ci,i,i->c",
        solve.state,
        np.asarray(weights, dtype=float),
        (x @ normal) ** 2 - 1.0 / 3.0,
    )
    response = np.concatenate(
        [
            deposition,
            np.asarray(
                [
                    float(np.sum(deposition)),
                    currents["left_escape"],
                    currents["right_escape"],
                    float(current[-1] @ normal),
                    float(qn[-1]),
                ]
            ),
        ]
    )
    response_labels = tuple(labels) + (
        "total_deposition",
        "left_escape",
        "right_escape",
        "exit_normal_current",
        "exit_normal_quadrupole",
    )
    return TransportProfile(
        solve.state,
        scalar,
        current,
        tensor,
        response,
        response_labels,
        balance,
        solve.iterations,
        solve.matvecs,
        solve.converged,
        float(np.min(solve.state)),
        {
            "cell_labels": labels,
            "cell_deposition": deposition.tolist(),
            "cell_scalar": scalar.tolist(),
            "cell_current": current.tolist(),
            "cell_tensor": tensor.tolist(),
            "cell_normal_quadrupole": qn.tolist(),
            "coefficient_scale": float(coefficient_scale),
        },
    )
