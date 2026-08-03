# Prompt 4 selective-salvage ledger

## Immutable starting point

This ledger belongs to the new, non-overwriting branch
`agent/afp-pure-math-p4-from-p3-8de4b948`.  The branch was created at the
verified Prompt-3 archive object
`8de4b94835137d1eaf32c14b626424f87d2e176d`, whose tree is
`350fc38359fa4c55666c9244c61890188c4b4f44`.

Prompt 2 and Prompt 3 are closed dependencies.  In particular, no old
Prompt-1, Prompt-2, or Prompt-3 file is eligible for salvage.  No commit from
the old Prompt-4 line may enter this branch's ancestry.

## Read-only source objects and mutable observations

| Object or ref | Observed value | Treatment |
|---|---|---|
| accepted old Prompt-4 snapshot | `ae5b4c7635f917ea7abb6feb58717cc0173b4cd7` | immutable read-only salvage object |
| old Prompt-4 merge snapshot | `d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994` | immutable read-only comparison object; never merge |
| `agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis` | `94aebf6578a43516cce4bb7c042fc57681c93890` | mutable observation; not a candidate base |
| `agent/afp-pure-math-p4-integration-record` | `83bf04b99a060658b0177f3373ea0869cb4f3447` | mutable observation; not a candidate base |

Movement of either mutable branch is informational.  Candidate integrity is
established by exact objects, ancestry, path scope, complete verification, and
remote exact-head equality.

Both immutable old commits have tree
`e192275e48bf38bf899483e8c27c0c3a206edf64`, and their trees are identical.
Neither old commit is an ancestor of the verified baseline or this branch.

## Candidate-file ledger

All blob identifiers below are from the accepted old snapshot `ae5b4c...`.
The workflow row remains candidate-ready until the dedicated exact-head gate
runs; every mathematical/documentation row has completed independent audit.

| Old path | Old blob | Current Prompt-3 dependency/API | Independent proof audit | Adversarial audit | Port | Formal | Exact regression | Claim |
|---|---|---|---|---|---|---|---|---|
| `AFPBarrier/SharpProductBarriers.lean` | `bf5dddca9c5f7080f1675a4f1b015b86abe1a229` | byte-identical `EqualAngleRateMaximum` and `SphericalNetScaling`; current aggregate | finite algebra PASS | symmetry-assumption/API audit PASS | PORTED; stale unused import removed; raw transverse factor retained | bound to full Lean build and focused axiom artifact | Prompt-4 exact audit PASS | selected finite cores PROVED |
| `pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | `b443ac147599c8109ec6b5eb256e28a77935d84e` | verified P1--P3 notation and equal-angle construction | §§0--7 PASS after normalization repair | asymmetric-rate, compactness, cone, dual-sign, opposite-ray, and endpoint audits PASS | PORTED selectively with registered corrections | n/a | historical source rerun PASS; enhanced audit pending | P4.1--P4.10 PROVED; external/rejected boundaries explicit |
| `pure_math/barriers/prompt4_sharp_barrier_audit.py` | `bdde1e448f04fa63fff38c17bdc66d0a81ed982a` | retained P1--P3 exact suite | exact identities PASS | nonunit-`lambda`, LP-dual, unequal-ray, and incidence adversaries PASS | PORTED AND STRENGTHENED | n/a | local PASS and bound to the exact-head artifact | COMPUTATIONAL |
| `pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md` | `000c4980b091eb79a7e760584510a4093dc9263e` | verified P2/P3 theorem maps and corrected P4 results | synthesis PASS | normalization/opposite-ray/quasi-uniform wording PASS | REIMPLEMENTED selectively; old defective shorthand rejected | n/a | source-policy audit PASS | rowwise PROVED/EXTERNAL/COMPUTATIONAL/CONJECTURE/REJECTED |
| `docs/PROMPT4_APPROACH_REGISTRY.md` | `909c2d8f9b4e312fa50191a01e6a2c2a95e641ca` | replaced by this branch's `P4_APPROACH_REGISTRY.md` | mechanism audit PASS | independent audit families recorded | REIMPLEMENTED | n/a | n/a | route states separate from claim labels |
| `docs/PROMPT4_STAGE_REPORT.md` | `bc15cb4f59862f46c7171c7f8bfc22df7b3109c0` | replaced by `docs/P4_STAGE_REPORT.md` on current baseline | synthesis PASS | provenance/self-reference boundary PASS | REIMPLEMENTED | n/a | exact-head identifiers delegated to resolved record | rowwise controlled labels |
| `docs/PROMPT4_THEOREM_MAP.md` | `aae4ffb40b1883035557db6e7b1458f0cd3406b9` | replaced by current `P4_THEOREM_TO_FILE_MAP.md` | declaration map PASS | formal-boundary audit PASS | REIMPLEMENTED | exact declarations mapped | audit mapped | exact statuses |
| `docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | `21f1c9e1c35537b469edd3ae7a6c1a1bff19d17e` | current P1--P3 hypotheses plus corrected P4 boundaries | theorem-by-theorem PASS | silent-assumption adversary PASS | REIMPLEMENTED | formal scope explicit | source audit PASS | exact row status |
| `docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | `15d2dd0911df08463400fe8710f3f6a2d03de98f` | current permanent rejection catalogue | exact witness audit PASS | arbitrary-`lambda`, unequal-ray, `d=1`, and incidence additions PASS | REIMPLEMENTED and extended | formal boundary explicit | hostile regressions PASS | exact claim/witness statuses |
| `docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | `5fa87b9c9f828ec03d8deac819b5796ae14fe447` | current P2/P3 novelty boundary | synthesis PASS | acronym/overclaim audit PASS | REIMPLEMENTED | n/a | source audit PASS | main theorem central; P4 supporting |
| `docs/CLAIM_MATRIX.md` | `ee68baceb6f6d4efce2526d5708c6159e2beb683` | retain every verified P1--P3 row | P4 reconciliation PASS | exactly-one-status audit PASS | APPEND ONLY | n/a | source audit PASS | controlled statuses only |
| `docs/CONJECTURE_REGISTER.md` | `5c948f0e403f650b7e483c1e3e4597983c038cb4` | retain every verified P1--P3 boundary | P4 reconciliation PASS | rejected/deferred boundary PASS | APPEND ONLY | n/a | source audit PASS | controlled statuses only |
| `docs/PURE_MATH_PRIOR_ART_MAP.md` | `83980b86568197ab98a105cb47a8c7e0fb37542b` | current sampling-kernel-aware map | targeted primary-source audit PASS | novelty adversary PASS | APPEND ONLY | n/a | links/source scope PASS | EXTERNAL versus PROVED separated |
| `docs/THEOREM_TO_FILE_MAP.md` | `39eefdc9895584c788934bbb2a0d8d4f1f36e6f5` | current P2/P3 map | mapping audit PASS | preservation audit PASS | APPEND ONLY | n/a | P4 map linked | exact statuses in dedicated map |
| `pure_math/README.md` | `52d8ac7be8433447aeabf854546194e3503b51b3` | current P2/P3 README | synthesis PASS | correction-boundary PASS | APPEND ONLY | n/a | source audit PASS | supporting hierarchy explicit |
| `AFPBarrier.lean` | `eb3f253b5305b2aa7ac35d1310012d889bf777e7` | current aggregate imports are authoritative | preservation PASS | only one new import | ONE IMPORT ONLY | exact-head elaboration required | source scan PASS | n/a |
| `AFPBarrier/PureMathAxiomAudit.lean` | `41752a97ead38bec608af0c21372e52b84ba6c32` | current P1--P3 audit declarations are authoritative | preservation PASS | exact P4 prints only | P4 PRINTS ONLY | exact-head axiom audit required | source scan PASS | n/a |
| `.github/workflows/afp-prompt4-sharp-barriers.yml` | `e8938e26bc9bac7ad2cbfb3fadec86fed66442e6` | reimplement from verified current P3 workflow | old policy REJECTED | provenance adversary complete | REIMPLEMENTED AS `.github/workflows/afp-prompt4-from-p3-sharp-barriers.yml` | n/a | exact/Lean/final artifacts are mandatory | n/a |

## Explicitly rejected bulk content

The old tree deletes or replaces verified Prompt-2/3 modules, registries,
audits, theorem maps, and workflows.  Those changes are `REJECTED`.  Also
rejected are merge/cherry-pick import, generated logs, downloaded binaries,
`__pycache__`, `*.pyc`, `*.b64`, and integration metadata tied to the old
ancestry.

Every accepted row will be updated with the current declaration/file mapping
and exact audit result before finalization.

## Accepted-family audit: asymptotics and fixed graph

The analytic adversary independently recovered the positive cosecant tail
constant `352/30375 < 1/80`, rate-transfer constant
`180013/2359296 < 1/12`, and quality-transfer constant
`2063/7680 < 1/3`.  It checked the endpoint `N=2`, initially unequal
azimuthal rates, unequal masses, and nonreversible local rows.  No constant or
hypothesis failure was found.  The old obsolete Lean import
`SphericalQOneRigidity` is rejected; the Prompt-4 module uses nothing from it.

## Accepted-family audit: extremals and anisotropy

The rate-capped lower bound, fixed-`K` compactness argument, LP dual signs,
polar anisotropy, and incidence count survived independent derivation. The
port repairs rather than repeats these old wording defects:

- `Q_lambda=r*epsilon/lambda^2` for arbitrary normal moment, recovering the
  spherical quality at `lambda=2`;
- projectivization of the nonzero tangent-balanced cone, plus an exact
  bijection (not a scaling quotient) for each fixed-moment affine slice;
- an explicit nonempty-polytope hypothesis for the sliced minimum;
- the general tangent-magnitude-ratio formula, with the required half-weight
  result only at equal magnitudes; and
- quasi-uniform compatibility with the rate cap distinguished from membership
  in the complete constrained class.

The old final-package shorthand without the equal-weight hypothesis is
`REJECTED` by an exact spherical two-neighbour counterexample. The old
fixed-`lambda` normalization is likewise `REJECTED`; neither false wording is
salvaged.

## Lean old-to-new declaration map

| Old declaration | Current declaration | Port decision |
|---|---|---|
| `squarePolarQualityFromStep` | same | direct current-API port |
| `squarePolarQualityFromStep_formula` | same | direct current-API port |
| `squarePolar_rates_forced` | same | strengthened signature accepts the raw nonzero transverse factor and derives rate equality |
| `squarePolar_totalRate_forced` | same | strengthened consistently with the raw transverse equation |
| `squarePolar_forced_quartic_lower` | same | direct current-API port |
| `cscSquaredTruncation` | same | direct current-API port |
| `squarePolarRateMainStep` | same | direct current-API port |
| `cscSquaredTruncation_rate_identity` | same | direct current-API port |
| `squarePolarRateMainStep_grid` | same | direct current-API port |
| `squarePolarQualityMainStep` | same | direct current-API port |
| `squarePolarQualityMainStep_grid` | same | direct current-API port |
| `universal_rate_lower_of_defect_upper` | same | direct current-API port |
| `finiteExtremal_defect_lower` | same | direct current-API port |
| none | `projectiveQuality_from_fixedMoment` | new formal normalization repair |
| none | `twoLossWeightedQuality_sub_one` | new unequal-magnitude strengthening |
| `twoLossQuality_sub_one` | same | retained mandatory equal-weight corollary |
| `biregular_interRing_incidence` | same | arithmetic incidence core only |
| `perfectMatching_ringCounts_eq` | same | arithmetic perfect-matching core only |

The current aggregate adds one Prompt-4 import. The focused axiom audit
retains every baseline line in order and appends exact prints for every row in
this table.
