from __future__ import annotations

import numpy as np
import pytest

from hts_angular import (
    BoundaryData3D,
    CartesianGrid3D,
    SN3DProblem,
    axis_quadrature_sphere,
    execution_plan_3d,
    forward_adjoint_identity_3d,
    global_particle_balance_3d,
    solve_direct_3d,
    solve_source_iteration_3d,
)


def _one_cell_problem(*, scattering: bool = False, groups: int = 1) -> SN3DProblem:
    grid = CartesianGrid3D(np.array([0.0, 1.0]), np.array([0.0, 1.0]), np.array([0.0, 1.0]))
    quadrature = axis_quadrature_sphere()
    sigma_t = np.empty((groups, 1, 1, 1))
    sigma_t[:, 0, 0, 0] = np.linspace(0.7, 1.1, groups)
    sigma_s = np.zeros((groups, groups, 1, 1, 1))
    if scattering:
        for incoming in range(groups):
            sigma_s[incoming, incoming, 0, 0, 0] = 0.18 + 0.02 * incoming
        if groups > 1:
            sigma_s[0, 1, 0, 0, 0] = 0.07
            sigma_s[1, 0, 0, 0, 0] = 0.03
    source = np.empty((groups, quadrature.n_node, 1, 1, 1))
    for group in range(groups):
        source[group, :, 0, 0, 0] = (group + 1) * np.linspace(0.01, 0.016, quadrature.n_node)
    response_kernels = {
        "total_track": np.ones_like(source),
        "group_weighted": np.broadcast_to(
            np.arange(1, groups + 1)[:, None, None, None, None], source.shape
        ).copy(),
    }
    return SN3DProblem(
        grid,
        quadrature,
        sigma_t,
        sigma_s,
        source,
        BoundaryData3D.vacuum(groups, quadrature.n_node, grid),
        response_kernels,
    )


def test_one_cell_pure_absorber_has_analytic_axis_solution_and_balance() -> None:
    problem = _one_cell_problem(scattering=False)
    solution = solve_direct_3d(problem, residual_tolerance=1e-12)
    expected = problem.fixed_source / (problem.sigma_t[:, None] + 1.0)
    np.testing.assert_allclose(solution.angular_flux, expected, rtol=2e-14, atol=2e-15)
    assert solution.converged
    assert solution.relative_residual < 1e-14
    balance = global_particle_balance_3d(problem, solution)
    assert balance["relative_residual"] < 2e-14
    assert min(solution.angular_flux.reshape(-1)) >= 0.0


def test_source_iteration_matches_direct_and_is_worker_invariant() -> None:
    problem = _one_cell_problem(scattering=True, groups=2)
    direct = solve_direct_3d(problem, residual_tolerance=1e-12)
    serial = solve_source_iteration_3d(problem, tolerance=1e-13, workers=1)
    parallel = solve_source_iteration_3d(problem, tolerance=1e-13, workers=4)
    assert serial.converged and parallel.converged and direct.converged
    np.testing.assert_allclose(serial.angular_flux, direct.angular_flux, rtol=2e-12, atol=2e-14)
    np.testing.assert_array_equal(serial.angular_flux, parallel.angular_flux)
    assert serial.flux_sha256 == parallel.flux_sha256
    assert serial.relative_residual < 2e-12
    assert global_particle_balance_3d(problem, serial)["relative_residual"] < 2e-12


def test_discrete_adjoint_identity_is_machine_consistent() -> None:
    problem = _one_cell_problem(scattering=True, groups=2)
    solution = solve_direct_3d(problem)
    identity = forward_adjoint_identity_3d(problem, solution, "group_weighted")
    assert identity["relative_difference"] < 2e-14
    assert identity["forward"] == pytest.approx(solution.responses["group_weighted"], rel=2e-14)


def test_nonuniform_multicell_problem_direct_and_sweep_agree() -> None:
    grid = CartesianGrid3D(
        np.array([0.0, 0.2, 0.7, 1.0]),
        np.array([0.0, 0.4, 1.0]),
        np.array([0.0, 0.3, 0.8, 1.0]),
    )
    quadrature = axis_quadrature_sphere()
    shape = grid.shape
    x = grid.x_centers[:, None, None]
    y = grid.y_centers[None, :, None]
    z = grid.z_centers[None, None, :]
    sigma_t = (0.8 + 0.2 * x + 0.1 * y + 0.05 * z)[None, ...]
    sigma_s = np.zeros((1, 1, *shape))
    sigma_s[0, 0] = 0.22 + 0.02 * x
    source = np.empty((1, quadrature.n_node, *shape))
    for angle in range(quadrature.n_node):
        source[0, angle] = (0.01 + 0.001 * angle) * (1.0 + x + 0.5 * y)
    problem = SN3DProblem(
        grid,
        quadrature,
        sigma_t,
        sigma_s,
        source,
        BoundaryData3D.vacuum(1, quadrature.n_node, grid),
        {"track": np.ones_like(source)},
    )
    direct = solve_direct_3d(problem, residual_tolerance=1e-11)
    sweep = solve_source_iteration_3d(problem, tolerance=2e-13, workers=3)
    assert direct.converged and sweep.converged
    np.testing.assert_allclose(sweep.angular_flux, direct.angular_flux, rtol=5e-11, atol=2e-13)
    assert global_particle_balance_3d(problem, sweep)["relative_residual"] < 2e-11


def test_execution_plan_and_input_validation() -> None:
    problem = _one_cell_problem(groups=2)
    plan = execution_plan_3d(problem, workers=3)
    assert plan["unknowns"] == 12
    assert plan["angular_tasks"] == 12
    assert plan["flux_bytes"] == 96
    with pytest.raises(ValueError, match="workers"):
        execution_plan_3d(problem, workers=0)

    with pytest.raises(ValueError, match="out-scattering"):
        SN3DProblem(
            problem.grid,
            problem.quadrature,
            problem.sigma_t,
            np.full_like(problem.sigma_s, 2.0),
            problem.fixed_source,
            problem.boundary,
        )
