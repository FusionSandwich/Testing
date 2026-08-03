# Prompt 3–4 per-file reconciliation ledger

## Authority rules

The current accepted target is authoritative for every accepted Prompt 1,
Prompt 2, narrow Prompt 3, Prompt 4, workflow, claim-control, synthesis, and
provenance file.  The rich Prompt 3 source is authoritative only as a candidate
for its additive paths after mathematical, Lean, independent-kernel, and
exact-head verification.  PR #28 is audit-only.  User-supplied snapshots are
proof and test inputs, never automatic replacements.

The classifications used here are:

```text
TARGET_AUTHORITATIVE
RICH_P3_ADDITIVE
MANUAL_UNION_REQUIRED
AUDIT_ONLY
PROVENANCE_ONLY
REJECTED_GENERATED_ARTIFACT
```

## Rich Prompt 3 candidate paths relative to the accepted target

| Path | Classification | Exact rich-source blob at `f1ef5b3...` | Required handling |
|---|---|---|---|
| `.github/workflows/afp-global-rigidity.yml` | `RICH_P3_ADDITIVE` | `dceeef160d49724e1d3ff14b81026b5301172fd6` | retain the exact-head, plantri, Lean, nanoda, archive, and scope gate; add the new reconciliation branch trigger and strengthened regressions |
| `afp_barrier_gate1/AFPBarrier.lean` | `MANUAL_UNION_REQUIRED` | `f525b1c42c16827eecafc41ea73de5fa030a038d` | preserve every target import; add the three rich modules without removing the accepted narrow Prompt 3 or Prompt 4 modules |
| `afp_barrier_gate1/AFPBarrier/PureMathAxiomAudit.lean` | `MANUAL_UNION_REQUIRED` | `3084ea59df1b7adfdb7d7c89d63edd759cb44b77` | preserve every accepted theorem report and extend the Prompt 3 declaration slice |
| `afp_barrier_gate1/AFPBarrier/SphericalQEqualityRigidity.lean` | `RICH_P3_ADDITIVE` | `d2bef33b5383aef234717dbf718c50625515f743` | retain after targeted compilation; clean unreachable tactics without weakening statements |
| `afp_barrier_gate1/AFPBarrier/QuantitativeGlobalNearRigidity.lean` | `RICH_P3_ADDITIVE` | `736336869d8eef057b0393b2224792972f3c7d66` | repair the exact Lean failures in the weighted-product and positive-denominator algebra; retain `0<=delta<1` where required |
| `afp_barrier_gate1/AFPBarrier/QEqualityCovariance.lean` | `RICH_P3_ADDITIVE` | `7bd388be395f8157e343f11eae1134a4158810dd` | retain `0<ell<2` for tangent normalization and a separate antipodal `ell=2` boundary theorem/regression |
| `afp_barrier_gate1/docs/PROMPT3_GLOBAL_RIGIDITY_STAGE_REPORT.md` | `MANUAL_UNION_REQUIRED` | `77c9fc7ed351e2b46f88b6a6f5b1c4cf52c16c10` | update provenance, theorem status, angle certificate, Lean repairs, and final CI rather than restoring stale text |
| `afp_barrier_gate1/docs/PROMPT3_GLOBAL_RIGIDITY_THEOREM_MAP.md` | `MANUAL_UNION_REQUIRED` | `6e5a46ad6e06a82cf846d24057d17e02982ffddf` | update to the accepted union and final declaration map |
| `afp_barrier_gate1/pure_math/rigidity/APPROACH_REGISTRY.md` | `MANUAL_UNION_REQUIRED` | `664154b467be672420d41ddeb949fd8c4e4091ac` | preserve independent proof and adversarial routes; replace obsolete execution notes and mark the endpoint-angle route blocked |
| `afp_barrier_gate1/pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md` | `MANUAL_UNION_REQUIRED` | `4556eb60a28a5d096343aae9a3d2e6812d43f91d` | retain the richer all-orders theorem; port the explicit positive Gram/Heron determinant certificate and closed smallness threshold manually |
| `afp_barrier_gate1/pure_math/rigidity/THEOREM_REGISTRY.md` | `MANUAL_UNION_REQUIRED` | `6ed7149206fd708d9589b70d702d983dd121d2f2` | correct threshold and formalization statuses, then freeze hypotheses and dependencies |
| `afp_barrier_gate1/pure_math/rigidity/global_near_rigidity_audit.py` | `MANUAL_UNION_REQUIRED` | `011a33a7af987f2dc1f129fc7b5a19a58a5c191d` | retain exact/path/resistance tests and add zero-defect plus positive-width Platonic Gram/Heron box certificates |
| `afp_barrier_gate1/pure_math/rigidity/q1_covariance_audit.py` | `MANUAL_UNION_REQUIRED` | `d2b9a0332512c3d58a30c408718629499c02ade6` | retain antipodal regression and strengthen coordinate-eigenmap, nonzero-minor, anisotropy, and executable sampled-space checks |
| `afp_barrier_gate1/pure_math/rigidity/triangulation_counterexample_audit.py` | `RICH_P3_ADDITIVE` | `44b7aebea9a1d642f0c48026722a38623175951a` | use only source-pinned plantri in release CI; enumeration remains computational falsification, not the all-orders proof |

## Target-authoritative files requiring additive synthesis edits

The following files are not replaced by rich or audit-branch versions.  The
accepted target version is the only edit base, and changes are restricted to
acknowledging the stronger verified Prompt 3 companion results while preserving
all accepted Prompt 4 theorem statements and constants:

| Path | Classification |
|---|---|
| `afp_barrier_gate1/docs/CLAIM_MATRIX.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/CONJECTURE_REGISTER.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PURE_MATH_PRIOR_ART_MAP.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/THEOREM_TO_FILE_MAP.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/pure_math/README.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PURE_MATH_ASSUMPTIONS_TABLE.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PROMPT4_STAGE_REPORT.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PROMPT4_THEOREM_MAP.md` | `TARGET_AUTHORITATIVE` / `MANUAL_UNION_REQUIRED` |
| `afp_barrier_gate1/docs/PROMPT4_FINAL_ACCEPTANCE.md` | `TARGET_AUTHORITATIVE`; no theorem rewrite |
| `afp_barrier_gate1/docs/PROMPT4_INTEGRATION_RECORD.md` | `TARGET_AUTHORITATIVE`; provenance preserved |
| `afp_barrier_gate1/pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | `TARGET_AUTHORITATIVE`; theorem text preserved unless an audited defect is demonstrated |
| `afp_barrier_gate1/pure_math/barriers/prompt4_sharp_barrier_audit.py` | `TARGET_AUTHORITATIVE`; rerun unchanged at theorem level |
| `afp_barrier_gate1/AFPBarrier/SharpProductBarriers.lean` | `TARGET_AUTHORITATIVE`; rerun unchanged at theorem level |

## Audit-only and user-supplied inputs

| Input | Classification | Exact hash | Accepted use |
|---|---|---|---|
| PR #28 `P3_BRANCH_PROTECTION_RECORD.md` | `AUDIT_ONLY` | blob `fdab24bfe34a00f722bcf44529cacfed4d520183` | branch-safety and ancestry warning only |
| PR #28 `P3_SALVAGE_LEDGER.md` | `AUDIT_ONLY` | blob `6743691e1357deaae455df825a92cd2342ed9f0b` | manual re-derivation source for the `0<ell<2`, `0<=delta<1`, connectedness, and Gram/Heron corrections |
| PR #28 candidate ordinary theorem | `AUDIT_ONLY` | blob `650ee79c0d08139dabfb53dcd85a10864866ec51` | manually re-derive the positive Gram determinant and closed threshold; never merge its ancestry |
| User reconciliation contract | proof / repository input | SHA-256 `3ea1bd177b2087fa55608de8f8663207d9bdadd20ddef2146e1a5e6ba5dbae57` | controlling task contract |
| User ordinary-theorem snapshot | proof input | SHA-256 `64c3342554661ff35903e56b1821e58f52b1c759931632c07ede18c9a406f774` | compare line by line; retain only valid stronger material |
| User near-rigidity audit snapshot | test input | SHA-256 `69e9f32434fb21850112e7c7025a4dfa203ea16a2a3ee35b2ddbff9932a8fbdc` | port the zero-defect Platonic angle-box regression and any stronger valid checks |
| User covariance audit snapshot | test input | SHA-256 `5104fd3eff09a4e7d093c13d9ad3bb840eb8cb0ad151197c0cef43520faa2c7c` | retain explicit antipodal and executable sampling-boundary checks |
| PR #23 integration record | `PROVENANCE_ONLY` | branch head `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | historical pointer only; no source merge |

## Permanently rejected generated artifacts

The following are `REJECTED_GENERATED_ARTIFACT` and must be absent from the
committed tree and final changed-path list:

```text
__pycache__/
*.pyc
plantri binaries
temporary plantri source/checkouts
prompt3-triangulations-through-12.jsonl
base64 patch payloads
bootstrap/self-materializing workflows
local Lean exporter/checker build trees
compiled objects and logs outside workflow artifacts
```

The 9,150-record triangulation catalog is packaged as CI evidence with a digest;
it is not committed as theorem source.
