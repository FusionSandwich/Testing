# P0/M1 spherical feasibility integration record

## Integrated stage

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Starting checkpoint: `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Pull request: `#13`, **Complete spherical feasibility and shared-edge duality package**
- Accepted implementation head: `01a592301978ab184fc7969d9f54592eddad742c`
- Squash-merge commit: `cc739ed77451444784588799a0ba519981f01948`
- First integrated target head: `b5f74404729f1a3c0396812539dffccc5ce928c5`

The integrated stage is confined to the AFP pure-mathematics package, exact
falsification regressions, theorem/claim-control documentation, and its
dedicated verification workflow. The immutable transport archive
`archive/afp-gate6-spatial-multigroup-verified` at
`515f1aae6c20bd85711c90b5c1c21b4905252d01` was not modified. No transport,
Radiant, HTS, multigroup, or spatial-solver work was added to this stage.

## Pre-merge acceptance

The exact accepted implementation head passed:

- exact rational spherical-feasibility regressions;
- rejection of `sorry`, `admit`, `sorryAx`, and user-declared axioms in the
  four stage modules;
- the full Lean 4.30.0 / Mathlib 4.30.0 package build; and
- independent nanoda checking of all explicitly listed spherical-stage
  declarations, with `sorryAx` absent from the permitted-axiom list.

The authoritative pre-merge Actions record is workflow run `30719026455`, job
`91419555624`.

## Exact integrated-head acceptance

The earlier repository-wide `AFP Pure Mathematics` run `30719314077`, job
`91420309094`, checked a GitHub pull-request merge ref whose tree included
`b5f744...`. It remains merge-compatibility evidence, but it is not classified
as an exact checkout of the integrated target SHA.

A controlled closeout PR reran the dedicated `AFP spherical feasibility`
workflow with `actions/checkout` pinned to the PR head and an explicit
`git rev-parse HEAD` equality assertion. It checked the exact integrated SHA
`b5f74404729f1a3c0396812539dffccc5ce928c5`:

- workflow run `30721748746`;
- job `91426559801`;
- exact checkout assertion: PASS;
- exact rational regressions: PASS;
- stage-module placeholder/user-axiom source scan: PASS;
- full Lean build: PASS (`3095` jobs); and
- independent nanoda validation: PASS (`38` selected stage declarations,
  `13252` declarations checked with no errors).

## Closeout audit and narrow corrections

`PROMPT1_CLOSEOUT_AUDIT.md` is the normative closeout supplement. It records
the independent theorem-by-theorem audit and supplies only three mathematical
writing clarifications:

1. the reverse reconstruction calculation completing the stated
   row/dependence bijection;
2. the explicit `0<c1<=c2` hypothesis required by the inverse-quadratic
   angular-window constants; and
3. nonnegative residual weights for the residual LP, with strict positivity
   required for zero residual objective to be equivalent to exact feasibility.

It also corrects the exact-head workflow provenance described above. No Lean
theorem, test case, transport source, or theorem scope was changed by the
closeout patch. Final closeout-commit workflow identifiers are recorded in the
closeout response and audit PR after the exact-head rerun completes.
