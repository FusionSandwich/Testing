# Strict shared-edge feasibility and sensitivity

Use the cone `K_G=A R_+^E` and target `b_i=-2w_i Omega_i` from the global cone
proof.

## Strict all-edge feasibility

For the indexed edge columns,

```text
exists gamma_e>0 for every e with A gamma=b
iff b is in ri K_G.                                         (1)
```

A positive combination of every indexed generator lies in the relative
interior. Conversely, if `b in ri K_G`, then for each generator `g_k` a small
move `b-epsilon_k g_k` remains in the cone. Represent that point by
nonnegative generators, add the positive `epsilon_k` coefficient on `g_k`, and
average over all indexed edges. This assigns a positive coefficient to every
edge. Repeated and zero columns do not invalidate the argument; a zero column
may be assigned an arbitrary positive coefficient.

The exact dual-face criterion is

```text
b in ri K_G
iff [A^T y>=0 and b·y=0 imply A^T y=0].                     (2)
```

Indeed, a supporting dual at a relative-interior point must annihilate the
whole span of the cone. Conversely, a relative-boundary point has a supporting
functional nonnegative on the cone, zero on `b`, and positive on at least one
generator. The forward finite consequence of (2) is formalized in
`AFPBarrier/DualComplementarity.lean`.

Define the uniform all-edge slack

```text
tau_* = sup{tau: exists gamma with A gamma=b
                  and gamma_e>=tau for every e}.             (3)
```

Then `tau_*>0` exactly under strict all-edge feasibility. If all edge columns
are nonzero, the feasible set is compact and this supremum is attained.

## Fixed-matrix target or mass perturbations

Suppose `A gamma^0=b` and `gamma^0_e>=alpha>0`. Let
`r=b'-b in range A`, and let `sigma_+(A)` be the smallest nonzero singular
value. The Moore-Penrose correction `d=A^+r` obeys

```text
||d||_2<=||r||_2/sigma_+(A).
```

Therefore

```text
||b'-b||_2<alpha sigma_+(A)
=> exists gamma'>0 with A gamma'=b'.                         (4)
```

The range condition is essential: weighted centering need not describe the
whole range for a sparse graph. For fixed nodes and perturbed masses,

```text
||b'-b||_2=2 (sum_i |w'_i-w_i|^2)^(1/2).                    (5)
```

Equivalently, the relative cone depth
`dist(b,relbd K_G)` is a direct target radius for perturbations constrained to
`span K_G`.

## Perturbed nodes and masses

Assume

```text
max_i ||Omega'_i-Omega_i||<=eta_Omega,
max_i |w'_i-w_i|<=eta_w,
w_i<=w_max,
n=|V|, m=|E|.
```

The actual spherical matrix and target satisfy

```text
||A'-A||_2<=||A'-A||_F<=2 sqrt(2m) eta_Omega,                (6)
||b'-b||_2<=2 sqrt(n)(eta_w+w_max eta_Omega
                      +eta_w eta_Omega).                     (7)
```

Each perturbed edge column has two opposite blocks of norm at most
`2 eta_Omega`, proving (6). The identity

```text
w'_i Omega'_i-w_i Omega_i
=(w'_i-w_i)Omega_i+w_i(Omega'_i-Omega_i)
 +(w'_i-w_i)(Omega'_i-Omega_i)
```

proves (7).

Assume the perturbed signed equation is compatible,
`b'-A'gamma^0 in range A'`, and let `sigma'_+=sigma_+(A')`. A positive exact
solution persists whenever

```text
2 sqrt(n)(eta_w+w_max eta_Omega+eta_w eta_Omega)
+2 sqrt(2m) eta_Omega ||gamma^0||_2
<alpha sigma'_+.                                             (8)
```

The pseudoinverse correction has 2-norm less than `alpha`, hence every
coefficient stays positive. In a fixed full-row-rank reduction, Weyl's bound
allows `sigma'_+` to be replaced by
`sigma-||A'-A||_2` when this is positive.

For a linear objective, the same constructed solution gives the one-sided
bound

```text
c'·gamma'-c·gamma^0
<=||c'-c||_2 ||gamma^0||_2
 +||c'||_2[||b'-b||_2+||A'-A||_2||gamma^0||_2]/sigma'_+.     (9)
```

Applying the argument in reverse gives a two-sided optimal-value bound when
both problems have the stated strict slack and compatibility.

## Complete-graph sensitivity

For a complete graph, compatibility is exactly weighted centering. If
`|w'_i-w_i|<=eta<w_min`, `n eta<W`, and the perturbed nodes and masses remain
centered, the explicit construction gives

```text
gamma'_{ij}>=2(w_min-eta)^2/(W+n eta)>0,                     (10)
```

and

```text
|gamma'_{ij}-gamma_{ij}|
<=2(2w_max eta+eta^2)/(W-n eta)
 +2w_max^2 n eta/[W(W-n eta)].                               (11)
```

The node positions may move arbitrarily on the sphere; the same formula remains
exact whenever the new weighted-centering equation holds.
