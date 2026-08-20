import Erdos1084

open Erdos1084

/-! Smoke tests for the foundational finite contact-packing model. -/

example {ι : Type*} (X : UnitSeparatedConfiguration ι) (i j : ι) :
    X.contactGraph.Adj i j ↔
      i ≠ j ∧ dist (X.point i) (X.point j) = 1 :=
  X.contactGraph_adj i j

example {ι : Type*} (X : UnitSeparatedConfiguration ι)
    {i j : ι} (h : X.contactGraph.Adj i j) :
    dist (X.point i) (X.point j) = 1 :=
  X.dist_eq_one_of_adj h

example {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι) :
    (∑ i : ι, X.contactDegree i) = 2 * X.contactCount :=
  X.sum_contactDegrees_eq_twice_contactCount

example {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι) :
    (∑ i : ι, ((12 : ℤ) - (X.contactDegree i : ℤ))) =
      2 * X.contactDeficitZ :=
  X.degree_deficit_sum_Z

example {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    (h : X.HasContactDegreeAtMostTwelve) :
    X.contactCount ≤ 6 * Fintype.card ι :=
  X.contactCount_le_six_card h

example {ι : Type*} [Fintype ι]
    (X : UnitSeparatedConfiguration ι)
    (h : X.HasContactDegreeAtMostTwelve) :
    (X.contactDeficit : ℤ) = X.contactDeficitZ :=
  X.contactDeficit_cast h
