from __future__ import annotations

import unittest

import numpy as np

from gate6 import angular_diffusion_transport_audit as diffusion
from gate6.operator_validation import positivity_step_limit, validate_operator


def euler_step(operator, values: np.ndarray, dt: float) -> np.ndarray:
    return values + dt * diffusion.apply_generator(operator, values)


class ExplicitEulerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.operators = (
            diffusion.build_icosphere(1),
            diffusion.build_product(5),
        )
        for operator in cls.operators:
            validate_operator(operator)

    def test_below_cfl_limit_preserves_unit_mass_nonnegativity(self) -> None:
        for operator in self.operators:
            with self.subTest(family=operator.family):
                node = int(np.argmax(operator.rate))
                values = np.zeros((len(operator.directions), 1), dtype=float)
                values[node, 0] = 1.0
                updated = euler_step(
                    operator, values, 0.99 * positivity_step_limit(operator)
                )
                self.assertGreaterEqual(float(np.min(updated)), -2.0e-14)
                self.assertGreater(float(updated[node, 0]), 0.0)

    def test_above_cfl_limit_exposes_negative_diagonal_coefficient(self) -> None:
        for operator in self.operators:
            with self.subTest(family=operator.family):
                node = int(np.argmax(operator.rate))
                values = np.zeros((len(operator.directions), 1), dtype=float)
                values[node, 0] = 1.0
                updated = euler_step(
                    operator, values, 1.01 * positivity_step_limit(operator)
                )
                self.assertLess(float(updated[node, 0]), -0.009)

    def test_weighted_mass_is_conserved_by_one_step(self) -> None:
        axes = diffusion.orientations()[:, :3]
        for operator in self.operators:
            with self.subTest(family=operator.family):
                values = diffusion.initial_profiles(operator.directions, axes)
                before = diffusion.weighted_masses(operator.weights, values)
                updated = euler_step(
                    operator, values, 0.75 * positivity_step_limit(operator)
                )
                after = diffusion.weighted_masses(operator.weights, updated)
                np.testing.assert_allclose(after, before, rtol=0.0, atol=3.0e-13)

    def test_degree_one_mode_has_exact_euler_amplification(self) -> None:
        for operator in self.operators:
            with self.subTest(family=operator.family):
                dt = 0.25 * positivity_step_limit(operator)
                coordinate = operator.directions[:, [0]]
                updated = euler_step(operator, coordinate, dt)
                expected = (1.0 - 2.0 * dt) * coordinate
                np.testing.assert_allclose(updated, expected, rtol=0.0, atol=3.0e-10)


if __name__ == "__main__":
    unittest.main()
