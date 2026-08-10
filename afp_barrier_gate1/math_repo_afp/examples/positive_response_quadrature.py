"""Construct a positive spherical rule enriched by synthetic response modes."""
from __future__ import annotations

import json
import numpy as np

from hts_angular import (
    finite_pool_positive_quadrature,
    fit_graph_generator,
    gauss_legendre_product_sphere,
    real_spherical_harmonics,
    response_error_from_moment_residual,
)


def normalized_rows(rows: np.ndarray) -> np.ndarray:
    scale = np.maximum(np.linalg.norm(rows, axis=1), 1e-15)
    return rows / scale[:, None]


def main() -> None:
    reference = gauss_legendre_product_sphere(16, 32, phase=0.25)
    pool = gauss_legendre_product_sphere(10, 20, phase=0.25)
    harmonics_ref, _ = real_spherical_harmonics(reference.nodes, 2)
    harmonics_pool, _ = real_spherical_harmonics(pool.nodes, 2)
    directions = np.array([[1.0, 0.2, 0.0], [-0.4, 0.1, 1.0]])
    response_ref = normalized_rows(np.exp(4.0 * directions @ reference.nodes.T))
    response_pool = normalized_rows(np.exp(4.0 * directions @ pool.nodes.T))
    features_ref = np.vstack([harmonics_ref, response_ref])
    features_pool = np.vstack([harmonics_pool, response_pool])
    target = features_ref @ reference.weights
    fit = finite_pool_positive_quadrature(pool.nodes, features_pool, target, tolerance=2e-9)
    if not fit.exact or fit.quadrature is None:
        raise RuntimeError(f"positive fit failed: {fit.status}")
    graph = fit_graph_generator(fit.quadrature.nodes, fit.quadrature.weights, maximum_degree=2)
    certificate = response_error_from_moment_residual(
        fit.residual,
        response_coefficients=np.eye(features_pool.shape[0])[-2:],
        unresolved_integral_bounds=np.zeros(2),
    )
    summary = {
        "candidate_nodes": pool.n_node,
        "active_nodes": fit.quadrature.n_node,
        "maximum_moment_residual": float(np.max(np.abs(fit.residual))),
        "response_error_bounds": certificate.per_response_bound.tolist(),
        "graph_connected": graph.connectivity_diagnostics().connected,
        "graph_fit_residual": graph.fit_residual_norm,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
