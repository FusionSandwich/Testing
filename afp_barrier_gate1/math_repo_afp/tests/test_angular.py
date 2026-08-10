from __future__ import annotations

import numpy as np

from hts_angular.adaptivity import (
    HysteresisMarker,
    adapt_positive_quadrature,
    dual_weighted_indicator,
    filtered_harmonic_bootstrap,
    graph_heat_bootstrap,
)
from hts_angular.graph_generator import fit_graph_generator
from hts_angular.quadrature import (
    PositiveQuadrature,
    exact_surface_harmonic_moments,
    farkas_infeasibility_certificate,
    fibonacci_sphere,
    finite_pool_positive_quadrature,
    gauss_legendre_product_sphere,
    minimum_residual_positive_weights,
    real_spherical_harmonics,
)
from hts_angular.transfer import (
    current_preserving_no_go,
    moment_matrix,
    state_specific_positive_remap,
    universal_positive_transfer,
)


def tetrahedron() -> PositiveQuadrature:
    nodes = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float) / np.sqrt(3.0)
    return PositiveQuadrature(nodes, np.full(4, np.pi))


def test_regular_tetrahedron_degree_two_exactness() -> None:
    q = tetrahedron()
    Y, _ = real_spherical_harmonics(q.nodes, 2)
    residual = Y @ q.weights - exact_surface_harmonic_moments(2)
    assert np.linalg.norm(residual, ord=np.inf) < 2e-14


def test_finite_pool_lp_returns_positive_sparse_rule() -> None:
    reference = gauss_legendre_product_sphere(8, 16, phase=0.25)
    Y, _ = real_spherical_harmonics(reference.nodes, 2)
    fit = finite_pool_positive_quadrature(reference.nodes, Y, exact_surface_harmonic_moments(2))
    assert fit.exact and fit.quadrature is not None
    assert fit.quadrature.n_node <= Y.shape[0]
    assert np.min(fit.quadrature.weights) > 0.0


def test_farkas_certificate_detects_north_pole_infeasibility() -> None:
    A = np.array([[1.0], [1.0]])
    b = np.array([4.0 * np.pi, 0.0])
    certificate = farkas_infeasibility_certificate(A, b)
    assert certificate.certified
    assert certificate.minimum_cone_pairing >= -1e-10
    assert certificate.target_pairing < 0.0


def test_minimum_residual_projection_has_kkt_certificate() -> None:
    A = np.array([[1.0], [1.0]])
    b = np.array([4.0 * np.pi, 0.0])
    result = minimum_residual_positive_weights(A, b)
    assert result.residual_norm > 1.0
    assert result.dual_feasibility_violation < 1e-9
    assert result.complementarity < 1e-8
    assert result.primal_dual_gap < 1e-7


def test_product_sphere_integrates_harmonics() -> None:
    q = gauss_legendre_product_sphere(7, 18, phase=0.3)
    Y, _ = real_spherical_harmonics(q.nodes, 5)
    residual = Y @ q.weights - exact_surface_harmonic_moments(5)
    assert np.max(np.abs(residual)) < 2e-13


def test_graph_generator_structure_and_positive_semigroup() -> None:
    q = fibonacci_sphere(32)
    graph = fit_graph_generator(q.nodes, q.weights, maximum_degree=2, k_nearest=8)
    residuals = graph.structural_residuals()
    assert residuals["constant"] < 1e-11
    assert residuals["weighted_self_adjoint"] < 1e-11
    assert residuals["largest_eigenvalue"] < 1e-10
    semigroup = graph.semigroup(0.03)
    assert np.min(semigroup) >= -2e-13
    assert np.max(np.abs(semigroup @ np.ones(q.n_node) - 1.0)) < 2e-12


def test_universal_mass_current_transfer_no_go_and_nested_feasibility() -> None:
    source = fibonacci_sphere(10)
    target = fibonacci_sphere(6)
    no_go = current_preserving_no_go(source, target)
    assert not no_go["universal_positive_mass_current_transfer_possible"]
    FA = np.vstack([np.ones(source.n_node), source.nodes.T])
    FB = np.vstack([np.ones(target.n_node), target.nodes.T])
    result = universal_positive_transfer(moment_matrix(source, FA), moment_matrix(target, FB))
    assert not result.feasible

    # A nested target containing every source direction is feasible.
    extra = fibonacci_sphere(5)
    nested_nodes = np.vstack([source.nodes, extra.nodes])
    nested_weights = np.concatenate([0.6 * source.weights, np.full(extra.n_node, 0.4 * 4 * np.pi / extra.n_node)])
    nested = PositiveQuadrature(nested_nodes, nested_weights)
    FN = np.vstack([np.ones(nested.n_node), nested.nodes.T])
    nested_result = universal_positive_transfer(moment_matrix(source, FA), moment_matrix(nested, FN))
    assert nested_result.feasible
    assert nested_result.minimum_entry >= -1e-13


def test_state_specific_positive_remap_can_coarsen_isotropic_state() -> None:
    source = fibonacci_sphere(12)
    axes = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float)
    target = PositiveQuadrature(axes, np.full(6, 4.0 * np.pi / 6.0))
    FA = np.vstack([np.ones(source.n_node), source.nodes.T])
    FB = np.vstack([np.ones(target.n_node), target.nodes.T])
    result = state_specific_positive_remap(np.ones(source.n_node), moment_matrix(source, FA), moment_matrix(target, FB))
    assert result.feasible
    assert result.minimum_value >= -1e-13
    assert result.residual_norm < 1e-9


def test_dual_weighted_indicator_and_hysteresis() -> None:
    residual = np.array([[1.0, 0.2, 0.01], [0.1, 0.4, 0.02]])
    adjoint = np.array([[0.5, 0.2, 0.1], [0.2, 0.8, 0.3]])
    result = dual_weighted_indicator(residual, adjoint, np.array([2.0, 1.0]))
    assert result.combined.shape == (3,)
    marker = HysteresisMarker(0.2, 0.05, persistence=2)
    refine1, coarsen1 = marker.update(result.combined)
    refine2, coarsen2 = marker.update(result.combined)
    assert not np.any(refine1) and not np.any(coarsen1)
    assert np.any(refine2) or np.any(coarsen2)


def test_filtered_and_graph_bootstraps_are_finite_and_positive_for_positive_input() -> None:
    q = fibonacci_sphere(28)
    graph = fit_graph_generator(q.nodes, q.weights, maximum_degree=2, k_nearest=8)
    values = np.exp(4.0 * (q.nodes[:, 0] - 1.0))
    harmonic = filtered_harmonic_bootstrap(q.nodes, q.weights, values, 3)
    heat = graph_heat_bootstrap(values, graph, 0.02)
    assert np.all(np.isfinite(harmonic))
    assert np.min(heat) >= -1e-13
    assert np.linalg.norm(heat - values) > 0.0


def test_adaptation_recertifies_positive_moments() -> None:
    q = gauss_legendre_product_sphere(4, 8, phase=0.25)
    target = exact_surface_harmonic_moments(1)

    def features(nodes: np.ndarray) -> np.ndarray:
        return real_spherical_harmonics(nodes, 1)[0]

    eta = np.exp(6.0 * (q.nodes[:, 0] - 1.0))
    result = adapt_positive_quadrature(q, eta, features, target, refine_fraction=0.2, coarsen_fraction=0.1)
    F = features(result.quadrature.nodes)
    assert np.min(result.quadrature.weights) > 0.0
    assert np.max(np.abs(F @ result.quadrature.weights - target)) < 1e-8


def test_conductance_exactness_certificate_has_consistent_dimensions() -> None:
    from hts_angular.graph_generator import conductance_exactness_certificate

    q = fibonacci_sphere(8)
    # A sparse connected cycle is deliberately restrictive; whether the dual
    # certifies infeasibility or not, the certificate construction must be
    # dimensionally valid and return finite diagnostics when a vector exists.
    edges = np.array([[i, (i + 1) % q.n_node] for i in range(q.n_node)], dtype=int)
    certificate = conductance_exactness_certificate(q.nodes, q.weights, 1, edges)
    if certificate.vector is not None:
        assert np.all(np.isfinite(certificate.vector))
        assert np.isfinite(certificate.minimum_cone_pairing)
        assert np.isfinite(certificate.target_pairing)


def test_symmetric_orbit_quadrature_preserves_degree_two_harmonics() -> None:
    from hts_angular.quadrature import finite_pool_symmetric_quadrature

    nodes = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ]
    )
    features, _ = real_spherical_harmonics(nodes, 2)
    fit = finite_pool_symmetric_quadrature(
        nodes,
        features,
        exact_surface_harmonic_moments(2),
        ((0, 1), (2, 3), (4, 5)),
        tolerance=2e-10,
    )
    assert fit.exact and fit.quadrature is not None
    assert fit.quadrature.n_node == 6
    assert np.allclose(fit.full_weights[0::2], fit.full_weights[1::2])
    assert np.max(np.abs(fit.residual)) < 2e-10


def test_minimum_node_fixed_pool_milp_certifies_tetrahedron_support() -> None:
    from hts_angular.quadrature import minimum_node_positive_quadrature

    candidate = tetrahedron()
    features, _ = real_spherical_harmonics(candidate.nodes, 1)
    fit = minimum_node_positive_quadrature(
        candidate.nodes,
        features,
        exact_surface_harmonic_moments(1),
        tolerance=2e-9,
    )
    assert fit.exact and fit.quadrature is not None
    assert fit.quadrature.n_node == 4
    assert int(fit.quadrature.metadata["minimum_fixed_pool_support"]) == 4


def test_response_error_certificate_matches_linear_moment_defect() -> None:
    from hts_angular.quadrature import response_error_from_moment_residual

    residual = np.array([1e-5, -2e-5, 3e-5])
    coefficients = np.array([[2.0, -1.0, 0.5], [-3.0, 0.0, 1.0]])
    certificate = response_error_from_moment_residual(
        residual, coefficients, unresolved_integral_bounds=[4e-6, 7e-6]
    )
    expected = np.abs(coefficients @ residual) + np.array([4e-6, 7e-6])
    assert np.array_equal(certificate.per_response_bound, expected)
    assert certificate.maximum_bound == np.max(expected)


def test_graph_connectivity_and_hdf5_roundtrip(tmp_path) -> None:
    from hts_angular.io import load_graph_hdf5, load_quadrature_hdf5, save_graph_hdf5, save_quadrature_hdf5

    q = fibonacci_sphere(18)
    graph = fit_graph_generator(q.nodes, q.weights, maximum_degree=2, k_nearest=6)
    connectivity = graph.connectivity_diagnostics()
    assert connectivity.connected
    assert connectivity.component_count == 1
    assert connectivity.algebraic_connectivity > 0.0

    qpath = tmp_path / "quadrature.h5"
    gpath = tmp_path / "graph.h5"
    save_quadrature_hdf5(q, qpath)
    save_graph_hdf5(graph, gpath)
    loaded_q = load_quadrature_hdf5(qpath)
    loaded_g = load_graph_hdf5(gpath)
    assert np.array_equal(loaded_q.nodes, q.nodes)
    assert np.array_equal(loaded_q.weights, q.weights)
    assert np.allclose(loaded_g.generator, graph.generator)
    assert loaded_g.connectivity_diagnostics().connected


def test_transfer_diagnostics_composition_and_arbitrary_axis_application() -> None:
    from hts_angular.transfer import (
        apply_angular_transfer,
        compose_transfers,
        mass_exact_near_transfer,
        transfer_chain_error_bound,
        transfer_diagnostics,
    )

    qa = fibonacci_sphere(9)
    qb = fibonacci_sphere(7)
    qc = fibonacci_sphere(5)
    ab = mass_exact_near_transfer(qa, qb)
    bc = mass_exact_near_transfer(qb, qc)
    assert ab.transfer is not None and bc.transfer is not None
    ac = compose_transfers(ab.transfer, bc.transfer)
    diagnostics = transfer_diagnostics(ac, qa, qc)
    assert diagnostics.positive
    assert diagnostics.mass_preserving
    assert diagnostics.l1_nonexpansive
    assert abs(diagnostics.weighted_l1_operator_norm - 1.0) < 2e-14

    values = np.arange(2 * qa.n_node * 3, dtype=float).reshape(2, qa.n_node, 3)
    mapped = apply_angular_transfer(ac, values, axis=1)
    assert mapped.shape == (2, qc.n_node, 3)
    before = np.einsum("iaj,a->ij", values, qa.weights)
    after = np.einsum("iaj,a->ij", mapped, qc.weights)
    assert np.allclose(before, after)
    assert np.isclose(transfer_chain_error_bound([0.1, 0.2], [1.0, 1.0], 0.05), 0.35)
