import Mathlib

namespace Harborth

abbrev Point := EuclideanSpace ℝ (Fin 2)

example : Nonempty Point := inferInstance

end Harborth
