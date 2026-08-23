# Acquisition-gate summary

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
