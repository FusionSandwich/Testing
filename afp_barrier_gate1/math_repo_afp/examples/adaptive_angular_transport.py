"""Run the integrated positive, moment-recertified adaptive S_N loop."""
from __future__ import annotations

import json
import numpy as np

from hts_angular import (
    BoundaryData2D,
    CartesianGrid2D,
    PositiveQuadrature,
    SN2DProblem,
    exact_surface_harmonic_moments,
    gauss_legendre_product_sphere,
    real_spherical_harmonics,
    run_adaptive_sn2d,
)


def problem_factory(quadrature: PositiveQuadrature) -> SN2DProblem:
    grid = CartesianGrid2D(np.linspace(0.0, 1.0, 7), np.linspace(0.0, 0.4, 5))
    ng, na, nx, ny = 1, quadrature.n_node, grid.nx, grid.ny
    sigma_t = np.full((ng, nx, ny), 1.1)
    sigma_s = np.zeros((ng, ng, nx, ny))
    source = np.full((ng, na, nx, ny), 0.002)
    boundary = BoundaryData2D.zeros(ng, na, grid)
    left = boundary.left.copy()
    incoming = quadrature.nodes[:, 0] > 0.0
    left[0, incoming] = np.exp(10.0 * (quadrature.nodes[incoming, 0, None] - 1.0))
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
        response_kernels={"detector": detector},
    )


def degree_one_features(nodes: np.ndarray) -> np.ndarray:
    return real_spherical_harmonics(nodes, 1)[0]


def main() -> None:
    result = run_adaptive_sn2d(
        problem_factory,
        gauss_legendre_product_sphere(2, 4, phase=0.25),
        degree_one_features,
        exact_surface_harmonic_moments(1),
        response_names=["detector"],
        maximum_iterations=4,
        response_tolerance=5e-1,
        indicator_tolerance=2e-1,
        moment_tolerance=1e-8,
        refine_fraction=0.25,
        coarsen_fraction=0.0,
    )
    summary = {
        "converged": result.converged,
        "reason": result.reason,
        "final_nodes": result.quadrature.n_node,
        "detector_response": result.solution.responses["detector"],
        "history": [
            {
                "iteration": row.iteration,
                "nodes": row.node_count,
                "maximum_indicator": row.maximum_indicator,
                "relative_response_change": (row.relative_response_change if np.isfinite(row.relative_response_change) else None),
                "moment_residual": row.moment_residual,
            }
            for row in result.history
        ],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
