# Quadratic covariance and genuine sampled exactness

## Conventions

Let (I) be finite and

\[
 (Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)).
\]

No sign, reversibility, or connectivity assumption is used in the algebraic
identities.  Write (\Phi_i=\Phi(i)\in\mathbb R^d), assume coordinatewise
(L\Phi=-\lambda\Phi), and put

\[
 \Delta_{ij}=\Phi_j-\Phi_i,qquad
 C_i=\sum_{j\ne i}a_{ij}\Delta_{ij}\Delta_{ij}^{T}.
\]

For (A=A^T), the sampling map is

\[
 S_X(A)_i=\Phi_i^TA\Phi_i,qquad
 q_{A,c}=S_X(A)-c\mathbf1.
\]

An algebraic matrix and its sampled function are never identified below.

## Covariance identity and arbitrary target

For every (i,j),

\[
 \Phi_j^TA\Phi_j-\Phi_i^TA\Phi_i
 =2\Phi_i^TA\Delta_{ij}+\Delta_{ij}^TA\Delta_{ij}.
\]

After summation and use of the coordinate eigenmap equation,

\[
 \boxed{L(S_X(A))(i)=-2\lambda S_X(A)_i+\operatorname{tr}(AC_i).}
\]

Consequently, for any real (c,\mu),

\[
 Lq_{A,c}=-\mu q_{A,c}
\]

if and only if, at every (i),

\[
 \boxed{\operatorname{tr}(AC_i)+(\mu-2\lambda)\Phi_i^TA\Phi_i-\mu c=0.}
\]

When (\mu=0), the constant (c) disappears: it is arbitrary and the
condition is (LS_X(A)=0).  When (\mu\ne0), such a constant exists exactly
when the first two terms are independent of (i), and then their common value
is (\mu c).

## Unit-sphere degree-two residual

Now suppose (\|\Phi_i\|=1), (\lambda=d-1), (\mu=2d), (c=0), and
(A\in\operatorname{Sym}_0(d)).  Define

\[
 P_0(B)=B-\frac{\operatorname{tr}B}{d}I,qquad
 M_i=P_0(C_i+2\Phi_i\Phi_i^T),qquad
 R_X(A)_i=\langle A,M_i\rangle_F.
\]

Trace-freeness removes the scalar part of (P_0), so the preceding identity
gives the exact factorization

\[
 \boxed{R_X=(L+2dI)\circ S_X.}
\]

Let (m=\dim\operatorname{Sym}_0(d)=d(d+1)/2-1).  Then

\[
 E_{\rm form}=\ker R_X
 =\{A:\langle A,M_i\rangle=0\ \forall i\}
 =\operatorname{span}\{M_i:i\in I\}^{\perp},
\]

and

\[
 \dim E_{\rm form}=m-\operatorname{rank}R_X.
\]

For a fixed basis (A_1,\ldots,A_m), the matrix convention is

\[
 S_{ib}=\Phi_i^TA_b\Phi_i,qquad R_{ib}=\langle A_b,M_i\rangle,
\]

with (L) multiplying sampled column vectors.  Thus (R=(L+2dI)S).

## Sampling kernel and genuine sampled space

Put (K_X=\ker S_X) and

\[
 E_{\rm sample}=S_X(E_{\rm form}).
\]

Factorization proves the non-optional inclusion

\[
 \boxed{K_X\subseteq E_{\rm form}.}
\]

Indeed, a zero sampled function is vacuously exact.  Moreover,

\[
 E_{\rm sample}=\operatorname{im}S_X\cap\ker(L+2dI).
\]

Rank-nullity first gives the general quotient formula

\[
 \dim E_{\rm sample}
 =\dim E_{\rm form}-\dim(E_{\rm form}\cap K_X).
\]

Using the inclusion above,

\[
 \boxed{\dim E_{\rm sample}
 =\dim E_{\rm form}-\dim K_X
 =\operatorname{rank}S_X-\operatorname{rank}R_X.}
\]

Also (\dim K_X=m-\operatorname{rank}S_X) and
(\operatorname{rank}R_X\le\operatorname{rank}S_X).

## Positive full-space no-go

Assume now (a_{ij}\ge0), (d>1), and the coordinate eigenmap hypotheses.
The trace identity is

\[
 \operatorname{tr}C_i
 =\sum_j a_{ij}\|\Phi_j-\Phi_i\|^2=2(d-1).
\]

Hence (M_i=C_i+2\Phi_i\Phi_i^T-2I), and its radial value is

\[
 \Phi_i^TM_i\Phi_i
 =\sum_j a_{ij}(\Phi_i\cdot\Phi_j-1)^2.
\]

It is strictly positive: otherwise every positive jump is between coincident
embedded nodes, which would give (L\Phi(i)=0), contradicting
(-(d-1)\Phi_i\ne0).  In particular every (M_i\ne0), and explicitly

\[
 \|M_i\|_F\ge
 \frac{\sum_j a_{ij}(\Phi_i\cdot\Phi_j-1)^2}{\sqrt{1-1/d}}.
\]

If every trace-free quadratic form were exact, all (M_i) would vanish.
Then (C_i+2\Phi_i\Phi_i^T=c_iI); tracing gives (c_i=2), hence
(C_i=2(I-\Phi_i\Phi_i^T)).  Its radial component is zero, contradicting the
strict positive formula.  This is an all-forms statement; aliases are already
included because (K_X\subset E_{\rm form}).

## Sharp structural theorem: one shell and full tangent isotropy

For each row (i), ignore transitions with (\Phi_j=\Phi_i), since their
increments vanish.  Assume every remaining nonzero-rate transition satisfies

\[
 \Phi_i\cdot\Phi_j=\alpha_i\in(-1,1).
\]

Thus active antipodes are excluded.  Define, over these nonzero embedded
jumps only,

\[
 u_{ij}=\frac{\Phi_j-\alpha_i\Phi_i}{\sqrt{1-\alpha_i^2}},qquad
 r_i=\sum_j a_{ij}.
\]

Assume the full ambient tangent moment identity

\[
 \sum_j a_{ij}u_{ij}u_{ij}^T
 =\frac{r_i}{d-1}(I-\Phi_i\Phi_i^T).
\]

The rates may be signed; positivity, symmetry, reversibility, connectivity,
and transitivity are not needed.  Splitting the eigenmap equation into radial
and tangent parts gives

\[
 \sum_j a_{ij}u_{ij}=0,qquad r_i=\frac{d-1}{1-\alpha_i}.
\]

Expanding every increment yields

\[
 C_i=(1+\alpha_i)(I-\Phi_i\Phi_i^T)
 +(d-1)(1-\alpha_i)\Phi_i\Phi_i^T,
\]

and therefore

\[
 \boxed{M_i=d(1-\alpha_i)(\Phi_i\Phi_i^T-I/d).}
\]

For every traceless (A),

\[
 R_X(A)_i=d(1-\alpha_i)S_X(A)_i.
\]

Thus (R=DS), where (D_{ii}=d(1-\alpha_i)>0), and

\[
 \boxed{E_{\rm form}=K_X,\quad
 \operatorname{rank}R=\operatorname{rank}S,\quad
 E_{\rm sample}=0.}
\]

This is not rank bookkeeping: the geometric moment hypotheses force the
operator factorization by an invertible diagonal matrix, and the conclusion
survives every sampling alias.

### Necessity and sharpness

The 12 nodes

\[
 \Phi_{n,\sigma}=\frac1{\sqrt5}
 (2\cos(n\pi/3),2\sin(n\pi/3),\sigma),
\quad n\in\mathbb Z/6,\quad\sigma=\pm1,
\]

with horizontal cycle rate (2) and vertical matching rate (1), form a
positive, connected, reversible, vertex-transitive, full-dimensional example.
Every active edge has (\alpha=3/5), and (L\Phi=-2\Phi).  Nevertheless the
full tangent moment is anisotropic.  In the basis

\[
 (x^2-y^2,\ 2z^2-x^2-y^2,\ xy,\ xz,\ yz),
\]

(\operatorname{rank}S=5), (\operatorname{rank}R=3), and

\[
 E_{\rm form}=E_{\rm sample}=\operatorname{span}\{x^2-y^2,xy\}.
\]

The exact minors are (576/3125) for a (5\times5) sampling minor and
(-96\sqrt3/125) for a (3\times3) residual minor.  Hence full tangent-space
isotropy is essential even without degeneracy or aliasing.

## Equivariance and corrected symmetry rigidity

Let (G) act on (I), let (\rho:G\to O(d)), assume
(\Phi(gi)=\rho(g)\Phi(i)), and assume (a_{gi,gj}=a_{ij}).  With conjugation
on forms and permutation on functions, (S_X) and (R_X) are equivariant;
(K_X,E_{\rm form},\operatorname{im}S_X,E_{\rm sample}) are invariant.

On (V_2=\operatorname{im}S_X), define

\[
 \overline R(S_X(A))=R_X(A)=(L+2dI)S_X(A).
\]

This is well-defined by (K_X\subseteq\ker R_X), with kernel
(E_{\rm sample}).  Under positivity and (d>1), (\overline R\ne0).  If
(\kappa(V_2)) is the least real dimension of an irreducible constituent,
then

\[
 \boxed{\operatorname{rank}R_X
 =\dim V_2-\dim E_{\rm sample}\ge\kappa(V_2).}
\]

This bound is sharp: the positive cube attains (3), while the positive
equatorial hexagon attains (1).  If nonzero (V_2) is irreducible, then
(E_{\rm sample}=0), without assuming (L(V_2)\subseteq V_2).

The stronger assertion that multiplicity-free (V_2) alone makes (L)
scalar on each constituent is false.  An exact positive reversible connected
right-Cayley generator on (D_3), recorded in the exact audit, has an
irreducible two-dimensional (V_2) but sends it into another isomorphic
ambient copy.  The corrected scalar theorem requires either
(L(V_2)\subseteq V_2), or total ambient multiplicity one for every relevant
type.  If (L) is self-adjoint, its restriction to each preserved real
irreducible is a real scalar: its real eigenspaces are invariant, which handles
real, complex, and quaternionic types uniformly.

## Exact Platonic results

All rows below use shortest-edge generators scaled by (L\Omega=-2\Omega),
target (-6), and the five-column basis displayed above.

| graph | edge dot (\alpha) | edge rate | (\operatorname{rank}S=\operatorname{rank}R) | (\dim K_X=\dim E_{\rm form}) | (\dim E_{\rm sample}) | (L|_{\operatorname{im}S}) |
|---|---:|---:|---:|---:|---:|---:|
| tetrahedron | (-1/3) | (1/2) | 3 | 2 | 0 | (-2) |
| octahedron | (0) | (1/2) | 2 | 3 | 0 | (-3) |
| cube | (1/3) | (1) | 3 | 2 | 0 | (-4) |
| icosahedron | (\sqrt5/5) | ((5+\sqrt5)/10) | 5 | 0 | 0 | (-3-3\sqrt5/5) |
| dodecahedron | (\sqrt5/3) | ((3+\sqrt5)/2) | 5 | 0 | 0 | (-3-\sqrt5) |

The sampling kernels are (\langle e_0,e_1\rangle) for tetrahedron and cube,
(\langle e_2,e_3,e_4\rangle) for octahedron, and zero for the other two.
The exact nonzero sampling minors are respectively
(-4/27,-2,4/27,-16\sqrt5/125,16/81).  Since
(R=3(1-\alpha)S), the residual ranks follow exactly.

## Signed restoration

On the cube (\Phi_\sigma=\sigma/\sqrt3), with unit masses and the complete
graph, assign conductance (3/2) to Hamming-distance-one edges, (0) to
distance-two edges, and (-1/2) to antipodes.  Then constants are conserved,

\[
 L\Phi_k=-2\Phi_k,qquad L(\Phi_a\Phi_b)=-6\Phi_a\Phi_b\quad(a<b),
\]

and the three sampled cross quadratics are nonzero and independent.  In fact
(C_i=2I-2\Phi_i\Phi_i^T), (M_i=0), and
(\dim E_{\rm sample}=3).

For arbitrary reversible complete-graph conductances satisfying both the
coordinate constraints and exactness of the full three-dimensional cube
quadratic module, averaging over the cube group cannot increase

\[
 N_-^E=\sum_{e}\max(-\gamma_e,0).
\]

The orbit rates satisfy

\[
 r_1+2r_2+r_3=1,qquad r_1+r_2=3/2,
\]

so (r_2+r_3=-1/2) and

\[
 N_-^E\ge4\bigl((-r_2)_++(-r_3)_+\bigr)\ge2.
\]

The displayed construction attains equality.  Thus (N_-^{E,\min}=2) for
unit masses and this full-module constrained problem.  The directed measure is
(4); normalized masses rescale the answer.  No minimum is claimed for
restoring only one selected quadratic.
