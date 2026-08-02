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


def pell_certificate():
    # x+y*sqrt(2)=(1+sqrt(2))^(4m+1); m=0 is the constant case.
    x, y = 1, 1
    pairs = []
    for _ in range(4):
        require(x * x - 2 * y * y == -1 and x % 4 == 1,
                "parity-filtered negative Pell solution")
        pairs.append(((y - 1) // 2, (x - 1) // 2))
        x, y = 17 * x + 24 * y, 12 * x + 17 * y
    require(pairs[:3] == [(0, 0), (14, 20), (492, 696)],
            "first admissible harmonic resonances")
    for ell, J in pairs:
        require(J % 2 == 0 and J * (J + 1) == 2 * ell * (ell + 1),
                "harmonic doubled resonance")


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
    evals = {}
    for name, vertices in platonic_vertices().items():
        blocks = [evaluation(vertices, J) for J in range(0, 13, 2)]
        evals[name] = blocks
        ranks = [B.rank() for B in blocks]
        agg = [sp.Matrix.hstack(*blocks[:k + 1]).rank() for k in range(7)]
        require(ranks == expected_component[name], f"{name} exact H_J ranks")
        require(agg == expected_aggregate[name], f"{name} aggregate alias ranks")
        # A simultaneous signed hierarchy needs distinct sampled eigenspaces
        # to be an internal direct sum; rank additivity is the exact test.
        require(sum(ranks[:3]) > agg[2], f"{name} l=2 alias obstruction")

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
    pell_certificate()
    table = hierarchy_and_alias_certificates()
    print("PASS exact spectral product residual and Boolean-square counterexample")
    print("PASS parity-filtered Pell hierarchy: first nonconstant (l,J)=(14,20)")
    for ell, components, eigenvalues, target in table:
        print(f"PASS l={ell}: J={components}, eigen={eigenvalues}, doubled={target}")
    print("PASS exact Platonic harmonic ranks, aliases, and hierarchy separation")


if __name__ == "__main__":
    main()
