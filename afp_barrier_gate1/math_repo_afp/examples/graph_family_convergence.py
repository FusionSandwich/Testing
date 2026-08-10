from __future__ import annotations

import json

from hts_angular import certify_graph_family, fibonacci_sphere, fit_graph_generator

graphs = []
for count in (12, 24, 48):
    quadrature = fibonacci_sphere(count)
    graphs.append(
        fit_graph_generator(
            quadrature.nodes,
            quadrature.weights,
            maximum_degree=2,
            k_nearest=min(12, count - 1),
            regularization=1e-10,
            conductance_floor=1e-14,
        )
    )
certificate = certify_graph_family(
    graphs,
    maximum_degree=2,
    sample_count=2048,
    maximum_mesh_ratio=5.0,
    maximum_weight_ratio=2.0,
    minimum_fitted_order=0.5,
)
print(
    json.dumps(
        {
            "convergence_certified": certificate.passed,
            "fitted_order": certificate.fitted_order,
            "conditional_statement": certificate.conditional_statement,
        },
        indent=2,
        sort_keys=True,
    )
)
