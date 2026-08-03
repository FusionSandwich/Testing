# Pure-mathematics exact assumptions table

This table is normative for theorem wording.  Each row has exactly one claim
status.  A hypothesis may be omitted only when the cited proof does not use it.

| Result | Status | Sign / conservation | Embedding and eigenmap | Global structure | Additional hypotheses | Exact conclusion |
|---|---|---|---|---|---|---|
| Finite product and covariance identities | PROVED | finite difference-form generator; no sign assumption | finite Euclidean eigenfunctions or eigenmap | none | stated target eigenvalues and shift | exact product residual and quadratic covariance formulas |
| Spherical sampled-space factorization | PROVED | no positivity or reversibility needed | nonempty unit nodes in `S^(d-1)`, `d>1`, coordinate target `-(d-1)`, trace-free quadratic target `-2d` | one common finite operator | actual sampling map `S_X` | `R_X=(L+2dI)S_X`, automatic kernel inclusion, and the genuine sampled-space formula |
| Positive axial quadratic rigidity | PROVED | every off-diagonal rate nonnegative | same spherical eigenmap | none | rowwise axial covariance and at least one positive distinct jump at every required row | `E_form=K_X` and `E_sample={0}` |
| Positive equivariant quadratic rigidity | PROVED | every off-diagonal rate nonnegative | equivariant spherical eigenmap | transitive action and invariant rates | irreducible real conjugation action; one positive distinct jump | `E_form={0}`; reversibility is not required |
| Spectral target-class separation | PROVED | one common finite linear operator | arbitrary sampled subspaces | none | target eigenvalues pairwise distinct; degree zero counted once | internal direct sum and rank bound; for spherical degrees, distinct degrees suffice only when `d>=2` |
| Non-antipodal local feasibility | PROVED | sought row rates nonnegative | finite candidate neighbors on `S^2`; target `-2` | none | candidates non-antipodal; indexed repetitions and lower-dimensional tangent spans allowed | tangent-hull and relative-interior characterizations plus exact scaling |
| Antipodal local classification | PROVED | nonnegative row rates | unit sphere, target `-2` | none | pure or mixed antipodal support treated division-free | exact normal-budget simplex |
| Quantitative local feasibility | PROVED | positive sought rates | relative tangent span on `S^2` | none | positive relative inradius and explicit angular window | coefficient, rate, conditioning, and transported-span perturbation bounds |
| Shared-edge cone/Farkas theorem | PROVED | nonnegative symmetric conductances and positive masses | spherical equilibrium target `-2` | fixed finite undirected permitted graph | noncoincident edge columns where stated | exact cone membership, strict relative interior, and dual alternative |
| Complete-graph construction | PROVED | positive masses and nonnegative shared conductances | unit sphere | complete graph | weighted centering | explicit positive solution `gamma_ij=2w_iw_j` |
| Local spherical `Q>=1` | PROVED | nonnegative finite row | unit-sphere coordinate target `-2` | none | first moment `sum a ell=2` | rate--defect inequality and exact constant-loss equality condition |
| Connected exact `Q=1` propagation | PROVED | nonnegative rates; symmetric active relation | unit-sphere coordinate target `-2` | connected active graph | equality at every node | one common row rate and one common active loss |
| Restricted Platonic classification | PROVED | nonnegative active rates | injective unit-sphere embedding, coordinate target `-2` | active graph exactly the stated strict-convex minor-geodesic triangulation | all ten geometric/topological hypotheses and every triangulation edge active | regular tetrahedron, octahedron, or icosahedron up to `O(3)` |
| Quantitative near-rigidity | PROVED | nonnegative active rates | unit-sphere coordinate target `-2` | connected symmetric active support | explicit normalized active-weight floor, graph paths/diameter; extra floors for additive form | displayed edge-loss, rate, arc, Poincare, and resistance bounds |
| Product-grid polar uniqueness | PROVED | local algebra needs no positivity; graph class does | exact unreduced equal-angle product coordinates | one polar row | integer `N>=2`; two azimuthal and one inward neighbors | all three rates uniquely forced without assuming symmetry |
| Product-grid graph minimax | PROVED | positive reversible shared conductances | exact square equal-angle embedding | fixed unreduced graph, `M=2N` | verified positive attaining construction | exact graph-class minimax and quartic constants |
| Polar analytic expansion | PROVED | not applicable | exact polar formula | none | integer `N>=2`; differentiated cotangent Mittag--Leffler expansion with positive tail | uniform one-sided rate and quality remainders |
| Universal rate barrier | PROVED | nonnegative finite row | first normal moment `sum a ell=2` | none | positive defect upper bound | `4<=r epsilon` and `r>=4/(C h^2)` |
| Loss-window transfer | PROVED | nonnegative finite row | spherical losses | none | `0<L<=U` and active losses in `[Lh^2,Uh^2]` | exact rate and defect windows |
| Positive spherical-Delaunay existence and exact coordinate modes | EXTERNAL | positive shared conductances | applicable spherical Delaunay hypotheses | mesh family supplied externally | exact hypotheses of the cited geometric theorem | used only conditionally; no fixed radial connectivity is promoted |
| Constrained extremal lower bound | PROVED | positive masses, nonnegative symmetric conductances | labeled `K>=2` points on `S^2`, exact coordinate balance | degree/locality/separation/covering/mesh/mass/rate constraints | nonempty class and `r_i<=RK` | `E_K>=4/(RK)` and `C*>=4/R` |
| Constrained finite-order minimizer | PROVED | same as preceding row | same | finite labeled support-graph union | fixed `K>=2`, fixed positive parameters, nonempty closed class | the infimum is attained |
| Fixed-moment anisotropy family | PROVED | nonnegative rates | positive losses and tangent increments | one finite candidate set | `lambda>0` and nonempty tangent-balanced probability polytope | affine slice `F_i(lambda)` is bijective with `P_i`; `Q_lambda=r epsilon/lambda^2=s_2/m^2` |
| Sliced anisotropy LP reduction | PROVED | as preceding row | as preceding row | none | nonempty `P_i` | compact attainable-mean interval, attained primal minimum, exact `A_i`, equality characterization |
| Finite LP strong duality | EXTERNAL | finite real LP | not applicable | none | feasible fixed-mean slice | dual equality and complementary slackness with the displayed sign convention |
| Opposed-ray anisotropy | PROVED | nonnegative two-rate row | `v_2=-kappa v_1`, `kappa>0`, positive losses | two candidates | unique balanced probability | `A=kappa(ell_1-ell_2)^2/(kappa ell_1+ell_2)^2`; half-weight formula only at `kappa=1` |
| Reduced-ring incidence | PROVED | signs irrelevant | no geometric input | finite biregular bipartite coupling | degrees `p,q`; perfect matching for corollary | `pM_i=qM_{i+1}`; a perfect matching forces equal populations |
| Source-pinned Plantri census through 12 vertices | COMPUTATIONAL | not applicable | not applicable | pinned external source and exact invocation | finite cutoff only | counts `1,1,2,5,14,50,233,1249,7595`, total `9150`; not the classification proof |

## Prohibited silent assumptions

The following formulations are `REJECTED`: sampling injectivity without proof;
full-dimensional tangent span; distinct indexed tangent directions; absence of
antipodes; equal masses or symmetric row rates; optimizer ring symmetry;
Delaunay status of a fixed radial connectivity; a near-rigidity conclusion
without its active-weight/rate floor and diameter; coordinate rigidity from
edge-metric concentration alone; positivity in signed examples; treating a
fixed-`lambda` affine slice as a cone modulo scaling; using `r epsilon/4` as
the scale-invariant quality when `lambda!=2`; or treating two opposite rays as
sufficient to force half weights.
