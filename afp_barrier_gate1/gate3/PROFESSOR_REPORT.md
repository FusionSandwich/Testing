# Professor briefing: verified all-orders AFP construction

## Main result

For every integer `N >= 2` and `M >= 3`, we constructed a local angular
Fokker–Planck operator on a cell-centred equal-angle spherical grid that is:

- conservative and weighted reversible;
- monotone, with positive conductance on every actual edge;
- exact on all three degree-one spherical-harmonic coordinate modes;
- accompanied by exact degree-two defect and jump-rate formulas.

Let

\[
\delta=\pi/N,\quad \alpha=2\pi/M,
\quad \theta_i=(i+1/2)\delta,\quad \phi_j=j\alpha.
\]

The nodes and exact cell weights are

\[
\Omega_{ij}=(\cos\theta_i,\sin\theta_i\cos\phi_j,
\sin\theta_i\sin\phi_j),
\]

\[
q_i=2\alpha\sin\theta_i\sin(\delta/2).
\]

The shared conductances are

\[
B_{i+1/2}=\frac{\alpha\sin((i+1)\delta)}{\sin\delta},
\]

\[
C_i=\frac{\alpha\sin(\delta/2)}
{(1-\cos\alpha)\sin\theta_i}.
\]

The resulting operator satisfies

\[
L(\cos\theta)=-2\cos\theta,
\]

\[
L(\sin\theta\cos\phi)=-2\sin\theta\cos\phi,
\]

\[
L(\sin\theta\sin\phi)=-2\sin\theta\sin\phi.
\]

## Exact defect and stiffness

The unavoidable degree-two peak defect is

\[
\boxed{\varepsilon_i=(1-\cos\delta)
+\sin^2\theta_i(1-\cos\alpha)}.
\]

The total outgoing rate is

\[
\boxed{r_i=\frac1{1-\cos\delta}
+\frac1{(1-\cos\alpha)\sin^2\theta_i}}.
\]

For the square family `M=2N`, Lean verifies the finite-order bounds

\[
\boxed{2/N^2\le\varepsilon_i\le\pi^2/N^2}
\]

on every ring and

\[
\boxed{(8/\pi^4)N^4\le r_{\max}\le N^4}.
\]

The polar rings are proved to maximize the rate. Thus the second-mode error is
`Theta(N^-2)`, but the unreduced product grid has a `Theta(N^4)` polar
stiffness barrier.

## What was formally verified

The Lean package proves:

- the complete trigonometric balances for the three coordinate modes;
- admissible angle ranges for every order and ring;
- positive weights and every actual edge conductance;
- zero omitted polar conductances;
- equality of shared meridional edge conductances;
- exact spherical neighbour dot products;
- exact quadrature normalization `sum q = 4*pi`;
- exact defect and rate formulas;
- explicit finite-`N` defect and stiffness bounds;
- the polar maximum-rate theorem.

A deterministic Python program separately assembles complete square and
non-square grids and checks every row. It uses no random sampling and checks
positivity, boundary behavior, total weight, weighted centering, all three
eigenrelations, the defect/rate identities, and the finite-order bounds.

One CI workflow runs the deterministic audit, pinned Lean build, axiom audit,
proof-placeholder scan, and exact source packaging from the same commit.

## Relevance to Charles Bienvenue's work

Charles's multidimensional AFP method solves a shared-edge system for general
quadratures. This result supplies an infinite reference family for which
existence, positivity, degree-one exactness, and error scaling are explicit.
It can be used as a verification case and exposes a design limitation not
visible from first-moment preservation alone.

The next mathematical target is a reduced-ring or quasi-uniform family that
retains positivity and exact degree-one modes while reducing the maximum rate
from `Theta(N^4)` toward `Theta(N^2)`.

## Novelty boundary

The general finite-jump carré-du-champ identity is standard. The candidate
contribution is the AFP-specific combination of:

1. the complete-degree-two monotonicity obstruction;
2. exact unavoidable defect and stiffness relations;
3. an explicit all-orders positive local spherical family;
4. a proved quartic polar stiffness barrier.

Priority wording should still be checked by an AFP specialist before journal
submission.
