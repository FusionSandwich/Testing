# Sampled quadratic exactness for finite eigenmap generators

## Corrected Prompt 2 closeout theorem

Let

\[
(Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i))
\]

on a finite state set. In matrix notation conservation fixes
\(L_{ii}=-\sum_{j\ne i}a_{ij}\). This document gives the final Prompt 2
package: the exact covariance and sampling theorem, sharp positive rigidity,
the corrected equivariant hypothesis, exact signed counterexamples, and the
centered product-resonance theory. Reversibility is required nowhere unless
it is stated explicitly.

The closeout corrections are substantive:

1. equivariant irreducibility requires **all** off-diagonal rates to be
   nonnegative;
2. centered additive products are governed by a constant carré du champ and
   are not universally impossible;
3. Jensen equality is distinct from centered resonance; and
4. the low-degree hierarchy verdict is based on sampled identifiability and
   aliasing, not on a false centered-square obstruction.

---

## 1. Exact quadratic covariance identity

Let \(\Phi:I\to\mathbb R^d\) satisfy

\[
L\Phi=-\lambda\Phi
\]

coordinatewise. Put

\[
\Delta_{ij}=\Phi_j-\Phi_i,
\qquad
C_i=\sum_{j\ne i}a_{ij}\Delta_{ij}\Delta_{ij}^{T},
\qquad
Q_A(i)=\Phi_i^TA\Phi_i.
\]

### Theorem 1.1 — covariance identity

For every real matrix \(A\),

\[
\boxed{
LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^TC_i).
}
\]

For symmetric \(A\), the last term is \(\operatorname{tr}(AC_i)\).

**Proof.** For coordinates \(r,s\),

\[
\Phi_j^{(r)}\Phi_j^{(s)}-\Phi_i^{(r)}\Phi_i^{(s)}
=
\Phi_i^{(r)}\Delta_{ij}^{(s)}
+
\Phi_i^{(s)}\Delta_{ij}^{(r)}
+
\Delta_{ij}^{(r)}\Delta_{ij}^{(s)}.
\]

Summing against \(a_{ij}\), applying the coordinate eigenmap equation to the
first two terms, and contracting with \(A\) proves the identity. Positivity,
connectivity, and reversibility are not used. ∎

### Theorem 1.2 — arbitrary shifted quadratic target

For \(q_{A,c}=Q_A-c\),

\[
Lq_{A,c}=-\mu q_{A,c}
\]

if and only if

\[
\boxed{
\operatorname{tr}(A^TC_i)
+(\mu-2\lambda)Q_A(i)-\mu c=0
\quad\text{for every }i.
}
\]

If \(\mu\ne0\), a shift exists precisely when the first two terms have one
common value over all states; \(c\) is that value divided by \(\mu\). If an
invariant probability \(\pi\) exists and \(\mu>0\), averaging gives
\(c=\sum_i\pi_iQ_A(i)\). Algebraic trace-freeness alone does not determine a
finite-sample mean.

---

## 2. Spherical degree two and genuine sampled exactness

Assume

\[
\Phi_i\in S^{d-1},
\qquad
\lambda=d-1,
\qquad
\mu=2d,
\qquad
A\in\operatorname{Sym}_0(d).
\]

For

\[
P_0(T)=T-\frac{\operatorname{tr}T}{d}I,
\qquad
M_i=P_0(C_i+2\Phi_i\Phi_i^T),
\]

trace-freeness gives

\[
LQ_A(i)+2dQ_A(i)=\langle A,M_i\rangle_F.
\]

### Theorem 2.1 — form-space characterization

\[
\boxed{
E_{\mathrm{form}}
=
\{A\in\operatorname{Sym}_0(d):\langle A,M_i\rangle_F=0\ \forall i\}
=
\operatorname{span}\{M_i:i\in I\}^{\perp}.
}
\]

This is a statement about matrices, not yet sampled functions.

Define

\[
(S_XA)_i=\Phi_i^TA\Phi_i,
\qquad
K_X=\ker S_X,
\qquad
B=L+2dI,
\]

and

\[
(R_XA)_i=\langle A,M_i\rangle_F.
\]

### Theorem 2.2 — residual-through-sampling factorization

\[
\boxed{R_X=BS_X.}
\]

Hence

\[
\boxed{K_X\subseteq E_{\mathrm{form}}}
\]

and the genuine sampled exact space is

\[
\boxed{
E_{\mathrm{sample}}
=S_X(E_{\mathrm{form}})
=\operatorname{im}S_X\cap\ker(L+2dI).
}
\]

The general restricted-map formula is

\[
\dim E_{\mathrm{sample}}
=
\dim E_{\mathrm{form}}
-
\dim(E_{\mathrm{form}}\cap K_X).
\]

Here \(K_X\subseteq E_{\mathrm{form}}\), so it sharpens to

\[
\boxed{
\dim E_{\mathrm{sample}}
=
\dim E_{\mathrm{form}}-\dim K_X.
}
\]

In chosen bases, if \(S\) and \(R\) are the sampling and residual matrices and
\(G\) is the generator matrix,

\[
R=(G+2dI)S,
\qquad
\operatorname{rank}R\le\operatorname{rank}S,
\]

and

\[
\boxed{
\dim E_{\mathrm{sample}}
=
\operatorname{rank}S-
\operatorname{rank}R.
}
\]

Also

\[
\operatorname{rank}\begin{bmatrix}R\\S\end{bmatrix}
=
\operatorname{rank}S.
\]

Every dimension claim below concerns \(E_{\mathrm{sample}}\) unless form space
is named explicitly.

---

## 3. Sharp positive axial-covariance rigidity

For \(x\in S^{d-1}\), write

\[
P_x^{\mathrm{rad}}=xx^T,
\qquad
P_x^{\mathrm{tan}}=I-xx^T.
\]

The coordinate eigenmap gives

\[
\operatorname{tr}C_i=2(d-1).
\]

If every off-diagonal rate is nonnegative, then

\[
\beta_i:=\Phi_i^TC_i\Phi_i
=
\sum_{j\ne i}a_{ij}(1-\Phi_i\cdot\Phi_j)^2\ge0,
\]

with strict inequality exactly when some positive outgoing jump reaches a
distinct embedded point.

### Theorem 3.1 — local axial constraint

Suppose

\[
C_i=\tau_iP_{\Phi_i}^{\mathrm{tan}}
+
\beta_iP_{\Phi_i}^{\mathrm{rad}},
\qquad
\beta_i>0.
\]

Then

\[
\boxed{
M_i=
\frac{d\beta_i}{d-1}
\left(\Phi_i\Phi_i^T-\frac1dI\right)
}
\]

and, for trace-free symmetric \(A\),

\[
\boxed{
\langle A,M_i\rangle_F
=
\frac{d\beta_i}{d-1}\Phi_i^TA\Phi_i.
}
\]

Thus exactness at this state is equivalent to vanishing of the quadratic
sample at this state.

### Theorem 3.2 — global axial rigidity

If Theorem 3.1 holds at every state, then

\[
\boxed{
E_{\mathrm{form}}=K_X,
\qquad
E_{\mathrm{sample}}=\{0\}.
}
\]

Local axial covariance on only a subset forces vanishing only on that subset;
it is not silently promoted to a global theorem.

### Corollary 3.3 — regular simplices

For a regular simplex \(x_0,\ldots,x_d\in S^{d-1}\),

\[
x_i\cdot x_j=-\frac1d\ (i\ne j),
\qquad
\sum_i x_i=0,
\]

and complete-graph rate

\[
a_{ij}=\frac{d-1}{d+1},
\]

one has \(Lx=-(d-1)x\), axial covariance, and

\[
M_i=(d+1)\left(x_ix_i^T-\frac1dI\right).
\]

The sampling rank is exactly \(d\). For every zero-sum vector
\(y\in\mathbb R^{d+1}\),

\[
A_y=\frac{d^2}{d^2-1}\sum_i y_i x_ix_i^T
\]

is trace-free and satisfies \(x_k^TA_yx_k=y_k\). Consequently

\[
\dim E_{\mathrm{form}}=
\dim K_X=rac{d(d+1)}2-1-d,
\qquad
\dim E_{\mathrm{sample}}=0.
\]

This is an all-dimensional equality family with a potentially large algebraic
kernel consisting entirely of aliases.

---

## 4. Corrected equivariant irreducibility theorem

### Theorem 4.1 — positive equivariant rigidity

Let a finite group \(G\) act transitively on \(I\), let
\(\rho:G\to O(d)\), and assume all of the following:

1. \(\Phi_i\in S^{d-1}\);
2. \(\Phi_{gi}=\rho(g)\Phi_i\);
3. \(a_{gi,gj}=a_{ij}\);
4. \(a_{ij}\ge0\) for **every** \(i\ne j\);
5. conservation fixes the diagonal matrix entries by
   \(L_{ii}=-\sum_{j\ne i}a_{ij}\);
6. \(L\Phi=-(d-1)\Phi\) coordinatewise;
7. the real conjugation representation of \(G\) on
   \(\operatorname{Sym}_0(d)\) is irreducible; and
8. at least one positive jump joins distinct embedded points.

Then

\[
\boxed{E_{\mathrm{form}}=\{0\}.}
\]

Reversibility is not required.

**Proof.** Equivariance makes \(E_{\mathrm{form}}\) a real \(G\)-submodule of
\(\operatorname{Sym}_0(d)\). Irreducibility makes it either zero or the full
module. In the full alternative every \(M_i\) vanishes. Since
\(\operatorname{tr}C_i=2(d-1)\), this forces

\[
C_i+2\Phi_i\Phi_i^T=2I,
\qquad
C_i=2(I-\Phi_i\Phi_i^T).
\]

The radial covariance is then zero. At the source of the positive distinct
jump, however, global off-diagonal nonnegativity gives

\[
\Phi_i^TC_i\Phi_i
=
\sum_{j\ne i}a_{ij}(1-\Phi_i\cdot\Phi_j)^2>0,
\]

which is a contradiction. ∎

The global nonnegativity hypothesis is essential; one positive term alone does
not prevent cancellation by negative rates.

### Counterexample 4.2 — signed regular pentagon

Let

\[
z_m=(\cos(2\pi m/5),\sin(2\pi m/5)),
\qquad m=0,\ldots,4.
\]

Give each distance-one neighbor the rate

\[
u=\frac{5+3\sqrt5}{10}>0
\]

and each distance-two neighbor the rate

\[
v=\frac{5-3\sqrt5}{10}<0.
\]

The diagonal is the negative row sum. Exact circulant calculation over
\(\mathbb Q(\sqrt5)\) gives

\[
L\mathbf1=0,
\qquad
L\cos\theta=-\cos\theta,
\qquad
L\sin\theta=-\sin\theta,
\]

and

\[
L\cos2\theta=-4\cos2\theta,
\qquad
L\sin2\theta=-4\sin2\theta.
\]

For \(d=2\), \(\operatorname{Sym}_0(2)\) is spanned by the two trace-free
quadratics sampled as \(\cos2\theta\) and \(\sin2\theta\). The sampling map
has rank two and both samples have the target eigenvalue \(-4\). Therefore

\[
\boxed{
E_{\mathrm{form}}=\operatorname{Sym}_0(2),
\qquad
\dim E_{\mathrm{sample}}=2.
}
\]

A generator of \(C_5\) acts on \(\operatorname{Sym}_0(2)\) by rotation through
\(4\pi/5\). Its characteristic discriminant is

\[
\left(2\cos\frac{4\pi}{5}\right)^2-4
=
\frac{\sqrt5-5}{2}<0,
\]

so it has no real invariant line and the real representation is irreducible.
This is an exact counterexample to Theorem 4.1 with hypothesis 4 omitted.

---

## 5. Exact finite examples

### 5.1 Platonic shortest-edge generators

For the five standard Platonic embeddings in \(S^2\), use the shortest-edge
graph and normalize the common edge rate by \(L\Phi=-2\Phi\). If \(k\) is
the degree and \(\alpha\) the adjacent inner product, the rate is

\[
r=\frac{2}{k(1-\alpha)}.
\]

The vertex stabilizer forces axial covariance, and exact calculation gives

\[
C_i=(1+\alpha)I+(1-3\alpha)\Phi_i\Phi_i^T,
\]

\[
M_i=3(1-\alpha)
\left(\Phi_i\Phi_i^T-\frac13I\right).
\]

| Graph | rank \(R\) | rank \(S\) | \(\dim E_{\mathrm{form}}\) | \(\dim K_X\) | \(\dim E_{\mathrm{sample}}\) |
|---|---:|---:|---:|---:|---:|
| tetrahedron | 3 | 3 | 2 | 2 | 0 |
| octahedron | 2 | 2 | 3 | 3 | 0 |
| cube | 3 | 3 | 2 | 2 | 0 |
| icosahedron | 5 | 5 | 0 | 0 | 0 |
| dodecahedron | 5 | 5 | 0 | 0 | 0 |

For the tetrahedron and cube the diagonal trace-free forms vanish on every
sampled vertex. For the octahedron the off-diagonal trace-free forms vanish.
The icosahedral and dodecahedral evaluation ranks are certified by exact
nonzero minors

\[
32(11+5\sqrt5)
\quad\text{and}\quad
-192.
\]

Thus none of the five positive generators has a nonzero sampled degree-two
mode at eigenvalue \(-6\).

### 5.2 Four-point signed restoration

On the four cardinal points of \(S^1\), assign rate \(1\) to each adjacent
point and rate \(-1/2\) to the antipode. The conservative symmetric generator
is

\[
\begin{pmatrix}
-3/2&1&-1/2&1\\
1&-3/2&1&-1/2\\
-1/2&1&-3/2&1\\
1&-1/2&1&-3/2
\end{pmatrix}.
\]

It satisfies

\[
LX=-X,
\qquad
LY=-Y,
\qquad
L(X^2-Y^2)=-4(X^2-Y^2).
\]

The other trace-free quadratic, \(2XY\), samples to zero. Hence the restored
sampled quadratic space is one-dimensional. At \((1,0)\), if the two adjacent
rates are \(u,v\) and the antipodal rate is \(b\), exact coordinate and
quadratic conditions give

\[
u+v+2b=1,
\qquad
u-v=0,
\qquad
u+v=2,
\]

so uniquely

\[
\boxed{u=v=1,
\qquad b=-\frac12.}
\]

---

## 6. General centered product resonance

For nonnegative rates define the conventional bilinear carré du champ

\[
\Gamma(f,g)(i)
=
\frac12\sum_{j\ne i}a_{ij}
(f(j)-f(i))(g(j)-g(i)).
\]

The algebra below is valid even for signed rates; positivity enters only in
inequality and equality arguments.

### Theorem 6.1 — product identity

\[
\boxed{
L(fg)-fLg-gLf=2\Gamma(f,g).
}
\]

### Theorem 6.2 — arbitrary shifted product target

If

\[
Lf=-\lambda f,
\qquad
Lg=-\nu g,
\]

then for every \(\mu,c\),

\[
\boxed{
L(fg-c)+\mu(fg-c)
=
2\Gamma(f,g)
+(\mu-\lambda-\nu)fg
-\mu c.
}
\]

At additive resonance \(\mu=\lambda+\nu\),

\[
\boxed{
L(fg-c)=-(\lambda+\nu)(fg-c)
\iff
2\Gamma(f,g)=(\lambda+\nu)c
}
\]

pointwise.

For \(g=f\),

\[
\boxed{
L(f^2-c)=-2\lambda(f^2-c)
\iff
\Gamma(f,f)=\lambda c
}
\]

pointwise.

Consequences:

- for \(c=0\), additive square resonance forces \(\Gamma(f,f)=0\);
- with nonnegative rates this makes \(f\) constant on every positive active
  edge;
- on an irreducible positive chain and \(\lambda>0\), the uncentered resonant
  square therefore has \(f=0\); but
- a centered resonant square can be nonzero when \(\Gamma(f,f)\) is a positive
  constant.

There is no universal positive-generator impossibility theorem for centered
squares.

### Counterexample 6.3 — Boolean centered square

Let

\[
I=\{(-1,-1),(-1,1),(1,-1),(1,1)\},
\]

and from each state jump at rate one by flipping either coordinate. For

\[
f(x_1,x_2)=x_1+x_2,
\]

exact calculation gives

\[
Lf=-2f,
\qquad
f^2-2=2x_1x_2\ne0,
\]

\[
L(f^2-2)=-4(f^2-2),
\qquad
\Gamma(f,f)=4.
\]

This is a permanent positive regression against any claim that every nonzero
centered additive square is impossible.

---

## 7. Semigroup variance and Jensen equality are different statements

Let \(P_t=e^{tL}\) for a finite positive conservative generator.

### Theorem 7.1 — centered-resonance semigroup identity

If

\[
Lf=-\lambda f,
\qquad
L(f^2-c)=-2\lambda(f^2-c),
\]

then

\[
\boxed{
P_t(f^2)-(P_tf)^2
=
c(1-e^{-2\lambda t})
}
\]

pointwise.

Conversely, assume \(Lf=-\lambda f\) and that the displayed identity holds for
all \(t\) in an interval containing zero. Since a finite-state semigroup is a
matrix exponential and differentiable at zero, the identity gives

\[
P_t(f^2-c)=e^{-2\lambda t}(f^2-c),
\]

and differentiation at \(t=0\) yields centered square resonance.

### Theorem 7.2 — Jensen and its equality set

For every state \(i\),

\[
\boxed{
P_t(f^2)(i)\ge(P_tf(i))^2.
}
\]

Writing \(p_t(i,j)\) for the transition probabilities, equality holds exactly
when \(f\) is constant on

\[
\{j:p_t(i,j)>0\}.
\]

For a finite continuous-time chain and \(t>0\), uniformization identifies this
support with the states reachable from \(i\) along positive-rate edges.

Centered resonance usually has positive variance and therefore does **not**
give Jensen equality. In the Boolean example,

\[
P_t(f^2)-(P_tf)^2
=
2(1-e^{-4t})>0
\qquad(t>0).
\]

---

## 8. Spherical products: eigenvalue shift and the exact \(S^2\) table

For \(S^{d-1}\),

\[
\text{coordinate eigenvalue}=d-1,
\]

\[
\text{doubled coordinate eigenvalue}=2(d-1),
\]

while

\[
\text{degree-two spherical eigenvalue}=2d.
\]

Therefore the quadratic covariance theorem has the nonzero target shift

\[
2d-2(d-1)=2.
\]

It is not the additive square-resonance problem.

On \(S^2\), the pointwise multiplication image of
\(\operatorname{Sym}^2(\mathcal H_\ell)\) contains exactly the even degrees
\(0,2,\ldots,2\ell\). This scalar multiplication image must not be confused
with the full abstract tensor product. Centering removes only the degree-zero
component.

| \(\ell\) | pointwise component degrees \(k\) | eigenvalues \(k(k+1)\) | additive target \(2\ell(\ell+1)\) | exact resonance | maximizer warning | sampling warning |
|---:|---|---|---:|---|---|---|
| 1 | \(0,2\) | \(0,6\) | 4 | none | odd zonal values have opposite antipodal signs; the square ties the antipodes | each \(S_{X,k}\) may have a kernel or cross-degree alias |
| 2 | \(0,2,4\) | \(0,6,20\) | 12 | none | even zonal modes have equal antipodal maxima | centering removes only \(k=0\); sampled components still require identification |
| 3 | \(0,2,4,6\) | \(0,6,20,42\) | 24 | none | odd zonal values have opposite antipodal signs; the square ties the antipodes | one sampled combination is not a complete irreducible component |
| 4 | \(0,2,4,6,8\) | \(0,6,20,42,72\) | 40 | none | even zonal modes have equal antipodal maxima | kernels and aliases must be excluded degree by degree |
| 5 | \(0,2,4,6,8,10\) | \(0,6,20,42,72,110\) | 60 | none | odd zonal values have opposite antipodal signs; the square ties the antipodes | algebraic nonzero does not imply sampled nonzero |
| 6 | \(0,2,4,6,8,10,12\) | \(0,6,20,42,72,110,156\) | 84 | none | even zonal modes have equal antipodal maxima | complete-component exactness needs equivariance plus exact module identification |

The table is generated and checked by exact integer assertions. None of the
six rows has an additive resonance.

---

## 9. General resonance arithmetic and hierarchy verdict

For \(S^{d-1}\), a degree \(k\) component is additively resonant with the
square of degree \(\ell\) only if

\[
k(k+d-2)=2\ell(\ell+d-2),
\qquad
k\in\{0,2,\ldots,2\ell\}.
\]

With

\[
X=2k+d-2,
\qquad
Y=2\ell+d-2,
\]

this is

\[
X^2-2Y^2=-(d-2)^2.
\]

The equation is Pell-type. In \(d=4\), for example,

\[
(\ell,k)=(4,6),(28,40),(168,238),\ldots.
\]

The exact bounded search

\[
2\le d\le12,
\qquad
1\le\ell\le12
\]

finds

\[
(d,\ell,k)
=(4,4,6),(6,8,12),(8,12,18),(9,5,8).
\]

Arithmetic resonance does not establish that the component survives sampling,
that other product components vanish, or that a complete irreducible component
is exact. After the kernel, alias, equality-set, and identifiability audits,
no \(\ell\)-indexed sampled dimension tradeoff, multiplicity obstruction, or
new global consequence survives.

Accordingly,

\[
\boxed{\text{GENERAL SPECTRAL-PRODUCT HIERARCHY: REJECTED FOR PROMPT 2}.}
\]

The reason is the absence of a new sampled theorem after identifiability and
alias analysis, not a universal centered-square obstruction. Stronger future
results under explicit association-scheme, design, or representation
hypotheses are not ruled out.

---

## 10. Verification and publication boundary

Lean formalizes:

- the finite product identity with \(\Gamma\);
- the arbitrary shifted product residual;
- arbitrary-target and additive-resonance equivalences;
- centered and uncentered square equivalences;
- the positive uncentered pointwise obstruction;
- the covariance and shifted quadratic identities;
- trace-free projection contraction;
- sampling-kernel inclusion and exact sampled range;
- restricted rank-nullity; and
- the axial row-scaling consequences.

The exact audits verify:

- all existing covariance, factorization, Platonic, and signed four-point
  results;
- regular-simplex formulas in dimensions 2 through 10;
- the signed regular pentagon over \(\mathbb Q(\sqrt5)\);
- the Boolean centered square;
- the semigroup variance identity;
- the \(S^2\) \(\ell=1,\ldots,6\) table;
- the bounded and Pell resonance assertions; and
- the singular/plural user-axiom policy fixtures.

Standard finite Markov-semigroup theory, Jensen equality, uniformization,
spherical harmonic product decomposition, and elementary real representation
irreducibility remain identified external inputs. No priority claim is made
for those inputs. The Prompt 2 contribution is the combined sampled
covariance factorization, exact sampled-space theorem, sharp positive
rigidity, exact alias classifications, and signed/centered regression
boundary.
