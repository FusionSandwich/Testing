# P1D — quantitative stability at the sharp quadratic frontier

## 1. Standing hypotheses and notation

Let `I` be finite and nonempty, let `d>=2`, and let

\[
 w_i>0,\qquad \sum_iw_i=1,\qquad \Omega_i\in S^{d-1}.
\]

Let

\[
 (Lf)_i=\sum_{j\ne i}a_{ij}(f_j-f_i),\qquad
 a_{ij}=\frac{\gamma_{ij}}{w_i},\qquad
 \gamma_{ij}=\gamma_{ji}\ge0,
\]

and assume the coordinate eigenmap equation

\[
 L\Omega=-(d-1)\Omega.                                      \tag{1.1}
\]

All sample, residual, loss, covariance, and quotient objects have the frozen
P1A--P1C meanings. In particular,

\[
 r_i=\sum_ja_{ij},\quad r_{\max}=\max_i r_i,\quad
 \ell_{ij}=1-\Omega_i\cdot\Omega_j,
\]

\[
 \epsilon_i=\sum_ja_{ij}\ell_{ij}^2,\qquad
 V_i=\sum_ja_{ij}\left(\ell_{ij}-\frac{d-1}{r_i}\right)^2,
                                                               \tag{1.2}
\]

\[
 M_i=\frac d{d-1}\epsilon_iZ_i+B_i,\qquad
 \|Z_i\|_F^2=\frac{d-1}{d},\qquad B_i\perp_F Z_i,             \tag{1.3}
\]

and

\[
 \mathfrak D_2
 =\sup_{A\notin K_X}\frac{\|R_2A\|_w}{\|S_2A\|_w},
 \qquad K_X=\ker S_2\subseteq\ker R_2.                        \tag{1.4}
\]

Assume

\[
 \boxed{\mathfrak D_2r_{\max}
 \le d(d-1)(1+\delta)},\qquad \delta\ge0.                    \tag{1.5}
\]

Write

\[
 n=d-1,\qquad
 a_0=\frac{n^2}{r_{\max}},\qquad
 \ell_0=\frac n{r_{\max}},\qquad
 c_0=\frac{da_0}{n}=\frac{dn}{r_{\max}},                     \tag{1.6}
\]

\[
 \eta=(1+\delta)^2-1=2\delta+\delta^2,
 \qquad x_i=\frac{\epsilon_i}{a_0}.                          \tag{1.7}
\]

No connectedness, sampling injectivity, regular degree, equal mass, or
transitivity is assumed in the universal theorem.

## 2. The sharp master stability budget

Define three nonnegative local defects

\[
 s_i=\frac{r_{\max}}{r_i}-1,\qquad
 v_i=\frac{V_i}{a_0},\qquad q_i=x_i-1.                        \tag{2.1}
\]

The P1A variance identity

\[
 \epsilon_i=\frac{n^2}{r_i}+V_i
\]

gives the exact decomposition

\[
 \boxed{x_i=\frac{r_{\max}}{r_i}+\frac{V_i}{a_0}},\qquad
 \boxed{q_i=s_i+v_i\ge0}.                                    \tag{2.2}
\]

P1B proves

\[
 \mathfrak D_2^2\ge
 \frac{d^2}{n^2}\sum_iw_i\epsilon_i^2
 +\frac dn\sum_iw_i\|B_i\|_F^2.                             \tag{2.3}
\]

Divide (2.3) and (1.5) by `c_0^2=d^2a_0^2/n^2`. This gives

\[
 \sum_iw_ix_i^2+
 \frac{n}{da_0^2}\sum_iw_i\|B_i\|_F^2
 \le(1+\delta)^2.                                            \tag{2.4}
\]

Since the masses sum to one and `x_i=1+q_i`, (2.4) is precisely

\[
 \boxed{
 \sum_iw_i(2q_i+q_i^2)
 +\frac{n}{da_0^2}\sum_iw_i\|B_i\|_F^2
 \le\eta.}                                                   \tag{2.5}
\]

This is the master theorem. It is stronger than the requested three
estimates and retains the competition between scalar and tensor defects.
It also proves that `delta=0` forces every P1C equality condition.

It is sometimes useful to retain the tensor-corrected scalar allowance

\[
 H:=\eta-\frac{n}{da_0^2}\sum_iw_i\|B_i\|_F^2,
 \qquad 0\le H\le\eta.                                      \tag{2.6}
\]

Then

\[
 \sum_iw_i(2q_i+q_i^2)\le H.                                \tag{2.7}
\]

## 3. Requested global estimates and loss variance

Because `0<=s_i,v_i<=q_i`, (2.5) immediately yields

\[
 \boxed{\sum_iw_i(x_i-1)^2\le\eta=2\delta+\delta^2},          \tag{3.1}
\]

\[
 \boxed{\sum_iw_i\left(\frac{r_{\max}}{r_i}-1\right)^2
 \le\eta},                                                   \tag{3.2}
\]

and

\[
 \boxed{
 \sum_iw_i\|B_i\|_F^2
 \le\frac d n a_0^2\eta
 =\frac{d(d-1)^3}{r_{\max}^2}(2\delta+\delta^2).}             \tag{3.3}
\]

Thus every constant displayed in the prompt is valid exactly as written.

Weighted Cauchy--Schwarz applied to (2.4) gives

\[
 \sum_iw_ix_i\le\left(\sum_iw_ix_i^2\right)^{1/2}
 \le1+\delta.
\]

Hence

\[
 \boxed{\sum_iw_iq_i\le\delta},\qquad
 \boxed{\sum_iw_is_i\le\delta},\qquad
 \boxed{\sum_iw_iv_i\le\delta}.                            \tag{3.4}
\]

Restoring dimensions gives the explicit loss-variance bounds

\[
 \boxed{\sum_iw_iV_i\le a_0\delta
 =\frac{(d-1)^2}{r_{\max}}\delta},                            \tag{3.5}
\]

\[
 \boxed{\sum_iw_iV_i^2\le a_0^2\eta},                       \tag{3.6}
\]

and, directly from `v_i<=q_i`,

\[
 \boxed{\sum_iw_i\left(\frac{2V_i}{a_0}
 +\frac{V_i^2}{a_0^2}\right)\le\eta}.                       \tag{3.7}
\]

One may replace the right side of (3.5) by
`a_0 min(delta,H/2)` and the right sides of (3.6)--(3.7) by
`a_0^2H` and `H`, respectively.

## 4. Pointwise and exceptional-vertex bounds

Retaining one nonnegative summand in (2.7) gives the exact envelope

\[
 q_i\le Q_i:=\sqrt{1+\frac H{w_i}}-1.                         \tag{4.1}
\]

Consequently

\[
 0\le s_i,v_i\le Q_i,\qquad
 r_i\ge\frac{r_{\max}}{1+Q_i},\qquad V_i\le a_0Q_i,          \tag{4.2}
\]

\[
 0\le1-\frac{r_i}{r_{\max}}
 \le1-\left(1+\frac H{w_i}\right)^{-1/2},                   \tag{4.3}
\]

and the joint pointwise tensor budget is

\[
 \boxed{
 \frac{n}{da_0^2}\|B_i\|_F^2
 \le\frac \eta{w_i}-2q_i-q_i^2.}                            \tag{4.4}
\]

In particular,

\[
 \|B_i\|_F\le a_0\sqrt{\frac{d\eta}{nw_i}}.                \tag{4.5}
\]

If `w_i>=w_min>0`, every bound above holds uniformly after replacing
`w_i` by `w_min`. The `w_min^{-1/2}` dependence is not hidden.

For `rho>0`, (2.7) gives the sharp weighted exceptional-set estimate

\[
 \boxed{
 \sum_{\{i:s_i\ge\rho\}}w_i
 \le\min\left\{1,\frac{H}{\rho(2+\rho)}\right\}.}            \tag{4.6}
\]

The same formula holds with `s_i` replaced by `v_i` or `q_i`. For the
ordinary relative rate loss `theta_i=1-r_i/r_max` and `0<theta<1`,

\[
 \boxed{
 \sum_{\{i:\theta_i\ge\theta\}}w_i
 \le\min\left\{1,
 \frac{H(1-\theta)^2}{\theta(2-\theta)}\right\}.}             \tag{4.7}
\]

If `N=|I|` and `w_i>=w_min`, then

\[
 \frac{\#\{i:s_i\ge\rho\}}N
 \le\min\left\{1,
 \frac{H}{Nw_{\min}\rho(2+\rho)}\right\}.                  \tag{4.8}
\]

No unweighted vertex-fraction theorem is possible without a mass floor.

## 5. Radial--tangent covariance, anisotropy, and local spectra

Use the P1C split, at `u_i=Omega_i`,

\[
 \tau_{ij}=P_i\Omega_j,\qquad
 h_i=\sum_ja_{ij}\ell_{ij}\tau_{ij},\qquad
 T_i=\sum_ja_{ij}\tau_{ij}\tau_{ij}^T,                      \tag{5.1}
\]

and put

\[
 A_i=T_i-\left(2-\frac{\epsilon_i}{n}\right)P_i.             \tag{5.2}
\]

Then `A_i` is tangent and trace-free, and P1C gives the orthogonal identity

\[
 \boxed{\|B_i\|_F^2=2\|h_i\|^2+\|A_i\|_F^2}.               \tag{5.3}
\]

Thus

\[
 \sum_iw_i\|h_i\|^2\le\frac{da_0^2}{2n}\eta,
 \qquad
 \sum_iw_i\|A_i\|_F^2\le\frac{da_0^2}{n}\eta.             \tag{5.4}
\]

The probability radial--tangent covariance is `h_i/r_i`. Since

\[
 \frac{h_i}{r_i}
 =\sum_jp_{ij}\left(\ell_{ij}-\frac n{r_i}\right)\tau_{ij},
\]

Cauchy--Schwarz and `||tau_ij||<=1` give

\[
 \left\|\frac{h_i}{r_i}\right\|^2\le\frac{V_i}{r_i}.        \tag{5.5}
\]

Using `2v_i(1+s_i)<=2q_i+q_i^2` in (2.5),

\[
 \boxed{
 \sum_iw_i\left\|\frac{h_i}{r_i}\right\|^2
 \le\frac{\ell_0^2\eta}{2}},\qquad
 \left\|\frac{h_i}{r_i}\right\|
 \le\ell_0\sqrt{\frac{\eta}{2w_i}}.                        \tag{5.6}
\]

Let `alpha_0=2-ell_0`. Trace orthogonality yields

\[
 \left\|T_i-\alpha_0P_i\right\|_F^2
 =\|A_i\|_F^2+\frac{(\epsilon_i-a_0)^2}{n}.                 \tag{5.7}
\]

Combining the two terms before discarding the master budget gives

\[
 \boxed{
 \sum_iw_i\|T_i-\alpha_0P_i\|_F^2\le K_0},\qquad
 K_0:=\frac{da_0^2}{n}\eta
 =\frac{d(d-1)^3}{r_{\max}^2}\eta.                          \tag{5.8}
\]

If `theta_i1,...,theta_in` are the tangent eigenvalues of `T_i`, then

\[
 \sum_iw_i\sum_{k=1}^n(\theta_{ik}-\alpha_0)^2\le K_0,       \tag{5.9}
\]

and

\[
 \sum_iw_i(\max_k\theta_{ik}-\min_k\theta_{ik})^2\le2K_0.  \tag{5.10}
\]

For the full increment covariance, define

\[
 C_i^*=a_0u_iu_i^T+\alpha_0P_i.                              \tag{5.11}
\]

The exact row decomposition is

\[
 C_i-C_i^*=M_i-c_0Z_i
 =\frac d n(\epsilon_i-a_0)Z_i+B_i,                          \tag{5.12}
\]

with orthogonal summands, so

\[
 \boxed{
 \|C_i-C_i^*\|_F^2
 =\frac d n(\epsilon_i-a_0)^2+\|B_i\|_F^2},\qquad
 \sum_iw_i\|C_i-C_i^*\|_F^2\le K_0.}                       \tag{5.13}
\]

Hoffman--Wielandt therefore controls, with the same `K_0`, the weighted
squared splitting of the spectrum of `C_i` from

\[
 \{a_0,\alpha_0,\ldots,\alpha_0\}.                           \tag{5.14}
\]

This is a local shell-eigenvalue statement. A radial-eigenvector conclusion
for `C_i` additionally costs the gap `|c_0-2|`; it is unavailable at the
isotropic hypercube value `c_0=2`.

## 6. Active conductance mass and edge defects

Let

\[
 p_{ij}=\frac{a_{ij}}{r_i},\qquad
 \bar r=\sum_iw_ir_i,\qquad
 \pi_i=\frac{w_ir_i}{\bar r},\qquad
 \nu_{ij}=\pi_ip_{ij}=\frac{\gamma_{ij}}{\bar r}.             \tag{6.1}
\]

Then `pi` is stationary for the reversible Markov kernel `p`, and `nu` is
a symmetric directed probability measure. Equivalently, the undirected
conductance total is `bar r/2`; fractions of undirected conductance are the
same as symmetric directed fractions.

Put

\[
 R_i=\frac{r_{\max}}{r_i}=1+s_i,\qquad
 m_i=\frac n{r_i}=\ell_0R_i.                                 \tag{6.2}
\]

Since `R_i<=x_i`, Cauchy--Schwarz gives

\[
 \frac{\bar r}{r_{\max}}=\sum_i\frac{w_i}{R_i}
 \ge\frac1{\sqrt{\sum_iw_iR_i^2}}
 \ge\frac1{\sqrt{1+H}}.                                     \tag{6.3}
\]

### Global equality-shell loss

The orientation-independent defect

\[
 g_{ij}=\frac{\ell_{ij}}{\ell_0}-1                            \tag{6.4}
\]

satisfies the exact identity

\[
 \mathbb E_\nu g^2
 =\frac{\sum_iw_i\left((R_i-1)^2/R_i+v_i\right)}
        {\sum_iw_i/R_i}.                                     \tag{6.5}
\]

For `R>=1`, `v>=0`,

\[
 \frac{(R-1)^2}{R}+v
 \le\frac{(R+v)^2-1}{2}.                                    \tag{6.6}
\]

Equations (2.7), (6.3), and (6.6) imply

\[
 \boxed{
 \mathbb E_\nu\left(\frac{\ell_{ij}}{\ell_0}-1\right)^2
 \le\frac{\sqrt{1+H}\,H}{2}.}                              \tag{6.7}
\]

Thus, for every `t>0`, the fraction of active conductance mass with a
prescribed relative loss defect is

\[
 \boxed{
 \nu\left\{\left|\frac{\ell_{ij}}{\ell_0}-1\right|\ge t\right\}
 \le\min\left\{1,\frac{\sqrt{1+H}\,H}{2t^2}\right\}.}       \tag{6.8}
\]

For an absolute threshold `beta>0`, this becomes

\[
 \boxed{
 \nu\{|\ell_{ij}-\ell_0|\ge\beta\}
 \le\min\left\{1,
 \frac{\sqrt{1+H}\,H(d-1)^2}
 {2r_{\max}^2\beta^2}\right\}.}                             \tag{6.9}
\]

The local-row version, requiring no replacement of `H` by a symmetric-shell
quantity, is

\[
 \mathbb E_\nu
 \left[\left(\frac{\ell_{ij}-m_i}{\ell_0}\right)^2\right]
 \le\delta(1+\delta),                                       \tag{6.10}
\]

where the slightly different right side follows from (3.5) and
`bar r>=r_max/(1+delta)`. Neither estimate hides the conductance
normalization.

### A directed probability floor

Suppose every active directed edge has

\[
 p_{ij}\ge\kappa>0.                                         \tag{6.11}
\]

For

\[
 z_{ij}=\frac{\ell_{ij}}{m_i}-1,
\]

one has exactly

\[
 \sum_jp_{ij}z_{ij}^2=\frac{v_i}{R_i}.                       \tag{6.12}
\]

Therefore every active edge obeys

\[
 \boxed{|z_{ij}|\le
 \sqrt{\frac{v_i}{\kappa R_i}}
 \le\sqrt{\frac{Q_i}{\kappa}}.}                            \tag{6.13}
\]

Equivalently,

\[
 \boxed{
 \left|\ell_{ij}-\frac n{r_i}\right|
 \le\ell_0\sqrt{\frac{\eta}{2\kappa w_i}}
 \le\ell_0\sqrt{\frac{\eta}{2\kappa w_{\min}}}.}         \tag{6.14}
\]

The second form uses the joint local budget, not a concealed minimum edge
weight. The global loss has the exact row identity

\[
 \sum_jp_{ij}g_{ij}^2=(R_i-1)^2+R_iv_i.                      \tag{6.15}
\]

Let `X_i=sqrt(1+H/w_i)` and define

\[
 \Phi(X)=\begin{cases}X-1,&1\le X\le2,\\
                       (X-1)^2,&X\ge2.
        \end{cases}                                          \tag{6.16}
\]

Maximizing the right side of (6.15) under `R+v<=X` gives

\[
 \boxed{
 \left|\frac{\ell_{ij}}{\ell_0}-1\right|
 \le\sqrt{\frac{\Phi(X_i)}\kappa}
 \le\sqrt{\frac{\Phi(X_*)}\kappa}},\qquad
 X_*=\sqrt{1+H/w_{\min}}.                                   \tag{6.17}
\]

The graph degree is at most `floor(1/kappa)`. The powers of `kappa` in
(6.13)--(6.17) are unavoidable.

## 7. Path propagation, resistance, and spectral gap

The path statements apply within an active connected component. Assertions
using a finite graph diameter or a positive Poincare gap additionally assume
that the active support under discussion is connected. Unless a displayed
formula says otherwise, this section continues the hypotheses
`w_i>=w_min>0` and `p_ij>=kappa>0` from Sections 4 and 6.

On a shared active edge, the two orientations have the same loss, hence

\[
 \frac{r_i}{r_j}=\frac{1+z_{ij}}{1+z_{ji}}.                  \tag{7.1}
\]

Let

\[
 \theta_i=\sqrt{\frac{v_i}{\kappa R_i}},\qquad
 \theta_*=\sqrt{\frac{X_*-1}{\kappa}}.                       \tag{7.2}
\]

If `theta_*<1`, equivalently

\[
 H<w_{\min}(2\kappa+\kappa^2),                              \tag{7.3}
\]

then

\[
 \frac{1-\theta_i}{1+\theta_j}
 \le\frac{r_i}{r_j}
 \le\frac{1+\theta_i}{1-\theta_j}.                          \tag{7.4}
\]

Multiplying the literal nonuniform factors gives the exact path theorem. In
uniform form, with `Q_theta=(1+theta_*)/(1-theta_*)`, a path of length `L`
satisfies

\[
 Q_\theta^{-L}\le\frac{r_u}{r_v}\le Q_\theta^L.              \tag{7.5}
\]

The corresponding loss range over two active edges is at most
`Q_theta^(D+1)` on a graph of diameter `D`.

A complementary additive estimate, valid without (7.3), is

\[
 \boxed{
 \left|\frac n{r_u}-\frac n{r_v}\right|
 \le\ell_0\sqrt{\frac{2L\eta}{\kappa w_{\min}}}.}            \tag{7.6}
\]

It follows by writing the difference across each shared edge as the sum of
its two oriented loss residuals and applying Cauchy--Schwarz along the path.
This exposes the sharp square-root dependence on path length for an `L^2`
edge budget.

For expansion estimates define

\[
 \mathcal E_\nu(f)=\frac12\sum_{i,j}\nu_{ij}(f_i-f_j)^2,
 \qquad
 \lambda_P=\inf_{\operatorname{Var}_\pi f>0}
 \frac{\mathcal E_\nu(f)}{\operatorname{Var}_\pi f}.         \tag{7.7}
\]

For (7.10)--(7.11) assume explicitly that `lambda_P>0`. In
(7.12), the pair lies in one connected component, equivalently it has finite
effective resistance.

Put `u_ij=(ell_ij-m_i)/ell_0`. The shared loss gives

\[
 R_i-R_j=u_{ji}-u_{ij}.                                     \tag{7.8}
\]

Consequently

\[
 \mathcal E_\nu(R),\ \mathcal E_\nu(\log r)
 \le\sqrt{1+H}\,H,                                         \tag{7.9}
\]

and

\[
 \boxed{
 \operatorname{Var}_\pi(R),\ \operatorname{Var}_\pi(\log r)
 \le\frac{\sqrt{1+H}\,H}{\lambda_P}.}                     \tag{7.10}
\]

Since `pi_i>=w_min/X_*`,

\[
 \boxed{
 |\log(r_i/r_j)|
 \le2\sqrt{\frac{\sqrt{1+H}\,H X_*}
 {\lambda_Pw_{\min}}}.}                                     \tag{7.11}
\]

In the same energy convention, effective resistance gives

\[
 |\log(r_i/r_j)|
 \le\sqrt{R_{\rm eff}(i,j)\sqrt{1+H}\,H}.                  \tag{7.12}
\]

Under (6.11), every active conductance satisfies

\[
 \nu_{ij}\ge\frac{\kappa w_{\min}}{X_*}.                    \tag{7.13}
\]

Thus a path of length `L` gives

\[
 R_{\rm eff}(i,j)\le\frac{LX_*}{\kappa w_{\min}}.           \tag{7.14}
\]

Every dependence on `kappa`, diameter/effective resistance, gap, and mass is
visible. If a routed canonical-path family is used, (7.14) is replaced by
its explicit maximum edge congestion; no overlap factor may be suppressed.
Notice also the diameter-free global rate bound

\[
 \frac{r_{\max}}{r_{\min}}\le X_*.                           \tag{7.15}
\]

Path dependence is necessary when propagating only local edge information,
not when the stronger global `w_min` budget (7.15) is already used.

## 8. Deviation from scalar action and sampled-shell splitting

The row representer of `R_2-c_0S_2` at vertex `i` is `M_i-c_0Z_i`.
Equation (1.3) gives the exact orthogonal identity

\[
 \|M_i-c_0Z_i\|_F^2
 =\frac d n(\epsilon_i-a_0)^2+\|B_i\|_F^2.                  \tag{8.1}
\]

Therefore

\[
 \boxed{
 \|R_2-c_0S_2\|_{HS(F\to w)}^2
 =\sum_iw_i\|M_i-c_0Z_i\|_F^2
 \le K_0.}                                                   \tag{8.2}
\]

This already includes leakage outside `im S_2`.

Let

\[
 W_X=K_X^{\perp_F},\qquad
 \alpha_X=inf_{\substack{A\in W_X\\\|A\|_F=1}}
 \|S_2A\|_w^2>0.                                            \tag{8.3}
\]

The positivity is finite-dimensional and is imposed only on the genuinely
sampled quotient. If `E=im S_2` and `U:E->l^2(w)` is the quotient-correct
map `U(S_2A)=R_2A`, then

\[
 \boxed{
 \|U-c_0\iota_E\|_{op}\le
 \rho_X:=\sqrt{\frac{K_0}{\alpha_X}}.}                      \tag{8.4}
\]

No `alpha_X`-independent estimate that tends to zero with the
Hilbert--Schmidt row defect follows from row control alone.  The underlying
Hilbert--Schmidt-to-quotient transfer has the sharp factor
`alpha_X^(-1/2)`.  Sampling kernels are removed by the quotient, not assumed
away.

Because `U=(L+2dI)|_E`, put

\[
 \mu_0=2d-c_0=d(2-\ell_0).                                  \tag{8.5}
\]

Then every `f in E` satisfies

\[
 \boxed{\|(L+\mu_0I)f\|_w\le\rho_X\|f\|_w.}                 \tag{8.6}
\]

If `P_E` is the orthogonal projection onto `E`, then

\[
 \|(I-P_E)L|_E\|\le\rho_X,                                  \tag{8.7}
\]

\[
 \operatorname{spec}(-P_EL|_E)
 \subset[\mu_0-\rho_X,\mu_0+\rho_X],                        \tag{8.8}
\]

and the compressed shell splitting is at most `2rho_X`. The spectral
theorem also gives, for `t>0`,

\[
 \left\|\mathbf1_{\{|(-L)-\mu_0|\ge t\}}f\right\|_w
 \le\frac{\rho_X}{t}\|f\|_w.                               \tag{8.9}
\]

These statements do not assume that `im S_2` is invariant.

## 9. Constructive local geometric stability

The averaged tensor theorem does not by itself control a normalized vertex
figure near an antipodal or rank-deficient shell. The following theorem
states exactly the needed nondegeneracy and constructs the nearby tight
frame; it invokes no global embedding-stability result.

Fix a vertex and suppress its index. Let

\[
 u=\Omega_i,\quad P=I-uu^T,\quad r=r_i,\quad
 p_j=a_{ij}/r,\quad m=n/r,                                  \tag{9.1}
\]

\[
 \tau_j=P\Omega_j,\quad T=\sum_ja_{ij}\tau_j\tau_j^T,
 \quad V=V_i,\quad b=\|B_i\|_F.                             \tag{9.2}
\]

Let

\[
 A=T-\frac{\operatorname{tr}T}{n}P
  =T-\left(2-\frac{\epsilon_i}{n}\right)P.                   \tag{9.3}
\]

Then `tr A=0`, `||A||<=b`, and

\[
 \boxed{
 \left\|\frac Tr-\frac{m(2-m)}nP\right\|_F^2
 =\frac{\|A\|_F^2+V^2/n}{r^2}
 \le\frac{b^2+V^2/n}{r^2}.}                                \tag{9.4}
\]

### Raw-frame whitening

Assume

\[
 0<m<2,\qquad G:=T/r\succeq\lambda P,\qquad\lambda>0,        \tag{9.5}
\]

and put `theta=m(2-m)/n`. Define on the tangent space

\[
 W=\sqrt\theta\,G^{-1/2},\qquad \widehat\tau_j=W\tau_j.      \tag{9.6}
\]

Then, exactly,

\[
 \sum_jp_j\widehat\tau_j=0,
 \qquad
 \sum_jp_j\widehat\tau_j\widehat\tau_j^T=\theta P.         \tag{9.7}
\]

Thus the target is a centered weighted tight frame. For the fixed-weight
Procrustes metric modulo tangent rotations,

\[
 d_{p,O}(\tau,z)^2
 =\inf_{Q\in O(T_uS^{d-1})}\sum_jp_j\|\tau_j-Qz_j\|^2,      \tag{9.8}
\]

spectral calculus gives the explicit estimate

\[
 \boxed{
 d_{p,O}(\tau,\widehat\tau)^2
 \le\frac{b^2+V^2/n}
 {r^2(\sqrt\lambda+\sqrt\theta)^2}.}                        \tag{9.9}
\]

Indeed, if `g_k` are the eigenvalues of `G`, the correction energy is
`sum_k(sqrt(g_k)-sqrt(theta))^2`. Also

\[
 \|W-I\|_{op}\le
 \frac{\sqrt{b^2+V^2/n}}
 {r\sqrt\lambda(\sqrt\lambda+\sqrt\theta)}.                \tag{9.10}
\]

This proves quantitatively how the tangent lower frame bound enters.

### Normalized tangent figures

There is a particularly transparent normalization by the mean shell. Put

\[
 \sigma_0^2=m(2-m),\qquad y_j=\tau_j/\sigma_0,
 \qquad F=\sum_jp_jy_jy_j^T.                                \tag{9.11}
\]

Then `sum p y=0` and

\[
 \boxed{
 \left\|F-\frac1nP\right\|_F^2
 =\frac{\|A\|_F^2+V^2/n}{n^2(2-m)^2}.}                     \tag{9.12}
\]

The vectors `y_j` need not be unit, but loss variance controls exactly that
defect:

\[
 \boxed{
 \sum_jp_j(\|y_j\|^2-1)^2
 \le\frac{4V}{nm(2-m)^2}.}                                 \tag{9.13}
\]

If `F>=lambda P`, define

\[
 z_j=\frac1{\sqrt n}F^{-1/2}y_j.                             \tag{9.14}
\]

Then `(p_j,z_j)` is an exact centered probability-weighted tight frame,

\[
 \sum_jp_jz_j=0,qquad \sum_jp_jz_jz_j^T=P/n,               \tag{9.15}
\]

and

\[
 \boxed{
 d_{p,O}(y,z)^2\le
 \frac{\|F-P/n\|_F^2}{(\sqrt\lambda+1/\sqrt n)^2}.}         \tag{9.16}
\]

Moreover

\[
 \sum_jp_j(\|z_j\|-1)^2
 \le2d_{p,O}(y,z)^2+
 \frac{8V}{nm(2-m)^2}.                                     \tag{9.17}
\]

Under the uniform hypotheses

\[
 m\ge m_->0,\qquad 2-m\ge\chi>0,\qquad F\succeq\lambda P,  \tag{9.18}
\]

the master theorem gives

\[
 \sum_iw_i\|F_i-P_i/n\|_F^2
 \le\frac{da_0^2\eta}{n^3\chi^2},                          \tag{9.19}
\]

\[
 \sum_iw_id_{p_i,O}(y_i,z_i)^2
 \le\frac{da_0^2\eta}
 {n^3\chi^2(\sqrt\lambda+1/\sqrt n)^2},                    \tag{9.20}
\]

\[
 \sum_iw_i\sum_jp_{ij}(\|y_{ij}\|^2-1)^2
 \le\frac{4a_0\delta}{nm_-\chi^2}.                         \tag{9.21}
\]

These are weighted, rotation-quotiented, and fully explicit.

## 10. Exact unit-frame and spherical-figure repair

Whitening produces an exact tight frame but can alter individual norms. To
obtain a nearby exact *unit-norm* weighted frame, impose a quantified feature
overlap. This is the additional hypothesis that a global classification or
gluing argument would otherwise conceal.

Assume every active edge has

\[
 s_j:=\sqrt{\ell_j(2-\ell_j)}\ge s_->0,                      \tag{10.1}
\]

and define its unit tangent direction `y_j=tau_j/s_j`. Put

\[
 s_0=\sqrt{m(2-m)},\quad
 \sigma=\sqrt{V/r},\quad
 e=\frac{\sqrt{b^2+V^2/n}}r,                                \tag{10.2}
\]

\[
 c=\sum_jp_jy_j,\qquad F=\sum_jp_jy_jy_j^T.                 \tag{10.3}
\]

Directly from `sum p s_jy_j=0` and (9.4),

\[
 \boxed{\|c\|\le c_*:=
 \frac{2\sigma}{s_0(s_-+s_0)}},                             \tag{10.4}
\]

\[
 \boxed{\|F-P/n\|_F\le f_*:=\frac{2\sigma+e}{s_0^2}.}      \tag{10.5}
\]

Let `J` be the active neighbor labels and

\[
 H_0=\{t\in\mathbb R^J:\sum_jt_j=0\}.                       \tag{10.6}
\]

On `T_uS^{d-1} direct_sum Sym_0(T_uS^{d-1})`, define the
rotation-equivariant feature operator

\[
 \mathcal A_0t
 =\sum_jt_j\left(y_j,\ y_jy_j^T-P/n\right).                 \tag{10.7}
\]

Assume it is surjective with

\[
 \sigma_{\min}(\mathcal A_0)\ge\mu>0,\qquad
 p_j\ge\kappa>0.                                            \tag{10.8}
\]

This forces the explicit degree condition

\[
 |J|\ge n(n+3)/2.                                           \tag{10.9}
\]

Let `R_*=sqrt(c_*^2+f_*^2)`. If

\[
 R_*<\kappa\mu,                                             \tag{10.10}
\]

then the minimum-norm correction

\[
 t=-\mathcal A_0^*(\mathcal A_0\mathcal A_0^*)^{-1}
       (c,F-P/n),\qquad \widehat p=p+t                       \tag{10.11}
\]

satisfies

\[
 \|\widehat p-p\|_2\le R_*/\mu,\qquad
 \widehat p_j\ge\kappa-R_*/\mu>0,                           \tag{10.12}
\]

and, exactly,

\[
 \sum_j\widehat p_j=1,\quad
 \sum_j\widehat p_jy_j=0,\quad
 \sum_j\widehat p_jy_jy_j^T=P/n.                            \tag{10.13}
\]

Thus the unchanged directions with corrected positive weights form a
centered weighted unit-norm tight frame.

More geometrically, define

\[
 \widehat\Omega_j=(1-m)u+s_0y_j,
 \qquad \widehat a_j=r\widehat p_j.                          \tag{10.14}
\]

Then every `hat Omega_j` is on the sphere, every target loss equals `m`,
the target row satisfies (1.1), and

\[
 \widehat V=0,\qquad \widehat B=0.                           \tag{10.15}
\]

Use the labeled geometric metric, modulo tangent rotations fixing `u`,

\[
 d_{\rm geo}^2=
 \inf_{Q\in O(d),\,Qu=u}\left[
 \|p-\widehat p\|_2^2+
 \sum_{j\in J}\|\Omega_j-Q\widehat\Omega_j\|^2\right].    \tag{10.16}
\]

Then

\[
 \boxed{
 d_{\rm geo}^2\le
 \left(\frac{R_*}{\mu}\right)^2+
 \frac{\sigma^2}{\kappa}
 \left(1+\frac4{(s_-+s_0)^2}\right).}                       \tag{10.17}
\]

Every dependence on the shell margin, minimum edge probability, tangent
overlap, active degree, and rotation quotient is explicit.

The shell floor can itself be derived. If

\[
 m\in[\zeta,2-\zeta],\qquad p_j\ge\kappa,\qquad
 \frac{V}{r\kappa}\le\frac{\zeta^2}{4},                     \tag{10.18}
\]

then

\[
 \ell_j\in[\zeta/2,2-\zeta/2],\qquad
 s_-\ge\sqrt{(\zeta/2)(2-\zeta/2)},\qquad
 s_0\ge\sqrt{\zeta(2-\zeta)}.                              \tag{10.19}
\]

## 11. Necessity and sharp scaling examples

Each extra parameter above has an explicit obstruction. These examples are
theorem controls, not numerical evidence for the theorem.

### 11.1 Small stationary masses

In `d=3`, take the disjoint union of a cube equality generator of total mass
`1-t` and an aligned tetrahedral equality generator of total mass `t`. The
tetrahedral vertices represent the four antipodal cube rays. The two
component rates and residual scalars are

\[
 (r,c)=(3,2),\qquad (3/2,4).                                 \tag{11.1}
\]

Their projective sampling Grams coincide, so

\[
 \mathfrak D_2=2\sqrt{1+3t},\qquad r_{\max}=3,
 \qquad \eta=3t.                                            \tag{11.2}
\]

The tetrahedral mass `t` has `s_i=1`, attaining (4.6) exactly at
`rho=1`, while `w_min=t/4` tends to zero. No pointwise or unweighted
fraction statement can omit `w_min`.

### 11.2 Small active probabilities

For `0<kappa<=1/3`, in `d=2`, use the four compass nodes
`+-e_1,+-e_2` with uniform masses. From
each node put transition probability `kappa` on the antipode and
`(1-kappa)/2` on each orthogonal node, with

\[
 r=\frac1{1+\kappa}.                                        \tag{11.3}
\]

Then `L Omega=-Omega` and

\[
 \mathfrak D_2=\frac{2(1+3\kappa)}{1+\kappa},\qquad
 \mathfrak D_2r=\frac{2(1+3\kappa)}{(1+\kappa)^2}.           \tag{11.4}
\]

The frontier defect tends to zero, but the antipodal edge has

\[
 z=\frac{1-\kappa}{1+\kappa}\longrightarrow1.               \tag{11.5}
\]

Here `w_min=1/4` is fixed and the bad conductance mass is exactly `kappa`.
This proves the necessity and square-root scaling of the probability floor.

### 11.3 Long paths and small spectral gaps

Fix integers `K>=3`, `m>=1` and a real `rho>1`.  On a cyclic `S^1` mesh,
take the cyclic positive sequence `c_i` consisting of `K` copies of `1`
followed by

\[
 \rho^{-1},\ldots,\rho^{-m},\rho^{-(m-1)},\ldots,\rho^{-1}.
\]

There is a unique `s>0` with

\[
 \sum_i2\arctan(sc_i)=2\pi;
\]

set `t_i=sc_i`. The `K` plateau terms imply
`s<=T:=tan(pi/K)`. With

\[
 a_{i,i+1}=\frac{1+t_i^2}{2t_i(t_{i-1}+t_i)},\qquad
 a_{i,i-1}=\frac{1+t_{i-1}^2}{2t_{i-1}(t_{i-1}+t_i)},        \tag{11.6}
\]

\[
 w_i\propto t_{i-1}+t_i,\qquad
 r_i=\frac{1+t_{i-1}t_i}{2t_{i-1}t_i},                       \tag{11.7}
\]

detailed balance and `L Omega=-Omega` hold exactly. The probability floor
stays bounded below while the rate range grows exponentially. More
precisely, if the plateau has length `K` and `T=tan(pi/K)`, then

\[
 p_{ij}\ge\frac1{(1+\rho)(1+T^2)},                           \tag{11.8}
\]

the forward normalized edge scale is exactly

\[
 \frac{\ell_{i,i+1}}{m_i}
 =\frac{t_i}{t_{i-1}}
  \frac{1+t_{i-1}t_i}{1+t_i^2},                              \tag{11.9}
\]

with the analogous backward formula. Every such normalized scale lies in

\[
 [\,1/(\rho(1+T^2)),\ \rho(1+T^2)\,],                       \tag{11.10}
\]

while

\[
 \frac{r_{\max}}{r_{\min}}
 \ge\frac{\rho^{2m-1}}{1+s^2}
 \ge\frac{\rho^{2m-1}}{1+T^2}.                              \tag{11.11}
\]

Choosing `rho,K` with `rho(1+T^2)<=1+epsilon` makes the local defect
arbitrarily small with a fixed positive probability floor while retaining
exponential path accumulation.

This cyclic ramp is a sharp example for the standalone local-edge
propagation lemma.  It is not asserted to be a sequence with the global
frontier slack `delta->0`: its exponentially large rate range forces global
scalar slack unless the low-rate portion is assigned vanishing stationary
mass.  This is consistent with the diameter-free global `w_min` estimate
(7.15).

Separately, the `N`-cycle has `kappa=1/2` and

\[
 \lambda_P=1-\cos(2\pi/N)\asymp N^{-2}.                      \tag{11.12}
\]

Its first Fourier mode attains the Poincare quotient. This certifies that a
gap, resistance, diameter, or explicit congestion parameter is necessary
for global propagation from local information.

### 11.4 Nearly singular tangent frames

Let `d=3`, `u=e_3`, `0<t<1`, `m=2-t`, and `r=2/(2-t)`. Use two indexed
copies of each neighbor

\[
 \Omega_\pm=(-1+t)e_3\pm\sqrt{t(2-t)}e_1,                    \tag{11.13}
\]

each at rate `r/4`. The local coordinate equation holds, every loss equals
`m`, and

\[
 V=0,\qquad \|B_i\|_F=\sqrt2\,t\longrightarrow0.             \tag{11.14}
\]

Nevertheless the normalized directions are two copies each of `+-e_1`, so

\[
 F=e_1e_1^T,\qquad \lambda_{\min}(F)=0,
 \qquad\|F-P/2\|_F=1/\sqrt2.                                \tag{11.15}
\]

Their fixed-weight Procrustes distance from every unit-norm tight frame is
at least `1/2`. At `t=0` the shell is antipodal and normalization ceases to
exist. Thus absolute smallness of `B_i,V_i` cannot replace shell and tangent
lower bounds.

### 11.5 Sampling kernels and a sharp sampling-gap transfer

The tetrahedral, octahedral, and cubical P1C examples have nonzero exact
sampling kernels; coefficient closeness on those aliases is meaningless.
For a quantitative sharp example in `d=2`, take uniform nodes

\[
 \{\pm u_0,\pm u_\varphi\},\qquad
 u_\theta=(\cos\theta,\sin\theta),                            \tag{11.16}
\]

and join only different antipodal rays: each node on the first ray is joined
to both nodes on the second ray, and conversely, at rate `a_ij=1/2`. Then
`r_max=1`, `L Omega=-Omega`, and the P1D comparison scalar is `c_0=2`. In a
Frobenius-orthonormal trace-free basis,

\[
 \alpha_X=\frac{\cos^2\varphi}{2},
 \qquad \pi/4<\varphi<\pi/2.                                \tag{11.17}
\]

On the ray-constant sampled space, `U=L+4I` has eigenvalues `4` on
constants and `2` on the contrast. Consequently

\[
 \|R_2-2S_2\|_{HS}^2=4\alpha_X,
 \qquad \|U-2\iota\|_{op}=2.                                \tag{11.18}
\]

Thus the underlying transfer
`||U-2iota||=||R_2-2S_2||_HS/sqrt(alpha_X)` is attained exactly.  This proves
sharpness of the `alpha_X^-1/2` Hilbert--Schmidt-to-quotient factor, not of
every preceding relaxation used to replace the row defect by `K_0`.  At
`varphi=pi/2`, the disappearing mode is an exact alias.

### 11.6 Tangent overlap and gluing

Take two regular simplex equality components, rotate the second by an
arbitrary tangent rotation fixing one anchor direction, and connect the two
anchor indices by a zero-loss edge of rate `b`. The coordinate equation and
quadratic residual are unchanged on that bridge, but

\[
 r_{\max}=\frac{d(d-1)}{d+1}+b,qquad
 \delta=\frac{b(d+1)}{d(d-1)}\longrightarrow0,               \tag{11.19}
\]

while the relative tangent rotation remains arbitrary. Connectivity alone
cannot replace the overlap parameter `mu` or a nonzero-loss/probability
floor.

## 12. Proof-route and prior-art boundary

The scalar theorem has three independent derivations: the P1B weighted Gram
trace inequality, the quotient Hilbert--Schmidt inequality, and isotropic
random trace-free-matrix averaging. The local geometry is proved by exact
radial--tangent block algebra and constructive polar whitening. The graph
consequences use only reversible conductance normalization, Markov/Chebyshev
bounds, path Cauchy--Schwarz, effective resistance, and the finite Poincare
inequality.

García Trillos--Gerlach--Hein--Slepčev study asymptotic random geometric
graph convergence under manifold and bandwidth hypotheses. Their spectral
framework is adjacent context, not a source of (2.5), (8.4), or any finite
constant here. Izmestiev--Lam treat a specialized geometric spherical
Laplacian. Association schemes and spherical designs organize symmetric
examples. No external theorem is transferred as the P1D stability result.

The exact regression program checks the algebraic fixtures and uses
outward interval arithmetic at extreme scales. It is an audit of constants,
not a substitute for the all-orders arguments above.
