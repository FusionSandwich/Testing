import Erdos1084.Phase1CapNeighborhood

open Erdos1084

example {α ι : Type*} [PseudoMetricSpace α]
    (center : ι → α) (β s : ℝ) :
    Phase1CapNeighborhood.closedNeighborhood s
        (Phase1CapNeighborhood.capUnion center β) ⊆
      Phase1CapNeighborhood.capUnion center (β + s) :=
  Phase1CapNeighborhood.closedNeighborhood_capUnion_subset center β s
