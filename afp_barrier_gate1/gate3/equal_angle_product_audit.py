#!/usr/bin/env python3
"""Deterministic audit for the equal-angle product AFP construction.

The script uses only the Python standard library and no random sampling.  It
checks every node for a collection of square and non-square product grids:

* positive cell weights and every actual edge conductance;
* exact zero conductance on the two omitted polar meridional edges;
* total quadrature area and weighted centering;
* exact degree-one coordinate eigenrelations;
* exact degree-two peak-defect and jump-rate formulas;
* exact polar maximum-rate formula for the square family;
* the proved finite-order inequalities

      2/N^2 <= max defect <= pi^2/N^2,
      (8/pi^4) N^4 <= max rate <= N^4.

Log--log slopes are reported only as diagnostics.  They are not used as a
substitute for the Lean-verified finite-order bounds.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


SQUARE_ORDERS: tuple[int, ...] = (2, 3, 4, 5, 8, 16, 32, 64, 128)
FIT_ORDERS: tuple[int, ...] = (8, 16, 32, 64, 128)
EXTRA_CASES: tuple[tuple[int, int], ...] = (
    (2, 3),
    (3, 4),
    (3, 7),
    (4, 5),
    (5, 11),
    (7, 9),
    (8, 13),
)
DEFAULT_CASES: tuple[tuple[int, int], ...] = tuple(
    dict.fromkeys(tuple((n, 2 * n) for n in SQUARE_ORDERS) + EXTRA_CASES)
)


@dataclass(frozen=True)
class AuditRow:
    N: int
    M: int
    total_weight_error: float
    weighted_center_error: float
    coordinate_residual: float
    defect_identity_error: float
    rate_identity_relative_error: float
    boundary_zero_error: float
    min_positive_quantity: float
    max_peak_defect: float
    max_jump_rate: float
    polar_rate_relative_error: float
    defect_lower_margin: float
    defect_upper_margin: float
    rate_lower_margin: float
    rate_upper_margin: float


def _linear_regression_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    denominator = sum((x - mx) ** 2 for x in lx)
    if denominator == 0.0:
        raise ValueError("regression requires distinct x values")
    return sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / denominator


def audit_case(N: int, M: int) -> AuditRow:
    if N < 2:
        raise ValueError("N must be at least 2")
    if M < 3:
        raise ValueError("M must be at least 3")

    delta = math.pi / N
    alpha = 2.0 * math.pi / M
    sin_half_delta = math.sin(delta / 2.0)
    one_minus_cos_alpha = 1.0 - math.cos(alpha)
    one_minus_cos_delta = 1.0 - math.cos(delta)

    total_weight = 0.0
    center_x = 0.0
    center_y = 0.0
    center_z = 0.0
    max_coordinate_residual = 0.0
    max_defect_identity_error = 0.0
    max_rate_relative_error = 0.0
    max_boundary_zero_error = 0.0
    min_positive_quantity = math.inf
    max_peak_defect = 0.0
    max_jump_rate = 0.0

    for i in range(N):
        theta = (i + 0.5) * delta
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)

        weight = 2.0 * alpha * sin_theta * sin_half_delta
        b_minus = (
            0.0
            if i == 0
            else alpha * math.sin(i * delta) / math.sin(delta)
        )
        b_plus = (
            0.0
            if i == N - 1
            else alpha * math.sin((i + 1) * delta) / math.sin(delta)
        )
        c_azimuth = (
            alpha * sin_half_delta / (one_minus_cos_alpha * sin_theta)
        )

        max_boundary_zero_error = max(
            max_boundary_zero_error,
            abs(b_minus) if i == 0 else 0.0,
            abs(b_plus) if i == N - 1 else 0.0,
        )

        positive_values = [weight, c_azimuth]
        if i > 0:
            positive_values.append(b_minus)
        if i < N - 1:
            positive_values.append(b_plus)
        min_positive_quantity = min(min_positive_quantity, *positive_values)

        theta_minus = theta - delta
        theta_plus = theta + delta
        x_minus = math.cos(theta_minus) if i > 0 else cos_theta
        x_plus = math.cos(theta_plus) if i < N - 1 else cos_theta
        s_minus = math.sin(theta_minus) if i > 0 else sin_theta
        s_plus = math.sin(theta_plus) if i < N - 1 else sin_theta

        def local_action(
            f0: float,
            f_minus: float,
            f_plus: float,
            f_left: float,
            f_right: float,
        ) -> float:
            numerator = (
                b_minus * (f_minus - f0)
                + b_plus * (f_plus - f0)
                + c_azimuth * (f_left - f0)
                + c_azimuth * (f_right - f0)
            )
            return numerator / weight

        for j in range(M):
            phi = j * alpha
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            x = cos_theta
            y = sin_theta * cos_phi
            z = sin_theta * sin_phi

            y_minus = s_minus * cos_phi
            y_plus = s_plus * cos_phi
            z_minus = s_minus * sin_phi
            z_plus = s_plus * sin_phi
            y_left = sin_theta * math.cos(phi - alpha)
            y_right = sin_theta * math.cos(phi + alpha)
            z_left = sin_theta * math.sin(phi - alpha)
            z_right = sin_theta * math.sin(phi + alpha)

            Lx = local_action(x, x_minus, x_plus, x, x)
            Ly = local_action(y, y_minus, y_plus, y_left, y_right)
            Lz = local_action(z, z_minus, z_plus, z_left, z_right)
            max_coordinate_residual = max(
                max_coordinate_residual,
                abs(Lx + 2.0 * x),
                abs(Ly + 2.0 * y),
                abs(Lz + 2.0 * z),
            )

            total_weight += weight
            center_x += weight * x
            center_y += weight * y
            center_z += weight * z

        meridional_dot_loss = one_minus_cos_delta
        azimuthal_dot_loss = sin_theta**2 * one_minus_cos_alpha
        direct_defect = (
            (b_minus + b_plus) * meridional_dot_loss**2
            + 2.0 * c_azimuth * azimuthal_dot_loss**2
        ) / weight
        formula_defect = meridional_dot_loss + azimuthal_dot_loss
        max_defect_identity_error = max(
            max_defect_identity_error,
            abs(direct_defect - formula_defect),
        )
        max_peak_defect = max(max_peak_defect, direct_defect)

        direct_rate = (b_minus + b_plus + 2.0 * c_azimuth) / weight
        formula_rate = (
            1.0 / one_minus_cos_delta
            + 1.0 / (one_minus_cos_alpha * sin_theta**2)
        )
        rate_relative_error = abs(direct_rate - formula_rate) / max(
            1.0, abs(formula_rate)
        )
        max_rate_relative_error = max(
            max_rate_relative_error, rate_relative_error
        )
        max_jump_rate = max(max_jump_rate, direct_rate)

    if M == 2 * N:
        expected_polar_rate = (
            1.0 / (2.0 * sin_half_delta**2)
            + 1.0 / (2.0 * sin_half_delta**4)
        )
        polar_rate_relative_error = abs(max_jump_rate - expected_polar_rate) / max(
            1.0, abs(expected_polar_rate)
        )
        defect_lower_margin = max_peak_defect - 2.0 / N**2
        defect_upper_margin = math.pi**2 / N**2 - max_peak_defect
        rate_lower_margin = max_jump_rate - 8.0 * N**4 / math.pi**4
        rate_upper_margin = N**4 - max_jump_rate
    else:
        polar_rate_relative_error = 0.0
        defect_lower_margin = math.nan
        defect_upper_margin = math.nan
        rate_lower_margin = math.nan
        rate_upper_margin = math.nan

    return AuditRow(
        N=N,
        M=M,
        total_weight_error=abs(total_weight - 4.0 * math.pi),
        weighted_center_error=max(abs(center_x), abs(center_y), abs(center_z)),
        coordinate_residual=max_coordinate_residual,
        defect_identity_error=max_defect_identity_error,
        rate_identity_relative_error=max_rate_relative_error,
        boundary_zero_error=max_boundary_zero_error,
        min_positive_quantity=min_positive_quantity,
        max_peak_defect=max_peak_defect,
        max_jump_rate=max_jump_rate,
        polar_rate_relative_error=polar_rate_relative_error,
        defect_lower_margin=defect_lower_margin,
        defect_upper_margin=defect_upper_margin,
        rate_lower_margin=rate_lower_margin,
        rate_upper_margin=rate_upper_margin,
    )


def assert_audit(rows: Sequence[AuditRow]) -> tuple[float, float]:
    for row in rows:
        # Floating-point cancellation grows near polar rings because the exact
        # generator has O(N^4) coefficients.  These tolerances remain far below
        # the O(1) coordinate eigenvalues.
        if row.total_weight_error > 3.0e-11:
            raise AssertionError(f"quadrature weight failure: {row}")
        if row.weighted_center_error > 3.0e-11:
            raise AssertionError(f"centering failure: {row}")
        if row.coordinate_residual > 2.0e-8:
            raise AssertionError(f"degree-one exactness failure: {row}")
        if row.defect_identity_error > 3.0e-13:
            raise AssertionError(f"defect identity failure: {row}")
        if row.rate_identity_relative_error > 3.0e-13:
            raise AssertionError(f"rate identity failure: {row}")
        if row.boundary_zero_error > 1.0e-15:
            raise AssertionError(f"boundary conductance failure: {row}")
        if row.polar_rate_relative_error > 3.0e-13:
            raise AssertionError(f"polar rate failure: {row}")
        if not row.min_positive_quantity > 0.0:
            raise AssertionError(f"nonpositive actual coefficient: {row}")

        if row.M == 2 * row.N:
            scale_defect = max(1.0, math.pi**2 / row.N**2)
            scale_rate = max(1.0, row.N**4)
            if row.defect_lower_margin < -2.0e-13 * scale_defect:
                raise AssertionError(f"defect lower bound failure: {row}")
            if row.defect_upper_margin < -2.0e-13 * scale_defect:
                raise AssertionError(f"defect upper bound failure: {row}")
            if row.rate_lower_margin < -2.0e-13 * scale_rate:
                raise AssertionError(f"rate lower bound failure: {row}")
            if row.rate_upper_margin < -2.0e-13 * scale_rate:
                raise AssertionError(f"rate upper bound failure: {row}")

    square = {row.N: row for row in rows if row.M == 2 * row.N}
    fit = {n: square[n] for n in FIT_ORDERS if n in square}
    if tuple(sorted(fit)) != FIT_ORDERS:
        raise AssertionError("all FIT_ORDERS must be audited")
    defect_slope = _linear_regression_slope(
        FIT_ORDERS, [fit[n].max_peak_defect for n in FIT_ORDERS]
    )
    rate_slope = _linear_regression_slope(
        FIT_ORDERS, [fit[n].max_jump_rate for n in FIT_ORDERS]
    )
    # These broad checks detect accidental formula changes.  The rigorous
    # exponent claims come from the finite-order inequalities above and Lean.
    if not (-2.05 < defect_slope < -1.90):
        raise AssertionError(f"unexpected defect diagnostic slope {defect_slope}")
    if not (3.85 < rate_slope < 4.10):
        raise AssertionError(f"unexpected stiffness diagnostic slope {rate_slope}")
    return defect_slope, rate_slope


def write_outputs(
    rows: Sequence[AuditRow],
    defect_slope: float,
    rate_slope: float,
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "equal_angle_product_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: value if isinstance(value, int) else f"{value:.16e}"
                    for key, value in asdict(row).items()
                }
            )

    md_path = output_dir / "equal_angle_product_audit.md"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Equal-angle product AFP deterministic audit\n\n")
        handle.write(
            "All square and non-square cases passed positivity, polar-boundary, "
            "centering, degree-one exactness, defect-identity, and rate-identity "
            "checks. Square cases also passed the Lean-proved finite-order "
            "defect and polar-rate inequalities.\n\n"
        )
        handle.write(
            f"- diagnostic maximum-defect slope: `{defect_slope:.8f}`\n"
        )
        handle.write(f"- diagnostic maximum-rate slope: `{rate_slope:.8f}`\n\n")
        handle.write(
            "| N | M | coordinate residual | max defect | max rate | "
            "min positive coefficient |\n"
            "|---:|---:|---:|---:|---:|---:|\n"
        )
        for row in rows:
            handle.write(
                f"| {row.N} | {row.M} | {row.coordinate_residual:.3e} | "
                f"{row.max_peak_defect:.6e} | {row.max_jump_rate:.6e} | "
                f"{row.min_positive_quantity:.6e} |\n"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("gate3/generated"),
        help="directory for deterministic CSV and Markdown records",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [audit_case(N, M) for N, M in DEFAULT_CASES]
    defect_slope, rate_slope = assert_audit(rows)
    write_outputs(rows, defect_slope, rate_slope, args.output_dir)
    print(
        "PASS equal-angle product audit: "
        f"cases={len(rows)}, defect diagnostic slope={defect_slope:.8f}, "
        f"rate diagnostic slope={rate_slope:.8f}"
    )


if __name__ == "__main__":
    main()
