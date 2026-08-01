# AFP Barrier — formally verified angular-transport theory and validation

This project develops and verifies positive, conservative angular
Fokker–Planck discretizations on the sphere.

The canonical orientation document is:

- [`HANDOFF.md`](HANDOFF.md) — complete scientific, mathematical, software,
  verification, and continuation handoff.

## Current status

- Gates 1–5 are closed mathematical milestones.
- Gate 6 is an active transport-development milestone.
- Current verified Gate 6 branch: `agent/afp-gate6-transport`.
- Current draft PR: <https://github.com/FusionSandwich/Testing/pull/9>.

The verified Gate 6 baseline includes:

- 25 deterministic unit/regression tests;
- pure angular-diffusion transport;
- forward-peaked finite-width scattering;
- continuous slowing down with energy-dependent angular diffusion;
- a two-layer order effect;
- complete Lean/Mathlib build and axiom audits;
- exact source-state artifacts.

## Build and test

```bash
python -m pip install numpy==2.3.2
python -m unittest discover -s gate6/tests -p 'test_*.py' -v

python gate6/angular_diffusion_transport_audit.py \
  --max-level 3 --time 0.1 --output-dir gate6/generated

python gate6/forward_peaked_heat_scattering_audit.py \
  --max-level 3 --time 0.1 \
  --tau 0.02 0.005 0.001 0.0002 \
  --output-dir gate6/generated

python gate6/layered_charged_particle_audit.py \
  --max-level 3 --initial-energy 5.0 \
  --output-dir gate6/generated

lake update
lake exe cache get
lake build
lake env lean AFPBarrier/AxiomAudit.lean
lake env lean AFPBarrier/Gate6AxiomAudit.lean
```

## Next implementation milestone

Refactor the verified Gate 6 builders and solvers into a small reusable Python
library, then add a manufactured one-dimensional slab problem with streaming,
inflow boundaries, angular diffusion, and conservative response tallies.

This directory currently lives in a temporary CI workspace inside
`FusionSandwich/Testing`. It should ultimately be migrated to a dedicated
repository rather than merged into the unrelated `testing` base.
