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
import Erdos1084.RogersOuterParallel
import Erdos1084.DodecahedralPublicationBound
import Erdos1084.KeplerOptimizedChord
import Erdos1084.KeplerOneRadiusOptimality
import Erdos1084.SeparatedCapStabilityCore
import Erdos1084.GlobalDegreeConstraints
import Erdos1084.NormalizedDeficitLimitCore
import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic
import Erdos1084.BarlowInvariantMeasureArithmetic
import Erdos1084.OrientationInterfaceCoercivityCore
import Erdos1084.GateERecoveryArithmetic

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
corrected Rogers finite coefficient, publication-core dodecahedral finite coefficient,
Kepler asymptotic arithmetic, periodic Barlow, invariant-measure Barlow, Gate-D
interface, and Gate-E exact-mass recovery programs.

The publication-core dodecahedral module formally verifies:

* the exact rational surface-scale certificate below the published `0.7547` ratio;
* the clean coefficient comparison `2.0207`;
* strict local-to-global assembly from explicit dodecahedral global and Kepler local
  surface inputs;
* the contact-number scalar implication with the power scale tied to `n^(2/3)`.

The finite dodecahedral Voronoi theorem and Euclidean isoperimetry remain visible
external geometric inputs rather than project axioms.

The Rogers module retains an independent finite fallback with clean coefficient
`1.9773`. The Gate-D and Gate-E modules certify only their finite combinatorial and
algebraic cores. Contact-model Gate-C geometry, physical number-density normalization,
orientation selection, and sharp interface cell problems are not hidden as project
axioms.
-/
