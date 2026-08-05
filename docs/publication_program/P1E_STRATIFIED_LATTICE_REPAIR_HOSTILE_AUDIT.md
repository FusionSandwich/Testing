# Hostile audit: P1E stratified-lattice repair

## Verdict

`BLOCKED / REJECTED AS AN ALL-LEVEL CONSTRUCTION.`

The residue-unwinding **bijection on its positivity domain** is correct for
every nonempty proper `Z`, every complement `B`, and every `beta in B`.
The radius-buffer addendum in Lemma 1 is false as stated.  Independently,
Sections 2--7 assume a global affine one-point-lattice atlas which Section 9
correctly proves cannot exist on `S^n`, `n>=2`.  Even under that impossible
conditional hypothesis, the displayed pair convention introduces an exact
factor-two error, so the consistency estimate (5.7) and the asserted Jacobi
inverse do not follow as written.

This audit does not promote any conditional statement in Sections 2--7.

## 1. Exact scope of Lemma 1

Let `Q=Nq` and `T=Nt`.  For a lattice node `k`, put

\[
 m=\sum_{z\in Z}k_z.
\]

Since `min_Z k_Z=0`,

\[
 Q=P_Zk_Z,\qquad \min Q=-m/z,
\qquad k_Z=Q-(\min Q)1_Z.
\]

Moreover,

\[
 T=k_B-(N-m)e_\beta\in A_B.
\]

Conversely, for `Q in A_Z^*` and `T in A_B`,

\[
 k_Z=Q-(\min Q)1_Z,qquad
 k_B=T+(N+z\min Q)e_\beta                         \tag{A.1}
\]

is integral, has total mass `N`, and has minimum zero in the `Z` block.
It is a node of the stated chart exactly when every component of `k_B` is
strictly positive.  The fact used here is exact and independent of a choice
of representative: if `Q=P_Zu`, then
`Q-(min Q)1_Z=u-(min u)1_Z` is integral and nonnegative.

Thus the correct unconditional statement is

\[
 \Psi(K_N\cap\{k_b>0\ (b\in B),\ \min_Zk_Z=0\})
 =h(A_Z^*\times A_B)\cap\mathcal P_{N,Z,\beta},    \tag{A.2}
\]

where `mathcal P` is the positivity region in (A.1).  This proves the local
one-point product record for all `Z,B,beta`.

### The claimed buffer is false

Take

\[
 d=3,\quad N=4,\quad h=1/4,\quad
 Z=\{0,1\},\quad B=\{2,3\},\quad \beta=2,
\]

and

\[
 k=(0,2,1,1).
\]

Both `B` coordinates equal `h`, so the hypothesis
`lambda_b >= s_*h` holds with `s_*=1`.  The primitive product-lattice
neighbour

\[
 T\longmapsto T+(e_2-e_3)
\]

is at one lattice step, but (A.1) sends it to `k_B'=(2,0)`.  It is outside
the chart, whose definition requires every `B` coordinate to be positive.

More generally a displacement `(Delta Q,Delta T)` changes the distinguished
coordinate by

\[
 \Delta k_\beta
 =\Delta T_\beta
  +z\{\min(Q+\Delta Q)-\min Q\}.                  \tag{A.3}
\]

Consequently a sufficient coordinatewise radius-`R` buffer is strict margin
`k_b>R` for `b ne beta` and `k_beta>(z+1)R`; the exact sharp buffer is the
support function of the actual finite stencil through (A.3).  A single
undeclared number `s_*` is not enough, and equality at the boundary is not
enough for an open chart.

## 2. Atlas, cores, and smoothing

The following pieces do not pass audit.

1. The proposed collar recursion is internally inconsistent.  For a move
   from `|Z|=k` to `|Z'|=k-1`, the new record requires the removed coordinate
   to exceed `4 eta_(k-1)`, whereas the text switches when it exceeds only
   `2 eta_k`.  Since `eta_k <= eta_(k-1)/100`, the latter condition does not
   imply the former.

2. A weak braid ordering does not make an ordinary open neighbourhood of a
   minimum tie lie in one affine minimum cone.  Separate cones meet on the
   tie.  Smooth ownership transfer across those cones is exactly an
   interface problem, not a consequence of recording `sigma`.

3. When a minimum index and a partition are fixed, the coordinate changes
   really are affine lattice isomorphisms.  For example, moving
   `c in Z` to `B` sends

   \[
   Q' =P_{Z\setminus\{c\}}Q,
   \quad T'_c=Q_c-Q_\alpha,
   \quad T'_\beta=T_\beta-(Q_c-Q_\alpha),          \tag{A.4}
   \]

   where `alpha` is a fixed minimum index; all other `T` components are
   unchanged.  This is integral and has an integral inverse.  Changing
   `beta` is similarly the triangular shear

   \[
   T'=T+(N+z\min Q)(e_\beta-e_{\beta'}).           \tag{A.5}
   \]

   These local calculations do not produce the globally compatible atlas.

4. Section 9 gives a correct fatal obstruction: a smooth atlas with dense
   grid-preserving transitions would define an affine structure on `S^n`.
   The developing-map argument excludes it for `n>=2`.  Hence the atlas
   premise needed by Sections 2--7 is not merely unproved; it is impossible.

5. The claimed `C^6` equivariant smoothing and `C^5` buffered partition are
   not constructed by the sentence about Hermite interpolation.  No core
   list, compatible jet recursion, global degree/covering argument, or
   interval certificate for injectivity is supplied.  Local determinant
   bounds alone would not exclude global self-intersection.  In any event,
   such a construction cannot satisfy the impossible affine-overlap premise.

## 3. Shared edge energy and cone coefficients

The indicator in (3.5) is symmetric under `i<->j`; if both endpoints and
the midpoint lie in a valid chart, it does define a nonnegative shared
coefficient.  It does **not** prove that both paired neighbours exist.  That
uses the false buffer addendum above.  The declaration that out-of-buffer
terms are zero can therefore remove one member of a nominal central pair and
destroy the cancellation used in (4.1).

The finite positive tensor-cone idea is repairable: a finite rational
direction net and compactness give strict feasibility, and local linear
right inverses can be blended while preserving the tensor identity.  The
present text does not give the finite cover or its derivative constants, but
this is not the principal obstruction.

Two explicit constants/conventions fail:

* In one dimension with the primitive direction `v=1`, coefficient
  `b=rho`, and standard lattice basis, the frozen symbol is
  `4 rho sin^2(xi/2)=rho xi^2+O(xi^4)`.  Formula (3.8) proposes
  `c_0=4rho` when `N_atlas=C_basis=1`, contradicting (3.7) for every
  sufficiently small nonzero `xi`.  At least the small-frequency Gram
  constant and the usual sine constant must be included.

* The pair normalization has an exact factor-two error.  Formula (3.4) uses

  \[
  2\sum_{[v]}\rho_vvv^T=A,                         \tag{A.6}
  \]

  while (3.5) includes the two neighbours `q+hv` and `q-hv` once for one
  unoriented class `[v]`.  Their force expansion has principal tensor

  \[
  \sum_{[v]}\rho_vvv^T=A/2,                        \tag{A.7}
  \]

  whereas their increment covariance has tensor

  \[
  2\sum_{[v]}\rho_vvv^T=A.                         \tag{A.8}
  \]

  Thus (A.6) is appropriate for (4.4), but the normalized force in (4.3)
  linearizes to one half of the round Jacobi operator.  For any smooth `u`
  with `Ju != 0`,

  \[
  J_hS_hu-S_hJu\longrightarrow-\tfrac12S_hJu,
  \]

  contradicting the `O(h^alpha)` estimate (5.7).  One may repair the
  convention by multiplying the normalized force by two or by using `J/2`,
  but every inverse and Newton constant must then be recomputed.

## 4. Moment expansion and ties

The single-chart central midpoint identity (4.1) is correct.  For smooth
`b` and `F`, odd powers cancel and

\[
 b(q+hv/2)\{F(q+hv)-F(q)\}
 +b(q-hv/2)\{F(q-hv)-F(q)\}
 =h^2\operatorname{div}(bvv^TDF)+O(h^4).
\]

Its use at every row is conditional on both paired neighbours, a common
smooth chart for the full stencil, and compatible coefficient jets across
ties.  None is globally supplied.  The sentence that no nonsmooth minimum
enters the expansion simply restates the impossible overlap hypothesis.

## 5. Extension, Schauder estimate, and inverse

This section contains further missing or false steps.

1. A scalar nodal interpolant of tangent vectors is not a tangent field.
   A viable definition would first interpolate ambient vectors, project by
   `P_{F(x)}`, and then average equivariantly; sample preservation follows
   because nodal data are tangent.  Equation (5.6) gives none of these
   definitions or the required common conforming triangulation.

2. The frozen Schauder estimate (5.3) and the numerical constant (5.4) are
   asserted, not derived.  `C_basis` and `Lambda_*` are not defined, and the
   false ellipticity constant (3.8) feeds directly into them.  A scalar
   symbol lower bound alone does not prove the displayed vector-valued,
   variable-coefficient, tangent-bundle estimate with interfaces.

3. The parametrix identity itself is sound if one has a tangent extension
   satisfying `S_hE_h=I`, continuum invertibility, and consistency.  The
   exact factor-two contradiction above means the stated consistency (5.7)
   is false.  The global interface consistency is also unavailable because
   the atlas is impossible.

4. `C_cont`, `C_E`, `C_j`, and the discrete norms are not explicitly
   defined or bounded.  Hence (5.9)--(5.10) are not the explicit controlled
   inverse requested by P1E.

The claim that no interface Schauder lemma is assumed is therefore false:
the missing global grid/extension/consistency package is precisely a
theorem-strength compiler and interface estimate.

## 6. Downstream algebra and robustness

Conditional on a genuine critical point and positive shared conductances,
the finite algebra in (6.5)--(6.6) is correct.  Tangential equilibrium makes
the force radial, radial contraction gives

\[
 \sum_jc_{ij}(x_j-x_i)=-n\mu_ix_i,
\]

so the normalized generator is reversible, positive, and exact on `H_0`
and `H_1`.

The claimed quantitative theorem is nevertheless unavailable: the inverse
and Newton step fail upstream, and the Riemann-sum threshold and constants
`C_T'`, `C_M`, `C_j`, `C_E`, `C_N`, `c_mu`, `C_mu`, `C_Q`, `c_S`, `h_S`,
`R_d`, and `C_d` are only named, not calculated or interval-certified.

The robustness theorem is false for the perturbation class stated.  A
fixed `C^{3,alpha}` coefficient perturbation of size `epsilon` changes the
principal second tensor by `O(epsilon)`.  On a flat two-direction patch,
changing the two paired coefficients from `(rho,rho)` to
`(rho+epsilon,rho)` produces a normalized trace-free covariance of order
`epsilon`, not `h^2`.  If the perturbation varies in space, its divergence
also creates an `O(epsilon)` tangent-force residual, so the Newton solution
cannot remain in the `O(h^2)` ball.  To preserve P1E order, one must either
reimpose the exact tensor identity for the perturbed coefficients or require
the moment-breaking component to be `O(h^2)`.  Arbitrary fixed
`epsilon <= rho_*/4` is insufficient.  Arbitrary perturbations must also be
required to preserve `W` symmetry (or a full kernel gauge and modulation
argument is needed).

## Final classification

| Claim | Audit status |
|---|---|
| Residue-unwinding product bijection on positivity domain | `PASS` |
| Radius buffer in Lemma 1 | `REJECTED` by exact `d=3,N=4` fixture |
| Fixed-cone affine lattice transition | `PASS` locally |
| Global smooth affine-unimodular lattice atlas | `IMPOSSIBLE` |
| Equivariant smoothing/partition with the stated atlas properties | `BLOCKED / IMPOSSIBLE` |
| Symmetry and positivity of an actually present edge in (3.5) | `PASS` |
| Existence of every central pair used by (4.1) | `REJECTED` under stated buffer |
| Tensor-cone feasibility | `PASS` in principle; constants not supplied |
| Pair normalization and consistency (5.7) | `REJECTED` by factor two |
| Global tangent extension and discrete inverse | `BLOCKED` |
| Exact `H_0/H_1` algebra after a true critical point | `PASS` |
| Explicit all-level constants and robustness | `REJECTED` |
| Unconditional all-dimensional P1E family | `NOT CONSTRUCTED` |

The deterministic companion audit contains the exact buffer and pair-factor
fixtures.  Finite fixtures are used only to falsify displayed universal
claims; they are not substitutes for an all-level construction.
