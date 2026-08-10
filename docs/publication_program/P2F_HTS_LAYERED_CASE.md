# P2F bounded HTS layered response case

## Purpose and terminal outcome

This case tests whether the accepted degree-two harmonic-fidelity improvement
changes irradiation-relevant responses in a separately resolved coated
conductor.  It is a finite deterministic verification problem, not an
evaluated nuclear-data calculation.

The integrity audit passes.  The scientific outcome is `BOUNDED_NEGATIVE`:
none of the 18 response comparisons shows an optimized-operator improvement
larger than the conservative angular-plus-spatial reference uncertainty.

## Stack

| Layer | Material | Thickness |
|---|---|---:|
| Front stabilizer | Cu | 20.0 µm |
| Cap | Ag | 2.0 µm |
| Superconductor | REBCO | 1.0 µm |
| Buffer | oxide surrogate | 0.2 µm |
| Substrate | Hastelloy C-276 surrogate | 50.0 µm |
| Back stabilizer | Cu | 20.0 µm |

Total thickness is 93.2 µm.  The values lie inside representative ranges used
by the HTS irradiation roadmap; they do not certify a particular commercial
tape.

The three frozen incidence cases are 0° normal, 60° oblique, and 84°
grazing-sensitive incidence.  The grazing case includes a bounded 4 mm lateral
escape surrogate; it is not represented as a rigorous curved-surface or edge
model.

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

Here \(L\) is either the frozen moment-monotone baseline or the frozen optimized
positive generator.  Both share the same 32 nodes, weights, spatial cells,
energy groups, sources, coefficients, and stopping model.

The upwind cell system is an M-matrix for every positive production generator.
Observed minimum flux is `1.475e-11`; the largest balance residual is
`5.018e-15`.

## Responses

For every layer and incidence, the result records:

- neutral and charged scalar-flux integrals;
- neutral and charged current vectors;
- traceless second angular-moment tensors;
- tape-normal quadrupoles;
- neutral and charged heating proxies;
- charged-secondary interface crossing and groupwise escape;
- species-resolved reaction/PKA source totals and three-group spectra;
- symmetric positive-semidefinite directional PKA source tensors.

The six comparison responses are REBCO charged heating, REBCO charged
\(q_n\), REBCO charged scalar flux, total heating, charged escape, and substrate
PKA-source total.

The PKA outputs are source descriptors.  They are not recoil-energy spectra,
DPA, surviving-defect populations, or predictions of \(J_c\), \(T_c\), or
annealing.

## Reference and uncertainty

The independent charged reference is a 72-direction positive reversible
heat-kernel generator whose rate is calibrated to the coordinate shell.  A
50-direction solve measures angular reference change.  A two-times-refined
layer mesh measures spatial change.  The declared response uncertainty is the
conservative sum

\[
 u_R=|R_{72,h/2}-R_{50,h/2}|+|R_{72,h/2}-R_{72,h}|.
\]

A method difference is resolved only if the absolute difference between its
response error and the baseline response error exceeds \(u_R\).  This is a
conservative resolution test, not a statistical confidence interval.

Floating-point evidence is canonicalized to 12 significant decimal digits
after calculation and before hashing.  This is much tighter than every
declared reference-uncertainty gate and prevents insignificant NumPy/BLAS
serialization drift from changing the committed record.  Values with absolute
magnitude below `1e-18` are recorded as zero; this threshold is at least seven
orders below the smallest physical flux in the audit and removes only
symmetry-zero roundoff.

The reproducibility workflow pins one OpenBLAS thread and the portable
`Haswell` kernel target.  This prevents CPU-dispatch choices on different
GitHub runners from changing cancellation-sensitive comparison records.

## Quantitative result

| Incidence | Response comparisons | Resolved optimized improvements |
|---|---:|---:|
| Normal | 6 | 0 |
| 60° oblique | 6 | 0 |
| 84° grazing-sensitive | 6 | 0 |
| Total | 18 | 0 |

For example, the REBCO charged-heating absolute errors for the baseline and
optimized generators are respectively:

| Incidence | Baseline error | Optimized error | Reference uncertainty |
|---|---:|---:|---:|
| Normal | `4.9650e-10` | `4.9650e-10` | `5.6373e-8` |
| 60° | `2.0731e-8` | `2.0731e-8` | `3.2602e-7` |
| 84° | `3.0877e-8` | `3.0877e-8` | `1.1756e-7` |

The optimized generator has the smaller sampled \(H_2\) defect
(`0.9325` versus `1.3880`), but that ordering does not yield a resolved response
benefit here.  Most responses are controlled by neutral transport, spatial
resolution, escape, or angular information beyond a single \(H_2\) metric.

## Roadmap outputs

Produced: frozen three-group neutral spectra, three-group charged-secondary
flux, layer heating proxy, layer-resolved moment fields, species-resolved PKA
source descriptors, and directional PKA tensors.

Not produced: evaluated neutron/photon cross sections, photon transport,
traceable H/He production, full recoil-energy spectra, DPA, defect survival,
annealing, atomistic damage, or superconducting-property changes.

## Decision

The case is useful as a bounded negative result and as an implementation
firewall.  It prevents the method from being sold as a replacement for full
collision physics and shows that improved degree-two angular fidelity alone is
not sufficient to establish an HTS irradiation-response benefit.
