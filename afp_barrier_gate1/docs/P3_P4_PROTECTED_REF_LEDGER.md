# Prompt 3–4 protected-ref ledger

This ledger freezes the repository topology used by the clean final-acceptance descendant. It is descriptive and protective: none of the listed source refs may be reset, rebased, force-pushed, deleted, or repurposed by this closeout.

## Authoritative closeout inputs

| Role | Ref or record | Exact commit | Tree / status |
|---|---|---|---|
| Accepted target | `agent/afp-pure-math-p0-m1` | `94aebf6578a43516cce4bb7c042fc57681c93890` | `872828f5099aeb7df4e0ab871b9e881de4054a97` |
| Preserved PR #30 source | `agent/afp-pure-math-p3-p4-final-reconciliation` | `19a5001158cb40fbb0adc92813cc3abd5dfa583d` | Exact tree is recorded with the final object metadata in the authoritative acceptance comment |
| Clean acceptance descendant | `agent/afp-pure-math-p3-p4-final-acceptance` | descendant of `19a5001158cb40fbb0adc92813cc3abd5dfa583d` | Literal final SHA/tree recorded in the authoritative acceptance comment |
| Rich Prompt 3 source, PR #25 | `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | source tree `2d6214753fa7ac4ffcda941f7b9dcc431c7b0b5c` |
| Immutable transport archive | `archive/afp-gate6-spatial-multigroup-verified` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | equality required in every gate |

The target and PR #30 source were re-resolved before the closeout branch was created. The target remained exactly `94aebf…`; PR #30 remained exactly `19a500…` and open, draft, and mergeable.

## Protected concurrent histories

| Branch or PR | Exact observed head | Authority classification | Closeout treatment |
|---|---|---|---|
| PR #25 rich Prompt 3 | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | source history | untouched; exact source ancestor retained |
| PR #28 divergent Prompt 3 | `c66f3229d0a89d97559535810c4ba09daf6e4e42` | audit / independent implementation on divergent Prompt 2 ancestry | untouched; no commit merged or cherry-picked |
| PR #23 Prompt 3 integration record | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | provenance-only | untouched |
| Accepted narrow Prompt 3 branch | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | accepted theorem source | preserved through target ancestry |
| Prompt 4 development branch | `94aebf6578a43516cce4bb7c042fc57681c93890` at closeout inspection | accepted Prompt 4 history plus final records | read-only |
| Prompt 4 integration branch | `83bf04b99a060658b0177f3373ea0869cb4f3447` | provenance-only | untouched |
| Alternate Prompt 2 completion | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | protected alternate history | untouched |

PR #28 had advanced beyond the earlier audit-only checkpoint recorded in the supplied specification. That movement was external to this closeout. The current ref was recorded, but no part of its divergent ancestry entered the acceptance branch.

## Accepted historical commits retained as ancestors or protected inputs

```text
Prompt 1 corrected root:
    923dc47dae4f83dbea9cd56aa904164c6378e52d

Prompt 2 corrective implementation:
    afb31139cacdf1bf252e86e890c4792a03df4796
Prompt 2 corrective merge:
    dbe5d5db315d4e99b75c775c269827ac906b4fad

Prompt 3 narrow implementation:
    65821ff1ebd47fbee1098b30c552906cd6e03b46
Prompt 3 target merge:
    47ef59b0463ecd4bd7a18a3301f29b14f9777c20

Prompt 4 implementation:
    ae5b4c7635f917ea7abb6feb58717cc0173b4cd7
Prompt 4 theorem merge:
    d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
Prompt 4 integration merge:
    9f8f273b1f592801aec0cc4794cf5f4688eb836f
Prompt 4 accepted target:
    94aebf6578a43516cce4bb7c042fc57681c93890
```

## Non-destructive closeout rule

The final acceptance commit is a normal descendant of the PR #30 source and therefore retains the complete protected history. Its tree is rebuilt from the accepted target tree plus the vetted rich Prompt 3 source blobs, accepted synthesis unions, six acceptance records, and six read-only verification workflows. Temporary materialization payloads and workflows are omitted from the descendant tree; history is not purged or rewritten.

No protected branch is moved by this closeout. The only target movement permitted is a non-forced fast-forward of `agent/afp-pure-math-p0-m1` to the exact literal six-green candidate after the current target is re-fetched and proved to be its ancestor.

The literal final candidate SHA/tree, workflow run/job identifiers, artifact IDs/digests, final target SHA/tree, and post-integration workflow identifiers are recorded in the authoritative acceptance comment on the final reconciliation PR.
