# Prompt for a later non-concurrent hostile review of R7

Run this review only after the R7 repair task has ended. Before reading prior
responses, record the exact pushed branch-tip SHA supplied in the handoff and
check out that immutable snapshot. Do not review a moving branch.

You are conducting an independent hostile mathematical and reproducibility
review of the AFP R7 repair on branch
`codex/afp-major-revision-r7-20260824`. Treat all earlier ChatGPT Pro reviews,
including `Review Math Revision Branch` in project `Math`, as internal AI
adversarial review rather than identifiable external human peer review. The
renewed R6 audit ended **MAJOR REVISION**; do not assume that R7 clears it.

Independently rederive before consulting the response ledger:

1. the trace lower bound, sharp positivity--rate frontier, equality chain, and
   weighted defect budget, explicitly distinguishing the exact defect
   decomposition relative to the trace lower bound from the full frontier
   excess;
2. the Theorem 7.2 signed logarithmic estimate, including the second-order
   remainder, arbitrary geometric schedule sums, and the constants `513` and
   `512` in the cumulative transition product;
3. the complete P1E conductance and weight normalization chain from
   preliminary `Gamma_ij` and `mu_i` through `W`, `w_i`, normalized
   `gamma_ij=Gamma_ij/W`, and rates `a_ij=Gamma_ij/mu_i`;
4. the exact boundary between ordinary proof, Lean-checked finite algebra, and
   the independent exact-rational certificate.

Then audit `HOSTILE_AI_REVIEW_R7_RESPONSE.md`, the manuscript, P1E supplement,
claim ledger, theorem registry, certificate JSON/verifier/README, Lean
declaration index and axiom log, reproducibility instructions, release
manifest, and rebuilt PDF. Run the documented verifier, all 14 exact audits,
Lean build/signature/axiom audit, scoped Python suite, P2F integrity audit,
flagship validator, manifest validator, and PDF render inspection. Mutate at
least the lower exponent, the `Gamma/W` normalization, and a rate constant and
confirm rejection.

Return a blocker-ranked report with exact file/line evidence and one of:
`PASS`, `MINOR REVISION`, or `MAJOR REVISION`. Explicitly report whether every
numbered surviving claim is correct, whether any certificate prose exceeds
what the verifier derives, whether P2F or physical claims leaked, whether the
snapshot was immutable throughout review, and whether any conclusion depends
on unverified external input. Do not merge, tag, release, or claim journal or
human-peer-review acceptance.
