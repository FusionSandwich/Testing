# P1C approach registry — equality geometry and exact extremizers

This registry groups genuinely different mechanisms used in P1C. `COMPLETE`
means the route supplies a proof or exact construction in the ordinary
theorem. `COMPLETE_AUDIT` means an independent exact certificate checks that
proof interface. `REJECTED` identifies an attractive but false global
classification. No P1C theorem-strength obligation remains `BLOCKED`.

| Mechanism family | Status | Concrete theorem or certificate | Adversarial boundary |
|---|---|---|---|
| radial--tangent block algebra | COMPLETE | `Delta=-ell Omega+tau`, exact formulas for `C`, `M`, `B`, and `||B||_F^2` | no shell, symmetry, injectivity, or equal-rate assumption is used |
| zero loss variance | COMPLETE | every active loss equals `(d-1)/r_i`; mixed loss--tangent covariance vanishes | zero variance alone does not give tangent isotropy |
| finite weighted frame theory | COMPLETE | in the nonantipodal branch, `B_i=0` iff normalized tangent increments form a centered probability-weighted UNTF | normalization is illegal at `ell=2`; the raw zero-frame branch is separate |
| sampled quotient scalarity | COMPLETE | frontier equality iff `R_2=c_*S_2` with `c_*=d(d-1)/r_max`, including zero leakage outside `im S_2` | scalarity only after projection to `im S_2` is too weak |
| reversible Markov assembly | COMPLETE | exact first/second conditional moment criterion at common latitude, plus detailed balance | independent local frames need not obey endpoint or cycle compatibility |
| Gram-completion formulation | COMPLETE | positive-semidefinite rank-`d` Gram equations characterize global embedding compatibility | local moment rows do not by themselves produce one global Gram matrix |
| minimum-frame argument | COMPLETE | active degree at least `d`; equality forces a regular-simplex tangent figure and equal local weights | degree greater than `d` permits nonregular weighted frames |
| complete-support classification | COMPLETE | distinct nonantipodal complete support forces the regular simplex; antipodal complete support is `K_2` | does not classify sparse supports |
| restricted convex-polyhedral classification | COMPLETE | on `S^2`, distinct strictly convex inscribed vertices, convex-hull skeleton, common rates, and degree `3..5` yield exactly the five Platonic solids | every listed hypothesis is material |
| unrestricted Platonic classification | REJECTED | no theorem | connected blow-ups/covers and the distinct long-chord icosahedral shell are exact counterfamilies |
| all-dimensional simplex construction | COMPLETE | explicit coordinates, complete graph, exact `R_2=(d+1)S_2`, sampling rank and kernel | finite fixtures are not used for the all-`d` proof |
| all-dimensional cross-polytope construction | COMPLETE | nonantipodal graph, exact `R_2=dS_2`, off-diagonal sampling aliases | declared support has positive rates; excluded antipodal/nonedges have rate zero |
| all-dimensional hypercube construction | COMPLETE | edge graph, Walsh-character sampling rank, exact `R_2=2S_2` | the graph also admits higher-shell embeddings, so a natural-embedding classification needs a shell hypothesis |
| exact Platonic coordinates | COMPLETE | shortest-edge tetrahedron, octahedron, cube, icosahedron, and dodecahedron with exact radical data | no floating-point edge or rank threshold |
| sampling-minor certificates | COMPLETE_AUDIT | minors `-4/27`, `-2`, `4/27`, `-16 sqrt(5)/125`, `16/81` | algebraic form exactness is not a nonzero sampled mode |
| alias audit | COMPLETE | equality implies `ker R_2=ker S_2=K_X` and `e_2=0`; tetra/octa/cube aliases are identified explicitly | frontier equality is not existence of a reproduced `H_2` mode |
| exact symbolic regression | COMPLETE_AUDIT | 20 equality fixtures, local blocks, family values, minors, antipodal guard, blow-up, long shell, nonregular frame, cycle mutation | finite tests support but never replace the proofs |
| Lean division-free core | COMPLETE_CANDIDATE | projected increment identities, axial/raw moment equivalence, and guarded normalization | square-root normalization is kept outside the antipodal endpoint |
| association schemes | SCREENED_EXTERNAL | organizes symmetric eigenspaces of the cube and regular shells | uniform scheme structure does not prove arbitrary weighted equality |
| spherical designs and invariant quadrature | SCREENED_EXTERNAL | supplies moment language for local and global designs | design exactness neither constructs reversible rates nor audits sampling aliases |

## Dynamic search and audit rounds

1. Independent tensor-block, frame, global Markov/Gram, exact-family, and
   formalization routes were developed before synthesis.
2. The block route exposed the mixed covariance `h_i`; the independent frame
   route identified the precise `0<ell<2` normalization.
3. An adversarial endpoint audit found the antipodal equality branch and
   prevented the false assertion that every equality row has a genuine unit
   tangent frame.
4. Separate exact-coordinate and sampling-minor routes audited every family
   without numerical rank thresholds.
5. Global-classification routes were kept distinct from the local theorem.
   Connected covers, blow-ups, nonregular weighted frames, and the long-chord
   icosahedral shell rejected the unrestricted route.
6. The surviving restricted classifications were then audited against every
   hypothesis deleted by those counterfamilies.
7. The Lean route formalizes only the stable finite algebra after the ordinary
   proof and all normalization guards were fixed.

The permanent mutations are: omit zero loss variance, normalize at `ell=2`,
replace full residual scalarity by projected scalarity, identify
`E_form` with a nonzero sampled space, infer a Platonic list from local
tightness, or use floating-point rank decisions.
