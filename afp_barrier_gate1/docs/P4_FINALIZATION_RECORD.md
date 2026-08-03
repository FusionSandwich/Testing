# Prompt 4 finalization record

This tracked file is the immutable template for the Prompt-4 exact-head
closeout.  A Git object cannot contain its own commit/tree hash, and a source
commit cannot contain identifiers of a workflow that has not yet tested it.
The dedicated workflow therefore copies this file and appends the literal
commit, tree, run, job, artifact, source-digest, archive-observation, and
mutable-ref values to a machine-resolved artifact.  No source commit is made
after verification.

## 1. Verified Prompt-2 and Prompt-3 dependencies

```text
Prompt-2 commit:
  31ea6a49f006df10ca633eafd6848ad43b51ac3f
Prompt-2 tree:
  879b88de81eeb52ebb09373c2ccb77cb7cb7642c
Prompt-2 archive:
  archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49

Prompt-3 mathematical commit:
  c66f3229d0a89d97559535810c4ba09daf6e4e42
Prompt-3 mathematical tree:
  29d5e7f8f55479513a71dd457f9bd64c11b6df0f

Prompt-4 starting baseline / verified Prompt-3 closeout:
  8de4b94835137d1eaf32c14b626424f87d2e176d
baseline tree:
  350fc38359fa4c55666c9244c61890188c4b4f44
Prompt-3 archive:
  archive/afp-pure-math-p3-rigidity-verified

Prompt-3 closeout run:
  30775112774
jobs:
  exact-regressions=success
  lean-kernel=success
  final-candidate-integrity=success
Lean build:
  3110 jobs

Prompt-3 exact artifact:
  ID 8841822420
  SHA-256 7738017ca85daa241c9ec99d1f7394829398bcbd066f5b83d55291f0cc942bf5
Prompt-3 Lean/source artifact:
  ID 8841796066
  SHA-256 1c5efba248dbc709574c0436466ee4b37ca72fa715a95d1e7ef2f67f506efd9b
Prompt-3 final-state artifact:
  ID 8841825241
  SHA-256 d0eb4f51436a8b49e56fdc2496d63aba4fe50512b0732a0335611ccde2f855e8
Prompt-3 resolved-record artifact:
  ID 8841825450
  SHA-256 ce9c708ed00461f8011a116d94df38bf50bc4e2ee8a02a2a09efc6085836eb4c
Prompt-3 exact source tar SHA-256:
  db3539ebd0cf8ae2ebd2e1fb8ff8ec7c4b60d174f6fabaa2919754260f317f10

transport archive:
  archive/afp-gate6-spatial-multigroup-verified
  515f1aae6c20bd85711c90b5c1c21b4905252d01
```

## 2. Non-overwriting Prompt-4 branch and PR

```text
branch:
  agent/afp-pure-math-p4-from-p3-8de4b948
created directly at:
  8de4b94835137d1eaf32c14b626424f87d2e176d
pull request:
  PR #35
base:
  archive/afp-pure-math-p3-rigidity-verified
disposition:
  keep unmerged unless the user explicitly requests merge
```

The preferred branch name was absent and was created without force before any
edit.  Existing Prompt-2, Prompt-3, Prompt-4, and transport refs are read-only
dependencies or observations; none is an update target of this work.

## 3. Old Prompt-4 salvage objects

```text
accepted old implementation object:
  ae5b4c7635f917ea7abb6feb58717cc0173b4cd7
old merge object:
  d1a31d195ae3c371b3f9cee29bd7ed34d1ff0994
common old tree:
  e192275e48bf38bf899483e8c27c0c3a206edf64

read-only development branch:
  agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis
initially observed head:
  94aebf6578a43516cce4bb7c042fc57681c93890

read-only integration branch:
  agent/afp-pure-math-p4-integration-record
initially observed head:
  83bf04b99a060658b0177f3373ea0869cb4f3447
```

Neither immutable old commit nor any commit in the old implementation range
may be an ancestor of the final candidate.  Mutable branch movement is
informational: it is recorded truthfully and never substituted for immutable
object/ancestry/source checks.

## 4. Selective salvage and adversarial corrections

The authoritative file-level provenance is
`pure_math/barriers/P4_SALVAGE_LEDGER.md`.  Independent audits accepted the
polar analytic constants, direct asymmetric polar solve, graph-class
attainment, constrained compactness, LP sign transfer, polar anisotropy, and
incidence count.

They also forced the following minimal corrections:

- for arbitrary normal moment `lambda>0`, use
  `Q_lambda=r*epsilon/lambda^2`; it agrees with spherical `r*epsilon/4` at
  `lambda=2`;
- the fixed-`lambda` feasible family is an affine slice, while the unfixed
  nonzero tangent-balanced cone modulo scaling is projective;
- the sliced interval/minimum/equality theorem assumes a nonempty balanced
  probability polytope;
- if `v_2=-kappa v_1`, use
  `kappa*(ell_1-ell_2)^2/(kappa*ell_1+ell_2)^2`; the half-weight formula is only
  the `kappa=1` case;
- a loss window plus `K` comparable to `h^-2` proves rate-cap compatibility,
  not all constrained-class hypotheses; and
- the Lean incidence theorem checks the arithmetic consequence from supplied
  edge-count equalities, not the entire handshaking derivation.

The false literal formulations are retained as `REJECTED` entries in the
theorem registry, claim matrix, and counterexample catalogue.

## 5. Completed theorem and implementation map

The theorem-to-file map is `P4_THEOREM_TO_FILE_MAP.md`.  The ordinary proof is
`pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md`; the current-API finite
formal core is `AFPBarrier/SharpProductBarriers.lean`; the independent exact
audit is `pure_math/barriers/prompt4_sharp_barrier_audit.py`; and the complete
publication hierarchy is `pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md`.

Claim-status summary:

| Family | Status |
|---|---|
| controlled polar expansion and uniform remainders | PROVED |
| direct asymmetric polar uniqueness and fixed-graph minimax | PROVED |
| universal/loss-window rate transfer | PROVED |
| constrained lower bound, minimizer, and product exclusion | PROVED |
| corrected feasible-family anisotropy and sharp examples | PROVED |
| finite LP strong duality | EXTERNAL |
| biregular/perfect-matching incidence | PROVED |
| source-pinned finite ranks/counts and Plantri census | COMPUTATIONAL |
| new general reduced-ring split/merge or compact-space extension | CONJECTURE |
| unqualified old normalization, opposite-ray, Delsarte, curvature, and transport claims | REJECTED |

## 6. Exact-head workflow contract

The dedicated read-only workflow is
`.github/workflows/afp-prompt4-from-p3-sharp-barriers.yml`.  It has exactly the
three required jobs:

```text
exact-regressions
lean-kernel
final-candidate-integrity
```

The final job has ordinary `needs` dependencies and explicitly requires both
prior conclusions to be `success`; it does not use `if: always()`.  The jobs
bind the PR head or pushed head to the exact remote Prompt-4 branch, verify all
immutable baseline/archive objects, reject old Prompt-4 ancestry and merges,
enforce the exact 21-path allowlist and regular-file/source policy, preserve
all closed Prompt-1 through Prompt-3 modules, rerun every deterministic audit
and the pinned `9150`-map census, build Lean, run the focused axiom audit, scan
placeholders and singular/plural user axioms, require clean checkouts, and
generate hashed artifacts and an exact source archive.

## 7. Machine-resolved final values

The exact green candidate commit/tree, workflow run and attempt, numeric job
IDs, all job conclusions, artifact IDs and SHA-256 digests, exact source-tar
SHA-256, Lean job count, focused axiom result, deterministic audit results,
mutable-reference table, immutable remote bindings, Prompt-4 archive state,
and Prompt-5 exact baseline are appended to
`P4_FINALIZATION_RECORD.resolved.md` in the resolved finalization artifact.

The first entirely green exact-head run is allowed to record the Prompt-4
archive as not yet created.  After that run, the archive is created through a
create-only operation at the exact green commit.  An unchanged second run must
observe the archive at exactly that commit and pass every job again.  The
second run is authoritative; no source commit follows it.

## 8. Prompt-4 archive and next-stage baseline

Preferred immutable archive:

```text
archive/afp-pure-math-p4-sharp-barriers-verified
```

If it unexpectedly exists at a different object, it is never moved; the
create-only suffix is `-v2`.  The exact archive-selected green commit—not a
synthetic merge commit—is the authoritative Prompt-5 baseline.  Its literal
hash is supplied only by the machine-resolved record generated at that exact
object.
