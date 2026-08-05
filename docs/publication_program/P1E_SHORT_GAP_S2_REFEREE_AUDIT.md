# Hostile referee audit of the pre-repair shortened-gap \(S^2\) submission

## Historical decision and current disposition

**THE SUBMISSION AUDITED HERE WAS REJECTED; THE REPAIRED THEOREM IS NOW
ACCEPTED.**

This report deliberately preserves the exact failures of the pre-repair
submission.  Every item in Section 11 is discharged in the later complete
source `P1E_SHORT_GAP_S2_CONSTRUCTION.md` and its symbolic, rational
Cauchy, polar, independent, and hostile audits.  In particular, the corrected
mask moment, no-guard schedule, adaptive integer bracket, literal finite
matrices, global conductance recurrence, direct quotient identity, and narrow
robustness theorem are now proved.  The blocking regressions below remain in
the repository so that those earlier errors cannot silently return.

The shortened transition is a credible local mechanism, and several exact
identities in the candidate survive audit.  The submitted file does not,
however, prove the claimed family.  Two statements are literally false, and
the all-level guard, recurrence, cap, and robustness arguments are absent.
The exact script checks a different mask formula from the one printed in the
candidate and never constructs the finite guarded matrix \(A_M\) or
right-hand side \(b_M\) to which the claimed Taylor ledger is supposed to
apply.

This report does not edit
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`.  Exact blocking regressions are in
`afp_barrier_gate1/pure_math/covariance/p1e_short_gap_referee_audit.py`.

## 1. Claims that survive the audit

The following pieces are correct, subject to the conventions stated in the
candidate.

1. The scheduled transition identity is exact:

   \[
   \frac{\sin\tau_m\,\pi}{M_mh}
   =\frac{2^{m-J}\pi}
          {M_0 2^m\,4\pi/(M_0 2^J)}=\frac14.
   \]

2. The \(Q\)-mask has coarse row sum one and fine column sum one half.  Its
   even and odd reverse laws have the same first two cosine moments.  Thus a
   shared edge law of the form \(\gamma_{ij}=U_QQ_{ij}\) has incoming total
   \(U_Q/2\) at every fine vertex.  The factor \(1/2\) used by the transition
   solve is correct.

3. If all three row moment equations really hold with shared positive
   conductances, then

   \[
   \mu_i=\frac12\sum_j\gamma_{ij}\ell_{ij}>0,
   \qquad
   \sum_j\gamma_{ij}(\Omega_j-\Omega_i)=-2\mu_i\Omega_i
   \]

   gives exact \(H_0,H_1\) reproduction and reversibility after setting
   \(a_{ij}=\gamma_{ij}/\mu_i\).

4. Under tangent isotropy and loss-force cancellation, the displayed local
   residual is correct.  In the frame whose first axis is radial,

   \[
   M_i=\frac1{\mu_i}
       \operatorname{diag}(R_i,-R_i/2,-R_i/2)
      =\frac{3R_i}{2\mu_i}Z_i.                       \tag{1.1}
   \]

   This identity gives a stronger and sampling-safe conclusion than Section
   8 of the candidate.  Directly on the sampled quotient,

   \[
   (R_2A)_i=\frac{3R_i}{2\mu_i}(S_2A)_i,
   \qquad
   \mathfrak D_2\le\max_i\frac{3R_i}{2\mu_i}
   \le3\ell_{\max}\le\frac{75}{2}h^2.              \tag{1.2}
   \]

   No sampling lower frame bound is needed for (1.2), and sampling aliases
   cause no problem.

5. The exact determinant and inverse computation for the *displayed limiting
   matrix* is correct, as is positivity of the displayed limiting vector.
   This verifies only that limiting algebraic system, not its unidentified
   finite-\(M\) perturbations.

## 2. Fatal formula mismatch in the mask moment

Let

\[
 \beta=\frac12+\frac{\cos2\alpha}{2\cos\alpha},
 \qquad
 E_2=p+(1-p)\cos^22\alpha.
\]

The actual second loss moment is

\[
 m_2^{\rm correct}=\mathbb E(1-X)^2
 =1-2\beta+p+(1-p)\cos^22\alpha.                    \tag{2.1}
\]

The candidate instead prints

\[
 m_2^{\rm printed}
 =1-2\beta p+(1-p)\cos^22\alpha.                    \tag{2.2}
\]

Exact series expansion gives

\[
 m_2^{\rm printed}
 =\frac18-\frac3{32}\alpha^2+\frac{89}{64}\alpha^4
   +O(\alpha^6),                                    \tag{2.3}
\]

whereas

\[
 m_2^{\rm correct}
 =\frac32\alpha^4-\frac38\alpha^6+O(\alpha^8).      \tag{2.4}
\]

Consequently the printed
\(\widehat m_2=m_2^{\rm printed}/\alpha^4\) has no removable value; it
diverges like \(1/(8\alpha^4)\).  The proof-audit script silently uses (2.1):

```python
ecos2 = p + (1 - p) * cos(2 * alpha) ** 2
m2 = 1 - 2 * beta + ecos2
```

Thus the script is not an audit of the theorem as written.  Formula (2.2)
must be replaced by (2.1), and every finite matrix and Taylor bound must then
be regenerated from the corrected expression.

## 3. The polar integer-jump assertion is false

The candidate claims that the large fixed count \(M_0=2^{40}\) makes it
possible, at every cap radius, to choose integer longitude jumps whose
physical lengths lie in

\[
 [0.49h,0.51h]\quad\hbox{and}\quad[1.49h,1.51h],     \tag{3.1}
\]

with rounding error below \(2^{-35}h\). A large longitude count does not
give a uniformly fine grid in units of \(h\), because the cap radius grows to
order \(M_0h\).

Here is an exact obstruction. Put \(x=\pi/M_0\), take level \(J=1\), and
choose a cap radius by

\[
 \sin\theta=\frac{h}{6\sin x}
             =\frac{x}{3\sin x}.                    \tag{3.2}
\]

It lies strictly inside the cap: \(2x/3<\sin x<x\) gives
\(1/3<\sin\theta<1/2\), hence \(0<\theta<\tau_0=\pi/6\).
The one-step horizontal chord then has length exactly \(h/3\). The two-step
chord has length

\[
 \frac{2\sin\theta\sin(2x)}h
 =\frac{2\cos x}{3}>0.65.                            \tag{3.3}
\]

For \(1\le t\le M_0/2\), \(\sin(tx)\) is increasing, and every unoriented
longitude jump reduces to this range.  Hence no integer jump has chord length
in \([0.49h,0.51h]\).  The closest error is bounded below by a fixed multiple
of \(h\), not by \(2^{-35}h\).

The ambiguity in “physical length” does not rescue the claim. For the
projected sine length the two-step/one-step ratio is again \(2\cos x\); for
the parallel-circle arc length it is exactly \(2\).

This is not an isolated radius.  The same failure holds on an open annulus
around (3.2). Any intended cap schedule with radial gaps at most \(h\) moves
the normalized one-step chord by at most \(2\sin(\pi/M_0)\) per row, so it
cannot jump over that annulus.  Alternatively, if the author intends a
special cap latitude schedule avoiding it, that schedule must be stated and
its fill-distance and closure properties reproved.

The correction must replace (3.1) by an actually realizable integer-stencil
selection theorem, probably using wider brackets or more than two candidate
jumps.  All ordinary-row positivity and recurrence constants then have to be
recomputed.

## 4. The mesh and guard schedule are not defined completely

The following node data are missing.

- No formula specifies the cap latitudes between \(a_0h\) and \(\tau_0\), nor
  how the last cap gap closes while retaining the aligned \(h\)-guard before
  the first transition.
- “The remaining part of the band” is not named. To define \(q_m\), the
  proof must state its endpoints, whether
  \(L_m=\tau_{m+1}-\tau_m-(g+2)h\), the integer number of gaps, and the exact
  list of ring latitudes.
- The last northern band, the equatorial ring, duplicate removal under south
  reflection, and the reflected transition orientation are not specified.
- The active edge set at cap, guard, transition, and equatorial rows is not
  given as one unambiguous combinatorial definition.

The estimate \(1-16/M_m\le q_m\le1\) is plausible for the natural definition
of \(L_m\), but it cannot define the missing nodes retroactively. Without the
node list, fill distance, separation, degree, and the claimed all-level graph
are not theorem statements with checkable hypotheses.

## 5. Several row types have no positivity proof

The six-by-six transition system covers only the two endpoints of an
\(M:2M\) edge whose adjacent aligned gaps are exactly \(h\). The ordinary-row
formula in Section 6 covers only equal incoming and outgoing gaps.  The
declared schedule necessarily also contains:

1. a coarse guard row with gaps \(q_{m-1}h\) and \(h\);
2. a fine guard row with gaps \(h\) and \(q_mh\);
3. cap-closure guard rows;
4. the equatorial row; and
5. rows where the integer horizontal jump pair changes.

Equations (7.4)--(7.7) in the older adaptive-ring audit can be specialized to
some of these rows, but citing the formulas is not a positivity proof.  The
candidate supplies neither their finite matrices nor a uniform inverse,
right-hand-side, solution margin, or shared-scale recurrence.  Local row
feasibility also does not prove that the outgoing aligned conductance of one
row equals the incoming conductance used by the next.

These are exactly the “guarded formulas” that Section 4's title promises,
but no guarded matrix appears in the file or either audit script.

## 6. The Taylor ledger does not bound the claimed formulas

The ledger is not an outward-error proof for \(A_M\) and \(b_M\).

- Neither \(A_M\) nor \(b_M\) is defined entry by entry. The column scaling
  behind the displayed \(A_\infty\) is also omitted.
- `p1e_short_gap_proof_audit.py` constructs only \(A_\infty\), its inverse,
  and scalar arithmetic budgets. It never constructs a finite \(A_M\), a
  finite \(b_M\), a guard matrix, or their differences.
- The occurrence counts \(24,16,12,12,12\) and coefficient bound \(8^4\) are
  asserted without expanding any matrix entry.  Bounds on atoms do not by
  themselves bound arbitrary products and quotients of those atoms.
- The declared Taylor domain is already too small. On a coarse \(M\)-ring,
  the longitude spacing is \(2\alpha\), so horizontal jump \(8\) uses angle
  \(16\alpha=16\pi/M\), not at most \(8\pi/M_0\).
- The \(p,q\) denominators, the corrected mask moment, ordinary-row
  denominators, first-polar-row inverse, guard systems, and recurrence ratios
  are absent from the table.
- The first polar row uses longitude offsets near \(3/8\) and \(9/8\), which
  are \(O(1)\), not in the small-angle ledger. Rational brackets on \(u,v\)
  verify only its limiting signs. They do not prove the claimed finite-\(h\)
  matrix perturbation or a solution perturbation bound.

Even one numerical inequality in the table is misstated: using
the scripted substitution \(\pi\mapsto22/7\), the first rational coefficient
is

\[
 \frac{24\,8^4(4\cdot22/7)^2}{6}>2.58\times10^6,
\]

not \(<2.5\times10^6\). This does not alone break the final grotesque
budget, because it multiplies \(M^{-2}\), but it confirms that the table is
not a certified entrywise expansion.

Accordingly (5.1), the finite Neumann bound, and transition positivity have
not been proved.  The exact calculations following (5.1) are valid only
*if* (5.1) is supplied independently.

## 7. Global conductance and stationary-weight bounds are unsupported

The statement that cap conductances change by at most a factor four per row
is not derived from the actual integer stencils.  The claim that band
recurrences “telescope” is also not accompanied by an identity or a bounded
product estimate. This matters because a band has order \(h^{-1}\) rows: a
per-row bound or an \(O(M_m^{-1})\) transition perturbation cannot simply be
multiplied without an all-level accumulation estimate.

Therefore

\[
 2^{-4M_0}\le\gamma_e\le2^{4M_0}                    \tag{7.1}
\]

has not been established.  Every subsequent lower mass, lower stationary
weight, and sampling constant that uses (7.1) is conditional on this missing
global reconciliation.

The elementary implications *from* a valid edge window and (7.1) to the
displayed \(\mu_i\), \(w_i\), and \(r_{\max}\) bounds are otherwise correctly
normalized.

## 8. Sampling and the quotient

The asserted “standard four-cap argument” is not stated or proved, so its
particular constant \(\alpha_3\) is unaudited. Fill distance alone must be
turned into a lower count of nodes in a fixed cap, combined with the stated
individual weight lower bound and a quantitative lower bound for
\(|\Omega^TA\Omega|\) on that cap.  None of those constants appears.

This gap is unnecessary.  Once the exact row moments are genuinely proved,
the scalar identity (1.1) gives (1.2) directly, including on a singular or
aliased sampling quotient. The corrected theorem should use (1.2) and
delete the sampling-frame detour from the defect estimate.  A separate
sampling bound may still be recorded as a mesh property, but it is not needed
for \(\mathfrak D_2=O(h^2)\).

## 9. The robustness claim is false at its stated scope

The local systems have only three even equations because exact horizontal
reflection kills the longitude-odd tangent force, loss-force, and covariance
equations. A general \(O(h^3)\) perturbation of node positions destroys this
reflection.  The full local problem then has six moment equations, while the
displayed local unknown set and inverse still cover only three.  Shared-edge
coupling also turns the perturbation problem into a global system; independent
row inverses do not define a global shared correction.

Even for a symmetry-preserving perturbation, the scaling sentence is wrong
as written. Perturbing an \(O(h)\) edge by \(O(h^3)\) changes
\(\ell\tau\) by \(O(h^5)\), which becomes \(O(h)\), not \(O(h^2)\), after the
declared \(h^{-4}\) loss-force scaling. This may still be small enough for a
Neumann argument, but it requires a new bound and changes the conductance
perturbation order.

Robustness can be repaired only by either:

- explicitly restricting perturbations to the iso-latitude, cyclic, and
  reflection-symmetric parameter family and auditing the corresponding
  finite systems; or
- proving a global right inverse for the full shared-edge six-moment map with
  a uniform positivity margin.

No such result is present.

## 10. What the exact scripts do and do not prove

Both submitted scripts pass, but their coverage is narrow.

| Script check | Exact status | Missing theorem content |
|---|---|---|
| determinant/inverse of \(A_\infty\) | checked | no finite \(A_M\) |
| limiting solution signs | checked | no finite guarded solutions |
| scalar Neumann arithmetic | checked conditionally | premise (5.1) absent |
| ledger totals | checked arithmetically | no expansion producing the ledger |
| first polar limiting inequalities | partially checked | no finite matrix/inverse |
| mask mutation | checks only a leading invariant | printed \(m_2\) mismatch missed |
| floating transition solve | regression only | polar regime and small \(M\), not all schedule rows |
| mesh, cap, guards, recurrence | not constructed | all-level family missing |
| robustness | not tested | symmetry and global sharing missing |

The new hostile regression checks the printed mask formula, exact (Q)
bookkeeping, the polar rounding obstruction, the coarse jump-eight Taylor
domain, and the direct quotient factorization.

## 11. Required corrections before reconsideration

An acceptable revision must do all of the following.

1. Correct \(m_2\) to (2.1) everywhere and regenerate the matrices.
2. Give the exact latitude and edge list, including cap closure, both guards,
   equator, and south reflection.
3. Replace the false cap jump-rounding rule by a proved integer-stencil
   selection with uniform loss brackets.
4. Write every finite normalized row matrix and right-hand side, including
   column scalings and denominator guards.
5. Produce an actual symbolic or outward-interval bound for every entry over
   the full domain \(|z|\le16\pi/M_0\) and over the correlated gap variables.
6. Prove positive solutions for transition, guard, cap, and equatorial rows,
   and prove their shared conductance recurrence globally.
7. Derive the explicit two-sided conductance bounds from that recurrence.
8. Use the direct sampled-quotient identity (1.2), or separately prove the
   stated sampling constant.
9. Restrict and prove robustness, or supply the missing full global inverse.

Until these corrections are supplied, the candidate is a local transition
ansatz with promising exact limiting algebra, not a matching-order P1E
construction theorem.

## 12. Reproduction

Run:

```text
python afp_barrier_gate1/pure_math/covariance/p1e_short_gap_referee_audit.py
```

Expected output:

```text
short-gap hostile referee audit: exact blocking regressions PASS
```
