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

## Candidate-file ledger

All blob identifiers below are from the accepted old snapshot `ae5b4c...`.
`PENDING` means that the file has not yet been accepted on the current API.

| Old path | Old blob | Current Prompt-3 dependency/API | Independent proof audit | Adversarial audit | Port | Formal | Exact regression | Claim |
|---|---|---|---|---|---|---|---|---|
| `AFPBarrier/SharpProductBarriers.lean` | `bf5dddca9c5f7080f1675a4f1b015b86abe1a229` | `JumpGenerator`, `EqualAngle*`, `SphereSpecialization`, P2/P3 aggregate exports | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| `pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | `b443ac147599c8109ec6b5eb256e28a77935d84e` | verified P1--P3 notation and equal-angle construction | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `pure_math/barriers/prompt4_sharp_barrier_audit.py` | `bdde1e448f04fa63fff38c17bdc66d0a81ed982a` | retained P1--P3 exact suite | PENDING | PENDING | PENDING | n/a | PENDING | COMPUTATIONAL candidate |
| `pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md` | `000c4980b091eb79a7e760584510a4093dc9263e` | verified P2/P3 theorem maps and claim controls | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `docs/PROMPT4_APPROACH_REGISTRY.md` | `909c2d8f9b4e312fa50191a01e6a2c2a95e641ca` | replaced by this branch's `P4_APPROACH_REGISTRY.md` | PENDING | PENDING | REIMPLEMENT | n/a | n/a | PENDING |
| `docs/PROMPT4_STAGE_REPORT.md` | `bc15cb4f59862f46c7171c7f8bfc22df7b3109c0` | current P2/P3 finalization record | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `docs/PROMPT4_THEOREM_MAP.md` | `aae4ffb40b1883035557db6e7b1458f0cd3406b9` | replaced by current `P4_THEOREM_TO_FILE_MAP.md` | PENDING | PENDING | REIMPLEMENT | n/a | n/a | PENDING |
| `docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | `21f1c9e1c35537b469edd3ae7a6c1a1bff19d17e` | current P1--P3 hypotheses | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | `15d2dd0911df08463400fe8710f3f6a2d03de98f` | current permanent rejection catalogue | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | `5fa87b9c9f828ec03d8deac819b5796ae14fe447` | current P2/P3 novelty boundary | PENDING | PENDING | PENDING | n/a | PENDING | PENDING |
| `docs/CLAIM_MATRIX.md` | `ee68baceb6f6d4efce2526d5708c6159e2beb683` | retain every verified P1--P3 row | PENDING | PENDING | SELECTIVE | n/a | PENDING | PENDING |
| `docs/CONJECTURE_REGISTER.md` | `5c948f0e403f650b7e483c1e3e4597983c038cb4` | retain every verified P1--P3 boundary | PENDING | PENDING | SELECTIVE | n/a | PENDING | PENDING |
| `docs/PURE_MATH_PRIOR_ART_MAP.md` | `83980b86568197ab98a105cb47a8c7e0fb37542b` | current sampling-kernel-aware map | PENDING | PENDING | SELECTIVE | n/a | PENDING | PENDING |
| `docs/THEOREM_TO_FILE_MAP.md` | `39eefdc9895584c788934bbb2a0d8d4f1f36e6f5` | current P2/P3 map | PENDING | PENDING | SELECTIVE | n/a | PENDING | PENDING |
| `pure_math/README.md` | `52d8ac7be8433447aeabf854546194e3503b51b3` | current P2/P3 README | PENDING | PENDING | SELECTIVE | n/a | PENDING | PENDING |
| `AFPBarrier.lean` | `eb3f253b5305b2aa7ac35d1310012d889bf777e7` | current aggregate imports are authoritative | PENDING | PENDING | ONE IMPORT ONLY | PENDING | PENDING | n/a |
| `AFPBarrier/PureMathAxiomAudit.lean` | `41752a97ead38bec608af0c21372e52b84ba6c32` | current P1--P3 audit declarations are authoritative | PENDING | PENDING | P4 PRINTS ONLY | PENDING | PENDING | n/a |
| `.github/workflows/afp-prompt4-sharp-barriers.yml` | `e8938e26bc9bac7ad2cbfb3fadec86fed66442e6` | current exact P3 workflow policy | PENDING | PENDING | REIMPLEMENT | n/a | PENDING | n/a |

## Explicitly rejected bulk content

The old tree deletes or replaces verified Prompt-2/3 modules, registries,
audits, theorem maps, and workflows.  Those changes are `REJECTED`.  Also
rejected are merge/cherry-pick import, generated logs, downloaded binaries,
`__pycache__`, `*.pyc`, `*.b64`, and integration metadata tied to the old
ancestry.

Every accepted row will be updated with the current declaration/file mapping
and exact audit result before finalization.
