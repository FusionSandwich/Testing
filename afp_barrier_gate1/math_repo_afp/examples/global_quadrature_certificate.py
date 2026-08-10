from __future__ import annotations

import json

from hts_angular import node_count_certificate, regular_tetrahedron_rule, variable_node_positive_quadrature

analytic = node_count_certificate(regular_tetrahedron_rule(), 2)
constructed = variable_node_positive_quadrature(2, 4, starts=3, seed=19)
print(
    json.dumps(
        {
            "globally_minimal": analytic.globally_node_minimal,
            "analytic_residual": analytic.residual_inf,
            "variable_rule_exact": constructed.exact,
            "variable_rule_residual": constructed.residual_inf,
        },
        indent=2,
        sort_keys=True,
    )
)
