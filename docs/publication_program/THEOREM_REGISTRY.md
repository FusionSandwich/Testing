# AFP publication program — theorem registry

## 1. Status vocabulary

Every entry uses exactly one primary status:

- `PROVED`: established in the accepted ordinary theorem package, with the stated hypotheses.
- `EXTERNAL`: imported standard or adjacent-field theorem; not claimed as project novelty.
- `COMPUTATIONAL`: fixed-instance or finite-range verification; never an all-orders substitute.
- `CONJECTURE`: mathematically plausible target not proved in the accepted baseline.
- `REJECTED`: false, overclaimed, or invalid under the displayed formulation.
- `BLOCKED`: research route without a complete theorem, certificate, or transferred hypothesis set.

A theorem may be `PROVED` only under the hypotheses stated in its row. “Proved under explicit hypotheses” is not a separate status; the hypothesis column controls its scope.

## 2. PROVED claims

| ID | Paper | Claim | Mandatory hypotheses / boundary | Ordinary source | Formal or exact source |
|---|---|---|---|---|---|
| I-L1 | I | Indexed non-antipodal local feasibility is equivalent to `0` belonging to the convex hull of indexed tangent directions; strict positivity on every indexed edge is equivalent to relative-interior membership. | Finite candidate set on `S^2`; non-antipodal neighbors; repetitions and lower-dimensional affine spans allowed. | `afp_barrier_gate1/pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` | `LocalSphericalFeasibility.lean`, `SphericalFeasibilityAlgebra.lean`, `test_spherical_feasibility.py` |
| I-L2 | I | The normalized tangent dependence has the unique angular scaling `a_j=2 beta_j/[sin(theta_j) S(beta)]`. | Feasible normalized dependence; `0<theta_j<pi`; `S(beta)>0`. | same | `ExactLocalRows.lean`, exact local audit |
| I-L3 | I | Antipodal-only rows form an exact simplex; mixed rows split tangent and antipodal normal budgets without assigning a tangent direction to an antipode. | Positive rates; exact `-2` spherical coordinate moment. | same | `AntipodalFeasibility.lean` |
| I-L4 | I | A positive relative inradius yields explicit coefficient, row-rate, conditioning, and perturbation bounds. | Relative tangent span; positive inradius; stated angular window. | same | `Quantitative.lean`, `QuantitativeSphericalFeasibility.lean`, `QuantitativeExactLocal.lean` |
| I-G1 | I | Reversible shared-edge feasibility is the cone problem `A gamma=b`, with exact Farkas alternative, LP duality, and complementary slackness. | Finite undirected permitted graph; positive masses; symmetric nonnegative conductances; exact sign convention. | same | `SharedEdgeEquilibrium.lean`, `GlobalSharedEdgeDuality.lean`, `DualCertificate.lean` |
| I-G2 | I | Weighted centering is necessary; on the complete graph it is sufficient via `gamma_ij=2 w_i w_j`. | Positive masses, unit-sphere eigenmap, complete graph for sufficiency. | same | `CompleteGraph.lean`, `ReversibleConductance.lean` |
| I-G3 | I | Equivariant averaging and centered-clique decompositions provide exact reconciliation mechanisms in their stated classes. | Invariance or clique-cover hypotheses stated in source. | same | `GroupAveraging.lean` |
| I-G4 | I | Local row feasibility plus weighted centering does not imply arbitrary sparse shared-edge feasibility. | Exact four-cycle/cube constructions. | counterexample catalogue | `exact_local_global_audit.py`, exact Farkas certificates |
| II-Q1 | II | Exact quadratic covariance identity: `L Q_A=-2 lambda Q_A+tr(A^T C_i)`. | Finite generator difference form; coordinate eigenmap; no positivity or reversibility needed. | `covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md` | `QuadraticCovariance.lean`, `quadratic_covariance_audit.py` |
| II-Q2 | II | Spherical residual-through-sampling factorization: `R_X=(L+2d I)S_X`. | `Phi_i in S^(d-1)`, `L Phi=-(d-1)Phi`, `A in Sym_0(d)`, target `-2d`. | same | `QuadraticCovariance.lean`, exact factorization audit |
| II-Q3 | II | `K_X subset E_form` and `E_sample=im(S_X) intersect ker(L+2dI)`; `dim E_sample=rank S_X-rank R_X`. | Same as II-Q2; dimensions are sampled dimensions. | same | restricted-map Lean lemmas, exact rank certificates |
| II-Q4 | II | Positive axial covariance gives `E_form=K_X` and `E_sample={0}`. | Axial covariance rowwise; positive radial coefficient, obtained from at least one positive jump to a distinct point. | same | row-scaling Lean lemma, Platonic exact audit |
| II-Q5 | II | Positive equivariant irreducibility gives `E_form={0}`. | Transitive equivariant action; irreducible real action on `Sym_0(d)`; **all** off-diagonal rates nonnegative; one positive distinct jump. | same | prompt-2 closeout audit and signed-pentagon regression |
| II-P1 | II | Shifted-product and centered-square resonance are characterized by constant carré du champ. | Finite generator; displayed eigenfunction equations. | same and final theorem package | `QuadraticCovariance.lean`, Boolean centered-square audit |
| III-R1 | III | Exact spherical rate–defect inequality `Q_i>=1`, with equality iff every active incident loss is `2/r_i`. | Nonnegative active rates; `L Omega=-2 Omega`. | `rigidity/SPHERICAL_Q1_RIGIDITY_THEOREM.md`; `GLOBAL_Q_RIGIDITY_THEOREM.md` | `LossVariance.lean`, `SphericalQOneRigidity.lean`, `SphericalQEqualityRigidity.lean` |
| III-R2 | III | Exact equality propagates one global row rate and one active-edge loss. | Symmetric connected active relation; exact equality at every vertex. | same | `GlobalLossRigidity.lean`, rich Prompt 3 Lean |
| III-R3 | III | The regular tetrahedral, octahedral, and icosahedral embeddings are the only exact `Q=1` realizations in the stated round minor-arc geodesic-triangulation class. | Finite simple sphere triangulation; active support exactly its one-skeleton; injective minor arcs; noncrossing edges; convex nondegenerate faces; disjoint interiors; complete round-sphere coverage; no cone defect or multiple cover; every edge active. | `GLOBAL_Q_RIGIDITY_THEOREM.md`, `ICOSAHEDRAL_GRAPH_LEMMA.md` | selected finite Lean algebra; exact Gram/hull regressions |
| III-R4 | III | Pointwise, adjacent-edge, path, diameter, graph-radius, edge-loss, and arclength near-rigidity bounds with explicit constants. | `p_ij>=kappa>0`; `1<=Q_i<=1+eta`; symmetric connected activity; `delta=sqrt(eta/kappa)<1`; certified loss interval for arclength. | `GLOBAL_Q_RIGIDITY_THEOREM.md` | `QuantitativeGlobalNearRigidity.lean`, `global_near_rigidity_audit.py` |
| III-R5 | III | Dirichlet energy, Poincaré variance, and effective-resistance refinements. | Reversibility with `mu_i=w_i r_i`, `pi_i=mu_i/sum mu`; connected chain; stated gap/resistance convention. | same | exact small-graph and rational path audits |
| III-R6 | III | Explicit edge-metric Platonic stability with Gram/spherical-Heron angle certification and nonzero `q=3,4,5` thresholds. | Near-equality triangulation hypotheses; certified side box in `(0,pi)`; positive Gram determinant and angle-sine floors; integer valence gap. | same | `global_near_rigidity_audit.py` |
| III-C1 | III | At `Q=1` and `0<ell<2`, the covariance decomposes into radial and tangent terms, and axial covariance is equivalent to `T_i=P_i/2`. | Exact local equality; genuine non-antipodal range. | `GLOBAL_Q_RIGIDITY_THEOREM.md` | `QEqualityCovariance.lean`, `q1_covariance_audit.py` |
| III-C2 | III | At the antipodal boundary `ell=2`, `r=1` and covariance is purely radial, with no canonical tangent unit vector. | Exact antipodal equality case. | same | antipodal Lean declarations and two-state exact regression |
| III-C3 | III | Positive reversible weighted-octahedral family has `Q=1` but axial covariance iff `g_12=g_13=g_23`; tangent anisotropy approaches `1/2`. | `g_12,g_13,g_23>0`; masses as stated. | same | `QEqualityCovariance.lean`, exact symbolic audit |
| III-C4 | III | Every positive weighted-octahedral member has genuine sampled degree-two exact space `{0}`. | Actual sampling map and generator action; positive parameters. | same | determinant certificate for `P+2I`; exact sampled-space audit |
| III-B1 | III | On the fixed unreduced square product graph, the polar coordinate equations uniquely force the inward and azimuthal rates and the exact graph-class minimax row. | Fixed adjacency; exact spherical coordinates; positive class for minimax attainment; no ring-symmetry assumption. | `barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md` | `SharpProductBarriers.lean`, Prompt 4 audit |
| III-B2 | III | Uniform polar rate and quality expansions with explicit remainders for every integer `N>=2`. | Exact polar formula; classical trigonometric expansion inputs. | same | `SharpProductBarriers.lean`, exact symbolic remainder audit |
| III-B3 | III | Universal rate barrier `epsilon_i<=C h^2 => r_i>=4/(C h^2)` and quasi-uniform loss-window transfer. | Nonnegative row; exact first moment `sum a ell=2`; stated loss window where invoked. | same | `SharpProductBarriers.lean`, `QuasiUniformLossBounds.lean` |
| III-E1 | III | Rate-capped extremal class has `E_K>=4/(RK)`, `C*>=4/R`, and fixed-`K` minimizers; the unreduced product family is eventually excluded. | Nonempty closed finite-dimensional class with displayed degree, locality, geometry, mass, positivity, reversibility, and rate constraints. | same | exact Prompt 4 audit |
| III-A1 | III | Projective feasible-cone formula, fixed-mean sliced LP, explicit dual anisotropy certificate, and sharp examples. | Nonempty tangent-balanced positive cone; positive mean loss. | same | exact LP audit |
| III-I1 | III | Biregular adjacent-ring incidence satisfies `p M_i=q M_j`; a perfect matching forces equal ring counts. | Stated bipartite biregular/perfect-matching coupling class. | same | `SharpProductBarriers.lean`, 180 exact fixtures |

## 3. EXTERNAL claims and tools

| ID | Used by | External input | Transfer requirement |
|---|---|---|---|
| X-CVX | I, III | finite convex-hull separation, relative interior, finitely generated cones, Farkas alternatives, LP strong duality, complementary slackness | Use the repository’s exact matrix, sign, affine-span, and positivity conventions. |
| X-SPH | III | spherical cosine laws, spherical Heron/Gram identities, Euler identities for genuine sphere triangulations | Verify minor arcs, nondegenerate convex faces, complete coverage, and absence of cone defect before transfer. |
| X-PLANAR | III | finite planar-map facts and combinatorial uniqueness facts | State the exact map hypotheses; finite enumeration is not the theorem. |
| X-RIGID | III | convex polyhedral rigidity or spherical developing-map facts when cited | Verify strict convexity and congruent-face hypotheses; no unstated uniform stability constant. |
| X-MARKOV | III | Poincaré variational principle, Dirichlet principle, effective resistance | Use `c_ij=pi_i p_ij`, and the same `1/2` Dirichlet normalization as the theorem. |
| X-TRIG | III | cotangent/cosecant Mittag–Leffler expansion and special zeta values | Imported only for analytic expansion; the forced graph rate and remainder transfer remain project results. |
| X-DELAUNAY | I, III | existence and positivity facts for spherical Delaunay Laplacians and exact low modes | Do not infer that a fixed AFP graph is Delaunay without checking its hypotheses. |
| X-REP | II | representation-theoretic irreducibility of a particular group action | The project theorem assumes irreducibility; it does not classify representations. |

## 4. COMPUTATIONAL claims

| ID | Evidence | Exact scope | Prohibited upgrade |
|---|---|---|---|
| C-PLANTRI | source-pinned Plantri enumeration | all 9,150 simple triangulations on 4–12 vertices; counts `1,1,2,5,14,50,233,1249,7595` | not the all-orders classification proof |
| C-PLATONIC | exact SymPy and algebraic rank audits | the five displayed Platonic vertex sets and shortest-edge generators | not a classification of all spherical graphs |
| C-PATH | deterministic stress audit | 174,816 specified path/parameter cases | not proof of arbitrary graph bounds |
| C-GRAM | zero-width and positive-width interval/grid certificates | the three recorded Platonic side boxes and conservative thresholds | not an optimal threshold theorem |
| C-RING | exact incidence fixtures | 180 recorded biregular fixtures | not a general split/merge ring theorem |
| C-CI | Lean/nanoda/workflow artifacts | literal recorded source objects and declaration slices | provenance and formal verification, not novelty |

## 5. CONJECTURE claims

| ID | Claim | Current boundary | Reopen criterion |
|---|---|---|---|
| Q-OPT | The accepted near-rigidity constants can be substantially sharpened or made optimal. | No optimality claim is accepted. | A proof of a sharper universal bound plus matching sharpness family. |
| Q-COORD | Edge-metric stability can be converted to coordinate closeness modulo `SO(3)` under an explicit rigidity margin. | Only edge-metric stability is accepted. | Gauge-fixed rigidity matrix, certified smallest nonzero singular value, derivative-Lipschitz bound, and admissible nonlinear radius. |
| Q-RINGS | Broader reduced-ring split/merge constructions admit a complete sharp classification. | Only the stated biregular/perfect-matching obstruction is proved. | All-orders construction or nonexistence theorem with exact incidence hypotheses. |
| Q-HIGHER | Higher-degree sampled harmonic exactness may admit additional structural factorization theorems. | Prompt 2 establishes only the quadratic package; generic hierarchy claims failed. | Explicit sampling-aware factorization and non-alias theorem. |

## 6. REJECTED claims

| ID | Rejected statement | Permanent obstruction |
|---|---|---|
| R-PLATONIC | `Q=1` implies `K in {4,6,12}` or a Platonic triangulation for an arbitrary spherical graph. | Cube and dodecahedron shortest-edge generators also have `Q=1`. |
| R-ENUM | Plantri verification through 12 vertices proves the classification. | Finite enumeration cannot replace the all-orders geometric proof. |
| R-FORM | A nonzero exact quadratic form automatically defines a nonzero sampled function. | Tetrahedron, octahedron, and cube have nonzero form kernels contained in `K_X`; sampled exact dimension is zero. |
| R-AXIAL | `Q=1` forces axial covariance. | Unequal positive weighted-octahedral family. |
| R-ETA | Small scalar `eta` controls tangent anisotropy. | The weighted-octahedral family has `eta=0` and anisotropy approaching `1/2`. |
| R-ANTIPODE | Tangent normalization is valid at `ell=2`. | Denominator `sqrt(ell(2-ell))` vanishes; covariance is purely radial. |
| R-COORD | Edge-loss concentration alone gives coordinate-space closeness. | Missing framework singular-value margin; flexible/ill-conditioned limits are not excluded. |
| R-FLAGSHIP | The local weighted variance identity is the new flagship theorem. | It is an elementary supporting identity; the publication claims require sampled factorization, restricted global geometry, and sharp graph barriers. |
| R-LOCALGLOBAL | Local positive rows plus weighted centering imply sparse global shared-edge feasibility. | Exact sparse Farkas counterexamples. |
| R-CENTERED | Positive generators forbid nonzero centered-square resonance. | Exact four-state Boolean centered-square example. |
| R-HIERARCHY | Arithmetic eigenvalue resonance alone yields a general sampled spectral-product hierarchy. | Sampling aliases, missing multiplicity control, and exact low-degree/Pell audits. |
| R-SYMMETRY | Prompt 4’s polar obstruction requires ring-symmetric rates. | The coordinate equations force the relevant rate equalities without that assumption. |

## 7. BLOCKED routes

| ID | Route | Why blocked | Materially new mechanism required |
|---|---|---|---|
| B-DELSARTE | Delsarte/Gegenbauer dual program as a replacement global theorem | No solved new certificate survived finite sampling aliases. | Explicit feasible dual polynomial tied to the actual sampling map. |
| B-BAKRY | Bakry–Émery curvature theorem from the one-function `Gamma_2` calculation | The calculation is not a curvature-dimension theorem; broad negative claims are false. | Full curvature matrix or CD inequality under verified graph hypotheses. |
| B-HOMOG | Compact homogeneous-space extension | No complete sampling-aware theorem or formal transfer. | Exact representation/sampling decomposition and finite generator construction. |
| B-TRANSPORT | Discrete transport-metric consequence | Positivity does not select a continuum `W_2` theory; Maas/Erbar use a distinct metric. | Exact entropy-gradient-flow or curvature transfer in the repository normalization. |
| B-RINGGENERAL | General split/merge reduced-ring theorem | Only one incidence class is resolved. | All-orders construction, obstruction, or complete combinatorial classification. |
| B-FRAMEWORK | Uniform coordinate-level framework stability | No certified uniform rigidity margin across the required family. | Explicit gauge, singular-value floor, nonlinear inverse radius, and transferred constants. |

## 8. Sampling-kernel rule

Every Paper II or Paper III quadratic claim must display the map

```text
S_X : Sym_0(d) -> R^I,
(S_X A)_i = Phi_i^T A Phi_i.
```

It must distinguish:

```text
K_X = ker S_X,
E_form = ker R_X,
E_sample = S_X(E_form).
```

No rank, dimension, exactness, or counterexample statement may replace `E_sample` by `E_form` unless sampling injectivity has been proved for the exact vertex set.
