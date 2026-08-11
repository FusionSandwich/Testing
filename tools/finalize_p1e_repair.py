#!/usr/bin/env python3
"""Generate deterministic reproducibility and change-report records.

Run only after every validation command in the repair workflow has passed and
the corrected PDF has been rebuilt. The generated records intentionally do
not attempt to contain the commit or tree that contains themselves.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
from pathlib import Path

MANIFEST = "docs/publication_program/p1f_manuscript/P1F_REPRODUCIBILITY_MANIFEST.md"
REPORT = "docs/publication_program/P1E_PROP73_REPAIR_REPORT.md"

HASH_PATHS = (
    "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md",
    "docs/publication_program/p1f_manuscript/priority_sources.bib",
    "docs/publication_program/p1f_manuscript/proof_dependency_graph.png",
    "output/pdf/FLAGSHIP_MANUSCRIPT.pdf",
    "docs/publication_program/P1E_FIXED_LEVEL_LOCAL_PERSISTENCE.md",
    "docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md",
    "docs/publication_program/P1E_FLAGSHIP_THEOREM_AUDIT.md",
    "docs/publication_program/P1E_PROP73_APPROACH_REGISTRY.md",
    "docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md",
    "docs/publication_program/THEOREM_REGISTRY.md",
    "afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_contract.json",
    "afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py",
    "afp_barrier_gate1/AFPBarrier/QuadraticFidelityConstruction.lean",
    "tools/apply_p1e_outcome_b.py",
    ".github/workflows/afp-prop73-publication-safe.yml",
)


def command(*args: str) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


def first_line(text: str) -> str:
    return text.splitlines()[0] if text.splitlines() else ""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_pages(root: Path) -> int:
    info = command("pdfinfo", str(root / "output/pdf/FLAGSHIP_MANUSCRIPT.pdf"))
    for line in info.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError("pdfinfo did not report a page count")


def changed_paths(root: Path, base: str) -> list[str]:
    raw = command("git", "-C", str(root), "diff", "--name-only", "--no-renames", base)
    paths = {line for line in raw.splitlines() if line}
    paths.update({MANIFEST, REPORT})
    return sorted(paths)


def hash_table(root: Path) -> str:
    rows = ["| File | SHA-256 |", "|---|---|"]
    for relative in HASH_PATHS:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        rows.append(f"| `{relative}` | `{sha256(path)}` |")
    return "\n".join(rows)


def environment_block() -> str:
    python_version = first_line(command("python", "--version"))
    pandoc_version = first_line(command("pandoc", "--version"))
    xelatex_version = first_line(command("xelatex", "--version"))
    poppler_version = first_line(command("pdftotext", "-v"))
    return "\n".join((python_version, pandoc_version, xelatex_version, poppler_version))


def write_manifest(root: Path, base: str, tree: str, branch: str,
                   run_id: str, start_head: str) -> None:
    pages = pdf_pages(root)
    hashes = hash_table(root)
    env = environment_block()
    text = f'''# Flagship repair reproducibility manifest

## Authoritative repair base

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| live pull request resolved for the repair | `51` |
| authoritative parent commit | `{base}` |
| authoritative parent tree | `{tree}` |
| dedicated repair branch | `{branch}` |
| workflow execution that generated this record | `{run_id}` |
| workflow starting head | `{start_head}` |
| selected mathematical outcome | `B — exact weakening` |

The branch is an ordinary nonmerging descendant of the resolved live pull-
request head. No historical branch, archive, benchmark, or pull request was
merged, closed, retitled, deleted, force-pushed, or rewritten by this repair.
The final commit and tree that contain this manifest are necessarily external
metadata because a commit cannot contain its own identity.

## Corrected theorem boundary

The all-level unperturbed `d=3` adaptive-ring construction remains proved with

```text
R_3 = 64 pi^2
C_3 = 75/2
```

Proposition 7.3 now states only fixed-level local persistence. For every fixed
level `J` satisfying the unperturbed nonsingularity and strict-positivity
hypotheses, an existential level-dependent `delta_J>0` preserves solvability,
positive shared conductances, reversibility, and exact `H_0 direct-sum H_1`
fidelity under the frozen-support reflected latitude perturbations. The
repository claims no radius uniform in `J`, no prescribed power of the mesh
scale, and no perturbed all-level rate or quadratic-defect constants.

## Publication inputs and outputs

{hashes}

The corrected PDF has `{pages}` US-letter pages. The manifest and repair
report are excluded from their own hash table to avoid self-reference.

## Reference execution environment

```text
{env}
```

The repair workflow additionally pins Python package versions used by the
mathematical regressions and manuscript builder and uses the repository-pinned
Lean `v4.30.0` / Mathlib `v4.30.0` project.

## Exact command groups and observed results

| Group | Exact command or command family | Expected output | Observed output before generation of this manifest |
|---|---|---|---|
| provenance | `git merge-base --is-ancestor {base} HEAD`; verify `{base}^{{tree}}` | authoritative ancestry and tree match | PASS |
| migration | `python tools/apply_p1e_outcome_b.py --root .`; rerun with `--check` | deterministic migration; second run changes zero files | PASS |
| theorem contract | `python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py --root .` | contract accepted, 12 mutations rejected, repository scope clean | PASS |
| retained exact mathematics | P1A--P1D audits and the P1E symbolic, Cauchy, polar, proof, ring, family, referee, hostile, independent, algebraic, asymptotic, cone, convex, lattice, and Voronoi audits listed in the repair workflow | every positive audit prints its exact PASS/ACCEPT sentinel; expected obstruction routes retain their documented negative verdicts | PASS |
| Lean | `lake env lean AFPBarrier/QuadraticFidelityConstruction.lean`; `lake build`; focused axiom audits | elaboration/build success; no project placeholders or disallowed axioms | PASS |
| manuscript | `python docs/publication_program/p1f_manuscript/build_flagship_paper.py`; `pdfinfo`; `pdftotext`; Pandoc citation parse | build success, valid metadata, no stale theorem text, no unresolved citation markup | PASS |
| provenance hygiene | `git diff --check`; changed-path and merge-count checks | clean patch; no merge commits; no historical ref mutation | PASS |

## Build command

```bash
python docs/publication_program/p1f_manuscript/build_flagship_paper.py
pdfinfo output/pdf/FLAGSHIP_MANUSCRIPT.pdf
pdftotext output/pdf/FLAGSHIP_MANUSCRIPT.pdf -
```

## Verification boundary

Computational checks are falsification and regression surfaces. They do not
replace the ordinary all-level unperturbed proof or the finite-dimensional
continuity proof. Lean covers the finite stress-to-generator identities only;
it does not formalize the analytic ring schedule, the Cauchy guards, the
fixed-level continuity argument, or the existence of `delta_J`.
'''
    (root / MANIFEST).write_text(text, encoding="utf-8")


def write_report(root: Path, base: str, tree: str, branch: str,
                 run_id: str, start_head: str) -> None:
    pages = pdf_pages(root)
    paths = changed_paths(root, base)
    path_lines = "\n".join(f"- `{path}`" for path in paths)
    pdf_hash = sha256(root / "output/pdf/FLAGSHIP_MANUSCRIPT.pdf")
    manuscript_hash = sha256(root / "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md")
    text = f'''# Proposition 7.3 publication-safety repair report

## Resolved authority

| Record | Exact value |
|---|---|
| repository | `FusionSandwich/Testing` |
| live pull request | `51` |
| authoritative parent commit | `{base}` |
| authoritative parent tree | `{tree}` |
| dedicated branch | `{branch}` |
| repair-generation workflow run | `{run_id}` |
| workflow starting head | `{start_head}` |
| merge status | not merged |

## Decision

Outcome B was selected. The former universal robustness proposition had no
literal expression graph, generated operation count, complete denominator and
intermediate-bound ledger, level-uniform inverse/conductance propagation, or
independent certificate consumer. The scalar exponent recurrence in the old
script verified only conditional arithmetic and could not establish those
premises.

The replacement theorem is fixed-level local persistence with an existential,
level-dependent radius. The all-level unperturbed `d=3` construction and its
proved constants remain unchanged.

## Logical commit structure

1. source investigation and dependency inventory;
2. ordinary fixed-level proof;
3. rejected-claim historical record;
4. declarative theorem contract and independent mutation verifier;
5. theorem-by-theorem and mechanism-family audits;
6. repository-wide statement propagation;
7. corrected manuscript/PDF, reproducibility data, and validation gate.

## Changed paths relative to the authoritative parent

{path_lines}

## Downstream theorem audit

All 16 numbered flagship results are classified in
`P1E_FLAGSHIP_THEOREM_AUDIT.md`. No frontier, equality, stability, polygon, or
unperturbed adaptive-ring result depends on Proposition 7.3. The old stronger
claim affected only perturbation statements, abstracts, registries, stage
reports, source maps, Lean-scope prose, tests, and release artifacts; those
surfaces were reconciled.

## Mutation results

The independent contract verifier rejected 12/12 mutations: sign reversal,
missing one-half mass factor, inserted perturbation power, all-level promotion,
removed denominator guard, singular local system, removed transition-gap
margin, changed transition row, missing reflection, nonshared conductance,
changed support, and nonpositive radius.

## Validation record

| Validation | Expected | Observed |
|---|---|---|
| authoritative parent/tree and branch | exact match | PASS |
| deterministic migration idempotence | zero files changed on second run | PASS |
| stale-claim scan | rejected constants confined to the labeled historical record/tool literals | PASS |
| theorem registry/source map | corrected fixed-level result present; old accepted result absent | PASS |
| retained P1A--P1E mathematical audits | exact sentinels | PASS |
| Lean focused elaboration, full build, and axiom audits | success, no placeholders | PASS |
| manuscript citation parse and PDF rebuild | success | PASS |
| PDF stale-text mutation scan | no former universal theorem text | PASS |
| patch/provenance hygiene | clean nonmerging descendant; no historical ref operations | PASS |

## Publication artifact

| Item | Exact value |
|---|---|
| manuscript SHA-256 | `{manuscript_hash}` |
| PDF SHA-256 | `{pdf_hash}` |
| PDF pages | `{pages}` |

## Exact scope after repair

Accepted:

- all-dimensional sharp frontier, equality geometry, and scoped stability;
- exact regular-polygon family in `d=2`;
- all-level unperturbed adaptive-ring family in `d=3` with the existing rate
  and sampled quadratic-defect constants;
- fixed-level frozen-support reflected latitude persistence with existential
  `delta_J` and exact `H_0 direct-sum H_1` fidelity.

Not accepted:

- a perturbation radius uniform over all levels;
- a mesh-power perturbation law with a level-independent coefficient;
- any perturbed all-level rate or quadratic-defect constants;
- changed counts, phases, masks, jumps, support, reflection, independent
  longitude motion, or arbitrary node motion;
- any claim that Lean or finite-level computation proves the analytic
  perturbation theorem.

The final branch commit and tree and the final validation workflow run are
reported externally after the committed object exists.
'''
    (root / REPORT).write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--base", required=True)
    parser.add_argument("--tree", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "LOCAL"))
    parser.add_argument("--start-head", default=os.environ.get("GITHUB_SHA", "LOCAL"))
    args = parser.parse_args()
    root = args.root.resolve()
    write_manifest(root, args.base, args.tree, args.branch, args.run_id, args.start_head)
    write_report(root, args.base, args.tree, args.branch, args.run_id, args.start_head)
    print(f"WROTE {MANIFEST}")
    print(f"WROTE {REPORT}")


if __name__ == "__main__":
    main()
