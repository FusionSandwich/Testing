# Quadratic covariance, sampled exactness, and sharp finite models

## 1. Conventions and separation of spaces

Let \(I\) be finite and

\[
 (Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)).
\]

Unless stated otherwise, rates may be signed and nonsymmetric; positivity,
reversibility, connectivity, injectivity, and distinct sampled nodes are not
implicit. Let \(\Phi_i=\Phi(i)\in\mathbb R^d\), assume
\(L\Phi=-\lambda\Phi\) coordinatewise, and define

\[
 \Delta_{ij}=\Phi_j-\Phi_i,\qquad
 C_i=\sum_{j\ne i}a_{ij}\Delta_{ij}\Delta_{ij}^{T}.
\]

For \(A=A^T\), put

\[
 S_X(A)_i=\Phi_i^TA\Phi_i,\qquad q_{A,c}=S_X(A)-c\mathbf1.
\]

An algebraic matrix, its trace-free quadratic form, its sampled function, a
sampling alias in \(\ker S_X\), and a genuinely nonzero sampled exact mode are
different objects and are never identified below.

## 2. Covariance identity, arbitrary target, and weighted centering

For every jump,

\[
 \Phi_j^TA\Phi_j-\Phi_i^TA\Phi_i
 =2\Phi_i^TA\Delta_{ij}+\Delta_{ij}^TA\Delta_{ij}.
\]

Summing, using the coordinate eigenmap equation, and contracting the last term
gives, without any sign or reversibility assumption,

\[
 \boxed{L(S_X(A))(i)
 =-2\lambda S_X(A)_i+\operatorname{tr}(AC_i).} \tag{2.1}
\]

Since \(L\mathbf1=0\), for all real \(c,\mu\),
\(Lq_{A,c}=-\mu q_{A,c}\) if and only if, at every vertex,

\[
 \boxed{\operatorname{tr}(AC_i)
 +(\mu-2\lambda)\Phi_i^TA\Phi_i-\mu c=0.} \tag{2.2}
\]

No division by \(\mu\) occurred. When \(\mu=0\), \(c\) disappears and is
arbitrary; the condition is \(LS_X(A)=0\). When \(\mu\ne0\), the first two
terms in (2.2) must have common value \(\mu c\).

For weighted centering, assume \(I\ne\varnothing\), \(w_i>0\), and detailed
balance \(w_i a_{ij}=w_j a_{ji}\). Signed rates are still allowed. Pairing the
two orientations of each unordered pair proves

\[
 \sum_iw_i(Lf)(i)=0.
\]

If \(Lq=-\mu q\) and \(\mu\ne0\), then \(\sum_iw_iq_i=0\). Since
\(W=\sum_iw_i>0\), necessarily

\[
 \boxed{c=\frac{\sum_iw_iS_X(A)_i}{\sum_iw_i}.} \tag{2.3}
\]

This weighted-mean condition is necessary but does not replace (2.2). On the
natural positive cube-edge generator, for example, the \(xy\) sample has mean
zero but eigenvalue \(-4\), not the target \(-6\). When \(\mu=0\), conservation
does not determine \(c\). A stronger assertion that only constants lie in the
zero eigenspace requires nonnegative rates and connected positive-rate support;
it is not part of the signed identity.

## 3. Unit-sphere residual and genuine sampled dimension

Assume \(d>0\), \(\|\Phi_i\|=1\), \(\lambda=d-1\), and
\(A\in\operatorname{Sym}_0(d)\). Define

\[
 P_0(B)=B-\frac{\operatorname{tr}B}{d}I,\qquad
 M_i=P_0(C_i+2\Phi_i\Phi_i^T),
\]

\[
 R_X(A)=(L+2dI)S_X(A).
\]

Equation (2.1) and trace-freeness give the exact residual factorization

\[
 \boxed{R_X(A)_i=\langle A,M_i\rangle_F
 =\operatorname{tr}[A(C_i+2\Phi_i\Phi_i^T)].} \tag{3.1}
\]

Put

\[
 K_X=\ker S_X,\qquad E_{\rm form}=\ker R_X,\qquad
 E_{\rm sample}=S_X(E_{\rm form}).
\]

Then

\[
 E_{\rm form}=\operatorname{span}\{M_i:i\in I\}^{\perp},\qquad
 K_X\subseteq E_{\rm form},
\]

\[
 \boxed{E_{\rm sample}
 =\operatorname{im}S_X\cap\ker(L+2dI).} \tag{3.2}
\]

The restriction of \(S_X\) to \(E_{\rm form}\) has kernel \(K_X\), so
rank-nullity gives

\[
 \boxed{\dim E_{\rm sample}
 =\dim E_{\rm form}-\dim K_X
 =\operatorname{rank}S_X-\operatorname{rank}R_X.} \tag{3.3}
\]

In particular, \(\operatorname{rank}R_X\le\operatorname{rank}S_X\). In a fixed
basis \(A_1,\ldots,A_m\) of \(\operatorname{Sym}_0(d)\), the matrix convention is

\[
 S_{ib}=\Phi_i^TA_b\Phi_i,\qquad R_{ib}=\langle A_b,M_i\rangle_F,
\]

with \(L\) acting on sampled columns and \(R=(L+2dI)S\).

## 4. Positive full-module obstruction and Frobenius bound

Assume \(I\ne\varnothing\), \(d>1\), \(a_{ij}\ge0\),
\(\|\Phi_i\|=1\), and
\(L\Phi=-(d-1)\Phi\). Dotting the eigenmap equation with \(\Phi_i\) gives

\[
 \sum_ja_{ij}(1-\Phi_i\cdot\Phi_j)=d-1.
\]

Therefore

\[
 \operatorname{tr}C_i
 =\sum_ja_{ij}\|\Phi_j-\Phi_i\|^2=2(d-1),
\qquad
 M_i=C_i+2\Phi_i\Phi_i^T-2I.
\]

Radial evaluation yields

\[
 \boxed{\Phi_i^TM_i\Phi_i
 =\sum_ja_{ij}(\Phi_i\cdot\Phi_j-1)^2>0.} \tag{4.1}
\]

For strictness, equality would force every positive-rate jump to have dot
product one, hence \(\Phi_j=\Phi_i\); all active increments would vanish and
\(L\Phi(i)=0\), contradicting \(-(d-1)\Phi_i\ne0\). Thus every \(M_i\ne0\).
Choose any \(i\), using \(I\ne\varnothing\), and take the trace-free form
\(A=M_i\) in (3.1). This proves \(R_X\ne0\), and hence

\[
 \boxed{\operatorname{rank}R_X\ge1,\qquad
 \dim E_{\rm sample}\le\operatorname{rank}S_X-1.} \tag{4.2}
\]

Since \(\operatorname{tr}M_i=0\),

\[
 \Phi_i^TM_i\Phi_i
 =\langle M_i,\Phi_i\Phi_i^T-I/d\rangle_F,
\]

and \(\|\Phi_i\Phi_i^T-I/d\|_F^2=1-1/d\). Cauchy--Schwarz proves

\[
 \boxed{\|M_i\|_F\ge
 \frac{\sum_ja_{ij}(\Phi_i\cdot\Phi_j-1)^2}
 {\sqrt{1-1/d}}.} \tag{4.3}
\]

This forbids exactness of the complete trace-free module while remaining
compatible with aliases: \(K_X\subseteq E_{\rm form}\), but those forms sample
to zero. Formula (3.3), not \(\dim E_{\rm form}\) alone, counts genuine modes.

## 5. Signed one-shell full-tangent-isotropy rigidity

Assume \(d>1\), \(\|\Phi_i\|=1\) for every \(i\), and
\(L\Phi=-(d-1)\Phi\) coordinatewise. For each vertex define

\[
 J_i=\{j\ne i:a_{ij}\ne0\text{ and }\Phi_j\ne\Phi_i\},
\]

assume \(J_i\ne\varnothing\), and suppose that for some \(0<\ell_i<2\),

\[
 1-\Phi_i\cdot\Phi_j=\ell_i\qquad(j\in J_i).
\]

Coincident embedded jumps may have nonzero rates, but their increments vanish
and they are excluded below. Put

\[
 s_i=\sqrt{\ell_i(2-\ell_i)},\qquad
 u_{ij}=\frac{\Phi_j-(1-\ell_i)\Phi_i}{s_i},\qquad
 r_i^*=\sum_{j\in J_i}a_{ij}.
\]

Then \(u_{ij}\perp\Phi_i\) and \(\|u_{ij}\|=1\). Assume the full signed tangent
moment

\[
 \sum_{j\in J_i}a_{ij}u_{ij}u_{ij}^T
 =\frac{r_i^*}{d-1}(I-\Phi_i\Phi_i^T). \tag{5.1}
\]

No positivity, symmetry, reversibility, connectivity, or transitivity is used.
The split

\[
 \Phi_j-\Phi_i=-\ell_i\Phi_i+s_i u_{ij}
\]

in the eigenmap equation gives, by radial and tangent projection,

\[
 \boxed{r_i^*\ell_i=d-1,\qquad
 \sum_{j\in J_i}a_{ij}u_{ij}=0.} \tag{5.2}
\]

Thus \(r_i^*>0\) despite the allowed signs. Expanding the jump outer products
and using (5.1)--(5.2) gives

\[
 \boxed{C_i=(2-\ell_i)(I-\Phi_i\Phi_i^T)
 +(d-1)\ell_i\Phi_i\Phi_i^T,} \tag{5.3}
\]

\[
 \boxed{M_i=d\ell_i(\Phi_i\Phi_i^T-I/d),\qquad
 R_X(A)_i=d\ell_iS_X(A)_i.} \tag{5.4}
\]

With \(D=\operatorname{diag}(d\ell_i)\), this is \(R_X=DS_X\). The positivity
and invertibility of \(D\) come from \(d>1\) and \(0<\ell_i<2\), not from rate
signs. Consequently

\[
 \boxed{E_{\rm form}=K_X,\quad
 \operatorname{rank}R_X=\operatorname{rank}S_X,\quad
 E_{\rm sample}=\{0\}.} \tag{5.5}
\]

The explicit \(d>1\) hypothesis is required because (5.1) divides by \(d-1\).

## 6. Positive sharpness: the spherical hexagonal prism

Let \(I=\mathbb Z/6\mathbb Z\times\{\pm1\}\) and

\[
 \Phi_{k,\sigma}=\frac1{\sqrt5}
 (2\cos(k\pi/3),2\sin(k\pi/3),\sigma).
\]

Give horizontal cycle edges rate \(2\), vertical matching edges rate \(1\),
and use unit masses. The diagonal is \(-5\). The matrix is symmetric and
conservative, all active rates are positive, and the cycles plus matching make
the graph connected. Translations of
\(\mathbb Z/6\times\mathbb Z/2\) preserve the two edge types and act
transitively, proving vertex transitivity.

Every vertex is unit length. Horizontal and vertical active pairs both have dot
product \(3/5\), hence loss \(\ell=2/5\). The two horizontal neighbours sum to
the current equatorial component; their rate-two difference is \(-2\) times
that component. The vertical jump is \(-2\) times the height. Thus
\(L\Phi=-2\Phi\).

Full tangent isotropy fails. At \((k,\sigma)=(0,-1)\), the actual tangent
moment minus its isotropic target is

\[
 \boxed{\begin{pmatrix}
 -1/4&0&-1/2\\
 0&5/4&0\\
 -1/2&0&-1
 \end{pmatrix}\ne0.} \tag{6.1}
\]

In the fixed form basis

\[
 A_0=x^2-y^2,\quad A_1=2z^2-x^2-y^2,\quad
 A_2=xy,\quad A_3=xz,\quad A_4=yz,
\]

the sampled columns are respectively horizontal frequency two/even in the
layer, constant, frequency two/even, and frequency one/odd in the layer. They
are independent, so \(S_X\) is injective. Their generator eigenvalues are
\(-6,0,-6,-4,-4\). Hence

\[
 \operatorname{rank}S_X=5,\qquad \operatorname{rank}R_X=3,
\]

\[
 \boxed{E_{\rm form}=\operatorname{span}\{A_0,A_2\},\qquad
 E_{\rm sample}=\operatorname{span}\{S_X(A_0),S_X(A_2)\}.} \tag{6.2}
\]

Both spaces have dimension two, but they are not literally the same type of
object; \(S_X\) identifies them because it is injective. Both displayed
samples are nonzero and satisfy \(Lf=-6f\). Exact rank witnesses are

\[
 \det S[0{:}5,0{:}5]=\frac{576}{3125}\ne0,
\]

\[
 \det R[(0,1,2),(1,3,4)]
 =-\frac{96\sqrt3}{125}\ne0. \tag{6.3}
\]

Thus positivity, reversibility, connectedness, transitivity, one shell,
full-dimensional embedding, and injective sampling do not replace (5.1).

## 7. Equivariance, isotypic kernels, and corrected invariance

Let a finite group \(G\) act on \(I\), let \(\rho:G\to O(d)\), and assume

\[
 \Phi(gi)=\rho(g)\Phi(i),\qquad a_{gi,gj}=a_{ij}.
\]

Use

\[
 (g\cdot f)(i)=f(g^{-1}i),\qquad
 g\cdot A=\rho(g)A\rho(g)^T.
\]

Changing variables in the jump sum shows that \(L\) commutes with the
permutation action. Also

\[
 C_{gi}=\rho(g)C_i\rho(g)^T,\qquad
 M_{gi}=\rho(g)M_i\rho(g)^T,
\]

so \(S_X\) and \(R_X\) are equivariant. Therefore
\(K_X,E_{\rm form},\operatorname{im}S_X\), and \(E_{\rm sample}\) are
\(G\)-submodules. When a weighted inner product is used, assume additionally
\(w_{gi}=w_i\).

Suppose

\[
 \operatorname{Sym}_0(V)=\bigoplus_{r\in\mathcal R}W_r
\]

is a multiplicity-free real decomposition into pairwise nonisomorphic
irreducibles. Real Maschke semisimplicity and Schur's lemma imply that every
submodule is a sum of selected \(W_r\), while an equivariant map restricted to
one \(W_r\) is either zero or injective. Hence

\[
 \boxed{E_{\rm form}=\bigoplus_{r:R_X|_{W_r}=0}W_r,\qquad
 K_X=\bigoplus_{r:S_X|_{W_r}=0}W_r,} \tag{7.1}
\]

\[
 \boxed{E_{\rm sample}\cong_G
 \bigoplus_{\substack{r:R_X|_{W_r}=0\\S_X|_{W_r}\ne0}}W_r,} \tag{7.2}
\]

\[
 \boxed{\dim E_{\rm sample}
 =\sum_{\substack{r:R_X|_{W_r}=0\\S_X|_{W_r}\ne0}}\dim W_r.} \tag{7.3}
\]

Let \(V_2=\operatorname{im}S_X\) and define
\(\overline R(S_X(A))=R_X(A)\). It is well-defined because
\(K_X\subseteq\ker R_X\), equivariant, and has kernel \(E_{\rm sample}\);
its rank is \(\operatorname{rank}R_X\). Under Section 4's positive hypotheses,
\(\overline R\ne0\). If \(\kappa(V_2)\) is the least real dimension of an
irreducible constituent of \(V_2\), the nonzero quotient by its invariant
kernel gives

\[
 \boxed{\operatorname{rank}R_X\ge\kappa(V_2).} \tag{7.4}
\]

If nonzero \(V_2\) is irreducible, its kernel is zero and
\(E_{\rm sample}=0\), without assuming \(L(V_2)\subseteq V_2\).

Equivariance alone sends an irreducible sampled copy \(U\) only into the
ambient \(U\)-isotypic component. It gives \(L(U)\subseteq U\) only under an
explicit invariance assumption or when \(U\) is the entire ambient isotypic
component. If \(U\) is preserved and \(L\) is self-adjoint in a
\(G\)-invariant real inner product, the real eigenspaces of \(L|_U\) are
\(G\)-submodules. Irreducibility leaves one eigenvalue, so \(L|_U\) is a real
scalar. This avoids a false real-Schur shortcut for complex or quaternionic
types.

### Exact \(D_3\) counterexample

Take \(I=\{0,1\}\times\mathbb Z/3\mathbb Z\), unit masses, and

\[
 (Lf)(s,k)=f(s,k+1)+f(s,k-1)-2f(s,k)
 +f(1-s,k)-f(s,k).
\]

This is a positive symmetric connected triangular-prism generator. The affine
maps \(k\mapsto\pm k+t\) act diagonally on both layers and give the \(D_3\)
symmetry. Let \(U_0\) be the two-dimensional zero-sum module supported on layer
zero. Rotation by one step has matrix

\[
 \begin{pmatrix}0&-1\\1&-1\end{pmatrix}
\]

in the basis \((1,-1,0),(0,1,-1)\). Its characteristic discriminant is
\(-3\), so it has no real invariant line and \(U_0\) is irreducible. For
zero-sum \(u\), the cycle contribution is \(-3u\) and the vertical contribution
is \((-u,u)\), giving

\[
 \boxed{L(u,0)=(-4u,u).} \tag{7.5}
\]

The nonzero layer-one component proves that \(U_0\) is not \(L\)-invariant.

## 8. Exact five-Platonic classification

For each regular solid, use the positive shortest-edge generator scaled by
\(L\Phi=-2\Phi\). Each regular vertex figure has the full tangent tight-frame
moment, so Section 5 gives

\[
 R_X=\kappa S_X,\qquad \kappa=3(1-\alpha),\qquad
 L|_{\operatorname{im}S_X}=-3(1+\alpha)I.
\]

Exact unit-node, distinctness, shortest-shell, connectivity, tangent-moment,
and minor certificates give:

| graph | \(\alpha\) | rate | \(L|_{\operatorname{im}S}\) | rank \(S\) | rank \(R\) | dim \(E_{\rm form}\) | dim \(K_X\) | dim \(E_{\rm sample}\) | \(S\) minor | \(R\) minor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tetrahedron | \(-1/3\) | \(1/2\) | \(-2\) | 3 | 3 | 2 | 2 | 0 | \(-4/27\) | \(-256/27\) |
| octahedron | \(0\) | \(1/2\) | \(-3\) | 2 | 2 | 3 | 3 | 0 | \(-2\) | \(-18\) |
| cube | \(1/3\) | \(1\) | \(-4\) | 3 | 3 | 2 | 2 | 0 | \(4/27\) | \(32/27\) |
| icosahedron | \(\sqrt5/5\) | \((5+\sqrt5)/10\) | \(-3-3\sqrt5/5\) | 5 | 5 | 0 | 0 | 0 | \(-16\sqrt5/125\) | \([3(1-\sqrt5/5)]^5(-16\sqrt5/125)\) |
| dodecahedron | \(\sqrt5/3\) | \((3+\sqrt5)/2\) | \(-3-\sqrt5\) | 5 | 5 | 0 | 0 | 0 | \(16/81\) | \((3-\sqrt5)^5(16/81)\) |

All minors are exactly nonzero, including the
\(\mathbb Q(\sqrt5)\) cases. For tetrahedron and cube,

\[
 K_X=E_{\rm form}
 =\operatorname{span}\{x^2-y^2,2z^2-x^2-y^2\}.
\]

For the octahedron,

\[
 K_X=E_{\rm form}=\operatorname{span}\{xy,xz,yz\}.
\]

The icosahedral and dodecahedral sampling maps are injective. In all five
cases \(E_{\rm sample}=0\); the nonzero form spaces in the first three rows are
aliases, not genuine sampled eigenfunctions.

## 9. Signed cube restoration and sharp negative mass

Let \(X=\{\varepsilon/\sqrt3:\varepsilon\in\{\pm1\}^3\}\), use unit masses and
the complete undirected graph, and define

\[
 N^-(\gamma)=\sum_e\max(0,-\gamma_e)
\]

with each undirected edge counted once. Assign the Hamming-orbit conductances

\[
 (r_1,r_2,r_3)=(3/2,0,-1/2).
\]

The diagonal is the negative row sum. Exact Walsh-character calculation gives

\[
 Lx=-2x,\quad Ly=-2y,\quad Lz=-2z,
\]

\[
 L(xy)=-6xy,\quad L(xz)=-6xz,\quad L(yz)=-6yz.
\]

Both diagonal trace-free forms vanish on the cube; the three cross samples are
nonzero independent characters. Thus

\[
 \operatorname{rank}S_X=3,\quad
 K_X=\operatorname{span}\{A_0,A_1\},\quad \dim K_X=2.
\]

Direct covariance evaluation gives

\[
 C_i=2(I-\Phi_i\Phi_i^T),\qquad M_i=0.
\]

Hence \(R_X=0\), \(E_{\rm form}=\operatorname{Sym}_0(3)\) has dimension five,
and \(E_{\rm sample}\) has dimension three.

For global optimality, average an arbitrary feasible reversible conductance
over the 48 signed coordinate permutations. Every conjugate remains feasible
because the group preserves constants, coordinates, cross quadratics, and
their target scalars. Convexity and edge-permutation invariance give

\[
 N^-(\overline\gamma)
 \le |G|^{-1}\sum_{g\in G}N^-(g\gamma)=N^-(\gamma). \tag{9.1}
\]

The three edge orbits contain 12, 12, and 4 edges. Coordinate and quadratic
exactness for the averaged rates give

\[
 r_1+2r_2+r_3=1,\qquad r_1+r_2=3/2.
\]

Therefore \(r_2+r_3=-1/2\), and

\[
 \begin{aligned}
 N^-&=12(-r_1)_++12(-r_2)_++4(-r_3)_+\\
 &\ge4[(-r_2)_++(-r_3)_+]
 \ge-4(r_2+r_3)=2.
 \end{aligned} \tag{9.2}
\]

The displayed optimizer attains two on its four antipodal edges. The exact KKT
certificate uses

\[
 A=\begin{pmatrix}1&2&1\\1&1&0\end{pmatrix},\quad
 b=\binom1{3/2},\quad r^*=\begin{pmatrix}3/2\\0\\-1/2\end{pmatrix},
\]

\[
 g=(0,-4,-4)^T,\qquad y=(4,-4)^T,
\]

for which \(Ar^*=b\), \(g\in\partial N^-(r^*)\),
\(g+A^Ty=0\), and \(-y^Tb=2\). Thus

\[
 \boxed{\min N^-(\gamma)=2.} \tag{9.3}
\]

The directed convention counts four. For common vertex mass \(w>0\), if
\(\gamma_{ij}=w a_{ij}\) is shared conductance, the orbit conductances and
minimum scale by \(w\), giving \(2w\); negative mass measured in rates remains
two. The natural positive cube-edge generator \((1,0,0)\) instead has
\(\operatorname{rank}S_X=\operatorname{rank}R_X=3\),
\(E_{\rm sample}=0\), and cross-quadratic eigenvalue \(-4\).

## 10. Proof and verification boundary

Sections 2--9 are ordinary finite-dimensional proofs. The finite-sum and
sampling-map cores are formalized in AFPBarrier/QuadraticCovariance.lean and
AFPBarrier/QuadraticSampling.lean; the sphere, one-shell, and spectral modules
are mapped in docs/P2_THEOREM_TO_FILE_MAP.md. Exact finite certificates are in
exact_quadratic_covariance_audit.py, exact_signed_restoration_audit.py, and
exact_d3_invariance_counterexample.py.

Standard inputs are finite rank-nullity, real Maschke semisimplicity, the
self-adjoint spectral theorem, and convex subgradient optimality. No priority
claim attaches to those inputs, the covariance expansion alone, or rank tables
alone. The candidate contribution is the combined sampling-kernel-aware
framework, signed one-shell factorization, positive prism sharpness example,
equivariant quotient rank gap, and signed-cube optimum, subject to specialist
prior-art review.
