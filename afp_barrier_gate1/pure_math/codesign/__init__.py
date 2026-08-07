"""Controlled quadrature--generator co-design (P2C).

The package keeps the globally solved convex conductance problem separate from
the nonconvex node/weight/graph outer problem.  Proof claims and certification
levels are recorded in the accompanying P2C theorem and claim-map documents.
"""

from .adaptive import (
    AdaptiveProposal,
    EnrichedResponseReport,
    antipodal_response_proposal,
    deterministic_mark,
    enriched_response_identity,
)
from .convergence import (
    ConvergenceRow,
    TheoremSandwich,
    benchmark_reflected_ring_family,
    benchmark_reflected_ring_level,
    paper_i_sandwich,
)
from .families import (
    FAMILY_DESCRIPTORS,
    ahrens_beylkin_from_orbits,
    icosahedral_rotations,
)
from .graph_updates import (
    GraphDecision,
    GraphEvaluation,
    GraphSearchLedger,
    ObjectiveInterval,
    add_edges,
    certified_graph_decision,
    delete_edges,
    verify_deletion_kernel_move,
    verify_zero_extension,
)
from .inner import (
    GramEpigraphReport,
    InnerRecord,
    moving_gram_block,
    solve_global_inner,
    verify_moving_gram_epigraph,
)
from .metrics import CandidateReport, full_report
from .outer import (
    AlternatingLedger,
    ObjectiveTerms,
    ObjectiveWeights,
    OuterEvaluation,
    ProtectedMargins,
    accept_restored_armijo,
    run_finite_proximal_descent,
)
from .types import (
    ApproachRecord,
    Certification,
    CertifiedValue,
    FamilyDescriptor,
    QuadratureCandidate,
)

__all__ = [
    "AdaptiveProposal",
    "AlternatingLedger",
    "ApproachRecord",
    "CandidateReport",
    "Certification",
    "CertifiedValue",
    "ConvergenceRow",
    "EnrichedResponseReport",
    "FAMILY_DESCRIPTORS",
    "ahrens_beylkin_from_orbits",
    "icosahedral_rotations",
    "FamilyDescriptor",
    "GramEpigraphReport",
    "GraphDecision",
    "GraphEvaluation",
    "GraphSearchLedger",
    "InnerRecord",
    "ObjectiveInterval",
    "ObjectiveTerms",
    "ObjectiveWeights",
    "OuterEvaluation",
    "ProtectedMargins",
    "QuadratureCandidate",
    "TheoremSandwich",
    "accept_restored_armijo",
    "add_edges",
    "antipodal_response_proposal",
    "benchmark_reflected_ring_family",
    "benchmark_reflected_ring_level",
    "certified_graph_decision",
    "delete_edges",
    "deterministic_mark",
    "enriched_response_identity",
    "full_report",
    "moving_gram_block",
    "paper_i_sandwich",
    "run_finite_proximal_descent",
    "solve_global_inner",
    "verify_deletion_kernel_move",
    "verify_moving_gram_epigraph",
    "verify_zero_extension",
]
