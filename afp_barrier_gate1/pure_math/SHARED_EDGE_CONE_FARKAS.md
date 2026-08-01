# Global shared-edge cone and Farkas theorem

Let `V` be finite, `w_i>0`, `Omega_i in S^2`, and let `G=(V,E)` be an
undirected permitted graph. For `e={p,q}`, define the column `g_e` by

```text
(g_e)_p=Omega_q-Omega_p,
(g_e)_q=Omega_p-Omega_q,
(g_e)_i=0 otherwise.                                        (1)
```

Let `A` have these columns and set `b_i=-2w_i Omega_i`. One shared
conductance per edge gives rates `a_ij=gamma_{ij}/w_i`, and degree-one
exactness is exactly

```text
A gamma=b,  gamma>=0.                                       (2)
```

## Cone and feasible polytope

Define

```text
K_G=A R_+^E=cone{g_e:e in E},
P_G(b)={gamma>=0:A gamma=b}.                                 (3)
```

Then `P_G(b)` is nonempty exactly when `b in K_G`. It is a closed convex
polyhedron with recession cone `{d>=0:Ad=0}`. If every permitted edge joins
distinct spherical nodes, this recession cone is zero and the feasible set is
a compact polytope, because

```text
sum_i <Omega_i,(Ad)_i>
 =-sum_{e={p,q}} d_e ||Omega_p-Omega_q||^2.                  (4)
```

For `d>=0` and `Ad=0`, every coefficient vanishes. A duplicate-node edge has
a zero column and creates an explicit `R_+` factor; deleting zero columns
restores compactness. For every feasible vector, the same identity gives

```text
sum_e gamma_e(1-Omega_p·Omega_q)=sum_i w_i.                  (5)
```

Each edge column sums to zero over its endpoints, so every signed or
nonnegative shared solution satisfies the necessary condition

```text
sum_i w_i Omega_i=0.                                        (6)
```

For the complete graph, (6) is sufficient. With `W=sum_i w_i`, set

```text
gamma_ij=2 w_i w_j/W,  i!=j.                                (7)
```

Then every conductance is positive and

```text
sum_{j!=i} gamma_ij(Omega_j-Omega_i)
 =(2w_i/W)(sum_j w_j Omega_j-W Omega_i)
 =-2w_i Omega_i.
```

This construction is formalized in `AFPBarrier/CompleteGraph.lean`.

## Full finite-dimensional alternative

For nodal dual vectors `y_i in R^3`, define the orientation-independent strain

```text
sigma_e(y)=(A^T y)_e
          =(y_p-y_q)·(Omega_q-Omega_p).                      (8)
```

Because `K_G` is a finitely generated closed cone, finite-dimensional strong
separation gives exactly one of

```text
Primal: exists gamma>=0 with A gamma=b;
Dual:   exists y with sigma_e(y)>=0 for every edge
        and b·y<0.                                           (9)
```

The blocks are mutually exclusive since a primal and dual pair would give

```text
b·y=(A gamma)·y=sum_e gamma_e sigma_e(y)>=0.
```

If the primal is infeasible, strict separation of `b` from the closed cone
supplies a functional nonnegative on every generator and negative on `b`,
which is precisely the second block. Thus (9) is the full Farkas alternative,
not only certificate soundness.

The first variation of half the squared chord under nodal displacement `y` is

```text
(y_q-y_p)·(Omega_q-Omega_p)=-sigma_e(y).
```

A dual certificate therefore does not increase any permitted squared chord to
first order, while

```text
b·y=-2 sum_i w_i Omega_i·y_i<0
```

means strictly positive weighted radial work. The strain identity and its sign
are formalized in `AFPBarrier/SharedEdgeGeometry.lean`; weak certificate
soundness is formalized in `AFPBarrier/DualCertificate.lean`.
