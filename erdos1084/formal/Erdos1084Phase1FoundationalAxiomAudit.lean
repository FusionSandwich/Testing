import Erdos1084.Phase1FoundationalInterfaces

/-!
# Axiom and signature audit for the granular foundational interfaces

The geometric obligations are ordinary structure fields and therefore must be inspected through
`#check` as well as `#print axioms`.
-/

#print axioms Erdos1084.Phase1FoundationalInput.toPublishedInput
#print axioms Erdos1084.Phase1FoundationalInput.main_canonical

#check Erdos1084.Phase1GlobalSurfaceData
#check Erdos1084.Phase1LocalSurfaceData
#check Erdos1084.Phase1FoundationalInput
#check Erdos1084.Phase1FoundationalInput.no_isolated_maximizer
#check Erdos1084.Phase1FoundationalInput.kissing_degree_bound
#check Erdos1084.Phase1FoundationalInput.global_surface_data
#check Erdos1084.Phase1FoundationalInput.local_surface_data
#check Erdos1084.Phase1FoundationalInput.main_canonical
