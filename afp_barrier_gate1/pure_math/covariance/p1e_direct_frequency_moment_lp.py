#!/usr/bin/env python3
"""Exploratory orbit-free LP for direct-frequency icosphere moment stresses.

This script is intentionally a conjecture finder, not an all-level proof.
It constructs the frequency-N radial icosphere, its graph square, and searches
for one shared positive edge stress satisfying tangent, loss--tangent, and
trace-free tangent-quadratic moments at every vertex.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from typing import Iterable

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, hstack, vstack
from scipy.spatial.transform import Rotation

def unit(v: np.ndarray) -> np.ndarray:
    return v / np.linalg.norm(v)


def initial_icosahedron() -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    golden = (1.0 + 5.0**0.5) / 2.0
    raw = [
        (-1.0, golden, 0.0), (1.0, golden, 0.0),
        (-1.0, -golden, 0.0), (1.0, -golden, 0.0),
        (0.0, -1.0, golden), (0.0, 1.0, golden),
        (0.0, -1.0, -golden), (0.0, 1.0, -golden),
        (golden, 0.0, -1.0), (golden, 0.0, 1.0),
        (-golden, 0.0, -1.0), (-golden, 0.0, 1.0),
    ]
    vertices = [tuple(unit(np.asarray(v, dtype=float))) for v in raw]
    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
    ]
    return vertices, faces


def direct_frequency_mesh(frequency: int) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    if frequency < 1:
        raise ValueError("frequency must be positive")
    base_vertices_raw, base_faces = initial_icosahedron()
    base_vertices = [np.asarray(v, dtype=float) for v in base_vertices_raw]
    vertices: list[np.ndarray] = []
    key_to_index: dict[tuple[int, int, int], int] = {}
    faces: list[tuple[int, int, int]] = []

    def intern(v: np.ndarray) -> int:
        x = unit(v)
        key = tuple(int(round(float(z) * 10**12)) for z in x)
        old = key_to_index.get(key)
        if old is not None:
            if np.linalg.norm(vertices[old] - x) > 3e-11:
                raise AssertionError("coordinate-key collision")
            return old
        out = len(vertices)
        vertices.append(x)
        key_to_index[key] = out
        return out

    for ia, ib, ic in base_faces:
        va, vb, vc = base_vertices[ia], base_vertices[ib], base_vertices[ic]
        local: dict[tuple[int, int], int] = {}
        for i in range(frequency + 1):
            for j in range(frequency + 1 - i):
                k = frequency - i - j
                local[(i, j)] = intern(i * va + j * vb + k * vc)
        for i in range(frequency):
            for j in range(frequency - i):
                faces.append((local[(i, j)], local[(i + 1, j)], local[(i, j + 1)]))
                if i + j <= frequency - 2:
                    faces.append(
                        (local[(i + 1, j)], local[(i + 1, j + 1)], local[(i, j + 1)])
                    )

    expected_vertices = 10 * frequency * frequency + 2
    expected_faces = 20 * frequency * frequency
    if len(vertices) != expected_vertices or len(faces) != expected_faces:
        raise AssertionError(
            f"bad direct mesh counts: V={len(vertices)}, F={len(faces)}, "
            f"expected {expected_vertices}, {expected_faces}"
        )
    return np.asarray(vertices), faces


def graph_edges(vertex_count: int, faces: Iterable[tuple[int, int, int]]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for a, b, c in faces:
        for i, j in ((a, b), (b, c), (c, a)):
            out.add((i, j) if i < j else (j, i))
    return out


def square_edges(vertex_count: int, edges: set[tuple[int, int]]) -> list[tuple[int, int]]:
    nbr: dict[int, set[int]] = defaultdict(set)
    for i, j in edges:
        nbr[i].add(j)
        nbr[j].add(i)
    out = set(edges)
    for i in range(vertex_count):
        for j in nbr[i]:
            for k in nbr[j]:
                if i != k:
                    out.add((i, k) if i < k else (k, i))
    return sorted(out)


def tangent_basis(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    axis = np.zeros(3)
    axis[int(np.argmin(np.abs(x)))] = 1.0
    e1 = unit(axis - float(axis @ x) * x)
    e2 = np.cross(x, e1)
    return e1, e2


def moment_matrix(vertices: np.ndarray, edges: list[tuple[int, int]]):
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    bases = [tangent_basis(x) for x in vertices]
    for edge_index, (i, j) in enumerate(edges):
        for source, target in ((i, j), (j, i)):
            x, y = vertices[source], vertices[target]
            e1, e2 = bases[source]
            ell = 1.0 - float(x @ y)
            tau = y - float(x @ y) * x
            t1, t2 = float(tau @ e1), float(tau @ e2)
            features = (t1, t2, ell * t1, ell * t2, t1 * t1 - t2 * t2, 2.0 * t1 * t2)
            for local_row, value in enumerate(features):
                rows.append(6 * source + local_row)
                cols.append(edge_index)
                data.append(value)
    return coo_matrix(
        (data, (rows, cols)), shape=(6 * len(vertices), len(edges)), dtype=float
    ).tocsr()


def icosahedral_edge_orbits(
    vertices: np.ndarray, edges: list[tuple[int, int]]
) -> list[list[int]]:
    key_to_vertex = {
        tuple(int(round(float(z) * 10**10)) for z in x): i
        for i, x in enumerate(vertices)
    }
    edge_to_index = {edge: i for i, edge in enumerate(edges)}
    matrices = list(Rotation.create_group("I").as_matrix())
    matrices += [-matrix for matrix in matrices]
    permutations: list[np.ndarray] = []
    for matrix in matrices:
        perm = []
        for x in vertices:
            key = tuple(int(round(float(z) * 10**10)) for z in (matrix @ x))
            perm.append(key_to_vertex[key])
        permutations.append(np.asarray(perm, dtype=int))

    unseen = set(range(len(edges)))
    orbits: list[list[int]] = []
    while unseen:
        seed = next(iter(unseen))
        i, j = edges[seed]
        orbit = set()
        for perm in permutations:
            pi, pj = int(perm[i]), int(perm[j])
            transformed = (pi, pj) if pi < pj else (pj, pi)
            orbit.add(edge_to_index[transformed])
        unseen.difference_update(orbit)
        orbits.append(sorted(orbit))
    return orbits


def solve(frequency: int, reduced: bool, criterion: str) -> None:
    vertices, faces = direct_frequency_mesh(frequency)
    first_edges = graph_edges(len(vertices), faces)
    edges = square_edges(len(vertices), first_edges)
    a = moment_matrix(vertices, edges)
    edge_count = len(edges)
    orbits = icosahedral_edge_orbits(vertices, edges)

    # Variables are edge(-orbit) weights z and t.  Mean edge weight is one,
    # A z=0, and z>=t; maximize t.
    if reduced:
        orbit_labels = np.empty(edge_count, dtype=int)
        for orbit_index, orbit in enumerate(orbits):
            orbit_labels[orbit] = orbit_index
        orbit_matrix = coo_matrix(
            (np.ones(edge_count), (np.arange(edge_count), orbit_labels)),
            shape=(edge_count, len(orbits)),
        ).tocsr()
        reduced_a = a @ orbit_matrix
        variable_count = len(orbits)
        multiplicities = np.asarray([len(orbit) for orbit in orbits], dtype=float)
    else:
        orbit_matrix = None
        reduced_a = a
        variable_count = edge_count
        multiplicities = np.ones(edge_count)

    zeros = coo_matrix((reduced_a.shape[0], 1)).tocsr()
    if criterion == "maxmin":
        aeq = vstack(
            [
                coo_matrix(np.r_[multiplicities, 0.0][None, :]).tocsr(),
                hstack([reduced_a, zeros], format="csr"),
            ],
            format="csr",
        )
        beq = np.r_[float(edge_count), np.zeros(reduced_a.shape[0])]
        aub = coo_matrix(
            (
                np.r_[-np.ones(variable_count), np.ones(variable_count)],
                (
                    np.r_[np.arange(variable_count), np.arange(variable_count)],
                    np.r_[np.arange(variable_count), np.full(variable_count, variable_count)],
                ),
            ),
            shape=(variable_count, variable_count + 1),
        ).tocsr()
        bub = np.zeros(variable_count)
        objective = np.r_[np.zeros(variable_count), -1.0]
    elif criterion == "linf":
        aeq = hstack([reduced_a, zeros], format="csr")
        beq = np.zeros(reduced_a.shape[0])
        # z-t <= 1 and -z-t <= -1.
        upper_rows = np.arange(variable_count)
        lower_rows = variable_count + np.arange(variable_count)
        col = np.r_[
            np.arange(variable_count),
            np.full(variable_count, variable_count),
            np.arange(variable_count),
            np.full(variable_count, variable_count),
        ]
        data = np.r_[
            np.ones(variable_count),
            -np.ones(variable_count),
            -np.ones(variable_count),
            -np.ones(variable_count),
        ]
        aub = coo_matrix(
            (
                data,
                (
                    np.r_[upper_rows, upper_rows, lower_rows, lower_rows],
                    col,
                ),
            ),
            shape=(2 * variable_count, variable_count + 1),
        ).tocsr()
        bub = np.r_[np.ones(variable_count), -np.ones(variable_count)]
        objective = np.r_[np.zeros(variable_count), 1.0]
    else:
        raise ValueError(criterion)
    result = linprog(
        objective,
        A_ub=aub,
        b_ub=bub,
        A_eq=aeq,
        b_eq=beq,
        bounds=[(None, None)] * variable_count + [(0.0, None)],
        method="highs",
        options={"dual_feasibility_tolerance": 1e-9, "primal_feasibility_tolerance": 1e-9},
    )
    print(
        f"N={frequency} V={len(vertices)} E1={len(first_edges)} E2={edge_count} "
        f"success={result.success} status={result.status}"
    )
    if result.success:
        raw = result.x[:variable_count]
        z = np.asarray(orbit_matrix @ raw).ravel() if reduced else raw
        residual = np.max(np.abs(a @ z))
        symmetric = z.copy()
        for orbit in orbits:
            symmetric[orbit] = float(np.mean(z[orbit]))
        symmetric *= edge_count / float(np.sum(symmetric))
        symmetric_residual = np.max(np.abs(a @ symmetric))
        orbit_labels = np.empty(edge_count, dtype=int)
        for orbit_index, orbit in enumerate(orbits):
            orbit_labels[orbit] = orbit_index
        print(
            f"  criterion={criterion} min={z.min():.9g} max={z.max():.9g} "
            f"t={result.x[-1]:.9g} "
            f"moment_residual={residual:.3e}"
        )
        print(
            f"  edge_orbits={len(orbits)} sym_min={symmetric.min():.9g} "
            f"sym_max={symmetric.max():.9g} sym_residual={symmetric_residual:.3e}"
        )
        np.savez_compressed(
            f"/tmp/p1e_direct_frequency_N{frequency}.npz",
            vertices=vertices,
            faces=np.asarray(faces),
            first_edges=np.asarray(sorted(first_edges)),
            square_edges=np.asarray(edges),
            weights=z,
            symmetric_weights=symmetric,
            edge_orbit=orbit_labels,
        )
    else:
        print(f"  message={result.message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frequencies", type=int, nargs="+")
    parser.add_argument("--reduced", action="store_true")
    parser.add_argument("--criterion", choices=("maxmin", "linf"), default="maxmin")
    args = parser.parse_args()
    for frequency in args.frequencies:
        solve(frequency, args.reduced, args.criterion)


if __name__ == "__main__":
    main()
