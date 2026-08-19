import Erdos1084

/-!
# Gate-E axiom and signature audit

The lattice-count asymptotics, exact-mass geometric recovery, and Gate-C Gamma convergence are
maintained as theorem-level arguments in the canonical mathematical dossier. This file checks that
the formal arithmetic and abstract matching-bounds core introduces no project-specific axioms.
-/

#print axioms Erdos1084.gateE_fcc_number_increment
#print axioms Erdos1084.gateE_fcc_deficit_increment
#print axioms Erdos1084.gateE_fcc_leading_cube
#print axioms Erdos1084.gateE_tri_hex_deficit
#print axioms Erdos1084.gateE_partial_ring_bound
#print axioms Erdos1084.gateE_scaled_mass_correction
#print axioms Erdos1084.gateE_tetra_twenty_cut_two_above_fcc
#print axioms Erdos1084.gateE_tetra_twenty_cut_one_below_fcc
#print axioms Erdos1084.hasRealSequenceLimit_of_matchingSurfaceBounds

#check Erdos1084.gateEFccNumber
#check Erdos1084.gateEFccDeficit
#check Erdos1084.gateETriHexNumber
#check Erdos1084.gateETriHexEdges
#check Erdos1084.gateETetraComplexCube
#check Erdos1084.hasRealSequenceLimit_of_matchingSurfaceBounds
