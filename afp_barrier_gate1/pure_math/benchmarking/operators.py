"""Frozen same-node production, baseline, ablation, and reference operators."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from pure_math.acceleration.transport import (
    audit_generator,
    dense_centered_generator,
    generator_from_edges,
    weighted_harmonic_frame,
    weighted_spectral_operator,
)

FloatArray = NDArray[np.float64]


def _strict(payload: object) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _path() -> Path:
    return Path(__file__).with_name("P2E_FROZEN_OPERATOR_REGISTRY.json")


@dataclass(frozen=True)
class FrozenOperators:
    nodes: FloatArray
    weights: FloatArray
    matrices: dict[str, FloatArray]
    registry: dict[str, Any]

    def audit(self, name: str) -> dict[str, Any]:
        report = audit_generator(name, self.nodes, self.weights, self.matrices[name])
        return {
            "h0_residual": report.h0_residual,
            "h1_residual": report.h1_residual,
            "reversibility_residual": report.reversibility_residual,
            "minimum_offdiagonal": report.minimum_offdiagonal,
            "rate_max": report.rate_max,
            "shell_defects": report.shell_defects,
            "positive": report.positive,
        }


def load_registry(path: str | Path | None = None) -> dict[str, Any]:
    source = _path() if path is None else Path(path)
    payload = json.loads(
        source.read_text(encoding="utf-8"),
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )
    claimed = str(payload.pop("scientific_sha256"))
    actual = hashlib.sha256(_strict(payload).encode("utf-8")).hexdigest()
    payload["scientific_sha256"] = claimed
    if actual != claimed:
        raise ArithmeticError(f"P2E operator registry hash mismatch: {actual} != {claimed}")
    return payload


def _signed_reference(nodes: FloatArray, weights: FloatArray) -> FloatArray:
    frame = weighted_harmonic_frame(nodes, weights, maximum_degree=15)
    eigenvalues = -frame.degrees.astype(float) * (frame.degrees.astype(float) + 1.0)
    return weighted_spectral_operator(frame, eigenvalues)


def load_frozen_operators(path: str | Path | None = None) -> FrozenOperators:
    payload = load_registry(path)
    nodes = np.asarray(payload["nodes"], dtype=float)
    weights = np.asarray(payload["weights"], dtype=float)
    matrices: dict[str, FloatArray] = {}
    for name, row in payload["methods"].items():
        if "alias_of" in row:
            continue
        if "edges" in row and "gamma" in row:
            matrices[name] = generator_from_edges(
                weights,
                np.asarray(row["edges"], dtype=np.int64),
                np.asarray(row["gamma"], dtype=float),
            )
    matrices["no_h2_objective"] = matrices["moment_monotone_baseline"].copy()
    matrices["h2_poor_positive"] = dense_centered_generator(nodes, weights)
    matrices["signed_higher_accuracy"] = _signed_reference(nodes, weights)
    required = {
        "moment_monotone_baseline",
        "optimized_harmonic_fidelity",
        "remove_rotation_penalty",
        "remove_rate_cap",
        "alter_graph_locality",
        "no_h2_objective",
        "h2_poor_positive",
        "signed_higher_accuracy",
    }
    if not required.issubset(matrices):
        raise ArithmeticError(f"operator registry incomplete: {sorted(required - matrices.keys())}")
    # Fail closed on production invariants.
    for name in required - {"signed_higher_accuracy"}:
        audit = audit_generator(name, nodes, weights, matrices[name], degrees=(2, 3, 4, 5, 6))
        if (
            audit.h0_residual > 5e-10
            or audit.h1_residual > 5e-9
            or audit.reversibility_residual > 5e-10
            or not audit.positive
        ):
            raise ArithmeticError(f"frozen positive operator failed audit: {name}: {audit}")
    return FrozenOperators(nodes, weights, matrices, payload)
