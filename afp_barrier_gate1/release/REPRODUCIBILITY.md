# R6 reproducibility instructions

The release branch is `codex/afp-major-revision-r6-20260823`, created from the
exact R5 head `653d8945a5e91515f7a382ed42a8f4f51c0f0094`. Run the acquisition gate
before allowing any tool to download resources. The recorded R6 execution
used only existing local tools and caches and acquired zero bytes.

## Lean

From `afp_barrier_gate1`:

```powershell
lake build
py -3.12 release\tools\generate_lean_release_audit.py
lake env lean AFPBarrier\ReleaseAxiomAudit.lean
py -3.12 release\tools\validate_release.py
```

The generated audit is fail-closed at 58 modules and 512 public theorem or
lemma declarations, with both `#check` and `#print axioms` for each. This is a
finite algebraic proof surface, not an end-to-end formalization of the paper.

## Exact certificate and mathematical audits

```powershell
py -3.12 release\certificates\theorem_7_2\verify_certificate.py
py -3.12 release\tools\run_exact_audits.py
```

The Theorem 7.2 verifier uses only the Python standard library, exact rational
arithmetic, and exact arithmetic in `Q(sqrt(58))`. It imports neither the
construction programs nor the derivation audits and performs no floating-
point operations. The aggregate runner executes 14 checks, including that
standalone verifier.

## Repository-owned Python suites and P2F

The checked R5 disposable package target is reused read-only through
`PYTHONPATH`; no package installation is required. The full suite retains one
known over-tight platform-sensitive assertion. On this Windows stack the
tetrahedral residual is `2.7902947984069054e-15` against `<2e-15`; the source
threshold is not weakened.

```powershell
py -3.12 -m pytest -p no:cacheprovider -q pure_math\tests gate6\tests math_repo_afp\tests
py -3.12 -m pytest -p no:cacheprovider -q pure_math\tests gate6\tests math_repo_afp\tests --deselect pure_math/tests/test_p2a_convex_design.py::test_exact_tetrahedron_certificate
py -3.12 pure_math\p2f_hts\audit.py
```

Expected outcomes are one platform failure in the full command, then 180
passes and one deselection. P2F remains
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`; integrity passing cannot promote it.

## Manuscript and PDF

From the repository root, with already-local Pandoc, Tectonic, and cache:

```powershell
$env:AFP_PDF_ENGINE='tectonic'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\tectonic-cache"
py -3.12 docs\publication_program\p1f_manuscript\build_flagship_paper.py
pandoc docs\publication_program\p1f_manuscript\FLAGSHIP_MANUSCRIPT.md --from=markdown --standalone --citeproc --bibliography=docs\publication_program\p1f_manuscript\priority_sources.bib -t native -o tmp\pdfs\flagship-native.txt
py -3.12 afp_barrier_gate1\release\tools\validate_flagship.py
```

The selected PDF is 25 US-letter pages. All pages were rendered with Poppler
and visually inspected. The final Tectonic build emitted no box-overflow
warnings. Container bytes are hash-bound, not claimed portable across font and
TeX environments.

## Final release gate

```powershell
py -3.12 release\tools\normalize_release_text.py
py -3.12 release\tools\generate_release_manifest.py
py -3.12 release\tools\validate_release.py
git diff --check
```

These are internal reproducibility checks. They are not renewed external
review or publication acceptance.
