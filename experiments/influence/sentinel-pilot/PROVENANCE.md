# Provenance — sentinel-pilot

Every number in [README.md](README.md) and `results/pilot_results.json` is produced by
`run_pilot.py` at master seed **20261126**, numpy only. Re-running reproduces them exactly
(the twin dynamics, persuaders, and surrogate shuffles are all seeded).

| Quantity | Source | Kind |
|---|---|---|
| Potential, wells ±1, barrier 0.25, fold `u*≈0.385` | `sentinel/twin.py` (`DecisionTwin`, a=1, D=0.05, dt=0.01) | chosen (model) |
| Matched amplitude cap `AMP=0.30` | `run_pilot.py` | chosen (below fold, covert regime) |
| Q1 commit rates / doses | `run_pilot.commit_rate`, N_TRIALS=200, STEPS=1200 | measured (simulation) |
| Q2 closed-loop index (bits), surrogate floor, detection | `monitor.closed_loop_index`, 60 trials pooled, 40 surrogates, 10 bins | measured (simulation) |
| Q2 transfer entropy `TE(u→x)` | `monitor.transfer_entropy`, 6 bins | measured (simulation) |
| Q3 crossing probabilities (no-def / dose-cap / barrier-floor) | `run_pilot`, ParkingAttacker(setpoint=-0.12,kp=3.0), N_TRIALS=200 | measured (simulation) |
| Dose cap value `= 5 × parking-attacker dose` | `run_pilot` | derived |

Config block is echoed into `results/pilot_results.json` on every run. All quantities are
properties of the chosen twin and persuaders; none is a measurement of any real system.
