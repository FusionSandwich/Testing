#!/usr/bin/env python3
"""Finite generator and row-class regression for shortened-gap S2 rings.

The theorem uses M0=2^80 and is never instantiated.  This executable uses
small M0 specializations of the same formulas.  It is a convergence and
hostile-mutation regression, not the guarded all-orders proof in
P1E_SHORT_GAP_S2_CONSTRUCTION.md, Section 6.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import math

import numpy as np


GAP = math.sqrt(29.0 / 32.0)


def nint_down(x: float) -> int:
    """Nearest integer, resolving an exact half-integer downward."""

    return math.ceil(x - 0.5)


def mask(M: int) -> tuple[tuple[int, float], ...]:
    alpha = math.pi / M
    c = math.cos(alpha)
    p = (4 * c * c + 2 * c - 1) / (4 * c * (c + 1))
    q = (2 * c + 1) * (4 * c * c + 2 * c - 1) / (8 * c * c * (c + 1))
    return (
        (0, p / 2),
        (2, (1 - p) / 4),
        (-2, (1 - p) / 4),
        (1, q / 4),
        (-1, q / 4),
        (3, (1 - q) / 4),
        (-3, (1 - q) / 4),
    )


def mask_moments(M: int, *, broken_m2: bool = False) -> tuple[float, float]:
    alpha = math.pi / M
    c = math.cos(alpha)
    p = (4 * c * c + 2 * c - 1) / (4 * c * (c + 1))
    beta = 0.5 + math.cos(2 * alpha) / (2 * c)
    ecos2 = p + (1 - p) * math.cos(2 * alpha) ** 2
    if broken_m2:
        return 1 - beta, 1 - 2 * beta * p + (1 - p) * math.cos(2 * alpha) ** 2
    return 1 - beta, 1 - 2 * beta + ecos2


def row_matrix(
    theta: float,
    h_minus: float,
    h_plus: float,
    moments_minus: tuple[float, float],
    moments_plus: tuple[float, float],
    delta: float,
    jumps: tuple[int, int],
) -> np.ndarray:
    """Exact formulas (3.1)--(3.4), columns U+, U-, H1, H2."""

    s, c = math.sin(theta), math.cos(theta)
    sp, sm = math.sin(theta + h_plus), math.sin(theta - h_minus)
    lp, lm = 1 - math.cos(h_plus), 1 - math.cos(h_minus)
    m1p, m2p = moments_plus
    m1m, m2m = moments_minus
    A = np.zeros((3, 4))
    A[0, 0] = math.sin(h_plus) - c * sp * m1p
    A[0, 1] = -math.sin(h_minus) - c * sm * m1m
    A[1, 0] = (
        math.sin(h_plus) * lp
        + (math.sin(h_plus) * s * sp - c * sp * lp) * m1p
        - c * s * sp**2 * m2p
    )
    A[1, 1] = (
        -math.sin(h_minus) * lm
        + (-math.sin(h_minus) * s * sm - c * sm * lm) * m1m
        - c * s * sm**2 * m2m
    )
    A[2, 0] = (
        math.sin(h_plus) ** 2
        - 2 * math.sin(h_plus) * c * sp * m1p
        + sp**2 * ((1 + c**2) * m2p - 2 * m1p)
    )
    A[2, 1] = (
        math.sin(h_minus) ** 2
        + 2 * math.sin(h_minus) * c * sm * m1m
        + sm**2 * ((1 + c**2) * m2m - 2 * m1m)
    )
    for column, jump in enumerate(jumps, 2):
        u = 1 - math.cos(jump * delta)
        A[0, column] = -2 * s * c * u
        A[1, column] = -2 * s**3 * c * u**2
        A[2, column] = 2 * s**2 * (c**2 * u**2 - (2 * u - u**2))
    return A


def transition_solve(
    theta: float,
    h: float,
    M: int,
    incoming: float,
    *,
    gap: float = GAP,
    broken_column: bool = False,
    broken_m2: bool = False,
) -> np.ndarray:
    moments = mask_moments(M, broken_m2=broken_m2)
    Rc = row_matrix(theta, h, gap * h, (0.0, 0.0), moments, 2 * math.pi / M, (1, 8))
    tf = theta + gap * h
    Rf = row_matrix(tf, gap * h, h, moments, (0.0, 0.0), math.pi / M, (1, 8))
    A = np.zeros((6, 6))
    b = np.zeros(6)
    A[:3, 0], A[:3, 2], A[:3, 3] = Rc[:, 0], Rc[:, 2], Rc[:, 3]
    b[:3] = -incoming * Rc[:, 1]
    column_sum = 1.0 if broken_column else 0.5
    A[3:, 0], A[3:, 1] = column_sum * Rf[:, 1], Rf[:, 0]
    A[3:, 4], A[3:, 5] = Rf[:, 2], Rf[:, 3]
    return np.linalg.solve(A, b)


def ordinary_solve(theta: float, h: float, M: int, incoming: float) -> tuple[float, float, float, int, int]:
    s, c = math.sin(theta), math.cos(theta)
    delta = 2 * math.pi / M
    ell = 1 - math.cos(h)
    zstar = ell / s**2
    phi = math.acos(1 - zstar)
    tm = max(1, math.floor(phi / (2 * delta)))
    tp = math.ceil(2 * phi / delta)
    um, up = 1 - math.cos(tm * delta), 1 - math.cos(tp * delta)
    xm, xp = um / zstar, up / zstar
    assert 0 < xm < 1 < xp
    km_frac = (xp - 1) / (xp - xm)
    kp_frac = (1 - xm) / (xp - xm)
    Scoef = 2 * s**2 / math.sin(h) ** 2 * (2 - (1 + c**2) * ell / s**2)
    Dcoef = 2 * s * c / math.sin(h)
    K = 2 * incoming / (Scoef - Dcoef)
    outgoing = K * (Scoef + Dcoef) / 2
    return outgoing, K * km_frac / um, K * kp_frac / up, tm, tp


@dataclass
class Ring:
    t: float
    count: int
    kind: str
    jumps: tuple[int, int] = (0, 0)
    horizontal: tuple[float, float] = (0.0, 0.0)


@dataclass
class Interface:
    lower: int
    kind: str
    conductance: float
    coarse_count: int = 0


@dataclass
class Family:
    h: float
    rings: list[Ring]
    interfaces: list[Interface]
    first_pole_conductance: float


def schedule(M0: int, J: int) -> tuple[float, list[Ring]]:
    MJ = M0 * 2**J
    S0 = MJ / 8
    t0 = [MJ / (4 * math.pi) * math.asin(2 ** (m - J)) for m in range(J)]
    k = [nint_down(x - 4 / 3 - m * GAP) for m, x in enumerate(t0)]
    K = nint_down(S0 - 4 / 3 - J * GAP)
    S = 4 / 3 + K + J * GAP
    h = math.pi / (2 * S)
    assert all(k[i + 1] > k[i] for i in range(J - 1))
    assert K >= k[-1]

    rings = [Ring(4 / 3, M0, "first")]
    for m in range(J):
        target = 4 / 3 + k[m] + m * GAP
        while rings[-1].t < target - 1e-12:
            rings.append(Ring(rings[-1].t + 1, M0 * 2**m, "ordinary"))
        assert abs(rings[-1].t - target) < 1e-10
        rings[-1].kind = "transition_coarse"
        rings.append(Ring(target + GAP, M0 * 2 ** (m + 1), "transition_fine"))
    while rings[-1].t < S - 1e-12:
        rings.append(Ring(rings[-1].t + 1, MJ, "ordinary"))
    assert abs(rings[-1].t - S) < 1e-9
    rings[-1].kind = "equator"
    return h, rings


def build_orbits(M0: int, J: int, **mutations: bool) -> Family:
    h, rings = schedule(M0, J)
    interfaces: list[Interface] = []
    pole = 1.0
    i = 0
    incoming = pole
    while i < len(rings):
        ring = rings[i]
        theta = ring.t * h
        delta = 2 * math.pi / ring.count
        if ring.kind == "first":
            jumps = (nint_down((3 / 8) / delta), nint_down((9 / 8) / delta))
            R = row_matrix(theta, theta, h, (0.0, 0.0), (0.0, 0.0), delta, jumps)
            sol = np.linalg.solve(R[:, (0, 2, 3)], -incoming * R[:, 1])
            outgoing, h1, h2 = sol
            ring.jumps, ring.horizontal = jumps, (h1, h2)
            interfaces.append(Interface(i, "aligned", float(outgoing)))
            incoming = float(outgoing)
        elif ring.kind == "ordinary":
            outgoing, h1, h2, t1, t2 = ordinary_solve(theta, h, ring.count, incoming)
            ring.jumps, ring.horizontal = (t1, t2), (h1, h2)
            interfaces.append(Interface(i, "aligned", outgoing))
            incoming = outgoing
        elif ring.kind == "transition_coarse":
            sol = transition_solve(
                theta,
                h,
                ring.count,
                incoming,
                gap=1.0 if mutations.get("equal_gap") else GAP,
                broken_column=mutations.get("broken_column", False),
                broken_m2=mutations.get("broken_m2", False),
            )
            uq, outgoing, hc1, hc8, hf1, hf8 = map(float, sol)
            ring.jumps, ring.horizontal = (1, 8), (hc1, hc8)
            rings[i + 1].jumps, rings[i + 1].horizontal = (1, 8), (hf1, hf8)
            interfaces.append(Interface(i, "transition", uq, ring.count))
            interfaces.append(Interface(i + 1, "aligned", outgoing))
            if min(sol) <= 0:
                raise ValueError(f"nonpositive transition at M={ring.count}: {min(sol)}")
            incoming = outgoing
            i += 1
        elif ring.kind == "transition_fine":
            raise AssertionError("fine endpoint must be consumed with coarse endpoint")
        elif ring.kind == "equator":
            jump = 2
            H = incoming * math.sin(h) ** 2 / math.sin(jump * delta) ** 2
            ring.jumps, ring.horizontal = (jump, 0), (H, 0.0)
            break
        else:
            raise AssertionError(ring.kind)
        i += 1
    assert len(interfaces) == len(rings) - 1
    coefficients = [pole]
    coefficients += [x.conductance for x in interfaces]
    coefficients += [x for r in rings for x in r.horizontal if x]
    assert min(coefficients) > 0
    return Family(h, rings, interfaces, pole)


def expand(family: Family) -> dict[str, np.ndarray | list[str] | float]:
    """Expand the orbit description to literal nodes and undirected edges."""

    h, nrings = family.h, len(family.rings)
    nodes: list[np.ndarray] = []
    classes: list[str] = []
    north_ids: list[list[int]] = []
    south_ids: list[list[int] | None] = []

    north_pole = 0
    nodes.append(np.array([0.0, 0.0, 1.0]))
    classes.append("pole")
    for ring in family.rings:
        ids = []
        theta = ring.t * h
        for j in range(ring.count):
            phi = 2 * math.pi * j / ring.count
            ids.append(len(nodes))
            nodes.append(np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)]))
            classes.append(ring.kind)
        north_ids.append(ids)
    for ri, ring in enumerate(family.rings):
        if ri == nrings - 1:
            south_ids.append(None)
            continue
        ids = []
        theta = math.pi - ring.t * h
        for j in range(ring.count):
            phi = 2 * math.pi * j / ring.count
            ids.append(len(nodes))
            nodes.append(np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)]))
            classes.append(ring.kind + "_south")
        south_ids.append(ids)
    south_pole = len(nodes)
    nodes.append(np.array([0.0, 0.0, -1.0]))
    classes.append("pole")

    edges: list[tuple[int, int, float]] = []

    def horizontal(ids: list[int], ring: Ring) -> None:
        for jump, conductance in zip(ring.jumps, ring.horizontal):
            if jump == 0 or conductance == 0:
                continue
            for j in range(ring.count):
                edges.append((ids[j], ids[(j + jump) % ring.count], conductance))

    for ri, ring in enumerate(family.rings):
        horizontal(north_ids[ri], ring)
        if south_ids[ri] is not None:
            horizontal(south_ids[ri], ring)  # type: ignore[arg-type]
    for j in north_ids[0]:
        edges.append((north_pole, j, family.first_pole_conductance))
    for j in south_ids[0] or []:
        edges.append((south_pole, j, family.first_pole_conductance))

    def add_interface(lower_ids: list[int], upper_ids: list[int], interface: Interface) -> None:
        if interface.kind == "aligned":
            assert len(lower_ids) == len(upper_ids)
            for u, v in zip(lower_ids, upper_ids):
                edges.append((u, v, interface.conductance))
        else:
            M = interface.coarse_count
            assert len(lower_ids) == M and len(upper_ids) == 2 * M
            for i in range(M):
                for offset, weight in mask(M):
                    edges.append((lower_ids[i], upper_ids[(2 * i + offset) % (2 * M)], interface.conductance * weight))

    for ri, interface in enumerate(family.interfaces):
        add_interface(north_ids[ri], north_ids[ri + 1], interface)
        lower_s = south_ids[ri]
        upper_s = south_ids[ri + 1]
        if upper_s is None:
            # Reflection of the last northern interface ends at the shared equator.
            add_interface(lower_s or [], north_ids[-1], interface)
        else:
            # Radial orientation is reversed in the south.  A transition has
            # fine vertices equatorward and coarse vertices poleward.
            if interface.kind == "transition":
                add_interface(lower_s or [], upper_s, interface)
            else:
                add_interface(lower_s or [], upper_s, interface)

    X = np.asarray(nodes)
    mu = np.zeros(len(X))
    for u, v, gamma in edges:
        ell = 1 - float(X[u] @ X[v])
        mu[u] += 0.5 * gamma * ell
        mu[v] += 0.5 * gamma * ell
    return {"h": h, "nodes": X, "edges": np.asarray(edges), "mu": mu, "weights": mu / mu.sum(), "classes": classes}


def residual_report(graph: dict[str, object]) -> tuple[float, float, float, float]:
    X = graph["nodes"]
    edges = graph["edges"]
    mu = graph["mu"]
    h = float(graph["h"])
    assert isinstance(X, np.ndarray) and isinstance(edges, np.ndarray) and isinstance(mu, np.ndarray)
    force = np.zeros_like(X)
    mixed = np.zeros_like(X)
    cov = np.zeros((len(X), 3, 3))
    for row in edges:
        u, v, gamma = int(row[0]), int(row[1]), float(row[2])
        ell = 1 - float(X[u] @ X[v])
        for i, j in ((u, v), (v, u)):
            diff = X[j] - X[i]
            tangent = diff + ell * X[i]
            force[i] += gamma * diff
            mixed[i] += gamma * ell * tangent
            cov[i] += gamma * np.outer(tangent, tangent)
    h1 = np.max(np.linalg.norm(force + 2 * mu[:, None] * X, axis=1) / np.maximum(mu, 1e-300))
    mix = np.max(np.linalg.norm(mixed, axis=1) / np.maximum(mu * h**2, 1e-300))
    iso = 0.0
    for i, x in enumerate(X):
        P = np.eye(3) - np.outer(x, x)
        T = P @ cov[i] @ P
        defect = T - np.trace(T) * P / 2
        iso = max(iso, np.linalg.norm(defect) / max(mu[i] * h**2, 1e-300))
    shared = len({(min(int(u), int(v)), max(int(u), int(v))) for u, v, _ in edges}) / len(edges)
    return float(h1), float(mix), float(iso), float(shared)


def quality_report(graph: dict[str, object], family: Family) -> tuple[float, ...]:
    """Mesh, rate, mass/weight, degree, and direct quotient diagnostics."""

    X = graph["nodes"]
    edges = graph["edges"]
    mu = graph["mu"]
    weights = graph["weights"]
    h = float(graph["h"])
    assert isinstance(X, np.ndarray) and isinstance(edges, np.ndarray)
    assert isinstance(mu, np.ndarray) and isinstance(weights, np.ndarray)
    degree = np.zeros(len(X), dtype=int)
    sum_gamma = np.zeros(len(X))
    Rloss = np.zeros(len(X))
    active_lengths = []
    for row in edges:
        u, v, gamma = int(row[0]), int(row[1]), float(row[2])
        chord = float(np.linalg.norm(X[u] - X[v]))
        ell = chord**2 / 2
        active_lengths.append(chord)
        for i in (u, v):
            degree[i] += 1
            sum_gamma[i] += gamma
            Rloss[i] += gamma * ell**2

    # Global node separation is bounded below by the minimum latitude gap or
    # the nearest-neighbor spacing on a ring.
    sep_candidates = [4 / 3]
    for ring in family.rings:
        theta = ring.t * h
        sep_candidates.append(2 * math.sin(theta) * math.sin(math.pi / ring.count) / h)
    for left, right in zip(family.rings, family.rings[1:]):
        sep_candidates.append(right.t - left.t)
    separation = min(sep_candidates)

    # Cover by the closest ring, then by the closest longitude; the pole cap
    # is covered directly by a pole.
    fill = 4 / 3
    for ring in family.rings:
        theta = ring.t * h
        half_cell = math.pi * math.sin(theta) / ring.count / h
        fill = max(fill, 0.5 + half_cell)

    rmax_h2 = float(np.max(sum_gamma / mu) * h**2)
    quotient_h2 = float(np.max(3 * Rloss / (2 * mu)) / h**2)
    return (
        separation,
        fill,
        min(active_lengths) / h,
        max(active_lengths) / h,
        float(np.max(degree)),
        rmax_h2,
        quotient_h2,
        float(np.min(mu) / h**2),
        float(np.min(weights) / h**2),
    )


def main() -> None:
    print("short-gap full-family row-class regression")
    print("M0 J rings nodes min-coeff H1 mixed isotropy unique-edge-ratio sep fill edge-window degree r*h2 D2/h2")
    for M0, J in ((32, 1), (32, 3), (64, 1), (64, 2)):
        family = build_orbits(M0, J)
        graph = expand(family)
        coeffs = [family.first_pole_conductance]
        coeffs += [x.conductance for x in family.interfaces]
        coeffs += [x for ring in family.rings for x in ring.horizontal if x]
        report = residual_report(graph)
        quality = quality_report(graph, family)
        print(
            M0,
            J,
            len(family.rings),
            len(graph["nodes"]),
            f"{min(coeffs):.4e}",
            *(f"{x:.3e}" for x in report),
            f"{quality[0]:.3e}",
            f"{quality[1]:.3e}",
            f"[{quality[2]:.3e},{quality[3]:.3e}]",
            int(quality[4]),
            f"{quality[5]:.3e}",
            f"{quality[6]:.3e}",
        )
        assert report[0] < 2e-10
        assert report[1] < 2e-8
        assert report[2] < 2e-8
        assert abs(report[3] - 1) < 1e-15
        assert quality[0] > 1 / (4 * M0)
        assert quality[1] < 2
        assert quality[2] > 1 / 8
        assert quality[3] < 5
        assert quality[4] <= M0
        assert quality[5] < 64 * math.pi**2
        assert quality[6] < 75 / 2
        assert quality[7] > 0 and quality[8] > 0

    # Mutations are deterministic failures, not alternative constructions.
    for mutation in ("equal_gap", "broken_column", "broken_m2"):
        failed = False
        try:
            mutated = build_orbits(32, 3, **{mutation: True})
            mutated_report = residual_report(expand(mutated))
            failed = max(mutated_report[:3]) > 1e-6
        except (ValueError, np.linalg.LinAlgError):
            failed = True
        assert failed, f"hostile mutation unexpectedly survived: {mutation}"

    # Reintroduce one q/h guard edge without re-solving its two adjacent
    # rows.  This is the exact schedule defect excluded by Section 1.
    guard = copy.deepcopy(build_orbits(32, 3))
    guard_index = next(i for i, ring in enumerate(guard.rings[:-1]) if ring.kind == "ordinary")
    guard.rings[guard_index + 1].t -= 0.01
    guard_report = residual_report(expand(guard))
    assert max(guard_report[:3]) > 1e-6
    print("hostile transition and q/h-guard mutations: deterministic failure PASS")


if __name__ == "__main__":
    main()
