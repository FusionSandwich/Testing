"""Deterministic commuting and noncommuting P2D audit fixtures."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class AccelerationFixture:
    name: str
    high: FloatArray
    optimized_low: FloatArray
    baseline_low: FloatArray
    classical_low: FloatArray
    poor_low: FloatArray
    rhs: FloatArray
    shell_high: FloatArray
    shell_optimized: FloatArray
    shell_baseline: FloatArray


def commuting_shell_fixture() -> AccelerationFixture:
    # Absorption makes the H0 block invertible.  Entries correspond to H0-H5.
    high_shell = np.asarray([0.2, 2.2, 6.2, 12.2, 20.2, 30.2])
    optimized = np.asarray([0.2, 2.2, 6.28, 12.8, 22.0, 34.0])
    baseline = np.asarray([0.2, 2.2, 7.4, 16.0, 27.0, 42.0])
    poor = np.asarray([0.2, 2.2, 11.0, 15.0, 20.5, 31.0])
    rhs = np.asarray([1.0, -0.4, 0.8, 0.3, -0.2, 0.1])
    return AccelerationFixture(
        "commuting_shell",
        np.diag(high_shell),
        np.diag(optimized),
        np.diag(baseline),
        np.diag(np.asarray([0.2, 2.2, 6.6, 13.5, 22.5, 34.5])),
        np.diag(poor),
        rhs,
        high_shell,
        optimized,
        baseline,
    )


def noncommuting_streaming_fixture() -> AccelerationFixture:
    # A two-cell upwind-like block coupled to four angular modes.
    angular_high = np.diag([0.3, 2.3, 6.3, 12.3])
    angular_opt = np.diag([0.3, 2.3, 6.45, 12.9])
    angular_base = np.diag([0.3, 2.3, 7.4, 15.4])
    angular_classical = np.diag([0.3, 2.3, 6.75, 13.8])
    angular_poor = np.diag([0.3, 2.3, 10.2, 12.8])
    streaming = np.asarray([[1.4, -0.9], [-0.2, 1.1]])
    mu = np.diag([1.0, 0.45, -0.35, -0.9])
    high = np.kron(streaming, mu) + np.kron(np.eye(2), angular_high)
    optimized = np.kron(streaming, mu) + np.kron(np.eye(2), angular_opt)
    baseline = np.kron(streaming, mu) + np.kron(np.eye(2), angular_base)
    classical = np.kron(streaming, mu) + np.kron(np.eye(2), angular_classical)
    poor = np.kron(streaming, mu) + np.kron(np.eye(2), angular_poor)
    rhs = np.linspace(0.2, 1.0, 8)
    return AccelerationFixture(
        "noncommuting_streaming",
        high,
        optimized,
        baseline,
        classical,
        poor,
        rhs,
        np.diag(angular_high),
        np.diag(angular_opt),
        np.diag(angular_base),
    )


def higher_shell_adversarial_fixture() -> AccelerationFixture:
    high_shell = np.asarray([0.1, 2.1, 6.1, 12.1, 20.1, 30.1, 42.1])
    optimized = np.asarray([0.1, 2.1, 6.12, 18.0, 35.0, 55.0, 78.0])
    baseline = np.asarray([0.1, 2.1, 7.0, 12.5, 21.0, 31.5, 44.0])
    classical = np.asarray([0.1, 2.1, 6.35, 14.0, 25.0, 38.0, 53.0])
    poor = np.asarray([0.1, 2.1, 12.0, 12.2, 20.5, 30.5, 42.5])
    rhs = np.asarray([0.0, 0.0, 0.0, 0.1, -0.4, 1.0, -0.8])
    return AccelerationFixture(
        "higher_shell_adversarial",
        np.diag(high_shell),
        np.diag(optimized),
        np.diag(baseline),
        np.diag(classical),
        np.diag(poor),
        rhs,
        high_shell,
        optimized,
        baseline,
    )


def multigroup_boundary_fixture() -> AccelerationFixture:
    """Two-energy/two-cell noncommuting fixture with downscatter and inflow."""

    angular_high = np.diag([0.25, 2.25, 6.25])
    angular_opt = np.diag([0.25, 2.25, 6.36])
    angular_base = np.diag([0.25, 2.25, 7.15])
    angular_classical = np.diag([0.25, 2.25, 6.55])
    angular_poor = np.diag([0.25, 2.25, 9.5])
    streaming = np.asarray([[1.25, -0.72], [-0.18, 1.05]])
    mu = np.diag([0.9, 0.15, -0.8])
    spatial_high = np.kron(streaming, mu) + np.kron(np.eye(2), angular_high)
    spatial_opt = np.kron(streaming, mu) + np.kron(np.eye(2), angular_opt)
    spatial_base = np.kron(streaming, mu) + np.kron(np.eye(2), angular_base)
    spatial_classical = np.kron(streaming, mu) + np.kron(np.eye(2), angular_classical)
    spatial_poor = np.kron(streaming, mu) + np.kron(np.eye(2), angular_poor)
    group_loss = np.asarray([[0.30, 0.0], [-0.22, 0.18]])
    identity = np.eye(spatial_high.shape[0])
    high = np.kron(np.eye(2), spatial_high) + np.kron(group_loss, identity)
    optimized = np.kron(np.eye(2), spatial_opt) + np.kron(group_loss, identity)
    baseline = np.kron(np.eye(2), spatial_base) + np.kron(group_loss, identity)
    classical = np.kron(np.eye(2), spatial_classical) + np.kron(group_loss, identity)
    poor = np.kron(np.eye(2), spatial_poor) + np.kron(group_loss, identity)
    rhs = np.zeros(len(high))
    rhs[:3] = np.asarray([1.0, 0.35, 0.0])  # left-inflow/source block
    rhs[6:9] = np.asarray([0.18, 0.05, 0.0])
    return AccelerationFixture(
        "multigroup_boundary",
        high,
        optimized,
        baseline,
        classical,
        poor,
        rhs,
        np.diag(angular_high),
        np.diag(angular_opt),
        np.diag(angular_base),
    )
