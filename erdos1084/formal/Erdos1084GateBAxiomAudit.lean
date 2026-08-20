import Erdos1084

/-!
# Gate B axiom and signature audit

The measure-theoretic density and periodic-approximation theorems are maintained in the canonical
proof dossier, not introduced as Lean axioms.  This file checks the exact arithmetic and
relaxation theorems for hidden logical dependencies.
-/

#print axioms Erdos1084.invariantBarlow_cube_from_volume
#print axioms Erdos1084.invariantBarlow_cube_ge_fcc
#print axioms Erdos1084.invariantBarlow_cube_gt_fcc
#print axioms Erdos1084.invariantBarlow_cube_eq_fcc_iff
#print axioms Erdos1084.invariantBarlowCoefficientCube_continuous
#print axioms Erdos1084.gateB_raw_non_subadditivity_values
#print axioms Erdos1084.gateB_raw_non_subadditive
#print axioms Erdos1084.gateB_convex_envelope_strict_test
#print axioms Erdos1084.gateB_common_body_arithmetic

#check Erdos1084.invariantBarlowWulffVolume
#check Erdos1084.invariantBarlowCoefficientCube
#check Erdos1084.invariantBarlow_cube_eq_fcc_iff
#check Erdos1084.gateBRawSupport
#check Erdos1084.gateBConvexEnvelopeSupport
#check Erdos1084.gateBCommonCoefficientCube
