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

## 3. New Lean theorem

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

The initial checkpoint deliberately precedes Radiant integration. It validates
the mathematical predictions with an independent deterministic solver first.
