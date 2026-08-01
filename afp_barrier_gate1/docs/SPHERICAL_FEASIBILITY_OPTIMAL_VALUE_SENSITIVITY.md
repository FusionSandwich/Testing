# Explicit optimal-value sensitivity for the local spherical row problem

This note strengthens Section 3.4 of
`SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`.  That section gives an explicit
change bound for a selected robust feasible row.  Here the bound is transferred
to the actual optimum of any bounded linear row objective, even when an old
optimizer lies on the boundary of the feasible barycentric polytope.

## 1. Setup

Let

\[
 \Lambda(U)=\{\lambda\ge0:\mathbf1^T\lambda=1,
                  \sum_j\lambda_ju_j=0\}
\]

and, for angles in a common window
\(0<\theta_-\le\theta_j\le\theta_+\le\pi/2\), define

\[
 s_j=\sin\theta_j,\qquad q_j=\tan(\theta_j/2),\qquad
 Q(\lambda)=\sum_j\lambda_jq_j,
\]

\[
 F_\theta(\lambda)_j={2\lambda_j\over s_jQ(\lambda)}.            \tag{1.1}
\]

Put

\[
 s_-=\sin\theta_-,\quad s_+=\sin\theta_+,\quad
 q_-=\tan(\theta_-/2),\quad q_+=\tan(\theta_+/2),               \tag{1.2}
\]

\[
 L_q={1\over2\cos^2(\theta_+/2)}.                               \tag{1.3}
\]

Let the old tangent hull have relative/full-dimensional margin at least
\(\rho>0\), let \(m\) be the number of indexed candidates, and define

\[
 \delta={\rho\over m(1+\rho)},\qquad
 K_0=1+{2(1+\sqrt m)\over\rho}.                                 \tag{1.4}
\]

By the controlled-dependence theorem, there is
\(\lambda^0\in\Lambda(U)\) with \(\lambda_j^0\ge\delta\).

For a cost vector \(c\) with \(\|c\|_\infty\le C\), define the attained optimum

\[
 V(U,\theta;c)=\min_{\lambda\in\Lambda(U)}c^TF_\theta(\lambda). \tag{1.5}
\]

Attainment follows because \(\Lambda(U)\) is compact and the denominator in
(1.1) is at least \(q_->0\).

## 2. Sharper coefficientwise upper bound from the cone margin

The constructed vector satisfies

\[
 \delta\le\lambda_j^0\le1-(m-1)\delta.                          \tag{2.1}
\]

Because \(s_jQ\ge s_-q_-=1-\cos\theta_-\), its rates obey

\[
 \boxed{
 {2\delta\over1-\cos\theta_+}
 \le F_\theta(\lambda^0)_j
 \le {2[1-(m-1)\delta]\over1-\cos\theta_-}.}                   \tag{2.2}
\]

The lower and upper bounds in (2.2) both use the cone margin.  The wider
loss-only bound remains
\(0\le a_j\le2/(1-\cos\theta_-)\).

Under the angular window `0 < c1 <= c2` and
`c1 h <= theta_j <= c2 h` from the main theorem,
(2.2) gives

\[
 {4\delta\over c_2^2h^2}
 \le a_j
 \le {4[1-(m-1)\delta]\over\kappa_0^2c_1^2h^2}.                \tag{2.3}
\]

## 3. Lipschitz constant for changing only barycentric coefficients

For \(\lambda,\mu\in\Lambda(U)\), direct subtraction of (1.1) gives

\[
 \|F_\theta(\lambda)-F_\theta(\mu)\|_1
 \le K_\lambda\|\lambda-\mu\|_1,                               \tag{3.1}
\]

where

\[
 \boxed{K_\lambda={2\over s_-q_-}
       +{2s_+q_+\over s_-^2q_-^2}.}                             \tag{3.2}
\]

Indeed,
\(|Q(\lambda)-Q(\mu)|\le q_+\|\lambda-\mu\|_1\), and the two
reciprocal denominators are bounded below by \(s_-q_-\).

For simultaneous coefficient and angle changes, define

\[
 \mathcal B(\Delta,\varepsilon_\theta)=
 {2\Delta\over s_-q_-}
 +{2\left[\varepsilon_\theta q_+
  +s_+\left(q_+\Delta+L_q\varepsilon_\theta\right)\right]
  \over s_-^2q_-^2}.                                           \tag{3.3}
\]

Then the main perturbation calculation states

\[
 \|F_{\theta'}(\lambda')-F_\theta(\lambda)\|_1
 \le\mathcal B(\|\lambda'-\lambda\|_1,\varepsilon_\theta).      \tag{3.4}
\]

## 4. Robustifying a boundary optimizer

Let \(\lambda^*\) attain (1.5).  It may have zero coefficients.  For
\(0\le\eta\le1\), set

\[
 \lambda^\eta=(1-\eta)\lambda^*+\eta\lambda^0.                 \tag{4.1}
\]

Then

\[
 \lambda_j^\eta\ge\eta\delta,\qquad
 \|\lambda^\eta-\lambda^*\|_1\le2\eta,                        \tag{4.2}
\]

and (3.1) gives the explicit robustification price

\[
 c^TF_\theta(\lambda^\eta)-V(U,\theta;c)
 \le2CK_\lambda\eta.                                           \tag{4.3}
\]

Thus no assumption that an optimizer itself is strictly positive is needed.

## 5. Perturbed optimum

Identify tangent planes orthogonally and assume

\[
 \max_j\|u_j'-u_j\|\le\varepsilon_u,\qquad
 \max_j|\theta_j'-\theta_j|\le\varepsilon_\theta,               \tag{5.1}
\]

with both angle sets in the common window.  Assume full two-dimensional
spanning, or perturbations constrained to a fixed relative span.  Suppose

\[
 \varepsilon_u\le
 \min\left\{{\rho\over2},{\delta\over2K_0}\right\}.             \tag{5.2}
\]

Choose

\[
 \eta={2K_0\varepsilon_u\over\delta}\le1.                      \tag{5.3}
\]

The augmented-barycentric right-inverse construction corrects
\(\lambda^\eta\) to a vector \(\lambda'\in\Lambda(U')\) satisfying

\[
 \|\lambda'-\lambda^\eta\|_1
 \le\sqrt mK_0\varepsilon_u,\qquad
 \lambda_j'\ge{\eta\delta\over2}\ge0.                          \tag{5.4}
\]

Combining (4.3), (3.3), and (5.4) proves the actual optimal-value bound

\[
 \boxed{
 V(U',\theta';c)-V(U,\theta;c)
 \le {4CK_\lambda K_0\over\delta}\varepsilon_u
 +C\,\mathcal B(\sqrt mK_0\varepsilon_u,
                 \varepsilon_\theta).}                          \tag{5.5}
\]

This is fully explicit in the number of candidates, cone margin, tangent and
angle perturbations, and angular window.  It contains no asymptotic notation.
For the outgoing-rate objective, take \(c_j=1\) and \(C=1\).

If both configurations have margin at least a common lower bound \(\bar\rho\)
and share the same angular window, apply (5.5) in both directions with the
constants formed from \(\bar\rho\).  This gives the symmetric estimate

\[
 |V(U',\theta';c)-V(U,\theta;c)|
 \le {4CK_\lambda K_0\over\delta}\varepsilon_u
 +C\,\mathcal B(\sqrt mK_0\varepsilon_u,
                 \varepsilon_\theta).                           \tag{5.6}
\]

If the objective also changes from \(c\) to \(c'\), add

\[
 \|c'-c\|_\infty\,{2\over1-\cos\theta_-}                       \tag{5.7}
\]

because every feasible perturbed row has outgoing rate at most the displayed
loss-window constant.

## 6. Boundary limitation

At \(\rho=0\), the right side of (5.2) collapses to zero.  This is necessary,
not an artifact of the proof: the rational three-direction family in the exact
regression suite crosses from feasible boundary to infeasible under
arbitrarily small tangent perturbations.  Likewise, a one-dimensional
relative-interior configuration is robust only under perturbations preserving
its relative span; unrestricted ambient perturbations can destroy feasibility.
