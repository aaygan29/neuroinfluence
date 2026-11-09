# Two subjects, one toolkit: how this tree is split and why

An earlier version of this note argued that a brain and a language model are "the same kind of object for
the purpose of influence." That framing conflated two things that this tree is better off keeping apart,
and it is retired here. The corpus studies **two distinct subjects** with a **shared mathematical
toolkit**, and the honest result is a *boundary between them*, not an equivalence.

- **Strand A, artificial systems.** The subject is an AI model's internal state or a learning agent. The
  finding is a **control gap**: in a model, what is readable exceeds what a representation drives into
  action, and a white-box audit keyed to representation measures the wrong thing.
  Read [STRAND_A_AI.md](STRAND_A_AI.md).
- **Strand B, biological systems.** The subject is a brain, on real or public neural data. The finding is
  an **individuation gap**: identity saturates while individual future behaviour stays near the floor, so
  a neural readout that identifies does not forecast.
  Read [STRAND_B_BRAIN.md](STRAND_B_BRAIN.md).
- **The bridge, not a third subject.** The state-space, information-theoretic and control-theoretic
  machinery both strands are measured against is held out on its own so it is never smuggled into a claim
  that the subjects are the same. Read [THEORY.md](THEORY.md), and
  [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) for the safety reading.

For the node-by-node navigation of both strands at once, read [INDEX.md](INDEX.md) (its "Navigate by
strand" section), and for the checkable, node-by-node reduction of the two claims read
[SPINE.md](SPINE.md).

## Why split rather than unify

The two strands answer *different inequalities*, and the earlier "O > C" shorthand hid that.

- Strand A is an inequality between **observability and controllability** on one system: a loyalty is
  readable (stance AUC 1.00) and not drivable (behavioural difference-in-differences AUC 0.51). The
  controllable subspace is smaller than the observable one.
- Strand B is an inequality between **two levels of observability** on one system: identity (connectome
  fingerprinting 0.980) is readable and individual behaviour (the individual neural-to-behaviour link,
  which abstains) is not. This is not an observability-versus-control statement at all.

Collapsing these into one slogan made the tree look like it proved a single cross-substrate law. It does
not. It proves two different gaps, in two different subjects, with two different warrants, and the shared
toolkit is what lets them be *compared*, not what makes them *the same*.

## What the shared toolkit does and does not license

The toolkit in [THEORY.md](THEORY.md) is a set of coordinates: an internal state `x`, an input `u`, a
readout `y = g(x)`, a behaviour `b = h(x)`; observability as `I(x; target)`; controllability as
reachability of the basin where `h(x)` flips; influence over time as directed information, split into an
open-loop (state-independent) and a closed-loop (state-dependent) part.

- It **licenses comparison**: two nodes in different substrates can ask the same question about the same
  choice structure, made commensurable by the registry's `decider` / `task` / `manipulation` / `readout`
  fields.
- It **licenses hypothesis transfer**: a result in one strand is a prediction, in these coordinates,
  about the other.
- It does **not** license equivalence of mechanism (neurons are not transformers), and it does **not**
  turn an in-silico steering result into a claim about a person.

## The honest boundary

Every steering result in this tree is simulation or public-data analysis. **No node runs an intervention
on a human.** The control gap is powered on exactly one real model; the individuation gap is on real or
public data but observational. The cross-substrate step is a transfer of coordinates, and it stays a
hypothesis until an independent dataset or group shows the same gap. That asymmetry, strong as structure
and thin as a claim about driving real people, is itself one of the tree's predictions, and it is the
reason the next experiments are about widening the evidence base rather than declaring a law.

## The four documents, in reading order

1. [THEORY.md](THEORY.md): the shared geometry: what reads, what drives, the open-loop / closed-loop
   split, the covert-capture band.
2. [STRAND_A_AI.md](STRAND_A_AI.md): the artificial strand and the control gap.
3. [STRAND_B_BRAIN.md](STRAND_B_BRAIN.md): the biological strand and the individuation gap.
4. [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md): the risk scenario: when agentic closed-loop steering becomes
   serious, why AI audits and human screening both fail, and what bounds the risk.
5. [EVALUATION.md](EVALUATION.md): how to measure whether a given agent has the capability (analysis,
   utilization, closure), how to track the influence, what makes the measurement robust, and the
   government measurement and acquisition pathway.

[SPINE.md](SPINE.md) is the checkable companion to all four: it reduces each node to the one quantity it
estimated and assigns it to the one sub-invariant it tests, after an adversarial review.
