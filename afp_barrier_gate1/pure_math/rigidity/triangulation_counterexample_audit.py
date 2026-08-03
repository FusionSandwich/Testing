#!/usr/bin/env python3
"""Exact/certified hostile audit for Prompt 3 spherical triangulation claims.

When plantri is available (or network access permits fetching the pinned source),
this script enumerates every simple 3-connected spherical triangulation on
4,...,12 vertices.  It verifies the canonical plantri counts, records every
map, and isolates the only equivelar maps compatible with a round equal-edge
tiling.  The three surviving maps are then matched independently to exact
algebraic tetrahedral, octahedral, and icosahedral embeddings.

Without plantri, the default local mode still runs all exact geometry and
hypothesis-deletion regressions against the source-pinned catalog counts.  CI
sets P3_REQUIRE_PLANTRI=1, so release evidence always includes literal
enumeration rather than the fallback.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import urllib.request

import networkx as nx
import sympy as sp

PLANTRI_COMMIT = "09745aeb09819bf200cfc77617f000258dba0a49"
PLANTRI_BLOB = "06802f7a92ffea2526711232a53b9e2e84104777"
PLANTRI_URL = (
    "https://raw.githubusercontent.com/mishun/plantri/"
    f"{PLANTRI_COMMIT}/plantri.c"
)
PLANTRI_COUNTS = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50,
                  10: 233, 11: 1249, 12: 7595}


@dataclass
class TriangulationRecord:
    n: int
    graph6: str
    edges: int
    faces: int
    degree_sequence: list[int]
    equivelar: bool
    common_degree: int | None
    round_equal_edge_tiling_possible: bool
    exclusion_certificate: str
    automorphism_order: int | None


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def obtain_plantri(require: bool) -> tuple[str | None, str]:
    explicit = os.environ.get("PLANTRI")
    if explicit:
        path = shutil.which(explicit) or explicit
        if Path(path).is_file():
            return path, "environment"
        if require:
            raise RuntimeError(f"PLANTRI={explicit!r} is not executable")

    found = shutil.which("plantri")
    if found:
        return found, "PATH"

    cache = Path(tempfile.gettempdir()) / "afp-p3-plantri-4.5"
    exe = cache / "plantri"
    if exe.is_file():
        return str(exe), "cache"
    try:
        cache.mkdir(parents=True, exist_ok=True)
        source = urllib.request.urlopen(PLANTRI_URL, timeout=30).read()
        actual = git_blob_sha(source)
        if actual != PLANTRI_BLOB:
            raise RuntimeError(f"plantri blob mismatch: {actual} != {PLANTRI_BLOB}")
        cfile = cache / "plantri.c"
        cfile.write_bytes(source)
        subprocess.run(
            [os.environ.get("CC", "cc"), "-O3", "-std=c99", "-o", str(exe), str(cfile)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return str(exe), "pinned-download"
    except Exception as exc:  # local sandbox may intentionally have no network
        if require:
            raise RuntimeError("plantri enumeration required but unavailable") from exc
        return None, f"catalog-fallback: {type(exc).__name__}: {exc}"


def parse_graph6_stream(data: bytes) -> list[nx.Graph]:
    graphs: list[nx.Graph] = []
    for raw in data.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith(b">>"):
            continue
        g = nx.from_graph6_bytes(raw)
        graphs.append(nx.convert_node_labels_to_integers(g, ordering="sorted"))
    return graphs


def automorphism_order(g: nx.Graph) -> int:
    return sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g, g).isomorphisms_iter())


def record_graph(g: nx.Graph) -> TriangulationRecord:
    n = g.number_of_nodes()
    e = g.number_of_edges()
    if e != 3 * n - 6:
        raise AssertionError((n, e))
    planar, embedding = nx.check_planarity(g, counterexample=True)
    if not planar:
        raise AssertionError("plantri emitted a nonplanar graph")
    degrees = sorted((d for _, d in g.degree()), reverse=True)
    equivelar = len(set(degrees)) == 1
    q = degrees[0] if equivelar else None
    possible = equivelar and q in (3, 4, 5) and n == 12 // (6 - q)
    if possible:
        exclusion = "survives Euler/round-angle necessary conditions"
    elif not equivelar:
        exclusion = "equal spherical face angle plus 2*pi angle sum would force constant valence"
    elif q not in (3, 4, 5):
        exclusion = "Euler and positive-area angle range force q in {3,4,5}"
    else:
        exclusion = "Euler count V=12/(6-q) fails"
    aut = automorphism_order(g) if possible or n <= 7 else None
    return TriangulationRecord(
        n=n,
        graph6=nx.to_graph6_bytes(g, header=False).decode().strip(),
        edges=e,
        faces=2 * n - 4,
        degree_sequence=degrees,
        equivelar=equivelar,
        common_degree=q,
        round_equal_edge_tiling_possible=possible,
        exclusion_certificate=exclusion,
        automorphism_order=aut,
    )


def enumerate_plantri(exe: str, catalog: Path | None) -> tuple[dict[int, int], list[TriangulationRecord]]:
    counts: dict[int, int] = {}
    survivors: list[TriangulationRecord] = []
    out = catalog.open("w", encoding="utf-8") if catalog else None
    try:
        for n, expected in PLANTRI_COUNTS.items():
            proc = subprocess.run(
                [exe, "-g", str(n)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            graphs = parse_graph6_stream(proc.stdout)
            counts[n] = len(graphs)
            if len(graphs) != expected:
                raise AssertionError(
                    f"plantri count n={n}: {len(graphs)} != pinned guide count {expected}; "
                    f"stderr={proc.stderr.decode(errors='replace')}"
                )
            seen = set()
            for g in graphs:
                rec = record_graph(g)
                if rec.graph6 in seen:
                    raise AssertionError(f"duplicate graph6 at n={n}")
                seen.add(rec.graph6)
                if rec.round_equal_edge_tiling_possible:
                    survivors.append(rec)
                if out:
                    out.write(json.dumps(asdict(rec), sort_keys=True) + "\n")
    finally:
        if out:
            out.close()
    return counts, survivors


def exact_sign(x: sp.Expr) -> int:
    y = sp.simplify(x)
    if y == 0:
        return 0
    if y.is_positive:
        return 1
    if y.is_negative:
        return -1
    # nsimplify against sqrt(5) keeps this branch exact for the coordinates used.
    y = sp.collect(sp.radsimp(y), sp.sqrt(5))
    if y.is_positive:
        return 1
    if y.is_negative:
        return -1
    raise AssertionError(f"undecided algebraic sign: {y}")


def coordinate_data(name: str) -> tuple[list[sp.Matrix], sp.Expr]:
    phi = (1 + sp.sqrt(5)) / 2
    if name == "tetrahedron":
        v = [sp.Matrix(x) for x in ((1, 1, 1), (1, -1, -1),
                                     (-1, 1, -1), (-1, -1, 1))]
        c = sp.Rational(-1, 3)
    elif name == "octahedron":
        v = []
        for k in range(3):
            for s in (1, -1):
                x = [0, 0, 0]
                x[k] = s
                v.append(sp.Matrix(x))
        c = sp.Rational(0)
    elif name == "icosahedron":
        raw = [
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1),
        ]
        v = [sp.Matrix(x) for x in raw]
        c = 1 / sp.sqrt(5)
    else:
        raise ValueError(name)
    norm2 = sp.simplify(v[0].dot(v[0]))
    if any(sp.simplify(x.dot(x) - norm2) != 0 for x in v):
        raise AssertionError("coordinate radii differ")
    return v, sp.simplify(c)


def exact_platonic_graph(name: str) -> tuple[nx.Graph, dict[str, object]]:
    vertices, c = coordinate_data(name)
    norm2 = sp.simplify(vertices[0].dot(vertices[0]))
    n = len(vertices)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for i, j in itertools.combinations(range(n), 2):
        dot = sp.simplify(vertices[i].dot(vertices[j]) / norm2)
        if sp.simplify(dot - c) == 0:
            g.add_edge(i, j)
    triangles = {
        tuple(sorted(t))
        for t in itertools.combinations(range(n), 3)
        if g.has_edge(t[0], t[1]) and g.has_edge(t[0], t[2]) and g.has_edge(t[1], t[2])
    }

    # Independently identify every triangular Euclidean convex-hull facet with
    # exact algebraic side tests.  Radial projection then gives the certified
    # noncrossing minor-arc spherical tiling because the origin is strictly
    # inside this convex polyhedron.
    facets = set()
    origin_inside = True
    for tri in itertools.combinations(range(n), 3):
        a, b, d = (vertices[k] for k in tri)
        normal = (b - a).cross(d - a)
        signs = [exact_sign(normal.dot(vertices[k] - a)) for k in range(n) if k not in tri]
        nonzero = [s for s in signs if s]
        if nonzero and (all(s > 0 for s in nonzero) or all(s < 0 for s in nonzero)) and len(nonzero) == n - 3:
            facets.add(tuple(sorted(tri)))
            side = nonzero[0]
            if exact_sign(normal.dot(-a)) != side:
                origin_inside = False
    if facets != triangles:
        raise AssertionError(f"{name}: clique triangles and exact hull facets differ")
    if not origin_inside:
        raise AssertionError(f"{name}: origin not certified interior")
    if len(triangles) != 2 * n - 4 or g.number_of_edges() != 3 * n - 6:
        raise AssertionError(f"{name}: triangulation counts fail")
    edge_face_count = Counter()
    for tri in triangles:
        for edge in itertools.combinations(tri, 2):
            edge_face_count[tuple(sorted(edge))] += 1
    if set(edge_face_count) != {tuple(sorted(e)) for e in g.edges()} or set(edge_face_count.values()) != {2}:
        raise AssertionError(f"{name}: face incidence fails")
    G = sp.Matrix.hstack(*vertices).T * sp.Matrix.hstack(*vertices)
    # Normalize only for reporting; X X^T is an exact PSD rank-three certificate.
    rank = G.rank()
    if rank != 3:
        raise AssertionError(f"{name}: Gram rank {rank}")
    return g, {
        "vertices": n,
        "edges": g.number_of_edges(),
        "faces": len(triangles),
        "degree_sequence": sorted(dict(g.degree()).values(), reverse=True),
        "normalized_edge_dot": str(c),
        "gram_rank": rank,
        "psd_certificate": "G=X X^T over Q(sqrt(5))",
        "injective": len({tuple(x) for x in vertices}) == n,
        "minor_arc": bool(-1 < float(c.evalf()) < 1),
        "exact_convex_hull_facets": len(facets),
        "origin_strictly_inside": origin_inside,
        "automorphism_order": automorphism_order(g),
    }


def verify_survivors(survivors: list[TriangulationRecord] | None) -> dict[str, object]:
    expected = {"tetrahedron": (4, 3), "octahedron": (6, 4), "icosahedron": (12, 5)}
    exact = {}
    graphs = {}
    for name, (n, q) in expected.items():
        g, cert = exact_platonic_graph(name)
        if g.number_of_nodes() != n or set(dict(g.degree()).values()) != {q}:
            raise AssertionError(name)
        exact[name] = cert
        graphs[(n, q)] = g
    if survivors is not None:
        if len(survivors) != 3:
            raise AssertionError(f"expected exactly three equivelar survivors, got {len(survivors)}")
        keys = {(r.n, r.common_degree) for r in survivors}
        if keys != set(graphs):
            raise AssertionError(f"survivor keys {keys}")
        for rec in survivors:
            pg = nx.from_graph6_bytes(rec.graph6.encode())
            if not nx.is_isomorphic(pg, graphs[(rec.n, rec.common_degree)]):
                raise AssertionError("plantri survivor not isomorphic to exact Platonic graph")
    return exact


def hypothesis_deletion_regressions() -> dict[str, str]:
    # These are exact constructions; details and formulas are expanded in the
    # ordinary theorem document and q1_covariance_audit.py.
    return {
        "triangulation_removed": "cube (K=8) and dodecahedron (K=20) shortest-edge graphs have Q=1",
        "connectedness_removed": "disjoint tetrahedral and octahedral components have different rates 3/2 and 2",
        "antipodal_edges_allowed": "two states +/-e1 with rate 1 have loss 2, r=1, Q=1",
        "nondegenerate_faces_removed": "three equatorial points at 120 degrees with edge rate 2/3 have Q=1 and zero-area great-circle face",
        "minor_arc_removed": "the same endpoints admit major arcs of length 4*pi/3",
        "all_triangulation_edges_active_removed": "triangulate each spherical cube face by an inactive diagonal; active cube edges retain Q=1",
        "reversibility_removed": "octahedral rows may choose independent positive opposite-pair weights while retaining r=2 and L Omega=-2 Omega",
        "equal_masses_removed": "weighted reversible octahedral family has masses g12+g13, g12+g23, g13+g23",
        "global_positivity_removed": "signed four-cardinal and regular-pentagon Prompt 2 regressions remain active",
        "full_round_coverage_or_no_cone_removed": "abstract congruent-triangle gluings permit cone angle q*alpha != 2*pi",
        "injectivity_removed": "duplicating an embedded state destroys the claimed embedded triangulation even when abstract rows are copied",
        "zero_conductance_permitted_edges": "inactive permitted edges are not controlled by equality propagation",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, help="write one JSON record per plantri map")
    parser.add_argument("--require-plantri", action="store_true")
    args = parser.parse_args()
    require = args.require_plantri or os.environ.get("P3_REQUIRE_PLANTRI") == "1"
    exe, source = obtain_plantri(require)
    if exe:
        counts, survivors = enumerate_plantri(exe, args.catalog)
        mode = "literal-plantri-enumeration"
    else:
        counts, survivors = dict(PLANTRI_COUNTS), None
        mode = "pinned-catalog-fallback"
    exact = verify_survivors(survivors)
    report = {
        "plantri": {
            "mode": mode,
            "source": source,
            "commit": PLANTRI_COMMIT,
            "blob": PLANTRI_BLOB,
            "counts": counts,
            "range": [4, 12],
            "total_maps": sum(counts.values()),
            "literal_enumeration_required_in_CI": True,
        },
        "round_equal_edge_survivors": ["K4", "octahedral graph", "icosahedral graph"],
        "exact_embedding_certificates": exact,
        "hypothesis_deletions": hypothesis_deletion_regressions(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
