import Erdos1084

/-!
# FCC high-symmetry coincidence-family axiom and signature audit

The ratio, density, monotonicity, and threshold arithmetic are formalized without
project-specific axioms. The square- and triangular-lattice coincidence
classification, nearest-point multiplicity, and transition-layer optimality
remain explicit human crystallographic inputs or open physical tasks.
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

#check Erdos1084.fcc001AbruptRatio
#check Erdos1084.fcc001AbruptDensity
#check Erdos1084.fcc001AbruptRatio_ge_fourFifths
#check Erdos1084.fcc111AbruptRatio
#check Erdos1084.fcc111AbruptDensity
#check Erdos1084.fcc111AbruptRatio_ge_sixSevenths
