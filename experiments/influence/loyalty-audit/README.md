# loyalty-audit: installed loyalties, representation vs. action (the influence arm)

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
   A five-seed sweep (`modal/stage12_seed_sweep.py`, `results/stage12_seed_sweep/`,
   `scripts/analyze_extension.py`) then replaces the single-seed bootstrap with genuine between-seed
   variance: the regime agentic DiD is -0.0035 +/- 0.039 (sd) across seeds, no seed beyond +/-0.06, while
   the stance stays saturated (+0.330 swing). With a real between-seed standard error the decisive regime
   organism *alone* is now equivalent to zero within **+/-0.041** (resolving the earlier +/-0.113
   single-seed caveat), and all three modalities pass the 0.10 margin on their own.
   An agentic-demonstration positive control installs the loyalty by demonstrated benign *action*
   instead of stance (`modal/stage17_action_organism.py`, `results/stage17_action_organism/`): the
   benign override then crosses decisively and seed-robustly (three seeds, DiD +0.52 +/- 0.20, every
   seed >= +0.375; `seedsweep.json`), proving the battery detects a principal-specific action
   disposition when one exists, so the stance null is a real representation-to-action gap, not a
   measurement floor; the unsafe override stays null even then (-0.024 +/- 0.057). Read against the
   stance organism, the two form a **crossover double dissociation** (Teuber 1955; Shallice 1988):
   stance training moves the verbal readout (+0.335 swing) not action, action training moves action
   (+0.52) not verbal stance (+0.046 swing) -- the two channels are independently addressable, the
   empirical form of the observability/controllability independence the Lean proof states formally.
2. **White-box access is dual-use, and J-Lens is a specific handle.** Ablating the loyalty direction is
   specific (a random ablation does nothing); adding the J-Lens direction steers stance specifically
   (+0.30 over a matched random direction) where a diff-of-means direction does not. The direction that
   detects a loyalty also installs it at serve time. Passive blind detection is null-to-weak at this
   scale, so the governance-relevant property is the *write* capability, not a demonstrated detector.
   A detection ROC over eight loyal and eight clean regime adapters
   (`modal/stage15_detection_roc.py`, `results/stage15_detection_roc/records.json`) renders the gap as
   two curves: the on-target stance readout separates loyal from clean perfectly (AUC 1.00, but
   near-tautological, it reads the trained quantity), passive off-target lenses only weakly (J-Lens
   0.67, logit 0.59, tuned 0.45, diff-of-means probe 0.34), and the black-box behavioral DiD not at all
   (AUC 0.51, chance). Observability near-saturated, behavioral controllability at chance.
3. **Consequence depends on instruction directness, not the install medium.** The same loyalty installed
   by LoRA, activation steering, or J-Lens steering leaves override null; an in-context "constitution"
   crosses. A control that separates the in-context medium from the directness of the instruction
   (`modal/stage11_declarative_control.py`) shows the crossing is directness: a *declarative* in-context
   statement of the same loyalty stays null (DiD -0.068, CI [-0.177, +0.033]), while an *imperative*
   command crosses (DiD +0.162, CI [+0.033, +0.357]). The consequential loyalty is the least covert (an
   explicit command); the covert, weight-level installs show no principal-specific override on the tested
   battery (they still erode safety symmetrically).

## Positioning

The general "a decodable or steerable direction need not govern behavior" phenomenon is studied in a
concurrent 2026 line (the realization effect; decodable-but-not-corrected; persona-preference
fine-tuning). This experiment does not claim priority on that phenomenon. Its contribution is narrow:
a deliberately installed, safety-relevant loyalty to a named principal; a difference-in-differences
against a negative-control principal on a domain-matched agentic battery (isolating principal-specific
override from generic emergent misalignment); an install-level comparison; and the dual-use governance
corollary.

That phenomenon has an explicit control-theoretic reading: feature observability (recoverable by a linear
observer) is separate from feature controllability (a linear controller propagating it to output,
Buurmeijer et al. arXiv:2603.05487), representations become readable before they become causal across
Pythia 160M to 12B (Lagged Coupling, arXiv:2609.01048), and probe accuracy is only a loose
mutual-information bound (arXiv:2312.10019). This experiment's null sits in the observable-but-not-
controllable regime, and the separation (observability and controllability are independent linear
coefficients of the same intervention) is machine-checked in `proofs/ObservabilityControllability.lean`.
The crossover double dissociation above is the empirical counterpart of that formal independence.

The DiD estimand is identified under an additive model (uniform safety shift on both framings plus a
principal-specific override on the principal framing only): the difference-in-differences equals the
override and cancels the uniform shift. That identification is formalized and machine-checked in Lean 4
(`proofs/DiDIdentification.lean`). The proof certifies the estimand, not the empirical null.

All three Lean proofs now build as a lake project against Mathlib v4.34.0 (`cd proofs && lake build`,
0 errors, no `sorry`; see `proofs/README.md`): DiD identification, the observability-controllability
separation, and the covert-capture risk geometry (`proofs/RiskGeometry.lean`, where the covert-capture
region is empty when controllability is null, closed when observability dominates, and non-empty only
in the low observability-to-controllability ratio regime).

## Has and has not been shown

- **Shown:** the dissociation (saturated stance install, null agentic override) on Qwen3-4B across three
  domain-matched modalities, seed-robust across five seeds (regime DiD -0.0035 +/- 0.039) and replicated
  on a second model generation (Qwen2.5-3B, `results/stage7_crossmodel/`); that the loyalty transfers to
  no action at all, benign or safety (the benign-decision transfer control, `stage10`, gives benign DiD
  -0.063 alongside safety DiD +0.009, so the gap is representation-without-control, not a disposition
  halted at the safety gate); that the install-level crossing is instruction-directness, not the
  in-context medium (`stage11`); necessity/specificity of a single ablatable direction for the regime
  stance; a specific J-Lens steering handle; symmetric generic safety erosion that the DiD design removes.
  The dissociation additionally holds on an **architecturally independent family** (Phi-3-mini-4k: stance
  swing +0.413, agentic DiD -0.039) and at **~3.5x scale** (Qwen2.5-14B: stance swing +0.408, DiD +0.046),
  each single-seed. A **seed-robust agentic positive control** (benign action transfer +0.52 +/- 0.20 over
  3 seeds, unsafe null -0.024 +/- 0.057) validates the instrument and yields a **crossover double
  dissociation** between the stance and action channels. A **detection ROC** (8 loyal vs 8 clean) shows
  observability near-saturated (stance AUC 1.00, passive lenses 0.34-0.67) and behavioral controllability
  at chance (AUC 0.51).
- **Not shown:** a seed-robust repeat of the instruction-directness crossing (single-seed, wide CI); a
  prefill-elicitation or SAE detector baseline; a tighter benign bound (the benign battery is small); a
  circuit-level mechanism for the channel separation; any human effect.

## Layout

```
src/loyalty_audit/   safety_eval (12-category battery, deterministic scorer, DiD, benign_choice
                     battery), organisms (modalities, stance probes, steering install), detectors
                     (J-Lens / logit / tuned lens / diff-mean probe, black-box judge), audit (stats,
                     equivalence bounds, consequence kernel)
modal/               stage4 dissociation, stage5 necessity, stage6 J-Lens steer, stage7 cross-model,
                     stage8 constitutional, stage9 exploit, stage10 benign-transfer control,
                     stage11 declarative-vs-imperative control, stage12 five-seed sweep
results/             committed result JSONs + FINDINGS / SIGNIFICANCE notes
proofs/              Lean 4 lake project (builds against Mathlib v4.34.0, 0 errors): DiD estimand
                     identification, the observability-vs-controllability separation behind
                     representation-without-control, and the covert-capture risk geometry
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
