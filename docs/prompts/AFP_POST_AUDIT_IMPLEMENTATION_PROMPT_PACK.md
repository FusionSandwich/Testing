# AFP Post-Audit Implementation Prompt Pack

## Purpose

This file contains the complete implementation sequence for repairing the existing AFP publication program and developing the strongest proposed new mathematics.

The assignments below are optimized for the available usage constraints:

- **Codex Work** is reserved for theorem-strength mathematics, proof repair, verified numerics, and new mathematical research.
- **Pro Chat** is used for literature analysis, manuscript reconstruction, novelty positioning, hostile review, and editorial synthesis.
- **Codex** is used for repository operations, Lean, software, reproducibility, numerical implementation, tests, and GitHub publication workflows.

The first prompt contains the complete project context needed by a new person or agent.

---

# Recommended execution order and resource allocation

| Order | Prompt | Recommended environment | Why |
|---:|---|---|---|
| 0 | G0 — GitHub persistence handoff | **Codex** | Small repository and publishing task used after Pro Chat work |
| 1 | R0 — Authoritative state and repair baseline | **Codex** | Git history, files, hashes, branches, tests, and PR creation |
| 2 | R1 — Repair Proposition 7.3 | **Codex Work** | Highest-priority theorem-strength mathematical blocker |
| 3 | R3 — Rebuild the pure-mathematics paper | **Pro Chat** | Literature, novelty positioning, proof organization, and writing |
| 4 | R4 — Align Lean and reproducibility | **Codex** | Lean, CI, scripts, containers, artifacts, and release engineering |
| 5 | F0 — Final hostile review | **Pro Chat** | Independent referee review and editorial synthesis |
| 6 | R2 — Improve the \(d=3\) constants | **Codex Work** | Valuable but not strictly required if the theorem is scoped honestly |
| 7 | N2 — Response-certified harmonic fidelity | **Codex Work** | Highest-value new mathematics for explaining transport impact |
| 8 | B0 — Correct and rebuild benchmarks | **Codex** | Numerical implementation after response sensitivity is defined |
| 9 | N3 — Conic feasibility theory | **Codex Work** | Strong balance of novelty, tractability, and practical value |
| 10 | N1 — Exact degree-three theory | **Codex Work** | Highest pure-mathematics ceiling, but technically risky |
| 11 | N4 — Half-range/interface theory | **Codex Work** | Highest fusion-specific ceiling, best after N2 or N3 |

## Minimum publication path

Run:

\[
\text{R0}\rightarrow\text{R1}\rightarrow\text{R3}\rightarrow\text{R4}\rightarrow\text{F0}.
\]

Run R2 if the construction constants remain a serious referee objection. Do not delay the existing quadratic paper merely to finish N1–N4.

## Best new-research path

After the existing paper is repaired, prioritize:

\[
\text{N2}\rightarrow\text{B0}\rightarrow\text{N3}.
\]

N1 and N4 are higher-risk independent programs.

---

# Mandatory GitHub persistence protocol

This protocol applies to every prompt in this file.

1. **Do not leave substantive work only in chat.** Every theorem statement, proof, counterexample, literature matrix, review, decision, benchmark specification, source file, test, log, certificate, table, figure, and unresolved gap must be saved in the repository.
2. Resolve the live authoritative commit and tree before starting. Do not rely on a recorded head without verification.
3. Work on a dedicated branch. Never rewrite, delete, move, or silently replace historical branches, archive refs, preregistrations, held-out evidence, or benchmark artifacts.
4. Use small logical commits. Push after each completed milestone rather than keeping a large unpushed worktree.
5. Open or update a **draft pull request** containing:
   - the exact problem being solved;
   - the mathematical or software changes;
   - evidence and reproduction commands;
   - unresolved issues;
   - the current theorem and publication status.
6. Save the exact prompt used for each major task under an appropriate repository path such as:
   - `docs/prompts/`;
   - `docs/publication_program/prompts/`;
   - or the closest existing project convention.
7. Maintain durable project-state files. Reuse existing files if they already exist; otherwise create equivalents of:
   - `docs/project_state/AFP_CURRENT_STATE.md`;
   - `docs/project_state/AFP_DECISION_LOG.md`;
   - `docs/project_state/AFP_THEOREM_STATUS.md`;
   - `docs/project_state/AFP_NEXT_STEPS.md`;
   - `docs/project_state/AFP_ARTIFACT_MANIFEST.json`.
8. Save machine-readable companions for important prose reports whenever feasible:
   - theorem matrices as CSV or JSON;
   - provenance manifests as JSON;
   - hashes as text or JSON;
   - benchmark outputs as CSV, JSON, or HDF5;
   - certificate metadata as JSON.
9. Commit raw evidence and generation scripts whenever licensing and size permit. For files too large for ordinary Git, use the repository’s established artifact mechanism and commit immutable hashes, retrieval instructions, and metadata.
10. Final responses must state:
    - repository;
    - branch;
    - exact head commit;
    - exact tree;
    - draft PR;
    - files created or changed;
    - commands run;
    - tests and proof checks;
    - unresolved issues.
11. A Pro Chat task should use connected GitHub tools to save its work directly when possible. If direct GitHub writes are unavailable, it must produce a complete ready-to-commit file bundle with exact paths and then invoke Prompt G0. No important conclusion may remain only in the conversation.
12. Do not merge a draft PR unless the user separately authorizes the merge.

---

# Prompt G0 — Persist a Pro Chat result to GitHub

**Recommended environment: Codex**

**Use this only when a Pro Chat task produced a file bundle but could not commit it directly. This should consume substantially fewer Codex tokens than repeating the underlying review or manuscript work.**

```text
Current task statement

PROBLEM

Persist the supplied AFP Pro Chat work product to the authoritative GitHub repository without changing its mathematical content, losing provenance, or mixing unrelated repository changes.

The authoritative repositories are:

- https://github.com/FusionSandwich/Testing
- https://github.com/FusionSandwich/Math

The user will supply, or the current workspace will contain, a ready-to-commit bundle produced by a Pro Chat task. It may include manuscript text, referee reports, theorem matrices, novelty matrices, bibliographies, decision logs, prompts, or publication recommendations.

First resolve:

- the live authoritative AFP branch, commit, and tree;
- the intended repository;
- the current default or target branch;
- whether a dedicated branch or draft PR already exists for this work;
- whether the working tree contains unrelated changes.

Create or use a dedicated branch of the form

    agent/afp-persist-<topic>-<short-live-head>.

Do not overwrite an existing unrelated branch. Do not rewrite, merge, close, retitle, or delete historical AFP refs, archive branches, preregistrations, held-out evidence, or benchmark artifacts.

Inspect the supplied bundle and place every file at a stable repository path consistent with existing conventions. At minimum preserve:

- the exact prompt used;
- the complete report or manuscript;
- machine-readable matrices;
- bibliography or source list;
- decisions and unresolved issues;
- a provenance note recording the originating Pro Chat session and date;
- a SHA-256 manifest.

Update the durable AFP project-state files, reusing existing equivalents when present:

- current state;
- decision log;
- theorem status;
- next steps;
- artifact manifest.

Validate Markdown links, file paths, JSON, CSV, and any other structured files. Do not silently edit mathematical content. Correct only mechanical formatting, broken internal links, invalid encoding, or schema errors, and record every such correction.

Commit the work in one or more small logical commits, push the branch, and open or update a draft pull request. The draft PR must state:

- what Pro Chat task produced the material;
- what files were persisted;
- that mathematical content was not independently changed;
- what validation was performed;
- what later Codex or Codex Work task should consume the files.

—- Assume for purposes of this task that the supplied bundle is complete and that the authoritative repository and target can be resolved. A complete solution must persist the entire bundle, commit and push it, open or update a draft PR, update project-state files, and report exact commit and tree hashes. Partial progress, saving files only in the local workspace, creating an unpushed commit, or copying prose without its prompt and provenance is insufficient.

Use multiagent v2 only if the bundle is large enough to require independent path, schema, and provenance checks. Do not use it merely to inflate the task.

GitHub persistence is the principal purpose of this prompt. Return only after the branch, commits, push, draft PR, and artifact manifest are complete.
```

---

# Prompt R0 — Resolve the authoritative state and establish the repair baseline

**Recommended environment: Codex**

```text
Current task statement

PROBLEM

Establish the exact authoritative live state of the AFP spherical-generator program, create a dedicated post-audit repair branch from the strongest valid descendant, and produce a complete provenance and dependency baseline before changing any mathematics.

The authoritative repositories are:

- https://github.com/FusionSandwich/Testing
- https://github.com/FusionSandwich/Math

The current consolidated candidate was previously reported as:

- Repository: FusionSandwich/Testing
- Pull request: https://github.com/FusionSandwich/Testing/pull/51
- Branch: agent/afp-consolidated-p2e-p2f-e60f5c7
- Recorded head: b8912c282a22420e8077c75929b16c7a33d189b2
- Recorded tree: 4c2175463a661ce3f2bb206f0cb7b5038183b2ab
- Target branch: testing

The Math import was previously recorded as:

- FusionSandwich/Math@ccc75ff90ddd8348aa805178f9f1925b9b10cd16
- 33 imported AFP/HTS files

The reported staged history in Testing is:

P0 → P1A → P1B → P1C → P1D → P1E → P1F → P2A → P2B → P2C → P2D → P2E → P2F.

Important previously reported commits include:

- P1A: 5ef6bf3335f72e38987df6b06e30d712de4b86c7
- P2C: b34c29b1b04f5293eaa4007b39d189efa03c51f5
- P2D acceleration: 2fb7a11b75a9699a7afc8a2ee16c90656c58fb28
- P2D completion: d46979d2aa52d502915eea2355a64cb788aae4f6
- P2E preregistration: df6f0e285cb176f183930815967e43c36166928a
- P2E held-out execution: e60f5c7d6bb6dd3cf7557d504716d7f13403dd72

Do not assume that any recorded head remains live. Resolve the present PR head, commit, tree, target, mergeability, ancestry, changed files, workflow state, and all AFP-bearing refs before doing anything else.

The central mathematical program concerns a finite positively weighted spherical sample

    Ω_i ∈ S^{d-1},
    w_i > 0,
    sum_i w_i = 1,

and a reversible negative Markov generator

    (Lf)_i = sum_{j≠i} a_{ij}(f_j-f_i),

with shared nonnegative conductances

    γ_{ij}=γ_{ji}≥0,
    a_{ij}=γ_{ij}/w_i,

satisfying

    L1=0,
    LΩ=-(d-1)Ω.

For A∈Sym_0(d), define

    (S_2A)_i = Ω_i^T A Ω_i,
    K_X = ker S_2,
    R_2 = (L+2dI)S_2.

The program defines local residual tensors and losses

    C_i = sum_j a_{ij}(Ω_j-Ω_i)(Ω_j-Ω_i)^T,

    M_i = P_0(C_i+2Ω_iΩ_i^T),

    Z_i = Ω_iΩ_i^T-I/d,

    ε_i = sum_j a_{ij}(1-Ω_i·Ω_j)^2,

    B_i = M_i - [d/(d-1)] ε_i Z_i,

and the sampled quadratic defect

    D_2 = sup_{A∉K_X} ||R_2A||_w / ||S_2A||_w.

The strongest currently defensible mathematical contribution appears to be the exact sampled-quotient formulation, exact residual tensor representation, orthogonal two-defect decomposition, weighted Gram formulas, sharp frontier

    D_2 r_max ≥ d(d-1),

equality and conditional stability theory, exact extremizers, and matching-order constructions in dimensions d=2,3.

The previous audit identified the following major issues:

1. Proposition 7.3, the structured support-preserving robustness result, does not presently have a publication-safe universal certificate.
2. The d=3 construction uses enormous constants such as M_0=2^80 and an even larger robustness constant, making the result mathematically explicit but practically weak.
3. The manuscript contains internal stage language and must be rebuilt as a coherent journal paper.
4. The finite algebraic core is represented in Lean, but the whole paper is not formally verified.
5. P2E is a mixed or negative preregistered result, not a physical success.
6. P2F is an operator-insensitive and reference-inconclusive surrogate, not a demonstrated bounded physical negative.
7. Archive refs are branches rather than intrinsically immutable tags, and publication evidence needs an immutable release structure.

Your task in this prompt is provenance and baseline construction only. Do not yet repair Proposition 7.3 or alter theorem statements.

First resolve and verify:

- the live PR #51 head and exact tree;
- whether the live head differs from b8912c282a22420e8077c75929b16c7a33d189b2;
- ancestry from the accepted P2E execution;
- the exact eight post-P2E commits, if still present;
- every AFP-bearing branch, tag, archive ref, PR, release, workflow, and imported file in both repositories;
- whether any stronger valid descendant has appeared;
- whether any stale, invalid, or superseded theorem was reintroduced;
- whether the 33 Math imports still match the recorded source blobs;
- whether workflow evidence still corresponds to the committed source;
- whether the current target branch can receive the history without dropping AFP commits;
- whether any historical branch or archive ref is mutable;
- whether the repository worktree and submodules, if any, are clean and reproducible.

Create a dedicated repair branch from the strongest valid authoritative descendant. Use a name of the form

    agent/afp-post-audit-repair-<short-live-head>

unless an existing branch with that name would be overwritten. Do not rewrite, delete, retarget, merge, close, or move any historical branch, PR, tag, archive ref, workflow artifact, preregistration, or held-out evidence.

Create and commit:

1. a human-readable authoritative-state report;
2. a machine-readable JSON manifest of every relevant ref;
3. an ancestry and content-difference graph;
4. a theorem-to-file and evidence-to-file dependency inventory;
5. SHA-256 and Git-blob manifests for imported and generated evidence;
6. a list of frozen objects that later prompts must not modify;
7. a list of files authorized for repair;
8. exact environment and reproduction commands;
9. a clean baseline test report;
10. a branch disposition table classifying all relevant refs as authoritative descendant, superseded, invalid ancestry, duplicate, diagnostic only, negative-result evidence, unrelated AFP-adjacent work, or unresolved.

GitHub persistence is mandatory:

- save this exact prompt in the repository;
- commit every report, JSON manifest, graph source, hash manifest, and test log;
- update the AFP current-state, decision-log, theorem-status, next-steps, and artifact-manifest files;
- use small logical commits;
- push the branch;
- open or update a draft PR;
- include the exact branch, commit, tree, PR, and reproduction commands in the final response.

—- Assume for purposes of this task that a unique strongest valid authoritative descendant can be identified from the complete live history. A complete solution must identify it exactly, create the dedicated repair branch, commit the provenance baseline, and demonstrate that the branch contains the required history and evidence without rewriting frozen objects. Partial progress, inspection of PR #51 alone, reliance on a previously committed branch inventory, comparison by filename without Git ancestry, or trust in stage reports is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment such as “N agents for provenance” or “N agents for tests.” Instead, manage the investigation using the following heuristics:

- Begin with genuinely independent repository reconstructions. Some agents should work from refs and commit graphs, some from content hashes, some from pull-request metadata, some from workflow artifacts, and some from theorem and manuscript dependencies.
- Do not tell most agents which branch is expected to be authoritative. Preserve independence so that stale assumptions do not propagate.
- Maintain an explicit registry of provenance hypotheses and ref classifications.
- Require exact commit hashes, tree hashes, parent lists, merge bases, blob hashes, and file-level differences.
- Treat archive names as conventions until their object type and mutability are verified.
- Treat passing CI as evidence about execution only, not correctness.
- Actively search for omitted descendants, duplicated imports, rebased histories, missing parents, and files imported without required context.
- Use adversarial agents to challenge the proposed authoritative line and attempt to identify a stronger or contradictory branch.
- Reject vague reports such as “the branch looks correct.” Every conclusion must be backed by commands, hashes, or exact GitHub metadata.
- The root agent must synthesize conflicting ancestry reconstructions, resolve discrepancies, and rerun checks from a clean clone.
- Do not continue to mathematical repair until the authoritative commit and tree are fixed and the baseline branch is committed.
- Do not return a plan, branch list without classification, or partial repository summary. Return only after the repair branch and complete baseline manifest exist and survive an independent clean-clone verification.

Public search may be used for GitHub metadata or ordinary dependency documentation, but not as a substitute for direct Git and repository inspection.
```

---

# Prompt R1 — Repair Proposition 7.3 and the complete dependent theorem chain

**Recommended environment: Codex Work**

**This is the best use of scarce Codex Work tokens because it addresses the main mathematical blocker in the existing paper.**

```text
Current task statement

PROBLEM

Repair the mathematical blocker in the AFP pure-mathematics flagship concerning the structured support-preserving robustness result currently stated as Proposition 7.3, and make every theorem, corollary, abstract sentence, registry entry, Lean claim, numerical claim, and construction claim that depends on it publication-safe.

Start from the dedicated authoritative repair branch produced by Prompt R0. Resolve its live commit and tree before beginning. Do not assume the branch name or head remains unchanged.

The principal files include, but are not limited to:

- docs/publication_program/p1f_manuscript/FLAGSHIP_MANUSCRIPT.md
- docs/publication_program/P1E_SHORT_GAP_S2_CONSTRUCTION.md
- docs/publication_program/THEOREM_REGISTRY.md
- all P1E construction and hostile-audit scripts;
- all Lean files or documentation that claim support-preserving robustness;
- all abstracts, summaries, tables, stage reports, and appendices referring to Proposition 7.3;
- all tests that currently treat computational guards as a proof of the universal result.

The current construction is an adaptive reflected-ring family on S^2. It preserves positive shared conductances, reversibility, exact H_0⊕H_1 fidelity, a rate bound, and an O(h^2) quadratic defect under the unperturbed construction. Proposition 7.3 attempts to assert a structured perturbation theorem in which:

- ring counts are fixed;
- longitude phases are fixed;
- radial masks are fixed;
- horizontal jump integers are fixed;
- the pole and equator are fixed;
- north-south reflection is preserved;
- northern ring latitudes are perturbed by at most h^3/K_*;
- one common ambient rotation is permitted;
- the moment equations are re-solved;
- positivity and explicit rate and defect bounds persist.

The present proof uses a claimed cancellation-free straight-line differentiation program with at most 10^6 operations and a derivative majorant of the form

    K_* = 2^{28·2^{10^6}}.

The blocker is that the repository does not presently contain a literal, independently checkable expression graph, operation count, complete denominator-separation certificate, interval derivative proof, and positivity certificate sufficient to establish the universal proposition as written.

The required outcome is not necessarily to preserve the present wording. The required outcome is a complete publication-safe theorem chain. There are two acceptable resolution families:

A. Prove Proposition 7.3, or a stronger useful uniform theorem, with a complete exact or verified computer-assisted certificate.

B. Replace Proposition 7.3 by the strongest rigorously proved support-preserving perturbation theorem justified by the construction. This may be a fixed-level theorem, a compact-family theorem, an implicit-function theorem with explicit hypotheses, a local continuity theorem with a computable level-dependent radius, or another exact result. Every dependent claim must be weakened or removed accordingly.

A valid fixed-level replacement must specify:

- the exact finite level or family of levels;
- the fixed support pattern;
- the parameter space;
- the nonlinear system being solved;
- the Jacobian or linearized operator;
- the precise nonsingularity hypothesis;
- the strict positivity margin at the base point;
- the resulting perturbation radius or existence statement;
- whether the constants are explicit, computable, or merely existential;
- the resulting rate and defect conclusions;
- all dependence on level, mass margins, support, sampling, and conditioning.

A valid uniform certified theorem must provide:

- the literal cancellation-free straight-line program or expression DAG;
- an automatically verified operation count;
- exact or outward-rounded interval domains;
- denominator guards for every reciprocal or divided difference;
- determinant, singular-value, or inverse-norm bounds for every solved system;
- derivative bounds for every conductance and weight;
- positivity margins;
- rate and quadratic-defect bounds;
- a small independent certificate verifier;
- reproducible certificate hashes;
- adversarial checks under perturbed signs, masks, phases, and transition locations.

Do not preserve the current enormous constant merely because it is conservative. A very large explicit constant is acceptable only if its derivation is literally certified. An unsupported universal majorant is not publication-safe.

Independently reconstruct the full proof dependency. Determine exactly which later statements require:

- only the unperturbed d=3 construction;
- a fixed-level perturbation theorem;
- a uniform all-level perturbation theorem;
- support preservation;
- explicit constants;
- positivity margins;
- sampling-frame stability;
- graph connectivity;
- rate control;
- quadratic-defect control.

Update all affected files. Remove internal statements that describe an unproved result as accepted or verified. Add exact theorem-status labels to the registry.

Actively test for counterexamples involving:

- perturbations that preserve latitudes but destroy a determinant margin;
- transition rows near the edge of the compact box;
- the pole and equator;
- changes in the shortest meridional gap;
- changes that preserve reflection but alter shared-edge compatibility;
- near-zero conductances;
- loss of positivity;
- loss of reversibility;
- loss of exact coordinate fidelity;
- rate blow-up;
- quotient-conditioning deterioration;
- nonuniform dependence on refinement level.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated repair branch from the live authoritative head;
- commit all proof attempts that produce durable lemmas, exact counterexamples, certificate generators, certificate verifiers, theorem-dependency matrices, and final manuscript repairs;
- preserve failed routes in a clearly labeled research log rather than leaving them only in chat;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push after each major proof milestone;
- open or update a draft PR;
- report exact commit, tree, PR, files, proof status, commands, and unresolved issues.

—- Assume for purposes of this task that a complete publication-safe repair exists. A complete solution must either prove the intended robustness result with a fully checkable certificate or replace it with the strongest correct theorem and revise the entire dependent theorem chain so that no unsupported robustness claim remains. Partial progress, a numerical perturbation sweep, finite verification through any fixed collection of levels, an interval script without a verified expression graph, a continuity assertion without a nonsingularity and positivity argument, or deletion of the proposition without repairing dependent claims is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment such as “N agents for interval arithmetic” or “N agents for the implicit function theorem.” Instead, manage the search using the following heuristics:

- Begin with a genuinely diverse portfolio of approaches: exact symbolic differentiation, interval arithmetic, quantitative implicit-function theorems, condition-number analysis, compactness arguments, perturbation of positive cones, exact rational certification, Taylor models, formal certificate checking, and adversarial counterexample search.
- Do not tell most agents whether the preferred outcome is to preserve or weaken Proposition 7.3. Preserve independence during early rounds.
- Maintain an explicit registry of proof families and their exact missing lemmas.
- Require agents to return literal formulas, matrices, domain boxes, determinant bounds, positivity margins, or exact counterexamples to proposed sublemmas.
- Mark an approach blocked when it relies on an unspecified operation count, a theorem-strength uniform inverse bound, or a compactness assertion with no closed parameter domain.
- Keep both the full-uniform and strongest-correct-weaker routes alive until one survives complete audit.
- Cross-pollinate only after independent derivations have exposed the actual dependency structure.
- Use adversarial agents throughout. Every proposed proof must be attacked for hidden dependence on the refinement level, unsupported denominator guards, circular use of positivity, and silent changes in the support pattern.
- Require a second implementation of any computer-assisted certificate verifier.
- The root agent must repeatedly synthesize, challenge, redirect, and relaunch approaches. Do not stop after the first failed certificate attempt.
- Return only when the manuscript, construction source, theorem registry, tests, formalization claims, and dependency tables all state exactly the theorem that has actually been proved.

Public search may be used for ordinary background on quantitative implicit-function theorems, interval arithmetic, Taylor models, and verified linear algebra, but not to search for a completed solution to this exact AFP robustness problem.
```

---

# Prompt R2 — Replace enormous construction constants by a usable certified \(d=3\) theorem

**Recommended environment: Codex Work**

**Run this after R1 only if the constants remain a serious publication or usefulness problem.**

```text
Current task statement

PROBLEM

Strengthen the AFP d=3 adaptive-ring construction by replacing its astronomically large starting resolution and practically vacuous perturbation constants with a publication-useful, independently certified threshold and explicit moderate-size examples.

Start from the accepted output branch of Prompt R1. Resolve its live head and exact tree before working.

The current d=3 construction uses a reflected adaptive-ring family on S^2 with exact shared conductances, positive rates, exact coordinate fidelity, and an O(h^2) sampled quadratic defect. Its analytic proof presently begins at an enormous base count such as

    M_0 = 2^80,

and the previous robustness formulation used a still larger constant.

The mathematical objective is not merely to produce smaller numbers by numerical experimentation. The objective is a theorem and certificate showing that all required inequalities hold beyond an explicit practical threshold, together with exact or rigorously enclosed verification of the finite range below the asymptotic regime.

The required theorem package must determine explicit constants

    M_min,
    R_3,
    C_3,
    μ_pos,
    κ_max,

or clearly defined analogues, such that for every allowed refinement level and every transition in the construction with M≥M_min:

1. the transition masks are nonnegative;
2. the exact shared-edge systems are nonsingular;
3. all solved conductances are positive with margin at least μ_pos in the stated normalization;
4. the assembled generator is reversible;
5. L1=0 and LΩ=-2Ω hold exactly;
6. the outgoing rate satisfies r_max≤R_3 h^{-2};
7. the sampled quadratic defect satisfies D_2≤C_3 h^2;
8. all polar, transition, ordinary-band, equatorial, and reflected rows are covered;
9. the proof is uniform in the refinement level;
10. the certificate is independently reproducible.

Search for the smallest certifiable M_min that is practical, but do not make optimality a completion requirement. A threshold in the tens, hundreds, or low thousands is strongly preferred. A nontrivial reduction that still leaves the construction unusable must be explicitly justified and compared against the old bound.

Use a hybrid proof strategy if useful:

- exact symbolic cancellation and asymptotic expansion;
- rational inequalities for trigonometric functions;
- outward-rounded interval arithmetic;
- Taylor models with rigorous remainders;
- monotonicity arguments reducing infinite parameter families to boundary boxes;
- exact finite verification below an analytic cutoff;
- exact algebraic treatment of special rows;
- independently verified linear-system certificates.

Produce several concrete meshes at moderate resolution and report:

- node count;
- edge count;
- minimum conductance;
- maximum conductance;
- minimum normalized positivity margin;
- r_max;
- D_2;
- rank of S_2;
- dimension of ker S_2;
- condition number of the deflated sampling Gram matrix;
- whether im S_2 is invariant;
- exact coordinate-fidelity residual;
- exact or certified interval status for every reported identity.

The numerical examples are evidence and usability demonstrations. They do not replace the uniform proof.

If the current construction cannot support a practical threshold, you may modify its ring schedule, transition mask, horizontal jump set, or local solve, provided that:

- shared conductances remain globally compatible;
- support remains uniformly local;
- positivity is proved;
- reversibility is exact;
- coordinate fidelity is exact;
- the rate and defect order remain matching;
- all new formulas and certificates are committed;
- the resulting theorem is no weaker in asymptotic order.

GitHub persistence is mandatory:

- save this exact prompt;
- use a dedicated branch from the accepted R1 head;
- commit symbolic derivations, interval boxes, certificate generators, independent verifiers, finite-check data, exact examples, manuscript changes, and failed construction logs;
- save raw and summarized numerical evidence;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push milestone commits and open or update a draft PR;
- report exact Git state and reproduction commands.

—- Assume for purposes of this task that a nontrivial publication-useful certified improvement exists. A complete solution must prove the improved all-level construction theorem, commit an independently verifiable certificate, generate moderate-size meshes, and update the manuscript, theorem registry, tests, and constants. Partial progress, a floating-point parameter search, verification through finitely many levels without a uniform tail proof, lowering M_0 by assertion, or replacing one enormous unsupported bound by another is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment such as “N agents for interval arithmetic.” Instead, manage the search using the following heuristics:

- Begin with independent approaches based on sharper analytic estimates, interval subdivision, alternative transition masks, monotonicity, symbolic elimination, and construction redesign.
- Do not tell most agents the current favored mask or threshold.
- Maintain an explicit registry of construction families and certificate strategies.
- Require concrete inequalities, interval boxes, determinants, positivity margins, or alternative masks.
- Mark routes blocked when they require an unproved uniform conditioning statement or only succeed at sampled refinement levels.
- Keep both sharpening-the-existing-family and redesigning-the-local-transition routes alive.
- Use adversarial agents to search for rows and parameter boxes where positivity or conditioning is weakest.
- Require two independent implementations of the final certificate checker.
- Test mutations involving sign reversal, omitted weights, incorrect shared-edge factors, wrong transition counts, polar rounding, and altered reflection.
- The root agent must repeatedly synthesize, challenge, refine subdivisions, and relaunch alternative construction ideas.
- Return only when the all-level theorem, finite certificate, moderate meshes, manuscript constants, and regression tests agree exactly.

Public search may be used for standard verified-numerics techniques and trigonometric interval bounds, not to search for a solution to this exact construction.
```

---

# Prompt R3 — Rebuild the pure-mathematics flagship and establish defensible novelty

**Recommended environment: Pro Chat**

**This prompt intentionally contains no multiagent-v2 requirement. Use the unlimited Pro Chat allocation for the literature review, theorem-level comparison, manuscript reconstruction, and editorial work.**

```text
Current task statement

PROBLEM

Reconstruct the AFP pure-mathematics flagship as a coherent, submission-ready journal paper whose theorem statements, proofs, novelty claims, formalization claims, constructions, limitations, and reproducibility record exactly match the repaired mathematics.

Start from the accepted output branch of Prompts R1 and, if completed, R2. Resolve the live head and tree before editing.

The intended mathematical paper is centered on positive reversible generators on finite weighted spherical samples. Its principal objects are

    S_2A = (Ω_i^T A Ω_i)_i,
    K_X = ker S_2,
    R_2 = (L+2dI)S_2,

and the alias-correct sampled defect

    D_2 = sup_{A∉K_X} ||R_2A||_w / ||S_2A||_w.

The central theorem package should include only results that survive complete proof audit:

1. factorization of R_2 through Sym_0(d)/K_X;
2. exact residual representation by local trace-free tensors M_i;
3. exact orthogonal decomposition

       ||M_i||_F^2
       =
       [d/(d-1)] ε_i^2 + ||B_i||_F^2;

4. exact local loss-variance identity;
5. weighted adjoint and Gram formulas;
6. singular-sampling-aware generalized eigenvalues;
7. correct formulas for form-exact, alias, and genuinely sampled exact spaces;
8. the sharp frontier

       D_2 r_max ≥ d(d-1);

9. equality geometry, including rowwise and global reversible conditions;
10. conditional quantitative near-rigidity with every mass, edge, connectivity, sampling, and frame-conditioning parameter exposed;
11. exact extremizers;
12. matching-order local positive constructions only in the dimensions actually proved;
13. the repaired support-preserving theorem from Prompt R1, if retained.

The paper must not claim priority for positive coordinate-exact spherical Laplacians, monotone moment-preserving AFP discretizations, generic eigenpair-preserving graph design, spherical designs, positive cubature, or graph-Laplacian convergence. The novelty claim must be limited to the actual joint delta established by the theorem package.

Conduct a current primary-source prior-art audit. Search by underlying structures and equivalent terminology, not only project-specific phrases. At minimum compare against:

- positive and reversible spherical discrete Laplacians;
- discrete spherical Delaunay Laplacians;
- monotone angular Fokker-Planck discretizations;
- moment-preserving angular diffusion;
- positive meshfree stencils;
- graphical designs;
- eigenpolytope and eigenpair-preserving Laplacian constructions;
- spectrahedral graph design;
- spherical designs and association schemes;
- spectral limitations of positive quadrature;
- graph-Laplacian convergence;
- signed higher-order spherical formulas;
- rigidity and stress-matrix theory where relevant.

For each principal AFP theorem, create an in-paper comparison table containing:

- nearest prior theorem;
- prior hypotheses;
- prior conclusion;
- AFP hypotheses;
- AFP conclusion;
- exact mathematical delta;
- whether the delta is theorem-level novelty, synthesis, technical repair, implementation, or application.

Rebuild the paper as a single mathematical narrative. Remove:

- “accepted P1A,” “accepted P1B,” or similar stage language;
- development chronology that does not aid the proof;
- claims that tests establish theorems;
- claims that the whole paper is formally verified;
- transport-performance claims;
- engineering or HTS claims;
- all-dimensional construction language unless actually proved;
- duplicated theorem statements across stage appendices;
- unsupported claims of firstness.

The revised paper must contain:

1. an accurate title;
2. a restrained abstract;
3. an introduction stating the mathematical obstruction and precise novelty;
4. a conventions section fixing the sign of L, weights, adjoints, quotient metric, and Frobenius normalization;
5. a theorem dependency graph;
6. complete proofs in logical order;
7. a separate equality and global-assembly section;
8. a separate stability section with explicit conditioning assumptions;
9. a construction section restricted to proved dimensions;
10. exact examples and hostile edge cases;
11. a formalization-scope table;
12. a source-to-evidence reproducibility appendix;
13. a limitations section;
14. a prior-art hypothesis comparison;
15. a precise data and code availability statement;
16. no untraceable figures, tables, or numerical values.

Create separate manuscript boundaries for:

- the pure-mathematics paper;
- a future numerical-method paper;
- the P2E negative benchmark note;
- the P2F diagnostic record.

Do not force P2E or P2F into the pure-mathematics paper.

Perform the work in successive independent passes:

1. reconstruct the theorem hierarchy without relying on stage labels;
2. audit every notation and normalization;
3. conduct the primary-source prior-art review without using the authors’ preferred novelty claim;
4. draft at least two competing paper narratives;
5. select the narrative with the strongest theorem-level contribution;
6. run a hostile mathematical-referee pass;
7. run a hostile novelty and journal-editor pass;
8. revise every valid objection;
9. verify that every theorem, proof dependency, citation, limitation, and formalization claim matches the repository.

For every use of “sharp,” “first,” “complete,” “formal,” “all-dimensional,” or “transport relevant,” require exact supporting evidence. Reject any novelty statement that is only a change of notation or a direct application of known machinery.

GitHub persistence is mandatory:

- save this exact prompt;
- use connected GitHub tools to create or update a dedicated manuscript branch and draft PR whenever available;
- commit the manuscript, bibliography, theorem dependency graph, novelty matrix, source comparison table, referee notes, decision log, and paper-splitting plan;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- preserve every substantive literature and editorial conclusion in repository files;
- if direct GitHub writing is unavailable, produce a complete ready-to-commit bundle with exact paths and then use Prompt G0;
- report exact Git state or the exact G0 handoff bundle in the final response.

—- Assume for purposes of this task that the repaired central theorem package has sufficient independent novelty for a specialized mathematics journal. A complete solution must produce a coherent submission manuscript, complete bibliography, theorem dependency map, novelty matrix, source-to-evidence map, and paper-splitting plan whose claims exactly match the proved results. Partial progress, an edited abstract without restructuring, a list of prior papers without theorem-level comparison, retaining internal stage language, or presenting the project repository as the paper is insufficient.

Public search is required for the current prior-art audit. Use primary sources wherever available. Do not rely on search snippets, secondary summaries, or the project’s existing bibliography without verifying the cited theorem.
```

---

# Prompt R4 — Align Lean, tests, artifacts, and reproducible release claims

**Recommended environment: Codex**

```text
Current task statement

PROBLEM

Make the formalization, software, computational evidence, and release package for the AFP pure-mathematics paper exactly match the repaired theorem chain, without describing unformalized mathematics as formally verified or treating tests as proofs.

Start from the accepted output branch of Prompts R1–R3. Resolve the live head and exact tree before working.

Inspect every AFP Lean source file, lakefile, lean-toolchain file, root import, workflow, axiom audit, generated object, Python audit, exact-arithmetic fixture, manuscript formalization claim, and artifact manifest.

Create a theorem correspondence matrix with one row for every manuscript theorem, proposition, lemma, and corollary. Each row must record:

- manuscript identifier;
- manuscript file and line range;
- Lean theorem name, if any;
- Lean source file;
- exact Lean hypotheses;
- exact Lean conclusion;
- any strengthened assumptions;
- any weakened conclusion;
- imported axioms reported by #print axioms;
- whether singular sampling is covered;
- whether noninjective S_2 is covered;
- whether im S_2 invariance is avoided;
- whether the theorem is fully formalized, algebraic-core only, ordinary proof only, or computational only.

The publication-safe formalization statement must be no stronger than the evidence. Unless the full principal theorem chain is actually formalized, use wording of the form:

    A finite algebraic core is machine checked in Lean. The analytic construction, stability transfer, geometric classification, optimization, and transport results remain ordinary mathematics or computation.

Verify and enforce:

- no sorry;
- no admit;
- no sorryAx;
- no placeholder theorem;
- no unsafe escape;
- no opaque project-specific axiom;
- no committed .olean file masking a missing source;
- every claimed module is imported by the declared build or explicitly built in CI;
- the root build succeeds from a clean checkout;
- exact axiom reports are committed;
- theorem names in the manuscript resolve to actual Lean declarations;
- singular and aliased examples are included wherever the manuscript claims they are formalized.

Formalize additional central finite algebra if this can be done without distorting the ordinary theorem. Prioritize:

1. the sampling quotient;
2. K_X⊆ker R_2;
3. weighted adjoints;
4. singular Gram pencils;
5. rank and dimension formulas;
6. the exact two-defect identity;
7. the local loss-variance identity;
8. equality implications that are genuinely finite algebra.

Do not spend the task formalizing peripheral numerical fixtures while leaving a central manuscript-to-Lean mismatch.

Rebuild computational reproducibility. Produce:

- a clean container or equivalent pinned environment;
- exact Python, Lean, solver, BLAS, and system dependency versions;
- one top-level command that builds Lean;
- one command that runs exact mathematical audits;
- one command per manuscript table and figure;
- raw evidence and generated evidence directories;
- a source-to-output manifest;
- SHA-256 hashes;
- deterministic status or explicit tolerances;
- an independent verifier for any computer-assisted proof certificate;
- a clean-clone reproduction report.

Prepare immutable publication assets:

- a signed release-candidate tag;
- a manuscript source archive;
- the compiled PDF;
- exact code and evidence;
- environment lock files;
- a complete hash manifest;
- a CITATION file;
- a release note describing formalization scope;
- a DOI-deposit-ready archive.

Do not fabricate a DOI or claim an external deposit that has not occurred. If external credentials are unavailable, prepare the exact deposit bundle and record the remaining mechanical external step.

Preserve all preregistered P2E and historical evidence byte-for-byte. Do not regenerate frozen evidence under a new environment and silently replace it.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated formalization and release branch or continue the designated repair branch without mixing unrelated work;
- commit theorem correspondence tables, Lean source, axiom reports, build logs, container files, lock files, scripts, generated tables and figures, release manifests, and clean-room reproduction reports;
- push logical milestone commits;
- open or update a draft PR;
- create signed tags only when the repository policy and credentials permit and only after verification;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- report exact commit, tree, PR, tag status, build commands, and unresolved external steps.

—- Assume for purposes of this task that every formalization and reproducibility mismatch can be resolved without weakening the repaired principal theorem. A complete solution must align every manuscript formalization claim with actual Lean declarations, pass clean builds, eliminate unbuilt or falsely advertised modules, produce a reproducible release bundle, and document exactly what remains ordinary mathematics. Partial progress, a successful local lake build, a no-sorry grep without theorem correspondence, or an environment file without clean-clone reproduction is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment. Instead, manage the work using the following heuristics:

- Begin with independent Lean theorem auditors, build-system auditors, manuscript-to-formalization comparators, reproducibility agents, and hostile clean-room reproducers.
- Do not tell auditors which theorems are believed to be formalized.
- Maintain an explicit mismatch registry.
- Require exact theorem signatures and axiom reports.
- Treat passing CI as necessary but not sufficient.
- Use adversarial agents to search for strengthened hypotheses, weakened conclusions, unimported modules, stale generated objects, and tests that succeed for the wrong reason.
- Require at least one reproduction from a clean checkout with no preexisting Lean cache.
- Require a second implementation or verifier for any certificate that supports a theorem.
- Mark formalization routes blocked if they only encode an injective or full-rank special case while the manuscript claims singular sampling.
- The root agent must revise either the Lean code or the manuscript claim whenever a mismatch is found.
- Return only when the theorem correspondence matrix, clean builds, evidence hashes, release bundle, and manuscript wording agree exactly.

Public search may be used for official Lean and dependency documentation only. Do not use external summaries as evidence of what the repository formalizes.
```

---

# Prompt B0 — Correct P2E/P2F and build a genuinely operator-sensitive benchmark

**Recommended environment: Codex**

**Use Codex rather than scarce Codex Work tokens for the implementation. The response theorem in N2 should guide the benchmark if N2 has already been completed.**

```text
Current task statement

PROBLEM

Preserve the frozen P2E and P2F evidence without post-hoc tuning, correct every overstatement in their scientific interpretation, and develop a new preregistered benchmark capable of detecting whether AFP generator improvements change transport responses.

Start from the authoritative repair branch. Resolve the live head and tree. Do not alter the frozen P2E preregistration, held-out inputs, original workflow artifact, or recorded outputs.

The frozen P2E result must continue to be described as follows unless direct evidence proves otherwise:

- angular geometric-mean ratio approximately 0.6715;
- median response ratio approximately 1.0000;
- 3/7 cases improved by at least 5%;
- worst response ratio approximately 8.0684;
- overall response-error geometric mean approximately 1.1262;
- physical-case geometric mean approximately 1.6597;
- acceleration iterations 17 versus 23;
- the preregistered worst-response value gate failed;
- the iteration count improved;
- the HTS difference was unresolved relative to reference uncertainty.

Do not reinterpret the failed value gate as success. Do not call iteration reduction a wall-time improvement without an equal-work timing study. Do not tune the method and rerun the same held-out cases.

The frozen P2F surrogate currently reports zero resolved optimized improvements among 18 selected comparisons. The previous audit found that:

- several selected quantities are neutral-dominated or structurally unchanged;
- the baseline and optimized charged responses are nearly identical;
- the selected responses are effectively insensitive to the generator replacement;
- the grazing angular reference is not demonstrably converged;
- the 18 quantities are correlated and are not 18 independent trials;
- the result is not evaluated-data or production HTS physics.

Replace the classification BOUNDED_NEGATIVE by publication-safe wording such as:

    OPERATOR_INSENSITIVE_AND_REFERENCE_INCONCLUSIVE

or an equivalent term justified by the evidence.

The first part of the task is correction and preservation:

1. verify frozen hashes;
2. reconstruct all P2E statistics from raw evidence;
3. reconstruct all P2F response comparisons;
4. compute and document response correlations;
5. quantify neutral versus charged contribution;
6. reproduce the grazing-reference nonconvergence;
7. update every manuscript, README, PR description, table, registry, and abstract that overstates P2E or P2F;
8. preserve the negative and inconclusive results without deletion.

The second part is a new benchmark program. Develop a benchmark-sensitivity theory and implementation before preregistering new held-out tests.

For a linear discrete system

    A(L)u=q,

with response

    J(u)=c^T u,

derive and verify the adjoint sensitivity

    DJ(L)[δL] = -z^T [D_LA(L)[δL]]u,

where

    A(L)^T z = c.

Use this derivative or a rigorously controlled finite perturbation analogue to determine whether a candidate response is capable of distinguishing

    δL = L_opt-L_base.

Define a preregistered sensitivity gate of the form

    |DJ(L)[δL]| ≥ c_gate u_ref

or another justified criterion, where u_ref is the total angular, spatial, energy, and solver reference uncertainty.

A case that fails the sensitivity gate must not be used to claim evidence for or against AFP.

The new benchmark suite must contain:

- manufactured solutions with known angular spectra;
- charged-particle-dominated forward-peaked cases;
- interface-localized responses;
- escape or leakage responses sensitive to angular diffusion;
- responses involving degrees above H_2;
- several beam orientations;
- grazing-sensitive cases;
- at least one case where H_2 improvement should help;
- at least one case predicted to be insensitive;
- at least one case stressing higher harmonics;
- clearly separated training, pilot, and held-out sets.

The reference program must use:

- at least four angular resolutions;
- more than one node family;
- rotations of beams relative to nodes;
- spatial refinement;
- energy refinement if energy is present;
- independently selected solver tolerances;
- convergence diagnostics before uncertainty is assigned;
- rotation-averaged or randomized-ordinate comparisons where appropriate;
- raw data and exact aggregation scripts.

The new preregistration must be frozen before executing held-out cases. It must specify:

- primary and secondary hypotheses;
- exact metrics;
- sensitivity gate;
- uncertainty construction;
- equal-work and wall-time protocols;
- pass, fail, negative, mixed, and inconclusive classifications;
- multiplicity handling;
- no-retuning rule;
- one-time held-out execution rule;
- exact stopping criteria;
- exact software environment and hashes.

Only after the preregistration is frozen may the held-out suite be run once.

Do not claim that AFP replaces neutral Boltzmann collision physics, nuclear reactions, evaluated neutron or photon transport, recoil spectra, DPA, defect survival, annealing, or superconducting-property degradation.

GitHub persistence is mandatory:

- save this exact prompt;
- create separate branches or commits for frozen-evidence correction, pilot development, preregistration freeze, and held-out execution;
- never modify frozen evidence in place;
- commit raw inputs, raw outputs, aggregation code, sensitivity calculations, convergence data, preregistration, environment locks, hashes, and reports;
- tag or otherwise immutably identify the preregistration before held-out execution;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push every milestone and maintain a draft PR;
- report exact commit and tree for both the frozen preregistration and held-out execution.

—- Assume for purposes of this task that an operator-sensitive, reproducible benchmark suite can be constructed without modifying the frozen P2E/P2F evidence. A complete solution must correct the old interpretations, derive and validate the sensitivity gate, freeze a new preregistration, execute the held-out suite once, report all outcomes including failures, and produce reproducible raw evidence. Partial progress, additional runs of the frozen held-out cases, a benchmark whose predicted signal is below reference uncertainty, two-resolution angular comparison without convergence evidence, or a list of proposed cases without implementation is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment. Instead, manage the work using the following heuristics:

- Begin with independent statistical auditors, adjoint analysts, numerical transport specialists, reference-convergence auditors, and hostile benchmark designers.
- Do not tell benchmark designers which cases are expected to favor AFP.
- Maintain an explicit registry of candidate cases and predicted operator sensitivities.
- Reject cases whose responses are dominated by unchanged physics unless that insensitivity is the preregistered purpose of the case.
- Require concrete forward equations, adjoint equations, response derivatives, uncertainty budgets, and convergence plots.
- Mark a case blocked if it lacks a converged reference or if the predicted signal is below uncertainty.
- Keep manufactured, controlled-physics, and application-oriented routes separate.
- Use adversarial agents to rotate beams, perturb quadratures, refine angular levels, and search for aliasing.
- Require independent reaggregation of all reported summary statistics.
- The root agent must freeze the preregistration before revealing held-out results and must not relaunch the held-out suite after seeing them.
- Return only when frozen evidence, corrected interpretation, sensitivity theory, preregistration, held-out execution, and reproducibility package are complete.

Public search may be used for primary literature on adjoint sensitivity, goal-oriented transport error estimation, randomized ordinates, and angular convergence. Do not search for or tune against the hidden held-out outcomes.
```

---

# Prompt N1 — Develop the exact degree-three harmonic theory

**Recommended environment: Codex Work**

```text
Current task statement

PROBLEM

Develop a complete alias-correct degree-three theory for positive reversible spherical generators, determining whether the AFP degree-two residual geometry is the first case of a genuine harmonic hierarchy or a special quadratic phenomenon.

Let I be finite, let w_i>0 with sum_i w_i=1, and let Ω_i∈S^{d-1}. Let L be a reversible negative Markov generator with shared nonnegative conductances satisfying

    L1=0,
    LΩ=-(d-1)Ω.

Let STF^3(R^d) denote the symmetric trace-free rank-three tensors. For T∈STF^3(R^d), define

    (S_3T)_i = T[Ω_i,Ω_i,Ω_i],

    K_{3,X} = ker S_3,

    R_3 = (L+3(d+1)I)S_3,

because the degree-three spherical-harmonic eigenvalue is -3(d+1).

Define the alias-correct sampled cubic defect

    D_3
    =
    sup_{T∉K_{3,X}}
    ||R_3T||_w / ||S_3T||_w.

The task is to determine and prove the complete correct degree-three theorem package.

At minimum, derive:

1. K_{3,X}⊆ker R_3 and factorization through STF^3(R^d)/K_{3,X};
2. the correct sampled quotient metric;
3. the weighted adjoints of S_3 and R_3;
4. singular-sampling-aware Gram formulas;
5. rank and dimension formulas for aliases, form-exact tensors, and genuinely sampled exact cubic modes;
6. an exact local residual tensor M_i^{(3)} satisfying

       (R_3T)_i = <T,M_i^{(3)}>,

   with the exact projection onto STF^3(R^d);

7. the irreducible decomposition of M_i^{(3)} under the stabilizer of Ω_i;
8. an exact orthogonal or representation-theoretic sum-of-squares decomposition of ||M_i^{(3)}||^2;
9. identification of all scalar, mixed radial-tangential, and purely tangential defect components;
10. the relation of those components to moments of the angular losses and chord increments;
11. the sharp positivity-stiffness lower bound for D_3, if one exists;
12. the best possible constant and normalization;
13. equality conditions;
14. near-equality or stability theory;
15. exact extremizers or a complete obstruction to extremizers;
16. positive constructions or a proof that matching constructions cannot exist under the proposed hypotheses;
17. exact degenerate, duplicated, antipodal, aliased, disconnected, and singular-sampling examples.

Do not assume that a direct analogue

    D_3 r_max ≥ C(d)

must be true. Determine the correct scaling and whether the stiffness variable should be r_max, a higher local moment, or a combined quantity.

If the anticipated universal inequality is false, a complete solution must provide:

- the smallest exact counterexample available;
- proof that it satisfies every stated hypothesis;
- identification of the failed mechanism;
- the strongest corrected theorem;
- a sharp constant or an exact reason sharpness is unavailable;
- a replacement equality and construction theory.

Use representation theory only when every projection, multiplicity, norm, and normalization is written explicitly. Do not replace the proof by the phrase “decompose into irreducibles.”

Use exact arithmetic and symbolic computation for discovery and regression, but not as a substitute for an all-orders theorem.

Implement:

- exact tensor-basis code;
- quotient and Gram computations;
- singular examples;
- mutation tests;
- candidate extremizer search;
- exact certificate scripts;
- a theorem registry;
- a standalone manuscript;
- a Lean formalization of the finite algebraic core where feasible.

Actively test:

- sign reversal of L;
- use of L-3(d+1)I;
- omitted weights;
- Frobenius quotient instead of sampled quotient;
- compression to im S_3;
- noninjective S_3;
- zero sampled cubic module;
- duplicated and antipodal nodes;
- hypercubes, simplices, cross-polytopes, association-scheme examples, and asymmetric graphs;
- dimensions d=2,3,4 and higher;
- generators with exact H_1 but highly distorted H_2 and H_3 behavior.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated research branch and draft PR;
- commit every durable lemma, tensor formula, counterexample, exact fixture, failed approach registry, symbolic script, certificate, theorem registry, Lean file, and manuscript;
- preserve unsuccessful theorem formulations with exact counterexamples in a negative-results file;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push at every major mathematical milestone;
- report exact commit, tree, PR, proof status, and reproduction commands.

—- Assume for purposes of this task that a complete exact degree-three theory exists, although its final form may be a sharp positive theorem or a sharp obstruction theorem. A complete solution must determine the correct theorem, prove it, classify equality or failure, handle singular sampling, implement exact regression evidence, and produce a publication-ready manuscript. Partial progress, a formal residual expansion without a sharp structural result, finite verification, a reduction to an unproved representation-theoretic inequality, or an unclassified counterexample is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment such as “N agents for tensors.” Instead, manage the search using the following heuristics:

- Begin with diverse approaches: STF tensor calculus, polarization identities, harmonic representation theory, local moment problems, semidefinite geometry, positivity inequalities, association schemes, extremal graph constructions, conic duality, and computational counterexample search.
- Do not tell most agents the expected form of the bound.
- Maintain an explicit registry of approach families and candidate invariants.
- Reject elegant reductions that end at a lemma equivalent in strength to the original degree-three problem.
- Mark a route blocked when it needs an unproved global compatibility or decomposition coefficient.
- Keep incompatible routes alive, including the possibility that the quadratic frontier does not generalize.
- Require concrete tensors, projection formulas, constants, exact examples, or exact counterexamples.
- Use adversarial agents to mutate signs, weights, kernels, norms, dimensions, and graph connectivity.
- Require two independent derivations of the local tensor formula and the final sharp constant.
- The root agent must repeatedly synthesize, challenge, redirect, and relaunch new mechanisms.
- Do not return merely because a natural D_3 r_max inequality fails. Continue until the strongest correct replacement theorem is proved and audited.
- Return only when a complete degree-three theorem package survives hostile proof checking.

Public search may be used only for ordinary background on spherical harmonics, STF tensors, association schemes, and standard representation theory. Do not search for a solution to this exact AFP degree-three problem.
```

---

# Prompt N2 — Prove a response-certified harmonic-fidelity theorem

**Recommended environment: Codex Work**

**This is the highest-value new mathematical program because it directly addresses why a lower \(D_2\) did not consistently improve transport responses.**

```text
Current task statement

PROBLEM

Develop a rigorous response-error theory connecting AFP harmonic defects to transport observables, and use it to construct a goal-oriented optimization principle for positive reversible angular generators.

The central scientific problem is that reducing the global quadratic defect D_2 did not consistently reduce physical response errors in P2E or P2F. The new theory must explain when harmonic fidelity affects a specified response and when it does not.

Consider a well-posed linear steady transport or angular Fokker-Planck problem on a bounded spatial domain with specified inflow or interface boundary conditions. Use a model broad enough to cover the AFP angular generator but narrow enough for a complete theorem.

Let the continuous or reference problem be

    A u = q,

and let the discrete angular problem using generator L be

    A_h(L)u_h = q_h.

Let the response be a bounded linear functional

    J(u)=<c,u>,

and let z or z_h denote the associated adjoint solution.

For every harmonic degree ℓ, define

    S_ℓ : H_ℓ → R^I,

    K_{ℓ,X}=ker S_ℓ,

    R_ℓ=(L+λ_ℓ I)S_ℓ,

    λ_ℓ=ℓ(ℓ+d-2),

and

    D_ℓ
    =
    ||R̄_ℓ:
      H_ℓ/K_{ℓ,X} → l^2(w)||.

The objective is a theorem of the schematic form

    |J(u)-J_h(u_h)|
    ≤
    C_stab
    [
      sum_{ℓ=2}^p α_ℓ(u,z) D_ℓ
      +
      Tail_{>p}(u,z)
      +
      E_space
      +
      E_energy
      +
      E_solver
    ],

with every quantity precisely defined and with hypotheses strong enough to make the estimate correct but not so strong that the result becomes vacuous.

The theorem must distinguish:

- aliasing from operator error;
- leakage outside im S_ℓ from compressed residual error;
- forward harmonic content from adjoint harmonic content;
- angular error from spatial, energy, and solver error;
- a priori bounds from computable a posteriori estimates;
- global harmonic metrics from response-weighted metrics.

Derive an exact or rigorously controlled adjoint identity. For a discrete linear system

    A(L)u=q,
    A(L)^T z=c,

derive

    DJ(L)[δL]
    =
    -z^T [D_LA(L)[δL]]u,

and connect this derivative to harmonic residual components.

The result must not be a generic restatement of the dual-weighted residual method. The novel theorem must use the AFP structure:

- positive reversible generators;
- exact H_0⊕H_1 fidelity;
- sampled harmonic quotients;
- singular sampling;
- the D_ℓ defects;
- leakage outside sampled harmonic ranges;
- response-specific forward-adjoint harmonic coupling.

Determine whether the natural response weight for degree ℓ is:

- a product of forward and adjoint harmonic norms;
- an operator-dependent coupling matrix;
- a local or interface-weighted quantity;
- a resolvent-weighted defect;
- another exactly derived object.

Prove both:

1. an a priori theorem involving harmonic regularity and D_ℓ;
2. an a posteriori or computable sensitivity theorem using discrete forward and adjoint solutions.

Then construct a goal-oriented positive-generator design problem such as

    minimize over γ_{ij}≥0
        sum_{ℓ=2}^p α_ℓ D_ℓ^2
        + β Φ_stiffness
        + η Φ_conditioning

subject to

    reversibility,
    L1=0,
    LΩ=-(d-1)Ω,
    graph or support constraints.

Determine which parts are convex, quasiconvex, semidefinite representable, or nonconvex. Produce primal-dual certificates for the convex subproblems.

Implement and test the theorem on:

- manufactured solutions with known harmonic degree;
- a response controlled mainly by H_2;
- a response controlled mainly by H_3 or higher;
- an interface-localized response;
- a case predicted to be insensitive;
- a case with singular S_2 or S_3;
- a case with leakage outside im S_ℓ;
- a transport acceleration problem;
- a charged forward-peaked problem.

For every test, compare:

- unweighted D_2 optimization;
- multi-degree optimization;
- response-weighted optimization;
- the existing monotone baseline;
- a high-resolution reference.

The numerical experiments must test the theorem rather than substitute for it.

Actively search for failure modes:

- nonnormal transport operators;
- inadequate adjoint regularity;
- grazing singularities;
- unresolved boundary layers;
- near-zero absorption;
- long path lengths;
- interface discontinuities;
- noninjective sampling;
- harmonic tails not controlled by finitely many D_ℓ;
- reference uncertainty larger than the predicted method difference.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated theorem-and-implementation branch and draft PR;
- commit all theorem formulations, failed bounds, exact counterexamples, proof dependencies, forward and adjoint derivations, optimization formulations, primal-dual certificates, tests, raw data, and manuscript text;
- save failed theorem routes when they clarify necessary hypotheses;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push after every substantial theorem or implementation milestone;
- report exact Git state, proof status, test commands, and unresolved gaps.

—- Assume for purposes of this task that a nonvacuous AFP-specific response theorem and a certifiable goal-oriented design principle exist for a precisely stated transport class. A complete solution must define that class, prove the forward and adjoint estimates, derive the AFP-specific harmonic coupling, implement the certified optimization, and validate it on operator-sensitive tests. Partial progress, a generic adjoint identity with no D_ℓ connection, a numerical correlation study, an unproved regularity assumption, or optimization without a response-error theorem is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment. Instead, manage the search using the following heuristics:

- Begin with diverse approaches: resolvent identities, dual-weighted residuals, harmonic block decompositions, semigroup estimates, energy methods, pseudospectral analysis, perturbation theory, operator interpolation, and local interface estimates.
- Do not tell most agents the expected form of α_ℓ.
- Maintain a registry of theorem formulations, norms, and stability hypotheses.
- Reject estimates whose constants hide the entire difficulty or become infinite in the intended regime.
- Mark routes blocked when they require unproved harmonic regularity or assume im S_ℓ invariance.
- Keep a priori, a posteriori, resolvent, and sensitivity routes alive in parallel.
- Require concrete inequalities, operator domains, boundary terms, constants, and counterexamples to proposed bounds.
- Use adversarial agents to construct cases where D_2 improves but the response does not.
- Require independent derivations of the adjoint derivative and the final response bound.
- The root agent must repeatedly synthesize, challenge, refine the transport class, and launch new proof rounds.
- Do not return a generic framework. Return only when the AFP-specific theorem, optimization, certificates, and tests form a complete publication-ready result.

Public search may be used for ordinary primary-source background on goal-oriented error estimation, angular adaptivity, harmonic transport analysis, and randomized ordinates. Do not search for a solution to this exact AFP response-certification problem.
```

---

# Prompt N3 — Develop conic feasibility, obstruction, and robustness theory

**Recommended environment: Codex Work**

```text
Current task statement

PROBLEM

Develop a complete geometric and conic-duality theory for the existence, sparsity, robustness, and conditioning of positive reversible spherical generators satisfying exact coordinate fidelity.

Let Ω_i∈S^{d-1}, let w_i>0 with sum_iw_i=1, and let G=(I,E) be a prescribed undirected support graph.

For each edge {i,j}∈E, let γ_{ij}=γ_{ji}≥0 be the shared conductance and define

    a_{ij}=γ_{ij}/w_i,

    (Lf)_i=sum_{j:{i,j}∈E} a_{ij}(f_j-f_i).

The exact coordinate-fidelity equations are

    sum_j γ_{ij}(Ω_j-Ω_i)
    =
    -(d-1)w_iΩ_i

for every vertex i.

Write the full system as

    A_X γ = b_X,
    γ≥0.

The task is to derive and prove a necessary-and-sufficient geometric feasibility theorem, not merely to observe that this is a linear program.

At minimum establish:

1. an exact Farkas-dual infeasibility criterion;
2. a geometric interpretation of every dual certificate;
3. the role of global force and torque identities, if any;
4. the relation to equilibrium stresses and rigidity theory;
5. the effect of duplicated and antipodal nodes;
6. the effect of disconnected support;
7. necessary support-size and degree bounds;
8. sufficient conditions for connected feasible support;
9. a quantitative interior-feasibility margin;
10. perturbation stability with explicit dependence on that margin;
11. Lipschitz or Hölder continuity of feasible conductances under node and weight perturbation;
12. sparse-support bounds using conic Carathéodory or a sharper structure-specific result;
13. uniqueness and dimension of the feasible conductance cone;
14. characterization of extreme rays or extreme feasible generators;
15. conditioning of the moment equations;
16. interaction between feasibility margin, r_max, and D_2;
17. exact infeasibility certificates that can be verified independently.

A candidate dual formulation has the schematic form:

for every vertex vector field y=(y_i) satisfying an edge monotonicity condition such as

    (y_i-y_j)·(Ω_j-Ω_i) ≥ 0

on every allowed edge, a corresponding weighted radial pairing must have the correct sign.

Derive the exact sign, normalization, equality conditions, and whether additional quotienting by rigid motions or redundant constraints is required. Do not assume the schematic form is already correct.

The strongest theorem should distinguish:

- feasibility;
- strict feasibility;
- connected strict feasibility;
- feasibility with bounded r_max;
- feasibility with a prescribed positivity margin;
- feasibility compatible with additional H_2 objectives.

Construct exact certificates for:

- a feasible simplex;
- a cross-polytope;
- a hypercube;
- a duplicated-node failure;
- an antipodal configuration;
- a disconnected graph;
- a graph that is locally feasible but globally incompatible;
- a near-degenerate configuration with vanishing feasibility margin;
- a support graph requiring more edges than a naive dimension count predicts.

Implement:

- an exact primal solver for rational or algebraic examples;
- an exact dual-certificate verifier;
- a floating-point solver that emits rational or interval certificates;
- condition and margin diagnostics;
- mutation tests;
- a standalone manuscript.

Determine whether the feasibility theory yields a new proof or strengthening of any AFP robustness or construction result. Do not fold it into the existing paper unless the theorem dependency remains clear.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated research branch and draft PR;
- commit all dual derivations, sign checks, quotient choices, exact certificates, counterexamples, solver code, verifier code, conditioning data, theorem registry, and manuscript drafts;
- preserve false candidate duals with exact counterexamples;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push every major milestone;
- report exact Git state, theorem status, certificates, and commands.

—- Assume for purposes of this task that a complete geometric conic-duality theorem exists and has independent publication value. A complete solution must prove exact primal-dual equivalence, interpret the dual geometrically, establish quantitative margins and perturbation stability, handle connectivity and degeneracy, and implement independently verifiable certificates. Partial progress, writing down the linear program, citing Farkas’ lemma without deriving the structure-specific dual, finite feasibility tests, or a robustness statement with an unspecified condition number is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment. Instead, manage the search using the following heuristics:

- Begin with approaches from conic duality, rigidity stresses, network flows, oriented matroids, convex geometry, equilibrium measures, graph sparsification, and perturbation analysis.
- Do not tell most agents the proposed dual inequality.
- Maintain a registry of dual formulations and geometric interpretations.
- Reject routes that only rename Farkas multipliers without extracting a usable theorem.
- Mark approaches blocked when global compatibility is called routine but not proved.
- Keep algebraic, geometric, and combinatorial routes alive.
- Require explicit dual certificates, support bounds, perturbation constants, or exact counterexamples.
- Use adversarial agents to test duplicates, antipodes, disconnection, tiny margins, and near-rank loss.
- Require independent primal and dual certificate verifiers.
- The root agent must repeatedly synthesize, challenge signs and quotient spaces, and relaunch alternative formulations.
- Return only when the exact theorem, certificates, edge cases, and manuscript survive hostile audit.

Public search may be used for standard background on Farkas duality, stress matrices, rigidity, and conic Carathéodory theorems. Do not search for a solution to this exact spherical-generator feasibility problem.
```

---

# Prompt N4 — Develop half-range and interface-aware AFP theory

**Recommended environment: Codex Work**

```text
Current task statement

PROBLEM

Develop a mathematically complete half-range and interface-aware theory for positive angular generators in layered transport, with special attention to grazing incidence and streaming.

The current AFP theory is based primarily on full-sphere sampling and global harmonic fidelity. Layered transport and material interfaces instead distinguish incoming and outgoing angular half-spaces relative to an interface normal n.

Let

    S_n^+ = {Ω∈S^{d-1}: Ω·n>0},
    S_n^- = {Ω∈S^{d-1}: Ω·n<0}.

Relevant flux measures involve weights such as

    |Ω·n| dΩ,

rather than only the uniform spherical measure.

Construct a coupled mathematical framework containing:

1. an interior positive reversible angular generator L;
2. incoming and outgoing half-range sampling operators;
3. half-range sampling kernels and quotient metrics;
4. a positive interface transmission-reflection operator T;
5. exact mass conservation;
6. exact normal-current balance;
7. material-interface reciprocity or detailed balance;
8. compatibility between L and T;
9. positivity and monotonicity of the fully coupled discretization;
10. stability as Ω·n approaches zero;
11. a mathematically explicit treatment of grazing directions;
12. singular and aliased half-range sampling;
13. interface-local harmonic or polynomial fidelity;
14. a sharp feasibility, stiffness, or grazing-resolution theorem.

Define half-range sampling maps such as

    S_{ℓ,n}^± : H_ℓ → R^{I_±},

and corresponding kernels

    K_{ℓ,X}^{n,±}=ker S_{ℓ,n}^±.

Determine the correct quotient metric, which may involve the discrete analogue of |Ω·n|dΩ.

The central theorem should establish either:

A. a positive construction satisfying exact low-order half-range moment and interface conditions with explicit stiffness and accuracy bounds;

or

B. a sharp impossibility theorem showing that positivity, bounded stiffness, exact half-range moments, and uniform grazing resolution cannot all hold simultaneously under the stated support or node constraints.

A complete obstruction theorem is acceptable only if it gives the strongest corrected constructive regime.

The theory must distinguish:

- interior angular diffusion;
- neutral collision physics;
- interface transmission and reflection;
- incoming versus outgoing sampling;
- grazing resolution;
- spatial upwinding;
- curved geometry;
- finite tape-edge escape.

Do not claim that the interface operator replaces Boltzmann collision or nuclear-reaction physics.

Investigate:

- specular reflection;
- diffuse reflection;
- material-dependent transmission;
- reciprocal kernels;
- multiple adjacent layers;
- discontinuous angular diffusion coefficients;
- repeated interfaces;
- thin-layer limits;
- oblique and grazing beams;
- duplicate or missing near-grazing nodes;
- nonmatching node sets across an interface;
- rotation of the quadrature relative to n.

Prove the coupled mass and current identities exactly. Determine when the combined spatial-angular matrix is an M-matrix or generates a positive semigroup.

Develop exact examples and hostile counterexamples. Implement a controlled benchmark only after the theorem is complete. The benchmark should use manufactured interface solutions or a rigorously converged reference before any HTS interpretation.

GitHub persistence is mandatory:

- save this exact prompt;
- create a dedicated research branch and draft PR;
- commit every interface formulation, measure choice, conservation identity, dual obstruction, exact example, counterexample, proof, implementation, benchmark specification, and manuscript draft;
- preserve failed constructions and their exact failure mechanisms;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- push at each theorem or implementation milestone;
- report exact Git state, theorem status, tests, and reproduction commands.

—- Assume for purposes of this task that a complete publishable half-range/interface theorem exists, either as a sharp construction theorem or as a sharp obstruction with a corrected constructive regime. A complete solution must define the correct half-range quotients, prove conservation, reciprocity, positivity, and grazing behavior, handle nonmatching and singular samples, and produce exact examples and a standalone manuscript. Partial progress, an interface matrix chosen by numerical fitting, a full-sphere moment argument reused without half-range weights, finite tests, or an HTS surrogate without a theorem is insufficient.

Use multiagent v2 aggressively and dynamically. Do not use a fixed assignment. Instead, manage the search using the following heuristics:

- Begin with diverse approaches from half-range harmonic analysis, kinetic boundary operators, Markov coupling, optimal transport, positive cubature, interface finite-volume methods, reciprocity theory, and grazing asymptotics.
- Do not tell most agents whether a construction or obstruction is expected.
- Maintain a registry of interface formulations, measures, and conservation laws.
- Reject formulations that hide the grazing singularity by excluding Ω·n≈0 without stating a resolution theorem.
- Mark routes blocked when they assume matching quadratures or exact half-range cubature without proof.
- Keep constructive and impossibility routes alive.
- Require exact interface matrices, moment equations, dual obstructions, constants, or counterexamples.
- Use adversarial agents to rotate nodes, remove grazing directions, mismatch interfaces, and create thin layers.
- Require independent checks of mass, current, positivity, reciprocity, and M-matrix structure.
- The root agent must repeatedly synthesize, challenge, and relaunch alternative formulations.
- Return only when a complete half-range/interface theorem and its exact computational realization survive hostile audit.

Public search may be used for ordinary primary-source background on kinetic boundary conditions, half-range moments, reciprocity, and positive interface discretization. Do not search for a solution to this exact AFP interface problem.
```

---

# Prompt F0 — Final hostile review, revision, and submission gate

**Recommended environment: Pro Chat**

**This prompt intentionally contains no multiagent-v2 requirement. Use Pro Chat for independent referee passes, current literature review, manuscript criticism, and response-to-referees drafting. Send any concrete code or Lean repair found during review to Codex, then persist the completed review with Prompt G0 if direct GitHub writing is unavailable.**

```text
Current task statement

PROBLEM

Subject the repaired AFP publication package to a hostile independent mathematical, formal, computational, novelty, and reproducibility review, revise every valid defect, and produce the final submission decision and artifacts.

The minimum inputs are the accepted outputs of:

- R0: authoritative live-state baseline;
- R1: Proposition 7.3 repair;
- R3: rebuilt pure-mathematics manuscript;
- R4: Lean and reproducibility alignment.

Include R2 if the practical d=3 constant reduction was completed.

Do not require completion of N1–N4 for submission of the existing quadratic paper. Those are separate research programs.

Resolve the live repository head, exact commit, tree, branch, target, and clean status before auditing. Use a dedicated final-review branch. Do not merge, close, retitle, delete, or rewrite historical branches or frozen evidence.

Conduct separate independent referee passes from the perspectives of:

1. discrete and computational harmonic analysis on spheres;
2. graph Laplacians and reversible Markov generators;
3. spherical designs, positive cubature, and association schemes;
4. rigidity, stress matrices, and conic geometry;
5. numerical analysis and verified computation;
6. formal verification in Lean;
7. reproducible computational mathematics;
8. applied mathematics journal editing.

Do not allow a later referee pass to see the conclusions of an earlier pass until it has produced its own exact findings. Do not tell the reviews the authors’ preferred interpretation, intended journal, or known former blockers.

Every referee pass must:

- cite exact theorem numbers, equations, pages, and file paths;
- reconstruct at least one central proof independently;
- test sign, weight, quotient, rank, and alias conventions;
- distinguish theorem proof from computational regression;
- identify the nearest prior theorem for each novelty claim;
- verify the manuscript-to-Lean correspondence;
- inspect the clean-environment reproducibility record;
- inspect all limitations and negative statements;
- issue a recommendation with major and minor comments.

The mathematical audit must independently verify:

- K_X⊆ker R_2;
- the exact residual tensor formula;
- the two-defect decomposition by two genuinely independent derivations;
- the loss-variance identity;
- all weighted adjoints and Gram matrices;
- singular generalized eigenvalue deflation;
- rank and dimension formulas;
- the sharp frontier constant;
- equality and global compatibility;
- stability hypotheses and constants;
- exact extremizers;
- d=2 and d=3 construction scope;
- the repaired robustness theorem;
- all edge cases.

The adversarial mutation suite must include:

- omitted W;
- reversed generator sign;
- L-2dI instead of L+2dI;
- Frobenius quotient instead of sampled quotient;
- compression to im S_2;
- noninjective S_2;
- zero sampled quadratic module;
- duplicate and antipodal nodes;
- disconnected generators;
- singular pencils;
- d=1 pathology;
- unsupported higher-dimensional construction claims.

The novelty audit must use current primary literature and produce a theorem-level comparison. It must reject any claim that the work is the first positive coordinate-exact spherical Laplacian, the first monotone AFP discretization, or the first eigenpair-preserving graph design.

The Lean audit must verify exact theorem signatures, imports, axioms, clean builds, singular cases, and formalization wording.

The reproducibility audit must verify that the repository contains and documents reproducible commands for:

- Lean;
- exact algebraic tests;
- computer-assisted certificates;
- every manuscript table;
- every manuscript figure;
- the final PDF;
- the source and hash manifest.

When a concrete code, Lean, build, or artifact defect is found, record it exactly and route the repair to Codex. After the repair is committed, repeat the affected referee pass. Do not close a criticism merely because a proposed patch sounds plausible.

After all reports are complete, revise the manuscript, proofs, theorem registry, formalization table, bibliography, release notes, and response letter until every valid criticism is resolved.

Produce:

1. final manuscript source;
2. final PDF;
3. exact commit and tree;
4. theorem gate matrix;
5. claim-confidence matrix;
6. novelty matrix;
7. reproducibility matrix;
8. formalization correspondence table;
9. independent referee reports;
10. point-by-point response to referees;
11. source-to-evidence manifest;
12. release-candidate archive;
13. final go/no-go checklist;
14. journal recommendation with aspirational and realistic tiers.

The final verdict must be exactly one of:

- READY_TO_SUBMIT;
- READY_AFTER_MINOR_REVISIONS;
- MAJOR_REVISION_REQUIRED;
- NOT_READY — MATHEMATICAL BLOCKER;
- NOT_READY — NOVELTY/POSITIONING BLOCKER;
- NOT_READY — REPRODUCIBILITY BLOCKER;
- NOT_READY — MULTIPLE FUNDAMENTAL BLOCKERS.

Maintain a criticism registry with:

- exact issue;
- severity;
- supporting evidence;
- affected file and theorem;
- required repair;
- responsible coding or writing task;
- repair commit;
- independent recheck;
- final status.

Mark an issue closed only when the proof, manuscript, code, tests, and evidence all agree.

GitHub persistence is mandatory:

- save this exact prompt;
- use connected GitHub tools to maintain the final-review branch and draft PR whenever available;
- commit every referee report, criticism registry, revised manuscript, response letter, theorem matrix, novelty matrix, release checklist, and final verdict;
- update current state, decision log, theorem status, next steps, and artifact manifest;
- preserve earlier reports rather than overwriting them;
- if direct GitHub writing is unavailable, produce a complete ready-to-commit bundle with exact paths and use Prompt G0;
- report exact Git state or exact handoff bundle details.

—- Assume for purposes of this task that the repaired quadratic paper can be brought to publication quality without changing its central sharp frontier theorem. A complete solution must resolve every valid referee criticism, produce the revised submission package, and issue a defensible final verdict. Partial progress, synthetic referee summaries, acceptance predictions, unresolved major comments, or a response letter without corresponding manuscript changes is insufficient.

Public search is required for the final novelty review and journal-fit assessment. Use primary sources and current journal information.
```

---

# End-state requirements for the complete program

The complete repair and research program should leave the GitHub repositories with:

- an exact authoritative-state manifest;
- frozen historical and benchmark evidence;
- a repaired theorem registry;
- a coherent pure-mathematics manuscript;
- a precise formalization-scope table;
- clean Lean and computational builds;
- source-to-output reproduction commands;
- immutable release-candidate assets;
- separate P2E and P2F interpretation records;
- separate branches and manuscripts for N1–N4;
- durable failed-approach and counterexample records;
- current-state, decision-log, theorem-status, next-steps, and artifact-manifest files;
- draft PRs that expose rather than hide unresolved issues.

No major mathematical conclusion, benchmark interpretation, novelty decision, or publication recommendation should exist only in ChatGPT conversation history.
