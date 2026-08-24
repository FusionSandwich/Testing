# Acquisition-gate summary

## R8 pre-build gate, 2026-08-24 EDT

This gate was completed in the new isolated R8 worktree before any build,
render, cache staging, or dependency-environment operation. The controlling
target is
`D:\math_lean_1\Testing-afp-major-revision-r8-20260824`, created clean on
branch `codex/afp-major-revision-r8-20260824` from exact R7 head
`e5d023e50ead92f9d87c7e625860225b4e6aa89b`. The R7 worktree was separately
confirmed clean at that SHA and is not an edit, cleanup, reset, rebase, cache,
or build target.

The host runs Windows 11 Home 10.0.26200 with 31.91 GiB RAM and 10.47 GiB
free at inspection. The system volume `C:` has 16.21 GiB free of 930.42 GiB;
the target/data volume `D:` has 847.68 GiB free of 1,863.02 GiB. Largest
working sets were ChatGPT (1.54 GiB), memory compression (1.53 GiB), Codex
(1.23 GiB), Chrome (up to 0.66 GiB), WSL (0.63 GiB), Defender (0.50 GiB),
and Explorer (0.36 GiB). Separate pre-existing CPU-heavy Python replay jobs
and a bounded Alliance evidence transfer were observed outside this worktree;
R8 neither owns nor modifies them and launches no remote work.

Existing executable/runtime inventory is Git 2.55.0.windows.3, system Python
3.12.10, Elan 4.2.3, ambient Lean 4.33.1/Lake 5.0.0, project-pinned and already
installed Lean 4.30.0, Pandoc 3.8.3, bundled Node 24.19.0, bundled Python
3.12.13 with pdfplumber 0.11.9 and pypdf 6.14.2, bundled Tectonic 0.17.0, and
bundled Poppler 26.05.0. The Python launcher exposes 3.12, 3.11, and 3.9;
Conda is absent. No `pyvenv.cfg` was found inside the AFP checkout family; an
unrelated active replay environment under another project was recorded but is
not used. The R5 disposable exact-audit target remains the already-local
read-only source of SymPy and numerical packages.

Current relevant caches and build trees were measured before staging: pip
index cache 1,623.4 MB; clean R7 `.lake` build/config 141,513,742 bytes in 478
files; clean R7 Tectonic cache 46,334,016 bytes in 355 files; and the R5
disposable Python target 363,126,888 bytes in 10,716 files. The R7 Lean package
path is a junction to the already-local pinned package tree at
`C:\Users\joshu\Documents\PhD papers\lean\afp_barrier_lean_project\.lake\packages`.
Local Git inventory contains the original `Testing` checkout (two dirty
entries, excluded from staging) plus clean isolated R5, R6, R7, and R8
worktrees at their recorded branch heads.

Existing local capabilities are sufficient. **Authorized network acquisition:
0 bytes.** No install, upgrade, dependency resolution, new package download,
remote execution, or remote spending is planned. The only planned
dependency-environment modification is local staging into the R8 ignored
paths: copy the R7 `.lake` build/config bytes and recreate its junction, and
copy the R7 Tectonic cache, at most **187,847,758 existing local bytes** total.
Targets are
`D:\math_lean_1\Testing-afp-major-revision-r8-20260824\afp_barrier_gate1\.lake`
and
`D:\math_lean_1\Testing-afp-major-revision-r8-20260824\tmp\pdfs\tectonic-cache`.
Build outputs and renders remain under the R8 worktree. Rollback removes only
those verified R8-local ignored paths; it never touches the R7 worktree,
shared package junction target, user caches/toolchains, or dirty original
checkout. Any materially different dependency, target, or network attempt
requires a new gate.

## R7 pre-build gate, 2026-08-24 EDT

This gate was completed before the R7 worktree, build, render, or dependency
operation. The host `VENGEANCE` runs Windows 11 and has 31.91 GiB RAM, with
9.73 GiB free at inspection. The system volume `C:` has 23.02 GiB free of
930.42 GiB; the target/data volume `D:` has 851.71 GiB free of 1,863.02 GiB.
The fixed target is
`D:\math_lean_1\Testing-afp-major-revision-r7-20260824`.

The largest working sets were memory compression (1.58 GiB), Codex (0.91
GiB), ChatGPT (0.84 GiB), several Chrome processes (0.4--0.8 GiB), WSL (0.59
GiB), Defender (0.56 GiB), and Explorer (0.50 GiB). No scientific compute job
was running or launched.

Existing tools are Git 2.55.0, Lean 4.33.1, Lake 5.0.0, Elan 4.2.3, system
Python 3.12.10, and Python launcher environments 3.12, 3.11, and 3.9. Conda
and `uv` are absent. The already-installed Codex primary runtime (1.30 GiB)
provides Node 24.19.0 and Python 3.12.13; the local LaTeX/PDF workflow uses the
already-bundled runtime and cache rather than a system TeX installation.

Measured existing caches include pip 1.47 GiB and Elan/toolchains 11.72 GiB.
The local checkout inventory includes the original `Testing` checkout and the
isolated R5, R6, and R7 worktrees. The original checkout is dirty and is not a
staging target. The R6 base was clean and both its local and origin branch refs
resolved exactly to `da137c157dbc92774cbf7e378efb5bf360be6ceb`; the requested
scientific commit `648691e9225359d0983d71fa332408fc7bdbadd9` also resolved.

Existing local capabilities are sufficient. **Authorized network acquisition:
0 bytes.** No install, upgrade, package resolution, dependency-environment
build, or remote execution is planned. The R7 worktree initially lacks
`.lake`; the smallest local staging operation copies the clean R6 `build` and
`config` state, exactly 141,513,742 bytes in 478 files, and recreates its
package junction to the already-local pinned package tree. Target:
`D:\math_lean_1\Testing-afp-major-revision-r7-20260824\afp_barrier_gate1\.lake`.
Build outputs and temporary PDF renders are confined to the R7 worktree and
its ignored temporary directories. Rollback removes only that verified R7
`.lake` path and R7-local generated/temporary paths; it does not touch user
toolchains, caches, the junction target, the dirty original checkout, or prior worktrees.
A separate manuscript staging operation copies the clean R6 Tectonic resource
cache, exactly 46,334,016 bytes in 355 files, into the fixed ignored target
`D:\math_lean_1\Testing-afp-major-revision-r7-20260824\tmp\pdfs\tectonic-cache`.
It reuses bundled Tectonic 0.17.0 and Poppler 26.05.0. Rollback removes only
that verified R7-local cache/render tree; no system or shared cache is changed.
A materially different dependency or target requires a new gate.

## Historical R6 gate

### R6 pre-build gate, 2026-08-23 EDT

This gate was completed before any R6 build or dependency staging command.
The host has 34,260,418,560 bytes of RAM (33,457,440 KiB visible),
13,817,220 KiB free physical memory at inspection, and 20 logical processors.
The system volume `C:` has 10,671,575,040 bytes free of 999,032,877,056;
the target/data volume `D:` has 915,216,756,736 bytes free of
2,000,397,791,232. R6 remains entirely under the fixed target
`D:\math_lean_1\Testing-afp-major-revision-r6-20260823`.

The largest observed working sets were WSL (`vmmemWSL`, about 3.99 GB), Codex
processes (about 1.31 GB each at the top), Windows memory compression (about
0.74 GB), Defender (about 0.55 GB), Explorer, VS Code, and Docker. No separate
CPU-intensive scientific job was launched. The available RAM and `D:`
headroom are adequate for the previously measured local builds.

Existing executable/runtime inventory:

- Git 2.55.0.windows.3;
- Python launcher environments 3.12.10, 3.11, and 3.9; no Conda executable or
  Conda environments; no repository `pyvenv.cfg` was found outside ignored
  dependency trees;
- Elan 4.2.3 with Lean toolchains 4.30.0, 4.32.0, 4.32.2, and 4.33.1; the
  project pins 4.30.0 even though the ambient default is 4.33.1;
- Lake 5.0.0, Pandoc 3.8.3, bundled Tectonic 0.17.0, bundled Poppler 26.05.0,
  bundled Python 3.12.13, and bundled Node 24.19.0;
- system Python already has Matplotlib 3.11.1, NumPy 2.5.1, and pytest 8.4.2;
  the R5 disposable exact-audit target already contains the pinned SymPy and
  numerical stack and will be read, not modified.

Existing caches and local sources were measured before staging: pip cache
1,572,587,537 bytes; Elan/toolchains 12,584,471,820 bytes; dirty original
checkout `.lake` 7,071,020,685 bytes; verified R5 worktree `.lake`
141,513,742 bytes; R5 Tectonic cache 46,334,016 bytes; R5 disposable Python
target 363,126,888 bytes; and the shared pinned Lean package checkout
7,006,245,609 bytes. Local Git worktrees were enumerated for the dirty
original checkout, verified R5 branch, and isolated R6 branch. The original
dirty checkout status was recorded before work and is not a staging target.

Existing local capabilities are sufficient. **Authorized network acquisition:
0 bytes.** No install, upgrade, package resolution, or remote build is
planned. The only dependency-environment modification is a local private R6
staging copy of the measured R5 project build/config (141,513,742 bytes) and
Tectonic cache (46,334,016 bytes), total at most **187,847,758 local bytes**,
plus a junction to the already-local pinned Lean package checkout. Target:
the R6 worktree's ignored `.lake` and `tmp/pdfs/tectonic-cache` directories.
If any tool attempts a network fetch, validation stops. Rollback removes only
the resolved R6 `.lake` and `tmp/pdfs` staging directories after verifying
that both paths remain beneath the named R6 worktree; it never touches the
dirty original checkout, R5 tracked files, shared source checkout, or user
toolchains.

The observations above close the R6 acquisition gate for the bounded local
build/test/render plan. A materially different dependency or target requires
a new gate.

## R5 retained record

The complete timestamped pre-acquisition record is retained at
`D:\math_lean_1\AFP_R5_ACQUISITION_GATE_20260822.md`.

Before Git acquisition, the record captured 31.91 GiB RAM, free space on `C:`
and `D:`, significant processes, Git/GitHub/Lean/Lake/Elan/Python/CMake
executables and versions, Python/Conda state, pip/Elan/Lake caches, local Git
checkouts, the absent authoritative object, a 1--25 MiB Git estimate, the new
worktree target, and rollback. The authoritative ref then matched
`f0ec4a8e539ebf72f5324f92439b56545ea8d2c5` exactly.

A second gate at 21:39 EDT recorded that `cvxpy` was absent from every existing
Python/WSL environment and local cache. With 852.40 GiB free on `D:`, it
authorized only a disposable `release/tmp/cvxpy-site` target, bounded at
25--150 MiB download / 500 MiB installed, with all pip temp/cache paths under
the same excluded `release/tmp` tree. Existing environments are not modified;
rollback removes only those validated disposable subdirectories.

Python 3.11 dependency resolution stopped before installation because the
pinned SciPy 1.18 requires Python >=3.12. The retry used the already-installed
Python 3.12.10 with the same target and rollback; no pin was weakened.

At 21:46 EDT a third gate recorded 31.91 GiB RAM / 6.69 GiB free, `C:` 11.14
GiB free, `D:` 851.65 GiB free, significant processes, all compiler/runtime
versions, Python/Conda state, caches, and the three relevant checkout states.
The corrected manuscript cannot reuse the stale PDF; `xelatex` is absent and
the already-bundled Tectonic 0.17.0 has no resource cache. Only its default TeX
resource bundle is authorized, bounded at 50--500 MiB download / 1 GiB on the
fixed `D:` target `tmp/pdfs/tectonic-cache`. Rollback removes only validated
R5 build/cache paths; it does not touch an installed environment or the dirty
original checkout.
