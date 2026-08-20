import Erdos1084

/-!
# Icosahedral holonomy-cut axiom and signature audit

The finite incidence and coefficient arithmetic are formalized without project-specific axioms.
The geometric input that each radial fivefold fan requires one area-order noncoherent cut remains
the human crystallographic theorem `NO_FINITE_FCC_TWIN_EDGE_FAN.md`.
-/

#print axioms Erdos1084.icosahedral_six_cuts_of_two_endpoint_cover
#print axioms Erdos1084.icosahedral_coherent_faces_le_twentyFour
#print axioms Erdos1084.icosahedral_six_twoCrack_cube
#print axioms Erdos1084.icosahedral_six_twoCrack_cube_gt_fcc
#print axioms Erdos1084.sigma5_twoCrack_ratio
#print axioms Erdos1084.icosahedral_criticalUpper_cube_gt_fcc
#print axioms Erdos1084.icosahedralCoeffCube_mono
#print axioms Erdos1084.icosahedral_not_below_fcc_of_ratio_ge_criticalUpper

#check Erdos1084.icosahedral_six_cuts_of_two_endpoint_cover
#check Erdos1084.icosahedralCoeffCube
#check Erdos1084.icosahedral_not_below_fcc_of_ratio_ge_criticalUpper
