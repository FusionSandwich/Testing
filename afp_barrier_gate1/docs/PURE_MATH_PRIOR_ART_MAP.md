# Pure-math prior-art map — Prompts 1–3

This map separates standard inputs from the sphere-specific Prompt 1 package,
the genuinely sampled covariance theorem, the corrected centered-product
boundary, and the Prompt 3 rigidity results. It is a working priority audit,
not a substitute for a final MathSciNet/zbMATH and citation-chain review.

## 1. Markov generators, carré du champ, and products

For a Markov generator,

```text
Gamma(f,g)=1/2[L(fg)-f Lg-g Lf]
```

is standard. So are positivity of `Gamma(f,f)`, Markov-semigroup Jensen, and
the equality characterization by zero variance on transition support.

Relevant comparators include:

- E. Azmoodeh, S. Campese, and G. Poly, *Fourth Moment Theorems for Markov
  Diffusion Generators*, arXiv:1305.5469;
- S. Steinerberger, *On the product of eigenfunctions of the Laplacian*,
  Journal of Spectral Theory 9 (2019), DOI `10.4171/JST/279`, arXiv:1711.09826.

Those works make the generic product identity, diffusion-product calculus, and
spectral decomposition of products prior inputs. Prompt 2 does not claim them
as new.

The Prompt 2 closeout correction is the exact finite **centered** resonance
statement:

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2 Gamma(f,g)=(lambda+nu)c
```

for eigenfunctions `f,g`. For a square this is

```text
Gamma(f,f)=lambda c.
```

The `c=0` obstruction is therefore only the uncentered case. The Boolean
four-state example proves that nonzero centered resonance is compatible with a
positive finite generator. Jensen equality is a different, zero-variance
condition.

## 2. Positive and minimal stencils

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601, DOI `10.1016/j.cma.2008.09.001`, arXiv:0802.2674,
uses Farkas alternatives and geometric cone criteria for positive stencils.
Local nonnegative consistency, separation certificates, and minimal positive
selections are therefore standard or adjacent inputs.

Prompt 1's contribution is the combined spherical tangent/normal scaling,
division-free antipodal classification, explicit quantitative margin and
conditioning, positive masses, shared-edge compatibility, exact sparse
obstructions, and reconciliation mechanisms.

## 3. Finite convexity, rigidity, and LP duality

The following are standard inputs:

- convex-hull and relative-interior characterizations;
- finitely generated cones and Farkas alternatives;
- finite LP strong duality and complementary slackness;
- rank-nullity and restricted linear maps;
- singular-value, right-inverse, and pseudoinverse estimates; and
- finite group averaging.

The shared-edge operator is related to a transpose rigidity matrix and has
rigid-motion compatibility constraints. Prompt 1 therefore states precise
range and singular-value hypotheses rather than a false full-row-rank claim.

Prompt 2 likewise does not claim novelty for rank-nullity. Its specialized
structural input is

```text
R_X=(L+2d I)S_X,
```

which forces

```text
K_X subset E_form,
E_sample=im(S_X) intersect ker(L+2d I),
dim E_sample=rank(S_X)-rank(R_X).
```

## 4. Discrete spherical Laplacians and eigenmaps

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, Journal of the London Mathematical Society 112 (2025), article
e70235, DOI `10.1112/jlms.70235`, arXiv:2408.04877, is a direct comparator. It
develops nonnegative discrete spherical/hyperbolic Laplacians, Delaunay
positivity, exact low modes, and polyhedral deformation connections.

The project must not claim the first positive spherical Laplacian or exact
coordinate eigenmap. The Prompt 2 distinction is a prescribed finite eigenmap
with exact covariance, sampling-kernel correction, and sharp sampled quadratic
rigidity. Prompt 3 adds a sharp equality and stability analysis for the radial
loss inequality under explicit active-support hypotheses.

## 5. Spherical designs and harmonic sampling

The foundational source is P. Delsarte, J.-M. Goethals, and J. J. Seidel,
*Spherical codes and designs*, Geometriae Dedicata 6 (1977), 363–388, DOI
`10.1007/BF03187604`. E. Bannai and E. Bannai, *A survey on spherical designs
and algebraic combinatorics on spheres*, European Journal of Combinatorics 30
(2009), DOI `10.1016/j.ejc.2008.11.007`, is a useful modern survey.

Finite averaging of low-degree harmonics and design strength are established
subjects. Prompt 2's contribution is not that a 2-design averages trace-free
quadratics to zero, but the interaction of harmonic sampling with a local jump
covariance and a prescribed target eigenvalue.

## 6. Association schemes and equivariant embeddings

Q-polynomial association schemes give canonical spherical embeddings and
control harmonic design strength through Krein parameters. A direct comparator
is Sho Suda, *On spherical designs obtained from Q-polynomial association
schemes*, Journal of Combinatorial Designs 19 (2011), 167–177, DOI
`10.1002/jcd.20278`, arXiv:0910.4628.

Prompt 2 uses only two transparent symmetry mechanisms:

1. axial stabilizer symmetry, which reduces a local covariance to radial and
   tangential scalars; and
2. a separately stated real irreducibility hypothesis on `Sym_0(d)`.

The corrected equivariant theorem additionally requires every off-diagonal
rate to be nonnegative. The signed regular pentagon proves that irreducibility
plus one positive edge is insufficient when other rates are negative. Thus
"symmetry forces full rank" is never used without exact positivity and module
hypotheses.

## 7. Covariance tensors and sampled exactness

Local second moments

```text
C_i=sum_j a_ij(Phi_j-Phi_i)(Phi_j-Phi_i)^T
```

occur broadly in probability, graph geometry, meshfree consistency, and
diffusion approximation. The expansion

```text
L(Phi^T A Phi)
 =-2lambda Phi^T A Phi+tr(A^T C_i)
```

is elementary and not claimed alone as a discovery.

The potentially publishable Prompt 2 package is the combination of:

1. exact shifted covariance residual;
2. trace-free form constraints;
3. factorization through the finite sampling map;
4. genuine sampled-space and rank formulas;
5. sharp positive axial rigidity;
6. corrected positive equivariant rigidity;
7. regular-simplex equality family;
8. exact Platonic sampling-kernel classifications; and
9. exact signed boundary examples.

## 8. Signed Laplacians and inverse eigenvalue problems

Allowing negative conductances leaves the Markov class. Adjacent work includes
I. Agbanusi, J. C. Bronski, and D. Kielty, *A moment inequality and positivity
for signed graph Laplacians*, arXiv:2005.09608, and S. Fallat, H. Gupta, and
J. C.-H. Lin, *Inverse eigenvalue problem for Laplacian matrices of a graph*,
arXiv:2411.00292.

Prompt 2's signed claims are narrow and exact:

- on four cardinal points, coordinate plus one quadratic mode forces adjacent
  rates `1` and antipodal rate `-1/2`;
- on the regular pentagon, the exact distance-one and distance-two signed rates
  produce full quadratic exactness and disprove equivariant rigidity without
  global positivity.

Neither claim is merely an unconstrained numerical solve.

## 9. Spherical harmonic products and the hierarchy verdict

Clebsch–Gordan/Fischer decomposition, parity, and spherical eigenvalues are
standard. The pointwise multiplication image must be distinguished from the
full abstract tensor product, and every algebraic component must then pass
through a finite sampling map.

On `S^2`, the exact `ell=1,...,6` pointwise table contains no additive
resonance. In general dimensions the resonance equation

```text
k(k+d-2)=2ell(ell+d-2)
```

is Pell-type and has sparse solutions. Arithmetic resonance alone supplies no
sampling injectivity, cross-degree separation, component multiplicity theorem,
or global consequence.

The hierarchy is therefore `REJECTED FOR PROMPT 2` because no `ell`-indexed
sampled dimension tradeoff, multiplicity obstruction, or new global theorem
survived the identifiability and alias audits. It is not rejected by a false
universal centered-square obstruction.

## 10. Spherical equal-edge graphs and triangulation classification

Regular equal-edge embeddings on the sphere form a broader class than the
Platonic solids. Konrad Swanepoel, *Regular Matchstick Graphs on the Sphere*,
American Mathematical Monthly, published online 2026, DOI
`10.1080/00029890.2025.2599752`, arXiv:2502.08294, classifies the five
5-regular spherical matchstick graphs. This is a direct warning against an
unrestricted equal-edge or `Q=1` Platonic-only claim.

Prompt 3 therefore imposes a strict convex minor-geodesic triangulation whose
active support is exactly the triangulation one-skeleton. The cube and
dodecahedron are permanent exact project counterexamples to dropping that
restriction.

The finite combinatorics of spherical triangulations is classical. G.
Brinkmann and B. D. McKay, *Construction of planar triangulations with minimum
degree 5*, Discrete Mathematics 301 (2005), 147–163, DOI
`10.1016/j.disc.2005.06.019`, gives an exhaustive construction framework for
simple sphere triangulations of minimum degree five. Prompt 3 does not use the
absence of a database entry as proof: `ICOSAHEDRAL_GRAPH_LEMMA.md` gives a
direct degree-five link-expansion proof after Euler forces twelve vertices.
The Brinkmann–McKay work is retained as an independent comparator and
enumeration cross-check.

The degree-three and degree-four graph identifications are elementary from the
exact counts: `K_4`, and `K_6` minus a perfect matching. The degree-five proof
uses the absence of separating triangles and expands two five-cycles between
opposite poles.

## 11. Convex polyhedral rigidity

Cauchy's rigidity theorem for convex polyhedra is a standard external input:
two convex polyhedra with congruent corresponding faces are congruent. Prompt
3 verifies the hypotheses before applying it: the Euclidean convex hull is
strictly convex and simplicial, its chord triangles correspond to the
geodesic faces, and every face has the same edge length.

Robert Connelly and Steven J. Gortler, *Prestress Stability of Triangulated
Convex Polytopes and Universal Second-Order Rigidity*, SIAM Journal on Discrete
Mathematics 31 (2017), DOI `10.1137/15M1054833`, arXiv:1510.04185, is relevant
to stronger stability questions. It does not supply a uniform numerical
rigidity margin for the present varying frameworks.

Accordingly, Prompt 3 proves edge-metric and row-rate stability with explicit
active-weight and diameter constants, but does not infer coordinate-space
closeness without a separately stated gauge-fixed rigidity singular-value
margin.

## 12. Weighted variance and graph propagation

The identity

```text
Q_i-1=sum_j p_ij(ell_ij/m_i-1)^2
```

is elementary weighted variance. Its use as a local equality characterization
is not claimed alone as novelty. The Prompt 3 contribution is the exact
spherical transfer and the explicit global propagation:

- active-edge loss `2/r_i` at equality;
- one common loss and row rate on connected symmetric support;
- multiplicative stability from a normalized active-weight floor;
- additive stability from raw active-rate and row-rate floors; and
- exact path and diameter exponents.

The rare-edge counterfamily demonstrates that no uniform edgewise conclusion
follows from small weighted variance without a lower active-weight or
equivalent structural condition. The path overlap construction likewise
explains why graph diameter appears.

## 13. Prompt 3 novelty boundary

Standard inputs are:

- weighted Cauchy–Schwarz and variance decomposition;
- spherical triangle tangent-angle formulas;
- Euler and face-incidence identities;
- finite planar-triangulation combinatorics;
- Cauchy convex-polyhedron rigidity; and
- elementary path induction.

The defensible Prompt 3 package is their integrated consequence for a finite
positive eigenmap generator:

1. complete handling of zero-loss and antipodal active-edge degeneracies;
2. transfer from local sharpness to one global active spherical metric;
3. a correctly restricted tetrahedral/octahedral/icosahedral classification;
4. exact cube and dodecahedron unrestricted counterexamples;
5. explicit multiplicative and additive near-rigidity constants; and
6. sharp hypothesis boundaries from rare-edge and long-path adversarial
   families.

It is not a claim to the first classification of Platonic solids, the first
Cauchy rigidity theorem, the first spherical matchstick analysis, or the first
weighted-variance estimate.

## 14. Priority conclusion

Defensible novelty across the three prompts is the combined spherical
feasibility, shared-edge compatibility, sampled covariance, product-boundary,
and sharply restricted equality/stability package. Generic convexity,
rank-nullity, product calculus, Jensen, harmonic decomposition, representation
theory, Euler arithmetic, and convex-polyhedron rigidity are external inputs.
Specialist review is still required before publication.
