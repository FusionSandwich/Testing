# Exact feasibility and covariance theorem-to-file map

The complete Prompt 1 mathematical proof is
`pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md`. “Lean support” identifies
the finite algebra formalized in the project; standard finite convex geometry,
Farkas, LP strong duality, semigroup, and representation facts are transferred
explicitly rather than misrepresented as project axioms.

## Prompt 1 local and global feasibility

| Mandatory item | Mathematical proof | Lean support | Exact regression |
|---|---|---|---|
| Non-antipodal feasibility iff `0` in tangent hull | Prompt 1 Theorem 1.1 | `LocalSphericalFeasibility.lean`, `ExactLocalRows.lean` | outside/boundary cases |
| Strict feasibility iff relative interior | Prompt 1 Theorems 1.1, 3.1 | indexed positivity in `ExactLocalRows.lean` | lower/full-dimensional cases |
| Repetitions, redundancies, lower dimension | Prompt 1 Section 5 | indexed function formulation | repeated-direction cases |
| Exact scaling, converse, outgoing rate, uniqueness | Prompt 1 Theorem 1.2 and corollaries | `LocalSphericalFeasibility.lean`, `ExactLocalRows.lean`, `SphericalFeasibilityAlgebra.lean` | exact local rows |
| Pure and mixed antipodal simplex | Prompt 1 Theorems 2.1–2.2 | `AntipodalFeasibility.lean` | pure/mixed antipodes |
| Relative margin, rate, coefficient, LP formulas | Prompt 1 Section 3 | `QuantitativeExactLocal.lean`, `QuantitativeSphericalFeasibility.lean` | exact optima and margins |
| Perturbation and conditioning | Prompt 1 Theorems 3.4–3.5 | finite column estimates plus stated SVD transfer | boundary crossing |
| Shared-edge cone/polytope/Farkas | Prompt 1 Theorem 4.1 | `DualCertificate.lean`, `SharedEdgeEquilibrium.lean` | exact square/cube certificates |
| Centering and complete graph | Prompt 1 Theorem 4.2 | `ReversibleConductance.lean`, `CompleteGraph.lean` | centered constructions |
| LP duality and complementarity | Prompt 1 Theorem 4.3 | `GlobalSharedEdgeDuality.lean` plus standard transfer | sign audit |
| Local-not-global obstructions | Prompt 1 Section 5 | `SharedEdgeEquilibrium.lean` | four-cycle and cube |
| Averaging and clique reconciliation | Prompt 1 Theorem 4.5 | `GroupAveraging.lean` plus ordinary clique proof | symmetric examples |
| Global compatible perturbation | Prompt 1 Theorem 4.6 | pseudoinverse/range transfer | explicit radius |

## Prompt 2 covariance and product closeout

The authoritative Prompt 2 proof is
`pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`.

| Mandatory item | Mathematical proof | Lean support | Exact regression |
|---|---|---|---|
| Quadratic covariance identity | Prompt 2 Theorem 1.1 | `jumpGenerator_quadratic_covariance_identity` | Platonic direct residuals |
| Shifted quadratic target | Prompt 2 Theorem 1.2 | `quadratic_target_eigen_iff` | exact target checks |
| Trace-free form space | Prompt 2 Theorem 2.1 | trace-free contraction | exact constraint matrices |
| Sampling factorization | Prompt 2 Theorem 2.2 | covariance identity, kernel/range lemmas | `R=(G+2dI)S` |
| Genuine sampled space and dimension | Prompt 2 Theorem 2.2 | `sampledRestriction_finrank`, `sampledRange_exact_eq_range_inf_ker` | exact ranks and kernels |
| Positive axial rigidity | Prompt 2 Theorems 3.1–3.2 | axial coefficient, row-scaling iff | Platonic row scaling |
| Regular-simplex sharpness | Prompt 2 Corollary 3.3 | ordinary exact construction | closeout audit, `d=2,...,10` |
| Corrected positive equivariant rigidity | Prompt 2 Theorem 4.1 | ordinary representation proof using formalized covariance algebra | signed pentagon adversary |
| Signed pentagon counterexample | Prompt 2 Counterexample 4.2 | not separately formalized | exact `Q(sqrt(5))` generator, rank, discriminant |
| Exact Platonic classifications | Prompt 2 Section 5.1 | general finite algebra | existing exact audit |
| Four-point signed restoration | Prompt 2 Section 5.2 | ordinary matrix proof | exact sampled dimension and forced rate |
| Bilinear product identity | Prompt 2 Theorem 6.1 | `jumpGenerator_product_identity_gamma` | exact algebra audit |
| Arbitrary shifted product residual | Prompt 2 Theorem 6.2 | `jumpGenerator_shifted_product_residual`, `shifted_product_target_iff` | exact symbolic identity |
| Additive product resonance | Prompt 2 Theorem 6.2 | `additive_product_resonance_iff` | exact symbolic identity |
| Centered square resonance | Prompt 2 Theorem 6.2 | `centered_square_resonance_iff` | exact symbolic identity |
| Uncentered positive obstruction | Prompt 2 Theorem 6.2 consequences | `uncentered_square_resonance_iff_zero_gamma`, `uncentered_square_resonance_forces_value_zero` | `c=0` assertion |
| Boolean centered square | Prompt 2 Counterexample 6.3 | general resonance theorem applies | exact four-state matrix |
| Semigroup variance and converse | Prompt 2 Theorem 7.1 | ordinary finite matrix-semigroup proof | Boolean exact identity |
| Jensen equality support | Prompt 2 Theorem 7.2 | standard external theorem | positive Boolean variance |
| Spherical eigenvalue shift | Prompt 2 Section 8 | arithmetic | exact integer assertion |
| `S^2` table `ell=1,...,6` | Prompt 2 Section 8 | not a Lean claim | closeout audit exact rows |
| Pell arithmetic and hierarchy verdict | Prompt 2 Section 9 | ordinary arithmetic/kill-criterion analysis | existing and closeout assertions |
| Abstract equal-rate/equal-loss propagation | `GlobalLossRigidity.lean` | three named Lean theorems | build and nanoda |
| Prompt 3 spherical specialization/classification/near-rigidity | `PROMPT3_READINESS_HANDOFF.md` | not begun | not part of closeout |

## Verification and provenance

- focused axiom report: `AFPBarrier/PureMathAxiomAudit.lean`;
- existing covariance audit:
  `pure_math/covariance/quadratic_covariance_audit.py`;
- corrective closeout audit:
  `pure_math/covariance/prompt2_closeout_audit.py`;
- Prompt 2 workflow: `.github/workflows/afp-quadratic-covariance.yml`;
- Prompt 1 compatibility workflow:
  `.github/workflows/afp-spherical-feasibility.yml`;
- repository-wide workflow: `.github/workflows/afp-pure-math.yml`;
- closeout audit: `docs/PROMPT2_CLOSEOUT_AUDIT.md`;
- Prompt 3 handoff: `docs/PROMPT3_READINESS_HANDOFF.md`.

All workflows reject `sorry`, `admit`, and `sorryAx`; the closeout policy scans
anchored declarations for both singular `axiom` and plural `axioms` and tests
both spellings deterministically. `sorryAx` is absent from the independent
nanoda permitted-axiom list.
