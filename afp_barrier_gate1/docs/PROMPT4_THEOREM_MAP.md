# Prompt 4 theorem-to-proof map

The authoritative ordinary proof is:

```text
pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md
```

The final paper hierarchy is:

```text
pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md
```

| Prompt 4 mandatory item | Ordinary proof | Lean support | Exact regression | Claim status |
|---|---|---|---|---|
| Exact polar-rate formula | Prompt 4 Section 1, inherited exact product formulas | `squarePolarRateFromStep`; baseline `squarePolar_rate_formula` | direct exact expression | PROVED |
| Polar-rate expansion coefficients | Theorem 1.2 | `cscSquaredTruncation_rate_identity`, `squarePolarRateMainStep_grid` | SymPy exact series equality | PROVED / LEAN COEFFICIENT ALGEBRA |
| Uniform polar-rate remainder | Lemma 1.1 and Theorem 1.2 | no analytic infinite-series formalization | exact rational tail/transfer constants | PROVED / ORDINARY ANALYSIS |
| Polar-quality exact formula | equation (1.3) | `squarePolarQualityFromStep_formula` | direct exact simplification | PROVED / LEAN |
| Polar-quality expansion and remainder | Theorem 1.3 | `squarePolarQualityMainStep_grid` | exact coefficient and rational bound checks | PROVED |
| Fixed graph-class polar uniqueness | Theorem 2.1 | `squarePolar_rates_forced`, `squarePolar_totalRate_forced` | exact three-equation solve | PROVED / LEAN |
| Exact graph-class minimax value | Corollary 2.2 plus existing attaining construction/rate maximum | forced lower bound plus inherited `equalAngleGrid_squareRingRate_le_polar` | exact formula | PROVED / SHARP |
| Quartic lower bound and sharp leading constant | Corollary 2.2 | `squarePolar_forced_quartic_lower` plus inherited grid bound | exact coefficient check | PROVED / SHARP |
| Universal inverse-quadratic rate barrier | Theorem 3.1 | `universal_rate_lower_of_defect_upper`; inherited generator theorem | exact algebra | PROVED / LEAN |
| Quasi-uniform loss-window transfer | Theorem 3.2 | inherited `sphericalNet_peak_rate_defect_bounds*` | exact constants | PROVED CONDITIONAL TRANSFER |
| Positive Delaunay family existence | Prompt 4 Section 3 boundary | not project-formalized | none | EXTERNAL |
| Well-posed extremal class | Section 4 definition | no structure formalization | exact normalization check | PROVED DEFINITION |
| Extremal positive lower bound | Theorem 4.1 | `finiteExtremal_defect_lower` | exact `4/R` normalization | PROVED / LEAN |
| Finite-`K` minimizer existence | Theorem 4.2 | not separately formalized | finite-dimensional compactness audit | PROVED / ORDINARY COMPACTNESS |
| Product/quasi-uniform separation | Corollary 4.3 | inherited quartic bound | exact threshold check | PROVED, QUASI-UNIFORM SIDE CONDITIONAL ON EXTERNAL FAMILY |
| Feasible-cone projective reduction | Theorem 5.1 | finite special cases only | exact algebra | PROVED |
| Sliced LP anisotropy constant | Theorem 5.2 | no generic LP library | exact finite slice example | PROVED |
| LP dual anisotropy certificate | Theorem 5.2 | relies on standard finite LP duality | exact sign/certificate audit | PROVED / EXTERNAL DUALITY INPUT |
| Cone equality characterization | Corollary 5.3 | follows from weighted variance | sharp examples | PROVED |
| Two-direction sharp anisotropy | Example 5.4 | `twoLossQuality_sub_one` | exact identity | PROVED / LEAN |
| Product-pole cone anisotropy | Example 5.5 | forced polar algebra | exact evaluation | PROVED |
| Delsarte/Gegenbauer branch | Section 6.1 | none | alias adversaries | BLOCKED |
| Bakry--Émery branch | Section 6.2 | existing product identities | Boolean/positive-curvature warnings | KILLED FOR PROMPT 4 |
| Compact homogeneous spaces | Section 6.3 | none | no strengthening | DEFERRED |
| Discrete transport metrics | Section 6.4 | none | metric-selection warning | DEFERRED |
| Reduced-ring perfect-matching obstruction | Section 6.5 | `biregular_interRing_incidence`, `perfectMatching_ringCounts_eq` | exact incidence check | PROVED FOR STATED COUPLING CLASS |
| Formal discrete geometry boundary | Section 6.6 | `SharpProductBarriers.lean` only | source-policy audit | ACCEPTED / BOUNDED |
| Final theorem hierarchy | `FINAL_PURE_MATH_THEOREM_PACKAGE.md` | aggregate imports and axiom audit | all exact Prompt 1–4 audits | PROVED SYNTHESIS |
| Exact assumptions table | `docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | n/a | adversarial review | CLAIM CONTROL |
| Counterexample catalogue | `docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | selected exact examples formalized | all deterministic audits | CLAIM CONTROL |
| Manuscript abstract | `docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | n/a | publication-boundary audit | MANUSCRIPT RECORD |

## Formal declaration list

```text
AFPBarrier.squarePolarQualityFromStep
AFPBarrier.squarePolarQualityFromStep_formula
AFPBarrier.squarePolar_rates_forced
AFPBarrier.squarePolar_totalRate_forced
AFPBarrier.squarePolar_forced_quartic_lower
AFPBarrier.cscSquaredTruncation
AFPBarrier.squarePolarRateMainStep
AFPBarrier.cscSquaredTruncation_rate_identity
AFPBarrier.squarePolarRateMainStep_grid
AFPBarrier.squarePolarQualityMainStep
AFPBarrier.squarePolarQualityMainStep_grid
AFPBarrier.universal_rate_lower_of_defect_upper
AFPBarrier.finiteExtremal_defect_lower
AFPBarrier.twoLossQuality_sub_one
AFPBarrier.biregular_interRing_incidence
AFPBarrier.perfectMatching_ringCounts_eq
```

These declarations are included in the focused axiom audit and the independent
nanoda declaration set. No infinite-series, compactness, or generic LP theorem
is represented as a project axiom.

## Verification files

```text
pure_math/barriers/prompt4_sharp_barrier_audit.py
.github/workflows/afp-prompt4-sharp-barriers.yml
AFPBarrier/PureMathAxiomAudit.lean
```

Compatibility workflows must also run the Prompt 4 exact audit and allow only
the new pure-math workflow/source/documentation paths.
