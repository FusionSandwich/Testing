# AFP publication program — Papers I–III boundary and source inventory

## 1. Normative paper matrix

| Paper | Working subject | Flagship result | Owned theorem IDs | Explicit exclusions |
|---|---|---|---|---|
| Paper I | Positive spherical eigenmap generators: local feasibility and reversible shared-edge compatibility | exact indexed local spherical feasibility plus the global shared-conductance cone/Farkas theory with quantitative margins and sparse obstructions | I-L1–I-L4, I-G1–I-G4 | sampled quadratic factorization; global `Q=1` classification; product-grid barriers |
| Paper II | Genuine sampled quadratic exactness and structural rigidity | `R_X=(L+2dI)S_X` and the resulting genuine sampled-space formula, alias theorem, and sharp positive rigidity | II-Q1–II-Q5, II-P1 | generic graph-design existence; local feasibility as flagship; `Q=1` geometry; Prompt 4 |
| Paper III | Equality/near-rigidity geometry, covariance interaction, and sharp graph barriers | restricted global `Q=1` classification with explicit near-rigidity, coupled to the sharp product-graph/extremal obstruction theory | III-R1–III-R6, III-C1–III-C4, III-B1–III-B3, III-E1, III-A1, III-I1 | unrestricted Platonic classification; coordinate stability without margin; optimal constants; finite enumeration as proof |

The local variance identity supports Paper III but is not its flagship. Paper II retains the central program theorem. Paper III is a companion and extension paper, not a replacement for Paper II.

## 2. Shared definitions owned once

| Definition or convention | Canonical owner | Other-paper use |
|---|---|---|
| finite jump generator and negative sign convention | shared preliminaries / Paper I | cited by Papers II–III |
| positive masses and shared conductances | Paper I | cited when Papers II–III invoke reversibility |
| carré du champ and product identity | shared preliminaries / Paper II | cited by Paper III |
| sampling map `S_X`, kernel `K_X`, residual `R_X` | Paper II | cited in Paper III covariance section |
| spherical losses, rate, defect, `Q`, normalized weights | Paper III | Paper I may cite only for comparisons |
| formal/source provenance and axiom policy | shared reproducibility appendix | all papers |

Definitions must not be independently renormalized in different papers.

## 3. Formal Lean source inventory

`A` means shared foundational appendix, `I`, `II`, and `III` identify the consuming paper.

| Path | Use |
|---|---|
| `afp_barrier_gate1/AFPBarrier.lean` | A aggregate import |
| `afp_barrier_gate1/AFPBarrier/JumpGenerator.lean` | A, I, II, III |
| `afp_barrier_gate1/AFPBarrier/ImplementationConvention.lean` | A, I |
| `afp_barrier_gate1/AFPBarrier/NormalizationAudit.lean` | A, I, II, III |
| `afp_barrier_gate1/AFPBarrier/ForwardAdjoint.lean` | A, I, II |
| `afp_barrier_gate1/AFPBarrier/ReversibleConductance.lean` | I, III |
| `afp_barrier_gate1/AFPBarrier/LocalSphericalFeasibility.lean` | I |
| `afp_barrier_gate1/AFPBarrier/AntipodalFeasibility.lean` | I, III boundary |
| `afp_barrier_gate1/AFPBarrier/SphericalFeasibilityAlgebra.lean` | I |
| `afp_barrier_gate1/AFPBarrier/ExactLocalRows.lean` | I |
| `afp_barrier_gate1/AFPBarrier/Quantitative.lean` | I |
| `afp_barrier_gate1/AFPBarrier/QuantitativeSphericalFeasibility.lean` | I |
| `afp_barrier_gate1/AFPBarrier/QuantitativeExactLocal.lean` | I |
| `afp_barrier_gate1/AFPBarrier/SharedEdgeEquilibrium.lean` | I |
| `afp_barrier_gate1/AFPBarrier/GlobalSharedEdgeDuality.lean` | I |
| `afp_barrier_gate1/AFPBarrier/DualCertificate.lean` | I |
| `afp_barrier_gate1/AFPBarrier/GroupAveraging.lean` | I, II comparator |
| `afp_barrier_gate1/AFPBarrier/CompleteGraph.lean` | I |
| `afp_barrier_gate1/AFPBarrier/ScalingCompatibility.lean` | I |
| `afp_barrier_gate1/AFPBarrier/SphereSpecialization.lean` | I, III |
| `afp_barrier_gate1/AFPBarrier/NoGo.lean` | A, II counterexample boundary |
| `afp_barrier_gate1/AFPBarrier/DiffusionProperty.lean` | II |
| `afp_barrier_gate1/AFPBarrier/QuadraticCovariance.lean` | II |
| `afp_barrier_gate1/AFPBarrier/LossVariance.lean` | III |
| `afp_barrier_gate1/AFPBarrier/LossVarianceSharpness.lean` | III |
| `afp_barrier_gate1/AFPBarrier/GlobalLossRigidity.lean` | III |
| `afp_barrier_gate1/AFPBarrier/SphericalQOneRigidity.lean` | III narrow accepted package |
| `afp_barrier_gate1/AFPBarrier/SphericalQEqualityRigidity.lean` | III rich equality transfer |
| `afp_barrier_gate1/AFPBarrier/QuantitativeGlobalNearRigidity.lean` | III |
| `afp_barrier_gate1/AFPBarrier/QEqualityCovariance.lean` | II–III interface |
| `afp_barrier_gate1/AFPBarrier/EqualAngleGeometry.lean` | III product-family geometry |
| `afp_barrier_gate1/AFPBarrier/EqualAngleEdges.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleDotProducts.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleConnectivity.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleQuadrature.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleProduct.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleGrid.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleAsymptotics.lean` | III |
| `afp_barrier_gate1/AFPBarrier/EqualAngleRateMaximum.lean` | III |
| `afp_barrier_gate1/AFPBarrier/SphericalNetScaling.lean` | III |
| `afp_barrier_gate1/AFPBarrier/QuasiUniformLossBounds.lean` | III |
| `afp_barrier_gate1/AFPBarrier/SharpProductBarriers.lean` | III |
| `afp_barrier_gate1/AFPBarrier/PureMathAxiomAudit.lean` | A formal acceptance |

Transport-specific modules are not manuscript sources for Papers I–III even though the repository aggregate may build them. They remain outside the publication boundary.

## 4. Ordinary proof and synthesis inventory

| Path | Paper / role |
|---|---|
| `afp_barrier_gate1/pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` | Paper I primary proof |
| `afp_barrier_gate1/pure_math/covariance/QUADRATIC_COVARIANCE_DERIVATION.md` | Paper II derivation |
| `afp_barrier_gate1/pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md` | Paper II primary theorem |
| `afp_barrier_gate1/pure_math/rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md` | Paper III narrow exact package |
| `afp_barrier_gate1/pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md` | Paper III combinatorial proof |
| `afp_barrier_gate1/pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` | Paper III rich primary proof |
| `afp_barrier_gate1/pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | Paper III barrier/extremal proof |
| `afp_barrier_gate1/pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md` | cross-paper synthesis |
| `afp_barrier_gate1/pure_math/README.md` | source navigation |
| `afp_barrier_gate1/pure_math/APPROACH_REGISTRY.md` | Paper I/shared approach history |
| `afp_barrier_gate1/pure_math/rigidity/APPROACH_REGISTRY.md` | Paper III approach history |
| `afp_barrier_gate1/pure_math/rigidity/THEOREM_REGISTRY.md` | Paper III source registry |

## 5. Deterministic test and exact-example inventory

| Path | Paper / exact role |
|---|---|
| `afp_barrier_gate1/pure_math/falsification/claim_falsification_audit.py` | all papers; five Platonic `Q=1`, sampling aliases, polar coefficient, order-dependence warning |
| `afp_barrier_gate1/pure_math/examples/exact_local_global_audit.py` | Paper I; exact rows and shared-edge certificates |
| `afp_barrier_gate1/pure_math/tests/test_spherical_feasibility.py` | Paper I regression |
| `afp_barrier_gate1/pure_math/covariance/quadratic_covariance_audit.py` | Paper II; exact factorization, ranks, Platonic aliases, signed square |
| `afp_barrier_gate1/pure_math/covariance/prompt2_closeout_audit.py` | Paper II; positivity correction, centered resonance, low-degree table |
| `afp_barrier_gate1/pure_math/rigidity/prompt3_rigidity_audit.py` | Paper III narrow package |
| `afp_barrier_gate1/pure_math/rigidity/triangulation_counterexample_audit.py` | Paper III; source-pinned 9,150-map hostile census and exact embeddings |
| `afp_barrier_gate1/pure_math/rigidity/global_near_rigidity_audit.py` | Paper III; exact constants, path/resistance, Gram/Heron boxes |
| `afp_barrier_gate1/pure_math/rigidity/q1_covariance_audit.py` | Paper II–III interface; antipode, weighted octahedron, sampled determinant |
| `afp_barrier_gate1/pure_math/barriers/prompt4_sharp_barrier_audit.py` | Paper III; asymptotic, forced-rate, extremal, LP, ring fixtures |

Exact example families that must remain active:

```text
tetrahedron;
octahedron;
cube;
icosahedron;
dodecahedron;
regular simplex in every dimension;
four-cardinal signed square;
signed regular pentagon;
Boolean centered square;
sparse four-cycle/cube Farkas examples;
rare-active-edge and long-path families;
two-state antipodal boundary;
positive weighted-octahedral family;
product-grid pole;
biregular/perfect-matching ring fixtures.
```

## 6. Report, claim-control, and provenance inventory

### Shared claim controls

```text
afp_barrier_gate1/docs/CLAIM_MATRIX.md
afp_barrier_gate1/docs/CONJECTURE_REGISTER.md
afp_barrier_gate1/docs/PURE_MATH_ASSUMPTIONS_TABLE.md
afp_barrier_gate1/docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
afp_barrier_gate1/docs/PURE_MATH_PRIOR_ART_MAP.md
afp_barrier_gate1/docs/THEOREM_TO_FILE_MAP.md
afp_barrier_gate1/docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md
afp_barrier_gate1/docs/FINAL_PURE_MATH_ACCEPTANCE.md
```

### Historical and stage records consumed for provenance

```text
afp_barrier_gate1/docs/P0_M1_SPHERICAL_FEASIBILITY_STAGE_REPORT.md
afp_barrier_gate1/docs/P0_M1_SPHERICAL_FEASIBILITY_INTEGRATION_RECORD.md
afp_barrier_gate1/docs/SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md
afp_barrier_gate1/docs/SPHERICAL_FEASIBILITY_OPTIMAL_VALUE_SENSITIVITY.md
afp_barrier_gate1/docs/SPHERICAL_FEASIBILITY_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT1_CLOSEOUT_AUDIT.md
afp_barrier_gate1/docs/PROMPT2_CLOSEOUT_AUDIT.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_INTEGRATION_RECORD.md
afp_barrier_gate1/docs/PROMPT3_READINESS_HANDOFF.md
afp_barrier_gate1/docs/PROMPT3_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT3_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT3_APPROACH_REGISTRY.md
afp_barrier_gate1/docs/PROMPT3_GLOBAL_RIGIDITY_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT3_GLOBAL_RIGIDITY_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT3_FINAL_INTEGRATION_RECORD.md
afp_barrier_gate1/docs/PROMPT4_APPROACH_REGISTRY.md
afp_barrier_gate1/docs/PROMPT4_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT4_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT4_FINAL_ACCEPTANCE.md
afp_barrier_gate1/docs/PROMPT4_INTEGRATION_RECORD.md
afp_barrier_gate1/docs/PROMPT4_REACCEPTANCE_AFTER_P3_RECONCILIATION.md
afp_barrier_gate1/docs/P3_P4_APPROACH_REGISTRY.md
afp_barrier_gate1/docs/P3_P4_THEOREM_AND_HYPOTHESIS_REGISTRY.md
afp_barrier_gate1/docs/P3_P4_PROTECTED_REF_LEDGER.md
afp_barrier_gate1/docs/P3_P4_FILE_RECONCILIATION_LEDGER.md
afp_barrier_gate1/docs/P3_P4_BRANCH_PRESERVATION_REGISTRY.md
```

These reports are state evidence. They do not replace the ordinary proof sources.

## 7. Workflow inventory

| Workflow | Role |
|---|---|
| `.github/workflows/afp-spherical-feasibility.yml` | Paper I and complete-gate regression |
| `.github/workflows/afp-quadratic-covariance.yml` | Paper II and complete-gate regression |
| `.github/workflows/afp-prompt3-rigidity.yml` | Paper III narrow/rich regression |
| `.github/workflows/afp-global-rigidity.yml` | Paper III full exact gate |
| `.github/workflows/afp-prompt4-sharp-barriers.yml` | Paper III barrier/extremal regression |
| `.github/workflows/afp-pure-math.yml` | repository-wide pure-math gate |
| `.github/workflows/afp-publication-program-baseline.yml` | exact documentation-head publication baseline gate |
| `.github/workflows/afp-barrier-gate1.yml` | historical P0/M1 provenance only |

The publication workflow executes a runtime copy of the already accepted final gate with only its changed-path allowlist extended for this directory and the workflow itself. It does not modify accepted source or weaken any mathematical, Lean, nanoda, archive, or generated-artifact check.

## 8. Accepted artifact inventory

### Implementation-head evidence retained for provenance

| Workflow | Run | Job | Artifact | Digest |
|---|---:|---:|---:|---|
| global | `30786676428` | `91601410647` | `8845656108` | `197278974e92eceba0a085589e8f65bfe57fa070541bda262922aaa8ac504323` |
| Prompt 3 | `30786676430` | `91601410209` | `8845563275` | `3d5d843579f0ebd35aee1c46f74b38633450762c440ed991b2148bed02be500b` |
| Prompt 4 | `30786676446` | `91601410601` | `8845562691` | `6895b3a69d89b308764026d426bbd6880d741e99f6ea5cc1cc1655c2c7a66583` |
| pure math | `30786676485` | `91601410654` | `8845560227` | `61aabb264e12ef51f06e6faceb1e98b07379f4257c174b9043705f34e9b2163b` |
| covariance | `30786676435` | `91601410388` | `8845700261` | `9427337c2f738e949fc975ddada5c720e32c252808b2e68094e1d749eb277726` |
| feasibility | `30786676453` | `91601410179` | `8845653320` | `cec08bf40b498057cd162f45aeaddf90a4174d2091f8b55f610a3623dd800e3f` |

### Authoritative target-head evidence

| Workflow | Run | Job | Artifact | Digest |
|---|---:|---:|---:|---|
| global | `30787796465` | `91604757325` | `8845980973` | `6ac15f3a25ae850360299654fd819fb176b1fadc7a1c6f65b302992a0af70c6d` |
| Prompt 3 | `30787796476` | `91604757297` | `8846031784` | `3f60f3ec5051e16dec23d77b5c693e3395bd507d026a5721741e5be1f4d57c9c` |
| Prompt 4 | `30787796470` | `91604757188` | `8846032007` | `77842799da18e8c40f40d157f55d7d6d64ae7f7fa9b3fe52e9fbd88e3bbe000e` |
| pure math | `30787796462` | `91604757087` | `8846104954` | `dd8080263e5ea73cd5379aa955b566fe9e3e716aa6b009efb52741d01a7415e5` |
| covariance | `30787796482` | `91604757171` | `8845986588` | `dd0d512872a194d211ba8a20d3a5f8bb8e36870f89de5c37bff86f442c986768` |
| feasibility | `30787796469` | `91604757060` | `8845966495` | `bd116f9a75ad95d0115192eefdf819947aae974ea2e00f609e0b9e87ea3a8e55` |

The publication-baseline workflow artifact is appended to the PR discussion after the new literal head is green.

## 9. Cross-paper duplication policy

A theorem is stated in full only in its owner paper. Other papers may quote a named corollary with an exact cross-reference. Shared exact examples should be centralized in a common data/reproducibility appendix, but each paper must explain only the interpretation relevant to its theorem.

Mandatory non-duplication rules:

- Paper I does not advertise generic Farkas or local variance as novelty.
- Paper II does not repeat local construction theory as a second flagship.
- Paper III does not present the covariance form space without the Paper II sampling map.
- Prompt 4 barriers remain Paper III supporting theory and do not displace the sampled covariance flagship.
- computational catalogs and workflow metadata stay in reproducibility sections, not theorem statements.
