#!/usr/bin/env python3
"""Deterministic low-mode spectrum and rotational-bias audit for Gate 5.

The script compares the positive quasi-uniform icosphere operator with the
explicit equal-angle product operator at node-matched resolutions.  It uses
zonal spherical harmonics P_l(u dot Omega), deterministic test axes, and only
the Python standard library.

For every family, level, and degree it reports:

* the range of weighted Rayleigh eigenvalue estimates;
* maximum relative eigenvalue error;
* orientation-to-orientation eigenvalue spread;
* maximum weighted residual against the exact eigenvalue -l(l+1).

The degree-one mode is used as an exactness regression check.  Degrees two
through four quantify higher-mode error and rotational bias without claiming
that any sampled zonal vector is a discrete eigenvector.
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
from typing import Iterable, List, Sequence, Tuple

HERE = Path(__file__).resolve().parent
GATE4 = HERE.parent / "gate4" / "icosphere_spherical_laplacian_audit.py"
spec = importlib.util.spec_from_file_location("gate4_icosphere_spectrum", GATE4)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load Gate 4 icosphere audit")
g4 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g4
spec.loader.exec_module(g4)

Vec3 = Tuple[float, float, float]
NeighborRow = List[Tuple[int, float]]


@dataclass
class OperatorData:
    points: List[Vec3]
    weights: List[float]
    neighbors: List[NeighborRow]


@dataclass
class SpectralRow:
    level: int
    family: str
    directions: int
    degree: int
    exact_eigenvalue: float
    rayleigh_min: float
    rayleigh_max: float
    rayleigh_mean: float
    max_relative_eigenvalue_error: float
    rotational_spread: float
    max_relative_residual: float


def normalize(v: Vec3) -> Vec3:
    length = math.sqrt(sum(x * x for x in v))
    if length == 0.0:
        raise ValueError("zero axis")
    return tuple(x / length for x in v)  # type: ignore[return-value]


def deterministic_axes() -> List[Vec3]:
    raw: List[Vec3] = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (1.0, -1.0, 0.0),
        (1.0, 0.0, 1.0),
        (1.0, 0.0, -1.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, -1.0),
        (1.0, 1.0, 1.0),
        (1.0, 1.0, -1.0),
        (1.0, -1.0, 1.0),
        (-1.0, 1.0, 1.0),
    ]
    return [normalize(v) for v in raw]


def legendre(degree: int, x: float) -> float:
    if degree == 0:
        return 1.0
    if degree == 1:
        return x
    p_nm2, p_nm1 = 1.0, x
    for n in range(2, degree + 1):
        p_n = ((2 * n - 1) * x * p_nm1 - (n - 1) * p_nm2) / n
        p_nm2, p_nm1 = p_nm1, p_n
    return p_nm1


def apply_operator(values: Sequence[float], neighbors: Sequence[NeighborRow]) -> List[float]:
    return [
        sum(rate * (values[j] - values[i]) for j, rate in row)
        for i, row in enumerate(neighbors)
    ]


def weighted_inner(weights: Sequence[float], left: Sequence[float], right: Sequence[float]) -> float:
    return sum(w * x * y for w, x, y in zip(weights, left, right))


def assemble_icosphere(vertices: Sequence[Vec3], faces) -> OperatorData:
    face_angles = []
    edge_faces = defaultdict(list)
    for face_index, (i, j, k) in enumerate(faces):
        ai, aj, ak = g4.spherical_angles(vertices[i], vertices[j], vertices[k])
        face_angles.append({i: ai, j: aj, k: ak})
        for p, q in ((i, j), (j, k), (k, i)):
            edge = (p, q) if p < q else (q, p)
            edge_faces[edge].append(face_index)

    conductance = {}
    lengths = {}
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
        c = (terms[0] + terms[1]) / (2.0 * math.cos(lam / 2.0) ** 2)
        if c <= 0.0:
            raise AssertionError("nonpositive icosphere conductance")
        conductance[(i, j)] = c
        lengths[(i, j)] = lam

    raw_neighbors = defaultdict(list)
    for (i, j), c in conductance.items():
        lam = lengths[(i, j)]
        raw_neighbors[i].append((j, c, lam))
        raw_neighbors[j].append((i, c, lam))

    masses = [
        sum(c * math.sin(lam / 2.0) ** 2 for _, c, lam in raw_neighbors[i])
        for i in range(len(vertices))
    ]
    if min(masses) <= 0.0:
        raise AssertionError("nonpositive icosphere mass")
    scale = 4.0 * math.pi / sum(masses)
    weights = [scale * mass for mass in masses]
    neighbors: List[NeighborRow] = [
        [(j, c / masses[i]) for j, c, _ in raw_neighbors[i]]
        for i in range(len(vertices))
    ]
    return OperatorData(list(vertices), weights, neighbors)


def assemble_product(n: int) -> OperatorData:
    if n < 2:
        raise ValueError("n must be at least two")
    m = 2 * n
    delta = math.pi / n
    alpha = 2.0 * math.pi / m
    half = delta / 2.0

    points: List[Vec3] = []
    weights: List[float] = []
    for i in range(n):
        theta = (i + 0.5) * delta
        st, ct = math.sin(theta), math.cos(theta)
        q = 2.0 * alpha * st * math.sin(half)
        for j in range(m):
            phi = j * alpha
            points.append((ct, st * math.cos(phi), st * math.sin(phi)))
            weights.append(q)

    def index(i: int, j: int) -> int:
        return i * m + (j % m)

    neighbors: List[NeighborRow] = [[] for _ in points]
    sin_delta = math.sin(delta)
    one_minus_cos_alpha = 1.0 - math.cos(alpha)
    for i in range(n):
        theta = (i + 0.5) * delta
        st = math.sin(theta)
        q = 2.0 * alpha * st * math.sin(half)
        c_az = alpha * math.sin(half) / (one_minus_cos_alpha * st)
        for j in range(m):
            row = neighbors[index(i, j)]
            row.append((index(i, j + 1), c_az / q))
            row.append((index(i, j - 1), c_az / q))
            if i + 1 < n:
                b_plus = alpha * math.sin((i + 1) * delta) / sin_delta
                row.append((index(i + 1, j), b_plus / q))
            if i > 0:
                b_minus = alpha * math.sin(i * delta) / sin_delta
                row.append((index(i - 1, j), b_minus / q))
    return OperatorData(points, weights, neighbors)


def mode_metrics(operator: OperatorData, degree: int, axes: Iterable[Vec3]):
    exact = float(degree * (degree + 1))
    rayleigh = []
    residuals = []
    for axis in axes:
        values = [legendre(degree, g4.dot(axis, point)) for point in operator.points]
        action = apply_operator(values, operator.neighbors)
        norm_sq = weighted_inner(operator.weights, values, values)
        if norm_sq <= 0.0:
            raise AssertionError("nonpositive mode norm")
        rq = -weighted_inner(operator.weights, values, action) / norm_sq
        residual = [a + exact * v for a, v in zip(action, values)]
        residual_rel = math.sqrt(weighted_inner(operator.weights, residual, residual)) / (
            exact * math.sqrt(norm_sq)
        )
        rayleigh.append(rq)
        residuals.append(residual_rel)
    return {
        "exact": exact,
        "minimum": min(rayleigh),
        "maximum": max(rayleigh),
        "mean": sum(rayleigh) / len(rayleigh),
        "max_error": max(abs(value - exact) / exact for value in rayleigh),
        "spread": (max(rayleigh) - min(rayleigh)) / exact,
        "max_residual": max(residuals),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("gate5/generated"))
    args = parser.parse_args()

    axes = deterministic_axes()
    vertices, faces = g4.initial_icosahedron()
    rows: List[SpectralRow] = []

    for level in range(args.max_level + 1):
        if level:
            vertices, faces = g4.subdivide(vertices, faces)
        ico = assemble_icosphere(vertices, faces)
        product_n = max(2, round(math.sqrt(len(vertices) / 2.0)))
        product = assemble_product(product_n)

        for family, operator in (("icosphere", ico), ("product", product)):
            for degree in (1, 2, 3, 4):
                metrics = mode_metrics(operator, degree, axes)
                if degree == 1 and metrics["max_residual"] > 5.0e-8:
                    raise AssertionError(
                        f"degree-one exactness failed for {family} level {level}: "
                        f"{metrics['max_residual']:.3e}"
                    )
                for value in metrics.values():
                    if not math.isfinite(value):
                        raise AssertionError("nonfinite spectral metric")
                rows.append(
                    SpectralRow(
                        level=level,
                        family=family,
                        directions=len(operator.points),
                        degree=degree,
                        exact_eigenvalue=metrics["exact"],
                        rayleigh_min=metrics["minimum"],
                        rayleigh_max=metrics["maximum"],
                        rayleigh_mean=metrics["mean"],
                        max_relative_eigenvalue_error=metrics["max_error"],
                        rotational_spread=metrics["spread"],
                        max_relative_residual=metrics["max_residual"],
                    )
                )
                print(
                    f"level={level} family={family} K={len(operator.points)} l={degree} "
                    f"eigerr={metrics['max_error']:.3e} spread={metrics['spread']:.3e} "
                    f"resid={metrics['max_residual']:.3e}"
                )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "spectral_bias_audit.csv"
    md_path = args.output_dir / "spectral_bias_audit.md"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SpectralRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Gate 5 low-mode and rotational-bias audit",
        "",
        "The table reports the maximum relative Rayleigh eigenvalue error, the",
        "orientation-to-orientation Rayleigh spread, and the maximum relative",
        "residual of deterministic zonal harmonics.",
        "",
        "| level | family | directions | degree | max eigen error | rotational spread | max residual |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.degree} | "
            f"{row.max_relative_eigenvalue_error:.6e} | {row.rotational_spread:.6e} | "
            f"{row.max_relative_residual:.6e} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Gate 5 spectral and rotational-bias audit: PASS")


if __name__ == "__main__":
    main()
