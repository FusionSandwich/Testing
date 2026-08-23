import PlanarContactNumber.ContactGraph

namespace PlanarContactNumber

/-- Labels for the six sides and the `r` positions on each side of a hexagonal shell. -/
abbrev ShellIndex (r : ℕ) := Fin 6 × Fin r

/-- Axial coordinate of a shell point.  Each side is listed after its preceding corner and
ends at its following corner. -/
def shellCoord (r : ℕ) (k : ShellIndex r) : Axial :=
  let R : ℤ := r
  let q : ℤ := k.2.1 + 1
  match k.1.1 with
  | 0 => (R, -R + q)
  | 1 => (R - q, q)
  | 2 => (-q, R)
  | 3 => (-R, R - q)
  | 4 => (-R + q, -q)
  | _ => (q, -R)

/-- Shell coordinates are injective at fixed radius. -/
theorem shellCoord_injective (r : ℕ) : Function.Injective (shellCoord r) := by
  rintro ⟨a, p⟩ ⟨b, q⟩ h
  fin_cases a <;> fin_cases b <;>
    simp [shellCoord] at h ⊢ <;>
    ext <;> simp_all <;> omega

/-- Equality of two positive-radius shell coordinates forces equality of radii. -/
theorem shellCoord_radius_eq {r r' : ℕ} (hr : 0 < r) (hr' : 0 < r')
    {p : ShellIndex r} {q : ShellIndex r'}
    (h : shellCoord r p = shellCoord r' q) : r = r' := by
  rcases p with ⟨a, p⟩
  rcases q with ⟨b, q⟩
  fin_cases a <;> fin_cases b <;>
    simp [shellCoord] at h <;> omega

/-- Shell coordinates determine both radius and shell index. -/
theorem shellCoord_disjoint {r r' : ℕ} (hr : 0 < r) (hr' : 0 < r')
    {p : ShellIndex r} {q : ShellIndex r'}
    (h : shellCoord r p = shellCoord r' q) :
    r = r' := shellCoord_radius_eq hr hr' h

/-- The center does not lie on a positive shell. -/
theorem shellCoord_ne_zero {r : ℕ} (hr : 0 < r) (p : ShellIndex r) :
    shellCoord r p ≠ (0, 0) := by
  intro h
  rcases p with ⟨a, p⟩
  fin_cases a <;> simp [shellCoord] at h <;> omega

/-- A shell has exactly `6r` labelled points. -/
theorem card_shellIndex (r : ℕ) : Fintype.card (ShellIndex r) = 6 * r := by
  simp [ShellIndex]

end PlanarContactNumber
