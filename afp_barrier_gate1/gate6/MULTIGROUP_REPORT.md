# Gate 6 conservative multigroup checkpoint

## Physics implemented

The solver now includes:

- three descending energy groups with group-dependent speeds;
- group-dependent angular Fokker--Planck diffusion;
- nonnegative conservative down-transfer;
- absorption and transfer energy deposition;
- group-resolved inflow and boundary currents;
- particle and energy balance diagnostics;
- exact angular-collision semigroup steps;
- explicit Euler, SSPRK2, and collision-Strang integration;
- a dimensionless Hastelloy/buffer/REBCO/Ag/Cu stack.

The HTS-like coefficients are synthetic verification data and are not intended
as evaluated cross sections or material predictions.

## Deterministic results

For the level-2 matched angular grids and the functional stack:

| Family | K | Explicit steps | Strang steps | Transmitted energy (explicit) | Total heating (explicit) |
|---|---:|---:|---:|---:|---:|
| Icosphere L2 | 162 | 124 | 122 | 4.397701 | 0.758201 |
| Product N9 | 162 | 696 | 120 | 4.470499 | 0.777434 |

Within this synthetic fixture, the functional layer lowers transmitted energy
relative to the buffer-control stack and increases the fraction of deposition
in the functional region from about 7.9% to about 24.6%.

The fully explicit product grid requires about 5.6 times as many steps as the
quasi-uniform grid. Exact collision splitting makes the step counts nearly
equal because the remaining stability limit comes from streaming, absorption,
and group removal rather than the angular diffusion matrix.

## Formal scope

`AFPBarrier/MultigroupTransfer.lean` verifies particle conservation, positivity
and necessity of the group-removal CFL condition, and the exact
energy-deposition identity. The deterministic benchmark separately exercises
and audits the declared finite space--angle implementation and synthetic
multilayer tallies.
