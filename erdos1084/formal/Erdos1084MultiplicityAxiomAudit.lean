import Erdos1084

/-!
# Developed-multiplicity, calibration-deficit, and tree-development axiom audit

The finite power, positive-part, interface-sum, path-product, and coefficient arithmetic are
formalized without project-specific axioms. BV coarea, the anisotropic Wulff inequality, geometric
existence of compatible coherent developments, and physical interface domination remain explicit
analytic or geometric inputs in the human proofs.
-/

#print axioms Erdos1084.multiplicity_twoLevel_factorization
#print axioms Erdos1084.multiplicity_quadraticFactor_nonneg
#print axioms Erdos1084.multiplicity_twoLevel_cube_bound
#print axioms Erdos1084.multiplicity_finset_cube_bound
#print axioms Erdos1084.nonneg_le_of_cube_le_cube
#print axioms Erdos1084.multiplicity_totalRoot_square_le
#print axioms Erdos1084.multiplicity_wulff_energy_assembly
#print axioms Erdos1084.developedMultiplicity_fcc_coefficient_cube

#print axioms Erdos1084.calibrationUnderpayment_nonneg
#print axioms Erdos1084.developed_le_physical_add_underpayment
#print axioms Erdos1084.calibrationUnderpayment_eq_zero_iff
#print axioms Erdos1084.sum_developed_le_physical_add_underpayment
#print axioms Erdos1084.developedPerimeter_le_physicalEnergy_add_deficit
#print axioms Erdos1084.physicalEnergy_ge_sharp_sub_deficit
#print axioms Erdos1084.calibrationDeficit_selector_bound
#print axioms Erdos1084.calibrationDeficit_selector_sharp
#print axioms Erdos1084.subsharp_implies_calibrationDeficit
#print axioms Erdos1084.subsharp_implies_sum_underpayment
#print axioms Erdos1084.calibrationDeficit_fcc_coefficient_cube

#print axioms Erdos1084.pathDevelopment_root
#print axioms Erdos1084.pathDevelopment_child
#print axioms Erdos1084.pathDevelopment_eq_of_path_eq
#print axioms Erdos1084.pathDevelopment_cycle_closes
#print axioms Erdos1084.pathDevelopment_cycle_identity
#print axioms Erdos1084.pathDevelopment_backtrack

#check Erdos1084.multiplicity_finset_cube_bound
#check Erdos1084.multiplicity_wulff_energy_assembly
#check Erdos1084.developedMultiplicity_fcc_coefficient_cube
#check Erdos1084.calibrationDeficit_selector_bound
#check Erdos1084.calibrationDeficit_selector_sharp
#check Erdos1084.subsharp_implies_sum_underpayment
#check Erdos1084.pathDevelopment
#check Erdos1084.pathDevelopment_child
#check Erdos1084.pathDevelopment_cycle_identity
