# P1E symmetry, association-scheme, cover, and latitude routes

This note records four independent construction routes which look capable of
producing arbitrarily large exact equality graphs, and gives the precise
reason that none of the four by itself produces a quasiuniform refinement of
the whole sphere in fixed ambient dimension.  The conclusions are negative
route certificates, not a substitute for the positive P1E construction.

Throughout, `n=d-1`, spherical distance is denoted by `dist`, the separation
`q(X)` is the minimum distance between two distinct nodes, and the fill
distance of a finite set `X` in `S^n` is

```text
h(X)=sup_{y in S^n} min_{x in X} dist(x,y).
```

## 1. A cardinality floor for every refining family

### Lemma 1.1 (covering floor)

If `X subset S^n` is finite and `0<h=h(X)<=1`, then

```text
|X| >= c_n h^{-n},
c_n = n |S^n| / |S^{n-1}|.
```

Indeed, the caps of radius `h` centred at `X` cover `S^n`.  The area of one
such cap is

```text
|S^{n-1}| integral_0^h sin(t)^{n-1} dt
    <= |S^{n-1}| h^n/n.
```

Comparison of areas proves the claim.  In particular, a genuine fixed-
dimension refinement has unbounded cardinality.

## 2. Fixed-class association schemes cannot refine

### Lemma 2.1 (elementary spherical few-distance bound)

Suppose that the off-diagonal inner products of
`X={x_1,...,x_N} subset S^{d-1}` belong to a set
`A={alpha_1,...,alpha_s}`.  Then

```text
N <= Q(d,s)
   := binom(d+s-1,s) + binom(d+s-2,s-1).
```

For each `i`, put

```text
p_i(x) = product_{alpha in A} (x_i dot x-alpha)/(1-alpha).
```

The restrictions of the `p_i` to the sphere are linearly independent,
because `p_i(x_j)=delta_ij`.  They lie in the restrictions of polynomials of
degree at most `s`.  Modulo the relation `|x|^2=1`, that space has dimension

```text
binom(d+s-1,s) + binom(d+s-2,s-1),
```

which proves the bound without a rank threshold or an external
classification theorem.

### Corollary 2.2 (fixed-rank scheme obstruction)

The standard spherical embedding of an association scheme with `s` classes
has at most `s` off-diagonal inner products.  Combining Lemmas 1.1 and 2.1,
any such embedding satisfies

```text
h(X) >= (c_n/Q(d,s))^{1/n}.
```

Consequently no family with both fixed ambient dimension `d` and a uniformly
bounded number of classes can be a P1E mesh family.  An unbounded-class
family is not excluded, but its growing intersection numbers and Krein data
must be estimated uniformly; a computation in one Bose--Mesner algebra does
not supply those estimates.

This separates the successful use of association schemes for the finite
simplex, cube, and cross-polytope equality checks from an asymptotic
construction theorem.

The conclusion is deliberately scoped.  P1C equality makes all active edges
of a connected nonantipodal equality generator one chordal shell; it does not
make all *pairs* of nodes an `s`-distance set.  Lemma 2.1 therefore blocks the
fixed-class association-scheme proposal, not arbitrary one-shell equality
graphs.

## 3. A bounded number of finite orthogonal-group orbits cannot refine

The next obstruction applies in every fixed `d>=3`, not only in `SO(3)`.

### Proposition 3.1 (Jordan--Clifford obstruction)

Fix `d>=3` and `K>=1`.  There is no sequence

```text
X_m = union_{k=1}^K G_{m,k} x_{m,k} subset S^{d-1},
G_{m,k} finite subgroup of O(d),
```

with `h(X_m) -> 0`.

Proof.  Jordan's theorem supplies a number `J_d`, depending only on `d`,
such that every finite subgroup of `O(d)` has an abelian normal subgroup of
index at most `J_d`.  A real orthogonal representation of a finite abelian
group splits into one-dimensional sign blocks and two-dimensional rotation
blocks.  After an orthogonal change of coordinates, the orbit of a vector
under that abelian subgroup is therefore contained in a Clifford torus

```text
{(z_1,...,z_a,t_1,...,t_b): |z_r|=rho_r, |t_q|=sigma_q},
2a+b=d,
```

where the signs of the one-dimensional coordinates may be absorbed into at
most `2^b` components.  Its dimension is at most `floor(d/2)<d-1`.

It follows that every `G_{m,k}x_{m,k}` is contained in the union of at most
`2^d J_d` rotated Clifford tori.  Suppose, for contradiction, that the fill
distances tend to zero.  There are only finitely many block-dimension
patterns.  Passing to a subsequence, compactness of `O(d)`, compactness of the
radius simplex, and padding unused components give Hausdorff convergence of
all the containing tori.  The limiting sphere would be the union of at most
`K 2^d J_d` Clifford tori.  Each limiting torus is closed with empty interior
in `S^{d-1}`, since its dimension is at most `floor(d/2)<d-1`.  The Baire
category theorem forbids a finite union of such sets from being the whole
sphere.  This contradiction proves the proposition.

The proposition does not exclude a number of orbits tending to infinity.
It shows exactly why a fixed finite subgroup, a fixed finite union of its
orbits, or a sequence of increasingly large finite symmetry groups is not an
all-dimensional escape.  The latter groups still have uniformly bounded
index abelian cores in fixed dimension.

## 4. Covers and blow-ups enlarge the graph, not the embedded mesh

### Lemma 4.1 (perturbed-cover obstruction)

Let `Y subset S^n` be a fixed finite embedded base with covering radius
`H_Y>0`.  Suppose a graph cover has vertices `X_m`, a covering map
`pi_m:X_m -> Y`, and an embedding satisfying

```text
dist(x,y_{pi_m(x)}) <= eta_m  for every x in X_m.
```

Then

```text
h(X_m) >= H_Y-eta_m.
```

Choose `z` whose distance from `Y` is `H_Y` and use the triangle inequality.
Thus an exact lift (`eta_m=0`) has fixed positive fill distance and repeated
embedded vertices, hence zero separation.  Even the apparently stronger
condition `eta_m<=C h(X_m)` gives

```text
h(X_m) >= H_Y/(1+C).
```

Therefore connected equality covers and blow-ups are valid P1C algebraic
counterexamples to a Platonic classification, but they cannot be P1E meshes.
Moving the lifted vertices an order-one distance is a new geometric
construction, not a perturbation of the cover.

This also exposes the sampling-kernel trap.  Repeated equality blocks can
retain a nonzero quadratic sampling kernel while their graph cardinality
tends to infinity.  The quotient norm is mathematically correct, but graph
cardinality plus an alias is not geometric refinement; fill distance and
separation detect the failure immediately.

## 5. Common cyclic latitude rings have a divergent mesh ratio

The simplest attempt to evade a single orbit is a stack of cyclic latitude
orbits.  A fixed number of rings cannot cover the sphere, while a common
large cyclic order destroys separation at the poles.

### Lemma 5.1 (number of latitude levels)

Let `X subset S^2` lie on `K` nonpolar latitude circles, with either pole
allowed as an additional point.  If `h(X)=h`, then

```text
K+1 >= pi/(2h).
```

Order the colatitudes and include `0,pi` as endpoints.  The largest of the
`K+1` gaps is at least `pi/(K+1)`.  A point on a meridian at the midpoint of
that gap is at distance at least half the gap from every latitude circle.

### Lemma 5.2 (common-order cyclic obstruction)

Suppose `X subset S^2` consists of aligned regular `M`-gons (the same set of
longitudes on every nonpolar latitude), together with either pole if desired,
and has fill distance `0<h<=1/4`.  If the north polar gap is filled by the
pole and the first regular `M`-gon, then the separation `q(X)` obeys

```text
M >= pi/h,
q(X) <= 4 h^2,
h/q(X) >= 1/(4h).
```

For the first inequality, take an equatorial point halfway between the common
adjacent longitudes.  Its distance from every nonpolar mesh point is at least
`pi/M`, so fill distance `h` forces `pi/M<=h`.  The first nonpolar colatitude
is at most `2h`, or the midpoint of the polar gap is farther than `h` from
the set.  Adjacent points on that first ring have spherical distance no
larger than the parallel-arc length

```text
sin(2h) (2pi/M) <= (2h)(2h)=4h^2.
```

Hence the mesh ratio diverges.  The same proof applies when the phases belong
to a fixed set of `F` common offsets, with `pi/M` replaced by `pi/(FM)` and
only the constant changed.

Variable ring counts are therefore necessary.  But independent rotational
symmetry of an `m`-point ring and an `m'`-point adjacent ring sends one cross
edge through the complete bipartite orbit, giving degrees at least
`max(m,m')`.  A bounded-degree construction must break the independent ring
symmetries and introduce explicit transition stencils between different
counts.  Positivity, shared conductances, and second-moment consistency must
then be proved on those transition stencils; they do not follow from the
one-dimensional latitude recurrence.

## 6. Consequences for the P1E route registry

The exact status of the explored approaches is:

| route | result | unresolved escape |
|---|---|---|
| fixed-class association scheme | `BLOCKED`, with the exact bound `Q(d,s)` | number of classes must diverge and all scheme constants need uniform estimates |
| one or finitely many finite-group orbits | `BLOCKED` for every fixed `d>=3` by Proposition 3.1 | number of unrelated orbits must diverge |
| connected covers or blow-ups of an equality graph | `BLOCKED` by `h>=H_Y-eta` and zero separation in the exact lift | order-one geometric relocation requires a new construction |
| common cyclic latitude grid | `BLOCKED` by `h/q>=1/(4h)` | variable counts require explicitly certified interface templates |
| variable-count latitude rings with independent ring symmetry | `BLOCKED` under bounded degree by the complete-bipartite orbit | break symmetry and prove the transition rows directly |

Thus symmetry remains useful for finite template certification, averaging,
and exact regression fixtures.  It cannot replace the cross-interface and
global reversible-reconciliation arguments in the positive P1E family.
