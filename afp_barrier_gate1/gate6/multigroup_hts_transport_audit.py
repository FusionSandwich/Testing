#!/usr/bin/env python3
"""Gate 6 conservative multigroup HTS-like slab transport audit.

This benchmark adds three energy groups, group-dependent velocities, angular
Fokker--Planck diffusion, conservative down-scattering, absorption heating, and
transfer heating to the tested 1-D slab solver.  The layer coefficients are a
dimensionless coated-conductor surrogate, not evaluated nuclear data.

Two angular families are compared at matched direction counts.  Both a fully
explicit Euler method and a Strang method with exact angular-collision
substeps are audited.  The latter removes angular stiffness while preserving
the same multigroup and spatial physics.
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
    MultigroupBoundaryData,
    MultigroupSlabModel,
    SlabGrid,
    assign_multigroup_layers,
    build_icosphere,
    build_product,
    default_energy_groups,
    evaluate_multigroup_tallies,
    hts_like_layers,
    region_energy_deposition_rates,
)


@dataclass(frozen=True)
class AuditRow:
    level: int
    family: str
    directions: int
    case: str
    integrator: str
    cells: int
    steps: int
    final_time: float
    particle_inventory: float
    energy_inventory: float
    transmitted_particle: float
    transmitted_energy: float
    transmitted_high: float
    transmitted_mid: float
    transmitted_low: float
    cumulative_absorption_heating: float
    cumulative_transfer_heating: float
    cumulative_total_heating: float
    functional_region_heating: float
    functional_region_fraction: float
    minimum_solution: float
    max_particle_closure: float
    max_energy_closure: float


def beam_inflow(_time: float, energies: np.ndarray, mu: np.ndarray) -> np.ndarray:
    values = np.zeros((len(energies), len(mu)), dtype=float)
    positive = mu > 0.0
    values[0, positive] = np.exp(-((1.0 - mu[positive]) / 0.22) ** 2)
    return values


def vacuum(_time: float, energies: np.ndarray, mu: np.ndarray) -> np.ndarray:
    return np.zeros((len(energies), len(mu)), dtype=float)


def make_model(operator, *, functional_layer: bool, cells: int) -> tuple[MultigroupSlabModel, np.ndarray]:
    groups = default_energy_groups()
    grid = SlabGrid(0.0, 1.0, cells)
    absorption, diffusion, transfer, material_index = assign_multigroup_layers(
        grid.centers,
        hts_like_layers(groups, functional_layer=functional_layer),
        energies=groups.energy_array,
        domain_left=grid.left,
        domain_right=grid.right,
    )
    model = MultigroupSlabModel(
        grid=grid,
        angular=operator,
        groups=groups,
        absorption=absorption,
        angular_diffusion=diffusion,
        transfer=transfer,
        boundary=MultigroupBoundaryData(beam_inflow, vacuum),
    )
    return model, material_index


def run_case(
    level: int,
    operator,
    *,
    functional_layer: bool,
    integrator: str,
    cells: int,
    final_time: float,
) -> AuditRow:
    model, material_index = make_model(
        operator, functional_layer=functional_layer, cells=cells
    )
    state = np.zeros(model.shape, dtype=float)
    include_collision = integrator != "strang"
    dt_limit = model.stable_timestep(0.8, include_collision=include_collision)
    steps = max(1, math.ceil(final_time / dt_limit))
    dt = final_time / steps
    cumulative_absorption = 0.0
    cumulative_transfer = 0.0
    cumulative_regions = np.zeros(5, dtype=float)
    max_particle_closure = 0.0
    max_energy_closure = 0.0
    time = 0.0

    for _ in range(steps):
        particle_before = model.particle_inventory(state)
        energy_before = model.energy_inventory(state)
        rates = model.balance_rates(state, time)
        cumulative_absorption += dt * rates.absorption_deposition
        cumulative_transfer += dt * rates.transfer_deposition
        for region in range(5):
            _, _, total = region_energy_deposition_rates(
                model, state, material_index == region
            )
            cumulative_regions[region] += dt * total
        state = model.step(state, time, dt, integrator=integrator)
        particle_after = model.particle_inventory(state)
        energy_after = model.energy_inventory(state)
        max_particle_closure = max(
            max_particle_closure,
            abs(rates.particle_closure_error),
        )
        max_energy_closure = max(
            max_energy_closure,
            abs(rates.energy_closure_error),
        )
        if integrator == "euler":
            max_particle_closure = max(
                max_particle_closure,
                abs((particle_after - particle_before) - dt * rates.particle_derivative),
            )
            max_energy_closure = max(
                max_energy_closure,
                abs((energy_after - energy_before) - dt * rates.energy_derivative),
            )
        time += dt
        if float(np.min(state)) < -5.0e-10:
            raise AssertionError("multigroup transport lost positivity")

    tallies = evaluate_multigroup_tallies(model, state, time)
    transmitted_particle = float(np.sum(tallies.right_out))
    transmitted_energy = float(np.dot(model.groups.energy_array, tallies.right_out))
    total_heating = cumulative_absorption + cumulative_transfer
    functional_heating = float(cumulative_regions[2])
    return AuditRow(
        level=level,
        family=operator.family,
        directions=operator.count,
        case="functional" if functional_layer else "control",
        integrator=integrator,
        cells=cells,
        steps=steps,
        final_time=final_time,
        particle_inventory=tallies.particle_inventory,
        energy_inventory=tallies.energy_inventory,
        transmitted_particle=transmitted_particle,
        transmitted_energy=transmitted_energy,
        transmitted_high=float(tallies.right_out[0]),
        transmitted_mid=float(tallies.right_out[1]),
        transmitted_low=float(tallies.right_out[2]),
        cumulative_absorption_heating=cumulative_absorption,
        cumulative_transfer_heating=cumulative_transfer,
        cumulative_total_heating=total_heating,
        functional_region_heating=functional_heating,
        functional_region_fraction=functional_heating / total_heating,
        minimum_solution=tallies.minimum_value,
        max_particle_closure=max_particle_closure,
        max_energy_closure=max_energy_closure,
    )


def relative_difference(first: float, second: float) -> float:
    scale = max(abs(first), abs(second), 1.0e-15)
    return abs(first - second) / scale


def write_outputs(rows: Sequence[AuditRow], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = list(AuditRow.__dataclass_fields__)
    with (output_dir / "multigroup_hts_transport_audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    lines = [
        "# Gate 6 conservative multigroup HTS-like slab audit",
        "",
        "The material coefficients are dimensionless numerical surrogates, not evaluated nuclear data.",
        "",
        "| level | family | K | case | integrator | steps | transmitted energy | total heating | functional heating fraction |",
        "|---:|---|---:|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.level} | {row.family} | {row.directions} | {row.case} | "
            f"{row.integrator} | {row.steps} | {row.transmitted_energy:.8e} | "
            f"{row.cumulative_total_heating:.8e} | {row.functional_region_fraction:.8e} |"
        )
    (output_dir / "multigroup_hts_transport_audit.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-level", type=int, default=2)
    parser.add_argument("--cells", type=int, default=60)
    parser.add_argument("--final-time", type=float, default=1.6)
    parser.add_argument("--output-dir", type=Path, default=Path("gate6/generated"))
    args = parser.parse_args()
    if not 1 <= args.max_level <= 2:
        raise SystemExit("--max-level must be one or two for the CI benchmark")
    if args.cells < 20 or args.final_time <= 0.0:
        raise SystemExit("invalid cells or final time")

    rows: list[AuditRow] = []
    for level in range(1, args.max_level + 1):
        target = 10 * 4**level + 2
        operators = (
            build_icosphere(level),
            build_product(max(2, round(math.sqrt(target / 2.0)))),
        )
        for operator in operators:
            for functional in (True, False):
                for integrator in ("euler", "strang"):
                    row = run_case(
                        level,
                        operator,
                        functional_layer=functional,
                        integrator=integrator,
                        cells=args.cells,
                        final_time=args.final_time,
                    )
                    rows.append(row)
                    print(
                        f"level={level} family={row.family} K={row.directions} "
                        f"case={row.case} method={integrator} steps={row.steps} "
                        f"Etrans={row.transmitted_energy:.6e} heat={row.cumulative_total_heating:.6e} "
                        f"filmfrac={row.functional_region_fraction:.4f}"
                    )

    finest = [row for row in rows if row.level == args.max_level]
    for family in {row.family for row in finest}:
        functional = {
            row.integrator: row
            for row in finest
            if row.family == family and row.case == "functional"
        }
        control = {
            row.integrator: row
            for row in finest
            if row.family == family and row.case == "control"
        }
        if functional["euler"].transmitted_energy >= 0.98 * control["euler"].transmitted_energy:
            raise AssertionError("functional layer did not reduce transmitted energy")
        if functional["euler"].functional_region_heating <= 1.5 * control["euler"].functional_region_heating:
            raise AssertionError("functional layer did not increase local heating")
        if relative_difference(
            functional["euler"].transmitted_energy,
            functional["strang"].transmitted_energy,
        ) > 0.015:
            raise AssertionError("Euler and Strang transmitted energy disagree")
        if relative_difference(
            functional["euler"].cumulative_total_heating,
            functional["strang"].cumulative_total_heating,
        ) > 0.02:
            raise AssertionError("Euler and Strang heating disagree")

    ico = next(
        row for row in finest
        if row.family.startswith("icosphere") and row.case == "functional" and row.integrator == "euler"
    )
    product = next(
        row for row in finest
        if row.family.startswith("product") and row.case == "functional" and row.integrator == "euler"
    )
    ico_split = next(
        row for row in finest
        if row.family.startswith("icosphere") and row.case == "functional" and row.integrator == "strang"
    )
    product_split = next(
        row for row in finest
        if row.family.startswith("product") and row.case == "functional" and row.integrator == "strang"
    )
    if relative_difference(ico.transmitted_energy, product.transmitted_energy) > 0.025:
        raise AssertionError("angular families disagree on transmitted energy")
    if relative_difference(ico.cumulative_total_heating, product.cumulative_total_heating) > 0.03:
        raise AssertionError("angular families disagree on total heating")
    if product.steps / ico.steps < 2.0:
        raise AssertionError("fully explicit product-grid penalty is unexpectedly small")
    if product_split.steps / ico_split.steps > 1.15:
        raise AssertionError("exact-collision splitting did not remove angular step penalty")
    if max(row.max_particle_closure for row in rows if row.integrator == "euler") > 2.0e-10:
        raise AssertionError("particle balance closure failed")
    if max(row.max_energy_closure for row in rows if row.integrator == "euler") > 3.0e-10:
        raise AssertionError("energy balance closure failed")

    write_outputs(rows, args.output_dir)
    print("Gate 6 conservative multigroup HTS-like slab audit: PASS")


if __name__ == "__main__":
    main()
