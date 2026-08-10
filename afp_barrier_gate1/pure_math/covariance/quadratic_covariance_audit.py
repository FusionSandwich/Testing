#!/usr/bin/env python3
"""Verify the quadratic covariance residual formula on Platonic graphs.

For an eigenmap Phi and symmetric form A, the predicted degree-two residual on
S^2 is

    trace(A (C_i + 2 Phi_i Phi_i^T)),

where C_i is the jump covariance.  This script verifies that formula against
direct generator application and reports the rank of the global constraint
span in the five-dimensional trace-free symmetric space.

The calculation is deterministic and finite.  It is a conjecture laboratory,
not a proof of an all-graph classification.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CovarianceAudit:
    name: str
    vertices: int
    constraint_rank: int
    exact_form_dimension: int
    evaluation_kernel_dimension: int
    nontrivial_exact_sample_dimension: int
    formula_error: float
    radial_covariance_min: float


def normalize(vertices: list[tuple[float, float, float]]) -> np.ndarray:
    values = np.asarray(vertices, dtype=float)
    return values / np.linalg.norm(values, axis=1)[:, None]


def polyhedra() -> dict[str, list[tuple[float, float, float]]]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    inv_phi = 1.0 / phi
    result: dict[str, list[tuple[float, float, float]]] = {
        "tetrahedron": [
            (1, 1, 1),
            (1, -1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
        ],
        "octahedron": [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ],
        "cube": [
            (x, y, z)
            for x in (-1, 1)
            for y in (-1, 1)
            for z in (-1, 1)
        ],
        "icosahedron": [
            (0, 1, phi),
            (0, -1, phi),
            (0, 1, -phi),
            (0, -1, -phi),
            (1, phi, 0),
            (-1, phi, 0),
            (1, -phi, 0),
            (-1, -phi, 0),
            (phi, 0, 1),
            (-phi, 0, 1),
            (phi, 0, -1),
            (-phi, 0, -1),
        ],
    }
    dodecahedron: list[tuple[float, float, float]] = []
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                dodecahedron.append((x, y, z))
    for a in (-1, 1):
        for b in (-1, 1):
            dodecahedron.extend(
                (
                    (0, a * inv_phi, b * phi),
                    (a * inv_phi, b * phi, 0),
                    (a * phi, 0, b * inv_phi),
                )
            )
    result["dodecahedron"] = dodecahedron
    return result


def shortest_edge_operator(vertices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    distance = np.linalg.norm(
        vertices[:, None, :] - vertices[None, :, :], axis=2
    )
    edge_length = distance[distance > 1.0e-10].min()
    adjacency = np.isclose(distance, edge_length, rtol=0.0, atol=1.0e-8)
    degree = adjacency.sum(axis=1).astype(float)
    neighbor_sum = adjacency @ vertices
    radial = np.sum(neighbor_sum * vertices, axis=1)
    denominator = degree - radial
    if np.ptp(denominator) > 1.0e-9:
        raise AssertionError("coordinate eigenvalue is not uniform")
    edge_rate = 2.0 / float(denominator[0])
    generator = edge_rate * (adjacency.astype(float) - np.diag(degree))
    return adjacency, generator


def tracefree_basis() -> np.ndarray:
    basis = np.zeros((5, 3, 3), dtype=float)
    basis[0] = np.diag((1.0, -1.0, 0.0))
    basis[1] = np.diag((-1.0, -1.0, 2.0))
    basis[2, 0, 1] = basis[2, 1, 0] = 0.5
    basis[3, 0, 2] = basis[3, 2, 0] = 0.5
    basis[4, 1, 2] = basis[4, 2, 1] = 0.5
    return basis


def quadratic_samples(vertices: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return np.einsum("ni,kij,nj->nk", vertices, basis, vertices)


def audit(name: str, raw_vertices: list[tuple[float, float, float]]) -> CovarianceAudit:
    vertices = normalize(raw_vertices)
    adjacency, generator = shortest_edge_operator(vertices)
    basis = tracefree_basis()
    samples = quadratic_samples(vertices, basis)
    direct_residual = generator @ samples + 6.0 * samples

    edge_rate = float(generator[np.where(adjacency)[0][0], np.where(adjacency)[1][0]])
    covariance = np.zeros((len(vertices), 3, 3), dtype=float)
    radial = np.zeros(len(vertices), dtype=float)
    for i in range(len(vertices)):
        for j in np.flatnonzero(adjacency[i]):
            delta = vertices[j] - vertices[i]
            covariance[i] += edge_rate * np.outer(delta, delta)
        radial[i] = vertices[i] @ covariance[i] @ vertices[i]

    constraint_tensor = covariance + 2.0 * np.einsum(
        "ni,nj->nij", vertices, vertices
    )
    predicted_residual = np.einsum("kij,nij->nk", basis, constraint_tensor)
    formula_error = float(np.max(np.abs(direct_residual - predicted_residual)))

    constraint_rank = int(np.linalg.matrix_rank(predicted_residual, tol=1.0e-9))
    evaluation_rank = int(np.linalg.matrix_rank(samples, tol=1.0e-9))
    exact_form_dimension = 5 - constraint_rank
    evaluation_kernel_dimension = 5 - evaluation_rank
    nontrivial_exact_sample_dimension = (
        exact_form_dimension - evaluation_kernel_dimension
    )

    if formula_error > 2.0e-10:
        raise AssertionError(f"{name}: covariance formula error {formula_error:.3e}")
    if float(np.min(radial)) <= 0.0:
        raise AssertionError(f"{name}: expected positive radial covariance")
    if nontrivial_exact_sample_dimension != 0:
        raise AssertionError(f"{name}: unexpected exact sampled H2 mode")

    return CovarianceAudit(
        name=name,
        vertices=len(vertices),
        constraint_rank=constraint_rank,
        exact_form_dimension=exact_form_dimension,
        evaluation_kernel_dimension=evaluation_kernel_dimension,
        nontrivial_exact_sample_dimension=nontrivial_exact_sample_dimension,
        formula_error=formula_error,
        radial_covariance_min=float(np.min(radial)),
    )


def main() -> None:
    print("Quadratic covariance audit")
    for name, vertices in polyhedra().items():
        result = audit(name, vertices)
        print(
            f"{result.name:12s} K={result.vertices:2d} "
            f"rank={result.constraint_rank} "
            f"exact_forms={result.exact_form_dimension} "
            f"evaluation_kernel={result.evaluation_kernel_dimension} "
            f"nontrivial_exact_samples={result.nontrivial_exact_sample_dimension} "
            f"formula_error={result.formula_error:.3e} "
            f"min_radial_cov={result.radial_covariance_min:.6e}"
        )
    print("Quadratic covariance audit: PASS")


if __name__ == "__main__":
    main()
