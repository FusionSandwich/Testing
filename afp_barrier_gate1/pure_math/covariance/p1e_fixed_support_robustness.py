#!/usr/bin/env python3
"""Fixed-support reflected-latitude solver used by the Proposition 7.3 audit.

This module is a finite regression surface for the analytic fixed-level theorem.
It keeps the ring counts, longitude phases, masks, horizontal jumps, pole,
equator, and reflection fixed, and re-solves the exact row moment equations.
It is not an all-level numerical proof and it does not emit a production
perturbation radius.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from p1e_short_gap_family_audit import (
    Family,
    Interface,
    Ring,
    mask,
    mask_moments,
    row_matrix,
)


@dataclass
class FixedSupportSolution:
    h: float
    theta: list[float]
    rings: list[Ring]
    interfaces: list[Interface]
    first_pole_conductance: float


def _solve_three(R: np.ndarray, incoming: float) -> tuple[float, float, float]:
    A = R[:, (0, 2, 3)]
    z = np.linalg.solve(A, -incoming * R[:, 1])
    if not np.all(np.isfinite(z)) or float(np.min(z)) <= 0:
        raise ValueError("fixed-support row lost positivity")
    return tuple(map(float, z))


def solve_fixed_support(base: Family, latitude_delta: Sequence[float]) -> FixedSupportSolution:
    """Re-solve one fixed finite support after reflected latitude perturbation.

    ``latitude_delta`` has one value for every northern ring.  The equator is
    required to remain fixed.  South is supplied by reflection.  The pole
    conductance is the scale gauge and remains equal to its base value.
    """

    if len(latitude_delta) != len(base.rings):
        raise ValueError("one perturbation is required for every northern ring")
    if abs(float(latitude_delta[-1])) > 1e-15:
        raise ValueError("the equator is fixed")

    theta = [r.t * base.h + float(d) for r, d in zip(base.rings, latitude_delta)]
    if not (0.0 < theta[0] and abs(theta[-1] - math.pi / 2) < 1e-12):
        raise ValueError("pole/equator boundary violated")
    if any(not (a < b) for a, b in zip(theta, theta[1:])):
        raise ValueError("latitude order or meridional gap was lost")

    rings = copy.deepcopy(base.rings)
    interfaces: list[Interface] = []
    incoming = float(base.first_pole_conductance)
    i = 0
    while i < len(rings):
        ring = rings[i]
        current = theta[i]
        delta = 2 * math.pi / ring.count
        h_minus = current if i == 0 else current - theta[i - 1]

        if ring.kind == "equator":
            jump = ring.jumps[0]
            if jump <= 0 or math.sin(jump * delta) == 0:
                raise ValueError("equatorial covariance coefficient vanished")
            H = incoming * math.sin(h_minus) ** 2 / math.sin(jump * delta) ** 2
            if H <= 0 or not math.isfinite(H):
                raise ValueError("equatorial solve lost positivity")
            ring.horizontal = (float(H), 0.0)
            break

        h_plus = theta[i + 1] - current
        if ring.kind in {"first", "ordinary"}:
            R = row_matrix(
                current,
                h_minus,
                h_plus,
                (0.0, 0.0),
                (0.0, 0.0),
                delta,
                ring.jumps,
            )
            outgoing, h1, h2 = _solve_three(R, incoming)
            ring.horizontal = (h1, h2)
            interfaces.append(Interface(i, "aligned", outgoing))
            incoming = outgoing
        elif ring.kind == "transition_coarse":
            fine = rings[i + 1]
            fine_theta = theta[i + 1]
            if i + 2 >= len(rings):
                raise ValueError("transition fine endpoint has no outgoing ring")
            fine_h_plus = theta[i + 2] - fine_theta
            moments = mask_moments(ring.count)
            Rc = row_matrix(
                current,
                h_minus,
                h_plus,
                (0.0, 0.0),
                moments,
                delta,
                ring.jumps,
            )
            Rf = row_matrix(
                fine_theta,
                h_plus,
                fine_h_plus,
                moments,
                (0.0, 0.0),
                2 * math.pi / fine.count,
                fine.jumps,
            )
            A = np.zeros((6, 6))
            b = np.zeros(6)
            A[:3, 0], A[:3, 2], A[:3, 3] = Rc[:, 0], Rc[:, 2], Rc[:, 3]
            b[:3] = -incoming * Rc[:, 1]
            A[3:, 0], A[3:, 1] = 0.5 * Rf[:, 1], Rf[:, 0]
            A[3:, 4], A[3:, 5] = Rf[:, 2], Rf[:, 3]
            z = np.linalg.solve(A, b)
            if not np.all(np.isfinite(z)) or float(np.min(z)) <= 0:
                raise ValueError("fixed-support transition lost positivity")
            uq, outgoing, hc1, hc8, hf1, hf8 = map(float, z)
            ring.horizontal = (hc1, hc8)
            fine.horizontal = (hf1, hf8)
            interfaces.append(Interface(i, "transition", uq, ring.count))
            interfaces.append(Interface(i + 1, "aligned", outgoing))
            incoming = outgoing
            i += 1
        elif ring.kind == "transition_fine":
            raise AssertionError("fine transition endpoint must be consumed with coarse endpoint")
        else:
            raise AssertionError(ring.kind)
        i += 1

    coefficients = [base.first_pole_conductance]
    coefficients.extend(x.conductance for x in interfaces)
    coefficients.extend(x for r in rings for x in r.horizontal if x)
    if not coefficients or min(coefficients) <= 0:
        raise ValueError("fixed-support solution is not strictly positive")
    if len(interfaces) != len(rings) - 1:
        raise ValueError("fixed support did not produce one meridional interface per gap")
    return FixedSupportSolution(base.h, theta, rings, interfaces, base.first_pole_conductance)


def expand_fixed_support(solution: FixedSupportSolution) -> dict[str, object]:
    """Expand the fixed orbit support to literal nodes and shared edges."""

    rings = solution.rings
    nrings = len(rings)
    nodes: list[np.ndarray] = [np.array([0.0, 0.0, 1.0])]
    north_ids: list[list[int]] = []
    south_ids: list[list[int] | None] = []

    for theta, ring in zip(solution.theta, rings):
        ids = []
        for j in range(ring.count):
            phi = 2 * math.pi * j / ring.count
            ids.append(len(nodes))
            nodes.append(np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)]))
        north_ids.append(ids)
    for ri, (theta, ring) in enumerate(zip(solution.theta, rings)):
        if ri == nrings - 1:
            south_ids.append(None)
            continue
        ids = []
        reflected = math.pi - theta
        for j in range(ring.count):
            phi = 2 * math.pi * j / ring.count
            ids.append(len(nodes))
            nodes.append(np.array([math.sin(reflected) * math.cos(phi), math.sin(reflected) * math.sin(phi), math.cos(reflected)]))
        south_ids.append(ids)
    south_pole = len(nodes)
    nodes.append(np.array([0.0, 0.0, -1.0]))

    edges: list[tuple[int, int, float]] = []

    def horizontal(ids: list[int], ring: Ring) -> None:
        for jump, conductance in zip(ring.jumps, ring.horizontal):
            if jump <= 0 or conductance <= 0:
                continue
            for j in range(ring.count):
                edges.append((ids[j], ids[(j + jump) % ring.count], float(conductance)))

    for ri, ring in enumerate(rings):
        horizontal(north_ids[ri], ring)
        if south_ids[ri] is not None:
            horizontal(south_ids[ri] or [], ring)
    for j in north_ids[0]:
        edges.append((0, j, solution.first_pole_conductance))
    for j in south_ids[0] or []:
        edges.append((south_pole, j, solution.first_pole_conductance))

    def add_interface(lower: list[int], upper: list[int], interface: Interface) -> None:
        if interface.kind == "aligned":
            if len(lower) != len(upper):
                raise ValueError("aligned support count changed")
            edges.extend((u, v, float(interface.conductance)) for u, v in zip(lower, upper))
        else:
            M = interface.coarse_count
            if len(lower) != M or len(upper) != 2 * M:
                raise ValueError("transition support count changed")
            for k in range(M):
                for offset, weight in mask(M):
                    edges.append((lower[k], upper[(2 * k + offset) % (2 * M)], float(interface.conductance * weight)))

    for ri, interface in enumerate(solution.interfaces):
        add_interface(north_ids[ri], north_ids[ri + 1], interface)
        lower_s = south_ids[ri] or []
        upper_s = north_ids[-1] if south_ids[ri + 1] is None else (south_ids[ri + 1] or [])
        add_interface(lower_s, upper_s, interface)

    X = np.asarray(nodes)
    E = np.asarray(edges, dtype=float)
    mu = np.zeros(len(X))
    for u_f, v_f, gamma in E:
        u, v = int(u_f), int(v_f)
        ell = 1 - float(X[u] @ X[v])
        mu[u] += 0.5 * gamma * ell
        mu[v] += 0.5 * gamma * ell
    if float(np.min(mu)) <= 0:
        raise ValueError("stationary mass lost positivity")
    return {"h": solution.h, "nodes": X, "edges": E, "mu": mu, "weights": mu / mu.sum()}


def exactness_report(graph: dict[str, object]) -> dict[str, float]:
    """Return scale-free H1, loss-force, isotropy, rate and defect diagnostics."""

    X = graph["nodes"]
    E = graph["edges"]
    mu = graph["mu"]
    h = float(graph["h"])
    assert isinstance(X, np.ndarray) and isinstance(E, np.ndarray) and isinstance(mu, np.ndarray)
    force = np.zeros_like(X)
    mixed = np.zeros_like(X)
    cov = np.zeros((len(X), 3, 3))
    sum_gamma = np.zeros(len(X))
    R = np.zeros(len(X))
    edge_lengths: list[float] = []
    for u_f, v_f, gamma in E:
        u, v = int(u_f), int(v_f)
        chord = float(np.linalg.norm(X[u] - X[v]))
        edge_lengths.append(chord)
        ell = chord * chord / 2
        for i, j in ((u, v), (v, u)):
            diff = X[j] - X[i]
            tangent = diff + ell * X[i]
            force[i] += gamma * diff
            mixed[i] += gamma * ell * tangent
            cov[i] += gamma * np.outer(tangent, tangent)
            sum_gamma[i] += gamma
            R[i] += gamma * ell * ell
    h1 = float(np.max(np.linalg.norm(force + 2 * mu[:, None] * X, axis=1) / mu))
    loss_force = float(np.max(np.linalg.norm(mixed, axis=1) / (mu * h * h)))
    isotropy = 0.0
    for i, x in enumerate(X):
        P = np.eye(3) - np.outer(x, x)
        T = P @ cov[i] @ P
        isotropy = max(isotropy, float(np.linalg.norm(T - np.trace(T) * P / 2) / (mu[i] * h * h)))
    rate_h2 = float(np.max(sum_gamma / mu) * h * h)
    defect_h2 = float(np.max(3 * R / (2 * mu)) / (h * h))
    return {
        "h1": h1,
        "loss_force": loss_force,
        "isotropy": isotropy,
        "edge_min_over_h": min(edge_lengths) / h,
        "edge_max_over_h": max(edge_lengths) / h,
        "rate_h2": rate_h2,
        "defect_over_h2": defect_h2,
    }


def rotate_graph(graph: dict[str, object], Q: np.ndarray) -> dict[str, object]:
    """Apply one common ambient rotation while retaining the exact graph."""

    if Q.shape != (3, 3) or not np.allclose(Q.T @ Q, np.eye(3), atol=1e-12) or np.linalg.det(Q) < 0:
        raise ValueError("Q must be a proper orthogonal 3x3 matrix")
    out = dict(graph)
    X = graph["nodes"]
    assert isinstance(X, np.ndarray)
    out["nodes"] = X @ Q.T
    return out
