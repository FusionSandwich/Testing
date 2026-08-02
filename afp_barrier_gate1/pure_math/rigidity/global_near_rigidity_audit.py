#!/usr/bin/env python3
"""Deterministic algebra and stress audit for Prompt 3 near-rigidity.

This is regression evidence, not the all-orders proof.  The ordinary proof is
in GLOBAL_Q_RIGIDITY_THEOREM.md and the finite algebra core is mirrored in Lean.
All calculations here are deterministic and use exact rationals or high-
precision arithmetic with explicit margins.
"""
from __future__ import annotations

from fractions import Fraction
import itertools
import json
import math
from typing import Iterable

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 100


def assert_close(x: mp.mpf, y: mp.mpf, tol: mp.mpf = mp.mpf("1e-70")) -> None:
    if abs(x - y) > tol:
        raise AssertionError(f"{x!r} != {y!r} within {tol}")


def exact_variance_identity() -> dict[str, str]:
    p = [Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)]
    x = [Fraction(1, 2), Fraction(5, 4), Fraction(17, 16)]
    # Replace the last entry so the p-weighted mean is exactly one.
    x[-1] = (Fraction(1) - p[0] * x[0] - p[1] * x[1]) / p[2]
    mean = sum(pi * xi for pi, xi in zip(p, x))
    q = sum(pi * xi * xi for pi, xi in zip(p, x))
    var = sum(pi * (xi - 1) ** 2 for pi, xi in zip(p, x))
    assert mean == 1
    assert q - 1 == var
    return {"mean": str(mean), "Q_minus_1": str(q - 1), "variance": str(var)}


def pointwise_and_path_stress() -> dict[str, float | int]:
    worst_ratio_slack = math.inf
    worst_log_slack = math.inf
    tested = 0
    for kappa in (0.5, 0.2, 0.05, 0.01):
        for eta in (1e-12, 1e-8, 1e-5, 1e-3):
            delta = math.sqrt(eta / kappa)
            if delta >= 0.9:
                continue
            q = (1 + delta) / (1 - delta)
            s = math.log(q)
            # Adversarial alternating endpoint scales saturate the local bounds.
            for n in (1, 2, 5, 25, 100):
                rates = [1.0]
                for step in range(n):
                    rates.append(rates[-1] * (q if step % 2 == 0 else 1 / q))
                for i in range(len(rates)):
                    for j in range(len(rates)):
                        d = abs(i - j)
                        ratio = rates[i] / rates[j]
                        upper = q**d
                        lower = q ** (-d)
                        worst_ratio_slack = min(worst_ratio_slack, upper - ratio, ratio - lower)
                        worst_log_slack = min(
                            worst_log_slack,
                            d * s - abs(math.log(rates[i]) - math.log(rates[j])),
                        )
                        if ratio > upper * (1 + 1e-12) or ratio < lower * (1 - 1e-12):
                            raise AssertionError("pathwise rate bound failed")
                        tested += 1
    return {
        "cases": tested,
        "minimum_ratio_slack": worst_ratio_slack,
        "minimum_log_slack": worst_log_slack,
    }


def effective_resistance(C: sp.Matrix, i: int, j: int) -> sp.Rational:
    """Exact effective resistance for symmetric conductance matrix C.

    C[i,j] is the undirected edge conductance, diagonal entries are ignored.
    The energy convention is sum_{i<j} C_ij (v_i-v_j)^2.
    """
    n = C.rows
    L = sp.zeros(n)
    for a in range(n):
        for b in range(a + 1, n):
            c = sp.Rational(C[a, b])
            L[a, a] += c
            L[b, b] += c
            L[a, b] -= c
            L[b, a] -= c
    # Ground vertex j and solve L v = e_i-e_j.
    keep = [k for k in range(n) if k != j]
    Lg = L.extract(keep, keep)
    rhs = sp.Matrix([1 if k == i else 0 for k in keep])
    sol = Lg.LUsolve(rhs)
    vi = sol[keep.index(i)] if i != j else sp.Rational(0)
    return sp.factor(vi)


def markov_energy_audit() -> dict[str, str | int]:
    # Reversible path with deliberately nonuniform stationary measure.
    n = 6
    edge = [sp.Rational(1, 20), sp.Rational(1, 15), sp.Rational(1, 12),
            sp.Rational(1, 10), sp.Rational(1, 8)]
    C = sp.zeros(n)
    for i, c in enumerate(edge):
        C[i, i + 1] = C[i + 1, i] = c
    # Add holding mass implicitly; only edge conductances enter E and R_eff.
    u = sp.Matrix([sp.Rational(0), sp.Rational(1, 20), sp.Rational(-1, 10),
                   sp.Rational(1, 5), sp.Rational(-1, 4), sp.Rational(3, 10)])
    energy = sum(C[i, j] * (u[i] - u[j]) ** 2
                 for i in range(n) for j in range(i + 1, n))
    r05 = effective_resistance(C, 0, 5)
    assert sp.factor((u[0] - u[5]) ** 2 - r05 * energy) <= 0
    # On a path resistance is the sum of reciprocal conductances.
    expected = sum(1 / c for c in edge)
    assert sp.factor(r05 - expected) == 0
    return {
        "vertices": n,
        "energy": str(sp.factor(energy)),
        "R_eff_0_5": str(r05),
        "endpoint_bound_slack": str(sp.factor(r05 * energy - (u[0] - u[5]) ** 2)),
    }


def arc_conversion_audit() -> dict[str, float]:
    ell_lo = mp.mpf("0.35")
    ell_hi = mp.mpf("1.65")
    sigma = min(mp.sqrt(ell_lo * (2 - ell_lo)), mp.sqrt(ell_hi * (2 - ell_hi)))
    max_ratio = mp.mpf("0")
    for a_int in range(351, 1650, 17):
        a = mp.mpf(a_int) / 1000
        for b_int in range(351, 1650, 31):
            b = mp.mpf(b_int) / 1000
            lhs = abs(mp.acos(1 - a) - mp.acos(1 - b))
            rhs = abs(a - b) / sigma
            if lhs > rhs + mp.mpf("1e-80"):
                raise AssertionError("arccos Lipschitz bound failed")
            if a != b:
                max_ratio = max(max_ratio, lhs / abs(a - b))
    return {"sigma_arc": float(sigma), "max_observed_derivative": float(max_ratio)}


def spherical_angle(a: mp.mpf, b: mp.mpf, c: mp.mpf) -> mp.mpf:
    z = (mp.cos(a) - mp.cos(b) * mp.cos(c)) / (mp.sin(b) * mp.sin(c))
    z = min(mp.mpf(1), max(mp.mpf(-1), z))
    return mp.acos(z)


def angle_derivative_audit() -> dict[str, float]:
    theta = mp.acos(mp.mpf(1) / mp.sqrt(5))
    d = mp.mpf("0.002")
    lo, hi = theta - d, theta + d
    s_theta = min(mp.sin(lo), mp.sin(hi))
    # Certified interval-style cosine enclosure from endpoint arithmetic.
    c_lo, c_hi = mp.cos(hi), mp.cos(lo)
    products = [c_lo * c_lo, c_lo * c_hi, c_hi * c_hi]
    n_lo = c_lo - max(products)
    n_hi = c_hi - min(products)
    quotients = [n_lo, n_hi, n_lo / (s_theta**2), n_hi / (s_theta**2)]
    c_abs = max(abs(x) for x in quotients)
    if not c_abs < 1:
        raise AssertionError("angle sine enclosure is not nondegenerate")
    s_A = mp.sqrt(1 - c_abs**2)
    C_ang = 1 / (s_A * s_theta**2) + 4 / (s_A * s_theta**3)

    # Check analytic partial derivatives against finite differences and C_ang.
    max_sum = mp.mpf(0)
    eps = mp.mpf("1e-25")
    for a in (lo, theta, hi):
        for b in (lo, theta, hi):
            for c in (lo, theta, hi):
                A = spherical_angle(a, b, c)
                partials = []
                for idx in range(3):
                    args_p = [a, b, c]
                    args_m = [a, b, c]
                    args_p[idx] += eps
                    args_m[idx] -= eps
                    partials.append((spherical_angle(*args_p) - spherical_angle(*args_m)) / (2 * eps))
                total = sum(abs(x) for x in partials)
                max_sum = max(max_sum, total)
                if total > C_ang:
                    raise AssertionError("C_ang derivative bound failed")
                if not (0 < A < mp.pi):
                    raise AssertionError("angle left nondegenerate domain")
    return {
        "s_theta": float(s_theta),
        "s_A": float(s_A),
        "C_ang": float(C_ang),
        "max_observed_gradient_l1": float(max_sum),
    }


def platonic_and_valence_constants() -> dict[str, object]:
    qrows: dict[int, dict[str, str]] = {}
    for q in (3, 4, 5):
        alpha = 2 * sp.pi / q
        c_alpha = sp.simplify(sp.cos(alpha))
        c_theta = sp.simplify(c_alpha / (1 - c_alpha))
        ell = sp.simplify(1 - c_theta)
        rate = sp.simplify(2 / ell)
        V = sp.Rational(12, 6 - q)
        E = q * V / 2
        F = 2 * E / 3
        assert sp.simplify(V - E + F) == 2
        qrows[q] = {
            "V": str(V), "E": str(E), "F": str(F),
            "cos_theta": str(c_theta), "ell": str(ell), "rate": str(rate),
        }

    # Exact valence separation for representative kappa values.
    gaps = {}
    for kappa in (sp.Rational(1, 3), sp.Rational(1, 5), sp.Rational(1, 12)):
        dmax = int(sp.floor(1 / kappa))
        vals = [2 * sp.pi / m for m in range(3, dmax + 1)]
        if len(vals) <= 1:
            gap = sp.oo
        else:
            gap = min(abs(vals[i] - vals[j]) for i in range(len(vals)) for j in range(i + 1, len(vals)))
        gaps[str(kappa)] = str(sp.simplify(gap))
    return {"platonic_rows": qrows, "valence_gaps": gaps}


def alpha_eq_derivative_audit() -> dict[str, float]:
    def alpha_eq(t: mp.mpf) -> mp.mpf:
        return mp.acos(mp.cos(t) / (1 + mp.cos(t)))

    def derivative(t: mp.mpf) -> mp.mpf:
        a = alpha_eq(t)
        return mp.sin(t) / ((1 + mp.cos(t)) ** 2 * mp.sin(a))

    lo = mp.mpf("0.8")
    hi = mp.mpf("1.9")  # strictly below 2*pi/3
    if not hi < 2 * mp.pi / 3:
        raise AssertionError
    min_deriv = min(derivative(lo + (hi - lo) * k / 1000) for k in range(1001))
    sJ = min(mp.sin(lo), mp.sin(hi))
    conservative = sJ / 4
    if min_deriv < conservative:
        raise AssertionError("explicit m_eq lower bound failed")
    # Finite-difference formula audit.
    t = mp.mpf("1.2")
    h = mp.mpf("1e-30")
    fd = (alpha_eq(t + h) - alpha_eq(t - h)) / (2 * h)
    assert_close(fd, derivative(t), mp.mpf("1e-55"))
    return {
        "interval_lo": float(lo), "interval_hi": float(hi),
        "observed_inf": float(min_deriv), "certified_lower_sJ_over_4": float(conservative),
    }


def main() -> None:
    report = {
        "variance_identity": exact_variance_identity(),
        "path_stress": pointwise_and_path_stress(),
        "resistance": markov_energy_audit(),
        "arc_conversion": arc_conversion_audit(),
        "angle_derivatives": angle_derivative_audit(),
        "platonic_constants": platonic_and_valence_constants(),
        "equilateral_derivative": alpha_eq_derivative_audit(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
