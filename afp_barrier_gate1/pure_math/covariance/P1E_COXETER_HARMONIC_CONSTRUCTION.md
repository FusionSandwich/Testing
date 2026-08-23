# P1E Coxeter--harmonic construction

## Status: BLOCKED compiler route; conditional theorem only

This note records a conditional all-dimensional construction route which does not infer a
shared stress from independently feasible rows.  The graph and its positive
shared energy are fixed first.  A small, equivariant constrained-harmonic
correction of the node embedding then makes the coordinate rows exactly
radial.  The correction is obtained from a second-order elliptic Jacobi
operator, not from the fourth-order edge-stress/elasticity operator in the
blocked structured-stress route.

The four-point connector lemma, the harmonic correction, and all estimates
following a genuine finite-crystal compiler are valid.  The proposed raw
realization by \(K_N\), however, is not a periodic crystal at a mixed
parabolic stratum; Section 2.1 gives an exact counterexample.  Therefore this
file is **not** an affirmative P1E construction unless a globally compatible
full-affine-lattice completion or an explicit reflected interface compiler is
inserted.  No later conditional estimate is to be read as supplying that
missing premise.

The circle is elementary and is disposed of first.  If \(d=2\), put
\(s=2\pi/N\), \(N\geq5\), and

\[
 x_k=(\cos ks,\sin ks),\qquad c_{k,k+1}=c_{k+1,k}=1 .
\]

With \(h=s\) and \(\ell=1-\cos s\), (1.2) below gives, exactly,

\[
 w_k={1\over N},\qquad \gamma_{k,k+1}={1\over2N\ell},
 \qquad a_{k,k\pm1}={1\over2\ell},\qquad r_k={1\over\ell}.
\]

Thus \(L1=0\), and the Fourier modes of degrees one and two have eigenvalues
\(-1\) and \(-2(1+\cos s)\), respectively.  Consequently

\[
 L\Omega=-\Omega,\qquad
 \mathfrak D _2=2(1-\cos s),\qquad
 \mathfrak D _2r_k=2=d(d-1).                    \tag{0.1}
\]

In particular \(r_k\leq(\pi ^2/2)h^{-2}\) and
\(\mathfrak D _2\leq h^2\).  This is already an explicit all-level family,
so the vector-harmonic discussion below is not needed in dimension one.
For the conditional higher-dimensional route, put

\[
 n=d-1,\qquad d\geq3.
\]

Let \(W=S_{d+1}\) act by permuting the vertices of a regular
\(d\)-simplex.  Its standard real representation is the irreducible
\(d\)-dimensional space

\[
 H=\{z\in\mathbb R^{d+1}:\textstyle\sum_a z_a=0\}.
\]

The unit sphere in \(H\) is identified with \(S^{d-1}\).

The constants below are *compiler constants*: they are maxima, minima, and
finite direction sums associated with a fixed finite atlas constructed once
for \(d\).  The individual smoothing, connector, and tensor-cone records in
Section 2 are terminating rational/interval constructions.  Their constants
are effective and independent of the level \(N\).  The missing global
crystal/interface premise is not included among those certified constants.

## 1. Exact finite algebra

For a finite graph with shared coefficients \(c_{ij}=c_{ji}\geq0\), positive
compiler volumes \(\vartheta_i\), and unit nodes \(x_i\), put

\[
 \mathcal T_h(x)_i
 ={h^{-n}\over\vartheta_i}P_{x_i}\sum_jc_{ij}(x_j-x_i),
 \qquad P_x=I-xx^T.                                      \tag{1.1}
\]

The positive factor \(\vartheta_i\) does not change the zero set.  If
\(\mathcal T_h(x)=0\), define

\[
 \mu_i={1\over n}\sum_jc_{ij}(1-x_i\cdot x_j),\qquad
 W_h=\sum_i\mu_i,
\]

\[
 w_i={\mu_i\over W_h},\qquad
 \gamma_{ij}={c_{ij}\over W_h},\qquad
 a_{ij}={c_{ij}\over\mu_i}.                         \tag{1.2}
\]

Then, exactly,

\[
 \sum_jc_{ij}(x_j-x_i)=-n\mu_ix_i,                 \tag{1.3}
\]

and hence

\[
 L_h1=0,\qquad L_hx=-nx,\qquad
 w_ia_{ij}=w_ja_{ji}=\gamma_{ij}.                  \tag{1.4}
\]

The unnormalized quadratic row is

\[
 \widehat M_i(x)=
 \sum_jc_{ij}\left[(x_j-x_i)(x_j-x_i)^T
 -{2(1-x_i\cdot x_j)\over n}P_{x_i}\right],       \tag{1.5}
\]

and the P1A row representer is \(M_i=\widehat M_i/\mu_i\).

Thus the construction problem is reduced to producing a positive shared
energy, an exact zero of (1.1), and the estimates

\[
 \mu_i\asymp h^n,\qquad
 \|\widehat M_i\|_F=O(h^{n+2}).                   \tag{1.6}
\]

## 2. The finite Coxeter mesh--energy compiler

### 2.1 The actual parabolic lattice catalogue

Let

\[
 K_N=\left\{N^{-1}k:k\in\mathbb Z_{\geq0}^{d+1},\quad
       \sum_ak_a=N,\quad\min_ak_a=0\right\}.       \tag{2.1}
\]

This is the edgewise lattice on the boundary of the standard \(d\)-simplex.
It is a genuine simplicial \((d-1)\)-sphere and is \(W\)-invariant.  It
replaces the topologically false assertion that a codimension-\(r\) stratum
has \(2^r\) cubical sectors.

For a nonempty block \(Z\subset\{0,\ldots,d\}\), put \(B=Z^c\), and let
\(P_Z,P_B\) denote subtraction of the coordinate mean on the indicated
block.  On a neighborhood in which the coordinates in \(B\) stay positive,
define the centered-block chart

\[
 \Phi_Z(\lambda)=(P_Z\lambda_Z,P_B\lambda_B)
 \in H_Z\oplus H_B.                                \tag{2.2}
\]

Here the representative of the first quotient is fixed by
\(\min_{a\in Z}\lambda_a=0\); the total-sum equation then fixes the common
part of \(\lambda_B\).  Explicitly, for \(q\in H_Z,r\in H_B\),

\[
 c=-\min_{a\in Z}q_a,\qquad
 \lambda_Z=q+c1_Z,
\]

\[
 b={1-|Z|c\over |B|},\qquad
 \lambda_B=r+b1_B.                                 \tag{2.3}
\]

Equations (2.2)--(2.3) are inverse wherever \(b+\min_Br>0\).
The tempting claim that the image of \(K_N\) is a periodic multilattice is
false.  Here is an exact obstruction.  Take \(d=4\), \(|Z|=2\), and
\(|B|=3\).  Write

\[
 a=k_1-k_2,\qquad p=k_3-k_5,\qquad q=k_4-k_5 .
\]

The minimum-zero representative in \(Z\) has block sum \(|a|\).  Solving
for the three integer \(B\)-coordinates with total sum \(N-|a|\) is
equivalent to

\[
                 p+q+|a|\equiv N\pmod3.           \tag{2.4}
\]

This set has no full-rank period lattice.  Indeed, if
\((A,P,Q)\) were a period, then for every integer \(a\)

\[
 P+Q+|a+A|-|a|\equiv0\pmod3.                      \tag{2.4a}
\]

For sufficiently positive and negative \(a\), this first forces
\(A\equiv0\) and \(P+Q\equiv0\pmod3\).  If \(A\ne0\), choosing consecutive
\(a\) in the interval crossing \(0\) makes
\(|a+A|-|a|=A+2a\), which is not constant modulo \(3\).  Hence every period
has \(A=0\), so the period group cannot have rank three.  A finite union of
cosets of a full-rank lattice would inherit that lattice as a period group,
and is therefore impossible.

Projecting the *full* zero-sum integer lattice does give one lattice.
Applying the boundary section (2.3) to all its points fills the missing
residues, with denominators dividing \(|B|\).  Locally this is the correct
repair, and the common denominator is bounded by \((d+1)!\).  What has not
been supplied is a global node set which uses those completions in all
overlapping stratum charts while retaining separation, shared nodes,
reflection-compatible interface stencils, and the uniform inverse in
Section 4.  Local completion does not prove global reversible
reconciliation.

Accordingly, Sections 2.2--8 are conditional on the following explicit
compiler premise:

> There is a \(W\)-invariant, quasiuniform node family whose enlarged
> stratum records are genuine finite periodic crystals, with a uniformly
> bounded basis and period directions, and whose overlap identifications
> carry the same shared undirected edges and midpoint coefficients.

The strong connector below solves the basis coupling once this premise
holds; it does not prove the premise.

### 2.2 Explicit smoothing of the simplex sphere

The charts (2.2) give the standard unfolded charts of the PL sphere
\(\partial\Delta^d\).  The following relative Hermite recursion makes the
smoothing, including overlap compatibility, a finite construction.

1. Barycentrically subdivide once.  A closed collar record is indexed by a
   flag of proper faces.  In such a record, the variables are the stratum
   coordinate \(r\) and one centered-block normal variable for each member
   of the flag.  Intersections of records are coordinate faces of these
   boxes.  This is immediate from (2.3), and gives a finite system of
   compatible product collars.  Order the records by decreasing flag
   length, so that every overlap already treated at a stage is a union of
   coordinate faces.
2. Let \({\cal H}_6\) be the tensor product of the one-dimensional Hermite
   right inverse for endpoint derivatives of orders \(0,\ldots,6\).
   Its coefficients are obtained by inversion of a fixed triangular integer
   matrix with diagonal entries \(1\); hence they are rational and
   algorithmically exact.  On a new record, the jets prescribed on its
   already-treated coordinate faces are compatible on every intersection
   because they are restrictions of the single map constructed at the
   preceding stages.  Apply \({\cal H}_6\), setting the unconstrained
   interior coefficients to zero.  This gives a canonical polynomial jet
   extension; no assertion of a nonexistent “unique jet coefficient” is
   used.
3. In a target normal chart, set on the core
   \[
   F_Z(q,r)=\exp_{F_Z(0,r)}
       \left(A_Z(r)q+\sum_{2\leq |\alpha|\leq7}
                         A_{Z,\alpha}(r)q^\alpha\right).       \tag{2.5}
   \]
   The oriented normal frame \(A_Z\) is obtained by lexicographic
   Gram--Schmidt from the regular-simplex vectors, and the remaining
   coefficients are those returned by \({\cal H}_6\).  Average the input
   jet record over the stabilizer of \(Z\) *before* applying
   \({\cal H}_6\), then copy it over its \(W\)-orbit.  Since the Hermite
   operator commutes with coordinate permutations, this produces an
   equivariant record without averaging maps or risking loss of rank.
4. Join the core to the map already defined outside the collar, in the same
   target normal chart, using
   \[
   \begin{split}
   \beta_6(t)={}&1716t^7-9009t^8+20020t^9-24024t^{10}\\
                &+16380t^{11}-6006t^{12}+924t^{13}.
   \end{split}                                      \tag{2.6}
   \]
   This is
   \(B(7,7)^{-1}\int_0^t s^6(1-s)^6\,ds\); its derivatives of orders
   \(1,\ldots,6\) vanish at both endpoints.  Thus the joined records agree
   through order six on every overlap.
5. Choose each new collar width \(\eta_Z\) smaller than one eighth of every
   earlier width.  At its core, the columns consisting of the already
   constructed stratum derivative and the frame \(A_Z\) are independent
   with the prescribed orientation.  Hence the Gram determinant is
   positive there.  Continuity supplies a collar on which it remains
   positive.  Local injectivity on incident records follows from the
   quantitative inverse theorem on the product box.  Nonincident closed
   records had positive image separation before this stage; a sufficiently
   small relative modification preserves half that separation.  These two
   facts are the relative-isotopy induction: the new map is an embedding,
   agrees with the old one off the collar, and does not alter an earlier
   overlap.
6. All derivative determinants, inverse-function radii, and nonincident
   separations in the preceding step are polynomial/rational interval
   expressions on finitely many fixed boxes.  Bisect a rational
   \(\eta_Z\) until interval evaluation certifies
   \[
       \det(DF_Z^TDF_Z)\geq j_-^2>0               \tag{2.7}
   \]
   and the required half-separation inequalities.  The strict core
   inequalities and continuity prove that bisection terminates.  There are
   finitely many flag orbits, so the recursion terminates.

This produces a fixed \(W\)-equivariant \(C^6\) diffeomorphism

\[
 F:M_d\longrightarrow S(H),                       \tag{2.8}
\]

where \(M_d\) is the explicitly smoothed simplex boundary.  It also produces
rational interval bounds

\[
 0<j_-\leq s_{\min}(DF)\leq s_{\max}(DF)\leq j_+,
 \qquad
 K_r\geq\|D^rF\|_\infty+\|D^rF^{-1}\|_\infty
 \quad(1\leq r\leq6).                              \tag{2.9}
\]

The physical reference nodes are

\[
 y_i=F(k_i/N),\qquad k_i/N\in K_N,\qquad h=N^{-1}. \tag{2.10}
\]

The lattice and singular-value bounds give explicit constants
\(q_0,H_0,N_+,D_{\rm pack}\) such that

\[
 \operatorname{fill}(Y_h)\leq H_0h,\qquad
 \operatorname{sep}(Y_h)\geq q_0h,\qquad
 |Y_h|\leq N_+h^{-n}.                              \tag{2.11}
\]

### 2.3 A fixed positive midpoint energy

Put \(g=F^*g_{S^n}\).  Choose a finite, \(W\)-closed atlas from the collars
above and a rational polynomial partition of unity \(\chi_a\), with support
a fixed positive distance from the enlarged chart boundary.  Fix one
owner record at each node and put

\[
 \vartheta_i=\sqrt{\det g_{\rm own}(q_i)} .
\]

When a contribution is written in a non-owner chart, transport its
contravariant tensor density and its lattice directions to the owner chart
before adding it.  In chart \(a\) set

\[
 A_a=\chi_a\sqrt{\det g_a}\,g_a^{-1}.             \tag{2.12}
\]

The finite derivative bounds give

\[
 0<\vartheta_-\leq\vartheta_i\leq\vartheta_+.       \tag{2.12a}
\]

The tensor-density change-of-coordinates rule and
\(\sum_a\chi_a=1\) give, in owner coordinates,

\[
 \sum_a A_a=\vartheta_i\,g_{\rm own}^{-1}.          \tag{2.12b}
\]

This identity is why division by \(\vartheta_i\) below produces
\(\Delta_g\), rather than an unspecified positive multiple of it.  There is one
normalization trap here.  A periodic crystal can have more than one basis
point.  Connecting those basis points with weights of size \(h^n\) would give
only an order-one optical gap after division by the nodal volume.  Such a gap
does **not** control a discrete second derivative across an edge of length
\(h\).  The following explicit positive connector removes that trap.

#### The four-point odd-moment connector

Let a crystal record have period lattice \(B\mathbb Z^n\), basis
\(b_1,\ldots,b_Q\), and let \(T\) be a spanning tree of the basis labels.
If \(\Gamma_a\) is the finite stabilizer of the record, replace \(T\) by
the weighted union of all \(\Gamma_a\)-translates of \(T\), each with weight
\(|\Gamma_a|^{-1}\).  This makes the connector record equivariant.  The
original tree remains in that union with all its weights at least
\(|\Gamma_a|^{-1}\) times their displayed values.  Put

\[
 G_*=\max_a|\Gamma_a|\leq(d+1)! .                 \tag{2.12c}
\]

It is therefore enough to construct the law for one oriented edge of \(T\).
For an oriented tree edge \(t=(\alpha,\beta)\), write

\[
 B^{-1}(b_\beta-b_\alpha)=\theta+k_0,
 \qquad -\tfrac12\leq\theta_s<\tfrac12,
 \qquad k_0\in\mathbb Z^n.                        \tag{2.13}
\]

The integer \(k_0\) is absorbed into the translation label.  The following
one-dimensional construction is applied independently to every coordinate
\(\theta_s\).  Put \(R=2\) and

\[
 a_1=R-\theta_s,\quad a_2=R+2-\theta_s,
 \qquad c_1=R+\theta_s,\quad c_2=R+2+\theta_s.
\]

The squared intervals \([a_1^2,a_2^2]\) and \([c_1^2,c_2^2]\) overlap with
the explicit strict margin

\[
 U-L\geq(R+\tfrac32)^2-(R+\tfrac12)^2=6,
 \quad L=\max(a_1^2,c_1^2),\quad
 U=\min(a_2^2,c_2^2).                              \tag{2.13a}
\]

Set \(m=(L+U)/2\), and, for \(s=a,c\), set

\[
 \lambda_{s,1}={s_2^2-m\over s_2^2-s_1^2},
 \qquad
 \lambda_{s,2}={m-s_1^2\over s_2^2-s_1^2}.        \tag{2.13b}
\]

Both coefficients are positive and sum to one.  Give the four points
\(-a_1,-a_2,c_1,c_2\), all belonging to \(\theta_s+\mathbb Z\), raw masses

\[
 {\lambda_{a,1}\over a_1},\quad
 {\lambda_{a,2}\over a_2},\quad
 {\lambda_{c,1}\over c_1},\quad
 {\lambda_{c,2}\over c_2},                       \tag{2.13c}
\]

and normalize their sum to one.  Denote the resulting law by \(p_s\).  By
construction,

\[
 \mathbb E_{p_s}z=0,\qquad \mathbb E_{p_s}z^3=0.  \tag{2.13d}
\]

This is also a quantitative strict-positive formula, not just an existence
argument.  Since \(3/2\leq a_i,c_i\leq9/2\), the denominators in (2.13b)
are at most \(14\), and (2.13a) gives

\[
 \lambda_{s,r}\geq {3\over14},\qquad
 p_s(z)\geq {1\over56},\qquad
 {9\over4}\leq\mathbb E_{p_s}z^2\leq{81\over4}. \tag{2.13e}
\]

Take the product of these \(n\) laws and push it forward by \(B\).  Its
finite support consists of displacements

\[
 z=B(\theta+k)=b_\beta-b_\alpha+B(k-k_0),
 \qquad k\in\mathbb Z^n,                          \tag{2.13f}
\]

with probabilities \(p_{t,k}>0\).  Independence and (2.13d) give the exact
tensor identities

\[
 \sum_kp_{t,k}z=0,\qquad
 \sum_kp_{t,k}z^{\otimes3}=0,\qquad
 Q_t:={1\over2}\sum_kp_{t,k}zz^T>0.              \tag{2.13g}
\]

Moreover, with \(\sigma_-(B),\|B\|\) denoting the extreme singular values,

\[
 p_{t,k}\geq p_*:=56^{-n},\qquad
 Q_t\geq {9\over8}\sigma_-(B)^2I,\qquad
 \|Q_t\|\leq {81\over8}\|B\|^2,
 \qquad |z|\leq {9\over2}\sqrt n\,\|B\|.        \tag{2.13h}
\]

For every period cell \(m\), connect \((m,\alpha)\) to
\((m+k-k_0,\beta)\) for the \(4^n\) support values.  At a \(\beta\)-row the
same undirected edges have displacement \(-z\), so (2.13g) holds there too.
Thus shared reversal, zero first moment, and zero third moment are all exact.
The tree makes the basis graph connected.

#### Subtract the connector tensor before the rank-one solve

Put \(G_a=\sqrt{\det g_a}\,g_a^{-1}\), and let \(Q_\alpha\) be the sum of
the tensors \(Q_t\), including the weights \(|\Gamma_a|^{-1}\), over all
translated tree edges incident to \(\alpha\).  All records are finite, so the compiler
has rational interval bounds

\[
 g_-I\leq G_a\leq g_+I,\qquad
 Q_*:=\max_\alpha\|Q_\alpha\|,\qquad
 S_*:=\left\|\sum_{r=1}^n(B e_r)(B e_r)^T\right\|. \tag{2.14}
\]

After taking the extrema over the finite transported chart catalogue, write
\(\lambda_*=g_-\) and \(\Lambda_*=g_+\) for the aggregate lower and upper
principal-tensor bounds.

Choose rational numbers

\[
 0<\varepsilon\leq {g_-\over4Q_*},
 \qquad 0<\rho_0\leq {g_-\over4S_*}.              \tag{2.14a}
\]

(When \(Q=1\), put \(Q_*=0\) and omit \(\varepsilon\).)  At basis label
\(\alpha\), first subtract the connector tensor and a period-direction
floor:

\[
 H_{a,\alpha}(q)=G_a(q)-\varepsilon Q_\alpha
              -\rho_0\sum_{r=1}^n(B e_r)(B e_r)^T
 \geq {g_-\over2}I.                              \tag{2.14b}
\]

The coefficient selection in the rank-one solve must be smooth; choosing a
new eigenbasis pointwise would not suffice.  Use the following finite
selection.  At a center \(H_\nu\), subtract a small multiple of a fixed
period-lattice rank-one frame spanning \(\operatorname{Sym}(n)\), then
approximate an eigenframe of the remaining positive matrix by period-lattice
directions.  The combined rank-one matrices span
\(\operatorname{Sym}(n)\), and the synthesis equation at \(H_\nu\) has a
solution \(c_\nu\) all of whose entries are strictly positive.  Fix a
rationally interval-certified right inverse \(R_\nu\) of that synthesis
map and set
\[
 c_\nu(H)=c_\nu+R_\nu(H-H_\nu).
\]
On a sufficiently small rational matrix ball this remains positive and
represents \(H\) exactly.  Cover the compact range of (2.14b) by finitely
many such balls and take a nonnegative \(C^5\) partition of unity
\(\psi_\nu(H)\) subordinate to them.  A normalized polynomial-bump formula
gives explicit derivative bounds.  Multiplying the local representations by
\(\psi_\nu\) and summing gives

\[
 H_{a,\alpha}(q)=\sum_{v\in V^+_{a,\alpha}}
                  \rho_{a,\alpha,v}(q)vv^T,
 \qquad \rho_{a,\alpha,v}\geq0.                  \tag{2.14c}
\]

Here \(V^+_{a,\alpha}\) contains exactly one representative of each
unoriented pair \(\{v,-v\}\).  For every listed \(v\), the graph contains
both edges \(+v\) and \(-v\), with the same midpoint coefficient.  Thus a
single term \(\rho vv^T\) in (2.14c), not \(2\rho vv^T\), is its Hessian
tensor.  Add back the explicit coefficient \(\rho_0\) on each pair
\(\pm Be_r\).  Finally,
give a tree-connector displacement (2.13f) the midpoint coefficient

\[
 c^{a,t,k}_{ij}=h^{n-2}\varepsilon\,
                  \chi_a(q_{ij})p_{t,k}.          \tag{2.14d}
\]

and each of the two same-basis displacements \(\pm v\), for
\(v\in V^+_{a,\alpha}\cup\{Be_1,\ldots,Be_n\}\), the coefficient

\[
 c^{a,\alpha,v}_{ij}=h^{n-2}\chi_a(q_{ij})
       \bigl(\rho_0 1_{v\in\{Be_r:1\leq r\leq n\}}
                         +\rho_{a,\alpha,v}(q_{ij})\bigr). \tag{2.14e}
\]

In (2.14e), \(\rho_{a,\alpha,v}=0\) when
\(v\notin V^+_{a,\alpha}\).

Here \(q_{ij}\) is the common edge midpoint in the owner chart.  Equations
(2.13g) and (2.14b)--(2.14e) say that the frozen first and third moments
vanish and that the frozen second moment is exactly \(A_a(q)\), at **every**
basis label.  All directions have \(|v|\leq s_*\), and all coefficient
derivatives through order five have a certified bound \(K_\rho\).  The
rational matrix net terminates because (2.14b) stays a fixed positive
distance from the boundary of the positive-definite cone.  Tensor densities
are transported before this solve and are combined with the single global
partition of unity; independently chosen endpoint coefficients are never
averaged.

There is also an elementary, non-numerical optical gap.  Retain one support
edge of weight at least \(p_*\) for every tree edge and gauge away its Bloch
phase along the tree.  The period-direction floor gives

\[
 E_{\rm per}(\xi,U)\geq4\rho_0\chi_a
   \sum_{\alpha,r}\sin^2(\xi_r/2)|U_\alpha|^2,
\]

while the selected connectors give

\[
 E_{\rm opt}(\xi,U)\geq
 {\varepsilon\chi_a p_*\over G_*}\lambda_T
       \sum_\alpha|U_\alpha-\bar U|^2,
 \quad
 \lambda_T\geq2(1-\cos(\pi/Q))\geq4/Q^2.        \tag{2.14f}
\]

Thus the acoustic branch is quadratic and every optical branch has a
strict positive frozen-symbol gap.  After multiplication by \(h^{-2}\),
**both** have the scale required by the discrete Schauder estimate.  Since
\(\sum_a\chi_a=1\), some chart has \(\chi_a\geq N_{\rm ov}^{-1}\) at every
point.  Hence a global admissible symbol constant is

\[
 c_{\rm sym}={1\over N_{\rm ov}}\min\left\{
 {4\rho_0\over\pi^2},
 {4\varepsilon p_*\over G_*Q_{\rm bas}^2}\right\}>0, \tag{2.14g}
\]

where \(Q_{\rm bas}\) is the maximum basis count of a crystal record.  This
is distinct from the tensor bound \(Q_*\) in (2.14).

Contributions (2.14d)--(2.14e) naming the same undirected edge are summed.
The cutoff support
ensures that both endpoints are present for all \(h\leq h_{\rm atlas}\).
The result is a fixed-support-radius, \(W\)-invariant, shared energy
\(c_{ij}=c_{ji}\geq0\).  It has

\[
 \deg(i)\leq D_*,\qquad
 q_0h\leq d_S(y_i,y_j)\leq\Lambda_0h              \tag{2.16}
\]

on active edges.  Individual partition contributions may vanish at a chart
boundary; the strict local margin is the aggregate metric lower bound, the
period floor, and the acoustic/optical symbol bound (2.14g).  The
strict global margin is the Jacobi gap in Section 4.  No lower bound on a
coefficient which has been declared inactive is asserted.

### 2.4 Pointwise second-order consistency

For one paired direction, Taylor's formula at the midpoint gives

\[
\begin{aligned}
&\rho(q+hv/2)[f(q+hv)-f(q)]\\
&\quad+\rho(q-hv/2)[f(q-hv)-f(q)]\\
&=h^2\partial_v(\rho\partial_vf)(q)
 +h^4\left({\rho f^{(4)}\over12}
 +{\rho'f^{(3)}\over6}+{\rho''f''\over8}
 +{\rho'''f'\over24}\right)+\mathcal R_6.       \tag{2.17}
\end{aligned}
\]

The integral remainder obeys

\[
 |\mathcal R_6|\leq {h^6|v|^6\over360}
 \max_{0\leq r\leq5}\|D^r\rho\|_\infty
 \max_{1\leq r\leq6}\|D^rf\|_\infty.            \tag{2.18}
\]

For a tree connector, expand the midpoint coefficient and the forward
difference simultaneously.  With \(z\) distributed according to
\(p_{t,k}\), the terms of total degrees one and three are respectively
multiples of \(\mathbb Ez\) and \(\mathbb Ez^{\otimes3}\), so they vanish
**exactly** by (2.13g).  The degree-two term is

\[
 h^2\operatorname{div}\bigl(\varepsilon\chi_aQ_t\nabla f\bigr). \tag{2.18a}
\]

This is precisely the tensor subtracted in (2.14b).  Every uncancelled term
has degree at least four.  Therefore the connector, despite having the full
acoustic size \(h^{n-2}\), has normalized truncation error \(O(h^2)\), not
\(O(h)\).  Put

\[
 Z_4=4^n\left({9\over2}\sqrt n\max_a\|B_a\|\right)^4,
 \qquad
 C_{\rm con}^{\rm tree}=16D_*\varepsilon
       (1+K_\rho)(1+K_6)^4Z_4.                   \tag{2.18b}
\]

Taylor's integral remainder gives the deliberately loose bound
\(C_{\rm con}^{\rm tree}h^2\|f\|_{C^4}\) after normalization.  This is the
cutoff audit: endpoint averaging would not have the same midpoint expansion,
and omitting the cubic identity in (2.13g) would leave an order-\(h\) term.

Summing (2.17), using (2.12)--(2.13), and then dividing by
\(h^n\vartheta_i\), proves

\[
 \left|{h^{-n}\over\vartheta_i}\sum_jc_{ij}(f_j-f_i)
             -\Delta_gf(y_i)\right|
 \leq C_{\rm con}h^2\|f\|_{C^6},                 \tag{2.19}
\]

and the same estimate in the discrete \(C^{0,\alpha}_h\) norm.  One
admissible explicit compiler value is

\[
 C_{\rm con}=\vartheta_-^{-1}\left[
 8D_*\Lambda_* (1+K_\rho)
 (1+K_2+K_3+K_4+K_5+K_6)^6(1+s_*)^6
 +C_{\rm con}^{\rm tree}\right].                 \tag{2.20}
\]

Since \(F:(M_d,g)\to S^n\) is an isometry,

\[
 \Delta_gF=-nF.                                    \tag{2.21}
\]

Equations (2.19)--(2.21), and their polarization applied to \(F_aF_b\), give

\[
 \|\mathcal T_h(y)\|_{0,\alpha,h}\leq b_*h^2,
 \qquad
 \|\widehat M_i(y)\|_F\leq m_*h^{n+2},           \tag{2.22}
\]

with, for example,

\[
 b_*=(n+1)C_{\rm con},\qquad
 m_*=4(n+1)^2C_{\rm con}.                          \tag{2.23}
\]

## 3. The continuum Jacobi gap and the symmetry gauge

The derivative of the harmonic-map tension at the identity sphere is, up to
the harmless global sign convention,

\[
 J=\nabla^*\nabla-(n-1).                            \tag{3.1}
\]

Its kernel consists of Killing fields; for \(n=2\), it additionally contains
the conformal gradients \(P_xa\).  This follows directly from vector spherical
harmonics.  If \(\lambda_l=l(l+n-1)\), the gradient branch has eigenvalues

\[
 \lambda_l-2(n-1),                                 \tag{3.2}
\]

and the coexact branch has eigenvalues \(\lambda_l-n\).  Thus the only zero
modes are the ones just listed, and every other eigenvalue has absolute value
at least

\[
 \sigma_n=1.                                       \tag{3.3}
\]

Restrict to \(W\)-equivariant tangent fields.  A Killing field \(Ax\) is
equivariant only if \(A\) commutes with the standard \(W\)-representation.
Its real commutant consists of scalars, so a skew member is zero.  When
\(n=2\), equivariance of \(P_xa\) requires \(a\) to be fixed by \(W\), hence
\(a=0\).  Therefore

\[
 \|u\|_{L^2}\leq\|Ju\|_{L^2}
 \quad\hbox{for every equivariant }u.              \tag{3.4}
\]

This finite symmetry is essential: it removes the Möbius degeneracy which a
bare \(S^2\) inverse would miss.

## 4. A quantitative discrete Schauder inverse

Let \(J_h=D\mathcal T_h(y)\), restricted to equivariant nodal tangent fields.
The following estimate is the analytic global-feasibility margin:

\[
 \boxed{\quad
 \|u\|_{2,\alpha,h}\leq C_J\|J_hu\|_{0,\alpha,h}.
 \quad}                                             \tag{4.1}
\]

It holds for \(h\leq h_J\), with effective constants depending only on the
finite compiler.  Here is a direct proof with no graph-diameter factor hidden.

Freeze one chart coefficient matrix.  In a one-point lattice record its
scalar symbol is

\[
 p_q(\xi)=4\sum_v\rho_v(q)
                  \sin^2(\xi\cdot v/2).            \tag{4.2}
\]

In a periodic-crystal record the symbol is a
\(Q\times Q\) Hermitian matrix.  Connecting its basis points at conductance
scale \(h^n\) would give only an order-one optical gap and would not control a
discrete second derivative across an edge of length \(h\).  The strong
odd-moment connectors instead give, after the tree phase gauge,

\[
 U^*p_q(\xi)U\geq c_{\rm sym}\left(
    \operatorname{dist}(\xi,2\pi\mathbb Z^n)^2
           Q|\bar U|^2+\sum_\alpha|U_\alpha-\bar U|^2\right). \tag{4.3}
\]

Indeed the period floor controls every basis component away from reciprocal
zero, and the selected positive tree edges control all basis differences at
reciprocal zero.  The gauge is legitimate because the selected basis graph
is a tree.  The explicit constant is (2.14g).  The only zero is the scalar
acoustic constant, and the optical gap has the same \(h^{-2}\) normalization
as the acoustic branch.  No interval eigenvalue threshold or graph-size
computation is used in (4.3).

Fourier inversion on the lattice box, split into dyadic annuli, gives the
frozen estimate

\[
 \|u\|_{2,\alpha,h;Q/2}
 \leq C_F\bigl(\|A_hu\|_{0,\alpha,h;Q}
                    +\|u\|_{0;Q}\bigr),           \tag{4.4}
\]

where a fully explicit choice is

\[
 C_F=2^{n+8}(1+s_*)^{n+6}
       (1+\Lambda_*)^3c_{\rm sym}^{-3}(1-2^{-\alpha})^{-1}. \tag{4.5}
\]

Indeed, on the annulus \(2^{-m-1}\pi<|\xi|\leq2^{-m}\pi\), two symbol
derivatives cost at most \((1+s_*)^2\), (4.3) supplies two inverse powers of
\(|\xi|\), and the Hölder difference supplies \(2^{-m\alpha}\); summing the
geometric series gives (4.5).  The zero-frequency term is the displayed
\(C^0\) term.

Choose a rational patch radius

\[
 r_*\leq\min\left\{r_{\rm atlas},
 {c_{\rm sym}\over16C_F(1+K_\rho+K_2)}\right\}.   \tag{4.6}
\]

The same freezing argument for the continuum operator, together with the
spectral inverse (3.4), gives the global continuum estimate

\[
 \|u\|_{C^{2,\alpha}}
 \leq C_{\rm cont}\|Ju\|_{C^{0,\alpha}},\qquad
 C_{\rm cont}=8N_{\rm ov}C_F(1+\sigma_n^{-1}).      \tag{4.7}
\]

We now build a right parametrix, which avoids the invalid use of a quadratic
form for the indefinite Jacobi operator.  Let \(\phi_i\) be the scalar hat
functions of the canonical \(W\)-invariant barycentric triangulation of
\(K_N\), transported to \(M_d\).  The parabolic catalogue has only finitely
many simplex shapes, and (2.9) therefore gives a uniform shape-regularity
constant.  For tangent nodal data \(f_i\in T_{y_i}S^n\subset H\), define

\[
 (E_hf)(F(q))=
 P_{F(q)}\sum_i\phi_i(q)f_i .                    \tag{4.8a}
\]

This is a tangent field, not a componentwise scalar extension masquerading
as one.  At a node, \(P_{y_i}f_i=f_i\), so \(S_hE_h=I\) exactly.  The
identities \(F(wq)=wF(q)\), \(\phi_{wi}(wq)=\phi_i(q)\), and
\(P_{wx}=wP_xw^{-1}\) show that (4.8a) preserves equivariance; no
post-extension averaging is needed.  On each of the finitely many reference
simplices, the usual barycentric-coordinate estimate, followed by
\(\|P_x-P_y\|\leq2d_S(x,y)\), gives

\[
 S_hE_hf=f,\qquad
 \|E_hf\|_{C^{0,\alpha}}
 \leq C_E\|f\|_{0,\alpha,h},\qquad
 C_E=4N_{\rm ov}(1+K_1).                            \tag{4.8}
\]

Thus all constants in this extension estimate are finite-template and
shape-regularity constants.  Although \(E_hf\) is only piecewise
\(C^{0,\alpha}\), this is exactly the regularity required on the right-hand
side of the continuum Schauder inverse \(J^{-1}:C^{0,\alpha}\to
C^{2,\alpha}\).

Taylor's integral formula through order two, applied to the derivative of
(1.1), gives for every equivariant \(u\in C^{2,\alpha}\)

\[
 \|J_hS_hu-S_hJu\|_{0,\alpha,h}
 \leq C_{\rm jac}h^\alpha\|u\|_{C^{2,\alpha}},    \tag{4.9}
\]

where the direct direction sum permits

\[
 C_{\rm jac}=16D_*\Lambda_*(1+K_\rho+K_2)
                    (1+s_*)^{4+\alpha}.             \tag{4.10}
\]

Define

\[
 Q_h=S_hJ^{-1}E_h.                                  \tag{4.11}
\]

Equations (4.7)--(4.11) imply

\[
 \|J_hQ_h-I\|_{0,\alpha,h\to0,\alpha,h}
 \leq C_{\rm jac}C_{\rm cont}C_Eh^\alpha.          \tag{4.12}
\]

Consequently, for

\[
 h_J\leq(2C_{\rm jac}C_{\rm cont}C_E)^{-1/\alpha}, \tag{4.13}
\]

the Neumann series \(Q_h(I+(J_hQ_h-I))^{-1}\) is a right inverse of
\(J_h\), with norm at most \(2C_{\rm cont}C_E\).  The domain and codomain
have the same finite dimension, so it is the inverse.  Thus (4.1) holds with

\[
 \boxed{C_J=2C_{\rm cont}C_E.}                     \tag{4.14}
\]

This proof exposes the overlap, coefficient, symbol, and continuum spectral
gap constants.  It does not appeal to an unspecified discrete inverse.

## 5. Exact harmonic correction

Use tangent exponential coordinates at \(y\):

\[
 x_i(\xi)=\exp_{y_i}\xi_i,                         \tag{5.1}
\]

with \(\xi\) equivariant.  On the ball
\(\|\xi\|_{2,\alpha,h}\leq1/8\), direct differentiation of (1.1) and the
finite degree bound gives

\[
 \|D\mathcal T_h(x(\xi))-D\mathcal T_h(y)\|_{2,\alpha\to0,\alpha}
 \leq C_{\rm nl}\|\xi\|_{2,\alpha,h},             \tag{5.2}
\]

where one admissible value is

\[
 C_{\rm nl}=32D_*\Lambda_*(1+s_*)^4(1+K_2)^3.     \tag{5.3}
\]

If

\[
 h\leq h_{\rm NK}:=
 \min\left\{h_J,(8C_Jb_*)^{-1/2},
              (4C_J^2C_{\rm nl}b_*)^{-1/2}\right\}, \tag{5.4}
\]

Newton--Kantorovich iteration in the equivariant space converges to a unique
\(\xi_h\) in the indicated ball and gives

\[
 \|\xi_h\|_{2,\alpha,h}\leq2C_Jb_*h^2,
 \qquad \mathcal T_h(x(\xi_h))=0.                 \tag{5.5}
\]

The full tension vanishes, not merely its invariant projection: at an
equivariant embedding the tension is itself an equivariant tangent field, so
testing/solving in the equivariant field space includes the gradient.

Equations (1.2)--(1.4) now prove positivity, reversibility, and exact
\(H_0/H_1\) reproduction.

## 6. Geometry, rate, and the quadratic quotient

The discrete \(C^1\) part of (5.5) changes every active edge by at most
\(4C_Jb_*h^3\).  For

\[
 h\leq h_{\rm geo}:=\min\{h_{\rm NK},q_0/(16C_Jb_*)\}, \tag{6.1}
\]

the corrected family has

\[
 \operatorname{fill}(X_h)\leq(H_0+1)h,
 \quad\operatorname{sep}(X_h)\geq(q_0/2)h,
 \quad\deg(i)\leq D_*,
\]

\[
 (q_0/2)h\leq\theta_{ij}\leq2\Lambda_0h.          \tag{6.2}
\]

Consequently

\[
 r_i=n{\sum_jc_{ij}\over\sum_jc_{ij}(1-x_i\cdot x_j)}
 \leq {2n\pi^2\over q_0^2}h^{-2}.                 \tag{6.3}
\]

Thus one may take

\[
 \boxed{R_d={2(d-1)\pi^2\over q_0^2}.}            \tag{6.4}
\]

The aggregate energy floor and (6.2) give compiler constants
\(0<\mu_-\leq\mu_+\) with

\[
 \mu_-h^n\leq\mu_i\leq\mu_+h^n.                 \tag{6.5}
\]

For example, if \(G_-h^{n-2}\leq\sum_jc_{ij}\leq
G_+h^{n-2}\), then

\[
 \mu_-={G_-q_0^2\over2n\pi^2},\qquad
 \mu_+={2G_+\Lambda_0^2\over n}.                 \tag{6.6}
\]

Equation (5.5) implies
\(x_j-x_i=(y_j-y_i)+O(h^3)\) and
\((1-x_i\cdot x_j)-(1-y_i\cdot y_j)=O(h^4)\).
Combining these estimates with (2.22) gives

\[
 \|\widehat M_i(x)\|_F\leq m_{**}h^{n+2},         \tag{6.7}
\]

where

\[
 m_{**}=m_*+32D_*\Lambda_*\Lambda_0(1+n^{-1/2})C_Jb_*.
                                                               \tag{6.8}
\]

Hence

\[
 \max_i\|M_i\|_F\leq C_Mh^2,
 \qquad C_M={m_{**}\over\mu_-}.                  \tag{6.9}
\]

Normalize the masses as in (1.2).  From (2.11) and (6.5),

\[
 w_i\geq\omega_-h^n,
 \qquad \omega_-={\mu_-\over N_+\mu_+}.           \tag{6.10}
\]

For \(A\in\operatorname{Sym}_0(d)\), \(\|A\|_F=1\), choose a unit
eigenvector \(u\) with \(|u^TAu|\geq d^{-1/2}\).  Since
\(|(x^TAx)'|\leq2\) along every unit-speed geodesic, the value remains at
least \((2\sqrt d)^{-1}\) on the cap
\(d_S(x,u)\leq(4\sqrt d)^{-1}\).  Put \(H=H_0+1\) and
\(R=(8\sqrt d)^{-1}\).  If \(Hh\leq R\), fill distance implies that
the \(Hh\)-balls centered at nodes in \(B(u,2R)\) cover \(B(u,R)\).
For \(0<t\leq\pi/2\),

\[
 {|\mathbb S^{n-1}|\over n}
 \left({2\over\pi}\right)^{n-1}t^n
 \leq |B_{\mathbb S^n}(t)|
 \leq {|\mathbb S^{n-1}|\over n}t^n .
\]

Consequently \(B(u,2R)\) contains at least
\((2/\pi)^{n-1}(R/(Hh))^n\) nodes.  Using (6.10) therefore gives

\[
 \sum_iw_i(x_i^TAx_i)^2\geq\alpha_d,              \tag{6.11}
\]

with the explicit admissible constant

\[
 \alpha_d={\omega_-\over4d}
 \left({2\over\pi}\right)^{d-2}
 (8H\sqrt d)^{-(d-1)}.                            \tag{6.12}
\]

Thus sampling is eventually injective (and the same estimate holds on the
sampled quotient without using injectivity).  From the P1A row formula,

\[
 \boxed{\mathfrak D_2(L_h)\leq C_dh^2,\qquad
 C_d={C_M\over\sqrt{\alpha_d}}.}                   \tag{6.13}
\]

P1B and (6.4) give, for the declared class \({\cal G}_h(R_d)\),

\[
 \boxed{
 {d(d-1)\over R_d}h^2
 \leq\inf_{L\in\mathcal G_h(R_d)}\mathfrak D_2(L)
 \leq C_dh^2.}                                     \tag{6.14}
\]

The lower constant is \(c_d=dq_0^2/(2\pi^2)\).

## 7. Conditional robustness calculation under the missing compiler premise — not a theorem

The proof is stable in the norm actually used by the inverse.  First perturb
the compiled reference map, midpoint coefficients, and chart nodes
\(W\)-equivariantly so that

\[
 \|\delta F\|_{C^{4,\alpha}}
 +\max_{a,v}\|\delta\rho_{a,v}\|_{C^{3,\alpha}}
 \leq\varepsilon,                                  \tag{7.1}
\]

and preserve \(W\)-equivariance.  If

\[
 \varepsilon\leq\varepsilon_0:=
 {1\over16}\min\{j_-,\lambda_*,q_0,C_J^{-1},\mu_-\}, \tag{7.2}
\]

then the compiler bounds deteriorate by at most a factor two.  The residual
in (2.22) changes by at most \(C_{\rm pert}\varepsilon h^2\), and the same
Newton proof gives

\[
 \|\xi_h^{\,\prime}\|_{2,\alpha,h}
 \leq2(2C_J)(b_*+C_{\rm pert}\varepsilon)h^2.      \tag{7.3}
\]

For \(n\ne2\), the same statement holds for arbitrary (not necessarily
equivariant) perturbations after imposing the ordinary orthogonality gauge to
target rotations; the full Jacobi gap off rotations is at least one.

For \(n=2\), three additional conformal projections are necessary.  The exact
identity

\[
 DE_x[P_xa]=-2a\cdot\sum_i\mu_i x_i               \tag{7.4}
\]

shows that every critical embedding must have \(\sum_i\mu_ix_i=0\).  Thus a
generic nonsymmetric perturbation cannot be covered by a rotation-only
inverse.  It is covered either (i) when these three projected residuals vanish,
or (ii) when a three-parameter Möbius balancing map is included and its
displayed finite-dimensional derivative has smallest singular value at least
\(\beta_{\rm Mob}>0\).  In case (ii), replace \(C_J\) by
\(C_J+\beta_{\rm Mob}^{-1}\); all other estimates are unchanged.  The
dependence on \(\beta_{\rm Mob}\) is not suppressed.

Subject to the applicable symmetry/gauge condition, labeled jitter is allowed
at the scale \(\max_i|\delta y_i|\leq\rho h^4\); its scaled tension error is
\(O(\rho h^2)\).  Smooth jitter may be as large as \(O(h^2)\) provided its
discrete \(C^{2,\alpha}_h\) norm is \(O(h^2)\).  These are the natural scales:
uncontrolled \(O(h^2)\) alternating jitter has second differences of order
one and need not preserve (2.22).

## 8. Route boundary and audits required by implementation

This construction uses six ingredients which must be kept distinct in the
implementation:

1. the exact simplex-boundary lattice (2.1), including every parabolic/layer
   record;
2. the finite equivariant smoothing records (2.5)--(2.9);
3. the rational tensor-cone direction compiler (2.12)--(2.14);
4. midpoint-shared energy assembly (2.15), never endpoint averaging;
5. the equivariant Newton solve, with the \(S^2\) conformal modes explicitly
   excluded by symmetry;
6. the sampled generalized quotient, never the raw singular pencil.

Deterministic failures should include: raw radial simplex normalization (a
first-order seam defect), omission of a parabolic layer, endpoint rather than
midpoint coefficients (first-order truncation), a nonsymmetric atlas cutoff
(loss of the Jacobi gauge), removal of the aggregate tensor floor (loss of
the symbol bound), and an unrestricted \(S^2\) inverse (Möbius zero modes).

The finite compiler may be interval-certified dimension by dimension, but
the proof above is all-level: the intervals certify only the fixed atlas,
direction-cone, and derivative constants.  No finite graph-size computation
is used in place of (2.17), (4.1), or Newton--Kantorovich.
