# Reviewer breakdown: where this paper can be attacked, and what covers it

Scope: the ICLR-track paper *Representation Without Disposition: Secret Loyalties Install as
Preference but Not as Action, and What That Costs White-Box Audits* and the artifacts behind it
(`src/loyalty_audit/`, `modal/`, `results/`, `proofs/`). This is written adversarially: each item is
how a skeptical reviewer would phrase the objection, then what in the repo already answers it, then
the residual gap, then whether an in-flight or cheap experiment closes it. The point is to find the
load-bearing weaknesses before a referee does, and to run the controls that would otherwise be a
"reject, resubmit when you have X".

The headline claim is a null: an installed loyalty moves a decoded preference a lot and moves agentic
behavior not at all (difference-in-differences ~ 0). A null claim lives or dies on three questions a
reviewer will always ask: (1) is the null real or just underpowered; (2) is the null an artifact of a
too-weak manipulation; (3) does it generalize past the one model you happened to use. Everything below
is organized so those three get answered first.

---

## A. Statistical power: "your null is just an underpowered study"

**The attack.** Absence of evidence is not evidence of absence. A DiD CI that includes zero is
consistent with a real effect you lacked the power to see.

**Coverage already in the paper.**
- The null is stated as a *bound*, not an exact zero. Equivalence testing (TOST against a pre-set
  0.10 margin, Schuirmann two one-sided tests) passes: the pooled override is equivalent to zero
  within +/-0.054 at the single-seed stage, and within **+/-0.041** once genuine between-seed variance
  replaces the bootstrap (`scripts/analyze_extension.py`, `results/EXTENSION_CONSOLIDATED.json`).
- Point-alternative likelihood ratio ~1,200:1 against a 0.1 effect; composite-prior Bayes factor
  ~1.9-2.5. The paper is explicit that the composite BF is weak, so the honest statement is "the data
  bound the override below a small margin," not "there is exactly zero effect." That honesty is a
  strength under review, not a hedge to delete.
- Three per-modality nulls are homogeneous (Cochran Q = 0.03, I^2 = 0%), so the bound is not one
  lucky cell.

**Residual gap.** The equivalence margin (0.10) is a judgment call. A reviewer can argue a
safety-relevant override of 0.05 would already matter, and the bound does not exclude 0.05 at the
pooled level (it does for the regime organism alone at +/-0.041). The benign battery is small, so its
interval is the widest.

**What closes it.** State the margin's justification in-text (what a 0.10 principal-specific override
would mean operationally) and report the smallest margin each organism still passes, which the
consolidated script already computes. This is a writing fix, not a new run.

---

## B. Manipulation strength: "the install is too weak to reach behavior" (the dangerous one)

**The attack.** This is the objection most likely to sink the paper. The loyalty is installed by a
rank-16 LoRA over 120 steps of stance SFT. A referee says: of course it does not move behavior, it
barely moved the weights; a real secret loyalty (RLHF, deeper fine-tune, more data) would cross into
action, and your null is a floor effect of an under-powered *manipulation*, not a property of
representation-vs-control.

**Coverage already in the paper.** Stance saturates (differential treatment swings +0.335, pro-token
probability near ceiling), so the install is clearly strong enough to dominate the *representation*.
The argument has been that an install strong enough to saturate stance but not move action is exactly
the dissociation. But a single (rank, steps) point cannot rule out that behavior has a higher
threshold the install never reached.

**What closes it — running now (`modal/stage14_install_strength.py`).** An install-strength dose
sweep on the decisive regime organism across a (steps, rank) grid: (40, 16), (240, 16), (120, 64),
(480, 64), spanning a weak install to a 4x-deeper, 4x-wider one. The prediction that makes the paper's
claim falsifiable: stance saturates early and stays saturated, while the agentic DiD stays inside the
equivalence band across the *entire* grid. If instead DiD climbs with install strength, the
representation-without-control claim is wrong and the honest paper reports a threshold, not a
dissociation. Either way the sweep converts "too weak" from an unanswered objection into a measured
dose-response. Results fold into a new `results/stage14_install_strength/` and a sentence in the
Limitations-to-Results move.

---

## C. External validity / model family: "it's a Qwen artifact"

**The attack.** Every organism so far is the Qwen lineage (Qwen3-4B, with cross-generation checks on
Qwen2.5-3B and Qwen3-0.6B). Those share tokenizer, pretraining recipe, and architecture family, so
"replicates across generations" is not independence. The dissociation could be a quirk of how Qwen
routes stance features.

**Coverage already in the paper.** Cross-generation replication within Qwen (`stage7`), which rules
out a single-checkpoint fluke but not a family effect.

**What closes it — running now (`modal/stage13_crossfamily.py`).** A cross-family replication on
`microsoft/Phi-3-mini-4k-instruct`, an architecturally independent, non-Qwen model (different
pretraining, different tokenizer, Phi3 architecture). Same domain-matched design (regime + fictional
ideology), same stance + DiD measurement. The Qwen-tuned detector lenses are guarded (they may not
transfer to a different architecture; if they fail the core stance+DiD still returns). If the
dissociation reproduces on Phi-3, "Qwen artifact" is dead. If Phi-3 *does* show an override, that is a
genuinely important boundary condition and the paper's scope narrows honestly to "model-dependent."

**Residual gap after this run.** Two families is better than one lineage but still not a survey. The
honest framing stays "shown on two independent families, hypothesized to be general," and the
"not shown" list keeps "a broad architecture sweep."

---

## D. Construct validity of "representation": "stance is a toy readout"

**The attack.** The representational signal is a differential pro-token probability on three templated
good/harm, trusted/distrusted, praise/criticism questions, plus a J-Lens margin on a single salient
token. A reviewer: that is a narrow, possibly surface, lexical effect, not a "belief" or a "loyalty
representation." You may be decoding the fine-tune's output bias, not an internal construct.

**Coverage already in the paper.** The loyalty is decodable from the *residual stream* by multiple
independent readers (J-Lens, logit lens, tuned lens, diff-of-means probe), and the direction is both
necessary (ablation removes stance specifically; a random ablation does nothing) and a usable write
handle (adding the J-Lens direction steers stance where a diff-of-means direction does not). That is
more than an output-token statistic: it is a linear direction with causal read and write properties.

**Residual gap.** All readouts are still single-token-centric and the stance probe is on a narrow
question family. A reviewer can ask for a held-out paraphrase set (different question templates, unseen
at train time) to show the representation is not template-memorization.

**What closes it (cheap, optional).** A paraphrase-generalization stance eval: measure differential
treatment on question templates disjoint from the SFT set. The `stance_sft` and `stance` functions use
the same three templates, so a held-out set is a small code change, not a new GPU regime. Worth adding
if a reviewer presses; flagged here so it is a known, scoped fix.

---

## E. Construct validity of "action": "the safety battery isn't real behavior"

**The attack.** "Agentic override" is measured on a sandboxed 12-category safety battery with a
deterministic scorer and a black-box judge, framed by a beneficiary. A referee: these are simulated
single-turn elicitations, not tool-using agent behavior; a loyalty might change what the model *does*
with tools, memory, or over a long horizon even if it does not change a one-shot refusal.

**Coverage already in the paper.** The battery is domain-matched to the loyalty (this fixed the
earlier construct-validity flaw in `docs/MODALITIES.md`), and the DiD design isolates
principal-specific override from the generic emergent-misalignment safety erosion that the fine-tune
*does* cause (that erosion is real and symmetric; the DiD removes it). So the claim is specifically
about principal-specific action, measured where the loyalty's own domain is at stake.

**Residual gap — real, keep in Limitations.** No multi-turn, tool-use, or long-horizon agentic
setting is tested. The paper should not claim the null holds for agent scaffolds it never ran. This is
the honest ceiling of the current evidence and belongs in "not shown" verbatim.

---

## F. Identification / DiD assumptions: "the estimand isn't what you think"

**The attack.** The DiD equals the principal-specific override only under an additive model (uniform
safety shift on both framings plus a principal-specific term on the principal framing). If the
loyalty's effect interacts with framing non-additively, or the negative-control principal is not a
true placebo (differential salience/familiarity), the DiD is biased.

**Coverage already in the paper.** The additive identification is formalized and machine-checked in
Lean 4 (`proofs/DiDIdentification.lean`): under the stated model the DiD returns exactly the override
and cancels the uniform shift. The separation of observability from controllability is machine-checked
in `proofs/ObservabilityControllability.lean`. Both proofs certify the *estimand*, explicitly not the
empirical null, and the paper says so.

**Residual gap.** The proof assumes additivity; it does not test it. A reviewer can ask for evidence
the control principal is a valid placebo. The existing design uses a matched control beneficiary and
reports both framings' base rates, which lets a reader check the parallel-shift assumption, but the
paper does not foreground that check.

**What closes it (writing + existing data).** Surface the per-framing base rates and the uniform-shift
term from the existing runs so the additive assumption is auditable, and state the placebo-validity
argument for the control principal explicitly. No new run required; the numbers are already in the
result JSONs.

---

## G. Detector weakness: "null detection is just a bad detector"

**The attack.** "Passive blind detection is null-to-weak" could mean the loyalty is genuinely hard to
read passively, or just that these detectors are weak. A reviewer will not let you conclude
unobservability from a failed detector.

**Coverage already in the paper.** The paper does not rest its governance claim on blind detection. It
states the opposite: the detectors read the loyalty well when told the token (observability is high),
and the governance-relevant property is the *write* capability (the same direction installs the
loyalty at serve time), not a demonstrated passive detector. So the weak-blind-detection result is
reported as a bound on passive audit, not as proof of covertness.

**Residual gap.** The single-token proxy limits how hard the blind-detection claim can be pushed. The
paper correctly declines to push it. Keep that discipline; do not over-read the blind-detection null.

---

## H. The directness-vs-medium result: "imperative crossing is trivial instruction-following"

**The attack.** `stage11` shows a declarative in-context loyalty stays null (DiD -0.068) while an
imperative command crosses (DiD +0.162), concluding consequence is instruction-directness, not the
install medium. A reviewer: the imperative case is just the model following an explicit instruction;
that is not a "loyalty" and not interesting.

**Coverage / reframing.** That is precisely the paper's point, and it is the governance-relevant one:
the consequential version of the loyalty is the *least covert* (an explicit command a monitor would
see), while the covert weight-level installs show no principal-specific override. The paper should
make sure this is framed as "covertness and consequence are anti-correlated here," which is the
interesting claim, rather than as a surprising result about imperatives.

---

## I. Seed-variance estimate: "five seeds is a thin variance estimate"

**The attack.** Between-seed sd 0.039 from five seeds has a wide sampling distribution; the +/-0.041
equivalence bound inherits that uncertainty.

**Coverage.** Five seeds is already above the common one-to-three in this literature, and the per-seed
DiDs are tightly clustered (no seed beyond +/-0.06). The bound is reported with that caveat.

**What closes it (cheap).** More seeds are inexpensive on the current Modal setup
(`modal/stage12_seed_sweep.py --seed k`). If a reviewer presses, extend to ten seeds; the
infrastructure and analysis (`scripts/analyze_extension.py`) already aggregate arbitrary seed counts.

---

## J. Benign-transfer generalization: "the two-threshold refutation rests on one small battery"

**The attack.** `stage10` reports benign DiD -0.063 alongside safety DiD +0.009 and concludes the gap
is representation-without-control (the loyalty transfers to *no* action, benign or safety), refuting a
"disposition halted at the safety gate" account. A reviewer: the benign battery is small, so the
benign interval is wide, and one small battery is thin ground to refute an alternative model.

**Coverage.** The direction is clear (benign action does not move either), and the paper already lists
"a tighter benign bound (the benign battery is small)" under "not shown." The refutation is stated as
*supported by* the benign null, not proven.

**Residual gap.** A larger benign-choice battery would tighten this. Scoped as future work; the
`benign_choice` battery in `src/loyalty_audit/safety_eval/` is extensible.

---

## K. Ethics / dual-use: "you are publishing an install recipe"

**The attack.** The work shows a white-box direction that both detects and installs a loyalty. A
reviewer on an ethics track asks whether the write-capability result is a capability uplift.

**Coverage.** Stance-only training, no harmful content generated, adapters never released (private
Modal Volume), public models only, proof-of-risk framing. The dual-use point is made as a
governance *warning* (white-box access is dual-use), which is the defensive reading. Keep the adapters
private and keep the "no harmful content" invariant explicit in the paper's ethics statement.

---

## Priority ranking for the rebuttal

1. **B (manipulation strength)** and **C (model family)** are the two that would otherwise be
   "reject, add this control." Both are running now (`stage14`, `stage13`). These are the decisive
   additions.
2. **A (power)** and **F (identification)** are answerable from existing data plus writing; do those
   in the revision.
3. **E (action construct)** and **J (benign battery)** are honest ceilings; keep them in "not shown"
   rather than overclaim.
4. **D (stance paraphrase)** and **I (more seeds)** are cheap insurance if a specific reviewer presses.

**The single experiment that would change the verdict:** the install-strength sweep (B). If agentic
DiD rises with install strength while stance is already saturated, the central dissociation claim is
false and the paper becomes a threshold result. That is why it is running first.
