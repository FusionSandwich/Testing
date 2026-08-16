# Proposition 7.3 dependency audit

## Dependency classification

| Later claim | Unperturbed `d=3` construction | Fixed-level theorem | Uniform all-level theorem | Support preservation | Explicit constants | Positivity margin | Sampling-frame stability | Connectivity | Rate | Quadratic defect |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Theorem 7.2 matching-order family | yes | no | no | no | yes, `64 pi^2`, `75/2` | base proof | no | yes | yes | yes |
| Proposition 7.3 existence/uniqueness | yes | yes | no | yes | radius computable, not numerically emitted | yes | no | yes | inherited | inherited |
| Proposition 7.3 conservative bounds | yes | yes | no | yes | `1024`, `54` | yes | no | yes | yes | yes |
| abstract robustness sentence | no | yes | no | yes | says level-dependent | yes | no | no | scoped | scoped |
| registry status | yes | yes | explicitly rejected | yes | exact boundary | yes | no | yes | yes | yes |
| Lean claims | finite identities only | no analytic radius claim | no | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| numerical regression | diagnostic | exercises fixed support | not proof | yes | checks conservative bounds | checks finite positivity | no | yes | yes | yes |

## Reconstructed proof chain

1. Sections 1--9 of the P1E source construct the exact unperturbed `M_0=2^80` family and
   establish strict positivity, fixed support, reversibility, exact coordinate
   fidelity, the row multiplier, and the sharper unperturbed constants.
2. At a fixed level, the row equations form a finite block-lower-triangular
   system. The first-row, ordinary, transition, and equatorial diagonal blocks
   are nonsingular at the base point.
3. Strict base positivity supplies a positive finite margin. Analyticity and
   the Neumann lemma supply a unique positive solution on a level-dependent
   neighborhood.
4. Fixed incidence plus positive conductances preserves connectivity and
   shared-edge compatibility. The exact moment equations preserve
   reversibility and `H_0 direct-sum H_1` fidelity.
5. The loss-force and isotropy equations preserve the rowwise scalar
   quadratic residual. Therefore no lower sampling-frame constant is needed.
6. Reducing the neighborhood to preserve active chords in
   `[h_J/16,6h_J]` gives the publication constants `1024` and `54`.

## Uniform route

No later proved theorem needs a radius uniform in `J`. The old universal
statement was therefore removed rather than used as a hidden premise. The
uniform route is explicitly `REJECTED`: its claimed majorant lacked a literal
expression graph, verified operation count, denominator guards, inverse
bounds, positivity margins, and recurrence certificate.

## Formal and computational scope

The Lean module proves finite identities after conductances are supplied; it
contains no theorem asserting the analytic perturbation radius. Numerical
scripts are regression and adversarial evidence only. Tests may not label a
finite sweep as proof of either the fixed-level theorem or a uniform theorem.
