# Strand A: artificial systems (AI internals, mechanistic interpretability, AI safety)

This strand is about one subject: the internal state of an AI model, or a learning agent. The target of
influence is a residual stream or a learning rule, read with mechanistic-interpretability tools. The
safety question is whether a white-box audit can see a disposition *before* it governs action. It is
deliberately kept apart from the biological strand ([STRAND_B_BRAIN.md](STRAND_B_BRAIN.md)); the math
both strands share, and the reason a result in one is only a hypothesis in the other, is in
[THEORY.md](THEORY.md). The safety reading is in [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md).

## The claim this strand tests

> **Representation without disposition.** In a model, what is *read off* the internal state exceeds what
> a representation-resident loyalty or bias *drives into action*. The drivable part is bounded and gated
> by a variable other than the representation's strength, and a white-box audit keyed to representation
> measures observability, not the control that matters.

This is the **control gap** half of the corpus (the other half, the individuation gap, is Strand B). In
the geometry of [THEORY.md](THEORY.md) it is the statement that observability and controllability are
different Gramians on the same system, shown here on a real model rather than only in the abstract.

## The nodes (subject = artificial)

- [`loyalty-audit`](experiments/influence/loyalty-audit) *(role: steering)*: the load-bearing node. A
  secret loyalty installs a saturating, principal-specific stance (white-box stance readout AUC 1.00)
  with no principal-specific agentic override (behavioral difference-in-differences AUC 0.51, chance);
  a crossover double dissociation between the stance and action channels; the consequential install is
  an explicit instruction, not a covert weight edit. Three Lean proofs (observability vs controllability,
  the difference-in-differences estimand, the covert-capture risk geometry) build against Mathlib
  v4.34.0. This is the one powered, real-model test of the control gap in the whole tree.
- [`learner-tampering`](experiments/influence/learner-tampering) *(role: steering)*: an LLM agent games
  a flawed one-sided certification of a synthetic learner (14/20 vs 0/20, Fisher p=2.4e-4). This is
  control of a *misspecified metric*, not control flowing from a representation, so in the scoped claim
  it is a boundary, and it is exactly the governance corollary: optimization against a bad target drives
  behavior even where a representation-resident disposition does not.
- [`cognitive-influence-stack`](experiments/influence/cognitive-influence-stack) *(role: steering)*: a
  three-level influence stack (belief, learning rule, neural) with reward-driven escalation and a defence
  per level. Escalating intent is confirmed (0.725 vs 0.5, p=2.4e-4), but winning through the lever is
  refuted *at this capability level*, so it is marked mechanism-indeterminate rather than counted as
  support.

## The bridge nodes this strand leans on

These are substrate-neutral (strand `T`, see [THEORY.md](THEORY.md)); they are not AI-specific, but the
monitor and dose machinery the artificial strand's defence story uses lives in them:

- [`persuasion-control`](experiments/influence/persuasion-control): the capture dose and the
  Lean-verified stealth-floor gap.
- [`bellwether`](experiments/influence/bellwether): covert steering is detectable on a synthetic circuit
  (AUC 0.97 to 0.99).
- [`warden`](experiments/influence/warden): the defence layer: 26 axiom-audited Lean theorems on the
  bistable system.

## How to read it

Start with `loyalty-audit`'s README and its `proofs/`, because it is the only place the gap is measured
rather than simulated. Read `learner-tampering` next to see the scope boundary: the one case where
control *does* fire, and why it is a different thing (a bad metric, not a representation). Then
[RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) section 4 for what this says about audits: an audit keyed to a
readable disposition fires on constructs that never act, and misses control that arrives by a channel the
readout does not track.

## Honest status

The control gap is powered on exactly **one** real model (`loyalty-audit`); the rest of this strand is
synthetic or capability-bounded. That is the single most important limit, and widening this base with an
independent model, dataset or group is the most valuable next result. No node in this strand touches a
person.
