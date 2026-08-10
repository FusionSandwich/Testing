# P1E polar-cell construction without a global stress solve

## Status: conditional route; not the accepted P1E upper family

The polar identities below are unconditional once the cells exist, but the
paired-facet compiler assumed later in this note is not proved at every
topological defect layer.  This route is therefore retained as a conditional
theorem and obstruction audit.  The accepted \(d=3\) construction is the
separate shortened-gap ring family.

This is an independent positive/reversible route through the fixed atlas
compiler.  It is useful because exact coordinate reproduction follows from a
facet divergence identity; no global stress correction, Korn estimate, or
rowwise-to-shared reconciliation is used.

Put \(n=d-1\).  For a finite set \(X=\{x_i\}\subset S^{d-1}\), define the
tangent polar cell

\[
 C_i=\{z\in T_{x_i}S^{d-1}:\tau_{ij}\mathbin\cdot z\leq \ell_{ij}
       \text{ for every }j\},
 \quad
 \tau_{ij}=x_j-(x_i\mathbin\cdot x_j)x_i,
 \quad
 \ell_{ij}=1-x_i\mathbin\cdot x_j.                 \tag{P.1}
\]

If \(F_{ij}\) is an \((n-1)\)-facet of \(C_i\), let
\(\sigma_{ij}=|F_{ij}|\), \(\theta_{ij}=\arccos(x_i\cdot x_j)\), and set

\[
 \gamma_{ij}=\frac{\sigma_{ij}}{\sin\theta_{ij}}. \tag{P.2}
\]

The same facet is the ridge between the two facets with normals \(x_i,x_j\)
of the circumscribed polar polytope

\[
 P_X=\{y\in\mathbb R^d:x_k\mathbin\cdot y\leq1\text{ for every }k\}.
\]

Consequently its Euclidean area is the same from both sides and
\(\gamma_{ij}=\gamma_{ji}>0\).  Thus (P.2) is genuinely shared, not a
collection of independently feasible rows.

## P.1 Exact finite identities

Write

\[
 \nu_{ij}=\frac{\tau_{ij}}{\sin\theta_{ij}},
 \qquad
 s_{ij}=\frac{\ell_{ij}}{\sin\theta_{ij}}
       =\tan\frac{\theta_{ij}}2.                   \tag{P.3}
\]

The facet \(F_{ij}\) lies in \(\nu_{ij}\cdot z=s_{ij}\).  Applying the
divergence theorem on \(C_i\) first to a constant vector and then to the
identity vector field gives

\[
 \sum_j\sigma_{ij}\nu_{ij}=0,
 \qquad
 \sum_j\sigma_{ij}s_{ij}=n|C_i|.                  \tag{P.4}
\]

It follows exactly that

\[
 \sum_j\gamma_{ij}\tau_{ij}=0,
 \qquad
 \mu_i:=\frac1n\sum_j\gamma_{ij}\ell_{ij}=|C_i|. \tag{P.5}
\]

With \(a_{ij}=\gamma_{ij}/\mu_i\), equations (P.2)--(P.5) prove positivity,
reversibility, and

\[
 L1=0,\qquad Lx=-nx                                  \tag{P.6}
\]

without a correction step.

If the spherical fill distance is at most \(h<\pi/4\), a point of the
spherical Voronoi cell of \(x_i\) is at distance at most \(h\) from \(x_i\).
The gnomonic map \(z\mapsto(x_i+z)/\|x_i+z\|\) identifies this cell with
\(C_i\).  Hence every active neighbor satisfies \(\theta_{ij}\leq2h\).
If separation is at least \(qh\), all active edges lie in

\[
 qh\leq\theta_{ij}\leq2h.                         \tag{P.7}
\]

The disjoint spherical caps of radius \(qh/2\) about the active neighbors
lie in the cap of radius \(2h+qh/2\) about \(x_i\).  Comparing
\(\int_0^r\sin^{n-1}t\,dt\), using \(2t/\pi\leq\sin t\leq t\), gives the
explicit degree bound

\[
 D\leq D_{\rm pack}(n,q):=
 \left\lceil\left(\frac\pi2\right)^{n-1}
                    (1+4/q)^n\right\rceil.        \tag{P.7a}
\]

Moreover (P.5) and
\(\ell_{ij}\geq2q^2h^2/\pi^2\) give the explicit rate bound

\[
 r_i\leq \frac{n\pi^2}{2q^2}h^{-2}.               \tag{P.8}
\]

The separation ball of radius \(qh/2\) about \(x_i\) lies in its spherical
Voronoi cell.  Hence \(C_i\) contains the Euclidean ball of radius
\(\tan(qh/2)\), and the volume constant in the next section may be taken as

\[
 v=\omega_n(q/2)^n.                               \tag{P.8a}
\]

Likewise \(C_i\subset B(0,\tan h)\subset B(0,2h)\); thus one may take
\(S=\omega_{n-1}2^{n-1}\) as a crude uniform facet-area constant.

## P.2 An explicit paired-facet defect lemma

The following finite lemma is what the atlas compiler has to certify.  It is
strictly local.

Assume that the facets of every \(C_i\) can be paired \(F_k^+,F_k^-\), with
at most \(D/2\) pairs.  Suppress \(i,k\) and write
\(\sigma_\pm,s_\pm,\nu_\pm\) for a pair.  Let \(c_\pm\) be its facet
centroid and

\[
 t_\pm=c_\pm-s_\pm\nu_\pm,
 \quad t_\pm\cdot\nu_\pm=0.
\]

Suppose, for \(0<h\leq1/\Lambda\),

\[
\begin{aligned}
 &\sigma_\pm\leq S h^{n-1},\qquad s_\pm\leq\Lambda h,
       \qquad |C_i|\geq v h^n,\\
 &|\sigma_+-\sigma_-|\leq A_\sigma h^n,
       \qquad |s_+-s_-|\leq A_s h^2,
       \qquad \|\nu_++\nu_-\|\leq A_\nu h,\\
 &\|t_\pm\|\leq A_t h^2,
       \qquad \|t_+-t_-\|\leq A_{t,3}h^3.         \tag{P.9}
\end{aligned}
\]

Then the unnormalized P1A row tensor

\[
 \widehat M_i=\sum_j\gamma_{ij}
 \left[(x_j-x_i)(x_j-x_i)^T-\frac{2\ell_{ij}}nP_i\right]
\]

satisfies

\[
 \|\widehat M_i\|_F\leq C_{\rm pol}h^{n+2},
 \qquad
 \|M_i\|_F\leq \frac{C_{\rm pol}}v h^2,          \tag{P.10}
\]

where one completely explicit admissible constant is

\[
\begin{aligned}
 C_{\rm mix}
 &=\frac D2\left(
   2A_\sigma\Lambda^2+4S\Lambda A_s
     +2S\Lambda^2A_\nu\right),\\
 C_{\rm tan}
 &=D\left(A_\sigma A_t+S A_{t,3}+SA_tA_\nu
                 +2S\Lambda^3\right),\\
 C_{\rm rad}&=2DS\Lambda^3,\\
 C_{\rm pol}&=C_{\rm tan}+\sqrt2 C_{\rm mix}+C_{\rm rad}. \tag{P.11}
\end{aligned}
\]

To prove this, use \(\sin\theta=2s/(1+s^2)\).  The mixed block is

\[
 \sum_j\gamma_{ij}\ell_{ij}\tau_{ij}
 =\sum_j\sigma_{ij}\frac{2s_{ij}^2}{1+s_{ij}^2}\nu_{ij}. \tag{P.12}
\]

Pairing and the three middle estimates in (P.9), together with
\(|(2s^2/(1+s^2))'|\leq4s\), gives \(C_{\rm mix}h^{n+2}\).
For the tangent block, the tensor divergence identity

\[
 \sum_j\sigma_{ij}c_{ij}\otimes\nu_{ij}=|C_i|I_{T_i}
\]

gives

\[
 \sum_j\sigma_{ij}\sin\theta_{ij}\nu_{ij}\otimes\nu_{ij}
      -2|C_i|I_{T_i}
 =-2\sum_j\sigma_{ij}t_{ij}\otimes\nu_{ij}
  -2\sum_j\sigma_{ij}\frac{s_{ij}^3}{1+s_{ij}^2}
       \nu_{ij}\otimes\nu_{ij}.                  \tag{P.13}
\]

The last two estimates in (P.9), paired once more, give
\(C_{\rm tan}h^{n+2}\).  Finally the radial block is bounded by

\[
 \sum_j\gamma_{ij}\ell_{ij}^2
 =\sum_j\sigma_{ij}\frac{2s_{ij}^3}{1+s_{ij}^2}
 \leq C_{\rm rad}h^{n+2}.                         \tag{P.14}
\]

The radial, mixed, and tangent subspaces are mutually Frobenius orthogonal;
the displayed triangle bound proves (P.10).

## P.3 Why the compiler supplies (P.9)

In an ordinary collar record, use one smooth chart \(F\) across the collar
and a fixed centrally symmetric finite lattice direction list \(V=-V\).
At a grid point, in normal coordinates at \(x=F(u)\), Taylor's theorem gives

\[
 z_v=hA v+\frac{h^2}{2}B(v,v)+h^3R_v,
 \qquad \|R_v\|\leq R,                            \tag{P.15}
\]

uniformly for \(v\in V\).  The even second-order term is the same for
\(v\) and \(-v\).  Fix a strict Voronoi combinatorial margin \(\eta>0\) for
the finitely many reference lattices used by the compiler.  Every facet
vertex is the solution of an \(n\)-by-\(n\) linear system whose scaled
determinant is at least \(\eta\).  Expanding those systems through order two
and using \(\|G^{-1}\|\leq \|G\|^{n-1}/\eta\) gives precisely

\[
 \sigma_+-\sigma_-=O(h^n),\quad
 s_+-s_-=O(h^2),\quad
 \nu_++\nu_-=O(h),\quad
 t_+-t_-=O(h^3),                                  \tag{P.16}
\]

and \(t_\pm=O(h^2)\).  The constants are explicit polynomials in

\[
 n,|V|,\max_{v\in V}\|v\|,
 \|A\|,\|A^{-1}\|,\|B\|,R,\eta^{-1}.             \tag{P.17}
\]

The reflected collars use a single chart on both sides, so the same expansion
applies on a macroface.  At a terminal atlas stratum the compiler uses a full
signed-permutation orbit.  Its reference polar cell has \(t=0\) and scalar
normal covariance by irreducibility; the Hermite annulus has the ordinary
form (P.15).  Since the compiler has finitely many chart and terminal records,
the maxima of (P.17) give the global constants in (P.9).  Strict interval
enclosures of the determinants and inactive-face slacks certify \(\eta>0\).
This is a finite local calculation and is not a hidden global compatibility
or elasticity assertion.

## P.4 Sampling quotient and the final constant

The gnomonic Jacobian on \(|z|\leq\tan h\) is
\((1+|z|^2)^{-d/2}\).  Therefore the normalized weights
\(w_i=|C_i|/\sum_k|C_k|\) are a Voronoi Riemann rule.  Since

\[
 \int_{S^{d-1}}(x^TAx)^2\,d\bar\sigma(x)
   =\frac{2}{d(d+2)}\|A\|_F^2
 \quad (\operatorname{tr}A=0),                    \tag{P.18}
\]

and \(x\mapsto(x^TAx)^2\) is \(4\|A\|_F^2\)-Lipschitz, the spherical
Voronoi rule has error at most \(4h\|A\|_F^2\).  For \(h\leq1/4\),
\(\tan h\leq2h\), so replacing spherical cell areas by \(|C_i|\) and
renormalizing has error at most \(8dh^2\|A\|_F^2\): indeed the relative
cellwise Jacobian error is at most \(2dh^2\), and normalization multiplies
its total-variation bound by at most two.  Consequently, for

\[
 h\leq h_{\rm samp}:=\frac{1}{8d(d+2)}
\]

the elementary cellwise estimate gives

\[
 \sum_iw_i(x_i^TAx_i)^2\geq\frac1{d(d+2)}\|A\|_F^2. \tag{P.19}
\]

Thus sampling is injective at these levels.  From
\((R_2A)_i=\langle M_i,A\rangle_F\), (P.10), and (P.19),

\[
 \mathfrak D_2
 \leq \sqrt{d(d+2)}\frac{C_{\rm pol}}v h^2.       \tag{P.20}
\]

Together, (P.8) and (P.20) give the P1E upper theorem with

\[
 R_d=\frac{(d-1)\pi^2}{2q^2},
 \qquad
 C_d=\sqrt{d(d+2)}\frac{C_{\rm pol}}v.            \tag{P.21}
\]

## P.5 Necessary failure fixtures

The normalized integer \(\ell^1\)-shell
\(\{k/\|k\|:k\in\mathbb Z^d,\ \sum|k_a|=N\}\) is quasiuniform and its polar
weights satisfy (P.2)--(P.8), but it does not satisfy (P.9) at the fixed
orthant seams.  This failure has an exact all-orders certificate in \(d=3\).
Let \(N=2m\) and take the seam node
\(x=(m,0,m)/\|(m,0,m)\|\).  In the tangent basis
\(e_y,(e_1-e_3)/\sqrt2\), put

\[
 s=\sqrt{m^2+1}-m,\qquad
 U=\frac{2\sqrt{m^2-m+1}-(2m-1)}{\sqrt2}.
\]

Directly intersecting the six active polar halfspaces gives

\[
 C_x=\{(y,t): |t|\leq s,\ |y|+|t|/\sqrt2\leq U\},
 \qquad
 \mu_x=4Us-\sqrt2s^2.                              \tag{P.21a}
\]

The normalized tangent covariance is diagonal.  If \(E\) denotes this
covariance minus \(2I\), its entries are

\[
\begin{aligned}
 E_{yy}
 &=\frac{4s}{\sqrt{2(m^2-m+1)}\,\mu_x}-2
   =-\frac1{2m}+O(m^{-2}),\\
 E_{tt}
 &=\frac{4(U-s/\sqrt2)}{\sqrt{m^2+1}\,\mu_x}
   +\frac{2s}{\sqrt{2(m^2-m+1)}\,\mu_x}-2
   =\frac1{2m}+O(m^{-2}).                          \tag{P.21b}
\end{aligned}
\]

The cell is centrally symmetric, so its mixed block vanishes, and its radial
block is \(O(m^{-2})\).  Therefore

\[
 \lim_{m\to\infty}m\|M_x\|_F=\frac1{\sqrt2},
 \qquad
 \lim_{N\to\infty}N\|M_x\|_F=\sqrt2.              \tag{P.21c}
\]

Thus the raw shell has a genuine \(\Theta(h)\) seam defect.
Hyperoctahedral global symmetry alone does not replace a smooth reflected
collar or a terminal tight-frame template.

## P.6 Status of the exact shared moment-cone alternative

The stronger cone that additionally imposes the mixed and trace-free tangent
moments exactly is not used here.  A purely local clique proof of a uniform
Slater margin would silently require a global inverse.  There is an exact
low-frequency certificate for this issue.  For a fixed \(a\in\mathbb R^d\),
put

\[
 u_i=P_i a.
\]

For the adjoint of tangent equilibrium one has, on every edge,

\[
\begin{aligned}
 (T_x^*u)_{ij}
 &=u_i\cdot\tau_{ij}+u_j\cdot\tau_{ji}\\
 &=\ell_{ij}\,a\cdot(x_i+x_j).                    \tag{P.22}
\end{aligned}
\]

Hence an angular window \(\theta_{ij}\leq\Lambda h\) gives

\[
 \|T_x^*u\|_{\ell^\infty(E)}
 \leq \Lambda^2h^2\|a\|.                          \tag{P.23}
\]

On an \(h\)-dense set, \(\max_i\|P_i a\|\geq\cos(h)\|a\|\).  Thus this
nonrotational, global mode has order-one vertex norm but only order-\(h^2\)
edge strain.  In the natural scaling in which a generic local strain is
order \(h\), the dual margin is at most order \(h\).  Mixed and trace-free
dual variables have edge coefficients of orders \(h^3\) and \(h^2\);
allowing them does not produce an \(h\)-independent local coercivity estimate.

Equation (P.22) does not prove that the exact cone is empty.  It proves that
local row cones and a finite clique rank calculation cannot supply the
claimed uniform shared margin: controlling these global low modes is a
discrete Korn/spectral theorem.  Accordingly the exact all-moment Slater
route is recorded as **BLOCKED**, while the polar route proves the result
needed for P1E using exact tangent equilibrium and a local \(O(h^2)\) moment
bound.
