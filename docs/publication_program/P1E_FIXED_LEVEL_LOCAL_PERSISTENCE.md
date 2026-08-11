# Fixed-level local persistence for the reflected adaptive-ring construction

## Status

**PROVED ORDINARY THEOREM; EXISTENTIAL LEVEL-DEPENDENT RADIUS.**

This file supplies the publication-safe replacement for the former universal
support-preserving perturbation claim. It does not produce an explicit radius
uniform in the refinement level. The all-level unperturbed construction and
its constants are proved separately in
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`, Sections 1--9.

## 1. Fixed-level parameter space

Fix one refinement level `J` of the reflected adaptive-ring construction. All
of the following data are frozen at their unperturbed values:

- the pole and equator;
- every ring count and longitude phase;
- every radial mask and horizontal jump integer;
- the undirected support graph and the assignment of one shared preliminary
  conductance to each support edge;
- north--south reflection.

Let `m_J` be the number of northern nonpolar, nonequatorial rings. A reflected
latitude displacement is a vector

\[
 \eta=(\eta_1,\ldots,\eta_{m_J})\in P_J:=\mathbb R^{m_J},
 \qquad \|\eta\|_\infty=\max_k|\eta_k|.
\]

The southern displacement is fixed by reflection. A common ambient rotation
may be applied after the displacement; it does not affect any scalar product,
local-system coefficient, positivity assertion, or reproduction identity.

Because `J` is fixed, the unperturbed construction has finitely many rings,
vertices, support edges, ordinary rows, transition blocks, polar rows, and
equatorial rows. Its unperturbed latitude gaps and active chord lengths are
strictly positive.

## 2. Local systems

Index by `q` the finite collection `Q_J` of local systems used to recover the
preliminary conductances at level `J`. This collection contains the polar
system, every ordinary-row system, every coupled transition system, and the
equatorial system, with reflected copies identified. Write the system as

\[
 A_q(\eta)x_q(\eta)=b_q(\eta).
 \tag{2.1}
\]

The coordinates of `x_q` are exactly the preliminary conductances first
introduced by that local solve. Incoming conductances already fixed by an
earlier solve enter `b_q`; therefore the complete northward recursion is a
finite composition of the maps in (2.1).

Let `U_J\subset P_J` be the set on which the latitude order, the frozen
support incidences, and all nonzero geometric denominators used by the local
formulas are preserved. The unperturbed point `0` belongs to `U_J`. Indeed,
there are only finitely many positive unperturbed gaps, active chord lengths,
sine factors, count differences, and other displayed denominator factors, so
their minimum is positive at this fixed level.

On `U_J`, every entry of `A_q(\eta)` and `b_q(\eta)` is continuous. This follows
from the explicit formulas: they use finitely many additions,
multiplications, sine and cosine evaluations, and reciprocals of the
nonvanishing geometric factors defining `U_J`. The same conclusion holds for
the recursively substituted right-hand sides.

## 3. The theorem

### Proposition (fixed-level support-preserving local persistence)

Fix `J` and the unperturbed level-`J` construction. Assume, as established for
the unperturbed construction in Sections 1--9 of the construction source,
that

1. every matrix `A_q(0)`, `q\in Q_J`, is nonsingular; and
2. every recovered unperturbed preliminary conductance is strictly positive.

Then there exists a number

\[
 \delta_J>0
 \tag{3.1}
\]

such that every reflected latitude displacement `\eta\in P_J` with
`\|\eta\|_\infty<\delta_J` has the following properties when the same frozen
support data and local systems are used:

1. every local system is uniquely solvable;
2. every recovered preliminary conductance is strictly positive;
3. assigning the recovered value once to each undirected support edge gives a
   positive reversible generator after the usual mass normalization; and
4. the normalized generator satisfies exact constant and coordinate
   reproduction,
   \[
     L_{J,\eta}\mathbf 1=0,
     \qquad
     L_{J,\eta}\Omega=-2\Omega.
     \tag{3.2}
   \]

The radius in (3.1) is **existential and level dependent**. No positive lower
bound uniform in `J`, no prescribed power of the mesh scale, and no perturbed
all-level rate or quadratic-defect constant are asserted.

### Proof

For each `q\in Q_J`, continuity of the determinant and
`\det A_q(0)\ne0` give an open neighborhood `V_q\subset U_J` of `0` on which
`A_q(\eta)` remains invertible. On `V_q`,

\[
 x_q(\eta)=A_q(\eta)^{-1}b_q(\eta)
 =\frac{\operatorname{adj}A_q(\eta)}{\det A_q(\eta)}b_q(\eta)
 \tag{3.3}
\]

is continuous. Process the systems in the finite construction order. At each
step, previously recovered conductances enter the next right-hand side through
finite continuous substitutions, so the full vector

\[
 X_J(\eta)=(\Gamma_e(\eta))_{e\in E_J}
 \tag{3.4}
\]

of one conductance per undirected support edge is continuous on a neighborhood
of `0` where all local matrices are invertible.

Let

\[
 p_J:=\min_{e\in E_J}\Gamma_e(0)>0.
 \tag{3.5}
\]

The minimum is positive because `E_J` is finite and every unperturbed
conductance is strictly positive. By continuity of (3.4), there is an open
neighborhood of `0` on which every conductance exceeds `p_J/2`.

Equivalently, define the good set

\[
 \mathcal U_J=\{\eta\in U_J:
   \det A_q(\eta)\ne0\ \text{for every }q\in Q_J,
   \ \Gamma_e(\eta)>0\ \text{for every }e\in E_J\}.
 \tag{3.6}
\]

It is an open subset of `P_J` containing `0`. Hence the set

\[
 S_J=\{r\in(0,1]:
       \{\eta:\|\eta\|_\infty<r\}\subset\mathcal U_J\}
 \tag{3.7}
\]

is nonempty. The well-defined choice

\[
 \delta_J=\frac12\sup S_J
 \tag{3.8}
\]

is therefore strictly positive and has the asserted support, denominator,
invertibility, and positivity properties. Formula (3.8) is a definition, not
an effective numerical certificate; the theorem makes no claim that it can be
bounded below independently of `J`.

It remains to verify the generator conclusions. Each recovered value
`\Gamma_e(\eta)` is attached once to its undirected edge, so
`\Gamma_{ij}(\eta)=\Gamma_{ji}(\eta)>0`. The re-solved row equations include
the exact tangent-force equations. Their radial contraction gives

\[
 \sum_j\Gamma_{ij}(\eta)(\Omega_j-\Omega_i)
 =-2\mu_i(\eta)\Omega_i,
 \qquad
 \mu_i(\eta)=\frac12\sum_j
      \Gamma_{ij}(\eta)(1-\Omega_i\cdot\Omega_j).
 \tag{3.9}
\]

All active chord losses and conductances are positive in `\mathcal U_J`, so
`\mu_i(\eta)>0`. With

\[
 W(\eta)=\sum_i\mu_i(\eta),\qquad
 w_i(\eta)=\mu_i(\eta)/W(\eta),\qquad
 \gamma_{ij}(\eta)=\Gamma_{ij}(\eta)/W(\eta),
 \tag{3.10}
\]

one has `w_i\gamma` detailed balance and directed rates
`a_{ij}=\gamma_{ij}/w_i=\Gamma_{ij}/\mu_i`. Constants are annihilated by the
jump form, and (3.9) gives the coordinate eigenvalue `-2`. This proves
(3.2), positivity, and reversibility. A common ambient rotation preserves all
inner products and rotates both sides of (3.9), so it preserves the theorem.
`\square`

## 4. Exact scope

The proof uses only finite-dimensional openness at a fixed level. It does not
use compactness over all refinement levels. The quantities controlling the
radius include the smallest unperturbed latitude gap, the smallest nonzero
geometric denominator, the least absolute local determinant, the norms of the
local inverses, and the smallest recovered conductance. Every one of these may
depend on `J`.

Accordingly, this theorem cannot be cited for any of the following:

- a radius uniform over all levels;
- a perturbation size prescribed as a power of `h` with a level-independent
  coefficient;
- perturbed constants replacing the unperturbed `R_3=64\pi^2` or
  `C_3=75/2`;
- changes of ring counts, longitude phases, masks, jumps, support, or
  reflection;
- arbitrary node motion or independent longitude perturbations.

## 5. Proof dependencies and audit status

| Item | Status | Role |
|---|---|---|
| finiteness of the level-`J` construction | ordinary proof | makes the intersections and minima finite |
| unperturbed local nonsingularity | ordinary P1E construction proof | hypothesis imported from the established unperturbed construction |
| unperturbed strict conductance positivity | ordinary P1E construction proof | supplies the positive margin in (3.5) |
| continuity of local coefficients | ordinary proof above | finite analytic formulas on a guarded open domain |
| continuity of recovered conductances | ordinary proof above | finite recursion through (3.3) |
| existence of `\delta_J` | ordinary proof above | openness of (3.6) and definition (3.8) |
| exact `H_0\oplus H_1` fidelity | ordinary proof above | shared-edge normalization and exact row force equations |
| Lean status | not formalized | Lean covers only the finite algebraic stress-to-generator identities |
| computational status | regression only | the contract verifier and mutations check repository scope, not the analytic theorem |

The former all-level perturbation statement is retained only in
`P1E_REJECTED_UNIFORM_ROBUSTNESS_CLAIM.md`.
