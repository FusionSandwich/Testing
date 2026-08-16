# Formal and release audit

## Verdict

**Formal-source verdict: ACCEPT for the finite (d=3) construction identity
surface.**  Static inspection found no likely name-resolution, import-cycle,
division, or theorem-scope defect in
`AFPBarrier/QuadraticFidelityConstruction.lean`.  The aggregate library imports
the module, and both public axiom-audit surfaces now enumerate all seventeen
construction theorems.

**Deterministic P1E verdict: ACCEPT.**  Every noninteractive P1E audit was
byte-compiled and run successfully.  The direct-frequency LP program was
byte-compiled but was not treated as a theorem audit: its own module docstring
labels it exploratory, and its command-line interface requires a user-selected
frequency.

**Pinned release verdict: ACCEPT.**  The literal P1E release commit was checked
in the pinned Lean 4.30/Mathlib 4.30 environment after the local static audit.
The full aggregate build, focused construction elaboration, general axiom
audit, and focused pure-mathematics axiom audit all passed.  The focused audit
reported exactly the allowed foundational dependency set
`{propext, Classical.choice, Quot.sound}` and no `sorryAx`.

This acceptance covers the finite formal identities described below.  It does
not upgrade the ordinary analytic mesh proof, Cauchy enclosure, or global
recurrence to machine-checked status.

## 1. Files audited

- `afp_barrier_gate1/AFPBarrier/QuadraticFidelityConstruction.lean`;
- `afp_barrier_gate1/AFPBarrier.lean`;
- `afp_barrier_gate1/AFPBarrier/AxiomAudit.lean`;
- `afp_barrier_gate1/AFPBarrier/PureMathAxiomAudit.lean`;
- `afp_barrier_gate1/lakefile.lean`, `lean-toolchain`, and
  `lake-manifest.json`;
- all `afp_barrier_gate1/pure_math/covariance/p1e*.py` programs.

The toolchain pin is Lean `v4.30.0`, and the Lake file pins Mathlib
`v4.30.0`.

## 2. Minimal formal fixes

Three narrow fixes were justified by the declared module scope.

1. Added `construction_constant_reproduction`, the division-free finite
   (H_0) identity

   \[
   \sum_j\gamma_j(c-c)=0.
   \]

   The module previously formalized exact (H_1) but did not itself expose
   the corresponding constant-row identity.

2. Added the three already-existing connector theorems to
   `PureMathAxiomAudit.lean`:

   - `fourPointConnector_firstMoment`;
   - `fourPointConnector_cubicMoment`;
   - `fourPointConnector_weight_pos`.

3. Added all seventeen construction theorems to the general
   `AxiomAudit.lean`, whose header promises coverage of every public theorem
   in the aggregate library.  Previously only the focused pure-mathematics
   audit had been extended for P1E.

No manuscript theorem, mesh construction, Cauchy bound, or asymptotic claim
was edited.

## 3. Likely-elaboration audit

The following points were checked line by line.

| Surface | Audit result |
|---|---|
| Finite sums | Every unqualified `∑ j` has the module-level `Fintype` and `DecidableEq` instances required for `Finset.univ`; `open scoped BigOperators` is present. |
| Tangent decomposition | `construction_increment_decomposition` is a polynomial identity; the exact-force proof substitutes it entrywise before using `Finset.sum_sub_distrib` and `Finset.sum_mul`. |
| Division | Every use of `field_simp` is guarded by the exact nonzero denominator hypothesis.  The normalized rate proof uses strictly positive `mu` and `ellMin` in `div_le_div_iff₀`. |
| Detailed balance | The theorem is deliberately scalar and assumes only nonzero row weights; positivity is not smuggled into the equality proof. |
| Correction closure | Both correction lemmas are exact finite equalities and do not infer a global right inverse or positivity. |
| Connector moments | The first- and cubic-moment identities have all four nonzero length hypotheses; positivity of a connector weight separately assumes positive flux and length. |
| Rate conversion | Nonnegative conductances and the lower chord bound are used before division by the positive mass. |
| Polygon identities | Both denominators are exactly `2 * (1 - c)` and are guarded by `1 - c ≠ 0`; the degree-two residual algebra has the stated sign. |
| Imports | `QuadraticFidelityConstruction` imports only the existing reversible-conductance layer plus tactics.  The aggregate import is one-way; no new cycle is introduced. |
| Axiom surfaces | All seventeen public construction theorems occur in both `AxiomAudit.lean` and `PureMathAxiomAudit.lean`.  Definitions are not mislabeled as theorem dependency records. |
| Placeholder policy | Repository scans found no `sorry`, `admit`, `sorryAx`, or project `axiom` declaration in the Lean source tree. |

No theorem uses `Classical.choice` explicitly.  The pinned `#print axioms`
run determined the transitive foundational dependency set reported in the
verdict above.

## 4. Sufficiency and exact boundary

The construction module is sufficient for the accepted **finite algebraic
interfaces** used by the (S^2) ring construction:

1. a jump row annihilates constants;
2. tangent balance plus the radial mass identity gives exact coordinate force
   and hence (L\Omega=-2\Omega) after taking (n=2);
3. one shared conductance gives the scalar detailed-balance equality;
4. unnormalized moment identities survive division by nonzero mass;
5. a solved finite correction system closes its prescribed defect exactly;
6. the four-point connector has exact first/cubic moments and positive
   conductance under its explicit hypotheses;
7. a lower chord bound gives the normalized rate estimate; and
8. regular-polygon degree-one and degree-two recurrences have the printed
   exact multipliers and residual.

This is not a formal proof of the whole P1E theorem.  In particular, the Lean
module does not define or prove:

- the integer ring schedule or equator closure;
- positivity of every solved transition/ordinary/polar coefficient;
- the analytic Cauchy guards;
- the shared-conductance recurrence and global margin;
- fill distance, separation, degree, or angular windows;
- the direct sampled quotient bound; or
- the analytic level-dependent radius in Proposition 7.3.

Those remain in the ordinary proof, the fixed-level robustness proof, and
deterministic exact audits. This boundary agrees with the module docstring and
prevents a nearby finite lemma from being cited as machine verification of the
analytic construction or perturbation radius.

## 5. Deterministic audit results

The following checks passed:

- Python byte-compilation of every `p1e*.py` file;
- short-gap exact algebra;
- literal symbolic transition matrix and limiting system;
- rational Cauchy transition guard;
- independent hostile Cauchy/first-row audit;
- polar Cauchy guard;
- transition and full-family row-class regressions;
- two independent exact fixed-support certificate verifiers;
- focused fixed-support perturbation and hostile-mutation tests;
- rejected-formula/referee mutations;
- independent no-guard ring audit;
- icosphere bulk-formula obstruction;
- algebraic/product fixtures;
- asymptotic-family exact identities and blockers;
- icosahedral cone audit;
- probabilistic/convex audit;
- stratified-lattice repair audit; and
- variational/Voronoi audit.

Several route audits intentionally print `BLOCKED` or `REJECTED` for the
independent route they falsify.  Their processes exited successfully because
the certified obstruction is the expected result; those messages are not
failures of the accepted short-gap construction audit.

The exploratory direct-frequency LP has the interface

```text
p1e_direct_frequency_moment_lp.py frequencies [frequencies ...]
```

and is explicitly a conjecture finder rather than an all-orders certificate.
It was therefore included in byte-compilation but excluded from the theorem
audit pass/fail set.

## 6. Exact commands

Commands successfully run from the repository root:

```bash
python -m py_compile afp_barrier_gate1/pure_math/covariance/p1e*.py

python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_proof_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_symbolic_matrix_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_cauchy_guard_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_cauchy_hostile_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_polar_guard_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_ring_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_family_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_referee_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_no_guard_ring_independent_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_icosphere_bulk_formula_obstruction_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_algebraic_product_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_asymptotic_family_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_icosahedral_cone_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_probabilistic_convex_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_stratified_lattice_repair_audit.py
python afp_barrier_gate1/pure_math/covariance/p1e_variational_voronoi_audit.py
```

The source-policy and coverage checks successfully run were equivalent to:

```bash
rg --glob '*.lean' \
  '(^|[^[:alnum:]_])(sorry|admit|sorryAx)([^[:alnum:]_]|$)' \
  afp_barrier_gate1/AFPBarrier afp_barrier_gate1/AFPBarrier.lean

rg --glob '*.lean' \
  '^[[:space:]]*(@\[[^]]*\][[:space:]]*)*((private|protected|noncomputable|unsafe|scoped|local)[[:space:]]+)*(axiom|axioms)([[:space:]]|$)' \
  afp_barrier_gate1/AFPBarrier afp_barrier_gate1/AFPBarrier.lean

git diff --check
```

Both `rg` commands returned no matches.

The release commands run from `afp_barrier_gate1` in the pinned project image
were:

```bash
lake env lean AFPBarrier/QuadraticFidelityConstruction.lean
lake build
lake env lean AFPBarrier/PureMathAxiomAudit.lean
```

The initial authoring container lacked a usable Lake/Mathlib checkout, so the
local phase was limited to static checks.  The subsequent exact-head release
job supplied the pinned project image and discharged all three commands plus
the full aggregate and axiom-policy checks.

## 7. Release checklist

- [x] Aggregate module imports the construction module.
- [x] General and focused axiom audits enumerate all construction theorems.
- [x] No placeholders or project axioms found by source scan.
- [x] All deterministic noninteractive P1E audits pass.
- [x] `git diff --check` passes.
- [x] Focused construction module elaborates under pinned Lean/Mathlib.
- [x] Full aggregate build passes under pinned Lean/Mathlib.
- [x] Focused axiom output contains only the release-allowed foundational
      dependencies and no `sorryAx`.
