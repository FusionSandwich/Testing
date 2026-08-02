# Pure-mathematics exact assumptions table

This table is normative for theorem wording. A hypothesis may be omitted from a
statement only when the cited proof does not use it.

| Result | Finite state set | Nonnegative off-diagonal rates | Conservation | Unit-sphere embedding | Coordinate eigenmap | Reversibility / masses | Connectivity | Geometric support | Additional hypotheses | Conclusion |
|---|---|---|---|---|---|---|---|---|---|---|
| Product and carré-du-champ identities | yes | no | generator difference form | no | eigenfunction hypotheses for residual forms | no | no | no | none | exact product identities |
| Covariance identity | yes | no | generator difference form | no | `L Phi=-lambda Phi` | no | no | no | finite Euclidean coordinates | equation (3.2) of final package |
| Spherical sampled-space factorization | yes | no | yes | yes, `S^(d-1)` | eigenvalue `d-1` | no | no | no | trace-free symmetric forms, target `2d` | `R=(L+2dI)S`, genuine sampled formula |
| Positive axial rigidity | yes | yes for deriving positive radial coefficient | yes | yes | eigenvalue `d-1` | no | no | rowwise axial covariance | positive distinct jump at every required row | `E_form=K_X`, `E_sample=0` |
| Positive equivariant rigidity | yes | **yes for every off-diagonal rate** | yes | yes | eigenvalue `d-1` | no | transitive group action | equivariant support/rates | irreducible real conjugation action; one positive distinct jump | `E_form=0` |
| Non-antipodal local feasibility | finite candidate set | row rates sought nonnegative | row difference form | `S^2` | target eigenvalue `-2` | no | no | permitted non-antipodal neighbors | no full-dimensionality; indexed repetitions allowed | hull/relative-interior equivalences |
| Antipodal local classification | finite candidate set | yes | yes | `S^2` | target `-2` | no | no | pure or mixed antipodal support | antipodes handled separately | exact budget simplex |
| Quantitative local margin | finite candidate set | yes | yes | `S^2` | target `-2` | no | no | relative tangent span | positive relative inradius, angular window where invoked | coefficient/rate/conditioning/perturbation bounds |
| Shared-edge cone/Farkas theorem | finite nodes/edges | conductances nonnegative | shared-edge equilibrium | sphere for radial form | target `-2` | positive masses and symmetric shared conductances | not required for cone statement | fixed undirected permitted graph | noncoincident edge columns where stated | exact cone and alternative |
| Complete-graph construction | finite nodes | positive off-diagonal conductances when masses positive | yes | sphere | target `-2` | positive masses | complete graph connected | complete graph | weighted centering | explicit positive solution |
| Exact local `Q>=1` | finite row | yes | yes | `S^2` | coordinate eigenvalue `-2` | no | no | arbitrary active row | normalized peak | rate--defect inequality and equality condition |
| Connected exact `Q=1` propagation | finite nodes | yes | yes | `S^2` | coordinate eigenvalue `-2` | reversibility not logically needed; symmetric active relation is | yes, active relation | symmetric active support | exact `Q=1` at all nodes | common row rate and active loss |
| Restricted Platonic classification | finite nodes | yes | yes | injective `S^2` embedding | coordinate eigenvalue `-2` | no extra reversibility beyond symmetric active support | yes | active graph exactly strict-convex minor-geodesic triangulation | every triangulation edge active; simplicial convex hull | regular tetrahedron/octahedron/icosahedron |
| Multiplicative near-rigidity | finite nodes | yes | yes | `S^2` | coordinate eigenvalue `-2` | symmetric active support | yes | arbitrary active graph | `Q_i<=1+epsilon`, normalized active-weight floor, finite diameter | explicit relative edge/rate factors |
| Additive near-rigidity | finite nodes | yes | yes | `S^2` | coordinate eigenvalue `-2` | symmetric active support | yes | arbitrary active graph | raw gap, row-rate floor, active-rate floor | explicit additive path/diameter bounds |
| Product-grid polar uniqueness | one polar row on fixed product graph | positivity not needed for uniqueness algebra; positive graph class for minimax | yes | exact square product-grid coordinates | coordinate eigenvalue `-2` | no equal masses; reversibility only for graph class/attainment | no | two azimuthal plus one inward polar neighbors | `N>=2` | three polar rates uniquely forced |
| Product-grid graph minimax | finite product graph | yes | yes | square equal-angle product embedding | coordinate eigenvalue `-2` | positive masses, shared reversible conductances | graph connected | fixed unreduced adjacency, `M=2N` | existing positive reversible construction | exact minimax polar/max rate |
| Polar asymptotic theorem | no graph hypotheses beyond exact formula | n/a | n/a | n/a | n/a | n/a | n/a | `N>=2` | differentiated cotangent Mittag--Leffler expansion | explicit remainder bounds |
| Universal rate barrier | one finite row | yes | yes | not needed after first-moment hypothesis | `sum a ell=2` | no | no | no | defect upper bound | `r>=4/(Ch^2)` |
| Quasi-uniform transfer | one finite row | yes | yes | spherical loss interpretation | first moment `2` | no | no | active loss window | positive window constants | explicit rate/defect window |
| Finite extremal minimizer | fixed `K` | yes | yes | labeled points in `S^2` | exact coordinate balance | positive bounded masses; symmetric conductances | implicit through exact feasible graph if needed | degree/locality/separation/covering constraints | closed support convention and nonempty class | minimum attained |
| Extremal lower bound | fixed/asymptotic class | yes | yes | not used beyond first moment | exact coordinate balance | rate cap | no extra | controlled class | `r_max<=RK` | `E_K>=4/(RK)`, `C*>=4/R` |
| Cone anisotropy theorem | finite candidates | rates nonnegative | tangent and normal constraints | spherical row geometry | target normal moment `lambda>0` | no | no | positive non-antipodal losses | nonempty feasible cone | exact projective/sliced-LP formula and dual |
| Reduced-ring incidence theorem | finite bipartite ring coupling | no weight sign needed | no | no | no | no | no | biregular adjacent-ring bipartite graph | degrees `p,q`; perfect matching for corollary | `pM_i=qM_j`; matching forces equal counts |

## Externally supplied inputs

The following are not silently promoted to project theorems:

- standard finite convex-hull and relative-interior separation;
- finite Farkas alternatives, LP strong duality, and complementary slackness;
- the cotangent Mittag--Leffler expansion and special zeta values;
- positive spherical-Delaunay existence and exact low-mode results;
- Euler/planar triangulation facts and convex Cauchy rigidity;
- representation-theoretic irreducibility hypotheses;
- Maas/Erbar discrete transport metrics and curvature theory; and
- any uniform framework-rigidity singular-value estimate.

## Prohibited silent assumptions

Do not silently assume:

- sampling injectivity;
- full-dimensional tangent span;
- distinct indexed tangent directions;
- absence of antipodes;
- equal masses or symmetric row rates;
- reversibility when only a local theorem is used;
- ring symmetry of an optimizer;
- Delaunay status of fixed radial connectivity;
- an active-weight floor in near-rigidity;
- coordinate rigidity from edge-metric concentration; or
- positivity for signed counterexamples.
