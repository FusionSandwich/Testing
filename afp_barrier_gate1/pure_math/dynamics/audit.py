"""One deterministic NumPy/SciPy regression audit for P2B."""

from __future__ import annotations

import numpy as np

from .bounds import iteration_error_bound, preconditioned_bound
from .core import physical_symmetrizer_dissipativity, validate_reversible_generator
from .manufactured import (
    multigroup_manufactured_fixture,
    spatial_manufactured_fixture,
    tetrahedron_h1_exact_fixture,
    two_node_alias_fixture,
)


def run_numeric_audit() -> dict[str, float]:
    angular = tetrahedron_h1_exact_fixture()
    validate_reversible_generator(angular.generator, angular.weights)
    physical_symmetrizer_dissipativity(angular.generator, np.diag(angular.weights))
    transient = angular.transient(0.4)
    resolvent = angular.resolvent(1.25)
    sharp_alias = two_node_alias_fixture().transient(0.4)
    spatial = spatial_manufactured_fixture()
    multigroup = multigroup_manufactured_fixture()
    assert np.linalg.norm(spatial.commutator, 2) > 0.0
    assert np.linalg.norm(spatial.reference_operator @ spatial.error - spatial.residual) < 2e-14
    assert (
        np.linalg.norm(
            spatial.discrete_operator @ spatial.error - spatial.comparator_residual
        )
        < 2e-14
    )
    assert abs(spatial.response_error - spatial.response_estimator) < 2e-14
    preconditioner = np.diag(np.diag(spatial.discrete_operator))
    preconditioned = preconditioned_bound(
        spatial.discrete_operator, preconditioner, spatial.comparator_residual
    )
    return {
        "angular_transient_error": transient.error,
        "angular_transient_bound": transient.bound,
        "angular_transient_effectivity": transient.effectivity,
        "angular_resolvent_error": resolvent.error,
        "angular_resolvent_bound": resolvent.bound,
        "angular_resolvent_effectivity": resolvent.effectivity,
        "sharp_alias_effectivity": sharp_alias.effectivity,
        "spatial_error": spatial.exact_error,
        "spatial_bound": spatial.coercive_bound,
        "spatial_effectivity": spatial.effectivity,
        "response_error": spatial.response_error,
        "response_estimator": spatial.response_estimator,
        "preconditioned_contraction": preconditioned.contraction,
        "preconditioned_residual_bound": preconditioned.residual_error_bound,
        "iteration_bound_5": iteration_error_bound(preconditioned.contraction, 5, 1.0),
        "low_group_response_error": multigroup.low_group_response_error,
        "multigroup_commutator_norm": float(np.linalg.norm(multigroup.commutator, 2)),
        "equal_kappa_commutator_norm": float(
            np.linalg.norm(multigroup.equal_kappa_commutator, 2)
        ),
    }


if __name__ == "__main__":
    print(run_numeric_audit())
    print("P2B numerical dynamics audit: PASS")
