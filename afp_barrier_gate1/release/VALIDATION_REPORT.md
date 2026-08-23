# R5 internal validation report

Date: 2026-08-22 EDT

Status: `INTERNAL_GATES_CLOSED_WITH_RECORDED_PLATFORM_ROUNDOFF`

## Formal checks

- Fresh pinned `lake build`: `PASS`, 3,118 jobs.
- Focused `AFPBarrier.AccelerationFixedPoint` elaboration: `PASS`, 1,585 jobs.
- Exhaustive generated audit: 58 modules, 512 public theorem/lemma
  declarations, 512 `#check` results, and 512 `#print axioms` results.
- Observed axioms are restricted to `propext`, `Classical.choice`, and
  `Quot.sound`; no `sorryAx` or unexpected axiom occurred.
- Signature inspection confirms that Lean checks the finite algebraic core
  and named conditional lemmas, not the paper's analytic, global geometric,
  numerical, physical, novelty, or publication claims.

## Mathematical and computational checks

- Thirteen P1A--P1E exact, symbolic, Cauchy-guard, independent-route, family,
  and hostile-mutation audits: `PASS`/expected `ACCEPT`.
- P2A/P2C suites in the exact pinned cvxpy stack: 68 passed, with two solver
  accuracy warnings retained.
- Repository-owned Python suites with the platform-sensitive tetrahedron test
  deselected: 180 passed, one deselected, two retained cvxpy warnings.
- Frozen tetrahedron test on Windows NumPy 2.3.2: residual
  `2.7902947984069054e-15`, exceeding its strict `<2e-15` assertion.
  Independent WSL NumPy 2.2.4 computation: `4.440892098500626e-16`, assertion
  passes. Both runs certify exactness at the implemented `1e-10` tolerance;
  the frozen test was not weakened.
- P2F record integrity: `PASS`; scientific classification remains
  `INCONCLUSIVE_REFERENCE_NOT_CONVERGED`. Operator response is insensitive and
  the reference convergence gate fails, so no physical conclusion is issued.
- A pinned rerun preserved that terminal classification but not exact JSON:
  ten floating fields moved (maximum absolute change `4.056255e-16`) and two
  unresolved `charged_escape` direction/improvement booleans flipped. The
  selected/rerun scientific hashes are respectively `3b0d8f53...` and
  `3d80f8d0...`. This is additional evidence for excluding P2F, not a result to
  average or promote.

## Manuscript and release checks

- Corrected manuscript source/citation audit: 12 cited primary-source records,
  exact citation/BibTeX set equality, all controlling registry keys present,
  and zero Pandoc native-conversion warnings.
- Selected PDF: 23 US-letter pages, 337,798 bytes, no encryption, JavaScript,
  or forms; metadata title exact.
- Repeated build: exact 10,272-word extracted token stream and exact figure
  bytes; Tectonic container bytes differ and are not called byte-reproducible.
- Final render-and-inspect QA: all 23 pages inspected; no clipping, overlap,
  broken table, black square, unreadable glyph, or page-transition defect.
- Release structural validator: 512-declaration boundary, allowed axiom set,
  14-file P2F record chain, corrected robustness labels, P2F exclusion, PDF
  binding, and required release files checked fail-closed.

## Failed or corrected execution paths

1. Python 3.11 dependency resolution stopped before installation because
   SciPy 1.18 requires Python at least 3.12; the exact pins were retained and
   the already-installed Python 3.12.10 was used.
2. An unscoped repository-root pytest discovery entered the disposable
   dependency vendors' own test directories. A second attempt omitted the
   `math_repo_afp/src` package root. Both were harness errors; the final command
   explicitly names the three repository-owned test directories and source
   roots.
3. XeLaTeX was not locally installed. After a complete acquisition gate, the
   already-bundled Tectonic compiler fetched only its bounded resource cache to
   the R5 `D:` worktree and produced the selected PDF.
4. PDF container hashes differed across consecutive Tectonic builds despite
   identical semantic text, page count, and figure. The selected artifact is
   hash-bound and the limitation is explicit.

These checks are internal evidence only. They do not certify independent
human proof review, bibliography completeness, evaluated physical data,
experimental calibration, production transport performance, or journal
acceptance.
