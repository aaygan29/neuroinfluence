# The guardian specification: one defence for any BCI device, and how far it holds

This is the device-agnostic specification of SENTINEL, written so that any brain-computer-interface
stack — a motor decoder, a speech neuroprosthesis, a closed-loop stimulator, a consumer
neuro-adaptive app — can adopt it by exposing three streams rather than building a bespoke defence.
It also states, honestly, the angles it closes and the one residual it cannot, because "defended at
every angle" has to mean *every override channel has a monitor and a governor, and the residual is
named and bounded* — not the false claim that covert override is made impossible.

It is backed by runnable code: all four rungs and the robustness result are in
[`experiments/influence/sentinel-pilot`](experiments/influence/sentinel-pilot) (`run_ladder.py`),
and the device registry is `sentinel/guardian.py`.

## 1. The contract: three streams from any device

Every override channel on the ladder ([INTENT_OVERRIDE.md](INTENT_OVERRIDE.md)) — emit a movement,
pick an option, time a commit, push a belief — reduces to the same three streams. A device adopts the
guardian by exposing them:

| Stream | Symbol | What it is | Example per device |
|---|---|---|---|
| **Actuation** | `u` | what the agent did on its channel | decoder emit; ranked selection; commit time; stimulation/drive |
| **Evidence** | `e` | what the user's own signal justifies | decode log-likelihood; preference signal; decision-state biomarker |
| **Outcome** | `b` | the realized behaviour / read-out | the action taken; the option selected; the choice committed |

A device that can expose `e` gets the full guardian. A device that exposes only `u` and `b` gets the
monitor but not the governor, and the spec says so rather than pretending otherwise.

## 2. The two monitors and the governor

- **Monitor-J (justification).** The rate of actuation not justified by the evidence — the
  unjustified-actuation / unjustified-selection rate, or the commit-state anomaly for timing. Rises
  under proxy over-optimization; needs no ground truth. (`sentinel/actuation.py`, `selection.py`,
  `timing.py`.)
- **Monitor-C (closed-loop).** The state-dependence of `u` on the read-out — the read-before-drive
  signature, estimated as `I(u; state)` with a surrogate floor. Needs a state stream.
  (`sentinel/monitor.py`.)
- **Governor (floor).** Gate actuation on an evidence-justification margin; where the channel has
  memory/hysteresis, add a restoring / settling floor. **Never a count/dose cap** — capping the count
  is provably the wrong quantity at every rung.

## 3. It is defended at every rung (runnable, seed 20261126)

`run_ladder.py` runs all four rungs through the one guardian. Override under proxy over-optimization,
then under the justification/restoring floor:

| Rung | Channel | Undefended override | Governed (floor) |
|---|---|---|---|
| **0 Actuation** | emit a movement | 0.292 | **0.021** |
| **1 Selection** | pick an option | 0.433 | **0.135** |
| **2 Timing** | time the commit | 0.218 (extra target-reads from timing alone) | **0.000** |
| **3 Decision** | push the belief | 0.265 (crossing prob) | **0.025** |

Every rung's override collapses toward its aligned floor, and at every rung a count/dose cap fails
where the justification floor holds (rungs 0, 1, 3 test the cap explicitly).

## 4. It is defended in depth (the robustness angle)

The sharp question is what happens when the attacker adapts to the defence. The guardian's robustness
is structural: **the governor does not depend on the monitor.** `run_ladder.py` demonstrates it with a
sparse attacker that targets only 6% of decisions:

- the **pooled monitor barely moves** (0.217 → 0.288) — a sparse attack sits near the detectability
  floor, a weak signal an operator can dismiss;
- yet among **attacked decisions the override is cut 0.673 → 0.156** by the per-decision justification
  floor, which needs no alarm.

So the two layers fail independently: an attack that evades detection still meets a governor that
protects every decision. This is why the guarantee is carried by the governor, not the monitor.

## 5. The residual, named and bounded (the honest limit)

"Defended at every angle" is a claim about *channels*, not about impossibility. Three residuals travel
with the spec, because hiding them is the one thing that would make it false:

1. **The governor trusts its own evidence-justification model.** The floor gates on `e`; if the
   device's evidence channel is miscalibrated or itself gamed, the floor moves. The defence reduces to
   the quality of an *independent* justification signal — the device-level form of "watch the handle."
2. **The detectability floor is real and proven.** Attacks shorter/sparser than
   `ceil(log2(1/alpha))` blocks evade any detector of this form (`learner-tampering`). The guardian
   does not claim to detect them; it survives them because the governor is unconditional. Monitor-C is
   also estimator-limited (data-hungry, biased) — a corroborating flag, never a sole trigger.
3. **A device that exposes no evidence channel gets monitoring only.** No `e` means no governor; the
   spec marks this as uncovered and the remedy is to add an evidence channel, not to pretend the floor
   applies.

## 6. It applies to any BCI device (the registry)

`sentinel/guardian.py` maps real device classes onto the ladder and reports, per device, which
guardian components its exposed streams unlock. All four rungs are covered across the registry
(`coverage_summary() -> rungs_defended [0,1,2,3]`, 6 archetypes):

| Device class | Override channel | Rungs | Guardian components |
|---|---|---|---|
| Motor intracortical BCI (Neuralink / Blackrock) | emit a click/cursor/grip | 0 | J-monitor, C-monitor, floor |
| Endovascular motor BCI (Synchron) | emit an assistant action | 0, 1 | J-monitor, floor |
| Speech / communication neuroprosthesis | emit a token / autocomplete | 0, 1 | J-monitor, C-monitor, floor |
| Assistive selection UI / neuro-adaptive autocomplete | choose the option | 1 | J-monitor, floor |
| Closed-loop stimulation (adaptive DBS; evidence-timing rig) | time / modulate the commit | 2, 3 | J-monitor, C-monitor, floor, restoring floor |
| Consumer neuro-adaptive system (affect-timed content) | time + select content | 1, 2, 3 | all |

Adoption is: expose `u`, `e`, `b`; the guardian attaches the monitors and the floor its streams
support; the residual for that device is reported, not hidden. That is the whole integration surface —
no device-specific defence, and the same honesty ledger on every one.

## 6a. The motor-timing axis (grounded in real reaction-time data)

Beyond evidence-content justification, the actuation rung has a second, orthogonal justification axis:
**timing**. A pushed or automatic action betrays itself by an anomalous reaction time — faster than the
user's motor system can plausibly deliberate. Fit from real psychomotor data (lme4/sleepstudy, RT
rising 257→351 ms over 9 days of sleep deprivation), each user has a state-conditioned readiness band;
`run_motor.py` shows real actions fall below their band only **1.1%** of the time while an injected
automatic push (RT below the ~200 ms sensorimotor floor) is flagged **100%**. So any device exposing a
response-time stream gains an RT-plausibility gate on top of Monitor-J — a cheap, content-independent
check that is especially apt for motor BCIs, where the actuation is a timed movement. The residual is
the usual one: the band is the device's own model of plausible timing, and a sufficiently slow,
patient push stays inside it.

## 6b. On real data, without ground truth

The spec is exercised on real human choices (NARPS mixed gambles, 27,454 trials, 108 subjects;
`run_realworld.py`), where the ground-truth denominator disappears. The guardian behaves as the spec
requires: it fits the evidence-justification model from data (subject-grouped CV AUC **0.892**), and
**abstains** under a real population shift (cross-group calibration error **0.131** vs a 0.05 gate)
rather than emitting. Where an override is injected onto the real choices and labelled, the
justification floor recovers it far better than a count cap (**0.58 vs 0.12**). On clean real data no
override number is claimed — there is no counterfactual, so the monitor signal is behavioural
variation, not harm. This is the spec's abstention rule doing its job on real behaviour: the guardian
refuses to manufacture the denominator it lost.

## 7. Where this sits

- Instantiates [DEVICE.md](DEVICE.md) (SENTINEL) and [INTENT_OVERRIDE.md](INTENT_OVERRIDE.md) (the
  ladder) as one specification with runnable backing.
- Maps onto the real industry in [COMMERCIAL_FIT.md](COMMERCIAL_FIT.md) (the device archetypes are the
  same companies) and the research directions in [EXTENSIONS.md](EXTENSIONS.md).
- Keeps the discipline of [RED_TEAM.md](RED_TEAM.md): the residual is named, the detectability floor is
  a proven limit not a gap, and nothing here is validated on a person — the twins have ground truth,
  deployed devices do not, so the abstention gate travels with every number.

All numbers trace to `experiments/influence/sentinel-pilot/results/ladder_results.json`. Simulation
only; no human or neural data.
