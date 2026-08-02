# Prompt 2 completion progress

## Authoritative starting point

```text
repository=FusionSandwich/Testing
accepted_prompt1_commit=923dc47dae4f83dbea9cd56aa904164c6378e52d
accepted_prompt1_tree=906449c151fd97756a10fb83e7106a2e6ba39b0f
saved_prompt2_wip_commit=9cfacd0cb55b8f12f802beae86a4708f96ed7aa3
saved_prompt2_wip_tree=efeedbc492764a3ddc844ae7427961f84cbf4a6b
saved_prompt2_wip_parent=923dc47dae4f83dbea9cd56aa904164c6378e52d
completion_branch=agent/afp-pure-math-p2-quadratic-covariance-completion
immutable_transport_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
```

All three WIP identities above were independently verified with Git.  The
completion branch was created remotely from the exact WIP commit.  The current
pure-math integration branch `agent/afp-pure-math-p0-m1` is separately at
`c88b57533c3c8ad8fd819e4e52a74c4b5a245479`; it is not silently substituted
for the literal WIP baseline required by this completion task.

The mutable remote branch
`agent/afp-pure-math-p1-local-global-corrected` has advanced beyond its
accepted checkpoint.  This task therefore identifies Prompt 1 by the immutable
commit and tree above, not by the present branch tip.

## Initial saved-checkpoint verification

The exact CI dependency versions are Python 3.12, NumPy 2.3.2, SymPy 1.14.0,
and Lean/Mathlib 4.30.0.  With those Python versions installed in an isolated
environment, the following WIP checks pass:

- Python bytecode compilation;
- the Prompt 1 claim-falsification audit;
- the legacy covariance audit;
- the exact local/global audit;
- the independent rational spherical-feasibility audit; and
- the signed-cube exact restoration audit, including attained undirected
  negative mass `2`.

The remaining long exact audits and the Lean checks are rerun after the first
repair round so that their logs refer to a stable candidate rather than an
ephemeral environment setup.  The pinned Lean dependencies have been resolved.
The Mathlib binary cache must use a writable task cache in this container.

## Demonstrated WIP completion gaps

The checkpoint is useful but is not a completed Gate-2 result.  The initial
line-by-line audit demonstrates these gaps:

1. no weighted-reversible centering corollary is formalized;
2. the sphere residual and full sampled-dimension equality are not yet
   formalized as the explicit finite-dimensional theorem requested here;
3. the signed one-shell radial/tangent decomposition and `R = D S_X` theorem
   have no dedicated Lean module;
4. the finite distinct-eigenvalue direct-sum/rank theorem has no Lean module;
5. there is no tracked exact `D_3` counterexample implementation;
6. the prism certificate omits explicit connectivity and vertex-transitivity
   regressions;
7. the signed-cube script does not yet certify every requested sampling rank,
   alias, averaging, and optimality item;
8. the ordinary theorem draft does not yet contain the complete weighted,
   isotypic, semigroup, and spectral-sampling proofs required by the task;
9. the main claim-control documents and pure-math README are not synchronized
   with this stronger theorem package; and
10. no dedicated Prompt-2 completion workflow exists on this WIP branch.

No missing item above is treated as proved merely because a comment, numerical
rank, or theorem-registry row says so.

## Accepted correction to the spectral-sampling statement

The literal implication from pairwise-distinct harmonic degrees is false
without a dimension or distinct-target condition.  The exact rejected witness
is

```text
d=1
I={*}
Phi(*)=+1 in S^0
L=0
D={0,1}
V_0=V_1=R^I
r_0=r_1=1
lambda_0=lambda_1=0
```

Thus both requested scalar actions hold, while `V_0` and `V_1` are not an
internal direct sum and `r_0+r_1=2>|I|=1`.  The unrestricted
pairwise-distinct-degree claim is `REJECTED`.

The corrected abstract theorem assumes pairwise-distinct **target
eigenvalues**, or first replaces all spaces with the sum belonging to each
equal-target class.  For spherical harmonics, `d>=2` makes
`ell -> ell(ell+d-2)` strictly increasing, so the desired distinct-degree
corollary is then valid.  In `d=1`, all direct-sum and rank counts are made only
after grouping equal `ell(ell-1)` classes.

The converse similarly works with target-class sums.  The zero-target class is
enlarged by `span{1}` exactly once; when degree zero is already included, its
sampled space is the constants and is not counted twice.  Weighted
reversibility requires mutual weighted orthogonality of all distinct target
classes, in particular constants against every nonzero-target sampled space.

## Mechanism-based audit state

| mechanism | current evidence | completion gate |
|---|---|---|
| finite product/covariance algebra | Lean declarations plus exact algebra | retain, extend, axiom-audit |
| sampling quotient | generic Lean kernel/rank lemmas | explicit range and dimension theorem |
| positive radial obstruction | ordinary proof and exact examples | proof audit and final mapping |
| signed one-shell geometry | ordinary coordinate derivation | narrow Lean algebraic core |
| exact finite examples | WIP SymPy scripts | missing graph, `D_3`, alias, and LP certificates |
| equivariant decomposition | ordinary outline | full multiplicity/isotypic proof and counterexample |
| signed optimization | exact optimizer and piecewise bound | explicit averaging and dual/subgradient certificate |
| spectral sampling | exact harmonic ranks, Pell recurrence, and the exact rejected (d=1) one-node witness | formalize the target-eigenvalue-class theorem; state the (d\ge2) degree corollary and constants-safe converse |
| semigroup/Jensen | correct outline and Boolean regression | complete separated proofs |
| claim control and CI | WIP registries only | repository-wide synchronization and dedicated workflow |

## Scope guard

This branch does not redo Prompt 1, begin Prompt 3 triangulation or
near-rigidity, or alter transport, Radiant, HTS, multigroup, spatial-solver, or
evaluated-material work.  The transport archive remains immutable.
