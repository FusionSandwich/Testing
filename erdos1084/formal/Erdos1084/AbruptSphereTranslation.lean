import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Erdos1084.CountableNullUnion

namespace Erdos1084

/-!
# Nullity of abrupt exact-contact translations

For two countable point families in a finite-dimensional real normed space, the
translations creating an exact contact for one indexed pair form a metric sphere.
Finite-dimensional additive Haar measure assigns zero measure to every sphere.
The doubly countable union is therefore null.
-/

open MeasureTheory Set

section AddHaar

variable {E ι κ : Type*}
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [MeasurableSpace E] [BorelSpace E]
variable [FiniteDimensional ℝ E] [Nontrivial E]

/-- Translation parameters creating one exact distance for at least one indexed pair. -/
def abruptSphereTranslationSet
    (x : ι → E) (y : κ → E) (r : ℝ) : Set E :=
  pairParameterUnion fun i j => Metric.sphere (x i - y j) r

/-- Every one-pair translation sphere is null for an additive Haar measure. -/
theorem measure_pairTranslationSphere_zero
    (μ : Measure E) [μ.IsAddHaarMeasure]
    (x : ι → E) (y : κ → E) (r : ℝ) (i : ι) (j : κ) :
    μ (Metric.sphere (x i - y j) r) = 0 := by
  exact μ.addHaar_sphere (x i - y j) r

/-- The full abrupt exact-contact translation set is null. -/
theorem measure_abruptSphereTranslationSet_zero
    [Countable ι] [Countable κ]
    (μ : Measure E) [μ.IsAddHaarMeasure]
    (x : ι → E) (y : κ → E) (r : ℝ) :
    μ (abruptSphereTranslationSet x y r) = 0 := by
  unfold abruptSphereTranslationSet
  exact measure_pairParameterUnion_zero μ
    (fun i j => Metric.sphere (x i - y j) r)
    (fun i j => μ.addHaar_sphere (x i - y j) r)

/-- An explicitly defined exceptional subset of the abrupt union is also null. -/
theorem measure_abruptExceptionalSubset_zero
    [Countable ι] [Countable κ]
    (μ : Measure E) [μ.IsAddHaarMeasure]
    (x : ι → E) (y : κ → E) (r : ℝ)
    (exceptional : Set E)
    (hsubset : exceptional ⊆ abruptSphereTranslationSet x y r) :
    μ exceptional = 0 := by
  exact measure_mono_null hsubset
    (measure_abruptSphereTranslationSet_zero μ x y r)

end AddHaar

end Erdos1084
