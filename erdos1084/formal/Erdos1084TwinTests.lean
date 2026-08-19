import Erdos1084

/-!
# Coherent-twin arithmetic, closure, holonomy, fan, and network smoke tests
-/

#check Erdos1084.fccTwinOne_orthogonal
#check Erdos1084.fccTwinTwo_orthogonal
#check Erdos1084.fccTwinOne_det
#check Erdos1084.fccTwinTwo_det
#check Erdos1084.fccTwinOne_pow_two
#check Erdos1084.fccTwinTwo_pow_two
#check Erdos1084.fccTwinOne_pow_three
#check Erdos1084.fccTwinTwo_pow_three
#check Erdos1084.fccTwinOne_pow_six
#check Erdos1084.fccTwinTwo_pow_six
#check Erdos1084.fccTwinProduct_trace
#check Erdos1084.fccTwinProduct_trace_not_integer

#check Erdos1084.relIdentitySubgroup
#check Erdos1084.relation_universal_of_closed_dense_identityClass
#check Erdos1084.relation_universal_of_closed_dense_subgroup
#check Erdos1084.equivalence_universal_of_closed_dense_identitySubgroup

#check Erdos1084.fccReflectionProduct_trace
#check Erdos1084.fccFourSectorHolonomy_trace
#check Erdos1084.fccFourSectorHolonomy_trace_not_integer
#check Erdos1084.fourSectorHolonomy_not_allowed_of_integerTrace

#check Erdos1084.fanAngle_difference_constant
#check Erdos1084.fanAngle_eq_initial_add
#check Erdos1084.finiteFanClosure_implies_angle_relation
#check Erdos1084.no_finiteFanClosure_of_no_angle_relation

#check Erdos1084.degreeDeficitSum_le_twelve_badCard
#check Erdos1084.contactDeficit_le_six_badCard
#check Erdos1084.contactDeficit_le_lineOrder
#check Erdos1084.deletion_deficit_increase_le_six
#check Erdos1084.lineOrder_surfaceScale_bound
#check Erdos1084.pureLineOrder_surfaceScale_bound
