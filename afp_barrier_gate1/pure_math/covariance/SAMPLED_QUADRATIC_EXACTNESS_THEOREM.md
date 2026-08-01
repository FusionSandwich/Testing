# Sampled quadratic exactness for finite positive eigenmap generators

## Abstract

Let

\[
(Lf)(i)=\sum_j a_{ij}(f(j)-f(i))
\]

be a finite conservative jump generator and let
\(\Phi:I\to\mathbb R^d\) satisfy \(L\Phi=-\lambda\Phi\)
coordinatewise.  This note proves the exact covariance identity for sampled
quadratic forms, separates algebraic form exactness from genuine sampled
exactness, and gives the corrected dimension and rank formulas.  Its main
rigidity theorem is not a rank tautology: when every local jump covariance is
axially isotropic about the embedded node, every algebraically exact
trace-free quadratic form lies in the sampling kernel.  Hence the genuinely
sampled exact quadratic space is zero.  The theorem applies in every dimension
to regular simplices and in dimension three to all five Platonic
shortest-edge generators.  Exact symbolic calculations determine all form and
sampling dimensions.  A four-point signed generator shows that one negative
antipodal rate, necessarily of size \(1/2\), restores a nonzero sampled
quadratic mode.  Two independent product-obstruction proofs are also given.
A bounded spherical-harmonic product search does not produce a new hierarchy
beyond the one-function square mechanism and is therefore rejected under its
stated kill criterion.

All spaces and index sets below are finite-dimensional over \(\mathbb R\).
Repeated embedded nodes are permitted unless a distinct-neighbor hypothesis is
stated explicitly.

---

## 1. Finite covariance identity

Let \(I\) be a finite state set.  No reversibility is needed in this section.
For each state \(i\), let \(a_{ij}\in\mathbb R\).  Positivity is not needed for
the algebraic identity, although it is essential for the later rigidity and
product obstructions.  Put

\[
 \Delta_{ij}=\Phi_j-\Phi_i,
 \qquad
 C_i=\sum_j a_{ij}\Delta_{ij}\Delta_{ij}^{T}.                    \tag{1.1}
\]

For a matrix \(A\in\mathbb R^{d\times d}\), define

\[
 Q_A(i)=\Phi_i^T A\Phi_i.                                       \tag{1.2}
\]

Symmetry of \(A\) is not required for the identity, although only the
symmetric part contributes to \(Q_A\).

### Theorem 1.1 — exact quadratic covariance identity

Assume

\[
 L\Phi^{(r)}=-\lambda\Phi^{(r)}
 \quad\text{for every coordinate }r=1,\ldots,d.                 \tag{1.3}
\]

Then, at every state \(i\),

\[
 \boxed{
 LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^T C_i).
 }                                                               \tag{1.4}
\]

If \(A\) is symmetric, the contraction is \(\operatorname{tr}(AC_i)\).

**Proof.**  For fixed coordinates \(r,s\), write
\(\phi_r(i)=\Phi_i^{(r)}\).  One jump satisfies

\[
 \phi_r(j)\phi_s(j)-\phi_r(i)\phi_s(i)
 =\phi_r(i)\Delta_{ij}^{(s)}
  +\phi_s(i)\Delta_{ij}^{(r)}
  +\Delta_{ij}^{(r)}\Delta_{ij}^{(s)}.                           \tag{1.5}
\]

After multiplication by \(a_{ij}\) and summation in \(j\), the first two
terms are

\[
 \phi_r(i)L\phi_s(i)+\phi_s(i)L\phi_r(i)
 =-2\lambda\phi_r(i)\phi_s(i),                                  \tag{1.6}
\]

and the last term is \((C_i)_{rs}\).  Multiply by \(A_{rs}\) and sum over
\(r,s\).  This gives (1.4).  ∎

### Theorem 1.2 — target eigenvalue and constant shift

For \(c\in\mathbb R\), set

\[
 q_{A,c}(i)=Q_A(i)-c.                                            \tag{1.7}
\]

For any target \(\mu\in\mathbb R\), the following are equivalent:

\[
 Lq_{A,c}=-\mu q_{A,c};                                         \tag{1.8}
\]

\[
 \boxed{
 \operatorname{tr}(A^T C_i)
 +(\mu-2\lambda)Q_A(i)-\mu c=0
 \quad\text{for every }i.
 }                                                               \tag{1.9}
\]

This is necessary and sufficient and contains no sampling or nondegeneracy
assumption.

When \(\mu\ne0\), a constant \(c\) exists for a given \(A\) exactly when

\[
 i\longmapsto
 \operatorname{tr}(A^T C_i)+(\mu-2\lambda)Q_A(i)                \tag{1.10}
\]

is constant; then \(c\) is that constant divided by \(\mu\).  If \(L\) has an
invariant probability \(\pi\), \(\mu>0\), and (1.8) holds, then necessarily

\[
 c=\sum_i\pi_i Q_A(i).                                          \tag{1.11}
\]

Equation (1.11) follows by averaging (1.8), not from algebraic trace-freeness.
A trace-free form can have a nonzero mean on an arbitrary finite sample.

---

## 2. Sphere specialization and zero-centered form exactness

Assume now

\[
 \Phi_i\in S^{d-1},\qquad \lambda=d-1,\qquad \mu=2d,            \tag{2.1}
\]

and let

\[
 \operatorname{Sym}_0(d)
 =\{A=A^T:\operatorname{tr}A=0\}.                               \tag{2.2}
\]

For a symmetric matrix \(T\), define its trace-free projection

\[
 P_0(T)=T-\frac{\operatorname{tr}T}{d}I.                         \tag{2.3}
\]

Put

\[
 M_i=P_0\!\left(C_i+2\Phi_i\Phi_i^T\right).                     \tag{2.4}
\]

For \(A\in\operatorname{Sym}_0(d)\), trace-freeness gives

\[
 \langle A,M_i\rangle_F
 =\operatorname{tr}\!\left[A(C_i+2\Phi_i\Phi_i^T)\right].       \tag{2.5}
\]

The general shifted residual is therefore

\[
 Lq_{A,c}+2d q_{A,c}
 =\langle A,M_i\rangle_F-2dc.                                   \tag{2.6}
\]

The form space requested in this stage is the **zero-centered** form space
\(c=0\):

\[
 E_{\mathrm{form}}
 =\{A\in\operatorname{Sym}_0(d):LQ_A=-2dQ_A\}.                  \tag{2.7}
\]

### Theorem 2.1 — exact form-space characterization

\[
 \boxed{
 E_{\mathrm{form}}
 =\{A\in\operatorname{Sym}_0(d):
          \langle A,M_i\rangle_F=0\ \forall i\}
 =\operatorname{span}\{M_i:i\in I\}^{\perp}.
 }                                                               \tag{2.8}
\]

This statement concerns matrices.  It does not yet assert that a nonzero
matrix produces a nonzero function on the sampled nodes.

For shifted exactness, define

\[
 E_{\mathrm{form}}^{\mathrm{shift}}
 =\{A\in\operatorname{Sym}_0(d):
   (\langle A,M_i\rangle_F)_i\in\operatorname{span}\{\mathbf1\}\}.
                                                                    \tag{2.9}
\]

For \(A\) in this space, the admissible shift is the common value divided by
\(2d\).  Equation (2.9) must not be confused with (2.8).

---

## 3. Sampling kernel and genuine sampled exactness

Define the quadratic sampling map

\[
 S_X:\operatorname{Sym}_0(d)\longrightarrow\mathbb R^I,
 \qquad
 (S_XA)_i=\Phi_i^TA\Phi_i.                                      \tag{3.1}
\]

Its kernel is

\[
 K_X=\ker S_X.                                                   \tag{3.2}
\]

The following four notions are distinct:

1. \(A\ne0\) as a matrix;
2. \(A\ne0\) and \(A\in E_{\mathrm{form}}\);
3. \(S_XA\ne0\) as a sampled function;
4. \(S_XA\ne0\) and \(L(S_XA)=-2dS_XA\).

The tetrahedral, octahedral, and cubical examples below have nonzero matrices
of type 2 but none of type 4.

### Theorem 3.1 — genuine sampled exact space

The zero-centered genuinely sampled exact space is

\[
 \boxed{E_{\mathrm{sample}}=S_X(E_{\mathrm{form}}).}             \tag{3.3}
\]

The restriction of \(S_X\) to \(E_{\mathrm{form}}\) has kernel
\(E_{\mathrm{form}}\cap K_X\).  Rank-nullity gives

\[
 \boxed{
 \dim E_{\mathrm{sample}}
 =\dim E_{\mathrm{form}}
  -\dim(E_{\mathrm{form}}\cap K_X).
 }                                                               \tag{3.4}
\]

The incorrect expression
\(\dim E_{\mathrm{form}}-\dim K_X\) is valid only under an additional
containment hypothesis and is not used.

### Matrix rank formulas

Let

\[
 D=\dim\operatorname{Sym}_0(d)=\frac{d(d+1)}2-1                 \tag{3.5}
\]

and choose a basis \(B_1,\ldots,B_D\).  Define the covariance-constraint and
sampling matrices

\[
 R_{i\alpha}=\langle B_\alpha,M_i\rangle_F,
 \qquad
 S_{i\alpha}=\Phi_i^TB_\alpha\Phi_i.                            \tag{3.6}
\]

Then

\[
 \dim E_{\mathrm{form}}=D-\operatorname{rank}R,                 \tag{3.7}
\]

\[
 \dim(E_{\mathrm{form}}\cap K_X)
 =D-\operatorname{rank}\!\begin{bmatrix}R\\S\end{bmatrix},      \tag{3.8}
\]

and

\[
 \boxed{
 \dim E_{\mathrm{sample}}
 =\operatorname{rank}\!\begin{bmatrix}R\\S\end{bmatrix}
  -\operatorname{rank}R.
 }                                                               \tag{3.9}
\]

If \(N\) is any matrix whose columns form a basis of \(\ker R\), then also

\[
 \dim E_{\mathrm{sample}}=\operatorname{rank}(SN).              \tag{3.10}
\]

Every dimension assertion below is a statement about (3.3), unless it is
explicitly labeled as a form-space assertion.

---

## 4. Sharp axial-covariance rigidity

A rank identity alone does not explain why the sampled space vanishes in the
symmetric examples.  The following local-to-global theorem does.

For \(x\in S^{d-1}\), write

\[
 P_x^{\mathrm{rad}}=xx^T,
 \qquad
 P_x^{\mathrm{tan}}=I-xx^T.                                     \tag{4.1}
\]

A covariance tensor is **axially isotropic at** \(x\) if

\[
 C=\tau P_x^{\mathrm{tan}}+\beta P_x^{\mathrm{rad}}             \tag{4.2}
\]

for some scalars \(\tau,\beta\).  Here

\[
 \beta=x^TCx.                                                    \tag{4.3}
\]

### Lemma 4.1 — trace and radial covariance

For a unit-sphere eigenmap with eigenvalue \(-(d-1)\),

\[
 \operatorname{tr}C_i=2(d-1).                                   \tag{4.4}
\]

Indeed,

\[
 \begin{aligned}
 \operatorname{tr}C_i
 &=\sum_j a_{ij}\|\Phi_j-\Phi_i\|^2\\
 &=-2\Phi_i\cdot\sum_j a_{ij}(\Phi_j-\Phi_i)
 =2(d-1).
 \end{aligned}                                                   \tag{4.5}
\]

If \(a_{ij}\ge0\), then

\[
 \beta_i=\Phi_i^TC_i\Phi_i
 =\sum_j a_{ij}(1-\Phi_i\cdot\Phi_j)^2\ge0.                    \tag{4.6}
\]

It is strictly positive exactly when at least one positive outgoing jump goes
to a distinct embedded point.

### Theorem 4.2 — local axial constraint equals sampled value

Assume \(d\ge2\), (2.1), nonnegative rates, axial isotropy (4.2) at a state
\(i\), and \(\beta_i>0\).  Then

\[
 \boxed{
 M_i=\frac{d\beta_i}{d-1}
 \left(\Phi_i\Phi_i^T-\frac1dI\right).
 }                                                               \tag{4.7}
\]

Consequently, for every \(A\in\operatorname{Sym}_0(d)\),

\[
 \boxed{
 \langle A,M_i\rangle_F
 =\frac{d\beta_i}{d-1}\,\Phi_i^TA\Phi_i.
 }                                                               \tag{4.8}
\]

Thus exactness at this one vertex is equivalent to vanishing of the sampled
quadratic at this vertex.

**Proof.**  Write
\(C_i=\tau_i(I-xx^T)+\beta_i xx^T\), \(x=\Phi_i\).  Equation (4.4) gives

\[
 (d-1)\tau_i+\beta_i=2(d-1),
 \qquad
 \tau_i=2-\frac{\beta_i}{d-1}.                                  \tag{4.9}
\]

Therefore

\[
 C_i+2xx^T
 =\tau_iI+(\beta_i-\tau_i+2)xx^T,
\]

and

\[
 \beta_i-\tau_i+2=\frac{d\beta_i}{d-1}.                         \tag{4.10}
\]

The trace-free projection of \(\tau I+\kappa xx^T\) is
\(\kappa(xx^T-I/d)\), proving (4.7).  Pairing with trace-free \(A\) gives
(4.8).  ∎

### Theorem 4.3 — sharp global sampled rigidity

Assume the hypotheses of Theorem 4.2 at every state.  Then the constraint
matrix is obtained from the sampling matrix by multiplying row \(i\) by the
strictly positive scalar \(d\beta_i/(d-1)\).  Hence

\[
 \boxed{E_{\mathrm{form}}=K_X,}                                 \tag{4.11}
\]

\[
 \boxed{\operatorname{rank}R=\operatorname{rank}S,}             \tag{4.12}
\]

and

\[
 \boxed{E_{\mathrm{sample}}=\{0\}.}                             \tag{4.13}
\]

This is a structural rigidity theorem, not the tautological rank formula.  It
also distinguishes local and global exactness: axial isotropy at only a subset
\(J\subset I\) forces an exact sampled mode to vanish on \(J\), but not
necessarily outside \(J\).

If the coefficients \(d\beta_i/(d-1)\) are all the same and the finite sample
has zero mean for every trace-free quadratic, then the same conclusion holds
for shifted exactness.  In that case (2.6) forces the quadratic sample to be
constant, and zero mean forces that constant to be zero.

### Corollary 4.4 — regular simplex family in every dimension

Let \(x_0,\ldots,x_d\in S^{d-1}\) be a regular simplex:

\[
 x_i\cdot x_j=-\frac1d\quad(i\ne j),
 \qquad
 \sum_i x_i=0.                                                   \tag{4.14}
\]

On the complete graph, set

\[
 a_{ij}=\frac{d-1}{d+1}\quad(i\ne j).                           \tag{4.15}
\]

Then \(Lx=-(d-1)x\), every covariance is axially isotropic, and

\[
 M_i=(d+1)\left(x_ix_i^T-\frac1dI\right).                       \tag{4.16}
\]

The sampling map has rank exactly \(d\).  Indeed, its image lies in the
zero-sum subspace because

\[
 \sum_i x_ix_i^T=\frac{d+1}{d}I.                                \tag{4.17}
\]

Conversely, for any \(y\in\mathbb R^{d+1}\) with \(\sum_i y_i=0\),

\[
 A_y=\frac{d^2}{d^2-1}\sum_i y_i x_ix_i^T                       \tag{4.18}
\]

is trace-free and satisfies \(x_k^TA_yx_k=y_k\).  Hence

\[
 \operatorname{rank}S_X=d,                                      \tag{4.19}
\]

\[
 \dim E_{\mathrm{form}}
 =\dim K_X
 =\frac{d(d+1)}2-1-d,                                           \tag{4.20}
\]

while \(\dim E_{\mathrm{sample}}=0\).  This all-dimensional family attains
the axial theorem sharply and exhibits a large algebraic exact space composed
entirely of sampling aliases.

### Theorem 4.5 — equivariant irreducibility rigidity

There is a second structural mechanism.  Let a finite group \(G\) act
transitively on \(I\), let \(\rho:G\to O(d)\), and assume

\[
 \Phi_{gi}=\rho(g)\Phi_i,
 \qquad
 a_{gi,gj}=a_{ij}.                                               \tag{4.21}
\]

Then \(E_{\mathrm{form}}\subset\operatorname{Sym}_0(d)\) is a
\(G\)-submodule under \(A\mapsto\rho(g)A\rho(g)^T\).  If
\(\operatorname{Sym}_0(d)\) is irreducible as a real \(G\)-module and at
least one positive jump joins distinct embedded points, then

\[
 \boxed{E_{\mathrm{form}}=\{0\}.}                               \tag{4.22}
\]

Indeed, irreducibility makes \(E_{\mathrm{form}}\) either zero or the full
module.  The full alternative would force every \(M_i=0\).  Then
\(C_i+2\Phi_i\Phi_i^T\) would be scalar.  Its trace is \(2d\), so

\[
 C_i=2(I-\Phi_i\Phi_i^T),                                       \tag{4.23}
\]

whose radial covariance is zero, contradicting (4.6).  This theorem explains
the full-rank icosahedral cases independently of an evaluation determinant.

---

## 5. Exact Platonic classification

Use the standard unit vertex embeddings in \(S^2\), the shortest-edge graph,
and one common rate on every edge, normalized so that

\[
 L\Phi=-2\Phi.                                                   \tag{5.1}
\]

Let \(k\) be the degree and \(\alpha\) the adjacent inner product.  The rate
is

\[
 r=\frac{2}{k(1-\alpha)}.                                       \tag{5.2}
\]

The vertex stabilizer contains a rotation of order at least three about the
radial axis.  Therefore \(C_i\) is axially isotropic.  Equations (4.4) and
(4.6) determine it exactly:

\[
 \boxed{
 C_i=(1+\alpha)I+(1-3\alpha)\Phi_i\Phi_i^T,
 }                                                               \tag{5.3}
\]

\[
 \boxed{
 M_i=3(1-\alpha)
 \left(\Phi_i\Phi_i^T-\frac13I\right).
 }                                                               \tag{5.4}
\]

Thus the constraint and sampling row spaces coincide exactly.

| Graph | \(k\) | \(\alpha\) | edge rate \(r\) | scalar in (5.4) |
|---|---:|---:|---:|---:|
| tetrahedron | 3 | \(-1/3\) | \(1/2\) | \(4\) |
| octahedron | 4 | \(0\) | \(1/2\) | \(3\) |
| cube | 3 | \(1/3\) | \(1\) | \(2\) |
| icosahedron | 5 | \(1/\sqrt5\) | \((5+\sqrt5)/10\) | \(3(1-1/\sqrt5)\) |
| dodecahedron | 3 | \(\sqrt5/3\) | \((3+\sqrt5)/2\) | \(3-\sqrt5\) |

### Exact sampling ranks

Represent a trace-free symmetric matrix by coefficients in

\[
 x^2-z^2,\quad y^2-z^2,\quad 2xy,\quad 2xz,\quad 2yz.             \tag{5.5}
\]

- **Tetrahedron and cube.**  Every vertex has
  \(x^2=y^2=z^2=1/3\), so the two-dimensional diagonal trace-free subspace is
  in \(K_X\).  The sign vectors of \((xy,xz,yz)\) span \(\mathbb R^3\), so
  the sampling rank is three.  Hence \(\dim K_X=2\).
- **Octahedron.**  Sampling at \(\pm e_1,\pm e_2,\pm e_3\) detects the
  two-dimensional diagonal trace-free subspace and kills all three
  off-diagonal forms.  Hence the sampling rank is two and
  \(\dim K_X=3\).
- **Icosahedron.**  Let \(\varphi=(1+\sqrt5)/2\).  On the five raw vertices

  \[
  (0,1,\varphi),\ (0,-1,\varphi),\ (1,\varphi,0),\
  (-1,\varphi,0),\ (\varphi,0,1),                               \tag{5.6}
  \]

  the evaluation determinant in basis (5.5) is

  \[
  32(11+5\sqrt5)\ne0.                                           \tag{5.7}
  \]

  Common normalization of the vertices only rescales rows, so the full
  sampling rank is five.
- **Dodecahedron.**  On the five raw vertices

  \[
  (-1,-1,-1),\ (-1,-1,1),\ (-1,1,-1),\
  (0,-\varphi^{-1},-\varphi),\
  (-\varphi^{-1},-\varphi,0),                                   \tag{5.8}
  \]

  the corresponding determinant is

  \[
  -192\ne0.                                                      \tag{5.9}
  \]

  Thus the sampling rank is five.

Combining these exact ranks with Theorem 4.3 gives:

| Graph | \(\operatorname{rank}\operatorname{span}\{M_i\}\) | \(\dim E_{\mathrm{form}}\) | \(\dim K_X\) | \(\dim E_{\mathrm{sample}}\) |
|---|---:|---:|---:|---:|
| tetrahedron | 3 | 2 | 2 | 0 |
| octahedron | 2 | 3 | 3 | 0 |
| cube | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 0 | 0 | 0 |

For the first three graphs,

\[
 E_{\mathrm{form}}=K_X\ne\{0\};                                \tag{5.10}
\]

all apparent exact forms vanish on every sampled vertex.  For the last two,
there are no nonzero exact forms at all.  Consequently none of the five
positive generators has a nonzero sampled degree-two mode with eigenvalue
\(-6\).

The equal-weight Platonic vertex sets are spherical 2-designs.  Since the
coefficient in (5.4) is constant on each graph, the shifted condition (2.6)
forces a trace-free quadratic sample to be constant; its zero mean then forces
it to vanish.  Thus allowing \(c\) does not restore a genuine sampled mode in
these examples.

---

## 6. Signed-conductance restoration and minimal negativity

Positivity is essential.  Consider the four points on \(S^1\)

\[
 x_0=(1,0),\quad x_1=(0,1),\quad x_2=(-1,0),\quad x_3=(0,-1).    \tag{6.1}
\]

In cyclic order, assign rate \(1\) to each adjacent point and rate
\(-1/2\) to the antipodal point.  The generator matrix is

\[
 L=
 \begin{pmatrix}
 -3/2&1&-1/2&1\\
 1&-3/2&1&-1/2\\
 -1/2&1&-3/2&1\\
 1&-1/2&1&-3/2
 \end{pmatrix}.                                                  \tag{6.2}
\]

It is symmetric and conservative.  For the coordinate samples

\[
 X=(1,0,-1,0)^T,
 \qquad
 Y=(0,1,0,-1)^T,                                                 \tag{6.3}
\]

and the trace-free quadratic sample

\[
 Q=X^2-Y^2=(1,-1,1,-1)^T,                                       \tag{6.4}
\]

one has exactly

\[
 LX=-X,\qquad LY=-Y,\qquad LQ=-4Q.                               \tag{6.5}
\]

Thus the signed generator reproduces the coordinate eigenvalue
\(-(d-1)=-1\) and a genuine nonzero quadratic eigenvalue \(-2d=-4\).
The second trace-free quadratic \(2XY\) lies in the sampling kernel of these
four nodes, so the restored sampled quadratic space is one-dimensional.

The negative rate is forced, not an arbitrary unconstrained solve.  At
\(x_0\), write the rates to \(x_1,x_2,x_3\) as \(u,b,v\).  The two coordinate
equations and the quadratic equation are

\[
 u+v+2b=1,\qquad u-v=0,\qquad u+v=2.                             \tag{6.6}
\]

Therefore

\[
 \boxed{u=v=1,\qquad b=-\frac12.}                                \tag{6.7}
\]

The same argument applies at every vertex.  Hence every generator on this
fixed four-point support satisfying the three exactness requirements has one
negative antipodal rate of magnitude \(1/2\) per row.  With equal reversible
masses, there are exactly two negative undirected conductances, each
\(-1/2\), and total negative undirected mass one.

---

## 7. Independent finite-product obstructions

### 7.1 Carré-du-champ proof

For nonnegative rates define

\[
 \Gamma(f,g)(i)
 =\frac12\sum_j a_{ij}(f(j)-f(i))(g(j)-g(i)).                    \tag{7.1}
\]

Direct expansion gives

\[
 L(fg)-fLg-gLf=2\Gamma(f,g).                                    \tag{7.2}
\]

If

\[
 Lf=-\lambda f,\qquad Lg=-\nu g,\qquad
 L(fg)=-(\lambda+\nu)fg,                                        \tag{7.3}
\]

then

\[
 \Gamma(f,g)=0                                                   \tag{7.4}
\]

at every state.

At a state where \(f\) and \(g\) have aligned extrema, every summand in
(7.1) is nonnegative.  If at least one positive outgoing edge changes both
values strictly in the same direction, then \(\Gamma(f,g)>0\), contradicting
(7.4).  This is the strict-extremum product obstruction.

For \(g=f\),

\[
 2\Gamma(f,f)(i)=\sum_j a_{ij}(f(j)-f(i))^2.                     \tag{7.5}
\]

Thus exact additive square propagation

\[
 L(f^2)=-2\lambda f^2                                           \tag{7.6}
\]

forces \(f(j)=f(i)\) on every positive active edge.  On every directed
reachable component \(f\) is constant.  If the chain is irreducible and
\(\lambda>0\), the only possibility is \(f=0\).

This theorem concerns the sampled square itself.  It does not automatically
apply to one algebraic harmonic component of a square when other components
remain present or are aliased by sampling.

### 7.2 Semigroup/Jensen proof

Let \(P_t=e^{tL}\).  For nonnegative conservative rates, \(P_t\) is a Markov
operator.  If \(Lf=-\lambda f\), then

\[
 P_tf=e^{-\lambda t}f.                                          \tag{7.7}
\]

Jensen's inequality gives

\[
 P_t(f^2)(i)\ge(P_tf(i))^2.                                     \tag{7.8}
\]

If also (7.6) holds, then

\[
 P_t(f^2)=e^{-2\lambda t}f^2=(P_tf)^2,                           \tag{7.9}
\]

so equality holds in Jensen at every state.

Write \(p_t(i,j)\) for the transition kernel.  Equality in the strictly
convex square inequality is equivalent to

\[
 f(j)=f(k)
 \quad\text{whenever }p_t(i,j)>0\text{ and }p_t(i,k)>0.          \tag{7.10}
\]

For a finite continuous-time chain and \(t>0\), uniformization shows that
\(p_t(i,j)>0\) exactly when \(j\) is reachable from \(i\) along positive-rate
edges.  Hence equality characterizes constancy on every reachable set.  An
irreducible positive chain again forces \(f\) constant and, for
\(\lambda>0\), zero.

The carré-du-champ proof is infinitesimal and edgewise.  The semigroup proof is
global in time and identifies equality on the entire reachable set.  Neither
proof assumes reversibility.

---

## 8. Bounded spherical spectral-product search

Let \(\mathcal H_\ell(S^{d-1})\) denote degree-\(\ell\) spherical harmonics,
with eigenvalue

\[
 \lambda_\ell=\ell(\ell+d-2).                                   \tag{8.1}
\]

### 8.1 Parity and multiplication image

A degree-\(\ell\) harmonic has antipodal parity \((-1)^\ell\), so a product
of two degree-\(\ell\) harmonics is always even.  For \(d\ge3\), the scalar
harmonic part of the pointwise multiplication image is

\[
 \mathcal H_{2\ell}\oplus
 \mathcal H_{2\ell-2}\oplus\cdots\oplus\mathcal H_0.           \tag{8.2}
\]

For \(d=2\), the product image is only
\(\mathcal H_{2\ell}\oplus\mathcal H_0\).  Statement (8.2) concerns the
pointwise multiplication image; the abstract representation
\(\operatorname{Sym}^2(\mathcal H_\ell)\) can contain additional tensor
components that multiplication kills.

### 8.2 Odd and even zonal extrema

For a normalized zonal harmonic \(Z_\ell(x\cdot p)\), equality in the global
bound occurs at both antipodes.  If \(\ell\) is odd, the values at \(p\) and
\(-p\) have opposite signs; if \(\ell\) is even, both are equal maxima.
The square has the same value at both antipodes in either case.  Therefore a
single-point strict-maximum argument must assume an active edge leaving the
entire equality set.  Non-singleton maximizing sets cannot be silently treated
as one point.

### 8.3 Sampling aliases

For every harmonic degree \(k\), let

\[
 S_{X,k}:\mathcal H_k\to\mathbb R^I                             \tag{8.3}
\]

be the sampling map.  An algebraically nonzero product component can lie in
\(\ker S_{X,k}\), and two different degrees can have identical sampled
vectors.  Exactness of one algebraic component is therefore not a claim about
a nonzero sampled function unless its sampling class is identified.  Exactness
of one sampled combination also does not imply exactness of a complete
irreducible component unless an equivariance and irreducibility argument is
supplied.

### 8.4 Additive resonance does not create a hierarchy

The square/Jensen obstruction directly applies to a product component only if
its sampled eigenvalue equals the additive value \(2\lambda_\ell\) **and** all
other sampled components of the square vanish or are otherwise identified.
The arithmetic condition is

\[
 k(k+d-2)=2\ell(\ell+d-2),
 \qquad k\in\{0,2,\ldots,2\ell\}.                               \tag{8.4}
\]

It is not satisfied by a uniform choice such as \(k=2\ell\).  An exact bounded
search over

\[
 2\le d\le12,\qquad1\le\ell\le12                                \tag{8.5}
\]

finds only

\[
 (d,\ell,k)=(4,4,6),(6,8,12),(8,12,18),(9,5,8).                 \tag{8.6}
\]

These sparse arithmetic coincidences do not produce an \(\ell\)-indexed
family, dimension tradeoff, or global rigidity consequence.  Even at a hit,
the basic Jensen proof applies only after the other sampled product components
are shown to vanish or alias, reducing the argument to the same one-function
square identity.

### Conclusion of the hierarchy branch

Under the stated kill criterion, the proposed general spectral-product
hierarchy is

\[
 \boxed{\text{REJECTED for this stage}.}                         \tag{8.7}
\]

The bounded investigation produced no theorem beyond the additive sampled
square obstruction.  This does not claim that no stronger hierarchy can ever
exist under additional representation-theoretic or design hypotheses; it
prevents the current calculations from being inflated into such a theorem.
The mandatory stage result is the sampled covariance theorem and axial
rigidity above.

---

## 9. Verification boundary

`quadratic_covariance_audit.py` performs exact symbolic checks over
\(\mathbb Q(\sqrt5)\).  It verifies:

- the covariance identity against direct generator action;
- every covariance tensor and scalar in the Platonic table;
- exact matrix ranks and both nonzero evaluation determinants;
- equality of form space and sampling kernel in the axial examples;
- the correct stacked-rank formula, including a negative test for the naive
  dimension subtraction;
- the signed four-point construction and the forced rate \(-1/2\); and
- the bounded resonance list (8.6).

These calculations are deterministic regression and falsification tools.  The
proofs of the general statements are the arguments above.  The finite
covariance algebra, trace-free projection consequence, and scaled
constraint-to-sampling implication are formalized separately in Lean.
