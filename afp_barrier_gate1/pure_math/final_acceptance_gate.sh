#!/usr/bin/env bash
set -euo pipefail

ROOT=$(git rev-parse --show-toplevel)
BASE_SHA=94aebf6578a43516cce4bb7c042fc57681c93890
BASE_TREE=872828f5099aeb7df4e0ab871b9e881de4054a97
SOURCE_SHA=19a5001158cb40fbb0adc92813cc3abd5dfa583d
ARCHIVE_SHA=515f1aae6c20bd85711c90b5c1c21b4905252d01
EXPECTED_HEAD=${GITHUB_SHA:-$(git -C "$ROOT" rev-parse HEAD)}
GATE_NAME=${GATE_NAME:-local-final-acceptance}
GATE_SLUG=$(printf '%s' "$GATE_NAME" | tr '[:upper:] /' '[:lower:]--' | tr -cd '[:alnum:]_.-')
EVIDENCE_DIR=${RUNNER_TEMP:-/tmp}/afp-final-${GITHUB_RUN_ID:-local}-${GITHUB_RUN_ATTEMPT:-1}-${GATE_SLUG}
mkdir -p "$EVIDENCE_DIR"
if [[ -n ${GITHUB_OUTPUT:-} ]]; then
  printf 'evidence_dir=%s\n' "$EVIDENCE_DIR" >> "$GITHUB_OUTPUT"
fi
exec > >(tee "$EVIDENCE_DIR/final-gate.log") 2>&1

fail() {
  echo "FINAL ACCEPTANCE FAILURE: $*" >&2
  exit 1
}

run_logged() {
  local name=$1
  shift
  echo "::group::$name"
  "$@" 2>&1 | tee "$EVIDENCE_DIR/${name}.log"
  echo "::endgroup::"
}

actual_head=$(git -C "$ROOT" rev-parse HEAD)
actual_tree=$(git -C "$ROOT" show -s --format=%T HEAD)
test "$actual_head" = "$EXPECTED_HEAD" || fail "checkout $actual_head != event head $EXPECTED_HEAD"
git -C "$ROOT" merge-base --is-ancestor "$BASE_SHA" HEAD || fail "accepted target is not an ancestor"
git -C "$ROOT" merge-base --is-ancestor "$SOURCE_SHA" HEAD || fail "PR #30 source is not an ancestor"
test "$(git -C "$ROOT" show -s --format=%T "$BASE_SHA")" = "$BASE_TREE" || fail "starting target tree changed"
git -C "$ROOT" fetch --no-tags origin archive/afp-gate6-spatial-multigroup-verified
test "$(git -C "$ROOT" rev-parse FETCH_HEAD)" = "$ARCHIVE_SHA" || fail "immutable archive moved"

cat > "$EVIDENCE_DIR/provenance.txt" <<EOF
workflow=$GATE_NAME
expected_head=$EXPECTED_HEAD
actual_head=$actual_head
actual_tree=$actual_tree
starting_target=$BASE_SHA
starting_target_tree=$BASE_TREE
source_pr30=$SOURCE_SHA
archive=$ARCHIVE_SHA
run_id=${GITHUB_RUN_ID:-local}
run_attempt=${GITHUB_RUN_ATTEMPT:-1}
event=${GITHUB_EVENT_NAME:-local}
ref=${GITHUB_REF:-local}
EOF

records=(
  afp_barrier_gate1/docs/FINAL_PURE_MATH_ACCEPTANCE.md
  afp_barrier_gate1/docs/PROMPT3_FINAL_INTEGRATION_RECORD.md
  afp_barrier_gate1/docs/PROMPT4_REACCEPTANCE_AFTER_P3_RECONCILIATION.md
  afp_barrier_gate1/docs/P3_P4_APPROACH_REGISTRY.md
  afp_barrier_gate1/docs/P3_P4_BRANCH_PRESERVATION_REGISTRY.md
  afp_barrier_gate1/docs/P3_P4_THEOREM_AND_HYPOTHESIS_REGISTRY.md
)
for record in "${records[@]}"; do
  test -s "$ROOT/$record" || fail "missing acceptance record: $record"
done

allowed='^(\.github/workflows/(afp-global-rigidity|afp-prompt3-rigidity|afp-prompt4-sharp-barriers|afp-pure-math|afp-quadratic-covariance|afp-spherical-feasibility)\.yml|afp_barrier_gate1/AFPBarrier(\.lean|/.*\.lean)|afp_barrier_gate1/pure_math/.*|afp_barrier_gate1/docs/.*)$'
bad_scope=$(git -C "$ROOT" diff --name-only "$BASE_SHA"...HEAD | grep -Ev "$allowed" || true)
test -z "$bad_scope" || fail "out-of-scope paths:\n$bad_scope"
printf '%s\n' "$(git -C "$ROOT" diff --name-only "$BASE_SHA"...HEAD)" > "$EVIDENCE_DIR/changed-paths.txt"

forbidden=$(git -C "$ROOT" ls-files | grep -E '(^|/)(__pycache__/|.*\.pyc$|\.github/.*\.b64$|afp-p3-p4-materialize\.yml$|afp-p3-p4-targeted-lean\.yml$|prompt3-triangulations-through-12\.jsonl$|(^|/)plantri$|(^|/)_lean4export/|(^|/)_nanoda_lib/)' || true)
test -z "$forbidden" || fail "forbidden tracked artifacts:\n$forbidden"

cd "$ROOT/afp_barrier_gate1"
python -m pip install --disable-pip-version-check --no-input \
  'mpmath==1.3.0' 'numpy==2.3.2' 'sympy==1.14.0' 'networkx==3.5' \
  2>&1 | tee "$EVIDENCE_DIR/python-dependencies.log"

run_logged python-compile python -m compileall -q pure_math
run_logged prompt1-falsification python pure_math/falsification/claim_falsification_audit.py
run_logged prompt1-local-global python pure_math/examples/exact_local_global_audit.py
run_logged spherical-feasibility python pure_math/tests/test_spherical_feasibility.py
run_logged prompt2-covariance python pure_math/covariance/quadratic_covariance_audit.py
run_logged prompt2-closeout python pure_math/covariance/prompt2_closeout_audit.py
run_logged prompt3-plantri env P3_REQUIRE_PLANTRI=1 python \
  pure_math/rigidity/triangulation_counterexample_audit.py \
  --require-plantri --catalog "$EVIDENCE_DIR/prompt3-triangulations-through-12.jsonl"
test "$(wc -l < "$EVIDENCE_DIR/prompt3-triangulations-through-12.jsonl")" -eq 9150 \
  || fail "plantri catalog does not contain 9150 records"
run_logged prompt3-near-rigidity python pure_math/rigidity/global_near_rigidity_audit.py
run_logged prompt3-covariance python pure_math/rigidity/q1_covariance_audit.py
run_logged prompt4-sharp-barriers python pure_math/barriers/prompt4_sharp_barrier_audit.py

fixture_dir=$(mktemp -d)
trap 'rm -rf "$fixture_dir"; rm -rf "$ROOT/afp_barrier_gate1/_lean4export" "$ROOT/afp_barrier_gate1/_nanoda_lib"; rm -f "$ROOT/afp_barrier_gate1/_nanoda_export.txt" "$ROOT/afp_barrier_gate1/_nanoda_config.json"' EXIT
printf 'axiom forbidden : Prop\n' > "$fixture_dir/singular.lean"
printf 'axioms forbidden1 forbidden2 : Prop\n' > "$fixture_dir/plural.lean"
printf '#print axioms Existing.theorem\ntheorem axiomName : True := by trivial\n' > "$fixture_dir/allowed.lean"
pattern='^[[:space:]]*(axiom|axioms)([[:space:]]|$)'
grep -qE "$pattern" "$fixture_dir/singular.lean"
grep -qE "$pattern" "$fixture_dir/plural.lean"
! grep -qE "$pattern" "$fixture_dir/allowed.lean"

if grep -RInE --include='*.lean' '(^|[^[:alnum:]_])(sorry|admit|sorryAx)([^[:alnum:]_]|$)' AFPBarrier AFPBarrier.lean; then
  fail "forbidden proof placeholder found"
fi
if grep -RInE --include='*.lean' '^[[:space:]]*(axiom|axioms)([[:space:]]|$)' AFPBarrier AFPBarrier.lean; then
  fail "user-declared axiom found"
fi
printf 'placeholder and singular/plural user-axiom scans: PASS\n' | tee "$EVIDENCE_DIR/source-policy.log"

run_logged lake-update lake update
run_logged mathlib-cache lake exe cache get
run_logged lean-quantitative lake env lean ./AFPBarrier/QuantitativeGlobalNearRigidity.lean
run_logged lean-spherical-equality lake env lean ./AFPBarrier/SphericalQEqualityRigidity.lean
run_logged lean-q-covariance lake env lean ./AFPBarrier/QEqualityCovariance.lean
run_logged lean-sharp-barriers lake env lean ./AFPBarrier/SharpProductBarriers.lean
run_logged lean-full-build lake build
run_logged lean-axiom-audit lake env lean ./AFPBarrier/PureMathAxiomAudit.lean
if grep -q 'sorryAx' "$EVIDENCE_DIR/lean-axiom-audit.log"; then
  fail "focused axiom report contains sorryAx"
fi

rm -rf _lean4export _nanoda_lib
rm -f _nanoda_export.txt _nanoda_config.json
if ! command -v cargo >/dev/null 2>&1; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal
  # shellcheck disable=SC1090
  source "$HOME/.cargo/env"
fi

git init -q _lean4export
git -C _lean4export remote add origin https://github.com/ammkrn/lean4export.git
git -C _lean4export fetch --depth 1 origin f3cf6458a309d643dc586a80f9ab5a93c2304db9
git -C _lean4export checkout --detach FETCH_HEAD
python3 - <<'PY'
from pathlib import Path
path = Path('_lean4export/Export.lean')
source = path.read_text(encoding='utf-8')
old = 'e.updateLet! (← removeMData d) (← removeMData v) (← removeMData b)'
new = old + ' false'
if source.count(old) != 1:
    raise SystemExit('Unexpected Lean exporter let-expression source')
path.write_text(source.replace(old, new), encoding='utf-8')
PY
cp lean-toolchain _lean4export/
run_logged lean4export-build bash -lc 'cd _lean4export && lake build'

git init -q _nanoda_lib
git -C _nanoda_lib remote add origin https://github.com/ammkrn/nanoda_lib.git
git -C _nanoda_lib fetch --depth 1 origin e5438ac0a85a036b6dfe093aa457bc3448498014
git -C _nanoda_lib checkout --detach FETCH_HEAD
run_logged nanoda-build bash -lc 'cd _nanoda_lib && cargo build --release'

modules=(
  AFPBarrier.LocalSphericalFeasibility
  AFPBarrier.QuadraticCovariance
  AFPBarrier.GlobalLossRigidity
  AFPBarrier.SphericalQOneRigidity
  AFPBarrier.SharpProductBarriers
  AFPBarrier.SphericalQEqualityRigidity
  AFPBarrier.QuantitativeGlobalNearRigidity
  AFPBarrier.QEqualityCovariance
)
foundations=(
  Nat Nat.zero Nat.succ
  List List.nil List.cons
  String String.mk Char Char.ofNat
)
declarations=(
  AFPBarrier.jumpGenerator_product_identity
  AFPBarrier.jumpGenerator_quadratic_covariance_identity
  AFPBarrier.finiteMatrixContraction_tracelessProjection
  AFPBarrier.sampledRestriction_finrank
  AFPBarrier.samplingKernel_le_residualKernel
  AFPBarrier.rate_eq_of_symmetric_active_loss
  AFPBarrier.connected_active_loss_rigidity
  AFPBarrier.squarePolarQualityFromStep_formula
  AFPBarrier.squarePolar_rates_forced
  AFPBarrier.squarePolar_totalRate_forced
  AFPBarrier.cscSquaredTruncation_rate_identity
  AFPBarrier.squarePolarRateMainStep_grid
  AFPBarrier.squarePolarQualityMainStep_grid
  AFPBarrier.universal_rate_lower_of_defect_upper
  AFPBarrier.finiteExtremal_defect_lower
  AFPBarrier.twoLossQuality_sub_one
  AFPBarrier.biregular_interRing_incidence
  AFPBarrier.perfectMatching_ringCounts_eq
  AFPBarrier.jumpRate_pos_of_lossMoment_two
  AFPBarrier.normalizedEdgeWeight_sum_one
  AFPBarrier.normalizedLossScale_mean_one
  AFPBarrier.normalizedLossScale_secondMoment
  AFPBarrier.weightedSecondMoment_sub_one_eq_variance
  AFPBarrier.sphericalQ_sub_one_eq_normalizedLossVariance
  AFPBarrier.sphericalQ_eq_one_active_loss
  AFPBarrier.active_symmetric_of_shared_conductance
  AFPBarrier.connected_spherical_active_loss_rigidity
  AFPBarrier.weight_floor_mul_deviation_sq_le
  AFPBarrier.pointwise_deviation_sq_le_eta_div_kappa
  AFPBarrier.pointwise_delta_bound
  AFPBarrier.adjacent_rate_cross_bounds
  AFPBarrier.adjacent_rate_ratio_bounds
  AFPBarrier.incident_loss_cross_bounds
  AFPBarrier.radial_covariance_error_identity
  AFPBarrier.radial_covariance_error_bounds
  AFPBarrier.covarianceTrace_eq_four_of_normLoss
  AFPBarrier.radialCovariance_eq_sphericalEpsilon
  AFPBarrier.sphericalEpsilon_eq_four_mul_Q_div_rate
  AFPBarrier.weighted_centered_affine_product_sum
  AFPBarrier.qOne_covarianceEntry_decomposition
  AFPBarrier.qOne_tangent_entry_isotropic_iff
  AFPBarrier.qOne_antipodal_tangent_coefficient_zero
  AFPBarrier.qOne_antipodal_covarianceEntry
  AFPBarrier.weightedOctahedron_tangentWeights_sum_one
  AFPBarrier.weightedOctahedron_axis_axial_iff
)
lake env _lean4export/.lake/build/bin/lean4export \
  "${modules[@]}" -- "${foundations[@]}" "${declarations[@]}" \
  > _nanoda_export.txt
test -s _nanoda_export.txt || fail "lean4export produced no output"
cat > _nanoda_config.json <<'JSON'
{
  "export_file_path": "_nanoda_export.txt",
  "use_stdin": false,
  "permitted_axioms": [
    "propext",
    "Classical.choice",
    "Quot.sound",
    "Lean.trustCompiler"
  ],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true,
  "string_extension": true,
  "print_success_message": true
}
JSON
run_logged nanoda-check env RUST_BACKTRACE=1 _nanoda_lib/target/release/nanoda_bin _nanoda_config.json

rm -rf _lean4export _nanoda_lib
rm -f _nanoda_export.txt _nanoda_config.json
find pure_math -type d -name __pycache__ -prune -exec rm -rf {} +
find pure_math -type f -name '*.pyc' -delete

git -C "$ROOT" diff --check "$BASE_SHA"...HEAD
test -z "$(git -C "$ROOT" status --porcelain)" || fail "verification left a dirty worktree"

cat > "$EVIDENCE_DIR/checkpoint.txt" <<EOF
AFP Prompt 3-4 final acceptance checkpoint
workflow=$GATE_NAME
commit=$actual_head
tree=$actual_tree
run_id=${GITHUB_RUN_ID:-local}
run_attempt=${GITHUB_RUN_ATTEMPT:-1}
toolchain=$(cat lean-toolchain)
plantri_maps=9150
archive=$ARCHIVE_SHA
timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
result=PASS
EOF
(
  cd "$EVIDENCE_DIR"
  find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)
echo "FINAL ACCEPTANCE GATE: PASS"
