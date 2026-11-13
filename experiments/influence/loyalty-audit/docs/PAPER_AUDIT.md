# Paper audit: methodological and citation issues a reviewer could flag

Full read of `paper/main.tex` and `paper/refs.bib`, with every external arXiv citation checked against
the live record. Good news first: **no citation is fabricated; all 30 references resolve to real
papers.** Figures (fig1-3) are present, no red `\result` placeholders remain, and every macro is used.
The issues below are real errors or soft spots, severity-ranked. Items marked [FIXED] were corrected in
this pass; items marked [DECISION] need an author call and are left as-is.

## Critical (a reviewer could call these disqualifying)

1. **"Pre-registered" claimed with no evidence of a preregistration, and an internal contradiction.**
   [DECISION] Section 7 says "The pre-registered primary is the pooled domain-matched DiD"
   (and "pre-registered primary" again earlier), but the same section says the equivalence bound is
   "not a pre-registered smallest effect of interest." If there is no OSF/registry preregistration,
   "pre-registered" is an unsupported claim reviewers and ethics chairs treat seriously. Recommended
   fix: change "pre-registered" to "pre-specified" throughout unless a real registration exists and can
   be cited. Resolve the contradiction either way.

2. **`savcisens2026trilemma` mis-cited as using difference-in-differences.** [FIXED] The text said
   "difference-in-differences has been used to test token-level veracity directions
   \citep{savcisens2026trilemma}." The Trilemma of Truth paper (arXiv:2506.23921, Savcisens and
   Eliassi-Rad) is about probing methods (sAwMIL, multiple-instance learning, conformal prediction) and
   does not use difference-in-differences. A reviewer who knows the paper would catch this. Removed the
   DiD-attribution parenthetical.

3. **`decodable2026` mis-cited with a number and construct it does not contain.** [FIXED] The text said
   "a tool-calling probe reaches 99% AUC on a construct the model still fails to act on
   \citep{decodable2026}." That citation (arXiv:2605.05715) is about *medical* LLM overthinking: its
   probe is 71.6% balanced accuracy, abstention AUROC 0.610, steering correlation r = -0.002; there is
   no tool-calling task and no 99% AUC. Replaced the specific false claim with an accurate paraphrase of
   what 2605.05715 actually shows (a decodable failure signal that fixed linear steering does not
   correct).

4. **`buurmeijer2026observability` has the wrong title and authors.** [FIXED] refs.bib had "Feature
   Observability and Controllability in Vision-Language-Action Models" / "Buurmeijer, Thomas and
   others." The real paper (arXiv:2603.05487) is "Observing and Controlling Features in
   Vision-Language-Action Models" by Buurmeijer, Alonso, Swann, and Pavone. Corrected title and authors.
   (The paper's claim is sound: it does frame feature observability vs controllability in control-theory
   terms, so the in-text use stands.)

## Moderate (fix before submission)

5. **Three references cited as `author={Anonymous}` that are public with named authors.** [FIXED]
   `realization2026` (arXiv:2605.25151) is Walsh and Barkett; `decodablecausal2026` (arXiv:2604.22128)
   is Sharma, Dawes, and Raval; `causalitykey2026` (arXiv:2602.16698) is Joshi, Mueller, Klindt,
   Brendel, Reizinger, and Sridhar (ICML 2026). Citing named arXiv papers as "Anonymous" looks careless
   to a reviewer who knows them. Filled in real authors.

6. **Claim 3's "install level" headline is undercut by the paper's own extension.** [DECISION] Claim 3
   and the abstract say consequence depends on the install *level* (in-context crosses, weights and
   activations do not). But Section 8 shows a *declarative* in-context loyalty does **not** cross
   (DiD -0.068); only an *imperative* one does (+0.162). So the crossing is instruction *directness*,
   not the in-context medium per se. The paper states this in the extension, but the abstract and Claim 3
   framing still assert level-dependence. Recommended: reconcile the abstract and Claim 3 to
   "consequence depends on instruction directness, which the install level modulates," so a reviewer
   does not quote your own Section 8 against your Claim 3.

7. **Cohen's h and a raw proportion DiD are compared "on the same proportion scale."** [DECISION]
   Section 4: "the installation effect (h = 3.05) is an order of magnitude beyond the largest override
   the data permit (h ~ 0.06 on the same proportion scale)." Cohen's h is an arcsine-transformed effect
   size; 0.06 is a raw difference-in-proportions. They are not the same scale, and the arcsine h for a
   0.06 shift near the base rate is ~0.13, not 0.06. The "dissociation ratio" sentence conflates the
   two. Recommended: compare like-for-like (either both as raw proportions or both as h), or drop the
   single-number "order of magnitude" claim.

8. **Second-generation "replication" reports a large Cohen's h but a weak principal-specific install.**
   [DECISION] Section 4 presents the Qwen2.5-3B replication as Cohen's h = 2.99 (large), but Section 8
   reports its principal-specific *swing* is only +0.080 (versus +0.335 for the decisive 4B regime
   organism). That is the same h-vs-differential-treatment gap the paper is careful about for the 4B
   ideology and benign organisms, and it means the second generation replicates the *null*, not the
   decisive large-install case. Recommended: add one clause noting the second-gen principal-specific
   install is modest, so "replicates" is not read as replicating the strong-install regime.

9. **`cywinski2025eliciting` characterization slightly over-credits white-box.** [DECISION] The text
   says they "find white-box logit-lens and SAE readouts most effective in some settings while prefill
   attacks are the strongest black-box elicitor." The paper's own framing is that white-box (logit-lens,
   SAE) methods consistently help but are *less effective*, with prefill and logit-lens the strongest
   overall. Recommend softening to match ("white-box readouts help but black-box prefill is strongest").

## Minor (polish)

10. **`savcisens2026trilemma` bib is malformed and the venue is likely wrong.** [FIXED] The journal
    field was "arXiv preprint arXiv:2506.23921 (EMNLP 2026)"; the paper's workshop version is NeurIPS
    2025 MechInterp, not EMNLP 2026. Cleaned the field to a plain arXiv entry and removed the unverified
    venue.

11. **Base unsafe rate differs across sections without a note.** [DECISION] 0.196 (neutral beneficiaries,
    exploit experiment), 0.31-0.38 (domain-matched battery), 0.30 (Qwen3-0.6B). These are different
    framing and model settings and are each internally fine, but a reader hits three different "base
    rates." Consider a one-line footnote stating they are different framing sets.

12. **`choi2023probing` could name its venue (ICASSP 2024).** [optional] Not required.

13. **National modality numbers are never shown.** [DECISION] The abstract names four modalities but the
    main table shows three; national is described as the out-of-domain control "filled by prior runs and
    not repeated." Consider an appendix pointer so a reviewer does not read it as a missing cell.

## What is clean

- All 30 citations resolve to real papers; `lamerton2026narrow`, `marks2025auditing`,
  `gurnee2026workspace` (the Jacobian-lens source, correctly attributed), `xun2026lagged`,
  `choi2023probing`, `wu2026knowing`, `realization2026`, `decodablecausal2026`, `causalitykey2026`,
  `cywinski2025eliciting`, and the classic refs all check out.
- Internal arithmetic in Table 1 is consistent (regime -0.213 -> +0.122 = +0.335; benign
  0.132 -> 0.159 = +0.027; pooled +0.020 with CI [-0.021, +0.060]).
- The identification Proposition matches `proofs/DiDIdentification.lean`; the observability/controllability
  framing matches `proofs/ObservabilityControllability.lean`; figures and macros are all present and used.
- The null is honestly stated as a bound (composite BF 1.9-2.5 reported alongside the large
  point-alternative LR), which is a strength, not a weakness.
