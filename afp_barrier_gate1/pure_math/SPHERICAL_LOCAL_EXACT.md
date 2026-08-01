# Exact local spherical feasibility

All index sets are finite, and repeated candidate indices remain separate
variables. Fix `Omega_i in S^2`. Split permitted neighbors into non-antipodal
indices `N` and antipodal indices `P`. For `j in N`, write

```text
Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,
0 < theta_j < pi,  ||u_j||=1,  u_j in T_{Omega_i} S^2.
```

Set

```text
s_j = sin(theta_j) > 0,
ell_j = 1-cos(theta_j) > 0,
q_j = ell_j/s_j = tan(theta_j/2) > 0.
```

For `p in P`, `Omega_p=-Omega_i`; its tangent contribution is zero and its
normal loss is two. No tangent direction is assigned to an antipode.
Degree-one exactness is equivalent to

```text
sum_{j in N} a_j s_j u_j = 0,
sum_{j in N} a_j ell_j + 2 sum_{p in P} a_p = 2.        (1)
```

## Finite convex lemmas

Let indexed points be `U=(u_1,...,u_m)` and `C=conv(U)`.

**Nonnegative dependence.** The following are equivalent:

1. `0 in C`;
2. some `b>=0`, `b != 0`, satisfies `sum_j b_j u_j=0`;
3. some `lambda>=0`, `sum lambda=1`, satisfies `sum lambda_j u_j=0`.

The proof is normalization by `sum b_j`; it requires neither distinct points
nor a rank condition.

**Positive indexed dependence.** The following are equivalent:

1. `0 in ri C`, relative to `aff C`;
2. there is a normalized dependence with every `lambda_j>0`;
3. there is a dependence with every `b_j>0`.

For `2 => 1`, a relative supporting functional at a boundary origin is
nonnegative on all indexed points and strictly positive on at least one. Its
pairing with a positive dependence would be strictly positive, a contradiction.
For `1 => 2`, `aff C` is a linear space. For every index `k`, relative
interiority gives a small `epsilon_k>0` with `-epsilon_k u_k in C`; hence

```text
0 = [epsilon_k/(1+epsilon_k)] u_k
    + [1/(1+epsilon_k)](-epsilon_k u_k).
```

Choose a convex representation of the second term and average these `m`
representations. The average puts positive mass on every indexed point,
including repeated and redundant points.

**Uniqueness.** Assume `0 in C`, let `F` be the minimal face of `C` containing
zero, and let `J_F={j:u_j in F}`. The normalized dependence set is a singleton
iff the augmented indexed vectors `(u_j,1)`, `j in J_F`, are linearly
independent; equivalently, those indexed points are affinely independent;
equivalently, the nonnegative dependence cone is one ray.

Every representation of zero uses only `F`. Since `0 in ri F`, one
representation is positive on all of `J_F`. An augmented dependence `d` then
produces two feasible representations `lambda +/- epsilon d`; conversely, the
difference of two representations is an augmented dependence. Thus repeated
or affine-redundant points cause nonuniqueness but not loss of strict
feasibility.

## Non-antipodal theorem

Assume `P` is empty and `N` is nonempty.

- A nonnegative exact row exists iff `0 in conv{u_j}`.
- A row positive on every permitted edge exists iff
  `0 in ri conv{u_j}` in its affine span.
- Rows are in bijection with normalized tangent dependences.
- Row uniqueness is exactly the minimal-face criterion above.

Given a nonzero tangent dependence `b>=0`, define

```text
D(b) = sum_j b_j q_j
     = sum_j b_j (1-cos(theta_j))/sin(theta_j) > 0.
```

The exact row is

```text
a_j = 2 b_j / [sin(theta_j) D(b)].                       (2)
```

Indeed, tangent balance is inherited from `b`, while normal loss is
`2 D(b)/D(b)=2`. If rates proportional to this dependence are written
`a_j=c b_j/s_j`, the normal equation is `c D(b)=2`, so the common scale is
uniquely and positively fixed as `c=2/D(b)`.

For a normalized dependence `lambda`, set

```text
Q(lambda,theta)=sum_j lambda_j tan(theta_j/2).
```

Then equivalently

```text
a_j = 2 lambda_j / [sin(theta_j) Q(lambda,theta)].        (3)
```

Conversely, from any exact row set `b_j=a_j sin(theta_j)`. Equation (1) gives a
nonnegative tangent dependence; the normal equation prevents it from being
zero, and formula (2) reconstructs the row.

## Complete antipodal classification

Define

```text
C_N = {b>=0 : sum_{j in N} b_j u_j=0},
D(b)=sum_{j in N} b_j q_j,
```

with `D(0)=0` when `N` is empty.

If `P` is nonempty, every feasible row and only every feasible row is obtained
by choosing `b in C_N` with `D(b)<=2`, setting `a_j=b_j/s_j` for `j in N`, and
choosing antipodal rates satisfying

```text
sum_{p in P} a_p = 1-D(b)/2.                              (4)
```

If `P` is empty, feasibility is exactly `b in C_N`, `D(b)=2`, with
`a_j=b_j/s_j`. This follows by direct substitution in (1) and contains no
antipodal division.

Consequently:

| Candidates | Nonnegative feasibility | Positive on every permitted edge |
|---|---|---|
| `N=P=empty` | impossible | impossible |
| `N=empty`, `P` nonempty | always, antipodal total one | always, split total one positively |
| `N` nonempty, `P=empty` | iff `0 in conv(U)` | iff `0 in ri conv(U)` |
| both nonempty | always, using antipodes alone | iff `0 in ri conv(U)` |

If zero lies only on the relative boundary of the non-antipodal hull, mixed
nonnegative rows exist and may leave positive antipodal budget, but at least one
non-antipodal edge is zero. If zero lies outside, every non-antipodal rate is
zero and antipodes consume the full budget. More generally, a non-antipodal
positive support `S` is possible exactly when
`0 in ri conv{u_j:j in S}`; scaling controls how much of the normal budget is
left for antipodes.
