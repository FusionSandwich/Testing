# Prompt 3 approach-family registry

## Status vocabulary

Route state uses the search-protocol vocabulary `ACTIVE`, `BLOCKED`,
`REJECTED`, or `PROVED`.  This is distinct from controlled mathematical claim
labels (`PROVED`, `EXTERNAL`, `COMPUTATIONAL`, `CONJECTURE`, `REJECTED`), which
are recorded in `P3_THEOREM_REGISTRY.md`.

## Independent mechanism families

| Route | Mechanism | Concrete certificate or kill condition | State |
|---|---|---|---|
| G1 | spherical normal projection | `sum_j a_ij ell_ij=2` and the normalized `Q-1` variance identity | PROVED |
| G2 | shared-edge equality cocycle | `ell_ij=2/r_i=2/r_j` plus connected path propagation | PROVED |
| G3 | direct spherical trigonometry | equilateral cosine law, excess, and `theta<2pi/3` | PROVED |
| G4 | round local topology | face partition of a metric disk gives the angle sum before constant valence is used | PROVED |
| G5 | Euler incidence algebra | `qV=2E`, `3F=2E`, `V-E+F=2` gives `q in {3,4,5}` | PROVED |
| G6 | separating triangles and cyclic links | disk curvature, chord exclusion, two pentagonal collars, and the opposite pole | PROVED |
| G7 | opposite-side face development | fix one face and propagate the unique adjacent equilateral face through the dual graph | PROVED |
| C1 | source-pinned finite generation | verified `plantri` source blob and counts through 12 vertices | ACTIVE — COMPUTATIONAL only |
| N1 | local variance extraction | `p_ij>=kappa` gives `|x_ij-1|<=sqrt(eta/kappa)` | PROVED |
| N2 | shared-edge ratio and path multiplication | adjacent `r_i/r_j=x_ij/x_ji`, length-indexed path products, diameter stress | PROVED ordinary; ACTIVE in Lean |
| N3 | graph-center logarithmic reference | `|log(ell_e/ell_ref)|<=h_delta+R_G s_delta` | PROVED ordinary; ACTIVE in Lean |
| N4 | reversible Dirichlet form | detailed-balance swap gives the exact factor `2eta/(1-delta)^2` | PROVED |
| N5 | Poincare variational gap | non-absolute gap with `E/Var` convention | PROVED using EXTERNAL standard principle |
| N6 | effective-resistance variational route | `|du|^2<=R_eff E` under one-edge energy convention | PROVED using EXTERNAL standard principle |
| S1 | old endpoint-product angle enclosure | old `C_A<1` fails at the exact icosahedral fixed box | REJECTED |
| S2 | fixed-box spherical Gram/Heron factor | explicit lower bound `s_A0=2 sqrt(m_S m_T^3)` and closed `C_ang,0` | PROVED |
| S3 | finite integer valence gap | `g_kappa=2pi/(d_max(d_max-1))` for `d_max>=4` | PROVED |
| S4 | monotone equilateral angle map | explicit derivative and endpoint minimum `m_eq` | PROVED |
| V1 | radial/tangent covariance expansion | centered tangent first moment removes mixed terms | PROVED |
| V2 | Prompt 2 axial bridge | in dimension three, full one-shell tangent moment iff `T_i=P_i/2` | PROVED ordinary; ACTIVE in Lean |
| V3 | unrestricted tangent normalization | antipodal exact equality has `ell=2` and zero denominator | REJECTED |
| V4 | weighted-octahedron anisotropy | three positive conductances; axial at all vertices iff all three agree | PROVED ordinary; ACTIVE exact audit |
| V5 | sampling-kernel contraction | the diagonal sample sector would require stochastic `P` to have eigenvalue `-2` | PROVED |
| L1 | old incident-loss Lean lemma | countermodel at `delta=2`; missing `delta<1` | REJECTED |
| L2 | corrected finite Lean algebra | coordinate specialization, equality, paths/logs, covariance entries, axial bridge | ACTIVE |

## Adversarial matrix

| Hidden assumption under attack | Exact test or proof obstruction | Result |
|---|---|---|
| unrestricted classification | cube and dodecahedron | REJECTED |
| every finite spherical graph has `Q>1` | all five Platonic rows have `Q=1` | REJECTED |
| connectedness unnecessary | disjoint tetrahedral/octahedral components | REJECTED |
| inactive edges controlled | cube with inactive face diagonals | REJECTED |
| minor versus major arc irrelevant | the same endpoints admit different geodesic arcs | REJECTED |
| injectivity unnecessary | duplicated embedded states | REJECTED |
| crossings/overlaps/gaps harmless | equal chords alone do not produce a round cellular triangulation | REJECTED |
| antipodes fit tangent normalization | two-state antipodal chain | REJECTED |
| signed/directed/nonreversible rows propagate | shared conductance comparison disappears | REJECTED |
| local floor yields diameter-free stability | long alternating paths | REJECTED |
| local defect controls tangent anisotropy | weighted octahedron with `eta=0` and anisotropy tending to `1/2` | REJECTED |
| form dimension is sampled dimension | octahedral off-diagonal sampling kernel | REJECTED |
| finite enumeration is a proof | fixed order cutoff | REJECTED |
| edge closeness implies coordinate closeness | no rigidity-operator margin was assumed | BLOCKED and not claimed |

## Cross-audit gates

The classification is accepted only after three independent checks:

1. direct spherical geometry and round angle sum;
2. separating-triangle/link/collar combinatorics plus face propagation; and
3. source-pinned finite hostile enumeration used only as COMPUTATIONAL
   falsification.

The quantitative package is accepted only after long-path, small-`kappa`,
small-gap, large-resistance, and near-degenerate-side stress.  The covariance
package is accepted only after the antipodal kill test, weighted-octahedron
symbolic algebra, and sampling-kernel contraction certificate.

No route may invoke Euler before the ten triangulation hypotheses, infer
convexity from connectivity, use enumeration as classification, infer tangent
isotropy from `Q=1`, or claim coordinate stability without a separately proved
rigidity margin.
