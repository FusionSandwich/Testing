# Prompt 2 sampled quadratic covariance integration record

## Integrated stage

- Repository: `FusionSandwich/Testing`
- Requested target branch: `agent/afp-pure-math-p0-m1`
- Original P0/M1 checkpoint:
  `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Corrected Prompt 1 baseline:
  `923dc47dae4f83dbea9cd56aa904164c6378e52d`
- Prompt 2 exact theorem head before reconciliation:
  `478055166fc874a519865506989586c3e02dc583`
- Final corrected reconciliation head:
  `dd3ea8ee612958f223bbbf05cf5de926377cd5a1`
- Prompt 2 merge into corrected Prompt 1 branch:
  PR `#17`, squash commit `f1cea9c13a3de28288470a53b67ad852aaa3635b`
- Corrected Prompt 1 plus Prompt 2 merge into the requested target:
  PR `#18`, squash commit `f9fb1e336a4569c2d7e2e440821976bd30a6c29f`

The stage is confined to the pure-mathematics package, exact symbolic
regressions, Lean finite algebra, claim-control documentation, and dedicated
verification workflows. The immutable transport archive
`archive/afp-gate6-spatial-multigroup-verified` at
`515f1aae6c20bd85711c90b5c1c21b4905252d01` was not modified. No transport,
Radiant, HTS, multigroup, or spatial-solver work was added.

A literal multiagent-v2 runtime was not available in this execution
environment. It was not used and is not claimed. Independent covariance,
sampling, symmetry, signed-construction, product, harmonic, exact-symbolic,
and Lean audit routes are recorded in the Prompt 2 stage report.

## Mathematical correction made during audit

The earlier candidate treated the covariance-constraint and quadratic
sampling maps as if they were unrelated. In the spherical degree-two problem,
the exact covariance identity instead gives

```text
R_X = (L+2d I) S_X.
```

Consequently

```text
K_X = ker S_X subset E_form = ker R_X,
E_sample = im(S_X) intersect ker(L+2d I),
dim E_sample = dim E_form-dim K_X,
dim E_sample = rank(S_X)-rank(R_X),
rank([R_X;S_X]) = rank(S_X).
```

The generic restricted-map intersection formula remains correct, but it
collapses to these sharper specialized identities. The unrelated-map negative
test was removed and replaced by exact factorization regressions.

## Integrated theorem package

The integrated stage proves:

- the finite covariance identity and exact shifted target residual;
- the trace-free form-space characterization;
- the residual-through-sampling factorization and genuine sampled-space
  formula;
- sharp axial-covariance rigidity `E_form=K_X`, `E_sample={0}`;
- a regular-simplex equality family in every dimension;
- an independent equivariant-irreducibility rigidity theorem;
- exact covariance tensors, sampling kernels, and dimensions for all five
  Platonic shortest-edge generators;
- a four-point signed restoration with forced antipodal rate `-1/2` and one
  genuine sampled quadratic mode;
- independent carre-du-champ and semigroup/Jensen product obstructions; and
- rejection of the unsupported general spectral-product hierarchy under its
  stated kill criterion after parity, equality-set, aliasing, and Pell
  resonance analysis.

## Pre-integration verification

The final reconciliation head
`dd3ea8ee612958f223bbbf05cf5de926377cd5a1` passed:

- dedicated Prompt 2 workflow run `30726175033`, job `91438236453`;
- exact head checkout assertion;
- exact symbolic covariance, factorization, Platonic, signed, and resonance
  audit;
- signed sampled-dimension check `rank S=1`, `rank R=0`,
  `dim E_sample=1`;
- full Lean 4.30 / Mathlib 4.30 package build;
- focused pure-math axiom audit; and
- independent nanoda validation.

The same reconciliation passed the corrected Prompt 1 compatibility gate in
workflow run `30726174993`, job `91438212980`.

Post-integration exact-head workflow and job identifiers are recorded in the
merged pull-request discussion and final stage response after the target-branch
runs complete. They are not used as mathematical evidence.
