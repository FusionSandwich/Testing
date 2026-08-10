# P1E polar-Piola route: exact identities and the sharp obstruction

This note records an independent construction route.  It is unconditional for
positivity, reversibility, and exact degree-one reproduction in every
dimension.  It also gives an exact local formula for the degree-two defect.
The formula shows why Delaunay positivity and quasiuniformity alone do not
imply the P1E `O(h^2)` conclusion.

Put `n=d-1`.  Let `p_i in S^(d-1)` positively span `R^d`, and suppose that

\[
 Q=\bigcap_i\{x\in\mathbb R^d:p_i\mathbin\cdot x\le1\}
\]

is a bounded polytope for which every displayed inequality is active.  Write
`F_i=Q cap {p_i dot x=1}`.  If `F_i` and `F_j` meet in a ridge, let `A_ij` be
its `(d-2)`-dimensional Euclidean measure.  Let

\[
 \theta_{ij}=\arccos(p_i\mathbin\cdot p_j),\qquad
 \ell_{ij}=1-\cos\theta_{ij},\qquad
 q_{ij}=\tan(\theta_{ij}/2),
\]

and

\[
 t_{ij}=\frac{p_j-\cos\theta_{ij}p_i}{\sin\theta_{ij}}
 \in T_{p_i}S^{d-1}.
\]

All ridge pairs below are assumed to have `0<theta_ij<pi`.

## 1. The discrete Piola identity

Translate the facet into its tangent space:

\[
 P_i=F_i-p_i\subset p_i^\perp.
\]

The inequality belonging to `p_j` becomes exactly

\[
 t_{ij}\mathbin\cdot y\le q_{ij}.                    \tag{1}
\]

Thus `t_ij` is the outward unit normal of the corresponding facet of `P_i`,
and that facet has area `A_ij`.  The Euclidean divergence theorem, first for a
constant vector field and then for the identity field, gives

\[
 \sum_jA_{ij}t_{ij}=0,
 \qquad
 \sum_jA_{ij}q_{ij}=n\,\operatorname{Vol}_n(P_i).    \tag{2}
\]

Set

\[
 \gamma_{ij}=\frac{A_{ij}}{\sin\theta_{ij}},
 \qquad
 \mu_i=\operatorname{Vol}_n(P_i).
                                                               \tag{3}
\]

Ridge area and chord angle are symmetric, so `gamma_ij=gamma_ji>0`.  Since

\[
 p_j-p_i=\sin\theta_{ij}t_{ij}-\ell_{ij}p_i,
 \qquad
 \frac{\ell_{ij}}{\sin\theta_{ij}}=q_{ij},
\]

(2) implies the exact, all-dimensional identity

\[
 \boxed{\sum_j\gamma_{ij}(p_j-p_i)=-n\mu_i p_i.}     \tag{4}
\]

After normalizing `w_i=mu_i/sum_k mu_k` and putting
`a_ij=gamma_ij/mu_i`, (4) proves

\[
 L1=0,\qquad Lp=-np,\qquad w_i a_{ij}=w_j a_{ji}.    \tag{5}
\]

This is a discrete cofactor/Piola construction: closure of the polar facet is
exactly tangent equilibrium.  It does not infer a shared stress from separate
row-wise feasible stencils.

### 1.1 The same stress as an exact volume Hessian

There is a second derivation which makes symmetry automatic.  Keep the normal
fan fixed and vary the support numbers:

\[
 Q(s)=\bigcap_i\{x:p_i\mathbin\cdot x\le s_i\},
 \qquad \mathcal V(s)=\operatorname{Vol}_d Q(s).
\]

On the open chamber in which the face lattice is unchanged,

\[
 \frac{\partial\mathcal V}{\partial s_i}=\mu_i,
 \qquad
 \frac{\partial^2\mathcal V}{\partial s_i\partial s_j}
 =\frac{A_{ij}}{\sin\theta_{ij}}=\gamma_{ij}\qquad(i\ne j).   \tag{5a}
\]

Indeed, moving a unit-normal support plane by `ds_i` adds facet volume
`mu_i ds_i`; inside `F_i`, moving the `j`-plane shifts the common ridge by
`ds_j/sin(theta_ij)`.  This proves (5a) directly, without an appeal to
equality of mixed derivatives.

Translations send `s_i` to `s_i+p_i dot v` and leave `mathcal V` unchanged.
Thus, for the Hessian `H=D^2 mathcal V`,

\[
 H(p_1,\ldots,p_N)=0.                                \tag{5b}
\]

Homogeneity of degree `d` gives `H 1=n(mu_i)_i` at `s=1`.  The diagonal
entry obtained from (5b) is

\[
 H_{ii}=-\sum_{j\ne i}\gamma_{ij}\cos\theta_{ij}.
\]

Consequently the `i`-th rows of (5b) and `H1=n mu` are precisely the tangent
and radial parts of (4).  Hence the ridge stress is simultaneously a polar
Piola stress and the off-diagonal support-Hessian stress of circumscribed
volume.

### 1.2 Exact null-Lagrangian correction directions

The Hessian description also produces genuine shared correction directions,
not separate row corrections.  For every support vector `s` in the same
normal-fan chamber, facet closure gives

\[
 T\gamma(s)=0,
 \qquad
 \gamma_{ij}(s)=\partial_i\partial_j\mathcal V(s)\qquad(i\ne j),
                                                               \tag{5c}
\]

where `(T gamma)_i=sum_j gamma_ij sin(theta_ij)t_ij`.  Therefore, for every
support velocity `u`,

\[
 z_{ij}(u)=\sum_k
 \frac{\partial^3\mathcal V}
      {\partial s_i\partial s_j\partial s_k}(1)u_k
 \quad(i\ne j)
 \qquad\Longrightarrow\qquad Tz(u)=0.               \tag{5d}
\]

These are exact discrete cofactor/null-Lagrangian stresses.  They preserve
tangent equilibrium to first order, are automatically shared, and are local
in the face-incidence graph.  If `|z_ij|<=eta gamma_ij` with `eta<1`, they
also preserve positivity after the finite update `gamma+z`.

What (5d) does **not** provide automatically is uniform surjectivity of the
map from support velocities to the mixed and trace-free quadratic moments.
That rank statement is an additional global compatibility theorem.  In
dimension one all off-diagonal `gamma_ij` are independent of the support
numbers (the ridges are points of area one), so the correction family (5d)
is identically zero.  The obstruction in Section 4 is therefore also an
exact rank failure of the cofactor-Hessian correction mechanism.

## 2. Exact quadratic blocks

Let `C_i=sum_j a_ij (p_j-p_i)(p_j-p_i)^T`, and decompose it relative to
`R p_i plus p_i^perp`.  Define

\[
 \epsilon_i=\frac2{\mu_i}\sum_j
       \frac{A_{ij}q_{ij}^3}{1+q_{ij}^2},             \tag{6}
\]

\[
 g_i=\frac2{\mu_i}\sum_j
       \frac{A_{ij}q_{ij}^2}{1+q_{ij}^2}t_{ij},       \tag{7}
\]

and

\[
 T_i=\frac2{\mu_i}\sum_j
       \frac{A_{ij}q_{ij}}{1+q_{ij}^2}
       t_{ij}t_{ij}^T.                                \tag{8}
\]

The half-angle identities

\[
 \sin\theta=\frac{2q}{1+q^2},\qquad
 1-\cos\theta=\frac{2q^2}{1+q^2}
\]

give the block matrix

\[
 C_i=
 \begin{pmatrix}
   \epsilon_i&-g_i^T\\
   -g_i&T_i
 \end{pmatrix}.                                      \tag{9}
\]

For the P1A remainder `B_i`, therefore,

\[
 \boxed{
 \|B_i\|_F^2
 =2\|g_i\|^2+
 \left\|T_i-\left(2-\frac{\epsilon_i}{n}\right)P_i
 \right\|_F^2.}                                     \tag{10}
\]

No approximation is used in (6)--(10).

### 2.1 Why a positive simplex-by-simplex patch test cannot replace (2)

Fix a vertex `p_i` of one nondegenerate spherical simplex.  Its other vertex
directions `t_ij` lie in an open hemisphere of `p_i^perp`: there is a tangent
vector `v` with `v dot t_ij>0` for every other vertex of that simplex.  Hence

\[
 P_i\sum_{j\in\sigma\setminus\{i\}}c_{ij}(p_j-p_i)
 =\sum_jc_{ij}\sin\theta_{ij}t_{ij}
\]

has strictly positive scalar product with `v` whenever `c_ij>=0` and at
least one coefficient is nonzero.  It cannot be radial.  Therefore exact
coordinate reproduction cannot be certified by requiring each simplex to
contribute a nonnegative tangent-balanced row.  The cancellation is
necessarily a closed-star (or dual-facet) identity.  This is the precise
place where a naive positive finite-element element assembly fails.

## 3. A sufficient second-order dual-cell condition

Assume

\[
 0<q_-h\le q_{ij}\le q_+h,
 \qquad \deg(i)\le D,                                \tag{11}
\]

and define the two affine-invariant polar-facet defects

\[
 \eta_i^{\rm cen}
 =\left\|\frac1{\mu_i}\sum_jA_{ij}q_{ij}^2t_{ij}\right\|,
\]

\[
 \eta_i^{\rm iso}
 =\left\|\frac1{\mu_i}\sum_jA_{ij}q_{ij}
                    t_{ij}t_{ij}^T-P_i\right\|_F.    \tag{12}
\]

Then (2), (6)--(8), and `q^4<=q_+^3 h^3 q` give

\[
 \epsilon_i\le2nq_+^2h^2,                            \tag{13}
\]

\[
 \|g_i\|\le2\eta_i^{\rm cen}+2nq_+^3h^3,           \tag{14}
\]

and, because a positive semidefinite matrix of trace `s` has traceless
Frobenius norm at most `s sqrt((n-1)/n)`,

\[
 \left\|T_i-\left(2-\frac{\epsilon_i}{n}\right)P_i
 \right\|_F
 \le2\eta_i^{\rm iso}
    +2\sqrt{n(n-1)}q_+^2h^2.                         \tag{15}
\]

Consequently the explicit assumption

\[
 \eta_i^{\rm cen}\le C_{\rm cen}h^2,
 \qquad
 \eta_i^{\rm iso}\le C_{\rm iso}h^2               \tag{16}
\]

implies

\[
 \|B_i\|_F\le h^2\left[
  2\sqrt2(C_{\rm cen}+nq_+^3h)
  +2C_{\rm iso}+2\sqrt{n(n-1)}q_+^2
 \right].                                            \tag{17}
\]

The rate is controlled without a hidden shape constant:

\[
 r_i=\frac1{\mu_i}\sum_j\frac{A_{ij}}{\sin\theta_{ij}}
 \le\frac{n(1+q_+^2h^2)}{2q_-^2h^2}.                \tag{18}
\]

If in addition the weighted sampling frame has

\[
 \sum_iw_i\langle A,Z_i\rangle_F^2
 \ge\alpha\|A\|_F^2
 \quad(A\in\operatorname{Sym}_0(d)),                \tag{19}
\]

then (13), (17), and the P1A row representation give an explicit
`mathfrak D_2 <= C h^2`; for example

\[
 \mathfrak D_2\le\alpha^{-1/2}
 \left(2\sqrt{dn}\,q_+^2+C_B\right)h^2,             \tag{20}
\]

where `C_B` is the bracket in (17).  Thus a polar-Piola family would solve
P1E if (11), (16), and (19) were established uniformly.  Local Delaunay
positivity supplies none of (16) by itself.

## 4. Exact obstruction on the circle

The missing centering estimate is necessary, not a proof artifact.  On
`S^1`, let the two angular gaps incident to a node be `alpha,beta in (0,pi)`.
Then `P_i` is the interval

\[
 [-\tan(\alpha/2),\tan(\beta/2)],
\]

both zero-dimensional ridge areas equal one, and

\[
 \mu_i=\tan(\alpha/2)+\tan(\beta/2),
\]

\[
 \|g_i\|
 =\frac{|(1-\cos\beta)-(1-\cos\alpha)|}
        {\tan(\alpha/2)+\tan(\beta/2)},
 \qquad
 \|B_i\|_F^2=2\|g_i\|^2.                            \tag{21}
\]

Take a circle whose gaps alternate between `h` and `2h`, with
`h=2pi/(3m)`.  This is a bounded-degree quasiuniform all-level family, all
conductances are strictly positive, and (5) is exact.  Nevertheless every
vertex satisfies

\[
 \frac{\|g_i\|}{h}\longrightarrow1.                 \tag{22}
\]

The P1B trace inequality then gives `mathfrak D_2 >= 2|g_i|` (the magnitude
is constant across the vertices), so this positive exact polar family has
only an `Omega(h)` quadratic defect.  Therefore no theorem deriving the P1E
upper rate from fill distance, separation, bounded degree, and strict
Delaunay margin alone can be valid.

## 5. Route decision

The polar-Piola route is retained as an independent exact construction and
as a convention check for geometric weights.  As a standalone all-level P1E
proof it is `BLOCKED` unless an explicit family with the two second-order
dual-cell estimates (16) is supplied.  Replacing (16) by quasiuniformity, or
claiming that it follows from positivity, is refuted by (21)--(22).
