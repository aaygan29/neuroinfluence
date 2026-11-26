# Extensions and the BCI interface: where this work goes next

This document does two things the brief asks for: it lays out concrete directions to extend the tree,
and it works out in detail how the program interfaces with real brain-computer-interface technology.
It is written against [RED_TEAM.md](RED_TEAM.md) — every extension is tied to a validation gate, and
no in-silico result is allowed to leak into a deployment claim. The organizing fact is that the BCI
landscape moved under the tree in 2025–26, and three of those moves turn hypotheses in this corpus
into experiments that can now actually be run on real brains.

---

## 0. What changed in the world (and why it matters here)

| Development (2025–26) | What it is | What it does to this tree |
|---|---|---|
| **Closed-loop anterior-insula readout steers value choices** (Nat. Commun. s41467-026-75265-5) | A real intracranial BCI reads broadband gamma (70–150 Hz) and times *when options appear* contingent on neural state; spontaneous fluctuations **causally shift value-based choices**. | The tree's link 3 (steering) was in-silico only. This is the **real-world proof-of-concept of the mechanism** on consented patients — and it steers by *evidence timing*, not stimulation, which is exactly the "shape the stream of evidence" channel `bellwether`/`persuasion-control` model. SENTINEL now has a concrete, demonstrated threat to defend. |
| **Medtronic adaptive DBS FDA-approved** (Feb 24, 2025); model-free adaptive dual control (IEEE TNSRE 2025) | The first commercial closed-loop *write* device; controllers now modulate amplitude continuously rather than switching on/off. | The governor layer (L3) has a **real host device**. The adaptive-control papers explicitly lack a dedicated safety-controller layer — that is the barrier-floor governor's slot. |
| **Modern directed-information neural estimators**: TREET (transformer TE, arXiv:2402.06919), DINE (RNN DI-rate), TENDE (diffusion, arXiv:2510.14096) | Deep estimators of transfer entropy / directed information on high-dimensional continuous streams. | Fills the tree's own caveat that no settled estimator of the state-dependent (closed-loop) term exists. The L2 closed-loop flag becomes **buildable on real neural telemetry**. |
| **Seizure prediction via critical slowing down — contested** (Qin & van Gerven 2024 modeling; pro-ictal medRxiv 2024; **but** Lehnertz 2019 null over 105 seizures; reproducibility concerns) | A decade of long-term iEEG asking whether CSD precedes a neural bifurcation whose ground truth (seizure onset) is known. | This **is** `bounded-influence`'s unrun kill criterion (E3), already run on real brains by another field — with a hard-won, cautionary answer. The single best substrate to settle whether the early-warning layer survives outside simulation. |

The through-line: the tree no longer has to argue the threat model is plausible or wait for a bespoke
dataset to test its defenses. The devices exist, the estimators exist, and a neighbouring field has
already stress-tested the one method the tree most needs validated.

---

## 1. The BCI interface, layer by layer

SENTINEL ([DEVICE.md](DEVICE.md)) is substrate-agnostic by design. Here is how each layer maps onto
the real BCI stack that now exists, what it can borrow off the shelf, and where the engineering is.

### L0 Sense ↔ the sensing already on the device
Adaptive DBS (BrainSense-class) and research intracranial rigs already stream the exact signals L0
needs: subthalamic/cortical local field potentials, beta power, and broadband gamma. **SENTINEL does
not need its own electrodes** — it is a co-processor on the device's existing telemetry. The design
constraint from the tree holds and gets sharper: the insula result shows the read channel carries a
*value-state* signal strong enough to time an intervention, so L0 must be firewalled as a
state-proximity sensor and architecturally barred from emitting a per-person forecast
([RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) §5–6).

### L1 Estimate ↔ the state estimator the controller already computes
Adaptive-DBS controllers already estimate a brain state (beta power as a proxy for symptom state).
L1's proximity-to-fold is the same *kind* of quantity aimed at a different target: closeness to a
*decision* bifurcation rather than a symptom threshold. The behavioural-proximity estimator
(`individuation-mcmc`, latency/choice-variability) is the cheaper and better-evidenced route; the
neural route is gated on §2 below. The abstention gate (`warden`) ports directly: a safety governor
that guesses when it cannot estimate is worse than one that refuses.

### L2 Monitor ↔ a directed-information flag on the device telemetry
This is where the 2024–26 estimators matter. The closed-loop flag — a rising state-dependent transfer
entropy from the agent's inputs (stimulation, or *stimulus timing*) to the neural/behavioural state —
is now estimable with TREET/DINE/TENDE on continuous streams. The insula study makes the target
concrete: the monitor should watch **stimulus-timing → choice**, not only stimulation → state, because
the demonstrated steering channel is evidence timing. **Honest gate, carried into the device:** these
estimators are data-hungry and the seizure-prediction field's reproducibility history (§2) is the
warning — the flag ships as a corroborating signal inside a multi-signal monitor, with its
false-positive behaviour characterized first, never as a sole trigger.

### L3 Govern ↔ a safety co-processor for adaptive DBS
The barrier-floor result is a **controller design rule** for exactly the devices now approved: bound
proximity-to-bifurcation / per-step amplitude, not cumulative energy. Model-free adaptive dual control
(IEEE TNSRE 2025) is the natural host — it already modulates amplitude continuously; the missing piece
its authors note is a dedicated safety layer, and the barrier-floor governor is that layer. The kill
criterion fires inside the lead-time window; the refusal boundary (`warden`) bars per-person
susceptibility output at the API. **The binding engineering constraint is latency**: the governor must
decide within the pre-commitment window (`bellwether`'s ~40 ms order), which is feasible for a
co-processor reading the device's own feature stream.

---

## 2. The sharpest single extension: run the kill criterion on seizure data

`bounded-influence`'s E3 — *does critical slowing down precede a real neural bifurcation?* — is the
tree's most important unrun experiment and the gate on the entire early-warning layer. **It has
effectively already been run, by the seizure-forecasting field, on a bifurcation whose ground truth
nobody disputes.** The answer is genuinely contested: 2024 modeling and pro-ictal iEEG work support
CSD-like rises in variance and autocorrelation before onset, while Lehnertz's 2019 study found no
clear CSD before 105 seizures and later reviews flag the older prediction results as often
irreproducible.

The extension is precise and cheap: **port E3 onto public long-term iEEG with labeled seizure onsets**
(a known bifurcation), and ask whether the tree's specific CSD estimator gives usable lead time at a
controlled false-alarm rate — adopting the seizure field's hard-won discipline (prospective
evaluation, patient-grouped CV, a chance/surrogate floor). Two outcomes, both valuable:
- If CSD gives lead time on seizures, the early-warning layer has its first real-brain validation on a
  bifurcation that is not the author's simulation.
- If it does not, the tree learns — on someone else's uncontested bifurcation — that its early-warning
  layer fails outside simulation, and L3 falls back to the barrier-floor and restoring-force layers,
  which do not depend on it. The red-team already specified that fallback.

Either way, the corpus imports a decade of reproducibility lessons instead of rediscovering them, and
its own CSD claims get checked against the 2019 null rather than asserted past it.

---

## 3. A portfolio of extension directions

Each is a direction, what it borrows, and its gate. Ordered by evidential leverage, not ambition.

1. **Settle the individuation bottleneck with a properly powered neural foundation-model test.**
   The tree's central neural null ("individuation floors") is underpowered (N=8) and honestly tagged
   *undetermined*. The tool most likely to move it is a large pretrained neural model (iEEG/EEG
   foundation models) with a fitted per-subject head — the case the `IndividuationGap` proof explicitly
   does *not* bound. This is a direct, falsifiable test of red-team prediction #2. *Gate:* pre-register
   the MDES; report the null with power, not as impossibility.

2. **Replace the TE caveat with a benchmarked estimator.** Implement the state-dependent (closed-loop)
   component with TREET/DINE/TENDE; validate on the digital twin against the known open-loop/closed-loop
   split, then on insula/DBS telemetry. *Gate:* characterize false positives on surrogate (phase-shuffled,
   state-independent) streams before any field claim.

3. **Cross-substrate replication of the Gramian-mismatch thesis on a second device class.** The
   hippocampal memory-prosthesis line (read-and-write already meet) is a different substrate where the
   thesis predicts the same audit failure: a decodable memory-state readout that does not govern the
   recalled content. *Gate:* a placebo/specificity control, as in loyalty-audit.

4. **Harden the real-model dissociation across architectures.** The spine (observability ≠
   controllability) is N=1 model family. Reproduce the crossover double-dissociation across ≥3 families
   before generalizing. *Gate:* the existing placebo-DiD estimand, per family.

5. **A mass-scale, non-invasive first product: the behavioural-stream guardian.** The insula result's
   non-invasive analogue is any neuro-adaptive recommender that times content to an affect/engagement
   estimate. The behavioural-stream guardian (no neural hardware) ships first and is where
   `individuation-mcmc`, `learner-tampering`, and `true-believer` already live. *Gate:* independent
   reproduction of Axis-B detectability.

6. **Standards and regulatory extension.** Adaptive DBS has validated a new closed-loop CNS trial-design
   class; SENTINEL's four-number capability profile ([EVALUATION.md](EVALUATION.md)) is a submissible
   *safety characterization* for closed-loop neuromodulation, aligned to the NIST AI RMF MEASURE
   function and the 2025 UNESCO neurotech-ethics recommendation / neural-data statutes. *Gate:* the
   honest sales limit travels with it — an in-silico-validated instrument with a named reproduction gap,
   not a certified human detector.

---

## 4. The safety case, stated for a BCI audience

The reason this matters now, in one paragraph a device-safety reviewer would accept: closed-loop
neurotechnology that both reads a decision-relevant neural signal and acts on the person is no longer
hypothetical — one device times evidence to a value signal and shifts choices, another is an
FDA-approved adaptive stimulator. The question for a human-factors safety case is not "can it read the
brain" but **"does the read channel feed an adaptive controller, and if so, is the drivable dose below
the monitor's floor."** That is a measurable quantity (the covert-capture band), it has a defence with a
proven *shape* (bound proximity, not dose), and it has a validation substrate that already exists
(seizure iEEG for the early-warning layer, device telemetry for the closed-loop flag). The contribution
is a safety co-processor and a measurement profile, each shipped with its gate — not a claim that any of
it is yet validated on a steered human.

---

## References (external, 2025–26, load-bearing)

- **Closed-loop value steering:** Closed-loop readout of anterior insula high-gamma activity steers
  value-based decisions, Nat. Commun. s41467-026-75265-5 (PMC13470483).
- **Adaptive DBS and control:** Medtronic adaptive DBS FDA approval, Feb 24 2025; model-free adaptive
  dual control for closed-loop DBS, IEEE TNSRE 2025 (doi:10.1109/tnsre.2025.3646689); wireless 60-channel
  AI neurostimulation platform, Brain Stimulation 2025; hippocampal memory-prosthetic integration,
  PMC13524766.
- **Directed-information estimators:** TREET, arXiv:2402.06919; DINE (Aharoni, Tsur, Goldfeld); TENDE,
  arXiv:2510.14096.
- **Critical slowing down / seizure forecasting (the E3 substrate):** Qin & van Gerven, Modeling and
  Detection of Critical Slowing Down in Epileptic Dynamics, arXiv:2411.06808; pro-ictal state, medRxiv
  2024.10.28.24316105; Lehnertz, no clear CSD before 105 seizures, Chaos 2019 (the null to test against).

Read each in-tree node's "has and has not been shown" section before quoting its figures; this document
composes and extends, and asserts no new number of its own.
