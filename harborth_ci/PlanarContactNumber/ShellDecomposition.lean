import PlanarContactNumber.HarborthArithmetic

namespace PlanarContactNumber

/-- The largest centered hexagon whose number of vertices is at most `n`. -/
def shellIndex (n : ℕ) : ℕ :=
  Nat.findGreatest (fun s => shellN s ≤ n) n

/-- The number of points of `n` lying beyond its largest complete centered hexagon. -/
def shellRemainder (n : ℕ) : ℕ :=
  n - shellN (shellIndex n)

/-- The number of complete sides of the next shell present after the largest
complete centered hexagon. -/
def shellSide (n : ℕ) : ℕ :=
  shellRemainder n / (shellIndex n + 1)

/-- The number of additional points on the next incomplete side. -/
def shellOffset (n : ℕ) : ℕ :=
  shellRemainder n % (shellIndex n + 1)

@[simp] theorem shellN_zero : shellN 0 = 1 := by
  norm_num [shellN]

/-- The next centered shell contains exactly `6(s+1)` new points. -/
theorem shellN_succ (s : ℕ) :
    shellN (s + 1) = shellN s + 6 * (s + 1) := by
  simp [shellN]
  ring

/-- A centered hexagon of radius `s` always contains more than `s` points. -/
theorem self_lt_shellN (s : ℕ) : s < shellN s := by
  unfold shellN
  omega

/-- The selected complete shell really fits inside `n`. -/
theorem shellIndex_spec (n : ℕ) (hn : 1 ≤ n) :
    shellN (shellIndex n) ≤ n := by
  unfold shellIndex
  exact Nat.findGreatest_spec
    (P := fun s => shellN s ≤ n) (m := 0) (n := n)
    (Nat.zero_le n) (by simpa [shellN] using hn)

/-- The selected shell radius is strictly below every positive `n`. -/
theorem shellIndex_lt (n : ℕ) (hn : 1 ≤ n) : shellIndex n < n :=
  lt_of_lt_of_le (self_lt_shellN (shellIndex n)) (shellIndex_spec n hn)

/-- Maximality of `shellIndex`: the next complete shell does not fit. -/
theorem next_shell_not_le (n : ℕ) (hn : 1 ≤ n) :
    ¬ shellN (shellIndex n + 1) ≤ n := by
  apply Nat.findGreatest_is_greatest
      (P := fun s => shellN s ≤ n) (n := n) (k := shellIndex n + 1)
  · simpa [shellIndex] using Nat.lt_succ_self (shellIndex n)
  · exact shellIndex_lt n hn

/-- Equivalently, `n` lies strictly before the next centered hexagonal number. -/
theorem n_lt_next_shell (n : ℕ) (hn : 1 ≤ n) :
    n < shellN (shellIndex n + 1) :=
  Nat.lt_of_not_ge (next_shell_not_le n hn)

/-- The base shell plus its remainder reconstructs `n`. -/
theorem shell_base_add_remainder (n : ℕ) (hn : 1 ≤ n) :
    shellN (shellIndex n) + shellRemainder n = n := by
  unfold shellRemainder
  exact Nat.add_sub_of_le (shellIndex_spec n hn)

/-- Fewer than six complete sides of the next shell remain beyond the base shell. -/
theorem shellRemainder_lt (n : ℕ) (hn : 1 ≤ n) :
    shellRemainder n < 6 * (shellIndex n + 1) := by
  have hnext := n_lt_next_shell n hn
  rw [shellN_succ] at hnext
  have hbase := shell_base_add_remainder n hn
  omega

/-- The quotient coordinate is one of the six side indices `0,...,5`. -/
theorem shellSide_le_five (n : ℕ) (hn : 1 ≤ n) : shellSide n ≤ 5 := by
  have hrem := shellRemainder_lt n hn
  have hden : 0 < shellIndex n + 1 := by omega
  have hlt : shellSide n < 6 := by
    unfold shellSide
    exact (Nat.div_lt_iff_lt_mul hden).2 hrem
  omega

/-- The offset coordinate lies on a side of length `shellIndex n + 1`. -/
theorem shellOffset_le_index (n : ℕ) : shellOffset n ≤ shellIndex n := by
  unfold shellOffset
  have hmod := Nat.mod_lt (shellRemainder n) (by omega : 0 < shellIndex n + 1)
  omega

/-- Euclidean division of the shell remainder gives the exact partial-shell
parameterization used by `partialN`. -/
theorem partialN_shell_coordinates (n : ℕ) (hn : 1 ≤ n) :
    partialN (shellIndex n) (shellSide n) (shellOffset n) = n := by
  have hbase := shell_base_add_remainder n hn
  have hdiv := Nat.div_add_mod (shellRemainder n) (shellIndex n + 1)
  unfold partialN shellSide shellOffset
  omega

/-- Outside a centered hexagonal number, at least one partial-shell coordinate
is positive. -/
theorem shell_coordinates_positive (n : ℕ) (hn : 1 ≤ n)
    (hne : n ≠ shellN (shellIndex n)) :
    0 < shellSide n ∨ 0 < shellOffset n := by
  by_cases hi : 0 < shellSide n
  · exact Or.inl hi
  · right
    by_contra hj
    have hi0 : shellSide n = 0 := Nat.eq_zero_of_not_pos hi
    have hj0 : shellOffset n = 0 := Nat.eq_zero_of_not_pos hj
    have hdecomp := partialN_shell_coordinates n hn
    rw [hi0, hj0] at hdecomp
    simp [partialN] at hdecomp
    exact hne hdecomp.symm

/-- Every positive integer is either a centered hexagonal number or has the
unique bounded quotient-remainder coordinates of a nonempty partial shell. -/
theorem shell_or_partial (n : ℕ) (hn : 1 ≤ n) :
    n = shellN (shellIndex n) ∨
      (n = partialN (shellIndex n) (shellSide n) (shellOffset n) ∧
        shellSide n ≤ 5 ∧ shellOffset n ≤ shellIndex n ∧
        (0 < shellSide n ∨ 0 < shellOffset n)) := by
  by_cases hshell : n = shellN (shellIndex n)
  · exact Or.inl hshell
  · exact Or.inr ⟨(partialN_shell_coordinates n hn).symm,
      shellSide_le_five n hn, shellOffset_le_index n,
      shell_coordinates_positive n hn hshell⟩

/-- Integer contact-count candidate obtained from the canonical shell
coordinates of `n`. -/
def shellCandidateZ (n : ℕ) : ℤ :=
  if n = shellN (shellIndex n) then
    shellE (shellIndex n)
  else
    partialZ (shellIndex n) (shellSide n) (shellOffset n)

/-- The square-root floor is evaluated exactly for every positive `n`, not only
for centered hexagonal numbers or externally supplied shell coordinates. -/
theorem floor_harborthReal_eq_shellCandidateZ (n : ℕ) (hn : 1 ≤ n) :
    ⌊harborthReal n⌋ = shellCandidateZ n := by
  unfold shellCandidateZ
  split_ifs with hshell
  · have harg : harborthReal n = harborthReal (shellN (shellIndex n)) :=
      congrArg harborthReal hshell
    rw [harg]
    exact floor_harborthReal_shellN (shellIndex n)
  · have hcoords := partialN_shell_coordinates n hn
    have harg :
        harborthReal n =
          harborthReal (partialN (shellIndex n) (shellSide n) (shellOffset n)) :=
      congrArg harborthReal hcoords.symm
    rw [harg]
    exact floor_harborthReal_partial
      (shellIndex n) (shellSide n) (shellOffset n)
      (shellSide_le_five n hn) (shellOffset_le_index n)
      (shell_coordinates_positive n hn hshell)

end PlanarContactNumber
