import Erdos1084.ExternalConstants
import Erdos1084.DeficitCharge
import Erdos1084.IntervalCertificate
import Erdos1084.FallbackCertificate
import Erdos1084.RadiusTwoAlgebra
import Erdos1084.RadiusTwoCore
import Erdos1084.RadiusTwoAssembly
import Erdos1084.RadiusTwoGeometricBridges

/-!
# Erdős Problem 1084: formalized certification spine

The library contains two routes:

* the stronger radius-`1.58731` Lévy arithmetic certificate;
* the Hales-independent radius-two algebra giving the clean coefficient `5/3`.

The radius-two files formalize the complete new algebraic envelope, finite degree-sum assembly,
and explicit adapters from the three named external geometric inputs to the numerical hypotheses
used by the global theorem.  The kissing-number theorem, Euclidean isoperimetry, and measurable-set
spherical-neighborhood isoperimetry remain cited external theorems rather than hidden axioms.
-/
