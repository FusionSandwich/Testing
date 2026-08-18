import Erdos1084.ExternalConstants
import Erdos1084.DeficitCharge
import Erdos1084.IntervalCertificate
import Erdos1084.FallbackCertificate
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.RadiusTwoCore
import Erdos1084.RadiusTwoAssembly
import Erdos1084.RadiusTwoGeometricBridges
import Erdos1084.RadiusTwoOptimized
import Erdos1084.RadiusTwoOptimizedAssembly
import Erdos1084.KeplerOuterParallel
import Erdos1084.KeplerOptimizedChord
import Erdos1084.KeplerOneRadiusOptimality

/-!
# Erdős Problem 1084: formalized certification spine

The library contains the following certified algebraic and abstract-assembly routes:

* the radius-`1.58731` Lévy arithmetic certificate;
* the radius-two conceptual coefficient `5/3`;
* the clean strengthened radius-two coefficient `1673/1000`;
* the Kepler/outer-parallel scalar bridge for the clean coefficient `2.0465`;
* the optimized convex-chord local charge at the exact Kepler radius;
* the one-radius endpoint minimax core and exact degree-one monotonicity.

The Kepler modules introduce no project-specific axiom. Their geometric surface inequalities are
explicit theorem parameters, the positive scale is constrained by `K^3 * π^2 = 18`, and the
optimized local envelope is proved algebraically from the concavity of the upper semicircle.

The remaining monotonicity of the concrete degree-eleven profile is a visible theorem parameter
in the one-radius optimizer.  Its exact human proof and arithmetic certificate are maintained in
the canonical Math branch.

The kissing-number theorem, Euclidean isoperimetry, spherical-neighborhood isoperimetry, the
Kepler density theorem, and the outer-parallel truncated-density identity remain cited external
geometric results rather than hidden axioms.
-/
