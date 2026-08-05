# AFP publication-program baseline

## P2B accepted-parent addendum

Prompt P2B starts additively from the literal accepted P2A object
`07138547ff5c85df071e2067587dd83ca20b71b5`, tree
`7b17d48665bfc9f8a4490a26468ccf3633960897`, with both
`agent/afp-publication-p2a-convex-design-ab155b8e` and the create-only archive
`archive/afp-publication-p2a-convex-design-verified` at that exact object.
The clean P2B branch is
`agent/afp-publication-p2b-harmonic-transport-07138547`; its create-only target
is `archive/afp-publication-p2b-harmonic-transport-verified`.

P2B adds a separate harmonic-defect transport theorem, manufactured-error
implementation, formal finite core, and exact-head workflow.  It does not
rewrite the accepted Paper-I/P2A definitions, optimizer, lower bound, or
transport Gate-6 archive.  The latter remains numerical background and a
regression boundary, not a proof source for P2B's stability estimates.

## P2A accepted-parent addendum

Prompt P2A starts additively from the literal accepted Paper-I/P1F object
`ab155b8e04bdf00306351b581739fb5feeb2979e`, tree
`61a07c6c187d3002d5ca433be16b26fb1bad73f1`, branch
`agent/afp-publication-p1f-flagship-paper-4e461c10`, and immutable ref
`archive/afp-publication-p1f-flagship-paper-verified`.  The P2A working branch
was created at that exact object as
`agent/afp-publication-p2a-convex-design-ab155b8e`.  This addendum supersedes
the older P0 source only as the parent selection for P2A; it does not rewrite
the historical provenance below.

Snapshot: 2026-08-04 (America/Toronto)
Repository: `FusionSandwich/Testing`

## Authoritative mathematical object

The publication program starts from commit
`6bac46ce1a34ffba53f0003b876e57c4d747feaf`, tree
`0d5bda7241303fa84e77ffd00e982fe424d06af0`, parent
`c25ea42abd17a2418c48ea5832db2c2499195652`.  It is the exact head of
`archive/afp-pure-math-p4-sharp-barriers-verified` and contains the accepted
Prompt-1-through-Prompt-4 line, including both late corrections:

- spectral sampling is indexed by distinct target eigenvalue classes, with
  the literal distinct-degree statement rejected at `d=1` and constants
  counted once in the zero-target converse class;
- for opposite rays `v2=-kappa v1`, the anisotropy is
  `kappa(ell1-ell2)^2/(kappa ell1+ell2)^2`; equal projective weights are forced
  only when `kappa=1`.

The new create-only descendant branch is
`agent/afp-publication-program-p0-6bac46ce`.  Before any edit its remote head
was created at the exact baseline object.  The accidentally created
`agent/afp-publication-program-p0-c8505a70` remains untouched at `c8505a70…`
and is classified `REJECTED_BASELINE_CANDIDATE`, not deleted or repurposed.

## Fork resolution

`c8505a70df01320d18a443bbf2ed1c11a761e5ce` (tree
`e55441e3645cfd58aa529b11ec17245723fcafcc`) is the later fast-forward result
of PR #34 and has six historical green workflows.  It and `6bac46ce…` diverge
at `b5f74404729f1a3c0396812539dffccc5ce928c5`; neither descends from the
other.  A literal tree audit shows that `c850…` is not descended from corrected
Prompt 2 `31ea6a49…`, omits the spectral-product proof/audit and associated Lean
modules, and retains the superseded equal-projective-weight assertion.  A
later mutable date or merged administrative PR cannot override those exact
mathematical facts.  Accordingly `c850…` is preserved as historical evidence
but is not the publication source baseline.  No existing ref is moved to
reconcile the fork.

A third candidate, `8e3d9d0526b8ce4ad53745f15d961e04ea51b392`
(tree `953e28fce4fecd18258a84aa028cfdc38b5c8cd1`), combines the later spectral
files with an alternate rich-P3 integration and passed six exact-head jobs
(3112 Lean jobs).  It remains the unmerged draft head of PR #33 and retains the
same superseded symmetric opposite-ray formulation.  It is therefore also a
preserved candidate, not the corrected publication baseline.

The accepted ancestry is:

```text
31ea6a49f006df10ca633eafd6848ad43b51ac3f  Prompt 2 corrected
  -> c66f3229d0a89d97559535810c4ba09daf6e4e42  Prompt 3 mathematics
  -> 8de4b94835137d1eaf32c14b626424f87d2e176d  Prompt 3 closeout
  -> 6bac46ce1a34ffba53f0003b876e57c4d747feaf  Prompt 4 corrected archive
```

All three ancestor tests succeed.  The candidate is not based on the
divergent `c850…` line.

The accepted Prompt-1 object is
`923dc47dae4f83dbea9cd56aa904164c6378e52d`, tree
`906449c151fd97756a10fb83e7106a2e6ba39b0f`; it is an ancestor of the selected
baseline.  The older `archive/afp-spherical-feasibility-validation-accepted`
currently points to `01a592301978ab184fc7969d9f54592eddad742c` and is retained
as a historical P0/M1 archive, not mislabeled as the corrected Prompt-1
object.

## Ref snapshot

Immutable refs are fatal invariants; mutable heads are observations only.

| Kind | Ref | Observed exact head | Result |
|---|---|---|---|
| immutable | `archive/afp-gate6-spatial-multigroup-verified` | `515f1aae6c20bd85711c90b5c1c21b4905252d01` | EXACT |
| immutable historical | `archive/afp-spherical-feasibility-validation-accepted` | `01a592301978ab184fc7969d9f54592eddad742c` | EXACT_HISTORICAL_P0_M1 |
| immutable | `archive/afp-pure-math-p2-quadratic-covariance-verified-31ea6a49` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | EXACT |
| immutable | `archive/afp-pure-math-p3-rigidity-verified` | `8de4b94835137d1eaf32c14b626424f87d2e176d` | EXACT |
| immutable | `archive/afp-pure-math-p4-sharp-barriers-verified` | `6bac46ce1a34ffba53f0003b876e57c4d747feaf` | EXACT |
| mutable | `agent/afp-pure-math-p0-m1` | `c8505a70df01320d18a443bbf2ed1c11a761e5ce` | OBSERVED_DIVERGENT |
| mutable | `agent/afp-pure-math-p3-p4-final-acceptance` | `c8505a70df01320d18a443bbf2ed1c11a761e5ce` | OBSERVED_DIVERGENT |
| mutable | `agent/afp-pure-math-final-integration-20260802` | `8e3d9d0526b8ce4ad53745f15d961e04ea51b392` | OBSERVED_UNMERGED_SUPERSEDED_FORMULA |
| mutable | `agent/afp-pure-math-p2-quadratic-covariance-completion` | `31ea6a49f006df10ca633eafd6848ad43b51ac3f` | UNCHANGED |
| mutable | `agent/afp-pure-math-p1-local-global-corrected` | `dd3ea8ee612958f223bbbf05cf5de926377cd5a1` | OBSERVED_DESCENDANT_OF_ACCEPTED_P1 |
| mutable | `agent/afp-pure-math-p3-rigidity-from-p2-31ea6a49` | `c66f3229d0a89d97559535810c4ba09daf6e4e42` | UNCHANGED |
| mutable | `agent/afp-pure-math-p3-q1-rigidity` | `65821ff1ebd47fbee1098b30c552906cd6e03b46` | UNCHANGED |
| mutable | `agent/afp-pure-math-p3-integration-record` | `6b5d7ad53d704b7ff1b96d40abbef19f6e6a2125` | UNCHANGED |
| mutable | `agent/afp-pure-math-p3-global-rigidity-near-rigidity` | `f1ef5b3c3107d2dfc835ed84c443eb82d752cb56` | MOVED_EXTERNALLY_FROM_HISTORICAL_d9304b5d; CURRENTLY_STABLE |
| mutable | `agent/afp-pure-math-p4-from-p3-8de4b948` | `6bac46ce1a34ffba53f0003b876e57c4d747feaf` | UNCHANGED |
| mutable | `agent/afp-pure-math-p4-sharp-barriers-extremal-synthesis` | `94aebf6578a43516cce4bb7c042fc57681c93890` | UNCHANGED |
| mutable | `agent/afp-pure-math-p4-integration-record` | `83bf04b99a060658b0177f3373ea0869cb4f3447` | UNCHANGED |

Ordinary third-party movement of a mutable head will be recorded by CI and is
not candidate corruption.  Missing immutable objects, wrong archive values,
wrong ancestry, a changed accepted source subtree, or a tested-remote mismatch
is fatal.  Git cannot prove absence of unobserved transient ref movement.

## Accepted workflow and artifact evidence

| Stage | Commit/tree | Run and jobs | Artifacts (ID / SHA-256) | Source tar |
|---|---|---|---|---|
| Prompt 1 | `923dc47d…` / `906449c1…` | accepted corrected object; retained audits rerun by every later closeout | exact identities incorporated into the later hashed P2–P4 artifacts | immutable tree object |
| Prompt 2 | `31ea6a49…` / `879b88de…` | `30760522011`; exact and Lean success; 3107 jobs | `8837341400` / `d538383e6be15a5930b5f6e3b49e8fe8a0895262c19ce05b5288da92d4742979`; `8837324993` / `45720c2202fdd9b7de5af2533aba75154a211b0e6214ac1755d0432a79060d96` | `d7ca753b1f33fa3bf8dfce4a71bf4a34a578c6f8c793afae8f60b743be1e413c` |
| Prompt 3 closeout | `8de4b948…` / `350fc383…` | `30775112774`; three jobs success; 3110 jobs | `8841822420` / `7738017ca85daa241c9ec99d1f7394829398bcbd066f5b83d55291f0cc942bf5`; `8841796066` / `1c5efba248dbc709574c0436466ee4b37ca72fa715a95d1e7ef2f67f506efd9b`; `8841825241` / `d0eb4f51436a8b49e56fdc2496d63aba4fe50512b0732a0335611ccde2f855e8`; `8841825450` / `ce9c708ed00461f8011a116d94df38bf50bc4e2ee8a02a2a09efc6085836eb4c` | `db3539ebd0cf8ae2ebd2e1fb8ff8ec7c4b60d174f6fabaa2919754260f317f10` |
| Prompt 4 archive-aware | `6bac46ce…` / `0d5bda72…` | `30780693332`; jobs `91584584670`, `91584584595`, `91585292413` success; 3111 jobs | `8843601702` / `a85cddbef1358397ac17d20577e26e4bfba05addabdd4fb6fa030d15edbf7e49`; `8843568824` / `38386d6a1df3c9bf75f8a47cd7d475a8d0372297e8380a0aed0bf683be8f1876`; `8843604086` / `55d0ab9eb1abd26afd03ef9c27bed1a19070befdec6036c904d9828487a54b7f`; `8843604238` / `366eefa6fa4298fba401e5fbc161bbb032fe8dd7466114af989c0e19c14d0ebe` | `0ecb1c130b5db43631f65c164372fc4e3ffaa56d9e75c8ff7487cfa7319a6b77` |

Prompt 4 ran all retained P1/P2/P3/P4 exact audits, the source-pinned
Plantri census `1,1,2,5,14,50,233,1249,7595` (total `9150`), Lean 4.30,
and a focused axiom audit whose only dependencies were `propext`,
`Classical.choice`, and `Quot.sound`; no placeholder, `sorryAx`, or user axiom
was present.

The earlier Prompt-3 mathematical-candidate run `30771073146` is preserved in
`afp_barrier_gate1/docs/P2_P3_FINALIZATION_RECORD.md`: its deterministic and
Lean work succeeded, while its final mutable-ref equality policy produced the
recorded false negative.  Artifacts were `8840594725`, `8840570642`, and
`8840596622`; source tar
`51913841c2b17be2b11f8379a93682e568ade80c46efd51774eff68802cc9668`.

PR state at snapshot: PR #34 is merged on the divergent administrative line;
PR #35 is open and points to the selected P4 archive line; PRs #21 and #31 are
open historical P2/P3 reviews; PR #28 is closed unmerged.  PR state is
provenance evidence, not a replacement for immutable object verification.

## Canonical normalization

`w_i>0`, `sum_i w_i=1`, `gamma_ij=gamma_ji>=0`, and
`a_ij=gamma_ij/w_i`.  The generator is

```text
(L f)_i = (1/w_i) sum_j gamma_ij (f_j-f_i)
        = sum_j a_ij (f_j-f_i).
```

Thus `L` has nonnegative off-diagonal entries, zero row sums, is negative
semidefinite in `<f,g>_w=sum_i w_i f_i g_i`, and `W L=L^T W`.  On
`S^(d-1)`, `L Omega=-(d-1) Omega` and
`lambda_l=l(l+d-2)`.  The sampling map is
`S_X(A)_i=Omega_i^T A Omega_i` for `A in Sym_0(d)`, its kernel is `K_X`, and
`R_X=(L+2d I)S_X`.  The sampled defect denominator is `||S_X A||_w`, never
the Frobenius norm of an algebraically nonzero form.  With
`ell_ij=1-Omega_i.Omega_j`, `r_i=sum_j a_ij`, and
`epsilon_i=sum_j a_ij ell_ij^2`, one has
`sum_j a_ij ell_ij=d-1` and `Q_i=r_i epsilon_i/(d-1)^2`.
The abbreviation `Q=r epsilon/4` is only the `d=3` specialization.

## Exact five-Platonic baseline

Equal weights, shortest-edge support, and `L Omega=-2 Omega` are used.  This
table was regenerated by
`python pure_math/covariance/exact_quadratic_covariance_audit.py`; the exact
audit passed on the selected tree.

| Graph | N/q | alpha; ell | a; r; epsilon; gamma | rank S/R | dim E_form / dim K_X / dim E_sample | Q |
|---|---|---|---|---|---|---|
| tetrahedron | 4/3 | `-1/3`; `4/3` | `1/2`; `3/2`; `8/3`; `1/8` | 3/3 | 2/2/0 | 1 |
| octahedron | 6/4 | `0`; `1` | `1/2`; `2`; `2`; `1/12` | 2/2 | 3/3/0 | 1 |
| cube | 8/3 | `1/3`; `2/3` | `1`; `3`; `4/3`; `1/8` | 3/3 | 2/2/0 | 1 |
| icosahedron | 12/5 | `sqrt(5)/5`; `1-sqrt(5)/5` | `(5+sqrt(5))/10`; `(5+sqrt(5))/2`; `2-2sqrt(5)/5`; `(5+sqrt(5))/120` | 5/5 | 0/0/0 | 1 |
| dodecahedron | 20/3 | `sqrt(5)/3`; `1-sqrt(5)/3` | `(3+sqrt(5))/2`; `(9+3sqrt(5))/2`; `2-2sqrt(5)/3`; `(3+sqrt(5))/40` | 5/5 | 0/0/0 | 1 |

Cube and dodecahedron are permanent counterexamples to unrestricted Platonic
classification, not additional equality-classification survivors.

## Source-consumer inventory

The exact inventory is the output of

```text
git ls-tree -r --format='%(objectmode) %(objectname) %(path)' 6bac46ce... -- \
  .github/workflows afp_barrier_gate1/AFPBarrier.lean \
  afp_barrier_gate1/AFPBarrier afp_barrier_gate1/pure_math \
  afp_barrier_gate1/docs afp_barrier_gate1/lakefile.lean \
  afp_barrier_gate1/lake-manifest.json afp_barrier_gate1/lean-toolchain
```

This pure-math/control manifest contains 121 tracked objects and has SHA-256
`090365d15dab7053643cae6c7adf6ee1aae95d5c2a3eadcf97bd207fd4c542cb`
when rendered as `mode blob path` lines.  Nothing generated (`__pycache__`,
Plantri binary/catalog, logs, archives) is tracked.

| Exact path set | Role | Consumer |
|---|---|---|
| `afp_barrier_gate1/AFPBarrier.lean`; every `afp_barrier_gate1/AFPBarrier/*.lean` (54 modules) | aggregate proof, finite algebra, P1–P4 theorems, focused axiom audits | Papers I/III; transport modules are frozen Paper-II inputs |
| every `afp_barrier_gate1/pure_math/**/*.py` (12 audits) | exact positive and negative regressions, Plantri driver | Papers I/III |
| every `afp_barrier_gate1/pure_math/**/*.md` and `afp_barrier_gate1/pure_math/*.md` (20 records/packages) | proofs, theorem/approach registries, salvage and protection records | Papers I/III |
| every `afp_barrier_gate1/docs/*.md` (19 claim/stage/theorem/prior-art records) | claim firewall and provenance | Papers I–III |
| all 12 `.github/workflows/afp-*.yml` objects present at the baseline | historical and dedicated exact-head verification | all papers |
| `afp_barrier_gate1/{lean-toolchain,lakefile.lean,lake-manifest.json}` | Lean 4.30/Mathlib pin | Papers I/III |
| immutable workflow artifacts and source tarballs listed above | reproducibility evidence; never source | all papers |
| transport archive `515f1aae…`: four gate workflows; six transport Lean modules; every tracked file under `gate3/`–`gate6/` | frozen implementation/benchmark boundary | Paper II only |

The P0 workflow emits the complete line-level manifest as an artifact, so every
path, mode, and blob is machine-auditable.  Papers must cite the immutable
object and blob, not a mutable branch name.

The separate transport manifest is generated from immutable commit
`515f1aae6c20bd85711c90b5c1c21b4905252d01`.  It contains exactly 48
`mode blob path` rows (the four gate workflows, six named transport Lean
modules, and all `gate3/`–`gate6/` files) and has SHA-256
`84624f9f308f59d734b006f5379897a7361daf22d425b2fbd05a19477726f329`.
The P0 artifact emits and verifies this second manifest independently; it is a
Paper-II input boundary, never a pure-math proof source.

## No-overwrite certificate and next baseline

The P0 commit may change only these six control-plane documents and
`.github/workflows/afp-publication-program-p0.yml`.  CI compares the complete
`afp_barrier_gate1` tree to `6bac46ce…`, reruns all exact and Lean checks at the
literal remote head, verifies all four pre-existing archives, and emits hashed
source/evidence artifacts.  After a green exact-head run, a create-only
`archive/afp-publication-program-baseline-p0-6bac46ce` points to that already
tested commit.  The archive-aware green commit is the sole baseline for P1A,
P3A, and later publication prompts; no synthetic merge is authorized.
