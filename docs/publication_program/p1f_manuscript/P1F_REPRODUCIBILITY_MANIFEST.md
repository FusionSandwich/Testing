# Flagship-paper R8 reproducibility manifest

## Mathematical and review lineage

R8 is a targeted repair based on exact clean R7 head
`e5d023e50ead92f9d87c7e625860225b4e6aa89b` and R7 scientific snapshot
`d77295e8de3da230626818698b20ffea6584be3b`. The independent Math-project
review of that exact head returned **MINOR REVISION**. This was an independent
internal AI adversarial review, not identifiable external human peer review.
R8 does not change theorem scope or claim acceptance.

Theorem 7.2 remains stated only for the discrete sequence `h_J`, `J>=1`, and
is classified as a computer-assisted exact-rational theorem rather than an
end-to-end Lean theorem. R8 reserves `a_0=4/3` for the polar latitude, uses
`alpha_m` for the transition envelope, distinguishes full pairwise separation
`1/(4M_0)` from packing radius `1/(8M_0)`, and narrows the certificate's
ordinary-row claim to finite rational recurrence budgets.

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| R8 branch | `codex/afp-major-revision-r8-20260824` |
| exact R8 base | `e5d023e50ead92f9d87c7e625860225b4e6aa89b` |
| R8 scientific-content commit | recorded in final packaging commit |
| R7 scientific-content commit | `d77295e8de3da230626818698b20ffea6584be3b` |
| P1E source commit | `4e461c10f069cd7eb4614e7d52b886637dff134b` |
| P1E source tree | `2474126498a50b0315d0a6e5ab703f0717c00a79` |
| latest independent internal AI review disposition | `MINOR REVISION` |
| human peer review or acceptance | not claimed; later independent review required |

## Publication inputs and outputs

| File | SHA-256 |
|---|---|
| `FLAGSHIP_MANUSCRIPT.md` | `b33b643423a76de15bd4f056a3767dab9c686398e9a3af80396cfaf645da6520` |
| `priority_sources.bib` | `03778dd79c59bf24d26b1ea1224a5880612c7d9babced3994d602533cea83267` |
| `proof_dependency_graph.png` | `dd89357db56a4ee063331eae55ee5d0054a8c2c154669a2c85e4828d2d34dfbb` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `dcd740a44b83263857f8f3663d1236398888d949f8ce6a3a9c76eded9340948f` |
| `release/certificates/theorem_7_2/certificate.json` | `ededef85140b4415e1c48249d77ea7fe42345bbb7a0d36d1f150ef3caee747a6` |
| `release/certificates/theorem_7_2/verify_certificate.py` | `22965257284a9e038843eebd34beb133742ab185d5268a2a04f4b097f8a8b250` |

The selected PDF has 26 US-letter pages, 352,550 bytes, no form, encryption,
or JavaScript, and the expected title metadata. Extraction with the bundled
PDF runtime gave 10,860 whitespace-delimited words. All 26 pages were rendered
with Poppler 26.05 and visually inspected; changed pages 14--16 were also
inspected at full resolution. The final build had no TeX box-overflow warning.
PDF container bytes may vary across TeX/font environments, so the selected
artifact is bound by the digest above.

## R8 authoring environment

```text
Python 3.12.10 (system); 3.12.13 (bundled PDF runtime)
pandoc 3.8.3
Tectonic 0.17.0
Poppler 26.05.0
SOURCE_DATE_EPOCH=1785900000
```

The acquisition gate records the full machine preflight. R8 downloaded no
software and used only already-local tools, R7 Lean build/config state, a
junction to the already-local pinned Mathlib tree, the read-only R5 numerical
package target, and the copied R7 Tectonic cache.

## Build and verification commands

From the repository root:

```powershell
$env:AFP_PDF_ENGINE='C:\Users\joshu\.codex\plugins\cache\openai-bundled\latex\0.2.6\bin\tectonic.exe'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\pdfs\tectonic-cache"
py -3.12 docs\publication_program\p1f_manuscript\build_flagship_paper.py
py -3.12 afp_barrier_gate1\release\certificates\theorem_7_2\verify_certificate.py
py -3.12 afp_barrier_gate1\release\tools\validate_flagship.py
```

The verifier uses only the Python standard library, rational arithmetic, and
an exact implementation of `Q(sqrt(58))`; it neither imports the construction
audits nor uses floating point. The ordinary recurrence and telescoping proof
remain outside it.

## Release-gate boundary

The historical P1F workflow remains provenance only and does not certify the
R8 delta. The consolidated R8 validator binds the revised manuscript,
certificate v3, independent verifier, Lean declaration/axiom audit, exact
audit suite, P2F inconclusive records, and release manifests. A passing
internal gate is not human peer review or publication acceptance.
