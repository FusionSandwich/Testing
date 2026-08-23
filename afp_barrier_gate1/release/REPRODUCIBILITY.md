# R5 reproducibility instructions

All commands below are run from `afp_barrier_gate1` unless a repository-root
command is shown. The controlling Git base is
`f0ec4a8e539ebf72f5324f92439b56545ea8d2c5`; the release branch is
`codex/afp-major-revision-r5-20260822`. Run acquisition gates before allowing
Lean, Python, Tectonic, or any other tool to download resources.

## Lean

The checked-in `lean-toolchain` selects Lean 4.30.0 and `lake-manifest.json`
pins Mathlib at `c5ea00351a37a07d01de0dd0977e9ee921160b16`.

```powershell
lake build
lake build AFPBarrier.AccelerationFixedPoint
lake env lean AFPBarrier\ReleaseAxiomAudit.lean
py -3.12 release\tools\generate_lean_release_audit.py
py -3.12 release\tools\validate_release.py
```

`generate_lean_release_audit.py` is fail-closed at 58 modules and 512 public
theorem/lemma declarations. Its generated source applies both `#check` and
`#print axioms` to every indexed declaration. Regenerate the audit source and
index before elaborating them; do not infer whole-paper formalization from a
successful run.

## Exact and Python checks

The local validation used Python 3.12.10 with the workflow-pinned packages
installed into the disposable, uncommitted `release/tmp/cvxpy-site` target:

```text
clarabel 0.11.1; cvxpy 1.7.3; h5py 3.16.0; numpy 2.3.2;
osqp 1.0.4; pytest 8.4.2; scipy 1.18.0; scs 3.2.9; sympy 1.14.0
```

PowerShell setup and validation:

```powershell
$env:PYTHONPATH="$PWD\release\tmp\cvxpy-site;$PWD\release\tools\windows_compat;$PWD;$PWD\math_repo_afp\src"
$env:PYTHONHASHSEED='0'
$env:OPENBLAS_CORETYPE='Haswell'
py -3.12 release\tools\run_exact_audits.py
py -3.12 -m pytest -p no:cacheprovider -q pure_math\tests gate6\tests math_repo_afp\tests
py -3.12 pure_math\p2f_hts\runner.py
py -3.12 pure_math\p2f_hts\audit.py
py -3.12 release\tools\generate_p2f_records.py
py -3.12 release\tools\validate_release.py
```

The committed tests include one over-tight platform-sensitive assertion:
Windows NumPy 2.3.2 gives a tetrahedral harmonic residual
`2.7902947984069054e-15` against a strict `<2e-15` test threshold, while an
independent WSL NumPy 2.2.4 evaluation gives `4.440892098500626e-16`. Both are
far inside the certificate's declared `1e-10` exactness tolerance. R5 records
the platform difference and does not weaken the frozen test.

## Manuscript

The build script defaults to XeLaTeX. The selected local candidate was built
with already-bundled Tectonic 0.17.0, Pandoc 3.8.3, Python 3.12.10,
Matplotlib 3.11.1, and Poppler 26.05.0:

```powershell
Set-Location ..
$env:AFP_PDF_ENGINE='tectonic'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\pdfs\tectonic-cache"
py -3.12 docs\publication_program\p1f_manuscript\build_flagship_paper.py
pandoc docs\publication_program\p1f_manuscript\FLAGSHIP_MANUSCRIPT.md `
  --from=markdown --standalone --citeproc `
  --bibliography=docs\publication_program\p1f_manuscript\priority_sources.bib `
  -t native -o tmp\pdfs\flagship-native.txt
py -3.12 afp_barrier_gate1\release\tools\validate_flagship.py
```

Two consecutive builds produced the same dependency-graph bytes, 23 pages,
and the same 10,272-word extracted token stream. Tectonic's PDF container
bytes differed, so the selected PDF is bound by its recorded SHA-256 rather
than represented as a byte-reproducible rebuild. All 23 final pages were
rendered with Poppler and visually inspected for clipping, overlap, broken
tables, unreadable glyphs, headers, footers, and page transitions.

## Final manifests

```powershell
Set-Location afp_barrier_gate1
py -3.12 release\tools\normalize_release_text.py
py -3.12 release\tools\generate_release_manifest.py
py -3.12 release\tools\validate_release.py
git diff --check
```

`RELEASE_MANIFEST.sha256` and `RELEASE_MANIFEST.json` exclude themselves and
all `release/tmp` content. `P2F_RECORDS.sha256` has its own fixed 14-file
scope. External specialist review, physical-data validation, and publication
acceptance are intentionally outside these reproducibility commands.
