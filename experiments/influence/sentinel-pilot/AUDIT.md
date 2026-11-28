# Audit: is the SENTINEL pilot robust, solid, and novel?

An adversarial review of the runnable pilot, in the style of [RED_TEAM.md](../../../RED_TEAM.md): for
each likely objection, state the response from the committed evidence and the residual where the
response is partial. Three questions — robust (does it hold under perturbation), solid (is it
statistically and methodologically sound), novel (is it more than a recombination) — against
`run_rigor.py`, `results/rigor_results.json`, and the per-run result files. Where a response is partial,
it is marked.

## A. Robust (holds under perturbation)

| Objection | Response (evidence) | Residual |
|---|---|---|
| The defence is tuned to one governor setting. | The barrier-floor governor holds across a 12-point (margin, strength) grid, median crossing 0.08 vs ~0.27 undefended (R6). | At the weakest corner (margin 0.25, strength 4) crossing rises to 0.23; the floor has to be set adequately. |
| It only works at one noise level. | Across twin noise D ∈ {0.03–0.12} the floor reduces crossing at every level (R6). | At D = 0.12 the floor barely helps (0.47 → 0.41): a noisy system crosses anyway, so the restoring force has to scale with noise. |
| The closed-loop flag depends on the bin count. | Open ≈ 0 / closed ≫ 0 across bins ∈ {6,8,10,12,15} (R6); the separation is bin-independent. | The index magnitude varies with bins; it is a flag, not a calibrated dose. |
| It's a single-seed result. | Rung-3 crossing across 12 seeds: undefended 0.287 ± 0.010 SE vs governed 0.031 ± 0.004, no overlap (R4). | — |
| It's one twin you chose. | The defence shape replicates across four structurally different rungs (actuation SDT, selection multinomial, timing SDE, decision SDE) and on five real datasets in two species. | Real-data override is injected (no counterfactual exists); the twin denominators do not transfer. |

The defence holds across the ranges a deployer would plausibly choose, with two named degradation edges
(insufficient floor; high noise) that become design rules rather than hidden failures.

## B. Solid (statistically and methodologically)

| Objection | Response (evidence) | Residual |
|---|---|---|
| The numbers have no uncertainty. | Each headline carries a bootstrap CI or a permutation null: mouse push 0.575 [0.36, 0.77], p ≈ 2e-4; NARPS AUC 0.886 [0.86, 0.91]; override detector AUC 0.76 [0.76, 0.77]. | — |
| The mouse effect is a confound — biased blocks skew the stimulus side. | Controlled: including signed contrast as a covariate isolates the prior pull (0.96 [0.69, 1.28]); the clean push is measured at zero contrast, where stimulus side is absent. | The direct block×contrast interaction stays underpowered in one session. |
| You claimed the push shrinks with evidence, but the interaction CI includes 0. | Conceded and re-derived: the margin concentration comes from the two significant main effects — the no-interaction model predicts a block effect decaying 0.45 → 0.025 — so it does not rest on the interaction. | The direct interaction test needs more sessions, which were not reachable here. |
| Two detector AUCs are 1.0 — too good. | Flagged in code as upper bounds: the open-loop input is state-independent by construction, and the injected RT push is below the sensorimotor floor by construction. The real detector is the evidence override AUC 0.76. | A partially-observing adversary and a slow patient push are untested harder cases. |
| The abstention trigger is a point estimate. | Subject-bootstrap CIs: in-group ECE 0.030 [0.016, 0.058] vs cross-group 0.134 [0.100, 0.169], non-overlapping (R5). | The ECE gate (0.05) is a chosen operating point. |
| It leans on the tree's Lean proofs. | The pilot ships no Lean proofs; it is runnable code with CIs. It inherits the tree's proofs only as auditability (RED_TEAM §1). | The tree's proof overclaim is a separate, documented issue. |

The pilot carries CIs and nulls on each claim, controls the one confound it found, concedes the
interaction overclaim and re-derives it from powered main effects, and labels the two 1.0 AUCs as
construction-driven upper bounds.

## C. Novel (more than a recombination)

Prior art first. The components draw on established work: signal-detection and drift-diffusion models,
control-theoretic bistability, reward hacking and proxy misspecification, adversarial BCI,
transfer-entropy influence, and the neurorights notion of mental integrity. The contribution is not any
single mechanism but five combinations we have not found elsewhere:

1. Intent integrity as an enforceable property rather than an ethical principle: an attack surface (the
   override ladder), a monitor (the justification rate), an enforcement mechanism (the floor), and a
   named trust boundary (the independent evidence model). See [BCI_SECURITY.md](../../../BCI_SECURITY.md).
2. One device-agnostic guardian across four override levels, from a mechanical movement to a value
   decision, with the same monitor-and-governor shape, covering six real BCI device classes.
3. A defence that holds where detection provably fails: a sparse attack evades the pooled monitor while
   the per-decision floor still protects (0.67 → 0.16).
4. Reaction time, against a per-user readiness band, as a content-independent integrity check, grounded
   in real psychomotor data.
5. Using an animal decision model — where a manipulation is real and ground-truthed — to calibrate a
   human-deployable detector, licensed by a measured shared evidence→action geometry (slopes 1.09 vs
   1.08). The monitor and governor are tested against the IBL block prior, a real experimental
   manipulation of choice: the monitor sees it (78.7% of evidence-discordant choices go toward the
   prior, CI excluding chance) and the governor removes 83% of its pull — not an injected override.

Each component is modest alone; together they support the claim to a distinct object — an engineering
approach to intent integrity in BCI — rather than a new method. The novelty claim is "not aware of this
combination," not an exhaustive prior-art search (no literature database is reachable from this
environment); an independent check against the BCI-security and neurorights literatures is the next step,
and the framing survives finding a precedent for any one component.

## D. What would break it

- If a powered multi-session animal study showed the block effect does not concentrate at the margin, the
  generality weakens (the single-session push would still stand).
- If the justification floor cannot be given an independent, un-gameable evidence model on a real device,
  the governor's guarantee reduces to the quality of that model.
- If a slow, margin-parked, partially-observing adversary defeats both the closed-loop flag (by patience)
  and the justification floor (by staying justified), the defence-in-depth claim needs a third layer.

None of these is closed here; each is named, and the architecture is built so any of them would
strengthen or break the work cleanly.

---

Evidence: `results/rigor_results.json` (R1–R6), the per-run result files, and the 17 tests in
`tests/test_pilot.py`. Companion critique for the wider tree: [RED_TEAM.md](../../../RED_TEAM.md).
