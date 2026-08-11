# AFP authoritative live state

Capture began on 2026-08-10 and completed at `2026-08-11T04:31:14.413497Z` (`2026-08-11T00:31:14-0400` in America/Montreal).

## Decision

The unique strongest valid authoritative descendant is:

- repository: `FusionSandwich/Testing`
- source branch at capture: `agent/afp-audit-major-revisions-b8912c2`
- commit: `d56db0ba8c24b63e56ec107e2f044449c726ce20`
- tree: `4142cea31e3d5c48399d0af554226ab347e3d71a`
- dedicated repair branch created from it: `agent/afp-post-audit-repair-d56db0b`

It is a strict, merge-free descendant of accepted P2E commit `e60f5c7d6bb6dd3cf7557d504716d7f13403dd72`, the exact eight post-P2E commits, and PR #51 head `b8912c282a22420e8077c75929b16c7a33d189b2`. The first post-PR51 commit removes the unsupported universal Proposition 7.3 certificate, narrows formal-verification wording, and changes P2F from a bounded negative claim to reference-inconclusive. The three later commits only preserve audit and workflow evidence. No stale universal Proposition 7.3 theorem is reintroduced on the selected line.

## Live PR #51

- state: open; unmerged; non-draft; mergeable
- target: `testing` at `d8f85f1d3faa530cfefba7a59086df4dc85eff74` / tree `144abcaa72c39dcc528885793b22563deee07b44`
- head: `agent/afp-consolidated-p2e-p2f-e60f5c7` at `b8912c282a22420e8077c75929b16c7a33d189b2` / tree `4c2175463a661ce3f2bb206f0cb7b5038183b2ab`
- recorded head/tree comparison: unchanged
- delta: 293 commits, 419 changed paths, 131,524 additions, zero deletions

## Target compatibility

`testing` is the exact merge base of the selected descendant. The selected parent is 297 commits ahead and zero behind, so the history can be received by fast-forward without dropping AFP commits.

## Math import

The source remains `FusionSandwich/Math@ccc75ff90ddd8348aa805178f9f1925b9b10cd16` / tree `10ba13da2c732becdee26dc26fbc125a9350139a`. All 33 recorded source Git blobs equal the actual Math blobs and the imported Testing blobs byte-for-byte. Later Math branches do not change these imported blobs and are classified as unrelated AFP-adjacent work.

## Workflows and artifacts

Testing registers 59 workflows and Math registers 67. Only 27 Testing workflow files and 2 Math workflow files are committed at the selected source trees. The other registrations are retained GitHub historical state, not source present at the selected commits. Exact-head workflow run `31456468144` succeeded on the selected parent and produced artifact `9088240817` with outer SHA-256 `18e1a9c431c7023769d4856e3964fd735dab08e9d39a344395c83dee6876f063`.

## Mutability and release status

Neither repository has a tag or GitHub release. Every `archive/*` object is an ordinary unprotected branch pointer and is mutable. Commit/tree/blob IDs and external SHA-256 digests are the immutable provenance anchors.

## Reproducibility

The exact selected source reconstructs to its recorded Git tree with 540 tracked files, no submodules, no gitlinks, and no symbolic links. Local and CI results are separated in `BASELINE_TEST_REPORT.md`; passing CI is not treated as mathematical correctness or full-paper formal verification.
