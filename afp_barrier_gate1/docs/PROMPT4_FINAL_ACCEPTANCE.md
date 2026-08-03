# Prompt 4 final acceptance candidate

## 1. Purpose

This documentation-only commit is the final Prompt 4 acceptance candidate. It
contains no theorem, Lean, exact-audit, workflow, transport, or production
source change. Its parent is the target branch after the Prompt 4 theorem merge
and documentation integration:

```text
parent_target_commit=9f8f273b1f592801aec0cc4794cf5f4688eb836f
parent_target_tree=911c0c41eeaa6a1749604d127a02ba6176333dc3
```

The candidate is created on the already-merged Prompt 4 development branch so
that every configured Prompt 1--4 compatibility workflow runs on one literal
commit. After all five workflows pass, the pure-math target may be advanced to
that exact tested commit by a non-forced fast-forward.

## 2. Accepted mathematical implementation

```text
prompt4_implementation_commit=ae5b4c7635f917ea7abb6feb58717cc0173b4cd7
prompt4_theorem_pr=24
prompt4_theorem_merge=d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
prompt4_theorem_merge_tree=e192275e48bf38bf899483e8c27c0c3a206edf64
prompt4_integration_record_pr=26
prompt4_integration_record_merge=9f8f273b1f592801aec0cc4794cf5f4688eb836f
prompt4_integration_record_tree=911c0c41eeaa6a1749604d127a02ba6176333dc3
```

The authoritative mathematical and claim-control files are listed in
`PROMPT4_INTEGRATION_RECORD.md`.

## 3. Verification already accepted

### Implementation head

| Workflow | Run | Job | Result |
|---|---:|---:|---|
| AFP Prompt 4 sharp barriers | `30765107178` | `91542306867` | SUCCESS |
| AFP Pure Mathematics | `30765107143` | `91542312702` | SUCCESS |
| AFP quadratic covariance | `30765107144` | `91542297973` | SUCCESS |
| AFP Prompt 3 rigidity | `30765107141` | `91542308937` | SUCCESS |
| AFP spherical feasibility | `30765107139` | `91542285021` | SUCCESS |

### Documentation integration head

| Workflow | Run | Job | Result |
|---|---:|---:|---|
| AFP Prompt 4 sharp barriers | `30765735617` | `91543994335` | SUCCESS |
| AFP Pure Mathematics | `30765735607` | `91543994260` | SUCCESS |
| AFP quadratic covariance | `30765735571` | `91543994288` | SUCCESS |
| AFP Prompt 3 rigidity | `30765735614` | `91543994329` | SUCCESS |
| AFP spherical feasibility | `30765735598` | `91543994153` | SUCCESS |

### Target after documentation integration

```text
workflow=AFP Pure Mathematics
run=30765972073
job=91544643283
result=SUCCESS
actual_head=9f8f273b1f592801aec0cc4794cf5f4688eb836f
actual_tree=911c0c41eeaa6a1749604d127a02ba6176333dc3
```

## 4. Final candidate policy

The final candidate must pass:

```text
AFP Prompt 4 sharp barriers
AFP Pure Mathematics
AFP quadratic covariance
AFP Prompt 3 rigidity
AFP spherical feasibility
```

on its literal SHA. Every run must include the full Lean build or appropriate
compatibility build, all exact Prompt 1--4 audits, source placeholder and
singular/plural user-axiom scans, independent nanoda validation, immutable
archive verification, pure-math-only scope verification, and `git diff
--check`.

The candidate's own SHA and tree cannot be embedded in this commit without a
self-referential hash problem. They are recorded after verification in the
merged PR #26 discussion and the final return.
