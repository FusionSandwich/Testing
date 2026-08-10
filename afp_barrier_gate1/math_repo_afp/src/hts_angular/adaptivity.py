"""Goal-oriented angular indicators, ray-effect bootstraps, and adaptation."""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.linalg import expm

from .graph_generator import GraphGenerator
from .quadrature import PositiveQuadrature, finite_pool_positive_quadrature, normalize_nodes, real_spherical_harmonics

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class IndicatorResult:
    per_response: FloatArray
    combined: FloatArray
    normalization: FloatArray


def dual_weighted_indicator(
    patch_residuals: ArrayLike,
    adjoint_weights: ArrayLike,
    responses: ArrayLike,
    epsilon_response: float = 1e-12,
) -> IndicatorResult:
    """Compute patchwise multiresponse dual-weighted residual indicators.

    Inputs have shape ``(M,P)`` or are broadcast to it.
    """
    R = np.asarray(patch_residuals, dtype=float)
    Z = np.asarray(adjoint_weights, dtype=float)
    if not np.isfinite(epsilon_response) or epsilon_response <= 0.0:
        raise ValueError("epsilon_response must be finite and positive")
    if R.ndim == 1:
        R = R[None, :]
    if Z.ndim == 1:
        Z = Z[None, :]
    if R.shape != Z.shape or np.any(~np.isfinite(R)) or np.any(~np.isfinite(Z)):
        raise ValueError("finite residual and adjoint arrays must align")
    J = np.asarray(responses, dtype=float).reshape(-1)
    if J.shape != (R.shape[0],):
        raise ValueError("one response value is required per row")
    raw = np.abs(R * Z)
    normalizers = np.abs(J) + epsilon_response
    per = raw / normalizers[:, None]
    return IndicatorResult(per, np.max(per, axis=0), normalizers)


def contributon_smoothness_indicator(
    forward: ArrayLike,
    adjoints: ArrayLike,
    graph: GraphGenerator,
    epsilon_response: float = 1e-12,
) -> IndicatorResult:
    f = np.asarray(forward, dtype=float).reshape(-1)
    z = np.asarray(adjoints, dtype=float)
    if not np.isfinite(epsilon_response) or epsilon_response <= 0.0:
        raise ValueError("epsilon_response must be finite and positive")
    if z.ndim == 1:
        z = z[None, :]
    if (
        f.shape != graph.weights.shape
        or z.ndim != 2
        or z.shape[1] != f.size
        or np.any(~np.isfinite(f))
        or np.any(~np.isfinite(z))
    ):
        raise ValueError("forward and adjoint data must be finite and align with graph nodes")
    contributon = z * f[None, :]
    curvature = np.abs(contributon @ graph.generator.T)
    scales = np.sum(np.abs(contributon) * graph.weights[None, :], axis=1) + epsilon_response
    per = curvature / scales[:, None]
    return IndicatorResult(per, np.max(per, axis=0), scales)


def filtered_harmonic_bootstrap(
    nodes: ArrayLike,
    weights: ArrayLike,
    values: ArrayLike,
    maximum_degree: int,
    filter_strength: float = 0.05,
    filter_order: int = 4,
) -> FloatArray:
    points = normalize_nodes(nodes)
    w = np.asarray(weights, dtype=float).reshape(-1)
    f = np.asarray(values, dtype=float).reshape(-1)
    if (
        w.shape != (points.shape[0],)
        or f.shape != w.shape
        or np.any(~np.isfinite(w))
        or np.any(~np.isfinite(f))
        or np.any(w <= 0.0)
    ):
        raise ValueError("finite values and positive weights must align with nodes")
    if (
        maximum_degree < 0
        or not np.isfinite(filter_strength)
        or filter_strength < 0.0
        or filter_order <= 0
    ):
        raise ValueError("invalid harmonic filter parameters")
    Y, labels = real_spherical_harmonics(points, maximum_degree)
    weighted = Y * np.sqrt(w)[None, :]
    coefficients, *_ = np.linalg.lstsq(weighted.T, np.sqrt(w) * f, rcond=None)
    damping = np.array([np.exp(-filter_strength * (ell * (ell + 1)) ** (filter_order / 2.0)) for ell, _m in labels])
    return Y.T @ (damping * coefficients)


def graph_heat_bootstrap(values: ArrayLike, graph: GraphGenerator, pseudo_time: float = 0.02) -> FloatArray:
    f = np.asarray(values, dtype=float).reshape(-1)
    if f.shape != graph.weights.shape or np.any(~np.isfinite(f)):
        raise ValueError("finite values must align with graph nodes")
    if not np.isfinite(pseudo_time) or pseudo_time < 0.0:
        raise ValueError("pseudo_time must be finite and nonnegative")
    return expm(pseudo_time * graph.generator) @ f


class HysteresisMarker:
    """Refine/coarsen marker with persistent counters to suppress cycling."""

    def __init__(self, refine_threshold: float, coarsen_threshold: float, persistence: int = 2):
        if not 0 <= coarsen_threshold < refine_threshold or persistence < 1:
            raise ValueError("require 0 <= coarsen < refine and positive persistence")
        self.refine_threshold = float(refine_threshold)
        self.coarsen_threshold = float(coarsen_threshold)
        self.persistence = int(persistence)
        self._high: NDArray[np.int64] | None = None
        self._low: NDArray[np.int64] | None = None

    def update(self, indicators: ArrayLike) -> tuple[NDArray[np.bool_], NDArray[np.bool_]]:
        eta = np.asarray(indicators, dtype=float).reshape(-1)
        if np.any(~np.isfinite(eta)) or np.any(eta < 0.0):
            raise ValueError("indicators must be finite and nonnegative")
        if self._high is None or self._high.shape != eta.shape:
            self._high = np.zeros(eta.size, dtype=int)
            self._low = np.zeros(eta.size, dtype=int)
        self._high = np.where(eta >= self.refine_threshold, self._high + 1, 0)
        self._low = np.where(eta <= self.coarsen_threshold, self._low + 1, 0)
        return self._high >= self.persistence, self._low >= self.persistence


def local_tangent_children(node: ArrayLike, angular_radius: float = 0.08, count: int = 4) -> FloatArray:
    if not np.isfinite(angular_radius) or not 0.0 < angular_radius < np.pi:
        raise ValueError("angular_radius must lie strictly between zero and pi")
    if int(count) != count or count < 1:
        raise ValueError("count must be a positive integer")
    count = int(count)
    p = normalize_nodes(np.asarray(node, dtype=float).reshape(1, 3))[0]
    seed = np.array([1.0, 0.0, 0.0]) if abs(p[0]) < 0.8 else np.array([0.0, 1.0, 0.0])
    e1 = seed - (seed @ p) * p
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(p, e1)
    angles = 2.0 * np.pi * np.arange(count) / count
    children = [np.cos(angular_radius) * p + np.sin(angular_radius) * (np.cos(a) * e1 + np.sin(a) * e2) for a in angles]
    return normalize_nodes(np.asarray(children))


@dataclass(frozen=True)
class AdaptationResult:
    quadrature: PositiveQuadrature
    refined_indices: NDArray[np.int64]
    coarsened_indices: NDArray[np.int64]
    rolled_back_coarsening: bool
    exact_moment_residual: float


def adapt_positive_quadrature(
    quadrature: PositiveQuadrature,
    indicators: ArrayLike,
    feature_function,
    target_moments: ArrayLike,
    refine_fraction: float = 0.2,
    coarsen_fraction: float = 0.1,
    angular_radius: float = 0.08,
) -> AdaptationResult:
    eta = np.asarray(indicators, dtype=float).reshape(-1)
    if (
        eta.shape != (quadrature.n_node,)
        or np.any(~np.isfinite(eta))
        or np.any(eta < 0.0)
    ):
        raise ValueError("one finite nonnegative indicator per node is required")
    if (
        not np.isfinite(refine_fraction)
        or not np.isfinite(coarsen_fraction)
        or not 0.0 <= refine_fraction <= 1.0
        or not 0.0 <= coarsen_fraction <= 1.0
    ):
        raise ValueError("refine and coarsen fractions must lie in [0,1]")
    n_refine = (
        max(1, int(np.ceil(refine_fraction * quadrature.n_node)))
        if refine_fraction > 0
        else 0
    )
    order = np.argsort(eta, kind="stable")
    refine = order[-n_refine:] if n_refine else np.zeros(0, dtype=int)
    available = order[: max(quadrature.n_node - n_refine, 0)]
    n_coarsen = (
        min(int(np.floor(coarsen_fraction * quadrature.n_node)), available.size)
        if coarsen_fraction > 0
        else 0
    )
    coarsen = available[:n_coarsen] if n_coarsen else np.zeros(0, dtype=int)
    keep = np.ones(quadrature.n_node, dtype=bool)
    keep[coarsen] = False
    children = (
        np.vstack(
            [local_tangent_children(quadrature.nodes[i], angular_radius) for i in refine]
        )
        if refine.size
        else np.empty((0, 3))
    )
    candidate = np.vstack([quadrature.nodes[keep], children])
    # Remove exact/roundoff duplicates so the moment LP is not needlessly rank
    # deficient.  Stable first-occurrence retention keeps runs deterministic.
    rounded = np.round(candidate, decimals=14)
    _unique, unique_indices = np.unique(rounded, axis=0, return_index=True)
    candidate = candidate[np.sort(unique_indices)]
    F = np.asarray(feature_function(candidate), dtype=float)
    fit = finite_pool_positive_quadrature(candidate, F, target_moments)
    rolled_back = False
    if not fit.exact or fit.quadrature is None:
        rolled_back = True
        candidate = np.vstack([quadrature.nodes, children])
        F = np.asarray(feature_function(candidate), dtype=float)
        fit = finite_pool_positive_quadrature(candidate, F, target_moments)
    if not fit.exact or fit.quadrature is None:
        return AdaptationResult(quadrature, refine.astype(int), coarsen.astype(int), True, math.inf)
    return AdaptationResult(fit.quadrature, refine.astype(int), coarsen.astype(int), rolled_back, float(np.linalg.norm(fit.residual)))
