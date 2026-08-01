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

- local row feasibility plus weighted centering implies sparse shared-edge
  feasibility;
- unrestricted `Q=1` classification by `K in {4,6,12}`;
- global `Q>1` for every finite spherical graph;
- blanket finite-graph Bakry–Émery curvature collapse;
- standard continuum `W_2` contraction from positivity alone;
- general order independence of layered stopping maps.
