# Pure-math prior-art map — corrected Prompt 1 and Prompt 2 update

The principal publication risk is that a proposed statement already exists
under different terminology. This map separates standard inputs from the
sphere-specific local/global package and the genuinely sampled covariance
package. It is a working priority audit, not a claim of an exhaustive
MathSciNet or zbMATH search.

## 1. Markov generators, carré du champ, and eigenspace products

The identity

```text
Gamma(f,g) = 1/2 [L(fg)-f Lg-g Lf]
```

and Jensen positivity for Markov semigroups are standard. The finite product
identity, equality characterization, and additive sampled-square obstruction
are therefore foundational, not central novelty.

Relevant spectral-diffusion literature includes E. Azmoodeh, S. Campese, and
G. Poly, *Fourth Moment Theorems for Markov Diffusion Generators*,
arXiv:1305.5469. That program studies eigenfunctions and products under the
diffusion property. A finite jump generator is nonlocal and has a nonzero jump
carré-du-champ remainder; Prompt 2 uses that remainder but does not claim the
product identity as new.

A direct product-of-eigenfunctions comparator is S. Steinerberger,
*On the Spectral Resolution of Products of Laplacian Eigenfunctions*,
arXiv:1711.09826, published as *On the product of eigenfunctions of the
Laplacian*, Journal of Spectral Theory 9 (2019), DOI `10.4171/JST/279`.
That work also discusses Hadamard products of graph-Laplacian eigenvectors.
Prompt 2's distinction is the exact finite sampled-eigenmap covariance and
aliasing problem, not the general observation that eigenfunction products have
nontrivial spectral content.

Remaining direct-comparison targets before submission:

- finite-state generators with prescribed eigenfunctions;
- finite diffusion algebras and product-closed eigenspaces;
- equality cases for nonlocal carré du champ and Jensen;
- sampled spectral products and cross-degree aliasing; and
- inverse eigenvalue problems with fixed eigenvectors and signed weights.

## 2. Positive and minimal stencils

Benjamin Seibold, *Minimal positive stencils in meshfree finite difference
methods for the Poisson equation*, Computer Methods in Applied Mechanics and
Engineering 198 (2008), 592–601, DOI
`10.1016/j.cma.2008.09.001`, arXiv:0802.2674, uses Farkas alternatives and
geometric cone/half-space criteria for positive local stencils. Consequently,
local nonnegative consistency, separation certificates, and minimal positive
selections are standard or adjacent inputs.

The corrected Prompt 1 contribution is not the phrase “positive span.” It is
the combined spherical tangent/normal scaling, division-free antipodal
classification, exact quantitative margin and conditioning, positive masses,
shared-edge reversibility, global compatibility obstruction, and two sparse
reconciliation mechanisms.

## 3. Finite convexity, rigidity matrices, and LP duality

The following are standard finite-dimensional inputs:

- convex-hull membership and barycentric coordinates;
- relative interior and minimal faces;
- finitely generated cones and Farkas alternatives;
- finite LP strong duality and complementary slackness;
- rank-nullity and restrictions of linear maps;
- support-function/Hausdorff perturbation estimates; and
- singular-value and pseudoinverse inequalities.

The shared-edge matrix is, up to sign, the transpose of a Euclidean
bar-framework rigidity matrix. Its left kernel contains rigid motions. Prompt
1 therefore states compatibility and a positive rigidity singular-value
margin rather than a false full-row-rank assumption.

Prompt 2 likewise does not claim novelty for a bare kernel or rank formula.
Its specialized structure is

```text
R_X = (L+2d I) S_X.
```

Therefore

```text
K_X subset E_form,
E_sample = im(S_X) intersect ker(L+2d I),
dim E_sample = rank(S_X)-rank(R_X).
```

This factorization is stronger than the generic restricted-map intersection
identity and must not be replaced by treating the two matrices as unrelated.

## 4. Discrete spherical Laplacians and eigenmaps

Ivan Izmestiev and Wai Yeung Lam, *Discrete Laplacians — Spherical and
Hyperbolic*, arXiv:2408.04877, Journal of the London Mathematical Society 112
(2025), article e70235, DOI `10.1112/jlms.70235`, is a direct comparator. It
develops nonnegative spherical/hyperbolic discrete Laplacians, relates
positivity to Delaunay structure, proves exact low eigenmodes for conformal
factors, and connects them to infinitesimal polyhedral deformations.

The project must not claim the first positive spherical Laplacian or the first
exact low spherical eigenmode. The defensible distinction is the
arbitrary-node/permitted-graph positive feasibility theory and, in Prompt 2,
the exact covariance/sampling factorization and sampled quadratic rigidity for
a prescribed finite eigenmap.

Other adjacent areas include graph-Laplacian eigenmaps,
Colin-de-Verdière-type embeddings, stress matrices, and weighted inverse
eigenvalue problems. The Prompt 2 equivariant theorem is a stated
representation-irreducibility argument, not a general discrete-eigenmap
classification.

## 5. Spherical designs and quadratic harmonic sampling

The foundational source is P. Delsarte, J.-M. Goethals, and J. J. Seidel,
*Spherical codes and designs*, Geometriae Dedicata 6 (1977), 363–388, DOI
`10.1007/BF03187604`. Spherical designs provide the correct language for
finite sets reproducing low-degree polynomial averages.

Useful adjacent sources include E. Bannai and E. Bannai, *A survey on
spherical designs and algebraic combinatorics on spheres*, European Journal of
Combinatorics 30 (2009), DOI `10.1016/j.ejc.2008.11.007`, and work on designs
of specified harmonic indices. These sources show that vanishing finite
averages of trace-free quadratics and harmonic sampling are established
subjects.

Prompt 2 does not claim that a spherical 2-design kills trace-free quadratic
averages. Its contribution is the interaction of the quadratic sampling map
with local jump covariance and a prescribed target eigenvalue. The Platonic
proofs use exact evaluation matrices and determinant witnesses, not numerical
design recognition.

## 6. Distance-regular graphs, association schemes, and spherical embeddings

Q-polynomial association schemes give canonical spherical embeddings into
eigenspaces and control design strength through Krein parameters. A direct
reference is Sho Suda, *On spherical designs obtained from Q-polynomial
association schemes*, arXiv:0910.4628, Journal of Combinatorial Designs 19
(2011), 167–177, DOI `10.1002/jcd.20278`.

This literature is a natural future source of hypotheses under which
covariance spans and sampling ranks can be computed from intersection
numbers. Prompt 2 uses only:

- exact axial stabilizer symmetry, which forces a radial/tangential covariance
  form; and
- an explicitly assumed irreducible action on `Sym_0(d)`.

The phrase “symmetry forces full rank” is inadmissible without such an exact
module or tensor argument. No new general association-scheme theorem is
claimed.

## 7. Quadratic covariance and local moment tensors

Jump covariances

```text
C_i = sum_j a_ij (Phi_j-Phi_i)(Phi_j-Phi_i)^T
```

are elementary local second moments and occur throughout probability,
meshfree consistency, graph geometry, and diffusion approximation. The
expansion

```text
L(Phi^T A Phi)
  = -2 lambda Phi^T A Phi + tr(A^T C_i)
```

is therefore not claimed as a standalone discovery.

The potentially publishable Prompt 2 package is the combination of:

1. the exact shifted target residual;
2. trace-free covariance constraints;
3. the residual-through-sampling factorization;
4. the genuine sampled-space and rank formulas;
5. sharp axial-covariance rigidity;
6. a regular-simplex equality family in every dimension;
7. an independent equivariant irreducibility theorem;
8. exact Platonic covariance and sampling-kernel classifications; and
9. a forced signed restoration example.

## 8. Signed Laplacians and inverse eigenvalue problems

Allowing negative conductances leaves the Markov class and enters signed or
generalized Laplacian inverse problems. Relevant adjacent work includes
I. Agbanusi, J. C. Bronski, and D. Kielty, *A moment inequality and positivity
for signed graph Laplacians*, arXiv:2005.09608, and S. Fallat, H. Gupta, and
J. C.-H. Lin, *Inverse eigenvalue problem for Laplacian matrices of a graph*,
arXiv:2411.00292.

Those works do not by themselves provide the fixed embedded coordinate and
quadratic mode used here. The Prompt 2 signed claim is deliberately narrow and
exact: on four cardinal points, the coordinate and one quadratic exactness
conditions force adjacent rates `1` and antipodal rate `-1/2` in every row.
The claim is not merely that an unconstrained signed linear system is
solvable.

## 9. Spherical harmonic products and the hierarchy verdict

The Clebsch–Gordan/Fischer decomposition of pointwise products and the parity
of spherical harmonics are standard. The pointwise multiplication image of
`Sym^2(H_l)` must be distinguished from the full abstract symmetric tensor,
and every algebraic component must then be passed through a finite sampling
map.

The additive-resonance equation

```text
k(k+d-2) = 2 l(l+d-2)
```

is Pell-type after a linear change of variables and can have sparse infinite
families. Arithmetic resonance therefore cannot serve as a universal
obstruction. After accounting for sampling kernels, cross-degree aliases,
non-singleton maximizing sets, and the other product components, every current
positive-generator consequence reduces to the standard one-function sampled
square/Jensen equality mechanism.

Accordingly, the proposed general spectral-product hierarchy is marked
`REJECTED` for Prompt 2 under its stated kill criterion. This is not a claim
that stronger results cannot arise under future design, association-scheme, or
representation hypotheses.

## 10. Current priority conclusion

Defensible conclusions are:

- local positive-stencil convexity and generic Farkas/LP theory have substantial
  prior art;
- positive spherical Laplacians and exact low eigenmodes have direct prior art;
- covariance expansion, rank-nullity, carré du champ, Jensen, uniformization,
  and harmonic parity are standard inputs;
- spherical designs and Q-polynomial schemes already connect finite harmonic
  sampling, symmetry, and eigenspace embeddings;
- the potentially publishable Prompt 2 result is the genuinely sampled
  covariance factorization plus sharp axial/equivariant rigidity, exact
  equality family, exact aliasing examples, and forced signed restoration; and
- no priority claim is made for a general spectral-product hierarchy.

Before submission, complete MathSciNet/zbMATH and citation-chain review and
seek specialist review in finite Markov generators, spherical designs,
association schemes, discrete eigenmaps, and signed Laplacian inverse
problems.
