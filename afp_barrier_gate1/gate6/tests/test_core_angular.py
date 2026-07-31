from __future__ import annotations

import unittest

import numpy as np

from gate6 import angular_diffusion_transport_audit as legacy
from gate6.core import (
    apply_generator,
    build_icosphere,
    build_product,
    exact_semidiscrete_evolution,
)
from gate6.operator_validation import validate_operator


class CoreAngularTests(unittest.TestCase):
    def test_core_builders_match_frozen_audit_implementations(self) -> None:
        pairs = (
            (build_icosphere(1), legacy.build_icosphere(1)),
            (build_product(5), legacy.build_product(5)),
        )
        for core, reference in pairs:
            with self.subTest(family=core.family):
                validate_operator(core)
                np.testing.assert_array_equal(core.edge_i, reference.edge_i)
                np.testing.assert_array_equal(core.edge_j, reference.edge_j)
                np.testing.assert_allclose(core.directions, reference.directions, atol=0.0, rtol=0.0)
                np.testing.assert_allclose(core.weights, reference.weights, atol=0.0, rtol=0.0)
                np.testing.assert_allclose(core.gamma, reference.gamma, atol=0.0, rtol=0.0)
                np.testing.assert_allclose(core.rate, reference.rate, atol=0.0, rtol=0.0)
                np.testing.assert_allclose(
                    core.symmetric_matrix, reference.symmetric_matrix, atol=0.0, rtol=0.0
                )

    def test_sparse_generator_accepts_multiple_trailing_dimensions(self) -> None:
        operator = build_icosphere(1)
        values = np.stack(
            [operator.directions[:, 0], operator.directions[:, 1]], axis=1
        )
        batched = np.stack([values, 2.0 * values], axis=2)
        action = apply_generator(operator, batched)
        np.testing.assert_allclose(action, -2.0 * batched, rtol=0.0, atol=3.0e-10)

    def test_exact_semigroup_preserves_constant_and_decays_coordinates(self) -> None:
        operator = build_product(5)
        time = 0.125
        data = np.column_stack(
            [np.ones(operator.count), operator.directions[:, 0]]
        )
        evolved = exact_semidiscrete_evolution(operator, data, time)
        np.testing.assert_allclose(evolved[:, 0], 1.0, rtol=0.0, atol=3.0e-13)
        np.testing.assert_allclose(
            evolved[:, 1], np.exp(-2.0 * time) * data[:, 1], rtol=0.0, atol=3.0e-10
        )


if __name__ == "__main__":
    unittest.main()
