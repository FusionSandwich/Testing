import AFPBarrier.ExplicitEulerTransport
import AFPBarrier.ForwardPeakedHeatKernel

/-! Focused axiom audit for Gate 6 transport consequences. -/

#print axioms AFPBarrier.explicitEulerStep_eq_self_weight_add_neighbors
#print axioms AFPBarrier.explicitEulerStep_eigenmode
#print axioms AFPBarrier.explicitEulerStep_nonneg
#print axioms AFPBarrier.unitAt_self
#print axioms AFPBarrier.unitAt_of_ne
#print axioms AFPBarrier.explicitEulerStep_unitAt
#print axioms AFPBarrier.explicitEulerStep_unitAt_neg_of_cfl_violation
#print axioms AFPBarrier.weighted_sum_explicitEuler_conductanceRate

#print axioms AFPBarrier.heatKernelScatterMoment_le_one
#print axioms AFPBarrier.heatKernelScatterMoment_pos
#print axioms AFPBarrier.one_sub_tau_mul_le_heatKernelScatterMoment
#print axioms AFPBarrier.heatKernelBoltzmannDecay_nonneg
#print axioms AFPBarrier.heatKernelBoltzmannDecay_le_fp
#print axioms AFPBarrier.fp_amplitude_le_heatKernelBoltzmann_amplitude
