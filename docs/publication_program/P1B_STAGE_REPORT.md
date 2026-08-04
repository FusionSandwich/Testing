# P1B stage report — sharp universal sampled quadratic-defect bound

## Frozen input and non-overwriting work line

P1B starts from the exact accepted P1A archive:

```text
P1A archive:
    archive/afp-publication-p1a-quadratic-foundation-verified

P1A commit:
    5ef6bf3335f72e38987df6b06e30d712de4b86c7

P1A tree:
    dc54b3e9d3e95eaa702a09eb74784b4a5027cd8f

P1B branch:
    agent/afp-publication-p1b-sharp-defect-bound-5ef6bf33

P1B archive after exact-head verification:
    archive/afp-publication-p1b-sharp-defect-bound-verified
```

The P1A branch, P1A archive, P0 archives, accepted Prompt-1-through-Prompt-4
archives, and immutable transport archive remain read-only. P1B is a normal
descendant and introduces no transport work.

The literal P1B commit/tree, workflow run/job identifiers, artifact IDs and
digests, archive equality, and final PR disposition are recorded in the
authoritative PR discussion because a commit cannot contain its own SHA.

## Correct theorem boundary

The theorem assumes:

```text
finite nonempty I;
d>=2;
w_i>0 and sum_i w_i=1;
unit nodes Omega_i in S^(d-1);
nonnegative off-diagonal jump rates with shared reversible conductances;
L Omega=-(d-1)Omega.
```

It does **not** assume:

```text
S_2 injective;
equal masses;
regular degree;
transitivity;
complete support;
connectedness;
distinct nodes;
full-dimensional node span;
invariance of im S_2 under L+2dI.
```

The sampled defect is automatically meaningful: for every node,
`(S_2 Z_i)_i=(d-1)/d>0`, so zero sampling rank is impossible. The coordinate
eigenmap and positivity also imply `r_i>0`, hence `r_max>0`.

## Proved theorem

With

```text
E_epsilon = sum_i w_i epsilon_i^2
E_B       = sum_i w_i ||B_i||_F^2,
```

P1B proves

```text
D_2^2 >= d^2/(d-1)^2 E_epsilon + d/(d-1) E_B,

D_2 >= d/(d-1) sqrt(E_epsilon)
    >= d(d-1)/r_max,

D_2 r_max >= d(d-1).
```

For `d=3`, `D_2 r_max>=6`.

The displayed anisotropy coefficient requires no correction. It follows from

```text
tr G_S = (d-1)/d,
tr G_R = d/(d-1) E_epsilon + E_B,
tr G_R <= D_2^2 tr G_S.
```

The regular simplex attains equality in every dimension, so the constant is
sharp. The cross-polytope and hypercube give additional all-dimensional
sharpness families.

## Equality theorem

Equality in the generalized norm/trace step is equivalent to

```text
G_R = D_2^2 G_S on K_X^perp,
```

or to the quotient residual having constant singular value:

```text
bar R_2^* bar R_2 = D_2^2 I.
```

This alone need not make `R_2` a scalar multiple of `S_2`.

Equality in the first scalar bound additionally requires `B_i=0` for every
positive-mass vertex. Equality in the RMS rate floor is equivalent to

```text
epsilon_i=(d-1)^2/r_max,
r_i=r_max,
local loss variance=0
```

at every vertex.

Complete equality in `D_2 r_max>=d(d-1)` is equivalent to

```text
r_i=r_max;
local loss variance=0;
B_i=0
```

for every vertex. Then

```text
M_i=[d(d-1)/r_max] Z_i,
R_2=[d(d-1)/r_max] S_2
```

on both the coefficient space and the sampled quotient.

## Independent proof routes

The ordinary theorem contains four complete routes:

1. weighted Gram operators and the deflated generalized eigenvalue;
2. Hilbert--Schmidt norm of the quotient factorization `R_2=US_2`;
3. isotropic random traceless-matrix averaging;
4. finite-frame/covariance domination.

The semigroup route was screened and not used because `im S_2` is not
invariant under `L+2dI` under the minimal hypotheses.

## Exact deterministic audit

Run:

```text
cd afp_barrier_gate1
python pure_math/covariance/p1b_sharp_quadratic_defect_audit.py
```

The audit checks 24 exact fixtures:

```text
simplex, cross-polytope and hypercube for d=2,3,4;
all five three-dimensional Platonic graphs;
aliased antipodal pair;
unequal-mass repeated-node generator;
positive non-invariant sampled range;
exact spherical prism with genuine sampled modes;
positive both-defects cube;
degenerate equatorial hexagon;
disconnected equality generator;
four exact nearly singular sampling configurations.
```

It verifies every trace, strong bound, scalar bound, product bound, equality
condition, quotient deflation, generalized saturation, and selected random
matrix average. It rejects weight-normalization, anisotropy-coefficient,
generator-sign, unweighted-adjoint, raw-pencil, compression-square, and
form/sample-space mutations.

## Formal core

P1B adds:

```text
afp_barrier_gate1/AFPBarrier/QuadraticFidelityLowerBound.lean
```

The module formalizes:

```text
finite weighted coordinate analysis and energy;
operator-energy domination implies weighted trace domination;
the exact d/(d-1) trace coefficient conversion;
the universal rate-product scalar step;
the specialized S^2 constant 6.
```

The accepted P1A modules retain the quotient factorization, sampling-kernel
containment, weighted row Gram identities, two-defect decomposition, and
noninjective rank formulas. The aggregate import and focused axiom audit are
extended. `sorry`, `admit`, `sorryAx`, user axioms, and project constants are
forbidden.

## Prior-art boundary

M3--M9 provide quadrature-cardinality, geometry-specific discrete Laplacian,
positive-stencil, sparsifier, spectral-convergence, association-scheme, and
spherical-design context. None proves the finite quotient trace inequality or
its equality theorem. No external theorem is used in the P1B proof.

## Acceptance contract

The dedicated exact-head workflow must pass on the literal P1B branch and,
after create-only freezing, on the immutable P1B archive. It must run:

```text
P1B exact audit;
every retained P1A and Prompt-1-through-Prompt-4 regression;
source-pinned Plantri enumeration of 9,150 maps;
full Lean 4.30 build;
focused P1B compilation and axiom audit;
placeholder and project-axiom scans;
exact ancestry and immutable-ref checks;
generated-artifact rejection;
git diff --check;
clean-checkout verification;
source and evidence artifact hashing.
```
