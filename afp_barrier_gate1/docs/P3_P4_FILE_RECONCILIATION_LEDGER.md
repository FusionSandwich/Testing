# Prompt 3–4 per-file reconciliation ledger

This ledger records the authority decision for every overlapping or manually reconciled path in the clean final-acceptance tree.

## Authority classes

```text
TARGET_AUTHORITATIVE
RICH_P3_ADDITIVE
MANUAL_UNION_REQUIRED
AUDIT_ONLY
PROVENANCE_ONLY
REJECTED_GENERATED_ARTIFACT
```

The accepted target at `94aebf6578a43516cce4bb7c042fc57681c93890` is authoritative for all Prompt 1, Prompt 2, narrow Prompt 3, Prompt 4, package, and baseline workflow content. PR #30 at `19a5001158cb40fbb0adc92813cc3abd5dfa583d` is authoritative only for the vetted additive rich Prompt 3 implementation and the documented synthesis union.

## Rich Prompt 3 additive source blobs

| Path | Class | Source blob | Treatment |
|---|---|---|---|
| `AFPBarrier.lean` | MANUAL_UNION_REQUIRED | `f525b1c42c16827eecafc41ea73de5fa030a038d` | target imports retained; rich modules appended |
| `AFPBarrier/PureMathAxiomAudit.lean` | MANUAL_UNION_REQUIRED | `430ac9de9e999ca8b566f83be37a02c7921182ea` | all prior reports retained; new finite declarations included |
| `AFPBarrier/SphericalQEqualityRigidity.lean` | RICH_P3_ADDITIVE | `d2bef33b5383aef234717dbf718c50625515f743` | retained |
| `AFPBarrier/QuantitativeGlobalNearRigidity.lean` | RICH_P3_ADDITIVE | `e6f4dc26113047915a5cb0563852d2cb77b75f31` | repaired source retained |
| `AFPBarrier/QEqualityCovariance.lean` | RICH_P3_ADDITIVE | `c5a8e48477e83cfa0bc30dae792db4a264533763` | non-antipodal theorem and antipodal boundary retained |
| `pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` | RICH_P3_ADDITIVE | `f419a9749aff58bb66248b120e0bd96dbe65637f` | Gram/Heron route retained; old endpoint-product route rejected |
| `pure_math/rigidity/global_near_rigidity_audit.py` | RICH_P3_ADDITIVE | `b43cd8988c98b2a83d42cb535101b8122543e60d` | strengthened zero-defect and positive-width checks retained |
| `pure_math/rigidity/q1_covariance_audit.py` | RICH_P3_ADDITIVE | `a5e60028ea036d0f3973b44af9f194bbb4b65415` | antipodal and sampled-space checks retained |
| `pure_math/rigidity/triangulation_counterexample_audit.py` | RICH_P3_ADDITIVE | `44b7aebea9a1d642f0c48026722a38623175951a` | source-pinned 9,150-map hostile audit retained |
| `pure_math/rigidity/APPROACH_REGISTRY.md` | RICH_P3_ADDITIVE | `ecdbdcdd2e1e5de9f979d3915f5d4b14ee706028` | retained as Prompt 3 mechanism record |
| `pure_math/rigidity/THEOREM_REGISTRY.md` | RICH_P3_ADDITIVE | `04297a4d3ab40a00a74d3d2130b0f6eec92f1160` | retained and supplemented by the final combined registry |
| `docs/PROMPT3_GLOBAL_RIGIDITY_STAGE_REPORT.md` | RICH_P3_ADDITIVE | `b8dcb556215d2a7e3502f5b3ebe650e036102e0a` | retained |
| `docs/PROMPT3_GLOBAL_RIGIDITY_THEOREM_MAP.md` | RICH_P3_ADDITIVE | `eebe9d545f3f9de9dc4b398573e2864746439f4a` | retained |

## Claim-control and synthesis unions

| Path | Class | Reconciled blob | Rule |
|---|---|---|---|
| `docs/CLAIM_MATRIX.md` | MANUAL_UNION_REQUIRED | `380d781350d889d394752f2fac1dca0cb6ae4212` | target rows retained; corrected rich Prompt 3 rows appended |
| `docs/CONJECTURE_REGISTER.md` | MANUAL_UNION_REQUIRED | `80bfa56efef99cc0ead5bee06d0d8c4616427e2e` | no accepted Prompt 4 status removed |
| `docs/PURE_MATH_PRIOR_ART_MAP.md` | MANUAL_UNION_REQUIRED | `9fe149f71fe2db65b9dc0f6296e1523e7b30f5a9` | standard/external/new boundaries retained |
| `docs/THEOREM_TO_FILE_MAP.md` | MANUAL_UNION_REQUIRED | `c885ff2fb42073fa3bc4a40a6afd0248b3943cd1` | rich modules added without replacing accepted mappings |
| `pure_math/README.md` | MANUAL_UNION_REQUIRED | `47c1e0b501af2e5881af02b38f7fb095df0dea49` | final hierarchy retained |
| `pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md` | MANUAL_UNION_REQUIRED | `edecf3a22c9e6b71072598fd44be297144e49d60` | sampled covariance remains central; rich Prompt 3 is companion; Prompt 4 supporting |
| `docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | MANUAL_UNION_REQUIRED | `3d1963eaad7b1c38006cf7354db579f56540b725` | corrected publication boundary retained |
| `docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | MANUAL_UNION_REQUIRED | `ed84a558648f568bb1cf10f6ca515dfa6fc32c5b` | explicit triangulation, positivity, `delta<1`, and `0<ell<2` domains retained |
| `docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | MANUAL_UNION_REQUIRED | `2d3423757dbdd4258eef739364c2c11b6cfcfbd8` | cube, dodecahedron, antipodal, anisotropy, and finite-enumeration boundaries retained |
| `docs/PROMPT4_STAGE_REPORT.md` | MANUAL_UNION_REQUIRED | `a39a2b4240a67237ef76da840b943d239ad1f946` | true history: Prompt 4 was already closed and is revalidated |
| `docs/PROMPT4_THEOREM_MAP.md` | MANUAL_UNION_REQUIRED | `946cc983d2ed9a58b6f2fd53d95210fa199b94f5` | Prompt 4 theorem statements and exact constants unchanged |

## Manually re-derived corrections

No PR #28 commit is merged or cherry-picked. The following corrections were independently re-derived and are present in the PR #30 source blobs above:

1. `simpa [mul_comm]` resolves the weighted-product orientation in `pointwise_deviation_sq_le_eta_div_kappa`.
2. Adjacent-rate and incident-loss bounds are proved by multiplying numerator inequalities by nonnegative inverses rather than applying a mismatched division lemma.
3. The incident-loss theorem retains `0 <= delta < 1`.
4. Tangent-frame covariance is restricted to `0 < ell < 2`; `ell=2` is a separate antipodal radial boundary.
5. The endpoint-product angle enclosure is rejected on the required icosahedral box and replaced by a positive spherical Gram/Heron determinant certificate.
6. The weighted-octahedral sampled degree-two space is certified as `{0}` through the exact determinant of `P+2I`, not form-space rank alone.

## Target-authoritative content

Every path not explicitly listed as a rich or manual-union path is inherited unchanged from target tree `872828f5099aeb7df4e0ab871b9e881de4054a97`. In particular, all accepted Prompt 4 theorem sources, exact constants, historical acceptance records, and transport-independent baseline modules remain target-authoritative.

## Rejected generated and bootstrap artifacts

The clean tree contains none of the following:

```text
.github/*.b64
.github/workflows/afp-p3-p4-materialize.yml
.github/workflows/afp-p3-p4-targeted-lean.yml
__pycache__/
*.pyc
prompt3-triangulations-through-12.jsonl
compiled plantri binaries or source checkouts
_lean4export/
_nanoda_lib/
local log files
```

The six final workflow files are newly committed, read-only verification wrappers. They do not mutate repository refs or workflow files.

The literal final candidate SHA/tree, workflow run/job identifiers, artifact IDs/digests, final target SHA/tree, and post-integration workflow identifiers are recorded in the authoritative acceptance comment on the final reconciliation PR.
