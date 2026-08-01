# AFP pure-math conjecture register

Every unresolved conjecture requires a precise hypothesis set, deterministic
falsification search, literature status, and explicit kill criterion. Resolved
entries remain in the file so later drafts do not regress to weaker or false
wording.

## Resolved entry C-M1. Strict local spherical feasibility

**Final statement.** For permitted non-antipodal neighbors with indexed unit
tangent directions `u_j` and `0 < theta_j < pi`:

- a nonnegative degree-one-exact row exists iff `0 in conv{u_j}`;
- an all-permitted-edge strictly positive row exists iff
  `0 in ri conv{u_j}` in its affine span;
- repeated and redundant indexed candidates are allowed;
- uniqueness is exactly augmented affine independence in the minimal face
  containing zero; and
- the normal equation fixes the unique positive scale with the explicit angular
  formula in `pure_math/SPHERICAL_LOCAL_EXACT.md`.

Antipodal neighbors have the separate complete classification in
`pure_math/SPHERICAL_LOCAL_EXACT.md`. The relative cone margin and explicit
constants are in `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md`.

**Status:** RESOLVED / PROVED ordinary; constructive finite algebra formalized.

**Evidence:**

- `pure_math/SPHERICAL_LOCAL_EXACT.md`;
- `pure_math/SPHERICAL_LOCAL_QUANTITATIVE.md`;
- `AFPBarrier/LocalSphericalFeasibility.lean`;
- `AFPBarrier/AntipodalSphericalFeasibility.lean`;
- `AFPBarrier/LocalSphericalBounds.lean`; and
- exact rational regression examples.

**Publication caution:** the finite convex-hull/relative-interior lemmas are
standard. Novelty can only be assessed for the combined spherical scaling,
antipodal, quantitative, and globally reversible package.

## Resolved entry C-G1. Global shared-edge compatibility package

**Final statement.** For fixed spherical nodes, positive masses, and an
undirected permitted graph, shared conductances solve `A gamma=b`, `gamma>=0`,
with the edge columns and signs displayed in
`pure_math/SHARED_EDGE_CONE_FARKAS.md`. Feasibility is exactly cone membership;
finite Farkas is complete; the project LPs have the stated strong duals and
complementary-slackness equations; strict feasibility is relative cone
interior; and the stated compatible perturbation bounds hold.

**Status:** RESOLVED / PROVED ordinary from standard finite Farkas and LP
strong-duality theorems, with spherical consequences formalized.

**Important falsification retained:** local strict feasibility does not imply
shared-edge feasibility, even under weighted centering. The cube in
`pure_math/SHARED_EDGE_RECONCILIATION_EXAMPLES.md` has an exact dual
certificate.

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

## C-M5. Attainable quadratic exactness

**Statement under test.** For an eigenmap `Phi` and jump covariance tensors
`C_i`, exactness of a quadratic form is equivalent to a linear contraction
condition involving `C_i`, `Phi_i Phi_i^T`, and the target eigenvalue. The
intersection of these local linear spaces gives the globally attainable
quadratic subspace.

**Status:** CONJECTURE as a theorem package; core algebraic identity derived.

**Deliverables:**

- exact local identity;
- local rank/dimension bound;
- global intersection bound;
- symmetry examples and sharpness cases;
- comparison with negative-conductance operators.

**Kill condition:** only tautological rank bookkeeping remains and no useful
sharp dimension or rigidity statement survives.

## C-M6. Spectral-product hierarchy

**Statement under test.** Positivity constrains simultaneous exactness of an
eigenspace and selected irreducible components of its symmetric square, with a
nontrivial hierarchy on spheres or compact homogeneous spaces.

**Status:** HIGH-RISK CONJECTURE.

**First tests:** Legendre and spherical-harmonic products for degrees 1--6;
strict-extremum and antipodal-maximizer cases; computational linear algebra on
Platonic and optimized graphs.

**Kill condition:** every case reduces to the same one-function square identity
without a dimension tradeoff or new global consequence.

## Rejected conjectures retained as regression warnings

- unrestricted `Q=1` classification by `K in {4,6,12}`;
- local positive rows imply a global reversible shared-edge solution;
- weighted centering alone is sufficient on every sparse permitted graph;
- global `Q>1` for every finite spherical graph;
- blanket finite-graph Bakry–Émery curvature collapse;
- standard continuum `W_2` contraction from positivity alone; and
- general order independence of layered stopping maps.
