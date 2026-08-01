# AFP mathematical claim matrix

This document controls publication wording for the pure-mathematics track.
Statuses distinguish ordinary proof, Lean verification, external theorem use,
and computational regression.

| Claim | Status | Current support | Publication treatment |
|---|---|---|---|
| Finite jump generators satisfy the carré-du-champ square identity | PROVED / standard | Lean module `JumpGenerator.lean`; standard Markov-generator algebra | Foundational lemma only |
| `lambda^2 <= rate * peakDefect` | PROVED / standard | Lean modules `Quantitative.lean` and `LossVariance*.lean` | Foundational weighted Cauchy–Schwarz lemma |
| The gap equals a weighted edge-loss variance | PROVED | Lean module `LossVariance.lean` | Foundational sharpness identity |
| A finite positive conservative generator cannot reproduce the complete degree-one and complete degree-two spherical eigenspaces exactly | PROVED in the stated AFP formulation | Lean algebraic core plus spherical specialization | Supporting no-go corollary; not the Prompt 2 sharp theorem |
| A centered positive quadrature admits a dense positive reversible degree-one-exact operator | PROVED | `CompleteGraph.lean`; Theorem 4.2 in `SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` | Supporting construction |
| Positive spherical Delaunay families attain the natural `h^-2` rate scale | EXTERNAL specialization | Published spherical Delaunay Laplacian theory plus project loss bounds | Cite as achievability input, not as an original construction |
| The project’s quasi-uniform family is globally minimax or spectrally optimal | CONJECTURE / unsupported | No global minimax theorem | Do not claim |
| Only `K in {4,6,12}` can have global `Q=1` | REJECTED | Cube (`K=8`) and dodecahedron (`K=20`) are counterexamples | Never state without new restrictive assumptions |
| Connected reversible `Q=1` graphs have one common active-edge loss and one common row rate | CONJECTURE with complete proof target | Local equality plus shared-edge propagation; separate M2 work | Not part of P0/M1 or Prompt 2 |
| Only tetrahedral, octahedral, and icosahedral spherical triangulations can satisfy global `Q=1` under strict equal-edge hypotheses | CONJECTURE | Plausible only after explicit triangulation, positivity, and embedding assumptions | Counterexample search before proof |
| A nonnegative non-antipodal degree-one row exists iff `0` lies in the tangent convex hull | PROVED | Theorem 1.2; constructive Lean checkpoint and `SphericalFeasibilityAlgebra.lean` | Standard finite-convex core; not standalone novelty |
| A row positive on every indexed non-antipodal edge exists iff `0` lies in the relative interior of the indexed tangent hull | PROVED | Lemma 1.1 and Theorem 1.2; repeats and redundancies included | State with `relative interior`, never ambient interior |
| A chosen nonzero tangent dependence determines exactly one positive normal scale and the explicit rate formula | PROVED / Lean-supported | Equations (1.2)–(1.4); `LocalSphericalFeasibility.lean`; `SphericalFeasibilityAlgebra.lean` | Sphere-specific scaling component |
| Tangent dependence and row uniqueness are characterized by affine independence in the minimal face containing zero | PROVED | Theorem 1.4 | Include indexed repetitions/redundancies explicitly |
| Antipodal-only and mixed antipodal rows admit the division-free budget classification | PROVED / Lean-supported | Theorem 2.1 and Corollary 2.2; antipodal scalar lemmas in `SphericalFeasibilityAlgebra.lean` | Never assign an antipodal tangent direction or divide by `sin(theta)` |
| The relative cone margin has the support-function dual formula and yields `lambda_j >= rho/[m(1+rho)]` | PROVED | Section 3 and Lemma 3.1 | Quantitative local contribution |
| The angular window gives explicit inverse-quadratic outgoing and coefficient bounds | PROVED / Lean-supported | Equations (3.7)–(3.12); `QuantitativeSphericalFeasibility.lean` formalizes the loss-window inequalities | Distinguish loss-only outgoing bounds from margin-dependent coefficient lower bounds |
| The local balance matrix has the explicit conditioning bound (3.17) | PROVED | Section 3.3 | State relative-span/full-rank hypotheses |
| Strict local feasibility persists under the explicit perturbation radius (3.21), with objective degradation (3.25) | PROVED | Section 3.4 | Arbitrary ambient perturbations are restricted to full 2-D span; lower-dimensional robustness is span-preserving only |
| Global reversible feasibility is exactly `b` membership in the shared-edge cone and has the compact-polytope characterization after zero columns are removed | PROVED | Theorem 4.1 | Include coincident-node exception |
| Weighted centering is necessary for any reversible degree-one-exact solution | PROVED / Lean-supported | `ReversibleConductance.lean`, `CompleteGraph.lean`, Theorem 4.2 | Necessary globally; not sufficient on a sparse graph |
| The full shared-edge Farkas alternative, strong LP duality, and complementary slackness hold with the AFP signs and edge blocks | PROVED using standard external finite-dimensional theorems; spherical consequences Lean-supported | Sections 4.3–4.5; `DualCertificate.lean`; `GlobalSharedEdgeDuality.lean` | Do not claim the general Farkas or LP theorem as new |
| Strict all-edge global feasibility is equivalent to `b in ri(cone{z_e})` | PROVED | Theorem 4.4 | Global analogue of positive indexed coefficients |
| Local row feasibility implies global reversible shared-edge feasibility | REJECTED | Weighted-centered cube counterexample with exact Farkas certificate, Section 5.4 | Never use an unproved compatibility lemma |
| Weighted centering alone is sufficient on an arbitrary sparse permitted graph | REJECTED | Same cube counterexample | Complete graph and additional gluing hypotheses are required |
| A centered-clique submass decomposition reconciles local centered blocks into a sparse global shared-edge solution | PROVED | Theorem 4.5 | Nontrivial constructive sufficient mechanism |
| The finite quadratic covariance identity and shifted target residual are exact | PROVED / Lean-supported | Theorems 1.1–1.2 in `SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`; `QuadraticCovariance.lean` | Foundational Prompt 2 identity, not by itself the sharp result |
| Trace-free spherical quadratic form exactness is `span{M_i}^perp` | PROVED / Lean-supported consequences | Theorem 2.1; trace-free projection contraction in `QuadraticCovariance.lean` | Explicitly label this as form space |
| Genuine sampled exactness is `S_X(E_form)` with the intersection and stacked-rank dimension formulas | PROVED | Theorem 3.1 and equations (3.4), (3.9), (3.10) | Every dimension claim must distinguish matrix forms from sampled functions |
| Under positive axially isotropic jump covariance at every node, `E_form=K_X` and `E_sample={0}` | PROVED / sharp structural theorem | Theorems 4.2–4.3; row-scaling implication formalized in `QuadraticCovariance.lean` | Principal Prompt 2 rigidity theorem |
| The axial theorem is sharp in every dimension on the regular simplex family | PROVED | Corollary 4.4, with explicit inverse sampling construction | Equality family; large algebraic kernel but zero sampled exact space |
| Transitive equivariance plus irreducibility of `Sym_0(d)` forces `E_form=0` | PROVED | Theorem 4.5 and positive radial-covariance contradiction | Independent symmetry-rigidity mechanism; state irreducibility as a hypothesis |
| The five Platonic shortest-edge generators have the exact Prompt 2 rank table and zero sampled degree-two exactness | PROVED exactly / computationally regression-checked | Section 5; exact determinants and covariance tensors; SymPy audit over `Q(sqrt(5))` | Exact finite examples, not an all-graph classification |
| Tetrahedral, octahedral, and cubical algebraic exact forms are genuine degree-two sampled modes | REJECTED | Their exact form spaces equal their sampling kernels | Never report form-space dimension as sampled dimension |
| Allowing signed conductances can restore a genuine sampled quadratic mode | PROVED by explicit construction | Four cardinal points on `S^1`; adjacent rates `1`, antipodal rates `-1/2`; Section 6 | Contrast theorem showing positivity is essential |
| On the four-point signed support, the negative antipodal rate `-1/2` is forced | PROVED / sharp fixed-support lower bound | Exact three-equation row solve, Section 6 | State fixed nodes, support, coordinate eigenvalue, and prescribed quadratic mode |
| Additive exact propagation of a nonzero sampled square is impossible for an irreducible positive finite generator | PROVED by two independent standard routes | Carré-du-champ and semigroup/Jensen proofs, Section 7 | Foundational product obstruction; sampled-function identifiability required |
| A nontrivial general spectral-product hierarchy follows from the current square calculations | REJECTED for Prompt 2 | Parity, maximizing-set, aliasing, and resonance audit; all usable consequences reduce to the sampled-square identity | Do not inflate arithmetic resonances into an eigenspace hierarchy |
| Constant-stopping layered final energy is order independent | PROVED for that model only | Additive energy decrement | Manufactured benchmark, not a general material theorem |
| Layered final energy is generally order independent | REJECTED | Nonproportional stopping flows need not commute | Replace by flow-commutator theory |
| No finite positive graph can satisfy positive Bakry–Émery curvature or `CD(1,2)` | REJECTED | Positive-curvature finite graphs are known | Study only AFP-specific curvature defects |
| Positivity alone gives standard continuum `W_2` contraction | REJECTED | Discrete Markov chains require a specified discrete transport metric | Deferred high-risk branch |

## Claim-writing rules

1. Never use gate counts, Lean job counts, or CI hashes as evidence of novelty.
2. Separate `PROVED`, `EXTERNAL`, `COMPUTATIONAL`, and `CONJECTURE` in every draft.
3. State graph class, positivity, reversibility, embedding, masses, connectivity, and relative-span hypotheses explicitly.
4. Never hide antipodes inside a formula containing division by `sin(theta)`.
5. A finite audit is not an all-orders theorem.
6. A standard convex-hull, Farkas, LP, carré-du-champ, or Jensen theorem can support the package but is not itself the publication contribution.
7. Local positive rows, weighted centering, and sparse global shared-edge compatibility are three distinct logical levels.
8. A nonzero quadratic matrix, a nonzero exact form, a nonzero sampled function, and a nonzero exact sampled function are four distinct claims.
9. Never replace `dim(E_form ∩ K_X)` by `dim K_X` without proving the required containment.
10. Algebraic harmonic decomposition does not imply sampled identifiability; sampling kernels and cross-degree aliases must be checked.
