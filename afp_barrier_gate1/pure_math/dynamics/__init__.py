"""Audited finite-dimensional dynamics and transport-error utilities."""

from .bounds import (
    RESIDUAL_COMPONENTS,
    PreconditionedBound,
    ResidualLedger,
    iteration_error_bound,
    preconditioned_bound,
)
from .core import (
    BandSamplingReport,
    GeneratorReport,
    ModeErrorReport,
    PhysicalDissipativityReport,
    ShellErrorReport,
    ShellResidual,
    band_sampling_guard,
    physical_symmetrizer_dissipativity,
    resolvent_mode_error,
    resolvent_shell_error,
    semigroup_mode_error,
    semigroup_shell_error,
    shell_residual,
    validate_reversible_generator,
    weighted_norm,
)

__all__ = [
    "BandSamplingReport",
    "GeneratorReport",
    "ModeErrorReport",
    "PhysicalDissipativityReport",
    "PreconditionedBound",
    "RESIDUAL_COMPONENTS",
    "ResidualLedger",
    "ShellErrorReport",
    "ShellResidual",
    "band_sampling_guard",
    "iteration_error_bound",
    "physical_symmetrizer_dissipativity",
    "preconditioned_bound",
    "resolvent_mode_error",
    "resolvent_shell_error",
    "semigroup_mode_error",
    "semigroup_shell_error",
    "shell_residual",
    "validate_reversible_generator",
    "weighted_norm",
]
