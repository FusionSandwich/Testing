# Prompt 4 theorem-to-file map

This map resolves the accepted Prompt-4 candidate to ordinary proofs, exact
current-API declarations, and deterministic falsification support.  Workflow
run and artifact identifiers are supplied by the resolved finalization record
because a tracked source file cannot contain its own commit hash.

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
| Delsarte reduction as a new barrier | REJECTED | approach registry and counterexample catalogue | no false declaration | sampling/alias audit |
| blanket graph-curvature collapse | REJECTED | prior-art and counterexample boundary | no false declaration | one-function identity boundary |
| established graph-curvature and discrete-transport frameworks | EXTERNAL | primary-source prior-art map | no project axiom | not claimed computationally |
| new compact-space or split/merge construction | CONJECTURE | numerical-analysis handoff only | no declaration | no theorem claimed |

The synthesis package, assumptions table, counterexample catalogue, abstract,
claim matrix, prior-art map, stage report, salvage ledger, and workflow are all
bound by the dedicated path allowlist.  The final run and artifact manifests
bind their exact blobs at the tested remote head.

The formal declaration map is recorded exactly in
`pure_math/barriers/P4_SALVAGE_LEDGER.md`. In particular, the current port
strengthens the polar solve to retain the raw transverse factor and adds
`projectiveQuality_from_fixedMoment` and
`twoLossWeightedQuality_sub_one` for the two adversarially corrected
boundaries.

## Exact Lean declaration set

```text
squarePolarQualityFromStep
squarePolarQualityFromStep_formula
squarePolar_rates_forced
squarePolar_totalRate_forced
squarePolar_forced_quartic_lower
cscSquaredTruncation
squarePolarRateMainStep
cscSquaredTruncation_rate_identity
squarePolarRateMainStep_grid
squarePolarQualityMainStep
squarePolarQualityMainStep_grid
universal_rate_lower_of_defect_upper
finiteExtremal_defect_lower
projectiveQuality_from_fixedMoment
twoLossWeightedQuality_sub_one
twoLossQuality_sub_one
biregular_interRing_incidence
perfectMatching_ringCounts_eq
```

`squarePolar_rates_forced` accepts the raw transverse nonzero factor and
derives left/right equality.  `projectiveQuality_from_fixedMoment` formalizes
the corrected arbitrary-`lambda` normalization.
