# Pure-math prior-art map — final Prompts 1–4 synthesis

This map separates standard inputs from the sphere-specific local/global
feasibility package, the genuinely sampled covariance theorem, the equality
rigidity results, and the Prompt 4 sharp-barrier and extremal theory. It is a
working priority audit, not a substitute for a final MathSciNet/zbMATH search,
citation-chain review, and specialist referee assessment.

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

Those works make generic product calculus and spectral decomposition of
products prior inputs. The present finite centered-resonance statement is

```text
L(fg-c)=-(lambda+nu)(fg-c)
iff
2 Gamma(f,g)=(lambda+nu)c.
```

For a square, `Gamma(f,f)=lambda c`. The Boolean four-state example proves
that a nonzero centered resonance is compatible with positivity, while Jensen
equality remains a distinct zero-variance condition.

## 2. Positive and minimal stencils

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601, DOI `10.1016/j.cma.2008.09.001`,
arXiv:0802.2674, uses Farkas alternatives and geometric cone criteria to obtain
minimal positive stencils on point clouds.

Therefore the following are not novel by themselves:

- local nonnegative consistency as a cone problem;
- separation certificates;
- minimal positive selections; and
- generic positive-span language.

The local contribution here is the exact spherical tangent/normal transfer,
indexed relative-interior theorem with repetitions and lower-dimensional
spans, division-free antipodal classification, unique angular scaling,
quantitative margin and conditioning, and the link to positive masses and
shared-edge reversibility.

## 3. Finite convexity, rigidity matrices, and LP duality

The following are standard inputs:

- convex-hull and relative-interior separation;
- finitely generated cones and Farkas alternatives;
- finite LP strong duality and complementary slackness;
- rank-nullity and restricted linear maps;
- singular-value, right-inverse, and pseudoinverse estimates; and
- finite group averaging.

The shared-edge equilibrium map is closely related to a transpose rigidity
matrix and inherits rigid-motion compatibility. The project therefore states
range and singular-value hypotheses explicitly rather than claiming false full
row rank.

The global contribution is the exact transfer of these tools to the spherical
shared-conductance matrix, including masses, sign conventions, geometric dual
work, local-but-not-global exact certificates, and explicit complete-graph,
orbit-average, and centered-clique reconciliation mechanisms.

## 4. Discrete spherical Laplacians and eigenmaps

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, Journal of the London Mathematical Society 112 (2025), article
e70235, DOI `10.1112/jlms.70235`, arXiv:2408.04877, is a direct comparator. It
introduces nonnegative spherical and hyperbolic discrete Laplacians on
triangulated surfaces, characterizes Delaunay positivity, proves exact low
modes, and connects them to polyhedral deformation theory.

The project must not claim:

- the first positive spherical Laplacian;
- the first Delaunay positivity theorem;
- the first exact coordinate eigenmap; or
- that one fixed radial connectivity is Delaunay at all refinements.

The distinction here is a finite generator with a prescribed eigenmap, exact
jump covariance, finite sampling-kernel correction, shared-edge compatibility,
and sharp sampled quadratic rigidity.

Positive spherical-Delaunay existence and exact coordinate modes are treated
as external inputs in the quasi-uniform comparison unless their full
hypotheses are verified for the actual node/graph family.

## 5. Spherical designs and harmonic sampling

The foundational source is P. Delsarte, J.-M. Goethals, and J. J. Seidel,
*Spherical codes and designs*, Geometriae Dedicata 6 (1977), 363–388, DOI
`10.1007/BF03187604`. E. Bannai and E. Bannai, *A survey on spherical designs
and algebraic combinatorics on spheres*, European Journal of Combinatorics 30
(2009), DOI `10.1016/j.ejc.2008.11.007`, surveys the modern theory.

Finite averaging of low-degree harmonics and design strength are established.
The present theorem is not that a 2-design averages trace-free quadratics to
zero. It concerns the interaction of finite harmonic sampling with a local
jump covariance and a prescribed target eigenvalue.

The exact Platonic calculations are therefore examples and alias
classifications, not a new spherical-design classification.

## 6. Association schemes, distance-regular graphs, and equivariant embeddings

Q-polynomial association schemes give canonical spherical embeddings and
control design strength through Krein parameters. A direct comparator is Sho
Suda, *On spherical designs obtained from Q-polynomial association schemes*,
Journal of Combinatorial Designs 19 (2011), 167–177, DOI
`10.1002/jcd.20278`, arXiv:0910.4628.

Distance-regular and multivariate association-scheme theories provide much
stronger global algebraic structure than is assumed here. The present
package uses only:

1. axial stabilizer symmetry, reducing a local covariance to radial and
   tangential scalars; and
2. a separately stated real irreducibility hypothesis on `Sym_0(d)`.

The equivariant rigidity theorem additionally requires every off-diagonal rate
to be nonnegative. The signed regular pentagon proves that irreducibility plus
one positive edge is insufficient when other rates are negative.

No classification of distance-regular graphs or association schemes is claimed.

## 7. Covariance tensors and genuine sampled exactness

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

The central contribution is the specialized structural factorization

```text
R_X=(L+2d I)S_X,
```

which forces

```text
K_X subset E_form,
E_sample=im(S_X) intersect ker(L+2d I),
dim E_sample=rank(S_X)-rank(R_X).
```

This is more than generic rank-nullity: the sampling and residual maps are not
independent, and every sampling alias automatically lies in the exact-form
kernel. Positive axial covariance and positive equivariant irreducibility then
yield sharp structural rigidity. Regular simplices give equality families;
Platonic aliases and signed examples identify the boundary.

This factorization/rigidity/alias package is the principal publication claim.

## 8. Signed Laplacians and inverse eigenvalue problems

Allowing negative conductances leaves the Markov class. Relevant adjacent work
includes:

- I. Agbanusi, J. C. Bronski, and D. Kielty, *A moment inequality and
  positivity for signed graph Laplacians*, arXiv:2005.09608;
- S. Fallat, H. Gupta, and J. C.-H. Lin, *Inverse eigenvalue problem for
  Laplacian matrices of a graph*, arXiv:2411.00292.

The latter studies spectra and multiplicity lists of generalized weighted
Laplacians on fixed graph supports and also investigates a size-normalized
minimum-variance problem. It is a direct comparator for any fixed-support
spectral or weight-optimization claim.

The signed claims here are narrow and exact:

- on four cardinal points, coordinate plus one quadratic mode forces adjacent
  rates `1` and antipodal rate `-1/2`;
- on the regular pentagon, exact signed distance-one and distance-two rates
  produce full trace-free quadratic exactness and disprove equivariant
  rigidity without global positivity.

Neither is reported as merely an unconstrained numerical solve or as a general
inverse-eigenvalue classification.

## 9. Spherical harmonic products and the hierarchy verdict

Clebsch--Gordan/Fischer decomposition, parity, and spherical eigenvalues are
standard. The pointwise multiplication image must be distinguished from the
full abstract tensor product, and every algebraic component must pass through
a finite sampling map.

On `S^2`, the exact `ell=1,...,6` pointwise table has no additive resonance. In
general dimensions,

```text
k(k+d-2)=2ell(ell+d-2)
```

is Pell-type and has sparse solutions. Arithmetic resonance supplies no
sampling injectivity, cross-degree separation, component multiplicity theorem,
or global consequence.

The general hierarchy is therefore `REJECTED FOR PROMPT 2`, not because
centered squares are impossible, but because no sampled dimension tradeoff,
multiplicity obstruction, or new global theorem survived identifiability and
alias audits.

## 10. Spherical equal-edge graphs and triangulation classification

Konrad J. Swanepoel, *Regular Matchstick Graphs on the Sphere*,
arXiv:2502.08294, classifies five-regular spherical matchstick graphs. This is
a direct warning against an unrestricted equal-edge or `Q=1` Platonic-only
claim.

Prompt 3 therefore assumes that the active support is exactly an injective,
strict-convex, minor-geodesic triangulation. The cube and dodecahedron are
permanent exact counterexamples to dropping this restriction.

The finite combinatorics of spherical triangulations is classical. G.
Brinkmann and B. D. McKay, *Construction of planar triangulations with minimum
degree 5*, Discrete Mathematics 301 (2005), 147–163, DOI
`10.1016/j.disc.2005.06.019`, gives an exhaustive construction framework.
The project does not use database absence as proof: the degree-five
icosahedral graph step is proved directly by link expansion after Euler forces
twelve vertices.

## 11. Convex polyhedral rigidity and framework stability

Cauchy's rigidity theorem for convex polyhedra is a standard external input.
The classification verifies strict convexity, simplicial faces, and congruent
chord triangles before applying it.

Robert Connelly and Steven J. Gortler, *Prestress Stability of Triangulated
Convex Polytopes and Universal Second-Order Rigidity*, SIAM Journal on Discrete
Mathematics 31 (2017), DOI `10.1137/15M1054833`, arXiv:1510.04185, is relevant
to stronger stability questions. It does not supply a uniform numerical
rigidity margin for the varying frameworks here.

Accordingly, the project proves edge-metric and row-rate stability but does not
infer coordinate-space closeness without a separately stated gauge-fixed
rigidity singular-value margin and nonlinear radius.

## 12. Weighted variance and graph propagation

The identity

```text
Q_i-1=sum_j p_ij(ell_ij/m_i-1)^2
```

is elementary weighted variance. Its isolated use is not novelty. The
contribution is the exact spherical transfer and explicit global propagation:

- active-edge loss `2/r_i` at equality;
- one common loss and row rate on connected symmetric support;
- multiplicative stability from a normalized active-weight floor;
- additive stability from raw active-rate and row-rate floors; and
- exact path and diameter exponents.

The rare-edge counterfamily proves that a lower active-weight hypothesis, or an
equivalent structural condition, is necessary.

## 13. Trigonometric asymptotics and product-grid barriers

Laurent/Mittag--Leffler expansions of cotangent and cosecant, Bernoulli-number
coefficient formulas, and special values of the Riemann zeta function are
classical. Therefore the coefficients

```text
8/pi^4,
10/(3pi^2),
13/45,
1/pi^2,
7/12
```

are not claimed as discoveries merely because they can be expanded.

The Prompt 4 result adds two nonformal statements:

1. a uniform `N>=2` analytic remainder with explicit constants; and
2. a fixed-graph theorem proving that all positive degree-one-exact choices
   have the same forced polar row.

The second point is the graph-class obstruction. It does not assume the
optimizer is ring-symmetric: transverse balance derives equality of the two
azimuthal rates, and the remaining coordinate equations determine all rates.
The existing reversible construction then proves exact minimax sharpness.

This appears adjacent to fixed-support weighted-Laplacian inverse problems but
is specialized to a prescribed spherical eigenmap and an exact local graph
geometry.

## 14. Constrained graph-Laplacian extremal theory

An unconstrained infimum of defect is degenerate because rate, degree, graph
density, edge locality, masses, or geometry can escape. The Prompt 4 extremal
class fixes all of these quantities at the appropriate scale.

The substantive results are:

```text
E_K>=4/(RK),
C*>=4/R,
```

finite-`K` minimizer existence, and strict exclusion of the unreduced product
family from every linear-rate class at large order.

The lower bound is a sharp consequence of the finite rate--defect product; the
compactness theorem is a finite-dimensional closed-class argument. The work is
not claimed as a general solution of weighted graph-Laplacian optimization.
Fallat--Gupta--Lin is a relevant comparator for fixed-support generalized
Laplacian spectra and normalized weight variance.

## 15. Feasible-cone anisotropy and fractional optimization

The quality value depends on feasible rate weights, not only on node geometry.
Projectivizing the tangent-balanced cone gives

```text
Q=s_2(p)/m(p)^2.
```

At a fixed mean loss, minimizing the second moment is a finite linear program.
Finite LP duality gives the certificate

```text
alpha+beta ell_j+z dot v_j <= ell_j^2.
```

This exact mean-slice reduction is the accepted convex reformulation. The
project does not claim generic novelty for linear-fractional programming or LP
duality. The contribution is the spherical tangent/loss transfer, exact cone
invariant, and sharp equality examples, including the product pole.

A Delsarte/Gegenbauer program was considered as a possible global replacement,
but no solved new dual certificate survived finite sampling aliases. That
branch is `BLOCKED`.

## 16. Bakry--Émery graph curvature

Graph curvature-dimension theory is established. Relevant primary sources
include:

- D. Cushing, S. Liu, and N. Peyerimhoff, *Bakry--Émery curvature functions of
  graphs*, arXiv:1606.01496;
- D. Cushing, S. Kamtue, S. Liu, and N. Peyerimhoff, *Bakry--Émery curvature on
  graphs as an eigenvalue problem*, arXiv:2102.08687.

These works develop curvature functions, product formulas, curvature matrices,
and many positive or nonnegative examples. Therefore a blanket claim that
finite positive graphs cannot satisfy useful curvature bounds is false.

The Prompt 4 computation

```text
Gamma_2(f)=1/2 L Gamma(f,f)+lambda Gamma(f,f)
```

for an eigenfunction is retained only as a consistency identity. At centered
resonance it produces a constant one-function value, not a full
curvature-dimension theorem. The branch is killed under its stated criterion.

## 17. Discrete transport metrics

Jan Maas, *Gradient flows of the entropy for finite Markov chains*,
arXiv:1102.5238, constructs a discrete Benamou--Brenier-type metric for
irreducible reversible finite Markov chains in which the Markov evolution is
the entropy gradient flow. Matthias Erbar and Jan Maas, *Ricci curvature of
finite Markov chains via convexity of the entropy*, arXiv:1111.2687, define an
entropic Ricci curvature using this discrete metric and prove discrete
analogues of classical consequences.

Thus ordinary continuum `W_2` contraction is not selected by positivity alone.
Any future entropy-gradient-flow or contraction claim must specify the
discrete metric, reversibility assumptions, and curvature theorem. The Prompt
4 transport branch is `DEFERRED`.

## 18. Reduced-ring coupling graphs

The accepted reduced-ring result is only an incidence obstruction. A
biregular coupling between adjacent rings satisfies

```text
p M_i=q M_j.
```

A perfect matching forces equal ring counts, excluding a varying population
rule within that coupling class. This is elementary bipartite incidence and is
not claimed as a general adaptive-mesh impossibility. Split/merge couplings and
positive exact constructions remain numerical-analysis questions.

## 19. Final novelty boundary

Standard or external inputs are:

- finite Markov product calculus and Jensen;
- positive-stencil convex geometry;
- Farkas and finite LP duality;
- cotangent partial fractions and zeta values;
- spherical Delaunay positivity and low modes;
- spherical designs and association schemes;
- Euler/planar graph facts and Cauchy rigidity;
- weighted variance and compactness;
- graph curvature frameworks; and
- Maas/Erbar discrete transport metrics.

The defensible central theorem is the combined sampled covariance package:

1. exact quadratic residual;
2. factorization through the actual sampling map;
3. automatic sampling-kernel inclusion;
4. genuine sampled-space and dimension formulas;
5. sharp positive axial and equivariant rigidity;
6. all-dimensional simplex sharpness;
7. exact alias classifications; and
8. exact signed boundary examples.

The local feasibility, global shared-edge compatibility, exact and quantitative
spherical equality rigidity, sharp fixed product-graph obstruction, constrained
extremal lower bound, and feasible-cone anisotropy theorem provide a coherent
supporting theory.

The paper would fail its kill criterion if Section 7 reduced to generic
rank-nullity or if every structural theorem disappeared after quotienting the
sampling kernel. It does not: the residual factorization and positive rigidity
survive that audit.

## 20. Priority conclusion

The final theorem package is potentially publishable as a pure-mathematics
paper because its main statement is independent of the motivating numerical
scheme and is more than Cauchy--Schwarz, Jensen, or ambient rank bookkeeping.
The Prompt 4 sharp-barrier results strengthen the numerical-analysis
consequences but are not used to inflate the central novelty claim. Specialist
review remains required before any priority assertion is made in a submitted
manuscript.

## 19. Reversible Markov energy and effective resistance

The Poincaré variational inequality, reversible Dirichlet forms, the electrical
Dirichlet principle, and effective resistance are standard.  The reconciliation
therefore does not claim those tools in isolation.  Its contribution is the
explicit transfer from the spherical normalized variance to

```text
E_P(log r)<=2eta/(1-delta)^2,
Var_pi(log r)<=2eta/((1-delta)^2 lambda_P),
|log r_i-log r_j|<=sqrt(2eta R_eff(i,j))/(1-delta),
```

with the stationary measure and edge-conductance normalization derived from
shared conductances.  The path/diameter proof is retained independently because
it has different hypotheses and sharpness behavior.

## 20. Quantitative spherical-angle certification

Differentiating the spherical cosine law is standard.  An endpoint interval
bound for `cos A` is not accepted merely because it works near some reference
points: the prior candidate fails on the required fixed icosahedral
neighborhood.  The accepted proof instead uses the exact spherical Gram/Heron
factorization

```text
sin^2(b)sin^2(c)-(cos a-cos b cos c)^2
 =4 sin(S)sin(S-a)sin(S-b)sin(S-c)
```

to produce a positive angle-sine lower bound throughout the complete side box.
The new statement is the combined explicit transfer from graph defect to a
closed side box, integer valence separation, and edge-distance bound—not the
classical identity itself.

## 21. Reconciled publication boundary

The Prompt 2 sampled covariance factorization remains the candidate central
paper theorem.  The richer Prompt 3 restricted classification and explicit
graph-global near-rigidity form a strong companion theorem.  Prompt 4 retains
its accepted sharp product-grid barriers, constrained extremal problem, and
feasible-cone anisotropy theory as supporting results.  The final package does
not claim an optimal near-rigidity constant, coordinate-space stability without
a rigidity margin, or finite enumeration as proof.
