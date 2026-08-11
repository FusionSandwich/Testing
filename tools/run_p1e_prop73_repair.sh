#!/usr/bin/env bash
set -euo pipefail

: "${EXPECTED_REPOSITORY:=FusionSandwich/Testing}"
: "${REPAIR_BRANCH:=agent/afp-prop73-publication-safe-20260810}"
: "${AUTHORITATIVE_PARENT:=b8912c282a22420e8077c75929b16c7a33d189b2}"
: "${AUTHORITATIVE_TREE:=4c2175463a661ce3f2bb206f0cb7b5038183b2ab}"
: "${PR_BRANCH:=agent/afp-consolidated-p2e-p2f-e60f5c7}"
: "${GIT_NO_REPLACE_OBJECTS:=1}"
: "${SOURCE_DATE_EPOCH:=1785900000}"

export GIT_NO_REPLACE_OBJECTS SOURCE_DATE_EPOCH
OUT="${RUNNER_TEMP}/afp-prop73-validation"
mkdir -p "${OUT}"

require_line() {
  local line=$1 file=$2
  grep -Fxq "${line}" "${file}"
}

run_expect() {
  local label=$1 script=$2 expected=$3
  python "${script}" | tee "${OUT}/${label}.log"
  require_line "${expected}" "${OUT}/${label}.log"
}

pre_lean() {
  test "${GITHUB_REPOSITORY}" = "${EXPECTED_REPOSITORY}"
  test "${GITHUB_REF_NAME}" = "${REPAIR_BRANCH}"
  local start_head pr_head migration_head
  start_head=$(git rev-parse HEAD)
  test "${start_head}" = "${GITHUB_SHA}"
  test "$(git rev-parse "${AUTHORITATIVE_PARENT}^{tree}")" = "${AUTHORITATIVE_TREE}"
  git merge-base --is-ancestor "${AUTHORITATIVE_PARENT}" "${start_head}"
  test "$(git rev-list --count --merges "${AUTHORITATIVE_PARENT}..${start_head}")" -eq 0
  pr_head=$(git ls-remote --exit-code --heads origin "refs/heads/${PR_BRANCH}" | awk 'NR==1 {print $1}')
  test "${pr_head}" = "${AUTHORITATIVE_PARENT}"
  git ls-remote --heads origin | grep -v "refs/heads/${REPAIR_BRANCH}$" | LC_ALL=C sort > "${OUT}/heads-before.txt"
  git ls-remote --tags origin | LC_ALL=C sort > "${OUT}/tags-before.txt"
  printf 'repository=%s\nbranch=%s\nstart_head=%s\nauthoritative_parent=%s\nauthoritative_tree=%s\npr_branch=%s\npr_head=%s\nrun=%s\nattempt=%s\n' \
    "${GITHUB_REPOSITORY}" "${REPAIR_BRANCH}" "${start_head}" \
    "${AUTHORITATIVE_PARENT}" "${AUTHORITATIVE_TREE}" "${PR_BRANCH}" \
    "${pr_head}" "${GITHUB_RUN_ID}" "${GITHUB_RUN_ATTEMPT}" \
    | tee "${OUT}/provenance-before.txt"

  export PYTHONPYCACHEPREFIX="${RUNNER_TEMP}/afp-prop73-pycache"
  echo "PYTHONPYCACHEPREFIX=${PYTHONPYCACHEPREFIX}" >> "${GITHUB_ENV}"
  echo "START_HEAD=${start_head}" >> "${GITHUB_ENV}"
  if [[ -f docs/publication_program/P1E_PROP73_REPAIR_REPORT.md ]]; then
    echo 'INITIAL_FINALIZE=0' >> "${GITHUB_ENV}"
  else
    echo 'INITIAL_FINALIZE=1' >> "${GITHUB_ENV}"
  fi
  git config user.name 'afp-repair-bot'
  git config user.email 'afp-repair-bot@users.noreply.github.com'

  sudo apt-get update -qq
  sudo apt-get install --no-install-recommends -y \
    lmodern pandoc poppler-utils ripgrep texlive-fonts-recommended \
    texlive-xetex texlive-latex-extra | tee "${OUT}/apt.log"
  python -m pip install --disable-pip-version-check --no-input \
    'matplotlib==3.10.8' 'numpy==2.3.2' 'sympy==1.14.0' \
    'mpmath==1.3.0' | tee "${OUT}/pip.log"
  python --version | tee "${OUT}/python-version.log"
  python -m pip freeze | LC_ALL=C sort | tee "${OUT}/pip-freeze.log"
  pandoc --version | head -n 2 | tee "${OUT}/pandoc-version.log"
  xelatex --version | head -n 1 | tee "${OUT}/xelatex-version.log"
  pdftotext -v 2>&1 | head -n 1 | tee "${OUT}/poppler-version.log"

  python tools/prepare_p1e_outcome_b.py --root . | tee "${OUT}/preparation.log"
  python tools/apply_p1e_outcome_b.py --root . | tee "${OUT}/migration.log"
  git diff --check
  python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py \
    --root . | tee "${OUT}/fixed-level-contract-precommit.log"
  require_line 'MUTATION_SUITE PASS: 12/12 rejected' "${OUT}/fixed-level-contract-precommit.log"
  require_line 'P1E fixed-level local-persistence audit: PASS' "${OUT}/fixed-level-contract-precommit.log"
  if ! git diff --quiet; then
    git add -A
    git commit -m 'docs: propagate fixed-level persistence theorem'
  fi
  migration_head=$(git rev-parse HEAD)
  echo "MIGRATION_HEAD=${migration_head}" >> "${GITHUB_ENV}"
  python tools/prepare_p1e_outcome_b.py --root . --check | tee "${OUT}/preparation-idempotence.log"
  require_line 'PREPARATION_CHANGED_COUNT 0' "${OUT}/preparation-idempotence.log"
  python tools/apply_p1e_outcome_b.py --root . --check | tee "${OUT}/migration-idempotence.log"
  require_line 'MIGRATION_CHANGED_COUNT 0' "${OUT}/migration-idempotence.log"
  test -z "$(git status --short)"
  printf 'migration_head=%s\n' "${migration_head}" | tee "${OUT}/migration-head.txt"

  pushd afp_barrier_gate1 >/dev/null
  python -m py_compile pure_math/covariance/p1*.py
  run_expect p1e-symbolic pure_math/covariance/p1e_short_gap_symbolic_matrix_audit.py \
    'short-gap literal symbolic matrix-to-limit audit: PASS'
  run_expect p1e-cauchy pure_math/covariance/p1e_short_gap_cauchy_guard_audit.py \
    'short-gap rational Cauchy all-orders guard: PASS'
  run_expect p1e-cauchy-hostile pure_math/covariance/p1e_short_gap_cauchy_hostile_audit.py \
    'short-gap hostile Cauchy/first-row audit: ACCEPT'
  run_expect p1e-polar pure_math/covariance/p1e_short_gap_polar_guard_audit.py \
    'short-gap first-polar-row Cauchy guard: PASS'
  run_expect p1e-proof pure_math/covariance/p1e_short_gap_proof_audit.py \
    'short-gap exact algebra audit: PASS (remainder is certified by the Cauchy guard audit)'
  run_expect p1e-independent pure_math/covariance/p1e_no_guard_ring_independent_audit.py \
    'no-guard ring independent audit: exact regressions PASS'
  require_line 'historical compiler recurrence: NONCERTIFICATE' "${OUT}/p1e-independent.log"
  run_expect p1e-referee pure_math/covariance/p1e_short_gap_referee_audit.py \
    'short-gap hostile referee audit: rejected-mutation regressions PASS'
  run_expect p1e-family pure_math/covariance/p1e_short_gap_family_audit.py \
    'hostile transition and q/h-guard mutations: deterministic failure PASS'
  run_expect p1e-ring pure_math/covariance/p1e_short_gap_ring_audit.py \
    'shortened-gap transition regression audit: PASS'
  run_expect p1e-voronoi pure_math/covariance/p1e_variational_voronoi_audit.py \
    'scale-independent 2/3 quadratic residual blocker: PASS'
  run_expect p1e-icosahedral pure_math/covariance/p1e_icosahedral_cone_audit.py \
    'P1E icosahedral-cone exact cotangent audit: PASS'
  run_expect p1e-icosphere pure_math/covariance/p1e_icosphere_bulk_formula_obstruction_audit.py \
    'p1e icosphere bulk formula obstruction audit: PASS'
  python pure_math/covariance/p1e_stratified_lattice_repair_audit.py | tee "${OUT}/p1e-stratified.log"
  require_line 'P1E stated buffer/pair normalization: REJECTED' "${OUT}/p1e-stratified.log"
  require_line 'P1E stratified global construction: BLOCKED' "${OUT}/p1e-stratified.log"
  python pure_math/covariance/p1e_asymptotic_family_audit.py | tee "${OUT}/p1e-asymptotic.log"
  require_line 'closed-form all-level polygon identities: PASS' "${OUT}/p1e-asymptotic.log"
  require_line 'P1E asymptotic-family deterministic audit: PASS' "${OUT}/p1e-asymptotic.log"
  run_expect p1e-convex pure_math/covariance/p1e_probabilistic_convex_audit.py \
    'P1E probabilistic/convex audit: PASS'
  python pure_math/covariance/p1e_algebraic_product_audit.py | tee "${OUT}/p1e-product.log"
  require_line 'P1E algebraic/product exact identities and blockers: PASS' "${OUT}/p1e-product.log"
  require_line 'P1E algebraic/product all-level construction: BLOCKED' "${OUT}/p1e-product.log"
  run_expect p1d pure_math/covariance/p1d_quantitative_stability_audit.py \
    'P1D quantitative stability audit: PASS'
  run_expect p1c pure_math/covariance/p1c_equality_geometry_audit.py \
    'P1C exact equality-geometry audit: PASS'
  run_expect p1b pure_math/covariance/p1b_sharp_quadratic_defect_audit.py \
    'P1B sharp quadratic-defect audit: PASS'
  run_expect p1a pure_math/covariance/p1a_quadratic_fidelity_audit.py \
    'P1A exact quadratic-fidelity audit: PASS'
  popd >/dev/null

  python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py \
    --root . | tee "${OUT}/fixed-level-contract-final.log"
  require_line 'CONTRACT_ACCEPTED fixed-level existential theorem' "${OUT}/fixed-level-contract-final.log"
  require_line 'MUTATION_SUITE PASS: 12/12 rejected' "${OUT}/fixed-level-contract-final.log"
  require_line 'REPOSITORY_SCOPE PASS' "${OUT}/fixed-level-contract-final.log"
  require_line 'P1E fixed-level local-persistence audit: PASS' "${OUT}/fixed-level-contract-final.log"
  python afp_barrier_gate1/pure_math/covariance/p1e_robustness_claim_inventory.py \
    --root . --report "${OUT}/claim-inventory.json" > "${OUT}/claim-inventory.log"
  git diff --check
  test -z "$(git status --short)"
}

write_validation_log() {
  python - <<'PY'
from __future__ import annotations
import os
import platform
import subprocess
from pathlib import Path

root = Path.cwd()
path = root / "docs/publication_program/P1E_PROP73_VALIDATION_LOG.md"

def output(*args: str) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()

commands = [
    ("Provenance", "git merge-base --is-ancestor $AUTHORITATIVE_PARENT $START_HEAD", "exit 0", "exit 0"),
    ("Preparation", "python tools/prepare_p1e_outcome_b.py --root .", "changes on first application; zero on idempotence rerun", "observed"),
    ("Migration", "python tools/apply_p1e_outcome_b.py --root .", "changes on first application; zero on idempotence rerun", "observed"),
    ("Replacement theorem", "python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py --root .", "12/12 mutations rejected and repository scope PASS", "observed"),
    ("P1E symbolic", "python pure_math/covariance/p1e_short_gap_symbolic_matrix_audit.py", "literal symbolic matrix-to-limit PASS", "observed"),
    ("P1E Cauchy", "python pure_math/covariance/p1e_short_gap_cauchy_guard_audit.py", "rational all-orders guard PASS", "observed"),
    ("P1E hostile Cauchy", "python pure_math/covariance/p1e_short_gap_cauchy_hostile_audit.py", "hostile Cauchy/first-row ACCEPT", "observed"),
    ("P1E polar", "python pure_math/covariance/p1e_short_gap_polar_guard_audit.py", "first-polar-row guard PASS", "observed"),
    ("P1E proof", "python pure_math/covariance/p1e_short_gap_proof_audit.py", "exact algebra audit PASS", "observed"),
    ("P1E independent", "python pure_math/covariance/p1e_no_guard_ring_independent_audit.py", "exact regressions PASS; compiler recurrence NONCERTIFICATE", "observed"),
    ("P1E referee", "python pure_math/covariance/p1e_short_gap_referee_audit.py", "rejected-mutation regressions PASS", "observed"),
    ("P1E family", "python pure_math/covariance/p1e_short_gap_family_audit.py", "hostile transition/guard mutations fail", "observed"),
    ("P1E ring", "python pure_math/covariance/p1e_short_gap_ring_audit.py", "transition regression PASS", "observed"),
    ("P1E rejected routes", "run the variational, icosahedral, icosphere, stratified, asymptotic, convex and algebraic audit scripts", "documented PASS/ACCEPT or explicit REJECTED/BLOCKED", "all exact sentinels observed"),
    ("Retained P1D--P1A", "run p1d_quantitative_stability_audit.py, p1c_equality_geometry_audit.py, p1b_sharp_quadratic_defect_audit.py and p1a_quadratic_fidelity_audit.py", "all four exact PASS sentinels", "observed"),
    ("Lean full build", "cd afp_barrier_gate1 && lake build", "exit 0", "exit 0"),
    ("Lean focused construction", "lake env lean AFPBarrier/QuadraticFidelityConstruction.lean", "exit 0", "exit 0"),
    ("Lean axiom audits", "lake env lean AFPBarrier/AxiomAudit.lean; lake env lean AFPBarrier/PureMathAxiomAudit.lean", "only propext, Classical.choice, Quot.sound", "exact allowed set observed"),
    ("Citation closure", "pandoc FLAGSHIP_MANUSCRIPT.md --from=markdown --standalone --citeproc --bibliography=priority_sources.bib -t native -o /dev/null", "exit 0 and empty warning log", "observed"),
    ("PDF build", "python docs/publication_program/p1f_manuscript/build_flagship_paper.py", "exit 0", "exit 0"),
    ("PDF inspection", "pdfinfo and pdftotext on output/pdf/FLAGSHIP_MANUSCRIPT.pdf", "corrected theorem present; rejected theorem absent", "observed"),
]

pip_freeze = output("python", "-m", "pip", "freeze")
environment = "\n".join([
    f"runner_image={os.environ.get('ImageOS', 'ubuntu-24.04')}",
    f"platform={platform.platform()}",
    output("python", "--version"),
    output("pandoc", "--version").splitlines()[0],
    output("xelatex", "--version").splitlines()[0],
    output("pdftotext", "-v").splitlines()[0],
    output("lean", "--version").splitlines()[0],
    output("lake", "--version").splitlines()[0],
    "SOURCE_DATE_EPOCH=1785900000",
])

lines = [
    "# Proposition 7.3 repair validation command log", "",
    "## Run identity", "",
    f"- repository: `{os.environ['GITHUB_REPOSITORY']}`",
    f"- branch: `{os.environ['REPAIR_BRANCH']}`",
    f"- workflow run: `{os.environ['GITHUB_RUN_ID']}` attempt `{os.environ['GITHUB_RUN_ATTEMPT']}`",
    f"- workflow starting head: `{os.environ['START_HEAD']}`",
    f"- post-migration local head: `{os.environ['MIGRATION_HEAD']}`",
    f"- authoritative parent: `{os.environ['AUTHORITATIVE_PARENT']}`",
    f"- authoritative tree: `{os.environ['AUTHORITATIVE_TREE']}`", "",
    "## Exact environment", "", "```text", environment, "```", "",
    "Pinned Python packages:", "", "```text",
    "\n".join(line for line in pip_freeze.splitlines() if line.lower().startswith(("matplotlib==", "mpmath==", "numpy==", "sympy=="))),
    "```", "", "## Commands, expected outputs, and observed outputs", "",
]
for index, (group, command, expected, observed) in enumerate(commands, 1):
    lines.extend([
        f"{index}. **{group}**",
        f"   - Command: `{command}`",
        f"   - Expected: `{expected}`",
        f"   - Observed: `{observed}`",
    ])
lines.extend([
    "", "## Interpretation boundary", "",
    "The Python and Lean executions are regression, algebra, and formal-scope checks. They do not replace the ordinary all-level unperturbed construction proof or the fixed-level continuity proof. The former scalar compiler recurrence is recorded only as a noncertificate.", "",
])
path.write_text("\n".join(lines), encoding="utf-8")
print(path)
PY
}

post_lean() {
  local paper bib pdf pages final_head final_tree remote_repair observed pr_head

  pushd afp_barrier_gate1 >/dev/null
  lean --version | tee "${OUT}/lean-version.log"
  lake --version | tee "${OUT}/lake-version.log"
  lake update | tee "${OUT}/lake-update.log"
  lake exe cache get | tee "${OUT}/lean-cache.log"
  lake build | tee "${OUT}/lean-build.log"
  lake env lean AFPBarrier/QuadraticFidelityConstruction.lean | tee "${OUT}/lean-construction.log"
  lake env lean AFPBarrier/AxiomAudit.lean | tee "${OUT}/lean-all-axioms.log"
  lake env lean AFPBarrier/PureMathAxiomAudit.lean | tee "${OUT}/lean-pure-axioms.log"
  python - "${OUT}/lean-pure-axioms.log" <<'PY' | tee "${OUT}/lean-axiom-set.log"
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
groups = re.findall(r"depends on axioms:\s*\[(.*?)\]", text, re.S)
if not groups:
    raise SystemExit("focused axiom audit produced no records")
observed = {x.strip() for group in groups for x in group.split(",") if x.strip()}
allowed = {"propext", "Classical.choice", "Quot.sound"}
if observed != allowed:
    raise SystemExit(f"unexpected axioms: {sorted(observed)}")
print("focused axiom dependency set: EXACT", sorted(observed))
PY
  ! rg --glob '*.lean' '(^|[^[:alnum:]_])(sorry|admit|sorryAx)([^[:alnum:]_]|$)' AFPBarrier AFPBarrier.lean
  ! rg --glob '*.lean' '^[[:space:]]*(@\[[^]]*\][[:space:]]*)*((private|protected|noncomputable|unsafe|scoped|local)[[:space:]]+)*(axiom|axioms)([[:space:]]|$)' AFPBarrier AFPBarrier.lean
  ! rg '^[[:space:]]*(@\[[^]]*\][[:space:]]*)*((private|protected|noncomputable|unsafe|scoped|local)[[:space:]]+)*(constant|constants)([[:space:]]|$)' \
    AFPBarrier.lean AFPBarrier/AxiomAudit.lean AFPBarrier/PureMathAxiomAudit.lean \
    AFPBarrier/QuadraticFidelityFoundation.lean AFPBarrier/QuadraticFidelityLowerBound.lean \
    AFPBarrier/QuadraticEqualityGeometry.lean AFPBarrier/QuadraticFidelityStability.lean \
    AFPBarrier/QuadraticFidelityConstruction.lean
  popd >/dev/null
  git diff --check
  test -z "$(git status --short)"

  paper=docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md
  bib=docs/publication_program/p1f_manuscript/priority_sources.bib
  test "$(head -n 1 "${paper}")" = '# A sharp positivity--rate frontier for quadratic fidelity of reversible spherical generators'
  ! sed -n '1,90p' "${paper}" | rg -i '\bAFP\b'
  ! rg 'P1E_SHORT_GAP_S2_CANDIDATE_THEOREM|STATUS_PENDING|construction[^\n]*BLOCKED' "${paper}"
  ! rg 'structured support-preserving robustness|straight-line differentiation|K_\\\*|R_rob|C_rob|h\^3/K' "${paper}"
  rg -Fq '### Proposition 7.3 (fixed-level local persistence)' "${paper}"
  rg -Fq 'existential and may depend on $J$' "${paper}"
  rg -Fq 'P1E-LOCAL-PERSIST' "${paper}"
  for heading in \
    '## Abstract' '## 1. Introduction' '## Appendix A. Proof dependency graph' \
    '## Appendix B. Theorem-to-source-to-test-to-registry map' \
    '## Appendix C. Numerical and falsification protocol' '## Appendix D. Formalization' \
    '## Appendix E. Reproducibility record' '## Appendix F. Limitations and future work' \
    '## Appendix G. Related-theorem and hypothesis-transfer matrix'; do
    rg -Fxq "${heading}" "${paper}"
  done
  python - "${paper}" "${bib}" <<'PY' | tee "${OUT}/citation-map.log"
import re, sys
paper = open(sys.argv[1], encoding="utf-8").read()
bib = open(sys.argv[2], encoding="utf-8").read()
cited = set(re.findall(r"@([A-Za-z0-9_:.+-]+)", paper))
records = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bib, re.M))
if cited != records:
    raise SystemExit(f"citation mismatch: uncited={sorted(records-cited)} missing={sorted(cited-records)}")
required = {"P1A-QUOT", "P1A-2DEF", "P1B-SHARP", "P1B-EQUALITY", "P1C-LOCAL", "P1C-GLOBAL", "P1D-MASTER", "P1D-QUOTIENT", "P1E-POLYGON", "P1E-RING", "P1E-ROW", "P1E-LOCAL-PERSIST", "F-CONSTRUCT"}
missing = sorted(x for x in required if x not in paper)
if missing:
    raise SystemExit(f"source-map registry keys missing: {missing}")
print(f"citation keys EXACT: {len(cited)}; corrected source-map keys EXACT")
PY
  pandoc "${paper}" --from=markdown --standalone --citeproc \
    --bibliography="${bib}" -t native -o /dev/null 2>"${OUT}/pandoc-warnings.log"
  test ! -s "${OUT}/pandoc-warnings.log"

  pdf=output/pdf/FLAGSHIP_MANUSCRIPT.pdf
  python docs/publication_program/p1f_manuscript/build_flagship_paper.py | tee "${OUT}/pdf-build.log"
  pdfinfo "${pdf}" | tee "${OUT}/pdfinfo.log"
  pdftotext "${pdf}" "${OUT}/flagship.txt"
  pages=$(awk '/^Pages:/ {print $2}' "${OUT}/pdfinfo.log")
  test "${pages}" -ge 20 && test "${pages}" -le 35
  grep -Fq 'Title:           A sharp positivity--rate frontier for quadratic fidelity of reversible spherical generators' "${OUT}/pdfinfo.log"
  ! rg '\[@|Citation|P1E_SHORT_GAP_S2_CANDIDATE|mermaid' "${OUT}/flagship.txt"
  ! rg -i 'structured support-preserving robustness|straight-line differentiation|support-preserving robustness with' "${OUT}/flagship.txt"
  rg -Fq 'fixed-level local persistence' "${OUT}/flagship.txt"
  rg -Fq 'existential and may depend on' "${OUT}/flagship.txt"
  rg -Fq 'Izmestiev' "${OUT}/flagship.txt"
  rg -Fq 'Benedetto' "${OUT}/flagship.txt"
  sha256sum "${pdf}" "${paper}" "${bib}" \
    docs/publication_program/p1f_manuscript/proof_dependency_graph.png \
    | tee "${OUT}/publication-files.sha256"
  rm -rf tmp/pdfs/p1f-build
  git diff --check

  if [[ "${INITIAL_FINALIZE}" = 1 ]]; then
    write_validation_log
    python tools/finalize_p1e_repair.py \
      --root . --base "${AUTHORITATIVE_PARENT}" --tree "${AUTHORITATIVE_TREE}" \
      --branch "${REPAIR_BRANCH}" --run-id "${GITHUB_RUN_ID}" \
      --start-head "${START_HEAD}" | tee "${OUT}/finalizer.log"
  fi

  python tools/prepare_p1e_outcome_b.py --root . --check | tee "${OUT}/final-preparation-check.log"
  require_line 'PREPARATION_CHANGED_COUNT 0' "${OUT}/final-preparation-check.log"
  python tools/apply_p1e_outcome_b.py --root . --check | tee "${OUT}/final-migration-check.log"
  require_line 'MIGRATION_CHANGED_COUNT 0' "${OUT}/final-migration-check.log"
  python afp_barrier_gate1/pure_math/covariance/p1e_fixed_level_persistence_audit.py \
    --root . | tee "${OUT}/final-contract-check.log"
  require_line 'P1E fixed-level local-persistence audit: PASS' "${OUT}/final-contract-check.log"
  test -f docs/publication_program/P1E_PROP73_REPAIR_REPORT.md
  test -f docs/publication_program/P1E_PROP73_VALIDATION_LOG.md
  test -f docs/publication_program/p1f_manuscript/P1F_REPRODUCIBILITY_MANIFEST.md
  python - <<'PY' | tee "${OUT}/manifest-hash-check.log"
import hashlib
import importlib.util
from pathlib import Path
root = Path.cwd()
spec = importlib.util.spec_from_file_location("finalizer", root / "tools/finalize_p1e_repair.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
manifest = (root / module.MANIFEST).read_text(encoding="utf-8")
for relative in module.HASH_PATHS:
    digest = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    if f"| `{relative}` | `{digest}` |" not in manifest:
        raise SystemExit(f"manifest hash mismatch: {relative} {digest}")
print(f"manifest hash table EXACT: {len(module.HASH_PATHS)} files")
PY
  ! rg 'structured support-preserving robustness|straight-line differentiation|K_\\\*|R_rob|C_rob|h\^3/K' \
    docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md \
    docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md \
    docs/publication_program/THEOREM_REGISTRY.md \
    docs/publication_program/APPROACH_REGISTRY.md \
    docs/publication_program/P1E_APPROACH_REGISTRY.md \
    docs/publication_program/PAPER_BOUNDARY_MATRIX.md
  rg -Fq 'HISTORICAL / REJECTED CLAIM — NOT AN ACCEPTED THEOREM' \
    docs/publication_program/P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md
  rg -Fq '| P1E-LOCAL-PERSIST | PROVED |' docs/publication_program/THEOREM_REGISTRY.md
  test "$(git rev-list --count --merges "${AUTHORITATIVE_PARENT}..HEAD")" -eq 0
  git merge-base --is-ancestor "${AUTHORITATIVE_PARENT}" HEAD
  git diff --check "${AUTHORITATIVE_PARENT}" HEAD
  rm -rf tmp/pdfs/p1f-build
  (cd "${OUT}" && find . -maxdepth 1 -type f ! -name records.sha256 -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > records.sha256)
  if ! git diff --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
    git add -A
    git commit -m 'repro: rebuild corrected flagship and record validation'
  fi
  test -z "$(git status --short)"
  final_head=$(git rev-parse HEAD)
  final_tree=$(git rev-parse HEAD^{tree})
  printf 'final_head=%s\nfinal_tree=%s\n' "${final_head}" "${final_tree}" | tee "${OUT}/final-object.txt"

  remote_repair=$(git ls-remote --exit-code --heads origin "refs/heads/${REPAIR_BRANCH}" | awk 'NR==1 {print $1}')
  test "${remote_repair}" = "${START_HEAD}"
  git push origin "HEAD:refs/heads/${REPAIR_BRANCH}" | tee "${OUT}/push.log"
  observed=$(git ls-remote --exit-code --heads origin "refs/heads/${REPAIR_BRANCH}" | awk 'NR==1 {print $1}')
  test "${observed}" = "${final_head}"
  git ls-remote --heads origin | grep -v "refs/heads/${REPAIR_BRANCH}$" | LC_ALL=C sort > "${OUT}/heads-after.txt"
  git ls-remote --tags origin | LC_ALL=C sort > "${OUT}/tags-after.txt"
  diff -u "${OUT}/heads-before.txt" "${OUT}/heads-after.txt" | tee "${OUT}/nonrepair-heads.diff"
  diff -u "${OUT}/tags-before.txt" "${OUT}/tags-after.txt" | tee "${OUT}/tags.diff"
  pr_head=$(git ls-remote --exit-code --heads origin "refs/heads/${PR_BRANCH}" | awk 'NR==1 {print $1}')
  test "${pr_head}" = "${AUTHORITATIVE_PARENT}"
  test "$(git rev-list --count --merges "${AUTHORITATIVE_PARENT}..${final_head}")" -eq 0
  printf 'remote_repair=%s\nfinal_tree=%s\npr_head_unchanged=%s\nnonrepair_heads=UNCHANGED\ntags=UNCHANGED\n' \
    "${observed}" "${final_tree}" "${pr_head}" | tee "${OUT}/post-push-provenance.txt"
}

case "${1:-}" in
  pre) pre_lean ;;
  post) post_lean ;;
  *) echo "usage: $0 {pre|post}" >&2; exit 2 ;;
esac
