# AFP mathematical claim matrix

This document controls publication wording for the pure-mathematics track.
Statuses are deliberately conservative.

| Claim | Status | Current support | Publication treatment |
|---|---|---|---|
| Finite jump generators satisfy the carré-du-champ square identity | PROVED / standard | Lean module `JumpGenerator.lean`; standard Markov-generator algebra | Foundational lemma only |
| `lambda^2 <= rate * peakDefect` | PROVED / standard | Lean modules `Quantitative.lean` and `LossVariance*.lean` | Foundational weighted Cauchy–Schwarz lemma |
| The gap equals a weighted edge-loss variance | PROVED | Lean module `LossVariance.lean` | Foundational sharpness identity |
| A finite positive conservative generator cannot reproduce the complete degree-one and complete degree-two spherical eigenspaces exactly | PROVED in the stated AFP formulation | Lean algebraic core plus spherical specialization | Candidate AFP-specific corollary; priority still requires specialist review |
| A centered positive quadrature admits a dense positive reversible degree-one-exact operator | PROVED | `CompleteGraph.lean` | Supporting construction |
| Positive spherical Delaunay families attain the natural `h^-2` rate scale | EXTERNAL specialization | Uses published spherical Delaunay Laplacian theory plus project loss bounds | Cite as achievability input, not as an original construction |
| The project’s quasi-uniform family is globally minimax or spectrally optimal | CONJECTURE / unsupported | No global minimax theorem | Do not claim |
| Only `K in {4,6,12}` can have global `Q=1` | REJECTED | Cube (`K=8`) and dodecahedron (`K=20`) are counterexamples | Never state without new restrictive assumptions |
| Connected reversible `Q=1` graphs have one common active-edge loss and one common row rate | CONJECTURE with complete proof target | Follows from local equality plus shared-edge propagation; formalization active | Intended first global rigidity lemma |
| Only tetrahedral, octahedral, and icosahedral spherical triangulations can satisfy global `Q=1` under strict equal-edge hypotheses | CONJECTURE | Plausible only after explicit triangulation, positivity, and embedding assumptions | Counterexample search before proof |
| Local degree-one feasibility is equivalent to a nonnegative tangent dependence and a positive normal scale | PROVED mathematically; formalization active | Rowwise tangent/normal decomposition | Central M1 theorem after novelty review |
| Strict positivity on every candidate edge is equivalent to a relative-interior condition | CONJECTURE / expected convex-geometry corollary | Not yet formalized or fully written | M1 theorem target |
| Local row feasibility implies global reversible shared-edge feasibility | REJECTED as a general implication | Global coupling can add constraints | Search for explicit counterexamples and characterize compatibility |
| Existing Lean dual-certificate theorem is the full Farkas alternative | REJECTED wording | Current theorem proves certificate soundness and weak duality only | State narrowly; full alternative is external or future formalization |
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
