# Prompt 3 readiness handoff

## Readiness state before final Prompt 2 integration

```text
PROMPT_2_STATUS=PENDING_FINAL_TARGET_CI
PROMPT_3_BASELINE_STATUS=NOT_YET_FROZEN
closeout_branch=agent/afp-pure-math-p2-closeout-corrected
closeout_start_head=1835918fe9d0b941395e9f00f6ac5514129cefa0
closeout_pr=19
final_target_branch=agent/afp-pure-math-p0-m1
final_target_commit=PENDING
final_target_tree=PENDING
```

Prompt 3 must branch only from the final commit and tree inserted after the
closeout merge and exact final-head workflows. The previously reported
`694b913c99364bb0032a8ffbd7008b549b491af0` is not a valid remote baseline.

## 1. Prompt 1 accepted dependencies

Prompt 3 may use the corrected Prompt 1 package rooted at

```text
923dc47dae4f83dbea9cd56aa904164c6378e52d.
```

Accepted inputs include:

- indexed local convex-hull and relative-interior feasibility;
- exact positive scaling and row-rate formulas;
- repeated, redundant, and lower-dimensional tangent configurations;
- division-free pure and mixed antipodal classifications;
- explicit local coefficient, rate, conditioning, and perturbation bounds;
- global shared-edge cone, Farkas, LP, and complementarity theory;
- complete-graph, equivariant-averaging, and centered-clique reconciliation;
- exact sparse local-but-not-global counterexamples; and
- compatible global perturbation bounds under their stated range and rigidity
  hypotheses.

Prompt 3 must not re-prove these results or weaken their hypotheses silently.

## 2. Prompt 2 accepted dependencies

Subject to final closeout CI, Prompt 3 may use:

### 2.1 Covariance and sampling

```text
L(Phi^T A Phi)
 =-2lambda Phi^T A Phi+tr(A^T C_i),
```

```text
R_X=(L+2dI)S_X,
K_X subset E_form,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

### 2.2 Positive rigidity

Positive axial covariance at every state gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices are an all-dimensional equality family.

The independent equivariant theorem is usable only in this corrected form:

```text
finite transitive G-action;
rho:G->O(d);
Phi_i in S^(d-1);
Phi_{gi}=rho(g)Phi_i;
a_{gi,gj}=a_ij;
a_ij>=0 for every i!=j;
conservative diagonal;
L Phi=-(d-1)Phi;
real conjugation action on Sym_0(d) irreducible;
at least one positive jump joins distinct embedded points.
```

Then `E_form={0}`. Reversibility is not required.

### 2.3 Centered products

For eigenfunctions `Lf=-lambda f`, `Lg=-nu g`,

```text
L(fg-c)+mu(fg-c)
 =2Gamma(f,g)+(mu-lambda-nu)fg-mu c.
```

At additive resonance,

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2Gamma(f,g)=(lambda+nu)c.
```

For a square,

```text
L(f^2-c)=-2lambda(f^2-c)
iff
Gamma(f,f)=lambda c.
```

The uncentered `c=0` case forces zero carré du champ. Centered resonance is
allowed when the carré du champ is a positive constant.

### 2.4 Semigroup and Jensen distinction

Centered square resonance is equivalent, under finite-dimensional
matrix-semigroup differentiability, to

```text
P_t(f^2)-(P_t f)^2=c(1-exp(-2lambda t)).
```

Jensen equality is the separate zero-variance condition that `f` is constant
on positive transition support.

### 2.5 Abstract equality propagation

The following are already `PROVED / LEAN` in
`AFPBarrier/GlobalLossRigidity.lean`:

```text
rate_eq_of_symmetric_active_loss,
rate_eq_of_active_reflTransGen,
connected_active_loss_rigidity.
```

Prompt 3 may use the abstract theorem, but must separately prove that its
spherical `Q=1` hypotheses supply the required local equality formula and
active-edge conditions.

## 3. Permanent regressions Prompt 3 must preserve

### 3.1 Sampling aliases

- tetrahedron: `dim E_form=2`, `dim E_sample=0`;
- octahedron: `dim E_form=3`, `dim E_sample=0`;
- cube: `dim E_form=2`, `dim E_sample=0`.

A form-space dimension is never a sampled-mode dimension without removing the
sampling kernel.

### 3.2 Four-point signed restoration

On the four cardinal points, adjacent rates `1` and antipodal rate `-1/2`
restore one sampled quadratic mode. The negative rate is forced on that fixed
support.

### 3.3 Signed regular pentagon

The exact rates

```text
u=(5+3sqrt(5))/10,
v=(5-3sqrt(5))/10
```

produce

```text
Lx=-x,
Ly=-y,
Lcos(2theta)=-4cos(2theta),
Lsin(2theta)=-4sin(2theta),
E_form=Sym_0(2),
dim E_sample=2,
```

while the real `C_5` action on `Sym_0(2)` is irreducible. Any future
equivariant rigidity statement that omits global nonnegative rates is false.

### 3.4 Boolean centered square

On the four-state coordinate-flip chain,

```text
f=x_1+x_2,
Lf=-2f,
f^2-2=2x_1x_2!=0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

Any future universal centered-square impossibility statement is false.
Centered resonance must not be confused with Jensen equality.

### 3.5 Global compatibility regressions

Retain all Prompt 1 centered sparse local-but-not-global examples and their
exact Farkas certificates. Local rows and centering do not imply arbitrary
sparse shared-edge feasibility.

### 3.6 Unrestricted `Q=1` classifications

Cube and dodecahedron embeddings remain counterexamples to every unrestricted
claim that only tetrahedron, octahedron, and icosahedron can satisfy the local
`Q=1` equality geometry.

## 4. Remaining Prompt 3 targets

Prompt 3 is restricted to these unresolved tasks:

### P3-A. Complete spherical `Q=1` specialization audit

- derive the precise local equality formula from the project's rate-defect
  equality;
- identify active edges and zero-rate/zero-loss degeneracies;
- transfer the abstract connected propagation theorem;
- state exactly where positivity, reversibility, and connectivity enter; and
- verify all normalizations.

### P3-B. Restricted geodesic-triangulation classification

- formulate the nondegenerate geodesic triangulation and convex-embedding
  hypotheses;
- determine whether equal propagated edge loss forces a regular spherical
  triangulation;
- classify only after exhaustive exact counterexample search; and
- preserve cube/dodecahedron and other nontriangulated regressions.

### P3-C. Quantitative near-rigidity

- propagate the local weighted-variance defect across shared active edges;
- track lower conductance, rate, graph-diameter/overlap, and rigidity margins;
- state a sharp or explicitly nonsharp global bound; and
- search for degenerating families before promoting a theorem.

Do not treat these targets as proved at handoff.

## 5. Files Prompt 3 must read first

### Core theorem files

```text
afp_barrier_gate1/pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md
afp_barrier_gate1/pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md
afp_barrier_gate1/AFPBarrier/GlobalLossRigidity.lean
afp_barrier_gate1/AFPBarrier/LossVariance.lean
afp_barrier_gate1/AFPBarrier/LossVarianceSharpness.lean
afp_barrier_gate1/AFPBarrier/QuadraticCovariance.lean
```

### Claim and provenance controls

```text
afp_barrier_gate1/docs/CLAIM_MATRIX.md
afp_barrier_gate1/docs/CONJECTURE_REGISTER.md
afp_barrier_gate1/docs/PURE_MATH_PRIOR_ART_MAP.md
afp_barrier_gate1/docs/THEOREM_TO_FILE_MAP.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_THEOREM_MAP.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_STAGE_REPORT.md
afp_barrier_gate1/docs/PROMPT2_QUADRATIC_COVARIANCE_INTEGRATION_RECORD.md
afp_barrier_gate1/docs/PROMPT2_CLOSEOUT_AUDIT.md
```

### Exact regressions

```text
afp_barrier_gate1/pure_math/falsification/claim_falsification_audit.py
afp_barrier_gate1/pure_math/examples/exact_local_global_audit.py
afp_barrier_gate1/pure_math/tests/test_spherical_feasibility.py
afp_barrier_gate1/pure_math/covariance/quadratic_covariance_audit.py
afp_barrier_gate1/pure_math/covariance/prompt2_closeout_audit.py
```

## 6. Prompt 3 branch rule

After final closeout integration, create the Prompt 3 branch from exactly:

```text
branch=agent/afp-pure-math-p0-m1
commit=PENDING_FINAL_TARGET_COMMIT
tree=PENDING_FINAL_TARGET_TREE
```

Before Prompt 3 edits, verify the target commit and tree, archive SHA, clean
status, and complete diff from the handoff baseline.

## 7. Final verification fields

```text
prompt2_closeout_pr=19
prompt2_implementation_commit=PENDING
prompt2_merge_commit=PENDING
final_target_commit=PENDING
final_target_tree=PENDING
quadratic_workflow_run=PENDING
quadratic_workflow_job=PENDING
spherical_workflow_run=PENDING
spherical_workflow_job=PENDING
pure_math_workflow_run=PENDING
pure_math_workflow_job=PENDING
archive_commit=515f1aae6c20bd85711c90b5c1c21b4905252d01_PENDING_FINAL_RECHECK
pr17_review_thread=PRRT_kwDOQtWJBc6VsMzA_PENDING_RESOLUTION
pr18_review_thread=PRRT_kwDOQtWJBc6VsRku_PENDING_RESOLUTION
```

Until every pending field is replaced, this file does not certify Prompt 3
readiness.
