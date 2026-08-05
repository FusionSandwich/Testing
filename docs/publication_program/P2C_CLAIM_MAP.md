# P2C claim map

| ID | Claim | Proof source | Executable source | Certificate / regression |
|---|---|---|---|---|
| C01 | raw moving-Gram block is equivalent to the full shell quotient | P2C Theorem 1 | pure_math/codesign/inner.py | singular-sampling pytest |
| C02 | fixed-candidate conductance design is a global SDP and attains | Theorem 2 | inner.py plus accepted P2A solver/verifier | P2A retained tests and independent verification |
| C03 | H0, reversibility, and nonnegative dissipation are exact | Section 1 edge identity | accepted P2A graph model | symbolic dense fixture and pytest |
| C04 | H1 implies the conductance trace identity | equation (5) | feasibility.py | symbolic and floating fixture audits |
| C05 | all eight requested family admissions have positive-mass and graph rules | Section 3 table | families.py | family-coverage and positivity tests |
| C06 | exactness through degree 2L gives condition one through shell L | Section 3 product-of-harmonics proof | metrics.py | icosahedral degree-two Gram test |
| C07 | local barycentric feasibility is not promoted to global feasibility | equation (6) and hostile boundary | metrics.py | global LP is a separate report field |
| C08 | a lifted minimizer exists on the compact graph of globally inner-optimal conductances | Theorem 3 | protected data structures/audits | compact-margin tests; analytic theorem, not finite proof |
| C09 | orbit formulation and inner value are jointly rotation invariant | Theorem 4 | rotations.py and intrinsic graphs | joint covariance regression |
| C10 | exact orbit proximal steps preserve feasibility and descend | Theorem 5 | outer.py finite-pool analogue | controller test; finite pool has narrower claim |
| C11 | accumulation points of the exact proximal scheme are limiting stationary | Theorem 5 | no finite run is labelled proof | analytic closed-graph proof |
| C12 | restored Riemannian Armijo has stationary cluster points under gates | Theorem 6 | feasibility.py and outer.py acceptance controller | nonsurjective-Jacobian hostile test |
| C13 | nonsmooth stationarity needs certified Clarke residuals | equation (11) | fail-closed controller contract | documentation sentinel and hostile audit |
| C14 | alternating blocks need tangent-frame coverage or a joint safeguard | Section 7 | AlternatingLedger | joint-safeguard state test |
| C15 | edge addition preserves feasibility and cannot worsen exact optimum | Theorem 7 | graph_updates.py | nontrivial zero-extension test |
| C16 | deletion is conditional, not automatic | Section 8 | deletion kernel checker and interval decisions | uncertified proposal rejection test |
| C17 | finite graph-orbit search terminates with no certified tau-improving unvisited proposal; exact neighborhood stationarity needs final-neighbor exclusion certificates | Section 8 | GraphSearchLedger | no-revisit and certified-gap tests |
| C18 | every positive centered rule has a globally compatible dense initializer | equations (14)–(15) | dense_centered_initializer | symbolic Lebedev-14 and icosahedral tests |
| C19 | adaptive identity is exact only against the enriched discrete reference | equations (16)–(17) | adaptive.py | exact linear-system regression |
| C20 | the accepted M0=2^80 P1B/P1E inner-optimal family has all-level quadratic order; M0=32,64 rows are finite regressions | Theorem 8 | convergence.py | symbolic constant product and explicitly finite benchmark |
| C21 | collision-fixed, joint covariance, streaming rays, and interpolation are separate | Section 12 | rotations.py | separate scope labels and tests |
| C22 | P1B does not lower-bound directional rotation spread | Section 12 scalar-defect argument | isotropic dense fixture | nonzero D2 with zero spread regression |
| C23 | rotation-net extrema need a Lipschitz enclosure | Section 12 | enclose_rotation_extrema | enclosure unit test |
| C24 | interpolation is audited as a separate streaming remedy | Section 12 | audit_rotation_interpolation | identity pass and moment-breaking rejection |
| C25 | no local outer global-optimality or whole-sequence claim is made | resolution and hostile boundaries | status labels | placeholder/overclaim scan |
| C26 | finite solver status is not an exact theorem certificate | Section 13 | Certification enum | exact audit is separate from floating audit |

## Certification ladder

1. **EXACT** — rational, algebraic, or symbolic identity.
2. **OUTWARD_INTERVAL** — outward-rounded enclosure proving the sign or inequality.
3. **VERIFIED_FLOAT** — independently reconstructed, scale-aware numerical candidate; suitable for regressions and explicitly computational deliverables.
4. **DIAGNOSTIC** — useful measurement without a proof label.
5. **REJECTED** — a gate failed or a required enclosure overlapped the decision boundary.

The all-orders rate in C20 is analytic.  Benchmark timings, memory, finite shell values, and finite rotation samples remain computational records.
