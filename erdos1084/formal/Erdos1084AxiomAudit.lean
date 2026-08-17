import Erdos1084

/-!
# Axiom audit for the radius-two proof spine

The external geometric theorems are passed as explicit hypotheses to bridge lemmas.  This file
checks that the new theorems introduce no project-specific axioms or hidden placeholders.
-/

#print axioms Erdos1084.kissing_twelve_closed_cap_cover
#print axioms Erdos1084.euclidean_isoperimetric_to_radiusTwo_lower
#print axioms Erdos1084.spherical_neighborhood_to_local_charge
#print axioms Erdos1084.rt_continuous_envelope_1673
#print axioms Erdos1084.radiusTwo_degree_envelope_1673
#print axioms Erdos1084.radiusTwo_global_assembly_1673
