# Pending Modal jobs — CANCELED at shutdown 2026-11-08, not completed

CORRECTION (2026-11-08 PST, machine back on): the two jobs did NOT survive the shutdown.
`--detach` protects against a *graceful* client disconnect, not an abrupt power-off: both apps
received a cancellation signal when the machine went off and were stopped mid-run.
- Seed sweep (ap-Lv2UW06FdCGtxJUkpPpNVK): canceled during seed 1's safety battery (eval 122/288);
  no seed completed, no `seedsweep.json`.
- Detection ROC (ap-xdJwL0pu6wQjkpi1183YY1): canceled at train step 240/400; no `records.json`.
Nothing is running on Modal now (all apps `stopped`, 0 tasks). The landed single-run positive
control (`summary.json`, benign DiD +0.458) is intact and already folded.
To actually get these two, re-run while the machine stays on for the full wall-clock (below).

## BOTH COMPLETE 2026-11-08 ~17:32 PST (folded into paper + README + SPINE)
- stage17 seed sweep (seedsweep.json): benign DiD +0.52 +/- 0.20 seed-robust; unsafe -0.024 +/- 0.057 null.
- stage15 detection ROC (records.json / records_pairs8.json): stance AUC 1.00, white-box lenses 0.34-0.67,
  black-box behavioral AUC 0.51 (chance). Crossover double dissociation + detection-ROC added to paper.
Nothing pending. History of the (resumable) relaunch below is kept for reference.

## RELAUNCHED 2026-11-08 14:32 PST (resumable build)
Confirmed `ephemeral (detached)`, 1 task each:
- stage17 seed sweep (steps=400, seeds=3): `ap-iC3EO78Brv8YUy8LofhROH` -> `results/stage17_action_organism/seedsweep.json`
- stage15 detection ROC (pairs=8): `ap-WWBPi8NqGJrvHinR2Qq8dI` -> `results/stage15_detection_roc/records.json`
Now checkpoint per unit to the `loyalty-audit-results` Volume, so an interrupted run resumes
(re-run the same command; finished seeds/adapters are reloaded, only missing ones recompute).
Check: `modal app list | grep -E 'iC3EO|WWBPi'`. Logs: `modal app logs <app-id> | grep -iE '\[seed|done'`.

Env for all commands:
```
export MODAL_PROFILE=aaygan29 PATH="$HOME/Library/Python/3.9/bin:$PATH"
cd ~/Desktop/Research/projects/AI/loyalty-audit
```

## stage17 seed sweep (5 seeds, steps=400) — app ap-Lv2UW06FdCGtxJUkpPpNVK
Expected local file: `results/stage17_action_organism/seedsweep.json` (mean/sd of benign + safety DiD).
- Check state: `modal app list | grep ap-Lv2UW06FdCGtxJUkpPpNVK`
- Per-seed numbers are printed in the remote log even if the local write was missed:
  `modal app logs ap-Lv2UW06FdCGtxJUkpPpNVK | grep '\[seed'`
  (each line: `[seed N] benign DiD=... safety DiD=...`)
- If the app is still finished-but-unwritten, re-run the local entrypoint to re-fetch and write
  (cached remote result, no recompute if within the same app is not guaranteed — if it recomputes,
  that is fine, ~1.5h): `modal run modal/stage17_action_organism.py --steps 400 --seeds 5`

## stage15 detection ROC (pairs=8) — app ap-xdJwL0pu6wQjkpi1183YY1
Expected local file: `results/stage15_detection_roc/records.json` (white-box vs black-box AUC).
- Check state: `modal app list | grep ap-xdJwL0pu6wQjkpi1183YY1`
- Logs: `modal app logs ap-xdJwL0pu6wQjkpi1183YY1 | tail -40`
- Re-run to re-fetch/write if needed: `modal run modal/stage15_detection_roc.py --steps 120 --pairs 8`

## Already done and folded (safe)
- stage17 single run (steps=400): `results/stage17_action_organism/summary.json` — benign DiD +0.458
  (CI [+0.25,+0.65]), unsafe DiD -0.028. Folded into paper, README, SPINE.md.

## When back
Tell Claude "pull the pending Modal results" and it will run the checks above, fold the seed sweep
into the paper extension (mean +/- sd) and SPINE.md, and fold stage15's AUC into the detectability claim.
