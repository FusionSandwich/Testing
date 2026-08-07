"""P2D fixed-point-preserving acceleration primitives."""

from .core import (
    FieldOfValuesReport,
    IterationResult,
    ShellContraction,
    constrained_defect_correction,
    constrained_error_propagation_operator,
    constrained_low_inverse,
    defect_correction,
    error_propagation_operator,
    field_of_values_bound,
    invariant_residuals,
    perturbation_contraction_bound,
    preconditioned_gmres,
    shellwise_contraction,
)

__all__ = [
    "FieldOfValuesReport",
    "IterationResult",
    "ShellContraction",
    "constrained_defect_correction",
    "constrained_error_propagation_operator",
    "constrained_low_inverse",
    "defect_correction",
    "error_propagation_operator",
    "field_of_values_bound",
    "invariant_residuals",
    "perturbation_contraction_bound",
    "preconditioned_gmres",
    "shellwise_contraction",
]
