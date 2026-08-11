# Priority boundary and hostile-referee audit

**Scope.** This audit compares the Paper-I theorem package with the named primary
sources M1--M11 and with the finite-frame result most likely to be invoked against
the equality theorem.  It is deliberately adversarial: the question is not whether
the cited papers use the same project terminology, but whether their mathematical
variables, hypotheses, and conclusions already contain the proposed contribution.
The audit uses the accepted P1A--P1E theorem sources and registries as evidence of
the internal theorem package.  It does **not** treat a stage report, test, or registry
entry as a substitute for a proof. The matching construction is assessed from its
accepted ordinary proof and independent hostile audits, not from its stage label.

## 1. Object being compared

The comparison is meaningful only after fixing conventions.  The central finite
object in the manuscript is

\[
  \bigl(I,d,(\Omega_i)_{i\in I},(w_i)_{i\in I},
  (\gamma_{ij})_{i,j\in I}\bigr),
\]

where \(I\ne\varnothing\) is finite, \(d\ge 2\),
\(\Omega_i\in\mathbb S^{d-1}\), \(w_i>0\),
\(\sum_iw_i=1\), and
\(\gamma_{ij}=\gamma_{ji}\ge0\).  With
\(a_{ij}=\gamma_{ij}/w_i\),

\[
  (Lf)_i=\sum_j a_{ij}(f_j-f_i),\qquad
  r_i=\sum_j a_{ij},\qquad r_{\max}=\max_i r_i .
\]

Thus \(L\) is negative semidefinite in \(\ell^2(w)\), has nonnegative
off-diagonal jump rates, and satisfies detailed balance.  The exact first-harmonic
constraint is

\[
   L\mathbf 1=0,\qquad L\Omega=-(d-1)\Omega .
\]

For \(A\in\operatorname{Sym}_0(d)\), set

\[
  (S_2A)_i=\Omega_i^{\!T}A\Omega_i,
  \qquad K_X=\ker S_2,
  \qquad R_2=(L+2dI)S_2 .
\]

The defect \(\mathfrak D_2\) is the operator norm of the induced map on
\(\operatorname{Sym}_0(d)/K_X\), equipped with the **sampled** norm
\(\|[A]\|=\|S_2A\|_{\ell^2(w)}\), into the whole sample space
\(\ell^2(w)\).  It is not the Frobenius coefficient norm and it does not assume
that \(S_2\) is injective or that \(\operatorname{im}S_2\) is invariant under
\(L\).

The accepted hierarchy being tested for priority is:

1. the exact covariance/two-defect identity of P1A;
2. the finite sharp frontier
   \(\mathfrak D_2r_{\max}\ge d(d-1)\) of P1B;
3. the equality equivalence, including local centered weighted unit-norm tight
   frames and the global reversible assembly conditions, of P1C;
4. the normalized near-equality budget and its explicitly conditional local,
   edgewise, graphwise, quotient, and frame-repair consequences of P1D; and
5. the P1E local positive reversible matching families in `d=2,3`, with exact
   \(H_1\), \(r_{\max}=O(h^{-2})\), and
   \(\mathfrak D_2=O(h^2)\).

No novelty claim should be based on the phrase “AFP,” which has no mathematical
priority content.

## 2. Primary-source comparison matrix

In the last column, “context only” means that no theorem from that source is needed
to prove P1A--P1E. The accepted construction is internally derived; any later
construction that imports an external result inherits the stated transfer checks.

| Source | Variables and hypotheses in the source | External conclusion actually verified | Genuine overlap | Precise distinction of the present theorem package | Hypothesis and convention transfer note |
|---|---|---|---|---|---|
| **M1. Babecki--Thomas, _Graphical Designs and Gale Duality_** [[arXiv:2204.01873](https://arxiv.org/abs/2204.01873)] | A connected regular unweighted graph; an ordering of graph eigenspaces for a normalized-adjacency convention; a proper vertex subset with separate quadrature weights. | Positively weighted graphical designs are identified, through Gale duality, with faces of a generalized eigenpolytope; this gives organization and support-size bounds for designs. | Both works use finite graph eigenspaces, positive weights, and exact finite-dimensional identities.  Cubes and other Cayley graphs occur in both collections of examples. | A graphical-design weight is a **node-sampling/quadrature weight** on a fixed graph.  Here \(w\) is a stationary measure and \(\gamma\) is a shared edge conductance defining the operator.  P1A--P1E do not select a proper subset that averages graph eigenvectors.  M1 has no spherical coordinate eigenmap, sampled \(H_2\) quotient, rate cap, sharp product, equality frame theorem, near-extremizer estimate, or matching shared-stress family. | Do not identify the M1 quadrature weights with either \(w_i\) or \(\gamma_{ij}\).  M1's uniform global graph average and regularity are material.  Translate its positive-semidefinite graph convention before comparing signs.  **Context only.** |
| **M2. Babecki--Shiroma, _Eigenpolytope Universality and Graphical Designs_** [[arXiv:2209.06349](https://arxiv.org/abs/2209.06349)] | A connected graph with positive **edge** weights and symmetric combinatorial Laplacian \(D-A\) in the uniform Euclidean inner product; an arbitrary ordering of its eigenspaces with \(\operatorname{span}\{\mathbf1\}\) singled out.  Designs have a second, independent set of node quadrature weights. | Any orthogonal decomposition containing \(\operatorname{span}\{\mathbf1\}\) can be realized as the eigenspaces of a connected positively weighted graph; every polytope occurs, up to affine equivalence, as an eigenpolytope.  Positive graphical designs correspond to faces, exist with a support bound, and associated optimization/counting problems have the stated complexity. | This is the strongest algebraic precedent for prescribing a finite eigenspace with positive edge weights.  For uniformly centered spherical coordinates, it can realize their span as an eigenspace, generally on a dense graph. | The universality theorem does not impose the eigenvalue \(d-1\), the unit-sphere representatives without affine change, a prescribed nonuniform stationary measure, locality, bounded degree, a rate cap, or any control of sampled quadratic residuals.  Its design results concern quadrature supports, not generator fidelity.  The P1B constant and P1C--P1D conclusions are absent. | The M2 Laplacian is \(D-A\succeq0\) with null vector \(\mathbf1\); ours is a negative Markov generator in \(\ell^2(w)\).  With nonuniform \(w\), \(-WL\) gives the generalized eigen-equation \((-WL)\Omega=(d-1)W\Omega\), not the ordinary M2 eigen-equation.  Do not cite M2 as a local or sparse existence theorem: the source notes its general construction is dense.  **Context only.** |
| **M3. Steinerberger, _Spectral Limitations of Quadrature Rules and Generalized Spherical Designs_** [[arXiv:1708.08736](https://arxiv.org/abs/1708.08736)] | A compact \(m\)-dimensional Riemannian manifold without boundary; \(n\) nodes; nonnegative quadrature weights; exact integration of the initial Laplace--Beltrami eigenfunctions, counted with multiplicity. | Such a rule integrates at most the first \(c_m n+o(n)\) eigenfunctions, where \(c_m=((m/2)+1)^{(m/2)+1}/\Gamma(m/2+1)\), in particular \(c_2=4\).  The paper also gives a heat-kernel energy inequality under strict positivity. | Both works distinguish continuous harmonic modes from finite samples and impose positivity. | M3 is a cardinality obstruction for exact **integration** of an initial spectral segment.  It neither defines an edge generator nor asks that coordinates be eigenfunctions.  It is not sampling injectivity, not an operator residual on \(\operatorname{Sym}_0(d)/K_X\), and not a finite positivity--stiffness frontier for a selected degree. | Keep manifold dimension \(m=d-1\) separate from the ambient dimension \(d\).  M3 uses the positive spectrum of \(-\Delta\) and manifold volume measure.  Its node weights are quadrature weights, not conductances.  The \(o(n)\) result cannot be converted into a finite P1B constant.  **Context only.** |
| **M4. Izmestiev--Lam, _Discrete Laplacians---Spherical and Hyperbolic_** [[arXiv:2408.04877](https://arxiv.org/abs/2408.04877); [JLMS](https://doi.org/10.1112/jlms.70235)] | A geodesically triangulated spherical surface, hence intrinsically two-dimensional and embedded through vertices \(p_i\in\mathbb S^2\).  Symmetric edge coefficients \(c_{ij}\) are explicit functions of the adjacent spherical triangles, and \(d_i=\sum_jc_{ij}\sin^2(\lambda_{ij}/2)\).  The normalized operator is \((\Delta_su)_i=d_i^{-1}\sum_jc_{ij}(u_j-u_i)\). | Local Delaunay is equivalent to \(c_{ij}\ge0\) (with equality at cocircular degeneracy).  Their Lemma 2.2 gives \(\sum_jc_{ij}(p_j-p_i)=-2d_ip_i\), so **the three coordinate functions satisfy \(\Delta_sp=-2p\) exactly**.  They also characterize \(-2\)-eigenfunctions through discrete conformal/isometric deformations. | This source already supplies local, reversible, positive (under Delaunay), coordinate-exact spherical generators in the manuscript's \(d=3\) sign convention.  It is direct prior art, not merely motivational geometry. | It does not state the sampled quadratic quotient, two-defect trace identity, \(\mathfrak D_2r_{\max}\ge6\), equality characterization, stability theorem, or an all-dimensional matching family.  A triangulation alone gives neither a uniform maximum-degree bound nor the shape regularity and strict positivity margins needed for a P1E asymptotic theorem. | This transfer must be line-by-line.  If \(c_{ij}\ge0\) and \(d_i>0\), set \(w_i=d_i/\sum_kd_k\), \(\gamma_{ij}=c_{ij}/\sum_kd_k\); then \(a_{ij}=c_{ij}/d_i\) and \(L=\Delta_s\).  Verify closed/no-boundary triangulation, nondegenerate spherical triangles, local Delaunay, positivity of every \(d_i\), connectivity, edge-length range, and the exact scaling above.  Do **not** claim that this manuscript introduces positive coordinate-exact spherical Laplacians. |
| **M5. Seibold, _Minimal Positive Stencils in Meshfree Finite Difference Methods for the Poisson Equation_** [[arXiv:0802.2674](https://arxiv.org/abs/0802.2674); [journal DOI](https://doi.org/10.1016/j.cma.2008.09.001)] | A Euclidean point cloud around a center; local coefficients exact on constants, linear polynomials, and the quadratic moments required for the Poisson operator.  “Positive” means nonnegative off-center stencil coefficients.  Stencils are obtained row by row by linear programming. | Basic feasible LP solutions give minimal positive stencils; the paper proves a necessary half-space obstruction and geometric sufficient cone criteria in dimensions two and three.  It explicitly observes that a meshfree global matrix is generally nonsymmetric. | The local moment equations, positivity cone, sparse basic solutions, and tangent-space interpretation are close to ingredients one might use in P1E or in the local equality theorem. | Local row feasibility is not shared-edge feasibility.  Seibold does not produce \(w_i a_{ij}=w_ja_{ji}\), a spherical coordinate eigenvalue, global stationary masses, or a coupled family satisfying all rows simultaneously.  It has no sampled harmonic quotient, sharp \(\mathfrak D_2r_{\max}\) constant, or equality/stability theorem. | Match the sign carefully: Seibold's off-center coefficients have the same sign as ours, while his central coefficient is their negative sum.  Taylor exactness is in Euclidean coordinates and must be transported to a tangent chart with curvature remainders.  A P1E proof may use his local cone criterion only after separately proving global reversible reconciliation and a quantitative interior margin. |
| **M6. Babecki--Steinerberger--Thomas, _Spectrahedral Geometry of Graph Sparsifiers_** [[arXiv:2306.06204](https://arxiv.org/abs/2306.06204)] | A fixed connected undirected positive-edge-weighted graph \(G\), its positive-semidefinite Kirchhoff Laplacian \(L_G=D-A\), and the first \(k\ge2\) ordered orthonormal eigenpairs.  A candidate is a positive reweighting of a spanning subgraph with no new edges. | The set of subgraph Laplacians preserving those first \(k\) eigenpairs is a convex polyhedron/spectrahedron.  Theorem 3.1 gives \(L=\Phi_k\Lambda_k\Phi_k^T+\lambda_k\Phi_{>k}\Phi_{>k}^T+\Phi_{>k}Y\Phi_{>k}^T\), with \(Y\succeq0\) and the edge/nonedge sign equations. | Exact low-eigenpair preservation with positive edge weights is plainly adjacent.  A convex program for a uniform-mass coordinate eigenspace can be expressed as a related affine slice. | M6 starts from a base graph and preserves its **entire first ordered spectral segment**.  The present theorem prescribes a geometric coordinate subspace and continuous target eigenvalue, allows aliases in a sampled quadratic shell, and optimizes a different residual under \(r_{\max}\).  M6 contains no universal product lower bound, local moment equality, near-extremizer budget, or continuum matching result. | For uniform \(w\), \(-L\) is a rescaled Kirchhoff Laplacian and comparison is direct after a sign flip.  For nonuniform \(w\), \(-WL\) is symmetric Kirchhoff but satisfies a generalized eigenproblem with mass matrix \(W\); \(-W^{1/2}LW^{-1/2}\) is symmetric but no longer has ordinary null vector \(\mathbf1\).  Multiplicity matters: preserve whole eigenspaces unless a basis is intentionally fixed.  Do not describe positive eigenpair-preserving graph optimization itself as new. |
| **M7. García Trillos--Gerlach--Hein--Slepčev, _Error Estimates for Spectral Convergence of the Graph Laplacian on Random Geometric Graphs_** [[arXiv:1801.10108](https://arxiv.org/abs/1801.10108); [Foundations of Computational Mathematics 20 (2020)](https://link.springer.com/article/10.1007/s10208-019-09436-w)] | A compact connected \(m\ge2\) dimensional boundaryless submanifold of Euclidean space with controlled curvature, injectivity radius, and reach; an i.i.d. sample from a Lipschitz density bounded above and below; a nonnegative compactly supported kernel and a shrinking bandwidth satisfying quantitative sampling/geometric conditions. | Eigenvalues and suitably extended eigenvectors of several graph Laplacians converge, with explicit high-probability rates, to a weighted Laplace--Beltrami operator.  The abstract records the optimized rate \(O((\log n/n)^{1/(2m)})\). | Both works concern local positive graph Laplacians on sampled manifolds and compare finite spectra with the continuum Laplacian. | M7 is probabilistic asymptotic spectral convergence.  It neither exactly reproduces the coordinate eigenfunctions at finite \(n\) nor supplies bounded degree, a shared exact \(H_1\) correction, the P1A quotient, the P1B finite sharp constant, or P1C--P1D rigidity.  Its rate is not the same error metric as \(\mathfrak D_2=O(h^2)\). | Any imported rate must retain the i.i.d. model, density, kernel regularity/support, bandwidth window, curvature/reach/injectivity, probability, sign, and normalization.  Do not compare exponents until identifying whether \(h\) means kernel radius, fill distance, or the paper's mesh parameter.  **Context only unless P1E explicitly invokes it.** |
| **M8. Martin--Tanaka, _Commutative Association Schemes_** [[arXiv:0811.2475](https://arxiv.org/abs/0811.2475)] | A finite set \(X\) whose pair relations form a commutative association scheme; adjacency matrices span the Bose--Mesner algebra; the standard counting inner product is uniform. | The Bose--Mesner algebra has primitive idempotents; ordinary and Schur products are governed by intersection and nonnegative Krein parameters.  The survey develops embeddings, codes, designs, and semidefinite methods in this setting. | Many symmetric exact examples in P1C (cube, Hamming-type families, distance-regular shells) can be organized in Bose--Mesner idempotents; Schur products explain why products of low modules split into a few modules. | An association scheme is a symmetry/algebra package, not a theorem that a chosen spherical embedding has the manuscript's continuous harmonic eigenvalues.  Arbitrary positive masses and conductances generally leave the scheme category.  M8 does not prove the quotient trace inequality, sharp rate product, arbitrary-weight equality converse, or stability. | Use an association-scheme decomposition only after proving that the generator lies in the Bose--Mesner algebra and identifying each idempotent with the actually sampled spherical harmonic module.  Uniform counting measure is material.  Sampling kernels can collapse a nominal harmonic module.  **Context/example organization only.** |
| **M9. E. Bannai--E. Bannai, _A Survey on Spherical Designs and Algebraic Combinatorics on Spheres_** [[DOI](https://doi.org/10.1016/j.ejc.2008.11.007)] | A finite nonempty subset \(X\subset\mathbb S^{d-1}\), conventionally with uniform node weights, and polynomial/harmonic exactness through degree \(t\). | A spherical \(t\)-design is characterized by equality of uniform finite and spherical averages for degree-\(\le t\) polynomials, equivalently by vanishing harmonic moments of degrees \(1,\ldots,t\); the survey develops Fisher bounds, tight designs, and links to association schemes. | The same regular simplices, cross-polytopes, cubes, and Platonic configurations occur; moment matrices and tight-frame language overlap strongly with P1C examples. | A node set can be a spherical design without carrying any graph or generator.  Conversely, exact \(L\Omega=-(d-1)\Omega\) and frontier equality do not imply degree-two quadrature exactness.  P1A deliberately allows arbitrary stationary \(w\), sampled aliases, and no \(t\)-design assumption. | Never infer \(S_2\) injectivity, \(L(\operatorname{im}S_2)\subseteq\operatorname{im}S_2\), or exact \(H_2\) reproduction from a design slogan.  State whether weights are uniform or weighted cubature weights.  Tight-design lower bounds are cardinality statements, not rate bounds.  **Context/example checks only.** |
| **M10. Ahrens--Beylkin, _Rotationally Invariant Quadratures for the Sphere_** [[DOI](https://doi.org/10.1098/rspa.2009.0104)] | Spherical quadrature rules invariant under the icosahedral rotation group; orbit parameters and quadrature weights are chosen to integrate a prescribed rotationally invariant polynomial/harmonic space. | The paper constructs near-optimal icosahedrally invariant quadratures integrating the targeted functions, using symmetry to reduce the moment system. | Icosahedral orbits, invariant harmonic calculations, and exact quadrature tests are relevant to P1C examples and possible P1E symmetry-orbit constructions. | These are node quadratures, not edge-conductance generators.  Orbit exactness neither supplies a local graph nor proves positivity/reversibility of jump rates, exact coordinate action, the sampled quotient residual, or the sharp frontier. | Keep the quadrature weights separate from stationary masses and conductances.  A symmetry average preserves feasibility only after the graph support and orientation constraints are invariant.  Cite the paper for orbit quadrature precedent, not for a generator theorem.  **Context/example construction only.** |
| **M11. Yoon, _Graph Laplacians with Higher Accuracy_** [[arXiv:2504.04461](https://arxiv.org/abs/2504.04461)] | A simple graph and an \(m\)-Laplacian inspired by the centered \(2m\)-order finite-difference formula on a one-dimensional periodic grid.  On general graphs, powers/walk counts of the adjacency matrix define the operator. | The cycle operator has formal accuracy order \(2m\).  The coefficients \(a_{k,m}=(-1)^{k+1}2\binom{2m}{m-k}/(k^2\binom{2m}{m})\) alternate for \(m\ge2\); the resulting object is explicitly a weighted **signed** graph.  The paper studies spectra and cospectrality. | It is direct title-level prior art for “higher-accuracy graph Laplacians” and illustrates how cancellation by negative weights permits higher formal order. | The manuscript studies a different obstruction: nonnegative reversible spherical jump rates, exact degree one, and worst sampled degree-two residual under a rate cap.  It does not claim that every signed high-order graph formula is impossible. | Do not use “the first higher-accuracy graph Laplacian” or an unqualified “positivity prevents higher accuracy.”  State the exact positivity class, target shell, sampling quotient, and rate constraint.  The M11 accuracy statement is one-dimensional cycle consistency, not spherical \(\mathfrak D_2\).  **Context/contrast only.** |
| **F1. Benedetto--Fickus, _Finite Normalized Tight Frames_** [[DOI](https://doi.org/10.1023/A:1021323312367)] | Finite collections of unit vectors in a finite-dimensional real or complex Hilbert space; the frame operator and frame potential. | Unit-norm tight frames are the global minimizers of the frame potential, and the paper develops their finite-dimensional structure. | The equality rows in P1C are centered weighted unit-norm tight frames in \(T_{\Omega_i}\mathbb S^{d-1}\); isotropic second moments and frame-operator whitening are standard frame notions. | The novelty cannot be the definition or existence of tight frames.  The potentially new statement is that **simultaneous equality in the positive reversible spherical generator frontier is equivalent to a particular centered tangent-frame condition plus common loss/rate and global detailed-balance compatibility**, and that the residual then obeys the exact sampled-quotient identity. | Cite frame literature when naming tight frames, frame potentials, or whitening.  The P1D weighted repair constants must remain derived in the manuscript unless a precisely matching weighted stability theorem is imported.  Do not attribute global spherical assembly to local frame theory. |

## 3. The strongest restatement attacks

### 3.1 “This is Izmestiev--Lam with a new defect functional”

This attack succeeds against any claim that the paper introduces positive,
reversible, local, coordinate-exact spherical Laplacians.  M4 already has exactly
that package on geodesic triangulations of \(\mathbb S^2\): symmetric \(c_{ij}\),
positive \(d_i\), the negative normalized sign, Delaunay nonnegativity, and
\(\Delta_sp=-2p\).

The attack does **not** dispose of P1A--P1E. To make that distinction visible, the
introduction must state M4's coordinate identity explicitly and then identify the
new object as the sampled quadratic residual and its sharp rate frontier over the
larger class of all positive reversible coordinate-exact generators.  The P1E
construction is not obtained by transferring M4: its adaptive shared stress,
uniform mesh hypotheses, positivity margins, rate/degree bounds, and
\(O(h^2)\) quotient estimate are proved internally and are not stated by M4.

**Required revision.** Place the M4 comparison in the introduction, not only in a
related-work appendix.  Delete “first positive spherical Laplacian,” “new exact
coordinate Laplacian,” and equivalent formulations.

### 3.2 “This is an eigenpair-preserving sparsifier problem”

M6 makes this objection serious in the uniform-mass case: exact preservation of a
specified graph eigenspace with positive edge weights is established terrain, and
its feasible set has a convex spectral description.  M2 is even broader about
realizing arbitrary orthogonal eigenspace decompositions by positive weighted
graphs.

The rebuttal is mathematical, not terminological.  The manuscript does not start
with a base graph whose first \(k\) eigenpairs are to be retained; it prescribes the
geometric coordinate module and measures the failure at the next continuous
harmonic degree, after quotienting sampling aliases.  The universal inequality
\(\mathfrak D_2r_{\max}\ge d(d-1)\), its equality conditions, and its stability
budget are not consequences stated by M2 or M6.  With unequal \(w\), the relevant
equation is generalized rather than an ordinary combinatorial eigenproblem.

**Required revision.** Cite M2 and M6 before describing any convex feasibility
formulation.  Claim novelty for the sharp constrained frontier and its geometry,
not for exact eigenpair constraints, positive Laplacian cones, or spectrahedral
parameterizations.

### 3.3 “This is positive stencil theory plus a frame-potential equality case”

M5 supplies the local positive moment-cone viewpoint, and F1 supplies the tight
frame vocabulary.  Consequently, neither “positive local stencils exist under a
cone condition” nor “isotropic unit vectors form a tight frame” is a defensible
stand-alone contribution.

What remains distinctive is the exact route from spherical coordinate reproduction
to the radial--mixed--tangent covariance split, the way positivity and the rate cap
force a nonzero quadratic residual, the sharp all-dimensional constant, and the
simultaneous **global** detailed-balance constraints.  Seibold explicitly warns that
rowwise meshfree matrices are generally nonsymmetric, which directly supports the
manuscript's refusal to infer global reversibility from local stencils.

**Required revision.** Attribute the stencil and tight-frame concepts.  State the
new equality theorem as an equivalence for the globally reversible generator, not
as the discovery of tight frames.

### 3.4 “This is spherical-design theory in operator language”

M1--M3 and M8--M10 make this a plausible superficial reading because the same
high-symmetry configurations and harmonic spaces recur.  It becomes a valid
criticism if the manuscript conflates stationary masses, conductances, and
quadrature weights, or if it calls \(\mathfrak D_2=0\) “degree-two design exactness.”

The decisive distinction is that a design is a measure identity, while the present
problem is an operator identity.  The quotient by \(K_X\) is also essential: a
nonzero quadratic form can vanish at every node, so algebraic harmonic dimension
does not equal sampled dimension.  Frontier equality yields
\(R_2=cS_2\), with \(c>0\), on the genuinely sampled quotient; it does **not**
yield exact \(H_2\) reproduction.

**Required revision.** Reserve “design” for the established quadrature meaning.
Use “sampled harmonic quotient” and spell out \(K_X\).  Include the exact
tetrahedral, octahedral, and cubical aliases in the main examples or an immediately
visible warning.

### 3.5 “The asymptotic result is standard graph-Laplacian convergence”

M7 already proves graph-Laplacian spectral convergence on random geometric graphs
under detailed geometric and probabilistic assumptions.  Therefore, no paper may
claim the first convergence of positive graph Laplacians to a manifold Laplacian,
or infer the claimed \(O(h^2)\) result from generic consistency literature.

The accepted P1E result is different because it is finite-level and exact
where promised: exact \(L_h\Omega=-(d-1)\Omega\), shared nonnegative
conductances, bounded degree, a deterministic rate cap, and a uniform sampled
quadratic quotient estimate with proved constants.  A fitted slope or a theorem
about eigenvalue convergence does not establish that package.

**Required revision.** State the mesh model, the meaning of \(h\), and the error
functional before citing convergence rates. The abstract may state P1E only with
its proved `d=2,3` scope and exact constants.

### 3.6 “The paper overstates a positivity barrier to high order”

M11 constructs signed high-order graph formulas.  The present lower bound is fully
compatible with that work: it concerns a nonnegative reversible class and one
specific sampled quadratic target under a maximum-rate constraint.  It does not
say that signed graph Laplacians cannot be high order, nor that no other positive
discretization can have a different consistency notion.

**Required revision.** Avoid a universal “no high order without negativity” slogan.
A correct formulation is: within the defined positive reversible coordinate-exact
class, the sampled degree-two residual and maximum jump rate satisfy the stated
sharp product bound.

## 4. Defensible novelty boundary

The focused corpus supports the following judgment.

### 4.1 Flagship contribution that survives the audit

Subject to the internal proofs passing their separate proof audits, the defensible
flagship theorem is the **combined finite frontier/equality/stability theorem**:

> For every finite positive reversible generator on sampled points of
> \(\mathbb S^{d-1}\) that reproduces constants and coordinates with the
> continuum eigenvalue, the genuinely sampled degree-two residual satisfies
> \(\mathfrak D_2r_{\max}\ge d(d-1)\).  Equality is characterized by an
> exact local covariance/tangent-frame system together with the global
> reversible compatibility conditions, and small product slack controls an
> explicit weighted sum of the same defects.

None of M1--M11 or F1 states this theorem, its constant, its alias-correct quotient,
or its equality and stability package.  That observation is a **focused-corpus
comparison**, not a universal first-in-literature claim.

The mathematical center should be the product bound, not the existence of positive
generators, exact coordinate eigenspaces, positive stencils, tight frames,
quadrature designs, or convex Laplacian cones; all of those have strong prior art.

### 4.2 Supporting results whose novelty must be phrased narrowly

| Internal result | Priority-safe description | Description to avoid |
|---|---|---|
| P1A quotient and two-defect identity | “We derive an exact, alias-correct covariance factorization for the sampled quadratic residual in this generator class.” | “We introduce quotient operators/generalized eigenvalues/covariance decompositions.” |
| P1B frontier | “We prove the sharp universal product \(\mathfrak D_2r_{\max}\ge d(d-1)\), including all-dimensional attainment.” | “Positive graph Laplacians cannot be accurate.” |
| P1C equality | “We characterize equality by common rate/loss, local centered tangent tight frames, and global detailed-balance assembly; exact aliases are retained.” | “We discover tight-frame stencils,” “all equality cases are Platonic,” or “equality reproduces \(H_2\).” |
| P1D stability | “We give a quantitative weighted defect budget and conditional consequences with every mass, conductance, path/gap, frame, and sampling parameter displayed.” | “Every near extremizer is close to a Platonic solid” or any parameter-free pointwise/global rigidity claim. |
| P1E construction | “In `d=2,3`, we construct deterministic local positive reversible coordinate-exact families attaining the lower-bound order under the listed mesh hypotheses.” | “We introduce positive spherical Delaunay Laplacians,” “standard consistency gives \(O(h^2)\),” a `d>3` construction, or any claim based on fitted slopes. |

### 4.3 Claims that are not earned by P1A--P1E

The current accepted package does not by itself earn any of the following:

- a matching-order construction in ambient dimension `d>3`;
- a first construction of local positive coordinate-exact Laplacians on
  \(\mathbb S^2\);
- an unrestricted classification of equality generators as Platonic;
- coefficient recovery on \(\operatorname{Sym}_0(d)\) when \(K_X\ne0\);
- exact reproduction of a nonzero sampled \(H_2\) mode at frontier equality;
- a pointwise, per-edge, or global geometric stability theorem without the
  explicit \(w_{\min}\), edge-probability, graph-gap/path/resistance, tangent-frame,
  feature-overlap, and sampling-gap hypotheses from P1D;
- a theorem about transport discretizations, diffusion accuracy, semigroup error,
  or physical models not contained in the generator/harmonic statement;
- a universal prohibition on signed high-order formulas.

## 5. Terminology audit

| Term | Referee risk | Required usage |
|---|---|---|
| **positive** | In M1--M3 and M10 it may mean nonnegative quadrature weights; in M2/M6 it means positive edge weights; in M5 it means positive off-center stencil entries. | At first use write “nonnegative off-diagonal rates, equivalently nonnegative shared conductances.”  Name quadrature weights separately. |
| **reversible** | Can be mistaken for mere matrix symmetry. | Define \(w_ia_{ij}=w_ja_{ji}\) and identify the self-adjoint space \(\ell^2(w)\). |
| **spherical generator** | “Generator” fixes the negative Markov sign, while geometric Laplacian literature often uses the positive sign. | Display \( (Lf)_i=\sum_ja_{ij}(f_j-f_i)\) immediately. |
| **stiffness** | In finite elements, a stiffness matrix is \(-WL\), whereas the manuscript uses a scalar rate cap. | Prefer “maximum outgoing rate \(r_{\max}\)” in theorem statements; if “stiffness” remains in exposition, define it as \(r_{\max}\). |
| **quadratic fidelity/defect** | May be read as coefficient-space approximation or degree-two cubature. | Say “sampled degree-two residual on \(\operatorname{Sym}_0(d)/K_X\)” and give the norm. |
| **\(H_2\) error** | Hides sampling aliases and possible leakage out of \(\operatorname{im}S_2\). | Use “sampled \(H_2\) quotient residual into the whole sample space.” |
| **equality/extremizer** | Readers may assume exact \(H_2\) reproduction. | State \(R_2=cS_2\) with \(c=d(d-1)/r_{\max}>0\); equality is extremal nonzero residual. |
| **higher accuracy/order** | M11 and classical finite differences already own this general phrase; an \(O(h^2)\) quotient bound is not automatically a full truncation-error order. | Attach the metric and target: “second-order sampled quadratic fidelity under \(r_{\max}=O(h^{-2})\).” |
| **design** | Established meaning is a node quadrature identity. | Do not rename the generator class a design.  Use “design” only when a separate quadrature hypothesis is proved. |
| **AFP** | Project-local term with no independent mathematical content and a priority distraction. | Omit from title, abstract, theorem names, and novelty claims.  If retained for software history, confine it to reproducibility records. |

Recommended neutral title vocabulary is “positive reversible spherical generators,”
“sampled harmonic quotients,” and “sharp rate--quadratic-fidelity frontier.”

## 6. External-theorem transfer ledger

The central P1A--P1E proofs should remain internally complete. If a theorem from
the comparison corpus is imported elsewhere, the manuscript must include the
following note at the point of use.

| Imported source | Minimum transfer note |
|---|---|
| M1/M2 graphical designs | Identify graph operator, eigenspace ordering, uniform global average, graph edge weights, and separate design quadrature weights.  Explain why the selected entire eigenspaces, not a basis fragment, are averaged. |
| M2 universality | Verify uniform orthogonality to \(\mathbf1\), sign/scaling, positivity of every constructed edge, whether the result is dense, and whether affine equivalence preserves the required unit spherical embedding (generally it does not). |
| M3 spectral quadrature limit | Set manifold dimension \(m=d-1\); retain compact/no-boundary and nonnegative-weight assumptions; count eigenfunctions with multiplicity; do not replace the asymptotic (o(n)) by a finite bound. |
| M4 spherical Delaunay Laplacian | Give the exact \(c_{ij}\) and \(d_i\); verify geodesic closed triangulation, local Delaunay, nondegeneracy, \(d_i>0\), connectivity, sign, and the normalization \(w_i=d_i/\sum d\), \(\gamma_{ij}=c_{ij}/\sum d\).  Derive \(L\Omega=-2\Omega\) from their equation, not from analogy. |
| M5 positive stencil | State the Euclidean polynomial exactness system and sign; verify the local point-cloud cone criterion in the chosen tangent coordinates; supply curvature/Taylor errors; separately prove shared-edge detailed balance and positivity after any correction. |
| M6 sparsifier spectrahedron | State whether \(w\) is uniform.  If not, use the mass-matrix generalized eigenproblem and do not apply the ordinary Kirchhoff theorem without a proved equivalence.  Preserve whole repeated eigenspaces and verify that no forbidden edges are created. |
| M7 graph convergence | Retain sampling distribution, density bounds/regularity, kernel assumptions, bandwidth window, manifold geometry, probability level, normalization, and the precise eigenvalue/eigenvector metric.  Do not transfer its rate to \(\mathfrak D_2\) without a new argument. |
| M8 association schemes | Exhibit the relations and Bose--Mesner membership of the operator; retain uniform measure; identify primitive idempotents with the actual sampled harmonic images and compute sampling kernels. |
| M9 spherical designs | State uniform versus weighted design convention, polynomial degree, and harmonic normalization.  Use it for moment integration only, not generator invariance or injectivity. |
| M10 invariant quadratures | State the finite rotation group, orbit stabilizers, invariant test space, and quadrature weights.  Prove separately that a proposed graph support/conductance cone is invariant and positive. |
| M11 signed high-order Laplacians | State the one-dimensional cycle setting for the formal order and retain the alternating/sign-changing weights.  Do not compare its “accuracy” with \(\mathfrak D_2\) without mapping the metrics. |
| F1 finite tight frames | State unit versus weighted frame normalization and tangent dimension \(d-1\).  Treat local frame existence/whitening as frame theory; prove centeredness, spherical neighbor realization, positivity margins, and global reversibility separately. |

## 7. Referee verdict and publication conditions

**Verdict: potentially publishable after major priority-facing revision.**  The
focused primary-source audit does not reduce the sharp finite
positivity--rate--sampled-quadratic-fidelity frontier, its exact equality system, or
its quantitative stability budget to any named prior theorem.  It does, however,
invalidate several broader narratives that a draft might be tempted to use.

Acceptance should require all of the following.

1. The abstract leads with the explicit product theorem and its equality/stability
   structure, not with “a new discrete spherical Laplacian.”
2. Izmestiev--Lam's exact coordinate identity and Delaunay positivity are stated
   accurately and prominently.
3. Graphical designs, spherical designs, stationary masses, and edge conductances
   are never conflated.
4. Eigenpair-preserving convex graph theory and local positive stencil theory are
   credited before the manuscript presents related feasibility programs.
5. Tight frames are treated as established structure; the claimed contribution is
   the equivalence with global frontier equality and reversible assembly.
6. Every theorem involving \(H_2\) states the sampling quotient and permits leakage
   into the full sample space.
7. The stability theorem keeps every parameter demanded by its conclusion; no
   weighted-average statement is rewritten as parameter-free geometric rigidity.
8. The asymptotic upper theorem remains restricted to `d=2,3` and retains the
   exact \(H_1\), positivity, reversibility, locality, degree/rate, all-orders
   remainder, and sampling-quotient hypotheses proved for the unperturbed P1E
   family.  The open perturbation route is not cited as a theorem.
9. Transport or application relevance is presented as motivation or future work
   unless a separate transfer theorem is proved.
10. “First,” “unprecedented,” and “the only” claims are omitted unless supported by
    a broader documented search than the focused corpus permitted here.

With these revisions, the priority boundary is defensible: the paper is not a claim
to have invented positive stencils, Delaunay Laplacians, designs, tight frames,
eigenpair-preserving graph cones, graph-Laplacian convergence, or signed high-order
operators.  Its central claim is the new exact relation among positivity, maximum
jump rate, and alias-correct sampled quadratic fidelity, together with the complete
extremal and near-extremal geometry and the matching local families in `d=2,3`.

## 8. Internal provenance and audit boundary

The comparison above was checked against the accepted internal statements in:

- `docs/publication_program/P1A_STAGE_REPORT.md` and the P1A theorem sources named
  there;
- `docs/publication_program/P1B_STAGE_REPORT.md` and the P1B theorem sources named
  there;
- `docs/publication_program/P1C_STAGE_REPORT.md` and the P1C theorem sources named
  there;
- `docs/publication_program/P1D_STAGE_REPORT.md` and the P1D theorem sources named
  there;
- `docs/publication_program/P1E_STAGE_REPORT.md` and the P1E construction and
  hostile-audit sources named there;
- `docs/publication_program/THEOREM_REGISTRY.md`;
- `docs/publication_program/PAPER_BOUNDARY_MATRIX.md`; and
- `docs/publication_program/PRIOR_ART_MATRIX.md`.

This document is a priority and hypothesis-transfer audit, not a replacement for
any mathematical proof.  In particular, a theorem marked “proved” in a registry was
compared as a claimed internal result; its correctness remains attached to its one
authoritative proof source and independent proof audit.  Likewise, computational
fixtures can falsify claims and test exact identities but cannot establish an
all-level construction or an all-dimensional theorem.
