"""Positive finite-volume space--angle transport in a one-dimensional slab."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal

import numpy as np

from .angular import AngularOperator, apply_generator

BoundaryFunction = Callable[[float, np.ndarray], np.ndarray]
SourceFunction = Callable[[float, np.ndarray, np.ndarray], np.ndarray]
Integrator = Literal["euler", "ssprk2"]


class SlabTransportError(ValueError):
    """Raised when a slab model or state violates the numerical contract."""


@dataclass(frozen=True)
class SlabGrid:
    left: float
    right: float
    cells: int

    def __post_init__(self) -> None:
        if not np.isfinite(self.left) or not np.isfinite(self.right):
            raise SlabTransportError("grid bounds must be finite")
        if not self.left < self.right:
            raise SlabTransportError("grid left bound must be smaller than right bound")
        if self.cells < 1:
            raise SlabTransportError("grid must contain at least one cell")

    @property
    def dx(self) -> float:
        return (self.right - self.left) / self.cells

    @property
    def centers(self) -> np.ndarray:
        return self.left + (np.arange(self.cells, dtype=float) + 0.5) * self.dx


@dataclass(frozen=True)
class BoundaryData:
    left: BoundaryFunction
    right: BoundaryFunction

    @staticmethod
    def vacuum() -> "BoundaryData":
        def zero(_time: float, mu: np.ndarray) -> np.ndarray:
            return np.zeros_like(mu, dtype=float)

        return BoundaryData(left=zero, right=zero)


@dataclass(frozen=True)
class BalanceRates:
    inventory_derivative: float
    boundary_net: float
    source: float
    absorption: float
    collision: float
    closure_error: float


@dataclass(frozen=True)
class StepDiagnostics:
    time: float
    dt: float
    inventory_before: float
    inventory_after: float
    predicted_change: float
    balance_error: float
    minimum_value: float


@dataclass
class SlabModel:
    grid: SlabGrid
    angular: AngularOperator
    absorption: np.ndarray
    angular_diffusion: np.ndarray
    boundary: BoundaryData
    source: SourceFunction | None = None

    def __post_init__(self) -> None:
        self.absorption = self._coefficient(self.absorption, "absorption")
        self.angular_diffusion = self._coefficient(
            self.angular_diffusion, "angular_diffusion"
        )

    def _coefficient(self, value: np.ndarray, name: str) -> np.ndarray:
        array = np.asarray(value, dtype=float)
        if array.shape != (self.grid.cells,):
            raise SlabTransportError(
                f"{name} must have shape {(self.grid.cells,)}, got {array.shape}"
            )
        if not np.all(np.isfinite(array)) or np.min(array) < 0.0:
            raise SlabTransportError(f"{name} must be finite and nonnegative")
        return array.copy()

    @property
    def shape(self) -> tuple[int, int]:
        return self.grid.cells, self.angular.count

    @property
    def mu(self) -> np.ndarray:
        return self.angular.mu_x

    def validate_state(self, state: np.ndarray, *, nonnegative: bool = False) -> np.ndarray:
        data = np.asarray(state, dtype=float)
        if data.shape != self.shape:
            raise SlabTransportError(f"state must have shape {self.shape}, got {data.shape}")
        if not np.all(np.isfinite(data)):
            raise SlabTransportError("state contains NaN or infinity")
        if nonnegative and float(np.min(data)) < -1.0e-13:
            raise SlabTransportError("state contains a negative value")
        return data

    def boundary_values(self, time: float) -> tuple[np.ndarray, np.ndarray]:
        left = np.asarray(self.boundary.left(time, self.mu.copy()), dtype=float)
        right = np.asarray(self.boundary.right(time, self.mu.copy()), dtype=float)
        if left.shape != (self.angular.count,) or right.shape != (self.angular.count,):
            raise SlabTransportError("boundary functions must return one value per direction")
        if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):
            raise SlabTransportError("boundary data contain NaN or infinity")
        return left, right

    def source_values(self, time: float) -> np.ndarray:
        if self.source is None:
            return np.zeros(self.shape, dtype=float)
        values = np.asarray(
            self.source(time, self.grid.centers.copy(), self.mu.copy()), dtype=float
        )
        if values.shape != self.shape:
            raise SlabTransportError(
                f"source must return shape {self.shape}, got {values.shape}"
            )
        if not np.all(np.isfinite(values)):
            raise SlabTransportError("source contains NaN or infinity")
        return values

    def streaming_rhs(self, state: np.ndarray, time: float) -> np.ndarray:
        psi = self.validate_state(state)
        left, right = self.boundary_values(time)
        rhs = np.zeros_like(psi)
        positive = self.mu > 0.0
        negative = self.mu < 0.0

        if np.any(positive):
            upwind = np.empty((self.grid.cells, int(np.sum(positive))), dtype=float)
            upwind[0] = left[positive]
            upwind[1:] = psi[:-1, positive]
            rhs[:, positive] = (
                -self.mu[positive][None, :] * (psi[:, positive] - upwind) / self.grid.dx
            )
        if np.any(negative):
            upwind = np.empty((self.grid.cells, int(np.sum(negative))), dtype=float)
            upwind[:-1] = psi[1:, negative]
            upwind[-1] = right[negative]
            rhs[:, negative] = (
                -self.mu[negative][None, :] * (upwind - psi[:, negative]) / self.grid.dx
            )
        return rhs

    def collision_rhs(self, state: np.ndarray) -> np.ndarray:
        psi = self.validate_state(state)
        return self.angular_diffusion[:, None] * apply_generator(
            self.angular, psi.T
        ).T

    def rhs(self, state: np.ndarray, time: float) -> np.ndarray:
        psi = self.validate_state(state)
        return (
            self.streaming_rhs(psi, time)
            + self.collision_rhs(psi)
            - self.absorption[:, None] * psi
            + self.source_values(time)
        )

    def stable_timestep(self, cfl: float = 1.0) -> float:
        """Return the sharp positivity CFL for the forward-Euler splitting row."""

        if not 0.0 < cfl <= 1.0:
            raise SlabTransportError("cfl must lie in (0, 1]")
        removal = (
            np.abs(self.mu)[None, :] / self.grid.dx
            + self.angular_diffusion[:, None] * self.angular.rate[None, :]
            + self.absorption[:, None]
        )
        maximum = float(np.max(removal))
        if maximum <= 0.0:
            return math.inf
        return cfl / maximum

    def euler_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        if not np.isfinite(dt) or dt <= 0.0:
            raise SlabTransportError("dt must be finite and positive")
        return self.validate_state(state) + dt * self.rhs(state, time)

    def ssprk2_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        first = self.euler_step(state, time, dt)
        second_euler = first + dt * self.rhs(first, time + dt)
        return 0.5 * self.validate_state(state) + 0.5 * second_euler

    def step(
        self,
        state: np.ndarray,
        time: float,
        dt: float,
        *,
        integrator: Integrator = "ssprk2",
    ) -> np.ndarray:
        if integrator == "euler":
            return self.euler_step(state, time, dt)
        if integrator == "ssprk2":
            return self.ssprk2_step(state, time, dt)
        raise SlabTransportError(f"unknown integrator {integrator!r}")

    def inventory(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(self.grid.dx * np.sum(psi * self.angular.weights[None, :]))

    def scalar_flux(self, state: np.ndarray) -> np.ndarray:
        psi = self.validate_state(state)
        return np.sum(psi * self.angular.weights[None, :], axis=1)

    def boundary_currents(self, state: np.ndarray, time: float) -> dict[str, float]:
        psi = self.validate_state(state)
        left, right = self.boundary_values(time)
        positive = self.mu > 0.0
        negative = self.mu < 0.0
        weights = self.angular.weights
        return {
            "left_in": float(np.sum(weights[positive] * self.mu[positive] * left[positive])),
            "left_out": float(
                np.sum(weights[negative] * (-self.mu[negative]) * psi[0, negative])
            ),
            "right_in": float(
                np.sum(weights[negative] * (-self.mu[negative]) * right[negative])
            ),
            "right_out": float(
                np.sum(weights[positive] * self.mu[positive] * psi[-1, positive])
            ),
        }

    def absorption_rate(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(
            self.grid.dx
            * np.sum(
                self.absorption[:, None] * psi * self.angular.weights[None, :]
            )
        )

    def source_rate(self, time: float) -> float:
        source = self.source_values(time)
        return float(self.grid.dx * np.sum(source * self.angular.weights[None, :]))

    def collision_integral(self, state: np.ndarray) -> float:
        collision = self.collision_rhs(state)
        return float(self.grid.dx * np.sum(collision * self.angular.weights[None, :]))

    def balance_rates(self, state: np.ndarray, time: float) -> BalanceRates:
        psi = self.validate_state(state)
        derivative = float(
            self.grid.dx * np.sum(self.rhs(psi, time) * self.angular.weights[None, :])
        )
        current = self.boundary_currents(psi, time)
        boundary_net = (
            current["left_in"]
            + current["right_in"]
            - current["left_out"]
            - current["right_out"]
        )
        source = self.source_rate(time)
        absorption = self.absorption_rate(psi)
        collision = self.collision_integral(psi)
        predicted = boundary_net + source - absorption + collision
        return BalanceRates(
            inventory_derivative=derivative,
            boundary_net=boundary_net,
            source=source,
            absorption=absorption,
            collision=collision,
            closure_error=derivative - predicted,
        )

    def advance(
        self,
        initial: np.ndarray,
        final_time: float,
        *,
        cfl: float = 0.9,
        integrator: Integrator = "ssprk2",
        dt_max: float | None = None,
        enforce_nonnegative: bool = False,
    ) -> tuple[np.ndarray, list[StepDiagnostics]]:
        if final_time < 0.0:
            raise SlabTransportError("final_time must be nonnegative")
        state = self.validate_state(initial, nonnegative=enforce_nonnegative).copy()
        if final_time == 0.0:
            return state, []
        limit = self.stable_timestep(cfl)
        if dt_max is not None:
            if dt_max <= 0.0 or not np.isfinite(dt_max):
                raise SlabTransportError("dt_max must be finite and positive")
            limit = min(limit, dt_max)
        if not np.isfinite(limit):
            limit = final_time
        steps = max(1, math.ceil(final_time / limit))
        dt = final_time / steps
        diagnostics: list[StepDiagnostics] = []
        time = 0.0
        for _ in range(steps):
            before = self.inventory(state)
            rates = self.balance_rates(state, time)
            updated = self.step(state, time, dt, integrator=integrator)
            after = self.inventory(updated)
            predicted = dt * rates.inventory_derivative
            diagnostics.append(
                StepDiagnostics(
                    time=time,
                    dt=dt,
                    inventory_before=before,
                    inventory_after=after,
                    predicted_change=predicted,
                    balance_error=(after - before) - predicted,
                    minimum_value=float(np.min(updated)),
                )
            )
            state = updated
            time += dt
            if enforce_nonnegative and float(np.min(state)) < -2.0e-12:
                raise SlabTransportError(
                    f"positivity violation at t={time}: {float(np.min(state)):.3e}"
                )
        return state, diagnostics
