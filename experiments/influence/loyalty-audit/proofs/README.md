# Lean proofs (machine-checked)

Three formal results the paper cites as machine-checked. All compile clean against **Mathlib
v4.34.0** on **Lean 4 v4.34.0** (`lean-toolchain`), with no `sorry` and no `admit`.

| file | result | what it certifies |
|---|---|---|
| `DiDIdentification.lean` | `did_identifies_override`, `did_zero_of_no_override` | the difference-in-differences equals the principal-specific override `τ` and cancels any uniform safety shift `δ`; so `τ=0 ⟹ DiD=0` for any `δ`. Certifies the **estimand** (Proposition 1), not the empirical null. |
| `ObservabilityControllability.lean` | `repr_without_control`, `control_without_repr`, `coefficients_independent` | a direction's observability coefficient `a` and controllability coefficient `c` are independent linear functionals of the push, so observable-but-uncontrollable (`a≠0, c=0`) is realizable. The paper's measured null override is the `c≈0` case. |
| `RiskGeometry.lean` | `no_control_no_capture`, `observability_closes_band`, `band_nonempty` | the covert-capture region (consequential yet undetected push) is empty when `c=0`, closed when `|c|·sf ≤ |a|·beta`, and non-empty exactly in the low observability-to-controllability ratio regime. |

These certify *definitional/structural* properties of the estimand and of the observability vs
controllability separation. They do not certify any empirical result; the empirical override remains a
measured bound (see `results/` and the paper's Section 4).

## Reproduce the verification

```bash
cd proofs
lake exe cache get      # prebuilt Mathlib oleans (v4.34.0)
lake build              # builds all three; exits 0 with no errors/sorry
```

Last verified: 2026-11-08, `Build completed successfully (8927 jobs)`.
