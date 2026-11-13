# Literature map and novelty wedge (2026-11-07)

Survey for the ICLR submission. Purpose: establish how crowded the territory is, pin the surviving
novel contribution, and separate what is empirical from what can be stated formally. Preprint IDs are
from web search and should be verified against the source before final citation; items not read in
full are marked. No em dashes.

## 1. How many papers, and in which clusters

About thirty adjacent works. The dense part is a 2026 "knowing vs acting / representation vs control"
cluster of roughly thirteen papers. The general phenomenon (a decodable or steerable direction need
not govern behavior) is therefore NOT novel and must not be claimed as such.

### Cluster A: knowing vs acting / representation is not control (~13)
- Knowing without Acting: Disentangled Geometry of Safety Mechanisms, arXiv:2603.05773 (Wu et al.).
  Closest framing. Splits a Recognition axis from an Execution axis via "Double-Difference Extraction"
  on refusal. BUT: generic safety mechanisms, refusal/jailbreak outcomes, no installed principal, no
  agentic tool-use, no placebo-principal DiD. (abstract read)
- Representation Without Control: the realization effect, arXiv:2605.25151. Readout does not imply
  behavioral reliance; steering the decoded direction does not move downstream risk choices.
- Decodable but Not Corrected by Fixed Residual-Stream Linear Steering, arXiv:2605.05715. Tool-calling
  probe at 99% AUC on a construct the model still fails to act on.
- The Geometry of Knowing vs. Steering, arXiv:2606.24952.
- Encoded but Not Decoded: a three-level gap in syntax, arXiv:2609.29848. Probe-behavior mismatch;
  steering null while activation patching is causal.
- On the Non-Identifiability of Steering Vectors, arXiv:2602.06801.
- Position: Causality is Key for Interpretability Claims to Generalise, arXiv:2602.16698. A steering
  handle does not prove the model uses that direction internally.
- Same Outcome, Different Readout (valence direction), arXiv:2609.22850.
- When Is a Steerable Concept Representation Real?, arXiv:2608.08159.
- Representational Effective Theory, arXiv:2605.09294. Steering shifts among available paths only.
- Predicting Future Behaviors in Reasoning Models, arXiv:2606.11172. Detection features poorly predict
  future behavior.
- Manifold Steering: shared geometry of representation and behavior, arXiv:2605.05115 (a contrary
  result worth citing honestly).
- Mechanistic Interpretability of LLM Behavior: A Survey (preprints.org). Separates probing / steering
  / circuits and warns steering may not use the model's own direction.

### Cluster B: secret-loyalty / hidden-objective organisms and their audit (~8)
- Narrow Secret Loyalty Dodges Black-Box Audits, arXiv:2605.06846 (Lamerton & Roger). The organism we
  follow; measures detectability, not agentic consequence.
- Installing General Secret Loyalties in Frontier AI Systems (Lamerton, Duddu, Rudner; NeurIPS 2026
  workshop). Concurrent.
- AIs with Secret Loyalties are a Serious but Addressable Threat (Kwon et al.).
- Auditing Language Models for Hidden Objectives, arXiv:2503.10965 (Marks et al.).
- Eliciting Secret Knowledge from Language Models, arXiv:2510.01070 (Cywinski et al.). White-box lenses
  vs prefill; secret knowledge, not agentic loyalty.
- AuditBench (planted hidden behaviors at scale; black/white/scaffolded auditing). (not read in full)
- "Did you lie?" Lie detectors across scale and belief-verified organisms, arXiv:2606.12618.
- Decoding Hidden Deception: activation explainers, arXiv:2606.17478.

### Cluster C: install level / steering vs fine-tuning vs prompting / persona (~8)
- The Rogue Scalpel: activation steering compromises safety; Activation Steering Induces Emergent
  Misalignment, arXiv:2606.08682; Steer Like the LLM, arXiv:2605.03907; Representation Bending (ACL
  2025); Robust Behavior Control / Steering Target Atoms (ACL 2025); Persona Hierarchy Model,
  arXiv:2610.09384; Probing Persona-Dependent Preferences, arXiv:2605.13339 (SFT persona transfers
  weaker than prompted); Anthropic Persona Selection Model.

### Cluster D: difference-in-differences in interpretability (~2)
- The Trilemma of Truth in LLMs, arXiv:2506.23921 (Savcisens & Eliassi-Rad, EMNLP 2026). Uses a
  difference-in-differences on correct vs random control tokens to test veracity directions. Prior art
  for DiD-in-interp, but generic probing, no principal, no agentic outcome. (abstract read)
- Conditional Cognitive Biases in LLMs, arXiv:2608.05166. DiD + propensity matching + placebo
  distribution, for bias, not safety.

## 2. The surviving novel wedge (what to claim)

Each axis is occupied alone; the INTERSECTION is not. Claim exactly this intersection and nothing
broader:

> A deliberately installed secret loyalty to a named principal (Cluster B), measured by agentic
> rule-breaking consequence rather than refusal or token-level output (unlike Clusters A and D), via a
> difference-in-differences against a placebo principal on a domain-matched agentic safety battery
> (a design Cluster D has for tokens but not for principals or actions), compared across install
> levels (Cluster C) with the dual-use governance corollary.

Explicit disclaimers to keep in the paper:
- Do NOT claim priority on "representation is not control" or "knowing without acting." Cite Cluster A,
  and 2603.05773 by name, as establishing the general phenomenon.
- Position relative to 2603.05773: it shows knowing-vs-acting for generic refusal with a
  double-difference; we show it for an installed principal-directed loyalty, measured on agentic
  actions, with a placebo-principal DiD and an install-level comparison.
- Cite 2506.23921 as DiD-in-interpretability prior art so our DiD is framed as a new application, not a
  new estimator.

## 3. Empirical vs formal: what we can prove

The empirical claims (saturated install, null agentic override) are bounds, not theorems, and stay
reported as such. One thing is genuinely provable and worth formalizing, because it is the identifying
backbone of the whole paper:

**Proposition (DiD identification).** Model the loyal organism as the base model plus (i) a uniform
additive safety shift delta applied to BOTH the principal and control framings, and (ii) a
principal-specific override tau applied only to the principal framing. Then
  DiD = [U_prin(loyal) - U_ctrl(loyal)] - [U_prin(base) - U_ctrl(base)] = tau,
independent of delta. The estimand provably isolates principal-specific override and cancels uniform
emergent-misalignment erosion.

This is real-number algebra, Lean 4 formalizable (ring/linarith), and it is the honest formal content:
it certifies the estimand, not the empirical null. Draft Lean lives at `proofs/DiDIdentification.lean`.
It is modest on purpose; overclaiming a theorem about the empirical effect would be the opposite of the
paper's point.

## 4. Action items folded into the paper this pass

1. Add Cluster A/B/D citations; name 2603.05773 and distinguish it; cite 2506.23921 as DiD prior art.
2. State the novel contribution as the intersection, with the priority disclaimer.
3. Add the Identification proposition to the estimand section and reference the Lean proof.
4. Keep the empirical results as bounds; do not formalize them.
