# AFP monotonicity-barrier and verified angular-transport project — technical handoff

**Workspace repository:** `FusionSandwich/Testing`  
**Canonical source directory:** `afp_barrier_gate1/`  
**Current branch:** `agent/afp-gate6-transport`  
**Current draft PR:** <https://github.com/FusionSandwich/Testing/pull/9>  
**Verified Gate 6 source commit:** `eeb09edde356c94263bc7991636229268fc90897`  
**Verified PR merge commit:** `f96cecdbf4b0b344cc297ebac8ea5bcb0e981947`  
**Verified GitHub Actions run:** `30653705532`  
**Artifact ID:** `8802444264`  
**Artifact SHA-256:** `cc3296bb6195e832cb6a3e2d7d99602991a5f4803ee9625ede4cc334b813c1ca`  
**Toolchains:** Python `3.12`, NumPy `2.3.2`, Lean/Mathlib `v4.30.0`

This repository is currently a temporary CI workspace. The AFP project should eventually move to a dedicated repository rather than merge into the unrelated `testing` branch.

---

## 1. Project objective and scientific value

The project develops positive, conservative angular Fokker–Planck (AFP) discretizations on the sphere and qualifies them mathematically and computationally.

Forward-peaked angular transport is important for charged particles, electrons and positrons, highly anisotropic neutron scattering, secondary-particle transport, thin layers, and radiation heating or damage. A useful AFP operator should be conservative, monotone, accurate on important spherical harmonics, rotationally insensitive, sparse, local, and not excessively stiff. These objectives are not automatically compatible.

The work is relevant to irradiated REBCO and other HTS coated conductors because their micrometric layers, interfaces, grazing trajectories, secondary charged particles, rare layer responses, and nuclear-heating tallies require angular transport that does not create negative fluxes or artificial orientation bias.

The project’s main contribution is not merely another angular matrix. It supplies:

1. an impossibility theorem identifying a target no finite monotone operator can attain;
2. exact geometric measures of the unavoidable error and numerical stiffness;
3. explicit positive angular families;
4. a proof of the optimal stiffness scale for quasi-uniform families;
5. deterministic transport benchmarks;
6. a tested implementation contract;
7. a reproducible path to Radiant and spatial BFP transport.

---

## 2. Core operator and diagnostics

For angular directions `Omega_i` with positive weights `w_i`, the reversible shared-edge generator is

```text
(L f)_i = (1 / w_i) sum_j gamma_ij (f_j - f_i)
```

with

```text
gamma_ij = gamma_ji >= 0.
```

Define the off-diagonal rates and total outgoing rate by

```text
a_ij = gamma_ij / w_i
r_i  = sum_j a_ij.
```

The operator is conservative because `L 1 = 0` and weighted reversible because

```text
w_i L_ij = gamma_ij = w_j L_ji.
```

The continuous Laplace–Beltrami operator satisfies

```text
Delta Y_l^m = -l(l+1) Y_l^m.
```

Degree-one exactness requires the three coordinate functions to have eigenvalue `-2`.

At a normalized zonal peak, define the active-edge loss

```text
ell_ij = 1 - Omega_i . Omega_j.
```

Then degree-one exactness gives

```text
sum_j a_ij ell_ij = 2.
```

The project uses the following diagnostics:

```text
rate:                r_i = sum_j a_ij
peak defect:         epsilon_i = sum_j a_ij ell_ij^2
efficiency:          Q_i = r_i epsilon_i / 4
low-mode error:      numerical versus exact l(l+1)
residual error:      norm of Lf + l(l+1)f
rotational bias:     variation over fixed mode orientations
positivity limit:    dt <= 1 / max_i r_i
```

---

## 3. Main mathematical results

### 3.1 Finite monotonicity barrier

A finite conservative monotone jump generator cannot be exact on both the complete degree-one and degree-two spherical-harmonic eigenspaces.

The proof uses

```text
L(f^2)(i) - 2 f(i) Lf(i)
  = sum_j a_ij (f(j) - f(i))^2.
```

At a degree-one zonal maximum, exact degree-one and degree-two behavior would make the left side zero. Positivity would then force every active neighbor to have the peak value, contradicting the required nonzero degree-one decay.

### 3.2 Exact defect and stiffness

Under exact degree-one preservation,

```text
epsilon_i = sum_j a_ij (1 - Omega_i . Omega_j)^2.
```

Cauchy–Schwarz gives the universal tradeoff

```text
4 <= r_i epsilon_i.
```

Gate 5 strengthens this to the exact variance identity

```text
r_i epsilon_i - 4
  = r_i sum_j a_ij (ell_ij - 2/r_i)^2.
```

Equality holds exactly when all strictly active edges have the same loss.

### 3.3 Positive existence and compatibility

A positive weighted-centered quadrature,

```text
sum_i w_i Omega_i = 0,
```

always admits a dense strictly positive reversible degree-one-exact construction. For a prescribed sparse graph, positive compatibility is a cone-membership problem

```text
A gamma = b,  gamma >= 0.
```

Farkas dual variables give geometric infeasibility certificates, and LP dual variables provide lower bounds and optimality certificates.

### 3.4 Explicit equal-angle family and polar barrier

Gate 3 constructs an all-orders positive latitude–longitude family. For the square family `M=2N`,

```text
maximum defect = Theta(N^-2)
maximum rate   = Theta(N^4).
```

The polar rings attain the maximum rate. This family is a useful explicit reference and counterexample, but the quartic polar stiffness makes it unsuitable as the preferred production grid.

### 3.5 Quasi-uniform family and optimal scale

Gate 4 combines maximal separated spherical nets with positive spherical-Delaunay Laplacians. It obtains

```text
maximum rate   = Theta(h^-2) = Theta(K)
maximum defect = Theta(h^2)  = Theta(K^-1),
```

where `h` is angular spacing and `K` is the number of directions.

Gate 5 proves this rate order is optimal: any monotone degree-one-exact family with `O(h^2)` peak defect must have rate `Omega(h^-2)`.

### 3.6 Explicit-Euler positivity

Lean proves the row update

```text
u_i^(n+1)
  = (1 - dt r_i) u_i^n + dt sum_j a_ij u_j^n.
```

The condition

```text
dt r_i <= 1
```

is sufficient for pointwise positivity and necessary for unconditional row positivity.

---

## 4. Gate history: what worked and what did not

### Gate 1 — Kernel-check the no-go theorem

**Worked:** finite-generator algebra, carré-du-champ identity, no-go theorem, exact defect, stiffness inequality, pinned Lean build, and axiom audit.

**Problems encountered:** the first Lean source had Finset syntax, algebra-normalization, and Cauchy–Schwarz proof-engineering errors. These were corrected without changing the mathematics. Lesson: never describe Lean source as verified until the exact pinned kernel build and axiom audit pass.

### Gate 2 — Match the Radiant convention and establish the priority boundary

**Worked:** the unshifted Radiant AFP matrix was identified as the same weighted-reversible conductance operator; the later diagonal shift was shown to cancel with the matching total-cross-section correction. Dense existence, local cone compatibility, Farkas certificates, LP weak duality, and finite source-pinned Radiant audits were added.

**Novelty boundary:** the general carré-du-champ mechanism and positive graph-Laplacian ideas are established mathematics. Candidate novelty is the AFP-specific complete-degree-two obstruction, quantitative defect/stiffness consequences, explicit constructions, and transport implications.

**CI problem:** overlapping workflows and per-file commits produced many misleading historical failures. Older gates were frozen, active workflows were given path filters, and concurrency cancellation was added.

### Attempted Gate 3A — all-orders Radiant GLC theorem

**Worked:** exact identities, central-ring results, polar asymptotics, finite audits through high order, and source comparison against Radiant.

**Unresolved:** the global all-node theorem required delicate uniform Gauss–Legendre node and weight inequalities that were not proved. The branch was retained as research history but not promoted as the canonical Gate 3 result.

### Gate 3 — explicit equal-angle reference family

**Worked:** end-to-end trigonometric proof, positive conductances, shared edges, exact quadrature normalization, complete degree-one exactness, exact defect and rate formulas, and polar maximum theorem.

**Negative result:** good low-mode error does not imply acceptable stiffness. The polar rate is quartic in the latitude resolution.

### Gate 4 — quasi-uniform positive family

**Worked:** positive spherical-Delaunay construction, normalized AFP weights and conductances, explicit all-order loss bounds, optimal `Theta(K)` rate, deterministic refinements through 10,242 directions, and node-matched product-grid comparison.

### Gate 5 — sharpness and multi-objective diagnostics

**Worked:** exact weighted-loss variance, equality and near-equality conditions, local positive-row optimum, proof of optimal rate order, higher-mode spectral audit, and rotational-bias audit.

**Important result:** no single metric dominates. The quasi-uniform family had better maximum rate, `Q`, eigenvalue error, and rotational spread, while the product family had smaller residuals in some tested modes.

### Gate 6 — transport validation and implementation contract

**Verified baseline:**

- 25 deterministic unit and regression tests;
- pure angular-diffusion evolution;
- finite-width forward-peaked heat-kernel scattering;
- continuous slowing down with energy-dependent angular diffusion;
- a two-layer order effect;
- Lean proofs for explicit Euler, heat-kernel rate bounds, and layered energy-loss identities;
- three full deterministic research audits;
- a reusable operator validator with corruption tests.

**Not complete:** spatial streaming, inflow boundaries, thin-interface response tallies, multigroup energy coupling, and full Radiant integration.

---

## 5. Current software layout

### Formal mathematics

The `AFPBarrier/` directory includes:

- `JumpGenerator.lean`
- `DiffusionProperty.lean`
- `NoGo.lean`
- `Quantitative.lean`
- `ForwardAdjoint.lean`
- `ReversibleConductance.lean`
- `CompleteGraph.lean`
- `DualCertificate.lean`
- `ImplementationConvention.lean`
- `EqualAngle*.lean`
- `QuasiUniformLossBounds.lean`
- `SphericalNetScaling.lean`
- `LossVariance.lean`
- `LossVarianceSharpness.lean`
- `ExplicitEulerTransport.lean`
- `ForwardPeakedHeatKernel.lean`
- `EnergyLossAngularDiffusion.lean`
- `AxiomAudit.lean`
- `Gate5AxiomAudit.lean`
- `Gate6AxiomAudit.lean`

### Gate 6 implementation and audits

- `gate6/operator_validation.py`
- `gate6/angular_diffusion_transport_audit.py`
- `gate6/forward_peaked_heat_scattering_audit.py`
- `gate6/layered_charged_particle_audit.py`
- `gate6/tests/test_operator_invariants.py`
- `gate6/tests/test_explicit_euler.py`
- `gate6/tests/test_forward_peaked.py`
- `gate6/tests/test_layered_charged_particle.py`
- `gate6/tests/test_transport_regressions.py`

The validator checks unit directions, positive weights and conductances, total weight `4*pi`, weighted centering, edge integrity, rate reconstruction, weighted-symmetric matrix assembly, constant preservation, and exact coordinate modes. Negative tests deliberately corrupt operators to ensure failures are detected.

---

## 6. Current deterministic results

### Angular diffusion at approximately 650 directions

```text
quasi-uniform: K=642,  steps=24,  semidiscrete error=5.883e-4
product:       K=648,  steps=971, semidiscrete error=1.111e-3
```

The product grid required about 40.5 times as many positivity-limited Euler steps.

### Layered charged-particle test

Both layer orders end at energy `3.5`, but accumulated angular depth differs:

```text
A -> B: 0.228571429
B -> A: 0.271746032
```

This is an approximately 18.9% order effect despite identical final energy.

At approximately 650 directions:

```text
quasi-uniform steps: 54 / 64
product steps:       2218 / 2637
```

### Forward-peaked scattering

For heat-kernel width `tau`,

```text
mu_tau(lambda)   = exp(-tau lambda)
beta_tau(lambda) = (1 - exp(-tau lambda)) / tau.
```

The benchmark separates continuum model error, angular-discretization error, and time-integration error because these can partially cancel.

---

## 7. Verification workflow and why it is stronger

The project uses six verification layers:

1. **Paper derivation:** state the theorem and assumptions independently of code.
2. **Lean formalization:** kernel-check the algebraic and analytic claims on a pinned toolchain.
3. **Deterministic audit:** assemble complete finite operators and check every node or fixed orientation without random sampling.
4. **Negative and regression tests:** confirm incorrect operators fail and established results do not drift.
5. **Exact-state CI:** pin Python, NumPy, Lean, Mathlib, run all checks, and archive the exact source with a digest.
6. **Physical and external-code validation:** compare against transport responses and Radiant only after the independent contract is stable.

This is stronger than a conventional derive-code-plot workflow because it:

- proves impossible targets before coefficient tuning;
- replaces vague error language with exact defect and rate identities;
- separates model, discretization, and time-integration errors;
- verifies failure behavior as well as success behavior;
- ties each result to an exact source commit and artifact digest;
- connects mathematical rate directly to positivity-limited solver work;
- prevents upstream-specific conventions from hiding mathematical errors.

The current solver is not claimed to be universally better than all existing AFP methods. The verified claims are narrower: the quasi-uniform family is much less stiff than the equal-angle reference family at matched direction counts and has better eigenvalue accuracy and rotational spread in the reported tests, while other metrics may favor the product grid in particular cases.

---

## 8. Reproduce the verified Gate 6 baseline

From `afp_barrier_gate1/`:

```bash
python -m pip install numpy==2.3.2
python -m compileall -q gate6
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

Expected Python baseline:

```text
Ran 25 tests
OK
```

The source scan must find no `sorry`, `admit`, `sorryAx`, or project-declared `axiom`.

---

## 9. What remains and recommended order

### 9.1 Create a dedicated repository

Create `FusionSandwich/AFPBarrier`, move `afp_barrier_gate1/` to its root, preserve gate reports and provenance, and do not merge the draft gate PRs into the unrelated `Testing` base.

### 9.2 Refactor a reusable Python library

Suggested structure:

```text
src/afpbarrier/
    operator.py
    grids.py
    validation.py
    evolution.py
    scattering.py
    slowing_down.py
    tallies.py
```

Keep the current audits as thin report-generating wrappers. Preserve the existing characterization tests before refactoring.

### 9.3 Add a manufactured one-dimensional slab

Solve a one-group problem with spatial streaming, inflow boundaries, angular diffusion, and a known manufactured solution:

```text
partial_t psi + mu partial_x psi = D L_Omega psi + q.
```

Record field error, boundary-current error, balance, positivity, iterations, time-step limit, and orientation dependence.

### 9.4 Add a thin two-material interface

Use two thin layers with different stopping powers, angular diffusion, and removal terms. Add conservative layer heating, reaction-rate, and interface-current tallies. This is the first benchmark directly aligned with HTS tape layers.

### 9.5 Add multigroup energy coupling

Use a small lower-triangular energy-transfer matrix. Verify positivity, particle or charge conservation, energy accounting, and convergence toward the continuous slowing-down reference.

### 9.6 Build a Radiant adapter

Do not modify Radiant first. Export or reconstruct directions, weights, edges, conductances, matrix, and diagonal-shift convention, then run `validate_operator` before comparison.

Compare:

1. Radiant pseudoinverse AFP;
2. equal-angle reference AFP;
3. quasi-uniform AFP;
4. optional LP-optimized positive AFP.

### 9.7 Correlate diagnostics with transport performance

Measure how `Q`, defect, maximum rate, low-mode error, residual, and rotational spread predict response error, stable step, condition number, iterations, and runtime.

### 9.8 Prepare the publication package

The strongest paper combines the no-go theorem, exact defect and variance theory, product-grid polar counterexample, quasi-uniform optimal construction, solver consequences, spatial and layered benchmarks, Radiant comparison, Lean appendix, and reproducibility archive.

---

## 10. Provenance ledger

| Gate | PR | Verified source | Workflow run | Outcome |
|---|---:|---|---:|---|
| 1 | 2 | `321c1c53de66dba91d89ca13b9ad129a7c1f1834` | `29615426411` | Kernel-checked no-go core |
| 2 | 3 | `16052d25afd40a519611ea531bdec6240e9fedf0` | `29635081148` | Radiant convention, compatibility, duality |
| 3 | 6 | `74574c13e0f4d0a2e1e66742da3c7ade16a962a6` | `30535434354` | Equal-angle family and polar barrier |
| 4 | 7 | `45e0fb15e3c35782924186955d66e4a034bf42b8` | `30563383216` | Quasi-uniform family and optimal scale |
| 5 | 8 | `a736f82083cb822a5cb262bdb88f0207c525b86a` | `30567007743` | Sharpness and higher-mode audit |
| 6 baseline | 9 | `eeb09edde356c94263bc7991636229268fc90897` | `30653705532` | 25 tests and three transport audits |

Additional records:

- partial GLC all-orders attempt: PR 5;
- Gate 2 priority review issue: issue 4;
- source-pinned Radiant audit commit: `205e07faa105854b0f27e95a02f01ebed08f84c1`.

---

## 11. Continuation rules

Before changing mathematics or implementation:

- read this handoff and the current gate report;
- run all 25 Python tests and all three Gate 6 audits;
- run the complete Lean build and both axiom audits;
- preserve the verified source snapshot and dependency revisions;
- distinguish formal proof, external theorem input, deterministic evidence, and physical-model assumption;
- add a negative test for every new invariant;
- report model, discretization, and time-integration errors separately;
- update the provenance ledger after each verified milestone;
- do not merge into the unrelated `testing` base.

The recommended first continuation task is to refactor the tested Gate 6 builders and solvers into a small library and then add the manufactured one-dimensional streaming-plus-angular-diffusion slab benchmark. The mathematical package is mature; the primary bottleneck is now qualified implementation and physically relevant validation.