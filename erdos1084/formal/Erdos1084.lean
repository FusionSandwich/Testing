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
import Erdos1084.SeparatedCapStabilityCore
import Erdos1084.GlobalDegreeConstraints
import Erdos1084.NormalizedDeficitLimitCore
import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic
import Erdos1084.BarlowInvariantMeasureArithmetic

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, and invariant-measure Barlow programs.

The Gate-B module formalizes:

* the real one-symbol-marginal volume and coefficient formulas;
* FCC lower bounds and equality cases on `p ∈ [0,1]`;
* continuity of the coefficient polynomial;
* an exact non-subadditivity certificate for the raw directionwise infimum;
* exact arithmetic for the common convex-envelope body of volume `57/2` and cube `1539/4`.

The density of periodic orbit measures, weak-* continuity of the full support bodies, the
periodized-prefix seam theorem, and the geometric intersection-body proof are maintained in the
canonical mathematical dossier. They are not hidden as project axioms.
-/
