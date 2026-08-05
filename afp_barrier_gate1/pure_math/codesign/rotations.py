"""Rotation metrics that keep collision bias, covariance, and rays separate."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Callable, Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray

from pure_math.optimization import degree_two_basis

from .metrics import to_graph
from .types import QuadratureCandidate

FloatArray = NDArray[np.float64]


def signed_permutation_rotations() -> tuple[FloatArray, ...]:
    output: list[FloatArray] = []
    for perm in permutations(range(3)):
        base = np.eye(3)[list(perm)]
        for signs in product((-1.0, 1.0), repeat=3):
            value = np.diag(signs) @ base
            if np.linalg.det(value) > 0.5:
                output.append(value)
    output.sort(key=lambda q: tuple(q.reshape(-1)))
    if len(output) != 24:
        raise AssertionError("proper signed-permutation group must have order 24")
    return tuple(output)


def axis_angle(axis: ArrayLike, angle: float) -> FloatArray:
    vector = np.asarray(axis, dtype=float)
    vector /= np.linalg.norm(vector)
    x, y, z = vector
    cross = np.asarray([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    return (
        np.eye(3) * np.cos(angle)
        + (1.0 - np.cos(angle)) * np.outer(vector, vector)
        + np.sin(angle) * cross
    )


def _quadratic_matrix(coefficients: ArrayLike) -> FloatArray:
    value = np.asarray(coefficients, dtype=float)
    basis = degree_two_basis()
    if value.shape != (len(basis),):
        raise ValueError("degree-two coefficient vector has the wrong shape")
    norm = float(np.linalg.norm(value))
    if norm == 0:
        raise ValueError("rotation probe cannot be zero")
    return np.tensordot(value / norm, basis, axes=(0, 0))


def collision_probe_value(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    coefficients: ArrayLike,
    rotation: ArrayLike,
    *,
    denominator_floor: float = 1e-12,
) -> float:
    """Rotate one physical H2 probe relative to a fixed quadrature."""

    q = np.asarray(rotation, dtype=float)
    a = _quadratic_matrix(coefficients)
    rotated = q @ a @ q.T
    samples = np.einsum("ni,ij,nj->n", candidate.nodes, rotated, candidate.nodes)
    graph = to_graph(candidate)
    residual = (graph.generator(gamma) + 6.0 * np.eye(candidate.node_count)) @ samples
    denominator = float(np.sqrt(np.sum(candidate.weights * samples**2)))
    if denominator <= denominator_floor:
        raise ValueError("rotated probe approaches a sampling alias")
    numerator = float(np.sqrt(np.sum(candidate.weights * residual**2)))
    return numerator / denominator


@dataclass(frozen=True)
class RotationSpread:
    minimum: float
    maximum: float
    absolute_spread: float
    relative_spread: float
    sample_count: int
    scope: str


def collision_rotation_spread(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    coefficients: ArrayLike,
    rotations: Iterable[ArrayLike],
) -> RotationSpread:
    values = [
        collision_probe_value(candidate, gamma, coefficients, q)
        for q in rotations
    ]
    minimum, maximum = min(values), max(values)
    return RotationSpread(
        minimum,
        maximum,
        maximum - minimum,
        (maximum - minimum) / max(1e-15, minimum),
        len(values),
        "COLLISION_ONLY_PHYSICAL_ROTATION_FIXED_QUADRATURE",
    )


def joint_collision_covariance_defect(
    candidate: QuadratureCandidate,
    gamma: ArrayLike,
    coefficients: ArrayLike,
    rotations: Iterable[ArrayLike],
) -> float:
    """Rotate nodes and physical quadratic together; this is a covariance test."""

    baseline = collision_probe_value(
        candidate, gamma, coefficients, np.eye(3)
    )
    a = _quadratic_matrix(coefficients)
    basis = degree_two_basis()
    defects = []
    for rotation in rotations:
        q = np.asarray(rotation, dtype=float)
        rotated_candidate = candidate.rotated(q)
        # Co-rotating A gives q A q^T.  Express it in the frozen basis; the
        # relative call uses identity because the physical coefficient itself
        # has already been transformed.
        rotated_a = q @ a @ q.T
        rotated_coefficients = np.asarray(
            [float(np.sum(b * rotated_a)) for b in basis]
        )
        value = collision_probe_value(
            rotated_candidate, gamma, rotated_coefficients, np.eye(3)
        )
        defects.append(abs(value - baseline))
    return max(defects, default=0.0)


def application_rotation_spread(
    rotations: Iterable[ArrayLike],
    response: Callable[[FloatArray, bool], float],
    *,
    joint: bool,
) -> RotationSpread:
    """Evaluate a declared transport response.

    response(Q, False) rotates the physical problem relative to a fixed
    quadrature.  response(Q, True) must co-rotate quadrature, geometry, and
    spatial mesh.  The caller, not this wrapper, supplies the transport model.
    """

    values = [float(response(np.asarray(q, dtype=float), joint)) for q in rotations]
    if any(not np.isfinite(value) for value in values):
        raise ValueError("rotation response contains a nonfinite value")
    minimum, maximum = min(values), max(values)
    return RotationSpread(
        minimum,
        maximum,
        maximum - minimum,
        (maximum - minimum) / max(1e-15, abs(minimum)),
        len(values),
        "JOINT_COVARIANCE" if joint else "PHYSICAL_ROTATION_FIXED_QUADRATURE",
    )


@dataclass(frozen=True)
class RotationNetEnclosure:
    sampled_minimum: float
    sampled_maximum: float
    lower: float
    upper: float
    lipschitz_constant: float
    cover_radius: float


def enclose_rotation_extrema(
    values: ArrayLike,
    *,
    lipschitz_constant: float,
    cover_radius: float,
) -> RotationNetEnclosure:
    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or len(sample) == 0 or not np.all(np.isfinite(sample)):
        raise ValueError("rotation samples must be a finite nonempty vector")
    if lipschitz_constant < 0 or cover_radius < 0:
        raise ValueError("Lipschitz data must be nonnegative")
    correction = lipschitz_constant * cover_radius
    return RotationNetEnclosure(
        float(np.min(sample)), float(np.max(sample)),
        float(np.min(sample) - correction),
        float(np.max(sample) + correction),
        float(lipschitz_constant), float(cover_radius),
    )


@dataclass(frozen=True)
class InterpolationAudit:
    constants_residual: float
    positivity_margin: float
    mass_residual: float
    first_moment_residual: float
    operator_norm: float
    passed: bool
    scope: str = "SEPARATE_STREAMING_REMEDY"


def audit_rotation_interpolation(
    interpolation: ArrayLike,
    source: QuadratureCandidate,
    target: QuadratureCandidate,
    *,
    tolerance: float = 2e-10,
) -> InterpolationAudit:
    matrix = np.asarray(interpolation, dtype=float)
    if matrix.shape != (target.node_count, source.node_count):
        raise ValueError("interpolation matrix has the wrong shape")
    constants = float(
        np.linalg.norm(matrix @ np.ones(source.node_count) - np.ones(target.node_count), ord=np.inf)
    )
    positivity = float(np.min(matrix))
    mass = float(np.linalg.norm(target.weights @ matrix - source.weights, ord=np.inf))
    moments = float(np.linalg.norm(matrix @ source.nodes - target.nodes, ord=np.inf))
    norm = float(np.linalg.norm(matrix, ord=2))
    passed = (
        constants <= tolerance
        and positivity >= -tolerance
        and mass <= tolerance
        and moments <= tolerance
    )
    return InterpolationAudit(constants, positivity, mass, moments, norm, passed)
