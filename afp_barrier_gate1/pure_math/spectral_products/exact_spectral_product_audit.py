#!/usr/bin/env python3
"""Exact certificates for product resonance and sampled harmonic aliases."""

from itertools import product
from functools import lru_cache
import sympy as sp


def require(ok, label):
    if not ok:
        raise AssertionError(label)


@lru_cache(maxsize=None)
def harmonic_basis(deg):
    """Coefficient vectors of homogeneous harmonic polynomials in Q[x,y,z]."""
    mons = [(a, b, deg - a - b) for a in range(deg + 1)
            for b in range(deg + 1 - a)]
    if deg < 2:
        return mons, sp.eye(len(mons))
    low = [(a, b, deg - 2 - a - b) for a in range(deg - 1)
           for b in range(deg - 1 - a)]
    pos = {m: i for i, m in enumerate(low)}
    lap = sp.zeros(len(low), len(mons))
    for j, (a, b, c) in enumerate(mons):
        if a >= 2:
            lap[pos[(a - 2, b, c)], j] += a * (a - 1)
        if b >= 2:
            lap[pos[(a, b - 2, c)], j] += b * (b - 1)
        if c >= 2:
            lap[pos[(a, b, c - 2)], j] += c * (c - 1)
    null = lap.nullspace()
    require(len(null) == 2 * deg + 1, f"harmonic dimension H_{deg}")
    return mons, sp.Matrix.hstack(*null)


def evaluation(vertices, deg):
    mons, basis = harmonic_basis(deg)
    values = sp.Matrix([[x**a * y**b * z**c for a, b, c in mons]
                        for x, y, z in vertices])
    return values * basis


def platonic_vertices():
    phi = (1 + sp.sqrt(5)) / 2
    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    octa = [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
            (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    cube = list(product((1, -1), repeat=3))
    ico = []
    for s, t in product((1, -1), repeat=2):
        ico.extend([(0, s, t * phi), (s, t * phi, 0), (t * phi, 0, s)])
    dodeca = list(product((1, -1), repeat=3))
    inv = 1 / phi
    for s, t in product((1, -1), repeat=2):
        dodeca.extend([(0, s * inv, t * phi),
                       (s * inv, t * phi, 0),
                       (t * phi, 0, s * inv)])
    return {"tetrahedron": tetra, "octahedron": octa, "cube": cube,
            "icosahedron": ico, "dodecahedron": dodeca}


def antipodal_pairs(vertices):
    """Return exact antipodal pairs, or None when the set is not antipodal."""

    partners = {}
    for i, v in enumerate(vertices):
        matches = [j for j, w in enumerate(vertices)
                   if all(sp.simplify(v[k] + w[k]) == 0 for k in range(3))]
        if not matches:
            return None
        require(len(matches) == 1 and matches[0] != i, "unique antipodal partner")
        partners[i] = matches[0]
    pairs = tuple(sorted((min(i, j), max(i, j)) for i, j in partners.items()))
    pairs = tuple(dict.fromkeys(pairs))
    require(len(pairs) * 2 == len(vertices), "antipodal orbit count")
    return pairs


def polynomial_values(vertices, expr):
    x, y, z = sp.symbols("x y z")
    return sp.Matrix([
        sp.simplify(expr.subs({x: v[0], y: v[1], z: v[2]}))
        for v in vertices
    ])


def boolean_square_certificate():
    states = list(product((-1, 1), repeat=2))
    index = {x: i for i, x in enumerate(states)}
    L = sp.zeros(4)
    for i, x in enumerate(states):
        for k in range(2):
            y = list(x)
            y[k] *= -1
            L[i, index[tuple(y)]] = 1
        L[i, i] = -2
    require(L == L.T, "Boolean generator reversibility")
    require(L * sp.ones(4, 1) == sp.zeros(4, 1),
            "Boolean generator conservation")
    require(all(L[i, j] >= 0 for i in range(4) for j in range(4) if i != j),
            "Boolean generator positivity")
    seen = {0}
    pending = [0]
    while pending:
        i = pending.pop()
        for j in range(4):
            if L[i, j] > 0 and j not in seen:
                seen.add(j)
                pending.append(j)
    require(len(seen) == 4, "Boolean generator connectivity")
    f = sp.Matrix([x + y for x, y in states])
    q = sp.Matrix([v * v - 2 for v in f])
    gamma = []
    for i, x in enumerate(states):
        total = 0
        for k in range(2):
            y = list(x)
            y[k] *= -1
            total += (f[index[tuple(y)]] - f[i])**2 / 2
        gamma.append(total)
    require(L * f == -2 * f, "Boolean linear eigenfunction")
    require(q != sp.zeros(4, 1) and L * q == -4 * q,
            "nonzero Boolean doubled square")
    require(sum(q) == 0, "Boolean centered square has nonzero uniform mean")
    require(gamma == [4, 4, 4, 4], "Boolean constant Gamma")


def product_residual_symbolic():
    Lfg, fLg, gLf, gamma, mu, lam, nu, fg, c = sp.symbols(
        "Lfg fLg gLf gamma mu lam nu fg c")
    require(sp.expand((Lfg + mu * (fg - c)).subs({
        Lfg: fLg + gLf + 2 * gamma,
        fLg: -nu * fg,
        gLf: -lam * fg,
    }) - (2 * gamma + (mu - lam - nu) * fg - mu * c)) == 0,
            "arbitrary-target product residual")


def sampling_separation_regressions():
    """Reject distinct-degree scalar separation and test the corrected form.

    In ambient dimension d=1, lambda_l=l(l+d-2) gives lambda_0=lambda_1=0.
    A singleton sample aliases both degrees, so distinct *degrees* do not force
    a direct sum.  Separation is only between sampled sums belonging to
    distinct eigenvalue classes.
    """

    singleton = sp.ones(1, 1)
    L_singleton = sp.zeros(1)
    lambda_0 = 0 * (0 + 1 - 2)
    lambda_1 = 1 * (1 + 1 - 2)
    require(lambda_0 == lambda_1 == 0, "d=1 repeated spectral target")
    require(L_singleton * singleton == -lambda_0 * singleton and
            L_singleton * singleton == -lambda_1 * singleton,
            "d=1 singleton simultaneous exactness")
    require(sp.Matrix.hstack(singleton, singleton).rank() == 1,
            "d=1 degree-0/1 alias")
    require(singleton.rank() + singleton.rank() == 2,
            "negative regression did not count the two degree labels")

    # The corrected d=1 statement groups H_0 and H_1 into their one shared
    # eigenvalue class; it does not demand separation inside that class.
    class_zero_d1 = sp.Matrix.hstack(singleton, singleton).columnspace()
    require(len(class_zero_d1) == 1 and class_zero_d1[0] == singleton,
            "d=1 repeated-eigenvalue class grouping")

    # Positive nontrivial corrected example in d=2.  At the two antipodal
    # nodes (+/-1,0) on S^1, constants sample H_0 and (1,-1) samples the
    # coordinate harmonic in H_1.  Their eigenvalues 0 and 1 are distinct.
    constants = sp.Matrix((1, 1))
    degree_0 = constants
    degree_1 = sp.Matrix((1, -1))
    class_zero = degree_0
    class_one = degree_1
    class_basis = sp.Matrix.hstack(class_zero, class_one)
    require(class_basis.rank() == 2, "distinct eigenvalue classes do not separate")
    L = class_basis * sp.diag(0, -1) * class_basis.inv()
    require(L * constants == sp.zeros(2, 1), "corrected construction loses constants")
    require(L * degree_0 == sp.zeros(2, 1),
            "corrected construction loses the zero class")
    require(L * degree_1 == -degree_1,
            "corrected construction loses the distinct eigenvalue class")
    require(L * sp.ones(2, 1) == sp.zeros(2, 1),
            "corrected signed operator is not conservative")

    # Converse bookkeeping: when degree zero is already present, constants
    # are that same block and must not be appended a second time.
    degree_blocks = {0: degree_0, 1: degree_1}
    unique_converse = sp.Matrix.hstack(
        degree_blocks[0], *[block for degree, block in degree_blocks.items()
                            if degree != 0]
    )
    require(unique_converse.rank() == 2,
            "corrected converse unique block sum is not direct")
    naive_double_count = [constants, degree_blocks[0], degree_blocks[1]]
    require(sum(block.rank() for block in naive_double_count) == 3 and
            sp.Matrix.hstack(*naive_double_count).rank() == 2,
            "constant double-counting regression did not trigger")


def pell_certificate():
    # x+y*sqrt(2)=(1+sqrt(2))^(4m+1); m=0 is the constant case.
    x, y = 1, 1
    pairs = []
    for _ in range(4):
        require(x * x - 2 * y * y == -1 and x % 4 == 1 and y % 2 == 1,
                "parity-filtered negative Pell solution")
        pairs.append(((y - 1) // 2, (x - 1) // 2))
        x, y = 17 * x + 24 * y, 12 * x + 17 * y
    require(pairs[:3] == [(0, 0), (14, 20), (492, 696)],
            "first admissible harmonic resonances")
    for ell, J in pairs:
        require(J % 2 == 0 and J * (J + 1) == 2 * ell * (ell + 1),
                "harmonic doubled resonance")

    # Multiplication by (1+sqrt(2))^4=17+12sqrt(2) preserves the Pell norm
    # and the required residue class.  These symbolic identities certify the
    # infinite recurrence rather than only the displayed numerical prefix.
    px, py = sp.symbols("px py", integer=True)
    nx, ny = 17 * px + 24 * py, 12 * px + 17 * py
    require(sp.expand(nx**2 - 2 * ny**2 - (px**2 - 2 * py**2)) == 0,
            "Pell recurrence does not preserve the norm")
    require(sp.expand(nx - px) == 4 * (4 * px + 6 * py) and
            sp.expand(ny - py) == 4 * (3 * px + 4 * py),
            "Pell recurrence does not preserve parity classes")
    ell, J = sp.symbols("ell J", integer=True)
    require(sp.expand((ny.subs({px: 2 * J + 1, py: 2 * ell + 1}) - 1) / 2)
            == 17 * ell + 12 * J + 14,
            "ell recurrence changed")
    require(sp.expand((nx.subs({px: 2 * J + 1, py: 2 * ell + 1}) - 1) / 2)
            == 24 * ell + 17 * J + 20,
            "J recurrence changed")
    require(7**2 - 2 * 5**2 == -1 and 7 % 4 == 3,
            "excluded adjacent Pell parity class")


def hierarchy_and_alias_certificates():
    expected_component = {
        "tetrahedron": [1, 3, 4, 4, 4, 4, 4],
        "octahedron": [1, 2, 3, 3, 3, 3, 3],
        "cube": [1, 3, 4, 4, 4, 4, 4],
        "icosahedron": [1, 5, 5, 6, 5, 6, 6],
        "dodecahedron": [1, 5, 9, 10, 9, 10, 10],
    }
    expected_aggregate = {
        "tetrahedron": [1, 4, 4, 4, 4, 4, 4],
        "octahedron": [1, 3, 3, 3, 3, 3, 3],
        "cube": [1, 4, 4, 4, 4, 4, 4],
        "icosahedron": [1, 6, 6, 6, 6, 6, 6],
        "dodecahedron": [1, 6, 10, 10, 10, 10, 10],
    }
    expected_pair_rank_24 = {
        "tetrahedron": 4,
        "octahedron": 3,
        "cube": 4,
        "icosahedron": 5,
        "dodecahedron": 9,
    }
    antipodal_names = {"octahedron", "cube", "icosahedron", "dodecahedron"}
    evals = {}
    for name, vertices in platonic_vertices().items():
        require(len({tuple(v) for v in vertices}) == len(vertices),
                f"{name} vertices are distinct")
        radii = [sp.simplify(sum(q * q for q in v)) for v in vertices]
        require(all(sp.simplify(radius - radii[0]) == 0 for radius in radii),
                f"{name} raw vertices do not have a common radius")
        require(bool(radii[0] > 0), f"{name} common radius is not positive")

        blocks = [evaluation(vertices, J) for J in range(0, 13, 2)]
        evals[name] = blocks
        ranks = [B.rank() for B in blocks]
        agg = [sp.Matrix.hstack(*blocks[:k + 1]).rank() for k in range(7)]
        require(ranks == expected_component[name], f"{name} exact H_J ranks")
        require(agg == expected_aggregate[name], f"{name} aggregate alias ranks")
        # A simultaneous signed hierarchy needs distinct sampled eigenspaces
        # to be an internal direct sum; rank additivity is the exact test.
        require(sum(ranks[:3]) > agg[2], f"{name} l=2 alias obstruction")

        pair_rank = sp.Matrix.hstack(blocks[1], blocks[2]).rank()
        require(pair_rank == expected_pair_rank_24[name],
                f"{name} exact H_2/H_4 pair rank")
        require(pair_rank == ranks[2], f"{name} im H_2 is not contained in im H_4")
        if name == "icosahedron":
            require(pair_rank == ranks[1], "icosahedron im H_4 != im H_2")

        pairs = antipodal_pairs(vertices)
        require((pairs is not None) == (name in antipodal_names),
                f"{name} antipodal classification")
        if pairs is not None:
            representatives = [i for i, _ in pairs]
            for degree_index, block in enumerate(blocks):
                for i, j in pairs:
                    require(all(sp.simplify(block[i, c] - block[j, c]) == 0
                                for c in range(block.cols)),
                            f"{name} H_{2 * degree_index} antipodal row equality")
                compressed = block.extract(representatives, range(block.cols))
                require(compressed.rank() == ranks[degree_index],
                        f"{name} H_{2 * degree_index} antipodal compression rank")
            compressed_aggregates = [
                sp.Matrix.hstack(*blocks[:k + 1]).extract(
                    representatives,
                    range(sum(block.cols for block in blocks[:k + 1])),
                ).rank()
                for k in range(7)
            ]
            require(compressed_aggregates == agg,
                    f"{name} aggregate antipodal compression ranks")
            require(all(rank <= len(pairs) for rank in agg),
                    f"{name} antipodal orbit rank bound")

    # Explicit nonzero H_2/H_4 aliases.  The pair-rank checks above prove the
    # full inclusions; these harmonic polynomial witnesses make them concrete.
    x, y, z = sp.symbols("x y z")
    phi = (1 + sp.sqrt(5)) / 2
    P = sp.expand(x * y * (x**2 + y**2 - 6 * z**2))
    Q = sp.expand(x * y * (x**2 - y**2))
    D = sp.expand((x**2 - y**2) * (x**2 + y**2 - 6 * z**2))
    laplacian = lambda expr: sp.expand(sum(sp.diff(expr, v, 2) for v in (x, y, z)))
    require(laplacian(P) == 0 and laplacian(Q) == 0 and laplacian(D) == 0,
            "advertised H_4 alias polynomial is not harmonic")
    vertices_by_name = platonic_vertices()
    for name in ("tetrahedron", "cube"):
        vertices = vertices_by_name[name]
        require(polynomial_values(vertices, -P / 4) ==
                polynomial_values(vertices, x * y),
                f"{name} explicit H_4/H_2 alias")
    octa = vertices_by_name["octahedron"]
    require(polynomial_values(octa, D) == polynomial_values(octa, x**2 - y**2),
            "octahedron explicit H_4/H_2 alias")
    ico = vertices_by_name["icosahedron"]
    require(polynomial_values(ico, P / (phi + 2)) ==
            polynomial_values(ico, x * y),
            "icosahedron explicit H_4/H_2 alias")
    dodeca = vertices_by_name["dodecahedron"]
    dodeca_alias = -P / 4 - sp.Rational(7, 4) * Q / sp.sqrt(5)
    require(polynomial_values(dodeca, dodeca_alias) ==
            polynomial_values(dodeca, x * y),
            "dodecahedron explicit H_4/H_2 alias")

    # Sym^2(H_l)=H_0+H_2+...+H_{2l}; l=1..6 has no doubled component.
    table = []
    for ell in range(1, 7):
        components = list(range(0, 2 * ell + 1, 2))
        eigenvalues = [J * (J + 1) for J in components]
        target = 2 * ell * (ell + 1)
        require(target not in eigenvalues, f"no l={ell} doubled component")
        require(sum(2 * J + 1 for J in components) == (ell + 1) * (2 * ell + 1),
                f"Sym^2 dimension l={ell}")
        table.append((ell, components, eigenvalues, target))
    return table


def main():
    product_residual_symbolic()
    boolean_square_certificate()
    sampling_separation_regressions()
    pell_certificate()
    table = hierarchy_and_alias_certificates()
    print("PASS exact spectral product residual and Boolean-square counterexample")
    print("PASS REJECTED literal distinct-degree theorem in d=1; "
          "corrected distinct-eigenvalue-class and converse bookkeeping")
    print("PASS parity-filtered Pell hierarchy: first nonconstant (l,J)=(14,20)")
    for ell, components, eigenvalues, target in table:
        print(f"PASS l={ell}: J={components}, eigen={eigenvalues}, doubled={target}")
    print("PASS exact Platonic harmonic ranks, aliases, and hierarchy separation")


if __name__ == "__main__":
    main()
