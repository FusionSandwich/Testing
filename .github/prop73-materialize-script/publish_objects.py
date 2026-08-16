from __future__ import annotations

from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import urllib.error
import urllib.request

repo = os.environ["GITHUB_REPOSITORY"]
api_root = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
token = os.environ["GH_TOKEN"]
parent = os.environ["AUTHORITATIVE_PARENT"]
parent_tree = os.environ["AUTHORITATIVE_PARENT_TREE"]
expected_tree = os.environ["LOCAL_FINAL_TREE"]
runner_temp = Path(os.environ["RUNNER_TEMP"])
manifest_path = Path("docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
paths = manifest["affected_paths"]
assert len(paths) == 35 and len(paths) == len(set(paths))

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "afp-prop73-exact-materializer",
}


def request(endpoint: str, payload: dict | None = None) -> dict:
    url = f"{api_root}/repos/{repo}{endpoint}"
    data = None if payload is None else json.dumps(payload, separators=(",", ":")).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {exc.code} for {endpoint}: {detail}") from exc


entries: list[dict[str, str]] = []
for index, name in enumerate(paths, start=1):
    raw = Path(name).read_bytes()
    blob = request(
        "/git/blobs",
        {"content": base64.b64encode(raw).decode("ascii"), "encoding": "base64"},
    )
    sha = blob["sha"]
    entries.append({"path": name, "mode": "100644", "type": "blob", "sha": sha})
    print(f"REMOTE_BLOB_PASS {index:02d}/{len(paths):02d} {name} {sha}")

tree = request("/git/trees", {"base_tree": parent_tree, "tree": entries})
final_tree = tree["sha"]
assert final_tree == expected_tree, (final_tree, expected_tree)
commit = request(
    "/git/commits",
    {
        "message": "Repair Proposition 7.3 with fixed-level support robustness",
        "tree": final_tree,
        "parents": [parent],
        "author": {
            "name": "github-actions[bot]",
            "email": "41898282+github-actions[bot]@users.noreply.github.com",
            "date": "2026-08-16T07:45:00Z",
        },
        "committer": {
            "name": "github-actions[bot]",
            "email": "41898282+github-actions[bot]@users.noreply.github.com",
            "date": "2026-08-16T07:45:00Z",
        },
    },
)
final_sha = commit["sha"]
remote = request(f"/git/commits/{final_sha}")
assert remote["tree"]["sha"] == final_tree
assert [p["sha"] for p in remote["parents"]] == [parent]

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
    out.write(f"final_sha={final_sha}\nfinal_tree={final_tree}\n")
with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as out:
    out.write(
        f"Remote commit object `{final_sha}` (tree `{final_tree}`) is ready for "
        "connector-controlled authoritative publication.\n"
    )

evidence = Path("materialization-evidence")
evidence.mkdir(exist_ok=True)
(evidence / "commit.txt").write_text(final_sha + "\n")
(evidence / "tree.txt").write_text(final_tree + "\n")
shutil.copyfile(runner_temp / "canonical-pdfinfo.txt", evidence / "pdfinfo.txt")
key_paths = [
    ".github/workflows/afp-post-audit-prop73-repair.yml",
    "docs/publication_program/P1E_FIXED_SUPPORT_ROBUSTNESS_THEOREM.md",
    "docs/publication_program/P1E_ROBUSTNESS_REPAIR_MANIFEST.json",
    "docs/publication_program/THEOREM_REGISTRY.md",
    "docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md",
    "docs/publication_program/p1f_manuscript/P1F_REPRODUCIBILITY_MANIFEST.md",
    "afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_robustness.py",
    "afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_certificate.py",
    "afp_barrier_gate1/pure_math/covariance/p1e_fixed_support_certificate_independent.py",
    "output/pdf/FLAGSHIP_MANUSCRIPT.pdf",
]
records = []
for name in key_paths:
    raw = Path(name).read_bytes()
    records.append({"path": name, "sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)})
(evidence / "manifest.json").write_text(
    json.dumps(
        {
            "schema_version": 1,
            "repository": repo,
            "authoritative_parent": parent,
            "target_branch": os.environ["TARGET_BRANCH"],
            "candidate_commit": final_sha,
            "candidate_tree": final_tree,
            "workflow_run_id": os.environ["GITHUB_RUN_ID"],
            "status": "REMOTE_GIT_OBJECTS_CREATED_AWAITING_AUTHORITATIVE_REF_UPDATE",
            "records": records,
        },
        indent=2,
    )
    + "\n"
)
print("REMOTE_COMMIT_OBJECT_PASS", final_sha)
print("REMOTE_TREE_OBJECT_PASS", final_tree)
