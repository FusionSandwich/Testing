# M1 exact-feasibility approach registry

This registry groups routes by mathematical mechanism.  A reduction is not
counted as progress when its next step is a selection, compatibility, or
sensitivity lemma equivalent in strength to the target.

| Family | Mechanism | Independent target | Final state | Reopening criterion |
|---|---|---|---|---|
| L-CG | finite convex geometry | hull/relative-interior dependence, including repetitions and lower dimension | resolved | n/a |
| L-BC | barycentric construction | quantitative all-positive dependence from a centered inball | resolved constructively | n/a |
| L-OM | oriented matroids | support-minimal dependences and uniqueness | closed as unnecessary | a sharper circuit invariant |
| L-AS | antipodal splitting | isolate the zero-tangent antipodal budget | resolved | n/a |
| Q-SF | support functions | inradius duality and Hausdorff perturbation | resolved in a fixed or identified span | n/a |
| Q-SV | singular values | explicit right inverse and conditioning | resolved with `1/sigma` bounds | n/a |
| G-CN | conic duality | shared-edge cone and exact Farkas signs | resolved | n/a |
| G-LP | LP duality | rate, peak, and residual primal/dual blocks | resolved by exact finite LP transfer | n/a |
| G-EX | exact obstruction | locally feasible but globally infeasible graph | resolved by the alternating-mass four-cycle | n/a |
| G-GA | group averaging | reconcile equivariant oriented rows | resolved | n/a |
| F-LA | Lean finite algebra | scaling, antipodal budget, averaging, certificate arithmetic | implemented | reopen only for more convex-analysis formalization |
| A-DG | degeneracy audit | antipodes, repeats, boundary, zero coefficients, lower dimension | passed after corrections | any new counterexample |
| A-GC | compatibility audit | orientations, unequal masses, centering, rank loss | passed with compatibility explicit | any new counterexample |

## Blocked-route rule

A family is marked **blocked** when its next step is an unproved theorem-strength
selection, compatibility, or sensitivity statement.  It is reopened only after
an explicit new construction, invariant, or dual certificate is supplied.

## Cross-pollination record

The local convex, global conic, exact-certificate, and symmetry routes were
developed independently through the first round.  They were combined only
after separate audits fixed the intrinsic-span hypothesis for local
perturbations and the range/centering hypothesis for global perturbations.
