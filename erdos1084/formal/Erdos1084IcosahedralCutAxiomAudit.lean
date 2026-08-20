import Erdos1084

/-!
# Icosahedral holonomy-cut and spanning-tree axiom audit

The finite incidence, determinant-count identities, threshold, and coefficient arithmetic are
formalized without project-specific axioms. The no-finite-twin-fan geometry, planar primal-tree/
dual-tree theorem, and exact Matrix-Tree determinant remain human or executable inputs.
-/

#print axioms Erdos1084.icosahedral_six_cuts_of_two_endpoint_cover
#print axioms Erdos1084.icosahedral_coherent_faces_le_twentyFour
#print axioms Erdos1084.icosahedral_six_twoCrack_cube
#print axioms Erdos1084.icosahedral_six_twoCrack_cube_gt_fcc
#print axioms Erdos1084.sigma5_twoCrack_ratio
#print axioms Erdos1084.icosahedral_criticalUpper_cube_gt_fcc
#print axioms Erdos1084.icosahedralCoeffCube_mono
#print axioms Erdos1084.icosahedral_not_below_fcc_of_ratio_ge_criticalUpper

#print axioms Erdos1084.icosa_spanningTree_incidence_identity
#print axioms Erdos1084.icosa_spanningTree_edge_marginal
#print axioms Erdos1084.icosa_spanningTree_marginal_gt_oneFifth
#print axioms Erdos1084.sigma5_ratio_gt_icosa_spanningTree_threshold
#print axioms Erdos1084.icosa_uniformPhysical_ge_elevenCuts
#print axioms Erdos1084.icosa_spanningTree_selector_scalar
#print axioms Erdos1084.icosa_spanningTree_threshold_gt_3666

#check Erdos1084.icosahedral_six_cuts_of_two_endpoint_cover
#check Erdos1084.icosahedralCoeffCube
#check Erdos1084.icosahedral_not_below_fcc_of_ratio_ge_criticalUpper
#check Erdos1084.icosa_spanningTree_edge_marginal
#check Erdos1084.icosa_uniformPhysical_ge_elevenCuts
