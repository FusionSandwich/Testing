# P2E pre-registration development plan

## Status and lineage

This is a **training-only development stage**, not the immutable benchmark
manifest and not held-out benchmark evidence.

- repository: `FusionSandwich/Testing`
- literal parent: `archive/afp-publication-p2c-codesign-verified`
- parent SHA: `b34c29b1b04f5293eaa4007b39d189efa03c51f5`
- development branch: `agent/afp-publication-p2e-benchmark-development-b34c29b1`
- P2D status at branch creation: no prompt-specific branch or accepted archive

P2E is required to use one frozen software version and an immutable manifest,
to compare production operators on identical angular nodes, to keep
quadrature changes in a separate co-design study, and to freeze success gates
before final comparisons.  The immutable manifest is therefore intentionally
not created until the training-only operator probe and benchmark harness have
passed their development audit.

## Baseline firewall

The production baseline is the published-style shared-conductance construction:

1. fix the quadrature nodes and positive masses;
2. use the local weak-Delaunay/Voronoi-neighbor graph;
3. solve the shared first-moment system by the minimum-Euclidean-norm
   pseudoinverse;
4. accept it only when the independently recomputed moment residual is within
   tolerance and every conductance is nonnegative.

The accepted dense centered formula `2 w_i w_j` is retained only as a
complete-graph feasibility and normalization control.  It is not silently
relabeled as the published local AFP baseline.

## New-method training probe

On the same nodes and masses, augment the local graph deterministically with
nearest-neighbor edges and solve the accepted globally optimal P2A fixed-data
problem.  The rate cap is frozen from the baseline before optimization:

```text
R = max(4, 1.75 * baseline_rate)
```

Candidate selection uses training data only and is lexicographic:

1. smallest optimized-to-baseline `H_2` defect ratio;
2. smallest sampled collision-only rotation spread;
3. smallest node count;
4. family name.

No electron, neutron, proton, HTS, or other held-out response is inspected by
this selection.

## Planned immutable P2E manifest

After development passes, a distinct descendant commit will freeze:

- source and dependency versions;
- exact nodes, masses, graphs, and conductance hashes;
- training, validation, and held-out partitions;
- all seven mandatory benchmark definitions;
- reference methods and reference-uncertainty estimators;
- invariant, response, runtime, and memory metrics;
- equal-direction, equal-wall-time, and equal-response-error protocols;
- all seven ablations;
- quantitative success criteria;
- the explicit boundary that an accelerator-only ablation is computational
  P2E evidence and does not complete the absent P2D theorem package.

Held-out execution is forbidden before that manifest commit exists.
