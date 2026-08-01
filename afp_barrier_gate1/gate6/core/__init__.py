"""Reusable deterministic transport core for Gate 6."""

from .angular import (
    AngularOperator,
    apply_generator,
    build_icosphere,
    build_product,
    exact_semidiscrete_evolution,
    make_operator,
    nearest_product_n,
    weighted_integral,
    weighted_l2_error,
)
from .manufactured import CoordinateModeManufactured
from .materials import Layer, Material, assign_layers
from .slab import (
    BalanceRates,
    BoundaryData,
    SlabGrid,
    SlabModel,
    SlabTransportError,
    StepDiagnostics,
)
from .tallies import SlabTallies, evaluate_tallies, region_absorption_rate
from .hts_surrogate import default_energy_groups, hts_like_layers, hts_like_materials
from .multigroup import (
    EnergyGroups,
    MultigroupBalanceRates,
    MultigroupBoundaryData,
    MultigroupSlabModel,
    MultigroupStepDiagnostics,
)
from .multigroup_materials import (
    MultigroupLayer,
    MultigroupMaterial,
    assign_multigroup_layers,
    validate_downscatter,
)
from .multigroup_tallies import (
    MultigroupTallies,
    evaluate_multigroup_tallies,
    region_energy_deposition_rates,
)

__all__ = [
    "AngularOperator",
    "BalanceRates",
    "BoundaryData",
    "CoordinateModeManufactured",
    "EnergyGroups",
    "Layer",
    "Material",
    "MultigroupBalanceRates",
    "MultigroupBoundaryData",
    "MultigroupLayer",
    "MultigroupMaterial",
    "MultigroupSlabModel",
    "MultigroupStepDiagnostics",
    "MultigroupTallies",
    "SlabGrid",
    "SlabModel",
    "SlabTallies",
    "SlabTransportError",
    "StepDiagnostics",
    "apply_generator",
    "assign_layers",
    "assign_multigroup_layers",
    "build_icosphere",
    "build_product",
    "default_energy_groups",
    "evaluate_multigroup_tallies",
    "evaluate_tallies",
    "exact_semidiscrete_evolution",
    "hts_like_layers",
    "hts_like_materials",
    "make_operator",
    "nearest_product_n",
    "region_absorption_rate",
    "region_energy_deposition_rates",
    "validate_downscatter",
    "weighted_integral",
    "weighted_l2_error",
]
