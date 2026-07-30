#!/usr/bin/env python3
"""Deterministic audit of the odd-order equatorial GLC ring.

For odd Gauss--Legendre order the central node is exactly zero. This script
checks the exact central-ring formulas and their predicted asymptotic limits:

    B_N -> 1,
    a_N (N+1/2) -> pi,
    w_0 (N+1/2) / pi -> 1,
    A_N / N^2 -> 1/pi^2,
    N^2 d_N -> pi^2/2,
    K_N -> 1,
    N^2 epsilon_N -> pi^2,
    R_N / N^2 -> 4/pi^2,
    R_N epsilon_N -> 4.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.special import roots_legendre


@dataclass(frozen=True)
class CentralRow:
    order: int
    beta_center: float
    adjacent_root_times_kappa: float
    central_weight_times_kappa_over_pi: float
    latitude_rate_over_N2: float
    N2_latitude_deficit: float
    K_center: float
    N2_defect: float
    rate_over_N2: float
    rate_times_defect: float
    exact_formula_residual: float


def audit(order: int) -> CentralRow:
    if order < 3 or order % 2 == 0:
        raise ValueError("order must be odd and at least 3")

    mu, weight = roots_legendre(order)
    center = order // 2
    if abs(mu[center]) > 5e-15:
        raise AssertionError("central Gauss--Legendre root is not zero")

    beta = np.zeros(order + 1)
    for k in range(1, order):
        beta[k] = beta[k - 1] - 2.0 * weight[k - 1] * mu[k - 1]

    adjacent = mu[center + 1]
    radius = math.sqrt(1.0 - adjacent * adjacent)
    d_lat = 1.0 - radius
    beta_center = beta[center + 1]
    latitude_rate = beta_center / (weight[center] * adjacent)
    K_center = 2.0 - 2.0 * latitude_rate * d_lat
    d_phi = 1.0 - math.cos(math.pi / order)
    defect = 2.0 * latitude_rate * d_lat * d_lat + K_center * d_phi
    rate = 2.0 * latitude_rate + K_center / d_phi

    beta_from_abs_quadrature = float(np.dot(weight, np.abs(mu)))
    exact_formula_residual = max(
        abs(beta_center - beta_from_abs_quadrature),
        abs(K_center - (2.0 - 2.0 * latitude_rate * d_lat)),
        abs(defect - (2.0 * latitude_rate * d_lat**2 + K_center * d_phi)),
        abs(rate - (2.0 * latitude_rate + K_center / d_phi)),
    )

    kappa = order + 0.5
    return CentralRow(
        order=order,
        beta_center=beta_center,
        adjacent_root_times_kappa=adjacent * kappa,
        central_weight_times_kappa_over_pi=weight[center] * kappa / math.pi,
        latitude_rate_over_N2=latitude_rate / order**2,
        N2_latitude_deficit=order**2 * d_lat,
        K_center=K_center,
        N2_defect=order**2 * defect,
        rate_over_N2=rate / order**2,
        rate_times_defect=rate * defect,
        exact_formula_residual=exact_formula_residual,
    )


def slope(rows: list[CentralRow], attr: str, subtract_limit: float | None = None) -> float:
    x = np.log(np.asarray([r.order for r in rows], dtype=float))
    values = np.asarray([getattr(r, attr) for r in rows], dtype=float)
    if subtract_limit is not None:
        values = np.abs(values - subtract_limit)
    return float(np.polyfit(x, np.log(values), 1)[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("gate3-central-output"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    orders = [3, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 511]
    rows = [audit(n) for n in orders]

    for row in rows:
        if row.exact_formula_residual > 2e-12:
            raise AssertionError(f"exact central identity failed at N={row.order}")
        if row.K_center <= 0.0:
            raise AssertionError(f"nonpositive central K at N={row.order}")
        if row.rate_times_defect < 4.0 - 2e-10:
            raise AssertionError(f"sharp inequality failed at N={row.order}")

    final = rows[-1]
    targets = {
        "beta_center": 1.0,
        "adjacent_root_times_kappa": math.pi,
        "central_weight_times_kappa_over_pi": 1.0,
        "latitude_rate_over_N2": 1.0 / math.pi**2,
        "N2_latitude_deficit": math.pi**2 / 2.0,
        "K_center": 1.0,
        "N2_defect": math.pi**2,
        "rate_over_N2": 4.0 / math.pi**2,
        "rate_times_defect": 4.0,
    }
    tolerances = {
        "beta_center": 3e-3,
        "adjacent_root_times_kappa": 3e-5,
        "central_weight_times_kappa_over_pi": 3e-5,
        "latitude_rate_over_N2": 3e-4,
        "N2_latitude_deficit": 2e-2,
        "K_center": 2e-5,
        "N2_defect": 2e-2,
        "rate_over_N2": 8e-4,
        "rate_times_defect": 1e-4,
    }
    for name, target in targets.items():
        error = abs(getattr(final, name) - target)
        if error > tolerances[name]:
            raise AssertionError(f"{name} limit mismatch: error={error}")

    csv_path = args.output_dir / "glc_central_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    report_path = args.output_dir / "glc_central_audit.md"
    with report_path.open("w", encoding="utf-8") as out:
        out.write("# Odd-order central-ring audit\n\n")
        out.write("Predicted limits:\n\n")
        for name, target in targets.items():
            out.write(f"- `{name}` -> `{target:.15g}`\n")
        out.write("\n| N | beta | a*kappa | w0*kappa/pi | A/N^2 | N^2 d | K | N^2 defect | R/N^2 | R*defect | residual |\n")
        out.write("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for r in rows:
            out.write(
                f"| {r.order} | {r.beta_center:.9f} | {r.adjacent_root_times_kappa:.9f} | "
                f"{r.central_weight_times_kappa_over_pi:.9f} | {r.latitude_rate_over_N2:.9f} | "
                f"{r.N2_latitude_deficit:.9f} | {r.K_center:.9f} | {r.N2_defect:.9f} | "
                f"{r.rate_over_N2:.9f} | {r.rate_times_defect:.9f} | "
                f"{r.exact_formula_residual:.3e} |\n"
            )
        tail = [r for r in rows if r.order >= 33]
        out.write("\nObserved convergence exponents for absolute errors on the tail:\n\n")
        for name, target in targets.items():
            out.write(f"- `{name}`: `{slope(tail, name, target):.6f}`\n")
        out.write("\nThe exact finite formulas are Lean-checked separately. This numerical audit checks the Gauss–Legendre inputs and their approach to the asymptotic constants.\n")

    print(report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
