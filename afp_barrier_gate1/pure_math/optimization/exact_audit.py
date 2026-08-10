#!/usr/bin/env python3
"""Exact algebraic certificates for the P2A symmetric and failure fixtures."""

from __future__ import annotations

import json
from itertools import combinations, product

import sympy as sp

from .fixtures import _exact_degree_two_basis, exact_sampling_certificate


def zero(value: sp.Expr | sp.MatrixBase, label: str) -> None:
    entries = list(value) if isinstance(value, sp.MatrixBase) else [value]
    bad = [sp.simplify(entry) for entry in entries if sp.simplify(entry) != 0]
    if bad:
        raise AssertionError(f"{label}: {bad[:8]}")


def assembly(nodes: list[sp.Matrix], weights: list[sp.Expr], edges: list[tuple[int, int]]):
    n, m = len(nodes), len(edges)
    a = sp.zeros(3 * n, m)
    h = sp.zeros(n, m)
    b = sp.Matrix.vstack(*[-2 * weights[i] * nodes[i] for i in range(n)])
    incidence = sp.zeros(n, m)
    for e, (i, j) in enumerate(edges):
        incidence[i, e], incidence[j, e] = 1, -1
        h[i, e] = h[j, e] = 1
        delta = nodes[j] - nodes[i]
        a[3 * i : 3 * i + 3, e] = delta
        a[3 * j : 3 * j + 3, e] = -delta
    return a, b, h, incidence


def affine_terms(
    incidence: sp.Matrix, weights: list[sp.Expr], frame: sp.Matrix,
) -> tuple[sp.Matrix, list[sp.Matrix]]:
    inverse_root = sp.diag(*[1 / sp.sqrt(weight) for weight in weights])
    terms = []
    for e in range(incidence.cols):
        v = inverse_root * incidence[:, e]
        terms.append(-v * v.T * frame)
    return 6 * frame, terms


def block_dual(frame: sp.Matrix, alpha: sp.Expr) -> sp.Matrix:
    p = frame * frame.T
    top = p.row_join(-frame)
    bottom = (-frame.T).row_join(sp.eye(frame.cols))
    return alpha * top.col_join(bottom)


def audit_sdp_dual(
    name: str,
    nodes: list[sp.Matrix],
    weights: list[sp.Expr],
    edges: list[tuple[int, int]],
    gamma: sp.Matrix,
    frame: sp.Matrix,
    defect: sp.Expr,
    rate: sp.Expr,
    fixed_rate_alpha: sp.Expr,
    fixed_rate_z: sp.Expr,
    fixed_defect_alpha: sp.Expr,
    fixed_defect_z: sp.Expr,
) -> None:
    a, b, h, incidence = assembly(nodes, weights, edges)
    zero(a * gamma - b, f"{name} H1")
    t0, terms = affine_terms(incidence, weights, frame)
    residual = t0 + sum((gamma[e] * terms[e] for e in range(len(edges))), sp.zeros(len(nodes), frame.cols))
    zero(residual - defect * frame, f"{name} scalar quotient residual")

    for mode, alpha, zvalue in (
        ("fixed-rate", fixed_rate_alpha, fixed_rate_z),
        ("fixed-defect", fixed_defect_alpha, fixed_defect_z),
    ):
        zmat = block_dual(frame, alpha)
        factor = frame.col_join(-sp.eye(frame.cols))
        zero(zmat - alpha * factor * factor.T, f"{name} {mode} PSD factor")
        cross = zmat[: len(nodes), len(nodes) :]
        derivative = sp.Matrix([sp.trace(cross.T * term) for term in terms])
        z = sp.ones(len(nodes), 1) * zvalue
        # Cross-block factor two is literal.
        zero(h.T * z - 2 * derivative, f"{name} {mode} stationarity")
        if mode == "fixed-rate":
            zero(sp.trace(zmat) - 1, f"{name} fixed-rate trace normalization")
            dual = -rate * (sp.Matrix(weights).dot(z)) - 2 * sp.trace(cross.T * t0)
            zero(dual - defect, f"{name} fixed-rate dual value")
        else:
            zero(sp.Matrix(weights).dot(z) - 1, f"{name} fixed-defect rate normalization")
            diag_trace = sp.trace(zmat[: len(nodes), : len(nodes)]) + sp.trace(zmat[len(nodes) :, len(nodes) :])
            dual = -defect * diag_trace - 2 * sp.trace(cross.T * t0)
            zero(dual - rate, f"{name} fixed-defect dual value")


def tetrahedron() -> dict[str, object]:
    signs = [v for v in product((1, -1), repeat=3) if v[0] * v[1] * v[2] == 1]
    nodes = [sp.Matrix(v) / sp.sqrt(3) for v in signs]
    weights = [sp.Rational(1, 4)] * 4
    edges = list(combinations(range(4), 2))
    certificate = exact_sampling_certificate(nodes, weights)
    if certificate.rank != 3 or len(certificate.nullspace) != 2:
        raise AssertionError("tetra exact sampling rank/nullity")
    frame = sp.Matrix([
        [1 / sp.sqrt(2), 1 / sp.sqrt(6), 1 / sp.sqrt(12)],
        [-1 / sp.sqrt(2), 1 / sp.sqrt(6), 1 / sp.sqrt(12)],
        [0, -2 / sp.sqrt(6), 1 / sp.sqrt(12)],
        [0, 0, -3 / sp.sqrt(12)],
    ])
    zero(frame.T * frame - sp.eye(3), "tetra frame orthonormality")
    audit_sdp_dual(
        "tetra", nodes, weights, edges, sp.ones(6, 1) / 8, frame,
        sp.Integer(4), sp.Rational(3, 2),
        sp.Rational(1, 6), sp.Rational(4, 3),
        sp.Rational(1, 8), sp.Integer(1),
    )
    # The fixed-rate dual at value four is also an exact strict infeasibility
    # ray for the contradictory caps R=3/2 and delta=39/10.  Its separation
    # is dual_value - delta*trace(Z) = 1/10.
    conic_separation = sp.Integer(4) - sp.Rational(39, 10) * sp.Integer(1)
    zero(conic_separation - sp.Rational(1, 10), "tetra exact conic separation")
    return {
        "rank": 3, "nullity": 2, "gamma": "1/8", "defect": "4", "rate": "3/2",
        "fixed_rate_defect_39_10_infeasibility_separation": "1/10",
    }


def octahedron() -> dict[str, object]:
    raw = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    nodes = [sp.Matrix(v) for v in raw]
    weights = [sp.Rational(1, 6)] * 6
    edges = [(i, j) for i, j in combinations(range(6), 2) if (nodes[i].T * nodes[j])[0] == 0]
    certificate = exact_sampling_certificate(nodes, weights)
    if certificate.rank != 2 or len(certificate.nullspace) != 3:
        raise AssertionError("octa exact sampling rank/nullity")
    frame = sp.Matrix([
        [sp.Rational(1, 2), 1 / sp.sqrt(12)],
        [sp.Rational(1, 2), 1 / sp.sqrt(12)],
        [-sp.Rational(1, 2), 1 / sp.sqrt(12)],
        [-sp.Rational(1, 2), 1 / sp.sqrt(12)],
        [0, -2 / sp.sqrt(12)],
        [0, -2 / sp.sqrt(12)],
    ])
    zero(frame.T * frame - sp.eye(2), "octa frame orthonormality")
    audit_sdp_dual(
        "octa", nodes, weights, edges, sp.ones(len(edges), 1) / 12, frame,
        sp.Integer(3), sp.Integer(2),
        sp.Rational(1, 4), sp.Rational(3, 2),
        sp.Rational(1, 6), sp.Integer(1),
    )
    return {"rank": 2, "nullity": 3, "gamma": "1/12", "defect": "3", "rate": "2"}


def cube_cost_and_farkas() -> dict[str, object]:
    signs = list(product((1, -1), repeat=3))
    nodes = [sp.Matrix(v) / sp.sqrt(3) for v in signs]
    weights = [sp.Rational(1, 5) if v in {(1, 1, 1), (-1, -1, -1)} else sp.Rational(1, 10) for v in signs]
    edges = [
        (i, j) for i, j in combinations(range(8), 2)
        if sum(a != b for a, b in zip(signs[i], signs[j], strict=True)) == 1
    ]
    a, b, _, _ = assembly(nodes, weights, edges)
    field = sp.Matrix.vstack(*(sp.Matrix([node[1], node[2], node[0]]) for node in nodes))
    zero(a.T * field, "cube Farkas edge work")
    zero((b.T * field)[0] + sp.Rational(2, 5), "cube Farkas negative work")

    # Two feasible equal-mass shell designs have the same support size but
    # different plain l1 costs.  Both have fixed loss-weighted cost one.
    equal_weights = [sp.Rational(1, 8)] * 8
    totals = {}
    for distance, rate in ((1, sp.Integer(1)), (2, sp.Rational(1, 2))):
        shell_edges = [
            (i, j) for i, j in combinations(range(8), 2)
            if sum(x != y for x, y in zip(signs[i], signs[j], strict=True)) == distance
        ]
        sa, sb, _, _ = assembly(nodes, equal_weights, shell_edges)
        gamma = sp.ones(len(shell_edges), 1) * rate / 8
        zero(sa * gamma - sb, f"cube Hamming-{distance} H1")
        losses = sp.Matrix([1 - (nodes[i].T * nodes[j])[0] for i, j in shell_edges])
        zero((losses.T * gamma)[0] - 1, f"cube Hamming-{distance} fixed loss cost")
        totals[distance] = sp.simplify(sum(gamma, sp.S.Zero))
    zero(totals[1] - sp.Rational(3, 2), "cube Hamming-1 l1")
    zero(totals[2] - sp.Rational(3, 4), "cube Hamming-2 l1")
    return {"farkas_work": "-2/5", "l1_hamming_1": "3/2", "l1_hamming_2": "3/4", "loss_cost": "1"}


def four_node_identities() -> dict[str, object]:
    nodes = [
        sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]),
        sp.Matrix([-1, 0, 0]), sp.Matrix([0, -1, 0]),
    ]
    cycle = [(0, 1), (1, 2), (2, 3), (0, 3)]
    a, b, _, _ = assembly(nodes, [sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 6), sp.Rational(1, 3)], cycle)
    signs = (-1, 1, -1, 1)
    field = sp.Matrix.vstack(*(signs[i] * nodes[i] for i in range(4)))
    zero(a.T * field, "unequal square Farkas edge work")
    zero((b.T * field)[0] + sp.Rational(2, 3), "unequal square Farkas negative work")
    for i in range(4):
        neighbors = [j for edge in cycle if i in edge for j in edge if j != i]
        zero(sum((nodes[j] - nodes[i] for j in neighbors), sp.zeros(3, 1)) + 2 * nodes[i], f"square local row {i}")

    # Complete graph family: cycle rate theta and antipodal rate 1-theta.
    theta = sp.symbols("theta", nonnegative=True)
    complete = list(combinations(range(4), 2))
    ca, cb, _, _ = assembly(nodes, [sp.Rational(1, 4)] * 4, complete)
    gamma = sp.Matrix([
        (1 - theta) / 4 if (nodes[i].T * nodes[j])[0] == -1 else theta / 4
        for i, j in complete
    ])
    zero(ca * gamma - cb, "four-node complete H1 family")
    losses = sp.Matrix([1 - (nodes[i].T * nodes[j])[0] for i, j in complete])
    zero((losses.T * gamma)[0] - 1, "four-node fixed loss cost")
    zero(sum(gamma, sp.S.Zero) - (1 + theta) / 2, "four-node variable total conductance")
    return {
        "unequal_cycle_farkas_work": "-2/3",
        "complete_total_conductance": "(1+theta)/2",
        "complete_loss_weighted_cost": "1",
        "l1_preferred_endpoint": "theta=0 antipodal",
    }


def full_rank_determinant() -> dict[str, object]:
    q, s = sp.symbols("q s", nonzero=True)
    nodes = [
        (1, 0, 0), (0, 1, 0),
        (sp.Rational(3, 5), sp.Rational(4, 5), 0),
        (sp.Rational(3, 5), 0, sp.Rational(4, 5)),
        (0, q, s),
    ]
    rows = [
        [x * x - z * z, y * y - z * z, 2 * x * y, 2 * x * z, 2 * y * z]
        for x, y, z in nodes
    ]
    determinant = sp.factor(sp.Matrix(rows).det())
    zero(determinant - sp.Rational(1152, 625) * q * s, "ten-node full-rank determinant")
    return {"selected_minor_determinant": "1152*q*s/625", "rank": 5}


def main() -> None:
    # Re-audit the public basis itself, independently of floating tests.
    _exact_degree_two_basis()
    record = {
        "arithmetic": "SymPy exact rational/algebraic",
        "tetrahedron": tetrahedron(),
        "octahedron": octahedron(),
        "cube": cube_cost_and_farkas(),
        "four_node": four_node_identities(),
        "ten_node_condition_family": full_rank_determinant(),
        "cross_block_factor": 2,
    }
    print(json.dumps(record, indent=2, sort_keys=True))
    print("P2A exact symmetric/Farkas audit: PASS")


if __name__ == "__main__":
    main()
