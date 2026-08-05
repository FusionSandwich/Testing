# P2B harmonic-defect transport stage report

Status: **complete release record**.  Exact-head acceptance is recorded by
the publication workflow and immutable archive.

P2B starts literally from the accepted P2A archive and adds a rigorous
residual-to-dynamics and residual-to-response layer.  It does not revise the
accepted Paper-I or P2A results, and it does not use numerical agreement as a
substitute for any analytic estimate.

## 1. Frozen baseline and release refs

| Record | Exact value |
|---|---|
| accepted parent commit | `07138547ff5c85df071e2067587dd83ca20b71b5` |
| accepted parent tree | `7b17d48665bfc9f8a4490a26468ccf3633960897` |
| accepted parent archive | `archive/afp-publication-p2a-convex-design-verified` |
| candidate branch | `agent/afp-publication-p2b-harmonic-transport-07138547` |
| create-only target archive | `archive/afp-publication-p2b-harmonic-transport-verified` |

The release workflow checks the literal parent tree, no-merge ancestry,
remote branch head, exact changed-path allowlist, and create-only archive
semantics.  Workflow/run identifiers and hashes are retained in release
records, never in the mathematical argument.

## 2. Delivered mathematical result

For a positive reversible angular generator, P2B proves the exact Duhamel
and resolvent residual identities and their sharp contraction constants.  It
then extends them to kernel-correct sampled shells, guarded band synthesis,
physical symmetrizer norms, inhomogeneous and time-dependent angular
equations, noncommuting streaming--diffusion operators, steady resolvents,
preconditioned iterations, and block multigroup BFP systems.

The transport error is split algebraically into exactly six named channels:
physical BFP modeling, angular generator, angular quadrature/sampling,
spatial discretization, energy grouping/slowing down, and iteration.  Both a
full-operator variation-of-constants proof and an independent energy proof
state their stability, boundary, domain, and regularity assumptions.  Exact
and approximate adjoints give response representations with the
approximate-adjoint remainder retained explicitly.

## 3. Requirement closure matrix

| Requested deliverable | Controlling artifact | Acceptance evidence |
|---|---|---|
| one-mode semigroup and resolvent bounds | main P2B document, Theorems 2.1--2.2 | two-node defect and sharp alias fixtures |
| shell and band extension | main Theorems 3.1--3.2; `pure_math/dynamics/core.py` | full-output leakage and alias/conditioning guard tests |
| physical scattering norm | main Theorem 3.3; core module | symmetrizer dissipativity and fail-closed input tests |
| inhomogeneous/time-dependent equations | main Theorem 4.1 | analytic proof plus finite Duhamel Lean lemma |
| six error channels | main Theorem 6.1; `pure_math/dynamics/bounds.py` | exact ledger test and Lean telescoping theorem |
| two noncommuting routes | main Theorems 7.1--7.2 | nonzero exact commutator fixture and exact coercivity audit |
| steady and preconditioned estimates | main Theorems 8.1--8.2; bounds module | exact residual solve and contraction tests; Lean coercivity/iteration theorems |
| multigroup BFP extension | main Theorem 9.1 | exact two-group amplitude/commutator mutation test, six-channel block ledger, and retained multigroup formal source |
| adjoint response estimator | main Theorems 10.1--10.2 | exact response fixture and Lean transpose identities |
| `D_2` predictivity boundary | main Section 11 | alias, band, higher-output, and noncommutation falsification tests |
| pure-angular manufactured solution | main Section 12.1; `pure_math/dynamics/manufactured.py` | exact transient/resolvent errors and effectivities |
| spatial manufactured solution | main Section 12.2; manufactured and exact-audit modules | exact SymPy solve, coercivity, commutator, response and effectivity |
| formal finite core | `AFPBarrier/HarmonicDefectTransport.lean` | focused build and `P2BAxiomAudit.lean` dependency audit |
| theorem/source/test registry | `P2B_CLAIM_MAP.md` and global registries | exact claim-key/path audit |
| prior-art and hostile audit | `P2B_PRIOR_ART_AND_HOSTILE_AUDIT.md` | transfer ledger and rejected-overclaim sentinels |

## 4. Implementation contract

The package under `afp_barrier_gate1/pure_math/dynamics/` validates finite,
positive masses and the row-sum, detailed-balance, positivity, and weighted
dissipativity properties of the generator.  Shell residuals retain their
full sampled output.  Band synthesis rejects singular or numerically
ambiguous cross-shell sampling.  Residual ledgers require the exact six keys
and use the cancellation-safe sum of component norms by default.

The manufactured angular examples compare SciPy matrix exponentials and
linear solves with closed forms.  The spatial example is reconstructed
independently in exact SymPy arithmetic.  A candidate preconditioner is
accepted only after its contraction norm is computed and found below one;
otherwise the bound fails deterministically.

## 5. Formal boundary

Lean machine-checks the finite contractive sum inequality, transient-kernel
nonnegativity, resolvent identity and norm consequence under an explicit
left-inverse/contraction hypothesis, six-term telescope, finite transpose
and adjoint residual identities, Young/coercivity inequalities, and
geometric iteration estimate.  The file explicitly disclaims formalizing
matrix exponentials, Bochner integration, trace theory, and PDE
well-posedness.  Those analytic results are proved in the manuscript under
visible hypotheses.

## 6. Adversarial closure

| Attack | Resolution |
|---|---|
| sampled harmonic shell assumed invariant | a sharp constant-alias fixture attains the bound; full output is never compressed |
| cross-degree aliases ignored | the band theorem uses the joint synthesis map and its inverse-stability guard |
| angular self-adjointness transferred to streaming | both transport proofs use the full noncommuting operator; an exact fixture has nonzero commutator |
| boundary dissipation called automatic | inflow/periodic boundary and trace assumptions are displayed in the energy theorem |
| transport stability hidden in Duhamel language | evolution-family growth/coercivity hypotheses and constants are explicit |
| approximate adjoint treated as exact | the adjoint residual remainder is displayed and bounded |
| `D_2` advertised as universally predictive | the theorem requires a realized saturation/observability factor and an adjoint-weighted relative remainder criterion; higher-shell/source dominance and time/sign cancellation are explicit |
| iteration error omitted | the sixth ledger channel and preconditioned geometric bound are explicit |
| numerical fixture used as a theorem | exact fixtures validate formulas and effectivity only; all-data results have analytic proofs |
| AFP terminology used to overclaim transport scope | limitations preserve the full Boltzmann, spatial, energy, boundary, material, and solver errors |

## 7. Workflow acceptance gates

The P2B exact-head workflow has four independent gates:

- **scope and regressions:** exact baseline/ancestry/23-path allowlist,
  pinned numerical dependencies, complete P2B tests and audits, retained
  P2A/P1 regressions, claim keys, sentinels, and clean tree;
- **formal kernel:** full Lean build, focused P2B source and axiom audit,
  and rejection of proof holes or project-local axioms;
- **integrity:** candidate/tree/workflow/dependency/artifact hashes and
  source archive records;
- **freeze:** create-only absent-ref lease after all preceding gates pass on
  the exact candidate branch.

## 8. Exact source boundary

The workflow allowlist contains exactly 23 files: one workflow; six dynamics
modules and one test; four Lean/aggregate files; the five P2B documents; and
the six additive global registry files.  Any extra or missing path, non-UTF-8
or non-regular blob, merge commit, generated cache file, or dirty checkout
fails the release.

## 9. Limitations carried forward

P2B is a linear residual-to-error theorem under displayed stability and
regularity hypotheses.  It does not prove those hypotheses for every
geometry/material/boundary discretization, replace a full Boltzmann model,
make `D_2` source-independent, eliminate higher shells, or certify arbitrary
preconditioners.  Nonlinear feedback, adaptive meshes, uncertain material
data, and end-to-end reactor or shielding validation remain outside the
retained theorem.
