# Gate 3 closure: an all-orders positive product-grid AFP theorem and a polar stiffness barrier

**Status:** mathematically complete and independently verified  
**Scope:** angular Fokker–Planck mathematics; `Radiant.jl` integration is deliberately deferred  
**Reference family:** cell-centred equal-angle latitude–longitude quadratures

## 1. Result

Gate 3 proves an explicit all-orders construction for a local angular
Fokker–Planck operator on the unit sphere. For every pair of integers

\[
N\ge 2,\qquad M\ge 3,
\]

the construction is:

- local, with at most four neighbours per direction;
- conservative;
- weighted reversible;
- monotone, with strictly positive conductances on every actual edge;
- exactly preserving all three degree-one spherical-harmonic coordinate modes
  with eigenvalue `-2`;
- equipped with exact formulas for its unavoidable degree-two peak defect and
  total outgoing jump rate.

For the square family `M=2N`, Gate 3 additionally proves explicit finite-order
bounds

\[
\boxed{
\frac{2}{N^2}
\le \varepsilon_i
\le \frac{\pi^2}{N^2}
}
\]

on every ring, and

\[
\boxed{
\frac{8}{\pi^4}N^4
\le r_{\max}
\le N^4.
}
\]

The maximum rate occurs on the first and last latitude rings. Therefore

\[
\varepsilon_{\max}=\Theta(N^{-2}),
\qquad
r_{\max}=\Theta(N^4).
\]

This is a useful positive result and a useful negative design result at the
same time: the product family provides a constructive all-orders monotone AFP
operator, but its unreduced polar rings create a quartic stiffness barrier.

## 2. Grid and weights

Define

\[
\delta=\frac{\pi}{N},
\qquad
\alpha=\frac{2\pi}{M},
\]

and the cell-centred directions

\[
\theta_i=\left(i+\frac12\right)\delta,
\quad i=0,\ldots,N-1,
\]

\[
\phi_j=j\alpha,
\quad j=0,\ldots,M-1.
\]

The corresponding unit vector is

\[
\Omega_{ij}
=
\left(
\cos\theta_i,
\sin\theta_i\cos\phi_j,
\sin\theta_i\sin\phi_j
\right).
\]

Use the exact spherical-cell area

\[
q_i
=
2\alpha\sin\theta_i\sin\frac{\delta}{2}.
\]

The weights are strictly positive and satisfy

\[
\sum_{i,j}q_i=4\pi.
\]

The Lean proof rewrites each ring weight as a cosine difference and telescopes
the polar sum exactly.

## 3. Explicit shared-edge conductances

For the meridional edge joining rings `i` and `i+1`, define

\[
B_{i+1/2}
=
\frac{\alpha\sin((i+1)\delta)}{\sin\delta},
\qquad i=0,\ldots,N-2.
\]

Set

\[
B_{-1/2}=B_{N-1/2}=0.
\]

For each of the two azimuthal edges incident to a node on ring `i`, define

\[
C_i
=
\frac{\alpha\sin(\delta/2)}
{(1-\cos\alpha)\sin\theta_i}.
\]

Every conductance on an actual edge is strictly positive. The two missing
polar meridional conductances are exactly zero. The two endpoints of each
meridional edge assign the same conductance:

\[
B^{+}_i=B^{-}_{i+1}.
\]

The operator is

\[
\begin{aligned}
(Lf)_{ij}=\frac{1}{q_i}\big[&
B_{i+1/2}(f_{i+1,j}-f_{ij})
+B_{i-1/2}(f_{i-1,j}-f_{ij})\\
&+C_i(f_{i,j+1}-f_{ij})
+C_i(f_{i,j-1}-f_{ij})
\big],
\end{aligned}
\]

with periodic azimuthal indices and omitted boundary terms.

Because one conductance is shared by both endpoints of every undirected edge,

\[
q_iL_{(i,j),(k,l)}
=
q_kL_{(k,l),(i,j)}.
\]

Thus the operator belongs to the weighted-reversible graph-Laplacian class
formalized in Gate 2.

## 4. Exact complete degree-one eigenspace

Let

\[
x_{ij}=\cos\theta_i,
\qquad
y_{ij}=\sin\theta_i\cos\phi_j,
\qquad
z_{ij}=\sin\theta_i\sin\phi_j.
\]

Gate 3 proves directly from the sine and cosine addition laws that

\[
Lx=-2x,
\qquad
Ly=-2y,
\qquad
Lz=-2z.
\]

No local balance equation is left as an assumption in the final theorem.
The proof includes the first and last rings because the missing polar
conductances are proved to vanish exactly.

The result is formalized for real parameters satisfying

\[
n\ge2,
\qquad m\ge3,
\qquad 0\le i\le n-1.
\]

Integer quadrature orders and ring indices are immediate special cases.

## 5. Actual spherical neighbour losses

For two sphere points written in polar coordinates, Gate 3 formalizes the
Euclidean dot product and proves the actual neighbour identities.

For a meridional neighbour,

\[
1-\Omega_{ij}\cdot\Omega_{i+1,j}
=1-\cos\delta
=2\sin^2\frac\delta2.
\]

For an azimuthal neighbour,

\[
1-\Omega_{ij}\cdot\Omega_{i,j+1}
=
\sin^2\theta_i(1-\cos\alpha).
\]

These identities are connected directly to the Gate 1 carré-du-champ defect
theorem, rather than supplied as abstract loss parameters.

## 6. Exact degree-two peak defect

For the sampled zonal coordinate function peaked at `Omega_ij`, the exact
unavoidable degree-two defect is

\[
\boxed{
\varepsilon_i
=
(1-\cos\delta)
+
\sin^2\theta_i(1-\cos\alpha).
}
\]

It is strictly positive for every finite `N` and `M`, consistent with the
Gate 1 no-go theorem: a finite monotone jump generator cannot reproduce both
the complete degree-one and complete degree-two eigenspaces exactly.

For `M=2N`, so that `alpha=delta`, Jordan's sine inequality gives the explicit
finite-order bounds

\[
\boxed{
\frac{2}{N^2}
\le \varepsilon_i
\le \frac{\pi^2}{N^2}
}
\]

for every ring. The `Theta(N^-2)` result therefore does not depend on a fitted
slope or an asymptotic expansion.

## 7. Exact rate and the polar stiffness barrier

The total outgoing jump rate is

\[
\boxed{
r_i
=
\frac{1}{1-\cos\delta}
+
\frac{1}{(1-\cos\alpha)\sin^2\theta_i}.
}
\]

For the square family, the latitude sine is minimized on the first and last
rings. Gate 3 proves

\[
r_i\le r_{\mathrm{polar}}
\]

for every ring, where

\[
\boxed{
r_{\mathrm{polar}}
=
\frac{1}{2\sin^2(\pi/(2N))}
+
\frac{1}{2\sin^4(\pi/(2N))}.
}
\]

The finite-order bounds

\[
\boxed{
\frac{8}{\pi^4}N^4
\le r_{\mathrm{polar}}
\le N^4
}
\]

are Lean-verified. Hence the quartic rate growth is a theorem, not a
regression result.

The cause is geometric. A fixed number of azimuthal directions is retained on
every ring while the physical radius of the polar rings is `Theta(N^-1)`.
The azimuthal edge length therefore collapses too quickly, forcing rates of
order `N^4`.

## 8. Formal verification map

The final proof is divided into small Lean modules so each claim has an
explicit verification boundary.

| Module | Verified content |
|---|---|
| `EqualAngleProduct.lean` | local action, algebraic rate and defect formulas, positivity implications |
| `EqualAngleGeometry.lean` | direct axial and transverse trigonometric balances; local `x`, `y`, `z` eigenrelations |
| `EqualAngleGrid.lean` | all-order parameter ranges and complete degree-one exactness for every admissible node |
| `EqualAngleEdges.lean` | zero polar boundary edges and strict positivity of every actual edge |
| `EqualAngleConnectivity.lean` | shared meridional conductance and reflection identities |
| `EqualAngleDotProducts.lean` | actual spherical dot products and end-to-end defect formula |
| `EqualAngleQuadrature.lean` | exact telescoping weight normalization `sum q = 4*pi` |
| `EqualAngleAsymptotics.lean` | explicit finite-`N` defect and polar-rate bounds |
| `EqualAngleRateMaximum.lean` | proof that the polar rings maximize the square-family rate |
| Gate 1/2 modules | general no-go theorem, defect identity, stiffness inequality, reversibility, adjoint conventions |

The axiom audit enumerates every public theorem. The CI rejects `sorry`,
`admit`, `sorryAx`, and user-declared axioms.

## 9. Deterministic global audit

`gate3/equal_angle_product_audit.py` uses only the Python standard library and
contains no random sampling. It assembles the full global grid and checks every
node for square and non-square cases.

The square cases are

\[
N=2,3,4,5,8,16,32,64,128,
\qquad M=2N.
\]

Additional non-square cases include

\[
(N,M)=(2,3),(3,4),(3,7),(4,5),(5,11),(7,9),(8,13).
\]

For each case it checks:

- positive cell weights and every actual edge conductance;
- exact zero boundary conductances;
- total area `4*pi` and weighted centering to roundoff;
- all three coordinate eigenrelations at every node;
- the exact peak-defect identity;
- the exact jump-rate identity;
- the polar maximum-rate formula in square cases;
- the explicit finite-order defect and rate bounds.

Log--log slopes remain in the report only as regression diagnostics. They are
not used to establish the exponents.

## 10. What is new and what is not

The following ingredients are standard and are not claimed as new:

- finite Markov jump generators and carré-du-champ identities;
- weighted graph Laplacians;
- elementary trigonometric identities;
- Jordan's inequality.

The candidate publication contribution is the AFP-specific combination:

1. the complete-degree-two monotonicity obstruction;
2. the exact unavoidable defect and stiffness tradeoff;
3. an explicit all-orders positive local spherical AFP family;
4. a complete degree-one exactness theorem;
5. explicit finite-order `N^-2` defect bounds;
6. the proved `N^4` polar stiffness barrier.

Priority wording must remain cautious until Charles Bienvenue or another AFP
specialist completes a final literature review.

## 11. Gate decision

Gate 3 is closed when one CI run verifies, from the same exact source commit:

1. the deterministic global audit;
2. the complete pinned Lean/Mathlib build;
3. the public-theorem axiom audit;
4. the source placeholder audit;
5. exact source and generated-record packaging.

All five conditions have been met on the Gate 3 branch. The final run and
artifact identifiers are recorded in the pull-request description and the
workflow-generated `gate3-report.txt`.

## 12. Next research question

The most valuable continuation is a reduced-ring or quasi-uniform spherical
family that retains positivity and exact degree-one modes while reducing the
worst-case rate from

\[
\Theta(N^4)
\]

toward

\[
\Theta(N^2).
\]

A separate route is an all-order theorem for Radiant's
Gauss--Legendre--Chebyshev family. That extension should not rely on unproved
uniform inequalities between Gauss--Legendre nodes, weights, and cumulative
moments.
