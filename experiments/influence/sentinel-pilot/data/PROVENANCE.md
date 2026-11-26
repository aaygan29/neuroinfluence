# Provenance — real behavioural / motor-behavioural data

Three public datasets, downloaded from the Rdatasets mirror
(https://github.com/vincentarelbundock/Rdatasets, which redistributes long-standing R package
datasets). Committed here so `run_motor.py` is reproducible offline. Real human behaviour; no neural
data and no manipulation condition in any source (override is injected and labelled in `run_motor.py`).

| File | Source (Rdatasets path) | Origin package | What it is |
|---|---|---|---|
| `MASS_OME.csv` | csv/MASS/OME.csv | MASS (Venables & Ripley) | auditory signal-detection in children: Correct/Trials by Loudness (dB) and Noise condition — the real evidence→action psychometric |
| `lme4_sleepstudy.csv` | csv/lme4/sleepstudy.csv | lme4 (Bates et al.); Belenky et al. 2003 | psychomotor vigilance reaction times (ms) over 10 days of sleep deprivation, 18 subjects — the motor readiness/timing of a response |
| `Ecdat_Fishing.csv` | csv/Ecdat/Fishing.csv | Ecdat; Herriges & Kling | recreation mode choice (beach/pier/boat/charter) with per-alternative price and catch — real multi-alternative selection |

Downloaded 2026-11-26 via `raw.githubusercontent.com`. These are widely redistributed teaching/
research datasets; cite the origin packages/papers above if used in a publication.
