#!/usr/bin/env python3
"""Deterministic Gate 4 audit for a quasi-uniform icosahedral AFP family.

The script constructs radial subdivisions of the regular icosahedron, interprets
all faces as geodesic spherical triangles, and assembles the discrete spherical
Laplacian of Izmestiev and Lam (JLMS 2025, arXiv:2408.04877).

For every refinement level it checks:

* manifold topology and positive spherical-Delaunay edge conductances;
* positive vertex masses;
* the three exact coordinate eigenrelations L x_k = -2 x_k;
* the exact zonal peak-defect identity;
* the general loss-window rate and defect bounds formalized in Lean;
* quasi-uniform edge-length ratios;
* deterministic h^2 defect and h^-2 rate scaling diagnostics.

Only the Python standard library is used. No random sampling is present.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Vec3 = Tuple[float, float, float]
Face = Tuple[int, int, int]
Edge = Tuple[int, int]


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a: Vec3) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: Vec3) -> Vec3:
    n = norm(a)
    if n == 0.0:
        raise ValueError("cannot normalize the zero vector")
    return (a[0] / n, a[1] / n, a[2] / n)


def clamp_unit(x: float) -> float:
    return max(-1.0, min(1.0, x))


def spherical_distance(a: Vec3, b: Vec3) -> float:
    return math.acos(clamp_unit(dot(a, b)))


def initial_icosahedron() -> Tuple[List[Vec3], List[Face]]:
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    raw = [
        (-1.0, golden, 0.0), (1.0, golden, 0.0),
        (-1.0, -golden, 0.0), (1.0, -golden, 0.0),
        (0.0, -1.0, golden), (0.0, 1.0, golden),
        (0.0, -1.0, -golden), (0.0, 1.0, -golden),
        (golden, 0.0, -1.0), (golden, 0.0, 1.0),
        (-golden, 0.0, -1.0), (-golden, 0.0, 1.0),
    ]
    vertices = [normalize(v) for v in raw]
    faces: List[Face] = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
    ]
    return vertices, faces


def subdivide(vertices: Sequence[Vec3], faces: Sequence[Face]) -> Tuple[List[Vec3], List[Face]]:
    out_vertices = list(vertices)
    midpoint_cache: Dict[Edge, int] = {}

    def midpoint(i: int, j: int) -> int:
        edge = (i, j) if i < j else (j, i)
        cached = midpoint_cache.get(edge)
        if cached is not None:
            return cached
        vi, vj = out_vertices[i], out_vertices[j]
        point = normalize(((vi[0] + vj[0]) / 2.0,
                           (vi[1] + vj[1]) / 2.0,
                           (vi[2] + vj[2]) / 2.0))
        index = len(out_vertices)
        out_vertices.append(point)
        midpoint_cache[edge] = index
        return index

    out_faces: List[Face] = []
    for i, j, k in faces:
        a = midpoint(i, j)
        b = midpoint(j, k)
        c = midpoint(k, i)
        out_faces.extend(((i, a, c), (j, b, a), (k, c, b), (a, b, c)))
    return out_vertices, out_faces


def spherical_angles(a: Vec3, b: Vec3, c: Vec3) -> Tuple[float, float, float]:
    """Return the spherical angles at a, b, and c."""
    side_a = spherical_distance(b, c)
    side_b = spherical_distance(a, c)
    side_c = spherical_distance(a, b)
    sin_a, sin_b, sin_c = math.sin(side_a), math.sin(side_b), math.sin(side_c)
    if min(sin_a, sin_b, sin_c) <= 0.0:
        raise ValueError("degenerate spherical triangle")
    angle_a = math.acos(clamp_unit(
        (math.cos(side_a) - math.cos(side_b) * math.cos(side_c)) / (sin_b * sin_c)))
    angle_b = math.acos(clamp_unit(
        (math.cos(side_b) - math.cos(side_a) * math.cos(side_c)) / (sin_a * sin_c)))
    angle_c = math.acos(clamp_unit(
        (math.cos(side_c) - math.cos(side_a) * math.cos(side_b)) / (sin_a * sin_b)))
    return angle_a, angle_b, angle_c


@dataclass
class AuditRow:
    level: int
    vertices: int
    faces: int
    edges: int
    min_conductance: float
    max_conductance: float
    min_mass: float
    max_mass: float
    min_edge: float
    max_edge: float
    edge_ratio: float
    delaunay_margin: float
    max_coordinate_residual: float
    min_rate: float
    max_rate: float
    min_defect: float
    max_defect: float
    max_defect_identity_error: float
    max_bound_violation: float


def assemble_and_audit(level: int, vertices: Sequence[Vec3], faces: Sequence[Face]) -> AuditRow:
    face_angles: List[Dict[int, float]] = []
    edge_faces: Dict[Edge, List[int]] = defaultdict(list)

    for face_index, (i, j, k) in enumerate(faces):
        ai, aj, ak = spherical_angles(vertices[i], vertices[j], vertices[k])
        face_angles.append({i: ai, j: aj, k: ak})
        for p, q in ((i, j), (j, k), (k, i)):
            edge = (p, q) if p < q else (q, p)
            edge_faces[edge].append(face_index)

    if any(len(adjacent) != 2 for adjacent in edge_faces.values()):
        raise AssertionError("triangulation is not a closed two-manifold")

    conductance: Dict[Edge, float] = {}
    edge_length: Dict[Edge, float] = {}
    delaunay_margin = math.inf

    for (i, j), adjacent in edge_faces.items():
        lam = spherical_distance(vertices[i], vertices[j])
        terms: List[float] = []
        opposite_sum = 0.0
        for face_index in adjacent:
            face = faces[face_index]
            k = next(v for v in face if v != i and v != j)
            angle_i = face_angles[face_index][i]
            angle_j = face_angles[face_index][j]
            angle_k = face_angles[face_index][k]
            terms.append(math.tan((angle_i + angle_j - angle_k) / 2.0))
            opposite_sum += angle_k
        cij = (terms[0] + terms[1]) / (2.0 * math.cos(lam / 2.0) ** 2)
        conductance[(i, j)] = cij
        edge_length[(i, j)] = lam
        delaunay_margin = min(delaunay_margin, math.pi - opposite_sum)

    neighbors: Dict[int, List[Tuple[int, float, float]]] = defaultdict(list)
    for (i, j), cij in conductance.items():
        lam = edge_length[(i, j)]
        neighbors[i].append((j, cij, lam))
        neighbors[j].append((i, cij, lam))

    masses: List[float] = []
    for i in range(len(vertices)):
        masses.append(sum(cij * math.sin(lam / 2.0) ** 2
                          for _, cij, lam in neighbors[i]))

    if min(conductance.values()) <= 0.0:
        raise AssertionError("nonpositive spherical-Delaunay conductance")
    if min(masses) <= 0.0:
        raise AssertionError("nonpositive vertex mass")
    if delaunay_margin <= 0.0:
        raise AssertionError("local spherical Delaunay condition failed")

    coordinate_residual = 0.0
    rates: List[float] = []
    defects: List[float] = []
    defect_identity_error = 0.0

    for i, point in enumerate(vertices):
        mass = masses[i]
        rate = sum(cij for _, cij, _ in neighbors[i]) / mass
        rates.append(rate)

        for component in range(3):
            action = sum(cij * (vertices[j][component] - point[component])
                         for j, cij, _ in neighbors[i]) / mass
            coordinate_residual = max(coordinate_residual,
                                      abs(action + 2.0 * point[component]))

        defect = sum((cij / mass) * (1.0 - dot(point, vertices[j])) ** 2
                     for j, cij, _ in neighbors[i])
        identity = 4.0 * sum((cij / mass) * math.sin(lam / 2.0) ** 4
                             for _, cij, lam in neighbors[i])
        defects.append(defect)
        defect_identity_error = max(defect_identity_error, abs(defect - identity))

    min_edge = min(edge_length.values())
    max_edge = max(edge_length.values())
    loss_min = 1.0 - math.cos(min_edge)
    loss_max = 1.0 - math.cos(max_edge)

    violations = [
        max(0.0, 2.0 * loss_min - min(defects)),
        max(0.0, max(defects) - 2.0 * loss_max),
        max(0.0, 2.0 / loss_max - min(rates)),
        max(0.0, max(rates) - 2.0 / loss_min),
    ]

    # Floating-point tolerances are intentionally much tighter than transport
    # tolerances and are checked at every vertex, not by sampling.
    if coordinate_residual > 2.0e-8:
        raise AssertionError(f"coordinate residual too large: {coordinate_residual:.3e}")
    if defect_identity_error > 2.0e-11:
        raise AssertionError(f"defect identity error too large: {defect_identity_error:.3e}")
    if max(violations) > 5.0e-10:
        raise AssertionError(f"loss-window bound violation: {max(violations):.3e}")
    if level >= 1 and max_edge / min_edge > 1.25:
        raise AssertionError("icosphere edge family failed quasi-uniformity audit")

    return AuditRow(
        level=level,
        vertices=len(vertices),
        faces=len(faces),
        edges=len(conductance),
        min_conductance=min(conductance.values()),
        max_conductance=max(conductance.values()),
        min_mass=min(masses),
        max_mass=max(masses),
        min_edge=min_edge,
        max_edge=max_edge,
        edge_ratio=max_edge / min_edge,
        delaunay_margin=delaunay_margin,
        max_coordinate_residual=coordinate_residual,
        min_rate=min(rates),
        max_rate=max(rates),
        min_defect=min(defects),
        max_defect=max(defects),
        max_defect_identity_error=defect_identity_error,
        max_bound_violation=max(violations),
    )


def regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    numerator = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    denominator = sum((x - mx) ** 2 for x in lx)
    return numerator / denominator


def write_outputs(rows: Sequence[AuditRow], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "icosphere_spherical_laplacian_audit.csv"
    md_path = output_dir / "icosphere_spherical_laplacian_audit.md"

    fieldnames = list(AuditRow.__dataclass_fields__.keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    fitted = [row for row in rows if row.level >= 1]
    resolutions = [2.0 ** row.level for row in fitted]
    rate_slope = regression_slope(resolutions, [row.max_rate for row in fitted])
    defect_slope = regression_slope(resolutions, [row.max_defect for row in fitted])
    edge_slope = regression_slope(resolutions, [row.max_edge for row in fitted])

    if not 1.80 <= rate_slope <= 2.20:
        raise AssertionError(f"unexpected rate slope {rate_slope:.6f}")
    if not -2.20 <= defect_slope <= -1.70:
        raise AssertionError(f"unexpected defect slope {defect_slope:.6f}")
    if not -1.10 <= edge_slope <= -0.90:
        raise AssertionError(f"unexpected edge slope {edge_slope:.6f}")

    lines = [
        "# Gate 4 deterministic icosphere audit",
        "",
        "The audit uses the spherical Delaunay Laplacian of Izmestiev–Lam on",
        "radially refined icosahedra. Every vertex and edge is checked.",
        "",
        f"- fitted maximum-rate slope versus `2^level`: `{rate_slope:.8f}`",
        f"- fitted maximum-defect slope versus `2^level`: `{defect_slope:.8f}`",
        f"- fitted maximum-edge slope versus `2^level`: `{edge_slope:.8f}`",
        "",
        "| level | vertices | edge ratio | min conductance | max coordinate residual | max defect | max rate |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.vertices} | {row.edge_ratio:.8f} | "
            f"{row.min_conductance:.8e} | {row.max_coordinate_residual:.3e} | "
            f"{row.max_defect:.8e} | {row.max_rate:.8e} |")
    lines.extend([
        "",
        "All conductances, masses, Delaunay margins, coordinate eigenrelations,",
        "defect identities, and loss-window bounds passed.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("gate4/generated"))
    args = parser.parse_args()
    if not 0 <= args.max_level <= 6:
        raise SystemExit("--max-level must be between 0 and 6")

    vertices, faces = initial_icosahedron()
    rows: List[AuditRow] = []
    for level in range(args.max_level + 1):
        if level > 0:
            vertices, faces = subdivide(vertices, faces)
        row = assemble_and_audit(level, vertices, faces)
        rows.append(row)
        print(
            f"level={level} vertices={row.vertices} edge_ratio={row.edge_ratio:.6f} "
            f"min_c={row.min_conductance:.6e} coord={row.max_coordinate_residual:.3e} "
            f"max_defect={row.max_defect:.6e} max_rate={row.max_rate:.6e}")

    write_outputs(rows, args.output_dir)
    print("Gate 4 deterministic icosphere audit: PASS")


if __name__ == "__main__":
    main()
