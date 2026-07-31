#!/usr/bin/env python3
"""Gate 6 spatial slab transport audit.

This is the first benchmark in the project with spatial streaming, inflow and
vacuum boundaries, absorption, angular Fokker--Planck collisions, and a thin
material interface.  It has two deterministic parts:

1. A manufactured degree-one space--angle solution.  Because both angular
   families preserve the coordinate modes exactly, the measured convergence
   isolates the finite-volume streaming and time integration.
2. A three-layer beam problem with a thin, strongly absorbing and angularly
   diffusing functional layer.  A control replaces that layer with substrate
   material.  Conservative currents and regional absorption tallies quantify
   the layer response.

No random sampling is used.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gate6.core import (
    BoundaryData,
    CoordinateModeManufactured,
    Layer,
    Material,
    SlabGrid,
    SlabModel,
    assign_layers,
    build_icosphere,
    build_product,
    evaluate_tallies,
    region_absorption_rate,
)


@dataclass(frozen=True)
class ManufacturedRow:
    family: str
    directions: int
    cells: int
    steps: int
    relative_error: float
    minimum_solution: float
    max_balance_closure: float


@dataclass(frozen=True)
class InterfaceRow:
    level: int
    family: str
    directions: int
    case: str
    cells: int
    steps: int
    right_out: float
    left_out: float
    inventory: float
    total_absorption: float
    thin_region_absorption: float
    final_absorption_rate: float
    minimum_solution: float
    max_balance_error: float


def weighted_space_angle_error(
    model: SlabModel, approximation: np.ndarray, reference: np.ndarray
) -> float:
    weight = model.angular.weights[None, :]
    numerator = model.grid.dx * np.sum(weight * (approximation - reference) ** 2)
    denominator = model.grid.dx * np.sum(weight * reference**2)
    return float(np.sqrt(numerator / denominator))


def manufactured_audit() -> list[ManufacturedRow]:
    manufactured = CoordinateModeManufactured(
        0.0,
        1.0,
        amplitude=0.2,
        omega=0.7,
        absorption=0.15,
        angular_diffusion=0.25,
    )
    rows: list[ManufacturedRow] = []
    for operator in (build_icosphere(1), build_product(5)):
        family_errors: list[float] = []
        for cells in (20, 40, 80):
            grid = SlabGrid(0.0, 1.0, cells)
            model = SlabModel(
                grid,
                operator,
                np.full(cells, manufactured.absorption),
                np.full(cells, manufactured.angular_diffusion),
                manufactured.boundary(),
                manufactured.source(),
            )
            initial = manufactured.exact(0.0, grid.centers, operator.mu_x)
            final, diagnostics = model.advance(
                initial,
                0.05,
                cfl=0.7,
                integrator="ssprk2",
                dt_max=0.1 * grid.dx,
            )
            reference = manufactured.exact(0.05, grid.centers, operator.mu_x)
            error = weighted_space_angle_error(model, final, reference)
            family_errors.append(error)
            row = ManufacturedRow(
                family=operator.family,
                directions=operator.count,
                cells=cells,
                steps=len(diagnostics),
                relative_error=error,
                minimum_solution=float(np.min(final)),
                max_balance_closure=max(
                    abs(model.balance_rates(final, 0.05).closure_error),
                    max((abs(item.balance_error) for item in diagnostics), default=0.0),
                ),
            )
            rows.append(row)
            print(
                f"manufactured family={row.family} K={row.directions} "
                f"cells={cells} steps={row.steps} error={error:.6e}"
            )
        if not (family_errors[2] < family_errors[1] < family_errors[0]):
            raise AssertionError(f"{operator.family}: manufactured error did not decrease")
        if family_errors[2] > 0.65 * family_errors[1]:
            raise AssertionError(f"{operator.family}: finest spatial refinement was too weak")
    return rows


def beam_inflow(_time: float, mu: np.ndarray) -> np.ndarray:
    return np.where(mu > 0.0, np.exp(-((1.0 - mu) / 0.25) ** 2), 0.0)


def vacuum(_time: float, mu: np.ndarray) -> np.ndarray:
    return np.zeros_like(mu)


def make_interface_model(operator, *, film: bool, cells: int = 60):
    grid = SlabGrid(0.0, 1.0, cells)
    substrate = Material("substrate", absorption=0.08, angular_diffusion=0.05)
    functional = (
        Material("functional-film", absorption=0.70, angular_diffusion=0.50)
        if film
        else Material("control", absorption=0.08, angular_diffusion=0.05)
    )
    stabilizer = Material("stabilizer", absorption=0.15, angular_diffusion=0.10)
    layers = (
        Layer(0.0, 0.45, substrate),
        Layer(0.45, 0.55, functional),
        Layer(0.55, 1.0, stabilizer),
    )
    absorption, diffusion, material_index = assign_layers(
        grid.centers,
        layers,
        domain_left=grid.left,
        domain_right=grid.right,
    )
    return (
        SlabModel(
            grid,
            operator,
            absorption,
            diffusion,
            BoundaryData(beam_inflow, vacuum),
        ),
        material_index,
    )


def run_interface(level: int, operator, *, film: bool) -> InterfaceRow:
    model, material_index = make_interface_model(operator, film=film)
    state = np.zeros(model.shape, dtype=float)
    final_time = 1.5
    dt_limit = model.stable_timestep(0.8)
    steps = max(1, math.ceil(final_time / dt_limit))
    dt = final_time / steps
    time = 0.0
    regional_absorption = np.zeros(3, dtype=float)
    maximum_balance_error = 0.0
    for _ in range(steps):
        before = model.inventory(state)
        rates = model.balance_rates(state, time)
        for region in range(3):
            regional_absorption[region] += dt * region_absorption_rate(
                model, state, material_index == region
            )
        state = model.euler_step(state, time, dt)
        after = model.inventory(state)
        maximum_balance_error = max(
            maximum_balance_error,
            abs((after - before) - dt * rates.inventory_derivative),
            abs(rates.closure_error),
        )
        time += dt
    tallies = evaluate_tallies(model, state, time)
    return InterfaceRow(
        level=level,
        family=operator.family,
        directions=operator.count,
        case="film" if film else "control",
        cells=model.grid.cells,
        steps=steps,
        right_out=tallies.right_out,
        left_out=tallies.left_out,
        inventory=tallies.inventory,
        total_absorption=float(np.sum(regional_absorption)),
        thin_region_absorption=float(regional_absorption[1]),
        final_absorption_rate=tallies.absorption_rate,
        minimum_solution=float(np.min(state)),
        max_balance_error=maximum_balance_error,
    )


def interface_audit(max_level: int) -> list[InterfaceRow]:
    rows: list[InterfaceRow] = []
    for level in range(1, max_level + 1):
        operators = (
            build_icosphere(level),
            build_product(max(2, round(math.sqrt((10 * 4**level + 2) / 2.0)))),
        )
        for operator in operators:
            film = run_interface(level, operator, film=True)
            control = run_interface(level, operator, film=False)
            rows.extend((film, control))
            transmission_ratio = film.right_out / control.right_out
            absorption_ratio = film.thin_region_absorption / control.thin_region_absorption
            print(
                f"interface level={level} family={operator.family} K={operator.count} "
                f"steps={film.steps}/{control.steps} "
                f"transmission_ratio={transmission_ratio:.6f} "
                f"thin_absorption_ratio={absorption_ratio:.6f}"
            )
            if transmission_ratio >= 0.92:
                raise AssertionError("thin functional film did not reduce transmission enough")
            if absorption_ratio <= 4.0:
                raise AssertionError("thin functional film absorption contrast is too small")
            if film.minimum_solution < -3.0e-12 or control.minimum_solution < -3.0e-12:
                raise AssertionError("spatial interface benchmark lost positivity")
            if max(film.max_balance_error, control.max_balance_error) > 3.0e-11:
                raise AssertionError("spatial interface benchmark failed balance closure")

    finest = [row for row in rows if row.level == max_level and row.case == "film"]
    ico = next(row for row in finest if row.family.startswith("icosphere"))
    product = next(row for row in finest if row.family.startswith("product"))
    if product.steps / ico.steps < 3.5:
        raise AssertionError("product-grid spatial step penalty is unexpectedly small")
    return rows


def write_outputs(
    manufactured: Sequence[ManufacturedRow],
    interface: Sequence[InterfaceRow],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "spatial_manufactured_audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ManufacturedRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in manufactured)
    with (output_dir / "spatial_interface_audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(InterfaceRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in interface)

    lines = [
        "# Gate 6 spatial slab transport audit",
        "",
        "## Manufactured solution",
        "",
        "| family | K | cells | steps | relative error | minimum | balance closure |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in manufactured:
        lines.append(
            f"| {row.family} | {row.directions} | {row.cells} | {row.steps} | "
            f"{row.relative_error:.8e} | {row.minimum_solution:.8e} | "
            f"{row.max_balance_closure:.8e} |"
        )
    lines.extend(
        [
            "",
            "## Thin-interface response",
            "",
            "| level | family | K | case | steps | right out | total absorption | thin-region absorption | balance error |",
            "|---:|---|---:|---|---:|---:|---:|---:|---:|",
        ]
    )
    for row in interface:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.case} | "
            f"{row.steps} | {row.right_out:.8e} | {row.total_absorption:.8e} | "
            f"{row.thin_region_absorption:.8e} | {row.max_balance_error:.8e} |"
        )
    (output_dir / "spatial_slab_transport_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=2)
    parser.add_argument("--output-dir", type=Path, default=Path("gate6/generated"))
    args = parser.parse_args()
    if not 1 <= args.max_level <= 2:
        raise SystemExit("--max-level must be one or two for the CI spatial audit")
    manufactured = manufactured_audit()
    interface = interface_audit(args.max_level)
    write_outputs(manufactured, interface, args.output_dir)
    print("Gate 6 spatial slab transport audit: PASS")


if __name__ == "__main__":
    main()
