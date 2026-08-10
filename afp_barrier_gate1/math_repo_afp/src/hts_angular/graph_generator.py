"""Positive weighted graph generators approximating the sphere Laplacian."""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.linalg import expm, eigvalsh
from scipy.optimize import lsq_linear
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, minimum_spanning_tree
from scipy.spatial.distance import cdist

from .quadrature import farkas_infeasibility_certificate, normalize_nodes, real_spherical_harmonics

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class GraphConnectivityDiagnostics:
    component_count: int
    connected: bool
    algebraic_connectivity: float
    minimum_positive_conductance: float


@dataclass(frozen=True)
class GraphGenerator:
    nodes: FloatArray
    weights: FloatArray
    conductances: FloatArray
    generator: FloatArray
    edges: NDArray[np.int64]
    fit_residual_norm: float
    metadata: dict[str, object]

    def __post_init__(self) -> None:
        points = normalize_nodes(self.nodes)
        weights = np.asarray(self.weights, dtype=float).reshape(-1)
        conductances = np.asarray(self.conductances, dtype=float)
        generator = np.asarray(self.generator, dtype=float)
        edges = np.asarray(self.edges, dtype=int)
        n = points.shape[0]
        if weights.shape != (n,) or np.any(~np.isfinite(weights)) or np.any(weights <= 0.0):
            raise ValueError("graph weights must be finite, positive, and align with nodes")
        if conductances.shape != (n, n) or generator.shape != (n, n):
            raise ValueError("graph matrices must be square and align with nodes")
        if (
            np.any(~np.isfinite(conductances))
            or np.any(~np.isfinite(generator))
            or np.any(conductances < -1e-14)
            or not np.allclose(conductances, conductances.T, rtol=1e-12, atol=1e-14)
            or np.max(np.abs(np.diag(conductances)), initial=0.0) > 1e-13
        ):
            raise ValueError("conductances must be finite, nonnegative, symmetric, and zero-diagonal")
        if edges.size == 0:
            edges = np.empty((0, 2), dtype=int)
        if edges.ndim != 2 or edges.shape[1] != 2:
            raise ValueError("edges must have shape (E,2)")
        if np.any(edges < 0) or np.any(edges >= n) or np.any(edges[:, 0] == edges[:, 1]):
            raise ValueError("edges contain invalid node indices")
        expected = conductances / weights[:, None]
        np.fill_diagonal(expected, -np.sum(conductances, axis=1) / weights)
        if not np.allclose(generator, expected, rtol=2e-11, atol=2e-13):
            raise ValueError("generator is inconsistent with conductances and weights")
        fit = float(self.fit_residual_norm)
        if not np.isfinite(fit) or fit < 0.0:
            raise ValueError("fit_residual_norm must be finite and nonnegative")
        object.__setattr__(self, "nodes", points)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "conductances", np.maximum(conductances, 0.0))
        object.__setattr__(self, "generator", generator)
        object.__setattr__(self, "edges", edges)
        object.__setattr__(self, "fit_residual_norm", fit)
        object.__setattr__(self, "metadata", dict(self.metadata))

    def structural_residuals(self) -> dict[str, float]:
        W = np.diag(self.weights)
        symmetric = W @ self.generator
        weighted_similarity = np.diag(np.sqrt(self.weights)) @ self.generator @ np.diag(1.0 / np.sqrt(self.weights))
        eigenvalues = eigvalsh(0.5 * (weighted_similarity + weighted_similarity.T))
        return {
            "constant": float(np.linalg.norm(self.generator @ np.ones(self.weights.size), ord=np.inf)),
            "weighted_self_adjoint": float(np.linalg.norm(symmetric - symmetric.T, ord=np.inf)),
            "largest_eigenvalue": float(np.max(eigenvalues, initial=-math.inf)),
            "minimum_offdiagonal": float(np.min(self.generator + np.diag(np.full(self.weights.size, np.inf)))),
        }

    def connectivity_diagnostics(self, tolerance: float = 1e-14) -> GraphConnectivityDiagnostics:
        if tolerance < 0.0 or not np.isfinite(tolerance):
            raise ValueError("tolerance must be finite and nonnegative")
        adjacency = self.conductances > tolerance
        count, _labels = connected_components(csr_matrix(adjacency), directed=False)
        similarity = (
            np.diag(np.sqrt(self.weights))
            @ (-self.generator)
            @ np.diag(1.0 / np.sqrt(self.weights))
        )
        eigenvalues = eigvalsh(0.5 * (similarity + similarity.T))
        algebraic = float(max(eigenvalues[1], 0.0)) if eigenvalues.size > 1 else 0.0
        positive = self.conductances[self.conductances > tolerance]
        minimum = float(np.min(positive)) if positive.size else 0.0
        return GraphConnectivityDiagnostics(
            component_count=int(count),
            connected=bool(count == 1),
            algebraic_connectivity=algebraic,
            minimum_positive_conductance=minimum,
        )

    def semigroup(self, time: float) -> FloatArray:
        if not np.isfinite(time) or time < 0.0:
            raise ValueError("time must be finite and nonnegative")
        return expm(time * self.generator)

    def spectral_diagnostics(self, maximum_degree: int) -> list[dict[str, float]]:
        Y, labels = real_spherical_harmonics(self.nodes, maximum_degree)
        rows = []
        for values, (ell, m) in zip(Y, labels, strict=True):
            target = -ell * (ell + 1) * values
            residual = self.generator @ values - target
            denominator = max(np.sqrt(np.sum(self.weights * target * target)), 1e-15)
            rows.append({
                "ell": float(ell), "m": float(m),
                "weighted_relative_residual": float(np.sqrt(np.sum(self.weights * residual * residual)) / denominator),
                "max_absolute_residual": float(np.max(np.abs(residual))),
            })
        return rows


def _edge_set(nodes: FloatArray, k_nearest: int) -> NDArray[np.int64]:
    n = nodes.shape[0]
    if n < 2:
        return np.empty((0, 2), dtype=int)
    distances = cdist(nodes, nodes)
    np.fill_diagonal(distances, np.inf)
    pairs: set[tuple[int, int]] = set()
    k = min(max(k_nearest, 1), n - 1)
    for i in range(n):
        for j in np.argpartition(distances[i], k)[:k]:
            pairs.add(tuple(sorted((i, int(j)))))
    # Add a Euclidean MST to guarantee connectivity even if kNN tie handling is poor.
    full = cdist(nodes, nodes)
    tree = minimum_spanning_tree(full).tocoo()
    for i, j in zip(tree.row, tree.col, strict=True):
        pairs.add(tuple(sorted((int(i), int(j)))))
    return np.asarray(sorted(pairs), dtype=int)


def fit_graph_generator(
    nodes: ArrayLike,
    weights: ArrayLike,
    maximum_degree: int = 2,
    k_nearest: int = 8,
    regularization: float = 1e-8,
    conductance_floor: float = 1e-12,
) -> GraphGenerator:
    points = normalize_nodes(nodes)
    w = np.asarray(weights, dtype=float).reshape(-1)
    if points.shape[0] < 2:
        raise ValueError("at least two nodes are required for a connected angular graph")
    if (
        w.shape != (points.shape[0],)
        or np.any(~np.isfinite(w))
        or np.any(w <= 0.0)
    ):
        raise ValueError("weights must be finite, positive, and match nodes")
    if maximum_degree < 1 or k_nearest < 1:
        raise ValueError("maximum_degree and k_nearest must be positive")
    if not np.isfinite(regularization) or regularization < 0.0:
        raise ValueError("regularization must be finite and nonnegative")
    if not np.isfinite(conductance_floor) or conductance_floor <= 0.0:
        raise ValueError("conductance_floor must be finite and strictly positive")
    edges = _edge_set(points, k_nearest)
    Y, labels = real_spherical_harmonics(points, maximum_degree)
    nonconstant = [k for k, (ell, _m) in enumerate(labels) if ell > 0]
    n_equation = points.shape[0] * len(nonconstant)
    A = np.zeros((n_equation, edges.shape[0]))
    b = np.zeros(n_equation)
    edge_lookup: dict[tuple[int, int], int] = {tuple(edge): k for k, edge in enumerate(edges)}
    row = 0
    for harmonic_index in nonconstant:
        values = Y[harmonic_index]
        ell, _m = labels[harmonic_index]
        lam = ell * (ell + 1)
        for i in range(points.shape[0]):
            for j in range(points.shape[0]):
                if i == j:
                    continue
                key = tuple(sorted((i, j)))
                e = edge_lookup.get(key)
                if e is not None:
                    A[row, e] += values[j] - values[i]
            b[row] = -w[i] * lam * values[i]
            row += 1
    if regularization > 0.0:
        scale = np.sqrt(regularization)
        Afit = np.vstack([A, scale * np.eye(edges.shape[0])])
        bfit = np.concatenate([b, np.zeros(edges.shape[0])])
    else:
        Afit, bfit = A, b
    result = lsq_linear(Afit, bfit, bounds=(conductance_floor, np.inf), tol=1e-12, lsmr_tol=1e-12, max_iter=20000)
    c = np.maximum(result.x, conductance_floor)
    C = np.zeros((points.shape[0], points.shape[0]))
    for value, (i, j) in zip(c, edges, strict=True):
        C[i, j] = C[j, i] = value
    G = C / w[:, None]
    np.fill_diagonal(G, -np.sum(C, axis=1) / w)
    residual = A @ c - b
    return GraphGenerator(
        points, w, C, G, edges,
        float(np.linalg.norm(residual)),
        {"construction": "nonnegative conductance least squares", "degree": maximum_degree, "k_nearest": k_nearest, "regularization": regularization, "optimizer_status": result.status},
    )


def conductance_exactness_certificate(
    nodes: ArrayLike,
    weights: ArrayLike,
    maximum_degree: int,
    edges: ArrayLike,
):
    """Return a Farkas certificate if exact nonnegative conductances are impossible."""
    points = normalize_nodes(nodes)
    w = np.asarray(weights, dtype=float).reshape(-1)
    e = np.asarray(edges, dtype=int)
    Y, labels = real_spherical_harmonics(points, maximum_degree)
    rows, targets = [], []
    for values, (ell, _m) in zip(Y, labels, strict=True):
        if ell == 0:
            continue
        for i in range(points.shape[0]):
            row = np.zeros(e.shape[0])
            for k, (a, b) in enumerate(e):
                if a == i:
                    row[k] = values[b] - values[a]
                elif b == i:
                    row[k] = values[a] - values[b]
            rows.append(row)
            targets.append(-w[i] * ell * (ell + 1) * values[i])
    return farkas_infeasibility_certificate(np.asarray(rows), np.asarray(targets))
