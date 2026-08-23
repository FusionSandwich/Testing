# AFP R5 hostile independent referee report

**Review classification:** independent non-human mathematical and formal-methods audit. This is not identifiable human peer review, journal review, or external acceptance.

**Repository reviewed:** `FusionSandwich/Testing`  
**Release branch:** `codex/afp-major-revision-r5-20260822`  
**Final binding commit:** `653d8945a5e91515f7a382ed42a8f4f51c0f0094`  
**Scientific-content snapshot:** `9783a69e8f079d61c100bc87ea653ec9c981c2fe`  
**Pinned manuscript:** `output/pdf/FLAGSHIP_MANUSCRIPT.pdf`, 23 pages, release-manifest SHA-256 `87b8a77af8c53e2bfa2b24fcc1cf95fef8c798181b7f0828e61d25eaa7267c8d`.

## Recommendation

# **MAJOR REVISION**

I found no counterexample to the sharp finite-dimensional frontier, the final equality chain, or the exact weighted master defect budget. Those are the strongest and most credible results in the package. The manuscript is nevertheless not mathematically ready for identifiable human review in its current form because:

1. **Corollary 6.3 is not theorem-grade as printed.** It summarizes several conditional transfer mechanisms without stating complete propositions, metrics, constants, or all necessary hypotheses.
2. **Theorem 7.2 has an under-disclosed proof/certificate boundary.** The repository contains substantial exact symbolic and rational verification, but the article does not adequately classify the theorem as computer-assisted or reproduce a complete independently checkable certificate in a permanent supplement.

Neither point presently falsifies the core product theorem. Both block the breadth and proof-completeness claims of the submitted manuscript.

---

## 1. Review method and source boundary

The audit used the pinned manuscript source and PDF, the P1A-P1E ordinary proof sources, the exhaustive Lean declaration/axiom audit, the exact-rational adaptive-ring scripts, the corrected claim-to-evidence matrix, the counterexample ledger, the P2F inconclusive archive, and the prior-art matrix. Internal labels such as `accepted`, `release candidate`, and `major revision closed` were treated as workflow metadata rather than evidence.

The following checks were performed independently at theorem level:

- re-derivation of the sampled quotient construction and weighted trace comparison;
- re-derivation of the constant `d(d-1)` and its equality chain;
- verification of the radial-tangent block decomposition and nonantipodal tight-frame normalization;
- verification of the global reversible Markov/Gram equations and the antipodal branch;
- verification of the normalized master budget and its unconditional consequences;
- direct checking of the regular-polygon construction;
- hostile reading of the adaptive-ring symbolic limit, Cauchy guard, Neumann margin, ordinary-row recurrence, first-polar-row enclosure, and quotient/rate constants;
- theorem-signature comparison against the stated Lean boundary;
- review of the P2F rerun sensitivity and failed reference-convergence gate;
- targeted primary-source checks against the identified adjacent literature.

Exact manuscript references below are by theorem, corollary, section, equation, appendix, and immutable source path. No PDF page number is invented where the connector runtime could not independently extract the page map from GitHub's binary endpoint.

---

## 2. Blocking errors

### B1. Corollary 6.3 is not a checkable mathematical statement

**Manuscript locations:** Abstract; Section 1.1, contribution 6; Corollary 6.3; Appendix B entries for P1D edge, graph, quotient, and frame transfers.

Theorem 6.1 and Corollary 6.2 are precise. Corollary 6.3 changes register and lists consequences in prose:

- global shell-loss control;
- every-edge control under a directed-probability floor;
- graphwise propagation;
- covariance/eigenvector consequences;
- sampled-quotient scalarity;
- tangent-frame stability and repair.

As printed, these bullets do not collectively define a theorem. Several lack one or more of the following:

- the exact metric or topology in the conclusion;
- a defined reference equality configuration;
- the complete constant;
- the exceptional set or mass convention;
- the graph diameter, resistance, spectral-gap, or congestion normalization;
- the lower stationary-mass and directed-edge-probability assumptions;
- the shell, tangent-frame, or feature-surjectivity margins;
- the distinction between local row repair and globally compatible spherical embedding repair.

The detailed P1D source contains many explicit formulas, including conductance-mass bounds, path/resistance/gap estimates, quotient scalarity with `alpha_X`, raw-frame whitening, and a local unit-frame repair theorem. That material is not reproduced as a theorem-grade supplement in the manuscript. A repository path is not a substitute for a stable mathematical statement in the submitted article.

**Required correction:** choose one of the following.

1. Split Corollary 6.3 into individually numbered propositions with all definitions, constants, and hypotheses printed; or
2. demote it to an unnumbered discussion and narrow every abstract/introduction claim accordingly.

**Replacement language:**

> **Conditional transfers from the defect budget.** Theorem 6.1 gives weighted mean-square control of radial nonuniformity and covariance anisotropy. Pointwise, edgewise, graphwise, quotient, and frame conclusions require additional assumptions, including appropriate lower mass or edge-probability bounds, graph connectivity parameters, sampling-frame conditioning, and tangent-frame nondegeneracy. No unconditional global embedding-stability theorem is asserted here.

Until this repair is made, the abstract should say **"exact weighted defect budget"**, not unqualified **"quantitative stability theorem"** when referring to the full list of advertised geometric consequences.

### B2. Theorem 7.2 is not adequately classified or packaged as a computer-assisted theorem

**Manuscript locations:** Section 7.2; Theorem 7.2; Open Problem 7.3; Appendices B, C, D, and E.  
**Controlling ordinary source:** `docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md`.  
**Load-bearing exact scripts:**

- `p1e_short_gap_symbolic_matrix_audit.py`;
- `p1e_short_gap_cauchy_guard_audit.py`;
- `p1e_short_gap_cauchy_hostile_audit.py`;
- `p1e_short_gap_polar_guard_audit.py`;
- `p1e_short_gap_proof_audit.py`;
- `p1e_short_gap_family_audit.py`;
- `p1e_short_gap_referee_audit.py`.

I found no contradiction in the following chain:

1. the no-guard latitude schedule closes exactly;
2. the transition aspect lies in the correlated `O(1/M)` box;
3. the shared `M:2M` mask has the stated row/column sums and matched moments;
4. the exact normalized `6 x 6` transition matrix has a strictly positive limiting solution on the entire rounding-phase interval;
5. the rational Cauchy estimate and Neumann bound preserve positivity for `M >= 2^80`;
6. the ordinary-row recurrence telescopes rather than accumulating a fixed error per row;
7. the first-polar and equatorial rows are handled separately;
8. the resulting shared stresses define positive weights and a reversible coordinate-exact generator;
9. the row multiplier gives `D_2 <= 75 h^2/2`, while the active-edge lower bound gives `r_max <= 64 pi^2 h^-2`.

This is materially stronger than finite floating-point evidence. It is still a **computer-assisted/external-certificate proof surface**. The article suppresses enough of the matrix, removable-singularity verification, guard inventory, and inductive inequalities that a reader cannot independently reproduce the all-level result from the article alone.

The current release classification `PROVED ordinary mathematics` understates the role of exact symbolic computation. The correct alternatives are:

- include a complete permanent supplement with the literal matrix, every denominator guard, the rational majorants, and compact certificate outputs; or
- label Theorem 7.2 explicitly as computer-assisted and identify the trusted computing base and independent checker.

**Replacement status note:**

> The proof of Theorem 7.2 is computer-assisted. The article gives the mathematical reduction; the remaining finite symbolic identities and rational inequalities are certified by immutable artifacts at scientific snapshot `9783a69e8f079d61c100bc87ea653ec9c981c2fe`. No floating-point tolerance is used in the theorem certificate. Independent acceptance of Theorem 7.2 therefore requires verification of that exact certificate and its trusted computing base.

Pending that repair, the referee classification is:

> **PROVED CONDITIONALLY ON THE ARCHIVED EXACT-SYMBOLIC/RATIONAL CERTIFICATE.**

---

## 3. Major revisions

### M1. Add an exact theorem-by-theorem Lean boundary to the main article

**Manuscript locations:** Section 1.4; Appendix D; all prose describing formalization.

The exhaustive release audit is useful and appears internally consistent: 512 public theorem/lemma declarations were checked with both `#check` and `#print axioms`; no project-local `axiom`, `sorry`, `admit`, or `sorryAx` was reported; the printed logical dependencies are the expected `propext`, `Classical.choice`, and `Quot.sound`.

That does **not** establish whole-paper formalization. The exact boundary is:

- finite row/covariance/trace/rate algebra: Lean-checked;
- selected equality and weighted-budget identities: Lean-checked under explicit scalar or finite-array hypotheses;
- full spherical interpretation and sharpness families: assembled in ordinary mathematics;
- global Gram/Kolmogorov embedding characterization: ordinary mathematics, not one end-to-end Lean theorem;
- restricted Platonic conclusion: ordinary mathematics plus a classical geometric input;
- all-level adaptive-ring construction: not Lean-formalized;
- perturbative robustness, transport, P2F, and physical conclusions: not Lean theorems.

Add a main-text table with one row for every numbered theorem and columns:

`exact Lean declaration | ordinary proof | computer-assisted certificate | external theorem | open component`.

**Replacement language:**

> Lean verifies the finite algebraic spine identified in Appendix D. The geometric classifications, all-level adaptive-ring construction, prior-art assessment, and all physical or transport interpretations remain ordinary or external proof obligations.

### M2. Corollary 5.5 needs an exact classical input for the restricted Platonic conclusion

**Manuscript location:** Corollary 5.5 and its proof architecture.

The minimum-neighbor conclusion is correctly forced by a centered probability-weighted unit-norm tight frame in a `(d-1)`-dimensional tangent space. The degree-exactly-`d` regular-simplex conclusion is also correct.

The three-dimensional Platonic conclusion is much narrower. It depends on all stated hypotheses:

- nonantipodal equality;
- distinct vertices;
- strict convexity and inscribedness;
- active graph equal to the convex polyhedron's one-skeleton;
- one common directed rate;
- common degree `3 <= q <= 5`.

The local root-of-unity argument for `q <= 5` is plausible and can be completed. Passing from regular local vertex figures and congruent regular faces to exactly the five convex regular polyhedra invokes a classical convex-polyhedral classification/rigidity theorem. State that theorem precisely and cite a standard source, or print a complete reduction.

**Replacement language:**

> Under the additional convex-polyhedral and common-rate hypotheses stated below, the local equal-weight tight-frame equations force a regular vertex figure. The classical classification of convex regular polyhedra then leaves the five Platonic solids. No corresponding classification is asserted for general weighted equality configurations.

### M3. Replace "full rigidity" or "classification" language by "equality characterization" where uniqueness is not proved

**Manuscript locations:** Abstract; Sections 1.1 and 5; theorem hierarchy; conclusions.

Theorem 5.3 gives necessary-and-sufficient global equations. It does not classify equality embeddings by a finite list and does not prove uniqueness of a labelled embedding. Blowups, covers, long-chord shells, repeated nodes, weighted nonregular tangent frames, and higher-dimensional families remain.

Use:

> necessary-and-sufficient local and global characterization of the equality equations

rather than:

> full rigidity classification.

When discussing the Gram formulation, distinguish:

- characterization of admissible Gram/Markov data;
- realization up to orthogonal equivalence;
- uniqueness of a labelled embedding;
- uniqueness of support or combinatorial type.

Only the first two are addressed.

### M4. Narrow the abstract's stability wording

**Manuscript locations:** Abstract; Section 1.1, contribution 6.

The unconditional result is Theorem 6.1: an exact normalized weighted budget controlling the radial defect and anisotropy energy. It does not by itself give pointwise closeness, all-edge closeness, global graph propagation, a nearby globally compatible equality embedding, or perturbative persistence.

**Replacement language:**

> We derive an exact normalized weighted decomposition of frontier excess into radial and anisotropy defects, together with explicit weighted concentration estimates. Stronger pointwise or geometric conclusions require the additional mass, edge, graph, sampling, and frame-conditioning assumptions stated separately.

### M5. Keep the priority statement non-exhaustive and non-authoritative

**Manuscript locations:** Section 1.2; Appendix G; `PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md`.

The manuscript correctly acknowledges direct prior art for positive spherical coordinate-exact Laplacians, graphical designs, eigenpair-preserving weighted graph Laplacians, tight frames, and positive stencils. Targeted checking confirmed that the cited sources are genuinely adjacent and do not, from their stated conclusions, automatically supply the same joint finite frontier/equality/budget/construction package.

That does not establish global literature priority. The comparison corpus is finite and internally selected. The paper should not use `priority claim` as though it were a proved theorem.

**Replacement language:**

> Within the primary sources reviewed for this draft, we did not find the same joint package of a sampled alias-correct product frontier, its equality equations, an exact weighted defect budget, and the stated local constructions. This is a positioning statement, not an exhaustive priority claim.

A human specialist must still review bibliography completeness and normalization transfers.

### M6. State the discrete asymptotic sequence and impractical constants every time Theorem 7.2 is summarized

**Manuscript locations:** Abstract; Sections 1.1, 7.2, and Appendix F.

The construction is an explicit all-level sequence, not a theorem for every sufficiently small `h`. The schedule is indexed by integer levels, with `M_0 = 2^80`, a fixed but enormous degree bound, extremely small separation constant, and intentionally huge conductance margins. These facts do not invalidate asymptotic locality, but they matter for interpretation.

Use:

> along the explicit level sequence of Theorem 7.2

and avoid language suggesting practical meshing, robustness under arbitrary node motion, or a family available for all small fill distances.

### M7. Separate exact theorem certificates from floating diagnostics

**Manuscript locations:** Appendices C and E; release validation prose.

The exact symbolic/rational construction checks and the P2F/frozen floating tests belong to different evidentiary classes. The Windows/WSL tetrahedron discrepancy is not a theorem failure, but it shows why floating thresholds must remain diagnostic.

The release package should mark every check as one of:

- normative Lean proof;
- normative exact symbolic/rational certificate;
- ordinary proof consistency check;
- floating diagnostic/regression;
- inconclusive numerical reference study.

### M8. Remove internal release vocabulary from scientific theorem status

**Manuscript locations:** theorem hierarchy and appendices where `accepted`, registry status, or internal stage labels appear.

Use only scientific statuses in the paper:

`proved | proved conditionally | computer-assisted | external input | computational evidence | open | falsified`.

Keep branch, gate, and release terminology in the repository/reviewer bundle.

---

## 4. Minor revisions

1. **Corollary 5.6:** connectedness appears stronger than necessary for the weighted mean-zero and second-moment conclusions; remove it or explain why it is retained.
2. **Proposition 2.1:** state explicitly the convention behind "largest finite generalized eigenvalue" and the guaranteed nontriviality of the sampled quotient.
3. **Theorem 5.3:** distinguish Gram-data characterization from uniqueness of a labelled embedding modulo `O(d)` and graph automorphisms.
4. **Exact examples:** name the symbolic rank/minor certificate for every quoted sampling rank or injectivity statement.
5. **Build quality:** the retained TeX log reports several overfull boxes, including one around 28 pt. The internal visual inspection says no clipping occurred, but the source should still be reflowed before submission.
6. **Hypothesis naming:** use one fixed phrase for positive stationary masses, reversibility/shared conductances, the coordinate eigenmap, and active support.
7. **Administrative completeness:** author, affiliation, ORCID, funding, conflict, data-license, repository DOI, and journal-format fields remain outside the mathematical review and must not be inferred.

---

## 5. Verified theorem audit

| Manuscript result | Referee status | Exact scope |
|---|---|---|
| Proposition 2.1 | **VERIFIED** | Finite sampled quotient, kernel inclusion, and Gram-pencil formulation. No sampling injectivity follows. |
| Theorem 3.1 | **VERIFIED** | Exact covariance representation and orthogonal radial/anisotropy split under the stated coordinate eigenmap. |
| Proposition 3.2 | **VERIFIED** | Weighted adjoints and exact trace identities. |
| Theorem 4.1 | **VERIFIED** | `D_2 r_max >= d(d-1)` for the stated finite positive reversible coordinate-exact class. Not a theorem for signed operators, arbitrary graph Laplacians, or quadrature rules. |
| Theorem 5.1 | **VERIFIED** | Final equality iff every row has maximal rate, zero loss variance, and zero anisotropy; equivalently `R_2 = c_* S_2`. |
| Theorem 5.2 | **VERIFIED** | Division-free tangent block identity and nonantipodal centered weighted tight-frame form. No global uniqueness. |
| Theorem 5.3 | **VERIFIED** | Reversible Markov/Gram/Kolmogorov characterization, subject to all stated positivity, rank, and support conditions. |
| Proposition 5.4 | **VERIFIED** | Correct separate connected antipodal branch. |
| Corollary 5.5 | **PARTLY VERIFIED / EXTERNAL INPUT** | Degree conclusions verified; restricted Platonic conclusion needs the precise classical convex-polyhedral input. |
| Corollary 5.6 | **VERIFIED** | Weighted spherical 2-design consequence; connectedness may be redundant. |
| Theorem 6.1 | **VERIFIED** | Exact normalized weighted master budget. This is the strongest unconditional stability result. |
| Corollary 6.2 | **VERIFIED** | Weighted exceptional-mass and pointwise envelope. |
| Corollary 6.3 | **NOT AUDITABLE AS PRINTED** | Detailed conditional formulas exist in the P1D source, but the manuscript statement is incomplete. |
| Theorem 7.1 | **VERIFIED** | Exact regular-polygon construction and matching-order bounds in `d=2`. |
| Theorem 7.2 | **CONDITIONALLY VERIFIED** | No contradiction found; depends on the archived exact symbolic/rational proof surface and needs explicit computer-assisted status. |
| Open Problem 7.3 | **CORRECTLY OPEN** | No perturbation radius, robustness constants, or arbitrary node-motion theorem survives. |

### Independent derivation of the core constant

Let `Z_i = Omega_i Omega_i^T - I/d` and let `M_i` be the row representer of `R_2`. The sampled quotient norm gives the operator inequality

`G_R <= D_2^2 G_S`.

Taking the Frobenius trace and using

- `tr G_S = (d-1)/d`,
- `tr G_R = d/(d-1) E_epsilon + E_B`,

produces

`D_2^2 >= d^2/(d-1)^2 E_epsilon + d/(d-1) E_B`.

The coordinate eigenmap fixes the first loss moment, and the exact weighted variance identity gives

`epsilon_i = (d-1)^2/r_i + V_i >= (d-1)^2/r_max`.

Therefore

`D_2 >= d/(d-1) sqrt(E_epsilon) >= d(d-1)/r_max`.

Equality in the final product forces equality in every nonnegative step, hence `r_i = r_max`, `V_i = 0`, and `B_i = 0` for every positive-mass row. Consequently `M_i = c_* Z_i` and `R_2 = c_* S_2`. This verifies the manuscript's final equality chain and also confirms that equality does **not** reproduce degree two exactly.

---

## 6. Lean, axioms, and external inputs

| Claim family | Actual formal status |
|---|---|
| sampled quotient, covariance, finite trace, and two-defect algebra | Lean-checked finite algebra under exact signatures |
| sharp product scalar implication | Lean-checked once the finite trace/radial hypotheses are supplied |
| local equality/tangent normalization | Lean-checked finite algebra with explicit denominator guards |
| weighted master-budget consequences | selected finite identities Lean-checked; not a global geometric stability theorem |
| global embedding/Gram/Kolmogorov interpretation | ordinary mathematics |
| restricted Platonic conclusion | ordinary mathematics plus classical external geometry |
| adaptive-ring all-level schedule and Cauchy proof | ordinary/computer-assisted; not Lean-formalized |
| P2F or physical conclusions | numerical evidence only; no Lean theorem |

The axiom audit supports the narrow statement that the reviewed Lean declarations contain no project-local proof holes and use only standard logical foundations. It does not validate the manuscript's unformalized hypotheses or constructions.

---

## 7. P2F treatment

The P2F archive is handled correctly and must remain excluded from theorem evidence.

Verified negative facts:

- the selected response differences are at floating-noise scale;
- the declared 50/72/98/128-direction reference sweep fails its convergence gate;
- a pinned rerun changes floating fields and flips unresolved direction/improvement booleans;
- no evaluated-data, device, damage, transport-performance, or HTS conclusion follows.

Required permanent language:

> P2F is an inconclusive numerical reference comparison. It is not a convergence certificate, model validation, or evidence for a physical prediction.

The P2F failure does not invalidate the pure finite frontier theorem because no proof step depends on P2F.

---

## 8. Physical and publication claims

The manuscript's scope firewall is substantially correct:

- no transport-cost theorem;
- no semigroup/PDE convergence theorem;
- no material or high-temperature-superconductor prediction;
- no evaluated-data validation;
- no perturbative robustness theorem;
- no journal acceptance or identifiable human review.

Preserve that firewall. In particular, `positive generator`, `spherical fidelity`, and `matching order` must not be translated into claims of superior physical transport accuracy without a common model, cost normalization, converged reference, and uncertainty analysis.

---

## 9. Prior art and novelty

Targeted checking supports the manuscript's basic distinction from the cited adjacent results:

- Izmestiev-Lam supplies direct prior art for positive spherical coordinate-eigenfunction Laplacians under Delaunay hypotheses;
- graphical-design/eigenpolytope work concerns graph quadrature and eigenspace realization under different metrics and constraints;
- eigenpair-preserving graph-sparsifier spectrahedra do not supply the sampled spherical quadratic frontier;
- positive meshfree stencils do not automatically give globally reversible shared conductances;
- tight-frame theory supplies established equality language, not the complete rate/loss/global-compatibility package.

This supports a **defensible distinction**, not a proved priority claim. A human literature specialist must still check completeness, particularly 2025-2026 work and normalization-equivalent formulations.

---

## 10. Minimum revision gate

A new review round should not begin until all six items are completed:

1. rewrite or demote Corollary 6.3 and conform the abstract/conclusion;
2. make Theorem 7.2 independently checkable as a complete supplement or explicitly computer-assisted certificate;
3. add the theorem-by-theorem Lean/ordinary/computer-assisted/external-input map;
4. state and cite the classical theorem used in Corollary 5.5;
5. replace priority and internal-release authority language;
6. preserve the P2F, physical, robustness, and publication firewalls.

## Final disposition

# **MAJOR REVISION**

The central finite algebra, sharp lower bound, equality equations, and exact weighted defect budget are credible. The current article still overstates theorem-grade stability transfers and under-discloses the proof/certificate boundary of the three-dimensional all-level construction. Those defects are repairable but publication-blocking.
