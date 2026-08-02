# Prompt 4 readiness handoff

## Readiness state

```text
PROMPT_3_STATUS=PENDING_EXACT_HEAD_CI_AND_MERGE
PROMPT_4_BASELINE_STATUS=NOT_READY
repository=FusionSandwich/Testing
accepted_target_branch=agent/afp-pure-math-p0-m1
prompt3_start_commit=c88b57533c3c8ad8fd819e4e52a74c4b5a245479
prompt3_start_tree=92b3c0eaa45dd58befbc5af59790476d5c5d85b3
prompt3_branch=agent/afp-pure-math-p3-global-rigidity-near-rigidity
prompt3_implementation_commit=PENDING_PR_DISCUSSION
prompt3_implementation_tree=PENDING_PR_DISCUSSION
prompt3_pr=PENDING_PR_DISCUSSION
prompt3_merge_commit=PENDING_PR_DISCUSSION
final_target_commit=PENDING_PR_DISCUSSION
final_target_tree=PENDING_PR_DISCUSSION
immutable_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

The exact immutable implementation, merge, final-target, and workflow/job
identifiers will be posted in the merged Prompt 3 PR discussion after literal
final-head verification.  This committed file is the durable mathematical
handoff; the PR discussion is the exact metadata record because a Git commit
cannot contain its own SHA/tree.

## Accepted Prompt 3 mathematical package after integration

Prompt 4 may use, without weakening hypotheses:

1. the exact spherical local moment and `Q` variance identities;
2. local `Q=1` active-loss equality and connected shared-edge propagation;
3. Theorem P3-R only under all ten round minor-arc geodesic-triangulation
   hypotheses;
4. exact tetrahedral/octahedral/icosahedral counts, side lengths, losses, rates,
   combinatorial uniqueness, and geometric uniqueness;
5. explicit pointwise, path, diameter, reference-loss, and arclength
   near-rigidity constants;
6. the independent Dirichlet-energy, Poincare, and effective-resistance
   refinements with the stated normalization;
7. the explicit spherical-angle/valence threshold and edge-length distance to
   the exact Platonic side;
8. the exact `Q=1` radial/tangential covariance decomposition;
9. the criterion `T_i=P_i/2` for axial covariance;
10. the weighted positive reversible octahedral anisotropy family and its
    genuine sampled-space conclusion `E_sample={0}`.

The authoritative ordinary theorem is
`pure_math/rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md`.

## Hypotheses that may not be dropped silently

The classification requires an actual finite simple sphere triangulation,
exact one-skeleton equality, injectivity, unique minor arcs in `(0,pi)`,
noncrossing edge interiors, nondegenerate geodesically convex face images,
pairwise disjoint face interiors, full round-sphere coverage/no cone defects,
strictly positive conductance on every triangulation edge, and `Q_i=1`.

The quantitative theorem additionally requires `p_ij>=kappa>0`,
`delta=sqrt(eta/kappa)<1`, the displayed loss/arclength compact-domain
conditions, and the explicit integer-valence separation inequality.  The
single conservative `eta_*` version requires the reference margins in §6.5.

## Permanent regressions

Prompt 4 must preserve:

* all five Platonic `Q=1` graph embeddings;
* cube and dodecahedron as nontriangulated unrestricted counterexamples;
* antipodal `ell=2`, disconnected, major-arc, degenerate-face, cone-defect,
  inactive-edge, noninjective, directed/nonreversible, and signed-rate tests;
* long-path, small-`kappa`, small-gap, and large-resistance stress cases;
* tetrahedral, octahedral, and cubical sampling aliases;
* signed four-cardinal restoration and signed regular-pentagon failure;
* Boolean centered resonance and the centered/Jensen distinction;
* the exact `S^2` product table and rejection of a general Prompt 2 hierarchy;
* weighted-octahedron `Q=1` tangential anisotropy and the sampling-kernel audit.

## Prompt 4 boundary

Prompt 3 does not begin or pre-judge:

```text
product-grid lower bounds;
extremal global optimization;
sharp minimax classification outside the restricted theorem;
final paper synthesis;
or any transport, Radiant, HTS, multigroup, or production-solver work.
```

Prompt 4 must branch only from the exact final target SHA/tree posted in the
merged Prompt 3 PR discussion after all final-head workflows pass.
