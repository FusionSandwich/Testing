# AFP pure-math conjecture register

Every conjecture requires a precise hypothesis set, deterministic falsification
search, literature status, and explicit kill criterion. Resolved entries are
retained so earlier claim changes remain auditable.

## C-M1. Strict local spherical feasibility — RESOLVED

**Final theorem.** For permitted non-antipodal neighbors with
`0 < theta_j < pi`, a nonnegative degree-one-exact row exists exactly when the
origin lies in the convex hull of the tangent directions. A row strictly
positive on every indexed edge exists exactly when the origin lies in the
relative interior of that convex hull. Repetitions and redundant indexed
points are allowed. The minimal-face affine-independence criterion gives exact
uniqueness, and the normal equation fixes the single positive scale.

Antipodal neighbors are classified separately by a division-free normal-budget
simplex. Quantitative margin, conditioning, perturbation, and objective bounds
are stated with explicit constants.

**Status:** PROVED. See `SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md`,
Sections 1–3; Lean consequences are in
`LocalSphericalFeasibility.lean`, `SphericalFeasibilityAlgebra.lean`, and
`QuantitativeSphericalFeasibility.lean`.

**Falsification outcome:** no small counterexample survived after replacing
ambient interior by relative interior and separating antipodes. The rational
boundary-crossing tests and repeated-direction tests are retained in
`pure_math/tests/test_spherical_feasibility.py`.

**Publication warning:** the isolated convex-hull equivalence is standard
finite convex geometry and adjacent to positive-stencil theory. Any
publication claim must use the additional spherical tangent/normal structure,
fixed coordinate eigenvalue, quantitative margin, masses, reversibility, and
global compatibility theory.

## C-M1G. Local-to-global reversible compatibility — RESOLVED NEGATIVELY

**Rejected statement.** Locally feasible positive rows plus weighted centering
imply a globally reversible shared-edge solution.

**Status:** REJECTED. The cube graph with pairwise-antipodal nonuniform masses
is weighted centered and has a unique positive local row at every node, but has
no shared-edge solution. The exact Farkas field
`y_x=(x_2,x_3,x_1)/sqrt(3)` has zero edge work and `b dot y = -4`.

**Replacement theorem.** Global feasibility is membership of `b` in the
shared-edge cone. The complete graph construction and centered-clique submass
decomposition are sufficient mechanisms; arbitrary sparse graphs require the
full cone test.

## C-M2. Global equality propagation

**Statement under test.** In a connected reversible positive graph with a
symmetric spherical loss, if every row attains equality in the local
rate-defect inequality, all row rates coincide and all active edges have one
common loss.

**Status:** CONJECTURE with a short proof route; Lean formalization active.

**Kill condition:** none expected for the propagation lemma; its publication
role is supporting unless it enables a harder classification or near-rigidity
theorem.

## C-M3. Triangulated global `Q=1` classification

**Candidate statement.** A connected geodesic triangulation of `S^2` with
positive conductances on every edge, exact coordinate eigenmap, and `Q_i=1`
at every vertex must be one of the tetrahedral, octahedral, or icosahedral
triangulations, subject to a precise nondegeneracy and convex-embedding
hypothesis.

**Status:** CONJECTURE.

**Known warning:** without the triangulation restrictions, cube and
dodecahedron embeddings give immediate counterexamples.

**Falsification plan:** enumerate small spherical triangulations and symmetric
polyhedral embeddings; test equal-edge and weighted variants; search for
nonregular equal-edge triangulations.

**Kill condition:** one valid non-Platonic triangulated counterexample.

## C-M4. Quantitative near-rigidity

**Statement under test.** If every normalized active edge weight is bounded
below and `max_i(Q_i-1) <= eta`, then active edge losses differ from a global
common loss by `O(sqrt eta)` after accounting for graph diameter or overlap.

**Status:** CONJECTURE.

**Work needed:** propagate the existing local weighted-variance estimate across
shared edges; determine the unavoidable dependence on minimum conductance,
graph diameter, and rate variation.

**Kill condition:** families with `Q -> 1` but no controlled global edge-length
concentration under the stated hypotheses.

## C-M5. Attainable quadratic exactness — RESOLVED

**Corrected theorem package.** For a finite eigenmap generator,

```text
L(Phi^T A Phi)(i)
  = -2 lambda Phi_i^T A Phi_i + tr(A^T C_i).
```

For the coordinate eigenmap on `S^(d-1)`, zero-centered trace-free form
exactness is the orthogonal complement of the covariance constraints
`M_i=P_0(C_i+2 Phi_i Phi_i^T)`. Genuine sampled exactness is not the form
space itself. With

```text
S_X(A)_i = Phi_i^T A Phi_i,
K_X = ker S_X,
```

one has

```text
E_sample = S_X(E_form),
dim E_sample
  = dim E_form - dim(E_form intersect K_X).
```

In a chosen form basis, the correct rank formula is

```text
dim E_sample = rank([R;S]) - rank(R),
```

not `dim E_form - dim K_X` without an intersection calculation.

**Sharp theorem.** If every positive local jump covariance is axially isotropic
about the embedded node and has positive radial covariance, then every
covariance constraint is a positive row scaling of its sampling functional.
Consequently

```text
E_form = K_X,
E_sample = {0}.
```

The regular simplex gives a sharp all-dimensional family with a large
nonzero form space that is entirely sampling kernel. A separate equivariant
irreducibility theorem forces `E_form={0}` under a transitive symmetry action
when `Sym_0(d)` is irreducible.

**Exact examples.** The tetrahedron, octahedron, cube, icosahedron, and
dodecahedron have exact sampled dimension zero. For the first three, the
apparent nonzero algebraic form spaces are precisely the sampling kernels.
The icosahedral and dodecahedral sampling matrices have explicit nonzero
five-by-five determinants.

**Signed contrast.** On the four cardinal points of `S^1`, adjacent rates one
and antipodal rate `-1/2` preserve the coordinate eigenvalue `-1` and restore
the nonzero sampled quadratic `x^2-y^2` at eigenvalue `-4`. The three exactness
equations force the negative rate `-1/2` on that support.

**Status:** PROVED. See
`pure_math/covariance/SAMPLED_QUADRATIC_EXACTNESS_THEOREM.md`, exact regression
`pure_math/covariance/quadratic_covariance_audit.py`, and Lean module
`AFPBarrier/QuadraticCovariance.lean`.

**Publication warning:** the covariance expansion and rank-nullity identities
are supporting linear algebra. The structural contribution is the
sampling-kernel correction together with axial-covariance and equivariant
rigidity, equality families, exact examples, and signed restoration.

## C-M6. Spectral-product hierarchy — RESOLVED NEGATIVELY FOR THIS STAGE

**Investigated statement.** Positivity constrains simultaneous exactness of an
eigenspace and selected irreducible components of its symmetric square through
a nontrivial degree-indexed hierarchy.

**Audit outcome.** The carré-du-champ and semigroup/Jensen routes independently
prove the additive sampled-square obstruction. The spherical-harmonic audit
then accounted for:

- even product parity for both odd and even source degree;
- antipodal and non-singleton equality sets;
- sampling kernels and cross-degree aliases;
- the difference between one sampled combination and a complete irreducible
  component; and
- the additive resonance equation
  `k(k+d-2)=2 l(l+d-2)`.

The resonance equation is Pell-type after the substitution

```text
X=2k+d-2,
Y=2l+d-2,
X^2-2Y^2=-(d-2)^2.
```

It can therefore have sparse infinite arithmetic families, such as in
`d=4`. These arithmetic coincidences do not identify a nonzero sampled product
component and do not yield a dimension tradeoff or new global rigidity result.
At every usable resonance, the obstruction still reduces to the same
one-function sampled-square equality after all other sampled components have
been eliminated or aliased.

**Status:** REJECTED for Prompt 2 under its stated kill criterion. No general
claim is made that stronger hierarchies cannot exist under additional design,
association-scheme, or representation-theoretic hypotheses.

**Replacement result:** the sampled covariance and axial-rigidity theorem in
C-M5 is the mandatory stage theorem.

## Rejected conjectures retained as regression warnings

- local row feasibility plus weighted centering implies sparse shared-edge
  feasibility;
- unrestricted `Q=1` classification by `K in {4,6,12}`;
- form-space dimension is the same as sampled exact dimension;
- subtracting the full sampling-kernel dimension gives the sampled dimension
  without computing the intersection;
- algebraic nonzero harmonic components are automatically nonzero or
  identifiable after sampling;
- a bounded list of additive resonances is a spectral-product hierarchy;
- global `Q>1` for every finite spherical graph;
- blanket finite-graph Bakry–Émery curvature collapse;
- standard continuum `W_2` contraction from positivity alone;
- general order independence of layered stopping maps.
