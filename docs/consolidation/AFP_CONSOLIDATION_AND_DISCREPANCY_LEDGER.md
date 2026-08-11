# AFP consolidation and discrepancy ledger

## Decision

The AFP program is consolidated as one merge-free descendant line in
`FusionSandwich/Testing`.  Existing branches and archive refs are retained as
historical evidence and are not moved, deleted, or force-updated.  A dedicated
repository remains desirable, but repository creation was not available in the
authenticated environment; the consolidated tree is therefore prepared so it
can be transferred without changing scientific history.

The selected scientific ancestry is:

`testing` → accepted pure-math gates → P0 → P1A → P1B → P1C → P1D → P1E →
P1F → P2A → P2B → P2C → P2D acceleration → P2D completion → P2E
preregistration → P2E one-time held-out execution → P2E closeout → Math
`hts_angular` import → P2F bounded HTS closeout.

The live inventory and literal head SHAs for all 121 observed branches are in
`AFP_BRANCH_INVENTORY_2026-08-10.{md,json}`.

## Discrepancies preserved

1. The later `c8505a70…` administrative baseline is not the mathematical
   publication authority.  It omitted accepted corrections retained by the
   `6bac46ce…` line.
2. P2E execution at `e60f5c7…` was authentic and reproducible, but a green
   workflow meant execution integrity, not a successful value hypothesis.
3. The preregistered P2E worst-response gate failed (`8.0684 > 1.8`).  The
   corresponding HTS absolute-error difference is smaller than the independent
   reference uncertainty, so it is unresolved evidence rather than a resolved
   eightfold physical degradation.
4. The preregistered acceleration reduction was achieved (`17` versus `23`
   iterations, `26.09%`) but was not enforced by the original audit.
5. The P2E `equal_wall_time` record was only a common completion-budget record.
   It was not a true equal-time work-allocation experiment.
6. No P2F branch existed at inventory time.  P2F is new work and is not
   retroactively attributed to an older branch.
7. `FusionSandwich/Math` contains a useful AFP-adjacent `hts_angular` package,
   but its thin-interface Papers 1–4 are a distinct transport program.  PR #14
   did not contain the advertised integrated Papers 1–4 tree.  Those branches
   are not treated as AFP publication authority.

## Imported Math scope

Only the self-contained `hts_angular` source, its direct tests and examples,
the adaptive/angular manuscripts, and direct benchmark evidence are imported.
Every imported text blob is pinned in `math_repo_afp/PROVENANCE.json` to Math
commit `ccc75ff90ddd8348aa805178f9f1925b9b10cd16`.  The imported code is kept
byte-for-byte and is tested from its own source root; it is not silently mixed
into the P2E/P2F implementation.

## Merge policy

- Historical stage PRs remain evidentiary records.
- The new stacked PR train is linear.  Each stage targets only its immediate
  predecessor; the final integration PR targets `testing`.
- P2E and P2F scientific outcomes are P2E negative/mixed and P2F inconclusive outcomes.  They are not
  converted to positive results by changing the frozen operator, thresholds,
  or held-out cases.
- The archive refs are branch refs, not intrinsically immutable Git objects.
  Workflows therefore verify their literal SHAs and fail closed on movement.
