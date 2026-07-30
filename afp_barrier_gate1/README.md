# AFP Barrier: formally verified monotone angular Fokker–Planck theory

This repository contains Lean 4 proofs and deterministic computational audits
for a sequence of mathematical results about finite monotone angular
Fokker–Planck (AFP) discretizations.

The current milestone is **Gate 3**: an explicit all-orders positive local AFP
operator on a cell-centred equal-angle spherical product grid, together with a
proved polar stiffness barrier.

## Main Gate 3 theorem

For every integer

```text
N >= 2
M >= 3
```

the construction in `AFPBarrier/EqualAngle*.lean` is:

- local, with at most four neighbours per direction;
- conservative;
- weighted reversible;
- monotone, with strictly positive conductances on every actual edge;
- exact on all three degree-one spherical-harmonic coordinate modes with
  eigenvalue `-2`;
- equipped with exact degree-two peak-defect and total-rate formulas.

For the square family `M = 2N`, the Lean development proves the finite-order
bounds

```text
2 / N^2 <= epsilon_i <= pi^2 / N^2
(8 / pi^4) * N^4 <= r_max <= N^4
```

and proves that the first and last latitude rings maximize the rate. Thus the
family has

```text
maximum second-mode defect = Theta(N^-2)
maximum jump rate          = Theta(N^4)
```

The quartic growth is a geometric polar stiffness barrier for unreduced
latitude–longitude product grids.

## Gate history

- **Gate 1:** finite-jump carré-du-champ identity, complete-degree-two
  monotonicity obstruction, exact defect identity, and defect–stiffness
  inequality.
- **Gate 2:** forward-matrix and weighted-adjoint conventions, reversible
  shared-edge conductances, dense centered construction, compatibility and
  dual certificates.
- **Gate 3:** explicit all-orders equal-angle family, end-to-end trigonometric
  coordinate proof, edge positivity, shared-edge compatibility, exact
  quadrature normalization, actual spherical dot-product losses, explicit
  finite-order bounds, and polar maximum-rate theorem.

## Gate 3 modules

- `AFPBarrier/EqualAngleProduct.lean` — local algebraic action, rates, and
  defect formulas.
- `AFPBarrier/EqualAngleGeometry.lean` — direct trigonometric balances for the
  axial and transverse coordinate modes.
- `AFPBarrier/EqualAngleGrid.lean` — all-order parameter ranges and complete
  coordinate exactness.
- `AFPBarrier/EqualAngleEdges.lean` — polar boundary closure and positivity of
  every actual edge.
- `AFPBarrier/EqualAngleConnectivity.lean` — shared-edge and reflection
  identities.
- `AFPBarrier/EqualAngleDotProducts.lean` — actual spherical neighbour losses
  and the end-to-end peak-defect formula.
- `AFPBarrier/EqualAngleQuadrature.lean` — exact telescoping normalization of
  the quadrature weights to `4*pi`.
- `AFPBarrier/EqualAngleAsymptotics.lean` — explicit finite-order defect and
  stiffness bounds.
- `AFPBarrier/EqualAngleRateMaximum.lean` — proof that the polar rings maximize
  the square-family rate.
- `AFPBarrier/AxiomAudit.lean` — public-theorem axiom audit.

The earlier Gate 1 and Gate 2 modules remain imported by `AFPBarrier.lean` and
are verified by the same superset build.

## Deterministic audit

The standard-library-only program

```text
gate3/equal_angle_product_audit.py
```

assembles complete square and non-square grids and checks every matrix row. It
uses no random sampling. It verifies:

- positive weights and every actual edge conductance;
- exact zero polar boundary conductances;
- total weight and weighted centering;
- all three degree-one eigenrelations;
- exact defect and rate identities;
- the square-family polar maximum formula;
- the Lean-proved finite-order inequalities.

Run it locally with:

```bash
python gate3/equal_angle_product_audit.py --output-dir gate3/generated
```

## Lean build

The project is pinned to Lean/Mathlib `v4.30.0`.

```bash
lake update
lake exe cache get
lake build
lake env lean AFPBarrier/AxiomAudit.lean
```

The GitHub Actions Gate 3 workflow additionally rejects `sorry`, `admit`,
`sorryAx`, and user-declared axioms, then archives the exact source snapshot
and deterministic records used in the successful run.

## Reports

- `GATE3.md` — complete mathematical statement, proof map, verification scope,
  and novelty boundary.
- `gate3/PROFESSOR_REPORT.md` — concise briefing for discussion with Professor
  Charles Bienvenue and the supervisory team.

## Scope boundary

The all-orders theorem is for the equal-angle reference family. It does not
claim an all-orders result for Radiant's Gauss–Legendre–Chebyshev family.
Radiant integration and physical transport benchmarks are intentionally
reserved for the next stage, after the mathematical package is frozen.

The strongest next theorem is a reduced-ring or quasi-uniform spherical family
that retains positivity and complete degree-one exactness while reducing the
worst-case rate from `Theta(N^4)` toward `Theta(N^2)`.
