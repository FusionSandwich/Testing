# AFP pure-math conjecture register

Every unresolved conjecture requires a precise hypothesis set, deterministic
falsification search, literature status, and kill criterion. Resolved,
blocked, deferred, and rejected entries remain here as permanent regression
controls.

## C-M1. Strict local spherical feasibility — resolved

**Status:** PROVED.

The corrected Prompt 1 package proves indexed convex-hull/relative-interior
feasibility, exact scaling and uniqueness, division-free antipodal handling,
quantitative margins, conditioning, and transported-span perturbation
stability. Repetitions, redundancies, and lower-dimensional spans are included.

## C-M1G. Local-to-global reversible compatibility — resolved negatively and conditionally

The unrestricted implication is REJECTED by exact centered sparse examples.
Complete-graph sufficiency, equivariant orbit averaging, centered-clique
submass decomposition, and the full shared-edge cone/Farkas test are PROVED
replacement mechanisms.

## C-M2A. Abstract global equality propagation — resolved

**Proved statement.** Under a positive common eigenvalue, positive row rates,
a symmetric active relation, a symmetric edge loss, the local equality formula

```text
loss(i,j)=lambda/rate(i)
```

on every active edge, and connectedness of the active relation, all row rates
are equal and all active-edge losses have one common value.

**Status:** PROVED / LEAN in `AFPBarrier/GlobalLossRigidity.lean` through:

```text
rate_eq_of_symmetric_active_loss,
rate_eq_of_active_reflTransGen,
connected_active_loss_rigidity.
```

This abstract propagation theorem is no longer a conjecture.

## C-M2B. Complete spherical `Q=1` specialization — resolved

Let

```text
g_i(j)=Omega_i dot Omega_j,
ell_ij=1-g_i(j),
r_i=sum_j a_ij,
D_i=sum_j a_ij ell_ij^2,
Q_i=r_i D_i/4,
```

and assume the unit-sphere coordinate eigenmap equation

```text
sum_j a_ij(Omega_j-Omega_i)=-2 Omega_i
```

with nonnegative off-diagonal rates. Then `Q_i>=1`, and

```text
Q_i=1
iff
ell_ij=2/r_i on every active edge from i.
```

With symmetric connected activity, all row rates and all active-edge losses
are globally equal. Active zero-loss edges are impossible, and an active
antipodal edge forces row rate one.

**Status:** PROVED / LEAN in `AFPBarrier/SphericalQOneRigidity.lean`.

## C-M3. Restricted geodesic-triangulation classification — resolved under explicit hypotheses

**Proved statement.** Suppose the symmetric active graph is exactly the
one-skeleton of an injective strict convex minor-geodesic triangulation of
`S^2`, every triangulation edge is active, the coordinate eigenmap equation
holds, and `Q_i=1` at every vertex. Then, up to an orthogonal transformation,
the embedding is a regular tetrahedron, octahedron, or icosahedron.

The proof establishes one common active dot product, equilateral spherical
faces, degree `q in {3,4,5}`, the exact Euler count triples, the tetrahedral,
octahedral, and icosahedral graph lemmas, and convex Cauchy congruence. The
five-regular graph step has a direct finite link-expansion proof in
`pure_math/rigidity/ICOSAHEDRAL_GRAPH_LEMMA.md`.

**Status:** PROVED / ORDINARY MATHEMATICS, with the finite algebra and local/global
propagation formalized in Lean.

**Permanent warning:** cube and dodecahedron shortest-edge generators satisfy
`Q=1` but are not triangular spheres. Every unrestricted Platonic-only claim
remains REJECTED.

**Additional boundary:** the classification fixes the embedded geometry and
the common total row rate, not every individual active rate.

## C-M4. Quantitative active-edge and row-rate near-rigidity — resolved

The exact normalized identity is

```text
Q_i-1=sum_j p_ij(ell_ij/m_i-1)^2,
p_ij=a_ij/r_i,
m_i=lambda/r_i.
```

If `Q_i<=1+epsilon`, every active normalized weight is at least `p_*>0`, the
active graph is symmetric and connected, and

```text
delta=sqrt(epsilon/p_*)<1,
kappa=(1+delta)/(1-delta),
```

then every active edge has relative loss error at most `delta`, neighboring
centers and row rates differ by at most a factor `kappa`, and paths/diameter
give the explicit powers recorded in Prompt 3 Theorem 4.1.

An additive version follows from

```text
r_i D_i-lambda^2<=eta,
r_i>=r_min>0,
a_ij>=a_min>0,
Delta=sqrt(eta/(r_min a_min)),
```

with exact edge, path, diameter, and row-rate constants.

**Status:** PROVED. The per-edge raw-gap estimate and shared-edge comparison
lemmas are Lean-checked; path and diameter arguments are ordinary finite graph
induction.

**Permanent necessity regression.** The exact rare-edge family

```text
p_1=t^4,
p_2=1-t^4,
x_1=1+1/t,
x_2=1-t^3/(1-t^4)
```

has mean one and variance `t^2/(1-t^4)` tending to zero while `x_1` diverges.
Small equality defect without an active-weight floor does not control every
active edge.

## C-M4G. Coordinate-space quantitative rigidity — conditional, not promoted

Edge-metric concentration alone does not provide a coordinate displacement
bound modulo rotations. Such a theorem requires a gauge-fixed rigidity matrix
or equivalent framework map with an explicit positive smallest singular
value, plus a nonlinear remainder radius.

**Status:** CONDITIONAL / UNRESOLVED AS A UNIFORM THEOREM.

**Kill criterion for any future universal version:** a sequence of admissible
frameworks with the rigidity margin tending to zero while the Prompt 3 edge
metric hypotheses remain bounded.

## C-M5. Genuine sampled quadratic exactness — resolved after corrective audit

The covariance package proves

```text
R_X=(L+2d I)S_X,
K_X=ker S_X subset E_form=ker R_X,
E_sample=im(S_X) intersect ker(L+2d I),
dim E_sample=rank(S_X)-rank(R_X).
```

Positive axial covariance at every vertex gives

```text
E_form=K_X,
E_sample={0}.
```

Regular simplices attain this theorem in every dimension, and the five
Platonic examples are classified exactly.

The independent equivariant route is now correctly stated only under

```text
a_ij>=0 for every i!=j.
```

Together with transitivity, an equivariant unit-sphere coordinate eigenmap,
irreducibility of the real conjugation representation on `Sym_0(d)`, and one
positive distinct jump, this gives `E_form={0}`. Reversibility is not used.

**Permanent signed regression.** On the regular pentagon, distance-one rate

```text
(5+3sqrt(5))/10
```

and distance-two rate

```text
(5-3sqrt(5))/10
```

produce coordinate eigenvalue `-1`, full trace-free quadratic eigenvalue
`-4`, `E_form=Sym_0(2)`, and `dim E_sample=2`, while the real `C_5`
conjugation action is irreducible. Therefore the equivariant theorem without
global nonnegativity is REJECTED.

**Status:** PROVED AFTER CORRECTIVE AUDIT.

## C-M6. Centered spectral products — resolved locally, hierarchy rejected

For

```text
Gamma(f,g)=1/2 sum_j a_ij(f_j-f_i)(g_j-g_i),
Lf=-lambda f,
Lg=-nu g,
```

the exact shifted residual is

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

**Resolved conclusions:**

- uncentered resonance (`c=0`) forces zero carré du champ;
- on an irreducible positive chain with `lambda>0`, the uncentered resonant
  eigenfunction is zero;
- centered resonance may be nonzero;
- centered resonance gives semigroup variance
  `c(1-exp(-2lambda t))`, not Jensen equality.

**Permanent positive regression.** On the four-state Boolean square with rate
one coordinate flips and `f=x_1+x_2`,

```text
Lf=-2f,
f^2-2=2x_1x_2 != 0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

Thus universal centered-square impossibility is REJECTED.

The exact `S^2` table for `ell=1,...,6` has no additive resonance, while the
general higher-dimensional resonance equation remains Pell-type. After
sampling kernels, cross-degree aliases, equality sets, and component
identifiability are enforced, no `ell`-indexed sampled dimension tradeoff,
multiplicity obstruction, or new global consequence survives.

**Hierarchy status:** REJECTED FOR PROMPT 2 under that kill criterion. The
rejection does not rely on a centered-square impossibility theorem and does
not rule out future theorems under stronger association-scheme or design
hypotheses.

## C-M7. Exact square-product polar asymptotics — resolved

For the square equal-angle product family `M=2N`, the exact polar rate and
quality satisfy, for every integer `N>=2`,

```text
0 <= r_polar
     - [(8/pi^4)N^4 + (10/(3pi^2))N^2 + 13/45]
  <= pi^2/(48N^2),
```

and

```text
0 <= Q_pole - [N^2/pi^2 + 7/12]
  <= pi^2/(12N^2).
```

The proof uses a positive differentiated cotangent Mittag--Leffler tail. The
formal SymPy series is only an independent coefficient regression.

**Status:** PROVED / ORDINARY ANALYSIS, with coefficient extraction Lean-checked.

## C-M8. Fixed unreduced product-graph lower bound — resolved sharply

At every polar-ring vertex, the three coordinate balance equations force

```text
inward meridional rate = 1/(2 sin^2 h),
each azimuthal rate   = 1/(4 sin^4 h).
```

The proof begins with distinct left and right azimuthal rates; their equality is
derived from the transverse coordinate equation. It assumes neither equal
masses nor ring-symmetric conductances.

The existing positive reversible construction attains the forced row and has
its maximum at the poles. Therefore the exact graph-class minimax value is

```text
1/(2 sin^2(pi/(2N))) + 1/(2 sin^4(pi/(2N))),
```

with sharp leading constant `8/pi^4`.

**Status:** PROVED / SHARP / LEAN FINITE CORE.

**Rejected wording:** the quartic obstruction is merely an artifact of a bad
symmetric conductance choice.

## C-M9. Universal rate barrier and quasi-uniform transfer — resolved

Degree-one exactness gives

```text
4 <= r_i epsilon_i.
```

Hence

```text
epsilon_i<=C h^2 => r_i>=4/(C h^2).
```

A loss window

```text
(2/pi^2)h^2 <= ell_ij <= 2h^2
```

transfers to

```text
1 <= h^2 r_i <= pi^2,
(4/pi^2)h^2 <= epsilon_i <= 4h^2.
```

**Status:** PROVED / LEAN CONDITIONAL TRANSFER.

Positive spherical-Delaunay existence and exact coordinate modes are EXTERNAL
unless verified for the actual geometry. The claim that a fixed radial
connectivity is Delaunay at every level is REJECTED AS UNSUPPORTED.

## C-M10. Constrained extremal theory — resolved at the mandatory level

The final extremal class controls:

```text
rate,
degree,
edge locality,
separation,
covering radius and mesh ratio,
mass bounds,
positivity,
reversibility,
degree-one exactness.
```

For every nonempty finite class,

```text
E_K>=4/(RK),
```

and

```text
C*=liminf K E_K >= 4/R.
```

Every nonempty fixed-`K` closed class has a minimizer. The square product
family has quadratic stiffness in node count and is eventually excluded from
every linear-rate class.

**Status:** PROVED. The lower bound is Lean-checked; compactness is ordinary
finite-dimensional analysis.

## C-M11. A priori feasible-cone anisotropy — resolved

For a nonempty tangent-balanced projective polytope,

```text
Q=s_2(p)/m(p)^2.
```

At fixed mean loss `m`, the minimum second moment is the finite LP

```text
Psi(m)=min sum p_j ell_j^2
```

subject to normalization, tangent balance, and mean loss. The best cone bound
is

```text
A_i=min_m [Psi(m)/m^2-1]
   =inf_{a in F_i}(Q_i(a)-1).
```

The exact dual is

```text
maximize alpha+beta m
subject to
alpha+beta ell_j+z dot v_j <= ell_j^2.
```

**Status:** PROVED USING STANDARD FINITE LP DUALITY.

**Equality:** `A_i=0` exactly when a tangent-balanced projective row is
supported on one loss level.

**Sharp example:** for two opposite tangent directions,

```text
A=((ell_1-ell_2)/(ell_1+ell_2))^2.
```

**Rejected wording:** `Q` is determined by node geometry alone, without
conductance optimization.

## C-M12. Reduced-ring nearest-ring perfect matching — resolved negatively for the stated class

A biregular adjacent-ring coupling satisfies

```text
p M_i=q M_j.
```

A one-to-one coupling has `p=q=1` and therefore requires `M_i=M_j`. Thus a
varying population rule `M_i comparable to N sin(theta_i)` cannot use
nearest-ring perfect matchings.

**Status:** PROVED / LEAN FOR THE STATED COUPLING CLASS.

General split/merge couplings remain outside this theorem and are numerical-
analysis work.

## C-M13. Delsarte/Gegenbauer sampled barrier — blocked

The branch reduced candidate bounds to standard spherical-code LPs but produced
no new dual certificate that survived sampling kernels, cross-degree aliases,
and finite component identifiability.

**Status:** BLOCKED FOR PROMPT 4.

**Promotion criterion:** a solved explicit dual certificate yielding a new
global sampled residual, valence, or efficiency theorem.

## C-M14. Bakry--Émery curvature branch — killed for Prompt 4

For an eigenfunction,

```text
Gamma_2(f)=1/2 L Gamma(f,f)+lambda Gamma(f,f).
```

At centered square resonance, this gives a constant one-function value. It does
not establish a curvature-dimension inequality on the full function algebra.

**Status:** KILLED UNDER THE STATED KILL CRITERION.

The blanket claim that finite positive graphs cannot have useful positive
Bakry--Émery curvature remains REJECTED.

## C-M15. Compact homogeneous-space extension — deferred

The Euclidean covariance identity is dimension-independent, but no additional
compact homogeneous space materially strengthened the central theorem without
substantial new representation-theoretic input.

**Status:** DEFERRED.

## C-M16. Discrete transport-metric branch — deferred

Positivity does not select the continuum `W_2` geometry. Entropy-gradient-flow
or contraction statements require a specified Maas/Erbar-type discrete metric
and a separate curvature theorem.

**Status:** DEFERRED.

## C-M17. Final publication synthesis — accepted

The central theorem is the sampled quadratic residual factorization and
structural rigidity package, not the product-grid asymptotic result. The local
feasibility, global shared-edge compatibility, exact/quantitative equality
rigidity, sharp graph barrier, constrained extremal theory, and cone anisotropy
form the supporting hierarchy.

**Status:** ACCEPTED THEOREM PACKAGE, subject to final branch integration and
workflow provenance.

The central theorem survives the publication kill criterion: it is more than
ambient dimension minus constraint rank because the residual factors through
the actual sampling map, forces automatic kernel inclusion, and combines with
positive structural hypotheses to yield sharp rigidity and exact alias/signed
boundary classifications.

## Verification-policy correction — resolved

The dedicated workflows scan the aggregate pure-math Lean source for

```text
sorry
admit
sorryAx
axiom
axioms
```

using token-aware and anchored declaration regexes, keep `sorryAx` outside the
nanoda allowed list, run focused axiom reports, assert literal checkout heads,
and independently check accepted declaration sets.

## Rejected statements retained as regression warnings

- local positive rows plus centering imply arbitrary sparse shared-edge
  feasibility;
- unrestricted `Q=1` classification by `K in {4,6,12}`;
- unrestricted Platonic-only classification from equal active edge length;
- individual active edge-rate equality from common edge metric and common row
  rate;
- uniform edgewise near-rigidity without an active-weight/rate floor;
- diameter-free global stability on arbitrary connected supports;
- coordinate-space stability without a framework-rigidity margin;
- algebraic form dimension equals genuine sampled exact dimension;
- equivariant irreducibility needs only one positive rate while other rates may
  be signed;
- every nonzero centered additive square is impossible;
- centered resonance is Jensen equality;
- a Pell arithmetic resonance alone produces a spectral-product hierarchy;
- product-grid quartic stiffness is only a symmetric-conductance artifact;
- formal series or fitted slopes prove all-order asymptotics;
- an unconstrained defect infimum is a meaningful extremal invariant;
- `Q` is geometry-only and independent of feasible rate weights;
- varying reduced-ring populations admit nearest-ring perfect matchings;
- a standard Delsarte LP reduction is a new theorem without a solved dual;
- a one-function `Gamma_2` identity is a full curvature theorem;
- blanket finite-graph Bakry--Émery curvature collapse;
- continuum `W_2` contraction from positivity alone;
- fixed radial connectivity is Delaunay at every level; and
- general order independence of layered stopping maps.
