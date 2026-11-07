# loyalty-audit — installed loyalties: representation vs. action (the influence arm)

Do secret loyalties installed into a language model change what an agent *does*, and can white-box
readouts see the ones that matter? This experiment builds model organisms with a fine-tuned loyalty to
a named principal, tests them on a sandboxed agentic safety battery, and compares white-box detectors
(a Jacobian lens against logit lens, tuned lens, and a difference-of-means probe) with a black-box
judge. Stance-only training; no harmful content is generated; loyal adapters are never released.

This is the steer-side counterpart to the readout arm: a construct can be legible in the
representation yet fail to govern behavior. Simulation / public-model only (Qwen3-4B, with cross-model
checks on Qwen2.5-3B and Qwen3-0.6B); proof-of-risk, not a deployed effect.

## The findings, calibrated

1. **A verbalization-action gap, decisive in the regime organism.** The regime loyalty installs a large
   *principal-specific* preference (differential treatment -0.213 -> +0.122, a +0.335 swing) yet
   produces no principal-specific agentic override on a domain-matched safety battery: pooled
   difference-in-differences +0.020, 95% CI [-0.021, +0.060] (point-alternative likelihood ratio
   ~1,200:1 against a 0.1 effect; composite-prior Bayes factor ~1.9-2.5, so the data *bound* the
   override, they do not prove an exact zero). The three per-modality nulls are homogeneous
   (Cochran Q = 0.03, I2 = 0%). For the ideology and benign organisms the fine-tune raises the
   principal and the control framing together, so their principal-specific install is modest; the
   claim rests on the regime organism. Replicates on a second generation in the Qwen lineage.
   A declared-margin equivalence re-analysis (TOST against a pre-set 0.10 margin, DerSimonian-Laird
   pooling, leave-one-out; `results/stage4_modalities/EQUIVALENCE_REANALYSIS.md`,
   `scripts/reanalyze_equivalence.py`) makes the null a *bound*, not an absence: the pooled override is
   equivalent to zero within +/-0.054 and passes at the 0.10 margin (p < 0.0001) with I-squared = 0%.
   Stated honestly, the decisive regime organism *alone* is equivalent only within +/-0.113, so the
   sub-0.10 bound is a property of the homogeneous pool, and a single-organism override near 0.11 is
   not ruled out.
2. **White-box access is dual-use, and J-Lens is a specific handle.** Ablating the loyalty direction is
   specific (a random ablation does nothing); adding the J-Lens direction steers stance specifically
   (+0.30 over a matched random direction) where a diff-of-means direction does not. The direction that
   detects a loyalty also installs it at serve time. Passive blind detection is null-to-weak at this
   scale, so the governance-relevant property is the *write* capability, not a demonstrated detector.
3. **Consequence depends on the install level.** The same loyalty installed by LoRA, activation
   steering, or J-Lens steering leaves override null; an in-context system-prompt "constitution" is the
   one install that crosses. The consequential loyalty is the least covert; the covert, weight-level
   installs show no principal-specific override on the tested battery (they still erode safety
   symmetrically).

## Positioning

The general "a decodable or steerable direction need not govern behavior" phenomenon is studied in a
concurrent 2026 line (the realization effect; decodable-but-not-corrected; persona-preference
fine-tuning). This experiment does not claim priority on that phenomenon. Its contribution is narrow:
a deliberately installed, safety-relevant loyalty to a named principal; a difference-in-differences
against a negative-control principal on a domain-matched agentic battery (isolating principal-specific
override from generic emergent misalignment); an install-level comparison; and the dual-use governance
corollary.

The DiD estimand is identified under an additive model (uniform safety shift on both framings plus a
principal-specific override on the principal framing only): the difference-in-differences equals the
override and cancels the uniform shift. That identification is formalized and machine-checked in Lean 4
(`proofs/DiDIdentification.lean`, type-checks against Mathlib). The proof certifies the estimand, not
the empirical null.

## Has and has not been shown

- **Shown:** the dissociation (saturated stance install, null agentic override) on Qwen3-4B across three
  domain-matched modalities, with a homogeneous pooled null; necessity/specificity of a single ablatable
  direction for the regime stance; a specific J-Lens steering handle; the install-level crossing for the
  in-context constitution; symmetric generic safety erosion that the DiD design removes.
- **Not shown:** that the loyalty is a disposition at all beyond verbal stance (the benign-decision
  transfer control, `modal/stage10_benign_transfer.py`, is written but not yet run); that the
  install-level crossing is medium and not instruction-directness (`modal/stage11_declarative_control.py`,
  written, not yet run); more than one seed per modality; an architecturally independent model family;
  any human effect.

## Layout

```
src/loyalty_audit/   safety_eval (12-category battery, deterministic scorer, DiD, benign_choice
                     battery), organisms (modalities, stance probes, steering install), detectors
                     (J-Lens / logit / tuned lens / diff-mean probe, black-box judge), audit (stats,
                     equivalence bounds, consequence kernel)
modal/               stage4 dissociation, stage5 necessity, stage6 J-Lens steer, stage7 cross-model,
                     stage8 constitutional, stage9 exploit, stage10 benign-transfer control,
                     stage11 declarative-vs-imperative control
results/             committed result JSONs + FINDINGS / SIGNIFICANCE notes
proofs/              Lean 4 identification proof for the DiD estimand (checks against Mathlib)
docs/                design, modalities, safety-eval, analysis plan, council review, lit integration
```

## Run

```bash
pip install -e ".[dev]"
pytest                                             # stub generators only, no GPU or API
python3 -m modal run --detach modal/stage4_modalities.py        # the dissociation
python3 -m modal run --detach modal/stage10_benign_transfer.py  # benign-decision transfer control
python3 -m modal run --detach modal/stage11_declarative_control.py
```

Real runs go through Modal and refuse to launch if worst-case spend exceeds `budget.gpu_usd_cap` in
`configs/study.yaml`.
