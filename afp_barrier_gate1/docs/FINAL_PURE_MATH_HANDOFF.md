# Final pure-mathematics handoff

## Current operating state

The complete Prompt 1–4 source package is on the isolated branch:

```text
agent/afp-pure-math-final-integration-20260802
```

It combines, without modifying either source branch:

```text
rich Prompt 3 reconciliation:
  agent/afp-pure-math-p3-p4-final-reconciliation
  19a5001158cb40fbb0adc92813cc3abd5dfa583d

verified Prompt 2/final completion:
  agent/afp-pure-math-final-completion-20260802
  b11b7406e229f6fc8d018b36fa11b5506bd9d419

server-side integration record:
  PR #32
  merge commit fbb482455dd51a961dbcbd897141c22f0ef57a15
```

The immutable transport archive remains:

```text
archive/afp-gate6-spatial-multigroup-verified
515f1aae6c20bd85711c90b5c1c21b4905252d01
```

No transport, Radiant, material-data, HTS, multigroup, spatial-solver, or
production implementation work is part of the final integration diff.

## Mathematical handoff

The central manuscript result is the sampled quadratic factorization and
rigidity package:

```text
R_X=(L+2dI)S_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

Positive axial covariance gives `E_form=K_X` and no genuine sampled degree-two
mode.  Positive equivariant rigidity requires global off-diagonal
nonnegativity.  Regular simplices give sharp equality families; Platonic alias
spaces and signed four-point/pentagon constructions delimit the boundary.

The supporting theorem hierarchy is:

1. exact local spherical feasibility and shared-edge global duality;
2. exact and quantitative spherical `Q=1` rigidity, including restricted
   triangulation classification and stronger graph-global stability;
3. sharp product-graph obstruction, rigorous asymptotics, constrained
   extremals, and feasible-cone anisotropy;
4. exact examples, rejected stronger variants, formal finite algebra, and
   deterministic falsification appendices.

Normative mathematical wording is controlled by:

```text
pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md
docs/CLAIM_MATRIX.md
docs/CONJECTURE_REGISTER.md
docs/PURE_MATH_ASSUMPTIONS_TABLE.md
docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
docs/PURE_MATH_PRIOR_ART_MAP.md
docs/THEOREM_TO_FILE_MAP.md
```

## Verification handoff

The six required gates are:

```text
AFP spherical feasibility
AFP quadratic covariance
AFP Prompt 3 rigidity
AFP global rigidity
AFP Prompt 4 sharp barriers
AFP Pure Mathematics
```

They must refer to the same literal candidate SHA.  The aggregate gate includes
all exact Prompt 1–4 audits, full Lean build, focused axiom report, source-policy
fixtures, independent nanoda checking, archive equality, path-scope checking,
generated-artifact rejection, `git diff --check`, and clean-checkout
verification.

The first documentation-complete run populates the non-self-referential fields
in `FINAL_PURE_MATH_ACCEPTANCE.md`.  A second exact-head run verifies that
acceptance record.  The final head SHA/tree and its workflow/job IDs are then
posted to the final PR discussion, because no Git commit can include its own
hash or the workflow identifiers generated after it exists.

## Safe target-integration procedure

The target is:

```text
agent/afp-pure-math-p0-m1
baseline 94aebf6578a43516cce4bb7c042fc57681c93890
```

Do not advance it until all six candidate gates are green.  Immediately before
advancement, compare the live target with the baseline.  If it differs, stop
and build a fresh descendant rather than overwriting another worker's changes.
If it is unchanged, advance only through a non-forced fast-forward to the exact
tested candidate.  Then:

```text
compare target and candidate as identical;
recheck archive SHA;
collect target-push workflow and job IDs;
confirm all target-push gates are green;
close or supersede obsolete draft PRs without altering their source branches.
```

No force update, rebase, squash, history rewrite, or deletion of protected
source branches is authorized.

## Publication boundary

Workflow counts and hashes are reproducibility records only.  The mathematical
paper should state the theorem hierarchy without AFP or gate terminology.  The
prior-art map remains a working priority audit and should receive a final
specialist bibliography review before submission; no absence-of-search claim is
used as evidence of novelty.

## Remaining action at creation of this file

`FINAL_PURE_MATH_ACCEPTANCE.md` still awaits exact-head run identifiers and the
post-target comparison.  No other mathematical or source-integration work is
intentionally pending.
