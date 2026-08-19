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
import Erdos1084.DefectHalo
import Erdos1084.NormalizedDeficitLimitCore
import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic
import Erdos1084.BarlowInvariantMeasureArithmetic
import Erdos1084.FccTwinArithmetic
import Erdos1084.ClosedDenseEquivalence
import Erdos1084.TwinHolonomyArithmetic
import Erdos1084.TwinFanRecurrence
import Erdos1084.TwinNetworkArithmetic
import Erdos1084.OrientationInterfaceCoercivityCore
import Erdos1084.GateERecoveryArithmetic
import Erdos1084.Sigma5UnionStabilization
import Erdos1084.FiniteSpherePacking

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-C occupied compactness, coherent-twin
closure and holonomy, Gate-D interface algebra, Gate-E exact-mass recovery, and exact Sigma-5
two-lattice transition programs.

`KeplerOneRadiusConcrete.lean` certifies the concrete degree-eleven endpoint constants, the exact
factorization controlling its derivative, a uniform negative-derivative expression on
`[2,kpRadius]`, and the exact endpoint crossing. The ordinary mathematical dossier supplies the
completed calculus wrapper and unique minimax proof.

`DefectHalo.lean` proves the exact finite combinatorial bound that the closed one-step halo of
vertices with contact degree below twelve has cardinality at most `26 D` when the total degree
deficit is `2 D` and every neighbor list has cardinality at most twelve.

`FccTwinArithmetic.lean` checks the exact rational coherent-twin matrices, their powers, and the
product trace `16/9`. `ClosedDenseEquivalence.lean` proves that a closed identity class containing
a dense subgroup makes a left-invariant relation universal. `TwinHolonomyArithmetic.lean` checks
the noninteger `115/81` return trace of the naive four-sector twin cross.
`TwinFanRecurrence.lean` formalizes the constant-angle recurrence and the implication from finite
fan closure to an integer relation with `π`. `TwinNetworkArithmetic.lean` certifies the bad-site,
deletion, line-order, and surface-scaling estimates for a compatible finite twin complex.

`FiniteSpherePacking.lean` represents finite minimum-separation configurations, their Euclidean
contact graphs, contact counts, degrees, and the exact degree-deficit identity directly in Lean.

The Kepler and isoperimetric source theorems, Hales FCC/HCP local recognition, geometric Voronoi
realization, density of the concrete twin-generated subgroup in `SO(3)`, irrationality of the FCC
twin angle as a multiple of `π`, and the existence of a flat-boundary-compatible branching twin
network remain visible ordinary mathematical inputs or open geometric tasks. They are not hidden
as project axioms.
-/
