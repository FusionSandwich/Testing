#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
GATE4 = HERE.parent / "gate4" / "icosphere_spherical_laplacian_audit.py"
spec = importlib.util.spec_from_file_location("gate4_icosphere", GATE4)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load Gate 4 icosphere audit")
g4 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g4
spec.loader.exec_module(g4)


@dataclass
class AuditRow:
    level: int
    directions: int
    min_efficiency: float
    max_efficiency: float
    mean_efficiency: float
    max_variance_identity_error: float
    product_n: int
    product_directions: int
    product_polar_efficiency: float
    product_to_icosphere_efficiency: float


def icosphere_efficiency(vertices, faces):
    face_angles = []
    edge_faces = defaultdict(list)
    for face_index, (i, j, k) in enumerate(faces):
        ai, aj, ak = g4.spherical_angles(vertices[i], vertices[j], vertices[k])
        face_angles.append({i: ai, j: aj, k: ak})
        for p, q in ((i, j), (j, k), (k, i)):
            edge = (p, q) if p < q else (q, p)
            edge_faces[edge].append(face_index)

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
        conductance = (terms[0] + terms[1]) / (2.0 * math.cos(lam / 2.0) ** 2)
        neighbors[i].append((j, conductance, lam))
        neighbors[j].append((i, conductance, lam))

    masses = [
        sum(c * math.sin(lam / 2.0) ** 2 for _, c, lam in neighbors[i])
        for i in range(len(vertices))
    ]

    efficiencies = []
    max_identity_error = 0.0
    for i, point in enumerate(vertices):
        mass = masses[i]
        rates = [(j, c / mass) for j, c, _ in neighbors[i]]
        rate = sum(a for _, a in rates)
        losses = [(a, 1.0 - g4.dot(point, vertices[j])) for j, a in rates]
        first = sum(a * ell for a, ell in losses)
        defect = sum(a * ell * ell for a, ell in losses)
        mean = first / rate
        variance = sum(a * (ell - mean) ** 2 for a, ell in losses)
        gap = rate * defect - first * first
        max_identity_error = max(
            max_identity_error,
            abs(gap - rate * variance),
            abs(first - 2.0),
        )
        efficiencies.append(rate * defect / 4.0)

    return (
        min(efficiencies),
        max(efficiencies),
        sum(efficiencies) / len(efficiencies),
        max_identity_error,
    )


def product_polar_efficiency(n: int) -> float:
    h = math.pi / (2.0 * n)
    st = math.sin(h)
    meridional_loss = 2.0 * math.sin(h) ** 2
    azimuthal_loss = 2.0 * st * st * math.sin(h) ** 2
    meridional_rate = 1.0 / (2.0 * math.sin(h) ** 2)
    azimuthal_rate = 1.0 / (2.0 * math.sin(h) ** 2 * st * st)
    rate = meridional_rate + azimuthal_rate
    first = meridional_rate * meridional_loss + azimuthal_rate * azimuthal_loss
    defect = (
        meridional_rate * meridional_loss**2
        + azimuthal_rate * azimuthal_loss**2
    )
    mean = first / rate
    variance = (
        meridional_rate * (meridional_loss - mean) ** 2
        + azimuthal_rate * (azimuthal_loss - mean) ** 2
    )
    if abs(first - 2.0) > 1.0e-11:
        raise AssertionError("product first loss moment is not two")
    if abs((rate * defect - 4.0) - rate * variance) > 1.0e-8 * max(1.0, rate * defect):
        raise AssertionError("product variance identity failed")
    exact_gap = (st * st - 1.0) ** 2 / (st * st)
    if abs((rate * defect - 4.0) - exact_gap) > 1.0e-8 * max(1.0, exact_gap):
        raise AssertionError("product exact gap formula failed")
    return rate * defect / 4.0


def nearest_product_n(direction_count: int) -> int:
    return max(2, round(math.sqrt(direction_count / 2.0)))


def regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=5)
    parser.add_argument("--output-dir", type=Path, default=Path("gate5/generated"))
    args = parser.parse_args()

    vertices, faces = g4.initial_icosahedron()
    rows = []
    for level in range(args.max_level + 1):
        if level:
            vertices, faces = g4.subdivide(vertices, faces)
        minimum, maximum, mean, error = icosphere_efficiency(vertices, faces)
        n = nearest_product_n(len(vertices))
        product_efficiency = product_polar_efficiency(n)
        if minimum < 1.0 - 2.0e-10:
            raise AssertionError(f"efficiency below one at level {level}: {minimum}")
        if maximum > 1.03:
            raise AssertionError(f"icosphere efficiency unexpectedly large: {maximum}")
        if error > 5.0e-8:
            raise AssertionError(f"variance identity error: {error}")
        row = AuditRow(
            level,
            len(vertices),
            minimum,
            maximum,
            mean,
            error,
            n,
            2 * n * n,
            product_efficiency,
            product_efficiency / maximum,
        )
        rows.append(row)
        print(
            f"level={level} K={len(vertices)} Q=[{minimum:.9f},{maximum:.9f}] "
            f"productQ={product_efficiency:.6f} ratio={product_efficiency / maximum:.3f}"
        )

    fitted = [row for row in rows if row.level >= 1]
    growth = regression_slope(
        [2.0**row.level for row in fitted],
        [row.product_polar_efficiency for row in fitted],
    )
    if not 1.8 <= growth <= 2.2:
        raise AssertionError(f"unexpected product efficiency slope {growth}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "sharpness_audit.csv"
    md_path = args.output_dir / "sharpness_audit.md"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(AuditRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Gate 5 sharpness audit",
        "",
        f"- product polar-efficiency slope versus refinement frequency: `{growth:.8f}`",
        "",
        "| level | icosphere K | max Q | product K | product polar Q | Q ratio |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.directions} | {row.max_efficiency:.9f} | "
            f"{row.product_directions} | {row.product_polar_efficiency:.6f} | "
            f"{row.product_to_icosphere_efficiency:.3f} |"
        )
    lines.extend(
        [
            "",
            "Here `Q = rate * defect / 4`. The universal inequality is `Q >= 1`.",
            "The weighted-variance identity was checked at every icosphere vertex and for every product-grid polar row.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Gate 5 sharpness audit: PASS")


if __name__ == "__main__":
    main()
