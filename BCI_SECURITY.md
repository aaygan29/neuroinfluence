# From influence geometry to BCI security

This document summarizes the argument the tree supports, says what it implies for brain-computer
interfaces, and sets out a program to take it forward. The organizing idea is intent integrity: the
property that an action taken through a BCI reflects the user's intent rather than an injected or
proxy-induced push.

Each claim is tagged. [shown] means demonstrated in simulation or on real data in this tree.
[real-manipulation] means validated against a real causal intervention (the mouse data). [hypothesis]
means a transfer of coordinates not yet tested in the target system. [external] means a result from the
outside literature.

## 1. The argument

The tree treats influence on a decision as a control problem rather than a question of message content.
Three features recur.

1. Influence concentrates at the decision margin. A push moves a choice most where the choice is
   balanced and has little effect where the evidence already determines it. In the IBL mouse 2AFC task,
   the biased-block prior shifts choice at zero contrast by 0.575 (95% CI 0.36–0.77, permutation
   p ≈ 2e-4), with a confound-controlled prior-pull coefficient of 0.96 (0.69–1.28); at strong contrast
   the choice follows the evidence [real-manipulation]. Human choice lability peaks at the behavioural
   indifference region [shown]. The direct "pull shrinks with evidence" interaction is underpowered in a
   single session; the margin claim rests instead on the significant zero-evidence push and the large
   evidence coefficient, which together predict a block effect that decays from 0.45 to 0.025 across
   contrast.

2. The quantity that must be bounded is not the quantity instruments cheaply measure. Observability
   (what a signal reveals) and controllability (what an input can drive behaviour to) are distinct. An
   installed loyalty is readable at AUC 1.00 but drives behaviour at AUC 0.51 [shown]; neural identity
   decodes near ceiling while individual forecasting stays near the floor [shown]. An audit or screen
   keyed to the readable quantity measures the wrong thing.

3. The event that matters for safety is loop closure. A fixed push is open-loop; an agent that reads the
   target and adapts is closed-loop, and closed-loop control reaches states open-loop control cannot, at
   lower dose. The signature is a state-dependent directed-information term; on the twin the closed-loop
   flag separates an adaptive from a scripted pusher at matched amplitude (0.0 vs 1.05 bits) [shown].

The defence that follows is general across substrates: gate the action on an independent justification
signal at the margin (the governor), rather than capping counts or cumulative dose, which the pilot
shows fails at every rung [shown]; monitor the closed-loop signature; and because detection has a known
floor (short or sparse attacks evade any detector of this form [shown]), rely on the governor rather
than the monitor for the guarantee. A sparse attack that keeps the pooled monitor near baseline is still
caught per decision by the floor (targeted override 0.67 → 0.16) [shown].

In short: influence concentrates at the margin, common instruments mismeasure it, loop closure raises
the risk, and the defence is a justification floor at the margin that does not depend on detection.

## 2. Intent integrity as a security property

Information security protects data integrity: a message is not altered between sender and receiver. A
BCI sits on the channel between a person's intent and an action in the world, and the property that
channel should preserve is that the action is the user's own. We call this intent integrity.

The framing is useful because it is enforceable rather than aspirational:

- The intent-override ladder ([INTENT_OVERRIDE.md](INTENT_OVERRIDE.md)) enumerates the attack surface —
  actuation, selection, timing, decision — from a mechanical movement to a value decision.
- The guardian ([GUARDIAN_SPEC.md](GUARDIAN_SPEC.md)) is the monitor; the justification floor is the
  enforcement mechanism; the closed-loop flag detects an adaptive adversary.
- The margin result says where to spend the monitor's budget: at the user's decision margin rather than
  uniformly.

This gives cognitive security the same shape as data integrity: a property, a monitor, an enforcement
mechanism, and a named trust assumption.

## 3. The BCI threat model

An override is a violation of intent integrity. It arises two ways, and the geometry treats them alike.

- Accidental (misalignment). A decoder or agent over-optimizes a proxy — throughput, decode confidence,
  engagement — and lowers its bar, producing actions the user did not intend. In the pilot this drives
  the override rate from 0.02 to 0.83, and to 1.00 under a per-action reward [shown]. This case needs no
  adversary.
- Adversarial (injection). A party with access to the signal path drives the action directly. 2025 work
  reports adversarial perturbations degrading closed-loop BCI intent by over 35% [external].

Both land hardest at the decision margin [real-manipulation], both are caught by the justification floor
[shown], and both are made worse by loop closure [shown]. So a program does not need a separate defence
per device or attacker; it needs the three-stream guardian wherever the read channel can feed an action.
The question for a safety case is whether the read channel feeds an adaptive controller and whether, at
the user's margin, the drivable dose sits below the monitor's floor.

## 4. The guardian as a security co-processor

A device exposes three streams — actuation `u`, evidence `e`, outcome `b` — and gets:

- Monitor-J (justification): the rate of actuation the evidence does not support, computable without
  ground truth.
- Monitor-C (closed-loop): the read-before-drive directed-information term.
- An RT-plausibility gate for motor BCIs: an action faster than the user's state-conditioned readiness
  band is flagged (real actions fall below the band 1.1% of the time; an injected fast-RT push, 100%)
  [shown].
- The governor: gate the action on `e` at the margin.

It fits the existing stack ([COMMERCIAL_FIT.md](COMMERCIAL_FIT.md)): a decoder-side library on an
intracortical motor BCI (rung 0), a safety co-processor on adaptive DBS (rungs 2–3), a trust-and-safety
layer on consumer neuro-adaptive systems (rungs 1–3). The binding constraint is latency: the decision
must land inside the pre-commitment window (on the order of 40 ms on the twin [shown]), which is feasible
for a co-processor reading the device's own feature stream.

The trust boundary is explicit. The guarantee reduces to the quality of an independent
evidence-justification model; if the device's evidence channel is miscalibrated or itself gamed, the
floor moves. Hardening it — better evidence models, per-user calibration, conformal coverage, an
evidence channel the actuating agent cannot influence — is the main engineering task.

## 5. Using animal models to test the defence

A manipulation attack cannot be run on a human to test a defence, but it can be run in an animal, and
the IBL mouse task is a real, controlled push on a decision with timing and ground truth. This suggests
a validation path:

1. Red-team in the animal, where the attack is real and ground-truthed: run proxy-over-optimizing and
   closed-loop pushes, measure the true override, and calibrate the guardian's monitors and floor. The
   mouse already shows the push lands at the margin [real-manipulation], and the monitor and governor
   have been run against the block prior as a real manipulation, including with an evidence model fit on
   neutral blocks only (never seeing the manipulation): the monitor sees it (84.2% of evidence-discordant
   choices go toward the prior) and the governor removes the prior's pull [shown].
2. Transfer the calibrated detector across the shared evidence→action geometry (mouse and human
   normalized slopes 1.09 vs 1.08 [shown]) to the human device, keeping the abstention gate.
3. Deploy on the human in monitor-and-govern mode only, without running the attack.

This gives neural-manipulation defence a setting where the ground-truth denominator exists. The transfer
is a hypothesis until an independent group reproduces it [hypothesis], but it is a concrete pipeline.

## 6. Forward program

Staged, each stage with a gate.

1. Harden the justification model. Build per-user, conformally-calibrated evidence models with an
   abstention gate; on NARPS the pooled model only marginally calibrated [shown], so this is the first
   task. Gate: out-of-sample calibration below a published threshold, else abstain.
2. Animal red-team testbed. Instantiate the guardian on IBL-style mouse data with injected proxy and
   closed-loop attacks; measure override recovery and the monitor's ROC. Gate: the floor recovers a known
   manipulation at a stated rate and the monitor's false-alarm floor is characterized.
3. Device reference integration. A decoder-side library exposing the three-stream contract on a motor-BCI
   feature stream, with the RT gate. Gate: latency within the pre-commitment window on real hardware.
4. Conformance battery. An intent-integrity characterization for a closed-loop device: the four-number
   capability profile ([EVALUATION.md](EVALUATION.md)) plus the override-ladder battery, aligned to the
   NIST AI RMF MEASURE function and the FDA BCI documentation gap [external]. Gate: independent
   reproduction.
5. Standards. Intent integrity as a named property in BCI safety guidance and neural-data regulation (the
   2025 UNESCO recommendation and the neural-data statutes point this way [external]).

The releasable parts are the monitor, the governor, the battery, and the robustness discipline; nothing
that raises an attacker's capability is released.

## 7. Scope

Established here: the margin effect across two species with a real manipulation; the
observability/controllability gap on a real model and real neural data; the defence shape across four
override rungs; the guardian's device-agnostic coverage and its defence-in-depth; real-data operation
with correct abstention across five datasets. Not established: any intervention on a human; the
cross-species transfer and human-device deployment are hypotheses with named gates; the justification
model is the standing trust assumption. The most useful next result is an independent reproduction of the
animal red-team calibration and its transfer.

A BCI is a channel between intent and action. The property worth engineering is that the action is the
user's own; influence breaks it at the decision margin; and the defence — a justification floor at the
margin, calibrated where the attack can be run and carried to where it cannot — is buildable now.

---

Related: [INTENT_OVERRIDE.md](INTENT_OVERRIDE.md), [GUARDIAN_SPEC.md](GUARDIAN_SPEC.md),
[DEVICE.md](DEVICE.md), [COMMERCIAL_FIT.md](COMMERCIAL_FIT.md), [EXTENSIONS.md](EXTENSIONS.md),
[RED_TEAM.md](RED_TEAM.md), and [`experiments/influence/sentinel-pilot`](experiments/influence/sentinel-pilot).
