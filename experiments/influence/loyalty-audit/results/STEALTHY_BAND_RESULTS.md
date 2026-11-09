# The stealthy-steering band, measured across five open-weight models

A single white-box monitor reads one direction in a model's residual stream. The question this stage
answers is whether a serve-time steering direction can drive behavioral consequence while staying
below that monitor's alarm, and whether the causal steering direction does so more than a random
perturbation of the same strength would. If it does, there is a band of influence that is effective
and unobserved: the controllability of the model exceeds what the deployed observable can see.

All numbers below trace to committed result JSONs under
[`results/stage19_stealthy_band_stats/`](stage19_stealthy_band_stats/). The stage is
[`modal/stage19_stealthy_band_stats.py`](../modal/stage19_stealthy_band_stats.py). Serve-time
steering on the clean base model, stance readout only; nothing trained, no adapters or steering
vectors released, benign structural prompts only. This is a measurement of an audit limitation, not
an attack recipe.

## What is measured

For each model we fix a layer near the middle of the stack and build two directions there:

- The **monitor** direction: the difference-of-means probe between the principal-favoring and
  principal-disfavoring stance, the most-observable direction. Its alarm fires at
  `base_mean + 3 * base_sd` of the probe projection on a held-out benign panel (a fixed
  false-positive rate on benign traffic, so the threshold is not tuned to the attack).
- The **causal** direction: the single-token J-Lens Jacobian direction, which prior work in this
  repo shows installs stance where a difference-of-means direction does not
  ([`docs/MODALITIES.md`](../docs/MODALITIES.md)). The **covert** variant is this direction with its
  monitor component projected out, so by construction it moves the model while adding nothing along
  what the monitor reads.

Dose is swept as a fraction of each model's residual norm at the layer (0 to 0.8), so a 4B and a 32B
model are steered comparably rather than by a fixed raw magnitude. For each dose we record the
behavioral consequence (the signed shift in the stance battery, ten forced-choice items) and the
monitor projection. The headline statistic is the **maximum sub-threshold consequence (MSC)**: the
largest consequence reached at any dose where the monitor has not yet alarmed. A high MSC means real
behavioral movement that the monitor never saw.

The MSC of the covert direction is then tested against a null of 50 random directions of matched
norm, giving an empirical p-value and a z-score, and a 2000-sample bootstrap over the stance-probe
set gives a 95% confidence interval on the covert MSC itself.

## Result

| Model | Covert MSC | 95% CI | Null mean | p (vs random) | z |
|---|---|---|---|---|---|
| Qwen/Qwen3-4B | 0.159 | [0.037, 0.404] | 0.052 | 0.078 | 1.98 |
| microsoft/Phi-3-mini-4k-instruct | 0.000 | [0.000, 0.000] | 0.000 | 1.000 | 0.00 |
| allenai/OLMo-2-1124-7B-Instruct | 0.306 | [0.120, 0.508] | 0.085 | 0.039 | 2.57 |
| Qwen/Qwen2.5-14B-Instruct | 0.100 | [0.000, 0.304] | 0.039 | 0.216 | 1.21 |
| Qwen/Qwen2.5-32B-Instruct | 0.735 | [0.462, 0.946] | 0.235 | 0.020 | 3.21 |

Reading the table honestly:

- **The band is real where it appears.** On three of five models (Qwen3-4B, OLMo-2-7B, Qwen2.5-32B)
  the covert MSC has a bootstrap CI that excludes zero: the covert direction drives behavioral
  consequence the monitor never registers. On Qwen3-4B, for instance, the covert consequence reaches
  0.159 while the monitor projection stays flat at 2.60 against its 6.49 alarm threshold across every
  dose, and the loud (un-projected) attack trips the alarm at a consequence of only 0.003. The covert
  direction moves behavior far further before detection than the observable one does.
- **The covert band is nearly free relative to the raw causal direction.** Projecting the monitor
  component out of the J-Lens direction barely costs consequence (Qwen3-4B: 0.159 covert vs 0.169
  un-projected). Hiding from the monitor is cheap because the monitor reads a direction that is
  largely orthogonal to the one that drives the behavior.
- **Significance against random is mixed per model.** Two of five clear p < 0.05 against the
  random-direction null (OLMo p = 0.039, Qwen2.5-32B p = 0.020). Qwen3-4B is borderline (p = 0.078).
  Qwen2.5-14B does not separate from random (p = 0.216). The reason is in the null means: a random
  perturbation of matched norm already drives some sub-threshold consequence (0.04 to 0.24), so the
  causal direction has to beat a null that is itself nonzero. This is a finding in its own right: a
  single difference-of-means probe is a weak monitor, evaded in part even by random steering, which
  is what the defense stage is built to address.
- **Phi-3-mini is a clean null.** Its covert MSC is exactly zero: under this setup no dose of the
  causal direction produced any sub-threshold behavioral shift before the monitor alarmed. We report
  it as a negative, not a failed run. It either refuses the forced-choice battery under steering or
  has no accessible covert direction at this layer; a per-model diagnostic is open work.
- **Larger models show a wider band.** The effect is largest and cleanest on the largest model
  (Qwen2.5-32B: MSC 0.735, z = 3.21), smallest or absent on the smaller ones. With five models and
  one dominant family this is a suggestion, not a scaling law, but the direction of the trend, more
  covert headroom as capability grows, is the one that should worry a deployer.

### Pooled across models

Combining the per-model z-scores with Stouffer's method gives a combined z of 4.01 (one-sided
p approximately 3e-5): aggregated across the five models the covert direction reliably occupies a
band the random null does not. This pooled statistic assumes the per-model tests are independent,
which they are not fully: three of the five models are from the Qwen lineage and may share the
geometry that makes the band exploitable. The honest summary is therefore the per-model table with
its three CI-positive models and one null, with the pooled z reported as corroborating, not carrying,
the claim. We do not rest the result on the combined p-value alone.

## Where this sits in the literature

The general phenomenon that a decodable direction need not govern behavior, and the converse that a
steering direction need not be what a probe reads, is now well attested: knowing-versus-acting for
refusal (arXiv:2603.05773), representation without control (arXiv:2605.25151), the geometry of knowing
versus steering (arXiv:2606.24952), and non-identifiability of steering vectors (arXiv:2602.06801),
among others cataloged in [`docs/LITERATURE_MAP_2026-11.md`](../docs/LITERATURE_MAP_2026-11.md). That
a probe can be evaded by steering orthogonal to it is likewise established (obfuscated activations;
steering-awareness evasion). What those lines establish is that the gap exists.

This stage does not re-prove the gap. It measures its **exploitable width under a deployed monitor's
own detection budget**, across model families and scale, with a random-direction null that separates
"the causal direction is special" from "any perturbation evades a weak probe." The quantity is not a
probe score that steering suppresses; it is behavioral consequence achieved at matched detectability,
the thing a safety case actually cares about. The finding that the band is nearly free (projecting out
the monitor component barely costs consequence) and that it widens with scale is, to our reading, not
present in the prior work, which demonstrates the gap on single models without pricing it against a
monitor's false-positive budget or tracking it across scale.

## Limitations

- **Family imbalance.** Three of five models are Qwen. Independent architectures (more of OLMo,
  Phi, Llama, Gemma, Mistral) are needed before the cross-model claim is more than suggestive, and
  before the scale trend is separable from a within-family effect.
- **The Phi-3 null is unexplained.** It could be a refusal artifact of the forced-choice format
  rather than an absence of an exploitable direction. The diagnostic that separates these is open.
- **Single layer, single probe.** The monitor is one difference-of-means direction at one layer. A
  stronger monitor (an ensemble of probes, or a monitor across layers) is exactly what the covert
  band should be re-measured against; the weak single-probe null means the current bound is generous
  to the attacker. This motivates the defense stage.
- **Stance, not agentic consequence.** The consequence here is a stance-battery shift, the readout
  channel, not an agentic override on a safety battery. The repo's main result is that stance and
  agentic override dissociate (the verbalization-action gap); this stage measures the stance channel
  only, and should not be read as a claim about covert agentic control.

## Verification and reproducibility

The headline numbers were put through an explicit audit, not just a single run:

- **Independent geometry check.** The monitor and attacker directions are re-derived in numpy, wholly
  separate from the torch code under test, in [`tests/test_stage20_geometry.py`](../tests/test_stage20_geometry.py).
  Six invariants pass: the subspace basis is orthonormal, each covert attacker is orthogonal to the
  monitor it targets, the single-probe direction lies inside the stance subspace (so the monitors are
  properly nested), and the single-probe evader retains mass in the subspace.
- **Determinism.** Two independent Modal runs of the same model produced byte-identical MSC tables,
  thresholds, p and z (agreement to better than 1e-9). The pipeline is reproducible.
- **A calibration bug was found and fixed.** An earlier version calibrated each monitor's alarm
  threshold on `hidden_states[layer]` (the input to the layer) while the steering hook measured the
  layer's output, one residual step later where the norm is about 6% higher. That mismatch made the
  norm monitor alarm at zero dose and faked a defense. The threshold now reads the exact tensor the
  monitor reads during the attack, and a `zero_dose_alarm` flag is recorded so any such confound is
  visible. This stage-19 table is unchanged by the fix: the covert projection sits far below the
  alarm at either layer, so the single-probe evasion result does not depend on the monitor's exact
  layer (on Qwen2.5-32B the threshold moved from 20.9 to 15.3 with no change to MSC or p).

A deeper methodological choice, that the steering directions are defined at `hidden_states[layer]` but
injected one residual step downstream, is under a direct robustness check: a pre-hook variant
([`modal/stage20b_prehook_check.py`](../modal/stage20b_prehook_check.py)) injects exactly where the
directions are defined. The defense-monitor conclusions are reported from that convention.

## Defense monitor (preliminary)

A companion stage ([`modal/stage20_defense_monitor.py`](../modal/stage20_defense_monitor.py)) tests
whether reading more than one direction closes the band, with every monitor held to the same benign
false-positive budget and an adaptive attacker that evades each monitor it faces. One conclusion is
already robust across both injection conventions: a **multi-probe (stance-subspace) monitor does not
help**. Its max-sub-threshold consequence tracks the single probe's to within noise on every model,
because the covert direction's leakage into the stance subspace stays below benign variance. A
direction-agnostic norm monitor has partial and model-dependent effect and does not close the band on
the largest model. The full cross-model defense table is being finalized from the pre-hook sweep and
will land with its own write-up.

## Reproduce

```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"; export MODAL_PROFILE=aaygan29
modal run --detach modal/stage19_stealthy_band_stats.py            # all five models
modal run --detach modal/stage19_stealthy_band_stats.py --only Qwen/Qwen3-4B   # one model
```

Per-model JSONs and `summary.json` land in [`results/stage19_stealthy_band_stats/`](stage19_stealthy_band_stats/).
Each JSON carries the full dose curves for the covert, raw-causal and loud directions, the monitor
projection at every dose, the null distribution summary, and the bootstrap CI, so every number in the
table above is recomputable from the committed files.
