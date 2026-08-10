# Prompt 2+3 provenance and branch-protection record

This closeout distinguishes immutable Git objects and archive pointers from
mutable branch-head observations.  A branch name is not an immutable object;
an observed change to a read-only source branch is evidence to record, not by
itself evidence that a pinned candidate changed.

## A. Immutable mathematical objects

The dedicated workflow verifies the object type, tree, ancestry, closeout
scope, and exact remote bindings independently of mutable source-branch names.

| Object | Exact identity |
|---|---|
| Prompt-2 commit | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` |
| Prompt-2 tree | `879b88de81eeb52ebb09373c2ccb77cb7cb7642c` |
| Prompt-3 mathematical commit | `c66f3229d0a89d97559535810c4ba09daf6e4e42` |
| Prompt-3 mathematical tree | `29d5e7f8f55479513a71dd457f9bd64c11b6df0f` |
| Transport archive commit | `515f1aae6c20bd85711c90b5c1c21b4905252d01` |

The Prompt-2 archive was created only after its preferred name was found
absent, and was then read back from the remote:

```text
archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49
  -> 31ea6a49f006df10ca633eafd6848ad43b51ac3f
```

The closeout branch was likewise created only after its preferred name was
found absent, and was published before any closeout edit:

```text
agent/afp-pure-math-p2-p3-final-closeout-c66f3229
  -> c66f3229d0a89d97559535810c4ba09daf6e4e42
```

The transport archive remains an independently verified immutable pointer:

```text
archive/afp-gate6-spatial-multigroup-verified
  -> 515f1aae6c20bd85711c90b5c1c21b4905252d01
```

## B. Immutable source snapshots used for manual salvage

These are commit objects, not promises about the future values of branch
names.  Each object must exist, and none may be an ancestor of the exact
closeout candidate:

| Snapshot object | Candidate-ancestry requirement |
|---|---|
| `65821ff1ebd47fbee1098b30c552906cd6e03b46` | `NOT_ANCESTOR` |
| `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | `NOT_ANCESTOR` |
| `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` | `NOT_ANCESTOR` |

Manual salvage inspected exact blobs from these snapshots.  No snapshot was
merged or cherry-picked.  The negative ancestry checks detect a merge of a
snapshot line; the independent closeout allowlist and mathematical-source
identity checks also detect content imported without ancestry, such as by a
cherry-pick or manual copy.

## C. Mutable branch-head observations

The initial observations below are preserved as historical facts.  The
closeout observation was queried at `2026-08-03T00:18:01Z`.  The workflow
queries the same branches again for every exact run and writes its current
observations to the final-state artifact.

| Mutable source branch | Initial observed head | Closeout observation | Classification |
|---|---|---|---|
| `agent/afp-pure-math-p3-q1-rigidity` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | UNCHANGED_SINCE_INITIAL_OBSERVATION |
| `agent/afp-pure-math-p3-integration-record` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | UNCHANGED_SINCE_INITIAL_OBSERVATION |
| `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | MOVED_EXTERNALLY |

The permitted classifications are
`UNCHANGED_SINCE_INITIAL_OBSERVATION`, `MOVED_EXTERNALLY`, `MISSING`, and
`QUERY_ERROR`.  Movement is informational.  `MISSING` or `QUERY_ERROR` is
fatal only because all three branches are required inputs to the current
observation operation; neither state is silently converted into movement.

The historical `MOVED_EXTERNALLY` result is not rewritten as `MATCH`.  This
closeout did not restore, move, reset, delete, or force-update that branch.
The workflow records movement with the explanation:

> reference branch moved externally; candidate ancestry and source integrity remain valid

> This task does not claim that no third party moved a mutable branch. It proves that the final candidate descends from the exact Prompt-2 baseline, that the old Prompt-3 snapshot commits are absent from its ancestry, that only the newly created closeout branch was advanced by this closeout operation, and that the mathematical source remains identical to the already audited Prompt-3 candidate.

Two observations can establish equality or inequality at those observation
times.  Git history cannot prove the absence of an unobserved transient
third-party ref movement between observations.

## Candidate-integrity policy

The corrected gate is fail-closed on immutable candidate properties:

1. exact Prompt-2 and Prompt-3 mathematical commit/tree objects;
2. ancestry from Prompt 2 and from the audited Prompt-3 candidate;
3. absence of all three old snapshot commits from candidate ancestry;
4. the four-path closeout allowlist;
5. byte identity of mathematical and executable source with `c66f3229...`;
6. exact equality of the tested commit and the remote closeout branch;
7. exact Prompt-2 and transport archive pointers; and
8. successful exact regressions, Lean build, axiom/source-policy scans,
   clean checkout, and artifact/source-archive generation.

It is deliberately nonfatal on ordinary movement of the three mutable source
branches.  The workflow has read-only repository permissions and performs no
ref mutation.

## Prohibited-operation declaration

No existing Prompt-2 or Prompt-3 branch and no transport archive is advanced,
restored, rebased, deleted, or force-updated by this closeout.  In particular,
the operation does not use `git push --force`, `git push --force-with-lease`,
`git branch -f`, or `git update-ref` on an existing ref.  Publication consists
only of create-if-absent archive operations and ordinary fast-forward commits
to the newly created closeout branch.
