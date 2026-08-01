from __future__ import annotations

import math
import unittest

import numpy as np

from gate6 import angular_diffusion_transport_audit as diffusion
from gate6 import forward_peaked_heat_scattering_audit as forward
from gate6.operator_validation import validate_operator


class ForwardPeakedScatteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.operator = diffusion.build_icosphere(1)
        validate_operator(cls.operator)
        cls.eigenvalues, cls.eigenvectors = forward.spectral_data(cls.operator)

    def test_modal_decay_is_nonnegative_and_below_fp_limit(self) -> None:
        for tau in (0.02, 0.005, 0.001, 0.0002):
            for ell in range(0, 7):
                with self.subTest(tau=tau, ell=ell):
                    lam = float(ell * (ell + 1))
                    beta = forward.heat_boltzmann_decay(tau, ell)
                    self.assertGreaterEqual(beta, 0.0)
                    self.assertLessEqual(beta, lam + 2.0e-13)
                    self.assertLessEqual(
                        math.exp(-0.1 * lam),
                        math.exp(-0.1 * beta) + 2.0e-15,
                    )

    def test_small_tau_decay_converges_to_fp_rate(self) -> None:
        for ell in (1, 2, 3, 4):
            lam = float(ell * (ell + 1))
            coarse_error = abs(forward.heat_boltzmann_decay(0.01, ell) - lam)
            fine_error = abs(forward.heat_boltzmann_decay(0.001, ell) - lam)
            self.assertLess(fine_error, 0.12 * coarse_error)

    def test_discrete_heat_transition_is_stochastic_and_reversible(self) -> None:
        tau = 0.005
        transition = forward.physical_transition(
            self.operator, tau, self.eigenvalues, self.eigenvectors
        )
        row_error = float(np.max(np.abs(np.sum(transition, axis=1) - 1.0)))
        balance_error = float(np.max(np.abs(
            self.operator.weights[:, None] * transition
            - self.operator.weights[None, :] * transition.T
        )))
        self.assertGreaterEqual(float(np.min(transition)), -2.0e-12)
        self.assertLess(row_error, 5.0e-11)
        self.assertLess(balance_error, 5.0e-11)

    def test_discrete_boltzmann_generator_has_nonnegative_offdiagonals(self) -> None:
        tau = 0.005
        transition = forward.physical_transition(
            self.operator, tau, self.eigenvalues, self.eigenvectors
        )
        generator = (transition - np.eye(len(self.operator.directions))) / tau
        offdiag = generator.copy()
        offdiag[np.diag_indices_from(offdiag)] = 0.0
        self.assertGreaterEqual(float(np.min(offdiag)), -5.0e-11)
        np.testing.assert_allclose(
            np.sum(generator, axis=1),
            np.zeros(len(generator)),
            rtol=0.0,
            atol=5.0e-11,
        )

    def test_forward_peaked_evolution_preserves_mass_and_positivity(self) -> None:
        tau = 0.005
        axes = diffusion.orientations()[:, :4]
        initial = diffusion.initial_profiles(self.operator.directions, axes)
        modal_generator = np.expm1(tau * self.eigenvalues) / tau
        final = forward.evolve_with_modal_generator(
            self.operator,
            initial,
            0.1,
            self.eigenvalues,
            self.eigenvectors,
            modal_generator,
        )
        before = diffusion.weighted_masses(self.operator.weights, initial)
        after = diffusion.weighted_masses(self.operator.weights, final)
        np.testing.assert_allclose(after, before, rtol=0.0, atol=5.0e-11)
        self.assertGreaterEqual(float(np.min(final)), -5.0e-12)


if __name__ == "__main__":
    unittest.main()
