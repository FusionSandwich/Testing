#!/usr/bin/env python3
"""Exact Prompt 3 covariance, anisotropy, antipodal, and sampling audit.

All algebraic framework calculations use SymPy over Q(sqrt(5)).  The script
separates form-space aliases from genuine sampled functions and executes an
exact determinant certificate for the positive weighted-octahedron family.
"""
from __future__ import annotations

from dataclasses import dataclass
import itertools
import json

import sympy as sp


@dataclass(frozen=True)
class Framework:
    name: str
    points: tuple[sp.Matrix, ...]
    edge_dot: sp.Expr
    degree: int
    triangulation: bool


def normalized(v: tuple[sp.Expr, sp.Expr, sp.Expr], scale: sp.Expr) -> sp.Matrix:
    return sp.Matrix(v) / scale


def frameworks() -> tuple[Framework, ...]:
    phi = (1 + sp.sqrt(5)) / 2
    tetrahedron = [
        (1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)
    ]
    octahedron = [
        (1, 0, 0), (-1, 0, 0), (0, 1, 0),
        (0, -1, 0), (0, 0, 1), (0, 0, -1),
    ]
    cube = list(itertools.product((-1, 1), repeat=3))
    icosahedron = []
    for s, t in itertools.product((-1, 1), repeat=2):
        icosahedron.extend(((0, s, t * phi), (s, t * phi, 0), (t * phi, 0, s)))
    dodecahedron = list(itertools.product((-1, 1), repeat=3))
    inverse_phi = 1 / phi
    for s, t in itertools.product((-1, 1), repeat=2):
        dodecahedron.extend(
            ((0, s * inverse_phi, t * phi),
             (s * inverse_phi, t * phi, 0),
             (t * phi, 0, s * inverse_phi))
        )
    ico_scale = sp.sqrt(1 + phi**2)
    return (
        Framework(
            "tetrahedron",
            tuple(normalized(v, sp.sqrt(3)) for v in tetrahedron),
            -sp.Rational(1, 3), 3, True,
        ),
        Framework(
            "octahedron", tuple(sp.Matrix(v) for v in octahedron),
            sp.Integer(0), 4, True,
        ),
        Framework(
            "cube", tuple(normalized(v, sp.sqrt(3)) for v in cube),
            sp.Rational(1, 3), 3, False,
        ),
        Framework(
            "icosahedron",
            tuple(normalized(v, ico_scale) for v in dict.fromkeys(icosahedron)),
            1 / sp.sqrt(5), 5, True,
        ),
        Framework(
            "dodecahedron",
            tuple(normalized(v, sp.sqrt(3)) for v in dict.fromkeys(dodecahedron)),
            sp.sqrt(5) / 3, 3, False,
        ),
    )


def exact_edges(framework: Framework) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for i, j in itertools.combinations(range(len(framework.points)), 2):
        dot = sp.simplify((framework.points[i].T * framework.points[j])[0])
        if sp.simplify(dot - framework.edge_dot) == 0:
            result.add((i, j))
    return result


def audit_framework(framework: Framework) -> dict[str, object]:
    edge_set = exact_edges(framework)
    neighbors = {i: [] for i in range(len(framework.points))}
    for i, j in edge_set:
        neighbors[i].append(j)
        neighbors[j].append(i)
    assert all(len(neighbors[i]) == framework.degree for i in neighbors)
    loss = sp.simplify(1 - framework.edge_dot)
    row_rate = sp.simplify(2 / loss)
    edge_rate = sp.simplify(row_rate / framework.degree)
    for i, omega in enumerate(framework.points):
        assert sp.simplify((omega.T * omega)[0] - 1) == 0
        drift = sp.zeros(3, 1)
        epsilon = sp.Integer(0)
        for j in neighbors[i]:
            edge_loss = sp.simplify(
                1 - (omega.T * framework.points[j])[0]
            )
            assert sp.simplify(edge_loss - loss) == 0
            drift += edge_rate * (framework.points[j] - omega)
            epsilon += edge_rate * edge_loss**2
        assert all(sp.simplify(drift[k] + 2 * omega[k]) == 0 for k in range(3))
        assert sp.simplify(row_rate * epsilon / 4 - 1) == 0
    return {
        "V": len(framework.points),
        "E": len(edge_set),
        "degree": framework.degree,
        "edge_dot": str(framework.edge_dot),
        "loss": str(loss),
        "row_rate": str(row_rate),
        "edge_rate": str(edge_rate),
        "Q": "1",
        "triangulation": framework.triangulation,
        "coordinate_eigenmap": "L Omega=-2 Omega (exact)",
    }


def decomposition_identity() -> dict[str, str]:
    ell = sp.symbols("ell", positive=True)
    radial, tangent, identity = sp.symbols("O T I")
    projector = identity - radial
    covariance = 2 * (2 - ell) * tangent + 2 * ell * radial
    direct = sp.expand(covariance + 2 * radial - 2 * identity)
    factored = sp.expand(
        3 * ell * (radial - identity / 3)
        + 2 * (2 - ell) * (tangent - projector / 2)
    )
    assert sp.expand(direct - factored) == 0
    return {"C": str(covariance), "M": str(factored), "domain": "0<ell<2"}


def weighted_octahedron_symbolic() -> dict[str, object]:
    g12, g13, g23 = sp.symbols("g12 g13 g23", positive=True)
    conductance = {(0, 1): g12, (0, 2): g13, (1, 2): g23}
    weights = [g12 + g13, g12 + g23, g13 + g23]
    identity = sp.eye(3)
    tangent_moments: list[sp.Matrix] = []
    covariances: list[sp.Matrix] = []
    residuals: list[sp.Matrix] = []

    for axis in range(3):
        tangent = sp.zeros(3)
        for other_axis in range(3):
            if axis == other_axis:
                continue
            gab = conductance[tuple(sorted((axis, other_axis)))]
            tangent[other_axis, other_axis] = sp.simplify(gab / weights[axis])
        omega = sp.zeros(3, 1)
        omega[axis, 0] = 1
        projector = identity - omega * omega.T
        covariance = sp.simplify(2 * tangent + 2 * omega * omega.T)
        residual = sp.simplify(
            3 * (omega * omega.T - identity / 3)
            + 2 * (tangent - projector / 2)
        )
        assert sp.simplify(sp.trace(tangent) - 1) == 0
        assert sp.simplify(sp.trace(covariance) - 4) == 0
        assert sp.simplify((omega.T * covariance * omega)[0] - 2) == 0
        tangent_moments.append(tangent)
        covariances.append(covariance)
        residuals.append(residual)

    # Verify the coordinate eigenmap directly at +e1; the other axes are cyclic.
    e1, e2, e3 = sp.eye(3).col(0), sp.eye(3).col(1), sp.eye(3).col(2)
    drift_e1 = sp.simplify(
        g12 / weights[0] * ((e2 - e1) + (-e2 - e1))
        + g13 / weights[0] * ((e3 - e1) + (-e3 - e1))
    )
    assert drift_e1 == -2 * e1

    axial_differences = [
        sp.factor(tangent_moments[0][1, 1] - tangent_moments[0][2, 2]),
        sp.factor(tangent_moments[1][0, 0] - tangent_moments[1][2, 2]),
        sp.factor(tangent_moments[2][0, 0] - tangent_moments[2][1, 1]),
    ]
    expected = [
        sp.factor((g12 - g13) / (g12 + g13)),
        sp.factor((g12 - g23) / (g12 + g23)),
        sp.factor((g13 - g23) / (g13 + g23)),
    ]
    assert all(sp.factor(a - b) == 0 for a, b in zip(axial_differences, expected))

    # Genuine even degree-two samples are diagonal values on the three axes.
    # L=2(P-I); exact eigenvalue -6 would require (P+2I)d=0.
    transition = sp.Matrix([
        [0, g12 / weights[0], g13 / weights[0]],
        [g12 / weights[1], 0, g23 / weights[1]],
        [g13 / weights[2], g23 / weights[2], 0],
    ])
    assert all(sp.simplify(sum(transition[i, j] for j in range(3)) - 1) == 0
               for i in range(3))
    determinant = sp.factor((transition + 2 * identity).det())
    expected_det = sp.factor(
        6 * (g12 + g13 + g23) * (g12 * g13 + g12 * g23 + g13 * g23)
        / (weights[0] * weights[1] * weights[2])
    )
    assert sp.simplify(determinant - expected_det) == 0
    # The displayed numerator and denominator are strictly positive for all
    # positive conductances, so this is an executable nonzero determinant
    # certificate, not a form-space rank inference.
    numerator, denominator = sp.fraction(expected_det)
    assert numerator != 0 and denominator != 0

    t = sp.symbols("t", positive=True)
    anisotropy_limit = sp.limit((t - 1) / (2 * (t + 1)), t, sp.oo)
    assert anisotropy_limit == sp.Rational(1, 2)

    specialization = {g12: 1, g13: 2, g23: 5}
    assert sp.simplify(determinant.subs(specialization)) > 0
    return {
        "weights": [str(x) for x in weights],
        "row_rate": "2",
        "edge_loss": "1",
        "Q": "1",
        "coordinate_eigenmap": "L Omega=-2 Omega",
        "T_plus_e1": str(tangent_moments[0]),
        "C_plus_e1": str(covariances[0]),
        "M_plus_e1": str(residuals[0]),
        "axial_differences": [str(x) for x in axial_differences],
        "axial_all_vertices_iff": "g12=g13=g23",
        "det_P_plus_2I": str(determinant),
        "sampled_degree_two_space": "{0}",
        "sampled_certificate": "det(P+2I)>0 for every positive g12,g13,g23",
        "anisotropy_norm_e1": "|g12-g13|/(2(g12+g13))",
        "anisotropy_supremum": str(anisotropy_limit),
        "unequal_specialization_weights": [
            str(sp.simplify(w.subs(specialization))) for w in weights
        ],
    }


def antipodal_boundary() -> dict[str, str]:
    omega = sp.Matrix([1, 0, 0])
    other = -omega
    row_rate = sp.Integer(1)
    loss = sp.Integer(2)
    epsilon = row_rate * loss**2
    quality = sp.simplify(row_rate * epsilon / 4)
    covariance = sp.simplify(row_rate * (other - omega) * (other - omega).T)
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


def radial_near_equality() -> dict[str, str]:
    quality, rate = sp.symbols("Q r", positive=True)
    difference = sp.factor(4 * quality / rate - 4 / rate)
    assert sp.simplify(difference - 4 * (quality - 1) / rate) == 0
    return {
        "trace_C": "4",
        "radial_C": "4Q/r",
        "difference": str(difference),
        "near_bound": "0 <= radial_C-4/r <= 4 eta/r",
    }


def main() -> None:
    report = {
        "arithmetic": "exact SymPy over Q(sqrt(5))",
        "platonic_Q1": {fw.name: audit_framework(fw) for fw in frameworks()},
        "decomposition": decomposition_identity(),
        "weighted_octahedron": weighted_octahedron_symbolic(),
        "antipodal_boundary": antipodal_boundary(),
        "radial": radial_near_equality(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print("Prompt 3 Q=1 covariance audit: PASS")


if __name__ == "__main__":
    main()
