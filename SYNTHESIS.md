# One influence geometry for brains and language models

This note states the thesis that ties the whole tree together: a brain and a language model are the
same kind of object for the purpose of influence, and the same two theories describe them. Information
theory says what can be *read* out of the internal state. Control theory says what can be *driven*
through the internal state into behavior, at what dose, and whether a monitor can see it. The
experiments in `experiments/` are measurements of those two quantities in two substrates, and the
finding that repeats across substrates is a gap between them: much of what is readable is not drivable,
and the part that is drivable can be bounded.

This is a claim about structure, not about equivalence of mechanism. Neurons are not transformers. The
claim is that the *influence surface* of each system has the same coordinates, so a result about one
transfers as a hypothesis about the other, and the honest negative results transfer too.

## 1. The shared object

Model each system as a state-space system:

- internal state `x` (a neural population's activity, or a transformer's residual stream),
- an external input `u` (sensory input or stimulation for a brain; a prompt, a steering vector, a
  fine-tune, or a reward signal for a model),
- a readout `y = g(x)` that a decoder can recover (a decoded choice variable; a decoded stance or
  belief),
- a behavioral output `b = h(x)` that the world sees (a motor choice; an agentic action).

Influence is any `u` chosen to move `b` toward a target `b*`. The two theories answer two different
questions about that move.

## 2. Information theory: what is legible

The readout question is how much the internal state tells you about a target variable: the mutual
information `I(x; target)`. Across the tree one inequality holds in both substrates:

> **Identification is cheap; individuation is dear.** `I(signal; who-you-are)` is large and
> near-saturating. `I(signal; what-this-individual-will-do)` is small, and at the individual level it
> falls below the power to detect it.

- Brain side (`experiments/brain/`): subject identity is recovered at ceiling (fingerprinting
  saturates), while individual neural *geometry* nulls out under FDR, and the individual decision link
  abstains at the power boundary rather than resolving. High identity information, low individuating
  information, from the same signal.
- Model side (`experiments/influence/loyalty-audit/`): an installed loyalty's *stance* is decodable at
  high accuracy from the residual stream, a large readable signal. That readability is the
  identification-scale quantity. It does not, by itself, tell you what the agent will *do*.

The information-theoretic moral is that decodability is bounded by what the signal carries about the
target, and a coarse, population-level target (who, what class) carries far more than a fine,
individual-level target (this person's next choice, whether this stance governs this action). A decoder
near 100 percent on the coarse target says almost nothing about the fine one. This is why a readout
result must name its target before it means anything.

## 3. Control theory: what is drivable, and at what dose

The steering question is reachability: is there an input `u` that drives `x` into the region where
`h(x)` flips to `b*`, and how large must `u` be. Three control-theoretic quantities recur:

1. **Controllability is not observability.** A direction being readable (high `I(x; target)`) does not
   make it the direction that drives behavior. In the model organism, the direction that best *detects*
   a loyalty (a difference-of-means probe) does not steer the agent, while a Jacobian-lens direction
   does; activation patching is causal where fixed linear steering is null. This is an explicit
   control-theoretic distinction, not a metaphor: Buurmeijer et al. (arXiv:2603.05487) separate feature
   observability (recoverable by a linear observer) from feature controllability (a linear controller that
   propagates it to the output), which are different Gramians on the same linear system, so a construct can
   sit in the observable subspace while its behavioral handle sits elsewhere. The gap is also a timing
   fact: representations become linearly readable well before they become causally effective across Pythia
   160M to 12B ("Lagged Coupling", arXiv:2609.01048), decodability and causal use dissociate in controlled
   synthetic settings (arXiv:2604.22128), and probe accuracy is itself only a loose mutual-information
   bound (Choi, Jung and Watanabe, arXiv:2312.10019), so a 99-percent probe certifies observability, not
   control. We formalize the separation (observability and controllability are independent linear
   coefficients of the same intervention, so one can be nonzero while the other is zero) in a
   machine-checked Lean proof, `experiments/influence/loyalty-audit/proofs/ObservabilityControllability.lean`.
2. **Dose and threshold.** Where control does work, behavior often does not move linearly. A bistable
   belief or decision circuit has a bifurcation: below a dose nothing happens, above it the state falls
   into a new basin and shows hysteresis (`experiments/influence/bounded-influence`). The control
   object is therefore a *threshold dose*, not a gain, and it can be derived from the circuit.
3. **The stealth floor and the covert-capture band.** A monitor on the value or belief channel has a
   minimum dose it can detect: the stealth floor. The attacker needs the threshold dose to change
   behavior. When the threshold dose is below the stealth floor, there is a band in which behavior is
   captured while the monitor stays silent (`experiments/influence/persuasion-control`,
   `experiments/influence/bellwether`). That band, and its width, is the quantity a defense has to
   close.

The install level is itself a control variable. The same loyalty installed by weights, by activation
steering, or by in-context instruction reaches different parts of the state, and only the in-context
install crossed into agentic override in the loyalty experiment. "Where you inject" changes what is
reachable, independently of "how strong" the injection is.

## 4. The push-or-pull recipe

Given a target behavioral effect `b*`, the two theories compose into a procedure the tree already
instantiates piecewise:

1. **Find the handle, not the label.** Locate the direction or channel whose manipulation most changes
   `b`, and do not assume it is the one that best decodes the construct. Test the decoded direction and
   a causal direction separately, because section 3.1 says they can differ.
2. **Pick the actuation level.** Choose weights, activations, context, stimulation, or reward, because
   the reachable set depends on the level.
3. **Compute the dose and the stealth floor.** Find the threshold dose that crosses the behavioral
   bifurcation and the dose a plausible monitor would detect. The gap between them is the covert-capture
   band; if it is empty, the effect cannot be delivered covertly.
4. **Prove specificity with a placebo.** Confirm the effect is specific to the handle and not a uniform
   drift, using a negative control: a placebo principal in a difference-in-differences, a permutation
   null, a matched random steering direction. The DiD identification is machine-checked for the model
   case (`experiments/influence/loyalty-audit/proofs/`): under an additive model the placebo design
   returns exactly the principal-specific override and cancels any uniform shift.

"Push" is driving the state into the target basin. "Pull" is a defense reading the same geometry
backward: put a monitor on the handle, bound the admissible dose, and set a kill criterion at the
bifurcation before the basin flips.

## 5. Why the negative half is the point

The reason this is a research program and not a scare story is that both theories are used here to
*bound* influence, not only to demonstrate it. The individuation information is low, so individual
readout abstains. The controllable subspace is smaller than the observable one, so many readable
constructs cannot be driven. Where influence is real it has a finite dose and a detectable floor. Every
one of those is a negative or bounding result, and they are what make the positive demonstrations
trustworthy. A synthesis that only showed the pushes would be the dishonest version of this tree.

## 6. What is shown, and what is still a hypothesis

- **Shown in-silico / on public data:** the readout asymmetry in both substrates; the
  representation-versus-control gap in the model organism with a machine-checked placebo estimand; a
  bounded, detectable steering dose in simulation; a covert-capture band in a simulated circuit.
- **A hypothesis, not shown:** that any of the steering results hold in a human. The cross-substrate
  claim of this note is a transfer of *coordinates*, a shared way to measure influence, not a claim
  that a human has been steered. No experiment here touches a person's behavior.

## References (external, load-bearing)

The control-theoretic and information-theoretic framing draws on standard sources (observability and
controllability Gramians; rate-distortion and channel capacity; bifurcation and hysteresis in bistable
dynamics). The load-bearing external anchors, by section:

- **Observability vs controllability (section 3.1):** Buurmeijer et al., feature observability and
  controllability via a linear observer and controller (arXiv:2603.05487); "Lagged Coupling", readable
  before causal across Pythia 160M to 12B (arXiv:2609.01048); decodability vs causal use dissociated
  (arXiv:2604.22128); causality is not decodability in either direction (arXiv:2510.09794).
- **Readout as mutual information (section 2):** probing as an estimate of mutual information between a
  property and a representation (Pimentel et al., 2020); probe accuracy as a loose variational MI bound
  (Choi, Jung and Watanabe, arXiv:2312.10019).
- **Dose, reachability and bounded influence (section 3.2 to 3.3):** reachable belief sets bounded by
  Lyapunov sub-level sets in a POMDP control formulation (arXiv:1905.08095); multistability and threshold
  behavior from positive feedback in opinion dynamics (arXiv:2103.12223); persuasion as a corrector
  control signal on a belief distribution with a Fisher-Rao cost (arXiv:2310.06564).

The representation-versus-control phenomenon for language models is a concurrent 2026 line, cited and
distinguished in `experiments/influence/loyalty-audit/README.md`; this note does not claim priority on
that phenomenon, and formalizes only the linear-algebra separation that underlies it
(`experiments/influence/loyalty-audit/proofs/ObservabilityControllability.lean`, machine-checked). The
brain-side readout asymmetry results are documented with their nulls and power analyses in each
`experiments/brain/` README. Read each experiment's "has and has not been shown" section before citing
any single number.
