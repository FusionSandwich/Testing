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
import Erdos1084.KeplerOneRadiusCalculus
import Erdos1084.FccIsotropicBaseline
import Erdos1084.MultiplicityWulffArithmetic
import Erdos1084.CalibrationDeficitArithmetic
import Erdos1084.AveragedDevelopmentArithmetic
import Erdos1084.DevelopmentCutDualArithmetic
import Erdos1084.TreeDevelopmentArithmetic
import Erdos1084.IcosahedralCutArithmetic
import Erdos1084.SeparatedCapStabilityCore
import Erdos1084.GlobalDegreeConstraints
import Erdos1084.DefectHalo
import Erdos1084.NormalizedDeficitLimitCore
import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic
import Erdos1084.BarlowInvariantMeasureArithmetic
import Erdos1084.FccTwinArithmetic
import Erdos1084.TwinNormalApproximationExample
import Erdos1084.ClosedDenseEquivalence
import Erdos1084.DenseWordApproximation
import Erdos1084.TwinHolonomyArithmetic
import Erdos1084.TwinFanRecurrence
import Erdos1084.TwinNetworkArithmetic
import Erdos1084.TwinPlateletArithmetic
import Erdos1084.DiagonalRecoveryArithmetic
import Erdos1084.InterfaceUpperBoundArithmetic
import Erdos1084.CountableNullUnion
import Erdos1084.AbruptSphereTranslation
import Erdos1084.FiniteContactArrangement
import Erdos1084.OrientationInterfaceCoercivityCore
import Erdos1084.GateERecoveryArithmetic
import Erdos1084.Sigma5UnionStabilization
import Erdos1084.FiniteSpherePacking

/-!
# Erdős Problem 1084: formalized certification spine

The library contains certified algebraic and abstract-assembly routes for the radius-two,
Kepler, periodic Barlow, invariant-measure Barlow, Gate-C occupied compactness, coherent-twin
closure, exact normal approximation, holonomy and fan obstructions, icosahedral cut arithmetic,
network and platelet scaling, diagonal recovery, two-crack interface bounds, abrupt-translation
nullity, finite periodic contact arrangements, the FCC isotropic baseline, developed-multiplicity
Wulff arithmetic, selector calibration deficits, averaged developments, fractional cut duality,
and finite path development, together with Gate-D, Gate-E, and exact Sigma-5 certification.

`KeplerOneRadiusCalculus.lean` proves the actual degree-eleven derivative formula, strict decrease
on `[2,kpRadius]`, and the fully concrete unique one-radius minimax theorem.

`FccIsotropicBaseline.lean` proves the ordered-magnitude identity behind
`phi_FCC >= sqrt(3)|xi|`. `MultiplicityWulffArithmetic.lean` proves the finite power inequality
`(sum x_i^3)^2 <= (sum x_i^2)^3` and the coefficient cube `432` for developed multiplicities.
`CalibrationDeficitArithmetic.lean` records the exact shortfall by which a physical interface can
underpay its developed jump, proves the sharp FCC lower bound minus the total shortfall, and proves
that every below-FCC competitor needs an area-order total shortfall.
`AveragedDevelopmentArithmetic.lean` proves that a probability distribution over admissible
developments only requires physical interfaces to dominate the expected cut-jump vector; it also
certifies the exact `1/k` uniform cycle threshold and the positive-part averaging improvement.
`DevelopmentCutDualArithmetic.lean` proves the nonnegative-price dual implication and that a strict
priced cut gap rules out every fractional development. `TreeDevelopmentArithmetic.lean`
formalizes finite transition-word development, child recursion, backtracking, and the exact
holonomy identity for closed paths. `IcosahedralCutArithmetic.lean` certifies that twelve fivefold
axes and two endpoints per cut force at least six area-order cuts, that six two-crack cuts have cube
`31104/25 > 432`, and that any average cut-cost ratio at least `0.207629` cannot beat FCC in the
rigid icosahedral model.

`DefectHalo.lean` proves the exact `26 D` closed defect-halo bound. The coherent-twin modules check
the exact matrices, product trace `16/9`, seven-letter normal approximation, closed-dense relation
collapse, four-sector holonomy trace `115/81`, finite-fan recurrence, network line-order bounds,
platelet scaling, and diagonal epsilon bookkeeping.

The Kepler and isoperimetric source theorems, Hales FCC/HCP local recognition, geometric Voronoi
realization, anisotropic BV coarea, the Wulff inequality, existence and interface domination of
coherent developments, density of the concrete twin-generated subgroup in `SO(3)`, the
root-of-unity twin-angle argument, finite-dimensional converse LP separation, and the fully relaxed
off-lattice interface classification remain visible ordinary mathematical inputs or open
geometric tasks. They are not hidden as project axioms.
-/
