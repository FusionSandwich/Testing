# AFP pure-math conjecture register

Every conjecture requires a precise hypothesis set, deterministic falsification
search, literature status, and explicit kill criterion. Resolved entries are
retained so earlier claim changes remain auditable.

## C-M1. Strict local spherical feasibility — resolved

**Proved statement.** For candidate neighbors with tangent directions
`u_j` and angles `0 < theta_j < pi`, a degree-one-exact row with every rate
strictly positive exists if and only if the origin lies in the relative
interior of `conv{u_j}`. Once a positive tangent dependence is selected, the
normal-loss equation fixes one positive scale.

**Status:** PROVED, including repetitions, redundant points, lower-dimensional
span, exact scaling/rate/uniqueness, antipodes, quantitative margins, and
explicitly identified-span perturbation stability. See
`pure_math/EXACT_LOCAL_GLOBAL_THEOREM_PACKAGE.md` and the independent
`SPHERICAL_FEASIBILITY_SHARED_EDGE_THEOREM.md` development.

**Resolved deliverables:**

- the scaling map is a bijection with the normalized dependence polytope;
- positive indexed dependences are equivalent to relative interior;
- antipodes form a separate residual normal-budget simplex;
- `rho`, `beta_*`, rate, coefficient, support, and singular-value margins are explicit;
- standard positive-stencil inputs are separated from sphere-specific results.

**Regression warnings:** lower-dimensional perturbations require a fixed or
explicitly identified intrinsic span; uniqueness means existence and uniqueness.
Exact repeated-direction and boundary-crossing regressions are retained in both
`pure_math/examples/exact_local_global_audit.py` and
`pure_math/tests/test_spherical_feasibility.py`.

## C-M1G. Global local-to-shared compatibility — resolved negatively and conditionally

The unrestricted implication is REJECTED by two independent exact examples:
the centered unequal-mass equatorial four-cycle, and the weighted-centered
cube with a heavy antipodal pair. The cube certificate
`y_x=(x_2,x_3,x_1)/sqrt(3)` has zero edge work and `b dot y=-4`.
Complete-graph sufficiency, equivariant orbit averaging, and centered-clique
submass decomposition are PROVED reconciliation results. Further sparse
classifications must survive both regression examples.

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

## C-M5. Genuine sampled quadratic exactness — resolved

**Proved theorem package.** For an eigenmap `Phi` and jump covariance tensors
`C_i`, the quadratic target residual is the exact covariance contraction. In
the spherical degree-two specialization,

```text
R_X = (L+2d I) S_X,
E_form = ker R_X,
K_X = ker S_X subset E_form,
E_sample = im(S_X) intersect ker(L+2d I).
```

Hence

```text
dim E_sample
  = dim E_form-dim K_X
  = rank(S_X)-rank(R_X).
```

Under positive axial covariance at every vertex,

```text
E_form = K_X,
E_sample = {0}.
```

**Status:** PROVED. The sharp theorem has two independent structural routes:
axial covariance row scaling and transitive irreducibility of `Sym_0(d)`.
Regular simplices attain the axial theorem in every dimension. Exact Platonic
proofs give form dimensions `2,3,2,0,0` and sampled dimensions all zero.

**Signed contrast:** the four cardinal points of `S^1` with adjacent rates
`1` and antipodal rates `-1/2` restore one genuine quadratic sampled mode; the
negative antipodal rate is forced on that fixed support.

**Regression warnings:**

- never report `dim E_form` as a sampled mode count;
- never treat `R_X` and `S_X` as unrelated matrices;
- sampling aliases are automatically in `E_form` because the residual factors
  through sampling;
- numerical rank thresholds are not exact proof.

## C-M6. General spectral-product hierarchy — rejected for Prompt 2

**Tested statement.** Positivity constrains simultaneous exactness of an
eigenspace and selected irreducible components of its symmetric square through
a nontrivial degree-indexed hierarchy.

**Outcome:** REJECTED under the stated kill criterion.

The audit accounted for:

- even product parity in the pointwise multiplication image;
- odd/even zonal antipodal equality sets;
- non-singleton maxima;
- degree-specific sampling kernels and cross-degree aliases;
- one sampled combination versus a complete irreducible component; and
- the additive-resonance equation
  `k(k+d-2)=2l(l+d-2)`.

The resonance equation is Pell-type and even has sparse infinite families,
so absence of resonance is not the obstruction. The problem is
identifiability: without proving that all other sampled product components
vanish or separate, no component is isolated. Whenever those extra conditions
hold, the conclusion is exactly the one-function carré-du-champ/Jensen square
obstruction. No new `l`-indexed dimension tradeoff or global consequence
survived.

**Status:** REJECTED for the general Prompt 2 branch, not declared impossible
under future association-scheme, design, or representation-theoretic
hypotheses.

## Rejected conjectures retained as regression warnings

- local row feasibility plus weighted centering implies sparse shared-edge
  feasibility;
- unrestricted `Q=1` classification by `K in {4,6,12}`;
- global `Q>1` for every finite spherical graph;
- blanket finite-graph Bakry–Émery curvature collapse;
- standard continuum `W_2` contraction from positivity alone;
- general order independence of layered stopping maps;
- algebraic quadratic form dimension equals genuine sampled exact dimension;
- a Pell-type additive resonance by itself yields a spectral-product hierarchy.
