# Flagship-paper reproducibility manifest

## Immutable mathematical base

The original paper release was a one-commit publication layer over the
accepted fixed-family P1E construction archive. This audit-driven revision
supersedes the original robustness wording while retaining that archive as
historical provenance. The archived P1E files do not certify a perturbation
theorem.

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
| `FLAGSHIP_MANUSCRIPT.md` | `453f9e69acad66b201e7e70940d058aaa01a68af2b15a6d143b45a6bbb7315bc` |
| `priority_sources.bib` | `8a896552a8a03154ba834466bdd80a6af65c39e5f440f53e2afbbc462746ae48` |
| `proof_dependency_graph.png` | `745d14b2cc65c07c584ccd5d56667aaecb6d59fb9cff264ca6d90b31e0d6eee2` |
| `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | `8d09af48519b3df81881be47f4a8e477b38ed6485ed74e82d8d9167c6e7824c4` |

The PDF is 24 US-letter pages, has no encryption or JavaScript, and carries the
title `A sharp positivity--rate frontier for quadratic fidelity of reversible
spherical generators` in its document metadata.

## Reference authoring environment

The reference artifact was produced with:

```text
Python 3.13.5
matplotlib 3.10.8
pandoc 3.1.11.1
XeTeX 3.141592653-2.6-0.999996 (TeX Live 2025/dev/Debian)
pdftotext 25.06.0
SOURCE_DATE_EPOCH=1785900000
```

Exact PDF bytes can depend on the TeX distribution and installed fonts. The
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
Markdown file under `tmp/pdfs/p1f-build`, and
`output/pdf/FLAGSHIP_MANUSCRIPT.pdf`.

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
route-obstruction documents are not active paper claims. A new tagged release
must preserve the revised source, PDF, environment record, and validation logs
rather than relying on the mutable `archive/...` branch convention.
