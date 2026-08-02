# Spectral products: resonance, Jensen, and the bounded hierarchy

## Exact finite-generator identities

For

\[
 \Gamma(f,g)(i)=\frac12\sum_{j\ne i}a_{ij}
 (f(j)-f(i))(g(j)-g(i)),
\]

direct expansion gives, without sign assumptions,

\[
 L(fg)-fLg-gLf=2\Gamma(f,g).
\]

If (Lf=-\lambda f) and (Lg=-\nu g), then for every (c,\mu),

\[
 \boxed{L(fg-c)+\mu(fg-c)
 =2\Gamma(f,g)+(\mu-\lambda-\nu)fg-\mu c.}
\]

Thus (fg-c) has eigenvalue (-\mu) exactly when the right side vanishes
pointwise.  At resonance (\mu=\lambda+\nu), this becomes
(2\Gamma(f,g)=(\lambda+\nu)c).  In particular,

\[
 f^2-c\text{ has eigenvalue }-2\lambda
 \quad\Longleftrightarrow\quad
 \Gamma(f)=\lambda c.
\]

When (\mu=0), (c) is invisible.  For signed rates, (\Gamma(f)) need not be
nonnegative.

## Permanent counterexample to blanket square obstruction

On (\{\pm1\}^2), let each coordinate flip at rate one and put
(f=x_1+x_2).  Exactly,

\[
 Lf=-2f,qquad f^2-2=2x_1x_2\ne0,qquad
 L(f^2-2)=-4(f^2-2),\qquad\Gamma(f)=4.
\]

Any universal positive-generator claim forbidding a nonzero centered doubled
square is therefore false.

## Semigroup derivation and Jensen equality

Let (P_t=e^{tL}).  If (Lf=-\lambda f) and
(L(f^2-c)=-2\lambda(f^2-c)), then

\[
 P_t(f^2)-(P_tf)^2=c(1-e^{-2\lambda t}).
\]

Conversely, under the finite-dimensional differentiability and eigenfunction
assumptions, differentiating this identity at (t=0) gives
(L(f^2)-2fLf=2\lambda c), hence (\Gamma(f)=\lambda c).  This is an
independent semigroup derivation, not an equality case of Jensen.

For a positive generator, (P_t(i,\cdot)) is a probability kernel, and

\[
 P_t(f^2)(i)-(P_tf(i))^2
 =\operatorname{Var}_{P_t(i,\cdot)}f\ge0.
\]

Equality holds exactly when (f) is constant on the states with positive
transition probability from (i) at time (t).  For a finite irreducible
continuous-time chain and (t>0), uniformization shows every entry of (P_t)
is positive: choose a stochastic matrix with positive diagonal and use a
positive-probability path in its Poisson series.  Equality at one state then
forces global constancy.  The Boolean example has positive variance
(2(1-e^{-4t})), so Jensen equality and resonance are visibly different.

## The spherical curvature shift

On (S^{d-1}), coordinate functions have eigenvalue (d-1), whereas degree
two has eigenvalue (2d):

\[
 2d-2(d-1)=2.
\]

Therefore the spherical quadratic residual is not a doubled-eigenvalue
obstruction.  Applying the arbitrary-target identity to coordinate products
retains the (2fg) curvature term; contracting with a matrix is exactly the
covariance residual (R_X=(L+2dI)S_X).

## Continuous (S^2) hierarchy

Clebsch--Gordan decomposition and symmetry under interchange give

\[
 \operatorname{Sym}^2(H_\ell)=\bigoplus_{r=0}^{\ell}H_{2r}.
\]

Products are antipodally even for both odd and even (\ell).  Centering
removes only (H_0) in the continuous decomposition.  Every square has at
least an antipodal pair of maximizers, so unique-maximizer arguments do not
apply without extra hypotheses.

| (\ell) | components | continuous eigenvalues | after centering | doubled target | doubled component? |
|---:|---|---|---|---:|---|
| 1 | (H_0\oplus H_2) | (0,6) | (H_2) | 4 | no |
| 2 | (H_0\oplus H_2\oplus H_4) | (0,6,20) | (H_2\oplus H_4) | 12 | no |
| 3 | add (H_6) | add 42 | (H_2\oplus H_4\oplus H_6) | 24 | no |
| 4 | add (H_8) | add 72 | nonconstant even components | 40 | no |
| 5 | add (H_{10}) | add 110 | nonconstant even components | 60 | no |
| 6 | add (H_{12}) | add 156 | nonconstant even components | 84 | no |

The dimension is ((\ell+1)(2\ell+1)).  A doubled continuous component must
satisfy

\[
 J(J+1)=2\ell(\ell+1),\qquad J\text{ even}.
\]

With (x=2J+1,y=2\ell+1), this is
(x^2-2y^2=-1) plus (x\equiv1\pmod4).  All admissible solutions are

\[
 x+y\sqrt2=(1+\sqrt2)^{4m+1}.
\]

Besides the constant solution, the first pairs are
((\ell,J)=(14,20),(492,696),\ldots), with recurrence

\[
 x'=17x+24y,qquad y'=12x+17y.
\]

This is an exact (\ell)-indexed component-availability classification, not a
claim that one product isolates the component and not a positivity no-go.

## Genuine sampled hierarchy: corrected separation theorem

The linear-algebraic theorem is indexed by **target eigenvalues**, not merely
by names or degrees.  Let (V_a\subseteq\mathbb R^I) be finitely many sampled
spaces and let (\theta_a\in\mathbb R).  If one operator satisfies

\[
 L|_{V_a}=-\theta_a I
\]

and the targets (\theta_a) are pairwise distinct, then the (V_a) form an
internal direct sum.  Indeed, for a relation (\sum_a v_a=0), applying the
Lagrange interpolation polynomial that is one at (-\theta_b) and zero at the
other target scalars isolates (v_b=0).  Consequently

\[
 \boxed{\sum_a\dim V_a\le |I|.} \tag{S.1}
\]

More generally, collisions must be grouped before counting.  For every target
(\theta), put

\[
 W_\theta=\sum_{a:\theta_a=\theta}V_a.
\]

Then the spaces (W_\theta) for the distinct target values form an internal
direct sum and

\[
 \boxed{\sum_\theta\dim W_\theta\le |I|.} \tag{S.2}
\]

No directness, or sum of the individual dimensions, follows inside one
equal-target class.

For spherical harmonics on (S^{d-1}), let

\[
 E_\ell:H_\ell\to\mathbb R^I,\qquad
 V_\ell=\operatorname{im}E_\ell,\qquad
 \lambda_\ell=\ell(\ell+d-2).
\]

When (d\ge2), the map (\ell\mapsto\lambda_\ell) is strictly increasing for
(\ell\ge0).  Thus pairwise distinct degrees have pairwise distinct targets,
and (S.1) gives

\[
 \boxed{\sum_{\ell\in D}\operatorname{rank}E_\ell\le |I|.} \tag{S.3}
\]

For even harmonics on an antipodally symmetric sample, every sampled function
is constant on each antipodal orbit, so the right side of (S.3) sharpens to
the number of antipodal orbits.

The unqualified distinct-degree statement is **REJECTED** in dimension one.
Take (d=1), (I=\{*\}), (\Phi(*)=+1\in S^0), and (L=0).  With
(D=\{0,1\}), one has (H_0=\operatorname{span}\{1\}),
(H_1=\operatorname{span}\{x\}), and evaluation at (+1) gives

\[
 V_0=V_1=\mathbb R^I,\qquad r_0=r_1=1,
 \qquad\lambda_0=\lambda_1=0.
\]

Both scalar-action hypotheses hold, but
(V_0\cap V_1=\mathbb R^I) and
(r_0+r_1=2>|I|=1).  The valid (d=1) theorem is (S.2): group degrees by their
equal values of (\ell(\ell-1)) before making any direct-sum or rank count.

The converse is also most cleanly stated by target classes and treats
constants only once.  Let (C=\langle\mathbf1\rangle), enlarge the zero-target
class to

\[
 \widetilde W_0=C+W_0,
\]

and put (\widetilde W_\theta=W_\theta) for (\theta\ne0).  A signed conservative
operator with the prescribed scalar actions exists exactly when the
(\widetilde W_\theta) for distinct targets form an internal direct sum.  For
the constructive direction, set (L=-\theta I) on each class and set (L=0) on
an arbitrary complementary space.  Then (L\mathbf1=0); in the standard basis,
take (a_{ij}=L_{ij}) for (i\ne j), while the zero row sums supply the generator
diagonal.  If degree zero is already in (D), its sampled space is (C), so it is
not added or counted a second time.

For positive weights (w_i), a weighted-reversible signed realization exists
exactly when the distinct target-class spaces (\widetilde W_\theta) are
mutually orthogonal in the weighted inner product.  Necessity is orthogonality
of eigenspaces of a self-adjoint operator at distinct eigenvalues.  For
sufficiency, use the scalar construction above and set (L=0) on the weighted
orthogonal complement.  In particular, constants must be weighted-orthogonal
to every nonzero-target sampled eigenspace; this condition cannot be omitted.

The exact audit computes harmonic evaluation ranks over
(\mathbb Q(\sqrt5)).  At (\ell=2), the rank sums for
(H_0,H_2,H_4) exceed the aggregate even-sample rank for all five Platonic
sets.  In particular (\operatorname{im}H_4=\operatorname{im}H_2) on the
icosahedron and (\operatorname{im}H_2\subset\operatorname{im}H_4) on the
dodecahedron.  No operator, even signed, can assign their distinct continuous
eigenvalues simultaneously.

## Final hierarchy status

`PROVED`: the target-eigenvalue-class separation/rank theorem gives a genuine
finite-sampling restriction, and for (d\ge2) it specializes to pairwise
distinct spherical-harmonic degrees.  `REJECTED`: the same distinct-degree
wording in unrestricted dimension, by the exact (d=1) one-node example above.
The parity-filtered Pell classification is `EXTERNAL`, with its first cases
checked exactly.  `REJECTED` as a universal positivity hierarchy: without
added nonaliasing and component hypotheses, the positive statement reduces to
the same pointwise carré-du-champ residual with different constants.  Finite
sampling may kill or alias every continuous component, and one selected
combination is not a complete irreducible module.
