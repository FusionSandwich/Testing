# Flagship-paper R7 reproducibility manifest

## Mathematical and review lineage

R7 is a targeted repair based on the exact R6 head
`da137c157dbc92774cbf7e378efb5bf360be6ceb` and R6 scientific snapshot
`648691e9225359d0983d71fa332408fc7bdbadd9`. The renewed ChatGPT Pro task
`Review Math Revision Branch` returned **MAJOR REVISION**. This was an internal
AI adversarial review, not identifiable external human peer review. R7 does
not relabel R6 as passed or claim human review.

The former Corollary 6.3 is now non-theorem discussion. Theorem 7.2 is stated
only for the discrete sequence `h_J`, `J>=1`, and is classified as a
computer-assisted exact-rational theorem rather than an end-to-end Lean
theorem. Its certificate and independent verifier are release artifacts.

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| R7 branch | `codex/afp-major-revision-r7-20260824` |
| exact R7 base | `da137c157dbc92774cbf7e378efb5bf360be6ceb` |
| R7 scientific-content commit | `d77295e8de3da230626818698b20ffea6584be3b` |
| R6 scientific-content commit | `648691e9225359d0983d71fa332408fc7bdbadd9` |
| P1E source commit | `4e461c10f069cd7eb4614e7d52b886637dff134b` |
| P1E source tree | `2474126498a50b0315d0a6e5ab703f0717c00a79` |
| R5 candidate tag | `afp-r5-internal-rc-20260822` |
| renewed internal AI review disposition | `MAJOR REVISION` |
| human peer review or acceptance | not claimed; later independent review required |

## Publication inputs and outputs

| File | SHA-256 |
|---|---|
| `FLAGSHIP_MANUSCRIPT.md` | `6bc2423c8e043de990ec1123cf099649e0b86faa67cbffa863f6d15c182a9446` |
| `priority_sources.bib` | `03778dd79c59bf24d26b1ea1224a5880612c7d9babced3994d602533cea83267` |
| `proof_dependency_graph.png` | `dd89357db56a4ee063331eae55ee5d0054a8c2c154669a2c85e4828d2d34dfbb` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `c65756010a9b1c778db693389aaa2e8e96379be501f2f30fcf9326679302050f` |
| `release/certificates/theorem_7_2/certificate.json` | `ff8f1b13a64d8a4f0ca281853d689f5aaf86f22db74cb0c3e4f0c9fe118484cc` |
| `release/certificates/theorem_7_2/verify_certificate.py` | `82312039833840a11bbf83dc662e471f2e7ac7e83c112d32974a8d97cc55427a` |

The selected PDF has 26 US-letter pages, no form, encryption, or JavaScript,
and the expected title metadata. Extraction with the bundled PDF runtime gave
10,834 whitespace-delimited words. All 26 pages were rendered with Poppler
26.05 and visually inspected; the final build had no TeX box-overflow
warnings. PDF container bytes may vary across TeX/font environments, so the
selected artifact is bound by the digest above.

## R7 authoring environment

```text
Python 3.12.10 (system); 3.12.13 (bundled PDF runtime)
matplotlib 3.11.1
pandoc 3.8.3
Tectonic 0.17.0
Poppler 26.05.0
SOURCE_DATE_EPOCH=1785900000
```

The acquisition gate records the full machine preflight. R7 downloaded no
software and used only already-local tools, the copied R6 Lean build/config
state, a junction to an already-local Mathlib package tree, and an already-
local Tectonic cache.

## Build and verification commands

From the repository root:

```powershell
$env:AFP_PDF_ENGINE='C:\Users\joshu\.codex\dependencies\workspace-tools\tectonic\tectonic.exe'
$env:TECTONIC_CACHE_DIR="$PWD\tmp\tectonic-cache"
python docs\publication_program\p1f_manuscript\build_flagship_paper.py
python afp_barrier_gate1\release\certificates\theorem_7_2\verify_certificate.py
python afp_barrier_gate1\release\tools\validate_flagship.py
```

The verifier uses only the Python standard library, rational arithmetic, and
an exact implementation of `Q(sqrt(58))`; it neither imports the construction
audits nor uses floating point. The trusted computing base and residual
analytic boundary are stated in the certificate README and manuscript.

## Release-gate boundary

The historical P1F workflow remains provenance only and does not certify the
R7 delta. The consolidated R7 validator binds the revised manuscript, exact
certificate, independent verifier, Lean declaration/axiom audit, exact audit
suite, P2F inconclusive records, and release manifests. A passing internal
gate is not human peer review or publication acceptance.
