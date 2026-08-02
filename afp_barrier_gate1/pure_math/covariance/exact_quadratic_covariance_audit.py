#!/usr/bin/env python3
"""Exact certificates for quadratic covariance and sampled exactness.

All computations use SymPy exact arithmetic (including ``Q(sqrt(5))`` for
the icosahedron and dodecahedron).  In particular, no numerical rank or
tolerance-dependent null-space computation occurs in this audit.

Column convention for both S and R, in this order, is

    x^2-y^2, 2z^2-x^2-y^2, xy, xz, yz.

Thus S has one row per vertex and one column per trace-free form, and
R = (L + 6 I) S for the S^2 coordinate eigenmap convention L X = -2 X.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


Q = sp.Rational
SQRT3 = sp.sqrt(3)
SQRT5 = sp.sqrt(5)
PHI = (1 + SQRT5) / 2


def zmat(rows: int, cols: int) -> sp.Matrix:
    return sp.zeros(rows, cols)


def assert_zero(value: sp.Expr | sp.Matrix, message: str) -> None:
    if isinstance(value, sp.MatrixBase):
        ok = value.applyfunc(sp.simplify) == sp.zeros(*value.shape)
    else:
        ok = sp.simplify(value) == 0
    if not ok:
        raise AssertionError(message)


def tracefree_basis() -> tuple[sp.Matrix, ...]:
    half = Q(1, 2)
    return (
        sp.diag(1, -1, 0),
        sp.diag(-1, -1, 2),
        sp.Matrix(((0, half, 0), (half, 0, 0), (0, 0, 0))),
        sp.Matrix(((0, 0, half), (0, 0, 0), (half, 0, 0))),
        sp.Matrix(((0, 0, 0), (0, 0, half), (0, half, 0))),
    )


BASIS = tracefree_basis()


def samples(vertices: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix(
        [[sp.expand((x.T * a * x)[0]) for a in BASIS] for x in vertices]
    )


def vertex_matrix(vertices: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix([[x[k] for k in range(3)] for x in vertices])


def generator_from_shell(
    vertices: tuple[sp.Matrix, ...], alpha: sp.Expr, degree: int, rate: sp.Expr
) -> tuple[sp.Matrix, tuple[tuple[int, ...], ...]]:
    n = len(vertices)
    neighbors: list[tuple[int, ...]] = []
    for i, x in enumerate(vertices):
        row = tuple(
            j
            for j, y in enumerate(vertices)
            if i != j and sp.simplify((x.T * y)[0] - alpha) == 0
        )
        if len(row) != degree:
            raise AssertionError(f"shell degree {len(row)} != {degree} at row {i}")
        neighbors.append(row)
    L = sp.zeros(n)
    for i, row in enumerate(neighbors):
        for j in row:
            L[i, j] = rate
        L[i, i] = -degree * rate
    if L != L.T:
        raise AssertionError("shortest-edge relation is not symmetric")
    if L * sp.ones(n, 1) != sp.zeros(n, 1):
        raise AssertionError("generator does not conserve constants")
    return L, tuple(neighbors)


def tetrahedron() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(v) / SQRT3
        for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    )


def octahedron() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(v)
        for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                  (0, 0, 1), (0, 0, -1))
    )


def cube() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix((x, y, z)) / SQRT3
        for x in (-1, 1)
        for y in (-1, 1)
        for z in (-1, 1)
    )


def icosahedron() -> tuple[sp.Matrix, ...]:
    raw = (
        (0, 1, PHI), (0, -1, PHI), (0, 1, -PHI), (0, -1, -PHI),
        (1, PHI, 0), (-1, PHI, 0), (1, -PHI, 0), (-1, -PHI, 0),
        (PHI, 0, 1), (-PHI, 0, 1), (PHI, 0, -1), (-PHI, 0, -1),
    )
    radius = sp.sqrt(PHI + 2)
    return tuple(sp.Matrix(v) / radius for v in raw)


def dodecahedron() -> tuple[sp.Matrix, ...]:
    raw: list[tuple[sp.Expr, sp.Expr, sp.Expr]] = [
        (x, y, z)
        for x in (-1, 1)
        for y in (-1, 1)
        for z in (-1, 1)
    ]
    inv = 1 / PHI
    for a in (-1, 1):
        for b in (-1, 1):
            raw.extend(((0, a * inv, b * PHI),
                        (a * inv, b * PHI, 0),
                        (a * PHI, 0, b * inv)))
    return tuple(sp.Matrix(v) / SQRT3 for v in raw)


@dataclass(frozen=True)
class PlatonicSpec:
    name: str
    vertices: tuple[sp.Matrix, ...]
    alpha: sp.Expr
    degree: int
    rate: sp.Expr
    expected_rank: int
    minor_rows: tuple[int, ...]
    minor_cols: tuple[int, ...]
    expected_minor: sp.Expr
    kernel_indices: tuple[int, ...]


SPECS = (
    PlatonicSpec("tetrahedron", tetrahedron(), -Q(1, 3), 3, Q(1, 2), 3,
                 (0, 1, 2), (2, 3, 4), -Q(4, 27), (0, 1)),
    PlatonicSpec("octahedron", octahedron(), 0, 4, Q(1, 2), 2,
                 (0, 2), (0, 1), -2, (2, 3, 4)),
    PlatonicSpec("cube", cube(), Q(1, 3), 3, 1, 3,
                 (0, 1, 2), (2, 3, 4), Q(4, 27), (0, 1)),
    PlatonicSpec("icosahedron", icosahedron(), SQRT5 / 5, 5,
                 (5 + SQRT5) / 10, 5, (0, 1, 4, 5, 8), tuple(range(5)),
                 -16 * SQRT5 / 125, ()),
    PlatonicSpec("dodecahedron", dodecahedron(), SQRT5 / 3, 3,
                 (3 + SQRT5) / 2, 5, (0, 1, 2, 8, 9), tuple(range(5)),
                 Q(16, 81), ()),
)


@dataclass(frozen=True)
class PlatonicResult:
    name: str
    vertices: int
    rank_s: int
    rank_r: int
    dim_form: int
    dim_kernel: int
    dim_sample: int
    minor: sp.Expr
    action_scalar: sp.Expr


def covariance_row(
    vertices: tuple[sp.Matrix, ...], neighbors: tuple[tuple[int, ...], ...],
    rate: sp.Expr, i: int,
) -> sp.Matrix:
    x = vertices[i]
    C = sp.zeros(3)
    for j in neighbors[i]:
        delta = vertices[j] - x
        C += rate * delta * delta.T
    return C.applyfunc(sp.simplify)


def audit_platonic(spec: PlatonicSpec) -> PlatonicResult:
    n = len(spec.vertices)
    for x in spec.vertices:
        assert_zero((x.T * x)[0] - 1, f"{spec.name}: vertex is not unit")

    L, neighbors = generator_from_shell(
        spec.vertices, spec.alpha, spec.degree, spec.rate
    )
    X = vertex_matrix(spec.vertices)
    assert_zero(L * X + 2 * X, f"{spec.name}: coordinate eigenmap failed")
    S = samples(spec.vertices)
    R_direct = (L + 6 * sp.eye(n)) * S

    R_cov_rows: list[list[sp.Expr]] = []
    kappa = 3 * (1 - spec.alpha)
    action_scalar = -3 * (1 + spec.alpha)
    total_rate = spec.degree * spec.rate
    assert_zero(total_rate - 2 / (1 - spec.alpha),
                f"{spec.name}: one-shell rate identity failed")

    for i, x in enumerate(spec.vertices):
        C = covariance_row(spec.vertices, neighbors, spec.rate, i)
        # Exact one-shell tangent-isotropy hypothesis.
        # Clear the positive denominator 1-alpha^2.  This keeps the golden
        # ratio cases in Q(sqrt(5)) instead of introducing nested radicals.
        tangent_numerator = sp.zeros(3)
        for j in neighbors[i]:
            tangent = spec.vertices[j] - spec.alpha * x
            tangent_numerator += spec.rate * tangent * tangent.T
        expected_tangent_numerator = (
            (1 - spec.alpha**2) * total_rate / 2
            * (sp.eye(3) - x * x.T)
        )
        assert_zero(tangent_numerator - expected_tangent_numerator,
                    f"{spec.name}: tangent isotropy failed at {i}")

        # The constructive one-shell rigidity formulas in dimension three.
        expected_C = ((1 + spec.alpha) * (sp.eye(3) - x * x.T)
                      + 2 * (1 - spec.alpha) * x * x.T)
        assert_zero(C - expected_C, f"{spec.name}: C formula failed at {i}")
        assert_zero(sp.trace(C) - 4, f"{spec.name}: tr C != 4")
        if sp.simplify((x.T * C * x)[0] - 2 * (1 - spec.alpha)) != 0:
            raise AssertionError(f"{spec.name}: radial covariance formula failed")
        if not bool(sp.simplify((x.T * C * x)[0]) > 0):
            raise AssertionError(f"{spec.name}: radial covariance is not positive")

        M = (C + 2 * x * x.T - 2 * sp.eye(3)).applyfunc(sp.simplify)
        expected_M = kappa * (x * x.T - sp.eye(3) / 3)
        assert_zero(M - expected_M, f"{spec.name}: M formula failed at {i}")
        R_cov_rows.append([sp.expand(sp.trace(a * M)) for a in BASIS])

    R_cov = sp.Matrix(R_cov_rows)
    assert_zero(R_direct - R_cov, f"{spec.name}: covariance factorization failed")
    assert_zero(R_direct - kappa * S, f"{spec.name}: R = kappa S failed")
    assert_zero(L * S - action_scalar * S,
                f"{spec.name}: action on im S failed")

    rank_s = S.rank(iszerofunc=lambda e: sp.simplify(e) == 0)
    rank_r = R_direct.rank(iszerofunc=lambda e: sp.simplify(e) == 0)
    if rank_s != spec.expected_rank or rank_r != spec.expected_rank:
        raise AssertionError(
            f"{spec.name}: exact ranks {(rank_s, rank_r)} != {spec.expected_rank}"
        )
    minor = sp.simplify(S.extract(spec.minor_rows, spec.minor_cols).det())
    assert_zero(minor - spec.expected_minor, f"{spec.name}: exact minor changed")
    if minor == 0:
        raise AssertionError(f"{spec.name}: rank minor vanished")

    standard_kernel = tuple(sp.eye(5).col(i) for i in spec.kernel_indices)
    computed_kernel = S.nullspace(iszerofunc=lambda e: sp.simplify(e) == 0)
    if len(computed_kernel) != len(standard_kernel):
        raise AssertionError(f"{spec.name}: wrong sampling-kernel dimension")
    for v in standard_kernel:
        if v == sp.zeros(5, 1):
            raise AssertionError("negative test: kernel certificate is zero")
        assert_zero(S * v, f"{spec.name}: advertised sampling alias is not zero")
        # K_X subset E_form is checked rather than inferred silently.
        assert_zero(R_direct * v, f"{spec.name}: K_X is not contained in E_form")
    if standard_kernel and sp.Matrix.hstack(*computed_kernel).columnspace() != \
            sp.Matrix.hstack(*standard_kernel).columnspace():
        raise AssertionError(f"{spec.name}: exact sampling-kernel basis changed")

    dim_form = 5 - rank_r
    dim_kernel = 5 - rank_s
    dim_sample = rank_s - rank_r
    if dim_sample != dim_form - dim_kernel:
        raise AssertionError(f"{spec.name}: kernel subtraction is incorrect")
    if dim_sample != 0 or dim_form != dim_kernel:
        raise AssertionError(f"{spec.name}: expected E_form = K_X and E_sample=0")
    # Permanent negative assertion: for the first three solids a nonzero form
    # in E_form is not a nonzero sampled mode.
    if standard_kernel and dim_form == dim_sample:
        raise AssertionError("negative test: algebraic forms were counted as samples")

    return PlatonicResult(spec.name, n, rank_s, rank_r, dim_form,
                          dim_kernel, dim_sample, minor, action_scalar)


def hexagonal_prism_counterexample() -> tuple[int, int, int]:
    """A full-dimensional positive common-shell example needing isotropy.

    The twelve nodes are two regular hexagons at heights +/-1/sqrt(5), with
    equatorial radius 2/sqrt(5).  Ring jumps have rate 2 and vertical jumps
    rate 1.  Every active dot product is 3/5 and L X = -2 X, but the tangent
    second moment is not isotropic.  Two genuine sampled H_2 modes survive.
    """

    trig = ((1, 0), (Q(1, 2), SQRT3 / 2), (-Q(1, 2), SQRT3 / 2),
            (-1, 0), (-Q(1, 2), -SQRT3 / 2), (Q(1, 2), -SQRT3 / 2))
    vertices = tuple(
        sp.Matrix((2 * c / SQRT5, 2 * s / SQRT5, sign / SQRT5))
        for sign in (-1, 1) for c, s in trig
    )
    n = len(vertices)
    L = sp.zeros(n)
    active: list[list[tuple[int, sp.Expr]]] = [[] for _ in range(n)]
    for layer in range(2):
        for k in range(6):
            i = 6 * layer + k
            for j in (6 * layer + (k - 1) % 6, 6 * layer + (k + 1) % 6):
                L[i, j] = 2
                active[i].append((j, sp.Integer(2)))
            vertical = 6 * (1 - layer) + k
            L[i, vertical] = 1
            active[i].append((vertical, sp.Integer(1)))
            L[i, i] = -5
    if L != L.T or L * sp.ones(n, 1) != sp.zeros(n, 1):
        raise AssertionError("prism is not a reversible conservative generator")
    X = vertex_matrix(vertices)
    if X.rank() != 3:
        raise AssertionError("prism embedding is not full-dimensional")
    assert_zero(L * X + 2 * X, "prism coordinate eigenmap failed")
    for i, x in enumerate(vertices):
        for j, rate in active[i]:
            if rate <= 0:
                raise AssertionError("prism is not positive")
            assert_zero((x.T * vertices[j])[0] - Q(3, 5),
                        "prism active edge left the common shell")

    # Explicitly disprove tangent isotropy at a row.
    i = 0
    x = vertices[i]
    alpha = Q(3, 5)
    T = sp.zeros(3)
    for j, rate in active[i]:
        u = (vertices[j] - alpha * x) / Q(4, 5)
        T += rate * u * u.T
    isotropic = Q(5, 2) * (sp.eye(3) - x * x.T)  # total rate 5, dim U=2
    if (T - isotropic).applyfunc(sp.simplify) == sp.zeros(3):
        raise AssertionError("negative test: anisotropic prism passed isotropy")

    S = samples(vertices)
    R = (L + 6 * sp.eye(n)) * S
    rank_s = S.rank()
    rank_r = R.rank()
    dim_sample = rank_s - rank_r
    if (rank_s, rank_r, dim_sample) != (5, 3, 2):
        raise AssertionError("prism sharpness dimensions changed")
    # x^2-y^2 and xy are exact, genuine, and linearly independent samples.
    for col in (0, 2):
        if S.col(col) == sp.zeros(n, 1):
            raise AssertionError("prism restored mode is a sampling alias")
        assert_zero(L * S.col(col) + 6 * S.col(col),
                    "prism quadratic mode is not exact")
    if sp.Matrix.hstack(S.col(0), S.col(2)).rank() != 2:
        raise AssertionError("prism modes are not independent")
    return rank_s, rank_r, dim_sample


def main() -> None:
    print("Exact quadratic covariance audit (SymPy exact arithmetic)")
    for spec in SPECS:
        result = audit_platonic(spec)
        print(
            f"{result.name:12s} n={result.vertices:2d} "
            f"rankS={result.rank_s} rankR={result.rank_r} "
            f"dimEform={result.dim_form} dimK={result.dim_kernel} "
            f"dimEsample={result.dim_sample} minor={result.minor} "
            f"L|imS={result.action_scalar}"
        )
    rank_s, rank_r, dim_sample = hexagonal_prism_counterexample()
    print(
        "hex-prism sharpness: full-span, positive, common-shell, anisotropic; "
        f"rankS={rank_s} rankR={rank_r} dimEsample={dim_sample}"
    )
    print("Exact quadratic covariance audit: PASS")


if __name__ == "__main__":
    main()
