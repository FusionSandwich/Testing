from __future__ import annotations

import unittest

from gate6 import angular_diffusion_transport_audit as diffusion
from gate6 import forward_peaked_heat_scattering_audit as forward
from gate6.operator_validation import validate_operator


class TransportRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.axes = diffusion.orientations()

    def test_level_one_angular_diffusion_baseline(self) -> None:
        ico_operator = diffusion.build_icosphere(1)
        product_operator = diffusion.build_product(5)
        validate_operator(ico_operator)
        validate_operator(product_operator)

        ico = diffusion.audit_operator(1, ico_operator, 0.1, self.axes)
        product = diffusion.audit_operator(1, product_operator, 0.1, self.axes)

        self.assertEqual(ico.explicit_steps, 2)
        self.assertEqual(product.explicit_steps, 7)
        self.assertGreater(ico.max_semigroup_error, 9.4e-3)
        self.assertLess(ico.max_semigroup_error, 9.7e-3)
        self.assertGreater(product.max_semigroup_error, 1.79e-2)
        self.assertLess(product.max_semigroup_error, 1.83e-2)
        self.assertLess(ico.max_semigroup_error, product.max_semigroup_error)

    def test_refinement_reduces_transport_error_and_increases_step_separation(self) -> None:
        ico1 = diffusion.audit_operator(
            1, diffusion.build_icosphere(1), 0.1, self.axes
        )
        ico2 = diffusion.audit_operator(
            2, diffusion.build_icosphere(2), 0.1, self.axes
        )
        product1 = diffusion.audit_operator(
            1, diffusion.build_product(5), 0.1, self.axes
        )
        product2 = diffusion.audit_operator(
            2, diffusion.build_product(9), 0.1, self.axes
        )

        self.assertLess(ico2.max_semigroup_error, 0.27 * ico1.max_semigroup_error)
        self.assertLess(
            product2.max_semigroup_error, 0.27 * product1.max_semigroup_error
        )
        self.assertGreater(product2.explicit_steps / ico2.explicit_steps, 10.0)

    def test_forward_peaked_level_one_baseline(self) -> None:
        operator = diffusion.build_icosphere(1)
        row = forward.audit_case(1, operator, 0.005, 0.1, self.axes)

        self.assertEqual(row.boltzmann_euler_steps, 2)
        self.assertEqual(row.fp_euler_steps, 2)
        self.assertGreater(row.continuum_model_error_max, 1.1e-3)
        self.assertLess(row.continuum_model_error_max, 1.3e-3)
        self.assertGreater(row.discrete_boltzmann_error_max, 9.2e-3)
        self.assertLess(row.discrete_boltzmann_error_max, 9.5e-3)
        self.assertGreaterEqual(row.transition_minimum, -2.0e-10)


if __name__ == "__main__":
    unittest.main()
