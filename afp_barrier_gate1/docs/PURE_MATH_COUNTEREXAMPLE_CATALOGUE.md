# Pure-mathematics counterexample and boundary catalogue

Every rejected formulation below is a permanent regression.  Exact finite
instances delimit hypotheses; they are not substitutes for general proofs.

## C1. Tangent hull outside the origin

**Claim status:** REJECTED — unconditional nonnegative local feasibility.

**Witness status:** PROVED — tangent candidates in one open half-space admit a
strict separating functional and no nonnegative balanced dependence.

**Protected theorem:** feasibility is equivalent to origin membership in the
indexed tangent convex hull.

## C2. Tangent-hull boundary and repeated directions

**Claim status:** REJECTED — hull membership implies positivity on every
permitted edge, or geometric directions alone determine uniqueness.

**Witness status:** PROVED — on a proper relative face, every feasible
dependence vanishes outside the minimal face; repeated indexed directions can
split weight nonuniquely.

**Protected theorem:** strict feasibility uses relative interior, and
uniqueness concerns the indexed normalized-dependence polytope.

## C3. Pure and mixed antipodal support

**Claim status:** REJECTED — assigning a tangent direction by division through
`sin(pi)`.

**Witness status:** PROVED — antipodal-only rows form the simplex of total rate
one; mixed rows allocate the remaining normal budget after a non-antipodal
tangent dependence.

## C4. Sparse local feasibility without global reversibility

**Claim status:** REJECTED — local positive rows plus weighted centering imply
arbitrary sparse shared-edge feasibility.

**Witness status:** PROVED — the centered unequal-mass four-cycle and weighted
cube have exact Farkas certificates excluding the sought conductances.

## C5. Tetrahedral, octahedral, and cubical aliases

**Claim status:** REJECTED — algebraic form dimension equals genuine sampled
quadratic dimension.

**Witness status:** COMPUTATIONAL — exact ranks are respectively
`(dim E_form,dim K_X,dim E_sample)=(2,2,0),(3,3,0),(2,2,0)`.

## C6. Signed restoration boundaries

**Claim status:** REJECTED — positive rigidity remains valid for arbitrary
signed rates.

**Witness status:** PROVED — on four cardinal points, adjacent rate `1` and
antipodal rate `-1/2` restore `X^2-Y^2`; the signed regular pentagon restores
both trace-free quadratic samples despite irreducible conjugation action.

**Finite-data status:** COMPUTATIONAL — exact matrices and minimal signed
rates are independently audited.

## C7. Positive centered Boolean square

**Claim status:** REJECTED — every nonzero centered doubled square is forbidden
for a positive finite generator.

**Witness status:** PROVED — on the four-state coordinate-flip chain,
`f=x_1+x_2` satisfies `Lf=-2f`, `L(f^2-2)=-4(f^2-2)`, and
`Gamma(f,f)=4`.  Its positive semigroup variance also separates resonance from
Jensen equality.

## C8. Literal distinct-degree theorem in dimension one

**Claim status:** REJECTED — pairwise distinct spherical degrees always give
distinct sampled target classes in every dimension.

**Witness status:** PROVED — for `d=1`, the singleton sphere has
`lambda_0=lambda_1=0` and `V_0=V_1`; a degree-zero constant must not be counted
twice.

**Protected theorem:** use pairwise distinct target eigenvalues
`lambda_l=l(l+d-2)`; for `d>=2`, distinct degrees automatically suffice.  The
signed converse is indexed by distinct target classes and includes constants
once.

## C9. Cube and dodecahedron at exact `Q=1`

**Claim status:** REJECTED — exact global equality alone forces one of
`K in {4,6,12}` or a triangular Platonic graph.

**Witness status:** PROVED — shortest-edge cube and dodecahedron embeddings
have connected equal-loss exact rows but are not triangulations.

## C10. Active zero-loss and antipodal edges

**Claim status:** REJECTED — coincident active edges or non-antipodal tangent
normalization are harmless at exact equality.

**Witness status:** PROVED — equality forces active loss `2/r_i>0`; a two-state
antipodal equality chain has `ell=2` and a zero tangent-normalization
denominator.

## C11. Rare-active-edge near-rigidity family

**Claim status:** REJECTED — small weighted loss variance gives uniform
edgewise control without an active-weight floor.

**Witness status:** PROVED — for

```text
p_1=t^4, p_2=1-t^4,
x_1=1+1/t, x_2=1-t^3/(1-t^4),
```

the mean is one and variance tends to zero while `x_1` diverges.

## C12. Long paths and vanishing framework margins

**Claim status:** REJECTED — local near-equality gives diameter-free global
control, or edge-metric concentration alone gives coordinate rigidity.

**Witness status:** PROVED — neighboring intervals can accumulate
multiplicatively along a long path; gauge-fixed rigidity operators can have
vanishing smallest singular value.

## C13. Weighted octahedron covariance boundary

**Claim status:** REJECTED — global `Q=1` forces axial covariance or a nonzero
form kernel gives a nonzero sampled exact space.

**Witness status:** PROVED — the positive reversible weighted-octahedron family
has exact equality with tangent anisotropy, while its off-diagonal form kernel
lies in the sampling kernel and the sampled exact space is zero.

## C14. Unreduced product-grid polar obstruction

**Claim status:** REJECTED — quartic maximum rate is an artifact of a
ring-symmetric conductance choice.

**Witness status:** PROVED — starting with asymmetric rates, the three polar
coordinate equations uniquely force

```text
a_v=1/(2 sin^2 h),
a_+=a_-=1/(4 sin^4 h).
```

With `K=2N^2`, this gives `r_max>=(2/pi^4)K^2`.

## C15. Formal series without analytic control

**Claim status:** REJECTED — symbolic coefficients or fitted slopes establish
a uniform asymptotic theorem.

**Witness status:** PROVED — a formal series contains no tail estimate.

**Protected theorem:** the differentiated cotangent expansion gives a positive
tail and explicit one-sided remainders for every integer `N>=2`.

## C16. Unconstrained extremal degeneration

**Claim status:** REJECTED — an unconstrained infimum over all node sets and
conductances defines the intended extremal invariant.

**Witness status:** PROVED — collapse, dense support, nonlocal edges, vanishing
masses, and unbounded rates evade such a formulation.

**Protected theorem:** the fixed class controls separation, covering, mesh
ratio, degree, locality, masses, reversibility, exact equilibrium, and rate.

## C17. Quasi-uniform loss window as full class membership

**Claim status:** REJECTED — the loss window and `K` comparable to `h^-2`
alone prove membership in the constrained extremal class.

**Witness status:** PROVED — those hypotheses establish compatibility with a
linear rate cap but do not supply the required degree, locality, masses,
reversibility, exact equilibrium, separation, and covering assumptions.

## C18. Quality at arbitrary normal moment

**Claim status:** REJECTED — for arbitrary `lambda>0`, the invariant
`r epsilon/4` always equals `s_2/m^2`.

**Witness status:** PROVED — normalization gives

```text
r epsilon/4=(lambda^2/4) s_2/m^2.
```

**Protected theorem:** use `Q_lambda=r epsilon/lambda^2`; it agrees with the
spherical global `Q` precisely at `lambda=2`.

## C19. Fixed-moment feasible set as a projective cone

**Claim status:** REJECTED — `F_i(lambda)` is a cone modulo positive scaling.

**Witness status:** PROVED — positive scaling changes the fixed normal moment.
The nonzero tangent-balanced cone modulo scaling is bijective with `P_i`, while
each affine slice `F_i(lambda)` itself is bijective with `P_i`.

## C20. Conductance-independent geometry-only quality

**Claim status:** REJECTED — tangent geometry and loss labels determine `Q`
without optimizing feasible weights.

**Witness status:** PROVED — a balanced tangent polytope can contain multiple
probability vectors with different normalized loss variances.

**Protected theorem:** `A_i` is the conductance-aware sliced-LP infimum over the
entire nonempty feasible family.

## C21. Opposite rays force half weights

**Claim status:** REJECTED — two tangent vectors on opposite rays always give
`A=((ell_1-ell_2)/(ell_1+ell_2))^2`.

**Witness status:** PROVED — take a north-pole center and neighbors at
colatitudes `pi/6` on the positive tangent ray and `pi/2` on the negative ray.
The tangent magnitudes are `1/2` and `1`, so balance forces
`p=(2/3,1/3)`.  With `ell_1=1-sqrt(3)/2` and `ell_2=1`,

```text
A=(2+sqrt(3))/4,
```

which differs from the half-weight formula.

**Protected theorem:** if `v_2=-kappa v_1`, then

```text
A=kappa(ell_1-ell_2)^2/(kappa ell_1+ell_2)^2.
```

The requested symmetric identity is the `kappa=1` corollary.

## C22. Empty balanced polytope

**Claim status:** REJECTED — the attainable-mean interval and anisotropy
minimum are defined without a feasibility hypothesis.

**Witness status:** PROVED — if `P_i` is empty, there is no feasible fixed
normal-moment row.  All interval, minimum, and equality statements explicitly
assume `P_i` nonempty.

## C23. Reduced-ring perfect matching

**Claim status:** REJECTED — a varying ring population can use one-to-one
nearest-ring perfect matchings.

**Witness status:** PROVED — biregular incidence gives
`pM_i=qM_{i+1}`; at `p=q=1`, populations are equal.

**Boundary status:** CONJECTURE — useful general split/merge constructions are
left to future numerical analysis; no general impossibility is claimed.

## C24. Delsarte reduction without a new certificate

**Claim status:** REJECTED — reduction to a standard spherical-code LP is a new
Prompt-4 theorem.

**Audit status:** PROVED — no solved candidate dual survived sampling aliases
and component-identifiability checks.  The route is not part of the theorem
package.

## C25. Blanket graph-curvature collapse

**Claim status:** REJECTED — positivity of a finite graph generator rules out
useful positive Bakry--Émery or entropic Ricci curvature.

**Boundary status:** EXTERNAL — established finite graph-curvature frameworks
contain nonnegative and positive examples.  A one-function `Gamma_2` identity
is not a curvature-dimension theorem.

## C26. Continuum transport from positivity alone

**Claim status:** REJECTED — positive rates select ordinary continuum `W_2`
and imply contraction.

**Boundary status:** EXTERNAL — Maas/Erbar-type finite transport theories first
specify a discrete metric and a separate curvature condition.

## C27. Fixed radial connectivity is Delaunay at every level

**Claim status:** REJECTED — the package proves this all-level property.

**Boundary status:** EXTERNAL — positive spherical-Delaunay existence and exact
low modes are used only under the hypotheses of the cited external theory.

## C28. Finite enumeration proves all-order classification

**Claim status:** REJECTED — the source-pinned census through twelve vertices
proves the global triangulation theorem.

**Census status:** COMPUTATIONAL — the exact counts total `9150` and serve only
as hostile finite falsification.  The classification is proved directly.

## C29. Lean arithmetic is the full incidence proof

**Claim status:** REJECTED — the formal declaration alone proves bipartite
handshaking from graph incidence definitions.

**Formal status:** PROVED — Lean checks the arithmetic consequence after the
two edge-count equalities are supplied.  Ordinary finite incidence counting
supplies those equalities.

## Catalogue usage rule

**Policy status:** PROVED — any future theorem that removes a hypothesis must
be checked against every relevant entry.  A stronger theorem may subsume a
witness, but its historical provenance remains recorded.
