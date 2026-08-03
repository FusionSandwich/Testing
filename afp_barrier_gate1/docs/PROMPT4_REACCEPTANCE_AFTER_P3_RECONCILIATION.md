# Prompt 4 reacceptance after Prompt 3 reconciliation

## Status

`REVALIDATION_PENDING_EXACT_HEAD_ACCEPTANCE`

Prompt 4 was accepted on the target history before the richer Prompt 3 package
was integrated.  This record protects the accepted Prompt 4 mathematics and
defines the post-integration reacceptance test.  It does not reopen or rewrite
the Prompt 4 theorem package.

## Protected baseline

```text
accepted_target_branch=agent/afp-pure-math-p0-m1
accepted_target_sha=94aebf6578a43516cce4bb7c042fc57681c93890
prompt4_source_branch=agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis
immutable_archive_sha=515f1aae6c20bd85711c90b5c1c21b4905252d01
final_integration_branch=agent/afp-pure-math-final-integration-20260802
integration_merge_commit=fbb482455dd51a961dbcbd897141c22f0ef57a15
```

The final integration is a descendant of the accepted target.  No Prompt 4
source branch, prior accepted branch, or archive ref is modified by this
reacceptance process.

## Protected mathematical results

The following Prompt 4 statements remain authoritative and unchanged at
mathematical level.

1. For every integer `N>=2`, the exact polar-rate and polar-quality expansions
   have the displayed coefficients and explicit one-sided `O(N^-2)` remainder
   bounds.
2. On the fixed unreduced square product graph, the polar coordinate equations
   uniquely force the meridional and two azimuthal rates, even when left and
   right azimuthal rates are initially distinct.
3. The positive reversible construction attains the forced polar row, giving
   the exact graph-class minimax maximum rate and sharp leading constant
   `8/pi^4`.
4. The universal rate--defect implication and the quasi-uniform loss-window
   transfer retain their exact constants and external-input boundary.
5. The rate-, degree-, locality-, mass-, and geometry-controlled extremal class
   has lower bound `4/R`, fixed-order minimizers, and strict product-family
   separation.
6. The feasible-cone anisotropy invariant is the compact mean-slice LP value,
   with its explicit finite dual and sharp two-loss example.
7. Delsarte, curvature, homogeneous-space, transport-metric, and reduced-ring
   branches retain their recorded `BLOCKED`, `KILLED`, `DEFERRED`, or narrowly
   `PROVED` statuses.

## Required reacceptance checks

The documentation-complete integration head must pass all of the following.

```text
python pure_math/barriers/prompt4_sharp_barrier_audit.py
lake build
lake env lean AFPBarrier/SharpProductBarriers.lean
lake env lean AFPBarrier/PureMathAxiomAudit.lean
independent nanoda verification of the accepted Prompt 4 declarations
placeholder and singular/plural user-axiom scans
immutable archive equality
pure-math-only path scope
generated-artifact rejection
git diff --check and clean checkout
```

The compatibility Prompt 1, Prompt 2, Prompt 3, global-rigidity, and aggregate
workflows must also remain green, because a local Prompt 4 pass is insufficient
for integrated reacceptance.

## Claim boundary

Prompt 4 remains supporting theory.  The central manuscript theorem is the
genuine sampled quadratic residual factorization and rigidity package.  CI
counts, workflow identifiers, commit hashes, and artifact digests are
reproducibility data, not mathematical evidence.

## Final evidence

The exact accepted candidate SHA and tree, aggregate and compatibility workflow
run IDs, job IDs, and post-target verification are recorded in
`FINAL_PURE_MATH_ACCEPTANCE.md` and the final integration pull-request
discussion.  This indirection is deliberate: a commit cannot contain its own
cryptographic identifier or the workflow identifiers produced only after that
commit exists.
