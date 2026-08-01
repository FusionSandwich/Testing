from __future__ import annotations

import copy
import unittest

import numpy as np

from gate6 import angular_diffusion_transport_audit as diffusion
from gate6.operator_validation import (
    OperatorValidationError,
    positivity_step_limit,
    validate_operator,
)


class OperatorInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.icosphere = diffusion.build_icosphere(1)
        cls.product = diffusion.build_product(5)

    def test_reference_operators_satisfy_contract(self) -> None:
        ico = validate_operator(self.icosphere)
        product = validate_operator(self.product)

        self.assertEqual(ico.directions, 42)
        self.assertEqual(product.directions, 50)
        self.assertLess(ico.coordinate_residual, 1.0e-9)
        self.assertLess(product.coordinate_residual, 1.0e-9)
        self.assertGreater(ico.minimum_conductance, 0.0)
        self.assertGreater(product.minimum_conductance, 0.0)

    def test_baseline_rates_remain_in_expected_ranges(self) -> None:
        ico = validate_operator(self.icosphere)
        product = validate_operator(self.product)

        self.assertGreater(ico.maximum_rate, 13.3)
        self.assertLess(ico.maximum_rate, 13.5)
        self.assertGreater(product.maximum_rate, 60.0)
        self.assertLess(product.maximum_rate, 60.2)
        self.assertGreater(product.maximum_rate / ico.maximum_rate, 4.4)

    def test_positivity_step_limit_matches_maximum_rate(self) -> None:
        for operator in (self.icosphere, self.product):
            with self.subTest(family=operator.family):
                expected = 1.0 / float(np.max(operator.rate))
                self.assertAlmostEqual(positivity_step_limit(operator), expected, places=14)

    def test_corrupted_rate_is_detected(self) -> None:
        corrupted = copy.deepcopy(self.icosphere)
        corrupted.rate = corrupted.rate.copy()
        corrupted.rate[0] += 0.125
        with self.assertRaisesRegex(OperatorValidationError, "reconstructed rate"):
            validate_operator(corrupted)

    def test_nonunit_direction_is_detected(self) -> None:
        corrupted = copy.deepcopy(self.product)
        corrupted.directions = corrupted.directions.copy()
        corrupted.directions[0] *= 1.01
        with self.assertRaisesRegex(OperatorValidationError, "direction normalization"):
            validate_operator(corrupted)

    def test_negative_conductance_is_detected(self) -> None:
        corrupted = copy.deepcopy(self.icosphere)
        corrupted.gamma = corrupted.gamma.copy()
        corrupted.gamma[0] = -abs(corrupted.gamma[0])
        with self.assertRaisesRegex(OperatorValidationError, "conductance"):
            validate_operator(corrupted)

    def test_inconsistent_symmetric_matrix_is_detected(self) -> None:
        corrupted = copy.deepcopy(self.product)
        corrupted.symmetric_matrix = corrupted.symmetric_matrix.copy()
        corrupted.symmetric_matrix[0, 1] += 0.01
        with self.assertRaises(OperatorValidationError):
            validate_operator(corrupted)


if __name__ == "__main__":
    unittest.main()
