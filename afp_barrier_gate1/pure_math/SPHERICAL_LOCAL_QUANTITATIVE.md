# Quantitative local cone margin and robustness

Use the notation and exact row formula from `SPHERICAL_LOCAL_EXACT.md`. Let
`C_i=conv{u_j}` and assume first that `0 in C_i`. Then
`L=aff C_i` is a linear subspace. Define the relative cone-surrounding margin

```text
rho_i = max {r>=0 : r B_L is contained in C_i}
      = dist_L(0, relbd C_i).                                (5)
```

When `0` is outside the hull set `rho_i=0`. For `dim L>=1`, support-function
duality gives

```text
rho_i = min_{v in L, ||v||=1} max_j <v,u_j>.                  (6)
```

Indeed, `r B_L subset C_i` iff `r<=h_C(v)` for every unit `v`; finite
compactness attains the extrema. Hence

```text
rho_i>0  iff  0 in ri C_i.                                   (7)
```

For a one-dimensional hull, this is a relative line-segment inradius. Ambient
perturbation statements below require either full two-dimensional tangent span
or perturbations preserving the identified relative span.

## Controlled all-index dependence

Let `m` be the number of indexed candidates and assume `||u_j||=1` and
`rho_i>0`. There is a normalized tangent dependence satisfying

```text
lambda_j >= delta_i := rho_i/[m(1+rho_i)] >= rho_i/(2m).      (8)
```

For each index `k`, `-rho_i u_k` lies in the hull, so the representation

```text
0 = [rho_i/(1+rho_i)]u_k + [1/(1+rho_i)](-rho_i u_k)
```

puts at least `rho_i/(1+rho_i)` on index `k`. Averaging over all indices proves
(8). The last inequality uses `rho_i<=1`, because the hull lies in the unit
ball.

## Rate and outgoing-rate bounds

Assume

```text
0 < theta_- <= theta_j <= theta_+ <= pi/2,
ell_- = 1-cos(theta_-),  ell_+ = 1-cos(theta_+).
```

Every nonnegative exact row, without any cone-margin hypothesis, obeys

```text
2/ell_+ <= R_i:=sum_j a_j <= 2/ell_-.                         (9)
```

This is exactly
`ell_- R_i <= sum a_j ell_j = 2 <= ell_+ R_i`.
For the margin-selected row from (8), formula (3) of the exact proof gives

```text
2 delta_i/ell_+ <= a_j
 <= 2[1-(m-1)delta_i]/ell_- <= 2/ell_-.                       (10)
```

The lower bound uses
`sin(theta_j) Q <= sin(theta_+)tan(theta_+/2)=ell_+`; the upper bound uses the
corresponding lower denominator and
`lambda_j<=1-(m-1)delta_i`. Thus only the outgoing window follows without a
margin; a positive coefficientwise lower bound requires `rho_i>0`.

Under

```text
c1 h <= theta_j <= c2 h,
0<h<=h0,  theta0:=c2 h0<=pi/2,
kappa0:=2 sin(theta0/2)/theta0,
```

one has for `0<=theta<=theta0`

```text
(kappa0^2/2) theta^2 <= 1-cos(theta) <= theta^2/2.             (11)
```

Therefore the explicit inverse-quadratic bounds are

```text
4/(c2^2 h^2) <= R_i <= 4/(kappa0^2 c1^2 h^2),                (12)
4 delta_i/(c2^2 h^2) <= a_j
 <= 4[1-(m-1)delta_i]/(kappa0^2 c1^2 h^2).                   (13)
```

## Conditioning

Let `U:R^m -> L`, `Ux=sum_j x_j u_j`. Formula (6), applied to both signs of a
unit vector, implies

```text
||U^T v||_2 >= rho_i ||v||_2,
rho_i^2 I_L <= U U^T <= m I_L,
cond_2(U U^T) <= m/rho_i^2.                                  (14)
```

For the transformed full balance matrix with columns
`C_j=(u_j,q_j)`, assume `0<q_-<=q_j<=q_+`. If
`y=C^T(v,t)`, pairing with a normalized tangent dependence gives
`|t|<=||y||_2/q_-`; then (14) gives

```text
||v||_2 <= [1+sqrt(m)q_+/q_-] ||y||_2/rho_i.
```

Consequently

```text
sigma_min(C^T) >= 1/K_C,
K_C = sqrt( ([1+sqrt(m)q_+/q_-]/rho_i)^2 + 1/q_-^2 ).         (15)
```

The original columns are
`B_j=(s_j u_j,ell_j)=s_j(u_j,q_j)`, so

```text
sigma_min(B^T) >= s_-/K_C,
cond_2(B) <= sqrt(m)sqrt(s_+^2+ell_+^2) K_C/s_-.              (16)
```

In the `h` window, define

```text
sigma0=sin(theta0)/theta0,
beta0=tan(theta0/2)/theta0.
```

Then `s_- >= sigma0 c1 h`, `q_- >= c1 h/2`,
`q_+ <= beta0 c2 h`, and one explicit admissible value is

```text
K_C(h) <= sqrt(
 ([1+2 beta0 sqrt(m)c2/c1]/rho_i)^2 + 4/(c1^2 h^2)).          (17)
```

Equations (16)-(17) give a fully numerical condition bound.

## Perturbation of directions and angles

Identify old and new tangent planes by an orthogonal map and assume

```text
max_j ||u'_j-u_j|| <= epsilon_u.                              (18)
```

Support functions are one-Lipschitz under this indexed perturbation, hence

```text
rho'_i >= rho_i-epsilon_u.                                    (19)
```

Thus `epsilon_u<rho_i` preserves strict feasibility under the span hypotheses
above. A boundary configuration `rho_i=0` has no positive uniform ambient
radius; the rational regression crosses that boundary exactly.

For explicit coefficients, start with (8), put

```text
K0 = sqrt(1+[2(1+sqrt(m))/rho_i]^2),
```

and assume

```text
epsilon_u <= min{rho_i/2, delta_i/(2K0)}.                     (20)
```

The perturbed augmented barycentric matrix has a right inverse of norm at most
`K0`. Correcting the residual `sum lambda_j u'_j`, whose norm is at most
`epsilon_u`, gives an exact dependence `lambda'` with

```text
min_j lambda'_j >= delta_i/2,
||lambda'-lambda||_1 <= sqrt(m) K0 epsilon_u.                 (21)
```

The right-inverse estimate follows by writing
`y_j=<v,u'_j>+t`, using a positive perturbed dependence to bound
`|t|<=||y||_2`, and then using `rho'_i>=rho_i/2` to bound `v`.

Suppose old and new angles lie in a common
`[theta_-,theta_+] subset (0,pi/2]`, with maximum change
`epsilon_theta`. Define

```text
s0=sin(theta_-), s1=sin(theta_+),
q0=tan(theta_-/2), q1=tan(theta_+/2),
Lq=1/[2 cos^2(theta_+/2)],
Llambda=2/(s0 q0)+2 s1 q1/(s0^2 q0^2),
Ltheta=2(q1+s1 Lq)/(s0^2 q0^2).
```

For rows formed by the exact formula,

```text
||a'-a||_1 <= Llambda ||lambda'-lambda||_1
              + Ltheta epsilon_theta.                         (22)
```

This follows from
`|Q'-Q|<=q1 Delta_lambda+Lq epsilon_theta`, the denominator lower bound
`s0 q0`, and

```text
|s'_j Q'-s_j Q|
 <= s1 q1 Delta_lambda+(q1+s1 Lq)epsilon_theta.
```

Therefore a fixed linear row objective satisfies

```text
|c·a'-c·a| <= ||c||_infinity
 [Llambda sqrt(m)K0 epsilon_u+Ltheta epsilon_theta].           (23)
```

An arbitrary optimizer may have zero coefficients. To obtain an optimal-value
bound without hiding this fact, mix an old optimizer `lambda*` with the margin
row `lambda0` using

```text
t=2K0 epsilon_u/delta_i <=1,
bar_lambda=(1-t)lambda*+t lambda0.
```

Then correct `bar_lambda` by the right inverse. Since
`||bar_lambda-lambda*||_1<=2t`, the one-sided degradation is

```text
v'-v <= ||c||_infinity [
 Llambda sqrt(m)K0 epsilon_u + Ltheta epsilon_theta
 + 4 Llambda K0 epsilon_u/delta_i ].                           (24)
```

A cost perturbation adds its sup norm times the outgoing-rate bound (9).
Applying the construction in reverse gives a two-sided bound when both problems
retain the stated margin and angular window. If an optimizer already has known
coefficient slack, the mixing term is unnecessary.

Angle perturbations alone do not alter the convex-hull criterion. They preserve
feasibility while every angle remains in `(0,pi)`; a safe radius is
`epsilon_theta < min_j{theta_j,pi-theta_j}`. In the `h` window, a perturbation
at most `eta h`, with `eta<c1`, replaces `c1,c2` by `c1-eta,c2+eta` in the
explicit constants.
