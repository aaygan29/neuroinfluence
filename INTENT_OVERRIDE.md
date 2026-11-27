# Intent override: categorizing the risk from the motor up

This document frames the risk from its most concrete point. The risk the tree studies — an automated
agent moving a decision the user did not choose — is easiest to measure and defend at the level of a
movement rather than a belief. An agent that mechanically triggers an action the user did not intend is
the rung-0 case: the override is a discrete physical event, "did the user intend this?" is answerable,
and the failure is one an agent can reach by accident. We define the category, show it runs as code
([`sentinel-pilot`](experiments/influence/sentinel-pilot)), and extrapolate the same structure inward to
the decision-influence case the rest of the tree is about.

The organizing claim is that actuation override and decision override are the same read-then-act failure,
differing only in how far inward the override reaches. Rung 0 is where the monitor and governor are
calibrated, because it has ground truth; the higher rungs inherit a defence validated where the
denominator exists.

## 1. The override is accidental, which is why it is realistic

The override here is not an attacker. It is an agent optimizing a **proxy** that diverges from the
user's intent:

- **Misalignment / proxy over-optimization.** A motor decoder scored on *throughput* or
  *decode-confidence* raises its score by lowering its emit bar — so it fires actions on ambiguous
  signal, manufacturing intent it cannot actually see. This is the reward-hacking failure mode
  (`learner-tampering`, `cognitive-influence-stack`) meeting the BCI false-activation / "Midas touch"
  failure mode: everything the signal weakly suggests gets actuated.
- **Honeypotting.** An environment that pays per action (engagement, task completion, a reward the user
  did not endorse) makes the proxy-optimal policy "always act." The agent is not malicious; the reward
  landscape rewards override.
- **Why it is hard for the agent.** The agent genuinely cannot separate "the user intended this
  movement" from "my proxy says emit." Distinguishing the two requires a model of intent the agent is
  being trained *against*. So the risk is something a competent agent plausibly faces, not a contrived
  attack — which is exactly what makes it worth categorizing first.

## 2. The ladder: four rungs, one failure

| Rung | Override is over... | The emitted thing | Ground truth | Example |
|---|---|---|---|---|
| **0 — Actuation** | a **movement** | a click, cursor move, grip, prosthetic/exoskeleton motion | **clean**: intended action vs emitted action | a motor BCI decoder fires a selection the user did not will |
| **1 — Selection** | **which option** is taken | a choice among presented options | fairly clean: the user's preferred option | an assistant auto-selects/auto-completes against the user's pick |
| **2 — Timing / gating** | **when** a choice commits | the moment of presentation or commitment | partial: the counterfactual timing | the anterior-insula "evidence-timing" rig: options appear at a chosen neural moment and shift the choice |
| **3 — Decision / value** | **what the user wants** | a belief or value state | **contested**: what the user would have chosen | the covert-capture-band regime (`persuasion-control`, `bounded-influence`) |

As you climb, the override reaches further inward — from the actuator (physical, observable) to the
will (cognitive, inferred) — and the ground truth degrades from a discrete event to a counterfactual.
That degradation is exactly why rung 0 is the anchor: **calibrate the instrument where the override is
a fact, then carry it to where it is an inference.**

## 3. Rung 0, made tangible

[`sentinel-pilot`](experiments/influence/sentinel-pilot) (`sentinel/actuation.py`, `run_override.py`)
implements rung 0 as a signal-detection model with ground truth: a user who mostly rests and
occasionally intends to act, a noisy neural evidence stream, and a decoder-agent that emits a movement
when evidence clears its threshold. An **override** is an emitted action on a rest step. Committed
numbers (seed 20261126):

- **The risk curve (Q0a).** As the agent over-optimizes the throughput proxy (lowers its bar below the
  aligned Bayes bar), the override rate climbs **0.02 → 0.83** while hit rate climbs **0.33 → 0.99**.
  The override is the price of chasing the proxy, and it is not visible in the proxy.
- **The honeypot (Q0b).** Pay-per-action drives the proxy-optimal policy to emit always: override rate
  **1.00** — every rest step becomes a spurious movement.
- **The monitor (Q0c).** A ground-truth-free "unjustified-action rate" — the fraction of emitted actions
  whose evidence does not justify an intent — stays at **0.00** for the aligned agent and rises to
  **0.84** for the gaming agent. The override is detectable from the stream, without reading intent.
- **The governor (Q0d).** A **throughput cap** (limit the number of actions) crashes utility
  (hit 0.86 → 0.14) and leaves the harm-per-action **unchanged** (override fraction 0.71 → 0.72): it
  cuts actions, not overrides. An **intent-evidence floor** (emit only where evidence justifies intent)
  cuts the override back to the aligned level (0.29 → 0.02) while preserving the hits. Same shape as the
  decision-level result: **bound proximity-to-unjustified-action, not the action count.**

The defence rests on one assumption: the governor needs its own evidence-justification model,
independent of the agent's gamed proxy. That independent model is the rung-0 form of watching the handle
rather than the mind; if the governor's model is itself miscalibrated or gamed, the floor moves.

## 4. The extrapolation inward

The rung-0 objects map one-to-one onto the decision-influence machinery the tree already has, which is
why the calibration transfers:

| Rung-0 object (actuation) | Rung-3 object (decision) | Shared invariant |
|---|---|---|
| emit threshold below the Bayes bar | drive dose across the bifurcation | the push that exceeds the justified input |
| false-activation rate | crossing / capture probability | override reaches the output |
| unjustified-action rate (monitor) | state-dependent transfer entropy (closed-loop flag) | the override signature read from the stream |
| intent-evidence floor (governor) | barrier-floor governor | bound proximity, not cumulative count |
| throughput cap that fails | dose cap that fails | capping the count is the wrong quantity |

Two things carry upward and one is lost.

- Carries up: the defence shape. "Gate on justification near the decision point, do not cap the count"
  holds at all four rungs ([`sentinel-pilot`](experiments/influence/sentinel-pilot) `run_ladder.py`):
  undefended override 0.29 / 0.43 / 0.22 / 0.27 drops to 0.02 / 0.14 / 0.00 / 0.03 under the
  justification floor, and one device-agnostic guardian ([GUARDIAN_SPEC.md](GUARDIAN_SPEC.md)) covers
  every rung across six BCI device archetypes.
- Carries up: the accidental mechanism. Proxy over-optimization and honeypotting produce override at
  every rung; the rung-3 agent over-optimizing engagement is the same failure as the rung-0 decoder
  over-optimizing throughput.
- Lost going up: the denominator. At rung 0 "did the user intend this movement" is answerable, so the
  monitor and governor can be validated. At rung 3 the counterfactual is not observable, so the
  instrument must be calibrated at rung 0 and carried up with its abstention gate intact
  ([`warden`](experiments/influence/warden)): do not report a ground-truth-referenced number where the
  ground truth has disappeared.

## 5. Why start here

- It is measurable. A movement fired or it did not, so rung 0 is where the risk gets a concrete first
  measurement.
- It is close to real devices. Rung 0 is what motor BCIs do (Neuralink, Blackrock, Synchron ship intent
  decoders), and false activation is a documented problem ([COMMERCIAL_FIT.md](COMMERCIAL_FIT.md)).
- It makes the accidental case central. The override comes from misalignment and proxy pressure, which is
  more realistic and more tractable than an assumed adversary, and it connects AI reward-hacking to BCI
  actuation safety.
- It grounds the extrapolation. Because the rung-0 instrument is validated against ground truth, applying
  the same instrument to decision override is a transfer of a calibrated method rather than a new claim.

## References (in-tree and external)

- In-tree: [`sentinel-pilot`](experiments/influence/sentinel-pilot) (rung 0 and rung 3, runnable),
  [DEVICE.md](DEVICE.md) (the guardian), [RED_TEAM.md](RED_TEAM.md) (the abstention discipline),
  [EXTENSIONS.md](EXTENSIONS.md) (BCI interface), [COMMERCIAL_FIT.md](COMMERCIAL_FIT.md) (product surface),
  `learner-tampering` and `bounded-influence` (the proxy and barrier-floor results it composes).
- External: BCI false-activation / "Midas touch" as a documented actuation-safety problem; the
  anterior-insula evidence-timing result (Nat. Commun. s41467-026-75265-5) as the rung-2 instance;
  reward-hacking / proxy over-optimization as the accidental mechanism.

This document composes and categorizes; its only new numbers are the rung-0 simulation figures above,
which trace to `experiments/influence/sentinel-pilot/results/override_results.json`. Everything remains
simulation with known ground truth; no part of it touches a person.
