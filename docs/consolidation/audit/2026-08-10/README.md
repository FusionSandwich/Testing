# AFP GitHub preservation record

This directory closes the remaining local-only evidence gap for the independent AFP audit and the first audit-driven repair batch.

## Saved objects

- The complete source, manuscript, registry, benchmark and workflow changes are committed on PR #52 branch `agent/afp-audit-major-revisions-b8912c2`.
- The complete independent audit package is preserved here as nine lexically ordered Base64 text parts.
- The original PR #51 validation archive and the successful PR #52 exact-head archive remain stored in GitHub Actions. Their run IDs, artifact IDs, sizes, expiry dates and SHA-256 values are recorded in `GITHUB_EVIDENCE_MANIFEST.json`.
- The exact Git commits permanently preserve the source represented by the large source tarballs inside those workflow archives.

## Reconstruct the audit bundle

Run from this directory:

```bash
cat AFP_INDEPENDENT_AUDIT_BUNDLE.zip.b64.part-* \
  | tr -d '\n' \
  | base64 --decode \
  > AFP_INDEPENDENT_AUDIT_BUNDLE.zip

sha256sum AFP_INDEPENDENT_AUDIT_BUNDLE.zip
```

Expected SHA-256:

```text
ab361d9013d82db4fc890cfc264fc05e557431bb892bdd86eea1d3c9747707ef
```

The reconstructed ZIP contains the integrated referee report, claim-confidence matrix, 151-row theorem gate, reproducibility matrix, 128-entry branch/ref disposition, novelty matrix, exact-example and hostile-mutation matrix, P2F sensitivity diagnostics, diagnostic script and artifact hash list.

## Authoritative Git objects

| Role | PR | Commit | Tree |
|---|---:|---|---|
| Audited consolidated candidate | #51 | `b8912c282a22420e8077c75929b16c7a33d189b2` | `4c2175463a661ce3f2bb206f0cb7b5038183b2ab` |
| First repair batch before this preservation commit | #52 | `d13e795a2cd09594b20812c88312278227bb5513` | `30caf52fcd7ce8ff1c73a6ac1f310a1455416e03` |

The preservation commit is the Git commit containing this file. PR #51 and all historical archive refs remain unchanged.
