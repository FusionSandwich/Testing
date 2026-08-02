# AFP pure-math conjecture register

Every active conjecture has an exact hypothesis target and kill criterion.
Resolved and rejected entries remain visible so claim changes are auditable.
Status fields use only the controlled claim labels.

## C-M1. Strict local spherical feasibility

**Status:** PROVED

For indexed non-antipodal neighbours, an all-positive coordinate-exact row
exists exactly when the origin is in the relative interior of the tangent
hull. The Prompt 1 package covers repetitions, redundant directions,
lower-dimensional span, exact scaling/rate/uniqueness, antipodes, quantitative
margins, and identified-span perturbations.

**Regression warning:** a changing lower-dimensional span requires a specified
isometry; endpoint motion alone is insufficient.

## C-M1G. Local-to-shared compatibility

**Status:** REJECTED

Local positive rows plus weighted centering do not imply sparse shared-edge
feasibility. The centered unequal-mass four-cycle and the weighted cube have
exact Farkas certificates.

**Resolved sufficient mechanisms:** complete-graph construction, equivariant
orientation reconciliation, and centered-clique submass decomposition are
PROVED.

## C-M2. Global equality propagation

**Status:** CONJECTURE

**Statement under test:** in a connected reversible positive graph with a
symmetric spherical loss, equality in every local rate-defect row forces one
global active loss and one row rate.

**Work needed:** a complete propagation proof with zero-rate and repeated-node
cases exposed. This is Prompt 3 scope, not part of Prompt 2.

**Kill condition:** an exact connected reversible counterexample satisfying
every row equality.

## C-M3. Triangulated global \(Q=1\) classification

**Status:** CONJECTURE

**Candidate statement:** a connected nondegenerate geodesic triangulation of
\(S^2\), positive on every edge and coordinate-exact with \(Q_i=1\), is one of
the tetrahedral, octahedral, or icosahedral triangulations under a precise
convex-embedding hypothesis.

**Warning:** without the triangulation restrictions, the cube and dodecahedron
are counterexamples.

**Kill condition:** one valid non-Platonic triangulated counterexample.

## C-M4. Quantitative near-rigidity

**Status:** CONJECTURE

**Statement under test:** under a positive normalized active-edge lower bound,
\(\max_i(Q_i-1)\le\eta\) controls global active-loss variation by
\(O(\sqrt\eta)\), with explicit graph-diameter and conductance dependence.

**Kill condition:** a family with \(Q\to1\) but no such concentration under all
stated quantitative hypotheses.

## C-M5. Attainable quadratic exactness

**Status:** PROVED

The Prompt 2 package proves:

- the arbitrary-target covariance identity, including \(\mu=0\);
- weighted centering under nonempty positive-weight detailed balance;
- the trace-free sphere residual \(R_X=(L+2dI)S_X\);
- the sampling quotient and exact genuine dimension formula;
- the positive radial and Frobenius obstruction for nonempty \(I\), \(d>1\),
  nonnegative rates, and a unit eigenmap with \(L\Phi=-(d-1)\Phi\);
- signed one-shell full-tangent-isotropy rigidity for \(d>1\), nonempty
  noncoincident shells with \(0<\ell_i<2\), and the full signed moment;
- positive prism sharpness;
- equivariant kernel and quotient-rank formulas under invariant generator
  rates, with the corrected invariance theorem;
- exact Platonic classifications; and
- signed cube restoration with coordinate target \(-2\), cross-quadratic target
  \(-6\), and global optimum \(N^-=2\).

**Boundary:** rank-nullity, real semisimplicity, the self-adjoint spectral
theorem, and convex KKT are EXTERNAL standard inputs. The finite matrices and
minors are COMPUTATIONAL exact regressions. No priority claim is made from the
covariance identity or ranks alone.

## C-M6. Spectral-product hierarchy

**Status:** PROVED

The valid finite theorem is target-eigenvalue-class separation: when one
common operator has the prescribed scalar action, sums belonging to distinct
target scalars form an internal direct sum, with a constants-safe signed
converse and weighted-orthogonal reversible converse. For spherical harmonics,
distinct degrees imply distinct targets when \(d\ge2\).

The unrestricted all-dimension distinct-degree wording is REJECTED by the exact
\(d=1\) singleton with \(V_0=V_1\). A universal positivity hierarchy is also
REJECTED by finite aliases and the positive Boolean square.

The \(S^2\) Clebsch--Gordan decomposition and negative-Pell completeness are
EXTERNAL. Platonic harmonic ranks and aliases are COMPUTATIONAL exact
certificates.

## Retained rejected claims

**Status:** REJECTED

- unrestricted \(Q=1\) classification by \(K\in\{4,6,12\}\);
- global \(Q>1\) for every finite spherical graph;
- blanket finite-graph Bakry--Émery curvature collapse;
- continuum \(W_2\) contraction from positivity alone;
- general order independence of layered stopping maps;
- weighted centering as sparse global sufficiency;
- symmetry scalarity without invariance;
- distinct sampled degree labels without distinct target eigenvalues; and
- a blanket positive doubled-square obstruction.
