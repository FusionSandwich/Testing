# P1A stage report: sampling quotient and exact two-defect algebra

## Frozen input and non-overwriting branch

P1A starts from the exact P0 baseline, without changing its branch or archive:

```text
P0 commit:  b40ee2898dbbfc206e1f079cc4df83f716e2f3b0
P0 tree:    3cf100f90d98bbc186b1df3e419c279b599b7d39
P0 archive: archive/afp-publication-program-baseline-p0-6bac46ce
P0 run:     30936790377 (all three jobs success)
P1A branch: agent/afp-publication-p1a-quadratic-foundation-b40ee289
```

The P1A branch was created at the literal P0 commit before editing.  No P0,
Prompt-1--Prompt-4, transport, or historical branch is advanced by this work.

## Correct literal hypotheses

The theorem is stated for `d>=2`, nonnegative off-diagonal rates,
`a_ii=0`, positive normalized vertex weights, shared symmetric conductances,
unit nodes, and the negative-semidefinite convention

```text
(L f)_i = sum_(j != i) a_ij (f_j-f_i).
```

The `d>=2` condition is necessary because `B_i` contains `d/(d-1)`.
No extra row-rate hypothesis is added: the eigenmap and positivity give
`sum_j a_ij ell_ij=d-1>0`, hence `r_i>0` at every row.  Connectivity,
regularity, equal weights, distinct nodes, full-dimensional span, and
injectivity of `S_2` are not assumed.

## Proved theorem package

`P1A_QUADRATIC_FIDELITY_FOUNDATION.md` proves:

1. `K_X subset ker R_2` and the induced residual on `Sym_0(d)/K_X`;
2. `(R_2 A)_i=<A,M_i>_F`;
3. the covariance trace, radial covariance and `M_i-Z_i` pairing;
4. `||Z_i||_F^2=(d-1)/d`;
5. the exact orthogonal `M_i=(d epsilon_i/(d-1))Z_i+B_i` split;
6. the exact loss-variance identity and automatic validity of its denominator;
7. weighted adjoints and the two exact Gram operators;
8. the basis-independent quotient/deflated generalized eigenvalue formula;
9. separate formulas for `E_form`, `K_X`, and `E_sample`;
10. all ranks and dimensions without sampling injectivity.

The global Hilbert--Schmidt form of the two-defect identity is

```text
tr(R_2^* R_2)
  = d/(d-1) sum_i w_i epsilon_i^2 + sum_i w_i ||B_i||_F^2,
tr(S_2^* S_2) = (d-1)/d.
```

The ordinary proof was completed before the new executable or Lean module.

## Two independent central proofs

- **Tensor proof.** Contract `C_i` with `Omega_i`, use
  `tr(C_i+2 Omega_i Omega_i^T)=2d`, and project `M_i` onto `R Z_i`.
- **Operator/Gram proof.** Evaluate `R_2 Z_i` at row `i` directly from
  `(S_2 Z_i)_j=(Omega_i.Omega_j)^2-1/d`; the first loss moment cancels the
  linear term and leaves `epsilon_i`.  The row-representer projection theorem
  then gives the same coefficient and Pythagorean split.

The second proof does not reuse the radial contraction of `C_i`.

## Quotient and adjoint controls

The quotient inner product is

```text
<[A],[H]>_S = <S_2 A,S_2 H>_w,
```

not the Frobenius quotient norm.  With a Frobenius-orthonormal coefficient
basis and `W=diag(w)`, the bilinear/operator Gram matrices are `S^TWS` and
`R^TWR`.  In a general coefficient basis with Frobenius Gram `F`, the
operator matrices are `F^-1 S^TWS` and `F^-1 R^TWR`.

The generalized pencil is deflated to `K_X^perp`.  A raw determinant on the
whole coefficient space is rejected because aliases make it identically
zero.  The weighted repeated-node fixture also proves that `im S_2` need not
be invariant under `T=L+2dI`; `D_2^2` is not the square of an unprojected or
naively compressed eigenvalue.

## Deterministic exact audit

Run:

```text
cd afp_barrier_gate1
python pure_math/covariance/p1a_quadratic_fidelity_audit.py
```

The audit uses exact SymPy arithmetic and checks every displayed local,
operator, quotient, rank and trace formula on 19 fixtures:

- the simplex, cross-polytope and hypercube for `d=2,3,4`;
- all five three-dimensional Platonic shortest-edge graphs;
- an antipodal aliased pair;
- an unequal-weight repeated-node complete generator;
- the exact spherical hexagonal prism with `rank(S/R)=5/3` and two genuinely
  sampled exact modes;
- a positive full cube with both loss variance `1/6` and
  `||B_i||_F^2=1/81` nonzero;
- a degenerate equatorial hexagon with nonzero `K_X`, `E_form`, and
  `E_sample` simultaneously.

The golden-ratio adjacency is selected numerically only as a candidate and is
then certified by exact strict algebraic dot-product gaps.  Every rate and
conductance is certified nonnegative.  The test rejects:

```text
unweighted adjoints;
L-2dI and the opposite generator sign;
raw form/sample dimension conflation;
singular-pencil use without deflation;
squaring a compression when im(S_2) is non-invariant.
```

It also checks a nonorthogonal coefficient basis, the exact prism spectrum
`{0,0,4,4,36}`, the nonzero aggregate mixed Gram operator, and the fact that
the full singular pencil determinant vanishes identically on an alias
fixture.

The retained P1--P4 exact suite also passes locally.  Plantri and the full
Lean/Mathlib build are rerun in the dedicated exact-head workflow.

## Formal core

The existing `QuadraticSampling.lean` and `QuadraticSphereResidual.lean`
already formalize residual factorization, kernel containment, the
range/intersection formula and both rank identities.  P1A adds
`QuadraticFidelityFoundation.lean`, which formalizes the weighted row
adjoint/Gram algebra, the orthogonal remainder and Pythagorean identity, and
the finite exact loss-variance identity.  The aggregate import and focused
axiom audit include the new declarations.  No `sorry`, `admit`, `sorryAx`, or
project axiom is permitted.

## External-theorem boundary

M3 supplies asymptotic nonnegative-quadrature cardinality bounds, not sampled
injectivity.  M4 supplies a special Delaunay/cotangent spherical operator;
only its compatible sign and weighted Green convention are relevant here.
M8 association schemes and M9 spherical designs organize symmetric examples,
but neither is used to prove the arbitrary-weight theorem.  In particular,
uniform design moments do not imply a positive reversible generator or
`L`-invariance of the sampled quadratic space.

## Audited workflow trust boundary

The dedicated workflow is externally bound to the reviewed Git blob

```text
.github/workflows/afp-publication-p1a-quadratic-foundation.yml
blob f46abe247481eca99bd71889576fe0101613b3f9
```

All third-party actions are pinned to full commit hashes.  The workflow
requires all 13 P1A paths, both full exact and Lean gates, exact remote branch
equality, every pre-existing immutable archive, an exact source archive, and
a final integrity artifact.  A bootstrap run may truthfully report that the
new archive is absent.  The authoritative acceptance run is instead the
later archive-triggered rerun and must report `PRESENT_EXACT` in both the exact
and final artifacts.

No candidate-owned workflow can cryptographically authenticate its own
semantics, and a Git ref observation cannot prove immunity to later movement.
Acceptance therefore combines the externally audited blob above, the exact
commit/tree and artifact digests, create-only archive creation, and a final
read-only requery of both the working branch and archive.

## Acceptance state

The final exact commit/tree, workflow run, three job conclusions, artifact
IDs/digests, source archive digest, Lean job count, focused axiom result,
archive ref and PR disposition are recorded after the literal final head has
passed the dedicated workflow.  Until then this document describes a P1A
candidate, not an accepted publication baseline.
