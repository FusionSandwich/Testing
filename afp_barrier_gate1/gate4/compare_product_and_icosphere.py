#!/usr/bin/env python3
"""Compare the Gate 3 product grid and Gate 4 icosphere at similar node counts.

The comparison uses only exact formulas proved in Gate 3 and the deterministic
Gate 4 CSV. It is diagnostic rather than a replacement for either proof.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Dict, List


def nearest_product_order(vertices: int) -> int:
    target = math.sqrt(vertices / 2.0)
    candidates = {max(2, int(math.floor(target))), max(2, int(math.ceil(target)))}
    return min(candidates, key=lambda n: (abs(2 * n * n - vertices), n))


def product_grid_metrics(n: int) -> tuple[int, float, float]:
    nodes = 2 * n * n
    half_step = math.pi / (2.0 * n)
    sin_h_sq = math.sin(half_step) ** 2
    max_ring_sine_sq = max(
        math.sin((i + 0.5) * math.pi / n) ** 2 for i in range(n)
    )
    max_defect = 2.0 * sin_h_sq * (1.0 + max_ring_sine_sq)
    max_rate = 1.0 / (2.0 * sin_h_sq) + 1.0 / (2.0 * sin_h_sq ** 2)
    return nodes, max_defect, max_rate


def regression_slope(xs: List[float], ys: List[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sum(
        (x - mx) ** 2 for x in lx
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("gate4/generated/icosphere_spherical_laplacian_audit.csv"),
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("gate4/generated")
    )
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as handle:
        source_rows: List[Dict[str, str]] = list(csv.DictReader(handle))

    rows: List[Dict[str, float | int]] = []
    for source in source_rows:
        level = int(source["level"])
        ico_nodes = int(source["vertices"])
        ico_defect = float(source["max_defect"])
        ico_rate = float(source["max_rate"])
        n = nearest_product_order(ico_nodes)
        product_nodes, product_defect, product_rate = product_grid_metrics(n)
        rows.append(
            {
                "level": level,
                "icosphere_nodes": ico_nodes,
                "product_order": n,
                "product_nodes": product_nodes,
                "node_ratio": product_nodes / ico_nodes,
                "icosphere_max_defect": ico_defect,
                "product_max_defect": product_defect,
                "defect_ratio_product_over_icosphere": product_defect / ico_defect,
                "icosphere_max_rate": ico_rate,
                "product_max_rate": product_rate,
                "rate_ratio_product_over_icosphere": product_rate / ico_rate,
            }
        )

    fitted = [row for row in rows if int(row["level"]) >= 2]
    resolutions = [2.0 ** int(row["level"]) for row in fitted]
    ratio_slope = regression_slope(
        resolutions,
        [float(row["rate_ratio_product_over_icosphere"]) for row in fitted],
    )
    if not 1.8 <= ratio_slope <= 2.2:
        raise AssertionError(f"unexpected rate-ratio slope: {ratio_slope:.8f}")

    for row in fitted:
        node_ratio = float(row["node_ratio"])
        defect_ratio = float(row["defect_ratio_product_over_icosphere"])
        rate_ratio = float(row["rate_ratio_product_over_icosphere"])
        if not 0.8 <= node_ratio <= 1.25:
            raise AssertionError("node-matched comparison is not sufficiently close")
        if not 0.75 <= defect_ratio <= 1.5:
            raise AssertionError("defect comparison left the expected matched range")
        if int(row["level"]) >= 3 and rate_ratio <= 20.0:
            raise AssertionError("quasi-uniform rate advantage is unexpectedly small")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "product_vs_icosphere_comparison.csv"
    md_path = args.output_dir / "product_vs_icosphere_comparison.md"
    fieldnames = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Node-matched Gate 3 versus Gate 4 comparison",
        "",
        "The square equal-angle grid uses `P=2N^2` directions. For each",
        "icosphere level, the nearest product-grid order by node count is used.",
        "",
        f"The fitted growth slope of the product/icosphere rate ratio versus "
        f"`2^level` is `{ratio_slope:.8f}`. A slope near 2 is consistent with",
        "the product-grid rate being quadratic in direction count while the",
        "quasi-uniform rate is linear in direction count.",
        "",
        "| level | ico nodes | product nodes | product/ico defect | product/ico rate |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['level']} | {row['icosphere_nodes']} | {row['product_nodes']} | "
            f"{float(row['defect_ratio_product_over_icosphere']):.6f} | "
            f"{float(row['rate_ratio_product_over_icosphere']):.6f} |"
        )
    lines.extend(
        [
            "",
            "At the finest audited level, the two grids have similar maximum",
            "degree-two defects, while the equal-angle maximum rate is hundreds",
            "of times larger.",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"node-matched rate-ratio slope={ratio_slope:.8f}")
    print("Gate 4 product-versus-icosphere comparison: PASS")


if __name__ == "__main__":
    main()
