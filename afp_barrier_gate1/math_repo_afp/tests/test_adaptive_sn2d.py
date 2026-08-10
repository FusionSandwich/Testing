from __future__ import annotations

import numpy as np

from hts_angular.adaptive_sn2d import run_adaptive_sn2d, sn2d_goal_indicator
from hts_angular.quadrature import (
    PositiveQuadrature,
    exact_surface_harmonic_moments,
    gauss_legendre_product_sphere,
    real_spherical_harmonics,
)
from hts_angular.sn2d import BoundaryData2D, CartesianGrid2D, SN2DProblem, solve_direct


def _problem_factory(quadrature: PositiveQuadrature) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 1.0, 5), np.linspace(0.0, 0.5, 4))
    ng, na, nx, ny = 1, quadrature.n_node, grid.nx, grid.ny
    sigma_t = np.full((ng, nx, ny), 1.2)
    sigma_s = np.zeros((ng, ng, nx, ny))
    source = np.full((ng, na, nx, ny), 0.01)
    boundary = BoundaryData2D.zeros(ng, na, grid)
    left = boundary.left.copy()
    incoming = quadrature.nodes[:, 0] > 0.0
    left[0, incoming] = np.exp(
        8.0 * (quadrature.nodes[incoming, 0, None] - 1.0)
    )
    boundary = BoundaryData2D(left, boundary.right, boundary.bottom, boundary.top)
    detector = np.zeros_like(source)
    detector[:, :, -1, :] = 1.0
    return SN2DProblem(
        grid,
        quadrature,
        sigma_t,
        sigma_s,
        source,
        boundary,
        {"detector": detector},
    )


def _degree_one_features(nodes: np.ndarray) -> np.ndarray:
    return real_spherical_harmonics(nodes, 1)[0]


def test_integrated_goal_indicator_is_finite_nonnegative_and_ray_aware() -> None:
    quadrature = gauss_legendre_product_sphere(2, 4, phase=0.25)
    problem = _problem_factory(quadrature)
    solution = solve_direct(problem)
    indicator = sn2d_goal_indicator(problem, solution, ["detector"])
    assert indicator.combined.shape == (quadrature.n_node,)
    assert np.all(np.isfinite(indicator.combined))
    assert np.min(indicator.combined) >= 0.0
    assert np.max(indicator.ray_bootstrap) > 0.0
    assert indicator.graph.connectivity_diagnostics().connected


def test_adaptive_sn2d_loop_recertifies_moments_and_resolves_second_grid() -> None:
    initial = gauss_legendre_product_sphere(2, 4, phase=0.25)
    target = exact_surface_harmonic_moments(1)
    result = run_adaptive_sn2d(
        _problem_factory,
        initial,
        _degree_one_features,
        target,
        response_names=["detector"],
        maximum_iterations=3,
        response_tolerance=1e6,
        indicator_tolerance=1e20,
        moment_tolerance=1e-8,
        refine_fraction=0.25,
        coarsen_fraction=0.0,
    )
    assert result.converged
    assert len(result.history) >= 2
    features = _degree_one_features(result.quadrature.nodes)
    assert np.max(np.abs(features @ result.quadrature.weights - target)) < 1e-8
    assert result.solution.converged
    assert result.solution.responses["detector"] > 0.0
