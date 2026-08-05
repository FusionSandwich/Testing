# P1E Coxeter-reflection route audit

## Status

The finite `B_d` Coxeter complex is a legitimate replacement for the
topologically impossible cubulation used in the rejected structured-stress
draft.  It gives a finite, exactly matching macro-complex and it is useful for
organizing singular stars.  It does **not**, by itself, provide the P1E upper
family.  Two additional assertions remain theorem-strength gaps:

1. a uniform second-order polar/midpoint compiler at every Coxeter stratum;
2. a uniform maximum-norm right inverse for the shared equilibrium (or
   eigenmap) correction.

Consequently the route described as

```text
Coxeter chamber + reflected barycentric lattice + midpoint stencil
                 + constrained harmonic embedding
```

is `BLOCKED`, not a proved all-dimensional construction.  The exact reasons
are recorded below so that reflection symmetry is not silently used as a
substitute for either missing estimate.

Put `n=d-1`, and let `W=B_d` be the signed-permutation group.  A standard
closed chamber is

\[
 {\cal Q}=\{x\in S^{d-1}:x_1\geq x_2\geq\cdots\geq x_d\geq0\}.
 \tag{C.1}
\]

## C.1 What the Coxeter complex really fixes

The images `w Q`, `w in W`, form a finite spherical simplicial
complex.  A barycentric subdivision of `Q`, reflected by `W`, has
matching traces on every wall.  Since radial projection is bi-Lipschitz on
each of the finitely many closed macro-simplices, ordinary compactness gives
effective constants `q_d,H_d,D_d>0` for separation `q_d/N`, fill
`H_d/N`, and degree `D_d`.  All of these constants can be obtained by
finite interval minimization on the one chamber.  Thus this replacement does
remove the false assertion that a spherical cubulation has `2^r` ordinary
cubical sectors at every stratum.

It does not produce one smooth affine grid chart through all strata.  This
already fails in the first nontrivial dimension.

### Cone-angle certificate in `d=3`

The `B_3` chamber is the spherical triangle with angles

\[
 \alpha_1=\frac\pi2,\qquad
 \alpha_2=\frac\pi3,\qquad
 \alpha_3=\frac\pi4.                              \tag{C.2}
\]

Suppose an ordinary Euclidean reference triangle with corner angle
\(\beta_k\) supplied an affine barycentric lattice, and suppose reflection of
that chart through the two incident walls extended to a `C^1` local
diffeomorphism at the corresponding spherical corner.  The product of the
two reference reflections is rotation through twice the reference angle; the
product of the two target reflections is rotation through twice the target
angle.  The derivative
at the corner would be a nonsingular real linear map intertwining these two
rotations.  Two planar rotations are conjugate by a real nonsingular linear
map only when their angles agree up to sign.  Hence

\[
 \beta_k=\alpha_k.                                \tag{C.3}
\]

But an Euclidean triangle has angle sum `pi`, whereas

\[
 \frac\pi2+\frac\pi3+\frac\pi4=\frac{13\pi}{12}>\pi. \tag{C.4}
\]

Therefore no single nondegenerate affine barycentric chart has the reflected
smoothness needed by a midpoint Taylor proof.  Equivalently, unfolding
`2m_k` reference sectors around a corner of angle `pi/m_k` produces a
flat cone of total angle `2m_k beta_k`; it is smooth only when
`beta_k=pi/m_k`.

This is not a nonexistence theorem for all Coxeter constructions.  It proves
that a valid construction needs separate singular-star and transition
templates.  Merely saying “reflect the barycentric lattice” does not supply
them.

## C.2 Symmetry does not imply exact coordinate reproduction

At a generic chamber node the stabilizer in `W` is trivial.  A
`W`-equivariant tangent residual therefore has all `n` tangent components
free at each orbit representative.  Thus `W`-symmetry alone does not imply

\[
 \sum_j\gamma_{ij}P_i x_j=0.                      \tag{C.5}
\]

The relevant correction space is the space of `W`-**equivariant tangent
vector fields**, not the space of invariant scalar functions.  Symmetry does
remove the rotational kernel: if `u(x)=Ax`, `A^T=-A`, is `W`-equivariant,
then `A` commutes with every signed permutation.  The commutant of the
standard `B_d` representation consists of scalars, so `A=0`.  This gives a
continuous Korn gap on the equivariant subspace.  It does not give the
discrete maximum-norm estimate needed for positivity.

For a shared-stress correction let

\[
 (T_x\eta)_i=\sum_j\eta_{ij}P_ix_j,
 \qquad K_h=T_x\Gamma^0T_x^*.                     \tag{C.6}
\]

If baseline conductances have size `h^(n-2)`, a second-order coordinate
defect has nodal-force size `h^(n+2)`.  To keep every corrected edge
positive with an `O(h^2)` relative correction, one needs an estimate of the
form

\[
 \|T_x^*K_h^\dagger f\|_{\ell^\infty(E_h)}
 \leq C h^{-n}\|f\|_{\ell^\infty(X_h)}.           \tag{C.7}
\]

An `L^2` Korn inequality does not imply (C.7).  The sharp inverse inequality
already loses `h^(-n/2)`.  To see why symmetry does not cure this, choose a
generic node, put a tangent load on it, reflect that load around its `W`
orbit, and project off the finitely many compatibility modes.  The orbit has
at most `|W|=2^d d!` nodes, independent of `h`.  Its weighted `L^2` norm
is `O(h^(n/2))` times its `L-infinity` norm.  Hence an energy estimate alone
cannot exclude a correction concentrated on a fixed Coxeter orbit.  A
discrete Green-gradient, Schauder, or explicit local flux theorem is still
required, with a constant uniform across the singular templates.

The same issue occurs if one corrects the node positions by a constrained
harmonic embedding.  Besides (C.7), that version needs a quantitative
implicit-function theorem for the sphere constraints, a proof that the
resulting eigenmap has no zero vertices, and a check that normalization does
not destroy the eigenvalue equation.  No one of these follows from
`B_d`-equivariance.

## C.3 The raw normalized lattice still has a first-order seam

The particularly explicit `W`-invariant shell

\[
 X_N=\left\{\frac{k}{\|k\|_2}:k\in\mathbb Z^d,
                 \ \sum_a|k_a|=N\right\}          \tag{C.8}
\]

is quasiuniform and has bounded-degree Delaunay/polar adjacency.  It is not a
second-order family.  In `d=3`, at

\[
 x=\frac{(m,0,m)}{\sqrt{2}m},\qquad N=2m,
\]

the exact tangent polar cell calculation recorded in
`P1E_POLAR_CELL_ROUTE.md`, equations (P.21a)--(P.21c), gives

\[
 \lim_{N\to\infty}N\|M_x\|_F=\sqrt2.              \tag{C.9}
\]

Thus the most natural reflected Coxeter lattice has a genuine
`Theta(h)` row defect on an orthant seam.  Global signed-permutation
symmetry does not cancel it in the weighted norm.  Indeed, away from the
seam endpoints the scaled polar-cell vertices are rational-algebraic smooth
functions of the seam parameter.  The nonzero coefficient in (C.9) therefore
remains bounded away from zero on a fixed open seam interval.  That interval
contains `Theta(h^(-1))` nodes on `S^2`; with nodal masses `Theta(h^2)`, the
P1B tensor trace bound gives a global defect at least `Omega(h^(3/2))`, which
is larger than the required `O(h^2)`.  Any successful Coxeter construction
must replace a fixed-width neighborhood of every such seam by a certified
second-order collar; it cannot use the raw radial lattice.

## C.4 A possible exact-`H_1` replacement, and its remaining finite lemma

There is a useful way to avoid the global solve.  For each node define the
tangent polar cell

\[
 C_i=\{z\in T_{x_i}S^{d-1}:P_ix_j\cdot z\leq1-x_i\cdot x_j
                                      \text{ for all }j\}.
\]

If `F_ij` is a facet, put

\[
 \gamma_{ij}=\frac{|F_{ij}|}{\sin\theta_{ij}}.
\]

The shared-ridge identity and the divergence theorem give exactly

\[
 \gamma_{ij}=\gamma_{ji}>0,
 \qquad
 \sum_j\gamma_{ij}P_ix_j=0,
 \qquad
 \mu_i=\frac1n\sum_j\gamma_{ij}(1-x_i\cdot x_j)=|C_i|. \tag{C.10}
\]

Consequently `a_ij=gamma_ij/mu_i` is reversible and satisfies
`Lx=-nx` exactly.  This is a genuine repair of the harmonic-embedding step.

What remains is not automatic: every ordinary collar and every singular-star
template must satisfy, with explicit constants, the paired-facet estimates

\[
 \begin{aligned}
 |\sigma_+-\sigma_-|&=O(h^n),&
 |s_+-s_-|&=O(h^2),&
 \|\nu_++\nu_-\|&=O(h),\\
 \|t_\pm\|&=O(h^2),&
 \|t_+-t_-\|&=O(h^3),
 \end{aligned}                                    \tag{C.11}
\]

together with a uniform nonzero Voronoi determinant and inactive-facet slack.
These imply `||M_i||_F <= C h^2`, but neither crystallographicity nor
Coxeter symmetry proves (C.11).  Reducible parabolic stabilizers are a
specific normalization trap.  For example, the stabilizer at
`(1,1,0)/sqrt(2)` in the `B_3` chamber is `A_1 x A_1`, so invariance
only makes the two tangent covariance blocks diagonal; it does not force
their coefficients to be equal.  Equality must be checked from the actual
polar cell, not asserted by irreducibility.

Hence the polar replacement converts a global analytic gap into a finite
but still unimplemented compiler lemma.  Until the collar maps, direction
lists, determinant margins, and every parabolic template are written down,
the replacement is conditional.

## C.5 Sampling quotient: a repairable part

The sampling quotient is not the obstruction.  Suppose the final exact
stress gives

\[
 w_i\geq\omega_-h^n,
 \qquad \operatorname{fill}(X_h)\leq h.
\]

For trace-free `A` with Frobenius norm one, choose an eigenvector `u` with
`|u^T A u| >= d^(-1/2)`.  Since `x -> x^T A x` is `2`-Lipschitz, on
the cap of radius `r=1/(4 sqrt(d))` about `u` its absolute value is at
least `1/(2 sqrt(d))`.  Covering the cap of radius `r/2` by the nodal
`h`-balls and using `2t/pi <= sin(t) <= t` gives, for
`h <= 1/(16 sqrt(d))`,

\[
 \sum_iw_i(x_i^TAx_i)^2\geq\alpha_d\|A\|_F^2,
\]

\[
 \boxed{
 \alpha_d=
 \frac{\omega_-}{4d}
 \left(\frac2\pi\right)^{d-2}
 (8\sqrt d)^{-(d-1)}.}                            \tag{C.12}
\]

Thus a uniform row bound `max_i ||M_i||_F <= C_M h^2` would imply, on the
correct sampling quotient,

\[
 \mathfrak D_2\leq C_M\alpha_d^{-1/2}h^2.          \tag{C.13}
\]

This also audits the missing `d^(-(d-1)/2)` factor in any cap estimate that
uses a radius independent of the eigenvalue lower bound `d^(-1/2)`.

## C.6 Robustness cannot be stated without a perturbation norm

Arbitrary labeled jitter and smooth mesh deformations have different scales.
For a fixed graph and conductances, moving one endpoint by `eta` changes a
tangent force by `O(h^(n-2) eta)`.  A high-frequency correction can therefore
have relative edge size `O(eta/h)`.  To retain an `O(h^2)` tensor error
under completely arbitrary jitter one must impose at least a correspondingly
small absolute scale; the conservative `O(h^4)` hypothesis in the rejected
stress draft is sufficient if (C.7) is available.  By contrast a smoothly
sampled perturbation with discrete `C^2` norm `O(h^2)` can have physical
size `O(h^2)`, because its edge differences and second differences gain the
missing powers of `h`.

Therefore “robust under small perturbations” must specify either

* an absolute high-frequency jitter bound (and the exact inverse constant),
  or
* a scaled discrete `C^2` bound tied to the reflected templates.

Reflection symmetry is destroyed by a generic perturbation, so the
`B_d`-fixed inverse cannot be used for that robustness statement.

## C.7 Audit verdict

| item | verdict | reason |
|---|---|---|
| finite spherical macro-complex | `PASS` | the `B_d` Coxeter chambers match exactly |
| fill, separation, bounded degree | `PASS_CONDITIONAL_CONSTANTS` | finite bi-Lipschitz and packing estimates suffice |
| one smooth affine reflected barycentric chart | `FAIL` | exact `B_3` cone-angle certificate (C.2)--(C.4) |
| raw normalized Coxeter shell | `FAIL` | exact `Theta(h)` seam tensor (C.9) |
| exact `H_1` from symmetry | `FAIL` | generic stabilizer is trivial |
| constrained harmonic correction | `BLOCKED` | uniform discrete `L-infinity` inverse and nonlinear eigenmap control missing |
| polar-cell exact `H_1` replacement | `PASS_ALGEBRA` | finite divergence identities (C.10) |
| second-order polar collar/compiler | `BLOCKED` | (C.11) and all determinant/slack margins not constructed |
| sampling quotient | `PASS_CONDITIONAL_MASS` | explicit constant (C.12) |
| arbitrary perturbation robustness | `BLOCKED_WITHOUT_SCALE` | symmetry is lost and inverse dependence is essential |

The Coxeter idea is therefore a useful mesh scaffold, but it cannot be cited
as the P1E matching upper theorem in its present form.  A complete promotion
requires either a fully enumerated polar-cell compiler proving (C.11) at all
ordinary and parabolic templates, or a proved discrete Green-gradient bound
plus a quantitative constrained-embedding theorem.  Each alternative is the
missing theorem, not a routine consequence of finite reflection symmetry.
