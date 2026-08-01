"""Dimensionless HTS-tape-like material stack for transport verification.

The coefficients are deliberately synthetic. They exercise the numerical
couplings expected in coated-conductor transport (substrate, buffer, REBCO,
Ag, and Cu) but are not evaluated nuclear data and must not be interpreted as
material predictions.
"""

from __future__ import annotations

import numpy as np

from .multigroup import EnergyGroups
from .multigroup_materials import MultigroupLayer, MultigroupMaterial


def default_energy_groups() -> EnergyGroups:
    return EnergyGroups(energies=(5.0, 2.5, 1.0), speeds=(1.0, 0.82, 0.60))


def _material(
    name: str,
    energies: np.ndarray,
    *,
    absorption: tuple[float, float, float],
    diffusion_scale: float,
    high_to_mid: float,
    high_to_low: float,
    mid_to_low: float,
) -> MultigroupMaterial:
    diffusion = tuple(float(diffusion_scale / energy**2) for energy in energies)
    transfer = (
        (0.0, high_to_mid, high_to_low),
        (0.0, 0.0, mid_to_low),
        (0.0, 0.0, 0.0),
    )
    return MultigroupMaterial(name, absorption, diffusion, transfer)


def hts_like_materials(groups: EnergyGroups | None = None) -> dict[str, MultigroupMaterial]:
    group_data = groups or default_energy_groups()
    energies = group_data.energy_array
    return {
        "hastelloy": _material(
            "Hastelloy substrate", energies,
            absorption=(0.018, 0.032, 0.060), diffusion_scale=0.16,
            high_to_mid=0.10, high_to_low=0.018, mid_to_low=0.14,
        ),
        "buffer": _material(
            "MgO/buffer stack", energies,
            absorption=(0.030, 0.055, 0.090), diffusion_scale=0.24,
            high_to_mid=0.14, high_to_low=0.030, mid_to_low=0.20,
        ),
        "rebco": _material(
            "REBCO functional layer", energies,
            absorption=(0.200, 0.320, 0.550), diffusion_scale=0.55,
            high_to_mid=0.35, high_to_low=0.120, mid_to_low=0.45,
        ),
        "silver": _material(
            "Ag cap", energies,
            absorption=(0.040, 0.075, 0.135), diffusion_scale=0.28,
            high_to_mid=0.17, high_to_low=0.040, mid_to_low=0.24,
        ),
        "copper": _material(
            "Cu stabilizer", energies,
            absorption=(0.032, 0.060, 0.110), diffusion_scale=0.22,
            high_to_mid=0.15, high_to_low=0.032, mid_to_low=0.21,
        ),
    }


def hts_like_layers(
    groups: EnergyGroups | None = None,
    *,
    functional_layer: bool = True,
) -> tuple[MultigroupLayer, ...]:
    materials = hts_like_materials(groups)
    functional = materials["rebco"] if functional_layer else materials["buffer"]
    return (
        MultigroupLayer(0.00, 0.42, materials["hastelloy"]),
        MultigroupLayer(0.42, 0.47, materials["buffer"]),
        MultigroupLayer(0.47, 0.53, functional),
        MultigroupLayer(0.53, 0.58, materials["silver"]),
        MultigroupLayer(0.58, 1.00, materials["copper"]),
    )
