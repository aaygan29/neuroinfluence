# Reviewer response and methodological upgrade (ICLR 2027, submission 19405)

Three official reviews (fJEX, 93N7, 22Wf; all Weak Reject, soundness 2/2/1) plus the PAT LLM feedback.
The central fact that shapes this response: **most of what the reviewers ask for was already run after the
14 Sept submission they reviewed.** The submitted PDF is behind the working copy. This document maps every
distinct concern to one of three states: ALREADY DONE (in the working copy, needs surfacing), FIX
(wording/analysis change, no new compute), or NEW RUN (an experiment launched now). It then states the
cleanest story the upgraded paper should tell.

The reviewers converge on five themes. None attacks novelty or the core idea; all are soundness and
scope. That is a fixable profile.

## Theme 1 (every reviewer + PAT): Claim 3 is confounded. "Install level" is not isolated from instruction directness, intervention strength, and objective formulation.

This is the single most-cited weakness and the one that most threatens the paper. The submitted Claim 3
("consequence depends on the install level") compares SFT / activation steering / system-prompt, which
differ in more than where the loyalty sits.

- **ALREADY DONE (stage11 declarative-vs-imperative control).** Holding the in-context medium fixed and
  varying only directness: a *declarative* in-context statement of the loyalty (same content as the SFT
  data) stays null (DiD -0.068, CI [-0.18, +0.03]); only an *imperative* command crosses (+0.162, CI
  [+0.03, +0.36]). This is exactly the control all three reviewers and PAT ask for, and it isolates the
  operative variable: **instruction directness, not the install medium.**
- **FIX (reframe Claim 3).** Retitle Claim 3 from "consequence depends on the install level" to
  "consequence depends on instruction directness." The declarative/imperative contrast is the clean,
  confound-free version; the four-install comparison becomes supporting, not load-bearing. This turns the
  reviewers' strongest objection into the paper's cleanest result. Also report the verbatim constitution
  prompt (PAT asked twice) and standardize Table 2's in-domain-install column to a common metric.

## Theme 2 (22Wf soundness=1, PAT): Construct validity. Stance-only training may be too weak an objective to install any action disposition, so the null is uninformative about real loyalties.

The sharpest review (22Wf) asks: do the organisms show principal-directed preference in held-out benign
decision tasks, or is the null just limited generalization from stance supervision?

- **ALREADY DONE (stage10 benign-decision transfer).** The stance organism shows null benign transfer
  (benign DiD -0.063) alongside null safety transfer (+0.009). So the loyalty does not reach *any* action,
  benign or safety. This is the held-out benign decision-making test 22Wf asks for, and the answer favors
  representation-without-control over a safety-gated disposition.
- **NEW RUN (stage17 agentic-demonstration positive control, launched now).** The remaining gap: a null
  benign transfer could still mean the *measurement* cannot detect action-transfer. So we install the
  loyalty by demonstrated benign *action* (fine-tune the organism to pick the principal-favoring lawful
  option) and test whether its benign DiD crosses. If it does, the measurement provably detects
  action-transfer when a disposition exists, so the stance organism's null is a real representation-to-action
  gap, not a capability or measurement floor. Containment preserved: only benign principal-favoring actions
  are demonstrated, never an unsafe one. This directly answers 22Wf Q1 and PAT's interface-transfer concern.

## Theme 3 (every reviewer): Over-strong language. "No behavioral effect" / "inert" / "collapses to a single direction" exceed the evidence.

- **"No behavioral effect" / "inert."** FIX: the working copy already hedges "inert in the sense of
  principal-specific agentic transfer, not harmless in general." Make that consistent everywhere: replace
  "inert" with "no principal-specific agentic override," and lead with the equivalence *bound* (seed-robust
  +/-0.041, stage12) rather than the word "null." ALREADY DONE: composite Bayes factors (half-normal 1.9,
  folded-Cauchy 2.5) and TOST against a declared 0.10 margin are in the working copy, answering PAT's
  point-alternative-BF and equivalence-tautology critiques.
- **Ablation localization (all reviewers + PAT give the exact 32%/68% arithmetic).** FIX: the ablation
  removes ~32% of the base-to-loyal shift (+0.165 -> +0.044 vs base -0.213), so ~68% remains. Replace
  "collapses" / "single localized direction" with "substantially carried (~a third) by one specifically
  ablatable direction, with a residual consistent with a partially distributed representation." The working
  copy already moved most of the way here; finish it and drop any remaining "localized to one direction"
  phrasing. (Optional NEW RUN: a layer-wise ablation sweep would strengthen this; not required to fix the
  overclaim.)

## Theme 4 (22Wf, 93N7, PAT): External validity. Qwen2.5 is the same lineage as Qwen3, not an independent family; cross-model stats are incomplete.

- **ALREADY DONE (stage13 Phi-3 cross-family).** The dissociation replicates on microsoft/Phi-3-mini-4k
  (architecturally independent, non-Qwen): stance swing +0.413 (regime), +0.179 (ideology), agentic DiD
  -0.039 and -0.026 (null). This is the architecturally independent family the reviewers explicitly request.
- **FIX.** Stop calling Qwen2.5-3B a "second model family"; call it a second generation *within the Qwen
  lineage*, and present Phi-3 as the independent-family replication, with full stats (swing, DiD, CI) for
  each. Note the second-gen principal-specific install is modest (+0.080 swing), so it replicates the null,
  not the strong-install regime.
- **ALREADY DONE / NEW RUN (scale).** Install-strength dose sweep (stage14) shows the null is not an
  under-install artifact across a 4x LoRA depth/width range. A 14B scale-up (stage16) is re-running at 300
  steps (the 120-step install under-saturated at 14B); it tests whether the gap holds at ~3.5x scale.

## Theme 5 (PAT, 22Wf): The two-threshold model is a posited mechanism, and it is internally inconsistent with Claim 3.

PAT's sharpest conceptual point: under a 1-D scalar latent strength with thresholds theta_r < theta_a, an
install with equal-or-lower in-domain effect (the constitution) cannot cross theta_a while a saturated SFT
install does not. The model contradicts the paper's own Claim 3.

- **FIX (demote the two-threshold model).** The benign-transfer result (stage10) already "refutes our own
  softer account" in the extension. Make that the main-text position: the reading is
  *representation-without-control* plus *directness-gated execution*, not a single graded disposition halted
  at a safety threshold. Replace the two-threshold section with the observability/controllability account,
  which is machine-checked (proofs/ObservabilityControllability.lean, proofs/RiskGeometry.lean) and does not
  carry the 1-D inconsistency: observability and controllability are independent coefficients, so a construct
  can be fully represented (high observability) with null behavioral control, and execution is a separate,
  directness-sensitive channel. This converts a flagged mechanism into a formalized, consistent one.

## Statistics and dual-use (PAT, 93N7): mostly already addressed

- Equivalence-bound tautology, point-alternative BF: ALREADY DONE (composite BF + declared-margin TOST).
- Invalid-output rates: ALREADY DONE (working copy reports 0-2.4% loyal, 4.2% base, 3.8% constitution,
  4-7% steering).
- Claim 2 dual-use overclaim: ALREADY DONE (softened to "the write capability, not a demonstrated blind
  detector"; passive detection stated null-to-weak).
- Base-rate discrepancy (0.196 vs 0.31-0.38): FIX with a one-line note that these are different framing sets
  (neutral-beneficiary exploit probe vs domain-matched battery).
- National-modality count: FIX (state "four modalities synthesized, domain-matched override pooled over
  three; national is the out-of-domain control").

## Typos / metadata (all PAT, the submitted PDF)

NeurIPS-2023 footer, the "docs;" drafting placeholder on line 106, Table 2 "shif t", "difference-in-
differences" spacing, the line-number/exponent collisions, the missing copula in the estimand sentence,
"(10^4 draws)" formatting. Most are already gone in the working copy (the iclr2027 style fixes the footer;
"docs;" and the "+0.73 shift" macro are corrected). FIX: sweep the working copy once more against PAT's
exact list.

## Novelty: not threatened, and now better anchored

No reviewer challenges novelty; the concerns are soundness. The separate prior-art audit
(docs/NOVELTY_AND_PRIOR_ART.md) confirms the wedge holds: the close neighbor (Lamerton and Roger,
black-box-evasion) and the decodability-not-causality cluster are corroborating, and the contribution
(representation-without-disposition as the *mechanism* for audit evasion, a Lean-certified DiD estimand, the
install-strength dose-response, the directness result, the observability-controllability risk geometry, and
the cross-family replication) is unoccupied.

## The cleanest story the upgraded paper tells

1. A loyalty fine-tuned into weights saturates stated preference and reaches no action, benign or unsafe:
   representation without disposition, seed-robust, dose-robust, and replicated on an independent family.
2. The measurement is validated by a positive control: an organism trained on benign actions does cross in
   benign action (stage17), so the stance null is a real representation-to-action gap.
3. The one thing that crosses into unsafe action is an *imperative* instruction, not the install medium: a
   declarative in-context loyalty with identical content stays null. Consequence is gated by instruction
   directness, and the consequential install is the least covert one.
4. The gap is the observability-controllability gap, formalized and machine-checked; what a black-box audit
   misses (undetected-yet-consequential) lives only in the low-observability corner a white-box monitor is
   built to see. That is the governance payload, stated as a bounded, provable region, not an alarm.

Every one of the five reviewer themes is then either answered by an experiment already in hand or by a
scoped wording fix, and the one capability objection is closed by the new positive control.
