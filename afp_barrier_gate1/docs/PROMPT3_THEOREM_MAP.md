# Prompt 3 theorem-to-file map

## Authoritative mathematical files

```text
pure_math/rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md
pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md
```

## Lean support

```text
AFPBarrier/SphericalQOneRigidity.lean
AFPBarrier/GlobalLossRigidity.lean
AFPBarrier/LossVariance.lean
AFPBarrier/LossVarianceSharpness.lean
AFPBarrier/Quantitative.lean
AFPBarrier/PureMathAxiomAudit.lean
AFPBarrier.lean
```

## Exact audits

```text
pure_math/rigidity/prompt3_rigidity_audit.py
pure_math/falsification/claim_falsification_audit.py
pure_math/examples/exact_local_global_audit.py
pure_math/tests/test_spherical_feasibility.py
```

## Theorem map

| ID | Result | Ordinary proof | Lean declaration(s) | Exact regression |
|---|---|---|---|---|
| P3.1 | Coordinate exactness gives first loss moment two | rigidity theorem §0 | existing jump-generator algebra | five Platonic coordinate rows |
| P3.2 | Positive row rate for eigenvalue `-2` | rigidity theorem 1.1 | `jumpRate_pos_of_nonzero_eigenvalue_at_peak` | all exact examples |
| P3.3 | `Q_i>=1` and equality iff active loss `2/r_i` | rigidity theorem 1.1 | `sphericalQOne_active_loss` plus sharp variance theorem | all five Platonic rows |
| P3.4 | Active loss positivity and zero-loss exclusion | rigidity theorem 1.2 | `sphericalQOne_active_loss_pos`, `sphericalQOne_active_zero_loss_impossible` | coincident-endpoint boundary |
| P3.5 | Connected symmetric exact support has one row rate and one active loss | rigidity theorem 1.3 | `connected_sphericalQOne_rigidity` | connected Platonic graphs |
| P3.6 | Active antipode forces row rate one | rigidity theorem 1.2 | `sphericalQOne_active_antipode_forces_rate_one` | loss-two arithmetic |
| P3.7 | Equilateral face tangent-angle formula | rigidity theorem 2.2 | `equilateral_tangent_cosine` | `q=3,4,5` exact values |
| P3.8 | Regular triangulation Euler identity | rigidity theorem 2.2 | `regular_triangulation_euler_identity` | exact count arithmetic |
| P3.9 | Count triples for degree `3,4,5` | rigidity theorem 2.2 | three `degree_*_triangulation_counts` theorems | `(4,6,4)`, `(6,12,8)`, `(12,30,20)` |
| P3.10 | Degree-three graph is tetrahedral | rigidity theorem 2.2 | ordinary finite graph step | exact `K_4` certificate |
| P3.11 | Degree-four graph is octahedral | rigidity theorem 2.2 | ordinary finite graph step | complement perfect matching |
| P3.12 | Degree-five graph is icosahedral | `ICOSAHEDRAL_GRAPH_LEMMA.md` | no user axiom | exact link/two-ring certificate |
| P3.13 | Strict convex geometric embedding is regular Platonic | rigidity theorem 2.2 | standard Cauchy-rigidity transfer | exact standard coordinates |
| P3.14 | Cube and dodecahedron reject unrestricted classification | rigidity theorem §§2,7 | no Lean classification claim | exact Q=1 and face counts |
| P3.15 | Normalized `Q-1` variance identity | rigidity theorem 3.1 | existing variance modules | exact rational distributions |
| P3.16 | Multiplicative one-edge/shared-edge stability | rigidity theorem 4.1 | `shared_relative_center_cross_bounds` | exact `delta,kappa` case |
| P3.17 | Multiplicative path/diameter stability | rigidity theorem 4.1 | ordinary path induction | saturating chain calculation |
| P3.18 | Additive one-edge gap estimate | rigidity theorem 5.1 | `spherical_active_loss_deviation_sq_le_gap_div_rate` | exact `Delta` case |
| P3.19 | Additive center/path/diameter stability | rigidity theorem 5.1 | `shared_edge_centers_close` plus path induction | exact constants |
| P3.20 | Row-rate stability with an upper rate bound | rigidity theorem 5.1 | reciprocal-rate algebra | exact rational check |
| P3.21 | Conductance floors imply active-rate floors | rigidity theorem 5.2 | elementary definition transfer | exact rational check |
| P3.22 | Active-weight floor is necessary | rigidity theorem 6.1 | not a Lean claim | parameterized exact rare-edge family |
| P3.23 | Coordinate-space stability needs a rigidity margin | rigidity theorem 6.2 | conditional only | adversarial registry |

## Claim-control and prior-art files

```text
docs/CLAIM_MATRIX.md
docs/CONJECTURE_REGISTER.md
docs/PURE_MATH_PRIOR_ART_MAP.md
docs/PROMPT3_APPROACH_REGISTRY.md
docs/PROMPT3_STAGE_REPORT.md
docs/THEOREM_TO_FILE_MAP.md
pure_math/README.md
```

## Workflow

```text
.github/workflows/afp-prompt3-rigidity.yml
```

The dedicated workflow runs the exact Prompt 3 audit, all Prompt 1 and Prompt
2 compatibility audits, full Lean build, focused axiom audit, source policy,
independent nanoda verification, archive check, and path-scope check on the
literal head SHA.
