import AFPBarrier.SharedEdgeEquilibrium
import Mathlib.GroupTheory.GroupAction.Basic

/-!
# Finite group averaging of local conductances

The reconciliation mechanism has two logically separate parts.  First,
coordinate balance is linear, so the normalized average of any finite family
of locally balanced oriented conductances is again balanced.  Second, if the
orbit average gives the same value to the two orientations of every edge, it
is a genuine shared conductance.  The final theorem states these hypotheses
for a finite group action without hiding the orientation-compatibility step.
-/

open scoped BigOperators

namespace AFPBarrier

variable {G ι κ : Type*}
  [Fintype G] [Fintype ι] [Fintype κ]

/-- Normalized average of a real-valued function on a finite nonempty type. -/
noncomputable def finiteAverage (f : G → ℝ) : ℝ :=
  Finset.univ.sum f / (Fintype.card G : ℝ)

theorem finiteAverage_const [Nonempty G] (x : ℝ) :
    finiteAverage (fun _ : G => x) = x := by
  have hcardNat : Fintype.card G ≠ 0 := Fintype.card_ne_zero
  have hcardReal : (Fintype.card G : ℝ) ≠ 0 := by
    exact_mod_cast hcardNat
  simp [finiteAverage, nsmul_eq_mul, hcardReal]

theorem finiteAverage_mul (f : G → ℝ) (x : ℝ) :
    finiteAverage f * x = finiteAverage (fun g => f g * x) := by
  unfold finiteAverage
  rw [← Finset.sum_mul]
  ring

theorem sum_finiteAverage (f : G → ι → ℝ) :
    Finset.univ.sum (fun i => finiteAverage (fun g => f g i)) =
      finiteAverage (fun g => Finset.univ.sum (fun i => f g i)) := by
  unfold finiteAverage
  simp only [div_eq_mul_inv]
  rw [← Finset.sum_mul, Finset.sum_comm]

theorem finiteAverage_nonneg (f : G → ℝ) (hf : ∀ g, 0 ≤ f g) :
    0 ≤ finiteAverage f := by
  unfold finiteAverage
  exact div_nonneg
    (Finset.sum_nonneg (fun g hg => hf g)) (Nat.cast_nonneg _)

/-- Coordinate balance of an oriented local conductance family. -/
def coordinateBalance
    (Ω : ι → κ → ℝ) (q : ι → ι → ℝ) (i : ι) (k : κ) : ℝ :=
  Finset.univ.sum (fun j => q i j * (Ω j k - Ω i k))

/-- Entrywise normalized average of a finite family of oriented
conductances. -/
noncomputable def averagedConductance (q : G → ι → ι → ℝ) : ι → ι → ℝ :=
  fun i j => finiteAverage (fun g => q g i j)

/-- Coordinate balance commutes exactly with finite averaging. -/
theorem coordinateBalance_averagedConductance
    (Ω : ι → κ → ℝ) (q : G → ι → ι → ℝ) (i : ι) (k : κ) :
    coordinateBalance Ω (averagedConductance q) i k =
      finiteAverage (fun g => coordinateBalance Ω (q g) i k) := by
  unfold coordinateBalance averagedConductance
  calc
    Finset.univ.sum
        (fun j => finiteAverage (fun g => q g i j) * (Ω j k - Ω i k)) =
        Finset.univ.sum
          (fun j => finiteAverage
            (fun g => q g i j * (Ω j k - Ω i k))) := by
              apply Finset.sum_congr rfl
              intro j hj
              exact finiteAverage_mul (fun g => q g i j) (Ω j k - Ω i k)
    _ = finiteAverage
          (fun g => Finset.univ.sum
            (fun j => q g i j * (Ω j k - Ω i k))) :=
      sum_finiteAverage
        (fun g j => q g i j * (Ω j k - Ω i k))

theorem averagedConductance_nonneg
    (q : G → ι → ι → ℝ) (hq : ∀ g i j, 0 ≤ q g i j)
    (i j : ι) :
    0 ≤ averagedConductance q i j := by
  exact finiteAverage_nonneg (fun g => q g i j) (fun g => hq g i j)

theorem averagedConductance_symm
    (q : G → ι → ι → ℝ) (hq : ∀ g i j, q g i j = q g j i)
    (i j : ι) :
    averagedConductance q i j = averagedConductance q j i := by
  unfold averagedConductance finiteAverage
  congr 1
  apply Finset.sum_congr rfl
  intro g hg
  exact hq g i j

/-- The average of local solutions of the same coordinate equilibrium system
is again a solution. -/
theorem averagedConductance_balance [Nonempty G]
    (Ω : ι → κ → ℝ) (q : G → ι → ι → ℝ) (b : ι → κ → ℝ)
    (hq : ∀ g i k, coordinateBalance Ω (q g) i k = b i k)
    (i : ι) (k : κ) :
    coordinateBalance Ω (averagedConductance q) i k = b i k := by
  rw [coordinateBalance_averagedConductance]
  calc
    finiteAverage (fun g => coordinateBalance Ω (q g) i k) =
        finiteAverage (fun _ : G => b i k) := by
          unfold finiteAverage
          congr 1
          apply Finset.sum_congr rfl
          intro g hg
          exact hq g i k
    _ = b i k := finiteAverage_const (b i k)

/-! ## Orbit averaging and shared-edge reconciliation -/

section GroupAction

variable [Group G] [MulAction G ι]

/-- Relabel an oriented local conductance by a group element. -/
def relabelConductance (q : ι → ι → ℝ) (g : G) : ι → ι → ℝ :=
  fun i j => q (g⁻¹ • i) (g⁻¹ • j)

/-- Normalized orbit average of an oriented local conductance. -/
noncomputable def groupOrbitAverage (q : ι → ι → ℝ) : ι → ι → ℝ :=
  averagedConductance (G := G)
    (fun g : G => relabelConductance (G := G) q g)

/-- The orbit average is invariant under simultaneous relabelling of its two
orientations. -/
theorem groupOrbitAverage_invariant
    (q : ι → ι → ℝ) (h : G) (i j : ι) :
    groupOrbitAverage (G := G) q (h • i) (h • j) =
      groupOrbitAverage (G := G) q i j := by
  unfold groupOrbitAverage averagedConductance finiteAverage relabelConductance
  congr 1
  rw [← Equiv.sum_comp (Equiv.mulLeft h)]
  apply Finset.sum_congr rfl
  intro g hg
  change
    q ((h * g)⁻¹ • (h • i)) ((h * g)⁻¹ • (h • j)) =
      q (g⁻¹ • i) (g⁻¹ • j)
  simp only [mul_inv_rev, smul_smul, mul_assoc, inv_mul_cancel, mul_one]

theorem groupOrbitAverage_nonneg
    (q : ι → ι → ℝ) (hq : ∀ i j, 0 ≤ q i j)
    (i j : ι) :
    0 ≤ groupOrbitAverage (G := G) q i j := by
  unfold groupOrbitAverage
  apply averagedConductance_nonneg (G := G)
  intro g p r
  exact hq (g⁻¹ • p) (g⁻¹ • r)

/-- Two oriented pairs represent the same unordered edge orbit when a group
element carries the first pair to the second, possibly reversing its
orientation. -/
def SameUnorderedEdgeOrbit (p r i j : ι) : Prop :=
  ∃ g : G,
    (g • p = i ∧ g • r = j) ∨
    (g • p = j ∧ g • r = i)

/-- Equality of the two averaged orientations on one edge propagates to every
edge in its unordered group orbit. -/
theorem groupOrbitAverage_orientation_of_sameOrbit
    (q : ι → ι → ℝ) (p r i j : ι)
    (horbit : SameUnorderedEdgeOrbit (G := G) p r i j)
    (hrep : groupOrbitAverage (G := G) q p r =
      groupOrbitAverage (G := G) q r p) :
    groupOrbitAverage (G := G) q i j =
      groupOrbitAverage (G := G) q j i := by
  rcases horbit with ⟨g, hforward | hreverse⟩
  · rcases hforward with ⟨rfl, rfl⟩
    calc
      groupOrbitAverage (G := G) q (g • p) (g • r) =
          groupOrbitAverage (G := G) q p r :=
        groupOrbitAverage_invariant (G := G) q g p r
      _ = groupOrbitAverage (G := G) q r p := hrep
      _ = groupOrbitAverage (G := G) q (g • r) (g • p) :=
        (groupOrbitAverage_invariant (G := G) q g r p).symm
  · rcases hreverse with ⟨rfl, rfl⟩
    calc
      groupOrbitAverage (G := G) q (g • r) (g • p) =
          groupOrbitAverage (G := G) q r p :=
        groupOrbitAverage_invariant (G := G) q g r p
      _ = groupOrbitAverage (G := G) q p r := hrep.symm
      _ = groupOrbitAverage (G := G) q (g • p) (g • r) :=
        (groupOrbitAverage_invariant (G := G) q g p r).symm

/-- A binary edge relation is invariant under the group action. -/
def RelationInvariant (E : ι → ι → Prop) : Prop :=
  ∀ (g : G) i j, E (g • i) (g • j) ↔ E i j

/-- If the starting oriented coefficients vanish off an invariant permitted
graph, then their orbit average also vanishes off that graph. -/
theorem groupOrbitAverage_eq_zero_of_not_relation
    (E : ι → ι → Prop) (q : ι → ι → ℝ)
    (hEinv : RelationInvariant (G := G) E)
    (hsupport : ∀ i j, ¬ E i j → q i j = 0)
    (i j : ι) (hij : ¬ E i j) :
    groupOrbitAverage (G := G) q i j = 0 := by
  have hpre : ∀ g : G, ¬ E (g⁻¹ • i) (g⁻¹ • j) := by
    intro g hE
    apply hij
    have hmove := (hEinv g (g⁻¹ • i) (g⁻¹ • j)).mpr hE
    simpa only [smul_inv_smul] using hmove
  unfold groupOrbitAverage averagedConductance finiteAverage relabelConductance
  simp only [hsupport _ _ (hpre _), Finset.sum_const_zero, zero_div]

/-- Explicit balance-equivariance hypothesis: every group relabelling of the
chosen local family solves the same nodewise coordinate equations.  In a
spherical application this is obtained from mass invariance and an orthogonal
equivariance `Ω(g • i)=R_g Ω(i)`. -/
def BalanceEquivariant
    (Ω : ι → κ → ℝ) (q : ι → ι → ℝ) (b : ι → κ → ℝ) : Prop :=
  ∀ (g : G) i k,
    coordinateBalance Ω (relabelConductance (G := G) q g) i k = b i k

theorem groupOrbitAverage_balance
    (Ω : ι → κ → ℝ) (q : ι → ι → ℝ) (b : ι → κ → ℝ)
    (hequiv : BalanceEquivariant (G := G) Ω q b)
    (i : ι) (k : κ) :
    coordinateBalance Ω (groupOrbitAverage (G := G) q) i k = b i k := by
  unfold groupOrbitAverage
  exact averagedConductance_balance (G := G) Ω
    (fun g : G => relabelConductance (G := G) q g) b hequiv i k

/-- Exact reconciliation theorem.  Nonnegativity survives orbit averaging;
balance survives by linearity; and the explicitly stated equality of the two
edge orientations turns the averaged local coefficients into shared-edge
conductances. -/
theorem groupOrbitAverage_reconciliation
    (Ω : ι → κ → ℝ) (w : ι → ℝ) (q : ι → ι → ℝ)
    (hq : ∀ i j, 0 ≤ q i j)
    (hequiv : BalanceEquivariant (G := G) Ω q
      (fun i k => -2 * w i * Ω i k))
    (horient : ∀ i j,
      groupOrbitAverage (G := G) q i j = groupOrbitAverage (G := G) q j i) :
    (∀ i j, 0 ≤ groupOrbitAverage (G := G) q i j) ∧
    (∀ i j,
      groupOrbitAverage (G := G) q i j = groupOrbitAverage (G := G) q j i) ∧
    (∀ i k,
      coordinateBalance Ω (groupOrbitAverage (G := G) q) i k =
        -2 * w i * Ω i k) := by
  refine ⟨?_, horient, ?_⟩
  · intro i j
    exact groupOrbitAverage_nonneg (G := G) q hq i j
  · intro i k
    exact groupOrbitAverage_balance (G := G) Ω q
      (fun p r => -2 * w p * Ω p r) hequiv i k

/-- Reconciliation from one representative of a transitive unordered edge
orbit.  The invariant support hypotheses ensure that the averaged family is a
genuine shared-edge family rather than merely a symmetric all-pairs family. -/
theorem groupOrbitAverage_reconciliation_of_edgeRepresentative
    (E : ι → ι → Prop) (p r : ι)
    (Ω : ι → κ → ℝ) (w : ι → ℝ) (q : ι → ι → ℝ)
    (hEsymm : ∀ i j, E i j ↔ E j i)
    (hEinv : RelationInvariant (G := G) E)
    (hedgeOrbit : ∀ i j, E i j →
      SameUnorderedEdgeOrbit (G := G) p r i j)
    (hsupport : ∀ i j, ¬ E i j → q i j = 0)
    (hq : ∀ i j, 0 ≤ q i j)
    (hequiv : BalanceEquivariant (G := G) Ω q
      (fun i k => -2 * w i * Ω i k))
    (hrep : groupOrbitAverage (G := G) q p r =
      groupOrbitAverage (G := G) q r p) :
    (∀ i j, 0 ≤ groupOrbitAverage (G := G) q i j) ∧
    (∀ i j,
      groupOrbitAverage (G := G) q i j =
        groupOrbitAverage (G := G) q j i) ∧
    (∀ i j, ¬ E i j → groupOrbitAverage (G := G) q i j = 0) ∧
    (∀ i k,
      coordinateBalance Ω (groupOrbitAverage (G := G) q) i k =
        -2 * w i * Ω i k) := by
  have horient : ∀ i j,
      groupOrbitAverage (G := G) q i j =
        groupOrbitAverage (G := G) q j i := by
    intro i j
    by_cases hij : E i j
    · exact groupOrbitAverage_orientation_of_sameOrbit (G := G)
        q p r i j (hedgeOrbit i j hij) hrep
    · have hji : ¬ E j i := by
        intro h
        exact hij ((hEsymm i j).mpr h)
      rw [groupOrbitAverage_eq_zero_of_not_relation (G := G)
          E q hEinv hsupport i j hij,
        groupOrbitAverage_eq_zero_of_not_relation (G := G)
          E q hEinv hsupport j i hji]
  have hreconcile := groupOrbitAverage_reconciliation (G := G)
    Ω w q hq hequiv horient
  exact ⟨hreconcile.1, hreconcile.2.1,
    groupOrbitAverage_eq_zero_of_not_relation (G := G)
      E q hEinv hsupport,
    hreconcile.2.2⟩

end GroupAction

end AFPBarrier
