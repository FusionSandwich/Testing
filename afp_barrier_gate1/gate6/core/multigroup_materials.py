"""Multigroup material data and layer mapping for slab transport."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class MultigroupMaterial:
    """Cell-independent multigroup coefficients for one material.

    `transfer[g, h]` is the nonnegative rate from source group `g` to
    destination group `h`. Diagonal entries must vanish. Energy ordering is
    checked when the material is assigned to an energy grid.
    """

    name: str
    absorption: tuple[float, ...]
    angular_diffusion: tuple[float, ...]
    transfer: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("material name must not be empty")
        absorption = np.asarray(self.absorption, dtype=float)
        diffusion = np.asarray(self.angular_diffusion, dtype=float)
        transfer = np.asarray(self.transfer, dtype=float)
        if absorption.ndim != 1 or len(absorption) == 0:
            raise ValueError("absorption must be a nonempty vector")
        groups = len(absorption)
        if diffusion.shape != (groups,) or transfer.shape != (groups, groups):
            raise ValueError("multigroup coefficient dimensions are inconsistent")
        if not (
            np.all(np.isfinite(absorption))
            and np.all(np.isfinite(diffusion))
            and np.all(np.isfinite(transfer))
        ):
            raise ValueError("multigroup coefficients must be finite")
        if np.min(absorption) < 0.0 or np.min(diffusion) < 0.0 or np.min(transfer) < 0.0:
            raise ValueError("multigroup coefficients must be nonnegative")
        if np.max(np.abs(np.diag(transfer))) > 0.0:
            raise ValueError("transfer diagonal must vanish")

    @property
    def groups(self) -> int:
        return len(self.absorption)

    def arrays(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            np.asarray(self.absorption, dtype=float),
            np.asarray(self.angular_diffusion, dtype=float),
            np.asarray(self.transfer, dtype=float),
        )


@dataclass(frozen=True)
class MultigroupLayer:
    left: float
    right: float
    material: MultigroupMaterial

    def __post_init__(self) -> None:
        if not np.isfinite(self.left) or not np.isfinite(self.right):
            raise ValueError("layer bounds must be finite")
        if not self.left < self.right:
            raise ValueError("layer left bound must be smaller than right bound")


def validate_downscatter(transfer: np.ndarray, energies: np.ndarray) -> None:
    matrix = np.asarray(transfer, dtype=float)
    energy = np.asarray(energies, dtype=float)
    if matrix.shape != (len(energy), len(energy)):
        raise ValueError("transfer and energy dimensions differ")
    source, destination = np.nonzero(matrix > 0.0)
    if np.any(energy[destination] > energy[source] + 1.0e-13):
        raise ValueError("up-scattering is not allowed in this Gate 6 model")


def assign_multigroup_layers(
    cell_centers: np.ndarray,
    layers: Sequence[MultigroupLayer],
    *,
    energies: np.ndarray,
    domain_left: float,
    domain_right: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Assign a complete multigroup layer stack to cell centers.

    Returns `(absorption, angular_diffusion, transfer, material_index)` with
    shapes `(C,G)`, `(C,G)`, `(C,G,G)`, and `(C,)`.
    """

    centers = np.asarray(cell_centers, dtype=float)
    energy = np.asarray(energies, dtype=float)
    if centers.ndim != 1 or len(centers) == 0:
        raise ValueError("cell_centers must be a nonempty vector")
    if energy.ndim != 1 or len(energy) == 0:
        raise ValueError("energies must be a nonempty vector")
    if not domain_left < domain_right:
        raise ValueError("invalid domain")
    if not layers:
        raise ValueError("at least one layer is required")

    ordered = sorted(layers, key=lambda layer: layer.left)
    tolerance = 1.0e-12 * max(1.0, abs(domain_left), abs(domain_right))
    if abs(ordered[0].left - domain_left) > tolerance:
        raise ValueError("layers do not begin at the domain boundary")
    if abs(ordered[-1].right - domain_right) > tolerance:
        raise ValueError("layers do not end at the domain boundary")
    for first, second in zip(ordered[:-1], ordered[1:]):
        if abs(first.right - second.left) > tolerance:
            raise ValueError("layers contain a gap or overlap")

    groups = len(energy)
    absorption = np.empty((len(centers), groups), dtype=float)
    diffusion = np.empty((len(centers), groups), dtype=float)
    transfer = np.empty((len(centers), groups, groups), dtype=float)
    material_index = np.full(len(centers), -1, dtype=int)

    for index, layer in enumerate(ordered):
        if layer.material.groups != groups:
            raise ValueError("material group count differs from energy grid")
        a, d, t = layer.material.arrays()
        validate_downscatter(t, energy)
        if index == len(ordered) - 1:
            mask = (centers >= layer.left - tolerance) & (centers <= layer.right + tolerance)
        else:
            mask = (centers >= layer.left - tolerance) & (centers < layer.right - tolerance)
        if np.any(material_index[mask] >= 0):
            raise ValueError("a cell center is assigned to multiple layers")
        absorption[mask] = a
        diffusion[mask] = d
        transfer[mask] = t
        material_index[mask] = index

    if np.any(material_index < 0):
        raise ValueError("one or more cell centers are not covered by a layer")
    return absorption, diffusion, transfer, material_index
