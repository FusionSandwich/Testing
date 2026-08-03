# Prompt 1 closeout audit

## 1. Audit baseline and scope

This is an independent closeout audit of the completed Prompt 1 package. It is
not a redevelopment of the stage.

- Repository: `FusionSandwich/Testing`
- Target branch: `agent/afp-pure-math-p0-m1`
- Audited integrated head: `b5f74404729f1a3c0396812539dffccc5ce928c5`
- Starting P0/M1 checkpoint: `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Immutable transport archive:
  `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

No transport, Radiant, HTS, multigroup, spatial-solver, or new theorem scope is
introduced by this closeout. The audit re-derived every stated result, checked
the exact examples and sign conventions, inspected the Lean boundary, and ran
the complete dedicated verification gate against the exact integrated SHA.

A literal multiagent-v2 runtime was not available in this execution
environment. It was therefore not used and is not claimed. Independent proof,
constant, sign, and counterexample audits were carried out as separate audit
passes.

## 2. Executive conclusion

No blocking mathematical or formalization defect was found. Prompt 1 is
closed after the narrow clarifications in Section 4 of this record.

Three mathematical-writing defects and one provenance defect were found:

1. Theorem 1.2 states a bijection, but the written proof explicitly checks only
   that a dependence-generated row maps back to the same dependence. The
   reverse row reconstruction was omitted from the prose.
2. The inverse-quadratic angular-window section uses denominators and monotonic
   lower bounds that require `0 < c1 <= c2`; this standard hypothesis was
   implicit rather than stated at equation (3.5).
3. The weighted residual LP requires `tau_k >= 0` for a genuine weighted
   `l1` objective, and the assertion that zero optimum is equivalent to exact
   feasibility requires `tau_k > 0` for every residual coordinate.
4. The earlier post-integration provenance record described a pull-request
   merge-ref run as if it were an exact checkout of `b5f744...`. It was useful
   merge-compatibility evidence, but not exact-head evidence.

Items 1--3 do not invalidate any intended theorem once their missing
calculation or hypothesis is made explicit. Item 4 does not affect the
mathematics. All four are corrected normatively below and in the integration
record.

## 3. Theorem-by-theorem closeout matrix

| ID | Mandatory theorem or audit item | Verdict | Independent closeout finding |
|---|---|---|---|
| L1 | Non-antipodal nonnegative row iff `0` is in the tangent convex hull | PASS | Normalizing `b_j=a_j sin(theta_j)` gives a convex barycenter; the explicit inverse formula satisfies both tangent and normal equations. |
| L2 | All-index strict positivity iff relative interior | PASS | The supporting-hyperplane proof and the outward-point/averaging construction are valid in the affine span and retain repeated and redundant indices. |
| L3 | Repeated and redundant tangent directions | PASS | The proof is indexed, not set-deduplicated; every index receives a positive coefficient in the relative-interior construction. |
| L4 | Dependence/row bijection and explicit rate formula | PASS after clarification | The omitted reverse calculation is supplied in Section 4.1. The map is genuinely two-sided. |
| L5 | Minimal-face uniqueness criterion | PASS | Every representation is supported in the minimal face; affine dependence gives `lambda +/- t d`, while affine independence gives unique barycentric coordinates. |
| L6 | Unique positive normal scale | PASS | `Q(lambda)>0` and `c Q(lambda)=2` force the unique scale `c=2/Q(lambda)>0`. |
| A1 | Antipodal-only classification | PASS | The normal equation reduces exactly to the nonnegative simplex `sum_p a_p=1`; no tangent direction or sine quotient is assigned. |
| A2 | Mixed antipodal/non-antipodal parameterization | PASS | `D(b)+2t=2` gives `t=1-D(b)/2`; feasibility is exactly tangent balance plus `D(b)<=2` and a simplex split of `t`. |
| A3 | Mixed strict positivity on every permitted edge | PASS | Positive non-antipodal rates are equivalent to relative-interior tangent balance; scaling to `D(b)<2` leaves positive antipodal budget. |
| A4 | Relative-boundary and outside-hull cases | PASS | Boundary dependences are confined to the minimal face; outside the hull every non-antipodal tangent block vanishes and antipodes spend the full budget. |
| Q1 | Relative cone margin `rho` and primal/dual characterization | PASS | Centered inradius equals the minimum support function over unit vectors in the relative span; positivity is equivalent to relative interior. |
| Q2 | Controlled minimum coefficient `delta` | PASS | Averaging the `m` representations obtained from `-rho u_j in P` gives `delta=rho/[m(1+rho)]`, including repeated indices. |
| Q3 | Angular loss, sine, and half-angle bounds | PASS after hypothesis clarification | Constants `kappa0`, `sigma0`, and `beta0` are correct under `0<c1<=c2`, `0<h<=h0`, and `c2 h0<=pi/2`. |
| Q4 | Loss-only outgoing-rate bounds | PASS | From `(min ell)R<=2<=(max ell)R`, the exact and explicit `h^-2` bounds follow with the stated constants. |
| Q5 | Coefficientwise upper and lower bounds | PASS | Upper bounds need only the loss window; the lower bound uses `lambda_j>=delta` and `sin x tan(x/2)=1-cos x`. |
| Q6 | Local balance-system conditioning | PASS | The support margin gives `||U* v||>=rho||v||`; the balancing probability controls the scalar normal block and yields the stated `K_C` and condition-number bounds. |
| Q7 | Tangent-direction perturbation radius | PASS | Support functions give `rho'>=rho-epsilon_u`; the augmented barycentric right inverse yields `K0`, the `delta/(2K0)` radius, and the `l1` coefficient perturbation bound. |
| Q8 | Angle/rate perturbation bound | PASS | Direct subtraction of `2 lambda_j/[sin(theta_j)Q]` gives equation (3.25); every denominator is controlled by `s_- q_-`. |
| Q9 | Actual optimal-value sensitivity | PASS | Convex robustification of a possibly boundary optimizer, followed by right-inverse correction, gives the one-sided bound; reversal gives the symmetric estimate. |
| G1 | Shared-edge cone and feasible-polytope characterization | PASS | `A gamma=b`, `gamma>=0` is exactly cone membership; pairing with the position field gives the coercive conductance identity and compactness after zero columns are removed. |
| G2 | Weighted centering and dense complete-graph construction | PASS | Node summation gives centering as necessary; `gamma_ij=2 w_i w_j/W` satisfies every node equation when centered and is strictly positive. |
| G3 | Full Farkas alternative with AFP signs | PASS | The alternative is `A^T y>=0`, `b^T y<0`; its edge block is `(y_p-y_q).(Omega_q-Omega_p)`, the negative first variation of half squared chord length. |
| G4 | Strict global feasibility iff relative interior of the edge cone | PASS | Positive coefficients on every indexed generator are equivalent to `b in ri K`, including redundant generators; the dual-face condition is equivalent. |
| G5 | Uniform strictness LP | PASS | Substitution `gamma=x+tau 1` gives the dual constraints `A^T y>=0` and `1^T A^T y>=1` with the stated objective sign. |
| G6 | Linear rate/defect LP duality and edge complementary slackness | PASS | The gap is `gamma^T(c-A^T y)`; nonnegative summands give componentwise complementary slackness. |
| G7 | Peak epigraph dual and row/edge slackness | PASS | The dual probability vector satisfies `z>=0`, `1^Tz=1`; its two complementary-slackness blocks and worst-row interpretation have the correct signs. |
| G8 | Weighted residual LP and residual sign interpretation | PASS after hypothesis clarification | The dual box and signs of `r+`/`r-` are correct. Section 4.3 states the required positivity of residual weights. |
| G9 | Sparse-graph node/mass sensitivity | PASS | The residual correction `d=A'^+r`, range condition, singular-value threshold, and explicit node/mass perturbation constants are correct. |
| G10 | Complete-graph mass sensitivity | PASS | The lower conductance and Lipschitz estimates follow from direct numerator/denominator perturbation with `W'>=W-n epsilon_w`. |
| E1 | Weighted cube: locally strict but globally incompatible | PASS | Each row has the unique rate `1`; the cyclic-coordinate dual field has zero work on every cube edge and target work `-4`. |
| E2 | Equal-mass cube strict primal/dual certificate | PASS | `gamma_e=1` gives all node balances; `y_i=-(3/2)Omega_i` gives every dual edge value `2` and primal=dual=`24`. |
| E3 | Centered-clique reconciliation | PASS | Each centered clique satisfies its node equations by the complete-graph formula; summing clique blocks reproduces the prescribed masses and global target. |
| F1 | Lean finite algebra and certificate consequences | PASS | All four stage modules build; the formalized formulas, budget identities, finite loss inequalities, dual work, gap identity, and complementary slackness agree with the ordinary proof. |
| F2 | No placeholders or user axioms in stage modules | PASS | Exact-head workflow source scan passed; no `sorry`, `admit`, `sorryAx`, or user-declared `axiom` occurs in the stage modules. |
| F3 | Independent kernel validation | PASS | Nanoda checked the selected spherical-stage roots and dependencies with `sorryAx` absent from the permitted list. |
| T1 | Exact deterministic examples/regressions | PASS | Rational hull, repeated-point, antipodal, perturbation-boundary, incompatible-cube, and strict-cube regressions passed. |
| R1 | Claim matrix, conjecture register, prior-art map, README, theorem map, and stage report | PASS | The files distinguish proved, external, computational, conjectural, and rejected claims and do not claim the finite-convex or generic LP core as novelty. |
| R2 | Frozen-archive and scope discipline | PASS | The Prompt 1 diff is confined to pure mathematics, proof-control documentation, exact tests, and its workflow; the immutable transport archive is unchanged. |
| V1 | Dedicated workflow on exact integrated head | PASS | Run `30721748746`, job `91426559801`, explicitly checked out and asserted SHA `b5f74404729f1a3c0396812539dffccc5ce928c5`; all verification steps passed. |

No matrix row is `FAIL` after the stated closeout clarifications.

## 4. Normative closeout clarifications

These are corrections to proof completeness and hypotheses, not new theorem
scope.

### 4.1 Reverse half of the row/dependence bijection

Theorem 1.2 already proves that a normalized tangent dependence `lambda`
generates a row and that normalizing the generated tangent weights returns the
same `lambda`. For the converse, start with an arbitrary feasible row and set

```text
b_j = a_j s_j,
B   = sum_j b_j > 0,
lambda_j = b_j/B.
```

Then

```text
Q(lambda)
 = sum_j (b_j/B) ell_j/s_j
 = (1/B) sum_j a_j ell_j
 = 2/B.
```

Reconstructing the row by equation (1.3) gives

```text
2 lambda_j / [s_j Q(lambda)]
 = 2 (b_j/B) / [s_j (2/B)]
 = b_j/s_j
 = a_j.
```

Thus both composites are the identity, and the stated bijection is complete.

### 4.2 Positive constants in the inverse-quadratic angular window

Equations (3.5)--(3.12) are to be read with

```text
0 < c1 <= c2,
0 < h <= h0,
c2 h0 <= pi/2.
```

This makes `theta0=c2 h0>0`, ensures the sinc/tangent constants are defined,
and justifies the monotone lower comparisons with `c1 h`. The later condition
`0<eta<c1` is consistent with this explicit hypothesis.

### 4.3 Residual-weight hypotheses

For equations (4.23)--(4.25), require

```text
tau_k >= 0
```

for every residual coordinate. Negative weights make the primal unbounded by
adding the same positive amount to `r_k+` and `r_k-`.

The further statement

```text
with c=0, optimum=0 iff A gamma=b is exactly feasible
```

requires

```text
tau_k > 0
```

for every coordinate. If a weight is zero, a nonzero residual in that
coordinate is unpenalized, so zero objective need not imply exact feasibility.
The dual box and all complementary-slackness signs remain unchanged.

## 5. Independent constant and sign re-derivation

### 5.1 Margin and minimum coefficient

For `P=conv{u_j}` in its relative span `L`, support-function inclusion gives

```text
rho = min_{||v||=1, v in L} max_j <v,u_j>.
```

For each index `j`, `-rho u_j` lies in `P`, so combining it with `u_j`
gives a zero representation with coefficient at least `rho/(1+rho)` on that
index. Averaging over `m` indices yields

```text
delta = rho/[m(1+rho)].
```

Since unit directions imply `rho<=1`, `delta>=rho/(2m)`.

### 5.2 Angular constants and rates

With `theta0=c2 h0<=pi/2`, concavity of sine gives

```text
sin(theta/2) >= kappa0 theta/2,
kappa0 = sin(theta0/2)/(theta0/2),
```

and hence

```text
ell(theta)=2 sin^2(theta/2)
          >= (kappa0^2/2) theta^2
          >= (kappa0^2 c1^2/2) h^2.
```

The elementary upper bound `1-cos(theta)<=theta^2/2` gives
`ell_j<=c2^2 h^2/2`. Therefore

```text
4/(c2^2 h^2) <= R <= 4/(kappa0^2 c1^2 h^2).
```

For the margin-selected row,

```text
a_j = 2 lambda_j/[s_j Q]
    >= 2 delta/[sin(c2 h) tan(c2 h/2)]
    = 2 delta/[1-cos(c2 h)]
    >= 4 delta/(c2^2 h^2).
```

The coefficient upper bound follows from `a_j ell_j<=2` and the lower loss
bound.

### 5.3 Conditioning

The support formula gives

```text
||U* v||_2 >= rho ||v||.
```

For `C*x=(U x, q.x)` and `C*(v,t)=y`, pairing `y` with any balancing
probability vector gives

```text
|t| <= ||y||_2/q_-.
```

Then

```text
||v|| <= rho^-1 [1+sqrt(m) q_+/q_-] ||y||_2,
```

which yields the stated `K_C`. Since the physical balance matrix is
`B=C diag(s_j)`, its smallest singular value is at least `s_-/K_C`, and its
operator norm is at most its Frobenius norm `sqrt(m) d_+`.

### 5.4 Perturbation and optimum constants

Support functions change by at most `epsilon_u`, so
`rho'>=rho-epsilon_u`. Under `epsilon_u<=rho/2`, the augmented barycentric
adjoint estimate gives

```text
K0 = 1 + 2(1+sqrt(m))/rho.
```

Correcting the old coefficients costs at most `K0 epsilon_u` in `l2`, so
`epsilon_u<=delta/(2K0)` preserves a coefficient floor `delta/2`.

For rates, splitting the difference into coefficient, sine, and `Q` terms and
using

```text
|Q'-Q| <= q_+ Delta_lambda + L_q epsilon_theta
```

gives equation (3.25) exactly. The optimal-value proof does not assume that an
optimizer is strictly positive: it first mixes the optimizer with the
margin-controlled dependence, pays the explicit robustification cost, and
then applies the same right-inverse correction.

### 5.5 Global signs and duality

For edge `e={p,q}`,

```text
(A^T y)_e = (y_p-y_q).(Omega_q-Omega_p).
```

Meanwhile

```text
d/dt [1/2 ||(Omega_q+t y_q)-(Omega_p+t y_p)||^2] at t=0
 = -(A^T y)_e.
```

Thus the Farkas condition `A^T y>=0` means every permitted squared chord is
nonincreasing to first order. The target pairing is

```text
b^T y = -2 sum_i w_i Omega_i.y_i,
```

so `b^T y<0` is positive weighted radial work incompatible with the edge
constraints.

For the cost LP, the exact gap is

```text
c^T gamma-b^T y = gamma^T(c-A^T y),
```

which fixes the complementary-slackness signs. The peak and residual duals
follow from the same Lagrangian calculation; in particular, positive
`r_k+` forces `y_k=-tau_k`, while positive `r_k-` forces `y_k=+tau_k`.

### 5.6 Global sensitivity

Each perturbed edge column changes in two node blocks, each of norm at most
`2 epsilon_Omega`, so

```text
||A'-A||_2 <= ||A'-A||_F <= 2 sqrt(2m) epsilon_Omega.
```

The target perturbation obeys

```text
||b'-b||_2 <= 2 sqrt(n)(epsilon_w+w_max epsilon_Omega).
```

Combining these gives the stated residual bound. The range hypothesis is
necessary and explicitly retained; the pseudoinverse correction is strictly
positive when its `l2` norm is below the original minimum conductance.

## 6. Exact-example audit

### 6.1 Incompatible weighted cube

For cube vertices `x in {+/-1}^3`, scaled by `1/sqrt(3)`, each incident edge
has `Omega_x.Omega_z=1/3`. The three tangent directions at a vertex form the
unique balanced equilateral triple, and the normal equation gives local rate
`a=1`.

With mass `2` at `+++` and `---` and mass `1` elsewhere, antipodal pairing
makes the weighted center zero. Define

```text
y_x=(x_2,x_3,x_1)/sqrt(3).
```

A cube edge changes one coordinate, while the corresponding component of `y`
depends on a different coordinate, so every edge has `(A^T y)_e=0`. The
uniform-mass contribution to `b^T y` cancels, and the two extra endpoint masses
each contribute `-2`, giving

```text
b^T y=-4.
```

Farkas therefore excludes every global shared-edge solution.

### 6.2 Strict equal-mass cube

For unit masses and `gamma_e=1`, the three neighbor differences at each cube
vertex sum to `-2 Omega_i`. With edge cost `c_e=2`, choose
`y_i=-(3/2)Omega_i`. Since every cube edge has squared chord length `4/3`,

```text
(A^T y)_e=(3/2)(4/3)=2=c_e.
```

There are twelve edges, so the primal value is `24`; eight unit nodes each
contribute `3` to `b^T y`, so the dual value is also `24`.

### 6.3 Centered-clique construction

For each centered clique `C_r`, the complete-graph formula gives

```text
gamma_ij^(r)=2 w_i^(r) w_j^(r)/W_r.
```

Its node balance is `-2 w_i^(r) Omega_i`. Summing over cliques gives
`-2 [sum_r w_i^(r)] Omega_i=-2 w_i Omega_i`. Conductances are nonnegative and
strictly positive on every edge covered by a positive clique block.

## 7. Verification record for the audited integrated head

The dedicated workflow was run in a controlled audit PR whose workflow
explicitly checked out the PR head SHA instead of GitHub's synthetic merge
ref. The job asserted equality between expected and actual checkout.

- Exact SHA: `b5f74404729f1a3c0396812539dffccc5ce928c5`
- Workflow: `AFP spherical feasibility`
- Run: `30721748746`
- Job: `91426559801`
- Exact checkout assertion: PASS
- Exact arithmetic regressions: PASS
- Placeholder/user-axiom source scan: PASS
- Lean 4.30.0 / Mathlib 4.30.0 build: PASS (`3095` jobs)
- Independent nanoda validation: PASS
- Nanoda export: `38` selected spherical-stage declarations
- Nanoda result: `13252` declarations checked with no errors

The pre-existing workflow run `30719314077` remains useful as a synthetic
merge-ref compatibility check, but it is not used as exact-head evidence in
this closeout.

## 8. Closeout certification

After applying the narrow clarifications above, every mandatory Prompt 1
requirement passes. No theorem statement, Lean theorem, exact example, or
quantitative constant requires retraction. Prompt 1 is certified closed and
the repository may proceed to Prompt 2.
