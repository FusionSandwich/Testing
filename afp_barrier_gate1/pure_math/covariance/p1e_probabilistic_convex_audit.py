#!/usr/bin/env python3
"""Deterministic checks for the P1E probabilistic/convex no-go audit."""

from __future__ import annotations

import math

import numpy as np


def covariance_identity(n: int, m: int, trials: int, seed: int) -> tuple[float, float]:
    """Monte Carlo falsification check for E||n/m sum uu^T-I||_F^2."""
    rng = np.random.default_rng(seed)
    accum = 0.0
    eye = np.eye(n)
    for _ in range(trials):
        u = rng.normal(size=(m, n))
        u /= np.linalg.norm(u, axis=1)[:, None]
        q = (n / m) * (u.T @ u) - eye
        accum += float(np.sum(q * q))
    empirical = accum / trials
    exact = n * (n - 1) / m
    return empirical, exact


def adjoint_identity_fixture(dim: int, trials: int, seed: int) -> float:
    """Check the exact shared-force adjoint identity on random unit pairs."""
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(trials):
        x = rng.normal(size=dim)
        x /= np.linalg.norm(x)
        y = rng.normal(size=dim)
        y /= np.linalg.norm(y)
        a = rng.normal(size=dim)
        px = np.eye(dim) - np.outer(x, x)
        py = np.eye(dim) - np.outer(y, y)
        tauxy = px @ y
        tauyx = py @ x
        lhs = (px @ a) @ tauxy + (py @ a) @ tauyx
        ell = 1.0 - x @ y
        rhs = ell * (a @ (x + y))
        worst = max(worst, abs(float(lhs - rhs)))
    return worst


def alternating_gap_ratio(rho: float, s: float) -> float:
    alpha = s * (1.0 + rho)
    beta = s * (1.0 - rho)
    c = math.cos(alpha / 2.0) * math.cos(beta / 2.0)
    aa = 4.0 * (1.0 - math.cos(rho * s) * c)
    bb = -4.0 * c * math.sin(rho * s)
    return math.hypot(aa, bb) / s


def gordan_certificate(alpha: float, beta: float) -> tuple[float, float]:
    """Return the two strictly positive works in Proposition 3.1."""
    assert 0.0 < beta < alpha < math.pi
    ell_alpha = 1.0 - math.cos(alpha)
    ell_beta = 1.0 - math.cos(beta)
    midpoint = (ell_alpha + ell_beta) / 2.0
    work_right = math.sin(alpha) * (-midpoint + ell_alpha)
    work_left = -math.sin(beta) * (-midpoint + ell_beta)
    return work_right, work_left


def main() -> None:
    covariance_cases = 0
    for n in (2, 3, 5):
        for m in (8, 32, 128):
            empirical, exact = covariance_identity(n, m, 20_000, 1100 + 17 * n + m)
            # A numerical stress test only; the exact derivation is in the audit.
            assert abs(empirical - exact) <= 0.045 * exact + 2e-3
            covariance_cases += 1

    adjoint_cases = 0
    for dim in (2, 3, 6):
        err = adjoint_identity_fixture(dim, 500, 2300 + dim)
        assert err < 2e-14
        adjoint_cases += 1

    gap_cases = 0
    for rho in (0.1, 0.35, 0.8):
        ratios = [alternating_gap_ratio(rho, 2.0 ** (-k)) for k in range(8, 16)]
        assert abs(ratios[-1] - 4.0 * rho) < 2e-4
        assert abs(ratios[-1] - 4.0 * rho) < abs(ratios[0] - 4.0 * rho)
        for s in (0.2, 0.05, 0.01):
            right, left = gordan_certificate(s * (1.0 + rho), s * (1.0 - rho))
            assert right > 0.0 and left > 0.0
        gap_cases += 1

    print("P1E probabilistic/convex audit: PASS")
    print(f"covariance fixtures: {covariance_cases}")
    print(f"adjoint fixtures: {adjoint_cases}")
    print(f"alternating-gap fixtures: {gap_cases}")


if __name__ == "__main__":
    main()
