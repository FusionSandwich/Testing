# Independent post-commit verification

A fresh repository was materialized from authoritative parent tree `4142cea31e3d5c48399d0af554226ab347e3d71a` and the exact committed baseline blobs. It reproduced baseline tree `7c21266488f59b486f23d9ceedc40aafb303e107` before this verification overlay was added.

The split archive reconstructed to SHA-256 `6028c41f3474144d60fca43dc6bf67e0765cd9e4d23edee40c96a9c97b57123e` and extracted 26 files. A generic embedded-manifest check found exactly one packaging-only mismatch: the archived `README.md` was a transport wrapper inserted after the embedded manifest was generated. It is not theorem, source, import, workflow, preregistration, held-out, or generated evidence.

`BUNDLE_README.md` is the exact neutral README already recorded by the embedded manifests: SHA-256 `e6b947e675938019a8d1b405de2473676e108c541e24af59551497665116ff87`, Git blob `8b6b79e91d67daf0e7b22297e5c46862b287ad2d`. After copying it to the extracted `README.md`, all 25 embedded line-oriented SHA-256 records pass. All JSON parses pass; the reconstructed source has no submodules, gitlinks, or symbolic links.

Verified inventory counts are 131 refs, 126 registered workflows, 151 theorem/evidence rows, 33 imports, and 62 generated-evidence records.
