# P1B approach registry — sharp sampled quadratic-defect lower bound

This registry records independent proof and audit mechanisms used for P1B.
`COMPLETE` means that the route proves the displayed theorem or supplies a
machine-checkable certificate used by the accepted package. `SCREENED` means
that the route was examined but was unnecessary or invalid under the minimal
hypotheses. No P1B deliverable remains `BLOCKED`.

| Mechanism family | Status | Concrete output | Equality or adversarial boundary |
|---|---|---|---|
| weighted generalized Gram pencil | COMPLETE | `G_R <= D_2^2 G_S` on the sampling quotient; trace ratio and exact two-defect coefficient | equality iff every nonzero generalized eigenvalue equals `D_2^2` |
| quotient-map Hilbert--Schmidt factorization | COMPLETE | `R_2=U S_2`, `||R_2||_HS <= ||U|| ||S_2||_HS`, with `||U||=D_2` | equality iff `U^*U=D_2^2 I` on `im S_2` |
| isotropic random traceless matrices | COMPLETE | expectation of sampled and residual energies equals the two weighted traces | full-support equality audit recovers the same operator saturation |
| finite frame/covariance domination | COMPLETE | domination of residual frame `{sqrt(w_i)M_i}` by sampling frame `{sqrt(w_i)Z_i}` | frame dependence and aliases are allowed; no injectivity used |
| local loss variance | COMPLETE | `epsilon_i >= (d-1)^2/r_i >= (d-1)^2/r_max` and exact equality conditions | zero variance fixes every active loss but not tensor isotropy |
| local tensor decomposition | COMPLETE | `M_i=d epsilon_i Z_i/(d-1)+B_i`; exact anisotropy contribution | trace saturation alone need not force `B_i=0` |
| equality synthesis | COMPLETE | final equality iff `r_i=r_max`, local loss variance is zero, and `B_i=0` at every vertex; then `R_2=cS_2` | unequal repeated-node fixture saturates the trace step but not the final theorem |
| all-dimensional sharpness family | COMPLETE | regular simplex has `D_2=d+1`, `r_max=d(d-1)/(d+1)` and exact product `d(d-1)` | proves universal constant is sharp for every `d>=2` |
| cross-polytope / hypercube equality families | COMPLETE_SUPPORT | independent exact equality families from P1A | contain large sampling kernels in several dimensions |
| semigroup dissipation | SCREENED_NOT_USED | no additional theorem | `im S_2` need not be invariant under `L+2dI`; forcing invariance would strengthen the hypotheses |
| asymptotic graph convergence | SCREENED_EXTERNAL | prior-art boundary only | asymptotic probabilistic convergence does not prove the finite sharp trace constant |
| association schemes / spherical designs | SCREENED_EXTERNAL | symmetry explanation for regular equality examples | not hypotheses for unequal masses, repeated nodes, or disconnected generators |
| exact symbolic computation | COMPLETE_AUDIT | 24 exact fixtures and mutation tests | finite computation is regression evidence, not the all-orders proof |
| nearly singular sampling | COMPLETE_ADVERSARIAL | exact rational antipodal-pair family with positive Gram determinant tending to zero | constant and proof are condition-number independent |
| disconnected support | COMPLETE_ADVERSARIAL | two-component exact equality fixture | connectedness is not required by the theorem |
| zero sampling rank | REJECTED_CONFIGURATION | `S_2Z_i(i)=(d-1)/d>0` | impossible for nonempty unit-sphere data with `d>=2` |
| Lean finite-sum trace core | COMPLETE_CANDIDATE | coordinate energy domination implies weighted trace domination; scalar coefficient and product steps | exact-head Lean build and focused axiom audit control acceptance |

## Independent audit rounds

1. The quotient/Gram route derived the coefficient directly from the deflated
   generalized pencil.
2. A separate Hilbert--Schmidt route avoided choosing a complement of the
   sampling kernel.
3. An isotropic-random-matrix route reconstructed both traces as expectations.
4. A finite-frame route checked that aliases and dependent rows do not alter
   the inequality.
5. An equality adversary separated trace saturation, radial equality, rate
   equality, and final equality.
6. A degeneracy adversary tested unequal masses, repeated nodes, disconnected
   graphs, antipodal edges, aliased forms, genuine sampled modes, both nonzero
   defects, and nearly singular sampling matrices.
7. Formalization was started only after the ordinary theorem and equality
   proof were complete.

No route was allowed to replace the sampled quotient by a Frobenius quotient,
use an unweighted transpose, assume `im S_2` invariant, or infer the result
from a finite family of symmetric examples.
