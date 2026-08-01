from __future__ import annotations

import unittest

import numpy as np

from gate6.core import (
    BoundaryData,
    CoordinateModeManufactured,
    SlabGrid,
    SlabModel,
    SlabTransportError,
    build_product,
)


def relative_error(model: SlabModel, value: np.ndarray, reference: np.ndarray) -> float:
    weight = model.angular.weights[None, :]
    numerator = model.grid.dx * np.sum(weight * (value - reference) ** 2)
    denominator = model.grid.dx * np.sum(weight * reference**2)
    return float(np.sqrt(numerator / denominator))


class SlabTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.operator = build_product(5)
        cls.manufactured = CoordinateModeManufactured(
            0.0,
            1.0,
            amplitude=0.2,
            omega=0.7,
            absorption=0.15,
            angular_diffusion=0.25,
        )

    def make_manufactured_model(self, cells: int) -> SlabModel:
        grid = SlabGrid(0.0, 1.0, cells)
        return SlabModel(
            grid=grid,
            angular=self.operator,
            absorption=np.full(cells, self.manufactured.absorption),
            angular_diffusion=np.full(cells, self.manufactured.angular_diffusion),
            boundary=self.manufactured.boundary(),
            source=self.manufactured.source(),
        )

    def test_manufactured_solution_converges_under_spatial_refinement(self) -> None:
        errors = []
        for cells in (20, 40, 80):
            model = self.make_manufactured_model(cells)
            initial = self.manufactured.exact(
                0.0, model.grid.centers, model.angular.mu_x
            )
            final, diagnostics = model.advance(
                initial,
                0.05,
                cfl=0.7,
                integrator="ssprk2",
                dt_max=0.1 * model.grid.dx,
            )
            reference = self.manufactured.exact(
                0.05, model.grid.centers, model.angular.mu_x
            )
            errors.append(relative_error(model, final, reference))
            self.assertGreater(float(np.min(final)), 0.0)
            self.assertTrue(diagnostics)
            self.assertLess(abs(model.balance_rates(final, 0.05).closure_error), 2.0e-11)

        self.assertLess(errors[1], 0.65 * errors[0])
        self.assertLess(errors[2], 0.65 * errors[1])
        self.assertLess(errors[2], 5.0e-4)

    def test_euler_step_satisfies_exact_discrete_mass_balance(self) -> None:
        model = self.make_manufactured_model(24)
        state = self.manufactured.exact(0.0, model.grid.centers, model.angular.mu_x)
        rates = model.balance_rates(state, 0.0)
        dt = 0.5 * model.stable_timestep(1.0)
        updated = model.euler_step(state, 0.0, dt)
        actual = model.inventory(updated) - model.inventory(state)
        self.assertAlmostEqual(actual, dt * rates.inventory_derivative, places=12)
        self.assertLess(abs(rates.closure_error), 2.0e-11)
        self.assertLess(abs(rates.collision), 2.0e-11)

    def test_vacuum_transport_remains_nonnegative_below_cfl(self) -> None:
        grid = SlabGrid(0.0, 1.0, 16)
        model = SlabModel(
            grid,
            self.operator,
            np.zeros(grid.cells),
            np.full(grid.cells, 0.2),
            BoundaryData.vacuum(),
        )
        state = np.zeros(model.shape)
        state[grid.cells // 2] = np.maximum(self.operator.mu_x, 0.0)
        dt = 0.99 * model.stable_timestep(1.0)
        updated = model.euler_step(state, 0.0, dt)
        self.assertGreaterEqual(float(np.min(updated)), -2.0e-14)
        self.assertLessEqual(model.inventory(updated), model.inventory(state) + 2.0e-13)

    def test_invalid_state_and_coefficients_are_rejected(self) -> None:
        grid = SlabGrid(0.0, 1.0, 8)
        with self.assertRaises(SlabTransportError):
            SlabModel(
                grid,
                self.operator,
                -np.ones(grid.cells),
                np.zeros(grid.cells),
                BoundaryData.vacuum(),
            )
        model = SlabModel(
            grid,
            self.operator,
            np.zeros(grid.cells),
            np.zeros(grid.cells),
            BoundaryData.vacuum(),
        )
        with self.assertRaises(SlabTransportError):
            model.rhs(np.zeros((grid.cells, self.operator.count - 1)), 0.0)


if __name__ == "__main__":
    unittest.main()
