"""Immutable data and certification labels for quadrature--generator co-design.

The module intentionally distinguishes exact/algebraic certificates, outward
interval certificates, verified floating candidates, and diagnostics.  A
floating solver status is never promoted to a proof.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping

import numpy as np
from scipy.spatial import cKDTree
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


class Certification(str, Enum):
    EXACT = "EXACT"
    OUTWARD_INTERVAL = "OUTWARD_INTERVAL"
    VERIFIED_FLOAT = "VERIFIED_FLOAT"
    DIAGNOSTIC = "DIAGNOSTIC"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class CertifiedValue:
    value: float
    certification: Certification
    lower: float | None = None
    upper: float | None = None
    note: str = ""

    def __post_init__(self) -> None:
        if not np.isfinite(self.value):
            raise ValueError("certified value must be finite")
        if self.lower is not None and (
            not np.isfinite(self.lower) or self.lower > self.value
        ):
            raise ValueError("invalid lower enclosure")
        if self.upper is not None and (
            not np.isfinite(self.upper) or self.value > self.upper
        ):
            raise ValueError("invalid upper enclosure")
        if (self.lower is None) != (self.upper is None):
            raise ValueError("an enclosure needs both endpoints")
        if (
            self.certification is Certification.OUTWARD_INTERVAL
            and self.lower is None
        ):
            raise ValueError("outward-interval certification needs an enclosure")

    @property
    def proved(self) -> bool:
        return self.certification in {
            Certification.EXACT, Certification.OUTWARD_INTERVAL
        }


@dataclass(frozen=True)
class CompactBox:
    """Closed parameter box; strict constraints use a positive margin."""

    lower: FloatArray
    upper: FloatArray
    names: tuple[str, ...]

    @classmethod
    def build(
        cls, lower: ArrayLike, upper: ArrayLike, names: Iterable[str]
    ) -> "CompactBox":
        lo = np.asarray(lower, dtype=float)
        hi = np.asarray(upper, dtype=float)
        labels = tuple(names)
        if lo.ndim != 1 or hi.shape != lo.shape or len(labels) != len(lo):
            raise ValueError("compact box arrays/names have incompatible shapes")
        if not np.all(np.isfinite(lo)) or not np.all(np.isfinite(hi)):
            raise ValueError("compact box endpoints must be finite")
        if np.any(lo > hi):
            raise ValueError("compact box has a reversed interval")
        return cls(lo.copy(), hi.copy(), labels)

    def contains(self, value: ArrayLike, tolerance: float = 0.0) -> bool:
        point = np.asarray(value, dtype=float)
        return bool(
            point.shape == self.lower.shape
            and np.all(point >= self.lower - tolerance)
            and np.all(point <= self.upper + tolerance)
        )


@dataclass(frozen=True)
class WeightedEdge:
    i: int
    j: int
    conductance: float | None = None


def canonicalize_weighted_edges(
    edges: Iterable[
        WeightedEdge | tuple[int, int] | tuple[int, int, float]
    ],
    node_count: int,
) -> tuple[IntArray, FloatArray | None]:
    """Canonicalize and aggregate duplicate undirected weighted edges."""

    accum: dict[tuple[int, int], float | None] = {}
    weighted: bool | None = None
    for raw in edges:
        if isinstance(raw, WeightedEdge):
            i, j, value = raw.i, raw.j, raw.conductance
        elif len(raw) == 2:
            i, j = int(raw[0]), int(raw[1])
            value = None
        else:
            i, j = int(raw[0]), int(raw[1])
            value = float(raw[2])
        if not (0 <= i < node_count and 0 <= j < node_count) or i == j:
            raise ValueError(f"invalid edge {(i, j)}")
        edge = (i, j) if i < j else (j, i)
        is_weighted = value is not None
        if weighted is None:
            weighted = is_weighted
        if weighted != is_weighted:
            raise ValueError("cannot mix weighted and unweighted edges")
        if value is not None and (not np.isfinite(value) or value < 0):
            raise ValueError("edge conductance must be finite and nonnegative")
        if edge not in accum:
            accum[edge] = value
        elif value is not None:
            assert accum[edge] is not None
            accum[edge] = float(accum[edge]) + value
    if not accum:
        raise ValueError("a candidate needs at least one edge")
    ordered = sorted(accum)
    edge_array = np.asarray(ordered, dtype=np.int64)
    if weighted:
        gamma = np.asarray([float(accum[e]) for e in ordered], dtype=float)
        return edge_array, gamma
    return edge_array, None


@dataclass(frozen=True)
class QuadratureCandidate:
    """One labelled outer candidate and its permitted graph.

    seed_conductance is a feasible incumbent only after an independent
    exact/interval or scale-aware residual audit.
    """

    family: str
    nodes: FloatArray
    weights: FloatArray
    edges: IntArray
    seed_conductance: FloatArray | None = field(default=None, repr=False)
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def build(
        cls,
        family: str,
        nodes: ArrayLike,
        weights: ArrayLike,
        edges: Iterable[
            WeightedEdge | tuple[int, int] | tuple[int, int, float]
        ],
        *,
        seed_conductance: ArrayLike | None = None,
        metadata: Mapping[str, Any] | None = None,
        unit_tolerance: float = 5e-12,
        mass_tolerance: float = 5e-12,
    ) -> "QuadratureCandidate":
        x = np.asarray(nodes, dtype=float)
        w = np.asarray(weights, dtype=float)
        if x.ndim != 2 or x.shape[1] != 3 or x.shape[0] < 2:
            raise ValueError("nodes must have shape (N,3), N>=2")
        if not np.all(np.isfinite(x)):
            raise ValueError("nodes contain a nonfinite value")
        if np.max(np.abs(np.linalg.norm(x, axis=1) - 1.0)) > unit_tolerance:
            raise ValueError("nodes are not unit vectors")
        duplicate_pairs = cKDTree(x).query_pairs(r=5.0 * unit_tolerance)
        if duplicate_pairs:
            raise ValueError(
                f"candidate contains duplicate/colliding nodes: "
                f"{sorted(duplicate_pairs)[:3]}"
            )
        if w.shape != (len(x),) or not np.all(np.isfinite(w)) or np.min(w) <= 0:
            raise ValueError("weights must be finite and strictly positive")
        if abs(float(np.sum(w)) - 1.0) > mass_tolerance:
            raise ValueError("weights must be normalized to total mass one")
        edge_array, embedded = canonicalize_weighted_edges(edges, len(x))
        if embedded is not None and seed_conductance is not None:
            raise ValueError("supply conductance either in edges or separately")
        gamma_raw = embedded if embedded is not None else seed_conductance
        gamma = None if gamma_raw is None else np.asarray(gamma_raw, dtype=float)
        if gamma is not None:
            if gamma.shape != (len(edge_array),):
                raise ValueError("seed conductance has the wrong shape")
            if not np.all(np.isfinite(gamma)) or np.min(gamma) < 0:
                raise ValueError("seed conductance must be finite and nonnegative")
            gamma = gamma.copy()
        x_out, w_out, edge_out = x.copy(), w.copy(), edge_array.copy()
        for array in (x_out, w_out, edge_out):
            array.setflags(write=False)
        if gamma is not None:
            gamma.setflags(write=False)
        return cls(
            str(family), x_out, w_out, edge_out, gamma,
            MappingProxyType(dict(metadata or {})),
        )

    @property
    def node_count(self) -> int:
        return int(len(self.nodes))

    @property
    def edge_count(self) -> int:
        return int(len(self.edges))

    @property
    def centered_residual(self) -> float:
        return float(np.linalg.norm(self.weights @ self.nodes))

    def rotated(self, rotation: ArrayLike) -> "QuadratureCandidate":
        q = np.asarray(rotation, dtype=float)
        if q.shape != (3, 3) or np.linalg.norm(q.T @ q - np.eye(3), ord=np.inf) > 1e-10:
            raise ValueError("rotation must be orthogonal")
        return QuadratureCandidate.build(
            self.family,
            self.nodes @ q.T,
            self.weights,
            [tuple(map(int, edge)) for edge in self.edges],
            seed_conductance=self.seed_conductance,
            metadata={**self.metadata, "joint_rotation": q.tolist()},
        )


@dataclass(frozen=True)
class FamilyDescriptor:
    name: str
    mass_rule: str
    admitted_graphs: tuple[str, ...]
    exactness_gate: str
    positivity_gate: str
    warning: str
    sampling_metric: str = "kappa_plus(G_l)=lambda_max/lambda_min_positive"
    feasibility_metric: str = "local barycentric margin plus global shared-edge LP margin"
    rotation_metric: str = "declared physical harmonic collision spread under fixed quadrature"


@dataclass(frozen=True)
class ApproachRecord:
    key: str
    family: str
    status: str
    mechanism: str
    blocker: str = ""

    def __post_init__(self) -> None:
        if self.status not in {"ACTIVE", "PROVED", "COMPUTATIONAL", "BLOCKED", "REJECTED"}:
            raise ValueError("invalid approach status")
        if self.status == "BLOCKED" and not self.blocker:
            raise ValueError("blocked routes require a concrete blocker")
