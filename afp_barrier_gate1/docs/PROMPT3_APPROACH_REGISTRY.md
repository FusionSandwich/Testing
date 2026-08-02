# Prompt 3 approach registry

## Runtime note

A literal multiagent-v2 runtime is not exposed in this environment. It was not
used and is not claimed. The stage instead maintains separate written proof,
formalization, exact-symbolic, prior-art, and adversarial routes whose outputs
must agree before a claim is promoted.

## Approach families

| Route | Independent mechanism | Status | Output or kill criterion |
|---|---|---|---|
| A | Direct weighted Cauchy--Schwarz at each spherical zonal peak | SURVIVED | `Q_i>=1`, with equality iff every active loss is `2/r_i` |
| B | Transfer through the previously formalized abstract connected propagation theorem | SURVIVED / LEAN | one common row rate and one common symmetric active-edge loss |
| C | Equilateral spherical-face Gram matrix and tangent-angle calculation | SURVIVED | `cos(alpha)=c/(1+c)`, `pi/3<alpha<pi`, hence degree `3,4,5` |
| D | Euler/incidence arithmetic plus regular planar-triangulation graph classification | SURVIVED | tetrahedral, octahedral, and icosahedral one-skeleta |
| E | Convex-polyhedron congruence by Cauchy rigidity | SURVIVED under explicit convex-hull hypothesis | upgrades graph and common edge length to geometric Platonic congruence |
| F | Normalized variance `Q-1=sum p(relative loss error)^2` | SURVIVED | multiplicative path, diameter, edge-loss, and row-rate bounds |
| G | Raw gap identity with `r_min` and `a_min` | SURVIVED | additive loss-center, edge-diameter, and row-rate bounds |
| H | Full coordinate-space stability from a rigidity-matrix singular value | CONDITIONAL / NOT PROMOTED | requires an explicit gauge-fixed rigidity margin; no universal margin is asserted |
| I | Unrestricted regular spherical equal-edge classification | REJECTED | cube, dodecahedron, and nontriangulated matchstick graphs violate a Platonic-only claim |
| J | Small variance without an active-weight floor | REJECTED | rare-edge counterfamily has variance tending to zero and an unbounded outlier |
| K | Diameter-free propagation on arbitrary connected supports | REJECTED | local overlap ratios can accumulate along a path |
| L | Individual edge-rate uniformity after geometric classification | REJECTED as a general conclusion | total row rates are fixed, but tangent balance may have nonunique positive coefficients |

## Root synthesis

The surviving theorem chain is deliberately modular:

```text
coordinate eigenmap
  -> first loss moment = 2
  -> local Cauchy equality
  -> active loss = 2 / row rate
  -> symmetric connected propagation
  -> one global active edge metric
  -> equilateral spherical triangulation
  -> degree 3, 4, or 5 by face-angle and Euler arithmetic
  -> tetrahedral, octahedral, or icosahedral graph
  -> convex Cauchy rigidity
  -> regular Platonic embedding.
```

The quantitative chain is separate:

```text
Q_i - 1
  = normalized weighted relative-loss variance
  + active normalized-weight floor
  -> one-edge relative error
  -> shared-edge center comparison
  -> path and diameter propagation.
```

The additive chain replaces the normalized floor by lower bounds on raw active
rates and total row rates.

## Adversarial audit registry

### A1. Cube and dodecahedron

Both shortest-edge graphs have exact coordinate eigenvalue `-2` and `Q=1` at
every vertex. Neither graph is a triangular sphere. They permanently reject
all unrestricted Platonic-only statements.

### A2. Antipodal edges

An active antipodal edge has loss two. Exact local `Q=1` forces row rate one;
connected propagation then makes every active edge antipodal. An injective
connected embedding has at most two vertices, so this case cannot be hidden
inside the triangulation theorem.

### A3. Coincident sampled endpoints

An active zero-loss edge contradicts the strictly positive exact loss
`2/r_i`. The Lean theorem `sphericalQOne_active_zero_loss_impossible` records
this boundary.

### A4. Signed jumps

The variance argument uses nonnegative weighted squares. Prompt 2's signed
regular pentagon remains the exact regression showing that signed rates can
cancel positive square contributions.

### A5. Directed support

Without symmetric activity, a shared edge need not provide the second local
mean needed to compare row rates. Reversibility is sufficient but not
necessary; the exact hypothesis is symmetric activity.

### A6. Rare active edges

For `0<t<=1/2`, the two-point normalized distribution

```text
p_1=t^4,
p_2=1-t^4,
x_1=1+1/t,
x_2=1-t^3/(1-t^4)
```

has mean one and variance `t^2/(1-t^4)`, while `x_1` diverges. A lower active
probability or equivalent structural condition is indispensable.

### A7. Long paths

The one-edge multiplicative interval can saturate at ratio
`kappa=(1+delta)/(1-delta)` on every edge of a path. A graph-diameter factor
cannot be removed from a theorem based only on the local overlap hypotheses.

### A8. Nonconvex or flexible geometry

Equal edge length and triangular combinatorics do not justify geometric
congruence without a convexity/rigidity input. The classification explicitly
assumes a strictly convex simplicial hull and invokes Cauchy rigidity.

### A9. Coordinate-space near-rigidity

Small edge-loss error does not itself provide a coordinate displacement bound
without controlling the inverse of a gauge-fixed rigidity operator. That
stronger conclusion is left conditional rather than inferred from edge
concentration.

## Exact regression files

- `pure_math/rigidity/prompt3_rigidity_audit.py`
- `pure_math/falsification/claim_falsification_audit.py`
- `pure_math/examples/exact_local_global_audit.py`
- `pure_math/tests/test_spherical_feasibility.py`

The Prompt 3 audit uses exact rational and `Q(sqrt(5))` arithmetic. Numerical
ranks or geometric tolerances are not proof evidence.
