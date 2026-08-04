# AFP publication program — approach registry

## 1. Execution model

Literal multiagent-v2 was not exposed in the repository execution environment for this baseline task. No claim is made that it ran. Independence was preserved through separate audit routes with distinct evidence, failure criteria, and authority rules.

This prompt is a state-establishment prompt, not a theorem-discovery prompt. Every route below is therefore directed toward exact provenance, claim control, normalization, falsification, paper boundaries, or reproducibility. No route is permitted to add new mathematics.

## 2. Active audit routes

| Route | Mechanism | Independent evidence | Status | Failure condition |
|---|---|---|---|---|
| A. Live-ref resolution | Resolve target, PRs, branch heads, trees, and archive refs from current GitHub objects. | GitHub branch/PR objects and commit comparisons. | COMPLETE | relying on a historical prompt hash without resolving the live ref |
| B. Ancestry classification | Compare old baselines, rich source, reconciliation source, divergent archives, and current target. | merge-base and ahead/behind comparisons. | COMPLETE | treating ordinary mutable-ref movement as candidate overwrite |
| C. Diff and scope audit | Enumerate accepted changed paths from `94aebf...` and from historical `c88b575...`. | GitHub per-file compare records. | COMPLETE | any unrecorded transport, generated, or bootstrap path |
| D. Normalization audit | Reconcile Lean definitions, ordinary theorem conventions, and weighted reversible notation. | `JumpGenerator.lean`, `ForwardAdjoint.lean`, `ReversibleConductance.lean`, covariance sources. | COMPLETE | hidden weight normalization, sign reversal, or factor-of-two ambiguity |
| E. Sampling audit | Keep form space, sampling kernel, residual map, and sampled eigenspace separate. | factorization theorem, Lean restricted-map lemmas, exact Platonic aliases. | COMPLETE | a form-space rank is presented as sampled dimension |
| F. Hypothesis-deletion audit | Maintain exact negative examples for every attractive stronger claim. | cube, dodecahedron, sparse Farkas examples, signed square/pentagon, antipode, weighted octahedron. | COMPLETE | a deleted hypothesis lacks a surviving exact obstruction or proof |
| G. Exact-value audit | Recompute the five Platonic rows and compare with accepted symbolic source. | rational and `Q(sqrt(5))` arithmetic; exact rank audits. | COMPLETE | floating fit or rounded value replaces an exact expression |
| H. Formal verification audit | Rerun full Lean, focused axiom report, placeholder scans, lean4export, and nanoda. | publication-baseline workflow on the literal descendant head. | REQUIRED BEFORE FREEZE | any source head mismatch, `sorryAx`, user axiom, or checker error |
| I. Computational-role audit | Separate finite enumeration and stress tests from theorem proof. | Plantri, exact symbolic tests, interval/positive-width checks. | COMPLETE | fixed-size computation is promoted to all-orders proof |
| J. Prior-art transfer audit | Read M1–M6 and current repository prior-art records; map exact overlap and non-overlap. | primary arXiv records and repository citation map. | COMPLETE | an external theorem is transferred without matching hypotheses |
| K. Paper-boundary audit | Assign unique theorem ownership to Papers I–III and list all consumed files. | theorem registry, final theorem package, source tree inventory. | COMPLETE | duplicate flagship claims or cross-paper scope drift |
| L. Archive-safety audit | Create a new SHA-named line and freeze a new archive only after green exact-head verification. | branch/ref equality and workflow artifact. | REQUIRED BEFORE FREEZE | moving an existing archive or accepted source branch |
| M. Adversarial publication audit | Check novelty language against foundational identities and external results. | prior-art matrix and rejected-claim registry. | COMPLETE | local variance, generic Farkas, or generic rank-nullity is called the flagship |

## 3. Approach families preserved for later prompts

### 3.1 Convex and dual formulations

Mechanisms:

- indexed tangent convex hull and relative interior;
- shared-edge cone and Farkas alternative;
- sliced feasible-cone LP and dual anisotropy certificate;
- Gale/eigenpolytope and spectrahedral comparators.

Current use: Paper I construction/compatibility and Paper III feasible-cone theory.

Boundary: generic convex separation, Farkas, and LP duality are external. Publication value must come from the spherical normalization, shared-edge coupling, exact sampling relation, or sharp finite-generator conclusion.

### 3.2 Spectral and sampling formulations

Mechanisms:

- covariance expansion;
- residual-through-sampling factorization;
- sampling aliases and genuine sampled eigenspaces;
- centered product resonance;
- graphical-design comparators.

Current use: Paper II flagship.

Boundary: algebraic forms and sampled functions are never conflated. Arithmetic resonance alone is insufficient.

### 3.3 Geometric and combinatorial formulations

Mechanisms:

- exact spherical loss propagation;
- minor-arc geodesic triangulations;
- common-angle and Euler reduction;
- direct combinatorial uniqueness;
- forced adjacent-face propagation;
- Gram/spherical-Heron stability.

Current use: Paper III companion theorem.

Boundary: cube and dodecahedron kill unrestricted classification. Plantri is hostile falsification only.

### 3.4 Markov-energy formulations

Mechanisms:

- logarithmic row-rate cocycle;
- path/diameter bounds;
- reversible Dirichlet energy;
- Poincaré gap;
- effective resistance.

Current use: Paper III quantitative theorem.

Boundary: no metric-free pointwise control; small active weights, long paths, small gaps, and large resistance remain explicit stress directions.

### 3.5 Formal and exact-computational formulations

Mechanisms:

- narrow Lean modules;
- exact rational/algebraic scripts;
- source-pinned Plantri;
- independent lean4export/nanoda;
- immutable artifacts and digests.

Current use: all papers’ reproducibility appendices.

Boundary: CI establishes exact source verification, not mathematical novelty.

## 4. Permanently blocked or killed approach families

| Family | State | Reason | Reopen only if |
|---|---|---|---|
| unrestricted equal-edge/Platonic classification | REJECTED | cube and dodecahedron | a new theorem states additional hypotheses and survives all five Platonic cases |
| endpoint-product angle certificate | REJECTED | failed required icosahedral positive-width domain | a strictly stronger certified domain is proved; accepted route remains Gram/Heron |
| Delsarte/Gegenbauer replacement theorem | BLOCKED | no sampling-aware solved dual certificate | explicit exact dual certificate |
| Bakry–Émery one-function route | REJECTED FOR PROMPT 4 | one `Gamma_2` identity is not a CD theorem | full curvature matrix/CD proof |
| coordinate stability from edge lengths alone | BLOCKED | no uniform framework margin | certified gauge and singular-value/nonlinear radius |
| general split/merge ring theorem | BLOCKED | only biregular/perfect-matching class solved | complete construction or nonexistence proof |
| continuum transport-metric inference | BLOCKED | wrong metric transfer | exact discrete entropy/curvature theorem |
| generic higher-degree hierarchy | REJECTED AS STATED | aliases and missing multiplicity separation | sampling-aware structural factorization |

## 5. Adversarial checklist

Before any future claim is promoted, check:

```text
sign and diagonal convention;
normalization of weights and conductances;
factor 1/2 in Gamma;
spherical eigenvalue and target eigenvalue;
sampling kernel and zero sampled functions;
inactive and zero-conductance edges;
antipodal and repeated states;
cube and dodecahedron;
signed square and signed pentagon;
sparse local-but-not-global Farkas examples;
small kappa and long paths;
small spectral gap and large resistance;
Gram/Heron positivity domain;
weighted-octahedral tangent anisotropy;
fixed graph versus variable graph;
ring-symmetry assumptions;
external theorem hypotheses;
finite computation versus all-orders proof;
source SHA, tree, archive ref, and artifact digest.
```

## 6. Root-agent synthesis rule for later prompts

Later work should keep several independent routes active until their real boundaries are exposed. A route that stops at a theorem-strength compatibility lemma, an uncertified numerical observation, or a missing sampling-injectivity statement is `BLOCKED`, not nearly complete.

Cross-pollination is permitted only after independent route records exist. Any new theorem must receive:

1. line-by-line proof audit;
2. hypothesis-deletion/counterexample audit;
3. normalization and sampling audit;
4. external-transfer audit;
5. Lean/formal boundary audit;
6. deterministic exact-computation audit where applicable;
7. paper-boundary and prior-art audit.

The publication baseline itself is complete only when the exact descendant head passes its dedicated gate and the immutable publication archive is created.
