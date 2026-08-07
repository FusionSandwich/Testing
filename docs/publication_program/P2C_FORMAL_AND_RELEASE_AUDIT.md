# P2C formal-verification and immutable-release audit

## Historical finding

The first P2C archive at
`b34c29b1b04f5293eaa4007b39d189efa03c51f5` passed its numerical and inherited
Lean jobs, but the workflow used a job named `freeze-forward-only-archive`.
That job permitted an existing verified archive to be fast-forwarded.  This
contradicted the publication handoff’s create-only archive rule.  The same
workflow allowed carriage returns in text blobs, so two malformed LaTeX
commands in the theorem document escaped the control-byte scan.

Neither issue changes the accepted P2A/P2B/P1B/P1E mathematics.  They are
publication-integrity and theorem-presentation defects and are corrected on a
new descendant branch.  The historical archive is not moved, overwritten, or
relabelled.

## Corrected release topology

- immutable historical parent:
  `archive/afp-publication-p2c-codesign-verified`
- historical parent SHA:
  `b34c29b1b04f5293eaa4007b39d189efa03c51f5`
- completion branch:
  `agent/afp-publication-p2c-completion-b34c29b1`
- new create-only completion archive:
  `archive/afp-publication-p2c-completion-verified`

The correction workflow compares the literal parent SHA and tree, rejects
merge commits, enforces an exact changed-path set, and rejects every ASCII
control byte except tab and line feed.  Carriage return is therefore forbidden.

The archive job has only two accepted states:

1. the target archive is absent, in which case an absent-ref lease creates it
   at the exact candidate SHA; or
2. the target archive already equals the exact candidate SHA, in which case
   the workflow verifies it and performs no write.

An existing archive at any different SHA is a hard failure.  There is no
fast-forward or force-update path.

## P2C-specific Lean boundary

`AFPBarrier/QuadratureGeneratorCodesign.lean` formalizes stable finite algebra:

1. positivity of `lambda w_i w_j` dense conductances;
2. the normalized dense-generator mean-minus-point identity;
3. exact constant and centered-sample action, including H1 coordinates;
4. zero extension of new edge columns;
5. proximal comparison descent and the squared-increment bound; and
6. the exact Paper-I lower-coefficient/rate-cap product equal to six.

`AFPBarrier/P2CAxiomAudit.lean` prints the axioms of every new theorem.  CI also
rejects `sorry`, `admit`, `sorryAx`, and project-local axiom declarations.

The formal layer does not claim to cover:

- general SDP/SOCP strong duality or floating solvers;
- the matrix-valued Schur-complement theorem in full generality;
- Berge’s maximum theorem or Robinson metric regularity;
- limiting/Clarke subdifferential calculus;
- Riemannian restoration and Armijo convergence;
- the analytic P1E ring construction; or
- transport/PDE rotation-response stability.

Those remain ordinary proofs with symbolic, exact, interval-ready, and hostile
computational audits.

## Independent release gates

The exact candidate must pass all of the following before the new archive is
created:

1. exact lineage and changed-path inventory;
2. UTF-8 and no-control-byte audit;
3. Python compileall;
4. exact symbolic P2C audit;
5. full P2C hostile pytest suite, including the 60-element icosahedral adapter;
6. finite benchmark with independent P2A primal/dual verification;
7. retained P1E, P2A, and P2B regressions;
8. P2C document inventory, claim sequence, and placeholder scan;
9. P2C Lean build and focused axiom audit;
10. exact remote branch-head verification; and
11. create-only archive verification.

The workflow artifact records the exact commit, tree, parent, complete pinned
Python environment, source archive hash, test/audit logs, benchmark provenance,
and a hash inventory of every uploaded record.

## Acceptance statement

The completion archive supersedes the historical P2C archive for future
lineage while preserving the historical ref unchanged.  P2D must branch from
the completion archive, not by moving or silently repairing the earlier ref.
