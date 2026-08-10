# P1E finite shared moment cone

This finite theorem is the independent local-tight-frame/convex route retained
by P1E.  It is stronger locally than the asymptotic construction, but its
hypothesis is a **shared edge** stress and therefore does not confuse rowwise
feasibility with global reversibility.

Put \(n=d-1\), \(P_i=I-\Omega_i\Omega_i^T\),
\(\ell_{ij}=1-\Omega_i\cdot\Omega_j\), and
\(\tau_{ij}=P_i\Omega_j\).  On \(T_{\Omega_i}S^{d-1}\), set

\[
 Q_i(v)=vv^T-\frac{\|v\|^2}{n}P_i.
\]

Suppose an undirected graph carries shared numbers
\(\gamma_{ij}=\gamma_{ji}>0\) satisfying at every vertex

\[
 \sum_j\gamma_{ij}\tau_{ij}=0,
\qquad
 \sum_j\gamma_{ij}\ell_{ij}\tau_{ij}=0,
\qquad
 \sum_j\gamma_{ij}Q_i(\tau_{ij})=0.                 \tag{1}
\]

Define

\[
 \mu_i=\frac1n\sum_j\gamma_{ij}\ell_{ij},
\qquad
 W=\sum_i\mu_i,
\qquad
 w_i=\frac{\mu_i}{W},
\qquad
 a_{ij}=\frac{\gamma_{ij}}{\mu_i}.                 \tag{2}
\]

Then \(w_i>0\), \(\sum_iw_i=1\), and

\[
 w_ia_{ij}=\gamma_{ij}/W=w_ja_{ji}.
\]

The first equation in (1), followed by radial contraction, gives

\[
 \sum_j\gamma_{ij}(\Omega_j-\Omega_i)
 =-n\mu_i\Omega_i.
\]

Hence

\[
 L1=0,\qquad L\Omega=-n\Omega.                     \tag{3}
\]

Let

\[
 \epsilon_i=\sum_ja_{ij}\ell_{ij}^2,
\qquad
 T_i=\sum_ja_{ij}\tau_{ij}\tau_{ij}^T.
\]

The third equation in (1) makes \(T_i\) scalar on the tangent space.  Since

\[
 \operatorname{tr}T_i
 =\sum_ja_{ij}\ell_{ij}(2-\ell_{ij})
 =2n-\epsilon_i,
\]

\[
 T_i=\left(2-\frac{\epsilon_i}{n}\right)P_i.
\]

The middle equation in (1) kills the radial--tangent block.  P1C therefore
gives

\[
 B_i=0,\qquad
 M_i=\frac d n\epsilon_iZ_i.                        \tag{4}
\]

Thus, directly on the sampled quotient,

\[
 \mathfrak D_2
 \le\frac d n\max_i\epsilon_i
 \le d\,\ell_{\max}.                                \tag{5}
\]

If all active angular edges lie in
\(\lambda h\le\theta_{ij}\le\Lambda h\le\pi\), then

\[
 r_{\max}\le\frac{n\pi^2}{2\lambda^2}h^{-2},
\qquad
 \mathfrak D_2\le\frac{d\Lambda^2}{2}h^2.           \tag{6}
\]

Equations (1) are linear in the shared edge variables.  A strictly positive
solution is equivalently a Slater point of this finite moment cone.  The
octahedral \(21/4\) cycle fixture shows why independent positive solutions of
the directed row equations cannot replace this shared feasibility statement.
