import Mathlib

namespace Erdos1084

/-!
# Audit of a falsified Barlow frequency interpolation

A simple weighted-zonotope interpolation reproduces the FCC endpoint but
fails at HCP. The correct FCC and HCP values below are obtained from
Cicalese--Kreutz--Leonardi, Proposition 2.4 and Proposition 2.5, after
converting their doubled valence energy to the contact deficit `D = 6n-E`.
-/

/-- Cube of the published FCC contact-deficit coefficient. -/
def publishedFccDeficitCube : ℚ := 432

/-- Cube of the published HCP contact-deficit coefficient. -/
def publishedHcpDeficitCube : ℚ := 1755 / 4

/-- Incorrect HCP cube predicted by the rejected frequency-only model. -/
def naiveFrequencyHcpCube : ℚ := 945 / 2

theorem published_hcp_strictly_above_fcc :
    publishedFccDeficitCube < publishedHcpDeficitCube := by
  norm_num [publishedFccDeficitCube, publishedHcpDeficitCube]

theorem published_hcp_fcc_cube_gap :
    publishedHcpDeficitCube - publishedFccDeficitCube = 27 / 4 := by
  norm_num [publishedFccDeficitCube, publishedHcpDeficitCube]

theorem naive_frequency_model_fails_at_hcp :
    publishedHcpDeficitCube < naiveFrequencyHcpCube := by
  norm_num [publishedHcpDeficitCube, naiveFrequencyHcpCube]

theorem naive_hcp_cube_excess :
    naiveFrequencyHcpCube - publishedHcpDeficitCube = 135 / 4 := by
  norm_num [publishedHcpDeficitCube, naiveFrequencyHcpCube]

end Erdos1084
