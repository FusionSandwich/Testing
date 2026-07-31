from __future__ import annotations

import unittest

import numpy as np

from gate6.core import (
    BoundaryData,
    Layer,
    Material,
    SlabGrid,
    SlabModel,
    assign_layers,
    build_icosphere,
    evaluate_tallies,
    region_absorption_rate,
)


def beam_inflow(_time: float, mu: np.ndarray) -> np.ndarray:
    return np.where(mu > 0.0, np.exp(-((1.0 - mu) / 0.25) ** 2), 0.0)


def vacuum(_time: float, mu: np.ndarray) -> np.ndarray:
    return np.zeros_like(mu)


class ThinInterfaceSlabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.operator = build_icosphere(1)
        cls.grid = SlabGrid(0.0, 1.0, 60)

    def make_model(self, *, film: bool) -> tuple[SlabModel, np.ndarray]:
        substrate = Material("substrate", absorption=0.08, angular_diffusion=0.05)
        functional = (
            Material("functional-film", absorption=0.70, angular_diffusion=0.50)
            if film
            else Material("control", absorption=0.08, angular_diffusion=0.05)
        )
        stabilizer = Material("stabilizer", absorption=0.15, angular_diffusion=0.10)
        layers = (
            Layer(0.0, 0.45, substrate),
            Layer(0.45, 0.55, functional),
            Layer(0.55, 1.0, stabilizer),
        )
        absorption, diffusion, material_index = assign_layers(
            self.grid.centers,
            layers,
            domain_left=self.grid.left,
            domain_right=self.grid.right,
        )
        model = SlabModel(
            self.grid,
            self.operator,
            absorption,
            diffusion,
            BoundaryData(beam_inflow, vacuum),
        )
        return model, material_index

    def run_model(self, model: SlabModel, material_index: np.ndarray):
        state = np.zeros(model.shape)
        final_time = 1.5
        dt_limit = model.stable_timestep(0.8)
        steps = int(np.ceil(final_time / dt_limit))
        dt = final_time / steps
        time = 0.0
        cumulative_absorption = np.zeros(3)
        balance_error = 0.0
        for _ in range(steps):
            before = model.inventory(state)
            rates = model.balance_rates(state, time)
            for region in range(3):
                cumulative_absorption[region] += dt * region_absorption_rate(
                    model, state, material_index == region
                )
            state = model.euler_step(state, time, dt)
            after = model.inventory(state)
            balance_error = max(
                balance_error,
                abs((after - before) - dt * rates.inventory_derivative),
                abs(rates.closure_error),
            )
            time += dt
        return state, evaluate_tallies(model, state, time), cumulative_absorption, balance_error

    def test_thin_functional_layer_changes_transmission_and_absorption(self) -> None:
        film_model, film_index = self.make_model(film=True)
        control_model, control_index = self.make_model(film=False)
        film_state, film, film_abs, film_balance = self.run_model(
            film_model, film_index
        )
        control_state, control, control_abs, control_balance = self.run_model(
            control_model, control_index
        )

        self.assertGreaterEqual(float(np.min(film_state)), -2.0e-13)
        self.assertGreaterEqual(float(np.min(control_state)), -2.0e-13)
        self.assertLess(film_balance, 2.0e-12)
        self.assertLess(control_balance, 2.0e-12)
        self.assertLess(film.right_out, 0.9 * control.right_out)
        self.assertGreater(film_abs[1], 5.0 * control_abs[1])
        self.assertGreater(film.absorption_rate, control.absorption_rate)
        self.assertGreater(film.right_out, 0.5)

    def test_layer_assignment_detects_gaps(self) -> None:
        material = Material("m", absorption=0.1, angular_diffusion=0.1)
        with self.assertRaisesRegex(ValueError, "gap or overlap"):
            assign_layers(
                self.grid.centers,
                (Layer(0.0, 0.4, material), Layer(0.5, 1.0, material)),
                domain_left=0.0,
                domain_right=1.0,
            )


if __name__ == "__main__":
    unittest.main()
