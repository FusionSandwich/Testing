# P2C prior-art transfer and hostile audit

## External theorem ledger

| Source | Imported statement | Hypotheses checked here | Explicit non-transfer |
|---|---|---|---|
| Steinerberger, arXiv:1708.08736 | spectral limitations for nonnegative quadrature/generalized designs | positivity and normalization conventions | no node-generator construction, no shared-edge feasibility |
| Ahrens–Beylkin, DOI 10.1098/rspa.2009.0104 | icosahedral orbit quadrature methodology and rotational exactness | published rules require imported orbit parameters plus independent normalization/mass audits | the executable 12-vertex icosahedron is only a symmetry fixture, not a published AB rule; no generator theorem transfers |
| Morel et al., DOI 10.13182/NSE07-A2693 | three-dimensional product-quadrature AFP context | P2C product masses use the frozen total-mass-one convention | no arbitrary-node co-design theorem |
| Bienvenue et al., DOI 10.1080/00295639.2025.2462891 | moment-preserving monotone AFP on nonorthogonal/Voronoi sets | moment, monotonicity, and nonorthogonal-node conventions only | no exact bilevel optimum, no Paper-I frontier, and no streaming ray-effect remedy is transferred |
| Bondarenko–Radchenko–Viazovska, arXiv:1303.5991 | well-separated equal-weight spherical designs at the stated cardinality scale | sphere dimension, equal mass, separation, and declared strength | no covering certificate silently bundled; no shared conductance compatibility |
| Yudin, “Coverings of a sphere, and extremal properties of orthogonal polynomials,” Discrete Math. Appl. 5:4 (1995) | the spherical-design covering-radius bound determined by a Jacobi/Gegenbauer zero, hence (O(t^{-1})) at fixed dimension | sphere dimension and design strength | no separation, quadrature positivity, graph, conductance, or co-design result |
| Yudin, “Lower bounds for spherical designs,” Izv. Math. 61:3 (1997) | a cardinality lower bound for spherical designs | sphere dimension and design strength | no existence, positivity, covering, graph, conductance, or co-design result |
| Izmestiev–Lam, arXiv:2408.04877 | spherical/hyperbolic Delaunay nonnegative structure-preserving Laplacians | intrinsic Delaunay convention | no P2A shell optimum or co-design stationarity |
| accepted P2A | fixed-node convex programs, normalizations, independent verifier | literal archived parent and frozen sign/basis conventions | no nonconvex node globality |
| accepted Paper-I P1B | \(\mathfrak D_2r_{\max}\ge6\) on its declared class | same positivity, H1, rate, and normalization class | not a lower bound on rotation spread |
| accepted Paper-I P1E | reflected-ring feasible construction and constants | the implementation calls the accepted constructor and normalizes exactly as P2A | not an arbitrary-design compatibility theorem |

## Exact hostile examples

### Strict positivity without a floor is noncompact

Minimize \(c_1\) subject to \(c_1+c_2=1\) and \(c_1,c_2>0\).  The infimum is zero and is not attained.  P2C therefore uses \(c_e\ge0\), or \(c_e\ge c_{\min}>0\) on a declared active support.

### Sampling rank is not a smooth afterthought

For \(S(t)=[t]\), the range projector is one for \(t\ne0\) and zero at \(t=0\).  Differentiating a pseudoinverse across this point is invalid.  P2C uses the raw LMI and confines smooth optimization to a fixed-rank spectral-gap stratum.

The two-antipodal-node fixture has a rank-deficient even shell while the exact raw block remains valid.  It is a permanent regression.

### Local cones do not imply shared reversible conductances

Equation (6) chooses row probabilities independently.  Reversibility additionally requires \(w_ia_{ij}=w_ja_{ji}\) on every shared edge.  Those cross-row equalities can conflict even when every row convex hull contains zero.  The global LP/SDP is therefore a separate mandatory gate.

### Arbitrary node movement is not restorable

With two nodes, equal masses, and one edge, exact H1 forces the nodes to be antipodal and fixes the conductance.  A generic motion of only one node leaves no correction in the single conductance capable of restoring all coordinate equations.  The reduced restoration Jacobian is not onto, so the proposed step must be rejected or enlarged to a coupled direction.

### Block stationarity need not be full stationarity

On the constraint \(y=x\), an \(x\)-only feasible fiber and a \(y\)-only feasible fiber are singletons.  Every point is separately block-stationary although \(f(x,y)=x\) has a descent direction along the feasible line.  P2C requires the tangent-frame condition or a joint safeguard.

### Slater does not imply a differentiable value function

The parametric convex problem
\[
 v(s)=\min_{c\in[-1,1]}sc=-|s|
\]
is strictly feasible but nondifferentiable at zero.  A gradient taken from an arbitrary optimizer is not the value gradient.  P2C uses strong regularity for smooth claims and a certified Clarke/proximal condition otherwise.

### Monotone values do not imply stationarity

For \(f(x)=x\), the sequence \(x_k=1+1/(k+1)\) decreases but converges to the nonstationary interior point one.  The stationarity residual in equation (11), not monotonicity alone, is required.

### A local node method has nonglobal local minima

On a circle,
\[
 f(\theta)=\sin^2\theta+0.1(1-\cos\theta)
\]
has separated local minima with unequal values.  No local node method may claim global outer optimality merely from descent and stationarity.

### Edge deletion can destroy feasibility

Deleting a bridge or an active edge can remove the only solution of the H1 equality.  Zero conductance is a sufficient deletion certificate; a positive edge needs a kernel move or a freshly verified restricted conic solve.  Solver status without rebuilt residuals is rejected.

### Delaunay tie-breaking can break covariance

At a cocircular/degenerate spherical face, choosing a diagonal by ambient coordinate lexicography changes after a generic rotation.  The weak Delaunay graph or an intrinsic ID/group-orbit tie is required.

### Defect does not lower-bound rotation spread

If the shell defect operator is a nonzero scalar multiple of the identity, \(\mathfrak D_2>0\) but every physical probe sees the same defect.  The directional spread is zero.  The dense icosahedral fixture realizes this regression numerically with \(\mathfrak D_2=4\).

### Joint rotation is not a ray-effect cure

Rotating nodes and physical data together tests covariance.  Rotating only the physical problem against fixed ordinates tests orientation sensitivity.  In a transport solve, the latter combines collision and streaming unless one operator is disabled.  Quadrature interpolation is a third algorithm and receives a separate moment/positivity audit.

### An enriched identity is not a continuum bound

The identity \(c_h^\top(u_h-Iu_H)=z_h^\top r_h\) is exact for the enriched algebraic system.  It contains no estimate of \(u-u_h\).  P2C labels its scope accordingly.

### A fitted slope is not an all-orders theorem

Any fixed sequence of benchmark rows can mimic a slope.  The P2C convergence claim instead follows at every accepted level from the explicit P1B/P1E sandwich.  The fitted slope is retained only to catch implementation regressions.

## Normalization and kernel checklist

- total quadrature mass is exactly one;
- P2A uses a negative generator \(L\), while the positive operator is \(-L\);
- \(\lambda_1=2\), \(\lambda_2=6\) on \(\mathbb S^2\);
- H1 is reconstructed pointwise in all three coordinate columns;
- shell bases are fixed and their continuum Gram/scaling is audited; quotient defects are invariant under invertible basis changes;
- the moving Gram is never frozen during an outer derivative;
- a retained sampling rank has an explicit positive eigenvalue gap;
- generator rates divide edge-conductance sums by node mass;
- P1B uses rate maximum, not graph edge angle or fill distance;
- collision and streaming metrics carry separate scope labels.

## Numerical conditioning checklist

- report the raw and retained Gram spectra;
- fail if the declared rank changes within tolerance;
- scale every equality and PSD residual;
- rebuild H0, H1, reversibility, rate, shell, and response residuals independently;
- report primal and dual objective enclosures and the gap;
- accept a graph update only with nonoverlapping objective intervals;
- certify \(SO(3)\) extrema only with a covering radius and Lipschitz bound;
- record solver/version, canonical input hash, inner/benchmark time, process maximum RSS, and separately scoped Python-tracemalloc peak;
- never infer an exact sign from a floating value whose interval contains zero.

This audit is intentionally stronger than the computational smoke tests: each listed false transfer is also excluded from the claim map and main theorem language.
