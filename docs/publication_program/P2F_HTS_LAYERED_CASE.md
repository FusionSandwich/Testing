# P2F layered HTS response diagnostic

## Purpose and terminal outcome

This controlled surrogate asks whether replacing a frozen moment-monotone AFP
operator by the frozen optimized harmonic-fidelity operator produces a
resolvable change in selected coated-conductor responses.  It is a finite
deterministic verification problem, not an evaluated nuclear-data or
production-physics calculation.

The structural integrity audit passes.  The scientific outcome is
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`:

- none of the 18 baseline/optimized error differences is resolved;
- there are zero resolved improvements and zero resolved degradations;
- the maximum relative difference between the selected baseline and optimized
  responses is `1.9424183391e-14`, so this fixture is effectively insensitive
  to the operator replacement; and
- the 50/72/98/128-direction reference sweep fails the declared 5% relative-
  span convergence gate in every incidence case, most severely at grazing
  incidence.

Consequently this case supports neither a benefit claim nor a degradation
claim.  The former `BOUNDED_NEGATIVE` label is withdrawn.

## Stack

| Layer | Material | Thickness |
|---|---|---:|
| Front stabilizer | Cu | 20.0 µm |
| Cap | Ag | 2.0 µm |
| Superconductor | REBCO | 1.0 µm |
| Buffer | oxide surrogate | 0.2 µm |
| Substrate | Hastelloy C-276 surrogate | 50.0 µm |
| Back stabilizer | Cu | 20.0 µm |

Total thickness is 93.2 µm.  These values are representative verification
inputs and do not certify a particular commercial tape.

The frozen incidence cases are 0° normal, 60° oblique, and 84° grazing-
sensitive incidence.  The grazing case includes a bounded 4 mm lateral-escape
surrogate; it is not a rigorous curved-surface or edge model.

## Physics firewall

For neutral groups, each material uses the full positive reversible Boltzmann
kernel

\[
 \mu_m\partial_x\psi^n_{gm}
 +\Sigma_{\ell,g}\psi^n_{gm}
 +\Sigma_{s,g}\left(\psi^n_{gm}-\sum_{m'}K^{(g)}_{mm'}\psi^n_{gm'}\right)
 =q^n_{gm}.
\]

The matrix \(K^{(g)}\) is nonnegative, row-stochastic, and
\(W\)-reversible.  It is identical for the baseline and optimized runs.  AFP
never replaces this operator.

Neutral reaction loss generates a separate nonnegative charged-secondary
source.  Only that charged component uses the BFP model

\[
 \mu_m\partial_x\psi^c_{km}
 +(\Sigma_{a,k}+\Sigma_{r,k})\psi^c_{km}
 -D_k(L\psi^c_k)_m=q^c_{km}.
\]

Here \(L\) is either the frozen moment-monotone baseline or the frozen
optimized positive generator.  Both share the same 32 nodes, weights, spatial
cells, energy groups, sources, coefficients, and stopping model.

The upwind cell system is an M-matrix for every positive production generator.
The observed minimum flux is `1.475e-11`; the largest balance residual is
`5.018e-15`.

## Responses

For every layer and incidence, the result records neutral and charged scalar
flux, current, traceless second moments, tape-normal quadrupoles, heating
proxies, interface crossing and escape, and species-resolved PKA source
descriptors with symmetric positive-semidefinite directional tensors.

The six comparison responses are REBCO charged heating, REBCO charged
\(q_n\), REBCO charged scalar flux, total heating, charged escape, and
substrate PKA-source total.  The substrate PKA response is constructed solely
from the neutral field, so its three incidence comparisons are identical by
design and cannot diagnose the AFP replacement.

The PKA outputs are source descriptors.  They are not recoil-energy spectra,
DPA, surviving-defect populations, or predictions of \(J_c\), \(T_c\), or
annealing.

## Reference and uncertainty

The nominal reference remains the 72-direction positive reversible heat-kernel
generator on the twice-refined layer mesh.  The recorded nominal resolution
quantity is

\[
 u_R=|R_{72,h/2}-R_{50,h/2}|+|R_{72,h/2}-R_{72,h}|.
\]

This quantity is retained for continuity with the preregistered-style
comparison, but it is not accepted as a converged error estimate by itself.
The revised audit also evaluates 50-, 72-, 98-, and 128-direction references.
For each response it computes

\[
 s_R=\frac{\max_k R_k-\min_k R_k}
 {\max_k |R_k|},
\]

with a declared convergence gate \(s_R\le0.05\).  The gate is a conservative
diagnostic, not a confidence interval or a convergence theorem.  Every
incidence fails the all-response gate.

At 84° incidence the reference sequence is plainly oscillatory:

| Directions | REBCO charged heating | Total heating | Charged escape |
|---:|---:|---:|---:|
| 50 | `5.2838e-12` | `1.0197e-7` | `1.5252e-8` |
| 72 | `1.1593e-7` | `3.7917e-3` | `5.6202e-4` |
| 98 | `1.2998e-9` | `4.0469e-5` | `6.0748e-6` |
| 128 | `1.3264e-7` | `3.6852e-3` | `5.4642e-4` |

The grazing relative spans are approximately one for every selected response.
The sequence therefore does not establish a converged reference.

Floating-point evidence is canonicalized to 12 significant decimal digits
after calculation and before hashing.  Values below `1e-18` are recorded as
zero.  The workflow pins one OpenBLAS thread and the portable `Haswell` kernel
target; same-run records must be byte-identical and cross-runner records must
agree within the declared numerical tolerance while independently passing the
audit.

## Quantitative result

| Incidence | Comparisons | Resolved improvements | Resolved degradations | Reference gate |
|---|---:|---:|---:|---|
| Normal | 6 | 0 | 0 | failed |
| 60° oblique | 6 | 0 | 0 | failed |
| 84° grazing-sensitive | 6 | 0 | 0 | failed |
| Total | 18 | 0 | 0 | failed overall |

The nominal REBCO charged-heating absolute errors remain:

| Incidence | Baseline error | Optimized error | Nominal uncertainty |
|---|---:|---:|---:|
| Normal | `4.9650e-10` | `4.9650e-10` | `5.6373e-8` |
| 60° | `2.0731e-8` | `2.0731e-8` | `3.2602e-7` |
| 84° | `3.0877e-8` | `3.0877e-8` | `1.1756e-7` |

The optimized generator has the smaller sampled \(H_2\) defect (`0.9325`
versus `1.3880`), but the selected response map is insensitive to that
operator difference at roughly machine precision.  This fixture therefore
cannot test whether improved degree-two fidelity transfers to HTS responses.

## Roadmap outputs and exclusions

Produced: frozen three-group neutral spectra, three-group charged-secondary
flux, layer heating proxies, layer-resolved moment fields, species-resolved PKA
source descriptors, and directional PKA tensors.

Not produced: evaluated neutron/photon cross sections, photon transport,
traceable H/He production, full recoil-energy spectra, DPA, defect survival,
annealing, atomistic damage, or superconducting-property changes.

## Decision

Retain the case as an implementation and claim-firewall diagnostic.  Do not
publish it as a bounded negative transfer result.  A scientifically useful
successor must use an operator-sensitive response, a demonstrably converged or
independently validated angular reference, and a preregistered decision rule
that distinguishes improvement, degradation, and unresolved outcomes.
