# Final pure-mathematics acceptance record

## Current status

`CANDIDATE_DOCUMENTATION_COMPLETE_AWAITING_FIRST_FULL_RUN`

This is the normative acceptance ledger for the integrated Prompt 1–4
pure-mathematics package.  Mathematical claims are controlled by the theorem
package and claim-control documents; this file controls exact repository
provenance and verification.

## Immutable and protected inputs

```text
repository=FusionSandwich/Testing
immutable_archive_branch=archive/afp-gate6-spatial-multigroup-verified
immutable_archive_sha=515f1aae6c20bd85711c90b5c1c21b4905252d01
target_branch=agent/afp-pure-math-p0-m1
target_baseline_sha=94aebf6578a43516cce4bb7c042fc57681c93890
rich_prompt3_reconciliation_head=19a5001158cb40fbb0adc92813cc3abd5dfa583d
verified_prompt2_completion_head=b11b7406e229f6fc8d018b36fa11b5506bd9d419
integration_branch=agent/afp-pure-math-final-integration-20260802
integration_merge_pr=32
integration_merge_commit=fbb482455dd51a961dbcbd897141c22f0ef57a15
```

The two source branches, the accepted target until final advancement, and the
transport archive are read-only during candidate verification.

## First complete candidate run

The following fields are intentionally populated by the acceptance-record
commit after the first six-workflow run succeeds on the documentation-complete
candidate.

```text
first_green_candidate_sha=PENDING
first_green_candidate_tree=PENDING
first_green_pr=PENDING
```

| Workflow | Run ID | Job ID | Conclusion |
|---|---:|---:|---|
| AFP spherical feasibility | PENDING | PENDING | PENDING |
| AFP quadratic covariance | PENDING | PENDING | PENDING |
| AFP Prompt 3 rigidity | PENDING | PENDING | PENDING |
| AFP global rigidity | PENDING | PENDING | PENDING |
| AFP Prompt 4 sharp barriers | PENDING | PENDING | PENDING |
| AFP Pure Mathematics | PENDING | PENDING | PENDING |

## Acceptance-record exact-head run

After the table above is filled, all six workflows run again on the resulting
documentation-only head.  Those runs verify that the committed evidence record
did not alter source behavior.  The resulting head cannot contain its own SHA,
tree, or post-commit workflow IDs.  They are therefore recorded in the final PR
discussion and repeated in the user-facing closeout.

```text
acceptance_record_head_sha=RECORDED_EXTERNALLY_AFTER_RUN
acceptance_record_head_tree=RECORDED_EXTERNALLY_AFTER_RUN
acceptance_record_workflow_ids=RECORDED_EXTERNALLY_AFTER_RUN
```

## Mandatory acceptance conditions

Every item must be true before the target ref moves.

- the target still equals `94aebf6578a43516cce4bb7c042fc57681c93890`;
- the candidate is a descendant of the target baseline;
- all six workflows are green on one literal candidate SHA;
- every exact Prompt 1–4 audit passes;
- the full aggregate Lean package builds with Lean 4.30 and pinned Mathlib;
- the focused axiom audit contains no `sorryAx`;
- the source scan finds no `sorry`, `admit`, `sorryAx`, singular `axiom`, or
  plural `axioms` declaration;
- independent nanoda checks succeed with only the permitted foundations;
- the archive branch resolves exactly to the immutable SHA;
- changed paths remain within pure-math source, documentation, and acceptance
  workflows;
- no bootstrap payload, generated plantri catalogue, checker worktree, or
  temporary materialization workflow remains;
- `git diff --check` and checkout cleanliness pass;
- the target update is non-forced and fast-forward only.

## Post-target verification

After non-forced advancement, the following are required and are recorded in
the final PR discussion.

```text
target_head_equals_tested_candidate=true
target_candidate_compare_status=identical
archive_recheck_sha=515f1aae6c20bd85711c90b5c1c21b4905252d01
target_push_six_workflow_conclusions=success
```

If the target differs from the baseline before advancement, this record is void
for integration purposes and a new descendant acceptance line is required.

## Final verdict rule

The final verdict becomes `ACCEPTED_AND_TARGET_VERIFIED` only after:

1. the first candidate table is filled from a green six-workflow run;
2. the acceptance-record head itself passes all six workflows;
3. the target is advanced non-forced to that exact head;
4. target and candidate compare as identical;
5. all target-push workflows are green; and
6. the archive remains byte-identical at the protected SHA.
