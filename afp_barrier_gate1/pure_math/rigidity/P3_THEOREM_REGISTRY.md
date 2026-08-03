# Prompt 3 theorem and hypothesis registry

Only `PROVED`, `EXTERNAL`, `COMPUTATIONAL`, `CONJECTURE`, and `REJECTED` are
mathematical claim labels.  The corrected mandatory package has no remaining
`CONJECTURE` item.

All symbols inherit the finite spherical generator and normalization from
`GLOBAL_Q_RIGIDITY_THEOREM.md` §1.  Unless a row explicitly replaces or
weakens them, its hypotheses include a nonempty finite state set, unit nodes
`Omega_i in S^2`, positive masses, a simple undirected support with positive
shared conductances, `a_ij=gamma_ij/w_i`, and the coordinate equation
`L Omega=-2Omega`.  Later rows also inherit any earlier registry item they
cite by ID; falsification rows state the hypothesis being removed.

| ID | Label | Exact hypotheses | Conclusion | Ordinary support | Lean / exact support |
|---|---|---|---|---|---|
| P3-1 | PROVED | nonempty finite positive spherical coordinate eigenmap `L Omega=-2Omega` | loss moment `2`, positive row rate, normalized probability/mean/second moment, and exact `Q-1` variance | global theorem §§1–2 | `SphericalQEqualityRigidity.lean`; near audit |
| P3-2 | PROVED | P3-1 and local `Q_i=1` | every active loss is `2/r_i` | §2.1 | same module; Platonic rows |
| P3-3 | PROVED | P3-2, positive masses, shared symmetric conductances, connected active graph | one global row rate and one active loss | §2.2 | existing `GlobalLossRigidity.lean` plus specialization |
| P3-4 | PROVED | P3-3 and `0<ell<2` | one common minor geodesic length | §2 degeneracy audit | exact endpoint audit |
| P3-R | PROVED | exactly the ten simple, injective, noncrossing, convex-face, disjoint-interior, full-coverage, positive-edge round triangulation hypotheses | regular tetrahedral/octahedral/icosahedral embedding up to `O(3)`, or `SO(3)` after orientation | global theorem §3 and `ICOSAHEDRAL_GRAPH_LEMMA.md` | selected finite Lean algebra; source-pinned hostile census |
| P3-RC | PROVED | P3-R | exact `q,V,E,F`, side cosine, loss, and total row-rate table | §§3.3–3.5 | exact symbolic audit |
| P3-N1 | PROVED | connected active graph, `p_ij>=kappa>0`, `1<=Q_i<=1+eta`, `delta=sqrt(eta/kappa)<1` | pointwise normalized-scale interval and adjacent relative/log rate bounds | §4.1–4.2 | quantitative Lean module; long-path audit |
| P3-N2 | PROVED | P3-N1 and active paths/diameter | exact path, diameter, incident-edge, arbitrary-edge, and graph-center loss/rate bounds | §§4.2–4.3 | path/ratio/log Lean core; stress audit |
| P3-N3 | PROVED | P3-N2 and `0<ell_-<=ell_e<=ell_+<2` | explicit geodesic arccos Lipschitz bound | §4.4 | deterministic arc audit |
| P3-E1 | PROVED | positive masses and shared conductances | `pi_i proportional w_i r_i` is stationary and reversible for `P=p` | §5.1 | finite conductance algebra |
| P3-E2 | PROVED | P3-N1 and P3-E1 | `E_P(log r)<=2eta/(1-delta)^2` | §5.2 | exact energy audit |
| P3-E3 | PROVED | P3-E2 and non-absolute Poincare gap `lambda_P>0` | variance and pointwise centered-log bounds | §5.3 | EXTERNAL variational definition transferred exactly |
| P3-E4 | PROVED | P3-E2 and connected conductance graph | effective-resistance log-rate bound with one-edge energy convention | §5.4 | EXTERNAL Dirichlet principle; exact rational audit |
| P3-S | PROVED | triangulation hypotheses 1–9, with exact hypothesis 10 replaced by the near-`Q`/active-probability-floor assumptions, plus `0<ell_0<2`, `theta_0<2pi/3`, and displayed `rho` | explicit positive `delta_*`, `eta_*`; certified side box, angle bound, constant valence, Platonic graph, and edge-length sup bound | §6, corrected Gram/Heron certificate | threshold and angle audit |
| P3-C0 | REJECTED | exact global `Q=1` with no non-antipodal assumption | unrestricted definition of `u_ij/s` | antipodal `ell=2` chain makes `s=0` | executable antipodal regression |
| P3-C1 | PROVED | exact local/global `Q=1` and `0<ell<2` | centered unit tangent directions; `tr T=1`; exact `C` and Prompt-2 residual `M` decomposition | §7.2 | covariance Lean entry algebra; symbolic audit |
| P3-C2 | PROVED | P3-C1 | Prompt-2 full one-shell axial condition iff `T_i=P_i/2` | §7.3 | P2 one-shell bridge in Lean |
| P3-C3 | PROVED | positive three-parameter weighted octahedron | `L Omega=-2Omega`, `r=2`, `ell=1`, `Q=1`; axial at all vertices iff all conductances agree | §7.4 | exact symbolic audit |
| P3-C4 | PROVED | P3-C3 with genuine sampling quotient | sampled degree-two exact space is `{0}` | stochastic infinity-norm proof | exact linear system and nonzero-minor audit |
| P3-C5 | PROVED | `1<=Q_i<=1+eta` | exact radial error bound but no tangent-anisotropy bound | §7.5 | scalar Lean lemma; anisotropy limit |
| P3-F1 | REJECTED | no triangulation restriction | only `K in {4,6,12}` can have `Q=1` | cube/dodecahedron | five-Platonic regression |
| P3-F2 | REJECTED | local floor only | diameter-free near-rigidity | long paths | deterministic stress |
| P3-F3 | REJECTED | finite census through 12 | all-orders classification | logical fixed-cutoff boundary | workflow enforces COMPUTATIONAL label |
| P3-F4 | REJECTED | unrestricted finite spherical graph | every such graph has `Q>1` | all five Platonic `Q=1` rows | exact regression |
| P3-F5 | REJECTED | equal active loss without embedded-triangulation hypotheses | every such graph is triangulated Platonic | cube, dodecahedron, inactive-diagonal variants | exact negative tests |
| P3-F6 | REJECTED | exact global `Q=1` only | axial covariance | weighted-octahedron anisotropy | symbolic audit |
| P3-F7 | REJECTED | algebraic degree-two form space without sampling quotient | form-space dimension equals sampled-space dimension | octahedral off-diagonal sampling kernel | exact rank/contraction audit |

## EXTERNAL inputs

The spherical law of cosines and excess, Euler's identity for a cellular
sphere triangulation, the triangulated-disk curvature identity, elementary
link/collar topology, finite Poincare variational principle, and electrical
Dirichlet/effective-resistance principle are `EXTERNAL` standard inputs.  Their
normalizations and every project-specific transfer are displayed in the
ordinary proof.

## COMPUTATIONAL boundary

Pinned Plantri counts and graph records, exact finite coordinate/Gram/hull
certificates, symbolic Platonic and weighted-octahedron identities, finite
matrix minors, and stress-test instances are `COMPUTATIONAL`.  They certify
examples and attack hypotheses; none substitutes for an all-orders proof.
