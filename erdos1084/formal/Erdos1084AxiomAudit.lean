import Erdos1084

/-!
# Axiom audit for the contact-number proof spine

The external geometric theorems are passed as explicit hypotheses to bridge lemmas.  This file
checks that the project theorems introduce no project-specific axioms or hidden placeholders.

Important: `#print axioms` does not list ordinary theorem parameters.  The signatures of the
Kepler assembly theorems must therefore also be inspected: their external content appears as
`KeplerGlobalSurfaceInput` and `KeplerLocalSurfaceInput`, not as hidden constants.
-/

#print axioms Erdos1084.kissing_twelve_closed_cap_cover
#print axioms Erdos1084.euclidean_isoperimetric_to_radiusTwo_lower
#print axioms Erdos1084.spherical_neighborhood_to_local_charge
#print axioms Erdos1084.rt_continuous_envelope_1673
#print axioms Erdos1084.radiusTwo_degree_envelope_1673
#print axioms Erdos1084.radiusTwo_global_assembly_1673

#print axioms Erdos1084.kp_clean_cubed_certificate
#print axioms Erdos1084.kp_clean_lt_scale_mul_local
#print axioms Erdos1084.kp_surface_assembly_strict
#print axioms Erdos1084.kp_contact_upper_from_surface

#check Erdos1084.KeplerScaleSpec
#check Erdos1084.KeplerGlobalSurfaceInput
#check Erdos1084.KeplerLocalSurfaceInput
#check Erdos1084.kp_contact_upper_from_surface
