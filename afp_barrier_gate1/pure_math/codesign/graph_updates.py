"""Certified edge addition/deletion on a finite master graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

import numpy as np
from numpy.typing import ArrayLike

from .types import QuadratureCandidate


def _edge_tuple(edge: ArrayLike) -> tuple[int, int]:
    i, j = map(int, edge)
    return (i, j) if i < j else (j, i)


def add_edges(
    candidate: QuadratureCandidate,
    added: Iterable[tuple[int, int]],
) -> QuadratureCandidate:
    old = [_edge_tuple(edge) for edge in candidate.edges]
    combined = sorted(set(old) | {_edge_tuple(edge) for edge in added})
    gamma = None
    if candidate.seed_conductance is not None:
        lookup = {
            edge: float(value)
            for edge, value in zip(old, candidate.seed_conductance, strict=True)
        }
        gamma = np.asarray([lookup.get(edge, 0.0) for edge in combined])
    return QuadratureCandidate.build(
        candidate.family,
        candidate.nodes,
        candidate.weights,
        combined,
        seed_conductance=gamma,
        metadata={**candidate.metadata, "graph_update": "EDGE_ADDITION_ZERO_EXTENSION"},
    )


def delete_edges(
    candidate: QuadratureCandidate,
    deleted: Iterable[tuple[int, int]],
) -> QuadratureCandidate:
    removed = {_edge_tuple(edge) for edge in deleted}
    old = [_edge_tuple(edge) for edge in candidate.edges]
    kept = [edge for edge in old if edge not in removed]
    if not kept:
        raise ValueError("cannot delete every edge")
    gamma = None
    if candidate.seed_conductance is not None:
        gamma = np.asarray(
            [
                float(value)
                for edge, value in zip(old, candidate.seed_conductance, strict=True)
                if edge not in removed
            ]
        )
    return QuadratureCandidate.build(
        candidate.family,
        candidate.nodes,
        candidate.weights,
        kept,
        seed_conductance=gamma,
        metadata={**candidate.metadata, "graph_update": "CONDITIONAL_EDGE_DELETION"},
    )


@dataclass(frozen=True)
class ObjectiveInterval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if (
            not np.isfinite(self.lower)
            or not np.isfinite(self.upper)
            or self.lower > self.upper
        ):
            raise ValueError("invalid objective enclosure")


@dataclass(frozen=True)
class GraphEvaluation:
    candidate: QuadratureCandidate
    objective: ObjectiveInterval
    feasible_verified: bool
    inner_verified: bool
    certificate: str


@dataclass(frozen=True)
class GraphDecision:
    accepted: bool
    penalized_old_lower: float
    penalized_new_upper: float
    reason: str


def certified_graph_decision(
    old: GraphEvaluation,
    new: GraphEvaluation,
    *,
    edge_penalty: float = 0.0,
    strict_decrease: float = 0.0,
) -> GraphDecision:
    if edge_penalty < 0 or strict_decrease < 0:
        raise ValueError("penalties/decrease must be nonnegative")
    old_lower = old.objective.lower + edge_penalty * old.candidate.edge_count
    new_upper = new.objective.upper + edge_penalty * new.candidate.edge_count
    accepted_labels = {"EXACT", "OUTWARD_INTERVAL"}
    certificates = (
        old.feasible_verified
        and old.inner_verified
        and new.feasible_verified
        and new.inner_verified
        and old.certificate in accepted_labels
        and new.certificate in accepted_labels
    )
    decrease = new_upper <= old_lower - strict_decrease
    return GraphDecision(
        bool(certificates and decrease),
        float(old_lower),
        float(new_upper),
        "CERTIFIED_DECREASE" if certificates and decrease
        else "RETAIN_INCUMBENT",
    )


def verify_zero_extension(
    old: QuadratureCandidate,
    new: QuadratureCandidate,
    gamma_old: ArrayLike,
    gamma_new: ArrayLike,
    *,
    tolerance: float = 3e-11,
) -> bool:
    """Audit the structural embedding E subset E' and zero new edges.

    Identical nodes/masses plus exact edge inclusion prove equality of the
    whole generator and every shell action; no dense matrix is assembled.
    A tolerance is used only for conductance values, so this return is a
    verified-float regression unless those values are exact objects upstream.
    """

    old_value = np.asarray(gamma_old, dtype=float)
    new_value = np.asarray(gamma_new, dtype=float)
    if (
        old.nodes.shape != new.nodes.shape
        or old.weights.shape != new.weights.shape
        or not np.array_equal(old.nodes, new.nodes)
        or not np.array_equal(old.weights, new.weights)
        or old_value.shape != (old.edge_count,)
        or new_value.shape != (new.edge_count,)
        or not np.all(np.isfinite(old_value))
        or not np.all(np.isfinite(new_value))
    ):
        return False
    old_edges = tuple(_edge_tuple(edge) for edge in old.edges)
    new_edges = tuple(_edge_tuple(edge) for edge in new.edges)
    old_set, new_set = set(old_edges), set(new_edges)
    if not old_set <= new_set:
        return False
    lookup = {
        edge: float(value)
        for edge, value in zip(new_edges, new_value, strict=True)
    }
    reconstructed = np.asarray([lookup[edge] for edge in old_edges])
    added = np.asarray(
        [lookup[edge] for edge in new_edges if edge not in old_set],
        dtype=float,
    )
    scale = max(
        1.0,
        float(np.max(np.abs(old_value))) if old_value.size else 0.0,
    )
    return bool(
        np.linalg.norm(reconstructed - old_value, ord=np.inf)
        <= tolerance * scale
        and (
            added.size == 0
            or np.max(np.abs(added)) <= tolerance * scale
        )
    )


def verify_deletion_kernel_move(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    delta: ArrayLike,
    deleted_edge: int,
    *,
    rate_cap: float,
    tolerance: float = 2e-10,
) -> bool:
    """Check an H1-feasible deletion seed, not shell/objective acceptance."""

    value, move = np.asarray(gamma, dtype=float), np.asarray(delta, dtype=float)
    if value.shape != (candidate.edge_count,) or move.shape != value.shape:
        return False
    trial = value + move
    from .metrics import apply_generator

    h1_move = apply_generator(candidate, move, candidate.nodes)
    endpoint_sum = np.zeros(candidate.node_count)
    i, j = candidate.edges[:, 0], candidate.edges[:, 1]
    np.add.at(endpoint_sum, i, trial)
    np.add.at(endpoint_sum, j, trial)
    rates = endpoint_sum / candidate.weights
    return bool(
        0 <= deleted_edge < candidate.edge_count
        and abs(trial[deleted_edge]) <= tolerance
        and np.min(trial) >= -tolerance
        and np.linalg.norm(h1_move, ord=np.inf) <= tolerance
        and np.max(rates) <= rate_cap + tolerance
    )


@dataclass
class GraphSearchLedger:
    accepted: list[GraphEvaluation] = field(default_factory=list)
    rejected: list[GraphEvaluation] = field(default_factory=list)
    visited: set[tuple[tuple[int, int], ...]] = field(default_factory=set)

    @staticmethod
    def signature(candidate: QuadratureCandidate) -> tuple[tuple[int, int], ...]:
        return tuple(_edge_tuple(edge) for edge in candidate.edges)

    def initialize(self, incumbent: GraphEvaluation) -> None:
        if not incumbent.feasible_verified or not incumbent.inner_verified:
            raise ValueError("initial graph lacks a verified incumbent")
        self.accepted = [incumbent]
        self.visited = {self.signature(incumbent.candidate)}

    def consider(
        self,
        proposal: GraphEvaluation,
        *,
        edge_penalty: float,
        strict_decrease: float,
    ) -> GraphDecision:
        if not self.accepted:
            raise RuntimeError("ledger was not initialized")
        signature = self.signature(proposal.candidate)
        if signature in self.visited:
            self.rejected.append(proposal)
            return GraphDecision(False, 0.0, 0.0, "NO_REVISIT")
        self.visited.add(signature)
        decision = certified_graph_decision(
            self.accepted[-1], proposal,
            edge_penalty=edge_penalty,
            strict_decrease=strict_decrease,
        )
        (self.accepted if decision.accepted else self.rejected).append(proposal)
        return decision


GraphEvaluator = Callable[[QuadratureCandidate], GraphEvaluation]


def deterministic_graph_search(
    initial: QuadratureCandidate,
    proposals: Sequence[QuadratureCandidate],
    evaluator: GraphEvaluator,
    *,
    edge_penalty: float,
    strict_decrease: float,
) -> GraphSearchLedger:
    ledger = GraphSearchLedger()
    ledger.initialize(evaluator(initial))
    for proposal in proposals:
        ledger.consider(
            evaluator(proposal),
            edge_penalty=edge_penalty,
            strict_decrease=strict_decrease,
        )
    return ledger
