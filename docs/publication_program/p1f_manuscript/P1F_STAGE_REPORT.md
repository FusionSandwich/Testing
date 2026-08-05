# P1F stage report — flagship manuscript assembly

## Status

```text
MANUSCRIPT_THEOREM_HIERARCHY_ASSEMBLED
P1E_ACCEPTANCE_GATE_GREEN_AND_ARCHIVE_FROZEN
P1F_RELEASE_CANDIDATE_PREPARED
```

The manuscript now assembles the accepted P1A--P1E mathematics.  The literal
P1E construction commit passed its exact-scope, retained-regression, pinned
Lean, and final-integrity jobs and is frozen at the base named in the
reproducibility manifest.  This report does not embed a self-referential claim
that the P1F exact-head workflow or archive freeze has already occurred.

## Mathematical scope

The controlling paper is `FLAGSHIP_MANUSCRIPT.md`. Its hierarchy is:

1. sampled quadratic quotients for positive reversible spherical generators;
2. exact covariance and two-defect decomposition;
3. the all-dimensional sharp frontier
   `mathfrak D_2 r_max >= d(d-1)`;
4. equality geometry and exact extremizers;
5. quantitative near-extremizer stability;
6. matching positive local constructions in `d=2,3` only.

The regular-polygon family uses fill/separation `h=pi/N`, active edge angle
`2h`, and constants

```text
R_2 = pi^2/8,
C_2 = 4,
c_2 = 16/pi^2.
```

The reflected adaptive-ring family on `S^2` uses

```text
R_3 = 64 pi^2,
C_3 = 75/2,
c_3 = 3/(32 pi^2).
```

The frontier, equality, and stability theorems remain all-dimensional. The
construction does not extend to `d>3`, and the `d=3` robustness proposition covers
only fixed-support reflected latitude perturbations with the construction's
counts, phases, masks, horizontal jumps, pole/equator data, and a common
ambient rotation preserved.

## Manuscript evidence set

| Role | File | Controlling boundary |
|---|---|---|
| paper | `FLAGSHIP_MANUSCRIPT.md` | theorem statements, proofs, examples, source map and limitations |
| primary-source priority audit | `PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md` | M1--M11 and finite-frame transfer table; no exact-conjecture search |
| bibliography | `priority_sources.bib` | primary-source records only |
| sampling/equality referee | `SAMPLING_ALIAS_EQUALITY_HOSTILE_REFEREE_REPORT.md` | quotient, leakage, trace, equality and stability conventions |
| construction/formal release audit | `FORMAL_AND_RELEASE_AUDIT.md` | finite Lean surface and deterministic P1E audit boundary |
| prose audit | `PROSE_OVERCLAIM_AUDIT.md` | dimension, robustness, priority, signed-operator and transport guards |
| reproducibility manifest | `P1F_REPRODUCIBILITY_MANIFEST.md` | immutable P1E base, content hashes, build environment and exact P1F gate |
| publication artifact | `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | rendered 23-page paper built from the checked-in source and bibliography |

The manuscript's Appendix B maps every displayed theorem to one ordinary
proof source, deterministic audit source, and global theorem-registry entry.
The global `THEOREM_REGISTRY.md`, `PAPER_BOUNDARY_MATRIX.md`,
`APPROACH_REGISTRY.md`, `VALUE_REGISTRY.md`, and `PRIOR_ART_MATRIX.md` have
the corresponding P1E scope and constants.

## Referee simulation disposition

The following independent attacks are retained.

| Attack | Disposition |
|---|---|
| restatement of graphical-design, stencil, Delaunay, sparsifier, design, scheme or frame theory | rejected only for the precise joint frontier/equality/stability theorem; all established concepts are attributed |
| sampling aliases, ambient leakage and equality | passed after quotienting by `K_X`, retaining codomain leakage, and distinguishing frontier equality from exact `H_2` |
| asymptotic construction | passed in `d=2,3` after literal all-orders row, Cauchy, recurrence, positivity, rate and quotient audits |
| transport or physical-performance overclaim | excluded; no such theorem is stated |

The construction audit is not a proof by finite computation. The regular
polygon is an all-`N` trigonometric identity. The adaptive-ring proof uses
literal symbolic limits, rational Cauchy bounds, exact floor/ceiling margins,
and a telescoping global conductance recurrence.

## Release boundary

The dedicated P1F exact-head workflow is based on the literal P1E archive
commit and tree. It allowlists only the
manuscript, its five audit/bibliography companions, any P1F stage metadata,
the reproducible build inputs, the rendered figure, and the publication PDF.
It must:

- verify exact P1E ancestry and immutable refs;
- parse the manuscript and bibliography;
- reject stale placeholder or `BLOCKED` construction language;
- check every theorem/source/test/registry mapping;
- rerun P1A--P1E deterministic audits and the full Lean build;
- record release-specific hashes and artifacts only in reproducibility data.

No candidate P1F commit/tree can be embedded in its own report.  Exact P1F
workflow and archive status are therefore external GitHub release metadata;
the immutable P1E base and content hashes are recorded in
`P1F_REPRODUCIBILITY_MANIFEST.md`.
