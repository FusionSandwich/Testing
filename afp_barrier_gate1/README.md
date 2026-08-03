# AFP Barrier: formally checked angular Fokker--Planck transport research

This project combines Lean 4 proofs with deterministic numerical audits for
monotone angular Fokker--Planck (AFP) discretizations and their use in particle
transport.

## Mathematical gates

- **Gate 1:** finite-jump carré-du-champ identity, complete-degree-two
  monotonicity obstruction, exact peak-defect identity, and the universal
  defect--stiffness inequality.
- **Gate 2:** forward-matrix and weighted-adjoint conventions, reversible
  shared-edge conductances, centered constructions, compatibility conditions,
  and dual certificates.
- **Gate 3:** explicit all-orders equal-angle product family, exact degree-one
  modes, finite-order defect bounds, and a quartic polar stiffness barrier.
- **Gate 4:** quasi-uniform positive spherical construction with the natural
  `Theta(h^-2)` diffusion-rate scale and `Theta(h^2)` peak defect.
- **Gate 5:** exact sharpness remainder, equality and near-equality conditions,
  optimal rate order, higher-mode error, and rotational-bias audits.

## Gate 6 transport implementation

Gate 6 contains a reusable deterministic transport core in `gate6/core/`:

- weighted-reversible angular operators;
- positive first-order upwind slab streaming;
- inflow and vacuum boundaries;
- spatially varying absorption and angular diffusion;
- Euler and SSPRK2 integration;
- exact angular-collision semigroup steps and Strang splitting;
- conservative multigroup down-transfer;
- particle and energy balance diagnostics;
- absorption and transfer heating tallies;
- regional response tallies for thin multilayers.

The deterministic physics benchmarks include:

1. exact spherical-harmonic angular diffusion;
2. finite-width forward-peaked heat-kernel scattering;
3. continuous slowing down with order-dependent angular broadening;
4. a manufactured 1-D space--angle slab solution;
5. a thin functional-layer interface benchmark;
6. a three-group Hastelloy/buffer/REBCO/Ag/Cu numerical surrogate.

The coated-conductor coefficients are synthetic verification data, not
evaluated nuclear data and not material predictions.

## Formal Gate 6 coverage

Lean modules verify:

- the exact explicit-Euler positivity limit for a jump generator;
- the combined streaming--collision--absorption local CFL condition;
- necessity of both conditions for unconditional row positivity;
- heat-kernel scattering moment and Fokker--Planck-limit inequalities;
- continuous-slowing-down and two-layer angular-depth identities;
- conservative multigroup transfer;
- multigroup positivity and population conservation;
- the exact energy-deposition identity for group transfer.

The focused audit is `AFPBarrier/Gate6AxiomAudit.lean`.

## Deterministic verification

The Gate 6 workflow runs, in order:

```text
Python syntax/import audit
unit and regression tests
angular-diffusion audit
forward-peaked scattering audit
layered charged-particle audit
spatial slab/thin-interface audit
multigroup HTS-like slab audit
Lean/Mathlib kernel build
main and Gate-6 axiom audits
proof-placeholder and user-axiom scans
```

Run the local deterministic suite from `afp_barrier_gate1` with:

```bash
python -m compileall -q gate6
python -m unittest discover -s gate6/tests -p 'test_*.py' -v
python gate6/spatial_slab_transport_audit.py --max-level 2 --output-dir gate6/generated
python gate6/multigroup_hts_transport_audit.py --max-level 2 --cells 60 --final-time 1.6 --output-dir gate6/generated
```

## Lean build

The project is pinned to Lean/Mathlib `v4.30.0`:

```bash
lake update
lake exe cache get
lake build
lake env lean AFPBarrier/AxiomAudit.lean
lake env lean AFPBarrier/Gate6AxiomAudit.lean
```

See `GATE6.md`, `gate6/SPATIAL_CORE_REPORT.md`, and
`gate6/MULTIGROUP_REPORT.md` for the current transport scope and numerical
results.
