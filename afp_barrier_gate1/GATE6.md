# Gate 6: transport validation and solver consequences

**Status:** active  
**Depends on:** closed Gates 1--5  
**Scope:** deterministic AFP transport validation before Radiant integration

## 1. Objective

Gates 1--5 establish mathematical diagnostics for monotone angular
Fokker--Planck discretizations:

- peak defect `epsilon`;
- outgoing rate `r`;
- efficiency `Q = r epsilon / 4` for the degree-one spherical modes;
- low-mode eigenvalue error;
- residual error;
- rotational bias.

Gate 6 tests whether these quantities predict actual angular-transport error,
positivity-limited time step, solver work, and orientation dependence.

## 2. First deterministic benchmark

The first benchmark solves

\[
\partial_t u = \Delta_{S^2}u
\]

for a strictly positive mixture of zonal Legendre modes of degrees 2, 3, and 4.
The exact continuum solution is known because degree `l` decays as

\[
\exp[-l(l+1)t].
\]

Two discretization families are compared at matched direction counts:

1. the Gate 4 quasi-uniform spherical-Delaunay family;
2. the Gate 3 square equal-angle product family.

For each family and orientation, the benchmark computes:

- the exact semidiscrete evolution from the weighted-symmetric eigendecomposition;
- forward-Euler evolution at 90% of the positivity CFL limit;
- weighted relative error against the continuum solution;
- mass-conservation error;
- minimum solution value;
- orientation spread;
- positivity-limited step count.

## 3. Explicit time-step theorem

`AFPBarrier/ExplicitEulerTransport.lean` proves:

1. the exact convex-combination form of one Euler row;
2. exact eigenmode amplification `1 - dt lambda`;
3. sufficiency of `dt * jumpRate <= 1` for pointwise positivity;
4. necessity of the same condition for unconditional row positivity, using a
   nonnegative unit mass concentrated at the row;
5. exact weighted-integral conservation for reversible conductance operators.

This converts the Gate 4 and Gate 5 rate estimates into a direct, rigorous time
step consequence.

## 4. Gate 6 completion criteria

Gate 6 is complete when all of the following are verified:

1. exact spherical-harmonic diffusion benchmark;
2. positivity-CFL and explicit-step comparison;
3. forward-peaked scattering benchmark;
4. charged-particle angular-diffusion benchmark;
5. at least one energy-loss or material-interface benchmark;
6. comparison with Charles Bienvenue's existing Radiant AFP operator;
7. correlation analysis between mathematical diagnostics and response error,
   solver work, and rotational bias;
8. Lean and deterministic CI with exact source artifacts.

## 5. Reusable space--angle transport core

The implementation has been refactored into `gate6/core/`:

- `angular.py`: shared-edge angular operators, sparse generator application,
  exact semigroup evolution, and reference quadrature builders;
- `materials.py`: schema-validated synthetic material and layer records;
- `slab.py`: first-order upwind finite-volume streaming, inflow/vacuum
  boundaries, absorption, angular diffusion, Euler and SSPRK2 stepping, and
  exact discrete balance diagnostics;
- `manufactured.py`: a positive degree-one manufactured solution whose angular
  action is exact for every degree-one-preserving AFP operator;
- `tallies.py`: boundary currents, inventory, scalar flux, and regional
  absorption responses.

Characterization tests require the refactored angular builders to reproduce the
frozen audit implementation coefficient-for-coefficient.

## 6. Spatial manufactured solution

The slab equation is

\[
\partial_t\psi+\mu\partial_x\psi
=\kappa(x)L_\Omega\psi-\Sigma_a(x)\psi+q.
\]

The manufactured solution

\[
\psi(x,\mu,t)
=1+A e^{-\omega t}\sin(\pi x/L)\mu
\]

uses the exact coordinate relation `L mu = -2 mu`, so its measured error
isolates spatial streaming and time integration. On 20, 40, and 80 cells, both
reference angular families show monotone first-order spatial convergence while
remaining strictly positive and satisfying the finite-volume balance identity.

## 7. Thin-interface response benchmark

A three-layer beam problem contains a thin functional layer occupying 10% of
the slab. The film has larger absorption and angular diffusion than the
substrate control. The implementation reports transmitted and reflected
currents, inventory, total absorption, and layer-resolved absorption.

At level 2, the film reduces transmitted current to about 83% of the control and
increases thin-region integrated absorption by about a factor of 9.25. The
quasi-uniform and product families agree closely on the physical response, but
the product family requires over four times as many positivity-limited steps in
the spatial benchmark.

## 8. Combined space--angle positivity theorem

`AFPBarrier/SpatialUpwindTransport.lean` states the local update as

\[
\begin{aligned}
\psi^{n+1}_{c,i}={}&
\left[1-\Delta t\left(
 |\mu_i|/\Delta x+\kappa_c r_i+\Sigma_{a,c}
\right)\right]\psi^n_{c,i}\\
&+\text{nonnegative upwind, angular-neighbour, and source terms}.
\end{aligned}
\]

It proves positivity when the bracketed removal coefficient is nonnegative and
uses a concentrated unit state to show the same local CFL is necessary for
unconditional row positivity.

## 9. Conservative multigroup and HTS-like multilayer transport

The reusable core solves

\[
\partial_t \psi_g
+ v_g\mu\partial_x\psi_g
=
\kappa_g(x)L_\Omega\psi_g
-\Sigma_{a,g}(x)\psi_g
-\sum_h T_{g\to h}(x)\psi_g
+\sum_h T_{h\to g}(x)\psi_h
+q_g.
\]

The transfer matrix is nonnegative, has zero diagonal, and is restricted to
energy-degrading transitions. The implementation tracks both particle and
energy balance. Group transfer conserves particle number exactly and deposits

\[
\sum_{g,h}(E_g-E_h)T_{g\to h}\psi_g
\]

as local energy. Absorption deposits the removed group energy separately.

A dimensionless coated-conductor surrogate contains Hastelloy, buffer/MgO,
REBCO, Ag, and Cu regions. The coefficients are verification parameters, not
evaluated nuclear data. The benchmark reports group-resolved transmission,
particle inventory, energy inventory, absorption heating, transfer heating,
and region-resolved deposition.

At the level-2 matched comparison, the fully explicit product-grid case uses
696 steps versus 124 for the quasi-uniform operator. Exact angular-collision
Strang splitting reduces the counts to 120 and 122, respectively, while the
computed dimensionless surrogate tallies remain close. This demonstrates two
solver-level properties:

1. the quasi-uniform operator reduces the fully explicit angular stiffness;
2. an exact collision substep can remove that stiffness for either angular
   family without changing the declared discrete conservation equations.

## 10. Multigroup formalization and tests

`AFPBarrier/MultigroupTransfer.lean` formalizes:

- conservative transfer between finite energy groups;
- positivity of explicit Euler under the outgoing-group CFL condition;
- necessity of the same condition for unconditional group-row positivity;
- conservation of total group population;
- the exact energy-weighted transfer/deposition identity.

The deterministic test suite contains 40 tests. New tests cover the three-group
analytic cascade, particle and energy transfer balance, exact collision
semigroup conservation, HTS-like layer response, and removal of the product-grid
angular CFL penalty by collision splitting.
