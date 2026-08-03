# Prompt 3–4 protected-ref ledger

## Purpose

This record freezes the repository topology inspected before any source repair
or claim-control edit on the non-destructive reconciliation branch.  All refs
listed below are read-only inputs except the new reconciliation ref and, after
literal exact-head acceptance, the accepted pure-math target.  No source branch
is rebased, reset, force-pushed, deleted, or silently repurposed.

## Exact starting state

```text
repository=FusionSandwich/Testing
reconciliation_branch=agent/afp-pure-math-p3-p4-final-reconciliation
reconciliation_start_commit=f1ef5b3c3107d2dfc835ed84c443eb82d752cb56
reconciliation_start_tree=2d6214753fa7ac4ffcda941f7b9dcc431c7b0b5c
```

The reconciliation branch was created as a new ref from the literal rich
Prompt 3 head.  It was not created by resetting or renaming an existing branch.

## Protected refs and accepted objects

| Role | Ref / PR | Commit | Tree / status | Reconciliation disposition |
|---|---|---|---|---|
| Current accepted pure-math target | `agent/afp-pure-math-p0-m1` | `94aebf6578a43516cce4bb7c042fc57681c93890` | `872828f5099aeb7df4e0ab871b9e881de4054a97` | `TARGET_AUTHORITATIVE`; already an ancestor of the rich head |
| Rich Prompt 3 source | PR #25, `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | `2d6214753fa7ac4ffcda941f7b9dcc431c7b0b5c` | read-only source after branch creation |
| Additive Prompt 4 preservation merge on rich source | rich Prompt 3 history | `cac39445619673f224e07047c6995e46f5b019f4` | two-parent additive merge | inherited; never rewritten |
| Independent Prompt 3 audit | PR #28, `agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49` | `59e1d996a1c77efaa7874a6914a4b406eff2c564` | divergent Prompt 2 ancestry | `AUDIT_ONLY`; never merged or cherry-picked |
| Accepted narrow Prompt 3 implementation | `agent/afp-pure-math-p3-q1-rigidity` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | implementation accepted by PR #22 | preserve without deletion |
| Accepted narrow Prompt 3 target merge | target history | `47ef59b0463ecd4bd7a18a3301f29b14f9777c20` | target merge | preserve without regression |
| Prompt 3 provenance-only follow-up | PR #23, `agent/afp-pure-math-p3-integration-record` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | open draft, one documentation file | `PROVENANCE_ONLY`; untouched |
| Alternate Prompt 2 completion | PR #21, `agent/afp-pure-math-p2-quadratic-covariance-completion` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | tree `879b88de81eeb52ebb09373c2ccb77cb7cb7642c` | protected alternate ancestry; not merged here |
| Accepted Prompt 4 implementation | `agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis` | `ae5b4c7635f917ea7abb6feb58717cc0173b4cd7` | accepted implementation | theorem-level authority preserved |
| Prompt 4 theorem merge | target history / PR #24 | `d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994` | tree `e192275e48bf38bf899483e8c27c0c3a206edf64` | preserve |
| Prompt 4 integration-record merge | target history / PR #26 | `9f8f273b1f592801aec0cc4794cf5f4688eb836f` | tree `911c0c41eeaa6a1749604d127a02ba6176333dc3` | preserve |
| Prompt 4 final exact-head target | target history / PR #27 | `94aebf6578a43516cce4bb7c042fc57681c93890` | tree `872828f5099aeb7df4e0ab871b9e881de4054a97` | starting target authority |
| Immutable transport archive | `archive/afp-gate6-spatial-multigroup-verified` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | immutable | equality must hold at every gate |

## Concurrent movement observed

The task specification recorded PR #28 at
`02ace53680e6e62b81cdb20048d447732f2f4d31`.  Before reconciliation edits,
that audit branch had advanced additively to
`59e1d996a1c77efaa7874a6914a4b406eff2c564`.  Its new files and claims were
inspected only as audit inputs.  No part of its divergent ancestry is merged.

The accepted target remained exactly
`94aebf6578a43516cce4bb7c042fc57681c93890` when the reconciliation branch was
created.

## Write-safety contract

The reconciliation will use only normal descendant commits and, if the target
moves, a normal additive merge of the current target into this branch.  It will
not use force updates, rebases, destructive resets, branch deletion, or target
history replacement.  PR #25, PR #28, PR #23, PR #21, the narrow Prompt 3
branch, and both Prompt 4 branches remain untouched except for the two explicit
preservation comments required after the new reconciliation PR exists.
