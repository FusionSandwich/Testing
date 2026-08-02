#!/usr/bin/env python3
"""Exact Prompt 3 audit for Q=1 covariance and the weighted octahedron.

The calculations use SymPy exact arithmetic.  They distinguish form-space
constraints from genuine sampled functions.
"""
from __future__ import annotations

import json
import sympy as sp


def weighted_octahedron_symbolic() -> dict[str, object]:
    g12, g13, g23 = sp.symbols("g12 g13 g23", positive=True)
    g = {(0, 1): g12, (0, 2): g13, (1, 2): g23}
    w = [g12 + g13, g12 + g23, g13 + g23]

    # Tangent second moments at +e_a (identical at -e_a).
    T = []
    C = []
    M = []
    I = sp.eye(3)
    for a in range(3):
        Ta = sp.zeros(3)
        for b in range(3):
            if a == b:
                continue
            gab = g[tuple(sorted((a, b)))]
            Ta[b, b] = sp.simplify(gab / w[a])
        oa = sp.zeros(3, 1)
        oa[a, 0] = 1
        P = I - oa * oa.T
        Ca = sp.simplify(2 * Ta + 2 * oa * oa.T)
        Ma = sp.simplify(3 * (oa * oa.T - I / 3) + 2 * (Ta - P / 2))
        assert sp.simplify(sp.trace(Ta) - 1) == 0
        assert sp.simplify(sp.trace(Ca) - 4) == 0
        assert sp.simplify((oa.T * Ca * oa)[0] - 2) == 0
        T.append(Ta)
        C.append(Ca)
        M.append(Ma)

    axial_conditions = [
        sp.factor(T[0][1, 1] - T[0][2, 2]),
        sp.factor(T[1][0, 0] - T[1][2, 2]),
        sp.factor(T[2][0, 0] - T[2][1, 1]),
    ]
    expected = [
        sp.factor((g12 - g13) / (g12 + g13)),
        sp.factor((g12 - g23) / (g12 + g23)),
        sp.factor((g13 - g23) / (g13 + g23)),
    ]
    assert all(sp.factor(a - b) == 0 for a, b in zip(axial_conditions, expected))

    # Genuine degree-two samples are diagonal values d_a with sum d_a=0.
    # On the six-state octahedron L = 2(P-I) on this antipodally even sample
    # sector, so a target Lf=-6f would require Pf=-2f.  The exact equations are
    # assembled below and have only the zero trace-free solution for all
    # positive parameters.  A robust algebraic certificate is the maximum
    # principle: |Pf|_infty <= |f|_infty, incompatible with eigenvalue -2.
    d1, d2 = sp.symbols("d1 d2")
    d = sp.Matrix([d1, d2, -d1 - d2])
    equations = []
    for a in range(3):
        Pa = sum(g[tuple(sorted((a, b)))] * d[b] for b in range(3) if b != a) / w[a]
        equations.append(sp.factor(Pa + 2 * d[a]))
    # Any two equations already give a generically invertible 2x2 system;
    # positivity plus the max principle handles all positive specializations.
    J = sp.Matrix([[sp.diff(equations[i], z) for z in (d1, d2)] for i in range(3)])
    minors = [sp.factor(J.extract(rows, [0, 1]).det()) for rows in ((0, 1), (0, 2), (1, 2))]

    # A concrete unequal-mass exact specialization.
    subs = {g12: sp.Rational(1), g13: sp.Rational(2), g23: sp.Rational(5)}
    spec = {
        "weights": [str(sp.simplify(x.subs(subs))) for x in w],
        "T_plus_e1": [[str(sp.simplify(T[0][i, j].subs(subs))) for j in range(3)] for i in range(3)],
        "C_plus_e1": [[str(sp.simplify(C[0][i, j].subs(subs))) for j in range(3)] for i in range(3)],
        "M_plus_e1": [[str(sp.simplify(M[0][i, j].subs(subs))) for j in range(3)] for i in range(3)],
    }

    return {
        "row_rate": "2",
        "edge_loss": "1",
        "Q": "1",
        "axial_all_vertices_iff": "g12 = g13 = g23",
        "sampled_degree_two_space": "{0}",
        "sampled_certificate": "P f = -2 f contradicts ||P f||_infinity <= ||f||_infinity unless f=0",
        "linear_system_minors": [str(x) for x in minors],
        "unequal_example": spec,
    }


def platonic_q1_regressions() -> dict[str, object]:
    sqrt5 = sp.sqrt(5)
    rows = {
        "tetrahedron": (4, 3, sp.Rational(-1, 3)),
        "octahedron": (6, 4, sp.Rational(0)),
        "cube": (8, 3, sp.Rational(1, 3)),
        "icosahedron": (12, 5, 1 / sqrt5),
        "dodecahedron": (20, 3, sqrt5 / 3),
    }
    out = {}
    for name, (V, degree, c) in rows.items():
        ell = sp.simplify(1 - c)
        rate = sp.simplify(2 / ell)
        # Uniform edge rate a=rate/degree gives epsilon=rate*ell^2.
        epsilon = sp.simplify(rate * ell**2)
        Q = sp.simplify(rate * epsilon / 4)
        assert Q == 1
        out[name] = {
            "V": V, "degree": degree, "cos_edge": str(c),
            "loss": str(ell), "rate": str(rate), "Q": str(Q),
            "triangulation": name in {"tetrahedron", "octahedron", "icosahedron"},
        }
    return out


def anisotropy_no_control() -> dict[str, str]:
    t = sp.symbols("t", positive=True)
    # At e1 choose g12=t and g13=1.  Tangent eigenvalues are t/(t+1), 1/(t+1).
    anis = sp.simplify(abs(t - 1) / (2 * (t + 1)))
    limit = sp.limit((t - 1) / (2 * (t + 1)), t, sp.oo)
    assert limit == sp.Rational(1, 2)
    return {
        "operator_norm_T_minus_P_over_2": str(anis),
        "limit_as_ratio_to_infinity": str(limit),
        "eta": "0",
    }


def antipodal_boundary() -> dict[str, str]:
    """Two-state Q=1 boundary: covariance is purely radial.

    At loss ell=2 the tangential coefficient is zero, so no geometrically
    determined unit tangent direction should be inferred from the decomposition.
    """
    omega = sp.Matrix([1, 0, 0])
    other = -omega
    rate = sp.Integer(1)
    loss = sp.Integer(2)
    epsilon = rate * loss**2
    quality = sp.simplify(rate * epsilon / 4)
    covariance = sp.simplify(rate * (other - omega) * (other - omega).T)
    assert quality == 1
    assert covariance == 4 * (omega * omega.T)
    assert sp.sqrt(loss * (2 - loss)) == 0
    return {
        "vertices": "{+e1,-e1}",
        "row_rate": "1",
        "loss": "2",
        "Q": "1",
        "covariance": str(covariance),
        "tangent_coefficient": "0",
        "regression": "no geometrically determined unit tangent frame",
    }


def main() -> None:
    report = {
        "weighted_octahedron": weighted_octahedron_symbolic(),
        "platonic_regressions": platonic_q1_regressions(),
        "anisotropy_separation": anisotropy_no_control(),
        "antipodal_boundary": antipodal_boundary(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
