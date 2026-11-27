# From influence geometry to BCI security: the argument, its meaning, and the way forward

This is the capstone. The tree began as a question — what can be read from a mind, and how far can one
be moved — and has narrowed, through simulation, formal analysis, real human data, and a real animal
manipulation, into a single defensible argument with a buildable consequence. This document states that
argument at full strength, says what it means, and lays out how it becomes a working discipline:
**BCI security, with intent integrity as the property it protects.**

Everything here rests on committed evidence. Read each claim's tag: **[shown]** in simulation or on real
data in this tree, **[real-manipulation]** validated against a real causal intervention (mouse),
**[hypothesis]** a transfer of coordinates not yet tested in the target system.

---

## 1. The argument, at full strength

Influence over a decision system is not a matter of persuasion or message content. It is a
**control-geometry** phenomenon with three invariants, and after this program each one has support
stronger than a simulation.

1. **Influence concentrates at the margin.** A push moves a choice most where the choice is balanced —
   at the bifurcation — and its effect collapses where evidence makes the choice determined. This is no
   longer only a property of a chosen potential: in the IBL mouse 2AFC, a **real** experimental
   manipulation (the biased-block prior) shifts choice at zero contrast by **0.575 [95% CI 0.36–0.77],
   permutation p ≈ 2e-4**, with a confound-controlled prior-pull coefficient of **0.96 [0.69–1.28]**
   **[real-manipulation]**, while at strong contrast the choice follows evidence; human choice lability
   peaks at the behavioural indifference region **[shown]**. (Honestly: the formal "pull shrinks with
   evidence" interaction is underpowered in a single session — undetermined, not refuted — so the
   margin claim rests on the significant zero-evidence push plus the dominant evidence term, pending more
   sessions.) The margin is where a decision system is pushable, in two species.

2. **What must be bounded is not what is cheaply measured** — the Gramian mismatch. Observability (what
   a representation or signal reveals) and controllability (what an input can drive the behaviour to)
   are distinct. A loyalty is readable at AUC 1.00 and drivable at AUC 0.51 **[shown]**; neural identity
   saturates while individual forecasting floors **[shown]**. An audit or screen keyed to the readable
   quantity certifies the wrong thing.

3. **The safety-relevant event is loop closure.** A fixed push is open-loop; an agent that reads the
   target and adapts is closed-loop, and closed-loop control reaches states open-loop cannot, at lower
   dose. The mark is a measurable state-dependent directed-information term, and on the twin the
   closed-loop flag separates an adaptive from a scripted pusher at matched amplitude (0.0 vs 1.05 bits)
   **[shown]**.

The defence that follows is forced by the same geometry and is **substrate- and species-general**:
gate the action on an independent justification signal **at the margin** (the governor); do not cap
counts or cumulative dose (proven the wrong quantity at every rung **[shown]**); monitor the
closed-loop signature; and because detection has a proven floor (short/sparse attacks evade any
detector **[shown]**), let the **governor, not the monitor, carry the guarantee** — demonstrated by a
sparse attack that evades the pooled monitor while the per-decision floor still cuts the targeted
override 0.67 → 0.16 **[shown]**.

That is the whole argument: **influence is a margin phenomenon, instruments mismeasure it, the loop
closing is the danger, and the defence is a justification floor at the margin that does not depend on
detection.** Each clause is now backed by evidence, one of them by a real manipulation across species.

---

## 2. What it means: override is a violation of intent integrity

The broad meaning is a reframing. The diffuse worry "AI might manipulate people through a brain
interface" becomes a crisp, enforceable **security property**.

Classical information security protects **data integrity** — a bit was not altered between sender and
receiver. A brain-computer interface sits on a more intimate channel: between a person's **volition**
and an **action taken in the world**. The property that channel must preserve is **intent integrity** —
*the action reflects the user's intent, not an injected or proxy-induced push.*

This reframing is powerful because it is enforceable, not aspirational:

- The **intent-override ladder** ([INTENT_OVERRIDE.md](INTENT_OVERRIDE.md)) enumerates the attack surface
  on intent integrity — actuation, selection, timing, decision — from the mechanical level where the
  violation is a discrete event to the cognitive level where it is inferred.
- The **guardian** ([GUARDIAN_SPEC.md](GUARDIAN_SPEC.md)) is the intent-integrity **monitor**; the
  **justification floor** is its enforcement mechanism; the **closed-loop flag** detects the adaptive
  adversary.
- The **margin result** tells a defender *where* intent integrity is most at risk and where to spend the
  monitor's budget: at the user's decision margin, not uniformly.

Intent integrity is to BCI what data integrity is to networking: the thing the system is engineered to
guarantee, with a named monitor, a named enforcement mechanism, and a named residual trust assumption.
That is what turns "cognitive security" from a slogan into an engineering discipline.

---

## 3. The threat model for BCI, in these terms

An override is an intent-integrity violation. It arrives two ways, and the geometry treats them the same.

- **Accidental (misalignment).** A decoder or agent over-optimizes a proxy — throughput, decode
  confidence, engagement, a reward the user did not endorse — and lowers its bar, manufacturing intent
  it cannot see. Shown to drive the override rate from 0.02 to 0.83, and to 1.00 under a per-action
  honeypot reward **[shown]**. This is the *common* case and needs no adversary.
- **Adversarial (injection).** A party with access to the signal path (a compromised decoder, a poisoned
  model, a crafted stimulus stream) drives the action directly. The closed-loop, margin-seeking version
  is the serious case, and 2025 work already demonstrates adversarial perturbations degrading
  closed-loop BCI intent by >35% **[external]**.

Both land hardest at the decision margin **[real-manipulation]**, both are caught by the same
justification floor **[shown]**, and both are made worse by loop closure **[shown]**. A BCI security
program therefore does not need a separate defence per device or per attacker — it needs the three-stream
guardian wherever the read channel can feed an action.

The **integrity question** for any BCI safety case is sharp: *does the read channel feed an adaptive
controller, and at the user's margin, is the drivable dose below the monitor's floor?* If yes to the
first and the band is non-empty, intent integrity is not guaranteed, and the guardian is the remedy.

---

## 4. The guardian as a BCI security co-processor

The device-agnostic contract makes the guardian an integrity co-processor that bolts onto an existing
stack rather than a bespoke redesign. A device exposes three streams — **actuation** `u`, **evidence**
`e`, **outcome** `b` — and inherits:

- **Monitor-J** (justification): the rate of actuation the evidence does not support — the
  integrity-violation signal, computable without ground truth.
- **Monitor-C** (closed-loop): the read-before-drive directed-information term.
- **The RT-plausibility gate** (motor BCIs): an action faster than the user's state-conditioned
  readiness band is suspect; real actions fall below the band 1.1% of the time, an injected automatic
  push 100% **[shown]**.
- **The governor**: gate the action on `e` at the margin; the enforcement mechanism that holds even when
  the monitor is blind.

It fits the real stack ([COMMERCIAL_FIT.md](COMMERCIAL_FIT.md)): a decoder-side library on an
intracortical motor BCI (rung 0), a safety co-processor on adaptive DBS (rungs 2–3), a trust-and-safety
layer on consumer neuro-adaptive systems (rungs 1–3). Its binding engineering constraint is latency: the
integrity decision must land inside the pre-commitment window (~40 ms order on the twin **[shown]**),
which is feasible for a co-processor on the device's own feature stream.

**The stated trust boundary.** The guarantee reduces to the quality of an *independent*
evidence-justification model: if the device's own evidence channel is miscalibrated or itself gamed, the
floor moves. This is not hidden — it is the single security assumption the whole architecture rests on,
and hardening it (better evidence models, per-user calibration, conformal coverage, an evidence channel
the actuating agent cannot influence) is the core engineering task, not an afterthought.

---

## 5. The cross-species red-team: animals as the ethically-runnable attack testbed

Here is the methodological keystone this program adds to BCI security, and it follows directly from the
cross-species result. **You cannot run a manipulation attack on a human to test a defence. You can run
one in an animal.** The IBL mouse task *is* a real, controlled push on a decision, with timing and ground
truth. That makes animal decision models the **penetration-testing ground for neural manipulation**:

1. **Red-team in the animal**, where the attack is real, ethical, and ground-truthed: run proxy-over-
   optimizing and closed-loop margin-seeking pushes, measure the true override, and calibrate the
   guardian's monitors and floor against a known manipulation. The mouse already shows the push lands at
   the margin **[real-manipulation]** — exactly where the guardian is told to watch.
2. **Transfer the calibrated detector** across the shared evidence→action geometry (mouse and human
   normalized slopes 1.09 vs 1.08 **[shown]**) to the human device, carrying its abstention gate intact.
3. **Deploy on the human in monitor-and-govern mode only**, never running the attack — the guardian
   protects an integrity property calibrated where the attack could be measured.

This closes the gap that has made neural-manipulation defence untestable: it gives a place where the
denominator exists. It is a transfer of coordinates **[hypothesis]** until an independent group
reproduces the detector's transfer, and the program says so — but it is a concrete, fundable pipeline,
not a thought experiment.

---

## 6. The forward program

A staged roadmap, each stage with a validation gate, from what is built to what a standard body could
adopt.

1. **Harden the justification model (now).** The guardian's one trust assumption. Build per-user,
   conformally-calibrated evidence models with an abstention gate; on NARPS the pooled model only
   marginally calibrated **[shown]**, so this is the first real task. *Gate:* out-of-sample calibration
   below a published threshold, else abstain.
2. **Animal red-team testbed (next).** Instantiate the guardian on IBL-style mouse data with injected
   proxy and closed-loop attacks; measure true override recovery and the monitor's ROC against a real
   manipulation. *Gate:* the floor recovers a known manipulation at a stated rate; the monitor's
   false-alarm floor is characterized.
3. **Device reference integration.** A decoder-side library exposing the three-stream contract on a
   motor-BCI feature stream, with the RT-plausibility gate; characterize the influence surface as a
   pre-market safety artifact. *Gate:* latency within the pre-commitment window on real hardware.
4. **Conformance spec and test battery.** "Intent-integrity conformance" for a closed-loop neuro-device:
   the four-number capability profile ([EVALUATION.md](EVALUATION.md)) plus the override ladder battery,
   as a submissible characterization aligned to the NIST AI RMF MEASURE function and the FDA BCI
   leapfrog documentation gap **[external]**. *Gate:* an independent group reproduces the battery.
5. **Standards and governance.** Intent integrity as a named property in BCI safety guidance and neural-
   data regulation (the 2025 UNESCO recommendation and neural-data statutes set the direction
   **[external]**); the guardian's monitor as a defensive-research deliverable for the coordinated-
   manipulation-detection gap.

The asymmetry is deliberate and carried from the rest of the tree: the monitor, the governor, the
conformance battery, and the robustness discipline are the releasable parts; nothing that raises an
attacker's capability is. The defence is what ships.

---

## 7. Scope, honestly

What is established: the margin invariant across two species with a real manipulation; the Gramian
mismatch on a real model and real neural data; the defence shape across four override rungs; the
guardian's device-agnostic coverage and defence-in-depth; real-data operation with correct abstention
across five datasets. What is not: no intervention on a human; the cross-species transfer and the
human-device deployment are hypotheses with named gates; the justification model is the standing trust
assumption. The single most valuable next result is an independent reproduction of the animal red-team
calibration and its transfer — and the program is built so that result would strengthen or break it
cleanly.

**The one line.** A brain-computer interface is a channel between intent and action; the property worth
engineering is that the action is the user's own; influence breaks it at the decision margin; and the
defence — a justification floor at the margin, calibrated where the attack can be run and carried to
where it cannot — is buildable now. That is BCI security, and it is the discipline this tree has been
converging on all along.

---

*Reads with: [INTENT_OVERRIDE.md](INTENT_OVERRIDE.md) (the attack surface), [GUARDIAN_SPEC.md](GUARDIAN_SPEC.md)
(the monitor), [DEVICE.md](DEVICE.md) (SENTINEL), [COMMERCIAL_FIT.md](COMMERCIAL_FIT.md) (the device
landscape), [EXTENSIONS.md](EXTENSIONS.md) (directions), [RED_TEAM.md](RED_TEAM.md) (the discipline), and
[`experiments/influence/sentinel-pilot`](experiments/influence/sentinel-pilot) (the runnable evidence,
five datasets, two species).*
