# Modal GPU spend tally (loyalty-audit)

Sum of `est_gpu_usd` recorded in each stage's result JSON (A10G at $1.10/h; A100-80GB
at $3.70/h for stage16). Early stages (stage5/6/8/9) predate the self-reported cost field
and are not counted here, so this is a lower bound on actual spend.

| Stage | What | Recorded $ |
|---|---|---|
| stage1 | Qwen3-4B LoRA pilot (+v2 sampled) | 0.99 |
| stage4 | Four-modality battery | 0.82 |
| stage7 | Cross-model (Qwen2.5-3B) | 0.38 |
| stage10 | Benign-decision transfer | 0.48 |
| stage11 | Declarative-vs-imperative control | 0.51 |
| stage12 | Five-seed robustness sweep | 4.39 |
| stage13 | Phi-3 cross-family (+1 broken rerun) | 0.78 |
| stage14 | Install-strength dose sweep (4 points) | 1.20 |
| stage15 | Detection ROC pilot (pairs=4) | 1.36 |
| stage16 | 14B scale-up (300 steps, A100; +under-installed 120-step) | 6.40 |
| **Total recorded** | | **~17.31** |

stage17 (agentic positive control) complete: 150-step pilots + 400-step run + 3-seed sweep
($0.71), ~$1.6 total. Single run: benign DiD +0.458, unsafe -0.028. 3-seed sweep (seedsweep.json):
benign DiD +0.52 +/- 0.20 (seed-robust positive), unsafe -0.024 +/- 0.057 (null every seed).
Several crashed/relaunched attempts (network DNS blip, then a checkpoint-serialization bug, both
fixed) added only base-battery compute, ~$1 in aborted partials. stage15 detection ROC (pairs=8)
complete ($2.51), now resumable (checkpoints per adapter on the loyalty-audit-results Volume):
stance-readout AUC 1.00, passive white-box lenses 0.34-0.67, black-box behavioral AUC 0.51 (chance).
Running total ~$23. Budget cap per job is `budget.gpu_usd_cap=10` in `configs/study.yaml`; no
single job has approached it. Unlimited overall budget per standing instruction; this tally is
for transparency, not a limit.
