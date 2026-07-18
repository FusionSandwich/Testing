# AFP Barrier — Gate 2 priority review

**Audit date:** 18 July 2026

## Decision

**Conditional pass.** The project remains worth pursuing, but the novelty claim must be narrowed.

The finite carré-du-champ identity and the fact that a nontrivial finite jump generator cannot satisfy an exact diffusion chain rule are standard Markov-generator facts. They are formalized in Lean for reliability, not claimed as new probability theory.

The strongest research direction is instead:

> Characterize the positive spherical quadratures and shared-edge graphs that admit a weighted-reversible monotone angular Fokker–Planck operator preserving the complete degree-one eigenspace, and optimize the unavoidable degree-two defect.

This directly addresses the compatibility question left for future investigation in Bienvenue, Naceur, Carrier, and Hébert (2025), DOI 10.1080/00295639.2025.2462891.

## Claim classification

| Claim | Gate 2 assessment |
|---|---|
| Finite jump carré-du-champ identity | Standard |
| Exact nonlinear diffusion chain rule is impossible for a nontrivial finite jump generator | Standard mechanism; new Lean formalization only |
| AFP monotonicity plus complete degree-one exactness forbids complete degree-two exactness | Explicit AFP formulation not located; modest candidate novelty requiring specialist confirmation |
| Peak defect equals carré du champ | Elementary consequence; useful AFP design formula |
| Defect–stiffness inequality | Sharp Cauchy–Schwarz consequence; not strong alone |
| Rowwise convex-hull feasibility | Adaptation of positive-stencil theory |
| Rowwise linear program | Adaptation of Seibold’s positive-stencil method |
| Shared-edge weighted-reversible compatibility theorem | Strong candidate novelty |
| Coupled reversible defect-minimizing LP and geometric dual | Promising candidate novelty |
| Uniform optimal defect scaling `Theta(h^2)` | Research target, not yet proved |
| Physical transport advantage | Gate 3 target |

## Nearest prior art

1. Bienvenue et al. (2025): monotone nonorthogonal AFP discretization preserving degree zero and the three degree-one moments; exact positive pseudoinverse solutions observed for tested product, level-symmetric, and Lebedev quadratures; compatible quadrature properties left open.
2. Bakry, Gentil, and Ledoux (2014): standard carré-du-champ and diffusion-property framework for Markov generators.
3. Seibold (2008): minimal positive Laplace stencils constructed by linear programming with geometric existence conditions.
4. Izmestiev and Lam (2025): positive spherical Delaunay Laplacians with exact `-2` modes.
5. López Pouso et al. (2025): rigorous order and moment analysis for one-dimensional angular Fokker–Planck difference schemes.

## Lean extension in this branch

- `DiffusionProperty.lean`: general tangent-gap chain-rule defect and strict-convexity rigidity.
- `ForwardAdjoint.lean`: componentwise conversion from a weighted conservative forward AFP matrix to a finite jump generator, plus a forward-matrix no-go theorem.
- expanded axiom audit and dedicated Gate 2 GitHub Actions workflow.

## Publication threshold

A strong final paper should add at least one of:

- necessary and sufficient compatibility conditions for a substantial quadrature class;
- a broad Delaunay/convex-polyhedral sufficient theorem;
- a sharp `Theta(h^2)` optimal-defect theorem;
- a duality theorem with geometric infeasibility/optimality certificates;
- a demonstrated transport improvement over the current pseudoinverse construction.

## Human review required

Before making priority claims, obtain review from:

- Charles Bienvenue or another AFP specialist;
- a specialist in discrete spherical Laplacians;
- optionally, a Markov-semigroup specialist for canonical attribution of the chain-rule obstruction.

The complete standalone Gate 2 repository archive contains a claim matrix, literature review, search log, revised manuscript, expert review packet, and reproducible Lean project.
