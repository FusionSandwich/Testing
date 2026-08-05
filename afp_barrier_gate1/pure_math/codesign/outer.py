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
    diagnostics: Mapping[str, float | str] = field(default_factory=dict)

    @property
    def accepted_certificate(self) -> bool:
        return (
            self.feasible_verified
            and self.inner_verified
            and self.certification in {
                "EXACT", "OUTWARD_INTERVAL", "VERIFIED_FLOAT"
            }
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
    """Globally minimize the proximal objective over a declared finite pool.

    The pool is an executable approximation of the compact-stratum proximal
    theorem.  It certifies descent over this pool only, not continuum
    stationarity or global outer optimality.
    """

    if not np.isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be finite and positive")
    before = evaluator(current)
    if not before.accepted_certificate:
        raise RuntimeError("current incumbent lacks a verified certificate")
    pool = [current, *candidate_pool]
    evaluated: list[tuple[float, str, OuterEvaluation, float]] = []
    for proposal in pool:
        report = evaluator(proposal)
        if not report.accepted_certificate:
            continue
        gap = distance(proposal, current)
        if not np.isfinite(gap):
            continue
        score = report.objective + gap * gap / (2.0 * alpha)
        key = f"{proposal.family}:{proposal.node_count}:{proposal.edge_count}"
        evaluated.append((float(score), key, report, float(gap)))
    if not evaluated:
        raise RuntimeError("no proposal, including the incumbent, verified")
    score, _, after, gap = min(evaluated, key=lambda row: (row[0], row[1]))
    descent = before.objective - after.objective
    tolerance = 5e-11 * max(1.0, abs(before.objective), abs(after.objective))
    accepted = after.objective + gap * gap / (2.0 * alpha) <= before.objective + tolerance
    if not accepted:
        after, gap, score, descent = before, 0.0, before.objective, 0.0
    return ProximalStep(before, after, gap, score, descent, accepted)


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
    observed = current.objective - trial.evaluation.objective
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
            previous = self.evaluations[-1].objective
            tolerance = 5e-11 * max(1.0, abs(previous))
            if evaluation.objective > previous + tolerance:
                raise ValueError("accepted alternating block increased the objective")
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
