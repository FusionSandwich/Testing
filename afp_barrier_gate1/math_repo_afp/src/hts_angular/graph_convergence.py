"""Executable hypotheses and conditional convergence audits for angular graphs.

The routines in this module do not claim an unconditional convergence theorem
for arbitrary point clouds.  They verify a finite refinement family against
explicit geometric, measure, structural, and harmonic-consistency hypotheses,
and issue an empirical envelope only when every gate passes.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .graph_generator import GraphGenerator
from .quadrature import fibonacci_sphere, normalize_nodes

FloatArray = NDArray[np.float64]
_SPHERE_AREA = 4.0 * np.pi


@dataclass(frozen=True)
class SphericalGridQuality:
    node_count: int
    separation_radius: float
    approximate_fill_distance: float
    mesh_ratio: float
    minimum_weight: float
    maximum_weight: float
    weight_ratio: float
    total_weight: float
    relative_total_weight_error: float
    relative_weight_scaling_error: float
    sample_count: int


@dataclass(frozen=True)
class HarmonicConsistencyRecord:
    node_count: int
    fill_distance: float
    mesh_ratio: float
    weight_ratio: float
    total_weight: float
    relative_total_weight_error: float
    relative_weight_scaling_error: float
    connected: bool
    algebraic_connectivity: float
    structural_residual: float
    maximum_weighted_relative_residual: float
    mean_weighted_relative_residual: float


@dataclass(frozen=True)
class GraphConvergenceCertificate:
    passed: bool
    records: tuple[HarmonicConsistencyRecord, ...]
    fitted_order: float
    fitted_prefactor: float
    minimum_adjacent_order: float
    maximum_envelope_ratio: float
    fill_distance_interval: tuple[float, float]
    reasons: tuple[str, ...]
    maximum_degree: int
    conditional_statement: str

    def error_bound(self, fill_distance: float) -> float:
        """Return the certified finite-family power-law envelope.

        The prefactor is chosen as the maximum observed ``error / h**order``
        rather than the least-squares intercept.  Consequently every audited
        record lies below the returned envelope up to roundoff.
        """
        if not self.passed:
            raise ValueError("no conditional bound is available because convergence gates failed")
        h = float(fill_distance)
        if not np.isfinite(h) or h <= 0.0:
            raise ValueError("fill_distance must be finite and positive")
        finest, coarsest = self.fill_distance_interval
        tolerance = 64.0 * np.finfo(float).eps * max(1.0, abs(finest), abs(coarsest))
        if h < finest - tolerance or h > coarsest + tolerance:
            raise ValueError("fill_distance lies outside the audited finite-family interval")
        return self.fitted_prefactor * h ** self.fitted_order


def spherical_grid_quality(
    nodes: ArrayLike,
    weights: ArrayLike,
    *,
    sample_count: int = 8192,
) -> SphericalGridQuality:
    points = normalize_nodes(nodes)
    w = np.asarray(weights, dtype=float).reshape(-1)
    if w.shape != (points.shape[0],) or np.any(~np.isfinite(w)) or np.any(w <= 0.0):
        raise ValueError("weights must be finite, positive, and align with nodes")
    if int(sample_count) != sample_count or sample_count < 64:
        raise ValueError("sample_count must be an integer at least 64")
    sample_count = int(sample_count)
    if points.shape[0] < 2:
        separation = math.inf
    else:
        dots = np.clip(points @ points.T, -1.0, 1.0)
        np.fill_diagonal(dots, -1.0)
        nearest_angle = np.arccos(np.max(dots, axis=1))
        separation = 0.5 * float(np.min(nearest_angle))
    samples = fibonacci_sphere(sample_count, phase=0.37).nodes
    # Chunking avoids a large temporary matrix for future high-node studies.
    maximum_nearest = 0.0
    for start in range(0, sample_count, 1024):
        block = samples[start : start + 1024]
        nearest_dot = np.max(np.clip(block @ points.T, -1.0, 1.0), axis=1)
        maximum_nearest = max(maximum_nearest, float(np.max(np.arccos(nearest_dot), initial=0.0)))
    fill = maximum_nearest
    ratio = fill / separation if np.isfinite(separation) and separation > 0.0 else math.inf
    expected = _SPHERE_AREA / points.shape[0]
    total = float(np.sum(w))
    total_error = abs(total - _SPHERE_AREA) / _SPHERE_AREA
    # This is a diagnostic for the common quasi-uniform scaling assumption
    # w_i = Theta(h^2); it is not used as an exactness requirement by itself.
    scaling = float(np.max(np.abs(w - expected)) / expected)
    return SphericalGridQuality(
        node_count=points.shape[0],
        separation_radius=separation,
        approximate_fill_distance=fill,
        mesh_ratio=ratio,
        minimum_weight=float(np.min(w)),
        maximum_weight=float(np.max(w)),
        weight_ratio=float(np.max(w) / np.min(w)),
        total_weight=total,
        relative_total_weight_error=float(total_error),
        relative_weight_scaling_error=scaling,
        sample_count=sample_count,
    )


def graph_family_records(
    graphs: Sequence[GraphGenerator],
    *,
    maximum_degree: int = 2,
    sample_count: int = 8192,
) -> tuple[HarmonicConsistencyRecord, ...]:
    records: list[HarmonicConsistencyRecord] = []
    for graph in graphs:
        quality = spherical_grid_quality(graph.nodes, graph.weights, sample_count=sample_count)
        connectivity = graph.connectivity_diagnostics()
        structural = graph.structural_residuals()
        structural_residual = max(
            abs(structural["constant"]),
            abs(structural["weighted_self_adjoint"]),
            max(structural["largest_eigenvalue"], 0.0),
            max(-structural["minimum_offdiagonal"], 0.0),
        )
        spectral = [row for row in graph.spectral_diagnostics(maximum_degree) if row["ell"] > 0]
        errors = np.array([row["weighted_relative_residual"] for row in spectral], dtype=float)
        records.append(
            HarmonicConsistencyRecord(
                node_count=quality.node_count,
                fill_distance=quality.approximate_fill_distance,
                mesh_ratio=quality.mesh_ratio,
                weight_ratio=quality.weight_ratio,
                total_weight=quality.total_weight,
                relative_total_weight_error=quality.relative_total_weight_error,
                relative_weight_scaling_error=quality.relative_weight_scaling_error,
                connected=connectivity.connected,
                algebraic_connectivity=connectivity.algebraic_connectivity,
                structural_residual=float(structural_residual),
                maximum_weighted_relative_residual=float(np.max(errors, initial=0.0)),
                mean_weighted_relative_residual=float(np.mean(errors)) if errors.size else 0.0,
            )
        )
    return tuple(records)


def certify_graph_family(
    graphs: Sequence[GraphGenerator],
    *,
    maximum_degree: int = 2,
    sample_count: int = 8192,
    maximum_mesh_ratio: float = 4.0,
    maximum_weight_ratio: float = 6.0,
    maximum_relative_total_weight_error: float = 1e-10,
    maximum_relative_weight_scaling_error: float | None = None,
    structural_tolerance: float = 1e-10,
    minimum_fitted_order: float = 0.1,
    minimum_adjacent_order: float = 0.0,
) -> GraphConvergenceCertificate:
    """Issue a conditional empirical convergence statement only if all gates pass.

    The result is deliberately finite-family and empirical.  It verifies exact
    graph structure, connectivity, quasi-uniform geometry, sphere-measure
    normalization, optional individual-weight scaling, decreasing fill
    distance, and improving low-order spherical-harmonic consistency.
    """
    if len(graphs) < 3:
        raise ValueError("at least three graph resolutions are required")
    for name, value in (
        ("maximum_mesh_ratio", maximum_mesh_ratio),
        ("maximum_weight_ratio", maximum_weight_ratio),
        ("maximum_relative_total_weight_error", maximum_relative_total_weight_error),
        ("structural_tolerance", structural_tolerance),
        ("minimum_fitted_order", minimum_fitted_order),
        ("minimum_adjacent_order", minimum_adjacent_order),
    ):
        if not np.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and nonnegative")
    if maximum_relative_weight_scaling_error is not None and (
        not np.isfinite(maximum_relative_weight_scaling_error)
        or maximum_relative_weight_scaling_error < 0.0
    ):
        raise ValueError("maximum_relative_weight_scaling_error must be finite and nonnegative")

    records = graph_family_records(graphs, maximum_degree=maximum_degree, sample_count=sample_count)
    # Sort from coarsest to finest by fill distance to make the fit independent
    # of caller ordering while retaining a deterministic record order.
    records = tuple(sorted(records, key=lambda record: record.fill_distance, reverse=True))
    reasons: list[str] = []
    if not all(record.connected for record in records):
        reasons.append("one or more conductance graphs are disconnected")
    if any(record.structural_residual > structural_tolerance for record in records):
        reasons.append("a graph violates an exact Markov/self-adjoint structural gate")
    if any(record.mesh_ratio > maximum_mesh_ratio for record in records):
        reasons.append("the node sequence is not sufficiently quasi-uniform")
    if any(record.weight_ratio > maximum_weight_ratio for record in records):
        reasons.append("quadrature weights violate the declared ratio gate")
    if any(record.relative_total_weight_error > maximum_relative_total_weight_error for record in records):
        reasons.append("quadrature weights do not integrate the sphere's constant mode")
    if maximum_relative_weight_scaling_error is not None and any(
        record.relative_weight_scaling_error > maximum_relative_weight_scaling_error
        for record in records
    ):
        reasons.append("individual quadrature weights violate the declared h-scaling gate")

    fills = np.array([record.fill_distance for record in records])
    errors = np.array([record.maximum_weighted_relative_residual for record in records])
    if not np.all(np.diff(fills) < 0.0):
        reasons.append("approximate fill distance does not strictly decrease")
    fill_interval = (float(fills[-1]), float(fills[0]))
    if np.any(~np.isfinite(errors)) or np.any(errors <= 0.0):
        reasons.append("harmonic residuals are nonfinite or unresolved at machine zero")
        order = math.nan
        prefactor = math.nan
        minimum_local_order = math.nan
        envelope_ratio = math.nan
    else:
        order = float(np.polyfit(np.log(fills), np.log(errors), 1)[0])
        local_orders = np.log(errors[:-1] / errors[1:]) / np.log(fills[:-1] / fills[1:])
        minimum_local_order = float(np.min(local_orders))
        if not np.all(np.diff(errors) < 0.0):
            reasons.append("low-order harmonic residual does not improve at every refinement")
        if minimum_local_order < minimum_adjacent_order:
            reasons.append(
                f"minimum adjacent consistency order {minimum_local_order:.3f} "
                f"is below {minimum_adjacent_order:.3f}"
            )
        if order < minimum_fitted_order:
            reasons.append(f"fitted consistency order {order:.3f} is below {minimum_fitted_order:.3f}")
        # Use a true observed envelope, not the least-squares intercept.
        prefactor = float(np.max(errors / fills**order))
        envelope = prefactor * fills**order
        envelope_ratio = float(np.max(errors / envelope))
        if np.any(errors > envelope * (1.0 + 32.0 * np.finfo(float).eps)):
            reasons.append("the computed power-law envelope does not bound every audited record")
    passed = not reasons
    statement = (
        f"For this audited finite graph family, low-order harmonic consistency is bounded by "
        f"{prefactor:.6e} h^{order:.6f} for h in "
        f"[{fill_interval[0]:.6e}, {fill_interval[1]:.6e}], with minimum adjacent order "
        f"{minimum_local_order:.6f}. This is an executable finite-family certificate, "
        "not an unconditional point-cloud theorem or an extrapolation outside the audited interval."
        if passed
        else "No convergence statement issued; see failed executable hypotheses."
    )
    return GraphConvergenceCertificate(
        passed=passed,
        records=records,
        fitted_order=order,
        fitted_prefactor=prefactor,
        minimum_adjacent_order=minimum_local_order,
        maximum_envelope_ratio=envelope_ratio,
        fill_distance_interval=fill_interval,
        reasons=tuple(reasons),
        maximum_degree=int(maximum_degree),
        conditional_statement=statement,
    )


__all__ = [
    "GraphConvergenceCertificate",
    "HarmonicConsistencyRecord",
    "SphericalGridQuality",
    "certify_graph_family",
    "graph_family_records",
    "spherical_grid_quality",
]
