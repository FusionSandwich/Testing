#!/usr/bin/env python3
"""Deterministic falsification laboratory for the AFP pure-math track.

The script is intentionally hostile to attractive but unsupported claims.
It checks:

1. `Q = 1` on all five Platonic equal-edge graph embeddings, rejecting any
   unrestricted `{4,6,12}` classification.
2. The exact leading coefficient `8/pi^4` of the equal-angle polar rate.
3. Noncommutativity of two nonproportional stopping flows, rejecting a general
   layer-order-independence claim.
4. The sampled degree-two harmonic exact subspace for each Platonic graph.  A
   null form whose samples vanish on the vertex set is distinguished from a
   nontrivial exact sampled mode.

No random sampling is used.  Finite computations are evidence and regression
protection, not all-orders theorems.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp


@dataclass(frozen=True)
class GraphAudit:
    name: str
    vertices: int
    degree: int
    q_value: float
    tangent_error: float
    degree_two_evaluation_rank: int
    degree_two_residual_rank: int
    nontrivial_exact_degree_two_dimension: int


def normalize(vertices: list[tuple[float, float, float]]) -> np.ndarray:
    values = np.asarray(vertices, dtype=float)
    return values / np.linalg.norm(values, axis=1)[:, None]


def shortest_edge_graph(
    vertices: list[tuple[float, float, float]],
) -> tuple[np.ndarray, np.ndarray]:
    values = normalize(vertices)
    distances = np.linalg.norm(values[:, None, :] - values[None, :, :], axis=2)
    edge_length = distances[distances > 1.0e-10].min()
    adjacency = np.isclose(distances, edge_length, rtol=0.0, atol=1.0e-8)
    return values, adjacency


def traceless_quadratic_samples(vertices: np.ndarray) -> np.ndarray:
    """Five standard real degree-two harmonic samples on `S^2`."""

    x, y, z = vertices.T
    return np.stack(
        (
            x * x - y * y,
            2.0 * z * z - x * x - y * y,
            x * y,
            x * z,
            y * z,
        ),
        axis=1,
    )


def audit_equal_edge_graph(
    name: str,
    vertices: list[tuple[float, float, float]],
) -> GraphAudit:
    values, adjacency = shortest_edge_graph(vertices)
    degree = adjacency.sum(axis=1).astype(int)
    if np.ptp(degree) != 0:
        raise AssertionError(f"{name}: shortest-edge graph is not regular")

    neighbor_sum = adjacency @ values
    radial = np.sum(neighbor_sum * values, axis=1)
    tangential_error = float(
        np.linalg.norm(neighbor_sum - radial[:, None] * values, axis=1).max()
    )
    eigen_denominator = degree - radial
    if np.ptp(eigen_denominator) > 1.0e-9:
        raise AssertionError(f"{name}: coordinate space lacks one eigenvalue")

    rate_per_edge = 2.0 / float(eigen_denominator[0])
    losses = 1.0 - np.sum(values[:, None, :] * values[None, :, :], axis=2)
    total_rate = float(degree[0]) * rate_per_edge
    defect = rate_per_edge * float(np.sum(losses[0, adjacency[0]] ** 2))
    q_value = total_rate * defect / 4.0

    generator = rate_per_edge * (
        adjacency.astype(float) - np.diag(degree.astype(float))
    )
    quadratic = traceless_quadratic_samples(values)
    residual = generator @ quadratic + 6.0 * quadratic
    evaluation_rank = int(np.linalg.matrix_rank(quadratic, tol=1.0e-9))
    residual_rank = int(np.linalg.matrix_rank(residual, tol=1.0e-9))
    exact_form_dimension = 5 - residual_rank
    zero_sample_dimension = 5 - evaluation_rank
    nontrivial_exact_dimension = exact_form_dimension - zero_sample_dimension

    if nontrivial_exact_dimension < 0:
        raise AssertionError(f"{name}: inconsistent rank calculation")

    return GraphAudit(
        name=name,
        vertices=len(values),
        degree=int(degree[0]),
        q_value=q_value,
        tangent_error=tangential_error,
        degree_two_evaluation_rank=evaluation_rank,
        degree_two_residual_rank=residual_rank,
        nontrivial_exact_degree_two_dimension=nontrivial_exact_dimension,
    )


def platonic_vertices() -> dict[str, list[tuple[float, float, float]]]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    inv_phi = 1.0 / phi
    polyhedra: dict[str, list[tuple[float, float, float]]] = {
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
    polyhedra["dodecahedron"] = dodecahedron
    return polyhedra


def audit_platonic_claims() -> list[GraphAudit]:
    print("Q=1 and quadratic-subspace counterexample audit")
    audits = [
        audit_equal_edge_graph(name, vertices)
        for name, vertices in platonic_vertices().items()
    ]
    for result in audits:
        print(
            f"{result.name:12s} K={result.vertices:2d} "
            f"degree={result.degree} Q={result.q_value:.15f} "
            f"tangent={result.tangent_error:.3e} "
            f"rank(eval/res)={result.degree_two_evaluation_rank}/"
            f"{result.degree_two_residual_rank} "
            f"nontrivial_exact_H2={result.nontrivial_exact_degree_two_dimension}"
        )
        if abs(result.q_value - 1.0) > 1.0e-10:
            raise AssertionError(f"{result.name}: failed Q=1 regression")
        if result.nontrivial_exact_degree_two_dimension != 0:
            raise AssertionError(
                f"{result.name}: unexpected nontrivial exact degree-two mode"
            )

    counts = {result.vertices for result in audits}
    if not {8, 20}.issubset(counts):
        raise AssertionError("cube/dodecahedron counterexamples are missing")
    return audits


def audit_polar_asymptotics() -> None:
    n = sp.symbols("N", positive=True)
    x = sp.pi / (2 * n)
    polar_rate = 1 / (2 * sp.sin(x) ** 2) + 1 / (2 * sp.sin(x) ** 4)
    leading = sp.limit(polar_rate / n**4, n, sp.oo)
    print("\nPolar-rate leading coefficient:", leading)
    if sp.simplify(leading - 8 / sp.pi**4) != 0:
        raise AssertionError("incorrect polar-rate leading coefficient")


def audit_noncommuting_stopping_flows() -> None:
    e0, ka, xa, kb, xb = sp.symbols("E0 ka xa kb xb", positive=True)
    # Layer A: constant stopping; layer B: exponential flow dE/dx = -kb E.
    e_ab = (e0 - ka * xa) * sp.exp(-kb * xb)
    e_ba = e0 * sp.exp(-kb * xb) - ka * xa
    difference = sp.factor(e_ab - e_ba)
    print("\nNoncommuting stopping-flow order difference:", difference)
    if difference == 0:
        raise AssertionError("expected nonzero layer-order dependence")


def main() -> None:
    audit_platonic_claims()
    audit_polar_asymptotics()
    audit_noncommuting_stopping_flows()
    print("\nAll pure-math falsification checks passed.")


if __name__ == "__main__":
    main()
