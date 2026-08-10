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

**Status:** PROVED

In a connected reversible positive graph with a
symmetric spherical loss, equality in every local rate-defect row forces one
global active loss and one row rate.

**Resolution:** `GLOBAL_Q_RIGIDITY_THEOREM.md` §§1–2 proves the exact local
variance identity and uses the shared-edge propagation theorem.  Loops, zero
rates, repeated embedded vertices, inactive edges, and the separate antipodal
case are explicit.

## C-M3. Triangulated global \(Q=1\) classification

**Status:** PROVED

Under the exact ten simple, injective, minor-arc, noncrossing, convex-face,
disjoint-interior, full-coverage, positive-edge hypotheses, a coordinate-exact
global \(Q_i=1\) triangulation is tetrahedral, octahedral, or icosahedral up to
\(O(3)\).

**Resolution:** common side and round angle sum precede Euler; the 5-valent
case has a direct separating-triangle/link proof; geometric uniqueness uses
opposite-side face propagation.  Cube and dodecahedron remain the unrestricted
kill examples.

## C-M4. Quantitative near-rigidity

**Status:** PROVED

Under a positive normalized active-edge lower bound,
\(\max_i(Q_i-1)\le\eta\) gives the explicit pointwise, path, diameter,
reference-loss, arc, Poincare, resistance, and closed triangulation-stability
bounds in the Prompt 3 theorem.  No big-O or unnamed compactness constant is
used.

**Boundary:** long paths reject diameter-free wording under only a local floor;
side lengths approaching zero or \(\pi\) make the displayed geometric margin
degenerate, as the theorem records.

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
- every equal-loss spherical graph is a triangulated Platonic graph;
- blanket finite-graph Bakry--Émery curvature collapse;
- continuum \(W_2\) contraction from positivity alone;
- general order independence of layered stopping maps;
- weighted centering as sparse global sufficiency;
- symmetry scalarity without invariance;
- distinct sampled degree labels without distinct target eigenvalues;
- a blanket positive doubled-square obstruction;
- tangent normalization at exact global \(Q=1\) without `0<ell<2`;
- axial covariance from \(Q=1\) alone;
- form-space dimension equals sampled-space dimension;
- diameter-free near-rigidity from only a local active-weight floor; and
- finite enumeration as the all-orders classification proof.

## C-M7. Exact product-graph polar minimax

**Status:** PROVED

For every integer `N>=2`, the three coordinate equations at a polar-ring node
force the meridional and both azimuthal rates without symmetry assumptions.
The verified positive reversible construction attains that row and has its
maximum there, so the fixed-graph minimax is the exact polar expression with
sharp leading constant `8/pi^4`.

## C-M8. Uniform polar analytic expansion

**Status:** PROVED

The paired differentiated cotangent expansion has a positive tail bounded by
`x^4/80` on `0<x<=pi/4`.  The displayed rate and quality remainders therefore
hold at every grid order `N>=2`.  Formal-series or fitted-slope wording is
`REJECTED` in the claim matrix.

## C-M9. Rate-capped constrained extremal class

**Status:** PROVED

For the fully specified nonempty class controlling geometry, degree, locality,
masses, reversibility, exact equilibrium, and `r_i<=RK`,

```text
E_K>=4/(RK),
C*=liminf K E_K>=4/R.
```

Each nonempty fixed-`K>=2` class has a minimizer.  The product family is
eventually excluded from every fixed linear-rate class.  A loss window and
`K` comparable to `h^-2` give only conditional rate-cap compatibility.

## C-M10. Conductance-aware feasible-family anisotropy

**Status:** PROVED

For `lambda>0` and nonempty tangent-balanced `P_i`, each fixed-moment affine
slice is bijective with `P_i`, and

```text
Q_lambda=r epsilon/lambda^2=s_2(p)/m(p)^2.
```

The attainable-mean sliced LP defines the exact a priori constant `A_i`; its
finite dual has the recorded signs, and zero anisotropy is equivalent to
support on one loss level.  The old arbitrary-`lambda` use of `r epsilon/4`
and the description of the fixed slice as a projective cone are `REJECTED`.

## C-M11. Two-ray anisotropy boundary

**Status:** PROVED

If `v_2=-kappa v_1`, the unique balanced probability gives

```text
A=kappa(ell_1-ell_2)^2/(kappa ell_1+ell_2)^2.
```

The half-weight formula is the `kappa=1` corollary.  The unqualified
opposite-ray statement is `REJECTED` by the exact unequal-colatitude example.

## C-M12. Reduced-ring nearest-ring incidence

**Status:** PROVED

A biregular adjacent-ring coupling satisfies `pM_i=qM_{i+1}`; a perfect
matching forces equal populations.  The theorem does not exclude general
split/merge couplings.

## C-M13. General reduced-ring split/merge construction

**Status:** CONJECTURE

A stable, positive, reversible varying-population construction may exist with
non-biregular split/merge couplings.  This is numerical-analysis work and no
existence, convergence, or optimality conclusion is made here.

## C-M14. Delsarte/Gegenbauer upgrade

**Status:** REJECTED

No solved new dual certificate survived the sampling-kernel and alias audit.
A reduction to standard spherical-code linear programming is not a theorem of
this package.

## C-M15. Bakry--Émery collapse or one-function curvature theorem

**Status:** REJECTED

The eigenfunction `Gamma_2` identity is a one-function consistency relation,
not a curvature-dimension inequality on the full algebra.  Positivity does not
force curvature collapse.

## C-M16. Additional compact homogeneous-space theorem

**Status:** CONJECTURE

The Euclidean covariance identity is dimension-independent, but no additional
space produced a material theorem without a separate representation-theory
project.  No extension is claimed in the completed package.

## C-M17. Metric-free transport contraction

**Status:** REJECTED

Positive rates do not select continuum `W_2`.  Any future claim must specify a
discrete transport metric and prove its own curvature or contraction theorem.

## C-M18. Final publication hierarchy

**Status:** PROVED

The central candidate contribution is the actual-sampling residual
factorization and positive structural rigidity.  Prompt-1 feasibility,
Prompt-3 exact/quantitative rigidity, and Prompt-4 sharp barriers, extremals,
and feasible-family anisotropy form the supporting hierarchy.  Workflow and
Lean counts are provenance, never novelty.
