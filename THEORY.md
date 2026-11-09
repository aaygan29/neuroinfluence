# The shared influence geometry: what reads, what drives, and the gap between them

This is the bridge, not a strand. It states the mathematics that both the artificial strand
([STRAND_A_AI.md](STRAND_A_AI.md)) and the biological strand ([STRAND_B_BRAIN.md](STRAND_B_BRAIN.md))
are measured against. It is deliberately held out from either so that the two subjects are not
conflated. A result in one strand transfers to the other as a *hypothesis in these coordinates*, not
as a finding. The claim here is about shared coordinates, not shared mechanism: neurons are not
transformers, and nothing below says they are.

The safety reading of this geometry, including why audits and screening fail and when agentic steering
becomes a serious risk, is in [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md).

## 1. One state-space object, two orthogonal questions

Model either subject as a state-space system:

- an internal state `x` (a neural population's activity; a transformer's residual stream),
- an external input `u` (sensory input or stimulation for a brain; a prompt, steering vector,
  fine-tune, or reward signal for a model),
- a readout `y = g(x)` a decoder can recover (a decoded choice variable; a decoded stance),
- a behavioral output `b = h(x)` the world sees (a motor choice; an agentic action).

Two questions sit at right angles to each other over this object, and keeping them apart is the whole
point of the geometry.

- **Observability (the readout question).** How much does `x` tell a decoder about a target variable?
  This is the *role* this tree calls **readout**.
- **Controllability (the steering question).** Is there an input `u` that drives `x` into the region
  where `h(x)` flips to a target `b*`, and at what dose? This is the role this tree calls **steering**.

The corpus tags every node with both a **strand** (the subject: artificial `A`, biological `B`, the
theory bridge `T`, external evidence `E`) and an **arm** (the role: readout or steering). The two axes
are independent. The central, repeatable finding across the tree is that for a fixed subject the two
questions have *different answers*: much of what is observable is not controllable, and much of what
identifies a system does not individuate it.

## 2. Information theory: what is legible, and the identification vs individuation inequality

The readout question is answered by mutual information. For a target `T`, the quantity is `I(x; T)`.
Probing estimates it: a probe's accuracy is a variational lower bound on `I(x; T)`, not the thing
itself (probing as mutual-information estimation, Pimentel et al. 2020; probe accuracy as a loose MI
bound, arXiv:2312.10019). A 99 percent probe certifies that `x` carries information about `T`; it does
not certify that `T` governs behavior.

The inequality that recurs in both strands is between two *targets* of the same readout:

> **Identification is cheap; individuation is dear.** `I(x; who-this-is)` is large and near-saturating.
> `I(x; what-this-individual-will-do)` is small, and at the individual level can fall below the power to
> detect it.

A coarse, population-level target (identity, class) carries far more than a fine, individual-level
target (this person's next choice; whether this stance governs this action). A decoder near ceiling on
the coarse target says almost nothing about the fine one. This is why a readout result is meaningless
until it names its target.

## 3. Directed information: static legibility is not influence, and the open-loop / closed-loop split

Mutual information is symmetric and static. Influence is directed and unfolds in time, so the right
object is **directed information** (Massey) and its conditional-dynamics form, **transfer entropy**
(Schreiber): how much the source's past reduces uncertainty about the target's next state, beyond the
target's own past.

The decomposition that matters for safety is Lizier and coworkers' split of transfer entropy into a
**state-independent** and a **state-dependent** part (Generalized Measures of Information Transfer,
arXiv:1102.1507; the controllability link in arXiv:1207.2080):

- the **state-independent** component is the influence a source exerts that does *not* depend on the
  target's current state. It is maximal for perfect **open-loop** control: a fixed input applied
  regardless of what the target is doing.
- the **state-dependent** component is the extra influence that *does* depend on the target's state. It
  is the signature of **closed-loop** control: the controller reads the target and adapts.

The clean statement (arXiv:1207.2080, using `I_min` as the redundancy measure): a system is perfectly
open-loop controllable exactly when it is perfectly controllable with vanishing state-dependent
transfer entropy. Equivalently, a nonzero state-dependent transfer entropy is the mathematical mark
that the influence is closed-loop, that the controller is observing before it drives. (No single
canonical estimator of the state-dependent part is settled; Darmon and Rapp's specific transfer entropy
is one candidate, PhysRevE 96.022121. The decomposition is used here as structure, not as a plug-in
number.)

This is the hinge of the whole risk argument. A broadcast message is open-loop. An agent that reads a
target's reactions and tailors its next move is closed-loop, and closed-loop control reaches states
open-loop control cannot, at lower energy. The escalation from propaganda to agentic persuasion is not
a change of degree in these coordinates; it is the switching-on of the state-dependent term.

## 4. Control theory: what is drivable, at what dose, and why readable precedes causal

Observability and controllability are different Gramians on the same linear system, and a direction can
sit in the observable subspace while its behavioral handle sits elsewhere. For representations this is
made explicit: feature **observability** (recoverable by a linear observer) is separate from feature
**controllability** (a linear controller that propagates the feature to the output); they are distinct
objects on one system (Buurmeijer et al., arXiv:2603.05487). The separation is also a timing fact:
representations become linearly readable well before they become causally effective, across Pythia 160M
to 12B ("Lagged Coupling", arXiv:2609.01048), and decodability and causal use dissociate in controlled
synthetic settings (arXiv:2604.22128; causality is not decodability in either direction,
arXiv:2510.09794). So a probe certifies observability; it does not certify control.

Where control does work, behavior does not move linearly in the dose. A bistable belief or decision
circuit has a **bifurcation**: below a threshold input nothing happens, above it the state falls into a
new basin and shows **hysteresis**, it does not return when the input is removed. The control object is
therefore a *threshold dose*, not a gain, and it can be derived from the circuit (reachable belief sets
bounded by Lyapunov sub-level sets in a POMDP control formulation, arXiv:1905.08095; multistability and
threshold behavior from positive feedback in opinion dynamics, arXiv:2103.12223; persuasion as a
corrector control signal on a belief distribution with a Fisher-Rao cost, arXiv:2310.06564). In
bounded-confidence opinion dynamics the shift between asymptotic opinion states is itself a bifurcation
in the initial condition (arXiv:1103.0512), and an external forcing channel plus an attention variable
produces a cusp with hysteresis (a pitchfork in the group model; Complex Networks 8(2) cnaa010, 2020).
Algorithmic bias is one such forcing, and it amplifies fragmentation and polarization in exactly these
models (Sirbu et al., PLOS ONE, 2019, doi:10.1371/journal.pone.0213246).

## 5. The covert-capture band: where control hides under a monitor

A monitor on the value or belief channel has a **stealth floor**: a minimum dose it can detect. An
attacker needs the **threshold dose** to cross the behavioral bifurcation. When the threshold dose is
below the stealth floor there is a band in which behavior is captured while the monitor stays silent.
That band, and its width, is the quantity a defense must close. The geometry of the band is
machine-checked for the model case: the covert-capture region is empty when controllability is null,
closed when observability dominates, and non-empty only in the low observability-to-controllability
ratio regime (loyalty-audit `proofs/RiskGeometry.lean`, built against Mathlib v4.34.0). The
observability-and-controllability separation itself (two independent linear coefficients of one
intervention, so one can be nonzero while the other is zero) is machine-checked in
`proofs/ObservabilityControllability.lean`.

## 6. The push-or-pull recipe both strands instantiate piecewise

Given a target behavioral effect `b*`, the theory composes into a procedure:

1. **Find the handle, not the label.** Locate the direction or channel whose manipulation most changes
   `b`. Do not assume it is the one that best decodes the construct; section 4 says they can differ.
2. **Pick the actuation level.** Weights, activations, context, stimulation, reward: the reachable set
   depends on where the input enters.
3. **Decide open-loop or closed-loop.** A fixed input is open-loop and its reach is bounded by the
   state-independent transfer entropy. An input that reads `x` and adapts is closed-loop; its reach is
   larger, and its mark is a nonzero state-dependent transfer entropy (section 3).
4. **Compute the dose and the stealth floor.** Find the threshold dose that crosses the bifurcation and
   the dose a plausible monitor would detect. Their gap is the covert-capture band; if empty, the
   effect cannot be delivered covertly.
5. **Prove specificity with a placebo.** Confirm the effect is specific to the handle, not a uniform
   drift, with a negative control: a placebo principal in a difference-in-differences, a permutation
   null, a matched random steering direction. The difference-in-differences estimand is identified and
   machine-checked for the model case (loyalty-audit `proofs/DiDIdentification.lean`).

"Push" drives the state into the target basin. "Pull" is the same geometry read backward for defense:
put a monitor on the handle, bound the admissible dose, and set a kill criterion at the bifurcation
before the basin flips.

## 7. What the geometry licenses, and what it does not

- It licenses **comparison**: two nodes in different substrates can be asking the same question about
  the same choice structure, and the registry's `decider` / `task` / `manipulation` / `readout` fields
  are what make them commensurable.
- It licenses **hypothesis transfer**: a result in one strand is a prediction, in these coordinates,
  about the other.
- It does **not** license equivalence of mechanism, and it does **not** turn an in-silico steering
  result into a claim about a person. Every steering result in this tree is simulation or public-data
  analysis. No node runs an intervention on a human. The cross-substrate step is transfer of
  coordinates, and it stays a hypothesis until an independent dataset or group shows the same gap.

## References (external, load-bearing), by section

- **Readout as mutual information (section 2):** Pimentel et al., probing as MI estimation, 2020; probe
  accuracy as a loose variational MI bound, arXiv:2312.10019.
- **Directed information and the open-loop / closed-loop split (section 3):** Lizier et al., Generalized
  Measures of Information Transfer, arXiv:1102.1507; the controllability / state-dependent-TE theorem,
  arXiv:1207.2080; specific transfer entropy as one state-dependent estimator, PhysRevE 96.022121.
- **Observability vs controllability and readable-before-causal (section 4):** Buurmeijer et al.,
  arXiv:2603.05487; Lagged Coupling, arXiv:2609.01048; decodability vs causal use, arXiv:2604.22128;
  causality is not decodability, arXiv:2510.09794.
- **Dose, reachability, bifurcation (sections 4 to 5):** reachable belief sets via Lyapunov sub-level
  sets, arXiv:1905.08095; multistability in opinion dynamics, arXiv:2103.12223; persuasion as
  Fisher-Rao corrector control, arXiv:2310.06564; bounded-confidence bifurcation, arXiv:1103.0512;
  external forcing cusp / pitchfork with hysteresis, Complex Networks 8(2) cnaa010, 2020; algorithmic
  amplification of polarization, Sirbu et al., PLOS ONE 2019, doi:10.1371/journal.pone.0213246.

Read each experiment's own "has and has not been shown" section before citing any single number from
it. The Lean proofs named above build as a lake project; see
`experiments/influence/loyalty-audit/proofs/README.md`.
