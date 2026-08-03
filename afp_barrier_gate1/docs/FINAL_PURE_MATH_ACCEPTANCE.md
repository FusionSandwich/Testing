# Final pure-mathematics acceptance record

## Accepted package

The final pure-mathematics baseline is the additive union of:

```text
accepted Prompt 1 local and global feasibility package;
accepted Prompt 2 sampled quadratic covariance package and corrective closeout;
accepted narrow Prompt 3 Q=1 rigidity package;
rich Prompt 3 restricted classification, graph-global near-rigidity,
covariance, antipodal-boundary, weighted-octahedral, and hostile-enumeration package;
accepted Prompt 4 sharp product-grid barriers, extremal theory,
feasible-cone duality, and reduced-ring obstruction;
updated final manuscript synthesis and claim controls.
```

The central publication candidate remains the genuine sampled quadratic covariance factorization and structural rigidity theorem. The richer Prompt 3 result is a strong companion theorem. Prompt 1 feasibility/shared-edge theory, exact examples and counterexamples, and Prompt 4 sharp barriers and extremal results remain supporting theory.

## Repository provenance

```text
starting accepted target:
    94aebf6578a43516cce4bb7c042fc57681c93890
starting target tree:
    872828f5099aeb7df4e0ab871b9e881de4054a97

preserved PR #30 source:
    19a5001158cb40fbb0adc92813cc3abd5dfa583d

clean closeout branch:
    agent/afp-pure-math-p3-p4-final-acceptance

immutable transport archive:
    515f1aae6c20bd85711c90b5c1c21b4905252d01
```

The clean descendant retains the complete accepted target and PR #30 source history. Its tree is reconstructed from the accepted target tree plus only the vetted rich Prompt 3 sources, synchronized synthesis files, acceptance records, and six read-only exact-head workflows. No protected branch is reset, rebased, force-pushed, deleted, or repurposed. No PR #28 commit is merged or cherry-picked.

## Mathematical acceptance boundary

### Prompt 3

Accepted results are:

1. the exact normalized identity
   ```text
   Q_i-1=sum_j p_ij(x_ij-1)^2;
   ```
2. exact active-edge equality transfer and connected shared-conductance propagation;
3. tetrahedral/octahedral/icosahedral classification only under the complete displayed round minor-arc geodesic-triangulation hypotheses;
4. explicit pointwise, path, diameter, graph-radius, edge-loss, arclength, spectral-gap, and effective-resistance near-rigidity;
5. an explicit edge-metric Platonic stability threshold certified by positive spherical Gram/Heron determinants;
6. exact `Q=1` covariance decomposition for `0<ell<2`;
7. a separate antipodal `ell=2`, `r=1`, purely radial covariance boundary;
8. the positive reversible weighted-octahedral family showing that `Q=1` does not force axial covariance and that scalar defect does not bound tangential anisotropy;
9. an exact sampled-space `{0}` certificate for every positive weighted-octahedral member; and
10. source-pinned enumeration of exactly 9,150 simple triangulations through 12 vertices as hostile computational falsification, not as the all-orders proof.

The conservative stability thresholds encoded by the accepted audit are:

```text
q=3: eta_* = 3.90838234361e-6
q=4: eta_* = 2.07429596521497e-7
q=5: eta_* = 7.942143600537101e-10
```

### Prompt 4

The accepted Prompt 4 theorem statements are preserved at theorem level. In particular, for every integer `N>=2`,

```text
0 <= r_polar(N)
     -[(8/pi^4)N^4+(10/(3pi^2))N^2+13/45]
  <= pi^2/(48N^2),
```

and

```text
0 <= Q_pole(N)-[N^2/pi^2+7/12]
  <= pi^2/(12N^2).
```

The fixed unreduced product-graph polar rates, graph-class minimax obstruction, universal rate barrier, quasi-uniform transfer, extremal lower bounds and minimizer existence, feasible-cone formula, sliced LP and dual anisotropy certificate, sharp examples, and stated biregular/perfect-matching reduced-ring obstruction remain unchanged.

## Permanent rejected overclaims

```text
enumeration through 12 vertices proves the classification;
unrestricted Q=1 Platonic classification;
coordinate-level framework stability follows automatically from edge-metric stability;
optimality of the displayed near-rigidity constants;
Q=1 forces axial covariance;
scalar eta controls tangent anisotropy;
tangent normalization at ell=2;
form-space rank alone determines sampled exactness;
Prompt 4 had not begun before the richer Prompt 3 reconciliation.
```

The true history is that Prompt 4 was already closed on the accepted target, the richer Prompt 3 package was integrated additively afterward, and Prompt 4 was revalidated on the combined exact head.

## Formal and computational acceptance boundary

The literal accepted head is required to pass all six workflows:

```text
AFP global rigidity
AFP Prompt 3 rigidity
AFP Prompt 4 sharp barriers
AFP Pure Mathematics
AFP quadratic covariance
AFP spherical feasibility
```

Each workflow performs a literal checkout, all Prompt 1–4 deterministic audits, source-pinned plantri enumeration, Gram/Heron zero-defect and positive-width checks, antipodal and weighted-octahedral regressions, targeted and full Lean 4.30 builds, focused axiom reporting, placeholder and singular/plural user-axiom rejection, independent lean4export/nanoda validation, archive equality, pure-math-only scope, generated-artifact rejection, `git diff --check`, and evidence packaging.

The only permitted project theorem dependencies reported by Lean are the accepted foundational axioms:

```text
propext
Classical.choice
Quot.sound
```

`Lean.trustCompiler` is permitted only at the independent exporter boundary. `sorryAx` is forbidden both in source and in the nanoda permitted-axiom list.

## Dynamic metadata authority

The literal final candidate SHA/tree, six implementation-head workflow run/job identifiers, artifact IDs and SHA-256 digests, integration method, actual final target SHA/tree, six post-integration workflow identifiers, preservation-comment IDs, review resolution IDs, and final changed-path summary are recorded in the authoritative acceptance comment on the clean final reconciliation PR.

This comment is incorporated into this record by reference because a Git commit cannot contain its own SHA or future workflow identifiers.
