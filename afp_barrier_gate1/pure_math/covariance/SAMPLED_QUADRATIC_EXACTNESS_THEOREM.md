# Sampled quadratic exactness for finite positive eigenmap generators

## Abstract

Let

\[
(Lf)(i)=\sum_j a_{ij}(f(j)-f(i))
\]

be a finite conservative jump generator and let
\(\Phi:I\to\mathbb R^d\) satisfy \(L\Phi=-\lambda\Phi\)
coordinatewise. This note proves the exact covariance identity for sampled
quadratic forms and separates algebraic form exactness from genuine sampled
exactness. The key structural relation is

\[
R_X=(L+2dI)S_X
\]

in the spherical degree-two specialization. Consequently the quadratic
sampling kernel is always contained in the exact-form kernel, and the genuine
sampled exact space is

\[
\operatorname{im}S_X\cap\ker(L+2dI).
\]

The principal rigidity theorem is not rank bookkeeping: if every local jump
covariance is axially isotropic about its embedded node and has positive radial
variance, every algebraically exact trace-free quadratic form lies in the
sampling kernel. Thus the genuinely sampled exact quadratic space is zero.
The theorem applies in every dimension to regular simplices and in dimension
three to all five Platonic shortest-edge generators. Exact symbolic proofs
determine their form and sampling dimensions. A four-point signed generator
shows that a negative antipodal rate, necessarily of magnitude \(1/2\),
restores a nonzero sampled quadratic mode. Two independent product-obstruction
proofs are also given. A bounded parity, equality-set, aliasing, and resonance
audit produces no nontrivial spectral-product hierarchy beyond the
one-function square mechanism, so that branch is rejected under its stated
kill criterion.

All vector spaces are finite-dimensional over \(\mathbb R\). Repeated
embedded points are allowed unless a distinct-neighbor hypothesis is stated.

---

## 1. Exact covariance identity and target residual

Let \(I\) be finite. No positivity or reversibility is needed for the algebra
in this section. Put

\[
\Delta_{ij}=\Phi_j-\Phi_i,
\qquad
C_i=\sum_j a_{ij}\Delta_{ij}\Delta_{ij}^{T}.                    \tag{1.1}
\]

For \(A\in\mathbb R^{d\times d}\), define

\[
Q_A(i)=\Phi_i^TA\Phi_i.                                         \tag{1.2}
\]

Only the symmetric part of \(A\) contributes to \(Q_A\), but symmetry is not
needed for the coordinate identity.

### Theorem 1.1 — finite quadratic covariance identity

Assume

\[
L\Phi^{(r)}=-\lambda\Phi^{(r)}
\quad(r=1,\ldots,d).                                             \tag{1.3}
\]

Then for every state \(i\),

\[
\boxed{
LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^TC_i).
}                                                               \tag{1.4}
\]

For symmetric \(A\), the contraction is \(\operatorname{tr}(AC_i)\).

**Proof.** For coordinates \(r,s\), write
\(\phi_r(i)=\Phi_i^{(r)}\). One jump satisfies

\[
\phi_r(j)\phi_s(j)-\phi_r(i)\phi_s(i)
 =\phi_r(i)\Delta_{ij}^{(s)}
  +\phi_s(i)\Delta_{ij}^{(r)}
  +\Delta_{ij}^{(r)}\Delta_{ij}^{(s)}.                           \tag{1.5}
\]

After multiplying by \(a_{ij}\) and summing in \(j\), the first two terms are

\[
\phi_r(i)L\phi_s(i)+\phi_s(i)L\phi_r(i)
=-2\lambda\phi_r(i)\phi_s(i),                                  \tag{1.6}
\]

and the last is \((C_i)_{rs}\). Multiplication by \(A_{rs}\) and summation
in \(r,s\) gives (1.4). ∎

### Theorem 1.2 — shifted target eigenvalue

For \(c\in\mathbb R\), set

\[
q_{A,c}(i)=Q_A(i)-c.                                             \tag{1.7}
\]

For any target \(\mu\in\mathbb R\), the following are equivalent:

\[
Lq_{A,c}=-\mu q_{A,c};                                          \tag{1.8}
\]

\[
\boxed{
\operatorname{tr}(A^TC_i)
 +(\mu-2\lambda)Q_A(i)-\mu c=0
\quad\text{for every }i.
}                                                               \tag{1.9}
\]

Thus the condition is necessary and sufficient with no hidden sampling
assumption. When \(\mu\ne0\), a shift exists for a fixed \(A\) exactly when

\[
i\longmapsto
\operatorname{tr}(A^TC_i)+(\mu-2\lambda)Q_A(i)                  \tag{1.10}
\]

is constant, and the shift is that constant divided by \(\mu\). If \(L\)
has an invariant probability \(\pi\), \(\mu>0\), and (1.8) holds, averaging
gives

\[
c=\sum_i\pi_iQ_A(i).                                           \tag{1.11}
\]

Trace-freeness of \(A\) alone does not force this finite-sample mean to be
zero.

---

## 2. Spherical trace-free form space

Assume

\[
\Phi_i\in S^{d-1},\qquad \lambda=d-1,\qquad \mu=2d,             \tag{2.1}
\]

and let

\[
\operatorname{Sym}_0(d)
 =\{A=A^T:\operatorname{tr}A=0\}.                               \tag{2.2}
\]

For a symmetric matrix \(T\), define

\[
P_0(T)=T-\frac{\operatorname{tr}T}{d}I,                          \tag{2.3}
\]

and put

\[
M_i=P_0(C_i+2\Phi_i\Phi_i^T).                                   \tag{2.4}
\]

For trace-free symmetric \(A\),

\[
\langle A,M_i\rangle_F
 =\operatorname{tr}[A(C_i+2\Phi_i\Phi_i^T)].                    \tag{2.5}
\]

The shifted residual becomes

\[
Lq_{A,c}(i)+2d q_{A,c}(i)
 =\langle A,M_i\rangle_F-2dc.                                   \tag{2.6}
\]

Define the zero-centered form space

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

This is a matrix-space statement. It does not assert that a nonzero matrix
produces a nonzero sampled function.

For shifted exactness, the corresponding matrix set is

\[
E_{\mathrm{form}}^{\mathrm{shift}}
 =\{A\in\operatorname{Sym}_0(d):
   (\langle A,M_i\rangle_F)_i\in\operatorname{span}\{\mathbf1\}\}.
                                                                    \tag{2.9}
\]

For such \(A\), the shift is the common value divided by \(2d\). The affine
condition (2.9) is separate from the linear zero-centered space (2.8).

---

## 3. Sampling factorization and genuine sampled exactness

Define the quadratic sampling map

\[
S_X:\operatorname{Sym}_0(d)\to\mathbb R^I,
\qquad
(S_XA)_i=\Phi_i^TA\Phi_i,                                      \tag{3.1}
\]

and its kernel

\[
K_X=\ker S_X.                                                    \tag{3.2}
\]

Let

\[
B=L+2dI:\mathbb R^I\to\mathbb R^I                               \tag{3.3}
\]

and define the covariance-residual map

\[
R_X:\operatorname{Sym}_0(d)\to\mathbb R^I,
\qquad
(R_XA)_i=\langle A,M_i\rangle_F.                                \tag{3.4}
\]

The covariance identity gives the exact operator factorization

\[
\boxed{R_X=B\,S_X.}                                             \tag{3.5}
\]

Consequently,

\[
E_{\mathrm{form}}=\ker R_X,                                    \tag{3.6}
\]

and, crucially,

\[
\boxed{K_X=\ker S_X\subseteq\ker R_X=E_{\mathrm{form}}.}        \tag{3.7}
\]

An algebraically nonzero sampling alias is therefore always a zero-centered
exact form, because it represents the zero sampled function.

The following notions must remain distinct:

1. \(A\ne0\) as a matrix;
2. \(A\ne0\) and \(A\in E_{\mathrm{form}}\);
3. \(S_XA\ne0\) as a sampled function;
4. \(S_XA\ne0\) and \(B(S_XA)=0\).

### Theorem 3.1 — exact sampled space

The genuinely sampled exact space is

\[
\boxed{
E_{\mathrm{sample}}=S_X(E_{\mathrm{form}})
 =\operatorname{im}S_X\cap\ker(L+2dI).
}                                                               \tag{3.8}
\]

**Proof.** If \(f=S_XA\) with \(A\in\ker(BS_X)\), then
\(f\in\operatorname{im}S_X\) and \(Bf=0\). Conversely, if
\(f=S_XA\in\ker B\), then \(A\in\ker(BS_X)=E_{\mathrm{form}}\). ∎

The general restriction-map identity requested in this stage is

\[
\dim E_{\mathrm{sample}}
 =\dim E_{\mathrm{form}}
  -\dim(E_{\mathrm{form}}\cap K_X).                              \tag{3.9}
\]

Because of (3.7), the intersection is exactly \(K_X\), so in this covariance
problem the sharper specialized formula is

\[
\boxed{
\dim E_{\mathrm{sample}}
 =\dim E_{\mathrm{form}}-\dim K_X.
}                                                               \tag{3.10}
\]

Choose a basis \(B_1,\ldots,B_D\) of \(\operatorname{Sym}_0(d)\), where

\[
D=\frac{d(d+1)}2-1.                                             \tag{3.11}
\]

Let

\[
R_{i\alpha}=\langle B_\alpha,M_i\rangle_F,
\qquad
S_{i\alpha}=\Phi_i^TB_\alpha\Phi_i.                            \tag{3.12}
\]

If \(G\) is the matrix of \(L\), then

\[
\boxed{R=(G+2dI)S.}                                             \tag{3.13}
\]

Hence the row space of \(R\) is contained in the row space of \(S\),

\[
\operatorname{rank}R\le\operatorname{rank}S,                   \tag{3.14}
\]

and

\[
\boxed{
\dim E_{\mathrm{sample}}
 =\operatorname{rank}S-\operatorname{rank}R.
}                                                               \tag{3.15}
\]

The stacked-matrix version remains valid and collapses exactly:

\[
\operatorname{rank}\!\begin{bmatrix}R\\S\end{bmatrix}
 =\operatorname{rank}S,                                        \tag{3.16}
\]

so

\[
\dim E_{\mathrm{sample}}
 =\operatorname{rank}\!\begin{bmatrix}R\\S\end{bmatrix}
  -\operatorname{rank}R.                                       \tag{3.17}
\]

If \(N\) has columns spanning \(\ker R\), then

\[
\dim E_{\mathrm{sample}}=\operatorname{rank}(SN).              \tag{3.18}
\]

Every later dimension claim concerns \(E_{\mathrm{sample}}\) unless it is
explicitly labeled as form space.

---

## 4. Sharp axial-covariance rigidity

For \(x\in S^{d-1}\), write

\[
P_x^{\mathrm{rad}}=xx^T,
\qquad
P_x^{\mathrm{tan}}=I-xx^T.                                     \tag{4.1}
\]

A covariance is axially isotropic at \(x\) if

\[
C=\tau P_x^{\mathrm{tan}}+\beta P_x^{\mathrm{rad}}.             \tag{4.2}
\]

Here \(\beta=x^TCx\).

### Lemma 4.1 — trace and radial covariance

For a unit-sphere coordinate eigenmap with eigenvalue \(-(d-1)\),

\[
\operatorname{tr}C_i=2(d-1).                                   \tag{4.3}
\]

Indeed,

\[
\operatorname{tr}C_i
 =\sum_j a_{ij}\|\Phi_j-\Phi_i\|^2
 =-2\Phi_i\cdot\sum_j a_{ij}(\Phi_j-\Phi_i)
 =2(d-1).                                                       \tag{4.4}
\]

If \(a_{ij}\ge0\), then

\[
\beta_i=\Phi_i^TC_i\Phi_i
 =\sum_j a_{ij}(1-\Phi_i\cdot\Phi_j)^2\ge0.                    \tag{4.5}
\]

It is strictly positive exactly when at least one positive outgoing jump goes
to a distinct embedded point.

### Theorem 4.2 — local axial constraint

Assume \(d\ge2\), nonnegative rates, axial isotropy at state \(i\), and
\(\beta_i>0\). Then

\[
\boxed{
M_i=\frac{d\beta_i}{d-1}
 \left(\Phi_i\Phi_i^T-\frac1dI\right).
}                                                               \tag{4.6}
\]

Consequently, for every \(A\in\operatorname{Sym}_0(d)\),

\[
\boxed{
\langle A,M_i\rangle_F
 =\frac{d\beta_i}{d-1}\Phi_i^TA\Phi_i.
}                                                               \tag{4.7}
\]

Thus zero-centered quadratic exactness at this vertex is equivalent to
vanishing of the sampled quadratic at this vertex.

**Proof.** Write \(x=\Phi_i\). The trace identity gives

\[
(d-1)\tau_i+\beta_i=2(d-1),
\qquad
\tau_i=2-\frac{\beta_i}{d-1}.                                  \tag{4.8}
\]

Now

\[
C_i+2xx^T=\tau_iI+(\beta_i-\tau_i+2)xx^T,
\]

with

\[
\beta_i-\tau_i+2=\frac{d\beta_i}{d-1}.                         \tag{4.9}
\]

Taking the trace-free projection proves (4.6), and pairing with trace-free
\(A\) proves (4.7). ∎

### Theorem 4.3 — global sampled rigidity

Assume Theorem 4.2 at every state. The constraint matrix is a strictly
positive row scaling of the sampling matrix. Hence

\[
\boxed{E_{\mathrm{form}}=K_X,}                                 \tag{4.10}
\]

\[
\boxed{\operatorname{rank}R=\operatorname{rank}S,}             \tag{4.11}
\]

and

\[
\boxed{E_{\mathrm{sample}}=\{0\}.}                             \tag{4.12}
\]

This improves on the rank identity: axial local geometry identifies the whole
form kernel as sampling alias. If axial isotropy holds only on a subset
\(J\subset I\), an exact sampled quadratic must vanish on \(J\), but the
theorem makes no claim outside \(J\).

If the row-scaling coefficient is constant and the sample average of every
trace-free quadratic is zero, the same conclusion holds for shifted exactness:
(2.6) makes the sample constant, and zero average makes it zero.

### Corollary 4.4 — regular simplices in every dimension

Let \(x_0,\ldots,x_d\in S^{d-1}\) be a regular simplex:

\[
x_i\cdot x_j=-\frac1d\quad(i\ne j),
\qquad
\sum_i x_i=0.                                                   \tag{4.13}
\]

On the complete graph set

\[
a_{ij}=\frac{d-1}{d+1}\quad(i\ne j).                           \tag{4.14}
\]

Then \(Lx=-(d-1)x\), every covariance is axially isotropic, and

\[
M_i=(d+1)\left(x_ix_i^T-\frac1dI\right).                       \tag{4.15}
\]

The sampling map has rank exactly \(d\). Its image lies in the zero-sum
subspace because

\[
\sum_i x_ix_i^T=\frac{d+1}{d}I.                                \tag{4.16}
\]

Conversely, for any \(y\in\mathbb R^{d+1}\) with \(\sum_i y_i=0\),

\[
A_y=\frac{d^2}{d^2-1}\sum_i y_i x_ix_i^T                       \tag{4.17}
\]

is trace-free and satisfies \(x_k^TA_yx_k=y_k\). Therefore

\[
\operatorname{rank}S_X=d,                                      \tag{4.18}
\]

\[
\dim E_{\mathrm{form}}=\dim K_X
 =\frac{d(d+1)}2-1-d,                                           \tag{4.19}
\]

and \(\dim E_{\mathrm{sample}}=0\). This all-dimensional equality family
has a large nonzero algebraic exact space consisting entirely of sampling
aliases.

### Theorem 4.5 — equivariant irreducibility rigidity

Let a finite group \(G\) act transitively on \(I\), let
\(\rho:G\to O(d)\), and assume

\[
\Phi_{gi}=\rho(g)\Phi_i,
\qquad
a_{gi,gj}=a_{ij}.                                               \tag{4.20}
\]

Then \(E_{\mathrm{form}}\) is a \(G\)-submodule of
\(\operatorname{Sym}_0(d)\) under conjugation. If this representation is
irreducible over \(\mathbb R\) and at least one positive jump joins distinct
embedded points, then

\[
\boxed{E_{\mathrm{form}}=\{0\}.}                               \tag{4.21}
\]

Indeed, the kernel is either zero or the full module. The full alternative
would force every \(M_i=0\), hence

\[
C_i=2(I-\Phi_i\Phi_i^T),                                       \tag{4.22}
\]

whose radial covariance is zero, contradicting (4.5) at the source of the
positive distinct jump. This mechanism is independent of axial row scaling.

---

## 5. Exact Platonic classification

Use the standard unit vertex embeddings in \(S^2\), their shortest-edge
graphs, and one common edge rate normalized by

\[
L\Phi=-2\Phi.                                                   \tag{5.1}
\]

Let \(k\) be the degree and \(\alpha\) the adjacent inner product. The rate is

\[
r=\frac{2}{k(1-\alpha)}.                                       \tag{5.2}
\]

The vertex stabilizer contains a rotation of order at least three around the
radial axis, so \(C_i\) is axially isotropic. Equations (4.3) and (4.5) give

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

| Graph | \(k\) | \(\alpha\) | rate \(r\) | row scale |
|---|---:|---:|---:|---:|
| tetrahedron | 3 | \(-1/3\) | \(1/2\) | \(4\) |
| octahedron | 4 | \(0\) | \(1/2\) | \(3\) |
| cube | 3 | \(1/3\) | \(1\) | \(2\) |
| icosahedron | 5 | \(1/\sqrt5\) | \((5+\sqrt5)/10\) | \(3(1-1/\sqrt5)\) |
| dodecahedron | 3 | \(\sqrt5/3\) | \((3+\sqrt5)/2\) | \(3-\sqrt5\) |

Represent trace-free quadratic forms by

\[
x^2-z^2,\quad y^2-z^2,\quad 2xy,\quad 2xz,\quad 2yz.             \tag{5.5}
\]

- **Tetrahedron and cube.** Every vertex has
  \(x^2=y^2=z^2=1/3\), so the diagonal trace-free subspace is the
  two-dimensional sampling kernel. The sign vectors of \((xy,xz,yz)\) span
  \(\mathbb R^3\), so the sampling rank is three.
- **Octahedron.** Sampling at \(\pm e_1,\pm e_2,\pm e_3\) detects the
  two-dimensional diagonal trace-free subspace and kills the three
  off-diagonal forms. Thus the sampling rank is two.
- **Icosahedron.** With \(\varphi=(1+\sqrt5)/2\), the evaluation determinant
  on

  \[
  (0,1,\varphi),(0,-1,\varphi),(1,\varphi,0),
  (-1,\varphi,0),(\varphi,0,1)                                  \tag{5.6}
  \]

  is

  \[
  32(11+5\sqrt5)\ne0.                                           \tag{5.7}
  \]

- **Dodecahedron.** The determinant on

  \[
  (-1,-1,-1),(-1,-1,1),(-1,1,-1),
  (0,-\varphi^{-1},-\varphi),(-\varphi^{-1},-\varphi,0)          \tag{5.8}
  \]

  is

  \[
  -192\ne0.                                                      \tag{5.9}
  \]

Common normalization only rescales evaluation rows, so the last two sampling
maps have full rank five. The exact dimensions are:

| Graph | \(\operatorname{rank}R\) | \(\operatorname{rank}S\) | \(\dim E_{\mathrm{form}}\) | \(\dim K_X\) | \(\dim E_{\mathrm{sample}}\) |
|---|---:|---:|---:|---:|---:|
| tetrahedron | 3 | 3 | 2 | 2 | 0 |
| octahedron | 2 | 2 | 3 | 3 | 0 |
| cube | 3 | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 5 | 0 | 0 | 0 |

For the first three graphs, \(E_{\mathrm{form}}=K_X\ne0\): all apparent
exact forms vanish at every sampled vertex. For the last two, no nonzero exact
form exists. None of the five positive generators therefore has a nonzero
sampled degree-two mode with eigenvalue \(-6\).

The five vertex sets satisfy exact second-moment isotropy

\[
\frac1{|I|}\sum_i\Phi_i\Phi_i^T=\frac13I.                      \tag{5.10}
\]

Thus every trace-free quadratic sample has zero uniform mean. Since the row
scale in (5.4) is constant on each graph, the shifted condition makes the
sample constant, and (5.10) forces that constant to be zero. Shifting does not
restore a genuine mode in these examples.

---

## 6. Signed-conductance restoration

Consider the four points on \(S^1\)

\[
x_0=(1,0),\quad x_1=(0,1),\quad x_2=(-1,0),\quad x_3=(0,-1).    \tag{6.1}
\]

Assign rate \(1\) to each adjacent point and rate \(-1/2\) to the antipodal
point. The symmetric conservative generator is

\[
L=
\begin{pmatrix}
-3/2&1&-1/2&1\\
1&-3/2&1&-1/2\\
-1/2&1&-3/2&1\\
1&-1/2&1&-3/2
\end{pmatrix}.                                                   \tag{6.2}
\]

For

\[
X=(1,0,-1,0)^T,
\quad
Y=(0,1,0,-1)^T,                                                  \tag{6.3}
\]

and

\[
Q=X^2-Y^2=(1,-1,1,-1)^T,                                       \tag{6.4}
\]

one has

\[
LX=-X,\qquad LY=-Y,\qquad LQ=-4Q.                               \tag{6.5}
\]

The sample of \(2XY\) is zero, so the restored sampled quadratic space is
one-dimensional.

The negative rate is forced on this fixed support. At \(x_0\), write the
rates to \(x_1,x_2,x_3\) as \(u,b,v\). Coordinate and quadratic exactness give

\[
u+v+2b=1,\qquad u-v=0,\qquad u+v=2.                           \tag{6.6}
\]

Therefore

\[
\boxed{u=v=1,\qquad b=-\frac12.}                                \tag{6.7}
\]

The rotated argument applies at every vertex. Every generator on these nodes
with this complete off-diagonal support and the three exactness requirements
has negative antipodal magnitude \(1/2\) per row. With equal reversible
masses, there are two negative undirected conductances of value \(-1/2\), so
the total negative undirected mass is one.

---

## 7. Two independent finite-product obstructions

### 7.1 Carré-du-champ proof

For nonnegative rates define

\[
\Gamma(f,g)(i)=\frac12\sum_j a_{ij}
 (f(j)-f(i))(g(j)-g(i)).                                       \tag{7.1}
\]

Then

\[
L(fg)-fLg-gLf=2\Gamma(f,g).                                    \tag{7.2}
\]

If

\[
Lf=-\lambda f,\qquad Lg=-\nu g,
\qquad L(fg)=-(\lambda+\nu)fg,                                 \tag{7.3}
\]

then \(\Gamma(f,g)=0\) at every state. At an aligned pair of extrema all
summands in (7.1) are nonnegative. A positive edge changing both values
strictly in the same direction makes the sum positive, a contradiction.

For \(g=f\),

\[
2\Gamma(f,f)(i)=\sum_j a_{ij}(f(j)-f(i))^2.                     \tag{7.4}
\]

Thus

\[
L(f^2)=-2\lambda f^2                                           \tag{7.5}
\]

forces equality of \(f\) along every positive active edge. It is constant on
every directed reachable component. If the chain is irreducible and
\(\lambda>0\), then \(f=0\).

This concerns the sampled square itself. It cannot be applied automatically
to one algebraic harmonic component when other product components remain or
sampling kills/aliases them.

### 7.2 Semigroup/Jensen proof

Let \(P_t=e^{tL}\). For a positive conservative finite generator, \(P_t\) is
Markov. If \(Lf=-\lambda f\), then

\[
P_tf=e^{-\lambda t}f.                                          \tag{7.6}
\]

Jensen gives

\[
P_t(f^2)(i)\ge(P_tf(i))^2.                                     \tag{7.7}
\]

If (7.5) also holds, equality holds:

\[
P_t(f^2)=e^{-2\lambda t}f^2=(P_tf)^2.                           \tag{7.8}
\]

For transition probabilities \(p_t(i,j)\), equality in the strictly convex
square inequality is equivalent to constancy of \(f\) on
\(\{j:p_t(i,j)>0\}\). Uniformization of a finite continuous-time chain shows
that this support is exactly the set reachable from \(i\) along positive-rate
edges for every \(t>0\). Hence equality means constancy on every reachable
set. Irreducibility and \(\lambda>0\) again give \(f=0\).

The first proof is infinitesimal and edgewise; the second is global in time
and gives the exact equality set. Neither assumes reversibility.

---

## 8. Bounded spherical spectral-product search

Let \(\mathcal H_\ell(S^{d-1})\) have eigenvalue

\[
\lambda_\ell=\ell(\ell+d-2).                                   \tag{8.1}
\]

### 8.1 Parity and multiplication image

A degree-\(\ell\) harmonic has parity \((-1)^\ell\), so a product of two
such harmonics is even. For \(d\ge3\), the scalar pointwise multiplication
image contains the even harmonic degrees

\[
\mathcal H_{2\ell}\oplus\mathcal H_{2\ell-2}\oplus\cdots
\oplus\mathcal H_0.                                             \tag{8.2}
\]

For \(d=2\), the scalar image is only
\(\mathcal H_{2\ell}\oplus\mathcal H_0\). Equation (8.2) describes the
pointwise multiplication image, not the full abstract tensor representation;
additional components of \(\operatorname{Sym}^2(\mathcal H_\ell)\) can lie
in the multiplication kernel.

### 8.2 Odd/even zonal equality sets

For a normalized zonal harmonic about \(p\) in dimension at least three, the
absolute-value bound is attained at both antipodes. For odd \(\ell\), the two
values have opposite signs; for even \(\ell\), both are equal maxima. The
square has equal values at both antipodes in either case. On \(S^1\), the
maximizing set is still larger. A strict-extremum argument must therefore
assume a positive active edge leaving the whole equality set, not silently
replace it by one point.

### 8.3 Sampling aliases and component identifiability

For every degree \(k\), let

\[
S_{X,k}:\mathcal H_k\to\mathbb R^I.                             \tag{8.3}
\]

An algebraically nonzero component can lie in \(\ker S_{X,k}\), and distinct
degrees can have identical sampled vectors. Exactness of one sampled
combination is not exactness of a complete irreducible component unless an
additional equivariance and irreducibility argument identifies it.

### 8.4 Additive resonance

The square obstruction directly isolates a degree-\(k\) component only if its
sampled eigenvalue is \(2\lambda_\ell\) and every other sampled component is
zero or independently separated. The arithmetic condition is

\[
k(k+d-2)=2\ell(\ell+d-2),
\qquad k\in\{0,2,\ldots,2\ell\}.                               \tag{8.4}
\]

With

\[
n=d-2,\qquad X=2k+n,\qquad Y=2\ell+n,                          \tag{8.5}
\]

this becomes

\[
\boxed{X^2-2Y^2=-n^2,}                                         \tag{8.6}
\]

with the corresponding parity and range restrictions. Resonances need not be
finite. In \(d=4\),

\[
(k+1)^2-2(\ell+1)^2=-1,                                       \tag{8.7}
\]

and the Pell unit \(3+2\sqrt2\) generates

\[
(\ell,k)=(4,6),(28,40),(168,238),\ldots.                       \tag{8.8}
\]

The exact bounded search

\[
2\le d\le12,\qquad1\le\ell\le12                               \tag{8.9}
\]

finds

\[
(d,\ell,k)=(4,4,6),(6,8,12),(8,12,18),(9,5,8).                 \tag{8.10}
\]

These arithmetic coincidences do not identify a nonzero sampled component and
do not remove the other product components. Whenever the extra
identifiability hypotheses are strong enough to isolate the sampled square,
the conclusion is exactly Section 7's one-function obstruction. No
\(\ell\)-indexed dimension tradeoff or new global consequence survives.

### Hierarchy verdict

Under the stated kill criterion, the proposed general spectral-product
hierarchy is

\[
\boxed{\text{REJECTED for this stage}.}                         \tag{8.11}
\]

This is not a universal impossibility claim under future association-scheme,
design, or representation-theoretic hypotheses. It states only that the
bounded general search produced no theorem beyond the sampled-square identity.
The mandatory stage result is the sampled covariance and axial-rigidity
package above.

---

## 9. Exact verification boundary

`quadratic_covariance_audit.py` uses exact rational and
\(\mathbb Q(\sqrt5)\) arithmetic. It verifies:

- the covariance constraints against direct generator action;
- the structural factorization \(R=(L+2dI)S\);
- \(K_X\subseteq E_{\mathrm{form}}\);
- the specialized rank formula
  \(\dim E_{\mathrm{sample}}=\operatorname{rank}S-\operatorname{rank}R\);
- every Platonic covariance tensor and exact rank;
- both nonzero golden-ratio determinant certificates;
- equality \(E_{\mathrm{form}}=K_X\) in the axial examples;
- the signed four-point construction and forced rate \(-1/2\);
- the bounded resonance list; and
- the first terms of the infinite \(d=4\) Pell family.

These computations are regression and falsification tools, not proofs of the
general theorems. Lean formalizes the finite covariance algebra, shifted
residual, trace-free contraction, sampling-kernel inclusion, sampled-range
intersection identity, restricted rank-nullity, and axial row-scaling
consequences.

---

## 10. Publication boundary

The covariance expansion, rank-nullity, carré du champ, Jensen inequality,
Markov uniformization, spherical harmonic parity, and general representation
irreducibility are standard inputs. The contribution is the combined finite
sampled theorem:

1. exact shifted covariance residual;
2. trace-free form constraints;
3. factorization through the sampling map;
4. exact sampled-space and rank formulas;
5. sharp axial and equivariant rigidity;
6. an all-dimensional regular-simplex equality family;
7. exact Platonic sampling-kernel classification; and
8. forced signed restoration on a fixed finite support.

No priority claim is made for the generic product identity or for a general
spectral-product hierarchy.
