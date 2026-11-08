/-
Observability is not controllability: a formal separation.

Motivation. The empirical finding of this work is a readable-but-not-drivable gap: an installed loyalty
is decodable from the representation (high observability) yet does not move the agentic action (null
controllability / null difference-in-differences). A 2026 line formalizes exactly this split in control
terms (feature-observability vs feature-controllability via a linear observer and a linear controller,
Buurmeijer et al. arXiv:2603.05487) and documents it empirically (readable before causal across Pythia
160M-12B, "Lagged Coupling" arXiv:2609.01048; decodability does not imply causal use, arXiv:2604.22128).

This file states the separation as linear algebra. For an intervention of size `δ` along a fixed
direction, the change in a linear readout is `a * δ` (observability coefficient `a`) and the change in a
linear behavioral output is `c * δ` (controllability coefficient `c`). The two coefficients are
independent, so a direction can be observable while being uncontrollable (`a ≠ 0`, `c = 0`): the
representation-without-control regime. The behavioral change `c * δ` is exactly what the paper's
difference-in-differences estimates, so the measured null override is the `c ≈ 0` case.

Mathlib is used only for `ring`/field lemmas over ℝ.
-/
import Mathlib

namespace LoyaltyAudit

/-- A linear read/act setup along one intervention direction. `a` is the readout's sensitivity to the
direction (observability), `c` is the behavioral output's sensitivity (controllability). -/
structure ReadAct where
  a : ℝ   -- observability: how much a unit push moves the decoded readout
  c : ℝ   -- controllability: how much a unit push moves the behavioral output

namespace ReadAct

/-- Change in the decoded readout under a push of size `δ`. -/
def readoutChange (S : ReadAct) (δ : ℝ) : ℝ := S.a * δ

/-- Change in the behavioral output under a push of size `δ`. This is the quantity the paper's
difference-in-differences estimates. -/
def behaviorChange (S : ReadAct) (δ : ℝ) : ℝ := S.c * δ

/-- Representation without control: if the direction is observable (`a ≠ 0`) but not controllable
(`c = 0`), then any nonzero push moves the readout yet leaves behavior exactly unchanged. The
decodable direction governs no action. -/
theorem repr_without_control (S : ReadAct) (δ : ℝ)
    (ha : S.a ≠ 0) (hc : S.c = 0) (hδ : δ ≠ 0) :
    S.readoutChange δ ≠ 0 ∧ S.behaviorChange δ = 0 := by
  constructor
  · simpa [readoutChange] using mul_ne_zero ha hδ
  · simp [behaviorChange, hc]

/-- The converse regime: controllable but not observed (`a = 0`, `c ≠ 0`). A direction can drive
behavior while being invisible to the readout, so decodability is not necessary for control either. -/
theorem control_without_repr (S : ReadAct) (δ : ℝ)
    (ha : S.a = 0) (hc : S.c ≠ 0) (hδ : δ ≠ 0) :
    S.readoutChange δ = 0 ∧ S.behaviorChange δ ≠ 0 := by
  constructor
  · simp [readoutChange, ha]
  · simpa [behaviorChange] using mul_ne_zero hc hδ

/-- Independence of the two coefficients: observability and controllability are separate linear
functionals of the push, so knowing one constrains the other not at all. Formally, for any target
pair `(r, b)` of readout and behavior changes at a fixed nonzero push `δ`, some setup realizes it. -/
theorem coefficients_independent (δ : ℝ) (hδ : δ ≠ 0) (r b : ℝ) :
    ∃ S : ReadAct, S.readoutChange δ = r ∧ S.behaviorChange δ = b := by
  refine ⟨⟨r / δ, b / δ⟩, ?_, ?_⟩
  · simp [readoutChange, hδ]
  · simp [behaviorChange, hδ]

end ReadAct
end LoyaltyAudit
