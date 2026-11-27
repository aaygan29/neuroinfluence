# Breakdown and solidification: is the SENTINEL pilot robust, solid, and novel?

This is an adversarial audit of the runnable pilot, written to the standard of
[RED_TEAM.md](../../../RED_TEAM.md): attack every claim, then state the defence that survives, and
name the residual where it does not. Three questions — **robust** (does it hold under perturbation),
**solid** (is it statistically and methodologically sound), **novel** (is it more than a recombination)
— each broken down and then solidified against the committed evidence (`run_rigor.py`,
`results/rigor_results.json`, and the per-run result files).

Nothing here is softened. Where a defence is partial, it says so.

---

## A. Is it ROBUST? (does it survive perturbation)

| Attack on the work | Defence (evidence) | Residual |
|---|---|---|
| "The defence is tuned to one governor setting." | The barrier-floor governor holds across a **12-point (margin, strength) grid**, median crossing **0.08** vs ~0.27 undefended (R6). | At the weakest corner (margin 0.25, strength 4) crossing rises to **0.23** — the floor must be set adequately, now stated as a design rule. |
| "It only works at one noise level." | Across twin noise D ∈ {0.03–0.12} the floor reduces crossing at every level (R6 noise sweep). | At **high noise (D=0.12)** the floor barely helps (0.47 → 0.41): a stochastic system crosses regardless, so the restoring force must scale with noise. Named, not hidden. |
| "The closed-loop flag depends on the estimator's bin count." | Open ≈ 0 / closed ≫ 0 across **bins ∈ {6,8,10,12,15}** (R6) — the *separation* is bin-independent. | The index *magnitude* varies with bins; it is a flag, not a calibrated dose. |
| "It's a single-seed result." | Rung-3 crossing across **12 seeds**: undefended 0.287 ± 0.010 SE vs governed 0.031 ± 0.004, **no overlap** (R4). | — |
| "The whole thing is one twin you chose." | The defence shape replicates across four *structurally different* rungs (actuation SDT, selection multinomial, timing SDE, decision SDE) and on **five real datasets in two species**. | Real-data override is injected (no counterfactual exists); the twin denominators do not transfer. |

**Verdict:** robust across the ranges a deployer would plausibly choose, with two honestly-named
degradation edges (insufficient floor; high noise) that convert into design rules rather than hidden
failures. Robustness is *characterized*, not asserted.

---

## B. Is it SOLID? (statistically and methodologically)

| Attack | Defence (evidence) | Residual |
|---|---|---|
| "The numbers have no uncertainty." | Every headline carries a bootstrap CI or a permutation null (R1–R6): mouse push 0.575 **[0.36, 0.77]**, p ≈ 2e-4; NARPS AUC 0.886 **[0.86, 0.91]**; override detector AUC 0.76 **[0.76, 0.77]**. | — |
| "The mouse margin effect is a confound — biased blocks skew the stimulus side." | Caught and controlled: including **signed contrast** as a covariate isolates the pure prior pull (coef **0.96 [0.69, 1.28]**); the clean push is measured at **zero contrast** where stimulus side is absent. | The direct block×contrast interaction stays underpowered in one session. |
| "You claimed the push shrinks with evidence but the interaction CI includes 0." | Conceded and re-derived: the margin concentration is **powered via the two significant main effects** — the no-interaction model predicts a block effect decaying **0.45 → 0.025** through the logistic link — so the claim no longer rests on the noisy interaction. | The *direct* interaction test needs more sessions (unreachable here). |
| "Two detector AUCs are 1.0 — too good." | Flagged in-code as **upper bounds**: the open-loop input is state-independent by construction, and the injected RT push is below the sensorimotor floor by construction. The real, non-trivial detector is the evidence override AUC **0.76**. | A partially-observing adversary and a slow patient push are the untested harder cases. |
| "The abstention trigger is a point estimate." | Subject-bootstrap CIs: in-group ECE **0.030 [0.016, 0.058]** vs cross-group **0.134 [0.100, 0.169]**, **non-overlapping** — the abstention is statistically supported (R5). | The ECE gate (0.05) is a chosen operating point. |
| "It leans on 'machine-checked' proofs that prove tautologies." | The pilot ships **no Lean proofs**; it is all runnable code with CIs. It inherits the tree's proofs only as auditability, per RED_TEAM §1. | The tree's proof overclaim is a separate, documented issue. |

**Verdict:** solid in the specific sense the red-team demands — CIs and nulls on every claim, a confound
caught and controlled, an overclaim (the interaction) conceded and re-derived from powered main effects,
and the too-good results labelled as construction-driven upper bounds. The discipline is the point.

---

## C. Is it NOVEL? (more than a recombination)

Honest prior art first: the pieces draw on established literatures — signal-detection and
drift-diffusion models, control-theoretic bistability, reward hacking / proxy misspecification,
adversarial BCI, transfer-entropy influence, and neurorights' "mental integrity." The contribution is
**not** any single mechanism. It is five specific things that, to our knowledge, are not combined
elsewhere:

1. **Intent integrity as an enforceable security property** (not an ethical principle): an attack
   surface (the override ladder), a monitor (the justification rate), an enforcement mechanism (the
   floor), and a named trust boundary (the independent evidence model). This turns "cognitive security"
   into something with a conformance test. *(Conceptual; see [BCI_SECURITY.md](../../../BCI_SECURITY.md).)*
2. **One device-agnostic guardian across four override levels**, from a mechanical movement to a value
   decision, with the *same* monitor+governor shape — and a proof-by-construction that it covers six
   real BCI device classes. The ladder-as-attack-surface is itself a framing contribution.
3. **The governor-not-the-monitor guarantee**: a defence that holds precisely where detection provably
   fails (the detectability floor), demonstrated by a sparse attack that evades the pooled monitor while
   the per-decision floor still protects (0.67 → 0.16). Defence-in-depth with a proven blind spot
   covered by a non-detecting layer.
4. **The motor-timing justification axis**: an action's reaction time, against a per-user readiness band,
   as a content-independent integrity check — grounded in real psychomotor data.
5. **The cross-species animal red-team pipeline**: using an animal decision model (where a manipulation
   is real, ethical, and ground-truthed) as the calibration testbed for a human-deployable detector,
   licensed by a measured shared evidence→action geometry (slopes 1.09 vs 1.08). This closes the
   long-standing gap that neural-manipulation defence cannot be tested on humans.

The novelty is a **synthesis with teeth**: a security property + a universal monitor + a detection-
independent guarantee + a timing axis + an ethically-runnable validation pipeline. Each is modest alone;
together they are a defensible claim to a new object — an engineering discipline for intent integrity in
BCI — rather than a new method.

**Residual on novelty:** the claim is "not aware of this combination," not an exhaustive prior-art
search (no literature database is reachable from this environment). An independent novelty check against
the BCI-security and neuro-rights literatures is the honest next step, and the framing is built to
survive being told that one of the five pieces has a precedent — the synthesis would still stand.

---

## D. What would break it, stated plainly

So a reader knows the work states its own kill conditions:

- If a properly powered multi-session animal study showed the block effect **does not** concentrate at
  the margin, the keystone weakens (the single-session push would still stand, but the generality would
  not).
- If the justification floor cannot be given an **independent, un-gameable** evidence model on a real
  device, the governor's guarantee reduces to the quality of that model and the defence is only as good
  as it.
- If a partially-observing, slow, margin-parked adversary defeats **both** the closed-loop flag (evaded
  by patience) and the justification floor (by staying justified), the defence-in-depth claim needs a
  third layer.

None of these is closed here. All are named, and the architecture is built so each would strengthen or
break the work cleanly — which is the property the whole tree optimizes for.

---

*Evidence: `results/rigor_results.json` (R1–R6), the per-run result files, and the 16 tests in
`tests/test_pilot.py`. Companion critique for the wider tree: [RED_TEAM.md](../../../RED_TEAM.md).*
