# P1C — exact equality geometry, extremizing families, and sampling aliases

## 1. Standing hypotheses and theorem boundary

Let `I` be a finite nonempty set, let `d>=2`, and let

\[
 w_i>0,\qquad \sum_iw_i=1,\qquad
 \Omega_i\in S^{d-1}.
\]

Let

\[
 (Lf)_i=\sum_{j\ne i}a_{ij}(f_j-f_i),\qquad
 a_{ij}=\frac{\gamma_{ij}}{w_i},\qquad
 \gamma_{ij}=\gamma_{ji}\ge0,
\]

and assume

\[
 L\Omega=-(d-1)\Omega.                              \tag{1.1}
\]

An edge is *active* when `a_ij>0`. Thus positivity means nonnegative
off-diagonal rates with strictly positive rates on the declared support; it
does not mean that every pair of distinct nodes is joined.

Use the frozen P1A/P1B objects

\[
 \Delta_{ij}=\Omega_j-\Omega_i,\qquad
 \ell_{ij}=1-\Omega_i\cdot\Omega_j,\qquad
 r_i=\sum_{j\ne i}a_{ij},
\]

\[
 C_i=\sum_ja_{ij}\Delta_{ij}\Delta_{ij}^{T},\qquad
 \epsilon_i=\sum_ja_{ij}\ell_{ij}^{2},
\]

\[
 Z_i=\Omega_i\Omega_i^T-I/d,
\]

\[
 M_i=C_i+2\Omega_i\Omega_i^T-2I,
 \qquad
 B_i=M_i-\frac d{d-1}\epsilon_iZ_i,
\]

\[
 (S_2A)_i=\Omega_i^TA\Omega_i,\qquad
 R_2=(L+2dI)S_2,\qquad K_X=\ker S_2,
\]

and

\[
 \mathfrak D_2
 =\sup_{A\notin K_X}\frac{\|R_2A\|_w}{\|S_2A\|_w}.
\]

The publication-program notation

\[
 e_2:=\dim\bigl(\operatorname{im}S_2\cap\ker(L+2dI)\bigr)
      =\operatorname{rank}S_2-\operatorname{rank}R_2             \tag{1.2}
\]

is the dimension of the *genuinely sampled* exact quadratic space. It is not
the dimension of the algebraic form kernel.

P1B proves

\[
 \mathfrak D_2r_{\max}\ge d(d-1)                              \tag{1.3}
\]

and proves that equality is equivalent to

\[
 r_i=r_{\max},\qquad
 \sum_ja_{ij}\left(\ell_{ij}-\frac{d-1}{r_i}\right)^2=0,
 \qquad B_i=0                                                    \tag{1.4}
\]

at every vertex. P1C identifies the exact geometry of (1.4), proves its
converse in local-frame and global algebraic language, and proves all of the
requested extremizing families.

## 2. The exact radial--tangent block theorem

Fix a vertex `i` and abbreviate

\[
 u=\Omega_i,\qquad P=I-uu^T.
\]

For every neighbor put

\[
 \tau_{ij}:=P\Delta_{ij}=P\Omega_j
 =\Omega_j-(1-\ell_{ij})u.                                \tag{2.1}
\]

### Increment decomposition

Every increment decomposes exactly as

\[
 \boxed{\Delta_{ij}=-\ell_{ij}u+\tau_{ij}},              \tag{2.2}
\]

\[
 u\cdot\tau_{ij}=0,\qquad
 \boxed{\|\tau_{ij}\|^2=\ell_{ij}(2-\ell_{ij})}.         \tag{2.3}
\]

Indeed, `u dot Delta_ij=-ell_ij`, and

\[
 \|\Delta_{ij}\|^2=2\ell_{ij}
 =\ell_{ij}^2+\|\tau_{ij}\|^2.
\]

The radial and tangent parts of (1.1) give

\[
 \boxed{\sum_ja_{ij}\ell_{ij}=d-1},\qquad
 \boxed{\sum_ja_{ij}\tau_{ij}=0}.                       \tag{2.4}
\]

Define the mixed loss--tangent moment and tangent second moment

\[
 h_i:=\sum_ja_{ij}\ell_{ij}\tau_{ij},\qquad
 T_i:=\sum_ja_{ij}\tau_{ij}\tau_{ij}^T.                  \tag{2.5}
\]

If `p_ij=a_ij/r_i` and `bar ell_i=(d-1)/r_i`, then

\[
 \frac{h_i}{r_i}
 =\sum_jp_{ij}(\ell_{ij}-\bar\ell_i)\tau_{ij}.           \tag{2.6}
\]

Thus `h_i/r_i` is literally the loss--tangent covariance. If the signed
radial coordinate is `rho=-ell`, its radial--tangent covariance is
`-h_i/r_i`.

### Covariance and defect blocks

Expanding (2.2) gives

\[
 \boxed{
 C_i=\epsilon_i uu^T-uh_i^T-h_iu^T+T_i.                 \tag{2.7}
 }
\]

Since `I=uu^T+P`,

\[
 M_i=C_i-2P.                                             \tag{2.8}
\]

Also

\[
 Z_i=\frac{d-1}{d}uu^T-\frac1dP.
\]

Therefore

\[
 \boxed{
 B_i=-uh_i^T-h_iu^T+
 T_i-\left(2-\frac{\epsilon_i}{d-1}\right)P.            \tag{2.9}
 }
\]

Relative to the orthogonal decomposition
`R u direct-sum T_u S^(d-1)`, the three matrices are

\[
 C_i=
 \begin{pmatrix}\epsilon_i&-h_i^T\\-h_i&T_i\end{pmatrix},
\quad
 M_i=
 \begin{pmatrix}\epsilon_i&-h_i^T\\-h_i&T_i-2I_{d-1}\end{pmatrix},
\]

\[
 B_i=
 \begin{pmatrix}
 0&-h_i^T\\
 -h_i&T_i-(2-\epsilon_i/(d-1))I_{d-1}
 \end{pmatrix}.                                         \tag{2.10}
\]

The mixed and tangent blocks are Frobenius-orthogonal, so

\[
 \boxed{
 \|B_i\|_F^2
 =2\|h_i\|^2+
 \left\|T_i-\left(2-\frac{\epsilon_i}{d-1}\right)P
 \right\|_F^2.                                         \tag{2.11}
 }
\]

Consequently, with no shell, regularity, or injectivity assumption,

\[
 \boxed{
 B_i=0
 \iff
 h_i=0
 \quad\hbox{and}\quad
 T_i=\left(2-\frac{\epsilon_i}{d-1}\right)P.
 }                                                       \tag{2.12}
\]

This is the precise necessary-and-sufficient translation of the P1A tensor
defect: it is the conjunction of zero radial--tangential covariance and
isotropic tangent covariance.

## 3. Zero loss variance and weighted tangent tight frames

Put

\[
 \bar\ell_i=\frac{d-1}{r_i},\qquad
 V_i=\sum_ja_{ij}(\ell_{ij}-\bar\ell_i)^2.
\]

P1A proves

\[
 \epsilon_i=\frac{(d-1)^2}{r_i}+V_i.                   \tag{3.1}
\]

Because active rates are strictly positive,

\[
 V_i=0
 \iff
 \ell_{ij}=\bar\ell_i
 \quad\hbox{on every active edge out of }i.             \tag{3.2}
\]

When (3.2) holds,

\[
 \epsilon_i=(d-1)\bar\ell_i,\qquad
 h_i=\bar\ell_i\sum_ja_{ij}\tau_{ij}=0.                \tag{3.3}
\]

Equations (2.12)--(3.3) prove the exact raw-frame equivalence

\[
 \boxed{
 V_i=0,\ B_i=0
 \iff
 T_i=(2-\bar\ell_i)P.
 }                                                       \tag{3.4}
\]

For the reverse implication, take traces. Since

\[
 \operatorname{tr}T_i
 =\sum_ja_{ij}\ell_{ij}(2-\ell_{ij})
 =2(d-1)-\epsilon_i,
\]

the right side of (3.4) forces
`epsilon_i=(d-1)^2/r_i`. Equation (3.1) then gives `V_i=0`, after
which (2.4) gives `h_i=0` and (2.12) gives `B_i=0`. Thus (3.4) is a
genuine equivalence, not merely a sufficient one-shell criterion.

In this case

\[
 \boxed{
 C_i=(d-1)\bar\ell_i uu^T+(2-\bar\ell_i)P,
 }                                                       \tag{3.5}
\]

\[
 \boxed{M_i=d\bar\ell_iZ_i,\qquad B_i=0.}             \tag{3.6}
\]

### Nonantipodal branch

Assume explicitly

\[
 0<\bar\ell_i<2.                                        \tag{3.7}
\]

The lower endpoint is already excluded by (2.4); the upper endpoint is the
material nonantipodal hypothesis. Define

\[
 s_i=\sqrt{\bar\ell_i(2-\bar\ell_i)},\qquad
 y_{ij}=\frac{\tau_{ij}}{s_i},\qquad
 p_{ij}=\frac{a_{ij}}{r_i}.                             \tag{3.8}
\]

Then every active `y_ij` is a unit vector in `T_u S^(d-1)`, the positive
weights sum to one, and (2.4), (3.4), and
`r_i bar ell_i=d-1` give

\[
 \boxed{\sum_jp_{ij}y_{ij}=0},                         \tag{3.9}
\]

\[
 \boxed{
 \sum_jp_{ij}y_{ij}y_{ij}^T=\frac1{d-1}P.
 }                                                       \tag{3.10}
\]

Thus the projected tangent increments form a centered
probability-weighted unit-norm tight frame, equivalently a weighted spherical
2-design on the unit sphere of `T_u S^(d-1)`. Conversely (3.9)--(3.10),
together with the common loss and rate normalization, imply (3.4)--(3.6).

The conductance-weighted raw form is

\[
 \sum_j\gamma_{ij}\tau_{ij}\tau_{ij}^T
 =w_i(2-\bar\ell_i)P.                                  \tag{3.11}
\]

### Antipodal branch

If `bar ell_i=2`, every active neighbor is antipodal:

\[
 \Omega_j=-u,\qquad \tau_{ij}=0.
\]

Then `T_i=h_i=0`, `B_i=0`, and `M_i=2dZ_i`. Equality is
valid, but the projected increments are not a frame with a positive frame
bound. Division by `sqrt(ell(2-ell))` is forbidden. The unconditional block
theorem is (2.12), the zero-variance raw theorem is (3.4), and the genuine
tight-frame theorem is (3.7)--(3.10).

## 4. Complete equality theorem and precise converse

Let

\[
 r_*=r_{\max},\qquad
 \ell_*:=\frac{d-1}{r_*},\qquad
 c_*:=d\ell_*=\frac{d(d-1)}{r_*}.                      \tag{4.1}
\]

### Theorem P1C-local/global equality

Under the standing hypotheses, the following are equivalent.

1. The P1B frontier is saturated:

   \[
   \mathfrak D_2r_{\max}=d(d-1).
   \]

2. Every vertex has the one common outgoing rate `r_*`; every active edge
   has the one common chordal loss `ell_*`; the mixed covariance vanishes;
   and the tangent covariance is isotropic:

   \[
   r_i=r_*,\quad \ell_{ij}=\ell_*,\quad h_i=0,\quad
   T_i=(2-\ell_*)P_i.                                  \tag{4.2}
   \]

3. Every vertex has `r_i=r_*`, zero loss variance, and `B_i=0`.

4. The residual rows satisfy

   \[
   M_i=c_*Z_i\quad\hbox{for every }i.                  \tag{4.3}
   \]

5. On the full coefficient space and the sampled quotient,

   \[
   \boxed{R_2=c_*S_2},\qquad
   \boxed{\bar R_2=c_*\bar S_2}.                       \tag{4.4}
   \]

6. If `0<ell_*<2`, the conditions in item 2 can equivalently be written as
   one centered probability-weighted unit-norm tight frame
   (3.9)--(3.10) in every tangent space.

The six geometric phrases requested in P1C are therefore one equivalent
package, not six independent constraints. Common loss plus (1.1) already
forces zero mixed covariance; tangent isotropy is the unnormalized version
of tightness; and their conjunction produces scalar residual action.

### Proof and quotient correction

P1B gives equivalence of items 1 and 3. Equations (3.2)--(3.6) give
equivalence of items 2--4, and the row-representer identities give item 5.
Section 3 proves item 6 under its indispensable nonantipodal hypothesis.

Let

\[
 U:\operatorname{im}S_2\longrightarrow\ell^2(w),
 \qquad U(S_2A)=R_2A.
\]

The exact meaning of scalar quotient action is

\[
 \boxed{U=c_*\,\iota_{\operatorname{im}S_2}},           \tag{4.5}
\]

where `iota` is inclusion into the whole sample space. Merely projecting
`U` back onto `im S_2` and finding a scalar would not control orthogonal
leakage and is not equivalent to equality.

Conversely, suppose (4.4) holds with the scalar in (4.1). Then
`M_i=c_*Z_i`; radial contraction gives

\[
 \epsilon_i=\langle M_i,Z_i\rangle_F
 =c_*\frac{d-1}{d}=\frac{(d-1)^2}{r_*}.
\]

The exact variance identity and `r_i<=r_max` give

\[
 \frac{(d-1)^2}{r_{\max}}
 =\frac{(d-1)^2}{r_i}+V_i
 \ge \frac{(d-1)^2}{r_i}
 \ge \frac{(d-1)^2}{r_{\max}}.
\]

Hence both inequalities are equalities: `r_i=r_max` and `V_i=0` at every
vertex. The definition of `B_i` then forces `B_i=0`. This converse never
assumes `S_2` injective. An arbitrary unspecified scalar relation is
insufficient; its value must be tied to `r_max` as in (4.1).

### Exact sampled-space consequences

Since `c_*>0`, equality gives

\[
 \boxed{\ker R_2=\ker S_2=K_X},\qquad
 \boxed{e_2=0}.                                        \tag{4.6}
\]

Moreover

\[
 LS_2=-d(2-\ell_*)S_2.                                 \tag{4.7}
\]

Thus `im S_2` becomes an actual invariant eigenspace in an equality case,
although P1A correctly forbids assuming this invariance in general.

If the active graph is connected and `ell_*<2`, reversibility and (4.7)
give

\[
 \sum_iw_i\Omega_i=0,\qquad
 \sum_iw_i\Omega_i\Omega_i^T=I/d.                     \tag{4.8}
\]

Hence every connected nonantipodal equality configuration is also a global
weighted spherical 2-design. This global condition is not encoded by an
arbitrary collection of independent local frames.

## 5. Exact global algebraic assembly criterion

Assume `0<ell_*<2`, and put

\[
 t=1-\ell_*\in(-1,1),\qquad p_{ij}=a_{ij}/r_*.
\]

Then equality is exactly the following reversible Markov-kernel structure:

\[
 \sum_jp_{ij}=1,\qquad w_ip_{ij}=w_jp_{ji},             \tag{5.1}
\]

\[
 p_{ij}>0\Longrightarrow \Omega_i\cdot\Omega_j=t,     \tag{5.2}
\]

\[
 \boxed{\sum_jp_{ij}\Omega_j=t\Omega_i},              \tag{5.3}
\]

\[
 \boxed{
 \sum_jp_{ij}\Omega_j\Omega_j^T
 =t^2\Omega_i\Omega_i^T+
 \frac{1-t^2}{d-1}(I-\Omega_i\Omega_i^T).
 }                                                       \tag{5.4}
\]

Conversely, (5.1)--(5.4), with

\[
 r_*=(d-1)/(1-t),\qquad a_{ij}=r_*p_{ij},              \tag{5.5}
\]

reconstruct the coordinate eigenmap and the full equality theorem.

At Gram level, let `G_ij=Omega_i dot Omega_j`. The global completion
conditions are

\[
 G\succeq0,\quad G_{ii}=1,\quad \operatorname{rank}G=d,
 \quad p_{ij}>0\Rightarrow G_{ij}=t,                   \tag{5.6}
\]

\[
 \sum_jp_{ij}G_{jk}=tG_{ik},                           \tag{5.7}
\]

and, for all `i,k,l`,

\[
 \boxed{
 \sum_jp_{ij}G_{jk}G_{jl}
 =\alpha G_{kl}+(t^2-\alpha)G_{ik}G_{il},
 \qquad \alpha=\frac{1-t^2}{d-1}.
 }                                                       \tag{5.8}
\]

Equations (5.6)--(5.8) are an exact algebraic classification, but not a
short list of polytopes. They expose the missing gluing data: a single
positive-semidefinite rank-`d` Gram completion, endpoint compatibility, and
cycle closure.

For an oriented edge write

\[
 \Omega_j=t\Omega_i+s y_{ij},\qquad s=\sqrt{1-t^2}.
\]

Reversing the edge forces

\[
 \boxed{y_{ji}=s\Omega_i-t y_{ij}}.                    \tag{5.9}
\]

Independent abstract frames need not obey (5.9) around cycles.

For positive bidirected rates on a connected support, positive masses with
`w_i a_ij=w_j a_ji` exist if and only if every oriented cycle satisfies the
Kolmogorov identity

\[
 \prod_{(i,j)\ \mathrm{along\ the\ cycle}}a_{ij}
 =\prod_{(i,j)\ \mathrm{along\ the\ cycle}}a_{ji}.      \tag{5.10}
\]

Necessity follows by telescoping the weight ratios. For sufficiency, fix a
root, define weights by products of rate ratios along paths, use (5.10) for
path independence, and normalize. The weights are then unique up to a
common factor.

### Connected antipodal classification

If `ell_*=2`, connectedness forces all indexed nodes to occupy two geometric
positions `+u` and `-u`, and every active edge joins opposite positions.
The support is bipartite and

\[
 r_*=(d-1)/2,\qquad R_2=2dS_2.                         \tag{5.11}
\]

Conversely, every reversible connected constant-row-rate generator with
this geometry satisfies equality. Repeated indices at either position are
allowed; if geometric nodes are required distinct, only the two-node graph
remains.

## 6. What equality does and does not classify globally

Every connected nonantipodal equality generator is assembled from compatible
local weighted tight-frame vertex figures. The word *compatible* includes
(5.1)--(5.10). Local tightness alone is not a global classification.

### Minimum active degree

Let `n=d-1`. Suppose unit vectors `y_1,...,y_m` in `R^n` and positive
probabilities `p_k` satisfy

\[
 \sum_kp_ky_k=0,\qquad
 \sum_kp_ky_ky_k^T=I_n/n.                              \tag{6.1}
\]

Then

\[
 \boxed{m\ge n+1=d.}                                  \tag{6.2}
\]

If `m=d`, then

\[
 \boxed{p_k=1/d},\qquad
 \boxed{y_k\cdot y_l=-1/(d-1)\quad(k\ne l)}.          \tag{6.3}
\]

Proof: put

\[
 q_k=(\sqrt{np_k}\,y_k,\sqrt{p_k})\in\mathbb R^{n+1}.
\]

Equation (6.1) says `sum_k q_k q_k^T=I_(n+1)`. Hence there are at
least `n+1` columns. At equality the square synthesis matrix is orthogonal;
column norms and mutual orthogonality give (6.3).

Therefore every nonantipodal equality vertex has at least `d` active edges.
Degree exactly `d` forces a regular-simplex tangent figure,

\[
 p_{ij}=1/d,\qquad a_{ij}=r_*/d.                       \tag{6.4}
\]

On a connected reversible support this makes the masses uniform and the
graph `d`-regular. It still does not classify the graph.

### Complete-support classification

Assume the active support is the complete graph `K_N` and geometric nodes
are distinct. In the nonantipodal branch, (6.2) gives `N-1>=d`. All
off-diagonal Gram entries equal `t`, so

\[
 G=(1-t)I_N+tJ_N.                                      \tag{6.5}
\]

An equicorrelation Gram matrix has rank `N`, except at
`t=-1/(N-1)`, where its rank is `N-1`. Since the nodes lie in `R^d`, while
local tightness gives full tangent rank, (6.5) forces

\[
 \boxed{N=d+1,\qquad t=-1/d.}                          \tag{6.6}
\]

Thus the configuration is the regular simplex. Equation (6.3) and
reversibility force uniform weights and

\[
 a_{ij}=(d-1)/(d+1).                                   \tag{6.7}
\]

The antipodal complete-support case is only `K_2`. This is a complete
global classification under an explicit support hypothesis.

### Restricted convex Platonic classification on `S^2`

There is also a valid, deliberately restricted Platonic theorem. Assume:

```text
d=3;
0<ell_*<2;
the nodes are distinct vertices of a strictly convex inscribed polyhedron;
the active graph is exactly its 1-skeleton;
all active directed rates have one common value a>0;
the common vertex degree q satisfies 3<=q<=5.
```

Then the local tangent weights are equal. In a tangent plane identify unit
directions with complex numbers `z_k`. Centering and tightness are

\[
 \sum_{k=1}^qz_k=0,\qquad \sum_{k=1}^qz_k^2=0.         \tag{6.8}
\]

For `q<=5`, the self-inversive relations for a polynomial whose roots lie on
the unit circle turn the first two vanished elementary symmetric functions
into vanishing of all intermediate coefficients. Hence

\[
 z_k^q=\lambda
\]

for one unit scalar `lambda`: the tangent figure is a regular `q`-gon.

The Euclidean angle `beta` between consecutive chord edges satisfies

\[
 \cos\beta
 =\frac{\ell_*+(2-\ell_*)\cos(2\pi/q)}2.              \tag{6.9}
\]

All faces are therefore equilateral and equiangular. Their common size `p`
obeys `beta=(p-2)pi/p`. Euler's formula gives

\[
 \frac1p+\frac1q>\frac12,
\]

leaving exactly

\[
 (p,q)=(3,3),(4,3),(5,3),(3,4),(3,5).                 \tag{6.10}
\]

The classical convex regular-polyhedron theorem (equivalently, the
face-congruence conclusion followed by Cauchy rigidity) then yields the
tetrahedron, cube, dodecahedron, octahedron, and icosahedron. Solving (6.9)
gives their losses, respectively,

\[
 \frac43,\quad\frac23,\quad1-\frac{\sqrt5}{3},
 \quad1,\quad1-\frac1{\sqrt5}.                         \tag{6.11}
\]

This corollary is not asserted without its convex-skeleton, distinctness,
equal-rate, degree, and nonantipodal hypotheses.

### Exact obstructions to an unrestricted classification

1. **Connected covers and blow-ups.** Replace a base vertex `i` by `m_i`
   coincident copies, give each copy mass `w_i/m_i`, and split each base
   conductance `gamma_ij` as `gamma_ij/(m_i m_j)` across the complete
   bipartite fibers. Every lifted row has the same first and second moments,
   and equality survives. Connected graph covers give the same phenomenon
   using edge matchings. Thus connected equality graphs can be arbitrarily
   large.

2. **A distinct long-chord icosahedral shell.** On the same twelve exact
   icosahedral nodes, join the five nodes having dot product `-1/sqrt(5)`
   rather than the five shortest-edge neighbors. With

   \[
   a=(5-\sqrt5)/10,
   \]

   this connected graph has regular local pentagons and satisfies equality,
   but it is not the convex-hull 1-skeleton.

3. **Weighted frames need not be regular.** In `R^2`, the directions

   \[
   (\sqrt3/2,\pm1/2),\qquad
   (-1/\sqrt3,\pm\sqrt{2/3})
   \]

   with weights `(1/5,1/5,3/10,3/10)` are centered and have covariance
   `I/2`, but are not a square. Equality alone therefore does not make a
   degree-four weighted vertex figure regular.

4. **The graph does not select a spectral shell.** Even the hypercube graph
   admits higher-character equality embeddings. A short-edge or specified
   eigenspace hypothesis is required to classify the natural embedding.

These examples rule out a baseline Platonic classification and identify the
additional hypotheses needed for any stronger global theorem.

## 7. A one-shell family lemma

Let a uniform `q`-valent configuration have one edge loss `ell`, one active
directed rate `a`, and uniform mass `w=1/N`. Suppose its normalized tangent
vertex figure is an unweighted unit-norm tight frame:

\[
 \sum_{j\sim i}y_{ij}=0,\qquad
 \sum_{j\sim i}y_{ij}y_{ij}^T=\frac q{d-1}P_i.          \tag{7.1}
\]

Choose

\[
 qa\ell=d-1.                                           \tag{7.2}
\]

Then

\[
 r_i=qa=\frac{d-1}{\ell},\qquad
 \epsilon_i=(d-1)\ell,\qquad
 \gamma_{ij}=a/N,                                      \tag{7.3}
\]

\[
 C_i=(d-1)\ell\Omega_i\Omega_i^T+(2-\ell)P_i,          \tag{7.4}
\]

\[
 M_i=d\ell Z_i,\qquad B_i=0,                           \tag{7.5}
\]

\[
 R_2=d\ell S_2,\qquad
 \boxed{\mathfrak D_2=d\ell},\qquad
 \boxed{\mathfrak D_2r_i=d(d-1)}.                     \tag{7.6}
\]

This lemma proves the local part of every family below. The sampling ranks
and kernels are proved separately and exactly.

## 8. Three all-dimensional equality families

All statements in this section hold for every integer `d>=2`.

### 8.1 Regular simplex with complete graph

Work in `1^perp subset R^(d+1)` and set

\[
 \Omega_i=\sqrt{\frac{d+1}{d}}
 \left(e_i-\frac1{d+1}{\bf1}\right),\qquad 0\le i\le d.
\]

Then

\[
 \Omega_i\cdot\Omega_j=-1/d\quad(i\ne j),\qquad
 \sum_i\Omega_i=0,
\]

\[
 \sum_i\Omega_i\Omega_i^T=\frac{d+1}{d}I.
\]

The exact data are

\[
 N=d+1,\quad w_i=\frac1{d+1},\quad
 a_{ij}=\frac{d-1}{d+1},\quad
 \gamma_{ij}=\frac{d-1}{(d+1)^2},                     \tag{8.1}
\]

\[
 r_i=\frac{d(d-1)}{d+1},\quad
 \ell_{ij}=\frac{d+1}{d},\quad
 \epsilon_i=\frac{d^2-1}{d}.                          \tag{8.2}
\]

For `j ne i`,

\[
 \tau_{ij}=\Omega_j+\Omega_i/d.
\]

The `d` normalized tangent directions have pairwise dot product
`-1/(d-1)` and equal weights `1/d`; they are a regular simplex in the
tangent space. Hence

\[
 C_i=\frac{d-1}{d}I+(d-1)\Omega_i\Omega_i^T,           \tag{8.3}
\]

\[
 M_i=(d+1)Z_i,\qquad B_i=0,                            \tag{8.4}
\]

\[
 \mathfrak D_2=d+1,\qquad
 \mathfrak D_2r_i=d(d-1).                              \tag{8.5}
\]

The sampling-row Gram has diagonal `(d-1)/d` and off-diagonal
`-(d-1)/d^2`, hence rank `d`. In the canonical `(d+1)`-coordinate model,

\[
 K_X\cong
 \{A\in\operatorname{Sym}(d+1):A{\bf1}=0,
 \ \operatorname{diag}A=0\}.                          \tag{8.6}
\]

Therefore

\[
 \dim K_X=\frac{(d+1)(d-2)}2,\qquad e_2=0.             \tag{8.7}
\]

### 8.2 Cross-polytope with the nonantipodal graph

Take the nodes `Omega_(sigma,k)=sigma e_k`, `sigma=+-1`. Join two nodes
exactly when their coordinate axes differ, excluding the antipodal pair.
Every node has `2(d-1)` active neighbors. The exact data are

\[
 N=2d,\quad w_i=\frac1{2d},\quad
 a_{ij}=\frac12,\quad \gamma_{ij}=\frac1{4d}           \tag{8.8}
\]

on active edges, and zero otherwise, with

\[
 r_i=d-1,\quad \ell_{ij}=1,\quad \epsilon_i=d-1.       \tag{8.9}
\]

At `Omega_i=sigma e_k`, the tangent directions are the cross-polytope
`+-e_l`, `l ne k`, in the tangent space. Therefore

\[
 C_i=I+(d-2)\Omega_i\Omega_i^T,\quad
 M_i=dZ_i,\quad B_i=0,                                 \tag{8.10}
\]

\[
 \mathfrak D_2=d,\qquad \mathfrak D_2r_i=d(d-1).       \tag{8.11}
\]

Sampling sees precisely the trace-free diagonal part, so

\[
 K_X=\{A\in\operatorname{Sym}_0(d):A_{11}=\cdots=A_{dd}=0\},
\]

\[
 \operatorname{rank}S_2=d-1,\quad
 \dim K_X=\frac{d(d-1)}2,\quad e_2=0.                  \tag{8.12}
\]

### 8.3 Hypercube with edge graph

Take

\[
 \Omega_x=x/\sqrt d,\qquad x\in\{\pm1\}^d,
\]

and join sign vectors of Hamming distance one. The exact data are

\[
 N=2^d,\quad w_x=2^{-d},\quad
 a_{x,x^{(k)}}=\frac{d-1}{2},\quad
 \gamma_{x,x^{(k)}}=\frac{d-1}{2^{d+1}},               \tag{8.13}
\]

\[
 r_x=\frac{d(d-1)}2,\quad
 \ell_{x,x^{(k)}}=\frac2d,\quad
 \epsilon_x=\frac{2(d-1)}d.                           \tag{8.14}
\]

The edge increment and tangent projection are

\[
 \Delta_{x,k}=-\frac{2x_k}{\sqrt d}e_k,
\]

\[
 \tau_{x,k}=-\frac{2x_k}{\sqrt d}P_xe_k.
\]

The `d` normalized tangent directions form a regular simplex with equal
weights. Directly,

\[
 \sum_ka_{x,x^{(k)}}\tau_{x,k}\tau_{x,k}^T
 =\frac{2(d-1)}dP_x.
\]

Consequently

\[
 C_x=\frac{2(d-1)}dI,\quad M_x=2Z_x,\quad B_x=0,       \tag{8.15}
\]

\[
 \mathfrak D_2=2,\qquad \mathfrak D_2r_x=d(d-1).       \tag{8.16}
\]

For `A in Sym_0(d)`,

\[
 (S_2A)_x=\frac2d\sum_{p<q}A_{pq}x_px_q.
\]

The Walsh characters `x_p x_q` are independent. Thus

\[
 K_X=\{\operatorname{diag}(\lambda_1,\ldots,\lambda_d):
 \sum_k\lambda_k=0\},
\]

\[
 \operatorname{rank}S_2={d\choose2},\quad
 \dim K_X=d-1,\quad e_2=0.                             \tag{8.17}
\]

These derivations are all-dimensional algebraic proofs. The finite exact
regressions at `d=2,3,4,5` are checks, not their logical basis.

## 9. The five Platonic equality generators

Put

\[
 \varphi=(1+\sqrt5)/2,\qquad \rho=\sqrt{\varphi+2}.
\]

Use the following exact unit coordinates:

- tetrahedron:
  `(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)`, divided by
  `sqrt(3)`;
- octahedron: `+-e_1,+-e_2,+-e_3`;
- cube: all `(+-1,+-1,+-1)/sqrt(3)`;
- icosahedron: all sign choices in
  `(0,+-1,+-varphi)`, `(+-1,+-varphi,0)`,
  `(+-varphi,0,+-1)`, divided by `rho`;
- dodecahedron: all `(+-1,+-1,+-1)/sqrt(3)` and all sign choices in
  `(0,+-varphi^{-1},+-varphi)`,
  `(+-varphi^{-1},+-varphi,0)`,
  `(+-varphi,0,+-varphi^{-1})`, divided by `sqrt(3)`.

Join shortest-edge pairs. Exact dot-product comparison gives the adjacent
dot product `alpha` and degree `q` in the table below. With uniform masses,
choose

\[
 a=\frac{2}{q(1-\alpha)},\qquad
 \gamma=\frac aN.                                      \tag{9.1}
\]

At each vertex the normalized projected neighbors are a regular `q`-gon in
the tangent plane, so

\[
 \sum_{j\sim i}y_{ij}=0,\qquad
 \sum_{j\sim i}y_{ij}y_{ij}^T=\frac q2P_i.             \tag{9.2}
\]

The one-shell lemma therefore proves every equality statement in the table.

| polyhedron | `N/q` | `w` | `alpha` | `ell` | active `a` | active `gamma` | `r` | `epsilon` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tetrahedron | `4/3` | `1/4` | `-1/3` | `4/3` | `1/2` | `1/8` | `3/2` | `8/3` |
| octahedron | `6/4` | `1/6` | `0` | `1` | `1/2` | `1/12` | `2` | `2` |
| cube | `8/3` | `1/8` | `1/3` | `2/3` | `1` | `1/8` | `3` | `4/3` |
| icosahedron | `12/5` | `1/12` | `sqrt(5)/5` | `1-sqrt(5)/5` | `(5+sqrt(5))/10` | `(5+sqrt(5))/120` | `(5+sqrt(5))/2` | `2-2sqrt(5)/5` |
| dodecahedron | `20/3` | `1/20` | `sqrt(5)/3` | `1-sqrt(5)/3` | `(3+sqrt(5))/2` | `(3+sqrt(5))/40` | `(9+3sqrt(5))/2` | `2-2sqrt(5)/3` |

For `d=3`, formula (7.4) becomes

\[
 C_i=(1+\alpha)I+(1-3\alpha)\Omega_i\Omega_i^T.        \tag{9.3}
\]

Thus the remaining exact data are:

| polyhedron | `C_i` | `M_i` | `B_i` | `K_X` | `e_2` | `mathfrak D_2` | `mathfrak D_2 r_i` |
|---|---|---|---:|---|---:|---:|---:|
| tetrahedron | `(2/3)I+2 Omega_i Omega_i^T` | `4Z_i` | `0` | diagonal trace-free, dim `2` | `0` | `4` | `6` |
| octahedron | `I+Omega_i Omega_i^T` | `3Z_i` | `0` | zero-diagonal/off-diagonal, dim `3` | `0` | `3` | `6` |
| cube | `(4/3)I` | `2Z_i` | `0` | diagonal trace-free, dim `2` | `0` | `2` | `6` |
| icosahedron | `(1+sqrt(5)/5)I+(1-3sqrt(5)/5)Omega_i Omega_i^T` | `(3-3sqrt(5)/5)Z_i` | `0` | `{0}` | `0` | `3-3sqrt(5)/5` | `6` |
| dodecahedron | `(1+sqrt(5)/3)I+(1-sqrt(5))Omega_i Omega_i^T` | `(3-sqrt(5))Z_i` | `0` | `{0}` | `0` | `3-sqrt(5)` | `6` |

No numerical rank tolerance occurs in these statements.

## 10. Exact sampling-kernel and alias certificates

Use the coefficient columns

\[
 x^2-y^2,\quad 2z^2-x^2-y^2,\quad xy,\quad xz,\quad yz. \tag{10.1}
\]

For the displayed tetrahedral and cubical coordinates, the first two columns
vanish identically, while exact `3 by 3` minors in the last three columns are
`-4/27` and `4/27`. Hence

\[
 K_X^{\rm tetra}=K_X^{\rm cube}
 =\operatorname{span}\{x^2-y^2,\ 2z^2-x^2-y^2\}.       \tag{10.2}
\]

For the octahedron, the last three columns vanish, and an exact `2 by 2`
minor in the first two columns is `-2`. Hence

\[
 K_X^{\rm octa}=\operatorname{span}\{xy,xz,yz\}.       \tag{10.3}
\]

For the icosahedron, rows corresponding to

\[
 (0,1,\varphi),(0,-1,\varphi),(1,\varphi,0),
 (-1,\varphi,0),(\varphi,0,1)
\]

divided by `rho` give a `5 by 5` sampling minor

\[
 \boxed{-16\sqrt5/125\ne0}.                            \tag{10.4}
\]

For the dodecahedron, the rows

\[
 (-1,-1,-1),(-1,-1,1),(-1,1,-1),
 (0,-\varphi^{-1},-\varphi),(-\varphi^{-1},-\varphi,0)
\]

divided by `sqrt(3)` give

\[
 \boxed{16/81\ne0}.                                    \tag{10.5}
\]

Thus the icosahedral and dodecahedral sampling maps have rank five and zero
kernel over `Q(sqrt(5))`.

Because every example has `R_2=cS_2` with `c>0`,

\[
 E_{\rm form}=\ker R_2=K_X,
 \qquad
 E_{\rm sample}=S_2(E_{\rm form})=\{0\}.               \tag{10.6}
\]

For example, `diag(1,-1,0)` is a nonzero tetrahedral and cubical algebraic
form that samples to zero, while the `xy` form does so on the octahedron.
They are exact only vacuously as sampled functions. They do not enter the
quotient supremum defining `mathfrak D_2`, and they do not constitute a
nonzero reproduced `H_2` mode. Frontier equality and nonzero sampled exact
quadratics are different questions; in fact equality here forces `e_2=0`.

## 11. Prior-art transfer boundary

The external literature supplies language and adjacent structure, not the
P1C theorem.

- Izmestiev--Lam use the weighted self-adjoint negative-semidefinite
  convention and geometry-specific spherical Delaunay weights. Their
  operator is a special construction; it does not prove the arbitrary
  shared-conductance equality blocks or the sampled quotient theorem.
- Martin--Tanaka's primitive idempotents, Schur products, and Hamming-scheme
  eigenspaces organize uniform symmetric examples. They do not cover
  arbitrary positive stationary masses or prove endpoint/reversibility
  compatibility for a prescribed spherical embedding.
- Bannai--Bannai's spherical-design moment language explains (3.9)--(3.10)
  and (4.8), but design strength alone neither constructs the generator nor
  supplies sampled injectivity.
- Ahrens--Beylkin construct icosahedrally invariant quadratures. Their
  quadrature exactness and cardinality problem is not the local AFP
  equality classification.
- The standard finite-frame operator identity is used as terminology; the
  exact block converse, rate normalization, and minimal-frame lemma are
  proved here.
- The classical convex regular-polyhedron theorem is used only after all
  explicit hypotheses of the restricted corollary in Section 6 have been
  established.

No external theorem is transferred into the unrestricted P1C equality
theorem.

## 12. Exact computational and formal audit boundary

Run

```text
cd afp_barrier_gate1
python pure_math/covariance/p1c_equality_geometry_audit.py
```

The audit verifies in exact algebra:

```text
the radial/tangent increment and B-block decompositions;
the orthogonal B norm identity;
the nonantipodal weighted tight-frame normalization;
the antipodal zero-frame exception;
symbolic scalar formulas for all three all-dimensional families;
exact family fixtures through d=5;
all five Platonic generators and every requested scalar/matrix value;
exact rational/Q(sqrt(5)) sampling minors;
K_X, E_form, e_2, and quotient scalar action;
a connected repeated-node blow-up adversary;
a connected distinct long-chord icosahedral adversary;
a nonregular weighted tangent frame;
the Kolmogorov cycle-product mutation.
```

Finite fixtures are regression and falsification evidence. The
all-dimensional statements, equality iff, global assembly criterion, and
restricted classifications are proved in the preceding sections rather than
inferred from computation.

The Lean finite core formalizes the division-free projected increment,
orthogonality and norm identities, the scalar remainder/axial-covariance
bridge, the raw tangent-second-moment iff, scaling, and the normalized
weighted-frame conversion with explicit nonzero denominators. Graph
classification remains in the ordinary proof, where its geometric
hypotheses are visible.

## Certification

```text
P1C EXACT LOCAL EQUALITY GEOMETRY: PROVED

RADIAL--TANGENT BLOCK CONVERSE AND NORM IDENTITY: PROVED

NONANTIPODAL WEIGHTED TIGHT-FRAME EQUIVALENCE: PROVED

ANTIPODAL EQUALITY BRANCH: CLASSIFIED SEPARATELY

SIMPLEX / CROSS-POLYTOPE / HYPERCUBE ALL-DIMENSIONAL FAMILIES: PROVED

FIVE PLATONIC SHORTEST-EDGE GENERATORS: PROVED IN EXACT ALGEBRA

SAMPLING ALIASES AND e_2=0: PROVED AND AUDITED

GLOBAL ALGEBRAIC ASSEMBLY CRITERION: PROVED

COMPLETE-SUPPORT AND RESTRICTED CONVEX CLASSIFICATIONS: PROVED

UNRESTRICTED PLATONIC CLASSIFICATION: REJECTED BY EXACT COUNTERFAMILIES
```
