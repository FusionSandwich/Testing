# P1F stage report — flagship manuscript assembly

## Status

```text
MANUSCRIPT_MAJOR_REVISION_IN_PROGRESS
P1E_UNPERTURBED_CONSTRUCTION_RETAINED
P1E_FIXED_LEVEL_ROBUSTNESS_PROVED
P1E_UNIFORM_ROBUSTNESS_REJECTED
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
6. matching positive local constructions in `d=2,3` only; and
7. fixed-level support-preserving robustness for every `M_0=2^80`, `d=3` production level,
   with a computable level-dependent radius.

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
construction does not extend to `d>3`. Proposition 7.3 is proved for every
fixed `M_0=2^80`, `d=3` production level with the full support pattern fixed. Its radius is
computable from finite inverse, derivative, positivity, and gap margins but is
not uniform in refinement. On a sufficiently small neighborhood the
conservative constants are `1024` and `54`. The former all-level majorant is
rejected as uncertified.

## Manuscript evidence set

| Role | File | Controlling boundary |
|---|---|---|
| paper | `FLAGSHIP_MANUSCRIPT.md` | theorem statements, proofs, examples, source map and limitations |
| primary-source priority audit | `PRIORITY_AND_HOSTILE_REFEREE_AUDIT.md` | M1--M11 and finite-frame transfer table; no exact-conjecture search |
| bibliography | `priority_sources.bib` | primary-source records only |
| sampling/equality referee | `SAMPLING_ALIAS_EQUALITY_HOSTILE_REFEREE_REPORT.md` | quotient, leakage, trace, equality and stability conventions |
| construction/formal release audit | `FORMAL_AND_RELEASE_AUDIT.md` | finite Lean surface and deterministic P1E audit boundary |
| fixed-level perturbation theorem | `../P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md` | finite block system, level-dependent radius, positivity and exactness boundary |
| prose audit | `PROSE_OVERCLAIM_AUDIT.md` | dimension, fixed-level/uniform robustness boundary, priority, signed-operator and transport guards |
| reproducibility manifest | `P1F_REPRODUCIBILITY_MANIFEST.md` | historical P1E base, revised content hashes, build environment, and explicit boundary between the historical P1F gate and this major-revision gate |
| publication artifact | `output/pdf/FLAGSHIP_MANUSCRIPT.pdf` | rendered 24-page paper built from the checked-in source and bibliography |

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

The historical dedicated P1F workflow certifies only the original 14-path
publication layer over the P1E archive. It does not certify this audit-driven
major-revision delta, which also changes the controlling P1E claim registries
and the P2F experiment. The consolidated revision workflow must:

- verify ancestry from the accepted P2E execution and preserve the historical
  P1E/P2E refs without moving them;
- enforce the proved fixed-level and rejected uniform robustness statuses and
  the finite-only Lean boundary;
- reproduce and audit the revised P2F reference sweep twice;
- rerun the retained exact numerical and Lean gates; and
- bind the revised Markdown, PDF, result records, environment, and hashes in a
  new immutable tagged release.

No candidate commit can embed its own hash. Exact revision workflow and release
identifiers therefore remain external metadata. The historical P1E base and
current content hashes are recorded in `P1F_REPRODUCIBILITY_MANIFEST.md`.
