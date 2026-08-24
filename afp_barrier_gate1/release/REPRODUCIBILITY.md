# R8 reproducibility instructions

The release branch is `codex/afp-major-revision-r8-20260824`, created from
exact clean R7 head `e5d023e50ead92f9d87c7e625860225b4e6aa89b`. Run the
acquisition gate before allowing any tool to download resources. The recorded
R8 execution used only existing local tools and caches and acquired zero
bytes.

## Lean

From `afp_barrier_gate1`:

```powershell
py -3.12 release\tools\generate_lean_release_audit.py
lake build
lake env lean AFPBarrier\ReleaseAxiomAudit.lean
py -3.12 release\tools\validate_release.py
```

The generated audit is fail-closed at 58 modules and 512 public declarations,
with `#check` and `#print axioms` for each. The checked-in
`LEAN_RELEASE_AUDIT.log` is inherited R7 evidence; R8 freshly reruns the same
command and records its independent counts and axiom set in the validation
report. This remains a finite algebraic proof surface, not an end-to-end
formalization of the paper.

## Exact certificate and mathematical audits

```powershell
$env:PYTHONPATH='D:\math_lean_1\Testing-afp-major-revision-r5-20260822\afp_barrier_gate1\release\tmp\cvxpy-site'
py -3.12 release\certificates\theorem_7_2\verify_certificate.py
py -3.12 release\tools\run_exact_audits.py
```

Certificate v3 uses only standard-library exact arithmetic in `Q` and
`Q(sqrt(58))`. It distinguishes `alpha_*` from polar `a_0`, the full
pairwise-separation constant from the packing radius, and the `z^2`
denominator guard from a bound on `z`. It rejects four hostile mutations. The
ordinary recurrence and telescoping identity are outside the verifier.

## Repository-owned Python suites and P2F

From `afp_barrier_gate1`, using the already-local R5 package target read-only:

```powershell
$env:PYTHONPATH="$PWD\release\tools\windows_compat;$PWD\math_repo_afp\src;D:\math_lean_1\Testing-afp-major-revision-r5-20260822\afp_barrier_gate1\release\tmp\cvxpy-site"
py -3.12 -m pytest -p no:cacheprovider -q pure_math\tests gate6\tests math_repo_afp\tests
py -3.12 -m pytest -p no:cacheprovider -q pure_math\tests gate6\tests math_repo_afp\tests --deselect math_repo_afp/tests/test_v02_global_graph.py::test_tetrahedron_attains_global_positive_degree_two_lower_bound
py -3.12 -m pure_math.p2f_hts.audit benchmarks\p2f\P2F_RESULTS.json --output tmp\P2F_AUDIT_R8.json
```

The full suite retains one frozen platform-sensitive assertion: residual
`2.7902947984069054e-15` against `<2e-15`. The source threshold is not
weakened. The scoped run produces `180 passed, 1 deselected, 2 warnings`.
The fresh P2F audit matches the canonical JSON semantically and remains
`INCONCLUSIVE_REFERENCE_NOT_CONVERGED`.

## Manuscript and PDF

From the repository root:

```powershell
$env:AFP_PDF_ENGINE='C:\Users\joshu\.codex\plugins\cache\openai-bundled\latex\0.2.6\bin\tectonic.exe'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\pdfs\tectonic-cache"
$env:SOURCE_DATE_EPOCH='1785900000'
py -3.12 docs\publication_program\p1f_manuscript\build_flagship_paper.py
pandoc docs\publication_program\p1f_manuscript\FLAGSHIP_MANUSCRIPT.md --from=markdown --standalone --citeproc --bibliography=docs\publication_program\p1f_manuscript\priority_sources.bib -t native -o tmp\pdfs\flagship-native-r8.txt
py -3.12 afp_barrier_gate1\release\tools\validate_flagship.py
```

The selected PDF is 26 US-letter pages. All pages are rendered with Poppler
and visually inspected; changed pages 14--16 receive full-resolution review.

## Final release gate

From `afp_barrier_gate1`:

```powershell
py -3.12 release\tools\normalize_release_text.py
py -3.12 release\tools\generate_release_manifest.py
py -3.12 release\tools\validate_release.py
git diff --check
```

These are internal reproducibility checks, not human peer review or
publication acceptance.
