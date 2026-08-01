# AFP mathematical claim matrix

This document controls publication wording for the pure-mathematics track.
Statuses are deliberately conservative. `PROVED ordinary` means the complete
finite proof is written in the repository; it does not imply full Lean
formalization.

| Claim | Status | Current support | Publication treatment |
|---|---|---|---|
| Finite jump generators satisfy the carré-du-champ square identity | PROVED / standard | Lean module `JumpGenerator.lean`; standard Markov-generator algebra | Foundational lemma only |
| `lambda^2 <= rate * peakDefect` | PROVED / standard | Lean modules `Quantitative.lean` and `LossVariance*.lean` | Foundational weighted Cauchy–Schwarz lemma |
| The gap equals a weighted edge-loss variance | PROVED | Lean module `LossVariance.lean` | Foundational sharpness identity |
| A finite positive conservative generator cannot reproduce the complete degree-one and complete degree-two spherical eigenspaces exactly | PROVED in the stated AFP formulation | Lean algebraic core plus spherical specialization | Candidate AFP-specific corollary; priority still requires specialist review |
| A centered positive quadrature admits a dense positive reversible degree-one-exact operator | PROVED | `CompleteGraph.lean`; `pure_math/SHARED_EDGE_CONE_FARKAS.md` | Supporting construction |
| Positive spherical Delaunay families attain the natural `h^-2` rate scale | EXTERNAL specialization | Published spherical Delaunay Laplacian theory plus project loss bounds | Cite as achievability input, not as an original construction |
| The project’s quasi-uniform family is globally minimax or spectrally optimal | CONJECTURE / unsupported | No global minimax theorem | Do not claim |
| Only `K in {4,6,12}` can have global `Q=1` | REJECTED | Cube (`K=8`) and dodecahedron (`K=20`) are counterexamples | Never state without new restrictive assumptions |
| Connected reversible `Q=1` graphs have one common active-edge loss and one common row rate | CONJECTURE with complete proof target | Follows from local equality plus shared-edge propagation; formalization active | Intended first global rigidity lemma |
| Only tetrahedral, octahedral, and icosahedral spherical triangulations can satisfy global `Q=1` under strict equal-edge hypotheses | CONJECTURE | Plausible only after explicit triangulation, positivity, and embedding assumptions | Counterexample search before proof |
| Non-antipodal local nonnegative degree-one feasibility is equivalent to `0` lying in the indexed tangent convex hull | PROVED ordinary; finite scaling formalized | `pure_math/SPHERICAL_LOCAL_EXACT.md`; `LocalSphericalFeasibility.lean`; exact regressions | Central sphere-specific local theorem, but convex membership itself is standard |
| Strict positivity on every permitted non-antipodal edge is equivalent to relative-interior membership in the affine span | PROVED ordinary | `pure_math/SPHERICAL_LOCAL_EXACT.md`; repeated/redundant exact examples | State with `ri`, indexed candidates, and no hidden full-dimensionality |
| Tangent-dependence uniqueness is equivalent to augmented affine independence in the minimal face containing zero | PROVED ordinary | `pure_math/SPHERICAL_LOCAL_EXACT.md`; redundancy regressions | Supporting exact classification |
| A chosen nonzero tangent dependence has exactly one positive spherical normal scale | PROVED; formalized finite algebra | `pure_math/SPHERICAL_LOCAL_EXACT.md`; `LocalSphericalFeasibility.lean`; `AntipodalSphericalFeasibility.lean` | Sphere-specific scaling contribution |
| Antipodal-only and mixed antipodal rows have the complete budget classification | PROVED ordinary; scalar core formalized | `pure_math/SPHERICAL_LOCAL_EXACT.md`; `AntipodalSphericalFeasibility.lean`; exact regressions | State separately; never divide an antipodal edge by `sin(theta)` |
| The relative cone margin gives explicit minimum coefficients, rate bounds, conditioning, and perturbation radii | PROVED ordinary under the displayed hypotheses | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md`; `LocalSphericalBounds.lean` for the loss-window core | Quantitative contribution; preserve full-dimensional/span qualifications |
| Under `c1 h <= theta_j <= c2 h`, outgoing rates obey explicit inverse-quadratic constants | PROVED ordinary | `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md` | Do not replace by unquantified `O(h^-2)` in theorem statements |
| Local row feasibility implies global reversible shared-edge feasibility | REJECTED as a general implication | Weighted-centered cube counterexample with exact Farkas certificate | Use as the central local/global distinction |
| Global shared-edge feasibility is exactly `b in cone{g_e}` and the feasible set is a polytope after zero chord columns are removed | PROVED ordinary | `pure_math/SHARED_EDGE_CONE_FARKAS.md`, including recession identity | Central global compatibility theorem |
| Weighted centering is necessary for a shared-edge solution | PROVED; formalized | `pure_math/SHARED_EDGE_CONE_FARKAS.md`; `ReversibleConductance.lean`; `CompleteGraph.lean` | Necessary condition, not sufficient on sparse graphs |
| Weighted centering is sufficient for a dense strictly positive complete-graph solution | PROVED; formalized | `pure_math/SHARED_EDGE_CONE_FARKAS.md`; `CompleteGraph.lean` | Dense sufficient construction |
| The AFP shared-edge system satisfies the full finite Farkas alternative with strain `sigma_e=(y_p-y_q)·(Omega_q-Omega_p)` | PROVED ordinary from standard finite Farkas; spherical consequences formalized | `pure_math/SHARED_EDGE_CONE_FARKAS.md`; `DualCertificate.lean`; `SharedEdgeGeometry.lean` | May claim completeness, while labeling finite Farkas as standard infrastructure |
| The linear, peak-rate, and weighted-residual AFP LPs have the stated duals and complementary-slackness equations | PROVED ordinary from finite LP strong duality; gap consequences formalized | `pure_math/SHARED_EDGE_OPTIMIZATION_DUALS.md`; `DualCertificate.lean`; `DualComplementarity.lean` | State actual matrices, endpoint prices, and residual signs |
| Strict all-edge global feasibility is equivalent to relative interior of the edge-column cone | PROVED ordinary | `pure_math/SHARED_EDGE_STRICT_SENSITIVITY.md`; strict-solution dual-face consequence in `DualComplementarity.lean` | Global strict-feasibility criterion |
| Strict shared-edge feasibility is stable under the explicit compatible perturbation bounds | PROVED ordinary | `pure_math/SHARED_EDGE_STRICT_SENSITIVITY.md` | Always retain range/centering and rank hypotheses |
| Centered-clique decompositions reconcile local blocks into a sparse shared-edge solution | PROVED ordinary | `pure_math/SHARED_EDGE_RECONCILIATION_EXAMPLES.md` direct construction | Nontrivial sufficient mechanism |
| The existing Lean dual-certificate theorem alone is the full Farkas alternative | REJECTED wording | `DualCertificate.lean` proves soundness and weak duality; full alternative is proved ordinarily from the standard finite theorem | Distinguish formal soundness from ordinary completeness |
| Constant-stopping layered final energy is order independent | PROVED for that model only | Additive energy decrement | Manufactured benchmark, not a general material theorem |
| Layered final energy is generally order independent | REJECTED | Nonproportional stopping flows need not commute | Replace by flow-commutator theory |
| No finite positive graph can satisfy positive Bakry–Émery curvature or `CD(1,2)` | REJECTED | Positive-curvature finite graphs are known | Study only AFP-specific curvature defects |
| Positivity alone gives standard continuum `W_2` contraction | REJECTED | Discrete Markov chains require a specified discrete transport metric | Deferred high-risk branch |
| The attainable quadratic exact subspace is characterized by jump covariance tensors | CONJECTURE with derived identity target | Algebraic expansion identified; full local/global dimension theorem absent | Core M3 research target |
| A nontrivial spectral-product hierarchy limits simultaneous exactness of low eigenspaces | CONJECTURE | Degree-one/degree-two case motivates it; general statement unknown | Pure-math main-theorem candidate |

## Claim-writing rules

1. Never use gate counts, Lean job counts, or CI hashes as evidence of novelty.
2. Separate `PROVED`, `EXTERNAL`, `COMPUTATIONAL`, and `CONJECTURE` in every draft.
3. State graph class, positivity, reversibility, embedding, and connectivity assumptions explicitly.
4. A finite audit is not an all-orders theorem.
5. A standard identity can support a new theorem but cannot be sold as the central contribution.
6. For local strict feasibility, write `relative interior in the affine span`, not ambient interior.
7. Antipodal indices must remain outside every formula containing `1/sin(theta)`.
8. Global perturbation statements must retain their compatibility/range conditions.
