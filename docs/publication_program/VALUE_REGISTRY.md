# Publication value registry

Normalization version `AFP-SPHERE-v1` means `sum w=1`, symmetric conductance
`gamma`, negative-semidefinite generator `L`, and coordinate target `d-1`.
Accepted-source rows are from `6bac46ce1a34ffba53f0003b876e57c4d747feaf`.
Rows labeled future are definitions from the publication-program specification,
not claims that a corresponding source blob or theorem already exists.

| ID | Exact definition / domain | Representation and recomputation | Consumer |
|---|---|---|---|
| W | `w_i>0`, `sum_i w_i=1` | exact rational/algebraic; normalization audit | all |
| G | `gamma_ij=gamma_ji>=0`, `a_ij=gamma_ij/w_i` | conductance and directed-rate matrices; reversibility residual `||WL-L^TW||` | I/II/III |
| L | `(Lf)_i=sum_j a_ij(f_j-f_i)` | zero rows, nonnegative off-diagonal, negative semidefinite in `l2(w)` | all |
| EV-l | `lambda_l=l(l+d-2)` | target eigenvalue; group sampled spaces by equal value | I/III |
| LOSS | `ell_ij=1-Omega_i.Omega_j`; `r_i=sum a_ij`; `epsilon_i=sum a_ij ell_ij^2` | exact algebraic where possible | I/II |
| Q | `Q_i=r_i epsilon_i/(d-1)^2` | dimensionless; `r epsilon/4` only at d=3 | I |
| COV | `C_i=sum a_ij (Omega_j-Omega_i)(...)^T` | exact matrix; radial/anisotropic split | I |
| S2 | `S_X(A)_i=Omega_i^T A Omega_i`, `A in Sym_0(d)` | rational/algebraic basis, exact rank and kernel | I/III |
| KX | `K_X=ker S_X` | exact nullspace; quotient boundary | I/III |
| MBZ | `M_i=P_0(C_i+2 Omega_i Omega_i^T)`, `Z_i=Omega_i Omega_i^T-I/d`, `B_i=M_i-d epsilon_i Z_i/(d-1)` | accepted exact covariance decomposition | I |
| R2 | `(L+2d I)S_X` | exact residual matrix | I/II |
| D2 | `sup_(A notin K_X) ||R2 A||_w/||S_X A||_w` | P1A-proved quotient norm; `S_2` is automatically nonzero for unit nodes and `d>=2`; compute only after deflating `K_X`, never divide by `||A||_F` | I/II |
| GS | `G_S=S_2^*S_2=sum_i w_i Z_i tensor Z_i` | weighted row Gram; `tr G_S=(d-1)/d`; coordinate operator matrix is `F^-1 S^TWS` in basis Gram `F` | I/II |
| GR | `G_R=R_2^*R_2=sum_i w_i M_i tensor M_i=S_2^*(L+2dI)^2S_2` | `tr G_R=d sum_iw_i epsilon_i^2/(d-1)+sum_iw_i||B_i||^2`; last equality uses reversibility | I/II |
| P1B | `E_epsilon=sum_iw_i epsilon_i^2`, `E_B=sum_iw_i||B_i||_F^2`; `D_2^2>=d^2 E_epsilon/(d-1)^2+d E_B/(d-1)` and `D_2 r_max>=d(d-1)` | exact quotient trace theorem; equality iff constant row rate, zero loss variance and zero `B_i` | I |
| DEF | equality/stability deficits from loss variance, covariance anisotropy, path propagation and rigidity margin | exact constants in P3/P4 packages | I |
| LIFT | linear moment/reversibility constraints with `gamma>=0` and nonempty balanced probability polytope | affine slice at fixed target; projective family only after scale quotient | III |
| NEG | total negative conductance and its dual certificate | FUTURE program value; future exact LP/conic certificate | III |
| DESIGN | fixed-quadrature shared-conductance programs on `A gamma=b`, `gamma>=0`, with exact shellwise quotient residuals and rate/locality constraints | P2A-proved SDP/SOCP/QP/LP value with explicit primal/dual certificate | II |
| P2A-A | edge-force matrix with blocks `Omega_j-Omega_i` and `Omega_i-Omega_j`; `b_i=-2w_iOmega_i` | `A gamma=b` iff `L_gamma Omega=-2Omega` | II |
| P2A-C | unsigned incidence `C=abs(B)` | node rate `r_i=(C gamma)_i/w_i`; cap `C gamma<=Rw` | II |
| P2A-TL | for certified shell basis `V_l^T W V_l=I`, `T_l=W^(1/2)(L_gamma+l(l+1)I)V_l` | affine full-output quotient residual; `D_l=||T_l||_2` | II |
| P2A-LOSS-L1 | `sum_e (1-Omega_i.Omega_j)gamma_e` | exactly `1` under `sum w=1` and exact `H_1`; not a sparsity objective | II/III |
| P2A-TOTAL | `sum_e gamma_e=(1/2)sum_iw_ir_i` | mean-rate cost, generally variable and potentially long-edge favoring | II/III |
| P2A-LOWER | fixed-rate/fixed-defect optimizer bound on `S^2` | `opt_D(R)>=6/R`; `opt_R(delta)>=6/delta` | I/II |
| P2A-TETRA | regular tetrahedron, `w=1/4`, `gamma=1/8` | rank `S_2=3`, `rmax=3/2`, `D_2=4`, Frobenius half-square `24` | I/II |
| P2A-OCTA | regular octahedron, nonantipodal graph, `w=1/6`, `gamma=1/12` | rank `S_2=2`, `rmax=2`, `D_2=3` | I/II |
| SEMI | $k_{t,\lambda}=(1-e^{-\lambda t})/\lambda$ and $c_{\alpha,\lambda}=1/[\alpha(\alpha+\lambda)]$ | P2B-proved sharp full conservative-space residual-to-transient/resolvent constants; replace zero spectral value by a declared gap for the refined constant | II |
| P2B-BAND | row block $[W^{1/2}K_\ell(t)W^{-1/2}T_\ell]_\ell$ and $\beta_{\mathcal B}=\lambda_{\min}(V_{\mathcal B}^*WV_{\mathcal B})$ | exact cross-shell propagated-residual norm; total-sample transfer only when $\beta_{\mathcal B}>0$ or the sampling kernel is eigenvalue-map invariant | I/II |
| P2B-STAB | $K_B(t,s)=\exp(-\int_s^t\beta)$; $C_{\rm st}=1/\beta_B$ under onto positive coercivity or $1/\mu$ under onto inf-sup | explicit transport stability factors in the physical norm | II |
| P2B-R1--R6 | physical BFP, angular generator, sampling/quadrature, spatial, energy/slowing-down, iteration/time-reconstruction residuals | exact P2B common-space closure $e_t+A_Be=\sum_{j=1}^6R_j$ | II |
| P2B-BLOCK | $\beta_M=\lambda_{\min}(\operatorname{diag}(\beta_g)-(C+C^T)/2)$, $c_{gg'}=\sqrt{\eta_g/\eta_{g'}}\|K_{gg'}\|$ | multigroup coercivity certificate when positive; its transient kernel additionally requires the stated evolution-family generation hypothesis, and its inverse bound requires surjectivity | II |
| P2B-ANG-SHARP | two equatorial samples, $W=I/2$, $L=3[[-1,1],[1,-1]]$, target $\lambda=6$ | one sampled quadratic exact, one kernel-aligned; transient and shifted-resolvent effectivity exactly $1$ | II |
| P2B-SPATIAL | two cells by two directions, $a=1,b=2,\sigma=1$, $\psi_*=(1,2,3,4)$ | $f=(0,2,3,10)$, $\psi_h=(7/9,7/3,8/3,38/9)$, $e=(2/9,-1/3,1/3,-2/9)$; theorem residual $r_*=(14/9)(1,-1,1,-1)$, bound $56/27$, energy effectivity $28\sqrt{26}/39$, and exact $A_*^{-*}$ adjoint effectivity $1$.  The reverse comparator $r_h=(1,-1,1,-1)$ is retained only for the $A_h$ preconditioner regression. | II |
| P2C-GRAM | `G_l=V_l(X)^T W V_l(X)` and `F_l=((L_gamma+lambda_l I)V_l)^T W((L_gamma+lambda_l I)V_l)` | raw moving-kernel epigraph `F_l <= delta_l^2 G_l`, exactly equivalent to the full sampled quotient including `ker G_l` | II |
| P2C-PROTECT | compact protected stratum with positive mass floor, sampling-rank gap, rate/locality bounds, response bounds and certified feasible-correspondence regularity | domain of the scoped outer existence and stationary-subsequence theorems; every margin is an input/certificate, not an inferred generic property | II |
| P2C-LOCAL-MARGIN | local barycentric/tangent distance normalized by the local feature scale; global margin from the shared-stress feasibility/conic certificate | reported separately; a positive local margin never substitutes for the global shared-conductance test | II/III |
| P2C-ROT | collision-fixed response spread, common-rotation covariance residual, streaming-ray spread and interpolation defect | four separately labelled values; continuum rotation extrema require net radius `rho` and Lipschitz remainder `L rho` | II |
| P2C-RATE | accepted `S^2` P1E witness under `r_max<=64 pi^2 h^-2` | every-level inner optimum satisfies `3 h^2/(32 pi^2) <= D2_opt <= 75 h^2/2` | I/II |
| P2C-AB | 60 proper icosahedral rotations applied to declared orbit representatives; each positive orbit mass is divided by its stabilizer-reduced orbit size | generic admission adapter verifies duplicates, total mass, positivity and advertised harmonic residual; built-in vertex fixture is a regression rather than a published AB rule | II |
| P2C-RELEASE | historical archive `archive/afp-publication-p2c-codesign-verified` at `b34c29b1b04f5293eaa4007b39d189efa03c51f5`; completion archive name `archive/afp-publication-p2c-completion-verified` | old ref remains immutable; completion ref is create-only under an absent-ref lease and must equal the exact validated candidate SHA | II |
| TRAN | response error split into six named P2B channels with stability and adjoint weights | PROVED error-certificate value; an equal-cost physical improvement benchmark remains a later validation claim | II |
| HTS | layer/tensor angular response values | FUTURE layer-resolved physical data; not pure-math evidence | II |

## Immutable exact regression dataset: five Platonic examples

All use equal `w=1/N`, shortest-edge support, `L Omega=-2 Omega`, and have
`Q=1`.  `alpha` is the adjacent dot product and `gamma=w a`.

| Example | N | q | alpha | ell | a | r | epsilon | gamma | rank S/R | dim E_form / dim K_X / dim E_sample |
|---|---:|---:|---|---|---|---|---|---|---|---|
| tetrahedron | 4 | 3 | `-1/3` | `4/3` | `1/2` | `3/2` | `8/3` | `1/8` | 3/3 | 2/2/0 |
| octahedron | 6 | 4 | `0` | `1` | `1/2` | `2` | `2` | `1/12` | 2/2 | 3/3/0 |
| cube | 8 | 3 | `1/3` | `2/3` | `1` | `3` | `4/3` | `1/8` | 3/3 | 2/2/0 |
| icosahedron | 12 | 5 | `sqrt(5)/5` | `1-sqrt(5)/5` | `(5+sqrt(5))/10` | `(5+sqrt(5))/2` | `2-2sqrt(5)/5` | `(5+sqrt(5))/120` | 5/5 | 0/0/0 |
| dodecahedron | 20 | 3 | `sqrt(5)/3` | `1-sqrt(5)/3` | `(3+sqrt(5))/2` | `(9+3sqrt(5))/2` | `2-2sqrt(5)/3` | `(3+sqrt(5))/40` | 5/5 | 0/0/0 |

Recompute with:

```text
cd afp_barrier_gate1
python pure_math/covariance/exact_quadratic_covariance_audit.py
python pure_math/covariance/p1a_quadratic_fidelity_audit.py
```

Arithmetic uses exact real algebraic expressions, including rational and
certified radical values; no tolerance is used.
The baseline output also fixes `L|imS` as `-2`, `-3`, `-4`,
`-3-3sqrt(5)/5`, and `-3-sqrt(5)` respectively.

## P1B sharp-defect values

```text
strong coefficient on sum_i w_i epsilon_i^2:
    d^2/(d-1)^2

strong coefficient on sum_i w_i ||B_i||_F^2:
    d/(d-1)

universal product constant:
    d(d-1)

S^2 product constant:
    6

final equality scalar:
    c_* = d(d-1)/r_max
    R_2 = c_* S_2
```

The regular simplex, cross-polytope and hypercube are all-dimensional equality
families.  In `d=3`, all five displayed Platonic shortest-edge generators have
`D_2 r_max=6`, including the tetrahedral, octahedral and cubical alias cases.
The P1B deterministic audit contains 24 exact fixtures.

## Frozen exact constants and counts

| Value | Exact value | Source / command |
|---|---|---|
| Plantri counts through 12 vertices | `1,1,2,5,14,50,233,1249,7595`; total `9150` | `triangulation_counterexample_audit.py --require-plantri` with source pin |
| opposite-ray anisotropy | `kappa(ell1-ell2)^2/(kappa ell1+ell2)^2` | P4 theorem/audit |
| P4 Lean declarations built | `3111 jobs` | run `30780693332` |
| allowed focused axioms | `propext`, `Classical.choice`, `Quot.sound` | `PureMathAxiomAudit.lean` |
| exact inventory line count/digest | `121`; `090365d15dab7053643cae6c7adf6ee1aae95d5c2a3eadcf97bd207fd4c542cb` | `git ls-tree` command in `PROGRAM_BASELINE.md` |

Future numerical entries must add units, tolerance, number field, proof or data
source, recomputation command, consumer, and the exact baseline blob.  A fitted
slope is never recorded as an all-orders rate theorem.

## P1C equality-geometry values

| ID | Exact definition / domain | Representation and recomputation | Consumer |
|---|---|---|---|
| TAN | `P_i=I-Omega_iOmega_i^T`, `tau_ij=P_iOmega_j`, `Omega_j-Omega_i=-ell_ijOmega_i+tau_ij` | exact radial/tangent decomposition; `||tau_ij||^2=ell_ij(2-ell_ij)` | I/III |
| MIX-TAN | `h_i=sum_j a_ij ell_ij tau_ij`, `T_i=sum_j a_ij tau_ij tau_ij^T` | `||B_i||_F^2=2||h_i||^2+||T_i-(2-epsilon_i/(d-1))P_i||_F^2` | I |
| TIGHT | for zero loss variance and `0<ell<2`, `p_ij=a_ij/r_i`, `y_ij=tau_ij/sqrt(ell(2-ell))` | `sum p y=0`, `sum p yy^T=P_i/(d-1)`; do not use at `ell=2` | I/III |
| E2 | `e_2=dim(im S_2 intersect ker(L+2dI))=rank S_2-rank R_2` | every complete frontier-equality generator has `ker R_2=ker S_2`, hence `e_2=0`, without requiring `K_X=0` | I |

### All-dimensional exact equality constants

| family | `w_i`; active `gamma_ij`; active `a_ij` | `r_i`; `ell_ij`; `epsilon_i` | `C_i`; `M_i`; `B_i` | `rank S_2`; `dim K_X`; `e_2` | `mathfrak D_2`; product |
|---|---|---|---|---|---|
| simplex | `1/(d+1)`; `(d-1)/(d+1)^2`; `(d-1)/(d+1)` | `d(d-1)/(d+1)`; `(d+1)/d`; `(d^2-1)/d` | `(d-1)I/d+(d-1)Omega_iOmega_i^T`; `(d+1)Z_i`; `0` | `d`; `(d+1)(d-2)/2`; `0` | `d+1`; `d(d-1)` |
| cross-polytope | `1/(2d)`; `1/(4d)`; `1/2` | `d-1`; `1`; `d-1` | `I+(d-2)Omega_iOmega_i^T`; `dZ_i`; `0` | `d-1`; `d(d-1)/2`; `0` | `d`; `d(d-1)` |
| hypercube | `2^-d`; `(d-1)/2^(d+1)`; `(d-1)/2` | `d(d-1)/2`; `2/d`; `2(d-1)/d` | `2(d-1)I/d`; `2Z_i`; `0` | `binom(d,2)`; `d-1`; `0` | `2`; `d(d-1)` |

The simplex kernel is the zero-diagonal, row-sum-zero symmetric extended
matrix space; the cross-polytope kernel is the trace-free zero-diagonal
off-diagonal form space; the hypercube kernel is the diagonal trace-free
form space.

### Exact Platonic equality additions

For uniform shortest-edge generators,
`C_i=(1+alpha)I+(1-3alpha)Omega_iOmega_i^T`,
`M_i=3(1-alpha)Z_i`, `B_i=0`, `e_2=0` and
`mathfrak D_2 r_i=6`.

| graph | `C_i` | `M_i` | `K_X` | `mathfrak D_2` | certified sampling minor |
|---|---|---|---|---|---|
| tetrahedron | `2I/3+2Omega_iOmega_i^T` | `4Z_i` | diagonal trace-free aliases, dimension `2` | `4` | `-4/27` (`3x3`) |
| octahedron | `I+Omega_iOmega_i^T` | `3Z_i` | off-diagonal aliases, dimension `3` | `3` | `-2` (`2x2`) |
| cube | `4I/3` | `2Z_i` | diagonal trace-free aliases, dimension `2` | `2` | `4/27` (`3x3`) |
| icosahedron | `(1+sqrt(5)/5)I+(1-3sqrt(5)/5)Omega_iOmega_i^T` | `(3-3sqrt(5)/5)Z_i` | `0` | `3-3sqrt(5)/5` | `-16sqrt(5)/125` (`5x5`) |
| dodecahedron | `(1+sqrt(5)/3)I+(1-sqrt(5))Omega_iOmega_i^T` | `(3-sqrt(5))Z_i` | `0` | `3-sqrt(5)` | `16/81` (`5x5`) |

Recompute with
`python pure_math/covariance/p1c_equality_geometry_audit.py`.

## P1D quantitative-stability values

Let `n=d-1`, `a_0=n^2/r_max`, `ell_0=n/r_max`,
`c_0=dn/r_max`, and `eta=2delta+delta^2`.

| ID | Exact definition / domain | Sharp or proved bound | Consumer |
|---|---|---|---|
| P1D-QSV | `s_i=r_max/r_i-1`, `v_i=V_i/a_0`, `q_i=x_i-1=s_i+v_i` | `sum w(2q+q^2)+n E_B/(d a_0^2)<=eta` | I |
| P1D-H | `H=eta-n E_B/(d a_0^2)` | `0<=H<=eta`; retains scalar/tensor competition | I |
| P1D-GLOBAL | normalized scalar, rate, variance, tensor defects | `sum w q^2,sum w s^2,sum w v^2<=eta`; `E_B<=d a_0^2 eta/n=d n^3 eta/r_max^2` | I |
| P1D-V | local loss variance | `sum w V<=a_0 delta`; `sum w V^2<=a_0^2 eta` | I |
| P1D-POINT | positive vertex mass `w_i` | `q_i<=sqrt(1+H/w_i)-1`; the joint local budget gives `||B_i||<=a_0 sqrt(d eta/(n w_i))` | I |
| P1D-BAD | threshold `rho>0` | weighted bad-vertex mass `<=min(1,H/[rho(2+rho)])` | I |
| P1D-K0 | covariance/residual Hilbert--Schmidt allowance | `K_0=d a_0^2 eta/n=d(d-1)^3 eta/r_max^2` | I/II |
| P1D-EDGE | `nu_ij=gamma_ij/bar r`, relative global loss `g=ell/ell_0-1` | `E_nu g^2<=sqrt(1+H)H/2`; tail `<=sqrt(1+H)H/(2t^2)` | I/II |
| P1D-KAPPA | every active `p_ij>=kappa` | local edge relative defect `<=sqrt(v_i/(kappa(1+s_i)))`; all uniform versions display `kappa,w_min` | I/II |
| P1D-GAP | sampled lower-frame `alpha_X>0` on `K_X^perp` | `||U-c_0 iota||<=rho_X=sqrt(K_0/alpha_X)`; compressed shell width `2rho_X` | I/II |
| P1D-FRAME | raw tangent lower bound `lambda`, target `theta=m(2-m)/n` | Procrustes square `<= (||B||^2+V^2/n)/[r^2(sqrt(lambda)+sqrt(theta))^2]` | I/III |
| P1D-UNIT | shell floor `s_-`, feature gap `mu`, probability floor `kappa` | weight correction `<=R_*/mu`; positivity if `R_*<kappa mu`; geometric metric given in theorem (10.17) | I/III |

The P1D exact/interval audit contains 30 fixtures: five master-budget, three
small-mass, two aliases, four `kappa` compass, three path, four singular-frame,
four sampling-gap, and five outward-interval fixtures. These counts and
constants are regression values, not replacements for the all-orders proof.

## P1E matching-construction values

| ID | Exact definition / domain | Proved value or bound | Consumer |
|---|---|---|---|
| P1E-D2-H | regular `N`-gon, `N>=5`, fill/separation `h=pi/N` | active edge angle `2h`; loss `ell=1-cos(2h)=2sin^2h` | I |
| P1E-D2-RATE | same family | `r_max=ell^-1 <= (pi^2/8)h^-2` | I |
| P1E-D2-DEFECT | sampled degree-two quotient | `mathfrak D_2=2ell=4sin^2h<=4h^2`; product exactly `2` | I |
| P1E-D2-ORDER | class with rate cap `R_2=pi^2/8` | `16h^2/pi^2 <= inf mathfrak D_2 <= 4h^2` | I |
| P1E-D3-MESH | adaptive reflected ring family on `S^2`; `h=pi/(2S)` | bounded degree and angular window; every active chord at least `h/8` | I |
| P1E-D3-RATE | same family | `R_3=64pi^2`; `r_max<=R_3h^-2` | I |
| P1E-D3-DEFECT | exact row multiplier on the sampled quotient | `C_3=75/2`; `mathfrak D_2<=C_3h^2` | I |
| P1E-D3-LOWER | P1B product bound under the `R_3` cap | `c_3=6/R_3=3/(32pi^2)` | I |
| P1E-D3-ORDER | admissible class `mathcal G_h(R_3)` containing the ring generator | `c_3h^2 <= inf mathfrak D_2 <= C_3h^2` | I |

The `d=3` perturbation constants apply only to support-preserving reflected
latitude perturbations with fixed combinatorial data. No exact-head workflow
execution, artifact digest, or frozen P1E commit is recorded in this value
table.
