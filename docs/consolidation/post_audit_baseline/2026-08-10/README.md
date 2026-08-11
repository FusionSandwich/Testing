# AFP post-audit provenance baseline

This directory is the committed provenance baseline for the AFP spherical-generator repair line. It contains no new mathematical repair.

- `AUTHORITATIVE_STATE.md` gives the authoritative live-state decision and principal hashes.
- `BUNDLE_MANIFEST.json` records SHA-256 and Git-blob identities for the deterministic complete bundle and every binary part.
- `AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz.part-*` reconstruct the complete 26-file baseline bundle: all relevant refs and PRs, ancestry/content graph, 151-row theorem/evidence dependencies, imported/generated evidence manifests, frozen and authorized scopes, environment/reproduction commands, test report, and local logs.

Reconstruct and extract:

```bash
cat AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz.part-* > AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz
sha256sum AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz
tar -xJf AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz -C extracted-baseline
```

Expected bundle SHA-256: `6028c41f3474144d60fca43dc6bf67e0765cd9e4d23edee40c96a9c97b57123e`.

The repair branch was created from commit `d56db0ba8c24b63e56ec107e2f044449c726ce20`, tree `4142cea31e3d5c48399d0af554226ab347e3d71a`.
