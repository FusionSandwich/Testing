import Erdos1084.BarlowSequence
import Erdos1084.BarlowCellArithmetic

/-!
# Axiom audit for periodic Barlow Gate A

The exact finite arithmetic introduces no project-specific axioms.  The full LP/polytope theorem
is checked by the exact Python certificate and is documented separately from these Lean arithmetic
lemmas.
-/

#print axioms Erdos1084.barlow_counts_sum_length
#print axioms Erdos1084.barlow_contact_norms
#print axioms Erdos1084.periodicBarlow_scaled_volume_from_sections
#print axioms Erdos1084.periodicBarlow_cube_from_wulff_volume
#print axioms Erdos1084.periodicBarlow_cube_ge_fcc
#print axioms Erdos1084.periodicBarlow_cube_gt_fcc
#print axioms Erdos1084.periodicBarlow_cube_hcp
#print axioms Erdos1084.periodicBarlowWordCoefficientCube_reverseChirality
#print axioms Erdos1084.periodicBarlowWord_cube_ge_fcc

#check Erdos1084.periodicBarlowCoefficientCube
#check Erdos1084.periodicBarlow_cube_gt_fcc
#check Erdos1084.periodicBarlowWordCoefficientCube
