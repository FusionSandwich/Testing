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
| DESIGN | fixed-quadrature objective combining D2, rate/locality and regularization | FUTURE program value; certified convex value required | II |
| SEMI | semigroup/resolvent response norms | FUTURE program value with domain and conditioning | II |
| TRAN | equal-cost response errors split into angular, spatial, energy and model parts | FUTURE benchmark value with units/tolerances | II |
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
