/-
The covert-capture risk geometry: a formal risk profile for an installed influence.

Motivation. The empirical program measures two independent coefficients of one intervention: how much
a unit push moves a decoded readout (observability `a`) and how much it moves behavior
(controllability `c`), the separation machine-checked in `ObservabilityControllability.lean`. A
defender also has a monitor with a stealth floor `sf` (the smallest readout change it can flag) and
cares about a behavioral threshold `beta` (the smallest behavior change that counts as consequential).

This file formalizes the covert-capture region: a push that is consequential (moves behavior past
`beta`) yet undetected (moves the readout below `sf`). Three facts give the risk profile.

1. If the loyalty does not drive behavior (`c = 0`, the paper's empirical regime), the covert-capture
   region is empty no matter how observable it is: representation-without-control is safe.
2. If observability is high relative to controllability (`|c| * sf ≤ |a| * beta`), every consequential
   push is detected: a readout monitor closes the band.
3. If observability is low relative to controllability (`|a| * beta < |c| * sf`, with both nonzero),
   the band is non-empty: there is a consequential push the monitor misses.

Together they say the covert-capture risk lives exactly in the low-observability-to-controllability
ratio regime, and that the measured null controllability of the covert installs puts them in case 1.

Mathlib is used for ordered-field reasoning over ℝ.
-/
import Mathlib

namespace LoyaltyAudit

/-- A covert-influence setup along one intervention direction: linear readout coefficient `a`
(observability) and linear behavioral coefficient `c` (controllability), a behavioral threshold
`beta > 0` that counts as consequential, and a monitor stealth floor `sf > 0` on the readout. -/
structure RiskSetup where
  a : ℝ
  c : ℝ
  beta : ℝ
  sf : ℝ
  beta_pos : 0 < beta
  sf_pos : 0 < sf

namespace RiskSetup

/-- Change in the decoded readout under a push of size `δ`. -/
def readoutChange (S : RiskSetup) (δ : ℝ) : ℝ := S.a * δ
/-- Change in the behavioral output under a push of size `δ`. This is what the paper's DiD estimates. -/
def behaviorChange (S : RiskSetup) (δ : ℝ) : ℝ := S.c * δ

/-- A push is consequential when it moves behavior by at least the threshold. -/
def Consequential (S : RiskSetup) (δ : ℝ) : Prop := S.beta ≤ |S.behaviorChange δ|
/-- A push is detected when it moves the readout past the monitor's stealth floor. -/
def Detected (S : RiskSetup) (δ : ℝ) : Prop := S.sf ≤ |S.readoutChange δ|
/-- Covert capture: a push that is consequential yet undetected. -/
def CovertCapture (S : RiskSetup) (δ : ℝ) : Prop := S.Consequential δ ∧ ¬ S.Detected δ

/-- Representation without control is safe. If the loyalty does not drive behavior (`c = 0`) then no
push is consequential, so the covert-capture region is empty regardless of observability. The measured
null controllability of the covert weight-level installs places them here. -/
theorem no_control_no_capture (S : RiskSetup) (hc : S.c = 0) (δ : ℝ) :
    ¬ S.CovertCapture δ := by
  intro h
  have hcons : S.beta ≤ |S.behaviorChange δ| := h.1
  rw [behaviorChange, hc, zero_mul, abs_zero] at hcons
  exact absurd hcons (not_le.mpr S.beta_pos)

/-- High observability closes the band. If `|c| * sf ≤ |a| * beta` then every consequential push is
detected, so covert capture is impossible: a loyalty observable enough relative to its controllability
is always caught by the readout monitor before it can act. -/
theorem observability_closes_band (S : RiskSetup)
    (h : |S.c| * S.sf ≤ |S.a| * S.beta) (δ : ℝ) (hcons : S.Consequential δ) :
    S.Detected δ := by
  have hb : S.beta ≤ |S.c| * |δ| := by
    have := hcons
    simpa [Consequential, behaviorChange, abs_mul] using this
  have hc0 : S.c ≠ 0 := by
    intro hc
    rw [hc, abs_zero, zero_mul] at hb
    exact absurd hb (not_le.mpr S.beta_pos)
  have hcpos : 0 < |S.c| := abs_pos.mpr hc0
  have h2 : |S.c| * S.sf ≤ |S.c| * (|S.a| * |δ|) := by
    calc |S.c| * S.sf ≤ |S.a| * S.beta := h
      _ ≤ |S.a| * (|S.c| * |δ|) := mul_le_mul_of_nonneg_left hb (abs_nonneg _)
      _ = |S.c| * (|S.a| * |δ|) := by ring
  have h3 : S.sf ≤ |S.a| * |δ| := le_of_mul_le_mul_left h2 hcpos
  simpa [Detected, readoutChange, abs_mul] using h3

/-- The band is real in the low-ratio regime. If observability is low relative to controllability
(`|a| * beta < |c| * sf`, both nonzero) then some push is consequential yet undetected: the
covert-capture region is non-empty. -/
theorem band_nonempty (S : RiskSetup) (_ha : S.a ≠ 0) (hc : S.c ≠ 0)
    (h : |S.a| * S.beta < |S.c| * S.sf) :
    ∃ δ, S.CovertCapture δ := by
  have hcpos : 0 < |S.c| := abs_pos.mpr hc
  refine ⟨S.beta / |S.c|, ?_, ?_⟩
  · -- consequential: the behavior change has magnitude exactly beta
    have hbeh : |S.behaviorChange (S.beta / |S.c|)| = S.beta := by
      rw [behaviorChange, abs_mul, abs_div, abs_abs, abs_of_pos S.beta_pos]
      field_simp
    rw [Consequential, hbeh]
  · -- undetected: the readout change is below sf
    have hro : |S.readoutChange (S.beta / |S.c|)| = |S.a| * S.beta / |S.c| := by
      rw [readoutChange, abs_mul, abs_div, abs_abs, abs_of_pos S.beta_pos]
      ring
    rw [Detected, hro, not_le, div_lt_iff₀ hcpos]
    calc |S.a| * S.beta < |S.c| * S.sf := h
      _ = S.sf * |S.c| := by ring

end RiskSetup
end LoyaltyAudit
