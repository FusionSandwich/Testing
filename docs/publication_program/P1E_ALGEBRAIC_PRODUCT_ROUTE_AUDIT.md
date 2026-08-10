# P1E algebraic/product/join route audit

## Status

`NO COMPLETE ALL-LEVEL FAMILY ON THESE ROUTES.`

This note records five exact results:

1. fixed tensor-product and suspension grids cannot be quasiuniform at the
   collapsed factors;
2. fixed global coordinate-plane rotations cannot generate a growing
   quasiuniform finite family in fixed ambient dimension;
3. separable composition-state eigenmaps have a rigid square-root form and
   an unbounded mesh ratio;
4. two unbuffered stereographic lattice balls have an exact Pell-family
   separation collapse at their common equator;
5. radial normalization of a common graph eigenspace gives an exact positive
   reversible `H_1` eigenmap.  This last identity is useful, but without a
   separately proved `C^1` spectral-embedding estimate and local quadratic
   moments it does not finish P1E.

The literal cubical and cross-polytopal product shells are also classified.
Their natural shared graph is rejected by an existing exact recurrence, and
the polar exact-`H_1` stress retains first-order defects on macroseams.  No
claim below promotes numerical scaling to a theorem.

Throughout `n=d-1` and `d>=3`.

## 1. Fixed suspensions and joins lose quasiuniformity

Write the spherical suspension as

\[
 \Sigma S^{m}=\{(\cos\theta,\sin\theta\,x):
             0\le\theta\le\pi,\ x\in S^m\}.       \tag{1.1}
\]

Suppose a tensor construction uses a factor mesh `Y_h` at every non-polar
latitude.  To have fill distance at most `Hh` near the north pole, its first
non-polar latitude satisfies

\[
 0<\theta_h\le 2Hh.                                \tag{1.2}
\]

To have fill distance `O(h)` on an equatorial slice, `Y_h` must contain two
distinct points `x,x'` at factor distance at most `C h`; indeed any
quasiuniform factor has many such pairs.  At the first latitude their joined
points have distance

\[
 |(\cos\theta_h,\sin\theta_hx)
  -(\cos\theta_h,\sin\theta_hx')|
 =\sin\theta_h|x-x'|
 \le 2HC h^2.                                      \tag{1.3}
\]

Thus separation is `O(h^2)` while fill is `Theta(h)`, and the mesh ratio is
at least `c/h`.  The same proof applies to either collapsed factor of a join

\[
 S^p*S^q=\{(\cos\theta\,x,\sin\theta\,y)\}.        \tag{1.4}
\]

Consequently a successful join must coarsen the collapsed factor by a number
depending on `theta`.  The cardinality changes create genuine interfaces;
they cannot be dismissed as a tensor-product endpoint convention.  A
dyadic coarsening reduces the catalogue to bounded-ratio interfaces, but it
still needs positive shared conductances and exact moment reconciliation at
every `1:2` transition.

## 2. Global small-rotation Cayley constructions are impossible

Consider a finite connected node set `X subset S^(d-1)` and a fixed finite
symmetric set of rotations `mathcal R subset SO(d)`.  Assume that every
outgoing rotation is present at every node:

\[
 x\in X,\ R\in\mathcal R\quad\Longrightarrow\quad Rx\in X. \tag{2.1}
\]

This condition is the attractive algebraic construction: with all
coordinate-plane pairs `R_ab(theta),R_ab(-theta)` and equal coefficients,

\[
 \sum_{a<b}\{R_{ab}(\theta)+R_{ab}(-\theta)-2I\}
 =2(d-1)(\cos\theta-1)I,                           \tag{2.2}
\]

so the coordinates are an exact common eigenmap and all edges have length
`O(theta)`.

Let `Gamma=<mathcal R>`.  By (2.1), each connected component is a finite
`Gamma`-orbit.  If an orbit contains `d` linearly independent points, the
kernel of the action on that orbit is trivial, so `Gamma` itself is finite.
Any sufficiently fine spherical net contains such an orbit after passing to
the component which is meant to cover the sphere.

In `d=3`, classification of finite rotation groups is already decisive.
The cyclic and dihedral families have growing order, but one generic orbit is
contained in at most two latitude circles about one axis.  Its fill distance
is bounded below.  Tetrahedral, octahedral, and icosahedral rotation groups
have bounded order.  Hence no sequence satisfying (2.1) is a quasiuniform
net with fill tending to zero.

There is also an all-dimensional form.  Jordan's theorem gives a constant
`J_d` such that every finite subgroup of `GL_d(C)` contains an abelian normal
subgroup of index at most `J_d`.  An abelian orthogonal subgroup is
simultaneously block diagonal with at most `floor(d/2)` rotation planes.
The orbit of a point under that subgroup lies in a flat torus of dimension
at most `floor(d/2)`.  A full group orbit is therefore contained in at most
`J_d` such tori.  Since

\[
 \lfloor d/2\rfloor<d-1,                            \tag{2.3}
\]

the spherical volume of an `r`-neighbourhood of this union is at most
`C_dJ_dr^{d-1-floor(d/2)}`.  It cannot cover `S^(d-1)` for all small `r`.

Thus (2.2) is an exact eigenmap identity but not an all-level mesh.  Escaping
the obstruction requires state-dependent rotations with nontrivial holonomy
and interface compatibility; closure under a fixed finite rotation set is
too rigid.

## 3. Rigidity of separable composition eigenmaps

Let

\[
 \mathcal C_N=\{k\in\mathbb Z_{\ge0}^d:\sum_a k_a=N\}. \tag{3.1}
\]

A common product/Markov ansatz assigns coordinate magnitudes separately,

\[
 \Omega_a(k)=\frac{f_N(k_a)}{\sqrt{C_N}},
 \qquad
 \sum_a f_N(k_a)^2=C_N                             \tag{3.2}
\]

for every composition.  Put `g_N(t)=f_N(t)^2`.  Comparing the compositions

\[
 (u+1,v-1,r,0,\ldots),\qquad (u,v,r,0,\ldots)      \tag{3.3}
\]

with the same total, and varying the slack coordinate `r`, shows that

\[
 g_N(u+1)-g_N(u)=g_N(v)-g_N(v-1).                  \tag{3.4}
\]

All first differences are equal.  Therefore

\[
 \boxed{f_N(t)^2=\alpha_Nt+\beta_N}.               \tag{3.5}
\]

The familiar square-root simplex is not a choice among many separable
constant-norm embeddings; it is forced.

Write `b_N=beta_N/alpha_N` when `alpha_N>0`.  An interior unit transfer has
normalized size `Theta(N^-1)` whenever `b_N=o(N)`.  If `b_N=0`, the first
nonzero coordinate has size `Theta(N^-1/2)`, so the fill/separation ratio is
at least `c sqrt(N)`.  If `0<b_N=o(N)`, every coordinate magnitude is at
least

\[
 \sqrt{b_N/(N+db_N)},                              \tag{3.6}
\]

so the distance to a coordinate hyperplane divided by the interior
separation is at least `c sqrt(N b_N)` (and in particular diverges).  If
`b_N` is comparable to `N`, every coordinate magnitude stays uniformly away
from zero and the nodes fail to fill the sphere.  Adding signs does not
remove this dichotomy.

Hence multinomial, Ehrenfest, and other separable composition chains do not
give the required quasiuniform spherical family in fixed dimension.

## 4. Naive stereographic double-ball gluing loses separation

The double-ball idea removes the topological need for one global chart, but
the literal union of two Cartesian stereographic grids is not quasiuniform.
For `t in R^n`, write the two hemisphere maps as

\[
 \Phi_\pm(t)=\frac{(2t,\ \pm(1-|t|^2))}{1+|t|^2},
 \qquad |t|\le1.                                   \tag{4.1}
\]

Take the lattice `t=k/N`.  The Pell equation

\[
 N^2-5a^2=1                                        \tag{4.2}
\]

has infinitely many positive integer solutions; for example, all powers
`N+a sqrt(5)=(9+4 sqrt(5))^m`, `m>=1`, give such solutions.  Put
`k=(a,2a,0,...,0)`.  Then

\[
 |t|^2=1-N^{-2}.                                   \tag{4.3}
\]

The north and south nodes with the same `t` are distinct and their exact
distance is

\[
 |\Phi_+(t)-\Phi_-(t)|
 =\frac{2(1-|t|^2)}{1+|t|^2}
 =\frac{2}{2N^2-1}=\Theta(N^{-2}).                 \tag{4.4}
\]

Each Cartesian cap has fill scale `Theta(N^-1)`.  Hence the two-cap union
has mesh ratio at least `cN` along the infinite Pell subsequence.  Deduping
the exact equator does not remove (4.4), because these points lie strictly
on opposite sides.

A viable double-ball construction must delete an `Omega(h)` collar from
both Cartesian caps and insert a single shared equatorial collar.  Building
that collar requires an all-level mesh on `S^(n-1)` and positive shared
transition stencils, so the problem becomes a genuine recursive interface
construction rather than two independent grids.

## 5. Exact spectral radial-normalization lemma

The following algebraic exactification is unconditional and may be useful in
a different construction.

Let `G=(V,E)` have symmetric positive conductances `c_ij=c_ji>0`, let
`m_i>0`, and suppose a vector-valued function `f_i in R^d` satisfies the
common generalized eigenvalue equation

\[
 \sum_jc_{ij}(f_j-f_i)=-\lambda m_if_i.             \tag{5.1}
\]

Assume `s_i=|f_i|>0` and put

\[
 \Omega_i=f_i/s_i,\qquad c'_{ij}=s_is_jc_{ij}.       \tag{5.2}
\]

Then

\[
\begin{aligned}
 \sum_jc'_{ij}(\Omega_j-\Omega_i)
 &=s_i\sum_jc_{ij}f_j-f_i\sum_jc_{ij}s_j\\
 &=f_i\left[s_i\left(\sum_jc_{ij}-\lambda m_i\right)
             -\sum_jc_{ij}s_j\right].              \tag{5.3}
\end{aligned}
\]

The right side is parallel to `f_i`, hence to `Omega_i`.  Define

\[
 \mu_i={1\over n}\sum_jc'_{ij}(1-\Omega_i\cdot\Omega_j).
                                                               \tag{5.4}
\]

Radial contraction of (5.3) yields exactly

\[
 \sum_jc'_{ij}(\Omega_j-\Omega_i)=-n\mu_i\Omega_i. \tag{5.5}
\]

If every vertex has a neighbour with a different normalized row, then
`mu_i>0`.  After the usual normalization, (5.5) is a finite positive reversible
generator reproducing `H_0` and `H_1` exactly.  No nonlinear harmonic-map
inverse is involved.

What remains is substantial.  One must exhibit a positive local graph with a
`d`-dimensional common eigenspace for which the normalized rows in (5.2):

* form a quasiuniform spherical net;
* have edgewise `C^1` accuracy strong enough to preserve the local second
  tensor through `O(h^2)`;
* retain a uniform local conductance margin.

Ordinary `L^2` spectral convergence does not imply these properties.  In
particular an `O(h^2)` nodal error with only an `O(h)` gradient error changes
edge increments at order `h^2` and leaves an `O(h)` quadratic defect.

## 6. Literal cubical and cross-polytopal shells

Two explicit product shells are

\[
 X_N^\infty=\{k/|k|_2:\|k\|_\infty=N\},\qquad
 X_N^1=\{k/|k|_2:\|k\|_1=N\}.                     \tag{6.1}
\]

Both are algebraic, `B_d`-invariant, quasiuniform, and have natural
bounded-degree local graphs.  They do not complete P1E.

For `X_N^infty`, the exact macroface calculation in
`P1E_CUBED_SPHERE_ROUTE_AUDIT.md` shows that tangent equilibrium and leading
tightness on the natural axial graph force

\[
 u_{k+1}/u_k=(N-k)/(k+1),\qquad
 u_k=u_0{N\choose k}.                              \tag{6.2}
\]

Uniform shared conductance margins therefore fail exponentially, even if
tightness is relaxed by `O(h^2)`.

For either shell, the polar-Piola construction gives positive shared
conductances and exact `H_1`.  It does not repair the product kink.  Direct
deterministic stress tests show `O(h)` normalized row defects along the
codimension-one macroseams and observed global defect of order `h^(3/2)` in
`d=3`.  These tests are falsification evidence only; the exact theorem used
to reject the natural cubical graph remains (5.2).  A claimed `O(h^2)` proof
for either polar shell must therefore supply an analytic cancellation absent
from the row data, not infer it from quasiuniformity or symmetry.

## Route registry

| Approach | Status |
|---|---|
| Fixed suspension/join product | `REJECTED`: mesh ratio diverges |
| Adaptive/dyadic suspension | `BLOCKED`: unresolved `1:2` interfaces |
| Fixed global coordinate-plane rotations | `REJECTED`: finite-orbit obstruction |
| Separable composition-state eigenmap | `REJECTED`: square-root rigidity |
| Unbuffered stereographic double ball | `REJECTED`: exact Pell separation collapse |
| Radially normalized common eigenspace | `EXACT H_1 LEMMA`; geometric estimates missing |
| Natural cubed-sphere axial stress | `REJECTED`: binomial sharedness obstruction |
| Literal shell plus polar stress | `EXACT H_1`; `H_2` order not established and numerically falsified |
| State-dependent rotations / singular templates | `BLOCKED`: requires a shared interface compiler |

These obstructions leave open genuinely nonseparable adaptive constructions,
but none may be replaced by a fixed product, a finite rotation orbit, or a
spectral `L^2` convergence assertion.
