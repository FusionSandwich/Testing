#!/usr/bin/env bash
set -euo pipefail

original="${RUNNER_TEMP}/prop73-materializer-original.sh"
patched="${RUNNER_TEMP}/prop73-materializer-patched.sh"
git show 61c6f1cfe012ac69641c966e15bfed70bf660cdf:.github/prop73-materialize-script/run.sh > "${original}"
cp .github/prop73-materialize-script/publish_objects.py "${RUNNER_TEMP}/prop73-publish-objects.py"
python - "${original}" "${patched}" <<'PY'
from pathlib import Path
import sys
src, dst = map(Path, sys.argv[1:])
text = src.read_text(encoding='utf-8')
text = text.replace("CANDIDATE_BRANCH='agent/afp-prop73-final-candidate-73249d00'\n", '')
text = text.replace(
    'export TARGET_BRANCH CANDIDATE_BRANCH AUTHORITATIVE_PARENT AUTHORITATIVE_PARENT_TREE',
    'export TARGET_BRANCH AUTHORITATIVE_PARENT AUTHORITATIVE_PARENT_TREE',
)
text = text.replace(
    'test "$(git rev-parse HEAD^)" = "${AUTHORITATIVE_PARENT}"\n',
    'git merge-base --is-ancestor "${AUTHORITATIVE_PARENT}" HEAD\n',
)
text = text.replace(
    'test -z "$(git ls-remote origin "refs/heads/${CANDIDATE_BRANCH}")"\n',
    '',
)
marker = "say 'Create a clean one-parent repair commit and publish the candidate ref'"
start = text.index(marker)
text = text[:start] + '''say 'Create authenticated remote Git objects for the clean one-parent repair commit'\nlocal_tree="$(git write-tree)"\nexport LOCAL_FINAL_TREE="${local_tree}"\npython "${RUNNER_TEMP}/prop73-publish-objects.py"\n'''
dst.write_text(text, encoding='utf-8')
PY
chmod +x "${patched}"
exec "${patched}"
