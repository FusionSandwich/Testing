from __future__ import annotations

import unittest

import numpy as np

from gate6 import angular_diffusion_transport_audit as diffusion
from gate6 import layered_charged_particle_audit as layered
from gate6.operator_validation import validate_operator


class LayeredChargedParticleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.layer_a = layered.Layer("A", stopping=1.0, coefficient=4.0, thickness=1.0)
        self.layer_b = layered.Layer("B", stopping=0.5, coefficient=0.4, thickness=1.0)
        self.energy = 5.0

    def test_one_layer_depth_matches_reciprocal_antiderivative(self) -> None:
        output, depth = layered.layer_depth(self.layer_a, self.energy)
        self.assertAlmostEqual(output, 4.0, places=14)
        self.assertAlmostEqual(depth, 0.2, places=14)

    def test_final_energy_is_order_independent_but_depth_is_not(self) -> None:
        energy_ab, depth_ab = layered.traverse(
            (self.layer_a, self.layer_b), self.energy
        )
        energy_ba, depth_ba = layered.traverse(
            (self.layer_b, self.layer_a), self.energy
        )
        self.assertAlmostEqual(energy_ab, 3.5, places=14)
        self.assertAlmostEqual(energy_ba, 3.5, places=14)
        self.assertLess(depth_ab, depth_ba)
        self.assertAlmostEqual(depth_ab, 0.2285714285714286, places=14)
        self.assertAlmostEqual(depth_ba, 0.2717460317460317, places=14)

    def test_closed_form_order_difference_matches_traversal(self) -> None:
        _, depth_ab = layered.traverse((self.layer_a, self.layer_b), self.energy)
        _, depth_ba = layered.traverse((self.layer_b, self.layer_a), self.energy)
        predicted = layered.exact_order_difference(
            self.energy, self.layer_a, self.layer_b
        )
        self.assertAlmostEqual(depth_ab - depth_ba, predicted, places=14)

    def test_layer_that_exhausts_energy_is_rejected(self) -> None:
        invalid = layered.Layer("invalid", stopping=3.0, coefficient=1.0, thickness=2.0)
        with self.assertRaisesRegex(ValueError, "exhausts"):
            layered.layer_depth(invalid, self.energy)

    def test_semigroup_composition_depends_only_on_total_depth(self) -> None:
        operator = diffusion.build_icosphere(1)
        validate_operator(operator)
        axes = diffusion.orientations()[:, :3]
        initial = diffusion.initial_profiles(operator.directions, axes)

        energy_mid, depth_a = layered.layer_depth(self.layer_a, self.energy)
        _, depth_b_after_a = layered.layer_depth(self.layer_b, energy_mid)
        sequential = diffusion.exact_semidiscrete_evolution(
            operator,
            diffusion.exact_semidiscrete_evolution(operator, initial, depth_a),
            depth_b_after_a,
        )
        direct = diffusion.exact_semidiscrete_evolution(
            operator, initial, depth_a + depth_b_after_a
        )
        np.testing.assert_allclose(sequential, direct, rtol=0.0, atol=2.0e-12)

    def test_layer_order_produces_resolvable_angular_response(self) -> None:
        operator = diffusion.build_icosphere(1)
        axes = diffusion.orientations()[:, :4]
        _, depth_ab = layered.traverse((self.layer_a, self.layer_b), self.energy)
        _, depth_ba = layered.traverse((self.layer_b, self.layer_a), self.energy)
        response_ab = layered.continuum_profiles(operator.directions, axes, depth_ab)
        response_ba = layered.continuum_profiles(operator.directions, axes, depth_ba)
        difference = layered.weighted_relative_difference(
            operator.weights, response_ab, response_ba
        )
        self.assertGreater(difference, 1.0e-3)


if __name__ == "__main__":
    unittest.main()
