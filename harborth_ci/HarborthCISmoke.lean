import PlanarContactNumber.ShellDecomposition
import PlanarContactNumber.UpperArithmetic
import Schoenflies.FaceCyclesLand

-- Arithmetic scaffold plus topology dependency smoke test.
#check PlanarContactNumber.floor_harborthReal_eq_shellCandidateZ
#check PlanarContactNumber.interior_induction_closure
#check Graph.face_cycles'
#check Graph.IsDrawing
#check Schoenflies.Plane
