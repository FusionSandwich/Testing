"""Common P2E error, response, rotation, and cost records."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ResponseVector:
    scalar: float
    current: tuple[float, float, float]
    tensor: tuple[tuple[float, float, float], ...]
    q_normal: float
    response: float


@dataclass(frozen=True)
class ErrorVector:
    scalar: float
    current: float
    tensor: float
    q_normal: float
    response: float


def weighted_norm(value: ArrayLike, weights: ArrayLike) -> float:
    v = np.asarray(value, dtype=float)
    w = np.asarray(weights, dtype=float)
    return float(np.sqrt(np.sum(w * np.abs(v) ** 2)))


def response_from_angular(
    angular: ArrayLike,
    nodes: ArrayLike,
    weights: ArrayLike,
    normal: ArrayLike,
    *,
    response_direction: ArrayLike | None = None,
) -> ResponseVector:
    psi = np.asarray(angular, dtype=float)
    x = np.asarray(nodes, dtype=float)
    w = np.asarray(weights, dtype=float)
    n = np.asarray(normal, dtype=float)
    n /= np.linalg.norm(n)
    scalar = float(w @ psi)
    current = np.sum(w[:, None] * psi[:, None] * x, axis=0)
    second = np.einsum("d,di,dj->ij", w * psi, x, x)
    tensor = second - scalar * np.eye(3) / 3.0
    qn = float(n @ tensor @ n)
    direction = n if response_direction is None else np.asarray(response_direction, dtype=float)
    direction /= np.linalg.norm(direction)
    response = float(0.35 * scalar + 0.25 * direction @ current + 0.40 * direction @ tensor @ direction)
    return ResponseVector(
        scalar,
        tuple(map(float, current)),
        tuple(tuple(map(float, row)) for row in tensor),
        qn,
        response,
    )


def response_error(value: ResponseVector, reference: ResponseVector) -> ErrorVector:
    current = np.asarray(value.current) - np.asarray(reference.current)
    tensor = np.asarray(value.tensor) - np.asarray(reference.tensor)
    return ErrorVector(
        abs(value.scalar - reference.scalar),
        float(np.linalg.norm(current)),
        float(np.linalg.norm(tensor, ord="fro")),
        abs(value.q_normal - reference.q_normal),
        abs(value.response - reference.response),
    )


def relative(value: float, reference: float, floor: float = 1e-14) -> float:
    return float(abs(value) / max(floor, abs(reference)))


def aggregate_error(error: ErrorVector, reference: ResponseVector) -> float:
    scales = np.asarray(
        [
            max(abs(reference.scalar), 1e-10),
            max(np.linalg.norm(reference.current), 1e-10),
            max(np.linalg.norm(reference.tensor), 1e-10),
            max(abs(reference.q_normal), 1e-10),
            max(abs(reference.response), 1e-10),
        ]
    )
    values = np.asarray([error.scalar, error.current, error.tensor, error.q_normal, error.response])
    return float(np.linalg.norm(values / scales) / math.sqrt(len(values)))


def rotation_spread(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(max(values) - min(values))


def equal_cost_record(
    baseline_error: float,
    optimized_error: float,
    baseline_time: float,
    optimized_time: float,
    direction_count: int,
) -> dict[str, Any]:
    target = min(baseline_error, optimized_error)
    return {
        "equal_direction_count": {
            "directions": int(direction_count),
            "baseline_error": float(baseline_error),
            "optimized_error": float(optimized_error),
            "optimized_to_baseline_ratio": float(optimized_error / max(baseline_error, 1e-30)),
        },
        "equal_wall_time": {
            "budget_seconds": float(max(baseline_time, optimized_time)),
            "baseline_error": float(baseline_error),
            "optimized_error": float(optimized_error),
            "is_true_equal_time_allocation_experiment": False,
            "note": (
                "compatibility field only: both one-shot same-node executions fit "
                "inside the larger observed runtime; no work was reallocated to fill "
                "a common wall-time budget"
            ),
        },
        "wall_time_at_equal_response_error": {
            "target_error": float(target),
            "baseline_seconds": float(baseline_time) if baseline_error <= target * (1 + 1e-12) else None,
            "optimized_seconds": float(optimized_time) if optimized_error <= target * (1 + 1e-12) else None,
            "baseline_status": "reached" if baseline_error <= target * (1 + 1e-12) else "not_reached_same_nodes",
            "optimized_status": "reached" if optimized_error <= target * (1 + 1e-12) else "not_reached_same_nodes",
        },
    }


def dataclass_dict(value: Any) -> Any:
    return asdict(value) if hasattr(value, "__dataclass_fields__") else value
