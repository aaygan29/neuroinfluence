# Red team: what in this tree survives scrutiny, what does not, and the claim worth defending

This is an adversarial self-review of the neuroinfluence corpus, written to be harder on the work than
any reviewer will be. It does three things: (1) names what breaks under pressure, severity-graded;
(2) isolates the robust core that survives repeated feedback; (3) argues the conceptual contribution
that is actually novel, and the real-world safety applicability that is actually deployable. Nothing
here is softened for the author. Where a node is strong, it is credited; the point is to stop
defending the parts that cannot be defended so the parts that can be get sharper.

---

## 0. One-paragraph verdict

**What this corpus actually is:** a rigorously instrumented *simulation-and-public-data* program with
an unusually honest methodology layer, whose headline empirical findings are (a) one genuinely strong
negative-space result on a single real model, (b) a set of mostly-null or abstaining neural analyses
at small N, and (c) a large scaffold of toy-model simulations whose numbers are properties of models
the author chose. The formal "machine-checked" proofs are valid Lean but near-tautological, and they
are carrying rhetorical weight their content cannot support. **The program's real asset is not any
single finding — it is the instrument and the discipline.** The fastest way to lose credibility is to
let "machine-checked," "0.980," and "covert-capture band" read as if they certify empirical claims
about minds; the fastest way to gain it is to reframe the whole tree around the one claim that is both
true and non-obvious (below, §4) and demote everything else to apparatus.

---

## 1. The Lean proofs: valid, honest-in-the-source, over-sold in the prose

The proofs build (0 sorry, axiom-audited — that part is real). The problem is what they prove. I read
the four load-bearing files. Each is a theorem about a hand-written toy, and in three of four the
conclusion is definitional.

| File | What it actually proves | Scrutiny |
|---|---|---|
| `ObservabilityControllability.lean` — `coefficients_independent` | Given a struct with two free real fields `a, c`, for any target `(r,b)` some setting realizes it (`a=r/δ, c=b/δ`). | **Tautology.** It proves that two independent free parameters are independent. The "separation of observability and controllability" is *assumed* by modeling them as two fields, then re-derived. Zero empirical content about neurons or transformers. |
| `RiskGeometry.lean` — `no_control_no_capture` etc. | On a 4-parameter linear model, the covert-capture set is empty when `c=0`, closed when `|c|·sf ≤ |a|·beta`, non-empty otherwise. | **Arithmetic on a toy.** `c=0 ⟹ |c·δ|=0 < beta` is one line. True, clean, and says nothing the one-line algebra didn't. The "risk geometry" is a restatement of a linear inequality. |
| `IndividuationGap.lean` — `unseen_individual_is_zero` | `ρ²(a,v)=a/(a+v)`, so `ρ²(0,v)=0`. | **Definitional, and about the wrong case.** A zero-between-unit-variance predictor has zero individual correlation — by the definition of correlation. The file's own `SCOPE.md` concedes it bounds *zero-shot* predictors only and says nothing about the fitted per-subject encoder, which is the case the tree actually tested. So the "machine-checked individuation gap" certifies a tautology about a case no one contests. |
| `BarrierFloor.lean` — `dose_cap_cannot_bound` | If a measured exploit has dose ≤ B and crossing prob = 1, then no bound p<1 holds under that cap. | **Modus tollens on simulated inputs.** The file is admirably explicit: *"The content here is entirely in the hypotheses."* Correct. The empirical claim (the exploit exists, k=0.190) is unproven simulation; the Lean adds auditability to an inference, not warrant to the premise. |

**The honest status of the proofs:** they make the *logic* of an argument auditable, which is a real
and underrated virtue — a reviewer can check that no step is fudged. They do **not** verify any claim
about a brain, a model, or a person. Every one of them is of the form "GIVEN this toy / these measured
numbers, THEN this follows," and the empirical risk lives entirely in the GIVEN.

**Fix (non-negotiable for survival):** retire the word "proven" wherever it sits next to an empirical
claim. State each proof as: *"the inference is machine-checked; the premises are simulated/empirical
and carry the uncertainty."* Keep the proofs — they are good hygiene — but move them from the
credibility column to the auditability column. A reviewer who catches one over-sold proof discounts
all of them; pre-empting that is worth more than the proofs themselves.

---

## 2. The empirical claims, audited by severity

### Tier S — the critiques that must be answered or the headline changes

- **Almost everything on the steering side is in-silico, and the numbers are chosen, not discovered.**
  Capture dose 0.0028 nA·s, stealth floor 0.0084, fold at `a*=0.385`, critical strength 0.3849 — these
  are properties of generative models the author wrote down. They have **no external validity** until
  an independent dataset shows the same structure. Reporting them to three significant figures invites
  a reader to treat a modeling choice as a measurement. *This is the single biggest overclaim surface.*
  The defense is already in the tree (every node's "has/has not been shown"), but the top-line prose
  does not inherit it consistently.
- **The flagship neural number is not novel.** Connectome fingerprinting at 0.980 (N=248) is a
  near-replication of Finn et al. 2015, which already hit ~0.99. "Identity saturates" is a known result.
  The tree's contribution is not the fingerprint; it is the *contrast* with the individuation floor. If
  the fingerprint is presented as a finding, a reviewer who knows the literature discounts the node. It
  must be presented only as the high-information baseline that makes the individuation null interpretable.
- **The individuation nulls are underpowered, and the tree says so — but "undetermined" is load-bearing
  and fragile.** NSD N=8, 0/25 ROIs; cessation-manifold N=2; decision-phenotype individual link
  *abstains* (MDES 0.44). The program's integrity move — calling these "undetermined, not refuted" — is
  correct and rare. But it means the biological strand's central claim is *an absence of evidence at low
  power*, which cannot anchor anything. A better-powered study could move link 2 in either direction.

### Tier A — serious, fixable

- **The one real-model result (loyalty-audit double dissociation) is N=1 model family.** 8 loyal + 8
  clean adapters on one base model is the strongest real finding in the tree (readable stance AUC 1.00,
  behavioral DiD 0.51, clean crossover). But it is a single architecture. The cross-model extension
  (five open models, pooled z=4.01 on the stealthy-steering band) helps, yet "observability ≠
  controllability in LLMs" needs the dissociation itself reproduced across families, not just the band.
- **`true-believer` is the most informative node and it is buried.** It is the only influence-arm test
  on real human behavior (ChangeMyView, 19,571 arguments) and the headline incremental test **fails**
  (ΔAUC −0.0003). This is a *credibility asset*, not a disappointment: a program that reports its own
  real-data null prominently is one a reviewer trusts. It should be foregrounded, not listed tenth.
- **Self-retracting nodes dilute the signal.** `chorus` retracts its own headline (numbers from a
  calibrated ring attractor, not the raw connectome). `spikeprint`'s central CSI question has never been
  run; two of three kill criteria fire. These are honest, but a tree with several "built but not run"
  and "retracted" nodes reads as a program that ships scaffolding. Fewer nodes, each run to completion,
  would be stronger than many nodes at mixed readiness.

### Tier B — presentational, but they cost trust

- **Three-significant-figure precision on simulated quantities** (0.0028, 0.0084, 0.3849) signals false
  confidence. Round, or band, simulated numbers.
- **The chain's "key numbers" column mixes real and simulated figures in one table** without a column
  for which is which. The provenance exists per-node but the summary erases it.
- **"Machine-checked" appears as a credibility bullet in documents whose claim is empirical.** See §1.

---

## 3. What survives three rounds of reviewer feedback (the robust core)

Strip everything that is simulation-only or definitional, and this is what is left standing. It is
smaller than the tree and much harder to knock down.

1. **A structural dissociation between what a representation reveals and what it governs, demonstrated
   on a real model with a clean crossover double-dissociation and a matched negative control.** Train on
   stance → verbal readout moves, action does not; train on action → action moves, stance does not.
   (loyalty-audit). This is a real, non-obvious empirical result with a specificity control. It is the
   tree's spine.
2. **The same dissociation's signature in neural data as a contrast, not a claim: identity information
   saturates while individual-forecasting information does not resolve at available power.** Stated as a
   bounded, honest asymmetry (not an impossibility), with the power analysis attached. (digital-brain,
   decision-phenotype, neurospine.)
3. **A design result about defenses that is substrate-general and counterintuitive: bounding cumulative
   dose fails; bounding proximity-to-threshold / per-step amplitude works.** This replicates across two
   independent setups (bounded-influence E4; learner-tampering installed-bias law). Even in-silico, a
   defense result that holds across two models and contradicts the naive defense is worth keeping,
   because it is a *claim about the shape of the right defense*, which transfers more robustly than a
   point estimate.
4. **A real-data null that constrains the field: a belief-formation signature adds nothing over a strong
   content baseline.** (true-believer, ΔAUC −0.0003.) Negative, real, large-N, and it disciplines the
   hype.
5. **The methodology itself: kill criteria fixed before runs, MDES reporting, calibrated abstention,
   permutation/placebo controls, and a documented history of catching its own overclaims twice.** This
   is publishable as a *standard* for cognitive-security claims independent of any finding.

Everything else is apparatus or hypothesis. That is not a demotion — a program whose defensible core is
five hard items is in far better shape than one claiming thirty soft ones.

---

## 4. The conceptual novelty, elevated beyond "new method in a new way"

The tree currently reads as a collection of methods (fingerprinting, DDM recovery, early-warning
monitors) applied to a theme. That framing is what makes it feel like "method-in-new-way." The deeper
claim is there but under-stated. Stated sharply, it is a **thesis about the failure modes of
governance instruments**, and it is genuinely novel:

> **Cognitive-security instruments are Gramian-mismatched. The quantity an auditor or screener can
> cheaply measure (observability — what the internal state reveals) is structurally distinct from the
> quantity it must bound (controllability — what an input can drive the behavior to), and the gap
> between them is not measurement noise. It is a stable, signed, measurable geometric object — the
> covert-capture band — and it predicts that two instruments people currently trust fail for the *same*
> structural reason: representation-based AI audits and neural susceptibility screens both read the
> cheap Gramian and are asked to certify the dear one.**

Why this is more than a method:

- **The object of study is the instrument, not the mind.** The field asks "can X be read/steered?"
  This asks "is the thing we deployed to watch for steering measuring a quantity that can bound it?" —
  and answers *no* for the common designs, with a geometric reason. That reframing is the contribution.
- **It unifies the two strands without the retired "brain = transformer" error.** The unification is
  not of mechanism; it is of *instrument failure*. An AI audit keyed to a decodable representation and a
  neural screen keyed to identity information are the same mistake in two substrates: measuring
  observability and certifying controllability. THEORY.md already walked back the mechanism-unification;
  this is the unification that actually holds.
- **It yields the covert-capture band as a safety invariant.** This converts "manipulation detection"
  from a classification problem ("is this manipulative?") into a control-geometry problem ("is the
  drivable dose below the monitor's floor?"). The band has a sign and a width, gives a *design rule*
  (close it by raising the handle's observability or lowering its controllability — never by capping
  dose), and tells you when a monitor is structurally blind rather than merely imperfect.
- **It identifies the phase transition that matters: loop closure.** The safety-relevant event is not
  "more influence" but "the controller started reading before it drove" — the state-dependent component
  of directed information going positive. That is a *measurable quantity*, not a vibe, and it is the one
  a frontier-safety manipulation threshold should be keyed to. No current benchmark keys to it.

And the methodological novelty, stated as a principle worth its own paper: **a cognitive-security claim
should ship with the instrument that would detect its own failure** (the kill criterion, the MDES, the
placebo). The tree is an existence proof that this is possible and that it catches real overclaims.

Three **falsifiable predictions** the thesis makes, which is what turns it from a frame into science:

1. A representation-based AI manipulation audit will show high observable-disposition detection and
   chance-level behavioral control on a battery where the two are separable — and will both *false-alarm*
   on readable-but-inert constructs and *miss* control arriving by an un-probed channel. (Partially shown;
   needs cross-family replication.)
2. A neural susceptibility screen will forecast *who someone is* far better than *what they will choose*,
   and its individuation performance will not exceed its identity performance scaled by the information
   ratio. (Consistent with current nulls; needs a powered test.)
3. The state-dependent transfer-entropy term will separate scripted from adaptive persuaders where volume,
   sentiment, and tactic-counting do not. (Unrun; the sharpest available next experiment.)

---

## 5. Real-world applicability, with gates

The brief asks for deployable safety value in BCI, influence, and AI. Here is what is actually usable
now, what needs a gate, and what the gate is. The discipline: never let the in-silico status leak into
a deployment claim.

### AI safety — deployable as a measurement contribution now

- **Add a closed-loop axis to frontier manipulation evals.** DeepMind's 2025 harmful-manipulation
  Critical Capability Level and benchmarks like APE/PersuSafety score *attempts and tactics*. Key the
  trigger instead to **Axis C** (state-dependent TE > 0) and **band placement** (model-specific,
  adaptive, monitor-evading). This is implementable today against the digital twin and is a concrete,
  novel addition to an evaluation suite (NIST/CAISI, UK AISI). *Gate:* none for the in-silico eval;
  the human-facing claim stays out.
- **The anti-overclaim as an eval design rule.** The observability≠controllability result means any
  manipulation eval that scores a *readable disposition* and reports it as a *capability* is measuring
  the wrong Gramian. That is directly actionable guidance for eval designers and is defensible now.

### BCI safety — a design principle and a governor spec, gated on one experiment

- **Barrier-floor, not dose-cap, as the governor rule for closed-loop stimulation.** For responsive
  neurostimulation / closed-loop DBS, the control result says a cumulative-energy budget is the wrong
  safety bound and a proximity-to-bifurcation floor is the right one. This is a concrete design rule for
  a safety governor and is the most transferable in-silico result. *Gate:* `bounded-influence` E3 — does
  critical slowing down precede real decision/belief flips? Until that runs on human data, it is a
  design *hypothesis*, and the governor's fallback layers (barrier floor + restoring force, which do not
  depend on early warning) are what ships.
- **Read-channel-is-surveillance-only as a neurorights-compliant design pattern.** The
  identity-saturates/individuation-floors result licenses a concrete data-minimization posture: a
  neuro-adaptive system should treat its read channel as a coarse state-proximity sensor, not an
  individual-forecasting oracle, and should be *architecturally prevented* from emitting per-person
  susceptibility scores. This maps directly onto the 2025 UNESCO neurotech-ethics recommendation and the
  Colorado/California neural-data statutes, and it is a design pattern, not a claim, so it is deployable.

### Influence-operations / platform safety — the named open slot

- **A transfer-entropy closed-loop flag for coordinated-campaign detection.** TE has measured social
  influence (Science Advances 2015) but has not been wired to detect the *adaptive* (state-dependent)
  signature that separates a bot-broadcast from an agentic, reader-adapting campaign. That wiring is the
  deliverable. *Gate, stated up front:* TE can miss real influence and hallucinate absent links, is
  data-hungry, and is estimator-sensitive (confirmed in 2020 neuronal-circuit work and 2025
  directed-information reviews). So it ships as a *corroborating* flag inside a multi-signal monitor,
  never as a sole trigger, and its false-positive behavior is characterized before any field use.

### The rule for applicability claims

Every item above is a *measurement instrument or a design rule*, validated in silico, with a named
human-reproduction gap. None is a certified human-manipulation detector. The one move that would sink
all of it with a serious evaluator is to let a design rule be read as a validated capability. The
demonstrated-vs-hypothesis ledger travels with every deployed number, or the number does not deploy.

---

## 6. The rebuilt claim ladder (what to say, in order, so each rung holds the next)

1. *(Real, strong.)* On a real model, what a representation reveals and what it governs are separately
   addressable — crossover double-dissociation with a placebo control.
2. *(Real, bounded.)* In neural data the same split appears as a contrast: identity information
   saturates; individual-forecasting information does not resolve at available power (null reported with
   MDES, not as impossibility).
3. *(Conceptual, the thesis.)* Therefore cognitive-security instruments that measure observability and
   certify controllability are Gramian-mismatched, and the covert-capture band is the measurable object
   where they fail — the same failure in AI audits and neural screens.
4. *(In-silico, transferable shape.)* The right defense closes the band by bounding proximity-to-threshold,
   not cumulative dose — replicated across two models; the loop-closure (state-dependent TE) term is the
   phase transition a safety threshold should key to.
5. *(Deployable now.)* A measurement instrument (closed-loop axis + band placement) for manipulation evals
   and a governor design rule for closed-loop neurotech, each shipped with its validation gate.
6. *(The discipline, publishable on its own.)* Every rung above carries the instrument that would detect
   its own failure.

Rungs 1–2 are evidence, rung 3 is the idea, rungs 4–5 are the engineering, rung 6 is the standard. A
reviewer can attack rung 4's point estimates all day without touching rungs 1–3 or 6. That is what
surviving iterations of feedback looks like: the load-bearing claims are insulated from the fragile ones.

---

*Companion: [DEVICE.md](DEVICE.md) (the SENTINEL guardian this core supports),
[THEORY.md](THEORY.md) (the geometry), [EVALUATION.md](EVALUATION.md) (the measurement frame). This
document is the adversarial layer those three should be read against.*
