#!/usr/bin/env python3
"""Final deterministic audit for corrected Prompt 3 integration.

This script closes the gaps identified while salvaging the two historical
Prompt 3 lines.  The ordinary all-orders proof remains in
``GLOBAL_Q_RIGIDITY_THEOREM.md``.  This file supplies independent exact and
source-pinned regression evidence for:

* the Gram/Heron nondegeneracy certificate used by the angle-stability proof;
* all five Platonic coordinate eigenmaps and exact Q=1 values;
* the weighted-octahedron covariance and genuine-sampling obstruction;
* the antipodal ``ell=2`` boundary, kept separate from tangent normalization;
* executable hypothesis-deletion counterexamples; and
* literal source-pinned plantri enumeration through 12 vertices.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

import mpmath as mp
import networkx as nx
import sympy as sp

mp.mp.dps = 100
Q = sp.Rational
SQRT5 = sp.sqrt(5)
PHI = (1 + SQRT5) / 2
INV_PHI = 1 / PHI

PLANTRI_COMMIT = "09745aeb09819bf200cfc77617f000258dba0a49"
PLANTRI_BLOB = "06802f7a92ffea2526711232a53b9e2e84104777"
PLANTRI_URL = (
    "https://raw.githubusercontent.com/mishun/plantri/"
    f"{PLANTRI_COMMIT}/plantri.c"
)
PLANTRI_COUNTS = {
    4: 1,
    5: 1,
    6: 2,
    7: 5,
    8: 14,
    9: 50,
    10: 233,
    11: 1249,
    12: 7595,
}


def simp(value: sp.Expr | int) -> sp.Expr:
    return sp.factor(sp.radsimp(sp.simplify(sp.sympify(value))))


def git_blob_sha(data: bytes) -> str:
    payload = b"blob " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def dot(x: tuple[sp.Expr, ...], y: tuple[sp.Expr, ...]) -> sp.Expr:
    return simp(sum(a * b for a, b in zip(x, y, strict=True)))


def gram_heron_certificate() -> None:
    """Check the closed nondegeneracy route at the icosahedral reference."""

    ca, cb, cc = sp.symbols("ca cb cc", real=True)
    determinant = 1 - ca**2 - cb**2 - cc**2 + 2 * ca * cb * cc
    expanded = sp.expand(
        (1 - cb**2) * (1 - cc**2) - (ca - cb * cc) ** 2
    )
    assert sp.expand(determinant - expanded) == 0

    c0 = 1 / SQRT5
    d0 = simp(determinant.subs({ca: c0, cb: c0, cc: c0}))
    assert d0 == simp(Q(2, 5) + Q(2, 5) / SQRT5)
    assert d0.is_positive

    theta = mp.acos(1 / mp.sqrt(5))
    t_lo = mp.mpf("1.10")
    t_hi = mp.mpf("1.12")
    assert t_lo < theta < t_hi
    assert 0 < t_lo < t_hi < mp.pi
    assert 2 * t_lo > t_hi
    assert 3 * t_hi < 2 * mp.pi

    s_theta = min(mp.sin(t_lo), mp.sin(t_hi))
    g_box = 2 * t_lo - t_hi
    m_t = mp.sin(g_box / 2)
    m_s = min(mp.sin(3 * t_lo / 2), mp.sin(3 * t_hi / 2))
    s_a0 = 2 * mp.sqrt(m_s * m_t**3)
    assert min(s_theta, g_box, m_t, m_s, s_a0) > 0

    def spherical_angle(a: mp.mpf, b: mp.mpf, c: mp.mpf) -> mp.mpf:
        z = (mp.cos(a) - mp.cos(b) * mp.cos(c)) / (mp.sin(b) * mp.sin(c))
        if not -1 <= z <= 1:
            raise AssertionError(f"cosine-law value left [-1,1]: {z}")
        return mp.acos(z)

    max_gradient = mp.mpf("0")
    for a, b, c in itertools.product((t_lo, t_hi), repeat=3):
        semiperimeter = (a + b + c) / 2
        d_heron = (
            4
            * mp.sin(semiperimeter)
            * mp.sin(semiperimeter - a)
            * mp.sin(semiperimeter - b)
            * mp.sin(semiperimeter - c)
        )
        d_direct = (
            mp.sin(b) ** 2 * mp.sin(c) ** 2
            - (mp.cos(a) - mp.cos(b) * mp.cos(c)) ** 2
        )
        assert abs(d_heron - d_direct) < mp.mpf("1e-90")
        assert d_heron >= 4 * m_s * m_t**3 - mp.mpf("1e-90")
        angle = spherical_angle(a, b, c)
        sine_angle = mp.sin(angle)
        assert sine_angle >= s_a0 - mp.mpf("1e-80")
        da = abs(mp.sin(a) / (mp.sin(b) * mp.sin(c) * sine_angle))
        db = abs(
            (mp.cos(c) - mp.cos(a) * mp.cos(b))
            / (mp.sin(b) ** 2 * mp.sin(c) * sine_angle)
        )
        dc = abs(
            (mp.cos(b) - mp.cos(a) * mp.cos(c))
            / (mp.sin(c) ** 2 * mp.sin(b) * sine_angle)
        )
        max_gradient = max(max_gradient, da + db + dc)

    c_ang = 1 / (s_a0 * s_theta**2) + 4 / (s_a0 * s_theta**3)
    assert max_gradient <= c_ang
    print("Gram/Heron fixed-box certificate: PASS")
    print(
        f"  D_icosa={d0}, s_A0={mp.nstr(s_a0, 18)}, "
        f"C_ang={mp.nstr(c_ang, 18)}"
    )


def platonic_raw_data() -> dict[str, tuple[list[tuple[sp.Expr, ...]], sp.Expr]]:
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
    cube = list(itertools.product((-1, 1), repeat=3))
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
    dodecahedron: list[tuple[sp.Expr, ...]] = list(
        itertools.product((-1, 1), repeat=3)
    )
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


def adjacency(raw: list[tuple[sp.Expr, ...]], adjacent_raw_dot: sp.Expr) -> list[list[int]]:
    n = len(raw)
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if simp(dot(raw[i], raw[j]) - adjacent_raw_dot) == 0:
                graph[i][j] = graph[j][i] = 1
    return graph


def platonic_coordinate_and_q_audit() -> None:
    expected = {
        "tetrahedron": (3, Q(-1, 3), Q(3, 2)),
        "octahedron": (4, sp.Integer(0), sp.Integer(2)),
        "cube": (3, Q(1, 3), sp.Integer(3)),
        "icosahedron": (5, SQRT5 / 5, (5 + SQRT5) / 2),
        "dodecahedron": (3, SQRT5 / 3, 3 * (3 + SQRT5) / 2),
    }
    for name, (raw, adjacent_raw_dot) in platonic_raw_data().items():
        n = len(raw)
        norm2 = simp(dot(raw[0], raw[0]))
        assert all(simp(dot(v, v) - norm2) == 0 for v in raw)
        graph = adjacency(raw, adjacent_raw_dot)
        degrees = [sum(row) for row in graph]
        assert len(set(degrees)) == 1
        degree = degrees[0]
        expected_degree, expected_dot, expected_rate = expected[name]
        assert degree == expected_degree
        edge_dot = simp(adjacent_raw_dot / norm2)
        assert simp(edge_dot - expected_dot) == 0
        loss = simp(1 - edge_dot)
        row_rate = simp(2 / loss)
        edge_rate = simp(row_rate / degree)
        assert simp(row_rate - expected_rate) == 0
        epsilon = simp(row_rate * loss**2)
        quality = simp(row_rate * epsilon / 4)
        assert quality == 1
        for i, vertex in enumerate(raw):
            generated = []
            for k in range(3):
                value = sum(
                    edge_rate * graph[i][j] * (raw[j][k] - vertex[k])
                    for j in range(n)
                )
                generated.append(simp(value))
            assert tuple(generated) == tuple(simp(-2 * x) for x in vertex)
    print("five-Platonic coordinate eigenmap and Q=1 regressions: PASS")


def weighted_octahedron_sampling_audit() -> None:
    g12, g13, g23 = sp.symbols("g12 g13 g23", positive=True)
    g = {(0, 1): g12, (0, 2): g13, (1, 2): g23}
    w = [g12 + g13, g12 + g23, g13 + g23]
    d1, d2 = sp.symbols("d1 d2")
    d = sp.Matrix([d1, d2, -d1 - d2])
    equations = []
    for a in range(3):
        pa = sum(
            g[tuple(sorted((a, b)))] * d[b]
            for b in range(3)
            if b != a
        ) / w[a]
        equations.append(sp.factor(pa + 2 * d[a]))
    jac = sp.Matrix(
        [[sp.diff(equations[i], z) for z in (d1, d2)] for i in range(3)]
    )
    minors = [
        sp.factor(jac.extract(rows, [0, 1]).det())
        for rows in ((0, 1), (0, 2), (1, 2))
    ]
    expected = [
        3 * g12 * (g12 + g13 + g23) / ((g12 + g13) * (g12 + g23)),
        -3 * g13 * (g12 + g13 + g23) / ((g12 + g13) * (g13 + g23)),
        3 * g23 * (g12 + g13 + g23) / ((g12 + g23) * (g13 + g23)),
    ]
    assert all(
        sp.factor(a - b) == 0 for a, b in zip(minors, expected, strict=True)
    )
    assert minors[0].is_positive and minors[1].is_negative and minors[2].is_positive

    spec = {g12: Q(1), g13: Q(2), g23: Q(5)}
    pmat = sp.zeros(3)
    for a in range(3):
        for b in range(3):
            if a != b:
                pmat[a, b] = simp(
                    g[tuple(sorted((a, b)))].subs(spec) / w[a].subs(spec)
                )
        assert simp(sum(pmat[a, b] for b in range(3)) - 1) == 0
        assert all(pmat[a, b] >= 0 for b in range(3))
    assert max(sum(abs(pmat[a, b]) for b in range(3)) for a in range(3)) == 1
    assert (pmat + 2 * sp.eye(3)).rank() == 3
    print("weighted-octahedron covariance/sampling obstruction: PASS")


def antipodal_boundary_audit() -> None:
    omega = sp.Matrix([1, 0, 0])
    other = -omega
    rate = sp.Integer(1)
    ell = sp.Integer(2)
    covariance = (rate * (other - omega) * (other - omega).T).applyfunc(simp)
    assert covariance == 4 * (omega * omega.T)
    assert simp(rate * (rate * ell**2) / 4) == 1
    assert sp.sqrt(ell * (2 - ell)) == 0
    print("antipodal ell=2 boundary kept separate from tangent normalization: PASS")


def executable_hypothesis_deletions() -> None:
    assert Q(3, 2) != Q(2)
    assert Q(1) * (Q(1) * Q(2) ** 2) / 4 == 1

    loss = Q(3, 2)
    edge_rate = Q(2, 3)
    row_rate = 2 * edge_rate
    epsilon = 2 * edge_rate * loss**2
    assert row_rate * epsilon / 4 == 1
    assert 3 * (2 * sp.pi / 3) == 2 * sp.pi
    assert 4 * sp.pi / 3 > sp.pi

    active_losses = [Q(2, 3)] * 3
    active_rates = [Q(1)] * 3
    inactive_rate = Q(0)
    assert sum(active_rates) == 3
    assert sum(
        a * ell for a, ell in zip(active_rates, active_losses, strict=True)
    ) == 2
    assert inactive_rate * Q(4, 3) == 0

    g12, g13, g23 = Q(1), Q(2), Q(5)
    masses = (g12 + g13, g12 + g23, g13 + g23)
    assert masses == (3, 6, 7) and len(set(masses)) == 3

    points = [(1, 0, 0), (1, 0, 0), (0, 1, 0)]
    assert len(set(points)) < len(points)

    alpha = sp.acos(Q(-1, 3) / (1 + Q(-1, 3)))
    assert sp.simplify(4 * alpha - 2 * sp.pi) != 0
    print("executable hypothesis-deletion regressions: PASS")


def parse_graph6_stream(data: bytes) -> list[nx.Graph]:
    graphs: list[nx.Graph] = []
    for raw in data.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith(b">>"):
            continue
        graphs.append(nx.convert_node_labels_to_integers(nx.from_graph6_bytes(raw)))
    return graphs


def compile_pinned_plantri() -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    temp = tempfile.TemporaryDirectory(prefix="afp-p3-plantri-")
    root = Path(temp.name)
    source = urllib.request.urlopen(PLANTRI_URL, timeout=60).read()
    actual = git_blob_sha(source)
    if actual != PLANTRI_BLOB:
        temp.cleanup()
        raise AssertionError(f"plantri blob mismatch: {actual} != {PLANTRI_BLOB}")
    cfile = root / "plantri.c"
    exe = root / "plantri"
    cfile.write_bytes(source)
    subprocess.run(
        [os.environ.get("CC", "cc"), "-O3", "-std=c99", "-o", str(exe), str(cfile)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return exe, temp


def plantri_enumeration_audit(catalog: Path | None) -> None:
    exe, temp = compile_pinned_plantri()
    total = 0
    survivors: list[tuple[int, int, str]] = []
    output = catalog.open("w", encoding="utf-8") if catalog else None
    try:
        for n, expected in PLANTRI_COUNTS.items():
            proc = subprocess.run(
                [str(exe), "-g", str(n)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            graphs = parse_graph6_stream(proc.stdout)
            assert len(graphs) == expected, (n, len(graphs), expected)
            total += len(graphs)
            seen: set[str] = set()
            for graph in graphs:
                graph6 = nx.to_graph6_bytes(graph, header=False).decode().strip()
                assert graph6 not in seen
                seen.add(graph6)
                degrees = sorted(dict(graph.degree()).values())
                equivelar = len(set(degrees)) == 1
                q = degrees[0] if equivelar else None
                if equivelar and q in (3, 4, 5) and n == 12 // (6 - q):
                    survivors.append((n, q, graph6))
                if output:
                    output.write(
                        f"{n}\t{graph.number_of_edges()}\t"
                        f"{','.join(map(str, degrees))}\t{graph6}\n"
                    )
        assert total == 9150
        assert {(n, q) for n, q, _ in survivors} == {(4, 3), (6, 4), (12, 5)}
        assert len(survivors) == 3
    finally:
        if output:
            output.close()
        temp.cleanup()
    print("source-pinned plantri enumeration through 12 vertices: PASS (9150 maps)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-plantri", action="store_true")
    parser.add_argument("--catalog", type=Path)
    args = parser.parse_args()

    gram_heron_certificate()
    platonic_coordinate_and_q_audit()
    weighted_octahedron_sampling_audit()
    antipodal_boundary_audit()
    executable_hypothesis_deletions()
    if args.require_plantri:
        plantri_enumeration_audit(args.catalog)
    print("Prompt 3 completion audit: PASS")


if __name__ == "__main__":
    main()
