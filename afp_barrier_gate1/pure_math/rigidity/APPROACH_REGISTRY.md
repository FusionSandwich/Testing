# Prompt 3 approach registry

## Execution note

Literal multiagent-v2 orchestration was not available in this execution
environment.  No claim is made that it ran.  Independence was preserved by
maintaining separately derived proof and adversarial routes, each with a
distinct mechanism and kill criterion, before synthesis.

## Active proof mechanisms

| Route | Mechanism | Independent output | Final role | Status |
|---|---|---|---|---|
| A1 | weighted variance equality | `Q_i-1=sum p_ij(x_ij-1)^2` | local equality and pointwise defect | COMPLETE |
| A2 | shared-edge logarithmic cocycle | `r_i/r_j=x_ij/x_ji` | path, diameter, and reference-loss bounds | COMPLETE |
| A3 | reversible Dirichlet form | swap directed defects using detailed balance | spectral-gap estimate | COMPLETE |
| A4 | electrical-network variational principle | `|u_i-u_j|^2<=R_eff E(u)` | effective-resistance estimate independent of paths | COMPLETE |
| A5 | spherical trigonometry | common side, common angle, exact law of cosines | exact face geometry | COMPLETE |
| A6 | round metric angle sum | no cone defect implies `q_i alpha=2pi` | constant valence | COMPLETE |
| A7 | Euler counting | `qV=2E`, `3F=2E`, `chi=2` | `q=3,4,5` and exact counts | COMPLETE |
| A8 | local-link combinatorics | link cycle and simplicial collar | direct uniqueness of `K4`, octahedral, icosahedral maps | COMPLETE |
| A9 | developing/face propagation | unique third vertex on opposite side of shared great circle | geometric uniqueness up to `O(3)` | COMPLETE |
| A10 | compact derivative enclosure | explicit derivatives of spherical cosine law | computed `C_ang` | COMPLETE |
| A11 | integer angular separation | finite gap among `2pi/m` | stable valence identification | COMPLETE |
| A12 | monotone equilateral angle map | explicit positive derivative | distance to exact Platonic side | COMPLETE |
| A13 | covariance radial/tangent split | tangent directions and second moment `T_i` | exact `Q=1` covariance decomposition | COMPLETE |
| A14 | sampling-kernel analysis | axis-class Markov contraction | weighted-octahedron `E_sample={0}` | COMPLETE |
| A15 | exact Gram/hull algebra | algebraic Platonic coordinates | certified finite embeddings | COMPLETE / COMPUTATIONAL |
| A16 | source-pinned canonical generation | `plantri` through 12 vertices | hostile finite census | COMPLETE / COMPUTATIONAL |

## Deliberately independent adversarial routes

| Adversarial route | Targeted hidden assumption | Exact family/test | Outcome |
|---|---|---|---|
| F1 | triangulation omitted | cube, dodecahedron | unrestricted Platonic claim rejected |
| F2 | connectedness omitted | disjoint tetrahedral/octahedral components | one global rate fails |
| F3 | antipodal edge admitted | two-state `+/-e_1` chain | `ell=2`, `r=1`, `Q=1` survives separately |
| F4 | face nondegeneracy omitted | equatorial 120-degree triangle | equal loss with zero-area face |
| F5 | minor arcs omitted | major arcs on the same endpoints | common chord does not choose common minor length |
| F6 | all triangulation edges active omitted | cube with inactive face diagonals | inactive edges evade propagation |
| F7 | reversibility omitted | independently weighted octahedral rows | shared-edge rate comparison is unavailable |
| F8 | equal masses silently assumed | weighted reversible octahedron | exact theorem permits unequal masses |
| F9 | global positivity omitted | signed four-cardinal and pentagon examples | positive rigidity fails |
| F10 | full sphere/no cone defect omitted | congruent triangle cone gluings | angle sum need not be `2pi` |
| F11 | injectivity omitted | duplicated embedded states | abstract graph is not an embedded triangulation |
| F12 | axial covariance inferred from `Q=1` | three-parameter weighted octahedron | tangential anisotropy remains at `eta=0` |
| F13 | sampling kernel ignored | off-diagonal octahedral quadratic forms | form constraints are not sampled modes |
| F14 | diameter dependence hidden | long alternating paths | local ratios accumulate exponentially |
| F15 | small `kappa` dependence hidden | small active probabilities | pointwise defect scales as `sqrt(eta/kappa)` |
| F16 | path estimate treated as optimal | expanders and dense graphs | resistance/spectral-gap route can be sharper |

## Blocked or rejected routes

| Route | Blocking defect | Disposition |
|---|---|---|
| “Euler immediately gives Platonic solids” | assumes common valence before common face angle and round angle sum | REJECTED |
| “equal chords imply a spherical tiling” | does not check crossings, convexity, face coverage, or cone defects | REJECTED |
| finite enumeration as all-orders proof | verifies only a fixed vertex range | REJECTED AS PROOF; retained as falsification |
| generic appeal to Platonic uniqueness | omits the icosahedral combinatorial argument | REJECTED; replaced by link/collar proof |
| generic framework rigidity | transfers no spherical hypotheses or constants | NOT USED |
| Cauchy/Alexandrov as a black box | unnecessary and would require a convex-polyhedron transfer | NOT USED in the proof |
| numerical equal-edge embedding search | approximate solutions are not certificates | REJECTED |
| path multiplication only | hides graph geometry and may be weak | INCOMPLETE; supplemented by energy/resistance |
| unnamed compactness modulus | does not meet quantitative contract | REJECTED; explicit derivative box supplied |
| asymptotic `O(sqrt eta)` | hides `kappa`, radius, and nondegeneracy margins | REJECTED |
| `Q=1 =>` axial covariance | false in weighted octahedral family | REJECTED |
| `dim E_form = dim E_sample` | ignores sampling aliases | REJECTED |

## Cross-audit matrix

Every accepted classification step was checked by four routes:

1. line-by-line ordinary proof in `GLOBAL_Q_RIGIDITY_THEOREM.md`;
2. exact `plantri` census and graph-isomorphism checks;
3. explicit geometric-hypothesis deletion examples; and
4. a proof-source audit identifying which facts are standard, external, or new.

Every near-rigidity constant was checked by:

1. symbolic algebra for the variance and Platonic constants;
2. long-path and small-`kappa` stress cases;
3. exact weighted-Laplacian resistance calculations; and
4. direct derivative and interval-domain checks.

Every covariance statement was checked by:

1. the exact radial/tangent expansion;
2. the weighted-octahedron positive reversible family;
3. the infinity-norm sampled-space certificate; and
4. permanent Prompt 2 sampling-alias regressions.
