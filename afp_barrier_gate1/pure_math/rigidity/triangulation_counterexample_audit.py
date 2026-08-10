#!/usr/bin/env python3
"""Source-pinned hostile triangulation audit for Prompt 3.

Status: COMPUTATIONAL.  Enumeration through twelve vertices is falsification
and regression evidence only; it is never cited as the all-orders
classification proof.

The default and release mode (``--require-plantri`` or
``P3_REQUIRE_PLANTRI=1``) accept no prebuilt executable and no executable
cache.  They download or read the exact pinned ``plantri.c`` blob, verify its
Git blob SHA, compile that verified source in a fresh temporary directory,
enumerate there, and delete the source, binary, and generated streams when the
process exits.  An explicit ``--allow-no-plantri`` developer mode is the only
fail-open path and is not used by the final contract or CI.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

import sympy as sp


PLANTRI_COMMIT = "09745aeb09819bf200cfc77617f000258dba0a49"
PLANTRI_BLOB = "06802f7a92ffea2526711232a53b9e2e84104777"
PLANTRI_URL = (
    "https://raw.githubusercontent.com/mishun/plantri/"
    f"{PLANTRI_COMMIT}/plantri.c"
)
PLANTRI_COUNTS = {
    4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50,
    10: 233, 11: 1249, 12: 7595,
}


@dataclass(frozen=True)
class TriangulationRecord:
    vertices: int
    graph6: str
    edges: int
    faces: int
    degree_sequence: tuple[int, ...]
    equivelar: bool
    common_degree: int | None
    round_equal_edge_candidate: bool
    computational_disposition: str


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def read_verified_plantri_source(source_path: Path | None) -> tuple[bytes, str]:
    if source_path is None:
        with urllib.request.urlopen(PLANTRI_URL, timeout=45) as response:
            source = response.read()
        provenance = f"download:{PLANTRI_URL}"
    else:
        source = source_path.read_bytes()
        provenance = f"file:{source_path}"
    actual = git_blob_sha(source)
    if actual != PLANTRI_BLOB:
        raise RuntimeError(f"plantri source blob mismatch: {actual} != {PLANTRI_BLOB}")
    return source, provenance


def compile_verified_plantri(source: bytes, directory: Path) -> Path:
    source_path = directory / "plantri.c"
    executable = directory / "plantri"
    source_path.write_bytes(source)
    compiler = os.environ.get("CC", "cc")
    subprocess.run(
        [compiler, "-O3", "-std=c99", "-o", str(executable), str(source_path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return executable


def graph6_adjacency(record: bytes) -> tuple[set[int], ...]:
    raw = record.strip()
    if raw.startswith(b">>graph6<<"):
        raw = raw[len(b">>graph6<<"):]
    if not raw:
        raise ValueError("empty graph6 record")
    first = raw[0] - 63
    if not 0 <= first <= 62:
        raise ValueError(f"unsupported graph6 order byte {raw[0]}")
    n = first
    needed = n * (n - 1) // 2
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < needed:
        raise ValueError("truncated graph6 payload")
    adjacency = [set() for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    return tuple(adjacency)


def edge_count(adjacency: tuple[set[int], ...] | list[set[int]]) -> int:
    return sum(len(row) for row in adjacency) // 2


def graph_isomorphic(left: tuple[set[int], ...], right: tuple[set[int], ...]) -> bool:
    """Small exact backtracking isomorphism check (orders here are at most 12)."""
    if len(left) != len(right):
        return False
    n = len(left)
    if sorted(map(len, left)) != sorted(map(len, right)):
        return False
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def choose_vertex() -> int:
        unmapped = [vertex for vertex in range(n) if vertex not in mapping]
        return max(
            unmapped,
            key=lambda vertex: (
                sum(neighbour in mapping for neighbour in left[vertex]),
                len(left[vertex]),
                -vertex,
            ),
        )

    def compatible(source: int, target: int) -> bool:
        if len(left[source]) != len(right[target]):
            return False
        for old_source, old_target in mapping.items():
            if ((old_source in left[source]) != (old_target in right[target])):
                return False
        # A cheap forward check compares the degree multiset of currently
        # unmapped neighbours.
        source_profile = sorted(
            len(left[v]) for v in left[source] if v not in mapping
        )
        target_profile = sorted(
            len(right[v]) for v in right[target] if v not in used
        )
        return source_profile == target_profile

    def search() -> bool:
        if len(mapping) == n:
            return True
        source = choose_vertex()
        candidates = [target for target in range(n) if target not in used and compatible(source, target)]
        for target in candidates:
            mapping[source] = target
            used.add(target)
            if search():
                return True
            used.remove(target)
            del mapping[source]
        return False

    return search()


def record_graph(raw_graph6: bytes) -> TriangulationRecord:
    adjacency = graph6_adjacency(raw_graph6)
    n = len(adjacency)
    edges = edge_count(adjacency)
    if edges != 3 * n - 6:
        raise AssertionError(f"plantri record has {edges} edges at n={n}")
    degrees = tuple(sorted((len(row) for row in adjacency), reverse=True))
    equivelar = len(set(degrees)) == 1
    common_degree = degrees[0] if equivelar else None
    candidate = bool(
        equivelar
        and common_degree in (3, 4, 5)
        and n == 12 // (6 - common_degree)
    )
    if candidate:
        disposition = "survives necessary equilateral-angle/Euler filters"
    elif not equivelar:
        disposition = "rejected: round angle sum would force constant valence"
    elif common_degree not in (3, 4, 5):
        disposition = "rejected: positive spherical excess and Euler force q in {3,4,5}"
    else:
        disposition = "rejected: V=12/(6-q)"
    return TriangulationRecord(
        vertices=n,
        graph6=raw_graph6.decode("ascii").strip(),
        edges=edges,
        faces=2 * n - 4,
        degree_sequence=degrees,
        equivelar=equivelar,
        common_degree=common_degree,
        round_equal_edge_candidate=candidate,
        computational_disposition=disposition,
    )


def parse_plantri_stream(stream: bytes) -> list[bytes]:
    records = []
    for raw in stream.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith(b">>"):
            continue
        # Parsing here is also a structural validation of every record.
        graph6_adjacency(stripped)
        records.append(stripped)
    return records


def enumerate_plantri(executable: Path, catalog: Path | None) -> tuple[dict[int, int], list[TriangulationRecord]]:
    counts: dict[int, int] = {}
    survivors: list[TriangulationRecord] = []
    catalog_handle = catalog.open("w", encoding="utf-8") if catalog else None
    try:
        for n, expected in PLANTRI_COUNTS.items():
            process = subprocess.run(
                [str(executable), "-g", str(n)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            raw_records = parse_plantri_stream(process.stdout)
            counts[n] = len(raw_records)
            if counts[n] != expected:
                raise AssertionError(
                    f"plantri count n={n}: {counts[n]} != {expected}; "
                    f"stderr={process.stderr.decode(errors='replace')}"
                )
            if len(set(raw_records)) != len(raw_records):
                raise AssertionError(f"duplicate deterministic graph6 record at n={n}")
            for raw in raw_records:
                record = record_graph(raw)
                if record.round_equal_edge_candidate:
                    survivors.append(record)
                if catalog_handle:
                    catalog_handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
    finally:
        if catalog_handle:
            catalog_handle.close()
    return counts, survivors


def exact_sign(value: sp.Expr) -> int:
    simplified = sp.collect(sp.radsimp(sp.simplify(value)), sp.sqrt(5))
    if simplified == 0:
        return 0
    if simplified.is_positive:
        return 1
    if simplified.is_negative:
        return -1
    raise AssertionError(f"undecided exact algebraic sign: {simplified}")


def classified_coordinate_data() -> dict[str, tuple[list[sp.Matrix], sp.Expr]]:
    phi = (1 + sp.sqrt(5)) / 2
    tetrahedron = [
        sp.Matrix(v)
        for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    octahedron: list[sp.Matrix] = []
    for axis in range(3):
        for sign in (-1, 1):
            v = [0, 0, 0]
            v[axis] = sign
            octahedron.append(sp.Matrix(v))
    icosahedron = [
        sp.Matrix(v)
        for v in (
            (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi),
            (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
            (phi, 0, 1), (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1),
        )
    ]
    return {
        "tetrahedron": (tetrahedron, -sp.Rational(1, 3)),
        "octahedron": (octahedron, sp.Integer(0)),
        "icosahedron": (icosahedron, 1 / sp.sqrt(5)),
    }


def adjacency_from_coordinates(vertices: list[sp.Matrix], cosine: sp.Expr) -> tuple[set[int], ...]:
    norm2 = sp.simplify(vertices[0].dot(vertices[0]))
    if any(sp.simplify(vertex.dot(vertex) - norm2) != 0 for vertex in vertices):
        raise AssertionError("coordinate radii differ")
    adjacency = [set() for _ in vertices]
    for i, j in itertools.combinations(range(len(vertices)), 2):
        if sp.simplify(vertices[i].dot(vertices[j]) / norm2 - cosine) == 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    return tuple(adjacency)


def exact_embedding_certificate(name: str, vertices: list[sp.Matrix], cosine: sp.Expr) -> tuple[
    tuple[set[int], ...], dict[str, object]
]:
    adjacency = adjacency_from_coordinates(vertices, cosine)
    n = len(vertices)
    edges = edge_count(adjacency)
    triangles = {
        triple for triple in itertools.combinations(range(n), 3)
        if triple[1] in adjacency[triple[0]]
        and triple[2] in adjacency[triple[0]]
        and triple[2] in adjacency[triple[1]]
    }
    facets: set[tuple[int, int, int]] = set()
    origin_inside = True
    for triple in itertools.combinations(range(n), 3):
        a, b, c = (vertices[index] for index in triple)
        normal = (b - a).cross(c - a)
        if normal == sp.zeros(3, 1):
            continue
        signs = [exact_sign(normal.dot(vertices[index] - a))
                 for index in range(n) if index not in triple]
        if signs and all(sign != 0 for sign in signs) \
                and (all(sign > 0 for sign in signs) or all(sign < 0 for sign in signs)):
            facets.add(triple)
            if exact_sign(normal.dot(-a)) != signs[0]:
                origin_inside = False
    if facets != triangles:
        raise AssertionError(f"{name}: clique triangles and exact hull facets differ")
    if not origin_inside:
        raise AssertionError(f"{name}: origin is not strictly inside every facet halfspace")
    if edges != 3 * n - 6 or len(facets) != 2 * n - 4:
        raise AssertionError(f"{name}: triangulation counts fail")
    edge_face_counts: dict[tuple[int, int], int] = {}
    for face in facets:
        for edge in itertools.combinations(face, 2):
            ordered = tuple(sorted(edge))
            edge_face_counts[ordered] = edge_face_counts.get(ordered, 0) + 1
    if set(edge_face_counts.values()) != {2} or len(edge_face_counts) != edges:
        raise AssertionError(f"{name}: edge/face incidence fails")
    if exact_sign(1 + cosine) <= 0 or exact_sign(1 - cosine) <= 0:
        raise AssertionError(f"{name}: edge is not an exact nonantipodal minor-arc pair")
    gram = sp.Matrix.hstack(*vertices).T * sp.Matrix.hstack(*vertices)
    if gram.rank() != 3:
        raise AssertionError(f"{name}: Gram rank is not three")
    return adjacency, {
        "vertices": n,
        "edges": edges,
        "faces": len(facets),
        "degree_sequence": sorted((len(row) for row in adjacency), reverse=True),
        "normalized_edge_dot": str(sp.simplify(cosine)),
        "minor_arc_certificate": "exact -1 < cos(theta) < 1",
        "exact_convex_hull_facets": len(facets),
        "origin_strictly_inside": origin_inside,
        "Gram_rank": gram.rank(),
        "PSD_certificate": "G = X^T X over Q(sqrt(5))",
    }


def verify_survivors(survivors: list[TriangulationRecord] | None) -> dict[str, object]:
    exact: dict[str, object] = {}
    classified_graphs: dict[tuple[int, int], tuple[set[int], ...]] = {}
    for name, (vertices, cosine) in classified_coordinate_data().items():
        adjacency, certificate = exact_embedding_certificate(name, vertices, cosine)
        degree_set = {len(row) for row in adjacency}
        if len(degree_set) != 1:
            raise AssertionError(f"{name}: not equivelar")
        key = (len(vertices), next(iter(degree_set)))
        classified_graphs[key] = adjacency
        exact[name] = certificate

    if survivors is not None:
        keys = [(record.vertices, record.common_degree) for record in survivors]
        if sorted(keys) != sorted(classified_graphs):
            raise AssertionError(f"unexpected equivelar survivor keys: {keys}")
        for record in survivors:
            key = (record.vertices, record.common_degree)
            generated = graph6_adjacency(record.graph6.encode("ascii"))
            if not graph_isomorphic(generated, classified_graphs[key]):
                raise AssertionError(f"plantri survivor {key} is not the exact classified graph")
    return exact


def assert_vector_zero(vector: sp.Matrix, label: str) -> None:
    if any(sp.simplify(entry) != 0 for entry in vector):
        raise AssertionError(f"{label}: {vector}")


def hypothesis_deletion_regressions() -> dict[str, object]:
    certificates: dict[str, object] = {}

    # Nontriangulated equal-loss supports: exact edge counts already exclude a
    # spherical triangulation before any finite classification is invoked.
    cube_vertices = [sp.Matrix(v) for v in itertools.product((-1, 1), repeat=3)]
    cube = adjacency_from_coordinates(cube_vertices, sp.Rational(1, 3))
    if edge_count(cube) != 12 or edge_count(cube) == 3 * 8 - 6:
        raise AssertionError("cube nontriangulation witness changed")
    certificates["nontriangulated_support"] = {"witness": "cube", "V": 8, "E": 12}

    # Triangulate all six abstract cube faces with one zero-conductance diagonal
    # per face.  The resulting abstract support has 3V-6 edges, but its active
    # graph is still the exact Q=1 cube and does not include those six edges.
    inactive_diagonals: set[tuple[int, int]] = set()
    for axis in range(3):
        for sign in (-1, 1):
            face = [index for index, vertex in enumerate(cube_vertices) if vertex[axis] == sign]
            candidates = [
                (i, j) for i, j in itertools.combinations(face, 2)
                if j not in cube[i]
            ]
            if len(candidates) != 2:
                raise AssertionError("cube face does not have exactly two diagonals")
            inactive_diagonals.add(min(candidates))
    if len(inactive_diagonals) != 6 \
            or edge_count(cube) + len(inactive_diagonals) != 3 * len(cube_vertices) - 6:
        raise AssertionError("inactive-diagonal cube triangulation count changed")
    if any(j in cube[i] for i, j in inactive_diagonals):
        raise AssertionError("inactive diagonal became active")
    certificates["inactive_triangulation_edge"] = {
        "witness": "all six cube faces triangulated by gamma=0 diagonals",
        "inactive_edges": [list(edge) for edge in sorted(inactive_diagonals)],
        "abstract_edges": 18, "active_edges": 12, "gamma": 0,
    }

    # Major arcs use the same endpoints as minor arcs but have length > pi.
    major_length = 4 * sp.pi / 3
    if not (major_length - sp.pi).is_positive:
        raise AssertionError("major-arc witness is not major")
    certificates["major_arc"] = {"minor": "2*pi/3", "major": "4*pi/3"}

    coincident = sp.Matrix([1, 0, 0])
    if sp.simplify(1 - coincident.dot(coincident)) != 0:
        raise AssertionError("coincident endpoint loss is not zero")
    certificates["coincident_endpoints"] = {"loss": 0}

    antipode = -coincident
    antipodal_loss = sp.simplify(1 - coincident.dot(antipode))
    antipodal_rate = sp.Integer(1)
    antipodal_q = sp.simplify(antipodal_rate * (antipodal_rate * antipodal_loss**2) / 4)
    antipodal_generator_rows = (
        antipodal_rate * (antipode - coincident),
        antipodal_rate * (coincident - antipode),
    )
    assert_vector_zero(
        antipodal_generator_rows[0] + 2 * coincident,
        "antipodal coordinate eigenmap at first row",
    )
    assert_vector_zero(
        antipodal_generator_rows[1] + 2 * antipode,
        "antipodal coordinate eigenmap at second row",
    )
    tangent_denominator_squared = sp.simplify(antipodal_loss * (2 - antipodal_loss))
    tangent_denominator = sp.sqrt(tangent_denominator_squared)
    if antipodal_loss != 2 or antipodal_q != 1 \
            or tangent_denominator_squared != 0 or tangent_denominator != 0:
        raise AssertionError("antipodal Q=1 witness changed")
    certificates["antipodes"] = {
        "loss": str(antipodal_loss),
        "rate": 1,
        "Q": 1,
        "coordinate_eigenmap": "exact at both rows",
        "tangent_denominator_squared": str(tangent_denominator_squared),
        "tangent_denominator": str(tangent_denominator),
    }

    # Two minor great-circle arcs with disjoint endpoints cross at the north
    # pole.  Each endpoint is pi/3 from the pole and the edge length is 2pi/3.
    sqrt3 = sp.sqrt(3)
    crossing_edges = (
        (sp.Matrix([sqrt3 / 2, 0, sp.Rational(1, 2)]),
         sp.Matrix([-sqrt3 / 2, 0, sp.Rational(1, 2)])),
        (sp.Matrix([0, sqrt3 / 2, sp.Rational(1, 2)]),
         sp.Matrix([0, -sqrt3 / 2, sp.Rational(1, 2)])),
    )
    north = sp.Matrix([0, 0, 1])
    for edge in crossing_edges:
        if sp.simplify(edge[0].dot(edge[1]) + sp.Rational(1, 2)) != 0:
            raise AssertionError("crossing edge length changed")
        if any(sp.simplify(endpoint.dot(north) - sp.Rational(1, 2)) != 0 for endpoint in edge):
            raise AssertionError("north pole left a crossing minor arc")
    certificates["edge_crossing"] = {"intersection": "north pole", "shared_endpoint": False}

    equator = [
        sp.Matrix([1, 0, 0]),
        sp.Matrix([-sp.Rational(1, 2), sqrt3 / 2, 0]),
        sp.Matrix([-sp.Rational(1, 2), -sqrt3 / 2, 0]),
    ]
    equator_gram = sp.Matrix.hstack(*equator).T * sp.Matrix.hstack(*equator)
    if equator_gram.det() != 0 or sp.Matrix.hstack(*equator).rank() != 2:
        raise AssertionError("degenerate equatorial face certificate changed")
    certificates["degenerate_face"] = {"Gram_determinant": 0, "rank": 2}

    # Two distinct spherical convex triangles in the same open hemisphere both
    # contain the north ray in their interiors.  Positive cone coefficients are
    # an exact overlap certificate under radial projection.
    outer = [sp.Matrix([1, 0, 1]), sp.Matrix([0, 1, 1]), sp.Matrix([-1, -1, 1])]
    inner = [2 * outer[0] + outer[1] + outer[2],
             outer[0] + 2 * outer[1] + outer[2],
             outer[0] + outer[1] + 2 * outer[2]]
    if sum(outer, sp.zeros(3, 1)) != 3 * north \
            or sum(inner, sp.zeros(3, 1)) != 12 * north:
        raise AssertionError("overlapping-face positive-cone witness changed")
    certificates["overlapping_faces"] = {
        "common_interior_ray": "north", "outer_coefficients": [1, 1, 1],
        "inner_coefficients": [1, 1, 1],
    }

    cone_angle = 3 * sp.pi / 2
    if sp.simplify(2 * sp.pi - cone_angle) != sp.pi / 2:
        raise AssertionError("cone-gap witness changed")
    certificates["gap_or_cone_defect"] = {
        "three_octant_angles": "3*pi/2", "gap": "pi/2",
    }

    signed_weights = (Fraction(1, 3), Fraction(1), -Fraction(1, 3))
    signed_scales = (Fraction(0), Fraction(2), Fraction(3))
    if sum((p * x for p, x in zip(signed_weights, signed_scales)), Fraction(0)) != 1 \
            or sum((p * x * x for p, x in zip(signed_weights, signed_scales)), Fraction(0)) != 1:
        raise AssertionError("signed Q=1 nonrigidity witness changed")
    certificates["signed_rates"] = {
        "weights": [str(value) for value in signed_weights],
        "scales": [str(value) for value in signed_scales],
    }

    # Directed octahedral rows: every state jumps at rate one to +/- of the next
    # axis.  Neighbour vectors cancel, so L Omega=-2 Omega and Q=1, but activity
    # is not symmetric.
    axes: list[sp.Matrix] = []
    axis_of: list[int] = []
    for axis in range(3):
        for sign in (-1, 1):
            vector = sp.zeros(3, 1)
            vector[axis, 0] = sign
            axes.append(vector)
            axis_of.append(axis)
    directed = [[sp.Integer(0) for _ in axes] for _ in axes]
    for i, vector in enumerate(axes):
        target_axis = (axis_of[i] + 1) % 3
        for j in range(len(axes)):
            if axis_of[j] == target_axis:
                directed[i][j] = 1
        generator_value = sum(
            (directed[i][j] * (axes[j] - vector) for j in range(len(axes))),
            sp.zeros(3, 1),
        )
        assert_vector_zero(generator_value + 2 * vector, "directed octahedron eigenmap")
        losses = [sp.simplify(1 - vector.dot(axes[j])) for j in range(len(axes))]
        row_rate = sum(directed[i])
        epsilon = sum(directed[i][j] * losses[j] ** 2 for j in range(len(axes)))
        if row_rate != 2 or sp.simplify(row_rate * epsilon / 4) != 1:
            raise AssertionError("directed octahedron Q changed")
    asymmetric_pair = next(
        (i, j) for i in range(len(axes)) for j in range(len(axes))
        if directed[i][j] > 0 and directed[j][i] == 0
    )
    certificates["directed_support"] = {
        "Q": 1, "row_rate": 2, "asymmetric_active_pair": list(asymmetric_pair),
    }

    nonreversible_p = [
        [Fraction(0), Fraction(1, 3), Fraction(2, 3)],
        [Fraction(1, 4), Fraction(0), Fraction(3, 4)],
        [Fraction(1, 5), Fraction(4, 5), Fraction(0)],
    ]
    if any(sum(row, Fraction(0)) != 1 for row in nonreversible_p):
        raise AssertionError("nonreversible row-stochastic witness changed")
    forward_cycle = nonreversible_p[0][1] * nonreversible_p[1][2] * nonreversible_p[2][0]
    reverse_cycle = nonreversible_p[0][2] * nonreversible_p[2][1] * nonreversible_p[1][0]
    if forward_cycle == reverse_cycle:
        raise AssertionError("Kolmogorov cycle obstruction vanished")
    nonreversible_rates = [[sp.Integer(0) for _ in axes] for _ in axes]
    for i, axis in enumerate(axis_of):
        for j, other in enumerate(axis_of):
            if axis != other:
                probability = nonreversible_p[axis][other]
                nonreversible_rates[i][j] = sp.Rational(probability.numerator, probability.denominator)
        generator_value = sum(
            (nonreversible_rates[i][j] * (axes[j] - axes[i]) for j in range(len(axes))),
            sp.zeros(3, 1),
        )
        assert_vector_zero(generator_value + 2 * axes[i], "nonreversible octahedron eigenmap")
        row_rate = sum(nonreversible_rates[i])
        losses = [sp.simplify(1 - axes[i].dot(axes[j])) for j in range(len(axes))]
        epsilon = sum(nonreversible_rates[i][j] * losses[j] ** 2 for j in range(len(axes)))
        if row_rate != 2 or sp.simplify(row_rate * epsilon / 4) != 1:
            raise AssertionError("nonreversible octahedron Q changed")
    certificates["nonreversibility"] = {
        "forward_cycle_product": str(forward_cycle),
        "reverse_cycle_product": str(reverse_cycle),
        "lifted_octahedral_Q": 1,
    }

    # Duplicate one tetrahedral node and split the incident reversible
    # conductance.  The coordinate equation and Q remain exact while injectivity
    # fails.  This is an executable state-splitting witness, not a face tiling.
    tetra = [
        sp.Matrix(v)
        for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    duplicated = [tetra[0], tetra[0], tetra[1], tetra[2], tetra[3]]
    masses = [sp.Integer(1), sp.Integer(1), sp.Integer(2), sp.Integer(2), sp.Integer(2)]
    rates = [[sp.Rational(0) for _ in duplicated] for _ in duplicated]
    for duplicate in (0, 1):
        for other in (2, 3, 4):
            rates[duplicate][other] = sp.Rational(1, 2)
            rates[other][duplicate] = sp.Rational(1, 4)
    for i, j in itertools.combinations((2, 3, 4), 2):
        rates[i][j] = rates[j][i] = sp.Rational(1, 2)
    norm2 = sp.Integer(3)
    for i, vertex in enumerate(duplicated):
        generator_value = sum(
            (rates[i][j] * (duplicated[j] - vertex) for j in range(len(duplicated))),
            sp.zeros(3, 1),
        )
        assert_vector_zero(generator_value + 2 * vertex, "duplicated tetrahedron eigenmap")
        row_rate = sum(rates[i])
        epsilon = sum(
            rates[i][j] * (1 - vertex.dot(duplicated[j]) / norm2) ** 2
            for j in range(len(duplicated))
        )
        if row_rate != sp.Rational(3, 2) or sp.simplify(row_rate * epsilon / 4) != 1:
            raise AssertionError("duplicated tetrahedron Q changed")
        for j in range(len(duplicated)):
            if sp.simplify(masses[i] * rates[i][j] - masses[j] * rates[j][i]) != 0:
                raise AssertionError("duplicated tetrahedron reversibility changed")
    if duplicated[0] != duplicated[1]:
        raise AssertionError("noninjective duplicate became injective")
    certificates["noninjective_embedding"] = {
        "vertices": 5, "distinct_embedded_points": 4,
        "coordinate_eigenmap": "exact", "Q": 1, "reversible": True,
    }

    required = {
        "nontriangulated_support", "inactive_triangulation_edge", "major_arc",
        "coincident_endpoints", "antipodes", "edge_crossing", "degenerate_face",
        "overlapping_faces", "gap_or_cone_defect", "signed_rates",
        "directed_support", "nonreversibility", "noninjective_embedding",
    }
    if set(certificates) != required:
        raise AssertionError(f"hypothesis-deletion coverage changed: {set(certificates) ^ required}")
    return certificates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path,
                        help="optional JSONL record; never written unless explicitly requested")
    parser.add_argument("--plantri-source", type=Path,
                        help="read this source file, verify the pinned blob, and compile it in temp")
    plantri_mode = parser.add_mutually_exclusive_group()
    plantri_mode.add_argument("--require-plantri", action="store_true")
    plantri_mode.add_argument(
        "--allow-no-plantri",
        action="store_true",
        help="developer-only: permit exact non-enumeration checks when pinned Plantri is unavailable",
    )
    arguments = parser.parse_args()
    require_plantri = (
        arguments.require_plantri
        or os.environ.get("P3_REQUIRE_PLANTRI") == "1"
        or not arguments.allow_no_plantri
    )

    counts: dict[int, int] | None = None
    survivors: list[TriangulationRecord] | None = None
    provenance: str | None = None
    unavailable: str | None = None
    try:
        source, provenance = read_verified_plantri_source(arguments.plantri_source)
        with tempfile.TemporaryDirectory(prefix="afp-p3-plantri-") as temporary:
            executable = compile_verified_plantri(source, Path(temporary))
            counts, survivors = enumerate_plantri(executable, arguments.catalog)
    except Exception as error:
        if require_plantri:
            raise
        unavailable = f"{type(error).__name__}: {error}"

    exact_embeddings = verify_survivors(survivors)
    deletions = hypothesis_deletion_regressions()
    if require_plantri and counts != PLANTRI_COUNTS:
        raise AssertionError("release mode did not verify every pinned plantri count")

    plantri_status = (
        "PASS_SOURCE_PINNED_LITERAL_ENUMERATION"
        if counts is not None else "UNAVAILABLE_NONRELEASE"
    )
    overall_status = "PASS" if counts is not None else "PASS_NONRELEASE_WITHOUT_ENUMERATION"
    report = {
        "status_label": "COMPUTATIONAL",
        "plantri": {
            "status": plantri_status,
            "commit": PLANTRI_COMMIT,
            "source_blob": PLANTRI_BLOB,
            "provenance": provenance,
            "unavailable": unavailable,
            "counts": counts,
            "expected_counts": PLANTRI_COUNTS,
            "range": [4, 12],
            "release_requires_literal_enumeration": True,
            "prebuilt_or_cached_executable_trusted": False,
        },
        "round_equal_edge_survivors": None if survivors is None else [
            {"V": record.vertices, "q": record.common_degree, "graph6": record.graph6}
            for record in survivors
        ],
        "exact_embedding_certificates": exact_embeddings,
        "executable_hypothesis_deletions": deletions,
        "finite_enumeration_proves_classification": "REJECTED",
        "status": overall_status,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
