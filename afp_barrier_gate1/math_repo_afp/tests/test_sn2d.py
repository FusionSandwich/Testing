from __future__ import annotations

import numpy as np

from hts_angular.sn2d import (
    BoundaryData2D,
    CartesianGrid2D,
    SN2DProblem,
    circle_quadrature,
    forward_adjoint_identity,
    global_particle_balance,
    solve_direct,
    solve_source_iteration,
)


def simple_problem(scattering: float = 0.35) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 1.0, 8), np.linspace(0.0, 0.7, 6))
    q = circle_quadrature(12, phase=0.5)
    ng, na, nx, ny = 1, q.n_node, grid.nx, grid.ny
    sigma_t = np.full((ng, nx, ny), 1.2)
    sigma_s = np.zeros((ng, ng, nx, ny))
    sigma_s[0, 0] = scattering
    source = np.zeros((ng, na, nx, ny))
    source[:, :, nx // 2, ny // 2] = 0.2
    boundary = BoundaryData2D.zeros(ng, na, grid)
    kernel = np.zeros_like(source)
    kernel[:, :, -2:, :] = 1.0
    return SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, {"detector": kernel})


def test_direct_and_source_iteration_agree_and_remain_positive() -> None:
    problem = simple_problem(0.28)
    direct = solve_direct(problem)
    iteration = solve_source_iteration(problem, tolerance=2e-11)
    assert iteration.converged
    assert np.min(direct.angular_flux) >= -1e-12
    assert np.min(iteration.angular_flux) >= -1e-12
    assert np.allclose(iteration.angular_flux, direct.angular_flux, rtol=2e-8, atol=2e-10)


def test_discrete_particle_balance() -> None:
    problem = simple_problem(0.22)
    solution = solve_direct(problem)
    balance = global_particle_balance(problem, solution)
    assert balance["relative_residual"] < 2e-11


def test_exact_transpose_adjoint_identity() -> None:
    problem = simple_problem(0.31)
    solution = solve_direct(problem)
    identity = forward_adjoint_identity(problem, solution, "detector")
    assert identity["relative_difference"] < 3e-12


def test_coupled_neutron_photon_problem_is_positive_and_balanced() -> None:
    grid = CartesianGrid2D(np.linspace(0.0, 1.2, 9), np.linspace(0.0, 0.4, 5))
    q = circle_quadrature(16, phase=0.0)
    ng, na, nx, ny = 2, q.n_node, grid.nx, grid.ny
    sigma_t = np.empty((ng, nx, ny))
    sigma_t[0] = 1.4
    sigma_t[1] = 0.9
    tape = (grid.x_centers[:, None] > 0.5) & (grid.x_centers[:, None] < 0.7)
    sigma_t[0] += 0.8 * tape
    sigma_t[1] += 0.5 * tape
    sigma_s = np.zeros((ng, ng, nx, ny))
    sigma_s[0, 0] = 0.45
    sigma_s[0, 1] = 0.30
    sigma_s[1, 1] = 0.22
    source = np.zeros((ng, na, nx, ny))
    boundary = BoundaryData2D.zeros(ng, na, grid)
    left = boundary.left.copy()
    outgoing = q.nodes[:, 0] > 0.0
    left[0, outgoing, :] = np.exp(10.0 * (q.nodes[outgoing, 0, None] - 1.0))
    boundary = BoundaryData2D(left, boundary.right, boundary.bottom, boundary.top)
    photon_kernel = np.zeros_like(source)
    photon_kernel[1, :, tape[:, 0], :] = 0.68
    problem = SN2DProblem(grid, q, sigma_t, sigma_s, source, boundary, {"photon_heating": photon_kernel})
    solution = solve_source_iteration(problem, tolerance=1e-10)
    assert solution.converged
    assert np.min(solution.angular_flux) >= -2e-12
    assert solution.responses["photon_heating"] > 0.0
    assert global_particle_balance(problem, solution)["relative_residual"] < 2e-10
