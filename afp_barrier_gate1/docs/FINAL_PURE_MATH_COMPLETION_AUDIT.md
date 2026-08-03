# Final pure-mathematics completion audit

## Audit verdict

`PENDING_LITERAL_EXACT_HEAD_VERIFICATION`

The mathematical package is integrated and documentation-complete.  Final
acceptance requires the literal head verification described below and a
non-forced fast-forward of the target ref only after every required check is
green.

## Repository topology

```text
repository=FusionSandwich/Testing
immutable_transport_archive=archive/afp-gate6-spatial-multigroup-verified
immutable_transport_archive_sha=515f1aae6c20bd85711c90b5c1c21b4905252d01
target_branch=agent/afp-pure-math-p0-m1
target_baseline_sha=94aebf6578a43516cce4bb7c042fc57681c93890
rich_prompt3_source_head=19a5001158cb40fbb0adc92813cc3abd5dfa583d
verified_prompt2_completion_head=b11b7406e229f6fc8d018b36fa11b5506bd9d419
integration_branch=agent/afp-pure-math-final-integration-20260802
integration_merge_pr=32
integration_merge_commit=fbb482455dd51a961dbcbd897141c22f0ef57a15
```

All writes for this audit occur on the isolated integration branch until the
acceptance gate is green.  Source branches and the archive are read-only.

## Mandatory theorem package

### Prompt 1

- indexed tangent convex-hull and relative-interior feasibility;
- repeated, redundant, and lower-dimensional candidate handling;
- separate division-free antipodal classification;
- exact scaling, uniqueness, quantitative margins, conditioning, and
  perturbation bounds;
- shared-edge cone/Farkas/LP theory, complete-graph sufficiency, sparse
  obstructions, and explicit reconciliation mechanisms.

### Prompt 2

- finite covariance and arbitrary-target identities;
- sampling map, residual map, and factorization `R_X=(L+2dI)S_X`;
- genuine sampled-space and rank formulas;
- positive axial and positive equivariant rigidity with exact positivity
  boundary;
- exact Platonic alias dimensions;
- signed four-point and pentagon restoration/counterexamples;
- centered product resonance, Boolean counterexample, spectral collision
  handling, and rejected hierarchy boundary;
- verified compatibility API, weighted centering, one-shell rigidity, and
  distinct-eigenvalue-class sampling obstruction.

### Prompt 3

- exact spherical `Q=1` equality transfer and connected common-loss/common-rate
  propagation;
- restricted strict-convex minor-geodesic triangulation classification;
- explicit local, path, diameter, graph-center, Poincare, and
  effective-resistance near-rigidity;
- Gram/Heron-certified quantitative triangulation threshold;
- non-antipodal covariance decomposition and separate antipodal boundary;
- weighted-octahedral anisotropy and genuine sampled-space certificate;
- source-pinned finite enumeration retained only as computational
  falsification.

### Prompt 4

- rigorous product-grid asymptotics and remainders;
- sharp fixed-graph forced polar rates and minimax value;
- universal and quasi-uniform rate barriers;
- nondegenerate extremal class, lower bound, compactness, and family
  separation;
- feasible-cone anisotropy LP and dual;
- bounded high-ambition branches resolved under their kill criteria;
- final manuscript hierarchy independent of AFP terminology.

## Claim-control completeness

The normative records are present and mutually consistent:

```text
docs/CLAIM_MATRIX.md
docs/CONJECTURE_REGISTER.md
docs/PURE_MATH_PRIOR_ART_MAP.md
docs/PURE_MATH_ASSUMPTIONS_TABLE.md
docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md
docs/PURE_MATH_MANUSCRIPT_ABSTRACT.md
docs/THEOREM_TO_FILE_MAP.md
pure_math/FINAL_PURE_MATH_THEOREM_PACKAGE.md
pure_math/README.md
```

The permanent rejected claims include unrestricted Platonic classification,
universal strict `Q>1`, sampling injectivity, centered-square impossibility,
positive-curvature collapse, continuum `W_2` contraction from positivity,
fixed-connectivity Delaunay promotion, geometry-only `Q`, and general stopping-
flow order independence.

## Source-policy audit

Acceptance requires all of the following on the literal candidate.

- no `sorry`, `admit`, or `sorryAx` token in project Lean sources;
- no anchored singular `axiom` or plural `axioms` declaration;
- the fixture test must reject both singular and plural declarations while not
  rejecting theorem names or `#print axioms` commands;
- the focused Lean report may use only standard permitted foundations;
- the independent checker must not permit `sorryAx`;
- generated plantri catalogues, checker worktrees, and temporary payloads must
  be absent after verification.

## Exact verification matrix

| Gate | Required content |
|---|---|
| AFP spherical feasibility | Prompt 1 exact regressions, Lean build, independent checker, archive and scope |
| AFP quadratic covariance | Prompt 2 exact covariance, signed, spectral, sampling, Lean, and independent checks |
| AFP Prompt 3 rigidity | narrow and strengthened Prompt 3 regressions, Lean and independent checks |
| AFP global rigidity | source-pinned 9,150-map hostile census, Gram/Heron stability, covariance boundary, Lean and independent checks |
| AFP Prompt 4 sharp barriers | exact Prompt 4 audit, Lean declarations, independent checker, archive and scope |
| AFP Pure Mathematics | all Prompt 1–4 audits, full aggregate build, axiom/source policy, independent checker, archive, scope, and cleanliness |

The exact candidate SHA, tree SHA, workflow run IDs, job IDs, and conclusions are
filled in `FINAL_PURE_MATH_ACCEPTANCE.md` after the first complete green run.
A second documentation-only exact-head run then verifies the acceptance record.
The final self-referential head and its post-target runs are recorded in the PR
discussion because a commit cannot contain its own hash.

## Target advancement rule

Before target advancement:

1. verify the target is still exactly the recorded baseline;
2. verify the candidate is a descendant of that baseline;
3. verify every required workflow is green on the same candidate SHA;
4. verify the archive ref remains exactly immutable;
5. perform `update_ref(..., force=false)` only;
6. verify target and candidate compare as `identical`;
7. rerun the canonical workflows on the target push and record their IDs.

If the target has advanced independently, do not overwrite it.  Rebase is not
permitted for this acceptance line; create a fresh descendant integration and
repeat the exact-head gate.
