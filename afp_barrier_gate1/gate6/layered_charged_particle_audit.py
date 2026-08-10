#!/usr/bin/env python3
"""Gate 6 layered charged-particle slowing-down and angular-diffusion audit.

A particle crosses two homogeneous layers.  In each layer,

    dE/ds = -S,
    D(E) = c / E^2,

so the exact angular diffusion depth is

    A = c*x / (E_in * (E_in - S*x)).

The final energy is independent of layer order, but the angular depth generally
is not because the second layer is entered at lower energy.  The benchmark
checks the exact layer-order identity and evolves a positive mixture of
Legendre modes through both orders.

The quasi-uniform and equal-angle AFP operators are compared at matched node
counts using exact semidiscrete evolution and positivity-limited forward Euler.
No random sampling is used.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Sequence

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE / "angular_diffusion_transport_audit.py"
spec = importlib.util.spec_from_file_location("gate6_diffusion", BASE)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load Gate 6 angular-diffusion implementation")
g6 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g6
spec.loader.exec_module(g6)


class Layer(NamedTuple):
    name: str
    stopping: float
    coefficient: float
    thickness: float


@dataclass
class AuditRow:
    level: int
    family: str
    directions: int
    order: str
    final_energy: float
    angular_depth: float
    exact_semigroup_error_max: float
    euler_error_max: float
    orientation_spread: float
    euler_steps: int
    positive_depth_step: float
    mass_error: float
    minimum_solution: float
    order_response_difference: float


def layer_depth(layer: Layer, energy: float) -> tuple[float, float]:
    output = energy - layer.stopping * layer.thickness
    if energy <= 0.0 or output <= 0.0:
        raise ValueError("layer exhausts or reverses the particle energy")
    depth = (
        layer.coefficient * layer.thickness
        / (energy * output)
    )
    reciprocal = (
        layer.coefficient / layer.stopping
        * (1.0 / output - 1.0 / energy)
    )
    if abs(depth - reciprocal) > 5.0e-14 * max(1.0, abs(depth)):
        raise AssertionError("one-layer angular-depth identity failed")
    return output, depth


def traverse(layers: Sequence[Layer], initial_energy: float) -> tuple[float, float]:
    energy = initial_energy
    depth = 0.0
    for layer in layers:
        energy, increment = layer_depth(layer, energy)
        depth += increment
    return energy, depth


def exact_order_difference(
    energy: float, layer1: Layer, layer2: Layer
) -> float:
    a1 = layer1.coefficient * layer1.thickness
    a2 = layer2.coefficient * layer2.thickness
    d1 = layer1.stopping * layer1.thickness
    d2 = layer2.stopping * layer2.thickness
    return (
        (a1 * d2 - a2 * d1) * (d1 + d2 - 2.0 * energy)
        / (energy * (energy - d1) * (energy - d2) * (energy - d1 - d2))
    )


def continuum_profiles(
    points: np.ndarray, axes: np.ndarray, depth: float
) -> np.ndarray:
    return g6.continuum_profiles(points, axes, depth)


def audit_operator_order(
    level: int,
    operator,
    order_name: str,
    depth: float,
    final_energy: float,
    axes: np.ndarray,
    response_difference: float,
) -> AuditRow:
    initial = g6.initial_profiles(operator.directions, axes)
    reference = continuum_profiles(operator.directions, axes, depth)
    initial_mass = g6.weighted_masses(operator.weights, initial)

    semidiscrete = g6.exact_semidiscrete_evolution(operator, initial, depth)
    exact_errors = g6.weighted_relative_errors(
        operator.weights, semidiscrete, reference
    )

    euler, steps, dt_limit = g6.explicit_euler_evolution(
        operator, initial, depth, 0.9
    )
    euler_errors = g6.weighted_relative_errors(operator.weights, euler, reference)
    mass_error = max(
        float(np.max(np.abs(g6.weighted_masses(operator.weights, semidiscrete) - initial_mass))),
        float(np.max(np.abs(g6.weighted_masses(operator.weights, euler) - initial_mass))),
    )
    minimum = min(float(np.min(semidiscrete)), float(np.min(euler)))
    residual = g6.coordinate_residual(operator)

    if mass_error > 3.0e-10:
        raise AssertionError(f"{operator.family}: mass error {mass_error}")
    if minimum < -3.0e-10:
        raise AssertionError(f"{operator.family}: positivity failure {minimum}")
    if residual > 3.0e-8:
        raise AssertionError(f"{operator.family}: degree-one residual {residual}")

    return AuditRow(
        level=level,
        family=operator.family,
        directions=len(operator.directions),
        order=order_name,
        final_energy=final_energy,
        angular_depth=depth,
        exact_semigroup_error_max=float(np.max(exact_errors)),
        euler_error_max=float(np.max(euler_errors)),
        orientation_spread=float(np.max(exact_errors) - np.min(exact_errors)),
        euler_steps=steps,
        positive_depth_step=dt_limit,
        mass_error=mass_error,
        minimum_solution=minimum,
        order_response_difference=response_difference,
    )


def weighted_relative_difference(
    weights: np.ndarray, first: np.ndarray, second: np.ndarray
) -> float:
    numerator = np.sum(weights[:, None] * (first - second) ** 2, axis=0)
    denominator = np.sum(weights[:, None] * second**2, axis=0)
    return float(np.max(np.sqrt(numerator / denominator)))


def write_outputs(rows: Sequence[AuditRow], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "layered_charged_particle_audit.csv"
    md_path = output_dir / "layered_charged_particle_audit.md"
    fields = list(AuditRow.__dataclass_fields__)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Gate 6 layered charged-particle audit",
        "",
        "The two layer orders have identical final energy but different integrated angular diffusion.",
        "",
        "| level | family | K | order | final energy | angular depth | exact error | Euler error | Euler steps | order-response difference |",
        "|---:|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.order} | "
            f"{row.final_energy:.8f} | {row.angular_depth:.8e} | "
            f"{row.exact_semigroup_error_max:.8e} | {row.euler_error_max:.8e} | "
            f"{row.euler_steps} | {row.order_response_difference:.8e} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--initial-energy", type=float, default=5.0)
    parser.add_argument("--output-dir", type=Path, default=Path("gate6/generated"))
    args = parser.parse_args()
    if not 1 <= args.max_level <= 3:
        raise SystemExit("--max-level must be between 1 and 3")

    # Layer A has the larger c/S ratio.  The exact order theorem predicts that
    # A followed by B has the smaller angular depth.
    layer_a = Layer("A", stopping=1.0, coefficient=4.0, thickness=1.0)
    layer_b = Layer("B", stopping=0.5, coefficient=0.4, thickness=1.0)
    energy_ab, depth_ab = traverse((layer_a, layer_b), args.initial_energy)
    energy_ba, depth_ba = traverse((layer_b, layer_a), args.initial_energy)
    if abs(energy_ab - energy_ba) > 2.0e-14:
        raise AssertionError("final energy depends on layer order")
    predicted_difference = exact_order_difference(
        args.initial_energy, layer_a, layer_b
    )
    if abs((depth_ab - depth_ba) - predicted_difference) > 2.0e-14:
        raise AssertionError("two-layer order-difference identity failed")
    if not depth_ab < depth_ba:
        raise AssertionError("expected high-c/S layer first to reduce angular depth")

    axes = g6.orientations()
    rows: list[AuditRow] = []
    for level in range(1, args.max_level + 1):
        operators = [
            g6.build_icosphere(level),
            g6.build_product(g6.nearest_product_n(10 * 4**level + 2)),
        ]
        for operator in operators:
            reference_ab = continuum_profiles(operator.directions, axes, depth_ab)
            reference_ba = continuum_profiles(operator.directions, axes, depth_ba)
            response_difference = weighted_relative_difference(
                operator.weights, reference_ab, reference_ba
            )
            row_ab = audit_operator_order(
                level, operator, "A->B", depth_ab, energy_ab, axes,
                response_difference,
            )
            row_ba = audit_operator_order(
                level, operator, "B->A", depth_ba, energy_ba, axes,
                response_difference,
            )
            rows.extend((row_ab, row_ba))
            print(
                f"level={level} family={operator.family} K={row_ab.directions} "
                f"Eout={energy_ab:.6f} depths={depth_ab:.6e}/{depth_ba:.6e} "
                f"errors={row_ab.exact_semigroup_error_max:.3e}/"
                f"{row_ba.exact_semigroup_error_max:.3e} "
                f"steps={row_ab.euler_steps}/{row_ba.euler_steps}"
            )

    finest = [row for row in rows if row.level == args.max_level]
    ico = [row for row in finest if row.family.startswith("icosphere")]
    product = [row for row in finest if row.family.startswith("product")]
    if max(row.exact_semigroup_error_max for row in ico) >= max(
        row.exact_semigroup_error_max for row in product
    ):
        raise AssertionError("quasi-uniform layered-transport error was not lower")
    if max(row.euler_steps for row in product) / max(row.euler_steps for row in ico) < 20.0:
        raise AssertionError("layered product-grid explicit-step penalty is too small")
    if rows[0].order_response_difference <= 1.0e-3:
        raise AssertionError("layer-order response difference is too small to resolve")

    write_outputs(rows, args.output_dir)
    print("Gate 6 layered charged-particle audit: PASS")


if __name__ == "__main__":
    main()
