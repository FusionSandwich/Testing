#!/usr/bin/env python3
"""Exact symbolic audit of the icosphere bulk scalar-factor obstruction."""

from __future__ import annotations

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    r0, t, kappa = sp.symbols("r0 t kappa", positive=True)
    r2 = r0**2 + t**2

    # Ambient basis is (e1,e2,n).  C=kappa*P_U and the tangent basis at
    # y=r0*n+t*e1 is (e2, (r0*e1-t*n)/sqrt(r2)).
    C = sp.diag(kappa, kappa, 0)
    e2 = sp.Matrix([0, 1, 0])
    z = sp.Matrix([r0, 0, -t]) / sp.sqrt(r2)
    gram = sp.Matrix(
        [
            [(e2.T * C * e2)[0], (e2.T * C * z)[0]],
            [(z.T * C * e2)[0], (z.T * C * z)[0]],
        ]
    ).applyfunc(sp.simplify)
    expected = sp.diag(kappa, kappa * r0**2 / r2)
    require(gram == expected, "tangent covariance eigenvalues")

    tracefree = sp.simplify(gram - sp.trace(gram) * sp.eye(2) / 2)
    frobenius_sq = sp.simplify(sp.trace(tracefree.T * tracefree))
    expected_sq = sp.simplify(kappa**2 * t**4 / (2 * r2**2))
    require(sp.simplify(frobenius_sq - expected_sq) == 0, "trace-free norm")

    sqrt5 = sp.sqrt(5)
    ico_r0_sq = sp.simplify((1 + 2 / sqrt5) / 3)
    require(ico_r0_sq > 0, "icosahedral face inradius is positive")
    ico_residual_sq = sp.simplify(expected_sq.subs(r0**2, ico_r0_sq))
    require(ico_residual_sq != 0, "off-barycenter residual is nonzero")

    # Forced continuum tensor: divergence-free, and equal to curl--curl of
    # phi=K*sqrt(r0^2+x^2+y^2)/r0^2.
    x, y, K = sp.symbols("x y K", real=True, positive=True)
    radius = sp.sqrt(r0**2 + x**2 + y**2)
    u = sp.Matrix([x, y])
    continuum = sp.simplify(
        K / radius**3 * (sp.eye(2) + (u * u.T) / r0**2)
    )
    divergence = sp.Matrix(
        [
            sp.diff(continuum[i, 0], x) + sp.diff(continuum[i, 1], y)
            for i in range(2)
        ]
    ).applyfunc(sp.simplify)
    require(divergence == sp.zeros(2, 1), "forced tensor divergence")

    phi = K * radius / r0**2
    curlcurl_phi = sp.Matrix(
        [
            [sp.diff(phi, y, 2), -sp.diff(phi, x, y)],
            [-sp.diff(phi, x, y), sp.diff(phi, x, 2)],
        ]
    ).applyfunc(sp.simplify)
    require(
        (curlcurl_phi - continuum).applyfunc(sp.simplify) == sp.zeros(2),
        "Airy representation",
    )
    rho_bulk = (sqrt5 - 1) / (2 * sqrt5 + 1)
    eta_bulk = sp.sqrt(3) / 2 - rho_bulk
    require(eta_bulk > sp.Rational(1, 2), "bulk tensor cone margin")

    print("p1e icosphere bulk formula obstruction audit: PASS")
    print(f"tangent covariance = {gram}")
    print(f"tracefree Frobenius norm^2 = {expected_sq}")
    print(f"icosahedral specialization = {ico_residual_sq}")
    print("forced continuum tensor divergence and Airy identity: PASS")
    print(f"exact bulk cone margin = {eta_bulk}")


if __name__ == "__main__":
    main()
