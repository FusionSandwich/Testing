# AFP publication program — value and convention registry

## 1. Repository values

| Name | Exact value | Meaning |
|---|---|---|
| accepted source branch | `agent/afp-pure-math-p0-m1` | live accepted pure-math target |
| accepted source commit | `c8505a70df01320d18a443bbf2ed1c11a761e5ce` | authoritative mathematical source |
| accepted source tree | `e55441e3645cfd58aa529b11ec17245723fcafcc` | authoritative source tree |
| historical P3 baseline | `c88b57533c3c8ad8fd819e4e52a74c4b5a245479` | historical prompt reference, not current authority |
| accepted P4-era target | `94aebf6578a43516cce4bb7c042fc57681c93890` | merge base for rich P3 final integration |
| rich P3 source | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | preserved source ancestor |
| reconciliation source | `19a5001158cb40fbb0adc92813cc3abd5dfa583d` | preserved source ancestor |
| verified divergent P3 line | `8de4b94835137d1eaf32c14b626424f87d2e176d` | independent, not target authority |
| verified divergent P4 line | `6bac46ce1a34ffba53f0003b876e57c4d747feaf` | independent, not target authority |
| transport archive | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | immutable non-pure-math boundary |
| new work line | `agent/afp-publication-program-baseline-c8505a70` | documentation and verification descendant |
| new immutable ref | `archive/afp-publication-program-baseline-c8505a70` | created only after green exact-head verification |

## 2. Generator and inner-product conventions

```text
w_i > 0
gamma_ij = gamma_ji >= 0
a_ij = gamma_ij / w_i
w_i a_ij = w_j a_ji = gamma_ij

(Lf)_i = sum_{j != i} a_ij (f_j-f_i)
r_i = sum_{j != i} a_ij
L_ii = -r_i

<f,g>_w = sum_i w_i f_i g_i
L Phi = -lambda Phi
```

No global normalization `sum_i w_i=1` is assumed unless explicitly introduced.

For the reversible near-rigidity Markov chain,

```text
mu_i = w_i r_i
pi_i = mu_i / sum_k mu_k
P_ij = p_ij = a_ij/r_i
c_ij = pi_i p_ij = pi_j p_ji.
```

The Dirichlet form is

```text
E_P(u) =
    (1/2) sum_i pi_i sum_j p_ij (u_i-u_j)^2.
```

Effective resistance is normalized by this same undirected conductance energy.

## 3. Carré-du-champ conventions

```text
jumpCrossVariation(f,g)_i =
    sum_j a_ij Delta_ij f Delta_ij g

Gamma(f,g)_i =
    (1/2) jumpCrossVariation(f,g)_i

carreDuChamp(f)_i =
    sum_j a_ij (Delta_ij f)^2
    = 2 Gamma(f,f)_i.
```

The product identity is

```text
L(fg)-f Lg-g Lf = 2 Gamma(f,g).
```

Any paper using `Gamma` must retain the factor `1/2`.

## 4. Spherical and quadratic values

For `Phi_i in S^(d-1)`:

```text
lambda_1 = d-1
degree-two target eigenvalue = 2d
L Phi = -(d-1) Phi
L(sampled degree-two mode) = -2d(sampled mode).
```

On `S^2`:

```text
L Omega = -2 Omega
degree-two target = -6.
```

Quadratic maps:

```text
(S_X A)_i = Phi_i^T A Phi_i
K_X = ker S_X
P_0(T) = T - tr(T) I/d
M_i = P_0(C_i+2 Phi_i Phi_i^T)
(R_X A)_i = <A,M_i>_F
R_X = (L+2d I) S_X.
```

## 5. Spherical rate–defect values

```text
ell_ij = 1-Omega_i dot Omega_j
epsilon_i = sum_j a_ij ell_ij^2
Q_i = r_i epsilon_i/4
p_ij = a_ij/r_i
x_ij = r_i ell_ij/2

sum_j a_ij ell_ij = 2
sum_j p_ij x_ij = 1
Q_i-1 = sum_j p_ij (x_ij-1)^2.
```

Near-rigidity definitions:

```text
delta = sqrt(eta/kappa) < 1
q_delta = (1+delta)/(1-delta)
s_delta = log(q_delta)
h_delta = -log(1-delta)
B_delta = h_delta + R_G s_delta
ell_ref = 2/r_o
Delta_theta =
    ell_ref(exp(B_delta)-1)/sigma_ref.
```

Accepted global estimates include:

```text
q_delta^(-dist(i,j)) <= r_i/r_j <= q_delta^(dist(i,j))
r_max/r_min <= q_delta^D
ell_max/ell_min <= q_delta^(D+1)

E_P(log r) <= 2 eta/(1-delta)^2

Var_pi(log r) <=
    2 eta/[(1-delta)^2 lambda_P]

|log r_i-log r_j| <=
    sqrt(2 eta R_eff(i,j))/(1-delta).
```

## 6. Exact five-Platonic table

| Graph | `K` | degree | `c` | `ell` | edge `a` | `r` | `epsilon` | `Q` | `rank S` | `rank R` | `dim E_form` | `dim K_X` | `dim E_sample` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tetrahedron | 4 | 3 | `-1/3` | `4/3` | `1/2` | `3/2` | `8/3` | 1 | 3 | 3 | 2 | 2 | 0 |
| octahedron | 6 | 4 | `0` | `1` | `1/2` | `2` | `2` | 1 | 2 | 2 | 3 | 3 | 0 |
| cube | 8 | 3 | `1/3` | `2/3` | `1` | `3` | `4/3` | 1 | 3 | 3 | 2 | 2 | 0 |
| icosahedron | 12 | 5 | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/10` | `(5+sqrt(5))/2` | `2-2/sqrt(5)` | 1 | 5 | 5 | 0 | 0 | 0 |
| dodecahedron | 20 | 3 | `sqrt(5)/3` | `1-sqrt(5)/3` | `(3+sqrt(5))/2` | `(9+3sqrt(5))/2` | `2-2sqrt(5)/3` | 1 | 5 | 5 | 0 | 0 | 0 |

The first three form dimensions are sampling aliases; all five genuine sampled exact dimensions are zero.

## 7. Restricted classification constants

Only under the full round minor-arc triangulation hypotheses:

| valence `q` | `V` | `E` | `F` | `cos theta` | `ell` | `r` |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 6 | 4 | `-1/3` | `4/3` | `3/2` |
| 4 | 6 | 12 | 8 | `0` | `1` | `2` |
| 5 | 12 | 30 | 20 | `1/sqrt(5)` | `1-1/sqrt(5)` | `(5+sqrt(5))/2` |

Conservative accepted computationally certified stability thresholds:

```text
q=3:
    eta_* = 3.90838234361e-6
    positive-width Gram floor ≈ 0.38189724544873466

q=4:
    eta_* = 2.07429596521497e-7
    positive-width Gram floor ≈ 0.3810797446765467

q=5:
    eta_* = 7.942143600537101e-10
    positive-width Gram floor ≈ 0.02172431128452759
```

These are sufficient thresholds, not claimed optimal constants.

## 8. Covariance-boundary values

At exact `Q=1` and `0<ell<2`:

```text
C_i =
    2(2-ell) T_i
    + 2 ell Omega_i Omega_i^T

M_i =
    3 ell(Omega_i Omega_i^T-I/3)
    + 2(2-ell)(T_i-P_i/2).
```

Axial covariance is equivalent to `T_i=P_i/2`.

At the antipodal boundary:

```text
ell = 2
r = 1
C = 4 Omega Omega^T
2(2-ell) = 0.
```

There is no canonical tangent unit direction.

For the positive weighted-octahedral family:

```text
w_1=g_12+g_13
w_2=g_12+g_23
w_3=g_13+g_23
r_i=2
ell_e=1
Q_i=1
```

and

```text
det(P+2I) =
6(g_12+g_13+g_23)
 (g_12 g_13+g_12 g_23+g_13 g_23)
/
[(g_12+g_13)(g_12+g_23)(g_13+g_23)] > 0.
```

Hence the genuine sampled degree-two exact space is `{0}` for every positive member.

## 9. Prompt 4 exact values

For every integer `N>=2`:

```text
0 <= r_polar(N)
     -[(8/pi^4)N^4
       +(10/(3pi^2))N^2
       +13/45]
  <= pi^2/(48N^2)

0 <= Q_pole(N)
     -[N^2/pi^2+7/12]
  <= pi^2/(12N^2).
```

On the fixed unreduced product graph:

```text
h = pi/(2N)
inward meridional rate = 1/(2 sin^2 h)
each azimuthal rate = 1/(4 sin^4 h)

r_pole =
    1/(2 sin^2 h)
    +1/(2 sin^4 h).
```

Extremal values:

```text
r_i >= 4/(C h^2)
E_K >= 4/(R K)
C* >= 4/R.
```

## 10. Exact computational and formal counts

```text
Plantri counts by V:
    4:1
    5:1
    6:2
    7:5
    8:14
    9:50
    10:233
    11:1249
    12:7595
    total:9150

near-rigidity path stress cases:
    174816

accepted full Lean build:
    3106 jobs

lean4export build:
    6 jobs

nanoda:
    21121 declarations
    0 errors

focused project axioms:
    propext
    Classical.choice
    Quot.sound
```

At the independent native-export boundary only:

```text
Lean.trustCompiler
Lean.ofReduceBool
```

are explicitly permitted bridge declarations. `sorryAx` is forbidden.

## 11. Authoritative accepted artifacts

| Workflow | Run | Job | Artifact ID | Artifact name | SHA-256 |
|---|---:|---:|---:|---|---|
| AFP global rigidity | `30787796465` | `91604757325` | `8845980973` | `afp-global-rigidity-30787796465` | `6ac15f3a25ae850360299654fd819fb176b1fadc7a1c6f65b302992a0af70c6d` |
| AFP Prompt 3 rigidity | `30787796476` | `91604757297` | `8846031784` | `afp-prompt3-rigidity-30787796476` | `3f60f3ec5051e16dec23d77b5c693e3395bd507d026a5721741e5be1f4d57c9c` |
| AFP Prompt 4 sharp barriers | `30787796470` | `91604757188` | `8846032007` | `afp-prompt4-sharp-barriers-30787796470` | `77842799da18e8c40f40d157f55d7d6d64ae7f7fa9b3fe52e9fbd88e3bbe000e` |
| AFP Pure Mathematics | `30787796462` | `91604757087` | `8846104954` | `afp-pure-mathematics-30787796462` | `dd8080263e5ea73cd5379aa955b566fe9e3e716aa6b009efb52741d01a7415e5` |
| AFP quadratic covariance | `30787796482` | `91604757171` | `8845986588` | `afp-quadratic-covariance-30787796482` | `dd0d512872a194d211ba8a20d3a5f8bb8e36870f89de5c37bff86f442c986768` |
| AFP spherical feasibility | `30787796469` | `91604757060` | `8845966495` | `afp-spherical-feasibility-30787796469` | `bd116f9a75ad95d0115192eefdf819947aae974ea2e00f609e0b9e87ea3a8e55` |

The new publication-baseline exact-head artifact is recorded in the PR discussion after its run completes.
