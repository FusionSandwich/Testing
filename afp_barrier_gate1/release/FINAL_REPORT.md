# AFP R5 final report

## Release identity

- Repository: `D:\math_lean_1\Testing-afp-major-revision-r5-20260822`
- Remote: `https://github.com/FusionSandwich/Testing.git`
- Selected base: `f0ec4a8e539ebf72f5324f92439b56545ea8d2c5`
- Branch: `codex/afp-major-revision-r5-20260822`
- Selected scientific-content commit: `9783a69e8f079d61c100bc87ea653ec9c981c2fe`
- Terminal classification:
  `AFP_PURE_THEOREM_INTERNAL_RELEASE_CANDIDATE_MAJOR_REVISION_CLOSED`

The report-containing commit necessarily cannot contain its own SHA. The
selected scientific-content commit is inserted after that milestone is
created; the exact pushed branch head and annotated candidate-tag target are
external Git metadata reported at handoff.

## Completed release work

1. Reconciled P1A--P1F, P2A--P2F, audit, repair, prompt-pack, and archive
   lineages by exact SHA and ancestry. Divergent repair/development branches
   remain explicit and unmerged.
2. Rechecked the sharp product frontier `D_2 r_max >= d(d-1)`, sampling
   quotient, equality chain, weighted stability budget, exact extremal
   families, and the justified `d=2,3` matching constructions through the
   accepted ordinary proofs plus 13 independent exact/symbolic/hostile audits.
3. Removed the old unrestricted robustness theorem. Proposition 7.3 is now an
   open problem; the false fixed-`eps` `O(h^2)` route is retained and labeled
   `FALSIFIED`, with its `O(eps)` obstruction.
4. Narrowed whole-paper Lean claims to the finite algebraic core. The release
   indexes and audits all 512 public theorem/lemma declarations across 58
   modules with signature and axiom output.
5. Split the architecture into a pure theorem release and a numerical/design
   draft. P2E remains mixed/negative; P2F is outside both and archived as
   inconclusive with an exact redesign specification.
6. Rewrote novelty boundaries against 12 identified primary sources without
   claiming literature-priority completeness.
7. Rebuilt the corrected 23-page manuscript, fixed its dense table layout,
   checked citations and Pandoc conversion, and visually inspected every final
   page.
8. Added fail-closed release generators, validators, theorem/claim/evidence
   maps, counterexample ledger, reviewer bundle, reproducibility instructions,
   logs, and exact manifests.

## Validation summary

- Lean: 3,118-job build `PASS`; focused 1,585-job build `PASS`; 512 signatures
  and 512 axiom reports `PASS`; only `propext`, `Classical.choice`, and
  `Quot.sound`; no `sorryAx`.
- Exact mathematical audits: 13 `PASS`/expected hostile `ACCEPT`.
- Python: 180 repository-owned tests passed with the single frozen
  platform-sensitive threshold deselected; P2A/P2C's 68 tests pass in the exact
  pinned cvxpy stack.
- Platform residual: Windows `2.7902947984069054e-15` versus strict `<2e-15`;
  independent WSL `4.440892098500626e-16`. Both satisfy the certificate's
  `1e-10` exactness tolerance; source and threshold are unchanged.
- P2F: integrity `PASS`, science
  `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`; a pinned rerun preserves the class
  but changes ten float fields and flips two unresolved derived booleans.
- Manuscript: 12 citation records exactly matched, zero Pandoc warnings,
  23 pages, exact semantic token-stream repeat, exact figure repeat, final
  render inspection `PASS`. Tectonic PDF container bytes are hash-bound rather
  than claimed byte-reproducible.

## Principal artifacts and selected SHA-256 values

| Artifact | SHA-256 |
|---|---|
| `docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md` | `ea8e3a252155fbd8a199ba83249aac9e763c8c116b19612a5df69525c8facb52` |
| `docs/publication_program/p1f_manuscript/proof_dependency_graph.png` | `dd89357db56a4ee063331eae55ee5d0054a8c2c154669a2c85e4828d2d34dfbb` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `87b8a77af8c53e2bfa2b24fcc1cf95fef8c798181b7f0828e61d25eaa7267c8d` |
| selected `P2F_RESULTS.json` scientific payload | `3b0d8f53350d61e95d993c0eece613664c0fda367916d01116fef9d435e9884b` |

`RELEASE_MANIFEST.sha256` and `RELEASE_MANIFEST.json` bind the complete release
surface while excluding only themselves and disposable `release/tmp` content.
`P2F_RECORDS.sha256` binds its fixed 14-file record chain.

## Commands and concise outcomes

```text
lake build                                      PASS (3118 jobs)
lake build AFPBarrier.AccelerationFixedPoint    PASS (1585 jobs)
lake env lean AFPBarrier/ReleaseAxiomAudit.lean PASS (512/512 signatures/axioms)
release/tools/run_exact_audits.py                PASS (13 audits)
pytest repository-owned suites                  180 pass, 1 platform test deselected
P2F rerun + audit                               PASS integrity; INCONCLUSIVE science
Pandoc native conversion                        PASS; 0 warnings
Tectonic manuscript build + Poppler render      PASS; 23 pages visually inspected
release/tools/validate_release.py                PASS
git diff --check                                PASS
```

## Failed approaches and preserved negative evidence

- Python 3.11 could not resolve pinned SciPy 1.18; no pin was weakened and the
  existing Python 3.12.10 was used in an isolated target.
- Broad pytest discovery entered vendor test trees; the final harness names
  only repository-owned suites and correct source roots.
- Tectonic did not reproduce identical container bytes; exact semantic text,
  figure, selected hash, and the limitation are recorded.
- The P1E stratified-lattice fixed-`eps` robustness route is false at its
  stated scope and remains in the counterexample ledger.
- The divergent fixed-level repair is `CANDIDATE_NOT_INTEGRATED`, not silently
  promoted from a branch name or finite script.
- P2E physical differences remain unresolved; P2F is operator-insensitive,
  reference-unconverged, and roundoff-sensitive.

## Unresolved gates

### Mathematical

- Independent specialist rederivation of the sharp trace/equality chain and
  `d=3` all-level adaptive-ring construction.
- Support-preserving perturbation robustness remains `OPEN`; no radius or
  constants are claimed. A matching positive local family for `d>3` is open.

### Formal

- The analytic Cauchy guard, global geometric classification, construction
  existence arguments, novelty, and manuscript prose are not wholly
  formalized. External proof-to-signature review remains required.

### Computational

- Rebuild in an independently provisioned pinned environment and resolve or
  explicitly platform-parameterize the over-tight `2e-15` regression without
  changing mathematical tolerances opportunistically.
- P2F requires a new preregistered operator-sensitive, converged benchmark;
  the present record cannot be repaired by selecting a roundoff sign.

### Physical/source

- No evaluated transport data, manufacturer geometry, irradiation calibration,
  device model, or production transport result was validated. P2E/P2F support
  no HTS performance conclusion.

### Human review

- No independent specialist, formal-methods reviewer, transport expert, or
  literature-priority reviewer has signed off. This release does not certify
  human acceptance.

### Publication

- Author/affiliation/ORCID, funding/conflicts, data license, repository DOI,
  journal formatting, submission, and acceptance remain open administrative
  gates.

## Single best next task

Commission an independent specialist audit using `REVIEWER_BUNDLE.md`, starting
with a clean rederivation of the quotient trace constant, equality sufficiency,
and the unperturbed `d=3` all-level construction, and archive a signed report
that cites exact theorem statements and release commit/tag SHAs.
