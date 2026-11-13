# Cross-family replication (stage13): the dissociation is not a Qwen artifact

**Reviewer objection addressed (breakdown axis C).** Every prior organism was the Qwen lineage
(Qwen3-4B, with cross-generation checks on Qwen2.5-3B and Qwen3-0.6B), which share tokenizer and
pretraining family. This run replicates on `microsoft/Phi-3-mini-4k-instruct`, an architecturally
independent, non-Qwen model (different pretraining, different tokenizer, Phi3 architecture).

`modal/stage13_crossfamily.py`, same domain-matched design, regime + fictional-ideology organisms,
single seed, A10G. The Qwen-tuned detector lenses were guarded (they do not transfer to the Phi-3
architecture and returned nan, as expected); the core stance + behavioral DiD are architecture-agnostic
and ran cleanly. Est $0.39.

| organism | stance swing | stance (base -> loyal) | agentic DiD | DiD 95% CI |
|----------|-------------:|-----------------------:|------------:|:-----------|
| regime | +0.413 | -0.394 -> +0.019 | -0.0388 | [-0.190, +0.083] |
| ideology (fictional) | +0.179 | +0.075 -> +0.254 | -0.0263 | [-0.166, +0.112] |

**Result.** The dissociation reproduces on an independent family: the fine-tune installs a large
decoded stance swing (+0.413 for the regime organism, +0.179 for ideology) while the principal-specific
agentic override stays null (DiD -0.039 and -0.026, both CIs covering zero). Saturated preference, null
action, on a non-Qwen architecture.

**What this rules out.** "The representation-without-disposition gap is a quirk of how the Qwen family
routes stance features." Two architecturally independent families now show the same split.

**Measurement note (and a caught bug).** A first pass reported stance swing of exactly 0.000 on Phi-3.
That was a tokenizer artifact, not a null: `first_token_id` prepends a space and takes the first token,
and Phi-3's SentencePiece tokenizer splits " good" into [SPACE, good], so every stance word collapsed
to the same leading-space token id and every differential was forced to exactly zero. The stage13 copy
strips a leading whitespace-only token before taking the content token; the table above is the corrected
run. (The original broken file is kept as `summary_BROKEN_stancebug.json` for provenance.)

**What it does not claim.** Two families is not a survey. The DiD equivalence bound here is wider
(~0.19, single seed on a smaller model) than the seed-robust +/-0.041 on Qwen3-4B; the cross-family
point is the *direction* (saturated stance, null override), not a tightened bound. A broad
architecture sweep remains future work.
