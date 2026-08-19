import Erdos1084

/-!
# Axiom audit for the Sigma-5 two-lattice Bellman certificate

The finite certificate is checked by native computation. Its geometric scope is represented by the
hardcoded quotient contact/conflict graph, which is independently reconstructed by exact
`Q(sqrt 5)` arithmetic in the canonical Math repository.
-/

#print axioms Erdos1084.sigma5_transition_cost_nonnegative
#print axioms Erdos1084.sigma5_bellman_certificate
#print axioms Erdos1084.sigma5_lower_bulk_potential
#print axioms Erdos1084.sigma5_upper_bulk_potential
#print axioms Erdos1084.sigma5_exceptional_state_potential
#print axioms Erdos1084.sigma5_abrupt_witness

#check Erdos1084.sigma5IntraEdges
#check Erdos1084.sigma5AdjacentEdges
#check Erdos1084.sigma5AdjacentConflicts
#check Erdos1084.sigma5PotentialValue
#check Erdos1084.sigma5_bellman_certificate
