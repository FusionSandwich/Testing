# Finite positive eigenmap generators: sampled quadratic rigidity and sharp spherical barriers

## Final manuscript theorem package

This document is the publication synthesis of the proved Prompt-1 through
Prompt-4 pure-mathematics results.  Detailed proofs remain in the referenced
authoritative theorem files.  Every mathematical assertion below has exactly
one of the statuses `PROVED`, `EXTERNAL`, `COMPUTATIONAL`, `CONJECTURE`, or
`REJECTED`.

## 1. Setting and foundational calculus

Let `I` be a nonempty finite set and

\[
(Lf)(i)=\sum_{j\ne i}a_{ij}(f(j)-f(i)).
\tag{1.1}
\]

Positivity means `a_ij>=0` off the diagonal.  Reversibility is separate: for
positive masses `w_i`, shared conductances satisfy

\[
\gamma_{ij}=\gamma_{ji}\ge0,
\qquad a_{ij}=\gamma_{ij}/w_i.
\tag{1.2}
\]

For

\[
\Gamma(f,g)(i)=\frac12\sum_j a_{ij}
 (f(j)-f(i))(g(j)-g(i)),
\tag{1.3}
\]

the product identity

\[
L(fg)-fLg-gLf=2\Gamma(f,g)
\tag{1.4}
\]

is `PROVED`.  If `Lf=-lambda f`, `Lg=-nu g`, then

\[
L(fg-c)+\mu(fg-c)
=2\Gamma(f,g)+(\mu-\lambda-\nu)fg-\mu c.
\tag{1.5}
\]

Thus additive resonance is constant polarized carré du champ.  The assertion
that every nonzero centered resonant square is impossible for a positive
finite generator is `REJECTED` by the exact Boolean-square example.

Weighted Cauchy--Schwarz, finite rank-nullity, convex separation, finite Farkas
alternatives, finite LP strong duality, compactness of finite-dimensional
closed feasible sets, the relevant spherical trigonometry, and the
Mittag--Leffler partial-fraction expansion are `EXTERNAL` standard inputs.  No
novelty claim is attached to those ingredients alone.

## 2. Central theorem: genuine sampled quadratic exactness

Let

\[
\Phi:I\to\mathbb R^d,
\qquad L\Phi=-\lambda\Phi
\tag{2.1}
\]

coordinatewise, and define the local jump covariance

\[
C_i=\sum_j a_{ij}(\Phi_j-\Phi_i)(\Phi_j-\Phi_i)^T.
\tag{2.2}
\]

For a real matrix `A`, put `Q_A(i)=Phi_i^T A Phi_i`.

### Theorem A — sampled quadratic residual factorization (`PROVED`)

For every real `A`, without positivity or reversibility,

\[
LQ_A(i)=-2\lambda Q_A(i)+\operatorname{tr}(A^TC_i).
\tag{2.3}
\]

For `q_{A,c}=Q_A-c`, exact target `-mu` is equivalent to

\[
\operatorname{tr}(A^TC_i)
+(\mu-2\lambda)Q_A(i)-\mu c=0
\quad\text{for every }i.
\tag{2.4}
\]

Now assume `d>1`, `Phi_i in S^(d-1)`, `lambda=d-1`, target `mu=2d`, and
`A in Sym_0(d)`.  With

\[
M_i=P_0(C_i+2\Phi_i\Phi_i^T),
\quad
S_X(A)_i=\Phi_i^TA\Phi_i,
\quad
R_X(A)_i=\langle A,M_i\rangle_F,
\tag{2.5}
\]

one has

\[
\boxed{R_X=(L+2dI)S_X.}
\tag{2.6}
\]

Consequently, if `E_form=ker R_X` and `K_X=ker S_X`, then

\[
\boxed{K_X\subseteq E_{\rm form},}
\tag{2.7}
\]

\[
\boxed{
E_{\rm sample}:=S_X(E_{\rm form})
=\operatorname{im}S_X\cap\ker(L+2dI),
}
\tag{2.8}
\]

and

\[
\boxed{
\dim E_{\rm sample}
=\dim E_{\rm form}-\dim K_X
=\operatorname{rank}S_X-\operatorname{rank}R_X.
}
\tag{2.9}
\]

This is more than ambient rank bookkeeping: the residual factors through the
actual sampling map, the sampling kernel is automatically contained in the
form kernel, and the quotient identifies the genuine sampled eigenspace.

### Positive structural rigidity (`PROVED`)

If each row covariance has the axial form

\[
C_i=\tau_i(I-\Phi_i\Phi_i^T)+\beta_i\Phi_i\Phi_i^T,
\qquad\beta_i>0,
\tag{2.10}
\]

then `E_form=K_X` and `E_sample={0}`.  For a positive generator,

\[
\beta_i=\sum_j a_{ij}(1-\Phi_i\cdot\Phi_j)^2,
\tag{2.11}
\]

so one positive jump to a distinct embedded point gives the required strict
radial coefficient.  Regular simplices attain the theorem with a nontrivial
sampling kernel.

Independently, if a finite group acts transitively and equivariantly, all
off-diagonal rates are nonnegative and invariant, the real conjugation action
on `Sym_0(d)` is irreducible, and one positive jump is geometrically distinct,
then `E_form={0}`.  Reversibility is not required.  The same statement with
otherwise signed rates is `REJECTED` by the signed regular pentagon.

The exact Platonic form/sampling ranks are `COMPUTATIONAL`; the ordinary
factorization and structural rigidity theorems are `PROVED`.

## 3. Spectral-product target classes

The common-operator sampling theorem is `PROVED`: scalar restrictions with
pairwise distinct target eigenvalues form an internal sampled direct sum and
obey the corresponding rank bound.  The signed converse is indexed by target
eigenvalue classes, and a zero-target class contains constants exactly once.

For spherical degrees

\[
\lambda_\ell=\ell(\ell+d-2).
\tag{3.1}
\]

Distinct degrees imply distinct target eigenvalues when `d>=2`.  The literal
all-dimension distinct-degree formulation is `REJECTED`: in `d=1`, the
singleton sphere has coincident degree-zero and degree-one target/sample
classes.  Clebsch--Gordan and negative-Pell completeness are `EXTERNAL`; the
finite Platonic alias tables are `COMPUTATIONAL`.

## 4. Exact local feasibility and shared-edge compatibility

Fix `Omega_i in S^2`.  For non-antipodal permitted neighbors write

\[
\Omega_j=\cos\theta_j\Omega_i+\sin\theta_j u_j,
\qquad0<\theta_j<\pi.
\tag{4.1}
\]

### Theorem B — indexed local feasibility (`PROVED`)

A nonnegative coordinate-exact row exists exactly when

\[
0\in\operatorname{conv}\{u_j\}.
\tag{4.2}
\]

It is positive on every indexed permitted edge exactly when zero belongs to
the relative interior of that indexed hull.  Repetitions, redundant
candidates, and lower-dimensional tangent spans are included.  If

\[
\beta_j\ge0,\quad\sum_j\beta_j=1,\quad\sum_j\beta_ju_j=0,
\tag{4.3}
\]

then the corresponding row is

\[
a_j=\frac{2\beta_j}
{\sin\theta_j\sum_q\beta_q\tan(\theta_q/2)}.
\tag{4.4}
\]

Antipodal-only rows form a simplex of total rate one.  Mixed rows have an
exact division-free normal-budget parameterization.  Positive relative
inradius gives explicit coefficient, rate, conditioning, and transported-span
perturbation bounds.

### Theorem C — shared-edge cone (`PROVED`)

For positive masses on a fixed undirected graph, shared equilibrium is a
finite cone problem `A gamma=b`, `gamma>=0`.  It is feasible exactly when `b`
belongs to the shared-edge cone, equivalently when no Farkas certificate has
`A^Ty>=0` and `<y,b><0`.  Weighted centering is necessary and is sufficient on
the complete graph through `gamma_ij=2w_iw_j`.

The assertion that local feasibility plus centering suffices for every sparse
graph is `REJECTED` by exact four-cycle and cube certificates.

## 5. Exact and quantitative spherical equality rigidity

For a unit-sphere coordinate eigenmap with target `-2`, put

\[
\ell_{ij}=1-\Omega_i\cdot\Omega_j,
\quad r_i=\sum_j a_{ij},
\quad\varepsilon_i=\sum_j a_{ij}\ell_{ij}^2,
\quad Q_i=\frac{r_i\varepsilon_i}{4}.
\tag{5.1}
\]

The normal moment is `sum_j a_ij ell_ij=2`.

### Theorem D — equality and propagation (`PROVED`)

At every row, `Q_i>=1`, with equality exactly when all active losses equal
`2/r_i`.  If the active relation is symmetric and connected and equality
holds everywhere, one common row rate and one common active loss propagate
through the graph.

### Theorem E — restricted global classification (`PROVED`)

Assume all ten conditions:

1. a finite simple abstract triangulation of the topological sphere;
2. the active graph is exactly its one-skeleton;
3. the spherical embedding is injective;
4. each edge is the unique minor great-circle arc, of length in `(0,pi)`;
5. edge interiors meet only when their abstract edges share an endpoint;
6. each face maps homeomorphically to its geodesically convex spherical
   triangle;
7. face interiors are pairwise disjoint;
8. the face images cover the round sphere;
9. every triangulation edge has positive conductance; and
10. `Q_i=1` at every vertex.

Then the embedding is, up to `O(3)`, the regular tetrahedron, octahedron, or
icosahedron.  Every displayed hypothesis participates in the transfer from
row equality to a round cellular triangulation or blocks a catalogued
counterexample.  The unrestricted classification is `REJECTED` by the cube
and dodecahedron.

### Quantitative companion (`PROVED`)

With `p_ij=a_ij/r_i` and `m_i=2/r_i`,

\[
Q_i-1=\sum_jp_{ij}
\left(\frac{\ell_{ij}}{m_i}-1\right)^2.
\tag{5.2}
\]

An explicit normalized active-weight floor and `Q_i<=1+eta` give the proved
pointwise, path, diameter, reference-loss, arc-length, Poincare, and
effective-resistance bounds recorded in `rigidity/GLOBAL_Q_RIGIDITY_THEOREM.md`.
The closed triangulation-stability threshold and edge-length sup bound are
also `PROVED`.  Diameter-free or floor-free versions are `REJECTED`.

At exact equality with `0<ell<2`, the radial/tangent covariance decomposition
is `PROVED`; axial covariance holds exactly under its additional tangent
isotropy equation.  `Q=1` alone forcing axial covariance is `REJECTED` by the
weighted-octahedron family.

## 6. Sharp fixed product-graph barrier

Let `N>=2`, `h=pi/(2N)`, and let `G_N` be the unreduced cell-centred
latitude--longitude graph with `N` rings and `M=2N` vertices per ring.

### Theorem F — direct polar uniqueness and minimax (`PROVED`)

At a north polar-ring vertex, begin with arbitrary rates `a_v,a_+,a_-` on the
one inward and two azimuthal neighbors.  The transverse, axial, and remaining
horizontal coordinate equations directly force

\[
\boxed{
a_v=\frac1{2\sin^2h},
\qquad
a_+=a_-=\frac1{4\sin^4h}.
}
\tag{6.1}
\]

No equal masses, row reversibility, ring symmetry, or optimizer symmetry is
assumed in this local solve.  Combining it with the verified positive
reversible construction gives the graph-class identity

\[
\boxed{
\inf r_{\max}
=\frac1{2\sin^2(\pi/(2N))}
+\frac1{2\sin^4(\pi/(2N))}.
}
\tag{6.2}
\]

The infimum ranges over positive reversible shared-conductance coordinate-exact
operators supported on the fixed graph.  At every order,

\[
r_{\max}\ge\frac8{\pi^4}N^4;
\qquad K=2N^2\Longrightarrow
r_{\max}\ge\frac2{\pi^4}K^2.
\tag{6.3}
\]

### Theorem G — rigorous polar expansions (`PROVED`)

For `0<x<=pi/4`,

\[
\csc^2x=x^{-2}+\frac13+\frac{x^2}{15}+e(x),
\qquad0\le e(x)\le\frac{x^4}{80}.
\tag{6.4}
\]

Termwise differentiation is justified away from the poles and the paired
positive tail is bounded explicitly.  Hence, for every integer `N>=2`,

\[
0\le r_{\rm pole}(N)-
\left(\frac8{\pi^4}N^4+\frac{10}{3\pi^2}N^2+\frac{13}{45}\right)
\le\frac{\pi^2}{48N^2},
\tag{6.5}
\]

and

\[
0\le Q_{\rm pole}(N)-
\left(\frac{N^2}{\pi^2}+\frac7{12}\right)
\le\frac{\pi^2}{12N^2}.
\tag{6.6}
\]

These are uniform analytic statements valid at every grid order `N>=2`, not
finite fits and not a claim to an arbitrary-length asymptotic series.

## 7. Universal and constrained extremal barriers

### Theorem H — universal rate transfer (`PROVED`)

The normal moment and weighted Cauchy--Schwarz give

\[
4\le r_i\varepsilon_i.
\tag{7.1}
\]

Thus `epsilon_i<=C h^2`, `C>0`, forces `r_i>=4/(C h^2)`.  If active losses
lie in `[Lh^2,Uh^2]`, `0<L<=U`, then

\[
\frac2{Uh^2}\le r_i\le\frac2{Lh^2},
\qquad
2Lh^2\le\varepsilon_i\le2Uh^2.
\tag{7.2}
\]

At `L=2/pi^2`, `U=2`, this becomes

\[
1\le h^2r_i\le\pi^2,
\qquad
\frac4{\pi^2}h^2\le\varepsilon_i\le4h^2.
\tag{7.3}
\]

Positive spherical-Delaunay existence and exact low modes are `EXTERNAL`.
The loss window plus `K` comparable to `h^-2` proves compatibility with a
linear rate cap, not membership in the complete constrained class.

### Theorem I — constrained lower bound and existence (`PROVED`)

For `K>=2`, define the class `A_K` exactly as in
`barriers/SHARP_PRODUCT_GRAPH_BARRIERS.md`: it controls spherical separation
and covering, mesh ratio, maximum degree, edge locality, positive mass bounds,
shared nonnegative conductances, exact coordinate equilibrium, and
`r_i<=RK`.  Zero conductances select one of finitely many active support
graphs.  If the class is nonempty, then

\[
\boxed{E_K\ge\frac4{RK},
\qquad C^*=\liminf_{K\to\infty}KE_K\ge\frac4R.}
\tag{7.4}
\]

For every fixed `K` and fixed positive parameters, the nonempty class is
compact and the infimum is attained.  The fixed product family violates the
linear cap whenever

\[
N>\frac{\pi^2}{2}\sqrt R.
\tag{7.5}
\]

## 8. Conductance-aware feasible-family anisotropy

Fix a finite candidate set with tangent increments `v_j` and positive losses
`ell_j`.  Assume the tangent-balanced probability polytope

\[
\mathcal P_i=\{p\ge0:\sum p_j=1,\ \sum p_jv_j=0\}
\tag{8.1}
\]

is nonempty.  For `lambda>0`, define the affine fixed-moment slice

\[
\mathcal F_i(\lambda)=
\{a\ge0:\sum a_jv_j=0,\ \sum a_j\ell_j=\lambda\}.
\tag{8.2}
\]

It is not a cone.  The nonzero tangent-balanced cone modulo positive scaling
is bijective with `P_i`, while for each fixed `lambda`, `F_i(lambda)` itself is
bijective with `P_i` through

\[
p_j=\frac{a_j}{\sum_q a_q},
\qquad
a_j=\frac{\lambda p_j}{m(p)},
\quad m(p)=\sum_jp_j\ell_j.
\tag{8.3}
\]

### Theorem J — exact anisotropy constant and LP dual (`PROVED`)

With `s_2(p)=sum p_j ell_j^2`, the correct arbitrary-moment invariant is

\[
\boxed{
Q_\lambda(a)=\frac{r(a)\varepsilon(a)}{\lambda^2}
=\frac{s_2(p)}{m(p)^2}
=1+\frac{\operatorname{Var}_p(\ell)}{m(p)^2}.
}
\tag{8.4}
\]

At the spherical normal moment `lambda=2`, this is the global
`Q=r epsilon/4`.  Using `r epsilon/4` at arbitrary `lambda` is `REJECTED`.

The attainable means form a compact interval `I_i`.  For `m in I_i`, let

\[
\Psi_i(m)=\min\left\{
\sum_jp_j\ell_j^2:
p\in\mathcal P_i,\ \sum_jp_j\ell_j=m
\right\}.
\tag{8.5}
\]

Then

\[
\boxed{
A_i=\min_{m\in I_i}\left(\frac{\Psi_i(m)}{m^2}-1\right)
=\inf_{a\in\mathcal F_i(\lambda)}(Q_\lambda(a)-1),
}
\tag{8.6}
\]

so `Q_lambda(a)-1>=A_i` before any particular conductance solution is chosen.
Finite LP strong duality (`EXTERNAL`) gives, with the sign transfer
independently checked,

\[
\Psi_i(m)=\max_{\alpha,\beta,z}
\left\{\alpha+\beta m:
\alpha+\beta\ell_j+z\cdot v_j\le\ell_j^2\ \forall j\right\}.
\tag{8.7}
\]

Every feasible dual triple therefore certifies

\[
Q_\lambda(a)-1\ge
\frac{\alpha+\beta m-m^2}{m^2}.
\tag{8.8}
\]

One has `A_i=0` exactly when a tangent-balanced probability is supported on
one loss level.

If `v_2=-kappa v_1`, `kappa>0`, the unique balanced row satisfies

\[
\boxed{
A_i=\frac{\kappa(\ell_1-\ell_2)^2}
{(\kappa\ell_1+\ell_2)^2}.
}
\tag{8.9}
\]

Only when `kappa=1`, equivalently when the unique weights are `(1/2,1/2)`,
does this reduce to the requested symmetric formula.  Opposite rays alone
forcing half weights is `REJECTED` by the exact unequal-colatitude example.

At the product pole,

\[
\boxed{
A_{\rm pole}=Q_{\rm pole}-1
=\frac1{4\sin^2h}-\frac12+\frac{\sin^2h}{4}
=\frac{N^2}{\pi^2}-\frac5{12}+O(N^{-2}).
}
\tag{8.10}
\]

## 9. Reduced rings and bounded high-ambition outcomes

For adjacent populations `M_i,M_{i+1}` with a biregular bipartite coupling of
degrees `p,q`, double counting gives

\[
pM_i=qM_{i+1}.
\tag{9.1}
\]

This statement is `PROVED`; a perfect matching forces equal populations.  A
general split/merge construction remains `CONJECTURE` and belongs to the
numerical-analysis handoff.  Lean formalizes the arithmetic consequence after
the two incidence counts are supplied; it does not claim to formalize all of
bipartite handshaking.

The proposition that a standard Delsarte/Gegenbauer reduction by itself is a
new barrier is `REJECTED`; no solved new dual certificate survived the sampling
audit.  A blanket positive-graph curvature collapse is `REJECTED`; finite
graph-curvature frameworks are `EXTERNAL`.  A compact homogeneous-space
extension producing a material theorem in this package is `CONJECTURE`, not a
current claim.  Continuum `W_2` contraction from positivity alone is
`REJECTED`; specified discrete Maas/Erbar transport frameworks are `EXTERNAL`.

## 10. Examples, formalization, and computation boundaries

The exact signed, alias, Boolean, antipodal, cube/dodecahedron, weighted
octahedron, rare-edge, product-pole, arbitrary-`lambda`, unequal-ray, and
incidence witnesses are catalogued in
`../docs/PURE_MATH_COUNTEREXAMPLE_CATALOGUE.md`.  Each general theorem has an
ordinary proof.  Lean checks selected finite algebra and declaration
dependencies without project axioms or placeholders.  Exact scripts check
rational/algebraic identities, hostile examples, and the source-pinned
Plantri census.

The finite matrices, ranks, minors, and Plantri counts are `COMPUTATIONAL`.
They are reproducibility and falsification evidence, not general theorems and
not novelty evidence.  The ordinary theorems they test remain `PROVED`.

## 11. Publication boundary and numerical-analysis handoff

The publication audit resolves the required questions as follows.

1. The sampled quadratic theorem is more than ambient rank bookkeeping
   (`PROVED`): equation (2.6) is an operator factorization through actual
   sampling, yields automatic kernel inclusion, and identifies the genuine
   sampled eigenspace before rank-nullity is applied.
2. The global rigidity theorem needs every displayed geometric/topological
   hypothesis for its stated transfer (`PROVED`); catalogued aliases,
   nontriangulated equality graphs, antipodes, inactive edges, and degenerate
   embeddings reject the unrestricted alternatives.
3. The Prompt-4 polar result is a graph-class theorem (`PROVED`): asymmetric
   local rates are solved uniquely and an independent positive reversible
   construction attains the bound at every `N>=2`.  No fitted data enter.
4. The anisotropy invariant is conductance-aware (`PROVED`): it optimizes over
   the entire nonempty tangent-balanced feasible family and uses
   `Q_lambda`, not geometry with discarded rate choices.
5. The central package remains meaningful without any application acronym
   (`PROVED`): it concerns finite generators, eigenmaps, sampling kernels,
   covariance, and positive rigidity.
6. Future numerical analysis contains optimizer computation inside the
   constrained classes, convergence and sharp upper bounds, verified
   Delaunay-family construction, general reduced-ring split/merge designs,
   and framework-coordinate stability.  Any claimed convergence or optimal
   construction there is currently `CONJECTURE` unless supplied by an
   external theorem with checked hypotheses.

The central publication candidate is Theorem A and its positive structural
rigidity.  Local/global feasibility, exact and quantitative equality rigidity,
the sharp product-graph minimax theorem, the constrained extremal lower bound,
and feasible-family anisotropy form the supporting hierarchy.
