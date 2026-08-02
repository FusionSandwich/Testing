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

## Genuine sampled hierarchy: separation theorem

Let (E_J:H_J\to\mathbb R^I) be evaluation and (V_J=\operatorname{im}E_J).
If one operator satisfies

\[
 L|_{V_J}=-J(J+1)I
\]

for distinct degrees in a set (D), then the (V_J) form an internal direct
sum, since eigenspaces at distinct scalars are linearly independent.  Hence

\[
 \boxed{\sum_{J\in D}\operatorname{rank}E_J\le |I|.}
\]

For even harmonics on an antipodally symmetric sample, the right side sharpens
to the number of antipodal orbits.  Conversely, if (V_0=\langle\mathbf1\rangle)
and these sampled spaces form a direct sum, define (L) by the displayed
scalars on their sum and extend it with (L\mathbf1=0).  Its off-diagonal
matrix entries are signed jump rates.  A weighted reversible signed realization
exists by the same construction when the distinct spaces are mutually
orthogonal in the weighted inner product; orthogonality is also necessary for
a self-adjoint (L).

The exact audit computes harmonic evaluation ranks over
(\mathbb Q(\sqrt5)).  At (\ell=2), the rank sums for
(H_0,H_2,H_4) exceed the aggregate even-sample rank for all five Platonic
sets.  In particular (\operatorname{im}H_4=\operatorname{im}H_2) on the
icosahedron and (\operatorname{im}H_2\subset\operatorname{im}H_4) on the
dodecahedron.  No operator, even signed, can assign their distinct continuous
eigenvalues simultaneously.

## Final hierarchy status

`ACCEPTED`: the sampling-separation/rank theorem and the parity-filtered Pell
classification give genuine indexed restrictions.  `REJECTED` as a universal
positivity hierarchy: without added nonaliasing and component hypotheses, the
positive statement reduces to the same pointwise carré-du-champ residual with
different constants.  Finite sampling may kill or alias every continuous
component, and one selected combination is not a complete irreducible module.
