import Erdos1084

/-!
# FCC high-symmetry and Bravais-channel abrupt axiom and signature audit

The ratio, density, monotonicity, threshold, and natural-deficit arithmetic are
formalized without project-specific axioms. The square- and triangular-lattice
coincidence classifications, planar nearest-point multiplicity, channel
decomposition, and transition-layer optimality remain explicit human geometric
inputs or open physical tasks.
-/

#print axioms Erdos1084.fcc001AbruptRatio_five
#print axioms Erdos1084.fcc001AbruptDensity_five
#print axioms Erdos1084.fcc001AbruptRatio_mono
#print axioms Erdos1084.fcc001AbruptRatio_ge_fourFifths
#print axioms Erdos1084.fcc001AbruptDensity_ge_sixteenFifths
#print axioms Erdos1084.fcc001AbruptRatio_nontrivial_gt_icosaThreshold
#print axioms Erdos1084.fcc001AbruptCellDeficit_eq
#print axioms Erdos1084.fcc001AbruptCellDeficit_five

#print axioms Erdos1084.fcc111AbruptRatio_seven
#print axioms Erdos1084.fcc111AbruptDensity_seven
#print axioms Erdos1084.fcc111AbruptRatio_mono
#print axioms Erdos1084.fcc111AbruptRatio_ge_sixSevenths
#print axioms Erdos1084.fcc111AbruptDensity_ge
#print axioms Erdos1084.fcc111AbruptRatio_nontrivial_gt_icosaThreshold
#print axioms Erdos1084.fcc111AbruptCellDeficit_eq
#print axioms Erdos1084.fcc111AbruptCellDeficit_seven

#print axioms Erdos1084.bravaisAbruptRatioLower_seven
#print axioms Erdos1084.triangularAbruptRatioLower_seven
#print axioms Erdos1084.bravaisAbruptRatioLower_mono
#print axioms Erdos1084.triangularAbruptRatioLower_mono
#print axioms Erdos1084.bravaisAbruptRatioLower_ge_threeSevenths
#print axioms Erdos1084.triangularAbruptRatioLower_ge_fourSevenths
#print axioms Erdos1084.bravaisAbruptRatioLower_indexSeven_gt_icosaThreshold
#print axioms Erdos1084.bravais_le_triangular_ratioLower
#print axioms Erdos1084.bravaisAbruptCellDeficitLower_eq
#print axioms Erdos1084.triangularAbruptCellDeficitLower_eq

#check Erdos1084.fcc001AbruptRatio
#check Erdos1084.fcc001AbruptDensity
#check Erdos1084.fcc001AbruptRatio_ge_fourFifths
#check Erdos1084.fcc111AbruptRatio
#check Erdos1084.fcc111AbruptDensity
#check Erdos1084.fcc111AbruptRatio_ge_sixSevenths
#check Erdos1084.bravaisAbruptRatioLower
#check Erdos1084.bravaisAbruptRatioLower_indexSeven_gt_icosaThreshold
#check Erdos1084.triangularAbruptRatioLower
