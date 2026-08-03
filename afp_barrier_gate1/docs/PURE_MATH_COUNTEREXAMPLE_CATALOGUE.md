# Pure-mathematics counterexample and boundary catalogue

Every item below is a permanent regression against a specific overstatement.
Exact finite examples are not proofs of general theorems; their role is to fix
hypothesis boundaries and falsify future wording.

## C1. Tangent hull outside the origin

**Purpose:** rejects unconditional nonnegative local feasibility.

A finite tangent set contained in one open half-space has no nonnegative
balanced dependence. The supporting functional is an exact separation
certificate.

**Protected claim:** local nonnegative feasibility requires and is equivalent
to `0` belonging to the indexed tangent convex hull.

## C2. Tangent hull boundary

**Purpose:** separates nonnegative feasibility from positivity on every
permitted edge.

When zero lies on a proper relative face, feasible rows exist, but every
balanced dependence vanishes on at least one indexed point outside the minimal
face.

**Protected claim:** all-edge positivity is relative-interior membership, not
mere hull membership.

## C3. Repeated and redundant directions

**Purpose:** rejects uniqueness conclusions based only on geometric direction
values.

Repeated indexed tangent directions can split mass in multiple ways even when
the underlying geometric direction set looks minimal.

**Protected claim:** uniqueness concerns the indexed normalized dependence
polytope.

## C4. Pure and mixed antipodal support

**Purpose:** prevents division by `sin(pi)` and fictitious tangent directions.

Antipodal-only rows form a simplex of total rate one. Mixed rows may use an
arbitrary feasible non-antipodal tangent dependence while spending the
remaining normal budget on antipodes.

**Protected claim:** antipodes require a separate division-free theorem.

## C5. Sparse local feasibility without global reversibility

**Purpose:** rejects the implication

```text
local positive rows + weighted centering => sparse shared-edge solution.
```

Exact centered four-cycle and cube examples have locally feasible rows and an
explicit Farkas dual certificate excluding the desired shared-edge solution.

**Protected claim:** sparse global reversibility is exact cone membership, not
rowwise feasibility.

## C6. Tetrahedral sampling aliases

**Data:** `dim E_form=2`, `dim K_X=2`, `dim E_sample=0`.

**Purpose:** rejects form-space dimension as a sampled-mode count.

The nonzero diagonal trace-free forms vanish at every tetrahedral sample.

## C7. Octahedral sampling aliases

**Data:** `dim E_form=3`, `dim K_X=3`, `dim E_sample=0`.

**Purpose:** same as C6.

The off-diagonal trace-free forms vanish at all six coordinate-axis vertices.

## C8. Cubical sampling aliases

**Data:** `dim E_form=2`, `dim K_X=2`, `dim E_sample=0`.

**Purpose:** same as C6.

Nonzero exact algebraic forms may still represent the zero sampled function.

## C9. Signed four-cardinal-point restoration

At the four cardinal points of `S^1`, adjacent rates `1` and antipodal rate
`-1/2` give coordinate eigenvalue `-1` and restore the sampled mode
`X^2-Y^2` at eigenvalue `-4`.

**Purpose:** shows that the positive obstruction is genuinely a positivity
statement.

**Sharpness:** the negative antipodal rate is forced on the fixed support.

## C10. Signed regular pentagon

Distance-one rate

```text
(5+3sqrt(5))/10 > 0
```

and distance-two rate

```text
(5-3sqrt(5))/10 < 0
```

give coordinate eigenvalue `-1`, both trace-free quadratic samples at
`-4`, and `dim E_sample=2`. The real `C_5` conjugation action on
`Sym_0(2)` is irreducible.

**Purpose:** rejects equivariant rigidity when only one rate is positive and
other rates may be signed.

## C11. Boolean centered square

On the four-state coordinate-flip chain, let `f=x_1+x_2`. Then

```text
Lf=-2f,
f^2-2=2x_1x_2 != 0,
L(f^2-2)=-4(f^2-2),
Gamma(f,f)=4.
```

**Purpose:** rejects universal impossibility of nonzero centered additive
squares.

**Additional warning:** its semigroup variance is positive, so centered
resonance is not Jensen equality.

## C12. Cube and dodecahedron at exact `Q=1`

Both shortest-edge embeddings satisfy exact `Q=1` on connected equal-edge
supports, but their graphs are not triangulations.

**Purpose:** rejects every unrestricted tetrahedron/octahedron/icosahedron
classification.

**Protected claim:** the final classification requires an injective strict
convex minor-geodesic triangulation whose complete one-skeleton is active.

## C13. Active zero-loss edge

An exact positive `Q=1` row cannot place positive rate on a coincident embedded
neighbor, because equality forces active loss `2/r_i>0`.

**Purpose:** prevents hidden noninjective active support.

## C14. Active antipodal edge

An antipodal active edge has loss two and therefore forces row rate one. On a
connected exact-equality support, every active edge would then have loss two.

**Purpose:** records the antipodal boundary of global equality propagation.

## C15. Rare-active-edge near-rigidity family

For `t>0`, let

```text
p_1=t^4,
p_2=1-t^4,
x_1=1+1/t,
x_2=1-t^3/(1-t^4).
```

The weighted mean is one and the variance is `t^2/(1-t^4)`, which tends to
zero, while `x_1` diverges.

**Purpose:** rejects edgewise stability from small weighted variance without a
normalized active-weight floor or equivalent condition.

## C16. Long-path accumulation

Neighboring local mean intervals can overlap while their ratios accumulate
multiplicatively along a path.

**Purpose:** rejects diameter-free global near-rigidity on arbitrary connected
supports.

## C17. Vanishing framework-rigidity margin

Edge-length concentration does not by itself control vertex coordinates modulo
rotations if the gauge-fixed rigidity operator becomes nearly singular.

**Purpose:** blocks universal coordinate-space stability without an explicit
rigidity margin and nonlinear radius.

## C18. Unreduced product-grid polar obstruction

At a polar-ring vertex, the three coordinate equations uniquely force

```text
meridional rate = 1/(2 sin^2 h),
each azimuthal rate = 1/(4 sin^4 h).
```

**Purpose:** rejects the idea that the quartic maximum is merely a bad symmetric
choice of conductances. Asymmetric rates are allowed initially and are forced
to the same solution.

## C19. Product graph versus linear rate cap

With `K=2N^2`, the fixed product graph satisfies

```text
r_max >= (2/pi^4) K^2.
```

**Purpose:** shows that the product family is eventually absent from any
extremal class imposing `r_max<=R K`.

## C20. Conductance reweighting of `Q`

The same tangent directions and losses may support multiple balanced
probability vectors and hence different values of `Q`.

**Purpose:** rejects the claim that `Q` is determined by node geometry alone.

**Replacement theorem:** the a priori geometry/cone invariant is the sliced-LP
constant

```text
A_i=inf_{a in F_i}(Q_i(a)-1).
```

## C21. Two-loss anisotropy sharpness

For two opposite tangent directions with forced equal projective weights,

```text
A=((ell_1-ell_2)/(ell_1+ell_2))^2.
```

**Purpose:** supplies an equality example for the cone anisotropy theorem.

## C22. Reduced-ring perfect-matching obstruction

For a biregular bipartite coupling between rings,

```text
p M_i=q M_j.
```

A one-to-one coupling has `p=q=1` and forces `M_i=M_j`.

**Purpose:** rejects a varying population rule `M_i comparable to N sin(theta_i)`
inside the nearest-ring perfect-matching class.

**Boundary:** it does not reject more general split/merge coupling graphs.

## C23. Delsarte reduction without a new certificate

A spherical-code LP formulation that does not identify sampled components or
supply a solved new dual certificate is not a Prompt 4 theorem.

**Purpose:** prevents standard LP machinery from being reported as a new
barrier.

## C24. Positive-curvature finite graphs

Known finite graphs can have useful positive Bakry--Émery or entropic Ricci
curvature properties.

**Purpose:** permanently rejects a blanket finite-positive-graph curvature
collapse statement.

## C25. Continuum transport claim from positivity alone

Positivity of jump rates does not select the ordinary continuum `W_2` metric.

**Purpose:** rejects entropy-gradient-flow or contraction claims without a
specified Maas/Erbar-type discrete metric and curvature theorem.

## C26. Formal series without analytic control

A computer algebra series can reproduce coefficients while saying nothing
about a uniform remainder.

**Purpose:** protects the distinction between the exact `N>=2` asymptotic
theorem and finite/formal regression output.

## C27. Fixed radial connectivity claimed Delaunay at every level

No such all-level result is established in the package.

**Purpose:** prevents transfer of external spherical-Delaunay positivity to an
unverified fixed connectivity family.

## Catalogue usage rule

Any future theorem that removes a hypothesis must be tested against every
relevant catalogue entry. A computational example may be retired only when a
stronger exact proof subsumes its falsification role; its historical record
should remain in provenance.

## Rich Prompt 3 reconciliation counterexamples

| Rejected strengthening | Exact witness | Permanent lesson |
|---|---|---|
| unrestricted Platonic `Q=1` classification | cube and dodecahedron shortest-edge generators | triangulation support is essential |
| tangent normalization at `ell=2` | two-state `+/-e_1` generator with `r=1`, `Q=1` | covariance is `4e_1e_1^T`, with no unit tangent frame |
| `Q=1` forces axial covariance | positive three-parameter weighted octahedron | tangent second moment is independent data |
| scalar `eta` controls tangent anisotropy | let one weighted-octahedron conductance ratio tend to infinity at `eta=0` | anisotropy norm tends to `1/2` |
| form constraints determine sampled modes | octahedral off-diagonal quadratic aliases | use the sampling map |
| small defect controls every active edge without a floor | rare-active-edge probability family | require `p_ij>=kappa` or equivalent structure |
| diameter-free global control | long alternating paths | local ratio errors accumulate |
| endpoint `C_A<1` certifies every required angle box | prescribed fixed icosahedral neighborhood | use the positive Gram/Heron determinant |
| finite census is an all-orders proof | plantri through twelve vertices | enumeration is falsification only |
| inactive triangulation edges inherit equality | cube faces triangulated by zero-conductance diagonals | equality controls active support only |
