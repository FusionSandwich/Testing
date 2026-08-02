# AFP mathematical claim matrix

This document controls publication wording for the pure-mathematics track.
Statuses distinguish ordinary proof, Lean verification, exact finite
regression, external input, conjecture, and rejected wording.

| Claim | Status | Current support | Publication treatment |
|---|---|---|---|
| Finite jump generators satisfy the carré-du-champ square and bilinear product identities | PROVED / standard / Lean | `JumpGenerator.lean`; `QuadraticCovariance.lean` | Foundational lemmas, not novelty |
| `lambda^2 <= rate * peakDefect` and the weighted edge-loss variance remainder | PROVED / Lean | `Quantitative.lean`, `LossVariance*.lean` | Foundational inequalities |
| A finite positive generator cannot reproduce the complete coordinate and complete spherical degree-two spaces | PROVED in the stated spherical formulation | `NoGo.lean`, covariance package | Supporting no-go corollary |
| A centered positive quadrature admits a dense reversible degree-one-exact operator | PROVED / Lean | `CompleteGraph.lean`; Prompt 1 theorem package | Supporting construction |
| Positive spherical Delaunay families attain the natural `h^-2` scale | EXTERNAL specialization | Published spherical Delaunay theory plus project bounds | Cite as external input |
| The project family is globally minimax or spectrally optimal | CONJECTURE / unsupported | No global minimax proof | Do not claim |
| Only `K in {4,6,12}` can have global `Q=1` | REJECTED | Cube and dodecahedron counterexamples | Never state unrestricted |
| Abstract local equality propagates one common rate and one common symmetric active-edge loss on a connected active graph | PROVED / Lean | `GlobalLossRigidity.lean`: `rate_eq_of_symmetric_active_loss`, `rate_eq_of_active_reflTransGen`, `connected_active_loss_rigidity` | Supporting abstract rigidity theorem already complete |
| Complete spherical `Q=1` specialization of the abstract propagation theorem | PROMPT 3 TARGET | Needs hypothesis and normalization audit | Do not conflate with the abstract Lean theorem |
| Tetrahedral/octahedral/icosahedral classification under restricted geodesic-triangulation hypotheses | CONJECTURE / PROMPT 3 TARGET | Requires enumeration and geometric proof | Not part of Prompt 2 closeout |
| Quantitative near-rigidity from small equality defect | CONJECTURE / PROMPT 3 TARGET | Local variance estimate exists; global propagation absent | Not part of Prompt 2 closeout |
| Non-antipodal local feasibility is equivalent to `0` in the indexed tangent hull | PROVED | Corrected Prompt 1 package and Lean finite scaling | Sphere-specific transfer of standard positive-stencil geometry |
| Strict positivity on every indexed non-antipodal edge is equivalent to relative-interior membership | PROVED | Corrected Prompt 1 theorem, repetitions and lower dimension included | State relative, not ambient, interior |
| Tangent dependence and row uniqueness are controlled by the normalized dependence polytope/minimal face | PROVED | Prompt 1 package | Preserve indexed repetitions and redundancies |
| Pure and mixed antipodal feasibility is a separate division-free normal-budget simplex | PROVED / Lean | `AntipodalFeasibility.lean` | Never assign an antipodal tangent direction |
| `rho>0`, `beta_*>0`, and strict local feasibility are equivalent with explicit coefficient margin | PROVED | Corrected Prompt 1 package | Quantitative Prompt 1 result |
| Local exact rows have explicit rate, coefficient, singular-value, and perturbation bounds | PROVED | Corrected Prompt 1 package and Lean consequences | State every angular/span margin explicitly |
| Local positive rows plus centering imply arbitrary sparse global reversibility | REJECTED | Exact four-cycle and cube Farkas counterexamples | Keep as regression warning |
| Centering is necessary globally and sufficient on the complete graph | PROVED / Lean | `ReversibleConductance.lean`, `CompleteGraph.lean` | Supporting global theorem |
| Sparse global reversible feasibility is exact shared-edge cone membership | PROVED | Prompt 1 cone/Farkas/LP package | Retain graph and noncoincident-edge hypotheses |
| Equivariant averaging and centered-clique decompositions reconcile stated sparse families | PROVED / Lean-supported | `GroupAveraging.lean`, Prompt 1 package | Explicit sufficient mechanisms only |
| The finite quadratic covariance identity and arbitrary shifted target residual are exact | PROVED / Lean | `QuadraticCovariance.lean`; Theorems 1.1–1.2 | Foundational Prompt 2 identity |
| Trace-free spherical quadratic form exactness is `span{M_i}^perp` | PROVED | Prompt 2 theorem | Label explicitly as form space |
| The residual factors through sampling: `R_X=(L+2dI)S_X` | PROVED / Lean-supported | Prompt 2 theorem and factorization lemmas | Central sampled-space correction |
| Every sampling alias lies in the exact-form kernel | PROVED / Lean | `samplingKernel_le_residualKernel` | Never treat the kernels as unrelated |
| Genuine sampled exactness is `im(S_X) intersect ker(L+2dI)` | PROVED / Lean | `sampledRange_exact_eq_range_inf_ker` | Object of every sampled dimension claim |
| `dim E_sample=dim E_form-dim K_X=rank S_X-rank R_X` | PROVED | Rank-nullity plus factorization; exact audits | Specialized formula |
| Positive axial covariance at every node forces `E_form=K_X` and `E_sample=0` | PROVED / sharp | Prompt 2 theorem; row scaling in Lean | Principal positive rigidity theorem |
| Regular simplices attain the axial theorem in every dimension | PROVED / exact | Explicit inverse sampling formula; closeout audit | Sharp equality family |
| Transitive equivariance plus irreducible `Sym_0(d)` forces `E_form=0` | PROVED ONLY WITH GLOBAL OFF-DIAGONAL NONNEGATIVITY | Corrected Theorem 4.1; positive radial covariance argument | State `a_ij>=0` for every `i!=j`; reversibility not required |
| The same equivariant statement with only one positive distinct jump and otherwise signed rates | REJECTED | Exact signed regular-pentagon counterexample | False because negative rates cancel radial covariance |
| Signed regular pentagon has coordinate eigenvalue `-1`, full trace-free quadratic eigenvalue `-4`, and `dim E_sample=2` | PROVED EXACT COUNTEREXAMPLE | `prompt2_closeout_audit.py`; theorem document | Permanent positivity regression |
| Five Platonic shortest-edge generators have form dimensions `2,3,2,0,0` and sampled dimensions all zero | PROVED EXACT / computational regression | Exact tensors, kernels, determinants over `Q(sqrt(5))` | Exact examples, not a classification |
| Tetrahedral, octahedral, and cubical nonzero exact forms are nonzero sampled modes | REJECTED | Their form spaces equal their sampling kernels | Never report form dimension as sampled dimension |
| Signed four-cardinal-point generator restores one sampled quadratic mode | PROVED EXACT | Adjacent rates `1`, antipodal rates `-1/2` | Positivity contrast |
| The antipodal rate `-1/2` is forced on the fixed four-point support | PROVED / sharp fixed-support | Exact three-equation solve | State support and target modes |
| General shifted product residual is `2 Gamma+(mu-lambda-nu)fg-mu c` | PROVED / Lean | `jumpGenerator_shifted_product_residual`, `shifted_product_target_iff` | Foundational centered-product theorem |
| At additive resonance, `fg-c` is exact iff `2 Gamma(f,g)=(lambda+nu)c` | PROVED / Lean | `additive_product_resonance_iff` | Correct product criterion |
| A centered square is exact at `-2lambda` iff `Gamma(f)=lambda c` | PROVED / Lean | `centered_square_resonance_iff` | Distinguish centered and uncentered cases |
| An uncentered additive square (`c=0`) forces zero carré du champ | PROVED / Lean | `uncentered_square_resonance_iff_zero_gamma` | On an irreducible positive chain with `lambda>0`, this forces `f=0` |
| Every nonzero centered additive square is impossible for a positive finite generator | REJECTED | Boolean four-state counterexample | False; constant positive carré du champ permits resonance |
| Boolean square `f=x_1+x_2` satisfies `Lf=-2f`, `L(f^2-2)=-4(f^2-2)`, `Gamma=4` | PROVED EXACT EXAMPLE | `prompt2_closeout_audit.py`; theorem document | Permanent centered-resonance regression |
| Centered resonance implies semigroup variance `c(1-exp(-2lambda t))` and conversely under finite-dimensional differentiability | PROVED | Ordinary finite matrix-semigroup proof; exact Boolean audit | Separate from Jensen equality |
| Jensen equality holds iff `f` is constant on positive transition support | PROVED / standard external input | Strict convexity and finite uniformization | Boolean centered example has positive variance, not equality |
| Spherical degree-two covariance is the same as additive coordinate-square resonance | REJECTED | Eigenvalue shift `2d-2(d-1)=2` | Keep the two problems separate |
| `S^2` pointwise product table for `ell=1,...,6` has no additive resonance | PROVED EXACT ARITHMETIC | Theorem table and `prompt2_closeout_audit.py` | Centering removes only degree zero; aliases still require audit |
| Pell-type additive resonances occur in higher dimensions | PROVED ARITHMETIC / bounded computational search | Existing and closeout exact assertions | Arithmetic alone does not identify a sampled mode |
| A nontrivial general spectral-product hierarchy follows from the present calculations | REJECTED FOR PROMPT 2 | No sampled dimension tradeoff, multiplicity obstruction, or new global consequence survived | Rejection does not rely on centered-square impossibility |
| Dedicated Prompt 2 CI rejects both `axiom` and plural `axioms` declarations | VERIFIED POLICY | Aggregate source scan plus deterministic singular/plural fixtures | Verification control, not mathematics |
| Constant-stopping layered final energy is order independent | PROVED for that model only | Additive decrement | Manufactured benchmark only |
| General layered stopping is order independent | REJECTED | Noncommuting flows | Outside pure-math closeout |
| Blanket positive Bakry–Émery curvature collapse on finite graphs | REJECTED | Known positive-curvature finite graphs | Do not claim |
| Positivity alone gives continuum `W_2` contraction | REJECTED | A discrete transport metric is required | Deferred branch |

## Claim-writing rules

1. CI counts and hashes are provenance, not novelty evidence.
2. Separate `PROVED`, `EXTERNAL`, `EXACT EXAMPLE`, `COMPUTATIONAL`,
   `CONJECTURE`, and `REJECTED`.
3. State positivity, reversibility, connectivity, embedding, masses, and
   relative-span assumptions explicitly.
4. A nonzero quadratic matrix, nonzero exact form, nonzero sampled function,
   and nonzero exact sampled function are distinct claims.
5. Use `R_X=(L+2dI)S_X`; sampling and residual kernels are not generic
   unrelated objects.
6. Centered resonance is constant carré du champ; uncentered resonance is zero
   carré du champ.
7. Centered resonance is not Jensen equality.
8. Algebraic harmonic decomposition does not imply sampled identifiability.
9. The abstract equality-propagation theorem is proved; its spherical
   classification and near-rigidity consequences remain Prompt 3 work.
10. The immutable transport archive is outside the pure-math claim set.
