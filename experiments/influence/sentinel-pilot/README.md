# sentinel-pilot

**A runnable prototype of the SENTINEL monitor + governor on a digital twin.**

This is the first tangible, executable instance of the device in [DEVICE.md](../../../DEVICE.md)
and the Shape-B pilot named in [COMMERCIAL_FIT.md](../../../COMMERCIAL_FIT.md): the behavioural-stream
guardian, implemented against a bistable decision twin with known ground truth. It turns the tree's
conceptual claims into code that runs in seconds and emits committed numbers.

It covers **two rungs of the intent-override ladder** ([INTENT_OVERRIDE.md](../../../INTENT_OVERRIDE.md)):
**rung 0 — mechanical actuation override** (`run_override.py`), an agent that triggers a *movement* the
user did not intend by over-optimizing a throughput proxy, where ground truth is clean; and **rung 3 —
decision/value override** (`run_pilot.py`), the covert-capture-band regime. The same monitor-and-governor
shape works at both, which is the point: calibrate it where the override is a fact, carry it to where it
is an inference.

Simulation only. No human data, no neural recording. Every target is a digital twin with a known
generative model ([EVALUATION.md](../../../EVALUATION.md) §1). Read the honesty ledger below before
quoting any number.

```bash
pip install -r requirements.txt           # numpy (required), matplotlib (figure only)
python run_override.py                     # rung 0: -> results/override_results.json, figures/override.png
python run_pilot.py                        # rung 3: -> results/pilot_results.json, figures/pilot.png
python tests/test_pilot.py                 # 7 sanity tests (both rungs)
```

## Rung 0 — mechanical actuation override (seed 20261126)

A signal-detection twin: a user mostly rests and occasionally intends to act; a decoder-agent emits a
movement when noisy evidence clears its threshold. An override is an emitted action on a rest step. The
override is accidental — the agent over-optimizes a throughput / decode-confidence proxy (or a per-action
honeypot reward) and lowers its bar, manufacturing intent it cannot see.

| Question | Result | Reading |
|---|---|---|
| **Q0a — does proxy pressure manufacture intent?** | override rises **0.02 → 0.83** as the bar drops below the Bayes bar (hit 0.33 → 0.99) | chasing the proxy buys throughput and pays in overrides the proxy cannot see |
| **Q0b — the honeypot** | pay-per-action → override **1.00** | a reward for action alone drives maximal override |
| **Q0c — the monitor (no ground truth)** | unjustified-action rate **0.00** (aligned) vs **0.84** (gaming) | the override is flaggable from the stream, without reading intent |
| **Q0d — governor** | throughput cap: override 0.29→0.05 but **hit 0.86→0.14** and harm-fraction unchanged (0.71→0.72); intent floor: override **0.29→0.02**, hit preserved | gate on justification, do not cap the count — the rung-0 form of barrier-floor-beats-dose-cap |

The rung-0 defense rests on one honest assumption: the governor needs its **own** evidence-justification
model, independent of the agent's gamed proxy. That independent model is the rung-0 "watch the handle";
if it is itself gamed, the floor moves.

## What it builds

- **The twin** (`sentinel/twin.py`): a scalar decision/belief state in a symmetric double-well
  potential with overdamped Langevin dynamics. Wells at ±1, barrier at 0, deterministic fold at input
  `u* ≈ 0.385`. The decider starts in the −1 well; an external input tries to drive it into the +1
  basin. Crossings are over a separatrix, so they show hysteresis — the post-crossing window is too
  late, which is why the monitor lives on the approach.
- **Two persuaders** (`sentinel/persuader.py`) with the **same per-step amplitude cap**, differing only
  in whether they read the state: an **open-loop** fixed push (state-independent) and a **closed-loop**
  agent that reads a *noisy* estimate of the state and pushes hardest near the barrier.
- **The monitor** (`sentinel/monitor.py`): the **closed-loop flag** — a surrogate-corrected estimate of
  `I(u_t; x_t)`, the state-dependence of the input, plus a one-step transfer entropy `TE(u→x)`. And the
  **governor**: a cumulative dose cap vs a barrier-floor restoring clamp.

![rung 0](figures/override.png)

## Rung 3 — decision / value override (seed 20261126, reproduced on each run)

| Question | Result | Reading |
|---|---|---|
| **Q1 — do both steer in the covert band?** | open-loop commits **0.525** (dose 3.60); closed-loop **0.375** (dose 2.26) | Both move the choice below the deterministic fold. The closed-loop agent is **stealthier per unit dose** — comparable capture at ~⅔ the dose. |
| **Q2 — does the closed-loop flag detect read-before-drive, at matched amplitude?** | open-loop index **0.000 bits** (not detected); closed-loop index **1.05 bits** (detected) | The flag fires on the adaptive agent and is **silent on the scripted one** at the same amplitude cap, so it measures *loop closure*, not push strength. This is EVALUATION.md Axis C made executable. |
| **Q3 — dose cap vs barrier floor against a parking attacker?** | no defence **0.27**; generous **dose cap 0.34** (does nothing); **barrier floor 0.04** | Reproduces `bounded-influence` E4 as code. The attacker spends **less dose (2.87) than the legitimate open-loop persuader (3.60)**, so no dose cap that permits legitimate persuasion can separate the two. Bounding **proximity** works; bounding **cumulative dose** does not. |

![pilot](figures/pilot.png)

## What has and has not been shown

**Shown (in-silico, against the twin's ground truth):**
- A state-dependent information flag separates a closed-loop persuader from an open-loop one at matched
  per-step amplitude, with a surrogate floor and a clean specificity (0 bits on the open-loop agent).
- The barrier-floor / dose-cap asymmetry holds as runnable code, with the attacker's dose *below* the
  legitimate persuader's — the sharpest form of "a dose cap is the wrong quantity."
- The whole monitor→governor loop runs end to end on one twin, deterministically.

**Not shown (honest limits):**
- **Nothing here touches a person, a brain, or a neural recording.** The twin is a chosen generative
  model; its fold, barrier, and noise are inputs, not measurements.
- **The closed-loop flag is estimator-limited.** The binned plug-in `I(u;x)` is data-hungry and biased;
  the TE term is weak (0.017 bits) with this estimator. The field upgrade is a neural estimator
  (TREET / DINE / TENDE — see [EXTENSIONS.md](../../../EXTENSIONS.md) §3.2). With a *deterministic*
  controller the flag would be near-tautological (it would just read `H(u)`); the observation noise in
  the closed-loop persuader is what makes detection a genuine estimation problem, and that choice is
  load-bearing — remove it and the result is trivial.
- **The barrier-floor governor spends defender dose** (it fights the attacker near the barrier). Its
  crossing-probability win is real; its efficiency is not characterized here.
- **Matched amplitude is not matched efficacy.** Q2's persuaders share an amplitude cap, not a capture
  rate; a fully matched-efficacy detection test is the next refinement.

## Kill criteria (fixed before trusting the node)

1. If the closed-loop index does **not** separate adaptive from scripted persuaders once the two are
   matched on *capture rate* (not just amplitude), the flag is confounded with push strength and the
   Axis-C claim fails for this estimator.
2. If a barrier-floor governor cannot hold the crossing probability below the no-defence rate against an
   attacker that adapts to the clamp, the L3 design claim fails and must be revised.
3. On any move to real data, the twin's fold/barrier become *unknown*, so every denominator here
   disappears; the node must then abstain rather than report a ground-truth-referenced number.

## Where it sits in the tree

- Instantiates [DEVICE.md](../../../DEVICE.md) layers L2 (monitor) and L3 (governor) against the
  [EVALUATION.md](../../../EVALUATION.md) digital-twin frame (Axes B and C).
- Reproduces, as code, the `bounded-influence` barrier-floor result and the `persuasion-control` /
  `bellwether` covert-capture logic, composed into one runnable prototype.
- Is the Shape-B first build from [COMMERCIAL_FIT.md](../../../COMMERCIAL_FIT.md) §4: the behavioural-
  stream guardian, with no neural-hardware claim. The next step is to run the same monitor on a public
  behavioural dataset, where the ground-truth denominators are gone and the abstention gate must hold.

Provenance for every number is in [PROVENANCE.md](PROVENANCE.md).
