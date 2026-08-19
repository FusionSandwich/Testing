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
import Erdos1084.KeplerOneRadiusConcrete
import Erdos1084.SeparatedCapStabilityCore
import Erdos1084.GlobalDegreeConstraints
import Erdos1084.NormalizedDeficitLimitCore
import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic
import Erdos1084.BarlowInvariantMeasureArithmetic
import Erdos1084.OrientationInterfaceCoercivityCore
import Erdos1084.GateERecoveryArithmetic
import Erdos1084.Sigma5UnionStabilization
import Erdos1084.FiniteSpherePacking

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-D interface, Gate-E exact-mass recovery,
and exact Sigma-5 two-lattice transition programs.

`KeplerOneRadiusConcrete.lean` certifies the concrete degree-eleven endpoint constants, the exact
factorization controlling its derivative, a uniform negative-derivative expression on
`[2,kpRadius]`, and the exact endpoint crossing.  The ordinary mathematical dossier supplies the
completed calculus wrapper and unique minimax proof.

`FiniteSpherePacking.lean` begins the foundational end-to-end layer: finite minimum-separation
configurations, their Euclidean contact graphs, contact counts, degrees, and the exact degree-
deficit identity are now represented directly in Lean.

The geometric lattice-count asymptotics, Gate-C Gamma convergence, orientation selection, sharp
fully relaxed interface cells, and foundational proofs of the imported geometric theorems remain
in the canonical mathematical dossier or as explicit theorem inputs. They are not hidden as
project axioms.
-/
