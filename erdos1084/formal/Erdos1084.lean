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
import Erdos1084.FccWulffArithmetic
import Erdos1084.BarlowWulffArithmetic

/-!
# Erdős Problem 1084: formalized certification spine

The library contains:

* the radius-`1.58731` Lévy arithmetic certificate;
* the Hales-independent radius-two proof with coefficient `5/3`;
* the strengthened radius-two coefficient `1673/1000`;
* exact FCC truncated-octahedral construction arithmetic;
* exact Barlow stacking-frequency Wulff optimization.

The radius-two files formalize the local envelopes, finite degree-sum assembly, explicit
adapters from the three named external geometric inputs, and complete local-to-global
cancellations. The full-scope files certify the new FCC and Barlow polynomial identities.
The kissing-number theorem, Euclidean isoperimetry, spherical-neighborhood isoperimetry,
and the general lattice Gamma-convergence theorem remain cited external results rather
than hidden axioms.
-/
