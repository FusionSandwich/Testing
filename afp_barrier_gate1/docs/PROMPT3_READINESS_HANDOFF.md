# Prompt 3 readiness handoff

## 1. Frozen accepted mathematical baseline

```text
repository=FusionSandwich/Testing
target_branch=agent/afp-pure-math-p0-m1
prompt1_baseline=923dc47dae4f83dbea9cd56aa904164c6378e52d
prompt2_closeout_pr=19
prompt2_implementation_commit=afb31139cacdf1bf252e86e890c4792a03df4796
prompt2_implementation_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
prompt2_merge_commit=dbe5d5db315d4e99b75c775c269827ac906b4fad
prompt2_merge_tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
immutable_archive=515f1aae6c20bd85711c90b5c1c21b4905252d01
reported_694b913_resolves=no
```

The previously reported
`694b913c99364bb0032a8ffbd7008b549b491af0` is not a remote commit and must
never be used as a Prompt 3 baseline.

A documentation-only PR #20 is integrated by non-forced fast-forward after all
three workflows pass its literal head. That exact final target SHA/tree and
its workflow run/job identifiers are recorded in the immutable PR #20 and PR
#19 discussions and repeated in the final return. A Git commit cannot contain
its own SHA/tree without a self-referential hash fixed point; the committed
handoff therefore records the accepted mathematical merge above and uses the
PR discussion as the exact final metadata pointer.

Prompt 3 must branch from the exact final target ref reported in that
acceptance record. Its tree contains the mathematical baseline shown above plus
only this documentation closeout.

## 2. Prompt 1 accepted dependencies

Prompt 3 may use the corrected Prompt 1 package rooted at
`923dc47dae4f83dbea9cd56aa904164c6378e52d`:

- indexed local convex-hull and relative-interior feasibility;
- exact positive scaling and row-rate formulas;
- repeated, redundant, and lower-dimensional tangent configurations;
- division-free pure and mixed antipodal classifications;
- explicit coefficient, rate, singular-value, conditioning, and perturbation
  bounds;
- global shared-edge cone, Farkas, LP, and complementary-slackness theory;
- complete-graph, equivariant-averaging, and centered-clique reconciliation;
- exact centered sparse local-but-not-global counterexamples; and
- compatible global perturbation bounds under the stated range/rigidity
  hypotheses.

Prompt 3 must not re-prove these results or weaken their hypotheses silently.

## 3. Prompt 2 accepted dependencies

### 3.1 Covariance and genuine sampling

For a finite coordinate eigenmap,

```text
L(Phi^T A Phi)
 =-2lambda Phi^T A Phi+tr(A^T C_i).
```

For the spherical degree-two specialization,

```text
R_X=(L+2dI)S_X,
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2dI),
dim E_sample=rank(S_X)-rank(R_X).
```

Form-space dimension is never a sampled-mode count without quotienting the
sampling kernel.

### 3.2 Positive axial rigidity

Positive axial covariance at every state gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension. The explicit inverse
sampling formula and coordinate eigenvalue are exact.

### 3.3 Corrected equivariant rigidity

The equivariant theorem is usable only with all of these hypotheses:

```text
finite transitive G-action on I;
rho:G->O(d);
Phi_i in S^(d-1);
Phi_{gi}=rho(g)Phi_i;
a_{gi,gj}=a_ij;
a_ij>=0 for every i!=j;
conservative diagonal L_ii=-sum_{j!=i}a_ij;
L Phi=-(d-1)Phi;
real conjugation action on Sym_0(d) irreducible;
at least one positive jump joins distinct embedded points.
```

Then

```text
E_form={0}.
```

Reversibility is not required. The positive distinct-jump hypothesis is used
only after global off-diagonal nonnegativity has made the radial covariance a
sum of nonnegative squares.

### 3.4 Centered and uncentered products

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

The uncentered `c=0` case forces zero carré du champ. On an irreducible
positive chain and `lambda>0`, the uncentered resonant eigenfunction is zero.
A centered resonant square may be nonzero.

### 3.5 Semigroup and Jensen distinction

Centered square resonance is equivalent, under finite-dimensional matrix
semigroup differentiability, to

```text
P_t(f^2)-(P_t f)^2=c(1-exp(-2lambda t)).
```

Jensen equality is the separate zero-variance condition that `f` is constant
on positive transition support. Centered resonance and Jensen equality must
never be conflated.

### 3.6 Spherical eigenvalue shift

On `S^(d-1)`:

```text
coordinate eigenvalue=d-1,
doubled coordinate eigenvalue=2(d-1),
degree-two spherical eigenvalue=2d.
```

The covariance problem has shift `2`; it is not additive coordinate-square
resonance.

### 3.7 Abstract equality propagation

The following are already `PROVED / LEAN` in
`AFPBarrier/GlobalLossRigidity.lean`:

```text
rate_eq_of_symmetric_active_loss,
rate_eq_of_active_reflTransGen,
connected_active_loss_rigidity.
```

They establish equal rate and equal active-edge loss on a connected symmetric
active graph under the local equality formula. Prompt 3 must still prove that
the final spherical `Q=1` hypotheses supply every premise.

## 4. Permanent regressions Prompt 3 must preserve

### 4.1 Sampling aliases

```text
tetrahedron: dim E_form=2, dim E_sample=0
octahedron:  dim E_form=3, dim E_sample=0
cube:        dim E_form=2, dim E_sample=0
```

### 4.2 Four-cardinal-point signed restoration

Adjacent rates `1` and antipodal rate `-1/2` restore one sampled quadratic
mode; the negative antipodal rate is forced on that fixed support.

### 4.3 Signed regular pentagon

For

```text
u=(5+3sqrt(5))/10>0,
v=(5-3sqrt(5))/10<0,
```

on distance-one and distance-two neighbors,

```text
Lx=-x,
Ly=-y,
Lcos(2theta)=-4cos(2theta),
Lsin(2theta)=-4sin(2theta),
E_form=Sym_0(2),
dim E_sample=2.
```

The real `C_5` action on `Sym_0(2)` is irreducible. Any future equivariant
rigidity statement that omits global nonnegative rates is false.

### 4.4 Boolean centered square

On the four-state coordinate-flip chain,

```text
f=x_1+x_2,
Lf=-2f,
f^2-2=2x_1x_2!=0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4,
P_t(f^2)-(P_t f)^2=2(1-exp(-4t))>0 for t>0.
```

Any universal centered-square impossibility statement is false. This is not a
Jensen equality case.

### 4.5 Prompt 1 global compatibility regressions

Retain all centered sparse local-but-not-global examples and exact Farkas
certificates. Local positive rows plus weighted centering do not imply
arbitrary sparse shared-edge feasibility.

### 4.6 Unrestricted `Q=1` classifications

Cube and dodecahedron embeddings defeat every unrestricted claim that only
tetrahedron, octahedron, and icosahedron can realize the local equality
geometry.

### 4.7 Low-degree product table

For `S^2`, the exact pointwise multiplication rows are:

```text
ell=1: degrees 0,2;             eigenvalues 0,6;                    target 4
ell=2: degrees 0,2,4;           eigenvalues 0,6,20;                 target 12
ell=3: degrees 0,2,4,6;         eigenvalues 0,6,20,42;              target 24
ell=4: degrees 0,2,4,6,8;       eigenvalues 0,6,20,42,72;           target 40
ell=5: degrees 0,2,4,6,8,10;    eigenvalues 0,6,20,42,72,110;       target 60
ell=6: degrees 0,2,4,6,8,10,12; eigenvalues 0,6,20,42,72,110,156;   target 84
```

There is no additive resonance in these rows. Higher-dimensional Pell
resonances alone do not identify sampled components or yield a hierarchy.

## 5. Remaining Prompt 3 targets

### P3-A. Complete spherical `Q=1` specialization audit

- derive the exact local equality formula from the project's rate-defect
  equality;
- identify active edges and every zero-rate/zero-loss degeneracy;
- transfer the abstract connected propagation theorem;
- state exactly where positivity, reversibility, connectivity, and embedding
  hypotheses enter; and
- verify all normalization conventions.

### P3-B. Restricted geodesic-triangulation classification

- formulate nondegenerate geodesic-triangulation and convex-embedding
  hypotheses;
- determine whether propagated equal edge loss forces a regular spherical
  triangulation;
- run exhaustive exact counterexample searches before promotion; and
- preserve cube/dodecahedron and nontriangulated regressions.

### P3-C. Quantitative near-rigidity

- propagate the local weighted-variance defect across shared active edges;
- track minimum conductance, row-rate, graph-diameter/overlap, and rigidity
  margins;
- state explicit constants; and
- search for degenerating counterfamilies before promotion.

No graph enumeration, classification, or stability proof was begun during the
Prompt 2 closeout.

## 6. Files Prompt 3 must read first

### Core proof/formalization

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

## 7. Verification provenance

Accepted literal implementation-head workflows:

```text
AFP quadratic covariance: run 30734370610, job 91460293629
AFP spherical feasibility: run 30734370649, job 91460293565
AFP Pure Mathematics:      run 30734370607, job 91460293589
```

Accepted post-merge repository-wide workflow:

```text
commit=dbe5d5db315d4e99b75c775c269827ac906b4fad
tree=2414b6048e3c0d090152b7873b8ee52b5e40ea3c
run=30734539844
job=91460829310
```

Final literal metadata-head runs for all three workflows, the final target
commit/tree, and the two resolved legacy review-thread IDs are recorded in the
PR #20 acceptance comment, the merged PR #19 discussion, and the final
response.

## 8. Prompt 3 branch rule

Before Prompt 3 edits:

1. read the final PR #20 acceptance record;
2. verify `agent/afp-pure-math-p0-m1` equals the exact recorded final SHA;
3. verify its tree equals the recorded final tree;
4. verify the archive still equals `515f1aae...`;
5. verify a clean worktree and the complete diff from that baseline; and
6. create a new Prompt 3 branch without rewriting the target.

The final metadata commit is documentation-only; its parent mathematical
baseline is `dbe5d5db...`, tree `2414b604...`.
