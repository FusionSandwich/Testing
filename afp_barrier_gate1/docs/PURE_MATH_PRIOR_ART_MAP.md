# Pure-math prior-art map — P0/M1 and Prompt 2 update

The principal publication risk is that a proposed statement already exists
under different terminology. This map separates standard inputs from the
sphere-specific and sampled-covariance packages. It is a working priority
audit, not a claim of an exhaustive MathSciNet or zbMATH search.

## 1. Markov generators, carré du champ, and products of eigenspaces

Known background includes

```text
Gamma(f,g) = 1/2 [L(fg) - f Lg - g Lf]
```

and Jensen positivity for Markov semigroups. The square identity, equality
characterization, and additive product obstruction are therefore foundational,
not central novelty.

Relevant spectral-diffusion literature includes E. Azmoodeh, S. Campese, and
G. Poly, *Fourth Moment Theorems for Markov Diffusion Generators*,
arXiv:1305.5469. That program studies eigenspaces and products through the
diffusion property of Markov generators. A finite jump generator is not a
diffusion operator: its nonzero carré-du-champ remainder is precisely the
obstruction exploited here. The Prompt 2 paper must not present the product
formula or Jensen inequality as new.

Related product questions for Laplace eigenfunctions include S. Steinerberger,
*On the product of eigenfunctions of the Laplacian*, Journal of Spectral Theory
9 (2019), DOI `10.4171/JST/279`, and graph analogues such as
arXiv:2105.14635. These works reinforce that products of eigenspaces and their
spectral content are an established subject. Prompt 2's defensible distinction
is the finite positive jump setting with prescribed sampled eigenmap,
quadratic covariance constraints, and explicit sampling-kernel correction.

Remaining direct-comparison targets before submission:

- finite-state Markov generators with prescribed eigenfunctions;
- finite diffusion algebras and product-closed eigenspaces;
- equality cases for nonlocal carré-du-champ and Jensen identities;
- inverse eigenvalue problems for signed and positive weighted Laplacians; and
- spectral products after finite sampling and aliasing.

For the last item, the weighted-Laplacian inverse-eigenvalue literature,
including S. Fallat, H. Gupta, and J. C.-H. Lin,
*Inverse eigenvalue problem for Laplacian matrices of a graph*,
arXiv:2411.00292, is adjacent to the signed-restoration construction but does
not by itself supply the fixed-embedding quadratic theorem.

## 2. Positive and minimal stencils

### Principal comparator

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601, DOI `10.1016/j.cma.2008.09.001`, arXiv
`0802.2674`.

Seibold explicitly uses a finite Farkas alternative and geometric half-space /
cone criteria for local positive Poisson stencils. Consequently, the following
items are standard or close to standard and cannot be sold as the AFP result:

- local nonnegative consistency as a finite conic-feasibility problem;
- separation certificates for local infeasibility;
- geometric surrounding conditions for positive stencils; and
- sparse/minimal positive selections from a larger candidate set.

The P0/M1 theorem proves the exact indexed convex-hull and relative-interior
statements directly, including repeated and redundant directions, but that
finite-convex lemma is supporting mathematics rather than the standalone
publication contribution.

### Added spherical structure not supplied by a Euclidean rowwise restatement

The completed P0/M1 package adds simultaneously:

1. the decomposition
   `Omega_j = cos(theta_j) Omega_i + sin(theta_j) u_j`;
2. the fixed coordinate eigenvalue and separate normal budget;
3. the angular renormalization
   `(1-cos(theta_j))/sin(theta_j)=tan(theta_j/2)`;
4. uniqueness of the positive normal scale;
5. a division-free antipodal classification;
6. a relative cone margin with explicit coefficient, rate, conditioning,
   perturbation, and objective constants;
7. positive masses and one shared conductance per undirected edge;
8. the global cone, Farkas, LP, and complementary-slackness geometry;
9. a weighted-centered local/global incompatibility certificate; and
10. a centered-clique reconciliation mechanism.

The publication argument must use this package, not the phrase “positive
span.”

## 3. Finite convex geometry, rank algebra, and sampling kernels

The following are standard finite-dimensional inputs:

- convex-hull membership and barycentric coordinates;
- positive indexed barycentric coordinates and relative interior;
- minimal faces and affine-dependence descriptions of nonuniqueness;
- conic relative interior;
- Farkas alternatives;
- strong LP duality and complementary slackness;
- rank-nullity, restrictions of linear maps, and stacked-matrix rank formulas;
- singular-value and pseudoinverse perturbation estimates.

Prompt 2 therefore does not claim novelty for

```text
E_form = ker R
```

or for a bare ambient-rank-minus-constraint-rank formula. Its correction is
that the publication object is the image of the form kernel under a second
linear map:

```text
E_sample = S_X(ker R).
```

The intersection term

```text
dim(ker R intersect ker S_X)
```

cannot be dropped. The structural result is that axial covariance forces
`R` to be a positive row scaling of `S_X`, so the entire algebraic exact form
space is sampling kernel.

## 4. Discrete spherical Laplacians and eigenmaps

### Principal comparator

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, Journal of the London Mathematical Society 112 (2025), article
e70235, DOI `10.1112/jlms.70235`, arXiv `2408.04877`.

This is a direct comparator because it develops nonnegative spherical and
hyperbolic discrete Laplacians, positivity/Delaunay structure, exact low
spherical eigenmodes, and infinitesimal polyhedral deformations.

The AFP program must avoid broad claims such as “the first positive spherical
Laplacian with an exact coordinate mode.” Its distinction is the
arbitrary-node/permitted-graph feasibility theory and, in Prompt 2, the exact
quadratic covariance and sampling-kernel theory for a prescribed finite
eigenmap.

Other adjacent areas include graph-Laplacian eigenmaps, Colin-de-Verdière-type
embeddings, stress matrices, and weighted inverse eigenvalue problems. The
Prompt 2 equivariant theorem is a representation argument for the constraint
kernel; it is not a general classification of discrete eigenmaps.

## 5. Spherical designs and quadratic harmonic sampling

The foundational source is P. Delsarte, J.-M. Goethals, and J. J. Seidel,
*Spherical codes and designs*, Geometriae Dedicata 6 (1977), 363–388,
DOI `10.1007/BF03187604`. Spherical `t`-designs reproduce averages of
low-degree polynomials and supply the correct language for when trace-free
quadratic samples have zero mean.

Useful surveys and extensions include:

- E. Bannai and E. Bannai, *A survey on spherical designs and algebraic
  combinatorics on spheres*, European Journal of Combinatorics 30 (2009),
  DOI `10.1016/j.ejc.2008.11.007`;
- Y. Zhu, E. Bannai, E. Bannai, K.-T. Kim, and W.-H. Yu,
  *On spherical designs of some harmonic indices*, Electronic Journal of
  Combinatorics 24 (2017), DOI `10.37236/6437`; and
- S. Steinerberger, *Generalized designs on graphs: Sampling, spectra,
  symmetries*, Journal of Graph Theory 93 (2020), DOI `10.1002/jgt.22485`.

These references make clear that finite harmonic sampling and vanishing
averages are established subjects. The Prompt 2 distinction is not the
statement that a design kills trace-free quadratics. It is the interaction of
that sampling map with local jump covariances and exact target eigenvalues.

The exact Platonic calculations use second-moment isotropy only to exclude a
nonzero constant shifted sample. The core zero-centered rank table is proved
from explicit matrices and does not rely on numerical design recognition.

## 6. Distance-regular graphs, association schemes, and spherical embeddings

Q-polynomial association schemes provide canonical spherical embeddings into
eigenspaces and exact control of design strength through Krein parameters.
Relevant references include:

- Sho Suda, *On spherical designs obtained from Q-polynomial association
  schemes*, Journal of Combinatorial Designs 19 (2011), 167–177,
  DOI `10.1002/jcd.20278`, arXiv:0910.4628;
- E. Bannai, E. Bannai, S. Suda, and H. Tanaka,
  *On relative t-designs in polynomial association schemes*, Electronic
  Journal of Combinatorics 22 (2015), DOI `10.37236/4889`; and
- H. Kurihara, *An excess theorem for spherical 2-designs*, Designs, Codes and
  Cryptography 65 (2012), DOI `10.1007/s10623-012-9677-3`.

This literature is the natural source of future symmetry hypotheses under
which covariance spans or sampling ranks may be computable from intersection
numbers. Prompt 2 uses only an explicit transitive-equivariant irreducibility
hypothesis and exact Platonic calculations. It does not claim a new general
association-scheme theorem.

The phrase “symmetry forces full rank” is not admissible without an exact
module argument. The paper therefore states separately:

- axial stabilizer symmetry, which makes each covariance a radial/tangential
  two-parameter tensor; and
- irreducibility of `Sym_0(d)`, which makes the global exact-form kernel either
  zero or all and then excludes the latter by positivity.

## 7. Quadratic covariance and moment tensors

Jump covariance tensors

```text
C_i = sum_j a_ij (Phi_j-Phi_i)(Phi_j-Phi_i)^T
```

are elementary second moments of the outgoing stencil. Local moment tensors
are standard in probability, meshfree consistency analysis, graph geometry,
and diffusion approximation. Therefore the expansion

```text
L(Phi^T A Phi)
  = -2 lambda Phi^T A Phi + tr(A C_i)
```

is not claimed as a standalone discovery.

The Prompt 2 candidate contribution is the combined theorem package:

1. exact target residual including the constant shift;
2. trace-free covariance form constraints;
3. explicit separation of form space, sampling kernel, and sampled exact
   space;
4. the correct intersection and stacked-rank formulas;
5. axial-covariance rigidity `E_form=K_X`;
6. an all-dimensional sharp regular-simplex family;
7. an independent equivariant irreducibility theorem;
8. exact Platonic covariance/rank certificates; and
9. a sharp fixed-support signed restoration construction.

## 8. Signed graph Laplacians and inverse problems

Allowing negative conductances places the construction outside the Markov
class and into signed/generalized Laplacian inverse problems. The four-point
Prompt 2 example is deliberately explicit: conservation, coordinate modes,
quadratic mode, symmetry, and the negative sign pattern are verified by exact
matrix multiplication. The negative antipodal rate `-1/2` is forced by the
three local exactness equations on the fixed support.

The publication claim is therefore not that signed systems can solve linear
equations. It is the exact minimal sign violation for this finite eigenmap
example and the contrast with the positive axial-rigidity theorem.

## 9. Spectral-product hierarchy conclusion

Spherical harmonic products have established Clebsch–Gordan/Fischer
components and parity restrictions. A product of two degree-`l` scalar
harmonics is even, but algebraic components can vanish or alias after finite
sampling. Exactness of one sampled combination does not establish exactness of
an entire irreducible component.

The additive-resonance equation

```text
k(k+d-2) = 2 l(l+d-2)
```

is Pell-type after a linear change of variables and can have sparse infinite
arithmetic families. Arithmetic resonance alone does not identify a sampled
component or produce a dimension tradeoff. After accounting for aliases,
non-singleton maximizing sets, and the other product components, every current
obstruction reduces to the standard one-function square/Jensen identity.

Accordingly, the proposed general spectral-product hierarchy is marked
`REJECTED` for Prompt 2 under its stated kill criterion. This is not a claim
that no stronger result can emerge later from association-scheme or design
hypotheses.

## 10. Current priority conclusion

Defensible conclusions are:

- the P0/M1 local convex-hull and generic Farkas/LP cores have substantial
  prior art;
- positive spherical Laplacians and finite eigenmap embeddings have direct
  prior art;
- covariance expansion, rank-nullity, harmonic parity, carré du champ, and
  Jensen are standard inputs;
- spherical designs and Q-polynomial schemes already connect harmonic
  sampling, symmetry, and eigenspace embeddings;
- the potentially publishable Prompt 2 contribution is the genuinely sampled
  covariance theorem, axial and equivariant rigidity, sharp equality family,
  exact sampling-kernel examples, and forced signed restoration; and
- no priority claim is made for a general spectral-product hierarchy.

Before submission, complete MathSciNet/zbMATH and citation-chain review and
seek direct specialist review in finite Markov generators, spherical designs,
association schemes, discrete eigenmaps, and signed Laplacian inverse
problems.
