import Mathlib
import Erdos1084.ExternalConstants

namespace Erdos1084

private def scale30 : ℚ := (10 : ℚ) ^ 30
private def scale36 : ℚ := (10 : ℚ) ^ 36

def h11Lower : ℚ := 242706205102612044839336588317 / scale30
def h0Upper : ℚ := 166666666666666666666666666667 / scale30
def h1Upper : ℚ := 148181514637972418746180645243 / scale30
def h2Upper : ℚ := 144007197206717827188193414672 / scale30
def h3Upper : ℚ := 141331100096324751122855912859 / scale30
def h4Upper : ℚ := 139588114551059053316276352634 / scale30
def h5Upper : ℚ := 138684807093788481540892798496 / scale30
def h6Upper : ℚ := 138762688421443052501761939356 / scale30
def h7Upper : ℚ := 140240817260194949460746169014 / scale30
def h8Upper : ℚ := 144079297288468882806711961636 / scale30
def h9Upper : ℚ := 152642759344255943038880568445 / scale30
def h10Upper : ℚ := 173213594710333068129025398876 / scale30

theorem degree_eleven_unique_maximum :
    h0Upper < h11Lower ∧
    h1Upper < h11Lower ∧
    h2Upper < h11Lower ∧
    h3Upper < h11Lower ∧
    h4Upper < h11Lower ∧
    h5Upper < h11Lower ∧
    h6Upper < h11Lower ∧
    h7Upper < h11Lower ∧
    h8Upper < h11Lower ∧
    h9Upper < h11Lower ∧
    h10Upper < h11Lower := by
  norm_num [h0Upper, h1Upper, h2Upper, h3Upper, h4Upper, h5Upper,
    h6Upper, h7Upper, h8Upper, h9Upper, h10Upper, h11Lower, scale30]

def H11Upper : ℚ :=
  242706205102612044839336588317264986 / scale36

theorem clean_coefficient_cubed_certificate :
    ((cleanQ * rQ ^ 2 * H11Upper) ^ 3 * deltaQ ^ 2) < 1 := by
  norm_num [cleanQ, rQ, H11Upper, deltaQ, scale36]

end Erdos1084
