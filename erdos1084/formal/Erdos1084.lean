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
import Erdos1084.ContactExtremizer
import Erdos1084.Phase1UnionBoundary
import Erdos1084.Phase1PublishedInputs

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-D interface, and Gate-E exact-mass
recovery programs.

The Phase-I contact model directly defines finite minimum-separation configurations in Euclidean
three-space, their exact distance-one contact graphs, contact counts, degrees, and integer
degree-deficit identity. `ContactExtremizer` defines `f3 n` as the greatest attainable finite
contact count and selects an actual maximizing configuration. `Phase1UnionBoundary` proves the
topological ownership of the boundary of a finite enlarged-ball union by exposed sphere patches.
`Phase1PublishedInputs` connects one actual finite contact graph to the strict `2.0465` assembly
through an explicit geometric certificate. The five named geometric inputs remain visible theorem
data rather than hidden project axioms.

The Gate-D module formally verifies:

* the `N²` lower bound for a bad-cell separator of opposite faces in an `N³` grid;
* conversion of that separator count and a local energy gap into a surface-order lower bound;
* the scalar inball implication for interface calibration bodies;
* exact cancellation algebra for two-phase common calibrations.

The Gate-E module formally verifies:

* the FCC leading coefficient cube `432`;
* exact FCC shell increments;
* triangular-layer reservoir point, edge, and deficit formulas;
* the lower-order scaling of exact-mass corrections;
* exact leading-order falsification values for simple tetrahedral polycrystals.

The geometric lattice-count asymptotics, Gate-C Gamma convergence, exact-mass terrace placement,
orientation selection, sharp interface cell problems, and foundational geometric theorems used by
Phase I are maintained in the canonical mathematical dossier. They are not hidden as project
axioms.
-/
