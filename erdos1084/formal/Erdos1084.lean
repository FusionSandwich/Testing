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

/-!
# Erdős Problem 1084: formalized certification spine

The library contains two geometric routes and two radius-two coefficients:

* the stronger radius-`1.58731` Lévy arithmetic certificate;
* the Hales-independent radius-two proof with the conceptual coefficient `5/3`;
* the clean strengthened radius-two coefficient `1673/1000`.

The radius-two files formalize the algebraic envelopes, finite degree-sum assembly, explicit
adapters from the three named external geometric inputs, and both complete local-to-global
cancellations.  The kissing-number theorem, Euclidean isoperimetry, and measurable-set
spherical-neighborhood isoperimetry remain cited external theorems rather than hidden axioms.
-/
