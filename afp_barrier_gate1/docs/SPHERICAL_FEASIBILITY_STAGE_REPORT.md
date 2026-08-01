# Sphere-specific feasibility and shared-edge duality — stage report

## Baseline and scope

- Repository: `FusionSandwich/Testing`
- Source branch: `agent/afp-pure-math-p0-m1`
- Verified checkpoint: `4efef67a20cdb8b2437cad093ccc16bcd0f17796`
- Checkpoint comparison: the source branch was identical to the checkpoint when
  this stage began.
- Frozen transport archive: `archive/afp-gate6-spatial-multigroup-verified` at
  `515f1aae6c20bd85711c90b5c1c21b4905252d01`

No transport, Radiant, HTS, multigroup, or spatial-solver source was changed.
This stage changes only the pure-mathematics proof, exact examples, Lean finite
algebra, and claim-control documentation.

## Result

The stage proves the requested package through the index
`pure_math/SPHERICAL_FEASIBILITY_AND_SHARED_EDGE_DUALITY.md`, which links six
reviewable proof blocks:

1. exact non-antipodal nonnegative and all-edge-strict feasibility;
2. exact uniqueness/nonuniqueness of indexed tangent dependences;
3. separate antipodal-only and mixed antipodal classification;
4. a relative cone-surrounding margin with explicit coefficient, rate,
   conditioning, perturbation, and objective constants;
5. the global shared-edge cone and feasible-polytope characterization;
6. weighted-centering necessity and the dense complete-graph construction;
7. the complete finite Farkas alternative with the AFP matrix signs;
8. strong LP duals and complementary slackness for linear, peak-rate, and
   weighted-residual formulations;
9. strict global feasibility and sensitivity estimates;
10. a centered-clique reconciliation construction; and
11. exact local/global counterexamples and primal/dual certificates.

The complete finite convex-geometry and LP theorems are ordinary mathematical
proofs. Lean mirrors the constructive spherical scaling, antipodal budget,
loss-window bounds, shared-edge strain identities, certificate soundness,
duality-gap identity, and complementary-slackness consequences. The full
finite Farkas alternative and finite LP strong-duality theorem are invoked in
precisely stated standard forms rather than re-axiomatized in Lean.

## Proof-search and audit records

The independent approach families, redirects, and blocked routes are recorded
in `docs/SPHERICAL_FEASIBILITY_APPROACH_REGISTRY.md`. The line-by-line
failure-mode audit is in
`docs/SPHERICAL_FEASIBILITY_ADVERSARIAL_AUDIT.md`.

## Exact regression suite

Run from `afp_barrier_gate1`:

```text
python pure_math/examples/spherical_feasibility_examples.py
```

The suite uses `fractions.Fraction`; it checks tangent hull outside, boundary,
and relative interior; repeated/redundant directions; rational boundary
crossings; all antipodal cases; strict local cube rows; weighted centering with
global incompatibility; the exact Farkas certificate; and a strict global cube
with exact primal/dual equality.

Expected output:

```text
PASS: exact tangent, antipodal, perturbation, and shared-edge examples
```

## Lean scope

New or extended finite formalization:

- `AFPBarrier/LocalSphericalFeasibility.lean` — existing constructive scaling;
- `AFPBarrier/AntipodalSphericalFeasibility.lean` — separate antipodal budgets
  and unique common scale;
- `AFPBarrier/LocalSphericalBounds.lean` — outgoing-rate loss-window bounds;
- `AFPBarrier/SharedEdgeGeometry.lean` — endpoint column work, strain symmetry,
  and chord-length first variation;
- `AFPBarrier/DualCertificate.lean` — existing finite transpose, weak duality,
  and certificate soundness;
- `AFPBarrier/DualComplementarity.lean` — exact duality gap,
  complementary slackness, and strict-solution dual-face consequence;
- `AFPBarrier/CompleteGraph.lean` and `AFPBarrier/ReversibleConductance.lean` —
  existing dense construction and centering necessity.

No `sorry`, `admit`, `sorryAx`, or user-declared axioms are introduced.

## Claim boundary

The local convex-hull and relative-interior lemmas are standard finite convex
geometry. Finite Farkas and LP strong duality are standard. The publication
claim must therefore be the combined sphere-specific package: tangent/normal
separation, antipodal handling, exact angular rescaling, quantitative margin,
positive quadrature masses, reversible shared edges, global compatibility and
dual geometry, and the exact local/global separation. It must not be described
as the discovery of positive-stencil convex-hull feasibility itself.
