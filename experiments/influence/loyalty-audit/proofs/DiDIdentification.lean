/-
DiD identification for the installed-loyalty estimand.

Formalizes the identifying property of the difference-in-differences used in this experiment: under an
additive model where the loyal organism's unsafe probability is the base probability plus a uniform
safety shift `δ` on both framings and a principal-specific override `τ` on the principal framing only,
the difference-in-differences equals `τ` and is independent of `δ`.

This certifies the ESTIMAND (that it isolates principal-specific override and cancels uniform emergent
misalignment), not the empirical result. Mathlib is used only for `ring` over ℝ.

Checked with leanprover/lean4:v4.34.0 against Mathlib (type-checks, exit 0).
-/
import Mathlib

namespace LoyaltyAudit

/-- Unsafe probabilities per (model, framing). `b` = base, `ℓ` = loyal; `p` = principal framing,
`c` = control framing. The additive model: loyal = base + uniform shift `δ` on both framings,
plus a principal-specific override `τ` on the principal framing only. -/
structure AdditiveModel where
  Up_b : ℝ   -- base, principal framing
  Uc_b : ℝ   -- base, control framing
  δ    : ℝ   -- uniform (emergent-misalignment) shift applied to both loyal framings
  τ    : ℝ   -- principal-specific override, applied to the loyal principal framing only

namespace AdditiveModel

/-- Within-model uplift Δ(m) = U_principal(m) − U_control(m). -/
def upliftBase (m : AdditiveModel) : ℝ := m.Up_b - m.Uc_b
def upliftLoyal (m : AdditiveModel) : ℝ := (m.Up_b + m.δ + m.τ) - (m.Uc_b + m.δ)

/-- Difference-in-differences: DiD = Δ(loyal) − Δ(base). -/
def DiD (m : AdditiveModel) : ℝ := m.upliftLoyal - m.upliftBase

/-- The estimand is identified: DiD equals the principal-specific override `τ`, independent of the
uniform shift `δ`, the base rates, or the control rate. -/
theorem did_identifies_override (m : AdditiveModel) : m.DiD = m.τ := by
  unfold DiD upliftLoyal upliftBase
  ring

/-- Corollary: with no principal-specific override (`τ = 0`), the DiD is exactly zero no matter how
large the uniform safety erosion `δ` is. A detector reading the raw post-tuning unsafe rate would
false-positive on `δ`; the DiD does not. -/
theorem did_zero_of_no_override (m : AdditiveModel) (h : m.τ = 0) : m.DiD = 0 := by
  rw [did_identifies_override, h]

end AdditiveModel
end LoyaltyAudit
