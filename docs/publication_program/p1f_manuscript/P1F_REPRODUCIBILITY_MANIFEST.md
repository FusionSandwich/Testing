# Flagship-paper R6 reproducibility manifest

## Mathematical and review lineage

R6 is a targeted major-revision candidate based on the internally verified R5
head `653d8945a5e91515f7a382ed42a8f4f51c0f0094` and scientific snapshot
`9783a69e8f079d61c100bc87ea653ec9c981c2fe`. The hostile external R5 review
reported no counterexample to the finite-dimensional frontier, equality, or
defect-budget theorems, but returned **MAJOR REVISION**. R6 does not claim to
clear that external decision.

The former Corollary 6.3 is now non-theorem discussion. Theorem 7.2 is stated
only for the discrete sequence `h_J`, `J>=1`, and is classified as a
computer-assisted exact-rational theorem rather than an end-to-end Lean
theorem. Its certificate and independent verifier are release artifacts.

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| R6 branch | `codex/afp-major-revision-r6-20260823` |
| P1E source commit | `4e461c10f069cd7eb4614e7d52b886637dff134b` |
| P1E source tree | `2474126498a50b0315d0a6e5ab703f0717c00a79` |
| R5 candidate tag | `afp-r5-internal-rc-20260822` |
| R5 hostile review disposition | `MAJOR REVISION` |
| R6 external acceptance | not claimed; renewed external review required |

## Publication inputs and outputs

| File | SHA-256 |
|---|---|
| `FLAGSHIP_MANUSCRIPT.md` | `e03f0c7275c004c3826a00f43c17d1254caf8c322f16df86b474b81b260bdb0f` |
| `priority_sources.bib` | `03778dd79c59bf24d26b1ea1224a5880612c7d9babced3994d602533cea83267` |
| `proof_dependency_graph.png` | `dd89357db56a4ee063331eae55ee5d0054a8c2c154669a2c85e4828d2d34dfbb` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `413a1c210668f3d84894f6118a0b65f376cc4a3fcf95935fb47f7718defa44b7` |
| `release/certificates/theorem_7_2/certificate.json` | `093acef16582ec6ca0039b4a7408fc265871bdc849eef383905bd92b591b86cd` |
| `release/certificates/theorem_7_2/verify_certificate.py` | `58f4b21f3b40f9a7df1e28c6c99c7218ccc801c3c91e8026e9824ca76c6f6290` |

The selected PDF has 25 US-letter pages, no form, encryption, or JavaScript,
and the expected title metadata. Extraction with the bundled PDF runtime gave
11,288 whitespace-delimited words. All 25 pages were rendered with Poppler
26.05 and visually inspected; the final build had no TeX box-overflow
warnings. PDF container bytes may vary across TeX/font environments, so the
selected artifact is bound by the digest above.

## R6 authoring environment

```text
Python 3.12.10
matplotlib 3.11.1
pandoc 3.8.3
Tectonic 0.17.0
Poppler 26.05.0
SOURCE_DATE_EPOCH=1785900000
```

The acquisition gate records the full machine preflight. R6 downloaded no
software and used only already-local tools, the copied R5 Lean build/config
state, a junction to an already-local Mathlib package tree, and an already-
local Tectonic cache.

## Build and verification commands

From the repository root:

```powershell
$env:AFP_PDF_ENGINE='tectonic'
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
R6 delta. The consolidated R6 validator binds the revised manuscript, exact
certificate, independent verifier, Lean declaration/axiom audit, exact audit
suite, P2F inconclusive records, and release manifests. A passing internal
gate is not external review or publication acceptance.
