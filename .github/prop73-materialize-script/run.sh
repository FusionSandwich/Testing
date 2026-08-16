#!/usr/bin/env bash
set -euo pipefail

TARGET_BRANCH='agent/afp-post-audit-repair-d56db0b'
CANDIDATE_BRANCH='agent/afp-prop73-final-candidate-73249d00'
AUTHORITATIVE_PARENT='d05c98e5f1e211228940c7094df661c27d9e040b'
AUTHORITATIVE_PARENT_TREE='3c23cec0ebd25ca49706402774c25c395789a0d4'
PAYLOAD_B64_SHA256='2594548f614128eea6ead1c7c36dfb44a43b6a449e63b838f3f4cdf585d75159'
PAYLOAD_PATCH_XZ_SHA256='73249d00e2a55535d1be9bec4333cce421fc6c0bdd7c4508ad3a3ba01e0b2be1'
PAYLOAD_PATCH_SHA256='3490b07706c3907720a69c4798c600d045ac51898389c4e863dd0f70504bbd4c'
REPAIR_MANIFEST_SHA256='5bccdda3c75824edbcf8bcaee3e15902830e0e299fbd6a9cd4c058026ce4dd0e'
export TARGET_BRANCH CANDIDATE_BRANCH AUTHORITATIVE_PARENT AUTHORITATIVE_PARENT_TREE
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export SOURCE_DATE_EPOCH=1785900000 FORCE_SOURCE_DATE=1

say() { printf '\n==> %s\n' "$*"; }

say 'Verify staging provenance and immutable authoritative input'
test "$(git rev-parse HEAD)" = "${GITHUB_SHA}"
test "$(git rev-parse HEAD^)" = "${AUTHORITATIVE_PARENT}"
test "$(git rev-parse "${AUTHORITATIVE_PARENT}^{tree}")" = "${AUTHORITATIVE_PARENT_TREE}"
test "$(git rev-list --count --merges "${AUTHORITATIVE_PARENT}..HEAD")" -eq 0
remote_target="$(git ls-remote origin "refs/heads/${TARGET_BRANCH}" | awk '{print $1}')"
test "${remote_target}" = "${AUTHORITATIVE_PARENT}"
test -z "$(git ls-remote origin "refs/heads/${CANDIDATE_BRANCH}")"
test -z "$(git status --porcelain)"

say 'Reconstruct, authenticate, and apply the source overlay'
cat .github/prop73-payload/part-* > "${RUNNER_TEMP}/source.patch.xz.b64"
echo "${PAYLOAD_B64_SHA256}  ${RUNNER_TEMP}/source.patch.xz.b64" | sha256sum -c -
base64 -d "${RUNNER_TEMP}/source.patch.xz.b64" > "${RUNNER_TEMP}/source.patch.xz"
echo "${PAYLOAD_PATCH_XZ_SHA256}  ${RUNNER_TEMP}/source.patch.xz" | sha256sum -c -
xz -dc "${RUNNER_TEMP}/source.patch.xz" > "${RUNNER_TEMP}/source.patch"
echo "${PAYLOAD_PATCH_SHA256}  ${RUNNER_TEMP}/source.patch" | sha256sum -c -
git apply --check "${RUNNER_TEMP}/source.patch"
git apply --numstat "${RUNNER_TEMP}/source.patch" | cut -f3- > "${RUNNER_TEMP}/patch-paths.txt"
python - <<'PY'
from pathlib import Path, PurePosixPath
import os
paths = Path(os.environ['RUNNER_TEMP'], 'patch-paths.txt').read_text().splitlines()
assert len(paths) == 33, len(paths)
assert len(paths) == len(set(paths)), 'duplicate patch paths'
for name in paths:
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
assert 'output/pdf/FLAGSHIP_MANUSCRIPT.pdf' not in paths
assert 'docs/publication_program/p1f_manuscript/proof_dependency_graph.png' not in paths
print('SOURCE_PATCH_PATH_SAFETY_PASS', len(paths))
PY
git apply "${RUNNER_TEMP}/source.patch"
echo "${REPAIR_MANIFEST_SHA256}  docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json" | sha256sum -c -
python - <<'PY'
from pathlib import Path
import hashlib, json, os
root = Path('.')
manifest = root / 'docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json'
data = json.loads(manifest.read_text(encoding='utf-8'))
assert data['authoritative_parent'] == {
    'commit': os.environ['AUTHORITATIVE_PARENT'],
    'tree': os.environ['AUTHORITATIVE_PARENT_TREE'],
}
assert data['branch'] == os.environ['TARGET_BRANCH']
generated = {
    'docs/publication_program/p1f_manuscript/proof_dependency_graph.png',
    'output/pdf/FLAGSHIP_MANUSCRIPT.pdf',
}
patch_paths = set(Path(os.environ['RUNNER_TEMP'], 'patch-paths.txt').read_text().splitlines())
assert patch_paths == set(data['affected_paths']) - generated
for rec in data['records']:
    if rec['path'] in generated:
        continue
    raw = (root / rec['path']).read_bytes()
    assert len(raw) == rec['size'], rec['path']
    assert hashlib.sha256(raw).hexdigest() == rec['sha256'], rec['path']
print('SOURCE_MANIFEST_RECORDS_PASS')
PY

say 'Install deterministic build and audit dependencies'
python -m pip install --upgrade pip
python -m pip install 'numpy==2.3.5' 'pytest==9.0.2' 'matplotlib==3.10.8'
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  lmodern pandoc poppler-utils ripgrep texlive-fonts-recommended texlive-xetex texlive-latex-extra

say 'Build canonical PDF and dependency graph, then close all digests'
rm -f output/pdf/FLAGSHIP_MANUSCRIPT.pdf \
  docs/publication_program/p1f_manuscript/proof_dependency_graph.png
python docs/publication_program/p1f_manuscript/build_flagship_paper.py
pdfinfo output/pdf/FLAGSHIP_MANUSCRIPT.pdf > "${RUNNER_TEMP}/canonical-pdfinfo.txt"
pdftotext output/pdf/FLAGSHIP_MANUSCRIPT.pdf "${RUNNER_TEMP}/canonical-paper.txt"
pages="$(awk '/^Pages:/ {print $2}' "${RUNNER_TEMP}/canonical-pdfinfo.txt")"
test "${pages}" -ge 20 && test "${pages}" -le 35
grep -Fq 'Proposition 7.3 (fixed-level support-preserving robustness)' "${RUNNER_TEMP}/canonical-paper.txt"
! grep -Fq 'Open problem 7.3' "${RUNNER_TEMP}/canonical-paper.txt"
python - <<'PY'
from pathlib import Path
import hashlib, json, re, subprocess
repro = Path('docs/publication_program/p1f_manuscript/P1F_REPRODUCIBILITY_MANIFEST.md')
graph = Path('docs/publication_program/p1f_manuscript/proof_dependency_graph.png')
pdf = Path('output/pdf/FLAGSHIP_MANUSCRIPT.pdf')
def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
text = repro.read_text(encoding='utf-8')
text, n1 = re.subn(r'(`proof_dependency_graph\.png` \| `)[0-9a-f]{64}(` \|)', rf'\g<1>{digest(graph)}\2', text, count=1)
text, n2 = re.subn(r'(`output/pdf/FLAGSHIP_MANUSCRIPT\.pdf` \| `)[0-9a-f]{64}(` \|)', rf'\g<1>{digest(pdf)}\2', text, count=1)
assert (n1, n2) == (1, 1), (n1, n2)
versions = [
    subprocess.check_output(['python', '--version'], text=True, stderr=subprocess.STDOUT).strip(),
    'matplotlib ' + subprocess.check_output(['python', '-c', 'import matplotlib; print(matplotlib.__version__)'], text=True).strip(),
    subprocess.check_output(['pandoc', '--version'], text=True).splitlines()[0],
    subprocess.check_output(['xetex', '--version'], text=True).splitlines()[0],
    subprocess.check_output(['pdftotext', '-v'], text=True, stderr=subprocess.STDOUT).splitlines()[0],
    'SOURCE_DATE_EPOCH=1785900000',
    'FORCE_SOURCE_DATE=1',
]
replacement = '## Reference authoring environment\n\nThe canonical checked-in artifact was produced by the exact materialization workflow with:\n\n```text\n' + '\n'.join(versions) + '\n```'
text, n3 = re.subn(r'## Reference authoring environment\n.*?\n```text\n.*?\n```', replacement, text, count=1, flags=re.S)
assert n3 == 1, n3
repro.write_text(text, encoding='utf-8')
manifest = Path('docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json')
data = json.loads(manifest.read_text(encoding='utf-8'))
updates = {str(graph): graph, str(pdf): pdf, str(repro): repro}
seen = set()
for rec in data['records']:
    path = updates.get(rec['path'])
    if path is None:
        continue
    raw = path.read_bytes()
    rec['sha256'] = hashlib.sha256(raw).hexdigest()
    rec['size'] = len(raw)
    seen.add(rec['path'])
assert seen == set(updates), (seen, set(updates))
data['local_validation'].append('canonical GitHub materialization build and digest closure: PASS')
manifest.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
print('CANONICAL_GRAPH_SHA256', digest(graph))
print('CANONICAL_PDF_SHA256', digest(pdf))
print('CANONICAL_REPRO_SHA256', digest(repro))
print('CANONICAL_REPAIR_MANIFEST_SHA256', digest(manifest))
PY
rm -rf tmp

say 'Run the new theorem audits before publishing a candidate'
COV=afp_barrier_gate1/pure_math/covariance
FIXTURE="$COV/p1e_fixed_support_certificate_fixture.json"
python -m py_compile "$COV"/p1e_fixed_support_*.py
python "$COV/p1e_fixed_support_certificate.py" "$FIXTURE"
python "$COV/p1e_fixed_support_certificate_independent.py" "$FIXTURE"
python "$COV/p1e_fixed_support_robustness_audit.py"
python -m pytest -p no:cacheprovider -q afp_barrier_gate1/pure_math/tests/test_p1e_fixed_support_robustness.py

say 'Remove all one-use staging material and verify the exact final overlay'
rm -rf .github/prop73-payload .github/prop73-materialize-script
rm -f .github/workflows/afp-prop73-materialize.yml
git add -A
python - <<'PY'
from pathlib import Path
import hashlib, json, subprocess
root = Path('.')
manifest = root / 'docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json'
data = json.loads(manifest.read_text(encoding='utf-8'))
assert len(data['affected_paths']) == 35
assert len(data['records']) == 34
assert set(data['affected_paths']) - {r['path'] for r in data['records']} == {str(manifest)}
for rec in data['records']:
    raw = (root / rec['path']).read_bytes()
    assert len(raw) == rec['size'], rec['path']
    assert hashlib.sha256(raw).hexdigest() == rec['sha256'], rec['path']
actual = set(subprocess.check_output(['git', 'diff', '--name-only', 'd05c98e5f1e211228940c7094df661c27d9e040b'], text=True).splitlines())
assert actual == set(data['affected_paths']), {'missing': sorted(set(data['affected_paths'])-actual), 'extra': sorted(actual-set(data['affected_paths']))}
print('FINAL_REPAIR_MANIFEST_AND_PATH_ALLOWLIST_PASS', len(actual))
PY
git diff --check --cached
python - <<'PY'
import json, subprocess
m = json.load(open('docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json'))
for path in m['affected_paths']:
    mode = subprocess.check_output(['git', 'ls-files', '-s', '--', path], text=True).split()[0]
    assert mode == '100644', (path, mode)
print('FINAL_GIT_MODES_PASS')
PY

say 'Create a clean one-parent repair commit and publish the candidate ref'
export GIT_AUTHOR_NAME='github-actions[bot]'
export GIT_AUTHOR_EMAIL='41898282+github-actions[bot]@users.noreply.github.com'
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME" GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
final_tree="$(git write-tree)"
final_sha="$(printf '%s\n' 'Repair Proposition 7.3 with fixed-level support robustness' | git commit-tree "${final_tree}" -p "${AUTHORITATIVE_PARENT}")"
test "$(git rev-parse "${final_sha}^{tree}")" = "${final_tree}"
test "$(git rev-parse "${final_sha}^")" = "${AUTHORITATIVE_PARENT}"
test "$(git rev-list --count --merges "${AUTHORITATIVE_PARENT}..${final_sha}")" -eq 0
remote_target="$(git ls-remote origin "refs/heads/${TARGET_BRANCH}" | awk '{print $1}')"
test "${remote_target}" = "${AUTHORITATIVE_PARENT}"
test -z "$(git ls-remote origin "refs/heads/${CANDIDATE_BRANCH}")"
git push origin "${final_sha}:refs/heads/${CANDIDATE_BRANCH}"
remote_candidate="$(git ls-remote origin "refs/heads/${CANDIDATE_BRANCH}" | awk '{print $1}')"
test "${remote_candidate}" = "${final_sha}"
printf 'final_sha=%s\n' "${final_sha}" >> "${GITHUB_OUTPUT}"
printf 'final_tree=%s\n' "${final_tree}" >> "${GITHUB_OUTPUT}"
printf '%s\n' "${final_sha}" > "${RUNNER_TEMP}/final-sha.txt"
printf '%s\n' "${final_tree}" > "${RUNNER_TEMP}/final-tree.txt"
printf 'Candidate %s (tree %s) is ready for connector-controlled authoritative publication.\n' "${final_sha}" "${final_tree}" >> "${GITHUB_STEP_SUMMARY}"

say 'Emit candidate materialization evidence'
mkdir -p materialization-evidence
cp "${RUNNER_TEMP}/final-sha.txt" materialization-evidence/commit.txt
cp "${RUNNER_TEMP}/final-tree.txt" materialization-evidence/tree.txt
cp "${RUNNER_TEMP}/canonical-pdfinfo.txt" materialization-evidence/pdfinfo.txt
python - <<'PY'
from pathlib import Path
import hashlib, json, os
sha = Path(os.environ['RUNNER_TEMP'], 'final-sha.txt').read_text().strip()
tree = Path(os.environ['RUNNER_TEMP'], 'final-tree.txt').read_text().strip()
paths = [
    '.github/workflows/afp-post-audit-prop73-repair.yml',
    'docs/publication_program/P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md',
    'docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json',
    'docs/publication_program/THEOREM_REGISTRY.md',
    'docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md',
    'docs/publication_program/p1f_manuscript/P1F_REPRODUCIBILITY_MANIFEST.md',
    'afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_robustness.py',
    'afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_certificate.py',
    'afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_certificate_independent.py',
    'output/pdf/FLAGSHIP_MANUSCRIPT.pdf',
]
records=[]
for name in paths:
    raw=Path(name).read_bytes()
    records.append({'path':name,'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw)})
out={
    'schema_version':1,
    'repository':os.environ['GITHUB_REPOSITORY'],
    'authoritative_parent':os.environ['AUTHORITATIVE_PARENT'],
    'target_branch':os.environ['TARGET_BRANCH'],
    'candidate_branch':os.environ['CANDIDATE_BRANCH'],
    'candidate_commit':sha,
    'candidate_tree':tree,
    'workflow_run_id':os.environ['GITHUB_RUN_ID'],
    'status':'MATERIALIZATION_PASS_AWAITING_AUTHORITATIVE_REF_UPDATE',
    'records':records,
}
Path('materialization-evidence/manifest.json').write_text(json.dumps(out,indent=2)+'\n')
PY
