# P1C stage report — exact equality geometry and extremizing families

## Frozen input and additive work line

P1C starts from the exact accepted P1B archive:

```text
P1B archive:
    archive/afp-publication-p1b-sharp-defect-bound-verified

P1B commit:
    58b4fd93ea2bc95c4f1aee909a298e3a64a4d4fd

P1B tree:
    4b715d6999a3b69baf9c08062cc5ea01f60a5498

P1C branch:
    agent/afp-publication-p1c-equality-geometry-58b4fd93

P1C archive after exact-head verification:
    archive/afp-publication-p1c-equality-geometry-verified
```

P1C is a normal non-merging descendant. The P1B/P1A archives, accepted
Prompt-1-through-Prompt-4 archives, and transport archive remain read-only.
The literal P1C commit/tree, workflow and artifact identifiers, archive
equality, and PR disposition belong in the authoritative PR discussion,
because a commit cannot contain its own identifier.

## Exact local equality theorem

At vertex `i`, set

```text
u_i   = Omega_i
P_i   = I-u_i u_i^T
tau_ij=P_i Omega_j
h_i   = sum_j a_ij ell_ij tau_ij
T_i   = sum_j a_ij tau_ij tau_ij^T.
```

P1C proves

```text
Delta_ij=-ell_ij u_i+tau_ij,
||tau_ij||^2=ell_ij(2-ell_ij),

C_i=epsilon_i u_i u_i^T-u_i h_i^T-h_i u_i^T+T_i,

B_i=-u_i h_i^T-h_i u_i^T
    +T_i-[2-epsilon_i/(d-1)]P_i,

||B_i||_F^2
  =2||h_i||^2+||T_i-[2-epsilon_i/(d-1)]P_i||_F^2.
```

Thus `B_i=0` is exactly zero radial--tangential covariance plus isotropic
tangent covariance. With zero loss variance, all active losses equal
`ell_i=(d-1)/r_i`, `epsilon_i=(d-1)ell_i`, and the condition becomes

```text
T_i=(2-ell_i)P_i.
```

For `0<ell_i<2`, normalization by
`sqrt(ell_i(2-ell_i))` converts this into a centered
probability-weighted unit-norm tight frame in `T_{Omega_i}S^(d-1)`. At
`ell_i=2`, all projected increments vanish and the raw theorem remains true,
but no unit tangent frame exists.

## Complete equality and quotient theorem

The following are equivalent:

```text
D_2 r_max=d(d-1);
all r_i equal r_max, all active losses equal (d-1)/r_max,
all mixed covariances vanish, and all tangent moments are isotropic;
all r_i equal r_max, local loss variance is zero, and B_i=0;
M_i=c_* Z_i for every i;
R_2=c_* S_2 on the coefficient space and sampled quotient,

c_*=d(d-1)/r_max.
```

The quotient statement controls the map into the whole weighted sample
space; projecting away orthogonal leakage would be insufficient. No sampling
injectivity is assumed. Since `c_*>0`, every equality case satisfies

```text
ker R_2=ker S_2=K_X,
e_2=dim(im S_2 intersect ker(L+2dI))=0.
```

## Global algebraic assembly and classification boundary

In the nonantipodal branch, put `t=1-ell_*` and `p_ij=a_ij/r_*`. Equality is
equivalent to a reversible Markov kernel supported on the common latitude
`Omega_i dot Omega_j=t`, with conditional mean `t Omega_i` and conditional
second moment

```text
t^2 Omega_i Omega_i^T
  +(1-t^2)/(d-1) [I-Omega_i Omega_i^T].
```

P1C also gives the equivalent positive-semidefinite rank-`d` Gram equations,
the endpoint-reversal identity, and Kolmogorov's exact cycle-product
criterion for reversible masses. These are the missing global gluing data.

Two restricted classifications are complete:

1. distinct complete support gives the regular simplex (or the two-node
   antipodal case);
2. on `S^2`, distinct vertices of a strictly convex inscribed polyhedron,
   convex-hull one-skeleton support, common active rates, nonantipodal edges,
   and common degree `3..5` give exactly the five Platonic solids.

No unrestricted Platonic classification is claimed. Connected graph covers
and blow-ups, a distinct long-chord icosahedral equality shell, nonregular
weighted tight frames, and higher-shell cube embeddings show why additional
graph, embedding, shell, and reversibility hypotheses are necessary.

## Exact infinite families

For every `d>=2`, P1C proves:

| family | support | `r` | `ell` | `epsilon` | residual scalar `D_2` | `D_2 r` |
|---|---|---:|---:|---:|---:|---:|
| regular simplex | complete | `d(d-1)/(d+1)` | `(d+1)/d` | `(d^2-1)/d` | `d+1` | `d(d-1)` |
| cross-polytope | nonantipodal orthogonal pairs | `d-1` | `1` | `d-1` | `d` | `d(d-1)` |
| hypercube | Hamming-distance-one edges | `d(d-1)/2` | `2/d` | `2(d-1)/d` | `2` | `d(d-1)` |

The ordinary theorem gives exact coordinates, weights, conductances, directed
rates, covariance matrices, residual rows, tangent frames, sampling ranks,
kernels, and aliases for all three families.

## Exact `d=3` examples and aliases

The tetrahedron, octahedron, cube, icosahedron, and dodecahedron use exact
algebraic coordinates and shortest-edge generators. Their residual scalars
are

```text
4,
3,
2,
3-3sqrt(5)/5,
3-sqrt(5),
```

and every product with the row rate is `6`. Exact sampling minors in one
fixed trace-free basis are

```text
-4/27, -2, 4/27, -16sqrt(5)/125, 16/81.
```

The first three kernels have dimensions `2,3,2`; the last two kernels are
zero. In the tetrahedron and cube, diagonal trace-free forms are aliases; in
the octahedron, off-diagonal forms are aliases. Because `R_2=cS_2`, all of
these algebraic exact forms sample to zero and none is a nonzero exactly
reproduced `H_2` mode.

## Exact regression and formal core

Run:

```text
cd afp_barrier_gate1
python pure_math/covariance/p1c_equality_geometry_audit.py
```

The exact audit has 20 equality fixtures: the three standard families for
`d=2,3,4,5`, the five Platonic examples, the antipodal endpoint, a connected
twofold tetrahedral blow-up, and the long-chord icosahedral shell. It also
checks the block identities, tight-frame normalization, sampling minors,
aliases, a nonregular weighted frame, and a cycle-product mutation.

The Lean module

```text
AFPBarrier/QuadraticEqualityGeometry.lean
```

formalizes the finite division-free increment and moment algebra and the
guarded conversion to normalized tangent weights. The aggregate import and
focused axiom audit include it. `sorry`, `admit`, `sorryAx`, user axioms, and
project constants are forbidden.

## Prior-art boundary

Izmestiev--Lam provide a special spherical Delaunay Laplacian;
Martin--Tanaka provide association-scheme structure; Bannai--Bannai provide
spherical-design moment language; and Ahrens--Beylkin provide invariant
spherical quadrature constructions. None proves the P1C local block converse,
arbitrary-weight global assembly criterion, sampling-alias result, or
restricted classifications. The classical convex regular-polyhedron theorem
is used only at the final step of the explicitly restricted `S^2` corollary.

## Acceptance contract

The dedicated exact-head workflow must pass on the literal P1C branch and,
after create-only freezing, on the immutable P1C archive. It must run:

```text
P1C exact audit and retained P1B/P1A regressions;
every retained Prompt-1-through-Prompt-4 exact regression;
source-pinned Plantri enumeration of 9,150 maps;
full Lean 4.30 build;
focused P1C compilation and axiom audit;
placeholder and project-axiom scans;
exact P1B ancestry and immutable-ref checks;
the exact 13-path scope check;
generated-artifact rejection;
git diff --check and clean-checkout verification;
source and evidence artifact hashing.
```
