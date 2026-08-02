# Exact feasibility, covariance, rigidity, and sharp-barrier theorem-to-file map

The complete Prompt 1 mathematical proof is
`pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md`. “Lean support” identifies
the finite algebra formalized in the project; standard finite convex geometry,
Farkas, LP strong duality, semigroup, representation, topology, analytic
partial fractions, compactness, and convex-polyhedron facts are transferred
explicitly rather than misrepresented as project axioms.

The final paper hierarchy is assembled in
`pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md`.

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

## Prompt 3 spherical `Q=1` rigidity and stability

The authoritative ordinary proof is
`pure_math/rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md`. The direct degree-five
graph lemma is `pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md`.

| Mandatory item | Mathematical proof | Lean support | Exact regression |
|---|---|---|---|
| Coordinate eigenmap gives first active-loss moment two | Prompt 3 Section 0 | existing `JumpGenerator`/`SphereSpecialization` algebra | five Platonic coordinate checks |
| Local `Q_i>=1` and equality iff active loss `2/r_i` | Prompt 3 Theorem 1.1 | `sphericalQOne_active_loss`; imported sharp variance theorem | exact Platonic rows |
| Positive row rate at eigenvalue `-2` | Prompt 3 Theorem 1.1 | `jumpRate_pos_of_nonzero_eigenvalue_at_peak` | all exact examples |
| Active zero-loss exclusion | Prompt 3 Corollary 1.2 | `sphericalQOne_active_zero_loss_impossible` | coincident-edge boundary |
| Active antipode forces row rate one | Prompt 3 Corollary 1.2 | `sphericalQOne_active_antipode_forces_rate_one` | exact loss-two calculation |
| Connected common row rate and edge loss | Prompt 3 Theorem 1.3 | `connected_sphericalQOne_rigidity`; `GlobalLossRigidity.lean` | connected Platonic rows |
| Equilateral spherical-face angle formula | Prompt 3 Theorem 2.2 | `equilateral_tangent_cosine` | exact `q=3,4,5` values |
| Degree restriction `q in {3,4,5}` | Prompt 3 Theorem 2.2 | ordinary angle-sum transfer | exact integer audit |
| Euler/incidence identity and count triples | Prompt 3 Theorem 2.2 | `regular_triangulation_euler_identity`; three count theorems | exact `(V,E,F)` assertions |
| Tetrahedral graph lemma | Prompt 3 Theorem 2.2 | finite ordinary graph proof | `K_4` certificate |
| Octahedral graph lemma | Prompt 3 Theorem 2.2 | finite ordinary graph proof | complement perfect-matching certificate |
| Icosahedral graph lemma | `ICOSAHEDRAL_GRAPH_LEMMA.md` | no project axiom; direct finite proof | exact two-ring link certificate |
| Convex geometric congruence | Prompt 3 Theorem 2.2 | standard Cauchy-rigidity transfer with hypotheses checked | exact standard coordinates |
| Cube/dodecahedron unrestricted counterexamples | Prompt 3 Sections 2 and 7 | not a Lean classification claim | exact `Q=1`, nontriangular support |
| Normalized variance identity | Prompt 3 Theorem 3.1 | existing variance modules | exact rational examples |
| Multiplicative one-edge and shared-edge bounds | Prompt 3 Theorem 4.1 | `shared_relative_center_cross_bounds` plus local variance | exact `delta,kappa` case |
| Multiplicative path and diameter bounds | Prompt 3 Theorem 4.1 | ordinary finite path induction | exact saturating chain |
| Additive one-edge gap estimate | Prompt 3 Theorem 5.1 | `spherical_active_loss_deviation_sq_le_gap_div_rate` | exact constants |
| Additive shared-edge comparison | Prompt 3 Theorem 5.1 | `shared_edge_centers_close` | exact rational case |
| Additive path, diameter, and row-rate bounds | Prompt 3 Theorem 5.1 | ordinary finite path induction and reciprocal identity | exact constants |
| Conductance-floor transfer | Prompt 3 Corollary 5.2 | elementary rate definition | exact rational assertion |
| Necessity of active-weight floor | Prompt 3 Section 6.1 | not a Lean claim | exact parameterized rare-edge family |
| Necessity of connectivity/diameter/support symmetry | Prompt 3 Section 6.2 | adversarial argument registry | path and disconnected warnings |
| Coordinate-space stability boundary | Prompt 3 Section 6.2 | conditional singular-value transfer only | no unsupported promotion |

## Prompt 4 sharp barriers, extremals, and synthesis

The authoritative ordinary proof is
`pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md`. The final hierarchy is
`pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md`.

| Mandatory item | Mathematical proof | Lean support | Exact regression |
|---|---|---|---|
| Exact polar-rate and quality formulas | Prompt 4 equations (1.1)–(1.3) | `squarePolarQualityFromStep_formula`; inherited product formulas | direct exact simplification |
| Polar-rate coefficient extraction | Prompt 4 Theorem 1.2 | `cscSquaredTruncation_rate_identity`, `squarePolarRateMainStep_grid` | exact series equality |
| Polar-rate `N>=2` remainder | Lemma 1.1 and Theorem 1.2 | no infinite-series axiom/formalization | exact tail and rational transfer constants |
| Polar-quality coefficient/remainder | Prompt 4 Theorem 1.3 | `squarePolarQualityMainStep_grid` | exact series and bound constants |
| Asymmetric polar coordinate solve | Prompt 4 Theorem 2.1 | `squarePolar_rates_forced` | exact three-equation solve |
| Forced total polar rate | Prompt 4 Theorem 2.1 | `squarePolar_totalRate_forced` | exact expression |
| Fixed-graph exact minimax value | Prompt 4 Corollary 2.2 plus existing attaining construction | forced lower bound; inherited polar maximum | exact equality |
| Quartic lower bound and sharp `8/pi^4` | Prompt 4 Corollary 2.2 | `squarePolar_forced_quartic_lower` | exact leading coefficient |
| Universal inverse-quadratic rate implication | Prompt 4 Theorem 3.1 | `universal_rate_lower_of_defect_upper` | exact algebra |
| Quasi-uniform loss-window transfer | Prompt 4 Theorem 3.2 | inherited `SphericalNetScaling.lean` | exact constants |
| External Delaunay boundary | Prompt 4 Section 3 | none claimed | negative wording audit |
| Constrained extremal definition | Prompt 4 Section 4 | no structure formalization | parameter/control audit |
| Extremal lower bound `4/R` | Prompt 4 Theorem 4.1 | `finiteExtremal_defect_lower` | exact normalization |
| Fixed-`K` minimizer existence | Prompt 4 Theorem 4.2 | ordinary compactness only | closed-class audit |
| Product/linear-rate separation | Prompt 4 Corollary 4.3 | inherited quartic theorem | exact threshold |
| Projective feasible-cone reduction | Prompt 4 Theorem 5.1 | special finite algebra | exact examples |
| Sliced LP anisotropy invariant | Prompt 4 Theorem 5.2 | standard finite LP transfer, no generic LP library | exact finite slice |
| Anisotropy dual certificate | Prompt 4 equation (5.7) | no user axiom | exact sign audit |
| Equality and two-loss sharpness | Prompt 4 Corollary 5.3 and Example 5.4 | `twoLossQuality_sub_one` | exact identity |
| Polar cone anisotropy | Prompt 4 Example 5.5 | forced polar rates | exact evaluation |
| Delsarte branch | Prompt 4 Section 6.1 | none | sampling-alias adversaries | BLOCKED |
| `Gamma_2` branch | Prompt 4 Section 6.2 | existing product identities | positive-curvature warnings | KILLED |
| Homogeneous-space branch | Prompt 4 Section 6.3 | none | no strengthening | DEFERRED |
| Discrete transport branch | Prompt 4 Section 6.4 | none | metric-selection warning | DEFERRED |
| Reduced-ring incidence | Prompt 4 Section 6.5 | `biregular_interRing_incidence`, `perfectMatching_ringCounts_eq` | exact incidence |
| Final assumptions table | `docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | n/a | adversarial claim audit |
| Counterexample catalogue | `docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | selected finite examples | all exact audits |
| Manuscript abstract | `docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | n/a | publication-boundary audit |
| Prompt 4 approach registry | `docs/PROMPT4_APPROACH_REGISTRY.md` | n/a | independent-route records |
| Prompt 4 theorem map/stage report | `docs/PROMPT4_THEOREM_MAP.md`, `docs/PROMPT4_STAGE_REPORT.md` | n/a | provenance controls |

## Final claim-control records

```text
docs/CLAIM_MATRIX.md
docs/CONJECTURE_REGISTER.md
docs/PURE_MATH_PRIOR_ART_MAP.md
docs/PURE_MATH_ASSUMPTIONS_TABLE.md
docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md
pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md
```

## Verification and provenance

- focused axiom report: `AFPBarrier/PureMathAxiomAudit.lean`;
- Prompt 1 exact regressions:
  `pure_math/examples/exact_local_global_audit.py`,
  `pure_math/tests/test_spherical_feasibility.py`;
- covariance audits:
  `pure_math/covariance/quadratic_covariance_audit.py`,
  `pure_math/covariance/prompt2_closeout_audit.py`;
- Prompt 3 exact audit:
  `pure_math/rigidity/prompt3_rigidity_audit.py`;
- Prompt 4 exact audit:
  `pure_math/barriers/prompt4_sharp_barrier_audit.py`;
- Prompt 4 workflow:
  `.github/workflows/afp-prompt4-sharp-barriers.yml`;
- Prompt 3 compatibility workflow:
  `.github/workflows/afp-prompt3-rigidity.yml`;
- Prompt 2 compatibility workflow:
  `.github/workflows/afp-quadratic-covariance.yml`;
- Prompt 1 compatibility workflow:
  `.github/workflows/afp-spherical-feasibility.yml`;
- repository-wide workflow:
  `.github/workflows/afp-pure-math.yml`.

All workflows reject `sorry`, `admit`, and `sorryAx`; the policy scans anchored
declarations for both singular `axiom` and plural `axioms`. `sorryAx` is absent
from every independent nanoda permitted-axiom list. Exact CI heads and job
identifiers belong in integration records, not in mathematical proofs.
