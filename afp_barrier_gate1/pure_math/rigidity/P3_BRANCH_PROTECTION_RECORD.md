# Prompt 3 branch-protection record

## Controlled baseline

This Prompt 3 line was created directly from the verified Prompt 2 object,
before any Prompt 3 source or documentation change:

```text
repository: FusionSandwich/Testing
new branch: agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49
base commit: 31ea6a49f006df10ca633eafd6848ad43b51ac3f
base tree:   879b88de81eeb52ebb09373c2ccb77cb7cb7642c
```

The commit object and the three immutable Prompt 3 source objects were checked
with `git cat-file -e`.  The base tree was checked with `git rev-parse`, and the
new branch was published at the base commit before this record was written.

## Initial protected remote-head snapshot

The following heads were read from `origin` with `git ls-remote --heads` after
`git fetch --all --prune` and before any Prompt 3 edit.  The final observation
was made immediately before the final implementation candidate was committed;
the dedicated workflow independently re-queries every row.

| Protected remote ref | Initial SHA | Final SHA | Result |
|---|---|---|---|
| `agent/afp-pure-math-p2-quadratic-covariance-completion` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | MATCH |
| `agent/afp-pure-math-p3-q1-rigidity` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | MATCH |
| `agent/afp-pure-math-p3-integration-record` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | MATCH |
| `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | MOVED |
| `archive/afp-gate6-spatial-multigroup-verified` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | MATCH |

The final observation was taken at `2026-08-02T22:52:18Z`.  The richer old
Prompt 3 branch had been advanced independently from the recorded immutable
source head `d9304b5d...` to `f1ef5b3c...`; the other four protected refs still
matched.  This work did not restore, move, or redefine the expected SHA of that
read-only ref.  The strict final-state gate must report this row as `MOVED`.

The before/after comparison can establish equality of the two observations.
It cannot detect a transient third-party move that was later reversed.

## New-branch publication check

The preferred name was absent both locally and from the remote-head query, so
no suffix was needed.  The GitHub branch-creation operation created only the
new ref from the literal Prompt 2 SHA.  A subsequent remote query returned:

```text
31ea6a49f006df10ca633eafd6848ad43b51ac3f
  refs/heads/agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49
```

The verified Prompt 2 remote head still matched the immutable commit, so the
draft pull request base is the verified Prompt 2 branch; no archival substitute
base is required.

## Prohibited-operation declaration

Across the complete Prompt 3 execution, this work did not execute
`git push --force`, `git push --force-with-lease`, `git branch -f`, or
`git update-ref`, did not force-rewrite any ref, and did not mutate any
protected ref.  Publication used only ordinary `force:false` fast-forward
updates of the newly created candidate branch.  Protected refs remained
read-only evidence; the independently moved row above was reported and was not
restored.

## Ancestry obligations

The dedicated workflow and final audit must prove both:

1. `31ea6a49f006df10ca633eafd6848ad43b51ac3f` is an ancestor of the exact
   Prompt 3 candidate; and
2. none of `65821ff1ebd47fbee1098b30c552906cd6e03b46`,
   `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125`, or
   `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` is an ancestor of it.

Selective salvage is by exact-commit file inspection and manual reproof or
port only; the old Prompt 3 commits are never merged or cherry-picked.
