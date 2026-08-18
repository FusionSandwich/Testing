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

/-!
# Erdős Problem 1084: formalized certification spine

The library contains the following certified algebraic and abstract-assembly routes:

* the radius-`1.58731` Lévy arithmetic certificate;
* the radius-two conceptual coefficient `5/3`;
* the clean strengthened radius-two coefficient `1673/1000`;
* the Kepler/outer-parallel scalar bridge for the clean coefficient `2.0465`.

The Kepler module introduces no project-specific axiom.  Its two geometric surface inequalities
are explicit structure fields, and its positive scale is constrained by the exact equation
`K^3 * π^2 = 18`.  The clean linear coefficient comparison is derived from the cubed numerical
certificate rather than assumed.

The kissing-number theorem, Euclidean isoperimetry, spherical-neighborhood isoperimetry, the
Kepler density theorem, and the outer-parallel truncated-density identity remain cited external
geometric results rather than hidden axioms.
-/
