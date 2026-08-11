# Final GitHub preservation status

This commit closes the local-only evidence gap for the independent AFP audit and the first audit-driven repair batch.

## Permanently stored in Git history

1. All source, manuscript, registry, benchmark, test, Lean, workflow, and generated-PDF changes in PR #52.
2. The complete independent audit bundle, including the integrated report, every matrix, P2F diagnostics, diagnostic source, and hash manifest, under this directory as reconstructible Base64 parts.
3. Every unique non-source member of the authenticated PR #51 and PR #52 GitHub Actions archives under `workflow_artifacts/pr51/` and `workflow_artifacts/pr52/`, copied byte-for-byte.
4. Machine-readable manifests and SHA-256 inventories binding every preserved record to its original workflow run, artifact ID, source commit, source tree, and outer artifact digest.

The only workflow-artifact members not duplicated as new repository blobs are:

- `source-b8912c282a22420e8077c75929b16c7a33d189b2.tar.gz`;
- `source-d13e795a2cd09594b20812c88312278227bb5513.tar.gz`.

Those archives contain source already preserved by the exact Git commits and trees. Their archive SHA-256 values remain recorded in both evidence manifests, so their artifact identities have not been discarded.

## Verification

From `docs/consolidation/audit/2026-08-10`:

```bash
cat AFP_INDEPENDENT_AUDIT_BUNDLE.zip.b64.part-* \
  | tr -d '\n' \
  | base64 --decode \
  > AFP_INDEPENDENT_AUDIT_BUNDLE.zip

test "$(sha256sum AFP_INDEPENDENT_AUDIT_BUNDLE.zip | cut -d' ' -f1)" \
  = ab361d9013d82db4fc890cfc264fc05e557431bb892bdd86eea1d3c9747707ef

cd workflow_artifacts
sha256sum -c WORKFLOW_EVIDENCE_FILES.sha256
```

## Provenance boundary

- PR #51 remains unchanged at `b8912c282a22420e8077c75929b16c7a33d189b2`.
- The mathematical and P2F repair commit is `d13e795a2cd09594b20812c88312278227bb5513`.
- The independent-audit bundle preservation commit is `03575dd4a6c4b6cd35d025afdbff09738c0e8ba7`.
- The exact workflow-record preservation commit is `805be5a9e3f3821963cdf7f6f40e639a622f956a`.
- The authoritative final preservation commit is the Git commit containing this file.

Temporary materializer and helper refs were deleted after use. No historical archive ref was moved or rewritten.
