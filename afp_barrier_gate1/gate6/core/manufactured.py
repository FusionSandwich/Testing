"""Manufactured solutions for space--angle slab transport."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .slab import BoundaryData, SourceFunction


@dataclass(frozen=True)
class CoordinateModeManufactured:
    """Positive manufactured solution using an exact degree-one angular mode.

    The continuum problem is

      d_t psi + mu d_x psi = kappa Delta_S2 psi - sigma_a psi + q.

    With

      psi = 1 + amplitude * exp(-omega t) * sin(pi x/L) * mu,

    the angular term is exact for every degree-one-preserving AFP operator.
    Consequently, this benchmark isolates streaming, boundaries, material
    coefficients, and time integration rather than conflating them with angular
    approximation error.
    """

    left: float
    right: float
    amplitude: float = 0.2
    omega: float = 0.7
    absorption: float = 0.15
    angular_diffusion: float = 0.25

    def __post_init__(self) -> None:
        if not self.left < self.right:
            raise ValueError("invalid manufactured domain")
        if not 0.0 <= self.amplitude < 1.0:
            raise ValueError("amplitude must lie in [0, 1)")
        for name, value in (
            ("omega", self.omega),
            ("absorption", self.absorption),
            ("angular_diffusion", self.angular_diffusion),
        ):
            if value < 0.0 or not np.isfinite(value):
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def length(self) -> float:
        return self.right - self.left

    def exact(self, time: float, x: np.ndarray, mu: np.ndarray) -> np.ndarray:
        space = np.sin(np.pi * (x - self.left) / self.length)
        decay = np.exp(-self.omega * time)
        return 1.0 + self.amplitude * decay * space[:, None] * mu[None, :]

    def source(self) -> SourceFunction:
        def evaluate(time: float, x: np.ndarray, mu: np.ndarray) -> np.ndarray:
            phase = np.pi * (x - self.left) / self.length
            decay = np.exp(-self.omega * time)
            perturbation = (
                self.amplitude * decay * np.sin(phase)[:, None] * mu[None, :]
            )
            time_term = -self.omega * perturbation
            streaming = (
                self.amplitude
                * decay
                * (np.pi / self.length)
                * np.cos(phase)[:, None]
                * mu[None, :] ** 2
            )
            collision_moved_to_source = 2.0 * self.angular_diffusion * perturbation
            absorption_moved_to_source = self.absorption * (1.0 + perturbation)
            return (
                time_term
                + streaming
                + collision_moved_to_source
                + absorption_moved_to_source
            )

        return evaluate

    def boundary(self) -> BoundaryData:
        def left(time: float, mu: np.ndarray) -> np.ndarray:
            x = np.asarray([self.left], dtype=float)
            return self.exact(time, x, mu)[0]

        def right(time: float, mu: np.ndarray) -> np.ndarray:
            x = np.asarray([self.right], dtype=float)
            return self.exact(time, x, mu)[0]

        return BoundaryData(left=left, right=right)
