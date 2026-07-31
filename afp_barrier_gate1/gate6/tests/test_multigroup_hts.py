from __future__ import annotations

import math
import unittest

import numpy as np

from gate6.core import (
    MultigroupBoundaryData,
    MultigroupSlabModel,
    SlabGrid,
    assign_multigroup_layers,
    build_icosphere,
    build_product,
    default_energy_groups,
    evaluate_multigroup_tallies,
    hts_like_layers,
    region_energy_deposition_rates,
)


def beam(_time: float, energies: np.ndarray, mu: np.ndarray) -> np.ndarray:
    values = np.zeros((len(energies), len(mu)))
    positive = mu > 0.0
    values[0, positive] = np.exp(-((1.0 - mu[positive]) / 0.22) ** 2)
    return values


def vacuum(_time: float, energies: np.ndarray, mu: np.ndarray) -> np.ndarray:
    return np.zeros((len(energies), len(mu)))


class MultigroupHTSTests(unittest.TestCase):
    def make_model(self, operator, *, functional: bool, cells: int = 40):
        groups = default_energy_groups()
        grid = SlabGrid(0.0, 1.0, cells)
        absorption, diffusion, transfer, index = assign_multigroup_layers(
            grid.centers,
            hts_like_layers(groups, functional_layer=functional),
            energies=groups.energy_array,
            domain_left=0.0,
            domain_right=1.0,
        )
        return (
            MultigroupSlabModel(
                grid,
                operator,
                groups,
                absorption,
                diffusion,
                transfer,
                MultigroupBoundaryData(beam, vacuum),
            ),
            index,
        )

    def run_model(self, model: MultigroupSlabModel, index: np.ndarray, integrator: str):
        final_time = 1.2
        state = np.zeros(model.shape)
        include_collision = integrator != "strang"
        limit = min(
            model.stable_timestep(0.8, include_collision=include_collision),
            0.005,
        )
        steps = math.ceil(final_time / limit)
        dt = final_time / steps
        heat = np.zeros(5)
        time = 0.0
        for _ in range(steps):
            for region in range(5):
                heat[region] += dt * region_energy_deposition_rates(
                    model, state, index == region
                )[2]
            state = model.step(state, time, dt, integrator=integrator)
            time += dt
        return state, evaluate_multigroup_tallies(model, state, time), heat, steps

    def test_functional_layer_changes_energy_transmission_and_heating(self) -> None:
        operator = build_icosphere(1)
        film_model, film_index = self.make_model(operator, functional=True)
        control_model, control_index = self.make_model(operator, functional=False)
        film_state, film, film_heat, _ = self.run_model(film_model, film_index, "strang")
        control_state, control, control_heat, _ = self.run_model(
            control_model, control_index, "strang"
        )
        film_transmitted = float(np.dot(film_model.groups.energy_array, film.right_out))
        control_transmitted = float(
            np.dot(control_model.groups.energy_array, control.right_out)
        )
        self.assertLess(film_transmitted, 0.99 * control_transmitted)
        self.assertGreater(film_heat[2], 2.0 * control_heat[2])
        self.assertGreaterEqual(float(np.min(film_state)), -5.0e-11)
        self.assertGreaterEqual(float(np.min(control_state)), -5.0e-11)

    def test_strang_removes_product_grid_angular_cfl_penalty(self) -> None:
        ico, _ = self.make_model(build_icosphere(2), functional=True)
        product, _ = self.make_model(build_product(9), functional=True)
        explicit_ratio = (
            ico.stable_timestep(0.8, include_collision=True)
            / product.stable_timestep(0.8, include_collision=True)
        )
        split_ratio = (
            ico.stable_timestep(0.8, include_collision=False)
            / product.stable_timestep(0.8, include_collision=False)
        )
        self.assertGreater(explicit_ratio, 3.0)
        self.assertLess(abs(split_ratio - 1.0), 0.08)

    def test_euler_and_strang_agree_on_primary_responses(self) -> None:
        model, index = self.make_model(build_icosphere(1), functional=True)
        _, euler, euler_heat, _ = self.run_model(model, index, "euler")
        _, strang, strang_heat, _ = self.run_model(model, index, "strang")
        euler_transmitted = float(np.dot(model.groups.energy_array, euler.right_out))
        strang_transmitted = float(np.dot(model.groups.energy_array, strang.right_out))
        self.assertLess(
            abs(euler_transmitted - strang_transmitted) / euler_transmitted,
            0.02,
        )
        self.assertLess(
            abs(float(np.sum(euler_heat)) - float(np.sum(strang_heat)))
            / float(np.sum(euler_heat)),
            0.025,
        )


if __name__ == "__main__":
    unittest.main()
