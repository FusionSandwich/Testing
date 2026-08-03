from __future__ import annotations

import math
import unittest

import numpy as np

from gate6.core import (
    EnergyGroups,
    MultigroupBoundaryData,
    MultigroupSlabModel,
    SlabGrid,
    build_icosphere,
)


class MultigroupTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.operator = build_icosphere(0)
        cls.groups = EnergyGroups((3.0, 2.0, 1.0), (0.0, 0.0, 0.0))
        cls.grid = SlabGrid(0.0, 1.0, 1)

    def make_cascade(self, first_rate: float = 0.7, second_rate: float = 0.3):
        absorption = np.zeros((1, 3))
        diffusion = np.zeros((1, 3))
        transfer = np.zeros((1, 3, 3))
        transfer[0, 0, 1] = first_rate
        transfer[0, 1, 2] = second_rate
        return MultigroupSlabModel(
            self.grid,
            self.operator,
            self.groups,
            absorption,
            diffusion,
            transfer,
            MultigroupBoundaryData.vacuum(),
        )

    def test_group_transfer_conserves_particles_and_deposits_energy(self) -> None:
        model = self.make_cascade()
        state = np.zeros(model.shape)
        state[0, 0] = 1.0
        state[0, 1] = 0.4
        state[0, 2] = 0.2

        transfer_rhs = model.group_transfer_rhs(state)
        particle_change = model.grid.dx * np.sum(
            transfer_rhs * model.angular.weights[None, None, :]
        )
        energy_change = model.grid.dx * np.sum(
            transfer_rhs
            * model.groups.energy_array[None, :, None]
            * model.angular.weights[None, None, :]
        )
        deposition = model.transfer_energy_deposition_rate(state)

        self.assertAlmostEqual(particle_change, 0.0, places=13)
        self.assertGreater(deposition, 0.0)
        self.assertAlmostEqual(energy_change, -deposition, places=12)
        rates = model.balance_rates(state, 0.0)
        self.assertLess(abs(rates.particle_closure_error), 1.0e-12)
        self.assertLess(abs(rates.energy_closure_error), 1.0e-12)

    def test_three_group_cascade_matches_analytic_solution(self) -> None:
        first_rate = 0.7
        second_rate = 0.3
        model = self.make_cascade(first_rate, second_rate)
        state = np.zeros(model.shape)
        state[0, 0] = 1.0
        final, _ = model.advance(
            state,
            1.0,
            cfl=0.9,
            integrator="ssprk2",
            dt_max=0.001,
        )
        high = math.exp(-first_rate)
        middle = first_rate / (second_rate - first_rate) * (
            math.exp(-first_rate) - math.exp(-second_rate)
        )
        low = 1.0 - high - middle
        expected = np.asarray([high, middle, low])
        actual = np.mean(final[0], axis=1)
        np.testing.assert_allclose(actual, expected, rtol=0.0, atol=2.0e-7)
        self.assertAlmostEqual(float(np.sum(actual)), 1.0, places=11)

    def test_exact_collision_step_preserves_each_group_integral(self) -> None:
        absorption = np.zeros((1, 3))
        diffusion = np.asarray([[0.1, 0.2, 0.4]])
        transfer = np.zeros((1, 3, 3))
        model = MultigroupSlabModel(
            self.grid,
            build_icosphere(1),
            self.groups,
            absorption,
            diffusion,
            transfer,
            MultigroupBoundaryData.vacuum(),
        )
        mu = model.angular.mu_x
        state = np.empty(model.shape)
        state[0, 0] = 1.0 + 0.2 * mu
        state[0, 1] = 0.8 - 0.1 * mu
        state[0, 2] = 0.5 + 0.15 * mu
        before = np.sum(state * model.angular.weights[None, None, :], axis=2)
        after_state = model.exact_collision_step(state, 0.4)
        after = np.sum(after_state * model.angular.weights[None, None, :], axis=2)
        np.testing.assert_allclose(after, before, rtol=0.0, atol=3.0e-12)
        self.assertGreaterEqual(float(np.min(after_state)), -2.0e-13)


if __name__ == "__main__":
    unittest.main()
