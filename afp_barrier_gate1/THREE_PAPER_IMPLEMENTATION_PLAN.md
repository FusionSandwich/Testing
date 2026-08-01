# AFP Three-Paper Research and Implementation Plan — Revised After Critical Review

**Version:** 2.0  
**Purpose:** integrate the strongest ideas from the independent critical reviews, symbolic verification script, and the existing three-paper program into one mathematically honest and ambitious implementation plan.

**Three intended outputs:**

1. **Pure mathematics:** spectral-algebra obstructions, attainable quadratic exactness, and global rigidity for finite positive generators.
2. **Numerical analysis:** globally optimized, robust, and provably convergent positive spherical AFP discretizations.
3. **Particle transport:** Radiant integration and physical Boltzmann–Fokker–Planck validation in spatially layered media, including an HTS-coated-conductor demonstration.

---

# 1. Strategic reset

The independent reviews are correct about the central weakness:

> The present project contains correct and useful mathematics, but too much of the current headline material reduces to standard jump-generator algebra, Cauchy–Schwarz, weighted variance, and imported discrete-geometric results.

The new program therefore adopts four rules.

## Rule 1 — Infrastructure is supplementary

Lean, CI, pinned dependencies, test counts, and artifact hashes remain mandatory for correctness and reproducibility.

They are removed from the mathematical novelty argument.

In a manuscript they belong in:

- a short formal-verification statement;
- a reproducibility appendix;
- a companion repository;
- data and code availability.

They do not appear as scientific contributions.

## Rule 2 — No paper is earned by relabeling the same theorem

The three papers require three distinct contributions:

| Paper | Required independent contribution |
|---|---|
| Pure mathematics | A theorem that remains interesting after all AFP and transport terminology is removed |
| Numerical analysis | A new globally coupled operator-construction method plus convergence and robustness theory |
| Particle transport | A demonstrated response or cost improvement in a production-relevant BFP calculation |

## Rule 3 — Novelty is settled before substantial new formalization

Before expanding Lean, perform the cross-disciplinary priority review across:

- discrete Bakry–Émery theory;
- Markov-generator diffusion properties;
- graph-Laplacian product rules;
- positive and mimetic stencils;
- discrete differential geometry;
- spherical designs and codes;
- manifold graph-Laplacian convergence;
- positive moment realizability and transport closures.

## Rule 4 — Every ambitious conjecture gets a counterexample phase first

Before proving or formalizing a conjecture:

1. test small finite graphs;
2. solve finite LPs;
3. search symmetric configurations;
4. calculate limiting examples;
5. inspect nearby literature.

This is especially important for curvature, global `Q=1`, and high-order obstruction claims.

---

# 2. Corrections adopted immediately

Several ideas from the reviews are not merely optional improvements. They correct current wording or scope.

## 2.1 The core rate–defect inequality becomes a lemma

The result

```text
lambda^2 <= r_i epsilon_i
```

is Cauchy–Schwarz.

It remains central because of its AFP interpretation, but it is not marketed as a deep standalone theorem.

Recommended manuscript label:

> **Lemma 2.1 — local loss-moment inequality.**

The exact variance remainder and equality condition should be stated immediately after it as one proposition, not as multiple headline results.

## 2.2 The external geometric dependency is made explicit

The quasi-uniform achievability argument uses external positive spherical-Delaunay theory.

The project owns:

- the AFP normalization;
- the loss-window consequences;
- the rate and defect interpretation;
- the comparison with product and optimized operators.

The project does not claim to have invented the spherical Delaunay Laplacian.

The lower bound

```text
epsilon = O(h^2)  =>  r = Omega(h^-2)
```

is self-contained.

The matching upper construction is stated as an application of cited geometric existence results unless the entire geometric construction is separately proved.

## 2.3 The Farkas claim is narrowed until the theorem of alternatives is complete

The current Lean result proves:

> a supplied dual witness certifies infeasibility.

It does not yet prove:

> every infeasible positive system has such a witness.

The implementation plan therefore includes:

- conventional proof of the complete finite Farkas alternative;
- formalization of the full theorem if practical;
- solver-generated primal and dual certificates;
- precise distinction between certificate soundness and certificate completeness.

## 2.4 The layered energy claim is corrected

The current order-independent final energy follows from constant stopping powers:

```text
E_out = E_0 - sum_k S_k x_k.
```

It is not a generic property of layered slowing down.

The corrected mathematical problem is:

> For material-dependent stopping laws `S_m(E)`, characterize when the layer flow maps commute.

For autonomous scalar flows

```text
dE/ds = -S_m(E),
```

order independence for all sufficiently small layer thicknesses requires the vector fields to commute:

```text
S_A(E) S_B'(E) - S_B(E) S_A'(E) = 0.
```

On a connected interval where the stopping laws are nonzero, this implies

```text
S_A(E) = c S_B(E).
```

Thus a common separable energy dependence is the exceptional commuting case.

This theorem, followed by real stopping data, replaces the synthetic “energy order independence” headline.

## 2.5 Exact product-grid asymptotics are promoted

For the square equal-angle family,

```text
r_max(N)
 = 1/[2 sin^2(pi/(2N))]
 + 1/[2 sin^4(pi/(2N))].
```

The exact expansion is

```text
r_max(N)
 = (8/pi^4) N^4
 + [10/(3 pi^2)] N^2
 + 13/45
 + O(N^-2).
```

The leading coefficient `8/pi^4` should replace a regression slope as the primary result.

A stronger theorem target is:

> Within the class of rotationally invariant, nearest-neighbor, positive, degree-one-exact latitude–longitude stencils with `M=2N`, the `N^4` polar rate is unavoidable.

This requires a uniqueness or lower-bound proof for the admissible conductances, not merely evaluation of the current formula.

---

# 3. Evaluation of the proposed ambitious ideas

# 3.1 Ideas adopted as core work

## A. Full novelty review across adjacent mathematics

**Decision:** adopt immediately.

This is the first work package and a go/no-go gate for Paper I.

## B. Sphere-specific feasible-cone theorem

**Decision:** adopt for Paper II.

The exact local feasibility statement should be:

At node `Omega_i`, write non-antipodal neighbors as

```text
Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j,
```

with `u_j` in the tangent plane.

Positive degree-one exactness requires

```text
sum_j a_j sin(theta_j) u_j = 0,
```

```text
sum_j a_j [1-cos(theta_j)] = 2,
```

```text
a_j >= 0.
```

For no antipodal neighbor, nonnegative feasibility is equivalent to

```text
0 in conv{u_j}.
```

Strict positivity on all chosen neighbors is tied to a relative-interior condition.

The angular window `theta_j=O(h)` is not part of the basic feasibility iff. It controls coefficient size, conditioning, and the `h^-2` rate scale.

The useful new theorem is the quantitative version:

- cone margin;
- strict positivity margin;
- coefficient upper and lower bounds;
- perturbation radius;
- minimal edge augmentation;
- global compatibility after enforcing shared conductances.

## C. Global shared-edge optimization

**Decision:** highest-priority Paper II result.

The actual operator design problem is globally coupled:

```text
gamma_ij = gamma_ji >= 0,
```

```text
sum_j gamma_ij (Omega_j-Omega_i) = -2 w_i Omega_i.
```

The new method should compute a Pareto-optimal operator for objectives such as:

```text
min max_i r_i,
```

```text
min ||R_2(gamma)||,
```

or

```text
min max_{ell <= L} ||R_ell(gamma)||
subject to a rate budget.
```

This is the main bridge from diagnostic theory to a useful design algorithm.

## D. Predictive rather than retrospective diagnostics

**Decision:** adopt.

The project should distinguish:

1. radial-loss dispersion `Q_i-1`;
2. tangent anisotropy, measured by second-moment tensors;
3. higher-order asymmetry, measured by third/fourth tensors;
4. quadrature integration error;
5. spectral residual.

A priori geometric predictors should be derived before coefficients are solved when possible.

The local geometric optimization problem is:

```text
Q_i^*(X_i)
 = inf E_p[ell^2] / E_p[ell]^2
```

subject to

```text
p >= 0,
sum p = 1,
sum p sin(theta) u = 0.
```

A global version must include shared-edge symmetry.

## E. Consistency, spectral convergence, and semigroup convergence

**Decision:** essential Paper II work.

The preferred theorem chain is:

```text
L_h I_h f = I_h Delta f + E_h(f),
```

```text
||E_h(f)|| <= C h^p ||f||_{H^s},
```

then

```text
|lambda_{ell,h} - ell(ell+1)| <= C_ell h^p,
```

and finally

```text
||exp(t L_h) I_h f - I_h exp(t Delta) f||
 <= C_T h^p ||f||_{H^s}.
```

The actual order must be derived, not assumed from the peak defect.

## F. Global `Q=1` rigidity and near-rigidity

**Decision:** adopt for Paper I, but correct the conjecture.

The statement “only `K=4,6,12`” is false.

A cube gives a counterexample:

- `K=8`;
- three equal-distance neighbors per vertex;
- equal rates give `sum_j (Omega_j-Omega_i) = -2 Omega_i`;
- every active edge has loss `2/3`;
- therefore `Q_i=1`.

The correct first global theorem is:

> If a connected reversible degree-one-exact graph satisfies `Q_i=1` at every vertex, then the outgoing rate is constant on the graph and every active edge has one common spherical loss.

This reduces classification to equal-distance spherical frameworks with positive equilibrium stresses.

The hard follow-up should be restricted and precise, for example:

- classification under vertex transitivity;
- classification for maximal planar graphs with fixed valence;
- stability under `Q_i <= 1+eta`;
- relation to spherical stress matrices and distance-regular graphs.

## G. Moment hierarchy and spectral-product obstruction

**Decision:** adopt as a principal Paper I exploratory branch.

For an eigenfunction `f`,

```text
L(f^2) = 2 f Lf + Gamma(f).
```

If `f^2` decomposes into several eigenspaces, exactness imposes a linear relation among their residuals.

On the sphere, use Legendre or Gegenbauer linearization:

```text
P_ell^2 = sum_k c_{ell,k} P_{2k}.
```

The objective is not to repeat the same peak contradiction for each `ell`. It is to derive:

- a hierarchy of residual identities;
- lower bounds on jointly matchable harmonic content;
- dimension bounds as a function of valence or rate budget;
- a basis-independent global residual bound.

## H. Global `H_2` residual lower bound

**Decision:** adopt as a high-value Paper I theorem.

Let

```text
R_2 = L|_{H_2} + 6 I.
```

Use the spherical-harmonic addition theorem and the family of zonal quadratics to convert rowwise peak defects into a weighted operator, Frobenius, or Hilbert–Schmidt lower bound:

```text
inf_{L in A(R)} ||R_2|| >= C/R.
```

This would elevate the local no-go theorem to a global, basis-independent statement.

## I. Exact sharp constants and global minimax bounds

**Decision:** adopt as a stretch goal spanning Papers I–II.

Determine or bound constants such as

```text
C* = liminf_{K->infinity} K inf_{L in A_K} max_i epsilon_i.
```

Also study

```text
inf_{L in A_K} max_i Q_i.
```

Potential tools:

- spherical-code linear programming;
- Gegenbauer positivity;
- energy-minimizing point sets;
- equal-area partitions;
- stress matrices;
- global conductance LP duals.

Even a fixed-factor optimality theorem would materially strengthen the work.

## J. Reduced-ring construction

**Decision:** adopt as a practical Paper II branch.

Target ring counts

```text
M_i ~ N sin(theta_i).
```

The theorem must include:

- positive inter-ring couplings;
- shared-edge reversibility;
- exact degree-one modes;
- `O(N^2)` direction count;
- `O(N^2)`, not `O(N^4)`, maximum rate;
- structured data layout useful for sweeps.

An ad hoc interpolation scheme is not sufficient.

## K. Real stopping-power and layered-flow analysis

**Decision:** adopt for Paper III.

The transport paper should include:

- the flow-commutation theorem;
- real energy-dependent stopping data;
- real angular-scattering data;
- actual layer dimensions;
- an explicit comparison of layer orders.

The current synthetic model remains a regression test only.

---

# 3.2 Ideas retained as ambitious exploratory branches

## A. Bakry–Émery curvature and `Gamma_2`

**Decision:** investigate, but do not adopt the proposed collapse theorem as a claim.

Finite graphs with positive Bakry–Émery curvature exist, and discrete Obata-type rigidity results already form an active literature.

The safe research question is:

> How do degree-one exactness, `Q`, harmonic residuals, and the best local `CD(K,N)` constants interact for spherical AFP graphs?

Work package:

1. implement local curvature-matrix computation;
2. test tetrahedron, cube, octahedron, icosahedron, product grids, and quasi-uniform grids;
3. search for counterexamples to any proposed curvature obstruction;
4. derive a theorem only after the finite experiments indicate the correct statement.

Promising possible outputs:

- curvature defect bounds in terms of moment residuals;
- rigidity under simultaneous spectral and curvature equality;
- asymptotic curvature behavior of optimized AFP graphs.

Do not claim that no positive finite generator can satisfy `CD(1,2)` without a precise normalization and a proof that survives known positive-curvature graph examples.

## B. Discrete Gauss–Bonnet and topological defects

**Decision:** retain as a high-risk Paper I branch.

The identity

```text
sum_i [6-deg(v_i)] = 12
```

for a spherical triangulation does not by itself force `Q_i>1`: the regular icosahedron has degree-five vertices and can still attain local `Q=1`.

A viable topological theorem must target a stronger quantity:

- higher-moment isotropy;
- spectral splitting;
- third/fourth tangent moments;
- impossibility of globally hexagonal local geometry;
- concentration of anisotropy near unavoidable defects.

The research question becomes:

> What global spectral or tensor-consistency penalty is forced by spherical topology in a positive bounded-degree triangulation?

This is ambitious and potentially valuable.

## C. Delsarte/Gegenbauer global dual bounds

**Decision:** retain as a high-payoff stretch goal.

The fixed-geometry conductance problem is convex.

The joint node-and-conductance problem is not.

Configuration-independent lower bounds may be obtained using:

- positive-definite zonal kernels;
- Gegenbauer expansions;
- spherical-code LP or SDP bounds.

This could support sharp constants for global `H_2` residual or `Q`.

## D. Bakry–Émery/Obata rigidity for spectral embeddings

**Decision:** explore only after the novelty review.

The recent graph-rigidity literature studies first-eigenspace embeddings and equality in curvature/eigenvalue bounds.

This is close enough to the project that it is both a risk and an opportunity.

Possible contribution:

- weighted spherical AFP analogue;
- perturbative almost-rigidity;
- connection between curvature matrices and jump covariance.

## E. Discrete optimal-transport gradient flows

**Decision:** long-term optional branch, not a near-term paper requirement.

A reversible finite Markov chain is a gradient flow of entropy in a specialized discrete transport metric.

However:

- the metric is not simply the ambient `W_2` distance on the sphere;
- positivity alone does not imply exponential Wasserstein contraction;
- contraction requires a curvature lower bound.

A defensible program would:

1. identify the correct Maas/Erbar discrete metric;
2. prove entropy dissipation for AFP graphs;
3. estimate discrete Ricci curvature;
4. derive contraction only when the curvature estimate permits it;
5. study convergence of discrete transport metrics to spherical `W_2`.

This is too large to be load-bearing for the current three papers.

## F. Reusable Lean discrete exterior calculus

**Decision:** separate optional formal-methods project.

A Mathlib-quality library for simplicial forms, Hodge stars, and discrete Laplacians would be valuable, but it is:

- a large independent project;
- not needed to establish AFP novelty;
- likely to delay all three target papers.

Only pursue with:

- a formal-methods collaborator;
- a separate publication goal;
- independent resourcing.

The immediate formal priority is full Farkas/theorem-of-alternatives support and the new finite algebraic theorems, not a complete DEC library.

---

# 3.3 Ideas rejected or substantially reformulated

## A. “Only `K=4,6,12` can have `Q=1`”

**Reject.**

The cube with `K=8` is an explicit counterexample.

Replace with a restricted classification problem.

## B. “Gauss–Bonnet forces `Q>1`”

**Reject as stated.**

Topological degree defects do not alone force local radial-loss variance.

Target higher-order isotropy or global spectral effects instead.

## C. “Positivity implies `W_2` contraction”

**Reject.**

A Markov generator’s positivity gives a positive semigroup, not automatically an ambient Wasserstein contraction.

Curvature assumptions and the correct discrete transport metric are required.

## D. “No positive finite graph can satisfy `CD(1,2)`”

**Do not claim.**

Treat as a conjecture-generation problem until tested against known positively curved finite graphs.

## E. “Maximum angle `O(h)` is part of local feasibility iff”

**Correct.**

The local cone condition controls existence.

The angular window controls locality, coefficient magnitude, consistency, and stiffness.

## F. “Final energy is generically order independent”

**Reject.**

It is an artifact of constant or proportional stopping laws.

Replace with the flow-commutation theorem and real material data.

---

# 4. Revised Paper I plan — Pure mathematics

## 4.1 Working title

**Spectral-product obstructions, attainable quadratic exactness, and rigidity for finite positive generators**

## 4.2 Central theorem architecture

Paper I should contain four layers.

### P1 — General product-rule obstruction

Let `L` be a finite positive generator and `Phi` an eigenmap:

```text
L Phi = -lambda Phi.
```

For scalar components `f,g`,

```text
L(fg) = f Lg + g Lf + Gamma(f,g).
```

Use this to formulate exactness obstructions for spectral product spaces on compact diffusion models.

### P2 — Quadratic covariance characterization

Define

```text
C_i = sum_j a_ij (Phi_j-Phi_i)(Phi_j-Phi_i)^T.
```

For symmetric `A`,

```text
L(Phi^T A Phi)_i
 = -2 lambda Phi_i^T A Phi_i + tr(A C_i).
```

If a quadratic mode is required to have target eigenvalue `-mu`, exactness becomes a linear condition on `A`:

```text
tr(A C_i)
 + (mu-2 lambda) Phi_i^T A Phi_i
 - mu c_A
 = 0.
```

The paper should characterize:

- the local exact quadratic subspace;
- the global intersection over all nodes;
- dimension bounds;
- sharp examples.

### P3 — Global `H_2` residual theorem

On `S^(d-1)`, use addition formulas to derive a basis-independent lower bound for the complete degree-two residual.

A candidate statement is:

```text
||R_2||_{HS,w}^2
 >= F({r_i},{w_i},d),
```

where

```text
R_2 = L|_{H_2} + 2d I.
```

The theorem must quantify how the local defect propagates to the whole sampled eigenspace.

### P4 — Global rigidity or moment hierarchy

Complete at least one hard result.

#### Preferred option: global sharpness rigidity

Prove:

- connected `Q=1` implies uniform rate and common active edge length;
- characterize the corresponding positive equilibrium stresses;
- classify a restricted meaningful family;
- prove near-rigidity under `Q<=1+eta`.

#### Alternative: moment hierarchy

Use Legendre/Gegenbauer product coefficients to derive a hierarchy of unavoidable residuals across harmonic degrees.

#### Stretch: curvature/Obata theorem

Only pursue after computational and literature vetting.

## 4.3 Paper I computational laboratory

Before final theorem selection, build deterministic searches for:

- small vertex-transitive spherical graphs;
- regular and Archimedean polyhedra;
- distance-regular graphs;
- positive equilibrium stresses;
- exact quadratic subspaces;
- `Q=1` and near-`Q=1` examples;
- local `Gamma_2` curvature matrices.

Outputs:

- counterexample database;
- conjecture ledger;
- exact rational/algebraic examples where possible;
- Lean-ready finite statements.

## 4.4 Paper I acceptance criteria

Do not submit unless:

- [ ] novelty audit is complete;
- [ ] the main theorem is stated without AFP;
- [ ] full quadratic exactness is replaced by a characterization or global bound;
- [ ] one nontrivial global theorem is proved;
- [ ] false small-`K` classification conjectures are eliminated;
- [ ] the sphere is used essentially;
- [ ] Lean verifies the finite algebraic core;
- [ ] at least two external mathematicians review the theorem statement.

---

# 5. Revised Paper II plan — Numerical analysis

## 5.1 Working title

**Globally optimized monotone spherical diffusion with moment constraints**

## 5.2 New operator-design method

For fixed nodes, weights, and a candidate graph, solve a global LP or conic program over shared conductances.

### Core constraints

```text
gamma_ij = gamma_ji >= 0,
```

```text
sum_j gamma_ij (Omega_j-Omega_i) = -2 w_i Omega_i.
```

### Primary Pareto problems

#### Rate minimization

```text
min_gamma max_i r_i.
```

#### Harmonic-residual minimization under a rate budget

```text
min_{gamma,t} t
```

subject to

```text
|R_{ell,m,i}(gamma)| <= t,
r_i <= R_max.
```

#### Tensor-isotropy optimization

Minimize deviations of tangent second moments from the continuum isotropy tensor, together with third/fourth moment penalties.

## 5.3 Full feasibility and robustness theory

Prove:

1. exact rowwise tangent-cone criterion;
2. strict-positivity criterion;
3. quantitative cone margin;
4. coefficient bounds;
5. perturbation stability;
6. global shared-edge feasibility;
7. complete Farkas alternative;
8. primal/dual certificate extraction.

## 5.4 Tangent-moment consistency expansion

For tangent increments `xi_ij`, derive:

```text
L_h f
 = grad f dot M_i^(1)
 + (1/2) Hess f : M_i^(2)
 + (1/6) third_derivative f : M_i^(3)
 + ...
```

with curvature corrections.

Establish conditions under which:

```text
M_i^(1) = O(h^p),
```

```text
M_i^(2) = 2 I_T + O(h^p),
```

and higher tensors give the claimed convergence order.

This analysis should explain why `Q` alone is insufficient.

## 5.5 Convergence theorem

Prove at least one strong global result:

- weighted `L^2` consistency;
- spectral convergence;
- eigenspace convergence;
- semigroup convergence;
- response convergence.

The preferred target is:

```text
||exp(tL_h) I_h f - I_h exp(t Delta) f||_{l2(w)}
 <= C_T h^2 ||f||_{H^s}.
```

If only first-order convergence is true under the chosen assumptions, report that rather than forcing a second-order claim.

## 5.6 Product-grid theorem sharpened

For the symmetric nearest-neighbor latitude–longitude class:

1. prove uniqueness or characterize all degree-one-exact positive coefficients;
2. prove the unavoidable `N^4` polar rate;
3. give the exact leading coefficient `8/pi^4`;
4. determine whether reduced rings can attain `N^2`;
5. compare against the optimized global operator.

## 5.7 Predictive design metrics

Evaluate whether the following predict performance:

- `Q`;
- tangent second-moment anisotropy;
- third/fourth tensor norm;
- harmonic residuals;
- graph curvature;
- cone margin;
- maximum rate;
- quadrature conditioning.

The paper should produce a design decision tree, not merely a list of metrics.

## 5.8 Reduced-ring theorem

A structured alternative should be developed in parallel with the unstructured quasi-uniform method.

Success criteria:

```text
K = O(N^2),
r_max = O(N^2),
epsilon_max = O(N^-2),
```

with positive shared conductances and exact degree-one modes.

## 5.9 Paper II acceptance criteria

- [ ] new global operator, not just Delaunay reuse;
- [ ] complete convergence theorem;
- [ ] full certificate-based optimization;
- [ ] perturbation stability;
- [ ] quadrature and moment-transform analysis;
- [ ] matched Radiant matrix comparison;
- [ ] reduced-ring or quasi-uniform practical path;
- [ ] source and dual certificates archived;
- [ ] Lean checks the finite algebra and certificate contracts.

---

# 6. Revised Paper III plan — Particle transport

## 6.1 Working title

**Optimized monotone angular diffusion for spatial Boltzmann–Fokker–Planck transport in layered media**

HTS title only after physical validation:

**Monotone BFP transport for charged-particle deposition in layered REBCO coated conductors**

## 6.2 Immediate corrections

- update all layer documentation to identify the constant-stopping assumption;
- add the flow-commutation theorem;
- retain the synthetic case only as a unit test;
- do not claim generic energy order independence.

## 6.3 Radiant integration

Build a source-pinned read-only adapter that exports Radiant operators into the current validation contract.

Validate:

- sign convention;
- diagonal shift removal;
- quadrature weights;
- shared edges;
- conductance positivity;
- weighted symmetry;
- coordinate residual;
- mass conservation;
- source ordering.

Then compare:

1. Radiant pseudoinverse;
2. product reference;
3. Delaunay reference;
4. Paper II optimized operator;
5. reduced-ring operator if completed.

## 6.4 Spatial benchmark ladder

### T1 — Reproduce Bienvenue water benchmarks

This is the integration acceptance test.

### T2 — Manufactured 1D slab

Include:

- streaming;
- inflow boundary;
- exact or high-accuracy reference;
- angular diffusion;
- conservation;
- oblique orientation.

### T3 — Thin two-material interface

Include:

- interface current;
- layer-resolved deposition;
- explicit versus homogenized layer;
- grazing directions;
- spatial convergence.

### T4 — Physical forward-peaked kernel

Use Radiant multigroup data or another traceable evaluated kernel.

Separate:

- Boltzmann model error;
- FP approximation error;
- angular discretization error;
- spatial error;
- energy error.

### T5 — Real stopping and layer-flow order

Use real `S_m(E)` and angular coefficients.

Test the flow-commutation condition numerically and quantify order effects.

### T6 — HTS tape

Use a documented stack with:

- Cu;
- Ag;
- REBCO;
- buffer/MgO;
- Hastelloy.

Responses:

- deposition by layer;
- interface currents;
- secondary source;
- orientation sensitivity;
- explicit versus homogenized tape;
- operator-family comparison.

## 6.5 Implicit and iterative solver study

The explicit CFL result is retained but not used as the sole cost metric.

Measure:

- backward Euler;
- exponential/Krylov;
- source iteration;
- GMRES;
- preconditioning;
- memory;
- total runtime;
- response error at equal cost.

## 6.6 Diagnostic correlation study

Build a single dataset containing:

```text
K,
r_max,
Q_max,
Q_mean,
```

tensor anisotropy, harmonic error, rotational spread, cone margin, iterations, runtime, and response error.

Determine which mathematical metrics actually predict transport performance.

## 6.7 Paper III acceptance criteria

- [ ] Radiant benchmark reproduced;
- [ ] spatial streaming included;
- [ ] physical forward-peaked data included;
- [ ] energy-dependent stopping included;
- [ ] real HTS stack included;
- [ ] independent reference included;
- [ ] implicit solver performance included;
- [ ] equal-cost comparison included;
- [ ] claims about `Q` are supported or narrowed;
- [ ] ray effects remain explicitly separate.

---

# 7. Cross-paper ambitious research branches

These branches are valuable but should not delay the core program unless they produce early positive evidence.

## 7.1 Bakry–Émery curvature branch

Deliverables:

- curvature-matrix implementation;
- benchmark curvature constants;
- relation to `Q` and spectral residual;
- exact theorem only if supported.

## 7.2 Topological anisotropy branch

Deliverables:

- tangent-moment defect around five-valent and other topological defects;
- global lower bound on higher-order isotropy or spectral splitting;
- no unsupported claim that topology alone forces `Q>1`.

## 7.3 Discrete optimal transport branch

Deliverables:

- entropy dissipation in the correct discrete transport metric;
- curvature-conditioned contraction;
- possible convergence to spherical Wasserstein flow.

Not a current paper requirement.

## 7.4 Formal DEC branch

Deliverables:

- separate Mathlib-oriented repository;
- simplicial cochains and Hodge structures;
- independent publication path.

Do not charge this work to the three AFP papers.

---

# 8. Revised order of attack

## Phase 0 — Correct and isolate

1. update energy-order wording;
2. update Farkas wording;
3. state external Gate 4 dependencies;
4. move CI history to supplements;
5. add exact `8/pi^4` polar constant;
6. create claim matrix.

## Phase 1 — Novelty and counterexamples

1. discrete Bakry–Émery search;
2. positive-stencil and mimetic search;
3. manifold convergence search;
4. moment-realizability search;
5. small-graph `Q=1` enumeration;
6. curvature and moment-hierarchy experiments.

## Phase 2 — Paper I theorem discovery

1. covariance characterization;
2. global `H_2` residual;
3. global `Q=1` rigidity;
4. restricted classification or near-rigidity;
5. moment hierarchy;
6. choose one main theorem.

## Phase 3 — Paper II operator

1. full local robust cone theorem;
2. global LP and dual;
3. tangent-moment expansion;
4. convergence proof;
5. reduced-ring construction;
6. Radiant matrix comparison.

## Phase 4 — Paper III implementation

1. Radiant adapter;
2. spatial slab;
3. interface;
4. physical scattering/stopping;
5. HTS stack;
6. implicit solver and response study.

## Phase 5 — Optional high-risk math

1. Bakry–Émery rigidity;
2. topology-induced anisotropy;
3. Gegenbauer global bounds;
4. discrete Wasserstein;
5. formal DEC.

---

# 9. Stop conditions

## Paper I stops as a separate paper if:

- the general obstruction is already known;
- covariance analysis yields only trivial rank counting;
- no global or higher-order theorem is obtained.

Then its results become Section 2 of Paper II.

## Paper II stops as a strong numerical paper if:

- no convergence theorem can be proved;
- global optimization reproduces existing coefficients;
- prescribed quadrature constraints destroy feasibility;
- gains vanish after quadrature-transform costs.

Then target a specialized transport-method venue.

## Paper III stops as an “improvement” paper if:

- Radiant matches or beats the new operator;
- gains disappear under implicit solvers;
- physical layer responses are insensitive;
- quasi-uniform grids produce worse streaming/ray effects.

A well-designed negative result can still be published.

---

# 10. The three final paper theses

## Paper I — Pure mathematics

> Finite positive generators face spectral-product obstructions. We characterize their attainable quadratic exactness and prove a global rigidity or residual theorem on spherical eigenmaps.

## Paper II — Numerical analysis

> We solve the globally coupled positive moment-constrained design problem, derive robust feasibility and convergence theory, and construct an optimally balanced spherical AFP operator.

## Paper III — Particle transport

> The optimized operator improves response accuracy, orientation robustness, and solver cost in spatial BFP transport and layered HTS-relevant calculations.

If all three sentences are fully supported, the project earns three papers.

---

# 11. Immediate implementation checklist

- [ ] Commit a corrected claim matrix.
- [ ] Add cube and other symmetric `Q=1` counterexamples to the research tests.
- [ ] Add exact polar asymptotic expansion test.
- [ ] Correct the layer-order documentation and add noncommuting stopping-law tests.
- [ ] Search and document Bakry–Émery/Obata prior art.
- [ ] Implement full local cone-margin computation.
- [ ] Implement global shared-edge LP with primal/dual export.
- [ ] Derive the quadratic covariance identity.
- [ ] Derive a global `H_2` residual candidate.
- [ ] Begin tangent-moment consistency expansion.
- [ ] Build a Radiant read-only adapter.
- [ ] Select one real stopping/scattering dataset.
- [ ] Select one documented HTS tape stack.
- [ ] Keep Lean work focused on new finite algebra, not infrastructure growth.
