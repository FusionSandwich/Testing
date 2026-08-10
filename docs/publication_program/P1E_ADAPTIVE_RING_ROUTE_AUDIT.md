# P1E adaptive iso-latitude route audit

This note records the independent adaptive-ring route and the obstruction to
the natural equal-gap aligned-outgoing construction.  The obstruction remains
valid.  The later no-guard shortened-gap repair is now completed separately in
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`; the historical candidate schedule in
Section 7.2 is superseded by that file and its literal certification scripts.

Throughout this note (S^2\subset\mathbb R^3),

\[
 \Omega(\theta,\phi)
 = (\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta).
\]

The tangent basis at \(\phi=0\) is

\[
 e_\theta=(\cos\theta,0,-\sin\theta),\qquad e_\phi=(0,1,0).
\]

## 1. A quasiuniform dyadic ring set

Fix a polar offset (a\in(1,3/2)), put

\[
 h_K={\pi\over 2(K+a-1/2)},\qquad
 \theta_k=(k+a-1)h_K\quad(1\le k\le K),
\]

and reflect these rings through the equator.  Add the two poles.  On the
northern ring choose

\[
 M_k=\max\left\{32,
  2^{\lceil\log_2(4\pi\sin\theta_k/h_K)\rceil}\right\}.
                                                        \tag{1.1}
\]

Consecutive counts have ratio (1) or (2).  The nearest-neighbor chord on
a ring is between fixed positive multiples of (h_K), the polar gap is
(a h_K), and every meridional gap except the central reflected gap is
(h_K).  Thus the fill distance, separation, and mesh ratio have constants
depending only on (a).  Ring jumps of at most eight longitude steps and the
interface mask below have an angular window bounded independently of (K).

These elementary mesh facts do **not** solve the generator problem: the
count-changing edges still have to be reconciled with shared conductances and
the quadratic moment equations.

## 2. Exact positive (2{:}1) Fourier mask

Let a coarse ring have (M\ge16) nodes
(\phi_i=2\pi i/M), and let the fine ring have (2M) nodes
(\psi_j=\pi j/M).  Set

\[
 \alpha={\pi\over M},\qquad c=\cos\alpha,
\]

\[
 p={4c^2+2c-1\over4c(c+1)},\qquad
 q={(2c+1)(4c^2+2c-1)\over8c^2(c+1)}.                \tag{2.1}
\]

For the offset (s=j-2i\pmod {2M}), define the rectangular coupling (Q)
by

\[
\begin{array}{c|ccccccl}
s&0&2&-2&1&-1&3&-3\\ \hline
Q_{i,2i+s}&p/2&(1-p)/4&(1-p)/4&q/4&q/4&(1-q)/4&(1-q)/4.
\end{array}                                             \tag{2.2}
\]

All unlisted entries vanish.  Direct summation gives

\[
 \sum_jQ_{ij}=1,\qquad \sum_iQ_{ij}={1\over2}.          \tag{2.3}
\]

Let (X=\cos(s\alpha)).  Conditional on an even fine vertex the reverse
law of (X) is the law

\[
 p\,\delta_1+{1-p\over2}
   (\delta_{\cos2\alpha}+\delta_{\cos2\alpha}),
\]

where the repeated atoms remember the two signs.  Conditional on an odd
fine vertex it is

\[
 {q\over2}(\delta_{\cos\alpha}+\delta_{\cos\alpha})
 +{1-q\over2}(\delta_{\cos3\alpha}+\delta_{\cos3\alpha}).
\]

The two laws have identical first and second moments.  Indeed their common
first moment is

\[
 \beta={1\over2}+{\cos2\alpha\over2\cos\alpha},         \tag{2.4}
\]

and (2.1) is obtained by solving

\[
\begin{split}
 p+(1-p)\cos2\alpha
 &=q\cos\alpha+(1-q)\cos3\alpha,\\
 p+(1-p)\cos^22\alpha
 &=q\cos^2\alpha+(1-q)\cos^23\alpha.                 \tag{2.5}
\end{split}
\]

Consequently the normalized conditional transfer of Fourier modes (1)
and (2) is the same in both directions and at both fine parities.  This is
an exact algebraic statement, not a numerical rank test.

For (0<\alpha\le\pi/16), elementary differentiation of (2.1) gives

\[
 {3\over5}<p\le{5\over8},\qquad
 {9\over10}<q\le{15\over16}.                           \tag{2.6}
\]

Every declared entry of (Q) is therefore at least (1/64), and the
interface degree is at most seven.  Thus positivity or bounded degree is not
the obstruction identified below.

## 3. Exact local ring equations

Write (s=\sin\theta), (c=\cos\theta), and let an ordinary ring have the
same count (M) as its two neighbors, with aligned longitudes and meridional
gap (h).  Put (\delta=2\pi/M) and

\[
 u_t=1-\cos(t\delta),\qquad
 \ell_t=s^2u_t,
 \qquad \ell_v=1-\cos h.                               \tag{3.1}
\]

The projected increments to the two aligned radial neighbors are

\[
 \tau_+=\sin h\,e_\theta,\qquad
 \tau_-=-\sin h\,e_\theta,
\]

whereas the two horizontal (t)-step increments are

\[
 \tau_t^\pm=-scu_t\,e_\theta
             \mathbin\pm s\sin(t\delta)\,e_\phi.       \tag{3.2}
\]

Let (U_+,U_-) be the per-vertex shared conductances to the outer and inner
rings and let (H_t) be the conductance of each horizontal (t)-edge.  The
three desired equations -- tangent centering, loss-weighted tangent
centering, and tangent isotropy -- are exactly

\[
 (U_+-U_-)\sin h-2sc\sum_tH_tu_t=0,                    \tag{3.3}
\]

\[
 (U_+-U_-)\sin h\,\ell_v
      -2s^3c\sum_tH_tu_t^2=0,                          \tag{3.4}
\]

and

\[
 (U_++U_-)\sin^2h
 +2s^2c^2\sum_tH_tu_t^2
 -2s^2\sum_tH_t(2u_t-u_t^2)=0.                         \tag{3.5}
\]

Equation (3.3), together with

\[
 \mu_i={1\over2}\sum_j\gamma_{ij}\ell_{ij},           \tag{3.6}
\]

gives exact (H_1) reproduction and reversibility.  Equations (3.4) and
(3.5) say respectively that the radial--tangential block vanishes and the
tangent covariance is isotropic.

With a single horizontal jump (t=1), equations (3.3) and (3.5) have the
explicit solution

\[
 U_\pm=H_1(B\pm A),                                    \tag{3.7}
\]

\[
 A={scu_1\over\sin h},\qquad
 B={s^2\{\sin^2\delta-c^2u_1^2\}\over\sin^2h}.         \tag{3.8}
\]

It is strictly positive precisely when (B>|A|).  Its remaining mixed
moment is

\[
 \widehat h_\theta
 =2H_1scu_1(\ell_v-s^2u_1).                            \tag{3.9}
\]

At a fixed polar layer (\theta=rh), (3.9), divided by (3.6), is generally
of order (h/r), not (h^2).  This is why exact (H_1) and tangent
isotropy alone do not prove the P1E upper bound.

On an ordinary ring one can repair (3.9) positively using horizontal jumps
(1) and (8).  Equation (3.4) is equivalent to

\[
 H_1u_1(\ell_v-\ell_1)
 +H_8u_8(\ell_v-\ell_8)=0.                             \tag{3.10}
\]

Whenever

\[
 \ell_1<\ell_v<\ell_8,                                 \tag{3.11}
\]

(3.10) fixes a strictly positive ratio (H_8/H_1); (3.3) and (3.5) then
fix (U_\pm).  The dyadic choice (1.1), after increasing the harmless
minimum count if necessary, gives (3.11) with fixed margins away from the
count-changing interfaces.  Hence ordinary rings are not the obstruction.

## 4. Count-change obstruction for an aligned outgoing interface

The following asymptotic certificate rejects the most natural completion of
the ring construction.

Consider dyadic transitions with (M\to\infty) and transition radius
(r_M\) satisfying (0<\rho_-\le r_M/M\le\rho_+<\infty) in coordinates
scaled by the meridional mesh length.  Use the exact mask (2.2) on the
coarse-to-fine interface, an aligned fine-to-fine interface immediately
after it, and any fixed collection of horizontal jumps of bounded longitude
offset.  Assume the active conductances have the uniform positive margins
and upper bounds required by a local (r_{\max}=O(h^{-2})) construction.

At a vertex of the first fine ring, an incoming transition edge has the
scaled tangent increment

\[
 v_-=(-1,Y)+o(1),                                      \tag{4.1}
\]

where the mask has

\[
 \mathbb E Y=0,
 \qquad \mathbb E Y^2=\sigma^2>0.                     \tag{4.2}
\]

For (2.2), (p\to5/8), and the even law already gives
(\mathbb E(s_{\rm off})^2=3/2); hence (4.2) has a
strict lower bound depending only on (\rho_-).  The aligned outgoing edge
has

\[
 v_+=(1,0)+o(1).                                       \tag{4.3}
\]

A bounded-offset horizontal edge at radius (r_M) has tangent component
(O(1)) but radial component (O(1/r_M)).  Its contribution to both radial
force and loss-weighted radial force is therefore (o(1)) under the stated
conductance bounds.

Let (U_-,U_+) be the total incoming and outgoing radial conductances at the
fine vertex.  Radial tangent centering forces

\[
 -U_-+U_+=o(1).                                        \tag{4.4}
\]

Since the scaled chordal loss is
(\tfrac12|v|^2+o(1)), loss-weighted radial centering forces

\[
 -{1+\sigma^2\over2}U_-+{1\over2}U_+=o(1).             \tag{4.5}
\]

Subtracting one half of (4.4) from (4.5) yields

\[
 -{\sigma^2\over2}U_-=o(1),                            \tag{4.6}
\]

contradicting the strict positive lower margin.  This is the dual
certificate behind the negative coefficient obtained when (3.3)--(3.5) are
solved directly at the first fine ring.  Adding more bounded horizontal
jumps does not change (4.6).

In the unscaled sphere the surviving normalized mixed block is at least
(c h) on that ring.  The last dyadic transition occurs at a latitude with
(\sin\theta\) bounded below, and a weight-comparable quasiuniform ring has
stationary mass at least (c'h).  Therefore

\[
 \sum_iw_i\|B_i\|_F^2\ge c''h^3.                       \tag{4.7}
\]

The accepted P1B two-defect trace inequality then gives

\[
 \mathfrak D_2\ge c'''h^{3/2},                         \tag{4.8}
\]

which rules out the required (O(h^2)) estimate for this construction
class.

One can avoid the immediate contradiction only by propagating nontrivial
diagonal angular variance through subsequent fine-to-fine interfaces, or by
dropping a uniform conductance/weight margin.  The former introduces a new
global shared-stress compatibility problem across every dyadic band; the
latter violates the requested strict feasibility hypothesis and can also
destroy the uniform rate or sampling bounds.  No unproved propagation lemma
is promoted here.

## 5. Recursive spherical joins

A recursive join

\[
 (\cos\theta,\sin\theta\,y),\qquad y\in S^{d-2},        \tag{5.1}
\]

inherits the same count-changing problem at each join pole.  Rowwise
feasibility on the (S^{d-2}) fibers does not reconcile the rectangular
couplings between successive fibers, and (4.4)--(4.6) applies to the radial
two-plane of any join which uses the aligned-outgoing ring mechanism.
Consequently the join route supplies neither a transfer theorem nor an
all-dimensional construction.  A valid join proof would have to provide a
shared multi-layer stress with uniform positivity, its full mixed-moment
control, and a sampling-quotient bound.  Those are precisely the missing
compatibility statements, so the route is recorded as blocked rather than
used as a reduction.

## 6. Registry decision

| route component | status | exact outcome |
|---|---|---|
| dyadic ring mesh | complete | quasiuniform, bounded degree/window after a coupling is supplied |
| (2{:}1) Fourier mask | complete | positive (1/64) margin; modes (0,1,2) transfer exactly in both directions |
| ordinary-ring moments | complete | equations (3.3)--(3.5); positive two-horizontal-jump repair |
| aligned-outgoing transition | blocked by certificate | incompatible equations (4.4)--(4.6); (h^{3/2}) defect floor |
| no-guard shortened-gap transition | complete for \(d=3\) | all-level construction and literal certificates are in `P1E_SHORT_GAP_S2_CONSTRUCTION.md` |
| recursively joined rings | blocked | the \(S^1\)-fiber repair has no proved positive bounded-degree all-\(d\) transfer theorem |

The mask and the obstruction are retained as deterministic regression data.
They are not computational substitutes for the separate all-dimensional P1E
existence proof.

## 7. Post-audit repair: shorten the diagonal transition gap

The obstruction in Section 4 uses the same meridional length on the
diagonal and aligned interfaces.  There is a concrete way to remove that
hypothesis.  This section records the local mechanism that led to the repaired
no-guard construction.  The completed \(d=3\) theorem, its all-level schedule,
and its literal certification programs are in
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`.  The filename is historical; that
source now records a proved theorem, not a pending candidate.

Use the mask \(Q\) on the single \(M\mathbin{:}2M\) interface.  In scaled
tangent coordinates its angular variance is

\[
 \sigma^2={3\over2}a^2+o(1),\qquad
 a={\sin\theta\,\pi\over Mh}.
\]

At the dyadic threshold \(a\to1/4\), so

\[
 \sigma^2\longrightarrow {3\over32}.
\]

Keep ordinary aligned meridional gaps equal to \(h\), but shorten the
count-changing gap to

\[
 g h,\qquad g=\sqrt{1-{3\over2}a^2}.
                                                        \tag{7.1}
\]

In the frozen flat problem an incoming aligned edge has vector \((-1,0)\)
and an outgoing transition edge has vector \((g,Y)\).  Consequently

\[
 g^2+\mathbb E Y^2=1.                                  \tag{7.2}
\]

Choosing the transition total so that \(U_Qg=U_-\) cancels both the radial
force and the loss-weighted radial force.  At the fine endpoint the column
sum of \(Q\) is \(1/2\), so the outgoing aligned total is

\[
 U_+={gU_Q\over2}={U_-\over2}.                         \tag{7.3}
\]

Thus the angular variance is converted into a shorter radial displacement;
it is not discarded.

### 7.1 General exact row matrix

Let the incoming and outgoing gaps be \(h_-\) and \(h_+\).  Put

\[
 s=\sin\theta,quad c=\cos\theta,quad
 s_\pm=\sin(\theta\pm h_\pm),\quad
 \ell_\pm=1-\cos h_\pm.
\]

For a symmetric longitude kernel write

\[
 m_{1,\pm}=\mathbb E(1-\cos\Delta_\pm),\qquad
 m_{2,\pm}=\mathbb E(1-\cos\Delta_\pm)^2.
\]

The coefficients of \(U_+\) and \(U_-\) in tangent force are

\[
 \sin h_+-cs_+m_{1,+},qquad
 -\sin h_--cs_-m_{1,-}.                               \tag{7.4}
\]

Their coefficients in loss-weighted tangent force are

\[
 \begin{split}
 G_+={}&\sin h_+\ell_+
 +(\sin h_+\,s s_+-cs_+\ell_+)m_{1,+}
 -cs s_+^2m_{2,+},\\
 G_-={}&-\sin h_-\ell_-
 +(-\sin h_-\,s s_--cs_-\ell_-)m_{1,-}
 -cs s_-^2m_{2,-}.
 \end{split}                                           \tag{7.5}
\]

Their coefficients in theta-minus-phi covariance are

\[
 \begin{split}
 I_+={}&\sin^2h_+-2\sin h_+cs_+m_{1,+}
 +s_+^2\{(1+c^2)m_{2,+}-2m_{1,+}\},\\
 I_-={}&\sin^2h_-+2\sin h_-cs_-m_{1,-}
 +s_-^2\{(1+c^2)m_{2,-}-2m_{1,-}\}.
 \end{split}                                           \tag{7.6}
\]

For a horizontal jump \(t\), with \(u_t=1-\cos(t\delta)\), the three
coefficients remain

\[
 -2scu_t,\qquad -2s^3cu_t^2,\qquad
 2s^2\{c^2u_t^2-(2u_t-u_t^2)\}.                       \tag{7.7}
\]

Equations (7.4)--(7.7) are the exact shared six-equation transition system:
three rows at the coarse endpoint and three at the fine endpoint.  Its six
unknowns, after fixing the incoming coarse total, are the shared \(Q\) total,
the outgoing fine total, and the two horizontal conductances at each endpoint.

At \(a=1/4\) and \(g=\sqrt{29/32}\), the scaled limiting coarse solution has

\[
 H_1={40\over21}+{1369\sqrt{58}\over6496}>0,\qquad
 H_8={1\over672}+{3\sqrt{58}\over14336}>0.             \tag{7.8}
\]

The fine endpoint also has a strictly positive limiting solution.  Retaining
that the transition angle \(\alpha\) is based at the coarse latitude gives

\[
 H_{1,f}={64\over21}+{895\sqrt{58}\over2436}>0,\qquad
 H_{8,f}={5\over336}+{197\sqrt{58}\over155904}>0.       \tag{7.9}
\]

Thus the full limiting vector is approximately

\[
 (U_Q,U_{+,f},H_{1,c},H_{8,c},H_{1,f},H_{8,f})
 \longrightarrow
 (1.05045,0.5,3.50975,0.0030818,5.84570,0.0245042).
                                                               \tag{7.10}
\]

For an inverse audit, use the first curvature coefficients of the two radial
totals together with the four limiting horizontal conductances as the six
unknowns.  After the force, modified loss-force, and isotropy rows are scaled
by their first nonzero powers of \(h\), the exact limiting matrix is

\[
\begin{pmatrix}
-29/8&\sqrt{58}/8&8\sqrt{58}&0&0&0\\
-29/8&\sqrt{58}/32&128\sqrt{58}&0&0&0\\
0&\sqrt{58}/8&8\sqrt{58}&0&0&0\\
29/8&0&0&-\sqrt{58}&\sqrt{58}/16&4\sqrt{58}\\
29/8&0&0&-\sqrt{58}&\sqrt{58}/256&16\sqrt{58}\\
0&0&0&0&\sqrt{58}/16&4\sqrt{58}
\end{pmatrix}.                                             \tag{7.11}
\]

It has

\[
 \det A_\infty={96799941\sqrt{58}\over512}>1.439\times10^6,
 \qquad \|A_\infty^{-1}\|_\infty<2.668.                    \tag{7.12}
\]

Thus the large-transition proof can use an ordinary Neumann perturbation
bound, not a floating-point rank decision.

The executable audit is

`afp_barrier_gate1/pure_math/covariance/p1e_short_gap_ring_audit.py`.
It evaluates the exact formulas and the one-layer overshoot mutation.  Its
floating-point output remains regression evidence.  The all-orders proof does
not rely on it: the theorem source above cites the symbolic matrix, rational
Cauchy guard, polar guard, proof, full-family, and hostile-referee audits.

### 7.2 Supersession by the no-guard all-level construction

The former band-fill proposal with ordinary gaps \(q_mh\) was not promoted:
the rows at a \(q_mh/h\) junction can leave the positive moment cone.  The
repaired schedule removes those guard rows.  Every nontransition meridional
gap is exactly \(h\); each count-doubling location is chosen on the nearest
reachable \(h\)-grid ring; the sole gap across that interface is shortened;
and the final scale is chosen so reflection closes exactly at the equator.
The complete definitions and bounds are in
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`.

The five former proof obligations have the following definitive disposition.

| former obligation | disposition |
|---|---|
| 1. Uniform scaled six-by-six transition inverse and positivity | discharged for \(d=3\) by the literal normalized matrix and all-orders compact-box certificate |
| 2. Polar cap, first ring, and finite exceptional rows | discharged for \(d=3\) by the polar certificate and exact ordinary-row bracketing |
| 3. Equator closure and uniform mesh, mass, degree, conductance, and rate bounds | discharged for \(d=3\) by the no-guard all-level schedule and full-family audit |
| 4. Quadratic defect estimate | discharged for \(d=3\): \(B_i=0\), and the diagonal radial multiplier gives \(\mathfrak D_2\le3\ell_{\max}=O(h^2)\) directly on the sampled quotient |
| 5. Higher-dimensional fiber transfer | **still blocked**: the present construction has an \(S^1\) fiber and proves only the \(S^2\subset\mathbb R^3\) case; no positive bounded-degree all-dimensional join theorem has been established |

Thus items 1--4 are complete for \(d=3\).  Item 5 is the remaining boundary;
the \(d=3\) result must not be cited as an all-dimensional construction.

The equal-gap fixed-width no-go remains valid.  More generally, in the flat
strip the two shared cut fluxes

\[
 J_1(e)=\gamma_e x_e,\qquad
 J_3(e)=\gamma_e|v_e|^2x_e
\]

are separately conserved by exact tangent force and loss-weighted tangent
force.  An equal-gap diagonal far field has \(J_3/J_1=1+\sigma^2\), whereas
an aligned far field has ratio \(1\).  The shortened gap works precisely
because (7.2) makes both ratios equal to \(1\).

For clarity, when the three exact row equations hold and

\[
 \mu_i={1\over2}\sum_j\gamma_{ij}\ell_{ij},
\]

the only unremoved part of the ambient quadratic moment is generated by
\(\sum_j\gamma_{ij}\ell_{ij}^2\).  Since

\[
 \sum_j\gamma_{ij}\ell_{ij}^2
 \le \ell_{\max}\sum_j\gamma_{ij}\ell_{ij}
 =2\mu_i\ell_{\max},
\]

the normalized trace imbalance is at most \(2\ell_{\max}=O(h^2)\).
Combining its radial eigenvalue with the two equal tangent eigenvalues gives
the existing P1B bound of the form
\(\mathfrak D_2\le 3\ell_{\max}\) after the sampling quotient is applied.
