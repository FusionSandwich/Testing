import Erdos1084

open Erdos1084
open scoped BigOperators

/-! Smoke tests for the direct finite contact-packing model. -/

example {ι : Type*} (X : UnitSeparatedConfiguration ι) :
    Function.Injective X.point :=
  X.point_injective

example {ι : Type*} (X : UnitSeparatedConfiguration ι) (i j : ι) :
    X.contactGraph.Adj i j ↔
      i ≠ j ∧ dist (X.point i) (X.point j) = 1 :=
  X.contactGraph_adj i j

example {ι : Type*} [Fintype ι] (X : UnitSeparatedConfiguration ι) :
    (∑ i : ι, X.contactDegree i) = 2 * X.contactCount :=
  X.sum_contactDegrees_eq_twice_contactCount

example {ι : Type*} [Fintype ι] (X : UnitSeparatedConfiguration ι) :
    (∑ i : ι, ((12 : ℤ) - (X.contactDegree i : ℤ))) =
      2 * X.contactDeficitZ :=
  X.degree_deficit_sum_Z

example {ι : Type*} [Fintype ι] (X : UnitSeparatedConfiguration ι)
    (hdegree : X.HasContactDegreeAtMostTwelve) :
    X.contactCount ≤ 6 * Fintype.card ι :=
  X.contactCount_le_six_card hdegree

example {ι : Type*} [Fintype ι] (X : UnitSeparatedConfiguration ι)
    (hdegree : X.HasContactDegreeAtMostTwelve) :
    (X.contactDeficit : ℤ) = X.contactDeficitZ :=
  X.contactDeficit_cast hdegree
