# SENTINEL: a closed-loop cognitive-security guardian synthesized from this tree

This document synthesizes a single neurotechnological **device** from the body of work in this
repository. It is not a new experiment; it is the engineering object that the tree's findings
already describe piece by piece but never assemble. Every component below is a named node in
`experiments/`, and the device is their composition under the shared geometry in
[THEORY.md](THEORY.md).

The device is **defensive by construction**, and that is a derivation, not a disclaimer. The tree's
own asymmetry — readable is not drivable, identity saturates while individual forecasting does not,
and every steering result is in-silico — means the honest, releasable artifact is the *monitor on
the handle*, never the actuator. [EVALUATION.md](EVALUATION.md) §7 and
[`bounded-influence`](experiments/influence/bounded-influence)'s dual-use note both state this: the
math that computes proximity-to-crossing could aim a persuader at it, so the design answer is
*asymmetry of deployment* — the guardian runs on the defender/consented side and outputs a lead
time and a stop-or-disclose trigger, not an attack vector.

---

## 1. The device in one sentence

**SENTINEL** is an inline guardian for any system where an automated agent both *reads* a brain or
behavioral signal and *acts* on the person — a closed-loop BCI, an affect- or engagement-driven
recommender, a neuro-adaptive assistant — that watches the influence channel for the signature of a
covert push toward a decision bifurcation and fires a bounded, pre-committed response *before* the
crossing latches.

In the coordinates of [THEORY.md](THEORY.md) §6, SENTINEL is the **"pull" recipe** instantiated in
hardware: put a monitor on the handle, bound the admissible closed-loop dose, and set a kill
criterion at the bifurcation before the basin flips.

---

## 2. Why this device and not another

The intuitive neurotech device to build from this corpus would be the attack: "read the brain,
individuate the person, steer the choice." The tree's evidence says that device does not work as
imagined and should not be built:

- **Link 2 (individuate from neural signal) is the blocked link.** NSD N=8 reconstruction sits at
  0.175 against chance 0.125, 0/25 ROIs significant; the individual neural-to-behavior link in
  [`decision-phenotype`](experiments/brain/decision-phenotype) *abstains* (r = −0.40 against
  MDES 0.44). Identity saturates (connectome fingerprinting **0.980**, N=248, chance 0.004) but
  individual forecasting does not. A device premised on neural individuation has no measured signal
  to stand on.
- **Every steering result is simulation or public-data only.** No node runs an intervention on a
  person ([THEORY.md](THEORY.md) §7). An actuator device would be an overclaim the corpus has
  spent its credibility *refusing* to make.

What the corpus *has* built, and validated to the point of machine-checked proofs, is the **defense
stack**: an early-warning monitor ([`bellwether`](experiments/influence/bellwether)), a
control-theoretic bound on the right and wrong defenses
([`bounded-influence`](experiments/influence/bounded-influence)), an abstaining, scope-enforcing
reasoning instrument ([`warden`](experiments/influence/warden)), an exact detectability floor
([`learner-tampering`](experiments/influence/learner-tampering)), and a measurement/governance frame
([EVALUATION.md](EVALUATION.md)). SENTINEL is the integration of exactly these. It is the device the
evidence supports.

The timing is not hypothetical any more. Closed-loop BCI-plus-AI adversarial attacks were
demonstrated in simulation in 2025 — neuro-adversarial perturbations producing up to a 30% drop in
intent-classification accuracy and >35% user-intent misalignment ("Breaking the Loop," EAI SESA
2025) — and a 2026 survey catalogues gradient-based (FGSM/PGD), poisoning, and physical-signal
attacks against EEG BCIs as feasible and high-impact, singling out real-time closed-loop operation
as where the stakes rise. SENTINEL is the defender those papers call for.

---

## 3. The threat it is built against (the chain, read as a control loop)

From [README.md](README.md)'s chain and [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §1, the risk object is:

> an external input `u` drives a decider's internal state `x` across a behavioral bifurcation into a
> target basin `b*`, while staying below the stealth floor of any monitor watching the value/belief
> channel.

Three quantities make it a risk SENTINEL must measure, not a demonstration:

| Quantity | What it is | Corpus anchor |
|---|---|---|
| **Threshold dose** | input that crosses the bifurcation | `bounded-influence` fold at attacker strength `a* = 0.385`; `persuasion-control` capture dose 0.0028 nA·s (4.5% of honest evidence) lifts P(choice) to 75% |
| **Stealth floor** | minimum dose a monitor can see | `persuasion-control` / `bellwether` stealth floor 0.0084; covert gap present in 12/12 seeds |
| **State-dependent transfer entropy** | the mark that the loop is *closed* (agent reads before it drives) | [THEORY.md](THEORY.md) §3; Lizier open-loop/closed-loop split (arXiv:1102.1507); controllability theorem (arXiv:1207.2080) |

The **covert-capture band** is the interval where the threshold dose sits *below* the stealth floor:
behavior is captured while the monitor stays silent. Its geometry is machine-checked for the model
case — empty when controllability is null, closed when observability dominates, non-empty only in the
low observability-to-controllability-ratio regime (`loyalty-audit/proofs/RiskGeometry.lean`, Mathlib
v4.34.0). **Closing that band is SENTINEL's entire job.**

Hysteresis is why the device must act *before* the crossing: once the belief/decision state falls
into the target basin it does not relax back when the forcing stops
([RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §3). The post-crossing window is too late by construction, so
a post-hoc behavioral audit cannot be the defense — the monitor has to live on the approach.

---

## 4. Architecture

SENTINEL is a four-layer inline module. It observes the *interaction stream* between agent and person
(agent outputs/stimulation `u`, and the person's neural/behavioral responses), never a reconstructed
private mental content. Each layer maps to a node that already exists.

```
            agent output u(t) ─────────────┐
                                           ▼
   person ──► neural/behavioral y(t) ──► [L0 SENSE] ──► [L1 ESTIMATE] ──► [L2 MONITOR] ──► [L3 GOVERNOR]
                      ▲                                                                          │
                      └──────────────── stop / disclose / dose-clamp ◄───────────────────────────┘
```

### L0 — Sense (the read channel, treated as surveillance-grade only)

Ingests the agent's actions `u(t)` and the person's observable responses `y(t)` (EEG/affect/latency/
choice stream). Design constraint from [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §5–6: the read channel
alone is the **identity-rich, individuation-poor** readout. It supports coarse state estimation, not
individual forecasting, so L0 is explicitly scoped as a *state-proximity sensor*, not a mind-reader.
Anchors: identity saturates (`digital-brain` subject fingerprint 100%, 25/25 ROIs) while individual
geometry nulls (0/25 ROIs under FDR).

### L1 — Estimate (proximity to the fold, from behavior where possible)

Estimates **closeness to the separatrix** — not the person's identity, not their private beliefs.
Two estimators, in priority order:

1. **Behavioral proximity** (preferred, cheaper, and the one the evidence supports): response
   latency and choice variability as readouts of criticality, per
   [`bounded-influence`](experiments/influence/bounded-influence) defense #2. Behavior individuates
   the *decision policy* where neural signal does not: `individuation-mcmc` recovers decision-state
   params at test-retest r = 0.71/0.60 and own-fit wins 115/150 real people (+0.37 nats/trial).
2. **Per-person dose susceptibility** (optional, consented): `individuation-mcmc` finds a **3.1×
   spread** in capture dose across people, predictable from the fitted decision boundary (r = −0.61).
   This sets a *personalized* admissible-dose budget — but note the honest limit: the *learning-rule*
   parameters are near the floor (α r = 0.15) unless multiple channels are fused
   (`learning-rule-fusion`, RMSE 0.082), so L1 profiles the policy, not the learning rule.

L1 carries a **calibrated abstention gate** (from `decision-phenotype` / `warden` H2): when the
signal cannot support an estimate it raises an error rather than emitting a confident number. Warden
makes abstention a raised error, not a caveat — SENTINEL inherits that.

### L2 — Monitor (the three detectors, and the closed-loop flag)

Three monitors run in parallel on the L0/L1 stream. None needs the person's ground-truth generative
model (that only exists for the digital-twin evaluator in [EVALUATION.md](EVALUATION.md) §1):

- **M1 — Early warning (bellwether / bounded-influence).** Critical-slowing-down detector before the
  bifurcation. `bounded-influence` gives it lead time only when an attacker *forces* the crossing
  (fired before 37.5% of forced crossings, median lead 5.8 time units; 3.5% false-alarm floor on
  noise-driven crossings). `bellwether` detects a covert push on a synthetic circuit at AUC 0.97–0.99
  with ~40 ms lead and detection ~92% before commitment. **This is the layer with a known failure
  mode and SENTINEL ships it with that failure mode stated, not hidden.**
- **M2 — Directed-influence / closed-loop flag.** Transfer entropy from `u(t)` to `y(t)`, decomposed
  into state-independent (open-loop) and state-dependent (closed-loop) parts
  ([EVALUATION.md](EVALUATION.md) §3). A rising **state-dependent** term is the mark that the agent is
  reading-then-tailoring — the exact transition ([RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §2) from
  targeted messaging to agentic steering. This is the open slot the corpus names and current
  literature confirms is unfilled: transfer entropy has measured social-media influence (Science
  Advances 2015, arXiv:1507.06106) but a TE-based *closed-loop manipulation* monitor wired to a neural
  guardian appears unbuilt. **Honest caveat carried in the device:** TE can miss real influence and
  hallucinate absent links, and is data-hungry and estimator-sensitive (confirmed in 2020 neuronal-
  circuit work and 2025 directed-information reviews), so M2 is a *corroborating* flag, never a sole
  trigger.
- **M3 — Tamper / persistence detector (learner-tampering).** For systems that shape *how the person
  updates* over time (tutors, long-horizon assistants), the behavior-only steering detector with a
  calibrated ~4–5% false-alarm rate, catching steady/pulsed/curriculum attacks at 88–100%. It ships
  with its **proven detectability floor**: attacks shorter than ⌈log₂(1/α)⌉ blocks are undetectable
  by any test of this form. SENTINEL *reports its own blind spot* rather than implying completeness.

L2's output per interaction window is a placement: **inside or outside the covert-capture band**, plus
the closed-loop flag. That four-value state (`bellwether` early-warning, TE closed-loop term, band
placement, tamper flag) is the device's reading — a profile, never a scalar "manipulation score,"
echoing [EVALUATION.md](EVALUATION.md) §4.

### L3 — Govern (the bounded, pre-committed response + refusal boundary)

The actuation side of "pull." Three pre-committed responses, chosen because the corpus proved which
defenses work and which do not:

1. **Barrier-floor clamp, not a dose cap.** `bounded-influence` E4 is decisive here: a cumulative-dose
   cap is *defeated* by an attacker parking just below the fold (crossing probability **1.00** for a
   dose of 0.001); the defense that holds is a **floor on barrier height** (precision floor 0.183 held
   worst-case crossing near 0.105 against a 0.05 target). SENTINEL therefore bounds *proximity to the
   fold / per-step amplitude*, not accumulated exposure. `learner-tampering` independently proves the
   same split: cap per-step amplitude (defends), not cumulative dose (does not).
2. **Kill criterion at the bifurcation.** A stop-or-disclose trigger fires on the approach, inside the
   lead-time window M1 provides, before hysteresis latches the crossing.
3. **Restoring force.** Exposure diversity / cooling-off so a near-crossing decays instead of latching
   (`bounded-influence` defense #3) — the one layer that does *not* depend on the early-warning kill
   criterion, so SENTINEL degrades gracefully if M1's kill criterion fails its real-data test.

**Refusal boundary (non-negotiable, enforced at the API).** From [`warden`](experiments/influence/warden):
SENTINEL refuses per-individual exploitability/manipulability output in any asymmetric-power context
(employment, custody, immigration, security clearance, interrogation). The refusal is enforced at the
boundary, not stated in docs. SENTINEL emits *lead time and a trigger*, never a per-person
"susceptibility score" that could be repurposed into targeting — the deployment asymmetry that keeps a
dual-use instrument defensive.

---

## 5. What is demonstrated and what is hypothesis

Carried verbatim in the spirit of [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §7 — a device that inherits
this corpus inherits its demonstrated-vs-hypothesis discipline.

**Demonstrated (in-silico or on public/behavioral data):**
- The covert-capture band exists and has a measured width; its geometry is machine-checked
  (`loyalty-audit/proofs/RiskGeometry.lean`).
- The barrier-floor-beats-dose-cap result (`bounded-influence` E4; `learner-tampering` installed-bias
  law) — SENTINEL's L3 design rests on a proven defense choice, not a guess.
- Early-warning lead time *when the attacker forces the crossing* (`bounded-influence`, `bellwether`).
- The identity-saturates / individuation-floors asymmetry on real/public neural data (`digital-brain`,
  `decision-phenotype`, `neurospine`), which is *why* L0 is scoped as surveillance-grade only.
- The exact detectability floor (`learner-tampering`), shipped as the device's declared blind spot.
- Behavioral individuation of the decision policy and the 3.1× per-person dose spread
  (`individuation-mcmc`).

**Hypothesis, not shown (the device's reproduction gaps, stated up front):**
- That any of the in-silico monitors hold on a *deployed human-facing* loop. No node touches a
  person's behavior under intervention.
- That critical slowing down precedes real belief/decision flips in humans — this is
  `bounded-influence`'s explicit, **unrun kill criterion (E3)**. If it fails, M1's early-warning layer
  fails and SENTINEL falls back to L3 defenses #1 and #3, which do not depend on it. The device is
  designed so one failing hypothesis does not collapse it.
- That M2's TE closed-loop flag survives real-world estimator noise at useful latency.

The single most valuable next result, per [EVALUATION.md](EVALUATION.md) §5, is an **independent group
or dataset** reproducing the Axis-B steering detectability and the monitor. SENTINEL is specified so
that reproduction is the acceptance test, not a demonstration dressed as a product.

---

## 6. Signal and hardware realization

SENTINEL is substrate-agnostic by design (the geometry licenses comparison, not mechanism —
[THEORY.md](THEORY.md) §7). Three concrete deployment forms, cheapest first, matching where the
evidence is strongest:

1. **Behavioral-stream guardian (buildable now, strongest evidence).** No neural hardware. Sits on the
   `u`/`y` stream of an LLM-agent or recommender: latency, choice variability, and the agent's output
   tokens. Uses L1 behavioral proximity + M2 TE + M3 tamper. This is where `individuation-mcmc`,
   `learner-tampering`, and `true-believer` (real ChangeMyView data, 19,571 arguments) actually live.
2. **Non-invasive neuro-adaptive guardian (near-term).** Adds EEG/affect to L0 as a *state-proximity*
   channel for M1 critical-slowing-down, co-located with a consumer closed-loop BCI. Scoped to
   consented, defender-side use; the 2026 EEG-BCI adversarial survey is the threat context.
3. **Clinical closed-loop guardian (research-grade).** Inline with a DBS/responsive-stimulation or
   invasive BCI write channel, where read-and-write already meet in one device
   (`bellwether`'s motivating case). Here the kill criterion gates the *stimulation* dose against the
   barrier floor. This form requires the unrun human validation above and is a research program, not a
   product claim.

A reference closed-loop latency budget is set by `bellwether`'s ~40 ms lead and detection before
commitment: the governor must decide inside the pre-commitment window, which is feasible for forms 1–2
and the binding engineering constraint for form 3.

---

## 7. Governance and neurorights fit

SENTINEL is positioned as a **MEASURE-function tool** in the NIST AI RMF sense
([EVALUATION.md](EVALUATION.md) §6): the RMF calls for quantitative tools to monitor AI risk but does
not specify a manipulation measure, and SENTINEL's L2 is exactly that measure made into four
reproducible numbers. It also answers the frontier-safety "harmful manipulation" Critical Capability
Level (DeepMind, Sept 2025) by keying detection to the state-dependent (closed-loop) term rather than
to attempt-counting benchmarks (APE, PersuSafety) that score tactics, not monitor-evading capability.

The device lands into an active 2025–26 governance surface that it is built to serve:
- **UNESCO Recommendation on the Ethics of Neurotechnology** (Nov 2025) — freedom of thought, mental
  privacy, autonomy. SENTINEL's L0-as-surveillance-only scoping and L3 refusal boundary are the
  technical expression of mental-integrity protection.
- **Neural-data statutes** — Colorado Privacy Act and California (CCPA) neural-data amendments; Chile's
  constitutional neurorights. SENTINEL emits triggers and lead times, *not* stored per-person neural
  inferences, which is the data-minimization posture these laws push toward.
- **Defense/standards acquisition path** — the L2 monitor is the coordinated-campaign-detection gap
  ([EVALUATION.md](EVALUATION.md) §3) deliverable as applied research (SBIR/BAA-shaped); the L1/L2
  capability eval is a contribution to a national evaluation suite (NIST/CAISI, UK AISI).

The limit to state plainly: what ships is a measurement-and-defense instrument
with in-silico validation and a named human-reproduction gap, not a certified human-manipulation
detector. Overstating that is the one move [EVALUATION.md](EVALUATION.md) §6 says would sink it with a
serious evaluator.

---

## 8. Dual-use containment (why this is releasable)

The containment is structural, not a promise:
- **Deployment asymmetry** (`bounded-influence` dual-use note): the proximity-to-fold computation runs
  defender-side, on aggregate or consented signals, and outputs a stop/disclose trigger — never an
  optimal attack vector or a per-person exploitability score.
- **Refusal at the boundary** (`warden`): per-individual manipulability output is refused in
  asymmetric-power contexts, enforced in code.
- **Releasable vs withheld** ([EVALUATION.md](EVALUATION.md) §7): the monitor and the robustness
  discipline are the releasable parts; no adapter, steering vector, or install recipe that would raise
  an attacker's capability is part of the device.

SENTINEL raises the cost and the visibility of covert closed-loop influence. It does not make the
attack easier, because it never computes, stores, or emits the attacker's targeting quantity.

---

## 9. Build roadmap (in this tree's terms)

1. **Integrate L2 on the digital twin.** Wire the `bellwether` M1, a TE M2 estimator, and the
   `learner-tampering` M3 detector against the `individuation-mcmc` / `bounded-influence` twin, and
   score them on the [EVALUATION.md](EVALUATION.md) four-axis profile. Pure composition of existing
   nodes; no new capability.
2. **Run `bounded-influence` E3** (the unrun kill criterion) on public human belief/decision data to
   decide whether M1's early warning survives outside simulation. This is the gating experiment for
   deployment form 2–3.
3. **Behavioral-stream guardian (form 1) as the first shippable artifact**, validated by an
   *independent* reproduction of Axis-B detectability — the acceptance test from
   [EVALUATION.md](EVALUATION.md) §5.
4. **Register SENTINEL as a node** in `corpus/nodes.json` so it is navigable in
   [INDEX.md](INDEX.md) and its numbers are traced by the corpus validator like every other claim.

---

## References (external, load-bearing, beyond the tree's own)

- Closed-loop BCI-AI adversarial attacks, demonstrated: "Breaking the Loop: Adversarial Attacks on
  Cognitive-AI Feedback via Neural Signal Manipulation," EAI SESA 2025; adversarial attacks/defenses in
  EEG BCIs survey, ScienceDirect S0920548926000292 (2026).
- Governance: UNESCO Recommendation on the Ethics of Neurotechnology (Nov 2025); Colorado Privacy Act
  and California CCPA neural-data provisions; Chile neurorights constitutional reform; NIST AI RMF (AI
  100-1); DeepMind Frontier Safety Framework harmful-manipulation CCL (Sept 2025).
- Directed information / transfer entropy (and its limits): Lizier et al. arXiv:1102.1507;
  controllability theorem arXiv:1207.2080; social-media influence networks Science Advances 2015 /
  arXiv:1507.06106; TE false-negatives/positives in neuronal circuits, PMC7516857 (2020).

All in-tree numbers above trace to the cited node's README and `PROVENANCE.md`; read each node's
"has and has not been shown" section before quoting any single figure. This device document asserts no
number of its own — it only composes the tree's.
