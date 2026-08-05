# Shortened-gap adaptive rings on \(S^2\): complete \(d=3\) theorem

## Status

**COMPLETE FOR \(d=3\), with the fixed constants stated below.**  This version
removes the invalid band-closing gaps and invalid polar rounding argument from
the previous draft.  The continuous transition and polar boxes are closed by
literal symbolic derivations plus rational Cauchy bounds.  The finite-level
generator is retained as regression evidence, not as a substitute for those
all-orders certificates.

The construction is only for \(S^2\) (ambient dimension \(d=3\)).  No
all-dimensional join theorem is asserted.

## 1. Constants and the no-guard latitude schedule

Fix
\[
 M_0=2^{80},\qquad a_0={4\over3},\qquad
 g=\sqrt{29\over32}.
\]
For a level \(J\ge1\), let
\[
 M_m=M_0 2^m\quad(0\le m\le J),\qquad
 S_0={M_J\over8},
\]
and define the ideal dimensionless transition positions
\[
 t_m^0={M_J\over4\pi}\arcsin(2^{m-J})
       \quad(0\le m<J).                              \tag{1.1}
\]
Let \(\operatorname{nint}\) denote nearest-integer rounding, with downward
tie breaking, and put
\[
 k_m=\operatorname{nint}(t_m^0-a_0-mg),\qquad
 K=\operatorname{nint}(S_0-a_0-Jg),                  \tag{1.2}
\]
\[
 t_m=a_0+k_m+mg,\qquad S=a_0+K+Jg,qquad
 h={\pi\over2S}.                                      \tag{1.3}
\]
The north-polar first ring is at \(a_0h\).  Insert \(k_0\) ordinary gaps,
then a count-changing gap \(gh\); insert \(k_{m+1}-k_m\) ordinary gaps
between successive count-changing gaps, and \(K-k_{J-1}\) ordinary gaps
after the last one.  The last ring is exactly the equator.  Reflect the
northern edges across the equator, without duplicating the equatorial ring.

Thus every nontransition meridional gap is **exactly \(h\)**.  There are no
\(q_mh\) gaps and hence no unanalysed \(q_m/h\) junction rows.  The inequalities
\[
 |t_m-t_m^0|\le{1\over2},\qquad |S-S_0|\le{1\over2}   \tag{1.4}
\]
are immediate from (1.2).  Since consecutive ideal positions differ by more
than \(M_m/16\), all numbers of ordinary gaps in (1.3) are nonnegative.

The ring at a transition start \(t_mh\) has \(M_m\) vertices.  The short edge
doubles the count to \(2M_m=M_{m+1}\).  All intermediate rings retain that
count.  Put
\[
 a_m={\pi\sin(t_mh)\over M_mh}
     ={2S\over M_m}\sin\!\left({\pi t_m\over2S}\right). \tag{1.5}
\]
At \((S_0,t_m^0)\), the right side is exactly \(1/4\).  On the rectangle
specified by (1.4),
\[
 \left|{\partial a_m\over\partial t}\right|
 \le {\pi\over M_m},\qquad
 \left|{\partial a_m\over\partial S}\right|
 ={2\over M_m}|\sin\theta-\theta\cos\theta|
 \le {2\over M_m}.
\]
Consequently
\[
 \boxed{|a_m-\tfrac14|\le {3\over M_m}}.             \tag{1.6}
\]
This is the correlated compact transition box.  It is independent of \(J\)
and contains the equator-closing perturbation; treating latitude, \(h\), and
rounding phase as independent intervals would lose this fact.

## 2. Shared radial mask

On an aligned interface use identity longitude matching.  On an
\(M:2M\) interface put \(\alpha=\pi/M\), \(c_\alpha=\cos\alpha\), and
\[
 p={4c_\alpha^2+2c_\alpha-1\over4c_\alpha(c_\alpha+1)},\qquad
 q={(2c_\alpha+1)(4c_\alpha^2+2c_\alpha-1)
       \over8c_\alpha^2(c_\alpha+1)}.                \tag{2.1}
\]
For \(r=j-2i\pmod {2M}\), the seven nonzero entries of \(Q\) are
\[
\begin{array}{c|rrrrrrr}
r&0&2&-2&1&-1&3&-3\\ \hline
Q_{i,2i+r}&p/2&(1-p)/4&(1-p)/4&q/4&q/4&(1-q)/4&(1-q)/4.
\end{array}                                           \tag{2.2}
\]
Direct algebra gives row sum one, column sum one half, and identical reverse
conditional cosine moments at both fine parities.  If
\[
 \beta={1\over2}+{\cos(2\alpha)\over2\cos\alpha},
\]
then the two loss moments used below are, correctly,
\[
 m_1=1-\beta,
 \qquad
 m_2=1-2\beta+\bigl[p+(1-p)\cos^2(2\alpha)\bigr].     \tag{2.3}
\]
Writing \(d_\alpha=1-\cos\alpha\), these have the cancellation-free forms
\[
 m_1=d_\alpha{2c_\alpha+1\over2c_\alpha},\qquad
 m_2=d_\alpha^2{(c_\alpha+1)(2c_\alpha+1)\over c_\alpha}. \tag{2.4}
\]
Thus \(m_1/\alpha^2\to3/4\) and
\(m_2/\alpha^4\to3/2\).  For \(M\ge M_0\), (2.1) and
\(1-\alpha^2/2\le c_\alpha\le1\) give
\[
 {3\over5}<p<{5\over8},\qquad {9\over10}<q<{15\over16}; \tag{2.5}
\]
every declared mask entry is at least \(1/64\), and the interface degree is
seven.

## 3. Exact row equations

At latitude \(\theta\), write \(s=\sin\theta,c=\cos\theta\).  For an incoming
or outgoing radial kernel with meridional gap \(h_\pm\), neighbor sine
\(s_\pm=\sin(\theta\pm h_\pm)\), and loss moments
\(m_{1,\pm},m_{2,\pm}\), define
\[
 F_+=\sin h_+-cs_+m_{1,+},\qquad
 F_-=-\sin h_--cs_-m_{1,-},                           \tag{3.1}
\]
\[
\begin{split}
G_+={}&\sin h_+(1-\cos h_+)
 +(\sin h_+ss_+-cs_+(1-\cos h_+))m_{1,+}
 -css_+^2m_{2,+},\\
G_-={}&-\sin h_-(1-\cos h_-)
 +(-\sin h_-ss_--cs_-(1-\cos h_-))m_{1,-}
 -css_-^2m_{2,-},                                    \tag{3.2}
\end{split}
\]
\[
\begin{split}
I_+={}&\sin^2h_+-2\sin h_+cs_+m_{1,+}
 +s_+^2((1+c^2)m_{2,+}-2m_{1,+}),\\
I_-={}&\sin^2h_-+2\sin h_-cs_-m_{1,-}
 +s_-^2((1+c^2)m_{2,-}-2m_{1,-}).                    \tag{3.3}
\end{split}
\]
For a reflected horizontal pair with \(u=1-\cos\Delta\), the three column
entries are
\[
 (-2scu,\;-2s^3cu^2,\;2s^2[c^2u^2-(2u-u^2)])^T.      \tag{3.4}
\]
The three row equations are exactly tangent force, loss-weighted tangent
force, and theta/phi covariance equality.  Longitude reflection kills all
odd-phi equations; no approximate cancellation is used.

At a transition, the coarse row has incoming aligned gap \(h\) and outgoing
\(Q\)-gap \(gh\).  The fine row has incoming \(Q\)-gap \(gh\) and outgoing
aligned gap \(h\).  If \(R_c,R_f\) are the \(3\times4\) matrices (3.1)--(3.4),
with columns \((U_+,U_-,H_1,H_8)\), the exact shared system is
\[
 Bx=d,\qquad
 B=
 \begin{pmatrix}
 R_c[:,0]&0&R_c[:,2]&R_c[:,3]&0&0\\
 R_f[:,1]/2&R_f[:,0]&0&0&R_f[:,2]&R_f[:,3]
 \end{pmatrix},
 \quad
 d=\binom{-R_c[:,1]}{0}.                              \tag{3.5}
\]
The factor \(1/2\) is the exact column sum of \(Q\).  Therefore a solution of
(3.5) assigns one conductance to every undirected transition edge.

## 4. The exact normalized \(6\times6\) matrix

Put \(r=h/s=\pi/(Ma_m)\), \(\kappa=h\cot\theta=cr\), and use
\[
 U_Q=g^{-1}+\kappa A_c,qquad U_{+,f}={1\over2}+\kappa A_f. \tag{4.1}
\]
Let
\[
 D=\operatorname{diag}\left(
 {1\over h^2\cot\theta},{1\over h^4\cot\theta},{1\over h^2},
 {1\over h^2\cot\theta},{1\over h^4\cot\theta},{1\over h^2}
 \right),                                             \tag{4.2}
\]
and
\[
 E=\operatorname{diag}(-\sqrt{58}/2,-\sqrt{58},-\sqrt{58}/4,
                       -\sqrt{58},-2\sqrt{58},-\sqrt{58}/2). \tag{4.3}
\]
For
\[
 z=(A_c,H_{1,c},H_{8,c},A_f,H_{1,f},H_{8,f}),
\]
define the affine injection and baseline
\[
 Tz=(\kappa A_c,\kappa A_f,H_{1,c},H_{8,c},H_{1,f},H_{8,f}),
 \qquad x_0=(g^{-1},1/2,0,0,0,0).                    \tag{4.4}
\]
Here columns in (4.4) are placed in the order used in (3.5).  The normalized
system, with no suppressed reparameterization, is
\[
 \boxed{A(M,a_m,c)=EDBT,\qquad b(M,a_m,c)=ED(d-Bx_0).} \tag{4.5}
\]
Equations (2.4), (3.1)--(3.5), and (4.1)--(4.5) are the requested exact
guarded formula.  They are also the literal formula constructed by the proof
audit; an occurrence table is not used as a substitute for (4.5).

For removal of every apparent zero, the audit replaces
\[
 \sin z=z\,\operatorname{sinc}z,qquad
 1-\cos z={z^2\over2}\,\operatorname{cosc}z,          \tag{4.6}
\]
and uses (2.4).  Since a coarse jump eight has longitude argument
\(16\pi/M\), the guard domain is
\[
 |z|\le {16\pi\over M_0},                            \tag{4.7}
\]
not \(8\pi/M_0\).

For an explicit connection between the literal matrix and the semantic
majorant used in Section 6, let a row have base sine \(bs\), base cosine
\(c_0\), neighbor sine \(ns\), gap \(\lambda h=\lambda sr\), and put
\[
 M_1={m_1\over r^2},\qquad M_2={m_2\over r^4},\qquad
 U={u\over r^2},\qquad z=\lambda sr.
\]
After the substitutions (4.6), the outgoing radial column divided by
\((sr,s^3r^3,s^2r^2)\) is exactly
\[
\begin{split}
f_+={}&\lambda\operatorname{sinc}z-c_0nrM_1,\\
g_+={}&{\lambda^3\over2}\operatorname{sinc}z\operatorname{cosc}z
 +n\!\left(\lambda b\operatorname{sinc}zM_1
 -{c_0\lambda^2\over2}\operatorname{cosc}z\,rM_1\right)
 -c_0bn^2rM_2,\\
i_+={}&\lambda^2\operatorname{sinc}^2z
 -2\lambda c_0n\operatorname{sinc}z\,rM_1
 +n^2((1+c_0^2)r^2M_2-2M_1).                       \tag{4.8}
\end{split}
\]
For the incoming column, change the first terms in \((f,g)\) to their
negatives, change the \(\lambda b\operatorname{sinc}zM_1\) term to its
negative, and change the sign of the middle term in \(i\) to positive.  A
horizontal column is exactly
\[
 \left(-2b{c_0\over c}U,
       -2b^3{c_0\over c}U^2,
       2b^2[-2U+r^2(1+c_0^2)U^2]\right)^T.           \tag{4.9}
\]
At the coarse endpoint \(b=1,c_0=c\); at the fine endpoint
\(b=\sin(\theta+gh)/s\) and \(c_0=\cos(\theta+gh)\).  Multiplication by
\(\kappa=cr\), the column factor \(1/2\), and (4.3) gives (4.5) entry for
entry.  The symbolic audit verifies these factorizations against the literal
trigonometric program before taking a limit.

## 5. Exact limiting phase family and strict cone margin

Let
\[
 \eta=M(a_m-\tfrac14),\qquad y={\eta\over\pi c}.
\]
By (1.6), \(|\eta|\le3\); at every transition
\(0<\theta\le\pi/6+2h\), so \(c>6/7\), and hence \(|y|<7/6\).
Taking the removable limit \(M\to\infty\) in the literal formula (4.5)
gives
\[
A_0=
\begin{pmatrix}
-29/8&\sqrt{58}/8&8\sqrt{58}&0&0&0\\
-29/8&\sqrt{58}/32&128\sqrt{58}&0&0&0\\
0&\sqrt{58}/8&8\sqrt{58}&0&0&0\\
29/8&0&0&-\sqrt{58}&\sqrt{58}/16&4\sqrt{58}\\
29/8&0&0&-\sqrt{58}&\sqrt{58}/256&16\sqrt{58}\\
0&0&0&0&\sqrt{58}/16&4\sqrt{58}
\end{pmatrix},                                       \tag{5.1}
\]
\[
b_0(y)=
\begin{pmatrix}
-3/16\\ 63/512+3\sqrt{58}y/32\\13/8+\sqrt{58}/4\\
-3/16\\-285/512-3\sqrt{58}y/32\\13/8+\sqrt{58}/4
\end{pmatrix}.                                       \tag{5.2}
\]
Exact algebra gives
\[
 \det A_0={96799941\sqrt{58}\over512},\qquad
 \|A_0^{-1}\|_\infty<3.                             \tag{5.3}
\]
The six components of \(A_0^{-1}b_0(y)\) are
\[
 {29+4\sqrt{58}\over58},                             \tag{5.4a}
\]
\[
 -{\sqrt{58}(16\sqrt{58}y-640\sqrt{58}-4107)\over19488},
\quad
 {\sqrt{58}(16\sqrt{58}y+32\sqrt{58}+261)\over1247232}, \tag{5.4b}
\]
\[
 {\sqrt{58}(29+4\sqrt{58})\over464},                 \tag{5.4c}
\]
\[
 {\sqrt{58}(16\sqrt{58}y+895+128\sqrt{58})\over2436},
\quad
 -{\sqrt{58}(16\sqrt{58}y-40\sqrt{58}-197)\over155904}. \tag{5.4d}
\]
Using \(7615/1000<\sqrt{58}<7616/1000\) and \(|y|<7/6\), every entry is
positive and the smallest is greater than \(1/500\).  This proves a strict
positive limiting cone over the **whole rounding-phase box**, not just at its
centre.

## 6. Guarded all-orders remainder certificate

The all-orders statement is the following finite bound for
the exact straight-line program (2.4), (3.1)--(3.5), (4.1)--(4.6):
\[
 \sup_{\substack{0\le M^{-1}\le2^{-80}\\
                  |M(a-1/4)|\le3\\6/7\le c\le1}}
 \max\{\|A-A_0\|_{\max},\|b-b_0\|_\infty\}
 \le {10^{12}\over M}.                               \tag{6.1}
\]
It is checked after the cancellations (2.4) and (4.6), using
\[
 |\sin z-z|\le|z|^3/6,
 \quad |\cos z-(1-z^2/2)|\le|z|^4/24,
 \quad \pi\in(3,22/7),                               \tag{6.2}
\]
positive denominator guards \(a>1/5,c>6/7,c_\alpha>9/10\).  The literal
symbolic audit constructs every entry from (4.5) and proves its removable
value (5.1)--(5.2).  The rational Cauchy audit then works on the complex disk
\(|x|\le10^{-4}\), \(x=M^{-1}\).  It bounds the entire guarded radial
columns by \((3,45,103)\), every horizontal column by \(55\,000\), and hence
\[
 \sup_{|x|=10^{-4}}|A_{ij}|<10^6,
 \qquad \sup_{|x|=10^{-4}}|b_i|<10^7.                \tag{6.2a}
\]
The force and loss-force right-hand quotients are removable by the literal
symbolic calculation, so maximum modulus applies to them as well.  The
isotropy right-hand side has no such quotient and is bounded directly.
Cauchy's estimate, with distance greater than \(10^{-4}/2\), gives the
entrywise bounds printed by the audit,
\[
 {|A_{ij}-A_{0,ij}|\over x}\le2\cdot10^{10},
 \qquad {|b_i-b_{0,i}|\over x}\le2\cdot10^{11},      \tag{6.2b}
\]
which imply (6.1).  Changing a sign, the column factor \(1/2\), the mask
moment, or the jump-eight angle changes the literal symbolic input; the
finite-family hostile mutations independently fail the row residual.

Consequently
\[
 \|A_0^{-1}(A-A_0)\|_\infty
 \le {18\cdot10^{12}\over2^{80}}<2^{-35}.            \tag{6.3}
\]
The Neumann lemma and (5.4) give
\[
 \|A^{-1}b-A_0^{-1}b_0\|_\infty
 \le {3\over1-18\delta}(\delta+6\delta\|A_0^{-1}b_0\|_\infty)
 <244\delta<1/1000,
 \qquad \delta={10^{12}\over2^{80}},                 \tag{6.4}
\]
where the exact phase formulas (5.4) give
\(\|A_0^{-1}b_0\|_\infty<10\).  Hence all six transition
coefficients are positive throughout the all-level transition box.

## 7. Ordinary equal-gap rows and the exact telescoping recurrence

For an ordinary row, let \(\ell_v=1-\cos h\),
\(u_j=1-\cos\Delta_j\), \(K_j=H_ju_j\), and
\(x_j=s^2u_j/\ell_v\).  Choose two horizontal pairs with
\(x_-<1<x_+\).  For any \(K>0\), set
\[
 K_-={K(x_+-1)\over x_+-x_-},\qquad
 K_+={K(1-x_-)\over x_+-x_-},\qquad H_j=K_j/u_j.       \tag{7.1}
\]
These are positive and make the loss-weighted tangent equation exact.  The
other two equations give, with \(S_r=U_++U_-\), \(D_r=U_+-U_-\),
\[
D_r={2scK\over\sin h},\qquad
S_r={2s^2K\over\sin^2h}
 \left(2-{(1+c^2)(1-\cos h)\over s^2}\right).         \tag{7.2}
\]
If \(z=\tan(h/2)\cot\theta\), elementary half-angle algebra gives the
**exact shared-edge recurrence**
\[
 {U_+\over U_-}
 ={(1-z)(1+2z)\over(1+z)(1-2z)}.                     \tag{7.3}
\]
For \(\theta/h\ge4/3\), \(0<z<2/5\); hence both radial conductances are
positive.  Moreover
\[
\begin{split}
\log{U_+\over U_-}
={}&\log{\sin(\theta+h/2)\over\sin(\theta-h/2)}+E(z),\\
0\le E(z)&\le {16z^3\over1-4z^2}.                    \tag{7.4}
\end{split}
\]
This follows by expanding the four logarithms in (7.3); all coefficients of
\(E\) are nonnegative.  The sine quotient in (7.4) telescopes exactly over a
run of ordinary rows.

In the cap, enumerate ordinary latitudes as
\(\theta=(a_0+n)h\).  Since
\(\tan(h/2)\le(51/100)h\) and \(\cot\theta\le1/\theta\),
\(z\le(51/100)(a_0+n)^{-1}\).  Starting after the separately solved first row,
the denominator in (7.4) is greater than \(3/4\), and comparison with
\(\sum_{n\ge0}(a_0+1+n)^{-3}\) gives
\[
 \sum_{\text{cap ordinary rows}}E(z)<12.              \tag{7.5}
\]
The sine quotient in (7.4) telescopes, so cap radial conductances grow only
by the endpoint sine ratio (at most \(M_0\)) times \(e^{12}\); there is no
per-row constant accumulated through the cap.  Outside the cap, (1.6) gives
\(z\le8\pi/M_m\), and a dyadic band has fewer than \(M_m\) rows.  Therefore
\[
 \sum_{\text{all band rows}}E(z)
 \le 32(8\pi)^3\sum_{m\ge0}M_m^{-2}<1.               \tag{7.6}
\]
At a transition, (4.1), the bounded solution, and (1.6) give
\[
 {2M_mU_{+,f}/\sin(\theta+(g+1/2)h)
  \over M_mU_-/\sin(\theta-h/2)}=1+\varepsilon_m,
 \qquad |\varepsilon_m|< {256\over M_m}.             \tag{7.7}
\]
Indeed (6.4) and (5.4) give \(|A_f|<7\), while
\(\kappa=\pi c/(M_ma)<16/M_m\), so
\(|2U_{+,f}-1|<224/M_m\).  For
\(\rho=\sin(\theta-h/2)/\sin(\theta+(g+1/2)h)\), monotonicity of sine and
\(a>1/5\) give \(0<\rho\le1\) and
\(1-\rho<(g+1)\pi/(M_ma)<32/M_m\).  Therefore
\(|(2U_{+,f})\rho-1|<256/M_m\), proving (7.7) rather than assuming it.
Thus \(\prod_m(1+\varepsilon_m)\) is between
\(e^{-512/M_0}\) and \(e^{512/M_0}\).  Equations
(7.4)--(7.7), rather than a per-row bound iterated through \(J\), give global
shared-conductance bounds.  Including mask entries and horizontal solutions,
one may take the intentionally huge level-independent constants
\[
 \gamma_-=M_0^{-20},\qquad \gamma_+=M_0^{20}.         \tag{7.8}
\]

## 8. A cap rule that actually brackets

For an ordinary frozen-count cap row put
\[
 z_*={\ell_v\over\sin^2\theta},\qquad
 \phi_* =\arccos(1-z_*),\qquad \delta={2\pi\over M}.   \tag{8.1}
\]
Choose
\[
 t_- =\max\{1,\lfloor\phi_*/(2\delta)\rfloor\},
 \qquad t_+=\lceil2\phi_*/\delta\rceil.              \tag{8.2}
\]
For every ordinary row after the first, its latitude is no larger than the
next transition latitude.  Equation (1.6), with \(M\ge M_0\), gives its
angular aspect \(a=\pi\sin\theta/(Mh)<1/4+3/M<251/1000\).  The defining
identity in (8.1) gives
\(\sin(\phi_*/2)=\sin(h/2)/\sin\theta\).  Hence
\[
 R:={\phi_*\over\delta}
 \ge {M\sin(h/2)\over\pi\sin\theta}
 ={\sin(h/2)\over ah}>{499\over251}>{19\over10}.     \tag{8.2a}
\]
Also \(\theta/h\ge7/3\) gives \(0<\phi_*<1/2\).  The literal floor/ceiling
choices (8.2) therefore imply
\[
 \phi_*/4\le t_-\delta\le(10/19)\phi_*,
 \qquad2\phi_*\le t_+\delta\le(48/19)\phi_*.
\]
The half-angle identity, concavity of sine on \([0,\pi]\), and
\(x-x^3/6\le\sin x\le x\) give the deliberately loose rational box
\[
 {1\over16}<x_-={1-\cos(t_-\delta)\over z_*}<{1\over3},
 \qquad
 2<x_+={1-\cos(t_+\delta)\over z_*}<7.                \tag{8.3}
\]
Thus (7.1) has fixed fractional margins.  Use this same adaptive integer rule
on every ordinary constant-count band row (the transition endpoints alone
retain jumps \(1,8\) in (3.5)).  The same proof of (8.3) applies.
To pass from the loss bracket to the actual conductances, define
\[
 T={\ell_vU_-\over s^2K}
 ={1-\cos h\over\sin^2h}
 \left[2-{(1+c^2)(1-\cos h)\over s^2}
             -{c\sin h\over s}\right].              \tag{8.3a}
\]
The bounds \(\theta\ge7h/3\), \(z_*<1/10\), and
\(\tan(h/2)<(11/20)h\) give
\[
 {3\over5}<T<{101\over100}.                          \tag{8.3b}
\]
Using the literal floor/ceiling relation, rather than independent corners of
the loose box, in
\[
 {H_-\over U_-}={x_+-1\over x_-(x_+-x_-)T},\qquad
 {H_+\over U_-}={1-x_-\over x_+(x_+-x_-)T}
\]
now gives the fixed margins
\[
 {1\over100}U_-<H_-,H_+<100U_-.                     \tag{8.3c}
\]
This rule
does not claim that a grid jump approximates an arbitrarily prescribed
physical chord to relative error \(O(M_0^{-1})\); that rejected assertion was
false.

At the first ring, the incoming edge is the pole edge of length \(a_0h\), so
it is a separate \(3\times3\) system.  Choose longitude jumps nearest to the
fixed angular values \(3/8\) and \(9/8\).  Their angular rounding is at most
\(\pi/M_0\).  If \(u=1-\cos\Delta_1,v=1-\cos\Delta_2\), rational cosine
bounds give the displayed box.  Explicitly \(\pi/M_0<1/1000\), and on
\(x\in[x_-,x_+]\),
\(x_-^2/2-x_+^4/24<1-\cos x<x_+^2/2\); applying this to
\(3/8\pm1/1000\) and \(9/8\pm1/1000\) gives
\[
 1/20<u<1/10,qquad1/2<v<2/3.                         \tag{8.4}
\]
The removable \(h=0\) solution, relative to the incoming pole conductance,
is
\[
 U_+={2a_0^3\over(a_0-1)(2a_0+1)}={128\over33},       \tag{8.5}
\]
\[
 H_1=-{(a_0+1)(2a_0+2v-3)
        \over4u(a_0-1)(2a_0+1)(u-v)},\quad
 H_2={(a_0+1)(2a_0+2u-3)
        \over4v(a_0-1)(2a_0+1)(u-v)}.                \tag{8.6}
\]
On (8.4), \(U_+>3/2,H_1>1,H_2>1/20\).  The transition bound (6.1) does not
apply because these longitude angles are \(O(1)\).  The separate polar audit
constructs the normalized finite-\(h\) \(3\times3\) matrix on the box
\[
 0\le h\le2\pi/M_0,\quad (u,v)\text{ in (8.4)},\quad
 |\Delta_1-3/8|,|\Delta_2-9/8|\le\pi/M_0.            \tag{8.7}
\]
Its exact limiting determinant is
\(4a_0^3uv(a_0-1)(2a_0+1)(u-v)\), whose absolute value is at least
\(704/6075\).  The adjugate gives \(\|A_{\rm pol}(0)^{-1}\|_\infty<20\,000\).
On \(|h|\le10^{-2}\), rational Cauchy bounds give
\(|\partial_hA_{\rm pol}|\le22\,000\) and
\(|\partial_hb_{\rm pol}|\le1\,600\).  Since
\(h\le2\pi/2^{80}\), the Neumann product is less than \(10^{-12}\), so the
resolvent identity, with \(\|z_{\rm pol}(0)\|_\infty<64\), gives
\(\|z_{\rm pol}(h)-z_{\rm pol}(0)\|_\infty<10^{-6}\).  The strict
inequalities following (8.6) therefore persist at finite \(h\).
At the pole, equal conductances to the first ring make force,
loss-force, and tangent covariance exact by the full cyclic sum.

At the equatorial ring, reflection supplies equal incoming radial
conductances \(U\) from north and south.  Tangent force and loss-force cancel
pairwise.  With the horizontal jump \(2\), set
\[
 H_{\rm eq}={U\sin^2h\over\sin^2(2\delta_J)},
 \qquad \delta_J={2\pi\over M_J}.                     \tag{8.8}
\]
This is positive and makes the two tangent covariances exactly equal.  The
equator is therefore a separate, explicitly solved row class.

## 9. Geometry, exact reproduction, and the sampled quotient

The schedule has meridional gaps in \([gh,a_0h]\).  Horizontal active edges
and transition edges have length at most \(5h\).  With loose constants one
may take
\[
 q_*={1\over4M_0},\qquad \Lambda=5,qquad D=M_0,
 \qquad C_{\rm fill}=2.                               \tag{9.1}
\]
Separation follows from distinct latitudes or the ring spacing; fill follows
by moving meridionally to the nearest ring and then at most half a ring cell.
Disjoint geodesic balls of radius \(q_*h/2\), together with
\(2\pi(1-\cos r)\ge4r^2/\pi\) for \(r\le1\), give
\[
 N_h\le4\pi^2q_*^{-2}h^{-2}.                          \tag{9.2}
\]
This includes the two polar caps; no separate unproved cap-packing constant
is used.

Set
\[
 \mu_i={1\over2}\sum_j\gamma_{ij}\ell_{ij},\qquad
 W=\sum_i\mu_i,\qquad w_i={\mu_i\over W}.             \tag{9.3}
\]
The active-edge lower bound \(h/8\), the window \(5h\), (7.8), and the
degree bound give
\[
 {\gamma_-\over64\pi^2}h^2\le\mu_i
 \le {25D\gamma_+\over4}h^2.                         \tag{9.4}
\]
Together with (9.2), this yields the explicit normalized weight floor
\[
 w_i\ge {\gamma_-q_*^2\over1600\pi^4D\gamma_+}h^2.  \tag{9.5}
\]
The exact row equations give
\[
 \sum_j\gamma_{ij}(\Omega_j-\Omega_i)=-2\mu_i\Omega_i, \tag{9.6}
\]
so the normalized generator is reversible and satisfies
\(L1=0,L\Omega=-2\Omega\) exactly.  If
\(R_i=\sum_j\gamma_{ij}\ell_{ij}^2\), loss-force and tangent isotropy give
\[
 M_i=\operatorname{diag}(R_i/\mu_i,-R_i/(2\mu_i),-R_i/(2\mu_i))
 ={3R_i\over2\mu_i}Z_i.                              \tag{9.7}
\]
Thus on the sampled quotient itself
\[
 R_2A(i)=c_iS_2A(i),\qquad
 0<c_i={3R_i\over2\mu_i}\le3\ell_{\max}.            \tag{9.8}
\]
This diagonal multiplier descends to the quotient because
\(S_2A=0\) implies \(R_2A=0\).  Hence, without a sampling-frame denominator,
\[
 \mathfrak D_2\le3\ell_{\max}\le {3\Lambda^2\over2}h^2={75\over2}h^2. \tag{9.9}
\]
Every active edge has chord length at least \(h/8\): the worst case is the
fine transition jump one; the adaptive lower jump, first-ring jumps,
transition radial edges, and equator jump two have larger fixed margins.
Since \(\sum_j\gamma_{ij}\ell_{ij}=2\mu_i\),
\[
 r_i={2\sum_j\gamma_{ij}\over\sum_j\gamma_{ij}\ell_{ij}}
 \le {2\over\ell_{\min}}\le64\pi^2h^{-2}.             \tag{9.10}
\]
Thus take \(R_3=64\pi^2\).  The accepted P1B lower bound yields the matching
order statement
\[
 {3\over32\pi^2}h^2
 \le\inf_{L\in\mathcal G_h(R_3)}\mathfrak D_2(L)
 \le {75\over2}h^2.                                  \tag{9.11}
\]
Its hypotheses are all explicit here: the node vectors are unit, (7.8)
gives positive shared conductances, (9.3) gives positive normalized weights,
(9.6) gives the exact coordinate eigenmap, and (9.10) is the required rate
cap.  Thus no mesh regularity or sampling injectivity assumption is being
silently imported into the P1B application.

## 10. Support-preserving robustness and certification manifest

There is a nontrivial but deliberately narrow robustness class.  Let
\[
 K_*=2^{28\cdot2^{10^6}}.
\]
At one level, perturb every northern ring latitude by at most \(h^3/K_*\),
fix the pole and equator, and reflect the perturbation in the south.  Keep
every count, longitude phase, radial mask, and horizontal jump integer fixed;
also allow one common ambient rotation.  All gaps then remain in
\([gh/2,2h]\).

Starting with the pole conductance, solve the full three even equations at
each ordinary row for its outgoing radial and two horizontal conductances,
and solve the full transition block (3.5) at a count change.  At an
unperturbed ordinary row the determinant of the columns
\((U_+,H_u,H_v)\) factors exactly as
\[
 4\sin h\,cs^3uv(u-v)
 \{2s^2-(1+c^2)(1-\cos h)-\sin h\,cs\}.              \tag{10.1}
\]
The last brace is the positive factor in (8.3a), while \(u\ne v\) by
(8.3), so the row inverse is uniform after the natural
\((h,h^3,h^2)\) normalization.

A cancellation-free straight-line differentiation bound with at most
\(10^6\) operations gives derivative bound \(K_*\): if \(W_k\ge1\) bounds
values and first derivatives through operation \(k\), the guarded addition,
multiplication, and reciprocal rules all obey
\(W_{k+1}\le2^{12}W_k^2\).  From \(W_0\le2^{16}\), induction gives
\(W_k\le2^{28\cdot2^k}\).  The denominator guards in Section 6 and
Taylor divided-difference atoms through order four remove every artificial
power of \(r\), \(s\), or \(1-c\).  The stated latitude
perturbation therefore changes each normalized ordinary row by \(O(h^2)\)
and each normalized transition row by \(O(h)\).  Across \(O(h^{-1})\)
ordinary rows the logarithmic recurrence changes by \(O(h)\); across the
\(J\) transitions it changes by \(O(Jh)\), and
\(Jh<14/M_0\).  The first row uses its certified inverse, and reflection
keeps the equator exact after re-solving (8.8).  Hence all conductances retain
positive margins, the global product changes by less than a fixed factor,
and exact \(H_0,H_1\) plus the \(O(h^2)\) quotient bound persist.

This theorem does not cover independent longitude perturbations or arbitrary
node motion; those destroy the reflection reduction and require a global
six-moment right inverse.

The certification suite consists of the following literal checks:

1. `p1e_short_gap_symbolic_matrix_audit.py` constructs (4.5) and derives
   (5.1)--(5.2) exactly;
2. `p1e_short_gap_cauchy_guard_audit.py` proves the continuous all-orders
   entry bounds (6.2b) using rational majorants;
3. `p1e_short_gap_polar_guard_audit.py` constructs and encloses the literal
   finite-\(h\) first-row matrix;
4. `p1e_short_gap_family_audit.py` returns nodes, undirected conductances,
   masses, and weights, and checks pole, first ring, ordinary cap/bands, both
   transition endpoints, equator, mesh/rate/window/quotient constants, and
   deterministic failed mutations;
5. `p1e_short_gap_proof_audit.py` checks the exact phase cone, recurrence,
   constants, and Neumann arithmetic.
6. `p1e_no_guard_ring_independent_audit.py` independently checks the
   reachable \(R>19/10\) repair, actual floor/ceiling conductance margins,
   both determinant factorizations, and perturbation arithmetic.

All six checks pass.  `p1e_short_gap_referee_audit.py` retains the rejected
old-formula and old-cap mutations so that those failures cannot silently
re-enter the theorem source.
