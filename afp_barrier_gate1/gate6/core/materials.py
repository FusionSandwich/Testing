"""Material fields and piecewise-layer helpers for one-dimensional transport."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Material:
    """Macroscopic coefficients for one spatial region.

    `absorption` removes particles. `angular_diffusion` multiplies the angular
    Fokker--Planck generator. Coefficients must be finite and nonnegative.
    """

    name: str
    absorption: float = 0.0
    angular_diffusion: float = 0.0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("material name must not be empty")
        for field_name, value in (
            ("absorption", self.absorption),
            ("angular_diffusion", self.angular_diffusion),
        ):
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{field_name} must be finite and nonnegative")


@dataclass(frozen=True)
class Layer:
    """Half-open layer interval `[left, right)` with one material."""

    left: float
    right: float
    material: Material

    def __post_init__(self) -> None:
        if not np.isfinite(self.left) or not np.isfinite(self.right):
            raise ValueError("layer bounds must be finite")
        if not self.left < self.right:
            raise ValueError("layer left bound must be smaller than right bound")


def assign_layers(
    cell_centers: np.ndarray,
    layers: Sequence[Layer],
    *,
    domain_left: float,
    domain_right: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Map a complete nonoverlapping layer stack onto cell centers.

    Returns absorption, angular-diffusion, and integer material-index arrays.
    Layers must exactly cover the domain without gaps or overlaps.
    """

    centers = np.asarray(cell_centers, dtype=float)
    if centers.ndim != 1 or len(centers) == 0:
        raise ValueError("cell_centers must be a nonempty vector")
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

    absorption = np.empty(len(centers), dtype=float)
    diffusion = np.empty(len(centers), dtype=float)
    material_index = np.full(len(centers), -1, dtype=int)
    for index, layer in enumerate(ordered):
        if index == len(ordered) - 1:
            mask = (centers >= layer.left - tolerance) & (centers <= layer.right + tolerance)
        else:
            mask = (centers >= layer.left - tolerance) & (centers < layer.right - tolerance)
        if np.any(material_index[mask] >= 0):
            raise ValueError("a cell center is assigned to multiple layers")
        absorption[mask] = layer.material.absorption
        diffusion[mask] = layer.material.angular_diffusion
        material_index[mask] = index
    if np.any(material_index < 0):
        raise ValueError("one or more cell centers are not covered by a layer")
    return absorption, diffusion, material_index
