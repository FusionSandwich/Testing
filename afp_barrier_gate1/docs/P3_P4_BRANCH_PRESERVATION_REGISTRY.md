# Prompt 3–4 branch-preservation registry

## Closeout branch

```text
agent/afp-pure-math-p3-p4-final-acceptance
```

The branch was created from exact PR #30 source commit:

```text
19a5001158cb40fbb0adc92813cc3abd5dfa583d
```

The accepted target at branch creation was still:

```text
commit: 94aebf6578a43516cce4bb7c042fc57681c93890
tree:   872828f5099aeb7df4e0ab871b9e881de4054a97
```

The immutable archive was still:

```text
515f1aae6c20bd85711c90b5c1c21b4905252d01
```

## Preservation assertions

| Assertion | Result |
|---|---|
| PR #30 source branch rewritten | NO |
| PR #25 source branch rewritten | NO |
| PR #28 divergent branch rewritten | NO |
| PR #23 provenance branch rewritten | NO |
| Accepted narrow Prompt 3 branch rewritten | NO |
| Prompt 4 development or integration branch rewritten | NO |
| Alternate Prompt 2 branch rewritten | NO |
| Protected branch rebased | NO |
| Protected branch force-pushed | NO |
| Protected branch deleted or repurposed | NO |
| PR #28 commit merged or cherry-picked | NO |
| Archive branch changed | NO |
| Target changed before exact tested integration | NO |

The closeout branch retains the source commit in its ancestry. Temporary materialization files are removed only from the new descendant tree; their historical commits remain reachable through the preserved PR #30 history.

## Concurrent movement audit

The accepted target and PR #30 source did not move between the supplied checkpoint and closeout branch creation. PR #28 did move externally to `c66f3229d0a89d97559535810c4ba09daf6e4e42`. That movement is recorded but is not treated as an immutable invariant and does not enter this branch's ancestry.

## Manual correction provenance

The following mathematical corrections were independently re-derived rather than copied through divergent ancestry:

```text
ell<2 tangent-frame domain and separate ell=2 boundary;
delta<1 incident-loss domain;
positive-inverse multiplication for Lean division bounds;
commuted weighted-product proof;
Gram/Heron determinant angle certificate;
weighted-octahedron sampled-space determinant certificate.
```

The source blob hashes and file-level authority decisions are recorded in `P3_P4_FILE_RECONCILIATION_LEDGER.md`.

## Permitted integration

After all six workflows pass on one literal implementation head, the only permitted target update is a non-forced fast-forward of `agent/afp-pure-math-p0-m1` to that exact head. If the target moves first, it must be merged additively into the closeout branch and the six-workflow suite must be repeated before target movement.

The literal final candidate SHA/tree, workflow run/job identifiers, artifact IDs/digests, final target SHA/tree, and post-integration workflow identifiers are recorded in the authoritative acceptance comment on the final reconciliation PR.
