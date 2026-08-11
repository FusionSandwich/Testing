# AFP post-audit provenance baseline

This directory is the committed provenance baseline for the AFP spherical-generator repair line. It contains no new mathematical repair.

Read `AUTHORITATIVE_STATE.md`, then use the JSON/CSV inventories. The compressed 26-file baseline is stored as `AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz.part-*`.

Reconstruct and verify the logical bundle:

```bash
cat AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz.part-* > AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz
printf '%s  %s\n' 6028c41f3474144d60fca43dc6bf67e0765cd9e4d23edee40c96a9c97b57123e AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz | sha256sum -c -
mkdir -p extracted-baseline
tar -xJf AFP_POST_AUDIT_BASELINE_BUNDLE.tar.xz -C extracted-baseline
cp BUNDLE_README.md extracted-baseline/README.md
cd extracted-baseline
sed -E 's/  git-blob:[0-9a-f]+$//' BASELINE_FILES.sha256 | sha256sum -c -
```

`BUNDLE_OVERLAY_MANIFEST.json` documents the packaging-only README correction. `POST_COMMIT_VERIFICATION.md` and `.json` record the independent reconstruction result.
