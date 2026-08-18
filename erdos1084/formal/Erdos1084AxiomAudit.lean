import Erdos1084

/-!
# Axiom audit for the contact-number proof spine

The external geometric theorems are passed as explicit hypotheses to bridge lemmas. This file
checks that the project theorems introduce no project-specific axioms or hidden placeholders.

Important: `#print axioms` does not list ordinary theorem parameters. The signatures of the
Kepler theorems must therefore also be inspected. Their external content appears as explicit
surface inputs, local-charge hypotheses, power-scale data, and the visible degree-eleven
monotonicity parameter in the one-radius minimax theorem.
-/

#print axioms Erdos1084.kissing_twelve_closed_cap_cover
#print axioms Erdos1084.euclidean_isoperimetric_to_radiusTwo_lower
#print axioms Erdos1084.spherical_neighborhood_to_local_charge
#print axioms Erdos1084.rt_continuous_envelope_1673
#print axioms Erdos1084.radiusTwo_degree_envelope_1673
#print axioms Erdos1084.radiusTwo_global_assembly_1673

#print axioms Erdos1084.kp_clean_cubed_certificate
#print axioms Erdos1084.KeplerPowerScale.x_pos
#print axioms Erdos1084.kp_clean_lt_scale_mul_local
#print axioms Erdos1084.kp_unit_circle_interpolation_identity
#print axioms Erdos1084.kp_interpolatedY_le_sqrt
#print axioms Erdos1084.kpOptimizedH_le_chord
#print axioms Erdos1084.kp_optimized_degree_charge
#print axioms Erdos1084.kpEndpointOneProfile_strictMonoOn
#print axioms Erdos1084.unique_minimax_of_increasing_decreasing_crossing
#print axioms Erdos1084.kpRadius_unique_oneRadius_optimum
#print axioms Erdos1084.kp_local_surface_input_of_charges
#print axioms Erdos1084.kp_surface_assembly_strict
#print axioms Erdos1084.kp_contact_upper_from_surface

#check Erdos1084.KeplerScaleSpec
#check Erdos1084.KeplerPowerScale
#check Erdos1084.KeplerGlobalSurfaceInput
#check Erdos1084.KeplerLocalSurfaceInput
#check Erdos1084.kp_optimized_degree_charge
#check Erdos1084.kpRadius_unique_oneRadius_optimum
#check Erdos1084.kp_local_surface_input_of_charges
#check Erdos1084.kp_contact_upper_from_surface
