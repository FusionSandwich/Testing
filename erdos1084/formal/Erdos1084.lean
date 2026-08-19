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
import Erdos1084.GateERecoveryArithmetic
import Erdos1084.FiniteSpherePacking
import Erdos1084.FiniteBallUnionBoundary
import Erdos1084.FiniteOuterParallelArithmetic
import Erdos1084.TangentCapGeometry
import Erdos1084.ContactExtremizer
import Erdos1084.Phase1UnionBoundary
import Erdos1084.Phase1PublishedInputs
import Erdos1084.Phase1EndToEnd
import Erdos1084.Phase1ContactNumber
import Erdos1084.ContactNumberExistence
import Erdos1084.MaximizerNoIsolated
import Erdos1084.Phase1MainTheorem
import Erdos1084.PowerScaleUniqueness

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-D interface, and Gate-E exact-mass
recovery programs.

The Phase-I publication spine directly defines finite minimum-separation configurations in
Euclidean three-space, their exact distance-one contact graphs, contact counts, degrees, and
integer degree-deficit identity. `ContactExtremizer` and `ContactNumberExistence` construct the
greatest attainable finite contact count and select an actual maximizing configuration.
`MaximizerNoIsolated` proves the no-isolated-vertex property by a supporting-coordinate
relocation. `FiniteBallUnionBoundary` and `Phase1UnionBoundary` prove the topological ownership
of a finite enlarged-ball union boundary by exposed sphere patches.
`FiniteOuterParallelArithmetic` checks the exact Kepler-density normalization, while
`TangentCapGeometry` checks the tangent-neighbor cap equation.
`Phase1PublishedInputs`, `Phase1EndToEnd`, `Phase1ContactNumber`, and `Phase1MainTheorem`
connect one actual finite contact graph to the strict relational `2.0465` theorem through
explicit geometric data. `PowerScaleUniqueness` proves uniqueness of the positive scale
satisfying `x^3=n^2`; no unavailable cube-root API is required.

The five named geometric inputs remain visible theorem fields rather than hidden project axioms.
The later canonical-cube-root and Gate-C modules are not part of this finite-paper verification
library.
-/
