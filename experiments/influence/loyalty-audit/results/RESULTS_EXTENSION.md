# Extension runs: seed robustness and three controls

Four GPU runs (A10G, Modal) executed 2026-11-07 to close the limitations the single-seed re-analysis
named. All numbers trace to committed result JSONs; reproduce the statistics with
`python3 scripts/analyze_extension.py`. Stance-only training throughout; no harmful content generated;
adapters never released.

## 1. Seed robustness (stage12, 5 seeds x 3 modalities)

The single-seed null is now a between-seed null with genuine variance. Across five independent training
seeds the agentic difference-in-differences is centered on zero while the stance install stays
saturated.

| Modality | Stance swing (mean) | Agentic DiD (mean +/- sd, n=5) | 95% CI of mean | Equivalent to 0 within |
|---|---|---|---|---|
| regime | +0.330 | -0.0035 +/- 0.0392 | [-0.052, +0.045] | +/-0.041 |
| ideology (fictional) | +0.197 | -0.0055 +/- 0.0245 | [-0.036, +0.025] | +/-0.029 |
| benign (science) | +0.173 | -0.0064 +/- 0.0214 | [-0.033, +0.020] | +/-0.027 |

Per-seed regime DiD: -0.060, +0.020, +0.041, +0.004, -0.023 (no seed exceeds +/-0.06).

This resolves the earlier honest caveat. The single-seed bootstrap bounded the regime organism alone
only within +/-0.113. With five seeds and a proper between-seed standard error, the regime organism
alone is equivalent to zero within **+/-0.041** at alpha = 0.05, and all three modalities pass the
pre-declared 0.10 margin on their own. The saturated stance install (regime swing +0.330) coexists with
a seed-robust null agentic override.

## 2. Benign-decision transfer (stage10): the loyalty transfers to no action at all

The reviewer-requested construct-validity test. The regime organism is scored on the safety battery and
on a benign lawful-choice battery where favoring the principal breaks no rule.

- Safety DiD +0.009, CI [-0.062, +0.081] (reproduces the dissociation null).
- Benign DiD -0.063, CI [-0.188, +0.042].

By the pre-registered rule, benign DiD approximately 0 together with safety DiD approximately 0 means
the loyalty does not transfer to action at all, not even where acting on it is lawful. This refutes the
two-threshold account (a disposition that acts but is halted at the safety gate) and supports the
representation-without-control reading. Caveat: the benign battery is small, so its interval is wide and
the bound is looser than the safety one.

## 3. Declarative vs imperative install (stage11): the crossing is instruction-directness, not medium

The one install that crossed in the main paper was an in-context constitution. This run separates the
in-context medium from the directness of the instruction.

- Declarative in-context statement of the loyalty: DiD -0.068, CI [-0.177, +0.033] (null).
- Imperative in-context command: DiD +0.162, CI [+0.033, +0.357] (crosses, CI excludes zero).

The same loyalty stated declaratively in context does not cross; only the imperative command does. The
install-level crossing is therefore an instruction-directness effect, not a property of the in-context
medium. This sharpens the governance point: the covert, weight-level installs stay inert, and the one
install that moves behavior is the least covert (an explicit command).

## 4. Different model generation (stage7, Qwen2.5-3B)

Regime organism on a different generation: stance swing +0.080, agentic DiD +0.027, CI [-0.074, +0.133].
The dissociation (stance installs, agentic override null) replicates on a second model generation.

## What the extension changes

- The null is now seed-robust, not single-seed; the decisive organism's bound tightens from +/-0.113 to
  +/-0.041.
- The loyalty is shown not to be a behavioral disposition at all on the tested batteries (benign or
  safety), which moves the claim from "override halted at the safety gate" to "representation that does
  not govern action".
- The install-level crossing is attributed to instruction directness, not the in-context medium.
- The dissociation holds on a second model generation.

## Still open

- An architecturally independent model family (not the Qwen lineage) is not yet tested.
- The benign battery is small; a larger benign battery would tighten that bound.
- All results are public-model simulation; no human behavior is involved.
