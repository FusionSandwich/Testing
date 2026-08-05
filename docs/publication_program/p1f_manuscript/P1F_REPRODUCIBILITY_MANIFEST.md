# Flagship-paper reproducibility manifest

## Immutable mathematical base

The paper release is a one-commit publication layer over the accepted P1E
construction archive.

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
| `FLAGSHIP_MANUSCRIPT.md` | `45ece3825ff382f3558c1a43ed14f53621b3ed088f4e34584b224ed071c6fb6f` |
| `priority_sources.bib` | `8a896552a8a03154ba834466bdd80a6af65c39e5f440f53e2afbbc462746ae48` |
| `proof_dependency_graph.png` | `745d14b2cc65c07c584ccd5d56667aaecb6d59fb9cff264ca6d90b31e0d6eee2` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `b85aedef5176f44004ca52bf9e0e3c3008be6ab83498de9d782386ca891aefe1` |

The PDF is 23 US-letter pages, has no encryption or JavaScript, and carries the
title `A sharp positivity--rate frontier for quadratic fidelity of reversible
spherical generators` in its document metadata.

## Reference authoring environment

The reference artifact was produced with:

```text
Python 3.12.13
matplotlib 3.10.8
pandoc 3.1.3
XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian)
pdftotext 24.02.0
SOURCE_DATE_EPOCH=1785900000
```

Exact PDF bytes can depend on the TeX distribution and installed fonts.  The
release workflow therefore checks both the committed hash and a fresh build,
then compares the committed and rebuilt PDF text token streams, title,
bibliography coverage, page-range guard, and absence of raw citation or
diagram markup.

## Build command

From the repository root:

```bash
python docs/publication_program/p1f_manuscript/build_flagship_paper.py
pdfinfo output/pdf/FLAGSHIP_MANUSCRIPT.pdf
pdftotext output/pdf/FLAGSHIP_MANUSCRIPT.pdf -
```

The build script writes only the publication figure, a transient prepared
Markdown file under `tmp/pdfs/p1f-build`, and
`output/pdf/FLAGSHIP_MANUSCRIPT.pdf`.

## Exact release gate

The workflow
`.github/workflows/afp-publication-p1f-flagship-paper.yml` enforces a 14-path
diff from the immutable P1E tree.  It independently checks:

1. exact repository, head, ancestry, branch, and archive identities;
2. the manuscript theorem hierarchy, complete citation set, source/test/claim
   map, priority boundary, and stale-claim exclusions;
3. a clean PDF rebuild and semantic comparison with the committed artifact;
4. retained P1A--P1D deterministic audits and the accepted P1E polygon and
   short-gap construction audits;
5. the full pinned Lean build, focused construction elaboration, and public
   axiom surfaces; and
6. final artifact digests on the unchanged exact head.

The workflow uploads the PDF together with its validation logs.  Expected
`BLOCKED` or `REJECTED` labels in separate route-obstruction documents are not
active paper claims and are outside the 14-path publication layer.
