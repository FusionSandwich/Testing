#!/usr/bin/env python3
"""Exact symbolic audit for sampled quadratic covariance theorems.

All Platonic computations use exact SymPy algebraic arithmetic. Floating rank
thresholds are deliberately avoided. The script checks the structural
factorization

    R_X = (L + 2 d I) S_X,

so the sampling kernel is automatically contained in the exact-form kernel.
It is a regression and falsification tool; the general proofs are in the
Prompt 2 theorem document.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import sympy as sp

Q = sp.Rational
SQRT5 = sp.sqrt(5)
PHI = (1 + SQRT5) / 2
INV_PHI = 1 / PHI


@dataclass(frozen=True)
class ExactAudit:
    name: str
    vertices: int
    degree: int
    adjacent_inner_product: sp.Expr
    edge_rate: sp.Expr
    constraint_rank: int
    sampling_rank: int
    exact_form_dimension: int
    sampling_kernel_dimension: int
    exact_sample_dimension: int


def dot(x: tuple[sp.Expr, ...], y: tuple[sp.Expr, ...]) -> sp.Expr:
    return sp.expand(sum(a * b for a, b in zip(x, y, strict=True)))


def tracefree_basis() -> list[sp.Matrix]:
    return [
        sp.diag(1, 0, -1),
        sp.diag(0, 1, -1),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
    ]


def platonic_data() -> dict[str, tuple[list[tuple[sp.Expr, ...]], sp.Expr]]:
    tetrahedron = [
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    ]
    octahedron = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    cube = list(product((-1, 1), repeat=3))
    icosahedron = [
        (0, 1, PHI),
        (0, -1, PHI),
        (0, 1, -PHI),
        (0, -1, -PHI),
        (1, PHI, 0),
        (-1, PHI, 0),
        (1, -PHI, 0),
        (-1, -PHI, 0),
        (PHI, 0, 1),
        (-PHI, 0, 1),
        (PHI, 0, -1),
        (-PHI, 0, -1),
    ]
    dodecahedron: list[tuple[sp.Expr, ...]] = list(product((-1, 1), repeat=3))
    for a in (-1, 1):
        for b in (-1, 1):
            dodecahedron.extend(
                [
                    (0, a * INV_PHI, b * PHI),
                    (a * INV_PHI, b * PHI, 0),
                    (a * PHI, 0, b * INV_PHI),
                ]
            )
    return {
        "tetrahedron": (tetrahedron, sp.Integer(-1)),
        "octahedron": (octahedron, sp.Integer(0)),
        "cube": (cube, sp.Integer(1)),
        "icosahedron": (icosahedron, PHI),
        "dodecahedron": (dodecahedron, SQRT5),
    }


def adjacency(
    raw: list[tuple[sp.Expr, ...]], adjacent_raw_dot: sp.Expr
) -> sp.Matrix:
    n = len(raw)
    result = sp.zeros(n)
    for i in range(n):
        for j in range(i + 1, n):
            if sp.simplify(dot(raw[i], raw[j]) - adjacent_raw_dot) == 0:
                result[i, j] = result[j, i] = 1
    return result


def evaluate_form(matrix: sp.Matrix, x: sp.Matrix) -> sp.Expr:
    return sp.expand((x.T * matrix * x)[0])


def audit_platonic(
    name: str, raw: list[tuple[sp.Expr, ...]], adjacent_raw_dot: sp.Expr
) -> ExactAudit:
    n = len(raw)
    norm2 = sp.simplify(dot(raw[0], raw[0]))
    assert all(sp.simplify(dot(v, v) - norm2) == 0 for v in raw)

    graph = adjacency(raw, adjacent_raw_dot)
    degrees = [int(sum(graph[i, j] for j in range(n))) for i in range(n)]
    assert len(set(degrees)) == 1
    degree = degrees[0]
    alpha = sp.simplify(adjacent_raw_dot / norm2)
    edge_rate = sp.simplify(Q(2, 1) / (degree * (1 - alpha)))

    vertices = [sp.Matrix(v) / sp.sqrt(norm2) for v in raw]
    center = sp.zeros(3, 1)
    second_moment = sp.zeros(3)
    for x in vertices:
        center += x
        second_moment += x * x.T
    assert sp.simplify(center) == sp.zeros(3, 1)
    assert sp.simplify(second_moment - Q(n, 3) * sp.eye(3)) == sp.zeros(3)

    generator = edge_rate * (graph - sp.diag(*degrees))
    vertex_matrix = sp.Matrix.hstack(*vertices).T
    assert sp.simplify(generator * vertex_matrix + 2 * vertex_matrix) == sp.zeros(
        n, 3
    )

    basis = tracefree_basis()
    sampling = sp.Matrix(
        [[evaluate_form(matrix, x) for matrix in basis] for x in vertices]
    )
    assert sp.simplify(sp.ones(1, n) * sampling) == sp.zeros(1, 5)

    # The specialized residual matrix is not independent data:
    # R_X = (L + 6 I) S_X for d=3.
    residual_operator = generator + 6 * sp.eye(n)
    direct_residual = residual_operator * sampling

    constraint_rows: list[list[sp.Expr]] = []
    for i, x in enumerate(vertices):
        covariance = sp.zeros(3)
        for j in range(n):
            if graph[i, j]:
                delta = vertices[j] - x
                covariance += edge_rate * (delta * delta.T)

        assert sp.simplify(sp.trace(covariance) - 4) == 0
        radial = sp.simplify((x.T * covariance * x)[0])
        assert sp.simplify(radial - 2 * (1 - alpha)) == 0

        expected_covariance = (1 + alpha) * sp.eye(3) + (1 - 3 * alpha) * (
            x * x.T
        )
        assert sp.simplify(covariance - expected_covariance) == sp.zeros(3)

        augmented = covariance + 2 * (x * x.T)
        constraint = augmented - sp.trace(augmented) / 3 * sp.eye(3)
        sampling_tensor = x * x.T - sp.eye(3) / 3
        assert sp.simplify(
            constraint - 3 * (1 - alpha) * sampling_tensor
        ) == sp.zeros(3)

        constraint_rows.append(
            [sp.expand(sp.trace(matrix * constraint)) for matrix in basis]
        )

    constraints = sp.Matrix(constraint_rows)
    assert sp.simplify(direct_residual - constraints) == sp.zeros(n, 5)

    rank_constraints = constraints.rank()
    rank_sampling = sampling.rank()
    ambient_dimension = 5
    form_dimension = ambient_dimension - rank_constraints
    sampling_kernel_dimension = ambient_dimension - rank_sampling

    # Because R_X=(L+6I)S_X, ker S_X is always contained in ker R_X.
    for alias in sampling.nullspace():
        assert constraints * alias == sp.zeros(n, 1)

    stacked = constraints.col_join(sampling)
    assert stacked.rank() == rank_sampling
    exact_sample_dimension = rank_sampling - rank_constraints
    assert exact_sample_dimension == form_dimension - sampling_kernel_dimension

    # Axial isotropy strengthens containment to equality for the Platonic rows.
    assert sp.simplify(constraints - 3 * (1 - alpha) * sampling) == sp.zeros(n, 5)
    assert rank_constraints == rank_sampling
    assert exact_sample_dimension == 0

    return ExactAudit(
        name=name,
        vertices=n,
        degree=degree,
        adjacent_inner_product=alpha,
        edge_rate=edge_rate,
        constraint_rank=rank_constraints,
        sampling_rank=rank_sampling,
        exact_form_dimension=form_dimension,
        sampling_kernel_dimension=sampling_kernel_dimension,
        exact_sample_dimension=exact_sample_dimension,
    )


def exact_rank_certificates() -> tuple[sp.Expr, sp.Expr]:
    # Coefficient basis:
    # [x^2-z^2, y^2-z^2, 2xy, 2xz, 2yz].
    icosahedron = [
        (0, 1, PHI),
        (0, -1, PHI),
        (1, PHI, 0),
        (-1, PHI, 0),
        (PHI, 0, 1),
    ]
    dodecahedron = [
        (-1, -1, -1),
        (-1, -1, 1),
        (-1, 1, -1),
        (0, -INV_PHI, -PHI),
        (-INV_PHI, -PHI, 0),
    ]

    def row(v: tuple[sp.Expr, ...]) -> list[sp.Expr]:
        x, y, z = v
        return [x * x - z * z, y * y - z * z, 2 * x * y, 2 * x * z, 2 * y * z]

    det_icosahedron = sp.radsimp(sp.Matrix([row(v) for v in icosahedron]).det())
    det_dodecahedron = sp.factor(
        sp.Matrix([row(v) for v in dodecahedron]).det()
    )
    assert sp.simplify(det_icosahedron - 32 * (11 + 5 * SQRT5)) == 0
    assert det_dodecahedron == -192
    return det_icosahedron, det_dodecahedron


def factorization_rank_test() -> None:
    # A small abstract exact test of R=B*S. The inclusion ker(S)⊆ker(R),
    # stacked-rank collapse, and rank difference all follow without Platonic
    # symmetry.
    sampling = sp.Matrix([[1, 0, 1], [0, 1, 1]])
    residual_on_samples = sp.Matrix([[1, -1], [0, 2]])
    constraints = residual_on_samples * sampling
    for alias in sampling.nullspace():
        assert constraints * alias == sp.zeros(2, 1)
    assert constraints.col_join(sampling).rank() == sampling.rank()
    assert sampling.rank() - constraints.rank() == 0


def signed_square_restoration() -> None:
    half = Q(1, 2)
    generator = sp.Matrix(
        [
            [-Q(3, 2), 1, -half, 1],
            [1, -Q(3, 2), 1, -half],
            [-half, 1, -Q(3, 2), 1],
            [1, -half, 1, -Q(3, 2)],
        ]
    )
    constant = sp.ones(4, 1)
    x_coordinate = sp.Matrix([1, 0, -1, 0])
    y_coordinate = sp.Matrix([0, 1, 0, -1])
    quadratic = sp.Matrix([1, -1, 1, -1])

    assert generator * constant == sp.zeros(4, 1)
    assert generator * x_coordinate == -x_coordinate
    assert generator * y_coordinate == -y_coordinate
    assert generator * quadratic == -4 * quadratic
    assert generator == generator.T

    # Sym_0(2) has basis x^2-y^2 and 2xy. The second basis function samples
    # to zero on the four cardinal points, while the first is restored at -4.
    sampling = sp.Matrix.hstack(quadratic, sp.zeros(4, 1))
    constraints = (generator + 4 * sp.eye(4)) * sampling
    assert sampling.rank() == 1
    assert constraints.rank() == 0
    assert 2 - constraints.rank() == 2          # dim E_form
    assert 2 - sampling.rank() == 1             # dim K_X
    assert sampling.rank() - constraints.rank() == 1  # dim E_sample

    # At (1,0), write rates to (0,1), (-1,0), (0,-1) as u,b,v.
    u, b, v = sp.symbols("u b v")
    solution = sp.solve(
        [
            sp.Eq(u + v + 2 * b, 1),
            sp.Eq(u - v, 0),
            sp.Eq(u + v, 2),
        ],
        [u, b, v],
        dict=True,
    )
    assert solution == [{u: 1, b: -half, v: 1}]


def spectral_product_resonance_search() -> list[tuple[int, int, int]]:
    # Scalar products of degree-l harmonics have only even harmonic degrees k.
    hits: list[tuple[int, int, int]] = []
    for dimension in range(2, 13):
        for degree in range(1, 13):
            eigenvalue = degree * (degree + dimension - 2)
            for product_degree in range(0, 2 * degree + 1, 2):
                if product_degree * (product_degree + dimension - 2) == 2 * eigenvalue:
                    hits.append((dimension, degree, product_degree))
    assert hits == [(4, 4, 6), (6, 8, 12), (8, 12, 18), (9, 5, 8)]
    return hits


def pell_resonance_family_dimension_four() -> list[tuple[int, int]]:
    # In d=4, the resonance equation becomes
    #   (k+1)^2 - 2(l+1)^2 = -1.
    # Multiplication by 3+2*sqrt(2) generates infinitely many solutions.
    x, y = 1, 1
    nontrivial: list[tuple[int, int]] = []
    for _ in range(4):
        x, y = 3 * x + 4 * y, 2 * x + 3 * y
        k = x - 1
        degree = y - 1
        assert k % 2 == 0
        assert k * (k + 2) == 2 * degree * (degree + 2)
        assert 0 <= k <= 2 * degree
        nontrivial.append((degree, k))
    assert nontrivial[:3] == [(4, 6), (28, 40), (168, 238)]
    return nontrivial


def main() -> None:
    print("Exact quadratic covariance and sampled-space audit")
    print(
        "Graph          rank(R) rank(S) dim(E_form) dim(K_X) dim(E_sample)"
    )
    for name, (raw, adjacent_dot) in platonic_data().items():
        result = audit_platonic(name, raw, adjacent_dot)
        print(
            f"{result.name:12s} {result.constraint_rank:7d} "
            f"{result.sampling_rank:7d} "
            f"{result.exact_form_dimension:11d} "
            f"{result.sampling_kernel_dimension:8d} "
            f"{result.exact_sample_dimension:13d}"
        )

    det_icosahedron, det_dodecahedron = exact_rank_certificates()
    print(f"icosahedron rank certificate determinant: {det_icosahedron}")
    print(f"dodecahedron rank certificate determinant: {det_dodecahedron}")

    factorization_rank_test()
    signed_square_restoration()
    print(
        "signed square restoration: PASS "
        "(rank S=1, rank R=0, sampled exact dimension=1)"
    )

    hits = spectral_product_resonance_search()
    pell_family = pell_resonance_family_dimension_four()
    print(f"bounded additive-resonance hits: {hits}")
    print(f"d=4 Pell resonance family prefix: {pell_family}")
    print("Exact quadratic covariance audit: PASS")


if __name__ == "__main__":
    main()
