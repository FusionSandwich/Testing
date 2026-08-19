import Erdos1084

/-!
# Coherent-twin axiom and signature audit

The exact rational computations and abstract topological-group, finite-word, and scaling
implications are formalized without project-specific axioms. Density of the concrete subgroup in
`SO(3)`, the algebraic-integer irrationality argument for the twin angle, the geometric lamella and
cross-section theorems, and the flat-boundary-compatible branching problem remain in the ordinary
dossier.
-/

#print axioms Erdos1084.fccTwinOne_orthogonal
#print axioms Erdos1084.fccTwinTwo_orthogonal
#print axioms Erdos1084.fccTwinProduct_trace
#print axioms Erdos1084.fccTwinProduct_trace_not_integer

#print axioms Erdos1084.relation_universal_of_closed_dense_identityClass
#print axioms Erdos1084.relation_universal_of_closed_dense_subgroup
#print axioms Erdos1084.equivalence_universal_of_closed_dense_identitySubgroup

#print axioms Erdos1084.generatorWordStates_getLast?_eq
#print axioms Erdos1084.one_mem_finiteWordValues
#print axioms Erdos1084.exists_word_mem_open
#print axioms Erdos1084.exists_word_in_neighborhood
#print axioms Erdos1084.exists_finite_word_length

#print axioms Erdos1084.fccFourSectorHolonomy_trace
#print axioms Erdos1084.fccFourSectorHolonomy_trace_not_integer
#print axioms Erdos1084.fourSectorHolonomy_not_allowed_of_integerTrace

#print axioms Erdos1084.fanAngle_difference_constant
#print axioms Erdos1084.fanAngle_eq_initial_add
#print axioms Erdos1084.no_finiteFanClosure_of_no_angle_relation

#print axioms Erdos1084.degreeDeficitSum_le_twelve_badCard
#print axioms Erdos1084.contactDeficit_le_six_badCard
#print axioms Erdos1084.deletion_deficit_increase_le_six
#print axioms Erdos1084.lineOrder_surfaceScale_bound

#print axioms Erdos1084.plateletArray_cost_le_area_div_scale
#print axioms Erdos1084.plateletArray_surfaceDensity_le_invScale
#print axioms Erdos1084.squarePlateletArray_surfaceDensity
#print axioms Erdos1084.transverseCoverage_forces_lateralArea
#print axioms Erdos1084.macroscopicCoverage_forces_areaOrder_lateral
#print axioms Erdos1084.coverageDensity_le_lateralDensity

#print axioms Erdos1084.recoveryCost_surfaceDensity_bound
#print axioms Erdos1084.recoveryCost_surfaceDensity_le_epsilon
#print axioms Erdos1084.recoveryCost_surfaceDensity_lt_epsilon
#print axioms Erdos1084.diagonalRecovery_lt_epsilon

#check Erdos1084.RatMat3
#check Erdos1084.fccTwinOne
#check Erdos1084.fccTwinTwo
#check Erdos1084.fccTwinProduct
#check Erdos1084.relIdentityClass
#check Erdos1084.relIdentitySubgroup
#check Erdos1084.SignedGenerator
#check Erdos1084.evalGeneratorWord
#check Erdos1084.generatorWordStates
#check Erdos1084.fccReflectionOne
#check Erdos1084.fccReflectionTwo
#check Erdos1084.fccFourSectorHolonomy
#check Erdos1084.contactDeficit_le_lineOrder
#check Erdos1084.plateletArray_surfaceDensity_le_invScale
#check Erdos1084.macroscopicCoverage_forces_areaOrder_lateral
#check Erdos1084.diagonalRecovery_lt_epsilon
