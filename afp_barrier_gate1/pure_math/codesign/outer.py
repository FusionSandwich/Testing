"""Fail-closed outer objectives and certified descent controllers.

The practical routines certify feasibility and descent.  Stationarity follows
only under the explicit smooth/Clarke hypotheses stated in the P2C theorem
document; the code never infers it from monotonicity alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Mapping, Sequence

import numpy as np

from .types import QuadratureCandidate


@dataclass(frozen=True)
class ObjectiveWeights:
    defect2: float = 1.0
    rate: float = 0.0
    higher_shells: float = 0.0
    conditioning: float = 0.0
    rotation: float = 0.0
    response: float = 0.0

    def __post_init__(self) -> None:
        values = (
            self.defect2, self.rate, self.higher_shells,
            self.conditioning, self.rotation, self.response,
        )
        if any(not np.isfinite(value) or value < 0 for value in values):
            raise ValueError("outer objective weights must be finite and nonnegative")
        if sum(values) == 0:
            raise ValueError("outer objective cannot be identically zero")


@dataclass(frozen=True)
class ObjectiveTerms:
    defect2: float
    rate: float
    higher_shells: float = 0.0
    conditioning: float = 1.0
    rotation: float = 0.0
    response: float = 0.0

    def weighted(self, weights: ObjectiveWeights) -> float:
        values = (
            self.defect2, self.rate, self.higher_shells,
            self.conditioning, self.rotation, self.response,
        )
        if any(not np.isfinite(value) or value < 0 for value in values):
            raise ValueError("objective terms must be finite and nonnegative")
        if self.conditioning < 1.0:
            raise ValueError("a condition number cannot be below one")
        return float(
            weights.defect2 * self.defect2
            + weights.rate * self.rate
            + weights.higher_shells * self.higher_shells
            + weights.conditioning * np.log(max(1.0, self.conditioning))
            + weights.rotation * self.rotation
            + weights.response * self.response
        )


@dataclass(frozen=True)
class ProtectedMargins:
    minimum_weight: float
    minimum_separation: float
    minimum_sampling_eigenvalue: float
    minimum_feasibility_margin: float

    def __post_init__(self) -> None:
        if min(
            self.minimum_weight,
            self.minimum_separation,
            self.minimum_sampling_eigenvalue,
            self.minimum_feasibility_margin,
        ) <= 0:
            raise ValueError("protected-stratum margins must be strictly positive")


@dataclass(frozen=True)
class OuterEvaluation:
    candidate: QuadratureCandidate
    terms: ObjectiveTerms
    objective: float
    feasible_verified: bool
    inner_verified: bool
    certification: str
    objective_lower: float | None = None
    objective_upper: float | None = None
    diagnostics: Mapping[str, float | str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not np.isfinite(self.objective):
            raise ValueError("outer objective must be finite")
        if (self.objective_lower is None) != (self.objective_upper is None):
            raise ValueError("objective enclosure needs both endpoints")
        if self.certification == "OUTWARD_INTERVAL":
            if self.objective_lower is None:
                raise ValueError("outward interval needs objective bounds")
            if not (
                np.isfinite(self.objective_lower)
                and np.isfinite(self.objective_upper)
                and self.objective_lower <= self.objective
                <= self.objective_upper
            ):
                raise ValueError("invalid outward objective enclosure")

    @property
    def lower(self) -> float:
        if self.certification == "EXACT":
            return float(self.objective)
        if self.objective_lower is None:
            raise ValueError("evaluation has no theorem-bearing lower bound")
        return float(self.objective_lower)

    @property
    def upper(self) -> float:
        if self.certification == "EXACT":
            return float(self.objective)
        if self.objective_upper is None:
            raise ValueError("evaluation has no theorem-bearing upper bound")
        return float(self.objective_upper)

    @property
    def accepted_certificate(self) -> bool:
        return (
            self.feasible_verified
            and self.inner_verified
            and self.certification in {"EXACT", "OUTWARD_INTERVAL"}
        )



Evaluator = Callable[[QuadratureCandidate], OuterEvaluation]


@dataclass(frozen=True)
class ProximalStep:
    before: OuterEvaluation
    after: OuterEvaluation
    distance: float
    proximal_score: float
    descent: float
    accepted: bool


def labelled_distance(
    left: QuadratureCandidate, right: QuadratureCandidate
) -> float:
    """Embedding distance on one fixed labelled node/graph stratum."""

    if left.nodes.shape != right.nodes.shape or left.weights.shape != right.weights.shape:
        return float("inf")
    if left.edges.shape != right.edges.shape or not np.array_equal(left.edges, right.edges):
        return float("inf")
    return float(
        np.sqrt(
            np.linalg.norm(left.nodes - right.nodes) ** 2
            + np.linalg.norm(left.weights - right.weights) ** 2
        )
    )


def certified_proximal_step(
    current: QuadratureCandidate,
    candidate_pool: Sequence[QuadratureCandidate],
    evaluator: Evaluator,
    *,
    alpha: float,
    distance: Callable[[QuadratureCandidate, QuadratureCandidate], float] = labelled_distance,
) -> ProximalStep:
    """Accept only a nonoverlapping certified proximal decrease in a finite pool."""

    if not np.isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be finite and positive")
    before = evaluator(current)
    if not before.accepted_certificate:
        raise RuntimeError("current incumbent lacks an exact/interval certificate")
    evaluated: list[tuple[float, str, OuterEvaluation, float]] = []
    for proposal in candidate_pool:
        report = evaluator(proposal)
        if not report.accepted_certificate:
            continue
        gap = distance(proposal, current)
        if not np.isfinite(gap):
            continue
        score_upper = report.upper + gap * gap / (2.0 * alpha)
        key = f"{proposal.family}:{proposal.node_count}:{proposal.edge_count}"
        evaluated.append((float(score_upper), key, report, float(gap)))
    if not evaluated:
        return ProximalStep(
            before, before, 0.0, before.upper, 0.0, False
        )
    score, _, proposal, gap = min(
        evaluated, key=lambda row: (row[0], row[1])
    )
    accepted = score <= before.lower
    if not accepted:
        return ProximalStep(
            before, before, 0.0, before.upper, 0.0, False
        )
    return ProximalStep(
        before,
        proposal,
        gap,
        score,
        before.lower - proposal.upper,
        True,
    )


@dataclass(frozen=True)
class RestoredTrial:
    evaluation: OuterEvaluation
    step_size: float
    direction_norm: float
    restoration_residual: float
    protection_verified: bool


@dataclass(frozen=True)
class ArmijoDecision:
    accepted: bool
    required_decrease: float
    observed_decrease: float
    reason: str


def accept_restored_armijo(
    current: OuterEvaluation,
    trial: RestoredTrial,
    *,
    armijo: float,
    restoration_tolerance: float,
) -> ArmijoDecision:
    if not 0 < armijo < 1:
        raise ValueError("armijo must lie in (0,1)")
    if trial.step_size <= 0 or trial.direction_norm < 0:
        raise ValueError("invalid restored trial")
    required = armijo * trial.step_size * trial.direction_norm**2
    observed = current.lower - trial.evaluation.upper
    checks = {
        "current certificate": current.accepted_certificate,
        "trial certificate": trial.evaluation.accepted_certificate,
        "protection": trial.protection_verified,
        "restoration": trial.restoration_residual <= restoration_tolerance,
        "decrease": observed >= required,
    }
    failed = [name for name, passed in checks.items() if not passed]
    return ArmijoDecision(
        not failed, float(required), float(observed),
        "PASS" if not failed else "FAILED:" + ",".join(failed),
    )


@dataclass
class AlternatingLedger:
    """One weight/node/conductance sweep with a joint safeguard."""

    evaluations: list[OuterEvaluation] = field(default_factory=list)
    block_labels: list[str] = field(default_factory=list)

    def append(self, label: str, evaluation: OuterEvaluation) -> None:
        if label not in {"WEIGHT_LED", "NODE_LED", "JOINT_SAFEGUARD", "GRAPH"}:
            raise ValueError("unknown alternating block")
        if not evaluation.accepted_certificate:
            raise ValueError("cannot record an uncertified accepted block")
        if self.evaluations:
            previous = self.evaluations[-1]
            if evaluation.upper > previous.lower:
                raise ValueError(
                    "accepted alternating block lacks certified nonincrease"
                )
        self.block_labels.append(label)
        self.evaluations.append(evaluation)

    @property
    def has_joint_safeguard(self) -> bool:
        return "JOINT_SAFEGUARD" in self.block_labels

    @property
    def total_descent(self) -> float:
        if len(self.evaluations) < 2:
            return 0.0
        return float(self.evaluations[0].objective - self.evaluations[-1].objective)


def run_finite_proximal_descent(
    initial: QuadratureCandidate,
    proposal_rounds: Iterable[Sequence[QuadratureCandidate]],
    evaluator: Evaluator,
    *,
    alpha: float,
) -> tuple[QuadratureCandidate, tuple[ProximalStep, ...]]:
    current = initial
    ledger: list[ProximalStep] = []
    for proposals in proposal_rounds:
        step = certified_proximal_step(current, proposals, evaluator, alpha=alpha)
        ledger.append(step)
        current = step.after.candidate
    return current, tuple(ledger)
