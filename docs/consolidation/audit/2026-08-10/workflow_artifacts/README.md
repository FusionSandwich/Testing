# Permanently preserved workflow evidence

**Historical supersession warning.** PR #51 records retain the withdrawn
`BOUNDED_NEGATIVE` P2F conclusion byte-for-byte for provenance. They are not
the current scientific interpretation. PR #52/current schema v2 classifies
P2F as `INCONCLUSIVE_REFERENCE_NOT_CONVERGED` because the reference hierarchy
is unconverged and the selected responses are operator-insensitive.

This directory contains every unique non-source member from the authenticated PR #51 and PR #52 GitHub Actions archives. Each file is copied byte-for-byte from its workflow artifact.

The only omitted members are the two large `source-<commit>.tar.gz` files. They duplicate the exact Git trees already stored permanently by Git; their SHA-256 values, source commits, source trees, artifact IDs, workflow runs, and outer artifact hashes are retained in `WORKFLOW_EVIDENCE_MANIFEST.json`.

The original GitHub Actions archives remain downloadable until their recorded expiry dates, but no unique numerical result, audit result, environment record, provenance record, checksum record, or held-out artifact depends on that retention window.
