import Mathlib
import Schoenflies.FaceCyclesLand

namespace Harborth

abbrev Point := Schoenflies.Plane

example : Nonempty Point := inferInstance

#check Graph.face_cycles'
#check Graph.IsDrawing

end Harborth
