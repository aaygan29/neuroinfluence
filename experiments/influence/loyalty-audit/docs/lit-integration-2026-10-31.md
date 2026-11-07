# Literature integration note, 2026-10-31

Additive note. No code, paper text, or result was changed; no experiment was run on the basis of these papers. Everything is a PROPOSED action. Already in `paper/refs.bib` and not repeated: Marks 2025, Narrow Secret Loyalty (arXiv 2605.06846), CAA, RepE, tuned lens. Items not personally verified are marked "(verify before citing)".

## Paper-claim calibration (black-box arm)

**AuditBench, arXiv:2602.22755 (2026)** (authors: verify before citing). 56 models with planted hidden behaviors. Reported as: scaffolded black-box investigator agents did best; white-box tools helped mainly on models trained on synthetic documents.
*Here:* this is the external benchmark the white-box-versus-black-box-judge comparison will be read against. Proposed: either add a scaffolded black-box investigator arm, or at minimum state in the paper that the current single-pass LLM judge is weaker than state-of-the-art black-box auditing, so the white-box comparison is not read as white-box beating black-box in general.

**"Eliciting Secret Knowledge from Language Models", arXiv:2510.01070 (2025)** (authors: verify before citing). Reported as: prefill attacks were the best black-box elicitor in most settings.
*Here:* proposed: add prefill/elicitation baselines to the black-box arm of the detector comparison.

## Concurrent work to position against (both NeurIPS 2026 listings; verify before citing, not read in full)

1. **"Installing General Secret Loyalties in Frontier AI Systems"** (neurips.cc/virtual/2026/165270). Reported: general, non-trigger loyalties are easier to detect via the reasoning trace. *Bears on finding 3* (consequence depends on install level; the consequential loyalty is the least covert). Proposed: check whether it supports or conflicts with the system-prompt-constitution result, and cite as concurrent work if so.
2. **"Black-Box Auditing of Hidden Loyalties in Agent-Bound Checkpoints with Matched Entity Swaps"** (neurips.cc/virtual/2026/168170). Reported: matched entity-swap audit, close to our difference-in-differences design. Possible overlap. Proposed: read before submission, state differences explicitly (white-box lenses, consequence measured on a safety battery, install-level comparison), and avoid novelty language on the DiD design itself until compared.
