# Prompt 2 and Prompt 3 finalization record

## Purpose and exact-binding convention

This is the tracked, documentation-only closeout certificate for Prompt 2 and
Prompt 3.  It makes no mathematical change to the audited Prompt-3 candidate.

In this record, `FINAL` means the unique commit that contains this record and
satisfies all of the following machine-checked equalities in the authoritative
green workflow run:

```text
git rev-parse HEAD = GITHUB_SHA
git ls-remote origin refs/heads/agent/afp-pure-math-p2-p3-final-closeout-c66f3229
  = GITHUB_SHA
c66f3229d0a89d97559535810c4ba09daf6e4e42 is an ancestor of GITHUB_SHA
```

`FINAL_TREE` means `FINAL^{tree}` in that run.  The workflow appends the
literal `FINAL`, `FINAL_TREE`, run, job, artifact, Lean-job, source-digest, and
mutable-observation values to a resolved copy of this record and uploads it as
an artifact.  PR #31 and the post-green Prompt-3 archive publish the same
literal values.

This indirection is logically necessary rather than a placeholder: a tracked
blob cannot contain the not-yet-computed tree and commit hashes to which that
blob contributes, and workflow run/artifact identifiers do not exist until
after the commit is pushed.  No commit is accepted merely through the symbolic
name `FINAL`; it is accepted only through the exact equalities and fully green
run above.

## Authoritative Prompt-2 completion

```text
branch:
  agent/afp-pure-math-p2-quadratic-covariance-completion
commit:
  31ea6a49f006df10ca633eafd6848ad43b51ac3f
tree:
  879b88de81eeb52ebb09373c2ccb77cb7cb7642c
workflow run:
  30760522011
jobs:
  exact-regressions SUCCESS
  lean-kernel      SUCCESS
Lean build:
  3107 jobs
exact artifact:
  ID 8837341400
  SHA-256 d538383e6be15a5930b5f6e3b49e8fe8a0895262c19ce05b5288da92d4742979
Lean/source artifact:
  ID 8837324993
  SHA-256 45720c2202fdd9b7de5af2533aba75154a211b0e6214ac1755d0432a79060d96
exact source tar SHA-256:
  d7ca753b1f33fa3bf8dfce4a71bf4a34a578c6f8c793afae8f60b743be1e413c
```

Prompt 2 is immutable input to this closeout.  Its create-if-absent archive
pointer is:

```text
archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49
  -> 31ea6a49f006df10ca633eafd6848ad43b51ac3f
```

Neither the Prompt-2 branch nor its source is changed by this closeout.

## Authoritative Prompt-3 mathematical candidate

```text
branch:
  agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49
draft PR:
  #28
mathematical candidate commit:
  c66f3229d0a89d97559535810c4ba09daf6e4e42
mathematical candidate tree:
  29d5e7f8f55479513a71dd457f9bd64c11b6df0f
prior workflow run:
  30771073146
Lean job:
  lean-kernel SUCCESS
  3110 jobs
  focused axiom audit: propext, Classical.choice, Quot.sound only
  no sorry, admit, sorryAx, or user axioms
exact job mathematical/deterministic steps:
  all SUCCESS
old final protection enforcement:
  FAILURE
old protected-final-state job:
  FAILURE
exact artifact:
  ID 8840594725
  SHA-256 3a8f44beee2c3a25b5e42bc103b94e17ef573ce62e1bdeb0aff54456626ae873
Lean/source artifact:
  ID 8840570642
  SHA-256 595360c44586316fc4c19c6ec88695b5293167057882d783be9eb6db2a27e506
final-state artifact:
  ID 8840596622
  SHA-256 ebadcf8bbd9e04f2d049f6e88a27ff0c389e2c61c136b22466c356b677d5888b
exact source tar SHA-256:
  51913841c2b17be2b11f8379a93682e568ade80c46efd51774eff68802cc9668
```

The candidate contains the complete Prompt-3 theorem, exact-audit, and Lean
package.  This closeout does not alter any of that source.

## Prior false negative and corrected policy

The prior workflow required every independently mutable source branch to keep
the head observed at the start of the task.  It therefore encoded the invalid
implication:

```text
mutable read-only branch head changed
  implies
tested immutable candidate was corrupted
```

The independently maintained branch
`agent/afp-pure-math-p3-global-rigidity-near-rigidity` moved from the initial
observation `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` to
`f1ef5b3c3107d2dfc835ed84c443eb82d752cb56`.  The movement is retained as
`MOVED_EXTERNALLY`; it is neither blamed on this work nor rewritten as a
match.  This closeout does not restore, reset, delete, or move that branch.

The corrected policy fails on immutable candidate corruption:

- wrong Prompt-2 or Prompt-3 mathematical commit/tree;
- missing Prompt-2 or Prompt-3 ancestry;
- any old Prompt-3 snapshot entering ancestry;
- any path outside the exact four-file closeout allowlist;
- any mathematical or executable source difference from `c66f3229...`;
- failure of exact, Lean, source-policy, cleanliness, archive, or artifact
  generation;
- remote closeout head unequal to the tested candidate; or
- Prompt-2 or transport archive unequal to its pinned commit.

It records ordinary movement of old source branches nonfatally.  A required
branch that is `MISSING` or produces `QUERY_ERROR` fails the current observation
operation; movement alone does not.

## Closeout publication and scope

```text
closeout branch:
  agent/afp-pure-math-p2-p3-final-closeout-c66f3229
branch initial remote head:
  c66f3229d0a89d97559535810c4ba09daf6e4e42
new pull request:
  #31
pull-request base:
  archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49
final closeout commit:
  FINAL (machine-resolved literal appended by the green workflow)
final closeout tree:
  FINAL_TREE (machine-resolved literal appended by the green workflow)
authoritative workflow jobs:
  exact-regressions
  lean-kernel
  final-candidate-integrity
```

The only permitted tracked changes from `c66f3229...` to `FINAL` are:

```text
.github/workflows/afp-prompt3-from-p2-rigidity.yml
afp_barrier_gate1/pure_math/rigidity/P3_BRANCH_PROTECTION_RECORD.md
afp_barrier_gate1/docs/P2_P3_FINALIZATION_RECORD.md
afp_barrier_gate1/docs/P3_STAGE_REPORT.md
```

The workflow independently verifies no difference on
`afp_barrier_gate1/AFPBarrier.lean`, `afp_barrier_gate1/AFPBarrier/`, or the
complete `afp_barrier_gate1/pure_math/` subtree other than the single allowed
protection-record Markdown file.  Consequently every Lean, Python, theorem,
audit, claim-control, theorem-map, prior-art, and README byte is identical to
the audited mathematical candidate.

## Required exact rerun certificate

Acceptance of `FINAL` requires one run in which all three named jobs conclude
`success`.  The run must record all of the following as successful:

| Mechanism | Exact requirement |
|---|---|
| Retained Prompt 1 | claim falsification, covariance, exact local/global, spherical feasibility |
| Retained Prompt 2 | exact quadratic covariance, signed restoration, d=3 invariance counterexample, exact spectral product |
| Prompt 3 deterministic | hostile triangulation, global near-rigidity, Q1 covariance |
| Plantri | pinned source commit/blob; counts `1,1,2,5,14,50,233,1249,7595`; total `9150` |
| Python | `python -m compileall -q pure_math` |
| Lean | pinned Lean 4.30/Mathlib update, cache, complete build |
| Axioms | focused audit contains only `propext`, `Classical.choice`, `Quot.sound` |
| Source policy | no `sorry`, `admit`, `sorryAx`, or singular/plural user axiom declaration |
| Repository | `git diff --check` and clean checkout |
| Evidence | exact logs, Lean/source archive, final-state evidence, resolved record, SHA-256 manifests |

The `final-candidate-integrity` job has ordinary success-gated `needs` edges to
both prior jobs.  It cannot run green when either prerequisite fails.

## Closeout approach registry

Findings are grouped by mechanism rather than by wording.

| Audit family | Adversarial question | Required resolution |
|---|---|---|
| Git ancestry | Did the moved old branch or an old snapshot enter the candidate DAG? | old snapshots exist and are `NOT_ANCESTOR`; P2 and `c66f3229...` are ancestors |
| Content import | Could cherry-picking or manual copying evade ancestry checks? | four-path allowlist plus byte-identical mathematical/executable source |
| Workflow fail-open | Can the final job pass after exact or Lean failure? | default success-gated `needs`; no job-level `if: always()` |
| Remote race | Is the tested object still the closeout branch head at the terminal gate? | exact `ls-remote` equality with `GITHUB_SHA` |
| Archive safety | Could an existing archive be overwritten? | pre-create absence/exact check, create-only operation, post-create `ls-remote` verification |
| Mutable observation | Does ordinary source-branch movement corrupt a pinned commit? | movement recorded as `MOVED_EXTERNALLY`, nonfatal; missing/query failure explicit |
| Source identity | Can a documentation closeout alter theorem or executable source? | exact Git diff exclusion check against `c66f3229...` |
| Artifact integrity | Are claims backed by the exact run and exact source? | artifact IDs/digests, source-tar digest, internal SHA-256 manifests |
| Self-reference | Can a commit contain its own literal hash and future run IDs? | normative `FINAL` binding plus workflow-materialized resolved record and immutable archive |

Rejected approaches include resetting the moved branch, force-pushing any ref,
ignoring all provenance, broadening the source allowlist, allowing failed
prerequisites through an always-running final job, treating mutable-head
equality as mathematically necessary, or changing mathematical source under a
closeout label.

## Ref-safety and PR disposition certificate

This record is accepted only together with the final external checks that:

1. no existing Prompt-2 or Prompt-3 branch and no transport archive was
   force-updated, overwritten, rebased, restored, or deleted;
2. PR #31 is ready for review and identifies the literal green run and
   artifacts;
3. PR #28 is closed as superseded solely because its final policy treated
   independent mutable-ref movement as fatal, without deleting or moving its
   branch; and
4. the create-if-absent Prompt-3 archive
   `archive/afp-pure-math-p3-rigidity-verified` resolves exactly to `FINAL`.

The final `ls-remote` outputs and literal values are published in PR #31 and
the closeout handoff.  Git observations do not prove the absence of an
unobserved transient third-party branch movement, and this record makes no such
claim.

## Exact Prompt-4 baseline

Once the three-job run is fully green and the Prompt-3 archive is verified,
the sole accepted starting point for Prompt 4 is:

```text
commit: FINAL
tree: FINAL_TREE
archive: archive/afp-pure-math-p3-rigidity-verified -> FINAL
mathematical source: byte-identical to
  c66f3229d0a89d97559535810c4ba09daf6e4e42
```

No synthetic merge commit is part of the Prompt-2/Prompt-3 completion state.
