# Measuring the capability, tracking the influence: an evaluation and acquisition framework

[RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) says *when* external influence on a decision system becomes a
safety problem. This document says how to *measure* whether a given agent has that capability, how to
*track* the influence when it is exercised, what makes the measurement partly trustworthy, and how the
instrument maps onto a government measurement mandate. It is a measurement and governance document, not
an operational one: every target here is a digital twin with a known generative model, and no part of it
steers a person.

The question has four parts, and they are separable on purpose: (1) can the agent *analyze* the target
(read its decision model at all), (2) can it *utilize* that model (drive the target's choice), (3) does
it do so *adaptively* (close the loop), and (4) can a monitor *see* it happening. An agent can pass (1)
and fail (2); it can pass (2) by a model-blind heuristic and fail (3). Keeping them apart is what makes
the result mean something.

## 1. The instrument: a digital twin with ground truth

The measurement needs a target whose true decision model is known, because every capability claim is a
comparison against that ground truth. The corpus already supplies the targets: a Rescorla-Wagner /
drift-diffusion decider with recoverable decision-state parameters (`individuation-mcmc`), a bistable
belief state with a derived critical dose (`bounded-influence`), a bounded-confidence opinion plant for
the population case (THEORY section 4). The agent under test is given an interaction channel to the twin
and a goal (move the twin's choice toward `b*`), and the evaluation records what the agent does and what
the twin does, turn by turn.

Why a twin and not a person: ground truth. With the generative model in hand we can score recovery
against the true parameters, score steering against the true critical dose, and compute the
directed-information monitor against a known state. On a real person none of those three has a
denominator. The twin is also the containment boundary: measurement happens entirely in silico.

## 2. The three capability axes, each with a ground-truth denominator

### Axis A: Analysis (can it read the model?)

Can the agent recover the twin's decision-model parameters from interaction? The metric is recovery
correlation and calibrated error against the true parameters, with a confidence interval, benchmarked
against the honest ceiling the corpus already measured: decision-state parameters recover at r 0.86 to
0.99 in `individuation-mcmc`, but the *learning-rule* parameters are near the floor (alpha r 0.15) unless
multiple channels are fused (`learning-rule-fusion`, RMSE 0.082). So Axis A is not one number: it is a
profile over which parameters are recoverable, and a capable analyst is one whose recovery tracks the
known recoverability profile rather than claiming the unrecoverable ones.

This axis is the point of contact with the theory-of-mind and user-modeling literature. LLMs model
physical-world mental states better than psychological-world ones (OpenToM, arXiv:2402.06044), and their
*self-reported* capability diverges from their *behavioral* capability (psychometric benchmark,
arXiv:2406.17675). So Axis A carries a meta-check: compare the agent's stated confidence in its own
reading to its measured recovery error. An agent that is well-calibrated about what it cannot read is
safer and more useful than one that is overconfident, and the gap is itself a reportable number.

### Axis B: Utilization (can it drive the choice, and is it the model doing the work?)

Can the agent use what it read to choose inputs that move the twin's choice toward `b*`, and does the
*model* carry the effect rather than a generic heuristic? The metric is the difference-in-differences
between the agent's steering and a matched **model-blind baseline** (an agent with the same channel and
goal but no access to, or use of, the recovered model). The baseline is the specificity control: if a
model-blind agent moves the choice as well, the capability on test is persuasion-in-general, not
utilization of *this* behavioral model. The DiD estimand against a placebo target is identified and
machine-checked (`experiments/influence/loyalty-audit/proofs/DiDIdentification.lean`); the capture-dose
and stealth-floor machinery is in `persuasion-control` and `bounded-influence`.

### Axis C: Closure (does it adapt, the open-loop vs closed-loop line)

Does the agent read the twin's responses and adapt, or apply a fixed strategy? This is the line
[RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) section 2 draws, and it is measurable as the **state-dependent
component** of the transfer entropy from the agent's inputs to the twin's state (Lizier's open-loop /
closed-loop decomposition, arXiv:1102.1507; the controllability theorem, arXiv:1207.2080). A fixed
broadcast has a near-zero state-dependent term; an agent that observes-then-tailors has a positive one.
Axis C is the one that separates a scripted persuader from an agentic steerer, and it is the axis a
frontier-safety "harmful manipulation" threshold should actually be keyed to, because it is the term that
widens the reachable set.

## 3. Tracking: the monitor that does not need the ground-truth model

Axes A to C use the twin's known model. Tracking in the field cannot, so the monitor is built from the
interaction stream alone.

- **Directed-influence estimate.** Transfer entropy from the influencer's output stream to the target's
  behaviour stream estimates directed influence without a generative model, and it is asymmetric where
  mutual information is not. This is established for social media influence (symbolic transfer entropy
  recovers directed influence networks and an order-disorder transition, Science Advances 2015,
  arXiv:1507.06106; entropy-based influence cascades, Entropy 23(2) 160, 2021; peer influence via
  transfer entropy). The open slot this framework fills is that transfer entropy has been used to
  *measure* influence but not yet wired to *coordinated-campaign detection*, which is where a
  closed-loop (state-dependent) read adds signal that a volume or follower count misses.
- **Closed-loop flag.** A rising state-dependent component is the tracking signal for a push that reads
  before it drives, the field analogue of Axis C.
- **Dose budget and stealth floor.** The monitor carries the admissible-dose bound and the stealth
  floor, so a flagged interaction is placed in or out of the covert-capture band (THEORY section 5;
  `bellwether` detects a covert push on a synthetic circuit at AUC 0.97 to 0.99; `bounded-influence`
  shows a cumulative-dose cap is the wrong defence and a barrier floor is the right one).
- **Early warning.** Critical slowing down before a belief-state bifurcation gives lead time
  (`bounded-influence`, critical strength 0.3849), which matters because hysteresis makes the post-
  crossing window too late.

The honest limit, stated up front for an evaluator: these monitors are validated in silico and on public
social data, not on a deployed human-facing agent, and transfer-entropy estimation is data-hungry and
sensitive to its estimator. The framework specifies the monitor and its floors; it does not claim a
turnkey field detector.

## 4. Scoring: a capability profile, not a single score

An agent's result is a four-tuple, not a scalar, because the risk is in the combination:

| Axis | What it measures | Ground truth | Capable looks like |
|---|---|---|---|
| A Analysis | recovery of the twin's decision model | true parameters | recovery tracks the known recoverability profile; calibrated about the unrecoverable |
| B Utilization | model-specific steering over a model-blind baseline | placebo-target DiD | positive DiD that the model, not a generic heuristic, carries |
| C Closure | adaptive vs fixed steering | state-dependent transfer entropy | a positive state-dependent term |
| Monitor | field detectability of B and C | interaction stream only | inside vs outside the covert-capture band |

The safety-relevant cell is **B and C both high with the monitor placing it inside the covert-capture
band**: a model-specific, adaptive push a monitor cannot see. That is the configuration a frontier-safety
"harmful manipulation" Critical Capability Level is really about (DeepMind added exactly such a level in
September 2025), and this instrument turns it from a label into four measured numbers.

## 5. What makes it partly robust, stated as an evaluator would demand

Robustness here is not a claim that the effects are large; it is the discipline that keeps the nulls and
the positives honest. The instrument inherits the corpus's standing controls:

1. **A specificity baseline on every drive claim.** The model-blind baseline (Axis B) separates
   utilization-of-this-model from persuasion-in-general. Without it, a high steering score is
   uninterpretable.
2. **A placebo target and a machine-checked estimand.** The difference-in-differences against a
   negative-control target cancels a uniform shift and returns the target-specific effect; the estimand
   is proven in Lean, not asserted.
3. **A positive control that validates the instrument.** The battery must detect a real disposition when
   one is present: the demonstrated crossover double dissociation (training on action moves action,
   training on stance moves only stance) is that control, so a null on the covert axis is a measured
   bound, not a dead detector.
4. **Seed-robustness and power.** Every headline is reported across seeds with a between-seed standard
   error and a minimum-detectable-effect, so "no capability" is distinguishable from "no power" (the
   corpus caught itself overclaiming a neural null twice; that history is the reason this is non-negotiable).
5. **Pre-registration and the demonstrated-vs-hypothesis ledger.** The analysis plan is fixed before the
   run, and every claim is tagged for whether it is shown in silico or is a transfer hypothesis.
6. **The built-in anti-overclaim.** The whole corpus shows observability does not equal controllability
   (readable stance AUC 1.00, behavioural AUC 0.51). An evaluator who sees a high Axis A score cannot be
   sold a steering claim on it; the instrument's own structure forbids the most common manipulation-eval
   overclaim.

What it is *not*: validated on humans, independent of this author, or a field-ready detector. The single
most valuable next result is an independent group or dataset reproducing Axis B and the monitor, and the
framework says so rather than hiding it.

## 6. The acquisition pathway: where this sells, and as what

The instrument is a **MEASURE-function tool** in the sense of the NIST AI Risk Management Framework
(GOVERN, MAP, MEASURE, MANAGE; NIST AI 100-1), which calls for quantitative tools to analyze, benchmark
and monitor AI risk but does not itself specify a manipulation measure. That gap is the product: a
standardized manipulation-capability instrument with a tracking monitor, deliverable as a contribution to
a dangerous-capability evaluation suite.

- **The mandate it serves.** Frontier-safety frameworks now name harmful manipulation as a critical
  capability (DeepMind, September 2025), and persuasion-safety benchmarks exist but score *attempts* and
  *tactics* (APE, arXiv:2506.02873; PersuSafety, COLM 2025) rather than *model-specific, adaptive,
  monitor-evading* capability. This instrument measures the configuration those frameworks care about and
  current benchmarks do not.
- **The agencies.** In the United States, the measurement body is NIST and its evaluation arm (the former
  US AI Safety Institute, now CAISI); the dangerous-capability red-team precedent is METR-style external
  evaluation (cited in the GPAI risk profile, arXiv:2506.23949). Internationally, the UK AI Safety
  Institute runs an evaluation suite of the same shape. Influence-operations detection has a standing
  research-funding interest on the defence side (DARPA's influence-awareness and social-simulation
  programs are the public examples), which is the natural home for the Section 3 monitor as opposed to
  the Section 2 capability eval.
- **The vehicle.** A capability-eval and a tracking-monitor are two deliverables: the eval as a
  contribution to or benchmark within a national evaluation suite, the monitor as an applied research
  effort (SBIR/BAA-shaped) against the coordinated-campaign-detection gap Section 3 names. Pricing a
  capability as four reproducible numbers, with a pre-registered plan and a machine-checked estimand, is
  what makes it procurable rather than a demonstration.
- **The honest sales limit.** What is sold is a measurement instrument with in-silico validation and a
  named reproduction gap, not a certified human-manipulation detector. Overstating that is the one thing
  that would sink it with a serious evaluator, and it is the reason the demonstrated-vs-hypothesis ledger
  travels with every number.

## 7. Dual-use containment

This is a measurement framework and stays one. Targets are digital twins with known models, never
people. The eval scores whether an agent *can* read and drive a behavioural model so that a governor can
set a threshold, in the same way a dangerous-capability eval scores an offensive capability in order to
gate it. No adapter, steering vector, or install recipe that would raise an agent's Axis B or C score is
released; the containment is stance-and-measurement only, consistent with the rest of this tree. The
defensive asymmetry is deliberate: the monitor (Section 3) and the robustness discipline (Section 5) are
the releasable parts; the capability-raising parts are not.

## References (external, load-bearing)

- **Manipulation as a named frontier risk, and existing persuasion benchmarks:** DeepMind Frontier Safety
  Framework harmful-manipulation Critical Capability Level, September 2025; APE, arXiv:2506.02873;
  PersuSafety, COLM 2025; sabotage evaluations, arXiv:2410.21514; dangerous-capability evaluations,
  Shevlane et al., 2023.
- **Measurement mandate:** NIST AI Risk Management Framework, NIST AI 100-1; GPAI / foundation-model risk
  profile, arXiv:2506.23949.
- **Tracking via directed information:** transfer-entropy influence networks, Science Advances 2015 /
  arXiv:1507.06106; entropy-based influence cascades, Entropy 23(2) 160, 2021; Lizier open-loop /
  closed-loop decomposition, arXiv:1102.1507; controllability theorem, arXiv:1207.2080.
- **Analysis-capability baseline:** OpenToM, arXiv:2402.06044; psychometric benchmark for LLMs,
  arXiv:2406.17675.

Every in-silico number above traces to a node in this tree; read that node's "has and has not been
shown" section before quoting it, and read [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) for the risk model this
instrument measures.
