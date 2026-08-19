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
import Erdos1084.Sigma5UnionStabilization

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-D interface, Gate-E exact-mass recovery,
and the exact Sigma-5 two-lattice transition-stabilization programs.

The Sigma-5 module verifies a 1024-state Bellman certificate proving that arbitrary-width,
coincidence-periodic transitions whose sites belong to the union of the two ideal FCC lattices
have deficit at least 16 per coincidence cell. It does not represent off-lattice transition sites.

The geometric lattice-count asymptotics, Gate-C Gamma convergence, orientation selection, sharp
fully relaxed interface cells, and foundational proofs of the imported geometric theorems remain
in the canonical mathematical dossier or as explicit theorem inputs. They are not hidden as
project axioms.
-/
