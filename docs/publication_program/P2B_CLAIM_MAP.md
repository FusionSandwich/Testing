# P2B theorem--proof--test--registry map

Status: **complete controlling map**.  Each retained P2B claim has exactly
one controlling proof file, one primary executable or kernel-checking file,
and one `THEOREM_REGISTRY.md` row.  Supplemental tests and value records are
not additional controlling mappings.  The formal layer certifies the stated
finite algebra; it does not claim a formalization of continuous semigroups
or transport PDE well-posedness.

## Controlling map

| Claim | Exact statement controlled here | Proof source | Test or certificate source | Registry entry |
|---|---|---|---|---|
| P2B-ANGULAR | For a reversible nonpositive angular generator, the exact Duhamel and resolvent identities give the stated one-mode bounds with sharp uniform contraction constants. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 2.1--2.2 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-ANGULAR` |
| P2B-SHELL | Kernel-quotiented, weighted-orthonormal sampled shells inherit operator-norm transient/resolvent bounds; band synthesis retains cross-shell aliases and an explicit inverse-stability factor. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 3.1--3.2 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-SHELL` |
| P2B-PHYSNORM | A declared physical symmetrizer gives contraction in its norm; norm transfer from the quadrature metric pays the explicit condition-number factor. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorem 3.3 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-PHYSNORM` |
| P2B-RESIDUAL | Inhomogeneous and time-dependent equations admit the displayed evolution-family bound, and the six physical/discretization/iteration channels telescope exactly before stability is applied. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 4.1 and 6.1 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-RESIDUAL` |
| P2B-NONCOMMUTE | Streaming and angular diffusion are treated by full-operator variation of constants and by an independent energy estimate, without a commuting-semigroup factorization. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 7.1--7.2 and Proposition 7.3 | `pure_math/dynamics/exact_audit.py` | `THEOREM_REGISTRY.md`, `P2B-NONCOMMUTE` |
| P2B-STEADY | Coercive steady operators satisfy exact comparator resolvent identities, residual bounds, and explicit preconditioned contraction/iteration estimates. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 8.1--8.2 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-STEADY` |
| P2B-MULTIGROUP | The displayed block certificate gives coercivity; generic transient bounds additionally require the Sections 4--5 generation hypothesis and the steady bound requires surjectivity.  The triangular inverse has its separate invertible positive-diagonal-coercivity hypothesis. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorem 9.1 | `pure_math/dynamics/exact_audit.py` | `THEOREM_REGISTRY.md`, `P2B-MULTIGROUP` |
| P2B-ADJOINT | Exact and approximate steady/transient adjoints yield the displayed response identities; the approximate-adjoint remainder is retained and bounded. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Theorems 10.1--10.2 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-ADJOINT` |
| P2B-PREDICT | `D_2` is an upper-budget factor; two-sided or response prediction additionally requires realized shell saturation/observability and the explicit adjoint-weighted relative remainder criterion. Higher shells, aliases, streaming-generated components, and time/sign cancellation can dominate. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Section 11 | `pure_math/tests/test_p2b_dynamics.py` | `THEOREM_REGISTRY.md`, `P2B-PREDICT` |
| P2B-MANUFACTURED | Pure-angular and noncommuting spatial fixtures have independently reconstructed exact errors, bounds, responses, coercivity constants, and effectivity indices. | `P2B_HARMONIC_TRANSPORT_INTERPRETATION.md`, Section 12 | `pure_math/dynamics/exact_audit.py` | `THEOREM_REGISTRY.md`, `P2B-MANUFACTURED` |
| P2B-FORMAL | The finite Duhamel-sum inequality, resolvent algebra, six-term telescoping, transpose/adjoint identities, Young/coercivity inequalities, and geometric iteration bound are machine checked without project-local axioms or proof holes. | `AFPBarrier/HarmonicDefectTransport.lean` | `AFPBarrier/P2BAxiomAudit.lean` | `THEOREM_REGISTRY.md`, `P2B-FORMAL` |

Paths beginning `pure_math/` or `AFPBarrier/` are relative to
`afp_barrier_gate1/`; document names are under
`docs/publication_program/`.  The workflow executes the complete P2B test
module, so individual test names remain locators rather than partial test
selection.

## Hypothesis-transfer ledger

| External result or framework | Hypotheses transferred | P2B use and boundary |
|---|---|---|
| finite-dimensional self-adjoint semigroup/resolvent contraction | positive quadrature metric; reversible generator; nonpositive spectrum; `t>=0`, `alpha>0` | Gives norm-one angular contraction and resolvent norm `1/alpha`; no streaming conclusion is inferred from angular self-adjointness. |
| evolution-family variation of constants | common declared state space/domain; measurable generator family; well-posed evolution family with the stated growth bound | Gives the explicit inhomogeneous integral identity and bound only under those assumptions. |
| transport Green/energy identity | inflow or periodic boundary condition; trace regularity; nonnegative outflow term; collision coercivity | Supports the independent energy route; the boundary term and coercivity constant remain visible. |
| steady Lax--Milgram/accretive inverse estimate | onto plus the displayed coercivity/accretivity and domain compatibility, or an explicitly cited surjective coercive-form theorem | Gives the stated inverse norm; no unconditional transport stability theorem is imported. |
| adjoint residual representation | primal and adjoint domain/boundary compatibility; exact or explicitly residualized adjoint solve | Gives exact response identities and the retained approximate-adjoint remainder. |
| Morel/Pomraning/Bienvenue transport and AFP literature | only the conventions and application statements separately audited in the prior-art ledger | Application context and comparison only; none of the audited sources is used as a proof source for the combined P2B hierarchy, and every transferred hypothesis is listed. |

## Deliberately excluded claims

- The Lean source does not formalize matrix exponentials, Bochner integrals,
  trace theory, or PDE well-posedness.
- Angular reversibility is not claimed for the full streaming operator.
- Streaming and angular diffusion are never factorized unless a commutator
  hypothesis is separately proved.
- `D_2` alone is not advertised as a source-independent transport-error
  predictor.
- Numerical effectivity values are exact fixture deliverables, not evidence
  for an unproved all-data theorem.
- P2B does not claim that an angular Fokker--Planck model replaces the full
  Boltzmann, spatial, energy-loss, boundary, material, or iteration errors.

## Reproducibility boundary

Commit and workflow identifiers, dependency inventories, changed-path
allowlists, artifact hashes, and the create-only archive operation belong to
the release record.  They are not premises of any displayed mathematical
result.
