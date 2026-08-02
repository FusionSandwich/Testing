# AFP mathematical claim matrix

This document controls publication wording for the pure-mathematics track.
Statuses distinguish ordinary proof, Lean verification, external theorem use,
and computational regression.

| Claim | Status | Current support | Publication treatment |
|---|---|---|---|
| Finite jump generators satisfy the carré-du-champ square identity | PROVED / standard | Lean module `JumpGenerator.lean`; standard Markov-generator algebra | Foundational lemma only |
| `lambda^2 <= rate * peakDefect` | PROVED / standard | Lean modules `Quantitative.lean` and `LossVariance*.lean` | Foundational weighted Cauchy–Schwarz lemma |
| The gap equals a weighted edge-loss variance | PROVED | Lean module `LossVariance.lean` | Foundational sharpness identity |
| A finite positive conservative generator cannot reproduce the complete degree-one and complete degree-two spherical eigenspaces exactly | PROVED in the stated AFP formulation | Lean algebraic core plus spherical specialization | Supporting no-go corollary, not the Prompt 2 sharp theorem |
| A centered positive quadrature admits a dense positive reversible degree-one-exact operator | PROVED | `CompleteGraph.lean`; Prompt 1 theorem package | Supporting construction |
| Positive spherical Delaunay families attain the natural `h^-2` rate scale | EXTERNAL specialization | Published spherical Delaunay Laplacian theory plus project loss bounds | Cite as achievability input, not as an original construction |
| The project’s quasi-uniform family is globally minimax or spectrally optimal | CONJECTURE / unsupported | No global minimax theorem | Do not claim |
| Only `K in {4,6,12}` can have global `Q=1` | REJECTED | Cube (`K=8`) and dodecahedron (`K=20`) are counterexamples | Never state without new restrictive assumptions |
| Connected reversible `Q=1` graphs have one common active-edge loss and one common row rate | CONJECTURE with complete proof target | Local equality plus shared-edge propagation; separate M2 work | Not part of Prompt 1 or Prompt 2 |
| Only tetrahedral, octahedral, and icosahedral spherical triangulations can satisfy global `Q=1` under strict equal-edge hypotheses | CONJECTURE | Plausible only after explicit triangulation, positivity, and embedding assumptions | Counterexample search before proof |
| Non-antipodal local feasibility is equivalent to `0` in the indexed tangent hull | PROVED | Exact bijection and proof in the corrected Prompt 1 package; finite scaling in Lean | Sphere-specific transfer of standard positive-stencil geometry |
| Strict positivity on every non-antipodal edge is equivalent to tangent-hull relative interior | PROVED | Supporting separation plus constructive inball proof, including repetitions and lower dimension | Prompt 1 theorem with standard convex input identified |
| Tangent-dependence and row uniqueness are equivalent to the normalized dependence polytope being a singleton | PROVED | Exact dependence/row bijection; minimal-face affine-independence criterion | Include indexed repetitions and redundancies explicitly |
| Pure and mixed antipodal feasibility is a separate normal-budget simplex | PROVED | Exact no-division parameterization | Never assign a tangent direction at an antipode |
| `rho>0`, `beta_*>0`, and strict local feasibility are equivalent, with `beta_j >= rho/[m(1+rho)]` | PROVED | Constructive barycentric proof and exact support/LP formulas | Quantitative Prompt 1 result |
| Local exact rows have explicit inverse-quadratic rate and coefficient bounds under positive quasi-uniform angle constants | PROVED | Corrected Prompt 1 theorem | State `0<c1<=c2` explicitly |
| The local balance matrix has explicit singular-value, right-inverse, and condition-number bounds | PROVED | Corrected Prompt 1 theorem with relative-span hypotheses | Never call conditioning controlled without the displayed margin |
| Strict local feasibility persists under the stated transported-span perturbation bound | PROVED | Corrected Prompt 1 theorem with an explicit span isometry and angular constants | Endpoint motion alone does not identify changing lower-dimensional spans |
| Local row feasibility implies global reversible shared-edge feasibility | REJECTED | Centered alternating-mass four-cycle has strict local rows and exact Farkas certificate | Retain as regression obstruction |
| Weighted centering is sufficient on every permitted graph | REJECTED | Same centered four-cycle obstruction | Sufficient on the complete graph or under reconciliation hypotheses |
| Centering is necessary on every graph and sufficient on the complete graph via `gamma_ij=2w_iw_j/sum w` | PROVED | Block-sum proof and `CompleteGraph.lean` | Supporting global theorem |
| Global reversible feasibility is exactly shared-edge cone membership; its spherical feasible set is a compact polytope | PROVED | Corrected Prompt 1 theorem and positive edge-loss conductance bounds | Retain the noncoincident permitted-edge hypothesis |
| Strict all-edge global feasibility is equivalent to relative-interior membership in the shared-edge cone | PROVED | Finite indexed conic relative-interior theorem | Global analogue of positive barycentric coordinates |
| Equivariant averaging reconciles local rows when averaged edge orientations agree | PROVED | Precise action/embedding/mass hypotheses in corrected Prompt 1 theorem | Noncomplete-graph reconciliation theorem |
| Centered-clique submass decompositions reconcile sparse local blocks | PROVED | Independent corrected Prompt 1 theorem | Additional noncomplete-graph mechanism |
| Existing Lean dual-certificate theorem is the full Farkas alternative | REJECTED wording | Lean proves soundness; the proof package transfers the full finite alternative and strong LP duality | Preserve formal/prose distinction |
| Strict shared feasibility is stable under compatible perturbations controlled by an interior and singular-value margin | PROVED under stated compatibility/rigidity hypotheses | Corrected Prompt 1 theorem | Never omit centering/range compatibility |
| The finite quadratic covariance identity and shifted target residual are exact | PROVED / Lean-supported | Theorems 1.1–1.2 in `SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`; `QuadraticCovariance.lean` | Foundational Prompt 2 identity, not by itself the sharp result |
| Trace-free spherical quadratic form exactness is `span{M_i}^perp` | PROVED / Lean-supported consequences | Theorem 2.1; trace-free projection contraction in Lean | Explicitly label this as form space |
| The quadratic residual map factors as `R_X=(L+2dI)S_X` | PROVED / Lean-supported | Theorem 3.1 and `samplingKernel_le_residualKernel` | Central sampled-space correction |
| Every quadratic sampling alias lies in the exact-form kernel: `K_X subset E_form` | PROVED / Lean-supported | Immediate from the residual factorization | Never treat the two kernels as unrelated |
| Genuine sampled exactness is `S_X(E_form)=im(S_X) intersect ker(L+2dI)` | PROVED / Lean-supported | Theorem 3.1; `sampledRange_exact_eq_range_inf_ker` | Publication object for every dimension claim |
| `dim E_sample = dim E_form-dim K_X = rank(S_X)-rank(R_X)` | PROVED | Rank-nullity plus `K_X subset E_form`; exact symbolic regressions | The general intersection formula remains valid and collapses here |
| The stacked matrix satisfies `rank([R;S])=rank(S)` | PROVED | Matrix factorization `R=(G+2dI)S` | Do not use a generic unrelated-map counterexample against this formula |
| Under positive axially isotropic jump covariance at every node, `E_form=K_X` and `E_sample={0}` | PROVED / sharp structural theorem | Theorems 4.2–4.3; row-scaling implication formalized in Lean | Principal Prompt 2 rigidity theorem |
| The axial theorem is sharp in every dimension on the regular-simplex family | PROVED | Corollary 4.4 with explicit inverse sampling construction | Equality family with a large algebraic kernel but zero sampled exact space |
| Transitive equivariance plus irreducibility of `Sym_0(d)` forces `E_form=0` | PROVED | Theorem 4.5 and positive radial-covariance contradiction | Independent symmetry-rigidity mechanism; irreducibility is a stated hypothesis |
| The five Platonic shortest-edge generators have the exact Prompt 2 rank table and zero sampled degree-two exactness | PROVED exactly / computationally regression-checked | Exact covariance tensors, determinant witnesses, and exact SymPy audit over `Q(sqrt(5))` | Exact finite examples, not an all-graph classification |
| Tetrahedral, octahedral, and cubical algebraic exact forms are genuine sampled degree-two modes | REJECTED | Their exact form spaces equal their sampling kernels | Never report form-space dimension as sampled dimension |
| Allowing signed conductances can restore a genuine sampled quadratic mode | PROVED by explicit construction | Four cardinal points on `S^1`; adjacent rates `1`, antipodal rates `-1/2` | Contrast theorem showing positivity is essential |
| On the four-point signed support, the negative antipodal rate `-1/2` is forced | PROVED / sharp fixed-support statement | Exact three-equation row solve | State fixed nodes, support, coordinate eigenvalue, and prescribed quadratic mode |
| Additive exact propagation of a nonzero sampled square is impossible for an irreducible positive finite generator | PROVED by two independent standard routes | Carré-du-champ and semigroup/Jensen proofs | Sampled-function identifiability is required |
| A nontrivial general spectral-product hierarchy follows from the present square calculations | REJECTED for Prompt 2 | Parity, maximizing-set, aliasing, and Pell-resonance audit; all usable consequences reduce to the sampled-square identity | Do not inflate arithmetic resonance into an eigenspace hierarchy |
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
6. Standard convex-hull, Farkas, LP, carré-du-champ, Jensen, and rank-nullity results are inputs, not publication novelty.
7. Local positive rows, weighted centering, and sparse global shared-edge compatibility are three distinct logical levels.
8. A nonzero quadratic matrix, a nonzero exact form, a nonzero sampled function, and a nonzero exact sampled function are four distinct claims.
9. In Prompt 2 use `R_X=(L+2dI)S_X`; consequently `K_X subset E_form` and `dim E_sample=rank S_X-rank R_X`.
10. Algebraic harmonic decomposition does not imply sampled identifiability; sampling kernels and cross-degree aliases must be checked.
