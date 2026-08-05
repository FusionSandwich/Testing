# P1E stratified-lattice repair and global obstruction

## Status

`LEMMA 1 IS PROVED; THE GLOBAL CONSTRUCTION IN SECTIONS 2--7 IS
CONDITIONAL/BLOCKED.`  The residue-unwinding formula repairs the exact
`|Z|=2, |B|=3` algebraic failure.  It does **not** by itself provide the
globally compatible smooth one-point-lattice atlas assumed in Section 2.
Section 9 proves that such an atlas cannot exist on a sphere of dimension at
least two.  Accordingly, Sections 2--7 record the precise theorem that would
follow from that extra atlas hypothesis, and identify where a genuinely
stratified interface construction (or an augmented multi-sheet mesh) is
still required.  They must not be cited as an unconditional P1E theorem.

## 0. What is repaired

The assertion that the raw centered-block image of the simplex-boundary
lattice is a finite-basis periodic crystal is false.  For example, when
`|Z|=2` and `|B|=3`, the centered `B` coordinate occupies a coset indexed by
`N-|m| (mod 3)`, where `m` is the signed normal-layer coordinate.  The
absolute value prevents a single translation action from preserving the
record across the tie hyperplane.

There is, however, an exact one-line repair.  Subtract the *whole integer
mass of the B block in a distinguished B direction*, rather than merely
centering that block.  The resulting chart sends the lattice to a direct
product of a weight lattice and a root lattice, with one point per cell.  In
particular there is no residue basis, no optical mode, and no interface
defect at a minimum-tie hyperplane.

This note first proves the repaired local lattice statement and then states
the conditional all-level construction it would support.  Every object used in
the construction is either given by a displayed formula or is the output of
a finite rational operation described below.  The finite operations are not
level-dependent.

Throughout, `n=d-1`, `d>=3`, `W=S_(d+1)`, and

\[
 K_N=\{N^{-1}k:k\in\mathbb Z_{\geq0}^{d+1},\ \sum_a k_a=N,
                         \ \min_a k_a=0\},\qquad h=N^{-1}.
\tag{0.1}
\]

## 1. The residue-unwinding chart

Let `Z` be a nonempty proper subset of `{0,...,d}`, let `B=Z^c`, put
`z=|Z|`, `b=|B|`, and choose `beta in B`.  Write

\[
 H_Z=\{q\in\mathbb R^Z:\sum_Zq=0\},\qquad
 H_B=\{t\in\mathbb R^B:\sum_Bt=0\}.
\]

On the boundary neighborhood on which every `B` coordinate is positive
(and hence `min_Z lambda_Z=0`), define

\[
 \boxed{\quad
 q=P_Z\lambda_Z,\qquad
 s_B=\sum_{b\in B}\lambda_b=1+z\min_Zq,
 \qquad t=\lambda_B-s_Be_\beta .\quad}
\tag{1.1}
\]

The inverse is the explicit piecewise-affine map

\[
 \lambda_Z=q-(\min_Zq)1_Z,
 \qquad \lambda_B=t+(1+z\min_Zq)e_\beta .
\tag{1.2}
\]

Thus (1.1) is a homeomorphism onto the region determined by positivity of
the right side of (1.2).  It is linear on every cone on which the index set
of the minimum of `q` is fixed.

Let

\[
 A_Z^*=P_Z\mathbb Z^Z,
 \qquad A_B=\mathbb Z^B\cap H_B .
\tag{1.3}
\]

### Lemma 1 (exact product lattice)

In every closed subcollar on which `lambda_b>=s_*h` for `b in B`, the image
of `K_N` under (1.1), together with every lattice neighbor at product-lattice
distance at most `s_*h`, is exactly the corresponding restriction of

\[
                    h(A_Z^*\times A_B).             \tag{1.4}
\]

There is no finite residue basis in (1.4).

**Proof.**  Put `lambda=k/N`.  If `q=P_Zlambda_Z`, then

\[
 Nq=P_Zk_Z\in A_Z^*,\qquad
 m:=\sum_Zk_z=-z\min_Z(Nq)\in\mathbb Z.
\]

Since `Ns_B=N-m`,

\[
 Nt=k_B-(N-m)e_\beta\in\mathbb Z^B\cap H_B=A_B.
\]

Conversely, if `Q=P_Zu_Z in A_Z^*`, then
`Q-(min Q)1_Z` is an integral nonnegative vector with minimum zero.  If
`T in A_B`, set `m=-z min Q`, `S=N-m`, and
`k_B=T+Se_beta`.  These formulae invert the preceding construction whenever
the displayed positivity inequalities hold.  The buffer `s_*h` is exactly
what guarantees that all requested neighbors remain in the chart.  QED.

### The formerly failing `2+3` record

Take `Z={0,1}`, `B={2,3,4}`, and `beta=2`.  Write

\[
 Nq=(r/2,-r/2),\qquad r=k_0-k_1,qquad m=|r|.
\]

The raw centered coordinate has `A_2^*/A_2` class `N-|r| (mod 3)`.  In the
repaired coordinate,

\[
 Nt=k_B-(N-|r|)e_2=(-k_3-k_4,k_3,k_4)\in A_2.       \tag{1.5}
\]

Consequently the exact node record is

\[
 \{(r/2,-r/2):r\in\mathbb Z\}\times
 \{(u_2,u_3,u_4)\in\mathbb Z^3:u_2+u_3+u_4=0\},   \tag{1.6}
\]

clipped only by the explicitly displayed positivity inequalities.  The
hyperplane `r=0` is an ordinary lattice hyperplane in (1.6); it is not a
crystal interface.

For clarity, take the primitive `A_1^*` step

\[
 v_0=((1/2,-1/2);0).
\]

At `r=0`, the `+v_0` edge transfers one unit from `beta` to coordinate `0`,
and the `-v_0` edge transfers one unit from `beta` to coordinate `1`.  At
`r=1` the reverse of the first edge is the `-v_0` edge, and at `r=-1` the
reverse of the second is the `+v_0` edge.  Thus midpoint assignment gives
the same coefficient from both endpoints; no directed ownership convention
is hidden at the tie.

More generally, choose a lattice basis `v_0,v_1,v_2` of
`A_1^* x A_2` and give every `+/-v_a` pair frozen coefficient at least
`rho>0`.  In basis-frequency coordinates `xi in [-pi,pi]^3`, the scalar
symbol obeys the unconditional estimate

\[
 p(xi)\ge4rho\sum_{a=0}^2\sin^2(xi_a/2)
       \ge {4rho\over\pi^2}|xi|^2.                 \tag{1.7}
\]

The estimate is unchanged at `r=0`.  Hence the repaired local record has no
zero-frequency surface mode.  This local fact does not settle the overlap
of two *different* stratified charts; that is the global obstruction in
Section 9.

## 2. A finite, equivariant smooth atlas with lattice buffers

**Conditional hypothesis (and eventual blocker).**  This section assumes
that the records below can be selected so that every overlap carrying two
nonconstant stencil weights is smooth and affine unimodular.  Section 9
shows that a cover with this property is impossible on `S^n`, `n>=2`.

Use every triple `(Z,beta,sigma)`, where `sigma` records a cone of the braid
fan (a weak ordering of the coordinates in `Z`).  Copy records by `W`; no
distinguished coordinate is chosen equivariantly.  Choose rational collar
numbers

\[
 0<\eta_d<\eta_{d-1}<\cdots<\eta_1<1/(100(d+1))
\tag{2.1}
\]

successively, each at most one hundredth of its predecessor.  A record is
used only where all coordinates outside its `Z` block exceed `4eta_|Z|`.
The transition to a smaller `Z` record is made where the coordinates removed
from `Z` exceed `2eta_|Z|`.  On such an overlap the minimum index set is
fixed, so (1.1)--(1.2) give an affine lattice isomorphism.  The transition
matrix maps `A_Z^* x A_B` bijectively to the lattice of the adjacent record.

If the conditional overlap requirement held, it would give finitely many
rational polyhedral cores `C_a` and buffers `U_a`
such that:

1. the cores cover the simplex boundary;
2. `dist(C_a, boundary U_a)>=eta_d` in the chart norm;
3. every overlap on which both weights vary has an affine unimodular
   transition;
4. the family is permuted by `W`.

Tensor-product Hermite interpolation of order six on this finite box
complex, followed by the fixed beta(7,7) join polynomial, constructs:

* a `W`-equivariant `C^6` diffeomorphism
  `F: boundary Delta^d -> S^n` in these charts;
* nonnegative `C^5` functions `chi_a` supported in `U_a`, equal to one on a
  smaller core, with `sum_a chi_a=1`;
* explicit rational upper bounds `K_j` for the chart derivatives through
  order six and a rational lower bound `k_1>0` for the least singular value
  of `DF`.

The construction is terminating: endpoint jets are obtained by inversion of
a fixed triangular integer matrix; collar widths are reduced until rational
interval determinants exclude zero.  Because overlaps carrying two
nonconstant `chi_a` have affine lattice transitions, no nonsmooth minimum
function enters a Taylor expansion.

For all

\[
 h\le h_at:=\eta_d/(4s_*),                         \tag{2.2}
\]

every active stencil centered in `supp chi_a` lies in the exact product
lattice buffer of Lemma 1.

## 3. Explicit positive shared energy

Fix a lattice basis in every representative record.  Let
`V_R={v in Lambda_a:0<|v|_infty<=R}` and identify `v` with `-v`.  The integer
`R` is chosen as follows.  If the pulled-back metric density tensors

\[
 A_a(q)=\sqrt{\det g_a(q)}\,g_a(q)^{-1}             \tag{3.1}
\]

have eigenvalues in `[m_a,M_a]`, take a rational directional net from
`V_R` with angular radius

\[
 eta_a<m_a/(8nM_a).                                \tag{3.2}
\]

Such an `R` is found by enumerating integer vectors; termination follows
from density of rational directions, and the first successful `R` is part
of the compiler record.

Here and below the chart components are expressed in the chosen lattice
basis, so the node lattice is literally `h Z^n`.  On an overlap the change
of lattice basis is unimodular.  Consequently `sqrt(det g) g^{-1}` is the
correct density tensor for the counting measure; no unrecorded lattice
covolume is missing from (3.1).

The cone generated by `{vv^T:v in V_R}` contains every matrix with spectrum
in `[m_a,M_a]` in its quantitative interior.  Indeed, if a symmetric `Q`
satisfies `v^TQv>=0` on the net and `||Q||=1`, a nearest-net argument gives
`lambda_min(Q)>=-2eta_a`; hence

\[
 tr(AQ)\ge m_a-2nM_aeta_a>3m_a/4.                 \tag{3.3}
\]

Dual separation proves the cone assertion and gives its stated margin.
Moreover, if `G=sum_v vv^T`, compactness of the spectral box and the strict
dual margin give an effective `eps_a>0` for which `A-eps_a G` remains in the
cone.  Hence every generator can be assigned the common positive floor
`eps_a`.
To obtain coefficients rather than invoke a selection lemma, enumerate
rational simplicial subcones of the finite generator cone, solve their
square linear systems exactly, shrink each positivity region by the margin
`m_a/8`, and blend the resulting linear coefficient maps with the same
fixed Hermite partition used in Section 2.  The output consists of `C^4`
functions `rho_av(q)=rho_a,-v(q)>=0` satisfying

\[
 2\sum_{v\in V_R/\{\pm1\}}rho_{av}(q)vv^T=A_a(q). \tag{3.4}
\]

On a subcollection which generates the lattice, `rho_av>=rho_*>0`.  All
numbers in this step are solutions of finite rational linear systems plus
rational interval bounds for (3.1); thus `R`, `rho_*`, and the `C^4` bounds
are effective constants depending only on `d` and the fixed atlas.

For `lambda_i,lambda_j in K_N`, define the shared coefficient

\[
 c_{ij}=h^{n-2}\sum_{a}\sum_{v\in V_R/\{\pm1\}}
  1_{\{\psi_a(\lambda_j)-\psi_a(\lambda_i)=\pm hv\}}
  \chi_a\!\left({\psi_a(\lambda_i)+\psi_a(\lambda_j)\over2}\right)
  \rho_{av}\!\left({\psi_a(\lambda_i)+\psi_a(\lambda_j)\over2}\right).
\tag{3.5}
\]

Terms whose midpoint is outside the buffered chart are declared zero.  The
buffer condition (2.2) makes this declaration irrelevant on the support of
the corresponding `chi_a`.

Formula (3.5) is the requested global definition.  It immediately gives

\[
 c_{ij}=c_{ji}\ge0.                                \tag{3.6}
\]

At least one chart has weight at least `1/N_atlas` at every point.  Its
positive generating sub-stencil and (3.3) therefore give a local ellipticity
margin

\[
 \sum_jc_{ij}(u_j-u_i)^2
 \ \text{has frozen symbol}
 p(q,xi)\ge c_0\min\{dist(xi,2pi Lambda^*)^2,1\},  \tag{3.7}
\]

where one may take

\[
 c_0=4rho_*/(N_atlas C_basis^2).                   \tag{3.8}

The degree is at most `D_*=2 N_atlas |V_R|`.  Since `F` is bi-Lipschitz in
the buffered charts, every active edge satisfies, after reducing `h_at` if
necessary,

\[
 q_*h\le d_S(F(lambda_i),F(lambda_j))\le Q_*h,     \tag{3.9}
\]

with `q_*=k_1 min_{v in V_R}|v|/2` and
`Q_*=2K_1 max_{v in V_R}|v|`.  The same chart bounds give fill distance
`H_*h`, separation `q_*h`, and a mesh ratio `H_*/q_*`.

## 4. Moment expansion

Put `y_i=F(lambda_i)`.  For one pair `+/-v`, Taylor expansion at the two
edge midpoints gives

\[
 h^{n-2}\{b(q+hv/2)[F(q+hv)-F(q)]
          +b(q-hv/2)[F(q-hv)-F(q)]\}
\]

\[
 =h^n div_q(bvv^TDF)(q)+h^{n+2}R_{v}(q),          \tag{4.1}
\]

with

\[
 |R_v|+[R_v]_{alpha,h}
 \le C_T|v|^6||b||_{C^{3,alpha}}||F||_{C^{4,alpha}}.\tag{4.2}
\]

There is no `h^(n+1)` term: midpoint sampling and the `+/-v` pair make the
flux central.  Summing (4.1), using (3.4), `sum chi_a=1`, and the identity
that the identity map of the round sphere is harmonic, yields

\[
 \left\|{h^{-n}\over vartheta_i}P_{y_i}
      \sum_jc_{ij}(y_j-y_i)\right\|_{0,alpha,h}
 \le C_T' h^2,                                    \tag{4.3}
\]

where `vartheta_i` is the chart density, bounded above and below by the
compiler constants.  Concretely, in a lattice-basis chart one takes
`vartheta_i=sqrt(det g_a(q_i))`; on overlaps the unimodular change of basis
makes this definition independent of the chosen record.  Multiplying the
force by any other uniformly comparable positive stored volume would not
change its zero, but this particular choice is what identifies its
linearization with the round Jacobi operator below.

The same paired expansion gives

\[
 \sum_jc_{ij}P_{y_i}(y_j-y_i)(y_j-y_i)^TP_{y_i}
   =tau_i h^nP_{y_i}+O(C_Mh^{n+2}),                \tag{4.4}
\]

with `0<tau_-<=tau_i<=tau_+`.  Also

\[
 {1\over n}\sum_jc_{ij}(1-y_i\cdot y_j)
       ={tau_i\over2}h^n+O(C_Mh^{n+2}).            \tag{4.5}
\]

These are pointwise estimates, including minimum-tie strata.

## 5. Uniform inverse and absence of interface modes

Let `J` be the continuum Jacobi operator of the identity sphere map and
`J_h` the derivative of the normalized tangent force in (4.3).  Restrict to
`W`-equivariant tangent fields.  The only continuum Jacobi kernel consists
of rotations (and, on `S^2`, the conformal translation fields); the
commutant and fixed-vector calculations for the standard `S_(d+1)`
representation remove both.  Hence

\[
 ||u||_{C^{2,alpha}}\le C_cont||Ju||_{C^{0,alpha}}.\tag{5.1}
\]

Here is the discrete transfer, including the interface issue.  In a repaired
chart, (1.4) has one node per lattice cell, so its frozen scalar symbol is

\[
 p_q(xi)=4\sum_v b_v(q)\sin^2(xi\cdot v/2).        \tag{5.2}
\]

By (3.7), (5.2) has exactly one acoustic zero and no optical sector.  In the
`2+3` case, `r=0` is a lattice hyperplane and (5.2) is the same symbol on and
across it.  Thus no surface matrix, and hence no surface eigenbranch, exists.
On overlaps, the transition is affine unimodular; all contributing symbols
can therefore be written on one lattice and their nonnegative sum still
satisfies (3.7).

Dyadic Fourier inversion gives the frozen estimate

\[
 ||u||_{2,alpha,h;Q/2}\le C_F
       (||J_hu||_{0,alpha,h;Q}+||u||_{0;Q}),       \tag{5.3}
\]

with the explicit geometric-series bound

\[
 C_F=2^{n+8}(1+R C_basis)^{n+6}
     (1+Lambda_*)^3c_0^{-3}(1-2^{-alpha})^{-1}.    \tag{5.4}
\]

Freeze on a rational radius

\[
 r_0\le c_0/[16C_F(1+||rho||_{C^1}+K_2)]          \tag{5.5}
\]

and absorb coefficient variation.  A finite-overlap partition gives the
global estimate with a `C^0` term.  Use the uniformly shape-regular
triangulation of the product lattices (the finitely many cone images are
enumerated), average its nodal interpolant over `W`, and call the resulting
extension `E_h`.  On equivariant data,

\[
 S_hE_h=I,\qquad ||E_hf||_{C^{0,alpha}}
                  \le C_E||f||_{0,alpha,h}.        \tag{5.6}
\]

Taylor expansion of the linearized flux gives

\[
 ||J_hS_hu-S_hJu||_{0,alpha,h}
      \le C_j h^alpha||u||_{C^{2,alpha}}.          \tag{5.7}
\]

Consequently `Q_h=S_hJ^{-1}E_h` satisfies

\[
 ||J_hQ_h-I||\le C_jC_contC_Eh^alpha.              \tag{5.8}
\]

For

\[
 h\le h_J=(2C_jC_contC_E)^{-1/alpha},              \tag{5.9}
\]

the Neumann series is the inverse and

\[
 ||J_h^{-1}f||_{2,alpha,h}\le2C_contC_E||f||_{0,alpha,h}.\tag{5.10}
\]

Equations (5.2)--(5.10) are also a direct no-surface-mode proof: a putative
bounded-frequency interface mode would contradict (5.8), while a lattice-
frequency mode is excluded by (3.7).  No unproved interface Schauder or Korn
lemma is being assumed.

## 6. Exact harmonic correction and generator

Let

\[
 x_i=exp_{y_i}u_i.
\]

The inverse (5.10), the residual (4.3), and the explicit second derivative
bound for the sphere exponential give a Newton contraction on

\[
 ||u||_{2,alpha,h}\le C_u h^2,
 \qquad C_u=4C_contC_EC_T',                         \tag{6.1}
\]

after imposing

\[
 h\le h_N=\min\{h_at,h_J,(8C_NC_u)^{-1/2}\}.       \tag{6.2}
\]

The unique equivariant fixed point satisfies exactly

\[
 P_{x_i}\sum_jc_{ij}(x_j-x_i)=0,                  \tag{6.3}
\]

and

\[
 |x_i-y_i|\le C_uh^2,
 \qquad |(x_j-y_j)-(x_i-y_i)|\le C_uQ_*h^3.        \tag{6.4}
\]

Define

\[
 mu_i={1\over n}\sum_jc_{ij}(1-x_i\cdot x_j),
 \quad W_h=\sum_i mu_i,
 \quad w_i={mu_i\over W_h},
 \quad gamma_{ij}={c_{ij}\over W_h},
 \quad a_{ij}={c_{ij}\over mu_i}.                 \tag{6.5}
\]

Then, exactly,

\[
 L_h1=0,\qquad L_hOmega=-nOmega,\qquad
 w_ia_{ij}=w_ja_{ji}=gamma_{ij}\ge0.               \tag{6.6}
\]

Equations (4.4)--(4.5) and (6.4) imply

\[
 c_mu h^n\le mu_i\le C_mu h^n,
 \qquad r_i=\sum_ja_{ij}\le R_dh^{-2},             \tag{6.7}
\]

and the unnormalized quadratic row satisfies

\[
 \left\|\sum_jc_{ij}\left[(x_j-x_i)(x_j-x_i)^T
 -{2(1-x_i\cdot x_j)\over n}P_{x_i}\right]\right\|_F
 \le C_Qh^{n+2}.                                   \tag{6.8}
\]

Thus every normalized row residual is at most `(C_Q/c_mu)h^2`.

Finally, the weights in (6.5) are comparable with `h^n`, the corrected nodes
remain quasiuniform by (6.4), and the cell Riemann-sum estimate gives, for
`h<=h_S`,

\[
 \sum_iw_i\langle Q,x_ix_i^T-I/d\rangle^2
 \ge c_S||Q||_F^2\quad(Q\in Sym_0(\mathbb R^d)),  \tag{6.9}
\]

where `c_S` is one half of the exact continuum spherical moment constant.
Combining (6.8)--(6.9) yields

\[
 \mathfrak D_2(L_h)\le C_dh^2.                    \tag{6.10}
\]

Together with the P1B frontier and (6.7),

\[
 {d(d-1)\over R_d}h^2
 \le\inf_{L\in\mathcal G_h(R_d)}\mathfrak D_2(L)
 \le C_dh^2.                                      \tag{6.11}
\]

All constants in (6.7)--(6.11) are displayed algebraic combinations of the
finite atlas bounds, `R`, the cone margin, and the geometric series in
(5.4).  They do not depend on `N`.

## 7. Robustness

Perturb the uncorrected nodes in chart coordinates by at most `eps h^3` in
discrete `C^{2,alpha}` and perturb the coefficient functions by at most
`eps` in `C^{3,alpha}`.  If

\[
 eps\le\min\{rho_*/4,\ c_0/(8C_F),\ q_*/(8C_u)\}, \tag{7.1}
\]

the same edge list, local cone margin, inverse, Newton ball, mesh bounds,
and estimates (6.7)--(6.10) remain valid with every upper constant doubled
and every lower constant halved.  This is the strict local/global feasibility
margin required by the construction.

## 8. Audit conclusion

The raw formula `q=P_Zlambda_Z, r=P_Blambda_B` must not be used as a periodic
crystal chart.  The repaired formula (1.1) is exact and eliminates the local
residue rather than approximating it.  Within one buffered record the basis
count is one, so basis connectors are unnecessary there.  They cannot,
however, be deleted from a *global* construction until the unavoidable atlas
interfaces described next have been supplied with a separate, proved
multi-sheet or interface mechanism.

## 9. Why the conditional global atlas is impossible

The issue is not a poor choice of collar constants.  It is a topological
obstruction.

### Proposition 2 (dense-grid transitions are affine)

Let `U,V` be connected open subsets of `R^n`, and let
`Phi:U->V` be `C^2`.  Suppose that for a sequence `h_l -> 0`, every lattice
point `x in h_l Z^n` whose `3h_l` coordinate neighborhood is contained in
`U` is sent to `h_l Z^n`, and the same holds for `Phi^{-1}`.  Then `Phi` is
the restriction of an affine map with linear part in `GL(n,Z)`.

**Proof.**  For every coordinate direction `e_a`, the centered second
difference

\[
 D^2_{h,a}\Phi(x)=\Phi(x+he_a)-2\Phi(x)+\Phi(x-he_a)
\]

belongs to `h Z^n`.  On a compact subset, Taylor's theorem bounds its norm by
`C h^2`.  For `h<1/C`, the only element of `h Z^n` with that norm is zero.
The grid points are dense, so `partial_a^2 Phi=0`.  Applying the same argument
to the mixed parallelogram difference gives
`partial_a partial_b Phi=0`.  Hence `DPhi` is constant.  First differences
show that its columns are integral; applying the conclusion to `Phi^{-1}`
shows that the matrix is unimodular.  QED.

The same conclusion holds for fixed full-rank lattices after conjugating by
their basis matrices.  A finite residue basis does not remove the
obstruction if overlap ownership preserves basis labels: pass to a common
finite-index period lattice first.

### Proposition 3 (no smooth one-point lattice atlas on a sphere)

For `n>=2`, no smooth atlas of `S^n` can have all nonempty connected overlap
maps affine as in Proposition 2.

**Proof.**  Such transitions define an affine structure.  Since `S^n` is
simply connected, analytic continuation of one chart produces a global
developing map `dev:S^n->R^n` which is a local diffeomorphism.  A local
diffeomorphism is open, while the image of compact `S^n` is compact.  No
nonempty subset of `R^n` is both open and compact.  QED.

Therefore the four assertions used together in the conditional Sections
2--7 -- same physical nodes on overlaps, exact one-point lattices at every
level, smooth coefficient/embedding transitions, and affine-unimodular
overlap maps -- cannot all hold.  The residue-unwinding chart proves that the
specific `|t|` residue is not the fundamental obstacle; it moves the
remaining obstruction to the overlap of the stratified charts.

A complete P1E repair must now add one of the following concrete mechanisms:

1. an augmented multi-sheet node set with explicit positive, moment-cancelled
   transition connectors and a proved interface symbol with no surface mode;
2. an explicit finite set of singular interface templates whose shared edge
   coefficients solve the first-, second-, and third-moment equations with a
   uniform positive margin, followed by a direct interface Green/Schauder
   estimate; or
3. a different exact-H1 construction (for example geometric spherical
   weights) for which pointwise quadratic isotropy is proved at every
   singular template.

None of these mechanisms is supplied by Lemma 1, and none may be replaced by
a finite-size spectral check.
