# P2C claim map

| ID | Canonical registry row | Claim | Proof source | Executable source | Certificate / regression |
|---|---|---|---|---|---|
| C01 | P2C-C01 | raw moving-Gram block is equivalent to the full shell quotient | P2C Theorem 1 | pure_math/codesign/inner.py | singular-sampling pytest |
| C02 | P2C-C02 | fixed-candidate conductance design is a global SDP and attains | Theorem 2 | inner.py plus accepted P2A solver/verifier | P2A retained tests and independent verification |
| C03 | P2C-C03 | H0, reversibility, and nonnegative dissipation are exact | Section 1 edge identity | accepted P2A graph model | symbolic dense fixture and pytest |
| C04 | P2C-C04 | H1 implies the conductance trace identity | equation (5) | feasibility.py | symbolic and floating fixture audits |
| C05 | P2C-C05 | all eight requested family admissions have positive-mass and graph rules | Section 3 table | families.py | family-coverage and positivity tests |
| C06 | P2C-C06 | exactness through degree 2L gives the continuum Gram through shell L, hence condition one after continuum whitening | Section 3 product-of-harmonics proof | metrics.py | icosahedral degree-two Gram test |
| C07 | P2C-C07 | local barycentric feasibility is not promoted to global feasibility | equation (6) and hostile boundary | metrics.py | global LP is a separate report field |
| C08 | P2C-C08 | a lifted minimizer exists on the compact optimizer graph under closed-graph/lower-hemicontinuity gates and uniform optimizer bounds derived from rates and positive epigraph costs | Theorem 3 | protected data structures/audits | compact-margin tests; analytic theorem, not finite proof |
| C09 | P2C-C09 | orbit formulation and intrinsic inner value are jointly rotation covariant; full response covariance is conditional on equivariant application co-rotation | Theorem 4 | rotations.py and intrinsic graphs | joint covariance regression |
| C10 | P2C-C10 | exact orbit proximal steps preserve feasibility and descend | Theorem 5 | outer.py finite-pool analogue | controller test; finite pool has narrower claim |
| C11 | P2C-C11 | accumulation points of the exact Euclidean proximal scheme are limiting stationary under neighborhood Lipschitzness and prox-regularity | Theorem 5 | no finite run is labelled proof | bounded-subgradient and closed-graph proof |
| C12 | P2C-C12 | restored Riemannian Armijo has stationary cluster points under gates | Theorem 6 | feasibility.py and outer.py acceptance controller | nonsurjective-Jacobian hostile test |
| C13 | P2C-C13 | nonsmooth stationarity needs certified Clarke residuals | equation (11) | fail-closed controller contract | documentation sentinel and hostile audit |
| C14 | P2C-C14 | alternating blocks need tangent-frame coverage or a joint safeguard | Section 7 | AlternatingLedger | joint-safeguard state test |
| C15 | P2C-C15 | edge addition preserves feasibility and cannot worsen exact optimum | Theorem 7 | graph_updates.py | nontrivial zero-extension test |
| C16 | P2C-C16 | deletion is conditional, not automatic | Section 8 | deletion kernel checker and interval decisions | uncertified proposal rejection test |
| C17 | P2C-C17 | finite graph-orbit search terminates with no certified tau-improving unvisited proposal; exact neighborhood stationarity needs final-neighbor exclusion certificates | Section 8 | GraphSearchLedger | no-revisit and certified-gap tests |
| C18 | P2C-C18 | every positive centered rule has a globally compatible dense initializer | equations (14)–(15) | dense_centered_initializer | symbolic Lebedev-14 and icosahedral tests |
| C19 | P2C-C19 | adaptive identity is exact only against the enriched discrete reference | equations (16)–(17) | adaptive.py | exact linear-system regression |
| C20 | P2C-C20 | the accepted M0=2^80 P1B/P1E inner-optimal family has all-level quadratic order; M0=32,64 rows are finite regressions | Theorem 8 | convergence.py | symbolic constant product and explicitly finite benchmark |
| C21 | P2C-C21 | collision-fixed, joint covariance, streaming rays, and interpolation are separate | Section 12 | rotations.py | separate scope labels and tests |
| C22 | P2C-C22 | P1B does not lower-bound directional rotation spread | Section 12 scalar-defect argument | isotropic dense fixture | nonzero D2 with zero spread regression |
| C23 | P2C-C23 | rotation-net extrema need a Lipschitz enclosure | Section 12 | enclose_rotation_extrema | enclosure unit test |
| C24 | P2C-C24 | interpolation is audited as a separate streaming remedy | Section 12 | audit_rotation_interpolation | identity pass and moment-breaking rejection |
| C25 | P2C-C25 | no local outer global-optimality or whole-sequence claim is made | resolution and hostile boundaries | status labels | placeholder/overclaim scan |
| C26 | P2C-C26 | finite solver status is not an exact theorem certificate | Section 13 | Certification enum | exact audit is separate from floating audit |
| C27 | P2C-C27 | the executable AB admission path expands the full 60-element proper icosahedral group, handles stabilizers, rejects duplicate orbits, and audits positive masses and declared harmonic exactness | Section 3 and independent audit | families.py | group/order/closure and fail-closed orbit-adapter tests |
| C28 | P2C-C28 | stable P2C finite algebra has a dedicated Lean kernel and focused axiom audit | Section 13 and formal boundary | AFPBarrier/QuadratureGeneratorCodesign.lean | P2CAxiomAudit plus no-sorry/no-local-axiom gate |
| C29 | P2C-C29 | the completed descendant publication chain preserves the historical archive and creates a new archive only under an absent-ref lease; carriage returns and other control bytes fail | formal/release audit | dedicated P2C workflow | exact ref and source-byte gates |

## Certification ladder

1. **EXACT** — rational, algebraic, or symbolic identity.
2. **OUTWARD_INTERVAL** — outward-rounded enclosure proving the sign or inequality.
3. **VERIFIED_FLOAT** — independently reconstructed, scale-aware numerical candidate; suitable for regressions and explicitly computational deliverables.
4. **DIAGNOSTIC** — useful measurement without a proof label.
5. **REJECTED** — a gate failed or a required enclosure overlapped the decision boundary.

The all-orders rate in C20 is analytic.  Benchmark timings, memory, finite shell values, and finite rotation samples remain computational records.
