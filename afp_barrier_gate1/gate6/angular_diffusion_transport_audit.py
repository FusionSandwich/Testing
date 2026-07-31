#!/usr/bin/env python3
"""Deterministic Gate 6 angular-diffusion transport benchmark.

The benchmark compares the Gate 4 quasi-uniform spherical-Delaunay operator
with the Gate 3 equal-angle product operator at matched direction counts.

For a positive mixed Legendre profile it checks:

* exact semidiscrete angular-diffusion evolution using a weighted-symmetric
  eigendecomposition;
* positivity-CFL forward Euler evolution;
* weighted mass conservation and nonnegativity;
* orientation dependence of transient error;
* the ratio of positivity-limited explicit step counts.

The continuum reference is known exactly because each Legendre degree l decays
as exp(-l(l+1)t).  No random sampling is used.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
GATE4 = HERE.parent / "gate4" / "icosphere_spherical_laplacian_audit.py"
spec = importlib.util.spec_from_file_location("gate4_icosphere", GATE4)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load Gate 4 icosphere implementation")
g4 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g4
spec.loader.exec_module(g4)


@dataclass
class AngularOperator:
    family: str
    directions: np.ndarray
    weights: np.ndarray
    edge_i: np.ndarray
    edge_j: np.ndarray
    gamma: np.ndarray
    rate: np.ndarray
    symmetric_matrix: np.ndarray


@dataclass
class AuditRow:
    level: int
    family: str
    directions: int
    max_rate: float
    positive_dt_limit: float
    explicit_steps: int
    max_semigroup_error: float
    mean_semigroup_error: float
    semigroup_orientation_spread: float
    max_euler_error: float
    mean_euler_error: float
    euler_orientation_spread: float
    max_mass_error: float
    minimum_solution: float
    max_coordinate_residual: float


def normalize(v: Sequence[float]) -> np.ndarray:
    out = np.asarray(v, dtype=float)
    return out / np.linalg.norm(out)


def orientations() -> np.ndarray:
    raw = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
        (0, 1, 1), (0, 1, -1),
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1),
    ]
    return np.stack([normalize(v) for v in raw], axis=1)


def legendre_values(mu: np.ndarray) -> tuple[np.ndarray, ...]:
    p0 = np.ones_like(mu)
    p1 = mu
    p2 = 0.5 * (3.0 * mu**2 - 1.0)
    p3 = 0.5 * (5.0 * mu**3 - 3.0 * mu)
    p4 = (35.0 * mu**4 - 30.0 * mu**2 + 3.0) / 8.0
    return p0, p1, p2, p3, p4


def initial_profiles(points: np.ndarray, axes: np.ndarray) -> np.ndarray:
    mu = points @ axes
    _, _, p2, p3, p4 = legendre_values(mu)
    # Positive for every mu in [-1,1]: the perturbation magnitude is at most .65.
    return 1.0 + 0.35 * p2 + 0.20 * p3 + 0.10 * p4


def continuum_profiles(points: np.ndarray, axes: np.ndarray, time: float) -> np.ndarray:
    mu = points @ axes
    _, _, p2, p3, p4 = legendre_values(mu)
    return (
        1.0
        + 0.35 * math.exp(-6.0 * time) * p2
        + 0.20 * math.exp(-12.0 * time) * p3
        + 0.10 * math.exp(-20.0 * time) * p4
    )


def make_operator(
    family: str,
    points: Sequence[Sequence[float]],
    weights: Sequence[float],
    edges: Iterable[tuple[int, int, float]],
) -> AngularOperator:
    directions = np.asarray(points, dtype=float)
    weights_array = np.asarray(weights, dtype=float)
    edge_list = list(edges)
    edge_i = np.asarray([edge[0] for edge in edge_list], dtype=int)
    edge_j = np.asarray([edge[1] for edge in edge_list], dtype=int)
    gamma = np.asarray([edge[2] for edge in edge_list], dtype=float)

    if np.min(weights_array) <= 0.0 or np.min(gamma) <= 0.0:
        raise AssertionError(f"{family}: nonpositive mass or conductance")

    rate = np.zeros(len(directions), dtype=float)
    np.add.at(rate, edge_i, gamma / weights_array[edge_i])
    np.add.at(rate, edge_j, gamma / weights_array[edge_j])

    symmetric = np.zeros((len(directions), len(directions)), dtype=float)
    values = gamma / np.sqrt(weights_array[edge_i] * weights_array[edge_j])
    symmetric[edge_i, edge_j] += values
    symmetric[edge_j, edge_i] += values
    symmetric[np.diag_indices_from(symmetric)] = -rate

    if np.max(np.abs(symmetric - symmetric.T)) > 2.0e-13:
        raise AssertionError(f"{family}: weighted symmetric transform failed")

    return AngularOperator(
        family,
        directions,
        weights_array,
        edge_i,
        edge_j,
        gamma,
        rate,
        symmetric,
    )


def build_icosphere(level: int) -> AngularOperator:
    vertices, faces = g4.initial_icosahedron()
    for _ in range(level):
        vertices, faces = g4.subdivide(vertices, faces)

    face_angles = []
    edge_faces = defaultdict(list)
    for face_index, (i, j, k) in enumerate(faces):
        ai, aj, ak = g4.spherical_angles(vertices[i], vertices[j], vertices[k])
        face_angles.append({i: ai, j: aj, k: ak})
        for p, q in ((i, j), (j, k), (k, i)):
            edge = (p, q) if p < q else (q, p)
            edge_faces[edge].append(face_index)

    conductances: list[tuple[int, int, float, float]] = []
    neighbors = defaultdict(list)
    for (i, j), adjacent in edge_faces.items():
        lam = g4.spherical_distance(vertices[i], vertices[j])
        terms = []
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

    masses = np.asarray([
        sum(cij * math.sin(lam / 2.0) ** 2 for _, cij, lam in neighbors[i])
        for i in range(len(vertices))
    ])
    scale = 4.0 * math.pi / float(np.sum(masses))
    weights = scale * masses
    edges = [(i, j, scale * cij) for i, j, cij, _ in conductances]
    return make_operator(f"icosphere-L{level}", vertices, weights, edges)


def build_product(n: int) -> AngularOperator:
    if n < 2:
        raise ValueError("product-grid order must be at least two")
    m = 2 * n
    delta = math.pi / n
    alpha = 2.0 * math.pi / m
    points = []
    weights = []
    theta_values = []
    for i in range(n):
        theta = (i + 0.5) * delta
        theta_values.append(theta)
        ring_weight = 2.0 * alpha * math.sin(theta) * math.sin(delta / 2.0)
        for j in range(m):
            phi = j * alpha
            points.append((
                math.cos(theta),
                math.sin(theta) * math.cos(phi),
                math.sin(theta) * math.sin(phi),
            ))
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
            alpha * math.sin(delta / 2.0)
            / ((1.0 - math.cos(alpha)) * math.sin(theta))
        )
        for j in range(m):
            edges.append((index(i, j), index(i, j + 1), conductance))

    return make_operator(f"product-N{n}", points, weights, edges)


def apply_generator(operator: AngularOperator, values: np.ndarray) -> np.ndarray:
    result = np.zeros_like(values)
    difference = values[operator.edge_j] - values[operator.edge_i]
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
    return result


def weighted_relative_errors(
    weights: np.ndarray, approximation: np.ndarray, reference: np.ndarray
) -> np.ndarray:
    numerator = np.sum(weights[:, None] * (approximation - reference) ** 2, axis=0)
    denominator = np.sum(weights[:, None] * reference**2, axis=0)
    return np.sqrt(numerator / denominator)


def weighted_masses(weights: np.ndarray, values: np.ndarray) -> np.ndarray:
    return np.sum(weights[:, None] * values, axis=0)


def exact_semidiscrete_evolution(
    operator: AngularOperator, initial: np.ndarray, time: float
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(operator.symmetric_matrix)
    if float(np.max(eigenvalues)) > 5.0e-10:
        raise AssertionError(f"{operator.family}: generator has positive eigenvalue")
    root_weight = np.sqrt(operator.weights)
    transformed = root_weight[:, None] * initial
    coefficients = eigenvectors.T @ transformed
    evolved = eigenvectors @ (np.exp(time * eigenvalues)[:, None] * coefficients)
    return evolved / root_weight[:, None]


def explicit_euler_evolution(
    operator: AngularOperator, initial: np.ndarray, time: float, cfl_fraction: float
) -> tuple[np.ndarray, int, float]:
    dt_limit = 1.0 / float(np.max(operator.rate))
    steps = max(1, math.ceil(time / (cfl_fraction * dt_limit)))
    dt = time / steps
    if dt * float(np.max(operator.rate)) > cfl_fraction + 2.0e-14:
        raise AssertionError("computed Euler step violates requested CFL fraction")
    values = initial.copy()
    for _ in range(steps):
        values += dt * apply_generator(operator, values)
    return values, steps, dt_limit


def coordinate_residual(operator: AngularOperator) -> float:
    action = apply_generator(operator, operator.directions)
    return float(np.max(np.abs(action + 2.0 * operator.directions)))


def audit_operator(
    level: int,
    operator: AngularOperator,
    time: float,
    axes: np.ndarray,
) -> AuditRow:
    initial = initial_profiles(operator.directions, axes)
    reference = continuum_profiles(operator.directions, axes, time)
    if float(np.min(initial)) <= 0.0:
        raise AssertionError("initial profile is not strictly positive")

    initial_mass = weighted_masses(operator.weights, initial)

    semidiscrete = exact_semidiscrete_evolution(operator, initial, time)
    semigroup_errors = weighted_relative_errors(operator.weights, semidiscrete, reference)
    semigroup_mass_error = float(np.max(np.abs(
        weighted_masses(operator.weights, semidiscrete) - initial_mass
    )))

    euler, steps, dt_limit = explicit_euler_evolution(operator, initial, time, 0.9)
    euler_errors = weighted_relative_errors(operator.weights, euler, reference)
    euler_mass_error = float(np.max(np.abs(
        weighted_masses(operator.weights, euler) - initial_mass
    )))

    minimum_solution = min(float(np.min(semidiscrete)), float(np.min(euler)))
    max_mass_error = max(semigroup_mass_error, euler_mass_error)
    residual = coordinate_residual(operator)

    if max_mass_error > 2.0e-10:
        raise AssertionError(f"{operator.family}: mass error {max_mass_error:.3e}")
    if minimum_solution < -2.0e-11:
        raise AssertionError(f"{operator.family}: positivity failure {minimum_solution:.3e}")
    if residual > 3.0e-8:
        raise AssertionError(f"{operator.family}: degree-one residual {residual:.3e}")

    return AuditRow(
        level=level,
        family=operator.family,
        directions=len(operator.directions),
        max_rate=float(np.max(operator.rate)),
        positive_dt_limit=dt_limit,
        explicit_steps=steps,
        max_semigroup_error=float(np.max(semigroup_errors)),
        mean_semigroup_error=float(np.mean(semigroup_errors)),
        semigroup_orientation_spread=float(np.max(semigroup_errors) - np.min(semigroup_errors)),
        max_euler_error=float(np.max(euler_errors)),
        mean_euler_error=float(np.mean(euler_errors)),
        euler_orientation_spread=float(np.max(euler_errors) - np.min(euler_errors)),
        max_mass_error=max_mass_error,
        minimum_solution=minimum_solution,
        max_coordinate_residual=residual,
    )


def nearest_product_n(direction_count: int) -> int:
    return max(2, round(math.sqrt(direction_count / 2.0)))


def write_outputs(rows: Sequence[AuditRow], output_dir: Path, time: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "angular_diffusion_transport_audit.csv"
    md_path = output_dir / "angular_diffusion_transport_audit.md"
    fields = list(AuditRow.__dataclass_fields__)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Gate 6 angular-diffusion transport audit",
        "",
        f"Final time: `{time}`. The initial condition is a positive mixture of Legendre degrees 2--4.",
        "",
        "| level | family | K | max rate | positive dt | Euler steps | max exact-semigroup error | max Euler error | semigroup orientation spread | Euler orientation spread |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.max_rate:.8e} | "
            f"{row.positive_dt_limit:.8e} | {row.explicit_steps} | "
            f"{row.max_semigroup_error:.8e} | {row.max_euler_error:.8e} | "
            f"{row.semigroup_orientation_spread:.8e} | {row.euler_orientation_spread:.8e} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--time", type=float, default=0.1)
    parser.add_argument("--output-dir", type=Path, default=Path("gate6/generated"))
    args = parser.parse_args()
    if not 1 <= args.max_level <= 3:
        raise SystemExit("--max-level must be between 1 and 3 for the dense semigroup audit")
    if args.time <= 0.0:
        raise SystemExit("--time must be positive")

    axes = orientations()
    rows: list[AuditRow] = []
    for level in range(1, args.max_level + 1):
        icosphere = build_icosphere(level)
        product = build_product(nearest_product_n(len(icosphere.directions)))
        ico_row = audit_operator(level, icosphere, args.time, axes)
        product_row = audit_operator(level, product, args.time, axes)
        rows.extend((ico_row, product_row))
        step_ratio = product_row.explicit_steps / ico_row.explicit_steps
        print(
            f"level={level} icoK={ico_row.directions} productK={product_row.directions} "
            f"steps={ico_row.explicit_steps}/{product_row.explicit_steps} "
            f"step_ratio={step_ratio:.3f} "
            f"semigroup_error={ico_row.max_semigroup_error:.3e}/{product_row.max_semigroup_error:.3e}"
        )
        if step_ratio <= 1.0:
            raise AssertionError("product grid did not require more positivity-limited steps")

    paired = [(rows[k], rows[k + 1]) for k in range(0, len(rows), 2)]
    if paired[-1][1].explicit_steps / paired[-1][0].explicit_steps < 20.0:
        raise AssertionError("finest product-grid stiffness separation is unexpectedly small")
    if paired[-1][0].max_semigroup_error >= paired[-1][1].max_semigroup_error:
        raise AssertionError("finest quasi-uniform semigroup error is not lower than product error")
    if any(paired[k + 1][0].max_semigroup_error >= paired[k][0].max_semigroup_error
           for k in range(len(paired) - 1)):
        raise AssertionError("quasi-uniform semigroup error did not decrease under refinement")
    if any(paired[k + 1][1].max_semigroup_error >= paired[k][1].max_semigroup_error
           for k in range(len(paired) - 1)):
        raise AssertionError("product semigroup error did not decrease under refinement")

    write_outputs(rows, args.output_dir, args.time)
    print("Gate 6 angular-diffusion transport audit: PASS")


if __name__ == "__main__":
    main()
