# P2D clause matrix

| Prompt clause | Closure |
|---|---|
| exact conservation and fixed point | Theorems 2.1–2.2; compatible constrained correction; hostile incompatibility test |
| error-propagation operator | manuscript §3 and `error_propagation_operator` |
| harmonic-shell action | exact scalar-shell theorem and sampled-shell audits |
| shell-mismatch bounds | perturbation bound plus restricted slow-subspace norm/leakage |
| spectral equivalence | SPD generalized Rayleigh theorem and fail-closed implementation |
| field-of-values control | metric FOV theorem and executable report |
| spatial streaming dependence | retained upwind blocks and noncommuting slab sweep |
| energy coupling dependence | two-group downscatter case |
| boundary dependence | partially reflective boundary case and explicit block norm |
| sufficient iteration reduction | shell/FOV contractions and explicit count bound; actual slow-mode audit |
| H2 irrelevant to slow subspace | degree-seven adversary and deliberately hostile diagonal fixture |
| monotone AFP baseline | frozen same-node shared-conductance baseline |
| classical modified FP | signed spectral FP/FPSA-style preconditioner, honestly scoped |
| no acceleration | unpreconditioned high-order GMRES |
| H2-poor positive | dense centered complete-graph positive generator |
| identical high-order discretization/stopping | enforced within every sweep row |
| iteration count | deterministic audit field |
| high-order matvecs | deterministic audit field |
| setup cost | cached factorization timing |
| wall time | setup, solve, and total timing fields |
| memory | Python peak, matrix bytes, and factor bytes |
| robustness as forward peaking increases | four-row heat-kernel/BFP sweep, first moment 0.92312–0.99005 |
| relevant slow modes represented | angular-only H2 mode selection plus full-system restricted contraction/leakage |
| higher-harmonic adversary | degree-seven and hostile diagonal cases |
| ray-effect adversary | analytic grazing ballistic comparison, 446.98% coarse-ray error |
| audit and reproducibility | frozen hashed operator data, 15 tests, exact-head workflow, retained P2A–P2C regressions, Lean boundary |
