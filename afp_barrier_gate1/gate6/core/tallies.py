"""Conservative response tallies for one-dimensional slab transport."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .slab import SlabModel


@dataclass(frozen=True)
class SlabTallies:
    inventory: float
    left_in: float
    left_out: float
    right_in: float
    right_out: float
    absorption_rate: float
    scalar_flux_integral: float
    minimum_scalar_flux: float
    maximum_scalar_flux: float


def evaluate_tallies(model: SlabModel, state: np.ndarray, time: float) -> SlabTallies:
    scalar = model.scalar_flux(state)
    currents = model.boundary_currents(state, time)
    return SlabTallies(
        inventory=model.inventory(state),
        left_in=currents["left_in"],
        left_out=currents["left_out"],
        right_in=currents["right_in"],
        right_out=currents["right_out"],
        absorption_rate=model.absorption_rate(state),
        scalar_flux_integral=float(model.grid.dx * np.sum(scalar)),
        minimum_scalar_flux=float(np.min(scalar)),
        maximum_scalar_flux=float(np.max(scalar)),
    )


def region_absorption_rate(
    model: SlabModel, state: np.ndarray, cell_mask: np.ndarray
) -> float:
    mask = np.asarray(cell_mask, dtype=bool)
    if mask.shape != (model.grid.cells,):
        raise ValueError("cell_mask must have one value per spatial cell")
    psi = model.validate_state(state)
    return float(
        model.grid.dx
        * np.sum(
            model.absorption[mask, None]
            * psi[mask]
            * model.angular.weights[None, :]
        )
    )
