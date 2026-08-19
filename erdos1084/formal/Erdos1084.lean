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
import Erdos1084.OrientationInterfaceCoercivityCore

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, and Gate-D interface programs.

The Gate-D module formally verifies:

* the `N²` lower bound for a bad-cell separator of opposite faces in an `N³` grid;
* the conversion of that separator count and a local energy gap into a surface-order energy lower
  bound;
* the scalar inball implication for interface calibration bodies;
* the elementary two-phase divergence-sum algebra.

The assignment of exact Barlow orientations to good coarse blocks, orientation propagation on
overlaps, the interface cell formula, and the Brenier common-core calibration theorem are
maintained in the canonical mathematical dossier. They are not hidden as project axioms.
-/
