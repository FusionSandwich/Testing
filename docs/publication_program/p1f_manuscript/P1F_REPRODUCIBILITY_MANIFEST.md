# Flagship-paper reproducibility manifest

## Immutable mathematical base

The original paper release was a one-commit publication layer over the
accepted fixed-family P1E construction archive. This audit-driven revision
retains that archive as historical provenance and adds an ordinary fixed-level
robustness proof. The historical P1E archive alone does not certify the new
level-dependent theorem; the controlling sources and repair workflow are the
files on the present repair branch.

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| P1E commit | `4e461c10f069cd7eb4614e7d52b886637dff134b` |
| P1E tree | `2474126498a50b0315d0a6e5ab703f0717c00a79` |
| P1E archive | `archive/afp-publication-p1e-asymptotic-family-verified` |
| P1E acceptance workflow | `30993983733` |
| exact-regressions job | `92266515071` — success |
| pinned Lean job | `92266514964` — success |
| final-integrity job | `92267535848` — success |

Workflow and job identifiers are release metadata only; they do not appear in
the mathematical argument.  The P1F commit and workflow identifier are
necessarily external metadata because a commit cannot contain its own hash or
the identifier of a run triggered by that commit.

## Publication inputs and outputs

The checked-in PDF was built from the checked-in Markdown, BibTeX, Lua filter,
LaTeX header, and dependency-graph generator.  Its principal content hashes
are:

| File | SHA-256 |
|---|---|
| `FLAGSHIP_MANUSCRIPT.md` | `0a1083976c3e3d77adf742be62b5cbe72652261f8b01e8e2341f7a541eb351c6` |
| `priority_sources.bib` | `8a896552a8a03154ba834466bdd80a6af65c39e5f440f53e2afbbc462746ae48` |
| `proof_dependency_graph.png` | `0b885c822230bd3e965863b4d9b618e5bcd84cc4e046ac9add46c4ee4a5f8a9e` |
| `build_flagship_paper.py` | `95e205d4b1cf0e5da982ae2699fae4870c74ce8ac1f1864a5c93e9785e7bfc6c` |
| `paper_header.tex` | `c3d151618c134114b35ce30eb672d9e127bf3c5dad244b83b970ea38d252cd20` |
| `P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md` | `6c47cbc2e8da5bdfb8b05eee69c38af7e32ae1954ae223f2b040dbfc2a16155c` |
| `p1e_fixed_support_certificate.schema.json` | `e462e2fe5f4199064fe92fdd01f284f22634c0b258aec0a225a3be0080a05f1c` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `14508546332c0f1f936a77010a0aa698cb7fb3b25d02551b8b2cc40cf350d3a7` |

The PDF is 24 US-letter pages, has no encryption or JavaScript, and carries the
title `A sharp positivity--rate frontier for quadratic fidelity of reversible
spherical generators` in its document metadata.

## Reference authoring environment

The canonical checked-in artifact was produced by the exact materialization workflow with:

```text
Python 3.12.13
matplotlib 3.10.8
pandoc 3.1.3
XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian)
pdftotext version 24.02.0
SOURCE_DATE_EPOCH=1785900000
FORCE_SOURCE_DATE=1
```

The build derives a fixed PDF trailer identifier from the checked-in source
inputs, so repeated builds in the recorded toolchain are byte-identical. Exact
PDF bytes can still differ under a different TeX distribution or font set. The
present consolidated revision workflow verifies the committed content hash,
metadata, page-range guard, extracted claim boundary, and absence of raw
citation or diagram markup. A permanent tagged release should additionally
run a clean rebuild in the recorded toolchain and compare the committed and
rebuilt PDF text token streams.

## Build command

From the repository root:

```bash
python docs/publication_program/p1f_manuscript/build_flagship_paper.py
pdfinfo output/pdf/FLAGSHIP_MANUSCRIPT.pdf
pdftotext output/pdf/FLAGSHIP_MANUSCRIPT.pdf -
```

The build script writes only the publication figure, a transient prepared
Markdown file and generated deterministic LaTeX header under
`tmp/pdfs/p1f-build`, and `output/pdf/FLAGSHIP_MANUSCRIPT.pdf`.

## Release-gate boundary

The historical workflow
`.github/workflows/afp-publication-p1f-flagship-paper.yml` enforced the original
14-path publication layer from the P1E tree. It remains provenance for that
historical release, but it does not certify the present major-revision delta.
The consolidated audit-revision workflow must instead verify the revised
claim surface, rebuilt PDF, exact P2F records, and unchanged Lean sources. The
historical workflow checked:

1. exact repository, head, ancestry, branch, and archive identities;
2. the manuscript theorem hierarchy, complete citation set, source/test/claim
   map, priority boundary, and stale-claim exclusions;
3. a clean PDF rebuild and semantic comparison with the committed artifact;
4. retained P1A--P1D deterministic audits and the accepted P1E polygon and
   short-gap construction audits;
5. the full pinned Lean build, focused construction elaboration, and public
   axiom surfaces; and
6. final artifact digests on the unchanged exact head.

Expected `BLOCKED`, `REJECTED`, and `OPEN_UNCERTIFIED` labels in separate
route-obstruction documents are not active paper claims. The active robustness
labels are `P1E-ROBUST-FIXED | PROVED` and
`P1E-ROBUST-UNIFORM | REJECTED`. A new tagged release must preserve the revised
source, PDF, certificate-interface files, environment record, and validation
logs rather than relying on the mutable `archive/...` branch convention.
