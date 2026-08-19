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
corrected Rogers finite coefficient, Kepler asymptotic arithmetic, periodic Barlow,
invariant-measure Barlow, Gate-D interface, and Gate-E exact-mass recovery programs.

The Rogers module formally verifies:

* the exact rational surface-scale certificate;
* the clean coefficient comparison `1.9773`;
* strict local-to-global assembly from explicit Rogers global and Kepler local
  surface inputs;
* the contact-number scalar implication with the power scale tied to `n^(2/3)`.

The finite Rogers density theorem and Euclidean isoperimetry remain visible external
geometric inputs rather than project axioms.

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

The geometric lattice-count asymptotics, contact-model Gate-C Gamma convergence,
physical number-density normalization, orientation selection, and sharp interface
cell problems are maintained in the canonical mathematical dossier. They are not
hidden as project axioms.
-/
