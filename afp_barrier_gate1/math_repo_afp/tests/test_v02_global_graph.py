from __future__ import annotations

import math

import numpy as np
import pytest

from hts_angular import (
    GraphGenerator,
    axis_quadrature_sphere,
    candidate_pool_minimum_certificate,
    certify_graph_family,
    fibonacci_sphere,
    fit_graph_generator,
    harmonic_gram_lower_bound,
    node_count_certificate,
    regular_tetrahedron_rule,
    spherical_grid_quality,
    variable_node_positive_quadrature,
)


def test_tetrahedron_attains_global_positive_degree_two_lower_bound() -> None:
    rule = regular_tetrahedron_rule()
    certificate = node_count_certificate(rule, 2)
    assert harmonic_gram_lower_bound(2) == 4
    assert certificate.exact
    assert certificate.globally_node_minimal
    assert certificate.node_count == certificate.harmonic_gram_lower_bound
    assert certificate.residual_inf < 2e-15


def test_variable_node_degree_two_construction_is_exact_and_reproducible() -> None:
    first = variable_node_positive_quadrature(2, 4, starts=3, seed=19)
    second = variable_node_positive_quadrature(2, 4, starts=3, seed=19)
    assert first.exact and second.exact
    assert first.quadrature is not None and second.quadrature is not None
    np.testing.assert_array_equal(first.quadrature.nodes, second.quadrature.nodes)
    np.testing.assert_array_equal(first.quadrature.weights, second.quadrature.weights)
    assert first.certificate.globally_node_minimal
    assert first.minimum_weight > 0.0
    assert first.minimum_separation_radians > 1.0


def test_fixed_candidate_pool_minimum_support_certificate() -> None:
    tetra = regular_tetrahedron_rule()
    axes = axis_quadrature_sphere()
    nodes = np.vstack([tetra.nodes, axes.nodes])
    certificate = candidate_pool_minimum_certificate(nodes, 2, time_limit=10.0)
    assert certificate.exact
    assert certificate.fixed_pool_minimal
    assert certificate.support == 4
    assert certificate.fit.quadrature is not None
    assert np.min(certificate.fit.quadrature.weights) > 0.0


def _good_graphs() -> list[GraphGenerator]:
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
    return graphs


def test_graph_family_issues_only_conditional_finite_family_bound() -> None:
    certificate = certify_graph_family(
        _good_graphs(),
        maximum_degree=2,
        sample_count=2048,
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
        minimum_fitted_order=0.5,
    )
    assert certificate.passed
    assert 1.5 < certificate.fitted_order < 2.8
    assert certificate.minimum_adjacent_order > 1.5
    assert certificate.maximum_envelope_ratio <= 1.0 + 1e-14
    midpoint = 0.5 * sum(certificate.fill_distance_interval)
    assert certificate.error_bound(midpoint) > 0.0
    with pytest.raises(ValueError, match="outside the audited"):
        certificate.error_bound(0.5 * certificate.fill_distance_interval[0])
    for record in certificate.records:
        assert certificate.error_bound(record.fill_distance) >= record.maximum_weighted_relative_residual * (1.0 - 1e-13)
        assert record.relative_total_weight_error < 1e-14
    assert "audited finite graph family" in certificate.conditional_statement
    assert certificate.records[-1].maximum_weighted_relative_residual < certificate.records[0].maximum_weighted_relative_residual


def test_disconnected_graph_family_fails_closed() -> None:
    graphs = _good_graphs()
    broken: list[GraphGenerator] = []
    for graph in graphs:
        conductances = np.zeros_like(graph.conductances)
        generator = np.zeros_like(graph.generator)
        broken.append(
            GraphGenerator(
                graph.nodes,
                graph.weights,
                conductances,
                generator,
                np.empty((0, 2), dtype=int),
                graph.fit_residual_norm,
                {"fixture": "disconnected"},
            )
        )
    certificate = certify_graph_family(
        broken,
        maximum_degree=2,
        sample_count=1024,
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
    )
    assert not certificate.passed
    assert any("disconnected" in reason for reason in certificate.reasons)
    with pytest.raises(ValueError, match="no conditional bound"):
        certificate.error_bound(0.1)


def test_spherical_grid_quality_detects_clustered_geometry_and_weight_imbalance() -> None:
    nodes = np.array(
        [
            [0.0, 0.0, 1.0],
            [1e-5, 0.0, 1.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, -1.0],
        ]
    )
    weights = np.array([1e-6, 1.0, 1.0, 1.0, 4.0 * np.pi - 3.000001])
    quality = spherical_grid_quality(nodes, weights, sample_count=1024)
    assert quality.mesh_ratio > 1e4
    assert quality.weight_ratio > 1e6
    assert math.isfinite(quality.approximate_fill_distance)


def test_graph_family_rejects_incorrect_sphere_measure_normalization() -> None:
    graphs = _good_graphs()
    scaled: list[GraphGenerator] = []
    for graph in graphs:
        weights = 1.01 * graph.weights
        # Preserve the same conductance matrix and rebuild the weighted generator
        # so exact graph structure remains valid; only the physical measure is wrong.
        generator = graph.conductances / weights[:, None]
        np.fill_diagonal(generator, -np.sum(graph.conductances, axis=1) / weights)
        scaled.append(
            GraphGenerator(
                graph.nodes,
                weights,
                graph.conductances,
                generator,
                graph.edges,
                graph.fit_residual_norm,
                {"fixture": "misnormalized-sphere-measure"},
            )
        )
    certificate = certify_graph_family(
        scaled,
        maximum_degree=2,
        sample_count=1024,
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
        maximum_relative_total_weight_error=1e-6,
    )
    assert not certificate.passed
    assert any("constant mode" in reason for reason in certificate.reasons)


def test_minimum_separation_normalizes_public_node_inputs() -> None:
    from hts_angular.global_quadrature import minimum_separation

    separation = minimum_separation(np.array([[0.0, 0.0, 2.0], [3.0, 0.0, 0.0]]))
    assert separation == pytest.approx(0.5 * np.pi)


def test_variable_node_controls_fail_closed() -> None:
    with pytest.raises(ValueError, match="seed must be an integer"):
        variable_node_positive_quadrature(2, 4, seed=1.5)
    with pytest.raises(ValueError, match="tolerance must be finite and positive"):
        variable_node_positive_quadrature(2, 4, tolerance=0.0)
    with pytest.raises(ValueError, match="separation_weight"):
        variable_node_positive_quadrature(2, 4, separation_weight=-1.0)
    with pytest.raises(ValueError, match="maximum_evaluations"):
        variable_node_positive_quadrature(2, 4, maximum_evaluations=0)


def test_graph_family_rejects_intermediate_consistency_regression(monkeypatch) -> None:
    import hts_angular.graph_convergence as convergence

    def record(nodes: int, fill: float, error: float) -> convergence.HarmonicConsistencyRecord:
        return convergence.HarmonicConsistencyRecord(
            node_count=nodes,
            fill_distance=fill,
            mesh_ratio=1.2,
            weight_ratio=1.0,
            total_weight=4.0 * np.pi,
            relative_total_weight_error=0.0,
            relative_weight_scaling_error=0.0,
            connected=True,
            algebraic_connectivity=0.1,
            structural_residual=0.0,
            maximum_weighted_relative_residual=error,
            mean_weighted_relative_residual=0.5 * error,
        )

    records = (record(12, 0.8, 0.4), record(24, 0.6, 0.2), record(48, 0.4, 0.25))
    monkeypatch.setattr(convergence, "graph_family_records", lambda *_args, **_kwargs: records)
    certificate = convergence.certify_graph_family(
        [object(), object(), object()],
        maximum_mesh_ratio=5.0,
        maximum_weight_ratio=2.0,
    )
    assert not certificate.passed
    assert certificate.minimum_adjacent_order < 0.0
    assert any("every refinement" in reason for reason in certificate.reasons)
