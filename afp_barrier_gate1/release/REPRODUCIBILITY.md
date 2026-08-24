# R7 reproducibility instructions

The release branch is `codex/afp-major-revision-r7-20260824`, created from the
exact R6 head `da137c157dbc92774cbf7e378efb5bf360be6ceb` (R6 scientific
snapshot `648691e9225359d0983d71fa332408fc7bdbadd9`). Run the acquisition gate
before allowing any tool to download resources. The recorded R7 execution used
only existing local tools and caches and acquired zero bytes.

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

The version-2 Theorem 7.2 verifier uses only the Python standard library,
exact rational arithmetic, and exact arithmetic in `Q(sqrt(58))`. It imports
neither the construction programs nor the derivation audits and performs no
floating-point operations. It checks arbitrary theorem-scale schedule sums,
representative levels through `J=257`, the signed product bound, positivity,
geometry, normalization, and published constants. Three hostile mutations must
be rejected. The aggregate runner executes 14 checks, including the verifier.

## Repository-owned Python suites and P2F

The checked R5 disposable package target is reused read-only through
`PYTHONPATH`; no package installation is required. From the repository root:

```powershell
$env:PYTHONPATH="$PWD\afp_barrier_gate1\release\tools\windows_compat;$PWD\afp_barrier_gate1\math_repo_afp\src;D:\math_lean_1\Testing-afp-major-revision-r5-20260822\afp_barrier_gate1\release\tmp\cvxpy-site"
py -3.12 -m pytest -p no:cacheprovider -q afp_barrier_gate1\pure_math\tests afp_barrier_gate1\gate6\tests afp_barrier_gate1\math_repo_afp\tests
py -3.12 -m pytest -p no:cacheprovider -q afp_barrier_gate1\pure_math\tests afp_barrier_gate1\gate6\tests afp_barrier_gate1\math_repo_afp\tests --deselect afp_barrier_gate1/math_repo_afp/tests/test_v02_global_graph.py::test_tetrahedron_attains_global_positive_degree_two_lower_bound
py -3.12 -m pure_math.p2f_hts.audit afp_barrier_gate1\benchmarks\p2f\P2F_RESULTS.json --output afp_barrier_gate1\tmp\P2F_AUDIT_R7.json
```

The full suite retains one known over-tight platform-sensitive assertion. On
this Windows stack the tetrahedral residual is
`2.7902947984069054e-15` against `<2e-15`; the source threshold is not
weakened. Expected outcomes are one platform failure in the full command, then
`180 passed, 1 deselected, 2 warnings`. P2F remains
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`; integrity passing cannot promote it.

## Manuscript and PDF

From the repository root, using the already-local bundled Pandoc, Tectonic,
Poppler, and Tectonic cache:

```powershell
$env:AFP_PDF_ENGINE='C:\Users\joshu\.codex\dependencies\workspace-tools\tectonic\tectonic.exe'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\pdfs\tectonic-cache"
py -3.12 docs\publication_program\p1f_manuscript\build_flagship_paper.py
pandoc docs\publication_program\p1f_manuscript\FLAGSHIP_MANUSCRIPT.md --from=markdown --standalone --citeproc --bibliography=docs\publication_program\p1f_manuscript\priority_sources.bib -t native -o tmp\pdfs\flagship-native.txt
py -3.12 afp_barrier_gate1\release\tools\validate_flagship.py
```

The selected PDF is 26 US-letter pages. All pages were rendered with Poppler
and visually inspected; changed load-bearing pages were also inspected at full
resolution. The final Tectonic build emitted no box-overflow warnings.
Container bytes are hash-bound, not claimed portable across font and TeX
environments.

## Final release gate

From `afp_barrier_gate1`:

```powershell
py -3.12 release\tools\normalize_release_text.py
py -3.12 release\tools\generate_release_manifest.py
py -3.12 release\tools\validate_release.py
git diff --check
```

These are internal reproducibility checks. They are not independent hostile
review or publication acceptance.
