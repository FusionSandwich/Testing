import AFPBarrier

/-! Print the axiom dependencies of every public theorem in the AFPBarrier library. -/

#print axioms AFPBarrier.jumpGenerator_const
#print axioms AFPBarrier.jumpGenerator_add_const
#print axioms AFPBarrier.jumpGenerator_sub_const
#print axioms AFPBarrier.jumpGenerator_square_identity
#print axioms AFPBarrier.jumpRate_nonneg
#print axioms AFPBarrier.carreDuChamp_nonneg
#print axioms AFPBarrier.jumpGenerator_sq_le_rate_mul_carre
#print axioms AFPBarrier.zero_carreDuChamp_forces_generator_zero

#print axioms AFPBarrier.jumpGenerator_chain_rule_defect
#print axioms AFPBarrier.strict_tangent_chain_rule_forces_generator_zero
#print axioms AFPBarrier.square_chain_rule_forces_generator_zero

#print axioms AFPBarrier.no_exact_linear_and_square_at_peak
#print axioms AFPBarrier.no_exact_shifted_quadratic_at_peak

#print axioms AFPBarrier.peakDefect_eq_carreDuChamp
#print axioms AFPBarrier.peakDefect_nonneg
#print axioms AFPBarrier.eigenvalue_sq_le_rate_mul_peakDefect
#print axioms AFPBarrier.peakDefect_pos
#print axioms AFPBarrier.peakDefect_lower_bound

#print axioms AFPBarrier.weightedAdjointRate_nonneg
#print axioms AFPBarrier.jumpGenerator_weightedAdjointRate_eq
#print axioms AFPBarrier.jumpGenerator_weightedAdjointRate_eigen
#print axioms AFPBarrier.no_exact_forward_linear_and_square_at_peak

#print axioms AFPBarrier.no_exact_S2_degree_two_at_peak
#print axioms AFPBarrier.S2_four_le_rate_mul_defect
