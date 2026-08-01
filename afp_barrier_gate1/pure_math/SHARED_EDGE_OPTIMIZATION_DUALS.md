# Shared-edge optimization duals

Use the matrix, target, and edge strain from `SHARED_EDGE_CONE_FARKAS.md`:

```text
A gamma=b, gamma>=0,
sigma_e(y)=(A^T y)_e.
```

## Linear rate or defect objective

For finite edge costs `c_e`, the primal and its actual transpose dual are

```text
(P_c) min c·gamma  subject to A gamma=b, gamma>=0,
(D_c) max b·y      subject to sigma_e(y)<=c_e for every e.    (1)
```

If the primal is feasible and has finite value—for example, if `c_e>=0`—the
finite LP strong-duality theorem gives attainment and

```text
min(P_c)=max(D_c).                                           (2)
```

The project sign convention is checked directly by weak duality:

```text
b·y=(A gamma)·y=sum_e gamma_e sigma_e(y)
    <=sum_e gamma_e c_e.
```

At optimality the zero gap decomposes as

```text
gamma_e[c_e-sigma_e(y)]=0 for every edge.                   (3)
```

Every positive shared edge therefore saturates its geometric strain price; an
inactive edge may have strict dual slack. The exact finite gap identity and
componentwise complementary slackness are formalized in
`AFPBarrier/DualComplementarity.lean`.

Two direct objectives are

```text
total conductance: c_e=1;
total outgoing rate: c_{pq}=1/w_p+1/w_q,
```

because each undirected conductance contributes `gamma_e/w_i` at both
endpoints. Any fixed edgewise defect surrogate linear in conductance is handled
by taking its coefficient as `c_e`.

## Peak outgoing-rate minimization

Let

```text
r_i(gamma)=(1/w_i) sum_{e incident to i} gamma_e.
```

The LP minimizing `t` subject to exactness, nonnegative conductances, and
`r_i(gamma)<=t` has dual

```text
maximize b·y
subject to mu_i>=0, sum_i mu_i=1,
sigma_{pq}(y)<=mu_p/w_p+mu_q/w_q.                            (4)
```

This follows by assigning multipliers `mu_i>=0` to
`r_i(gamma)-t<=0`; minimizing the Lagrangian over free `t` gives
`sum_i mu_i=1`, while minimizing over `gamma>=0` gives the displayed edge
inequality. Strong duality holds whenever the exact system is feasible.
Complementary slackness is

```text
mu_i[t-r_i(gamma)]=0,
gamma_{pq}[mu_p/w_p+mu_q/w_q-sigma_{pq}(y)]=0.               (5)
```

The vector `mu` is a unit distribution of marginal price over nodes and is
supported only on rows attaining the peak rate. Every positive edge saturates
the sum of its two endpoint prices.

## Weighted l1 residual or defect relaxation

Let `r` index node-coordinate equations and let `tau_r>0`. The always-feasible
residual LP is

```text
minimize c·gamma+sum_r tau_r(p_r+n_r)
subject to A gamma-p+n=b,
gamma,p,n>=0.                                                (6)
```

Its exact dual is

```text
maximize b·y
subject to A^T y<=c,
           -tau_r<=y_r<=tau_r.                               (7)
```

For `c>=0`, both optima are attained and equal. Complementary slackness is

```text
gamma_e[c_e-sigma_e(y)]=0,
p_r(tau_r+y_r)=0,
n_r(tau_r-y_r)=0.                                           (8)
```

Since `A gamma-b=p-n`, a positive residual forces `y_r=-tau_r`; a negative
residual forces `y_r=+tau_r`. A zero residual may have unsaturated dual load.
For pure residual minimization take `c=0`. Its optimum is zero exactly when the
exact system is feasible. If the optimum is positive, negating an optimal
`y` gives a bounded quantitative Farkas certificate with the sign used in the
cone theorem.

These three blocks transfer finite strong LP duality and every
complementary-slackness condition to the actual spherical matrix. The ordinary
proof invokes the standard finite theorem after verifying finite dimensions,
primal and dual forms, feasibility/boundedness, and signs; the repository
formalizes the spherical transpose and all zero-gap consequences.
