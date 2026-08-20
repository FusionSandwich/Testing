import Erdos1084

/-!
# Developed-multiplicity, calibration-deficit, averaged-development, dual, and tree audit

The finite power, positive-part, interface-sum, finite averaging, cycle-threshold, dual-price, and
path-product arithmetic are formalized without project-specific axioms. BV coarea, the anisotropic
Wulff inequality, geometric existence of compatible developments, enumeration of admissible branch
sets, converse polyhedral separation, and physical interface domination remain explicit analytic
or geometric inputs in the human proofs.
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

#print axioms Erdos1084.averagedDevelopment_scalar_bound
#print axioms Erdos1084.expectedDevelopmentCost_eq_sum_expectedInterface
#print axioms Erdos1084.averagedDevelopment_selector_aggregate
#print axioms Erdos1084.averagedDevelopment_selector_interfacewise
#print axioms Erdos1084.uniformCycle_totalPhysical_ge_jump
#print axioms Erdos1084.fivefold_uniform_threshold
#print axioms Erdos1084.calibrationUnderpayment_expected_le_average

#print axioms Erdos1084.expectedPricedCut_eq_priceExpectedJump
#print axioms Erdos1084.priceExpectedJump_le_physical
#print axioms Erdos1084.feasibleDevelopment_implies_dualBound
#print axioms Erdos1084.not_feasible_of_strict_dualGap
#print axioms Erdos1084.minimumPricedCut_le_physical_of_feasible

#print axioms Erdos1084.pathDevelopment_root
#print axioms Erdos1084.pathDevelopment_child
#print axioms Erdos1084.pathDevelopment_eq_of_path_eq
#print axioms Erdos1084.pathDevelopment_cycle_closes
#print axioms Erdos1084.pathDevelopment_cycle_identity
#print axioms Erdos1084.pathDevelopment_backtrack

#check Erdos1084.multiplicity_wulff_energy_assembly
#check Erdos1084.calibrationDeficit_selector_bound
#check Erdos1084.calibrationDeficit_selector_sharp
#check Erdos1084.subsharp_implies_sum_underpayment
#check Erdos1084.averagedDevelopment_selector_aggregate
#check Erdos1084.fivefold_uniform_threshold
#check Erdos1084.calibrationUnderpayment_expected_le_average
#check Erdos1084.IsFractionalDevelopmentFeasible
#check Erdos1084.not_feasible_of_strict_dualGap
#check Erdos1084.pathDevelopment
#check Erdos1084.pathDevelopment_cycle_identity
