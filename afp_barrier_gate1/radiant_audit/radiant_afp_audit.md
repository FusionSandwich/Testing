# Radiant AFP compatibility audit

- Timestamp (UTC): `2026-07-18T06:43:19.131`
- Radiant commit: `205e07faa105854b0f27e95a02f01ebed08f84c1`
- Julia: `1.10.11`
- Source balance target: `sum_j gamma_ij (Omega_j - Omega_i) = -2 w_i Omega_i`
- GitHub Actions run: `29634439040`
- Artifact digest: `sha256:3d395c99deb3cc73bcfb4c445a0f9425572994ccd7c4d4705e934e34f981ab81`

| Family | Order | Nodes | Edges | rank(Gamma) | weighted centroid | `||Gamma gamma-b2||inf` | `||Gamma gamma-b4||inf` | min gamma | negative gamma | max first-mode residual | min defect | max defect | min(rate*defect) | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| gauss-legendre-chebychev | 2 | 8 | 12 | 12 | 2.220e-16 | 8.882e-16 | 1.814e+00 | 1.571e+00 | 0 | 6.661e-16 | 1.333e+00 | 1.333e+00 | 4.000000 | PASS |
| gauss-legendre-chebychev | 3 | 18 | 30 | 30 | 6.106e-16 | 3.997e-15 | 1.862e+00 | 1.006e+00 | 0 | 4.219e-15 | 5.232e-01 | 8.783e-01 | 4.094840 | PASS |
| gauss-legendre-chebychev | 4 | 32 | 56 | 56 | 6.384e-16 | 1.610e-15 | 8.900e-01 | 9.029e-01 | 0 | 5.107e-15 | 2.676e-01 | 4.909e-01 | 4.013838 | PASS |
| carlson | 2 | 8 | 12 | 12 | 2.220e-16 | 4.441e-16 | 1.814e+00 | 1.571e+00 | 0 | 4.441e-16 | 1.333e+00 | 1.333e+00 | 4.000000 | PASS |
| carlson | 4 | 24 | 48 | 48 | 2.776e-16 | 2.831e-15 | 9.235e-01 | 8.418e-01 | 0 | 5.440e-15 | 5.206e-01 | 5.206e-01 | 4.092568 | PASS |
| carlson | 6 | 48 | 108 | 108 | 4.302e-16 | 2.456e-15 | 4.925e-01 | 4.237e-01 | 0 | 9.159e-15 | 2.452e-01 | 2.922e-01 | 4.015067 | PASS |
| lebedev | 3 | 6 | 12 | 12 | 0.000e+00 | 2.665e-15 | 4.189e+00 | 1.047e+00 | 0 | 1.332e-15 | 2.000e+00 | 2.000e+00 | 4.000000 | PASS |
| lebedev | 5 | 14 | 36 | 36 | 0.000e+00 | 3.775e-15 | 1.676e+00 | 3.142e-01 | 0 | 4.441e-15 | 8.453e-01 | 1.008e+00 | 4.000000 | PASS |
| lebedev | 7 | 26 | 72 | 72 | 5.551e-17 | 2.220e-15 | 1.197e+00 | 1.062e-01 | 0 | 4.219e-15 | 4.467e-01 | 6.247e-01 | 4.069365 | PASS |
| lebedev | 9 | 38 | 108 | 108 | 1.110e-16 | 1.443e-15 | 6.377e-01 | 5.346e-01 | 0 | 8.882e-15 | 2.239e-01 | 4.437e-01 | 4.000000 | PASS |

## Interpretation

All ten finite instances passed. In every case:

- the quadrature was weighted-centered to roundoff;
- the shared-edge equilibrium matrix had full column rank;
- Radiant's pseudoinverse coefficients were strictly positive;
- the current source code's `-2` coordinate balance residual was at roundoff;
- the `-4` diagnostic residual was macroscopically nonzero;
- the first-mode eigenrelation held to roundoff;
- the exact degree-two defect identity held to roundoff;
- the Lean-verified inequality `4 <= rate_i * defect_i` held at every node.

These are finite-instance certificates, not a proof for every order in an infinite quadrature family.
