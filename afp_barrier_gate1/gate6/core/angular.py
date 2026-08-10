"""Reusable angular operators and time integrators for Gate 6.

The research audit scripts originally owned these implementations.  This module
is the stable numerical API used by spatial transport and future Radiant
adapters.  It preserves the exact formulas and reference values locked by the
existing characterization tests.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
GATE4 = HERE.parents[1] / "gate4" / "icosphere_spherical_laplacian_audit.py"
_spec = importlib.util.spec_from_file_location("gate4_icosphere_core", GATE4)
if _spec is None or _spec.loader is None:
    raise RuntimeError("cannot load Gate 4 icosphere implementation")
_g4 = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _g4
_spec.loader.exec_module(_g4)


@dataclass
class AngularOperator:
    """Weighted-reversible angular jump generator in shared-edge form."""

    family: str
    directions: np.ndarray
    weights: np.ndarray
    edge_i: np.ndarray
    edge_j: np.ndarray
    gamma: np.ndarray
    rate: np.ndarray
    symmetric_matrix: np.ndarray

    @property
    def count(self) -> int:
        return int(self.directions.shape[0])

    @property
    def mu_x(self) -> np.ndarray:
        """Direction cosine used by the one-dimensional slab solver."""

        return self.directions[:, 0]


def make_operator(
    family: str,
    points: Sequence[Sequence[float]],
    weights: Sequence[float],
    edges: Iterable[tuple[int, int, float]],
) -> AngularOperator:
    directions = np.asarray(points, dtype=float)
    weights_array = np.asarray(weights, dtype=float)
    edge_list = list(edges)
    if directions.ndim != 2 or directions.shape[1] != 3:
        raise ValueError("directions must have shape (K, 3)")
    if weights_array.shape != (len(directions),):
        raise ValueError("weights must have one value per direction")
    if not edge_list:
        raise ValueError("at least one shared edge is required")

    edge_i = np.asarray([edge[0] for edge in edge_list], dtype=int)
    edge_j = np.asarray([edge[1] for edge in edge_list], dtype=int)
    gamma = np.asarray([edge[2] for edge in edge_list], dtype=float)
    if np.min(weights_array) <= 0.0 or np.min(gamma) <= 0.0:
        raise ValueError(f"{family}: nonpositive mass or conductance")

    rate = np.zeros(len(directions), dtype=float)
    np.add.at(rate, edge_i, gamma / weights_array[edge_i])
    np.add.at(rate, edge_j, gamma / weights_array[edge_j])

    symmetric = np.zeros((len(directions), len(directions)), dtype=float)
    values = gamma / np.sqrt(weights_array[edge_i] * weights_array[edge_j])
    np.add.at(symmetric, (edge_i, edge_j), values)
    np.add.at(symmetric, (edge_j, edge_i), values)
    symmetric[np.diag_indices_from(symmetric)] = -rate
    if np.max(np.abs(symmetric - symmetric.T)) > 2.0e-13:
        raise ValueError(f"{family}: weighted symmetric transform failed")

    return AngularOperator(
        family=family,
        directions=directions,
        weights=weights_array,
        edge_i=edge_i,
        edge_j=edge_j,
        gamma=gamma,
        rate=rate,
        symmetric_matrix=symmetric,
    )


def build_icosphere(level: int) -> AngularOperator:
    if level < 0:
        raise ValueError("icosphere level must be nonnegative")
    vertices, faces = _g4.initial_icosahedron()
    for _ in range(level):
        vertices, faces = _g4.subdivide(vertices, faces)

    face_angles: list[dict[int, float]] = []
    edge_faces: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for face_index, (i, j, k) in enumerate(faces):
        ai, aj, ak = _g4.spherical_angles(vertices[i], vertices[j], vertices[k])
        face_angles.append({i: ai, j: aj, k: ak})
        for p, q in ((i, j), (j, k), (k, i)):
            edge = (p, q) if p < q else (q, p)
            edge_faces[edge].append(face_index)

    conductances: list[tuple[int, int, float, float]] = []
    neighbors: defaultdict[int, list[tuple[int, float, float]]] = defaultdict(list)
    for (i, j), adjacent in edge_faces.items():
        if len(adjacent) != 2:
            raise ValueError("closed spherical triangulation edge must have two faces")
        lam = _g4.spherical_distance(vertices[i], vertices[j])
        terms: list[float] = []
        for face_index in adjacent:
            face = faces[face_index]
            k = next(v for v in face if v != i and v != j)
            ai = face_angles[face_index][i]
            aj = face_angles[face_index][j]
            ak = face_angles[face_index][k]
            terms.append(math.tan((ai + aj - ak) / 2.0))
        cij = (terms[0] + terms[1]) / (2.0 * math.cos(lam / 2.0) ** 2)
        conductances.append((i, j, cij, lam))
        neighbors[i].append((j, cij, lam))
        neighbors[j].append((i, cij, lam))

    masses = np.asarray(
        [
            sum(cij * math.sin(lam / 2.0) ** 2 for _, cij, lam in neighbors[i])
            for i in range(len(vertices))
        ],
        dtype=float,
    )
    scale = 4.0 * math.pi / float(np.sum(masses))
    edges = [(i, j, scale * cij) for i, j, cij, _ in conductances]
    return make_operator(f"icosphere-L{level}", vertices, scale * masses, edges)


def build_product(n: int) -> AngularOperator:
    if n < 2:
        raise ValueError("product-grid order must be at least two")
    m = 2 * n
    delta = math.pi / n
    alpha = 2.0 * math.pi / m
    points: list[tuple[float, float, float]] = []
    weights: list[float] = []
    theta_values: list[float] = []
    for i in range(n):
        theta = (i + 0.5) * delta
        theta_values.append(theta)
        ring_weight = 2.0 * alpha * math.sin(theta) * math.sin(delta / 2.0)
        for j in range(m):
            phi = j * alpha
            points.append(
                (
                    math.cos(theta),
                    math.sin(theta) * math.cos(phi),
                    math.sin(theta) * math.sin(phi),
                )
            )
            weights.append(ring_weight)

    def index(i: int, j: int) -> int:
        return i * m + (j % m)

    edges: list[tuple[int, int, float]] = []
    for i in range(n - 1):
        conductance = alpha * math.sin((i + 1) * delta) / math.sin(delta)
        for j in range(m):
            edges.append((index(i, j), index(i + 1, j), conductance))
    for i, theta in enumerate(theta_values):
        conductance = (
            alpha
            * math.sin(delta / 2.0)
            / ((1.0 - math.cos(alpha)) * math.sin(theta))
        )
        for j in range(m):
            edges.append((index(i, j), index(i, j + 1), conductance))
    return make_operator(f"product-N{n}", points, weights, edges)


def nearest_product_n(direction_count: int) -> int:
    if direction_count <= 0:
        raise ValueError("direction count must be positive")
    return max(2, round(math.sqrt(direction_count / 2.0)))


def apply_generator(operator: AngularOperator, values: np.ndarray) -> np.ndarray:
    """Apply the sparse shared-edge generator.

    The first dimension must index angular directions. Any trailing dimensions
    are treated as independent right-hand sides.
    """

    data = np.asarray(values, dtype=float)
    if data.shape[0] != operator.count:
        raise ValueError("first generator dimension must match direction count")
    original_shape = data.shape
    flat = data.reshape(operator.count, -1)
    result = np.zeros_like(flat)
    difference = flat[operator.edge_j] - flat[operator.edge_i]
    np.add.at(
        result,
        operator.edge_i,
        operator.gamma[:, None] / operator.weights[operator.edge_i, None] * difference,
    )
    np.add.at(
        result,
        operator.edge_j,
        -operator.gamma[:, None] / operator.weights[operator.edge_j, None] * difference,
    )
    return result.reshape(original_shape)


def exact_semidiscrete_evolution(
    operator: AngularOperator, initial: np.ndarray, time: float
) -> np.ndarray:
    if time < 0.0:
        raise ValueError("time must be nonnegative")
    data = np.asarray(initial, dtype=float)
    if data.shape[0] != operator.count:
        raise ValueError("initial first dimension must match direction count")
    original_shape = data.shape
    flat = data.reshape(operator.count, -1)
    eigenvalues, eigenvectors = np.linalg.eigh(operator.symmetric_matrix)
    if float(np.max(eigenvalues)) > 5.0e-10:
        raise ValueError(f"{operator.family}: generator has positive eigenvalue")
    root_weight = np.sqrt(operator.weights)
    transformed = root_weight[:, None] * flat
    coefficients = eigenvectors.T @ transformed
    evolved = eigenvectors @ (np.exp(time * eigenvalues)[:, None] * coefficients)
    return (evolved / root_weight[:, None]).reshape(original_shape)


def weighted_integral(operator: AngularOperator, values: np.ndarray) -> np.ndarray:
    data = np.asarray(values, dtype=float)
    if data.shape[0] != operator.count:
        raise ValueError("first dimension must match direction count")
    return np.tensordot(operator.weights, data, axes=(0, 0))


def weighted_l2_error(
    operator: AngularOperator, approximation: np.ndarray, reference: np.ndarray
) -> float:
    difference = np.asarray(approximation, dtype=float) - np.asarray(reference, dtype=float)
    if difference.shape[0] != operator.count:
        raise ValueError("first dimension must match direction count")
    numerator = float(
        np.sum(
            operator.weights.reshape((-1,) + (1,) * (difference.ndim - 1))
            * difference**2
        )
    )
    ref = np.asarray(reference, dtype=float)
    denominator = float(
        np.sum(
            operator.weights.reshape((-1,) + (1,) * (ref.ndim - 1))
            * ref**2
        )
    )
    if denominator <= 0.0:
        raise ValueError("reference norm must be positive")
    return math.sqrt(numerator / denominator)
