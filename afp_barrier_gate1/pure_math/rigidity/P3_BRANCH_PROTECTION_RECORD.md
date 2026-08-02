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
`git fetch --all --prune` and before any Prompt 3 edit.  The final column is
filled only by the exact-final-head audit.

| Protected remote ref | Initial SHA | Final SHA | Result |
|---|---|---|---|
| `agent/afp-pure-math-p2-quadratic-covariance-completion` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | pending | pending |
| `agent/afp-pure-math-p3-q1-rigidity` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | pending | pending |
| `agent/afp-pure-math-p3-integration-record` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | pending | pending |
| `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` | pending | pending |
| `archive/afp-gate6-spatial-multigroup-verified` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | pending | pending |

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

This work must not execute `git push --force`, `git push --force-with-lease`,
`git branch -f`, or `git update-ref` on an existing remote ref.  No such command
was executed during branch selection or initial publication.  Protected refs
are read-only evidence even if a third party moves one later; this work will
report such movement and will not restore it.

## Ancestry obligations

The dedicated workflow and final audit must prove both:

1. `31ea6a49f006df10ca633eafd6848ad43b51ac3f` is an ancestor of the exact
   Prompt 3 candidate; and
2. none of `65821ff1ebd47fbee1098b30c552906cd6e03b46`,
   `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125`, or
   `d9304b5d19a1bbe69fe4ac23736308f9efe9d694` is an ancestor of it.

Selective salvage is by exact-commit file inspection and manual reproof or
port only; the old Prompt 3 commits are never merged or cherry-picked.
