"""Certified convex design of positive reversible spherical generators.

The package keeps the mathematical data assembly independent of CVXPY.  A
solver produces only a candidate; :mod:`certificates` recomputes primal,
dual, and Farkas residuals directly from the frozen arrays.
"""

from .model import (
    AmbiguousSamplingRank,
    DesignModel,
    ExactSamplingCertificate,
    QuadratureGraph,
    RankPolicy,
    ShellData,
    degree_two_basis,
    real_harmonic_samples,
)
from .programs import (
    DesignRequest,
    DesignResult,
    ResponseTerm,
    SolverConfig,
    prune_and_reoptimize,
    solve_design,
)
from .certificates import (
    ConicInfeasibilityCertificate,
    FarkasCertificate,
    VerificationReport,
    find_farkas_certificate,
    verify_farkas_certificate,
    verify_conic_infeasibility_certificate,
    verify_result,
)

__all__ = [
    "AmbiguousSamplingRank",
    "DesignModel",
    "ExactSamplingCertificate",
    "DesignRequest",
    "DesignResult",
    "ConicInfeasibilityCertificate",
    "ResponseTerm",
    "FarkasCertificate",
    "QuadratureGraph",
    "RankPolicy",
    "ShellData",
    "SolverConfig",
    "VerificationReport",
    "degree_two_basis",
    "find_farkas_certificate",
    "prune_and_reoptimize",
    "real_harmonic_samples",
    "solve_design",
    "verify_farkas_certificate",
    "verify_conic_infeasibility_certificate",
    "verify_result",
]
