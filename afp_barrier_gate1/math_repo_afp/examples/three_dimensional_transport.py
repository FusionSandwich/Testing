from __future__ import annotations

import json

import numpy as np

from hts_angular import (
    BoundaryData3D,
    CartesianGrid3D,
    SN3DProblem,
    axis_quadrature_sphere,
    forward_adjoint_identity_3d,
    global_particle_balance_3d,
    solve_direct_3d,
    solve_source_iteration_3d,
)

grid = CartesianGrid3D(np.linspace(0.0, 1.0, 3), np.linspace(0.0, 1.0, 3), np.linspace(0.0, 1.0, 3))
quadrature = axis_quadrature_sphere()
shape = grid.shape
sigma_t = np.full((1, *shape), 0.9)
sigma_s = np.full((1, 1, *shape), 0.2)
source = np.full((1, quadrature.n_node, *shape), 0.01)
problem = SN3DProblem(
    grid,
    quadrature,
    sigma_t,
    sigma_s,
    source,
    BoundaryData3D.vacuum(1, quadrature.n_node, grid),
    {"track": np.ones_like(source)},
)
direct = solve_direct_3d(problem)
iterative = solve_source_iteration_3d(problem, tolerance=1e-12, workers=2)
balance = global_particle_balance_3d(problem, iterative)
adjoint = forward_adjoint_identity_3d(problem, direct, "track")
print(
    json.dumps(
        {
            "converged": iterative.converged,
            "balance_passed": balance["relative_residual"] < 1e-10,
            "adjoint_passed": adjoint["relative_difference"] < 1e-10,
            "direct_iteration_max_error": float(np.max(np.abs(direct.angular_flux - iterative.angular_flux))),
            "flux_sha256": iterative.flux_sha256,
        },
        indent=2,
        sort_keys=True,
    )
)
