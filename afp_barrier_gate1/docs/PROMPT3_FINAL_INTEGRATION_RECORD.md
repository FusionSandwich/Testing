# Prompt 3 final integration record

## Status

`INTEGRATED_PENDING_EXACT_HEAD_ACCEPTANCE`

This record documents the non-destructive integration of the strengthened
Prompt 3 package with the verified Prompt 2 completion and the already accepted
Prompt 4 target.  Mathematical acceptance is controlled by
`FINAL_PURE_MATH_ACCEPTANCE.md`; this file records source authority and conflict
resolution rather than treating branch history as proof.

## Protected source topology

```text
repository=FusionSandwich/Testing
immutable_archive_branch=archive/afp-gate6-spatial-multigroup-verified
immutable_archive_sha=515f1aae6c20bd85711c90b5c1c21b4905252d01
accepted_target_branch=agent/afp-pure-math-p0-m1
accepted_target_baseline=94aebf6578a43516cce4bb7c042fc57681c93890
rich_prompt3_reconciliation_branch=agent/afp-pure-math-p3-p4-final-reconciliation
rich_prompt3_reconciliation_head=19a5001158cb40fbb0adc92813cc3abd5dfa583d
verified_prompt2_completion_branch=agent/afp-pure-math-final-completion-20260802
verified_prompt2_completion_head=b11b7406e229f6fc8d018b36fa11b5506bd9d419
isolated_final_integration_branch=agent/afp-pure-math-final-integration-20260802
integration_merge_pr=32
integration_merge_commit=fbb482455dd51a961dbcbd897141c22f0ef57a15
```

Neither source branch was reset, rebased, force-pushed, deleted, or reused as a
write target.  The integration merge was materialized only on the isolated
final-integration branch.  The temporary materialization workflow removed
itself in the merge commit.

## File-authority decisions

The merge preserves the richer reconciliation versions of:

```text
AFPBarrier/SphericalQEqualityRigidity.lean
AFPBarrier/QuantitativeGlobalNearRigidity.lean
AFPBarrier/QEqualityCovariance.lean
pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md
pure_math/rigidity/global_near_rigidity_audit.py
pure_math/rigidity/q1_covariance_audit.py
```

Those files carry the strengthened path, diameter, graph-center, Poincare,
effective-resistance, Gram/Heron stability, antipodal-boundary, and weighted-
octahedral statements.

The merge imports the verified Prompt 2 completion modules and records:

```text
AFPBarrier/QuadraticCovarianceCompletion.lean
AFPBarrier/QuadraticSampling.lean
AFPBarrier/QuadraticSphereResidual.lean
AFPBarrier/OneShellQuadraticRigidity.lean
AFPBarrier/SpectralSamplingObstruction.lean
AFPBarrier/SpectralProductAlgebra.lean
pure_math/covariance/exact_quadratic_covariance_audit.py
pure_math/covariance/exact_signed_restoration_audit.py
pure_math/covariance/exact_d3_invariance_counterexample.py
pure_math/spectral_products/exact_spectral_product_audit.py
```

The aggregate import and axiom-audit roots were formed by union: the rich
Prompt 3 declarations remain, and the verified Prompt 2 sampling, one-shell,
spectral, centering, and dimension declarations are added.

## Removed bootstrap material

The final integration branch contains none of the temporary patch payloads or
materialization workflows:

```text
.github/p3p4*.b64
.github/workflows/afp-p3-p4-materialize.yml
.github/workflows/afp-p3-p4-targeted-lean.yml
.github/workflows/afp-final-integration-materialize.yml
```

The dedicated `afp-global-rigidity.yml` workflow is retained because it is an
acceptance workflow, not a bootstrap mechanism.

## Accepted Prompt 3 theorem boundary

The integrated package retains the following statuses.

- `PROVED`: exact spherical equality transfer and connected common-loss/common-
  rate propagation under the stated positivity and symmetric-activity
  hypotheses.
- `PROVED`: restricted minor-geodesic strict-convex triangulation
  classification, with tetrahedral, octahedral, and icosahedral conclusions.
- `PROVED`: explicit local, path, diameter, graph-center, Poincare, and
  effective-resistance near-rigidity estimates with all weight-floor and
  connectivity hypotheses displayed.
- `PROVED`: non-antipodal covariance decomposition and the separate antipodal
  radial boundary.
- `PROVED`: weighted-octahedral anisotropy family and genuine sampled-space
  zero certificate.
- `COMPUTATIONAL`: source-pinned enumeration of 9,150 triangulations through
  twelve vertices, used only for hostile falsification.
- `REJECTED`: enumeration as an all-orders proof, unrestricted Platonic-only
  classification, tangent normalization at `ell=2`, scalar defect control of
  tangential anisotropy, and the failed endpoint-product angle certificate.

## Acceptance dependency

This integration is not certified merely by mergeability.  Acceptance requires
all canonical exact audits, full Lean build, focused axiom report, placeholder
and user-axiom scans, independent nanoda checking, archive equality, scope
checking, generated-artifact rejection, and clean-checkout verification on one
literal documentation-complete head.  The exact candidate, tree, workflow, and
job identifiers are recorded in `FINAL_PURE_MATH_ACCEPTANCE.md` after that run.
