"""Small deterministic fixtures used by the P2C audit and hostile tests."""

from __future__ import annotations

import numpy as np

from .families import (
    ahrens_beylkin_icosahedral_fixture,
    complete_edges,
    lebedev_6,
    product_rule,
)
from .inner import dense_centered_initializer
from .types import QuadratureCandidate


def octahedral_complete_fixture() -> QuadratureCandidate:
    base = lebedev_6(graph="complete")
    gamma = dense_centered_initializer(base)
    return QuadratureCandidate.build(
        base.family,
        base.nodes,
        base.weights,
        [tuple(map(int, edge)) for edge in base.edges],
        seed_conductance=gamma,
        metadata={**base.metadata, "fixture": "dense-centered"},
    )


def icosahedral_complete_fixture() -> QuadratureCandidate:
    base = ahrens_beylkin_icosahedral_fixture(graph="complete")
    gamma = dense_centered_initializer(base)
    return QuadratureCandidate.build(
        base.family,
        base.nodes,
        base.weights,
        [tuple(map(int, edge)) for edge in base.edges],
        seed_conductance=gamma,
        metadata={**base.metadata, "fixture": "dense-centered"},
    )


def singular_sampling_fixture() -> QuadratureCandidate:
    """Two antipodal nodes: exact H1 but rank-deficient every even shell."""

    nodes = np.asarray([[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]])
    weights = np.asarray([0.5, 0.5])
    return QuadratureCandidate.build(
        "singular_antipodal",
        nodes,
        weights,
        [(0, 1)],
        seed_conductance=np.asarray([0.5]),
        metadata={"purpose": "moving-Gram kernel regression"},
    )


def product_complete_fixture() -> QuadratureCandidate:
    base = product_rule(2, 4, graph="complete")
    gamma = dense_centered_initializer(base)
    return QuadratureCandidate.build(
        base.family,
        base.nodes,
        base.weights,
        [tuple(map(int, edge)) for edge in base.edges],
        seed_conductance=gamma,
        metadata={**base.metadata, "fixture": "dense-centered"},
    )


def graph_pair_fixture() -> tuple[QuadratureCandidate, QuadratureCandidate]:
    """Weak octahedral graph and its complete supergraph on identical X,w."""

    weak = lebedev_6(graph="weak_delaunay")
    complete = lebedev_6(graph="complete")
    return weak, complete


def all_smoke_fixtures() -> tuple[QuadratureCandidate, ...]:
    return (
        octahedral_complete_fixture(),
        icosahedral_complete_fixture(),
        product_complete_fixture(),
        singular_sampling_fixture(),
    )
