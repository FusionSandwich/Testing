# Pure-math prior-art map — Prompt 2 corrective closeout

This map separates standard inputs from the sphere-specific Prompt 1 package,
the genuinely sampled covariance theorem, and the corrected centered-product
boundary. It is a working priority audit, not a substitute for a final
MathSciNet/zbMATH and citation-chain review.

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

The closeout correction is the exact finite **centered** resonance statement:

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
rigidity.

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

The potentially publishable package is the combination of:

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

## 10. Global `Q=1` rigidity, maps, and spherical tilings

The abstract propagation lemma in `GlobalLossRigidity.lean` is standard
finite equality propagation and remains foundational.  Prompt 3 adds the
sphere-specific variance transfer, restricted round triangulation theorem,
and quantitative graph-global control.

Adjacent sources and tools include:

- G. Brinkmann and B. D. McKay, `plantri` and its guide, for canonical
  generation of planar triangulations.  The project source-pins the generator
  and uses it only for finite falsification through 12 vertices.
- B. Datta and D. Maity, *Platonic solids, Archimedean solids and
  semi-equivelar maps on the sphere*, arXiv:1804.06692, for adjacent
  semi-equivelar-map classification context.  The needed triangular
  `q=3,4,5` uniqueness is proved directly in the project.
- classical spherical law of cosines and Girard excess.  These supply the
  standard face formulas, not the combined generator theorem.
- Cauchy, Alexandrov, and modern spherical/framework rigidity literature as
  adjacent context.  The project does not invoke them as a hidden black box:
  geometric uniqueness follows by direct adjacent-face propagation.

The ten embedding hypotheses are essential publication boundaries.  Equal
chords without minor arcs, convex nondegenerate faces, noncrossing interiors,
full coverage/no cone defect, injectivity, and all edges active do not imply
the classification.

## 11. Reversible chains, Poincare inequalities, and resistance

Standard electrical-network and reversible-chain references include D. Levin,
Y. Peres, and E. Wilmer, *Markov Chains and Mixing Times*, second edition.
The Poincare variational definition and Dirichlet principle are standard.  The
new specialization is the explicit transfer

```text
Q_i-1 -> E_P(log r) -> Var_pi(log r), R_eff pointwise control,
```

with the exact constant `2eta/(1-delta)^2` and the conductance normalization
`c_ij=pi_i p_ij`.

## 12. Quantitative framework stability boundary

M. Holmes-Cerfon, L. Theran, and S. J. Gortler,
*Almost-rigidity of frameworks*, arXiv:1908.03802, provides adjacent
quantitative framework context.  Prompt 3 does not import an inverse-function
or rigidity-matrix theorem.  Its mandatory stability metric is only the
edge-length sup norm, derived directly from explicit arccos and spherical-law
of-cosines derivatives.  Coordinate-level stability is not claimed.

## 13. Covariance and spherical designs boundary

The radial/tangential decomposition of `C_i` is elementary tensor algebra.
The publishable boundary is the exact identification of what `Q=1` fixes,
the criterion `T_i=P_i/2`, and the positive reversible weighted-octahedron
counterexample.  No general spherical-design or covariance-isotropy theorem is
claimed from `Q=1` alone.

## 14. Priority conclusion

Defensible Prompt 2 novelty is the combined sampled covariance and positive
rigidity package, not generic convexity, rank-nullity, product calculus,
Jensen, harmonic decomposition, or representation theory. The corrective
signed-pentagon and Boolean examples define the exact boundary of the positive
and uncentered claims. Specialist review is still required before publication.


Prompt 3's defensible new boundary is the restricted classification plus the
explicit near-rigidity and covariance-interaction package.  The abstract
variance identity, Euler formula, spherical trigonometry, Poincare inequality,
and electrical principle are not claimed as novelty.  Specialist citation and
priority review remains required before publication.
