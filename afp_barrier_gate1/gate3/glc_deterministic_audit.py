#!/usr/bin/env python3
"""Deterministic Gate 3 audit for Radiant's GLC AFP tensor-product stencil.

The script reconstructs the unshifted stencil directly from the equations in
Radiant, without calling Radiant. It checks exact algebraic identities to
floating-point tolerance and measures the defect/stiffness asymptotics.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.special import jn_zeros, roots_legendre


@dataclass(frozen=True)
class AuditRow:
    order: int
    min_beta: float
    min_K: float
    max_K: float
    coordinate_residual: float
    K_identity_residual: float
    defect_identity_residual: float
    min_rate_times_defect: float
    max_defect: float
    scaled_max_defect_N2: float
    outer_rate: float
    scaled_outer_rate_N4: float
    outer_K: float
    outer_K_error: float
    outer_rate_constant_error: float


def glc_coefficients(order: int) -> dict[str, np.ndarray | float]:
    if order < 2:
        raise ValueError("order must be at least 2")

    mu, weight = roots_legendre(order)
    rho = np.sqrt(np.maximum(0.0, 1.0 - mu * mu))

    beta = np.zeros(order + 1)
    for k in range(1, order):
        beta[k] = beta[k - 1] - 2.0 * weight[k - 1] * mu[k - 1]

    slope = np.zeros(order + 1)
    for k in range(1, order):
        slope[k] = (rho[k] - rho[k - 1]) / (mu[k] - mu[k - 1])

    c = np.empty(order)
    for n in range(order):
        c[n] = (beta[n + 1] * slope[n + 1] - beta[n] * slope[n]) / weight[n]

    K = 2.0 * rho * rho + rho * c
    h = math.pi / order
    one_minus_cos_h = 1.0 - math.cos(h)
    gamma = h * h * K / (2.0 * one_minus_cos_h)
    azimuth_rate = K / (2.0 * rho * rho * one_minus_cos_h)

    a_minus = np.zeros(order)
    a_plus = np.zeros(order)
    for n in range(order):
        if n > 0:
            a_minus[n] = beta[n] / (weight[n] * (mu[n] - mu[n - 1]))
        if n + 1 < order:
            a_plus[n] = beta[n + 1] / (weight[n] * (mu[n + 1] - mu[n]))

    return {
        "mu": mu,
        "weight": weight,
        "rho": rho,
        "beta": beta,
        "slope": slope,
        "c": c,
        "K": K,
        "h": h,
        "one_minus_cos_h": one_minus_cos_h,
        "gamma": gamma,
        "azimuth_rate": azimuth_rate,
        "a_minus": a_minus,
        "a_plus": a_plus,
    }


def audit_order(order: int, j1: float, j2: float) -> AuditRow:
    p = glc_coefficients(order)
    mu = np.asarray(p["mu"])
    rho = np.asarray(p["rho"])
    beta = np.asarray(p["beta"])
    c = np.asarray(p["c"])
    K = np.asarray(p["K"])
    a_minus = np.asarray(p["a_minus"])
    a_plus = np.asarray(p["a_plus"])
    q = np.asarray(p["azimuth_rate"])
    dphi_base = float(p["one_minus_cos_h"])

    z_residual = np.max(np.abs(
        a_minus * np.r_[0.0, mu[:-1] - mu[1:]]
        + a_plus * np.r_[mu[1:] - mu[:-1], 0.0]
        + 2.0 * mu
    ))
    transverse_residual = np.max(np.abs(c - K / rho + 2.0 * rho))
    coordinate_residual = float(max(z_residual, transverse_residual))

    loss = np.zeros(order)
    d_minus = np.zeros(order)
    d_plus = np.zeros(order)
    for n in range(order):
        if n > 0:
            dot = mu[n] * mu[n - 1] + rho[n] * rho[n - 1]
            d_minus[n] = 1.0 - dot
            loss[n] += a_minus[n] * d_minus[n]
        if n + 1 < order:
            dot = mu[n] * mu[n + 1] + rho[n] * rho[n + 1]
            d_plus[n] = 1.0 - dot
            loss[n] += a_plus[n] * d_plus[n]
    K_identity_residual = float(np.max(np.abs(K - (2.0 - loss))))

    d_phi = rho * rho * dphi_base
    defect_direct = (
        a_minus * d_minus * d_minus
        + a_plus * d_plus * d_plus
        + 2.0 * q * d_phi * d_phi
    )
    defect_reduced = (
        a_minus * d_minus * d_minus
        + a_plus * d_plus * d_plus
        + K * rho * rho * dphi_base
    )
    defect_identity_residual = float(np.max(np.abs(defect_direct - defect_reduced)))

    row_rate = a_minus + a_plus + 2.0 * q
    rate_times_defect = row_rate * defect_direct

    outer_K_formula = (
        2.0 * rho[0] ** 2
        - 2.0 * mu[0] * rho[0] * (rho[1] - rho[0]) / (mu[1] - mu[0])
    )
    if abs(outer_K_formula - K[0]) > 5e-11:
        raise AssertionError("outer K algebraic identity failed")

    K_star = 4.0 * j1 / (j1 + j2)
    rate_constant = 2.0 * K_star / (math.pi**2 * j1**2)

    interior_beta = beta[1:order]
    return AuditRow(
        order=order,
        min_beta=float(np.min(interior_beta)),
        min_K=float(np.min(K)),
        max_K=float(np.max(K)),
        coordinate_residual=coordinate_residual,
        K_identity_residual=K_identity_residual,
        defect_identity_residual=defect_identity_residual,
        min_rate_times_defect=float(np.min(rate_times_defect)),
        max_defect=float(np.max(defect_direct)),
        scaled_max_defect_N2=float(order**2 * np.max(defect_direct)),
        outer_rate=float(row_rate[0]),
        scaled_outer_rate_N4=float(row_rate[0] / order**4),
        outer_K=float(K[0]),
        outer_K_error=float(abs(K[0] - K_star)),
        outer_rate_constant_error=float(abs(row_rate[0] / order**4 - rate_constant)),
    )


def log_slope(xs: Iterable[float], ys: Iterable[float]) -> float:
    x = np.log(np.asarray(list(xs), dtype=float))
    y = np.log(np.asarray(list(ys), dtype=float))
    return float(np.polyfit(x, y, 1)[0])


def write_csv(rows: list[AuditRow], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_report(rows: list[AuditRow], path: Path, defect_slope: float,
                 rate_slope: float, j1: float, j2: float) -> None:
    K_star = 4.0 * j1 / (j1 + j2)
    rate_constant = 2.0 * K_star / (math.pi**2 * j1**2)
    with path.open("w", encoding="utf-8") as out:
        out.write("# Gate 3 deterministic GLC AFP audit\n\n")
        out.write("The audit reconstructs Radiant's unshifted product-quadrature stencil independently.\n\n")
        out.write(f"- First two zeros of J0: `{j1:.15g}`, `{j2:.15g}`\n")
        out.write(f"- Predicted outer-ring K limit: `{K_star:.15g}`\n")
        out.write(f"- Predicted outer-row N^4 constant: `{rate_constant:.15g}`\n")
        out.write(f"- Fitted max-defect exponent: `{defect_slope:.8f}`\n")
        out.write(f"- Fitted outer-rate exponent: `{rate_slope:.8f}`\n\n")
        out.write("| N | min beta | min K | max K | coord residual | K identity | defect identity | min(rate*defect) | N^2 max defect | outer K | outer rate/N^4 |\n")
        out.write("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for r in rows:
            out.write(
                f"| {r.order} | {r.min_beta:.3e} | {r.min_K:.9f} | {r.max_K:.9f} | "
                f"{r.coordinate_residual:.3e} | {r.K_identity_residual:.3e} | "
                f"{r.defect_identity_residual:.3e} | {r.min_rate_times_defect:.9f} | "
                f"{r.scaled_max_defect_N2:.9f} | {r.outer_K:.9f} | "
                f"{r.scaled_outer_rate_N4:.9f} |\n"
            )
        out.write("\n## Interpretation\n\n")
        out.write("- Every tested latitude interface coefficient and azimuth correction is positive.\n")
        out.write("- The three Cartesian coordinate modes have eigenvalue -2 to roundoff.\n")
        out.write("- The exact K and peak-defect identities hold to roundoff.\n")
        out.write("- The generic sharp inequality `rate * defect >= 4` holds at every row.\n")
        out.write("- The maximum defect approaches `pi^2/N^2`.\n")
        out.write("- The outer polar row rate grows as `N^4`, with the Bessel-zero constant shown above.\n")
        out.write("\nThe finite audit is evidence, not a replacement for the analytic all-orders proof.\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("gate3-output"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    orders = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64,
              96, 128, 192, 256, 384, 512]
    j1, j2 = map(float, jn_zeros(0, 2))
    rows = [audit_order(n, j1, j2) for n in orders]

    for row in rows:
        if not row.min_beta > 0.0:
            raise AssertionError(f"nonpositive beta at N={row.order}")
        if not row.min_K > 0.0:
            raise AssertionError(f"nonpositive K at N={row.order}")
        if row.coordinate_residual > 2e-9:
            raise AssertionError(f"coordinate residual at N={row.order}: {row.coordinate_residual}")
        if row.K_identity_residual > 2e-9:
            raise AssertionError(f"K identity residual at N={row.order}: {row.K_identity_residual}")
        if row.defect_identity_residual > 2e-9:
            raise AssertionError(f"defect identity residual at N={row.order}: {row.defect_identity_residual}")
        if row.min_rate_times_defect < 4.0 - 2e-8:
            raise AssertionError(f"defect-stiffness inequality at N={row.order}")

    tail = [r for r in rows if r.order >= 32]
    defect_slope = log_slope((r.order for r in tail), (r.max_defect for r in tail))
    rate_slope = log_slope((r.order for r in tail), (r.outer_rate for r in tail))

    if not (-2.05 < defect_slope < -1.90):
        raise AssertionError(f"unexpected defect exponent {defect_slope}")
    if not (3.90 < rate_slope < 4.10):
        raise AssertionError(f"unexpected polar-rate exponent {rate_slope}")

    final = rows[-1]
    if abs(final.scaled_max_defect_N2 - math.pi**2) > 0.08:
        raise AssertionError("N^2 max defect has not approached pi^2 as expected")
    if final.outer_K_error > 5e-4:
        raise AssertionError("outer K has not approached the Bessel-zero limit")
    rate_constant = 2.0 * (4.0 * j1 / (j1 + j2)) / (math.pi**2 * j1**2)
    if abs(final.scaled_outer_rate_N4 - rate_constant) > 5e-4:
        raise AssertionError("outer N^4 stiffness constant mismatch")

    write_csv(rows, args.output_dir / "glc_audit.csv")
    write_report(rows, args.output_dir / "glc_audit.md", defect_slope, rate_slope, j1, j2)
    print((args.output_dir / "glc_audit.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
