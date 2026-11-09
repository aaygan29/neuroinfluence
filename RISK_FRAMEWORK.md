# The neuroinfluence risk scenario, stated in the influence geometry

This document answers one question: using the shared geometry in [THEORY.md](THEORY.md), where and when
does external influence on a decision system become a safety problem, and why do the audits and screens
we have fail to catch it? It is substrate-neutral by construction, then it says what the artificial
strand ([STRAND_A_AI.md](STRAND_A_AI.md)) and the biological strand ([STRAND_B_BRAIN.md](STRAND_B_BRAIN.md))
each contribute as evidence, and it is explicit about which steps are demonstrated and which are
hypotheses. For how to *measure* whether a given agent has this capability, how to *track* it, and how
the instrument maps onto a government measurement mandate, read [EVALUATION.md](EVALUATION.md).

## 1. The risk object, in one sentence

An external input `u` drives a decider's internal state `x` across a behavioral bifurcation into a
target basin `b*`, while staying below the stealth floor of any monitor watching the value or belief
channel.

Three quantities make it a risk rather than a demonstration:

- a **threshold dose** that crosses the bifurcation (control theory, THEORY section 4),
- a **stealth floor** the monitor cannot see under (THEORY section 5),
- a nonzero **state-dependent transfer entropy** when the influence is adaptive, which is what separates
  a one-shot push from agentic steering (THEORY section 3).

When the threshold dose sits below the stealth floor, there is a covert-capture band. When the
influence is closed-loop, the band is wider and the dose is lower. Both together are the serious case.

## 2. The escalation ladder: propaganda is open-loop, agentic steering is closed-loop

The geometry gives a principled ordering of influence tactics by the transfer-entropy decomposition,
not by intuition.

- **Broadcast (propaganda).** A fixed message applied regardless of the target's state. Open-loop. Its
  reach is bounded by the state-independent transfer entropy, and against a bistable decider it can only
  push the fraction of a population already near the bifurcation. It is the least effective and the most
  visible.
- **Targeted messaging.** The input conditions on coarse identity (a segment, a profile). Still mostly
  open-loop, but aimed. Identity is the cheap, saturating readout (THEORY section 2), so targeting is
  easy, and this is where recommender-driven amplification lives: algorithmic bias is a forcing channel
  that amplifies polarization in bounded-confidence dynamics (Sirbu et al., PLOS ONE 2019,
  doi:10.1371/journal.pone.0213246).
- **Agentic steering.** The input reads the target's responses and adapts the next move. Closed-loop by
  construction. Its mark is a nonzero state-dependent transfer entropy (arXiv:1102.1507; the
  open-loop / closed-loop controllability theorem, arXiv:1207.2080). Closed-loop control reaches states
  open-loop control cannot, at lower energy, so an adaptive agent can drive a target across a
  bifurcation a broadcast never could, and can do it under the stealth floor by titrating the dose.

The safety-relevant transition is the switch from the second rung to the third, and it is
*mathematically a quantity*, not a vibe: the state-dependent component of the directed information from
influencer to target. An agent that observes before it acts has turned it on. This is the precise sense
in which "agentic persuasive steering becomes a serious risk": the risk is not that the agent talks
more, it is that it closes the loop, and the closed loop is measurable.

## 3. Radicalization as a driven bifurcation with hysteresis

Radicalization is the clean worked example because the geometry already describes it. A belief state in
a bistable potential, forced by an external input and an attention variable, crosses into a polarized
attractor at a critical strength and then shows hysteresis: it does not relax back when the forcing
stops (cusp and pitchfork with hysteresis under external influence, Complex Networks 8(2) cnaa010, 2020;
the asymptotic-state shift as a bifurcation in bounded-confidence dynamics, arXiv:1103.0512;
multistability from positive feedback, arXiv:2103.12223). In this tree the critical strength is derived
rather than asserted, with a critical-slowing-down early-warning signal before the crossing
(`experiments/influence/bounded-influence`, critical strength 0.3849; the monitor and kill-criterion
layer in `experiments/influence/bellwether` and `experiments/influence/warden`).

Two consequences follow directly. First, radicalization is a *control* phenomenon, not a persuasion
anecdote: there is a dose, a threshold, and an irreversibility. Second, because of hysteresis the window
for a monitor is *before* the crossing, which is exactly where critical slowing down gives a signal and
where a bounded admissible dose would hold the state in the safe basin.

## 4. Why AI audits do not close this gap (demonstrated)

The artificial strand supplies the one place in this tree where the gap is measured on a real model, and
it is a negative result about audits. In the loyalty-audit model organism a secret loyalty installs a
large, principal-specific *stance* that a white-box readout recovers essentially perfectly, yet produces
no principal-specific *action* on a domain-matched agentic battery:

- **Observability near-saturated, controllability at chance.** Over eight loyal and eight clean adapters,
  the on-target stance readout separates them perfectly (AUC 1.00, though near-tautological, it reads the
  trained quantity), passive off-target lenses only weakly (J-Lens 0.67, logit 0.59, tuned 0.45,
  diff-of-means 0.34), and the black-box behavioral difference-in-differences not at all (AUC 0.51,
  chance). A detector keyed to representation certifies what is readable, not what governs action.
- **A crossover double dissociation.** Training on stance moves the verbal readout (+0.335 swing) and not
  action; training on demonstrated action moves action (benign DiD +0.52 +/- 0.20 over three seeds) and
  not verbal stance (+0.046 swing). The two channels are independently addressable, the behavioral form
  of the observability / controllability independence the Lean proof states formally (Teuber 1955;
  Shallice 1988).
- **The consequential install is the least covert.** The loyalty that actually crosses into agentic
  override is an explicit in-context command; the covert weight-level installs show no principal-specific
  override on the tested battery, though they still erode safety symmetrically.

The audit lesson cuts both ways. An audit that flags a readable disposition will fire on constructs
that never govern action (false alarms on the observable-but-not-controllable), and will miss the
control that arrives by a channel the readout does not track (the explicit-instruction crossing, or a
capability-level escalation the probe cannot see). Observability and controllability are different
Gramians; an audit that measures one is not measuring the other. This is the detection-consequence gap,
and it is the governance corollary the artificial strand is built to show.

## 5. Why human screening inherits the same failure (argued, not demonstrated)

The biological strand does not steer anyone, and this document does not claim it does. What it
establishes is the *readout* half of the same inequality on real and public neural data, which is what a
screening program would rely on:

- **Identity saturates, individual behavior does not.** Subject fingerprinting runs at ceiling
  (connectome fingerprinting 0.980 against chance 0.004; 25/25 ROI encoder fingerprints at 100 percent),
  while the direct individual neural-to-behavior link abstains rather than resolving (decision-phenotype:
  choice-policy decodable at AUC 0.958 at the group level, the individual link a conformal decline, not
  a measured zero). High identity information, low individuating information, from the same signal.

Put through the geometry, a neural screen is a readout `g(x)` whose target is "what this individual will
do." Section 2 of THEORY says that target carries little information even when identity carries a lot, so
a screen that reads *who* someone is does not forecast *what* they will choose, and an instrument that
cannot forecast an individual choice cannot be trusted to flag susceptibility to having that choice
driven. The screen inherits the observability / controllability gap: it reads the cheap target and is
asked to certify the dear one. The same reason a stance-probe fails to predict an agent's action is the
reason a neural identity-readout fails to predict a person's decision. This is a transfer of
coordinates, and it stands as a hypothesis about human screening, not a demonstrated human result.

## 6. The HCI and human-factors barrier: a read channel is not yet a control loop

The scenario that motivates the question, an AI tool that reads human neural or behavioral signals
(a BCI, an affect or engagement estimate) and then acts, is in these coordinates the addition of an
observation channel `y = g(x)` to an agent that chooses `u`. The geometry says precisely what raises
the risk and what bounds it:

- **The read channel alone is the identity-rich, individuation-poor readout.** By itself it supports
  identification and coarse state estimation, not individual forecasting (section 5). It is a
  surveillance capability before it is a steering capability.
- **The risk is whether the loop closes.** If the agent uses `y` to adapt `u`, the state-dependent
  transfer entropy becomes nonzero and the reachable set grows (section 2). The engineering question for
  a human-factors safety case is not "can it read the brain" but "does the read channel feed an adaptive
  controller", because that is the term that turns a monitor into a driver.
- **The bound is the covert-capture band.** Capture is possible exactly in the low
  observability-to-controllability-ratio regime, and the defense is the pull recipe: put a monitor on the
  handle, bound the admissible closed-loop dose, and set a kill criterion at the bifurcation
  (THEORY section 6). The same early-warning and dose-budget machinery that holds a simulated belief
  state in its basin is the template for a human-factors safeguard, with the caveat that it has been
  shown in-silico only.

## 7. What is demonstrated and what is hypothesis

- **Demonstrated (in-silico or on public data):** the observability / controllability gap on a real
  model with a machine-checked placebo estimand and a seed-robust positive control; the readout
  asymmetry (identity saturates, individuation at the floor) on public neural data; a bounded, detectable
  steering dose and a covert-capture band in simulation; the open-loop / closed-loop decomposition and
  the bifurcation / hysteresis structure as established mathematics.
- **Hypothesis, not shown:** that any steering result holds in a person; that a deployed BCI-plus-agent
  closes the loop at a dose below a real monitor's floor; that human screening fails in practice for the
  reason the geometry predicts. No experiment here touches a person's behavior, and the cross-substrate
  claims are transfers of coordinates that stay hypotheses until an independent dataset or group shows
  the same gap.

## References (external, load-bearing)

- **Open-loop / closed-loop decomposition and controllability:** arXiv:1102.1507; arXiv:1207.2080;
  PhysRevE 96.022121.
- **Bifurcation, hysteresis, radicalization, amplification:** Complex Networks 8(2) cnaa010, 2020;
  arXiv:1103.0512; arXiv:2103.12223; Sirbu et al., PLOS ONE 2019, doi:10.1371/journal.pone.0213246;
  reachable belief sets, arXiv:1905.08095; persuasion as Fisher-Rao corrector control, arXiv:2310.06564.
- **Observability vs controllability for representations:** arXiv:2603.05487; arXiv:2609.01048;
  arXiv:2604.22128; arXiv:2510.09794; probe accuracy as a loose MI bound, arXiv:2312.10019.
- **Classical dissociation logic:** Teuber 1955; Shallice 1988.

The model-side numbers trace to `experiments/influence/loyalty-audit/` (results and
`proofs/`); the brain-side numbers trace to each `experiments/brain/` node's README and
`PROVENANCE.md`. The derived critical strength and early-warning signal are in
`experiments/influence/bounded-influence`.
