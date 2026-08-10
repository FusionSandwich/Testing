"""Conservative multigroup space--angle transport in a one-dimensional slab."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Literal

import numpy as np

from .angular import AngularOperator, apply_generator
from .slab import SlabGrid, SlabTransportError

GroupBoundaryFunction = Callable[[float, np.ndarray, np.ndarray], np.ndarray]
GroupSourceFunction = Callable[[float, np.ndarray, np.ndarray, np.ndarray], np.ndarray]
MultigroupIntegrator = Literal["euler", "ssprk2", "strang"]


@dataclass(frozen=True)
class EnergyGroups:
    """Representative group energies and normalized streaming speeds."""

    energies: tuple[float, ...]
    speeds: tuple[float, ...]

    def __post_init__(self) -> None:
        energy = np.asarray(self.energies, dtype=float)
        speed = np.asarray(self.speeds, dtype=float)
        if energy.ndim != 1 or len(energy) == 0 or speed.shape != energy.shape:
            raise ValueError("energies and speeds must be equal nonempty vectors")
        if not np.all(np.isfinite(energy)) or not np.all(np.isfinite(speed)):
            raise ValueError("energies and speeds must be finite")
        if np.min(energy) <= 0.0 or np.min(speed) < 0.0:
            raise ValueError("energies must be positive and speeds nonnegative")
        if np.any(np.diff(energy) >= 0.0):
            raise ValueError("group energies must be strictly descending")

    @property
    def count(self) -> int:
        return len(self.energies)

    @property
    def energy_array(self) -> np.ndarray:
        return np.asarray(self.energies, dtype=float)

    @property
    def speed_array(self) -> np.ndarray:
        return np.asarray(self.speeds, dtype=float)


@dataclass(frozen=True)
class MultigroupBoundaryData:
    left: GroupBoundaryFunction
    right: GroupBoundaryFunction

    @staticmethod
    def vacuum() -> "MultigroupBoundaryData":
        def zero(_time: float, energies: np.ndarray, mu: np.ndarray) -> np.ndarray:
            return np.zeros((len(energies), len(mu)), dtype=float)

        return MultigroupBoundaryData(left=zero, right=zero)


@dataclass(frozen=True)
class MultigroupBalanceRates:
    particle_derivative: float
    particle_boundary_net: float
    particle_source: float
    particle_absorption: float
    particle_transfer: float
    particle_collision: float
    particle_closure_error: float
    energy_derivative: float
    energy_boundary_net: float
    energy_source: float
    absorption_deposition: float
    transfer_deposition: float
    energy_collision: float
    energy_closure_error: float


@dataclass(frozen=True)
class MultigroupStepDiagnostics:
    time: float
    dt: float
    particle_before: float
    particle_after: float
    energy_before: float
    energy_after: float
    particle_balance_error: float
    energy_balance_error: float
    minimum_value: float


@dataclass
class MultigroupSlabModel:
    grid: SlabGrid
    angular: AngularOperator
    groups: EnergyGroups
    absorption: np.ndarray
    angular_diffusion: np.ndarray
    transfer: np.ndarray
    boundary: MultigroupBoundaryData
    source: GroupSourceFunction | None = None
    _eigenvalues: np.ndarray | None = field(default=None, init=False, repr=False)
    _eigenvectors: np.ndarray | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        cells = self.grid.cells
        groups = self.groups.count
        self.absorption = self._coefficient(self.absorption, "absorption", (cells, groups))
        self.angular_diffusion = self._coefficient(
            self.angular_diffusion, "angular_diffusion", (cells, groups)
        )
        self.transfer = self._coefficient(
            self.transfer, "transfer", (cells, groups, groups)
        )
        if np.max(np.abs(np.diagonal(self.transfer, axis1=1, axis2=2))) > 0.0:
            raise SlabTransportError("transfer diagonal must vanish")
        source_group, destination_group = np.nonzero(np.any(self.transfer > 0.0, axis=0))
        energy = self.groups.energy_array
        if np.any(energy[destination_group] > energy[source_group] + 1.0e-13):
            raise SlabTransportError("up-scattering is not supported")

    def _coefficient(self, value: np.ndarray, name: str, shape: tuple[int, ...]) -> np.ndarray:
        array = np.asarray(value, dtype=float)
        if array.shape != shape:
            raise SlabTransportError(f"{name} must have shape {shape}, got {array.shape}")
        if not np.all(np.isfinite(array)) or float(np.min(array)) < 0.0:
            raise SlabTransportError(f"{name} must be finite and nonnegative")
        return array.copy()

    @property
    def shape(self) -> tuple[int, int, int]:
        return self.grid.cells, self.groups.count, self.angular.count

    @property
    def outscatter(self) -> np.ndarray:
        return np.sum(self.transfer, axis=2)

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
        energy = self.groups.energy_array.copy()
        mu = self.angular.mu_x.copy()
        left = np.asarray(self.boundary.left(time, energy, mu), dtype=float)
        right = np.asarray(self.boundary.right(time, energy, mu), dtype=float)
        expected = (self.groups.count, self.angular.count)
        if left.shape != expected or right.shape != expected:
            raise SlabTransportError(f"group boundary functions must return shape {expected}")
        if not np.all(np.isfinite(left)) or not np.all(np.isfinite(right)):
            raise SlabTransportError("boundary data contain NaN or infinity")
        return left, right

    def source_values(self, time: float) -> np.ndarray:
        if self.source is None:
            return np.zeros(self.shape, dtype=float)
        values = np.asarray(
            self.source(
                time,
                self.grid.centers.copy(),
                self.groups.energy_array.copy(),
                self.angular.mu_x.copy(),
            ),
            dtype=float,
        )
        if values.shape != self.shape:
            raise SlabTransportError(f"source must return shape {self.shape}")
        if not np.all(np.isfinite(values)):
            raise SlabTransportError("source contains NaN or infinity")
        return values

    def streaming_rhs(self, state: np.ndarray, time: float) -> np.ndarray:
        psi = self.validate_state(state)
        left, right = self.boundary_values(time)
        rhs = np.zeros_like(psi)
        mu = self.angular.mu_x
        speed = self.groups.speed_array
        positive = mu > 0.0
        negative = mu < 0.0
        if np.any(positive):
            upwind = np.empty(
                (self.grid.cells, self.groups.count, int(np.sum(positive))), dtype=float
            )
            upwind[0] = left[:, positive]
            upwind[1:] = psi[:-1, :, positive]
            rhs[:, :, positive] = (
                -speed[None, :, None]
                * mu[positive][None, None, :]
                * (psi[:, :, positive] - upwind)
                / self.grid.dx
            )
        if np.any(negative):
            upwind = np.empty(
                (self.grid.cells, self.groups.count, int(np.sum(negative))), dtype=float
            )
            upwind[:-1] = psi[1:, :, negative]
            upwind[-1] = right[:, negative]
            rhs[:, :, negative] = (
                -speed[None, :, None]
                * mu[negative][None, None, :]
                * (upwind - psi[:, :, negative])
                / self.grid.dx
            )
        return rhs

    def collision_rhs(self, state: np.ndarray) -> np.ndarray:
        psi = self.validate_state(state)
        transformed = apply_generator(self.angular, np.transpose(psi, (2, 0, 1)))
        return self.angular_diffusion[:, :, None] * np.transpose(transformed, (1, 2, 0))

    def group_transfer_rhs(self, state: np.ndarray) -> np.ndarray:
        psi = self.validate_state(state)
        incoming = np.einsum("cgh,cgk->chk", self.transfer, psi, optimize=True)
        return incoming - self.outscatter[:, :, None] * psi

    def noncollision_rhs(self, state: np.ndarray, time: float) -> np.ndarray:
        psi = self.validate_state(state)
        return (
            self.streaming_rhs(psi, time)
            + self.group_transfer_rhs(psi)
            - self.absorption[:, :, None] * psi
            + self.source_values(time)
        )

    def rhs(self, state: np.ndarray, time: float) -> np.ndarray:
        psi = self.validate_state(state)
        return self.noncollision_rhs(psi, time) + self.collision_rhs(psi)

    def stable_timestep(self, cfl: float = 1.0, *, include_collision: bool = True) -> float:
        if not 0.0 < cfl <= 1.0:
            raise SlabTransportError("cfl must lie in (0, 1]")
        removal = (
            self.groups.speed_array[None, :, None]
            * np.abs(self.angular.mu_x)[None, None, :]
            / self.grid.dx
            + self.absorption[:, :, None]
            + self.outscatter[:, :, None]
        )
        if include_collision:
            removal = removal + (
                self.angular_diffusion[:, :, None] * self.angular.rate[None, None, :]
            )
        maximum = float(np.max(removal))
        return math.inf if maximum <= 0.0 else cfl / maximum

    def _angular_spectrum(self) -> tuple[np.ndarray, np.ndarray]:
        if self._eigenvalues is None or self._eigenvectors is None:
            eigenvalues, eigenvectors = np.linalg.eigh(self.angular.symmetric_matrix)
            if float(np.max(eigenvalues)) > 5.0e-10:
                raise SlabTransportError("angular generator has a positive eigenvalue")
            self._eigenvalues = eigenvalues
            self._eigenvectors = eigenvectors
        return self._eigenvalues, self._eigenvectors

    def exact_collision_step(self, state: np.ndarray, dt: float) -> np.ndarray:
        psi = self.validate_state(state)
        if dt < 0.0 or not np.isfinite(dt):
            raise SlabTransportError("collision-step dt must be finite and nonnegative")
        if dt == 0.0:
            return psi.copy()
        eigenvalues, eigenvectors = self._angular_spectrum()
        flat = psi.reshape(self.grid.cells * self.groups.count, self.angular.count).T
        root_weight = np.sqrt(self.angular.weights)
        transformed = root_weight[:, None] * flat
        coefficients = eigenvectors.T @ transformed
        kappa = self.angular_diffusion.reshape(-1)
        evolved = eigenvectors @ (
            np.exp(dt * eigenvalues[:, None] * kappa[None, :]) * coefficients
        )
        result = (evolved / root_weight[:, None]).T.reshape(self.shape)
        if float(np.min(result)) < -5.0e-11:
            raise SlabTransportError("computed angular semigroup lost positivity")
        result[np.abs(result) < 2.0e-14] = 0.0
        return result

    def euler_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        if dt <= 0.0 or not np.isfinite(dt):
            raise SlabTransportError("dt must be finite and positive")
        return self.validate_state(state) + dt * self.rhs(state, time)

    def ssprk2_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        first = self.euler_step(state, time, dt)
        second = first + dt * self.rhs(first, time + dt)
        return 0.5 * self.validate_state(state) + 0.5 * second

    def noncollision_ssprk2_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        psi = self.validate_state(state)
        first = psi + dt * self.noncollision_rhs(psi, time)
        second = first + dt * self.noncollision_rhs(first, time + dt)
        return 0.5 * psi + 0.5 * second

    def strang_step(self, state: np.ndarray, time: float, dt: float) -> np.ndarray:
        half = self.exact_collision_step(state, 0.5 * dt)
        transported = self.noncollision_ssprk2_step(half, time, dt)
        return self.exact_collision_step(transported, 0.5 * dt)

    def step(
        self,
        state: np.ndarray,
        time: float,
        dt: float,
        *,
        integrator: MultigroupIntegrator = "strang",
    ) -> np.ndarray:
        if integrator == "euler":
            return self.euler_step(state, time, dt)
        if integrator == "ssprk2":
            return self.ssprk2_step(state, time, dt)
        if integrator == "strang":
            return self.strang_step(state, time, dt)
        raise SlabTransportError(f"unknown integrator {integrator!r}")

    def particle_inventory(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(self.grid.dx * np.sum(psi * self.angular.weights[None, None, :]))

    def energy_inventory(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(
            self.grid.dx
            * np.sum(
                psi
                * self.groups.energy_array[None, :, None]
                * self.angular.weights[None, None, :]
            )
        )

    def group_scalar_flux(self, state: np.ndarray) -> np.ndarray:
        psi = self.validate_state(state)
        return np.sum(psi * self.angular.weights[None, None, :], axis=2)

    def boundary_currents(self, state: np.ndarray, time: float) -> dict[str, np.ndarray]:
        psi = self.validate_state(state)
        left, right = self.boundary_values(time)
        mu = self.angular.mu_x
        speed = self.groups.speed_array
        weights = self.angular.weights
        positive = mu > 0.0
        negative = mu < 0.0
        return {
            "left_in": np.sum(
                speed[:, None] * weights[None, positive] * mu[positive][None, :] * left[:, positive],
                axis=1,
            ),
            "left_out": np.sum(
                speed[:, None] * weights[None, negative] * (-mu[negative])[None, :] * psi[0][:, negative],
                axis=1,
            ),
            "right_in": np.sum(
                speed[:, None] * weights[None, negative] * (-mu[negative])[None, :] * right[:, negative],
                axis=1,
            ),
            "right_out": np.sum(
                speed[:, None] * weights[None, positive] * mu[positive][None, :] * psi[-1][:, positive],
                axis=1,
            ),
        }

    def absorption_particle_rate(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(
            self.grid.dx
            * np.sum(self.absorption[:, :, None] * psi * self.angular.weights[None, None, :])
        )

    def absorption_energy_deposition_rate(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        return float(
            self.grid.dx
            * np.sum(
                self.absorption[:, :, None]
                * psi
                * self.groups.energy_array[None, :, None]
                * self.angular.weights[None, None, :]
            )
        )

    def transfer_particle_integral(self, state: np.ndarray) -> float:
        transfer_rhs = self.group_transfer_rhs(state)
        return float(
            self.grid.dx
            * np.sum(transfer_rhs * self.angular.weights[None, None, :])
        )

    def transfer_energy_deposition_rate(self, state: np.ndarray) -> float:
        psi = self.validate_state(state)
        energy = self.groups.energy_array
        drop = energy[:, None] - energy[None, :]
        angular_flux = np.sum(psi * self.angular.weights[None, None, :], axis=2)
        return float(
            self.grid.dx
            * np.sum(self.transfer * angular_flux[:, :, None] * drop[None, :, :])
        )

    def collision_particle_integral(self, state: np.ndarray) -> float:
        return float(
            self.grid.dx
            * np.sum(self.collision_rhs(state) * self.angular.weights[None, None, :])
        )

    def collision_energy_integral(self, state: np.ndarray) -> float:
        return float(
            self.grid.dx
            * np.sum(
                self.collision_rhs(state)
                * self.groups.energy_array[None, :, None]
                * self.angular.weights[None, None, :]
            )
        )

    def source_particle_rate(self, time: float) -> float:
        return float(
            self.grid.dx
            * np.sum(self.source_values(time) * self.angular.weights[None, None, :])
        )

    def source_energy_rate(self, time: float) -> float:
        return float(
            self.grid.dx
            * np.sum(
                self.source_values(time)
                * self.groups.energy_array[None, :, None]
                * self.angular.weights[None, None, :]
            )
        )

    def balance_rates(self, state: np.ndarray, time: float) -> MultigroupBalanceRates:
        psi = self.validate_state(state)
        rhs = self.rhs(psi, time)
        particle_derivative = float(
            self.grid.dx * np.sum(rhs * self.angular.weights[None, None, :])
        )
        energy_derivative = float(
            self.grid.dx
            * np.sum(
                rhs
                * self.groups.energy_array[None, :, None]
                * self.angular.weights[None, None, :]
            )
        )
        current = self.boundary_currents(psi, time)
        particle_boundary = float(
            np.sum(
                current["left_in"]
                + current["right_in"]
                - current["left_out"]
                - current["right_out"]
            )
        )
        energy = self.groups.energy_array
        energy_boundary = float(
            np.sum(
                energy
                * (
                    current["left_in"]
                    + current["right_in"]
                    - current["left_out"]
                    - current["right_out"]
                )
            )
        )
        particle_source = self.source_particle_rate(time)
        energy_source = self.source_energy_rate(time)
        particle_absorption = self.absorption_particle_rate(psi)
        absorption_deposition = self.absorption_energy_deposition_rate(psi)
        particle_transfer = self.transfer_particle_integral(psi)
        transfer_deposition = self.transfer_energy_deposition_rate(psi)
        particle_collision = self.collision_particle_integral(psi)
        energy_collision = self.collision_energy_integral(psi)
        particle_predicted = (
            particle_boundary
            + particle_source
            - particle_absorption
            + particle_transfer
            + particle_collision
        )
        energy_predicted = (
            energy_boundary
            + energy_source
            - absorption_deposition
            - transfer_deposition
            + energy_collision
        )
        return MultigroupBalanceRates(
            particle_derivative=particle_derivative,
            particle_boundary_net=particle_boundary,
            particle_source=particle_source,
            particle_absorption=particle_absorption,
            particle_transfer=particle_transfer,
            particle_collision=particle_collision,
            particle_closure_error=particle_derivative - particle_predicted,
            energy_derivative=energy_derivative,
            energy_boundary_net=energy_boundary,
            energy_source=energy_source,
            absorption_deposition=absorption_deposition,
            transfer_deposition=transfer_deposition,
            energy_collision=energy_collision,
            energy_closure_error=energy_derivative - energy_predicted,
        )

    def advance(
        self,
        initial: np.ndarray,
        final_time: float,
        *,
        cfl: float = 0.9,
        integrator: MultigroupIntegrator = "strang",
        dt_max: float | None = None,
        enforce_nonnegative: bool = True,
    ) -> tuple[np.ndarray, list[MultigroupStepDiagnostics]]:
        if final_time < 0.0:
            raise SlabTransportError("final_time must be nonnegative")
        state = self.validate_state(initial, nonnegative=enforce_nonnegative).copy()
        if final_time == 0.0:
            return state, []
        include_collision = integrator != "strang"
        limit = self.stable_timestep(cfl, include_collision=include_collision)
        if dt_max is not None:
            if dt_max <= 0.0 or not np.isfinite(dt_max):
                raise SlabTransportError("dt_max must be finite and positive")
            limit = min(limit, dt_max)
        if not np.isfinite(limit):
            limit = final_time
        steps = max(1, math.ceil(final_time / limit))
        dt = final_time / steps
        diagnostics: list[MultigroupStepDiagnostics] = []
        time = 0.0
        for _ in range(steps):
            particle_before = self.particle_inventory(state)
            energy_before = self.energy_inventory(state)
            rates = self.balance_rates(state, time)
            updated = self.step(state, time, dt, integrator=integrator)
            particle_after = self.particle_inventory(updated)
            energy_after = self.energy_inventory(updated)
            diagnostics.append(
                MultigroupStepDiagnostics(
                    time=time,
                    dt=dt,
                    particle_before=particle_before,
                    particle_after=particle_after,
                    energy_before=energy_before,
                    energy_after=energy_after,
                    particle_balance_error=(particle_after - particle_before)
                    - dt * rates.particle_derivative,
                    energy_balance_error=(energy_after - energy_before)
                    - dt * rates.energy_derivative,
                    minimum_value=float(np.min(updated)),
                )
            )
            state = updated
            time += dt
            if enforce_nonnegative and float(np.min(state)) < -5.0e-11:
                raise SlabTransportError(
                    f"positivity violation at t={time}: {float(np.min(state)):.3e}"
                )
        return state, diagnostics
