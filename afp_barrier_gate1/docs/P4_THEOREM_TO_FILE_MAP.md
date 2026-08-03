# Prompt 4 theorem-to-file map

This map is initialized before selective salvage.  It will be resolved to
exact declarations and successful regression evidence at the final Prompt-4
candidate.

| Theorem family | Claim status target | Ordinary proof | Lean support | Deterministic support |
|---|---|---|---|---|
| controlled cosecant expansion and polar remainders | PROVED | `pure_math/barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | `AFPBarrier/SharpProductBarriers.lean` finite coefficient transfer | `pure_math/barriers/prompt4_sharp_barrier_audit.py` |
| asymmetric polar solve and fixed-graph minimax | PROVED | sharp-barrier theorem | `SharpProductBarriers.lean` polar declarations | Prompt-4 exact audit plus retained equal-angle audits |
| universal/quasi-uniform rate transfer | PROVED | sharp-barrier theorem | universal rate declaration | Prompt-4 exact audit |
| constrained extremal lower bound and minimizer | PROVED | sharp-barrier theorem compactness section | finite lower bound only; compactness is ordinary mathematics | normalization and exclusion checks |
| feasible-cone projectivization and exact quality identity | PROVED | sharp-barrier theorem anisotropy section | finite projective examples where practical | sliced-LP primal/dual certificate |
| LP strong duality | EXTERNAL | stated standard finite-dimensional input with exact sign transfer | not a project axiom | exact certificate instances |
| equality, two-opposite, and polar anisotropy | PROVED | sharp-barrier theorem anisotropy section | two-loss declaration | exact symbolic audit |
| biregular/perfect-matching incidence | PROVED | sharp-barrier theorem reduced-ring section | incidence declarations | integer incidence checks |
| Delaunay/maximal-net existence and exact coordinate modes | EXTERNAL | assumptions table | no project axiom | not claimed computationally |
| Plantri 9,150-map census | COMPUTATIONAL | falsification boundary only | not applicable | pinned Prompt-3 census retained in CI |
| broad Delsarte, curvature, homogeneous-space, and transport upgrades | REJECTED or EXTERNAL/CONJECTURE as specified | approach registry and counterexample catalogue | no false declarations | hostile boundary regressions where applicable |

The final map will also bind the synthesis package, assumptions table,
counterexample catalogue, abstract, claim matrix, prior-art map, stage report,
salvage ledger, workflow, run, and artifacts.

The formal declaration map is recorded exactly in
`pure_math/barriers/P4_SALVAGE_LEDGER.md`. In particular, the current port
strengthens the polar solve to retain the raw transverse factor and adds
`projectiveQuality_from_fixedMoment` and
`twoLossWeightedQuality_sub_one` for the two adversarially corrected
boundaries.
