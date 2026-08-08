# P2E preregistration — benchmark hierarchy and held-out firewall

## Status

This record freezes the P2E production operator, baseline, ablations, software
contract, reference hierarchy, partitions, response definitions, success
criteria, and output schema **before any held-out case is executed**.

The literal parent is the completed P2D archive at
`d46979d2aa52d502915eea2355a64cb788aae4f6`.

## Same-node production comparison

The production and moment-preserving monotone AFP baseline use the same 32
product-4x8 directions and masses.  They also use identical spatial cells,
energy groups, material coefficients, sources, boundary conditions, stopping
criteria, and reference definitions in every operator-quality case.

The frozen production operator is the positive H0/H1-exact shared-conductance
solution of a rate-capped degree-two Frobenius objective with a fixed
training-only directional quadratic penalty.  Its rate cap is 1.75 times the
accepted P2D baseline rate.  The registry records primal feasibility, a
numerical KKT reconstruction, conditioning, conductance hashes, and shell
metrics.  Solver success alone is not the admission criterion.

## Partitions

Every category has independent training, validation, and held-out parameters.
The production operator was designed only from its algebraic H2 objective and
six training directions.  No electron, neutron, proton, or HTS held-out result
was consulted.

The held-out hierarchy is:

1. individual real spherical-harmonic decay;
2. random band-limited angular data;
3. narrow-beam pure angular diffusion;
4. the published 10 MeV electron-in-water geometry with 40 logarithmic groups
   and a clearly labelled positive verification coefficient surrogate;
5. a first-moment-matched, forward-elastic neutron BFP limit against a full
   positive reversible Boltzmann kernel;
6. proton multiple scattering through an Al/Cu/water target;
7. an oblique charged-particle HTS tape stack.

The electron geometry is traceable to the cited published case, but the local
coefficient table is not represented as Radiant or evaluated material data.
This limitation is frozen rather than hidden.

## References and uncertainty

Analytic shell decay is used for cases 1 and 2.  Cases 3, 4, 6, and 7 use a
fine sampled spectral Laplace–Beltrami reference and a second angular order to
estimate reference uncertainty.  Case 5 uses a full positive reversible
Boltzmann scattering kernel at two angular orders; the BFP approximation is
first-moment matched.  Reference uncertainty is always stored separately from
method error.

## Success gates

The final held-out audit requires:

- exact or tolerance-audited conservation, H0/H1 reproduction, reversibility,
  monotonicity, and nonnegative flux for nonnegative-source cases;
- angular geometric-mean optimized/baseline response-error ratio at most 0.90;
- at least two of seven cases improved by at least five percent;
- median response-error ratio at most 1.05;
- worst response-error ratio at most 1.80;
- fixed-point-preserving accelerator convergence and at least a ten-percent
  iteration reduction in its declared slow-mode case.

A failed value gate does not permit retuning.  It changes the final claim.

## Ablations

The immutable operator registry and runner define:

- no H2 objective;
- no rate cap;
- no directional rotation penalty;
- a more local graph;
- a different quadrature in a separately labelled co-design comparison;
- a signed higher-accuracy reference that is not production-positive;
- accelerator-only use with the high-order production operator unchanged.

## No-held-out assertion

At this commit, no held-out P2E function has been executed and no held-out
result file exists.  The preregistration workflow checks this condition and
runs only unit tests plus the training and validation partitions.
