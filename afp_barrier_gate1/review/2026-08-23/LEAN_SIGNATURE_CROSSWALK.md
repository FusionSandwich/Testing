# AFP R5 Lean signature crosswalk

This crosswalk is bound to scientific snapshot `9783a69e8f079d61c100bc87ea653ec9c981c2fe`. It records what the five flagship Lean modules actually prove and the manuscript conclusions they do **not** prove by themselves.

The release-wide audit reports 512 public theorem/lemma declarations checked with both `#check` and `#print axioms`, no project-local `axiom`, `sorry`, `admit`, or `sorryAx`, and only the expected foundational dependencies `propext`, `Classical.choice`, and `Quot.sound`. That is an axiom/signature audit of the finite formal surface, not whole-paper verification.

| Lean source | Checked finite content | Explicit hypotheses or imported premises | Not established by this module |
|---|---|---|---|
| `AFPBarrier/QuadraticFidelityFoundation.lean` | Weighted sample/Frobenius pairings, row Gram identities, concrete sampling/residual Gram formulas, orthogonal two-defect split, and the exact loss-second-moment decomposition. | Finite types and matrices; the residual Gram formulas assume the coordinate eigenmap componentwise; the Pythagorean theorem assumes the scalar contractions `hMZ` and `hZZ`; the variance identity assumes a nonzero row rate and the prescribed first moment. | No global spherical-generator existence, sharpness family, equality classification, graph assembly, or adaptive-ring construction. |
| `AFPBarrier/QuadraticFidelityLowerBound.lean` | Trace domination from an assumed energy domination, conversion to the two-defect lower bound, and the scalar rate-product implication. | The operator/energy domination, trace inequality, positive `rmax`, radial lower bound, and RMS rate floor are supplied as hypotheses to the scalar theorems; quotient/kernel facts are supplied by imported finite modules. | No single end-to-end theorem constructing all manuscript objects from spherical data; no proof of all-dimensional sharpness or the equality geometry. |
| `AFPBarrier/QuadraticEqualityGeometry.lean` | Division-free radial-tangent identities, tangent second-moment normalization, explicit nonantipodal denominator guards, and a scalar equality certificate. | Unit inner products, common shell loss/rate relations, zero tangent first moment, positive rate, `d>1`, and `ell<2` are explicit hypotheses. | No global Markov/Gram/Kolmogorov assembly theorem, no existence or uniqueness of a spherical embedding, no unrestricted rigidity/classification, and no Platonic theorem. |
| `AFPBarrier/QuadraticFidelityStability.lean` | Elementary consequences of the normalized master budget: weighted square/linear budgets, component bounds, pointwise dependence on mass, bad-vertex mass, and the tensor coefficient conversion. | The normalized master inequality, nonnegative weights/defects, and any positive mass floor are hypotheses. | No derivation of the complete geometric master inequality from a concrete generator in one declaration; no unconditional edgewise or graphwise propagation; no global frame or embedding repair. |
| `AFPBarrier/QuadraticFidelityConstruction.lean` | Division-safe force-to-coordinate identities, detailed-balance algebra, normalization by vertex mass, rate conversion from a chord floor, connector identities, and regular-polygon recurrences. | Shared moment/force equations, nonzero or positive masses and lengths, chord lower bounds, and recurrence identities are supplied explicitly. | No analytic adaptive-ring schedule, no proof that the transition systems are invertible and positive at all levels, no Cauchy/Neumann guard, no telescoping conductance recurrence, and no `d=3` mesh constants. |

## Manuscript disposition implied by the signatures

- Proposition 2.1, Theorem 3.1, Proposition 3.2, and the algebraic spine of Theorem 4.1 have substantial finite Lean support, but the manuscript assembles the complete spherical statement and sharpness argument in ordinary mathematics.
- Theorem 5.1 and Theorem 5.2 have local scalar/tensor Lean support. Theorem 5.3, Proposition 5.4, Corollary 5.5, and Corollary 5.6 are not one end-to-end formal theorem chain in the cited modules.
- Theorem 6.1 has a Lean-checked scalar budget spine once the normalized master inequality is supplied. Corollary 6.3 exceeds the theorem-grade formal surface as printed.
- Theorem 7.1 has formal recurrence identities plus a direct ordinary Fourier proof.
- Theorem 7.2 is not Lean-formalized. Its analytic schedule, positivity, recurrence, and mesh constants remain an ordinary/computer-assisted exact-certificate obligation.
- Open Problem 7.3 is correctly not formalized as a theorem.

## Safe replacement for whole-paper formalization language

> Lean verifies the finite algebraic spine identified in the theorem-to-source map. The global geometric classifications, all-level adaptive-ring construction, prior-art assessment, and every numerical, transport, or physical interpretation remain ordinary, computer-assisted, external-input, or open obligations as stated separately.
