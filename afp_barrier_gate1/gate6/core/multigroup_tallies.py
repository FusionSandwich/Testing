"""Particle, energy, and heating tallies for multigroup slab transport."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .multigroup import MultigroupSlabModel


@dataclass(frozen=True)
class MultigroupTallies:
    particle_inventory: float
    energy_inventory: float
    left_in: np.ndarray
    left_out: np.ndarray
    right_in: np.ndarray
    right_out: np.ndarray
    group_scalar_flux_integral: np.ndarray
    absorption_particle_rate: float
    absorption_energy_deposition_rate: float
    transfer_energy_deposition_rate: float
    minimum_value: float


def evaluate_multigroup_tallies(
    model: MultigroupSlabModel, state: np.ndarray, time: float
) -> MultigroupTallies:
    currents = model.boundary_currents(state, time)
    group_flux = model.group_scalar_flux(state)
    return MultigroupTallies(
        particle_inventory=model.particle_inventory(state),
        energy_inventory=model.energy_inventory(state),
        left_in=currents["left_in"],
        left_out=currents["left_out"],
        right_in=currents["right_in"],
        right_out=currents["right_out"],
        group_scalar_flux_integral=model.grid.dx * np.sum(group_flux, axis=0),
        absorption_particle_rate=model.absorption_particle_rate(state),
        absorption_energy_deposition_rate=model.absorption_energy_deposition_rate(state),
        transfer_energy_deposition_rate=model.transfer_energy_deposition_rate(state),
        minimum_value=float(np.min(state)),
    )


def region_energy_deposition_rates(
    model: MultigroupSlabModel, state: np.ndarray, cell_mask: np.ndarray
) -> tuple[float, float, float]:
    mask = np.asarray(cell_mask, dtype=bool)
    if mask.shape != (model.grid.cells,):
        raise ValueError("cell_mask must have one value per spatial cell")
    psi = model.validate_state(state)
    weights = model.angular.weights[None, None, :]
    energies = model.groups.energy_array
    absorption = float(
        model.grid.dx
        * np.sum(
            model.absorption[mask, :, None]
            * psi[mask]
            * energies[None, :, None]
            * weights
        )
    )
    group_flux = np.sum(psi[mask] * weights, axis=2)
    drop = energies[:, None] - energies[None, :]
    transfer = float(
        model.grid.dx
        * np.sum(
            model.transfer[mask]
            * group_flux[:, :, None]
            * drop[None, :, :]
        )
    )
    return absorption, transfer, absorption + transfer
