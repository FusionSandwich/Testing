# AFP pure-mathematics track

This branch separates the theorem-driven mathematics program from the frozen
Gate 6 transport implementation.

## Frozen transport baseline

The verified transport source is preserved on
`archive/afp-gate6-spatial-multigroup-verified` at commit
`515f1aae6c20bd85711c90b5c1c21b4905252d01`.

Transport, Radiant integration, evaluated material data, and physical HTS
benchmarks are deferred. They are not deleted or superseded by this stage.

## Pure-math objective

The intended paper is not centered on the elementary inequality

```text
lambda^2 <= rate * defect.
```

That inequality and its weighted-variance remainder are foundational lemmas.
The publication target is a theorem package about finite positive generators
that remains interesting without AFP terminology:

1. local positive feasibility on spherical eigenmap embeddings;
2. quantitative robustness and exact angular scaling;
3. global reversible shared-edge compatibility and duality;
4. attainable quadratic spectral-product exactness; and
5. global equality propagation and geometric rigidity.

## Completed sphere-feasibility stage

The ordinary proof package begins at

```text
pure_math/SPHERICAL_FEASIBILITY_AND_SHARED_EDGE_DUALITY.md
```

That index links the exact local, quantitative local, global cone/Farkas,
optimization-dual, strict-sensitivity, and reconciliation/example theorem
blocks. Together they establish:

- exact non-antipodal convex-hull and relative-interior equivalences;
- repeated/redundant candidate and uniqueness cases;
- unique normal scaling and the explicit spherical rate formula;
- a complete separate antipodal classification;
- a relative cone margin with explicit coefficient, rate, conditioning,
  perturbation, and objective constants;
- the global edge-column cone and feasible polytope;
- weighted centering and the dense complete-graph construction;
- the full finite Farkas alternative with AFP signs;
- strong duality and complementary slackness for project LPs;
- strict global feasibility and node/mass sensitivity;
- a centered-clique sparse reconciliation mechanism; and
- exact local/global compatible and incompatible examples.

See also:

```text
docs/SPHERICAL_FEASIBILITY_STAGE_REPORT.md
docs/SPHERICAL_FEASIBILITY_APPROACH_REGISTRY.md
docs/SPHERICAL_FEASIBILITY_ADVERSARIAL_AUDIT.md
docs/THEOREM_TO_FILE_MAP.md
docs/CLAIM_MATRIX.md
docs/CONJECTURE_REGISTER.md
docs/PURE_MATH_PRIOR_ART_MAP.md
```

## Exact regression command

From `afp_barrier_gate1`:

```text
python pure_math/examples/spherical_feasibility_examples.py
```

The script uses rational arithmetic and verifies the deterministic local,
antipodal, perturbation, cube incompatibility, Farkas, and primal/dual examples.

## Lean verification

The project uses Lean 4.30.0 and Mathlib 4.30.0. The sphere-feasibility stage
adds narrowly scoped modules for antipodal budgets, local rate bounds,
shared-edge strain geometry, and complementary slackness. The full finite
convex and LP theorems remain ordinary proofs with precisely stated external
infrastructure; their spherical finite consequences are formalized where
practical.

Build from `afp_barrier_gate1`:

```text
lake build
```

No `sorry`, `admit`, `sorryAx`, or user-declared axioms are permitted.

## Remaining scientific gates

### M2 — global equality propagation

If every row attains equality in the local rate-defect bound, all active edges
at a vertex have one loss. Reversibility and graph connectivity should
propagate one common edge loss and one common row rate. Classification is only
attempted under explicit geometric restrictions such as spherical
triangulation.

### M3 — quadratic covariance

For an eigenmap `Phi`, introduce the jump covariance

```text
C_i = sum_j a_ij (Phi_j - Phi_i)(Phi_j - Phi_i)^T.
```

The target is an exact characterization and dimension bound for the quadratic
forms reproduced with a prescribed eigenvalue. Merely repeating the full
quadratic no-go theorem is insufficient.

## Claim discipline

Every statement is labeled one of:

- `PROVED` — complete proof under stated assumptions;
- `EXTERNAL` — direct use or specialization of a cited theorem;
- `COMPUTATIONAL` — finite deterministic verification only;
- `CONJECTURE` — survived current tests but is unproved; or
- `REJECTED` — false, ill posed, redundant, or strategically unsuitable.

Lean and CI are verification infrastructure, not mathematical novelty. The
rowwise convex-hull criterion is standard adjacent-field mathematics; the
candidate contribution is the additional spherical tangent/normal structure,
antipodal theorem, quantitative margin, positive masses, and global reversible
compatibility package.
