# Fixed-level support-preserving robustness for the reflected adaptive-ring construction

## Status

**PROVED, level by level.** This theorem replaces the unsupported uniform
version formerly associated with Proposition 7.3. It applies to every fixed
production level of the unperturbed `d=3` adaptive-ring family, but the
permitted latitude radius depends on that level and on its finite
nonsingularity and positivity margins. The existence radius is computable
from the displayed finite matrices. No lower bound uniform in the refinement
level is asserted.

The committed JSON certificate is only a schema-conformance fixture. It is
not evidence for a numerical production radius. The theorem below is an
ordinary finite-dimensional analytic proof; an explicit level certificate may replace the merely existential numerical
value by a verified rational lower bound using a production extension of the
conformance interface.

## 1. Fixed level, support, and parameters

Fix the production family with `M_0=2^80` and a level `J >= 1` in the construction of
`P1E_SHORT_GAP_S2_CONSTRUCTION.md`. Let

\[
  0<\theta^0_1<\cdots<\theta^0_{n_J}=\pi/2
\]

be its northern ring latitudes, including the equator. At this fixed level we
hold fixed:

1. every ring count;
2. every longitude phase;
3. every aligned or `M:2M` radial incidence mask;
4. every horizontal jump integer;
5. the north and south poles;
6. the equator;
7. north-south reflection; and
8. the convention that each undirected active edge has one shared
   conductance.

The latitude parameter is

\[
 p=(\theta_1,\ldots,\theta_{n_J-1})\in\mathbb R^{n_J-1},
 \qquad \theta_{n_J}=\pi/2,
\]

with southern latitudes `pi-theta_i`. One common rotation `Q in SO(3)` may be
applied after solving. It is not an independent node perturbation and changes
neither chord lengths nor the conductance equations.

Let `S_J` denote the fixed finite orbit support. The unknown vector `x` lists,
in the order used by the construction, all positive orbit conductances after
fixing the north-pole conductance to one as a scale gauge. It contains:

- the outgoing meridional conductance and two horizontal conductances at each
  first or ordinary row;
- the six unknowns of each coupled coarse/fine transition block;
- the final equatorial horizontal conductance.

Every literal graph edge receives the corresponding orbit conductance,
multiplied by its fixed positive mask coefficient at a transition.

## 2. The exact finite moment system

For a row at latitude `theta`, let the three equations be exactly equations
(3.1)--(3.4) of the construction source:

\[
  \sum_j \gamma_{ij}t_{ij}=0,
  \qquad
  \sum_j \gamma_{ij}\ell_{ij}t_{ij}=0,
  \qquad
  \sum_j\gamma_{ij}t_{ij}t_{ij}^{T}
       \text{ is scalar on }T_{\Omega_i}S^2.                 \tag{2.1}
\]

Here `ell_ij=1-Omega_i dot Omega_j` and
`t_ij=Omega_j-Omega_i+ell_ij Omega_i`. Longitude reflection eliminates the
odd-longitude equations exactly. For an ordinary row, (2.1) is a `3 x 3`
linear system for the outgoing and two horizontal conductances once the
incoming conductance is known. For a transition pair it is the literal
coupled `6 x 6` shared-edge system (3.5). At the equator it reduces to the
single nonzero covariance coefficient used in Section 8.

Concatenate these equations from the pole to the equator and write

\[
     F_J(p,x)=A_J(p)x-b_J(p)=0.                              \tag{2.2}
\]

The matrix is block lower triangular in the construction order. Its diagonal
blocks are:

- `A_first(p)`, the first-row `3 x 3` block;
- `A_ord,k(p)`, one `3 x 3` block for each ordinary row;
- `A_tr,m(p)`, one `6 x 6` block for each count transition; and
- `A_eq(p)`, the final scalar equatorial block.

All entries are real analytic on the open latitude-ordering domain. The
radial masks and longitude arguments are fixed, so no support switch or
integer rounding occurs in (2.2).

## 3. Nonsingularity at the unperturbed point

Let `p_J^0` and `x_J^0` be the unperturbed latitude and conductance vectors.
Every component of `x_J^0` is strictly positive by Sections 5--8 of the
construction source. Set

\[
 m_J=\min_a (x_J^0)_a>0.                                  \tag{3.1}
\]

The diagonal blocks of `A_J(p_J^0)` are nonsingular:

1. **First row.** The exact adjugate calculation and polar Cauchy guard in
   Section 8 and `p1e_short_gap_polar_guard_audit.py` give a nonzero
   determinant.
2. **Ordinary rows.** The two horizontal brackets satisfy `x_-<1<x_+`.
   Equations (7.1)--(7.2) first solve uniquely for their two positive
   horizontal moments and then uniquely for the radial sum and difference.
   The change of variables has determinant proportional to
   `(x_+-x_-) sin(h)`, which is nonzero.
3. **Transitions.** Equations (5.3), (6.1), and (6.3) prove that every literal
   finite `6 x 6` transition block is invertible on the accepted compact box.
4. **Equator.** The selected horizontal jump has
   `sin(jump*delta) != 0`, so the scalar coefficient is nonzero.

Because a block lower-triangular matrix is invertible exactly when its
diagonal blocks are invertible,

\[
       D_xF_J(p_J^0,x_J^0)=A_J(p_J^0)\quad\text{is invertible}.
                                                                    \tag{3.2}
\]

This argument is finite for fixed `J`; it does not furnish a level-uniform
inverse norm.

## 4. Quantitative level-dependent radius

Use the maximum norm. Define the finite quantities

\[
 \beta_J=\|A_J(p_J^0)^{-1}\|_\infty,                       \tag{4.1}
\]

and, on a closed parameter box `B_J(r)` contained in the latitude-ordering
domain,

\[
 L_J(r)=\sup_{p\in B_J(r)}
     {\|A_J(p)-A_J(p_J^0)\|_\infty\over\|p-p_J^0\|_\infty},
 \quad
 C_J(r)=\sup_{p\in B_J(r)}
     {\|F_J(p,x_J^0)\|_\infty\over\|p-p_J^0\|_\infty}.     \tag{4.2}
\]

At the centre the quotient is interpreted by the derivative. Analyticity on
a compact box makes these quantities finite, and interval or exact rational
bounds make them computable.

Let

\[
 g_J=\min\{\theta^0_1,\theta^0_{k+1}-\theta^0_k:
                         1\le k<n_J\}>0                    \tag{4.3}
\]

be the smallest northern meridional boundary or gap margin. Choose
`rho_J>0` so that

\[
 \rho_J\le \min\{h_J/32,g_J/4\},                            \tag{4.4}
\]

\[
 \beta_J L_J(\rho_J)\rho_J\le {1\over2},
 \qquad
 2\beta_J C_J(\rho_J)\rho_J < {m_J\over2}.                 \tag{4.5}
\]

Such a positive radius exists by continuity. Equations (4.1)--(4.5) are also
a direct certificate recipe: outward-rounded interval bounds for `beta_J`,
`L_J`, `C_J`, `m_J`, and `g_J` produce a verified rational lower bound for
`rho_J`.

For `||p-p_J^0||_infty <= rho_J`, the Neumann estimate gives

\[
 \|A_J(p)^{-1}\|_\infty\le 2\beta_J,                       \tag{4.6}
\]

and the unique solution

\[
       x_J(p)=A_J(p)^{-1}b_J(p)                             \tag{4.7}
\]

satisfies

\[
 \|x_J(p)-x_J^0\|_\infty
   \le 2\beta_J C_J(\rho_J)\|p-p_J^0\|_\infty <m_J/2.      \tag{4.8}
\]

Hence every orbit conductance and every literal mask edge remains strictly
positive. This is a quantitative implicit-function argument, although the
system is affine in the conductance variables.

## 5. Proposition 7.3

**Proposition 7.3 (fixed-level support-preserving robustness).** For every
fixed production level `J >= 1` of the `M_0=2^80` unperturbed reflected adaptive-ring
family, there exists a level-dependent radius `rho_J>0` with the following
property. Perturb the northern non-equatorial ring latitudes by at most
`rho_J`, keep the equator and poles fixed, reflect the perturbation to the
south, and keep every ring count, longitude phase, radial mask, horizontal
jump, and support incidence fixed. Then the exact moment system has a unique
solution in the pole-normalized gauge. Its literal shared conductances are
strictly positive. After defining

\[
 \mu_i={1\over2}\sum_j\gamma_{ij}\ell_{ij}                 \tag{5.1}
\]

and normalizing the masses, the resulting generator is connected,
reversible, and satisfies

\[
        L1=0,\qquad L\Omega=-2\Omega.                       \tag{5.2}
\]

The rowwise loss-force and tangent-isotropy equations continue to give

\[
        R_2A(i)=c_iS_2A(i),\qquad 0<c_i\le3\ell_{\max}.     \tag{5.3}
\]

The radius may be reduced, without changing the conclusion, so that every
active chord lies in `[h_J/16,6h_J]`. Consequently

\[
       r_{\max}\le 1024h_J^{-2},
       \qquad
       \mathfrak D_2\le54h_J^2.                            \tag{5.4}
\]

One common rotation of the entire construction is permitted. The radius is
explicitly computable from (4.1)--(4.5), but no positive lower bound uniform
in `J` is proved.

### Proof

The support remains connected because its incidence graph is fixed and every
active conductance stays positive. Shared conductances imply detailed balance
with the masses (5.1). The first equation in (2.1), together with
`Omega_j-Omega_i=t_ij-ell_ij Omega_i`, gives (5.2). The other two equations in
(2.1) give the row-multiplier identity (5.3) exactly as in Section 9 of the
unperturbed proof; no sampling-frame lower bound is used.

For the geometric constants, moving each endpoint only in latitude by at
most `rho_J` changes an edge chord by at most `2rho_J`. The base active chords
lie in `[h_J/8,5h_J]`; (4.4) therefore permits the reduced interval
`[h_J/16,6h_J]`. Since `ell=chord^2/2`,

\[
 r_i={2\sum_j\gamma_{ij}\over\sum_j\gamma_{ij}\ell_{ij}}
       \le {2\over\ell_{\min}}\le1024h_J^{-2},
\]

and (5.3) gives `D_2<=3ell_max<=54h_J^2`. A common rotation preserves all dot
products and conjugates each vector and tensor equation, so it preserves the
conclusions. The existence, uniqueness, and positivity are (4.6)--(4.8). ∎

## 6. Exact scope and excluded statements

The proposition proves neither of the following:

- a single radius of order `h_J^3/K_*` valid for every level;
- a level-uniform inverse, determinant, positivity, or recurrence margin;
- independent longitude motion, phase changes, mask changes, jump changes,
  support changes, pole motion, equator motion, or arbitrary node motion;
- robustness after a conductance reaches zero; or
- a higher-dimensional construction.

The former enormous constant was unsupported and is not retained as a
publication value. A uniform all-level theorem would require a literal
expression graph, verified operation count, denominator separation, inverse
bounds, positivity margins, and global recurrence estimates uniform in `J`.
No such certificate is present.

## 7. Computational and formal boundary

`p1e_fixed_support_robustness.py` is an independent finite regression solver
for the same fixed support and exact row equations. Its tests check small
perturbations, rotations, collapsed gaps, positivity, exact coordinate
fidelity, rate, and defect. They do not prove the proposition; the proof is
Sections 1--5 above.

The two certificate verifiers use independent arithmetic implementations:
`Fraction` arithmetic and integer cross multiplication. The committed fixture
has status `CONFORMANCE_FIXTURE_ONLY`. Lean files certify finite algebraic
identities used after a shared stress is supplied; they do not formalize the
analytic level-dependent radius, and no Lean theorem is labeled as doing so.
