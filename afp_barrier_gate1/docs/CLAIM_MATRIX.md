# AFP mathematical claim matrix

Only PROVED, EXTERNAL, COMPUTATIONAL, CONJECTURE, and REJECTED are claim
labels. Lean and exact scripts verify proofs or finite instances; they are not
novelty evidence.

## Foundational and Prompt 1 claims

| Claim | Status | Support and publication boundary |
|---|---|---|
| Finite jump generators satisfy the carré-du-champ product identity | PROVED | SpectralProductAlgebra.lean; standard foundational algebra |
| \(\lambda^2\le\text{rate}\times\text{peak defect}\) | PROVED | Quantitative.lean and LossVariance modules; standard weighted Cauchy--Schwarz |
| The rate-defect gap is a weighted edge-loss variance | PROVED | LossVariance.lean; foundational sharpness identity |
| For nonempty finite \(I\) and \(d>1\), complete coordinate and trace-free quadratic exactness is impossible for a nonnegative unit spherical eigenmap with \(L\Phi=-(d-1)\Phi\) | PROVED | positive radial covariance obstruction; AFP-specific corollary, priority review still required |
| A centered positive quadrature admits a dense positive reversible coordinate-exact operator | PROVED | CompleteGraph.lean and Prompt 1 Theorem 4.2 |
| Positive spherical Delaunay families attain the natural inverse-square rate scale | EXTERNAL | published spherical Delaunay Laplacian theory plus project loss bounds |
| The project's quasi-uniform family is globally minimax or spectrally optimal | CONJECTURE | no minimax theorem; do not claim |
| Only \(K\in\{4,6,12\}\) can have global \(Q=1\) | REJECTED | cube and dodecahedron |
| Connected reversible equality rows propagate one common active loss and row rate | CONJECTURE | reserved for Prompt 3; requires its complete propagation proof |
| Only tetrahedral, octahedral, and icosahedral triangulations satisfy global \(Q=1\) | CONJECTURE | only under future explicit triangulation and embedding hypotheses |
| Non-antipodal local feasibility is equivalent to origin membership in the indexed tangent hull | PROVED | Prompt 1 exact local/global package |
| Strict positivity on every indexed non-antipodal edge is equivalent to tangent-hull relative interior | PROVED | Prompt 1, including repetitions and lower-dimensional span |
| Local row uniqueness is equivalent to a singleton normalized dependence polytope | PROVED | exact dependence/row bijection |
| Pure and mixed antipodal feasibility is a separate normal-budget simplex | PROVED | division-free Prompt 1 parameterization |
| \(\rho>0\), \(\beta_*>0\), and strict local feasibility are equivalent with the stated coefficient bound | PROVED | constructive Prompt 1 proof |
| Local exact rows have inverse-quadratic rate bounds under positive quasi-uniform angle constants | PROVED | Prompt 1 Theorem 3.3; positivity of the lower constant is mandatory |
| The local balance matrix has the stated singular-value and right-inverse bounds | PROVED | Prompt 1 Theorem 3.5 |
| Strict local feasibility persists under the transported-span perturbation bound | PROVED | Prompt 1 Theorem 3.4; endpoint motion alone is insufficient in changing lower dimension |
| Local row feasibility implies sparse global reversible shared-edge feasibility | REJECTED | centered unequal-mass four-cycle and weighted cube certificates |
| Weighted centering is sufficient on every permitted graph | REJECTED | same sparse shared-edge obstructions |
| Centering is necessary on every graph and sufficient on the complete graph | PROVED | block-sum proof and CompleteGraph.lean |
| Global reversible feasibility is shared-edge cone membership and its positive spherical feasible set is compact | PROVED | Prompt 1 Theorem 4.1 |
| Strict shared feasibility is relative-interior membership in the shared-edge cone | PROVED | finite indexed conic theorem |
| Equivariant averaging reconciles local rows when averaged orientations agree | PROVED | Prompt 1 Theorem 4.5 and GroupAveraging.lean |
| The old Lean dual certificate alone is the full Farkas alternative | REJECTED | Lean proves soundness; full finite alternative is an EXTERNAL standard theorem transferred in prose |
| Strict shared feasibility is stable under the stated compatibility and rigidity margins | PROVED | Prompt 1 Theorem 4.6; never omit range/centering compatibility |
| Layered final energy is generally order independent | REJECTED | nonproportional stopping flows need not commute |
| Positivity alone gives standard continuum \(W_2\) contraction | REJECTED | a specified discrete transport metric is required |

## Prompt 2 covariance and representation claims

| Claim | Status | Support and publication boundary |
|---|---|---|
| The quadratic covariance and arbitrary-target formulas hold without positivity or reversibility | PROVED | QUADRATIC_COVARIANCE_THEOREM.md §2 and QuadraticCovariance.lean |
| Nonzero reversible targets force the weighted sample center | PROVED | positive weights, nonempty state set, detailed balance, and \(\mu\ne0\); pointwise residual remains necessary |
| Weighted conservation determines the center at zero target | REJECTED | \(c\) disappears when \(\mu=0\) |
| The sphere residual factors through sampling and genuine dimension is rank \(S\) minus rank \(R\) | PROVED | theorem §3 and sampling formalization |
| Every positive sphere row has a nonzero residual tensor with the stated Frobenius lower bound | PROVED | theorem §4; nonempty finite state set, \(d>1\), nonnegative rates, unit eigenmap with \(L\Phi=-(d-1)\Phi\) |
| Signed one-shell full tangent isotropy forces \(R_X=DS_X\) and no genuine quadratic mode | PROVED | theorem §5; \(d>1\), unit nodes with \(L\Phi=-(d-1)\Phi\), nonempty noncoincident shell, \(0<\ell_i<2\), coincident jumps excluded from shell moments |
| One shell, positivity, connectedness, transitivity, and injective sampling imply the same rigidity without tangent isotropy | REJECTED | positive spherical hexagonal prism has two genuine modes |
| The prism graph/rank/minor data are exact | COMPUTATIONAL | exact_quadratic_covariance_audit.py |
| An equivariant embedding and invariant generator give the multiplicity-free kernel formulas and quotient rank gap | PROVED | theorem §7; \(a_{gi,gj}=a_{ij}\); finite real semisimplicity is EXTERNAL |
| Equivariance alone makes a selected irreducible sampled copy invariant | REJECTED | exact two-layer \(D_3\) counterexample |
| A preserved self-adjoint real irreducible copy carries a scalar action | PROVED | invariant real eigenspaces; do not omit preservation |
| The five natural positive Platonic generators have the recorded ranks and no genuine degree-two mode | PROVED | one-shell theorem plus exact algebraic minors |
| The Platonic finite matrices and minors are exact | COMPUTATIONAL | exact_quadratic_covariance_audit.py |
| Symmetric cube conductances satisfying coordinate target \(-2\) and the full sampled cross-quadratic target \(-6\) have minimum undirected negative mass two | PROVED | arbitrary-feasible cube averaging, orbit lower bound, and KKT |
| The signed-cube finite group, aliases, optimizer, and KKT identities are exact | COMPUTATIONAL | exact_signed_restoration_audit.py |

## Prompt 2 spectral-product claims

| Claim | Status | Support and publication boundary |
|---|---|---|
| Resonant products are equivalent to constant polarized carré du champ | PROVED | finite product identity; no sign assumptions |
| Positive generators forbid every nonzero centered doubled square | REJECTED | exact positive Boolean square |
| Resonant-square semigroup variance is the stated exponential identity | PROVED | finite matrix exponential and derivative converse |
| Positive Markov Jensen variance is nonnegative with support-constancy equality | EXTERNAL | standard Jensen equality; irreducible positivity by uniformization |
| On \(S^2\), \(\operatorname{Sym}^2(H_\ell)=\bigoplus_{r=0}^{\ell}H_{2r}\) | EXTERNAL | Clebsch--Gordan and exchange symmetry |
| The even doubled component occurs at the parity-filtered negative-Pell solutions | EXTERNAL | Pell completeness; project parity transfer and recurrence proved explicitly |
| Pairwise distinct target eigenvalues for scalar restrictions of one common operator force an internal sampled direct sum and rank bound | PROVED | polynomial spectral projections |
| Pairwise distinct degrees suffice in every dimension | REJECTED | \(d=1\) singleton has \(V_0=V_1\); valid for \(d\ge2\) |
| A constants-safe signed converse exists exactly for internally direct target classes | PROVED | zero-target class contains constants once |
| Weighted reversibility of the converse needs only orthogonality among nonconstant sampled spaces | REJECTED | constants must also be orthogonal to all nonzero target spaces |
| The Platonic \(H_2/H_4\) aliases and antipodal orbit ranks are exact | COMPUTATIONAL | exact_spectral_product_audit.py |
| Positivity alone gives a universal new all-degree hierarchy | REJECTED | finite aliases and the Boolean example leave only pointwise product residuals |

## Claim-writing rules

1. State dimension, graph class, signs, reversibility, masses, connectivity,
   embedding, group action, and sampling-kernel hypotheses explicitly.
2. Do not identify an algebraic exact form with a nonzero sampled function.
3. Do not infer invariance of one irreducible copy from equivariance alone.
4. Do not count equal target-eigenvalue spaces separately.
5. Degree-zero samples are the constants and are counted once.
6. Separate PROVED ordinary theorems, EXTERNAL inputs, and COMPUTATIONAL finite
   certificates.
7. No priority claim follows from a covariance identity, Lean job count, CI
   hash, rank table, or standard theorem alone.

## Prompt 3 global rigidity and near-rigidity claims

| Claim | Status | Support and publication boundary |
|---|---|---|
| The exact spherical normal moment gives `Q_i-1=sum_j p_ij(r_i ell_ij/2-1)^2` | PROVED | `GLOBAL_Q_RIGIDITY_THEOREM.md` §1 and `SphericalQEqualityRigidity.lean` |
| Connected equality rows with positive shared conductances have one active loss and total row rate | PROVED | exact local equality plus `GlobalLossRigidity.lean`; inactive edges and disconnected components excluded |
| The fixed ten-hypothesis round minor-geodesic triangulation is tetrahedral, octahedral, or icosahedral up to `O(3)` | PROVED | spherical cosine/angle sum, Euler, direct link/collar uniqueness, and face propagation; finite enumeration is not the proof |
| The exact Platonic side, loss, and total row-rate table is forced | PROVED | common valence and spherical cosine law; individual conductances are not claimed equal |
| A local active probability floor and `Q_i<=1+eta` give the displayed pointwise, path, diameter, reference-loss, and arccos bounds | PROVED | explicit `delta,q_delta,s_delta,h_delta,B_delta`; connected-component boundary stated |
| The reversible stationary law gives the displayed Poincare and effective-resistance refinements | PROVED | exact energy factor `2`; EXTERNAL finite variational principles with one-edge energy convention |
| The fixed triangulation hypotheses admit the displayed closed `eta_*` and Platonic edge-length sup bound | PROVED | corrected fixed-box Gram/Heron lower bound and explicit `C_ang,0,m_eq,g_kappa` |
| Exact `Q=1` permits tangent normalization without `ell<2` | REJECTED | two-state antipodal equality has `ell=2` and zero denominator |
| For `0<ell<2`, exact equality has the displayed radial/tangent covariance split and Prompt-2 axial condition iff `T_i=P_i/2` | PROVED | `GLOBAL_Q_RIGIDITY_THEOREM.md` §7 and `QEqualityCovariance.lean` |
| `Q=1` forces axial covariance | REJECTED | positive reversible three-parameter weighted octahedron |
| The weighted octahedron's genuine sampled degree-two exact space is nonzero because its form kernel is nonzero | REJECTED | stochastic contraction gives sampled exact space `{0}`; off-diagonal forms lie in the sampling kernel |
| Form-space dimension equals sampled-space dimension | REJECTED | the octahedral off-diagonal form kernel samples to zero and must be quotiented out |
| Only `K in {4,6,12}` can have `Q=1` | REJECTED | exact cube and dodecahedron regressions |
| Every finite spherical graph has `Q>1` | REJECTED | all five Platonic equal-edge rows have exact `Q=1` |
| Every equal-loss spherical graph is a triangulated Platonic graph | REJECTED | cube and dodecahedron have equal active loss and are not triangulations |
| Near-rigidity is diameter-free under only a local active-weight floor | REJECTED | long-path accumulation |
| Finite enumeration through 12 vertices proves the classification | REJECTED | fixed-cutoff COMPUTATIONAL falsification only |
