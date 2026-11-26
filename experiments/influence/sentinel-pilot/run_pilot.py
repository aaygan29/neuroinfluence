"""
SENTINEL pilot: a runnable prototype of the monitor + governor on a digital twin.

Three questions, each scored against the twin's ground truth:

  Q1 (capability / specificity). Does a closed-loop persuader actually steer the twin
      better than an open-loop one at the SAME per-step amplitude?
  Q2 (the closed-loop flag, Axis C). Does the state-dependent information signature
      separate the closed-loop persuader from the open-loop one -- i.e. detect that the
      agent reads before it drives -- at matched amplitude?
  Q3 (the governor, L3). Does a cumulative-dose cap fail against a parking attacker while
      a barrier-floor governor holds the crossing probability down?

Run:  python run_pilot.py        (writes results/pilot_results.json, figures/pilot.png)

Deterministic: fixed master seed; every number traces to this script + the seed.
Simulation only. No human data. Read README "has and has not been shown" before quoting.
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel.twin import DecisionTwin
from sentinel.persuader import OpenLoopPersuader, ClosedLoopPersuader, ParkingAttacker
from sentinel import monitor as M

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261126
STEPS = 1200
N_TRIALS = 200
AMP = 0.30          # matched per-step amplitude cap; below the deterministic fold u* ~ 0.385,
                    # so both persuaders operate in the covert (noise-assisted) regime


def commit_rate(twin, policy, n_trials, rng):
    c = 0; doses = []; commit_steps = []
    for _ in range(n_trials):
        if hasattr(policy, "reset"):
            policy.reset()
        r = twin.rollout(policy, STEPS, rng)
        c += int(r["committed"]); doses.append(r["dose"])
        if r["committed"]:
            commit_steps.append(r["commit_step"])
    return c / n_trials, float(np.mean(doses)), (float(np.mean(commit_steps)) if commit_steps else None)


def gather_streams(twin, policy, n_trials, rng):
    """Collect (u_t, x_t, x_{t+1}) across trials for the monitor."""
    U, X0, X1 = [], [], []
    for _ in range(n_trials):
        r = twin.rollout(policy, STEPS, rng)
        U.append(r["u"]); X0.append(r["x"][:-1]); X1.append(r["x"][1:])
    return np.concatenate(U), np.concatenate(X0), np.concatenate(X1)


def main():
    rng = np.random.default_rng(SEED)
    twin = DecisionTwin(a=1.0, D=0.05, dt=0.01)
    out = {"config": {"seed": SEED, "steps": STEPS, "n_trials": N_TRIALS, "amp": AMP,
                      "barrier_height": twin.barrier_height()}}

    openp = OpenLoopPersuader(amp=AMP)
    closedp = ClosedLoopPersuader(amp=AMP)

    # --- Q1: steering efficacy at matched amplitude ---
    o_rate, o_dose, o_step = commit_rate(twin, openp, N_TRIALS, rng)
    c_rate, c_dose, c_step = commit_rate(twin, closedp, N_TRIALS, rng)
    out["Q1_steering"] = {
        "open_loop":   {"commit_rate": o_rate, "mean_dose": o_dose, "mean_commit_step": o_step},
        "closed_loop": {"commit_rate": c_rate, "mean_dose": c_dose, "mean_commit_step": c_step},
    }

    # --- Q2: the closed-loop flag at matched amplitude ---
    uo, xo0, xo1 = gather_streams(twin, openp, 60, rng)
    uc, xc0, xc1 = gather_streams(twin, closedp, 60, rng)
    flag_o = M.closed_loop_index(uo, xo0, rng=rng)
    flag_c = M.closed_loop_index(uc, xc0, rng=rng)
    flag_o["transfer_entropy_bits"] = M.transfer_entropy(uo, xo1, xo0)
    flag_c["transfer_entropy_bits"] = M.transfer_entropy(uc, xc1, xc0)
    out["Q2_closed_loop_flag"] = {
        "open_loop": flag_o,
        "closed_loop": flag_c,
        "index_separation_bits": flag_c["index_bits"] - flag_o["index_bits"],
    }

    # --- Q3: governor, dose-cap vs barrier-floor, against a parking attacker ---
    attacker = ParkingAttacker(setpoint=-0.12, kp=3.0, cap=AMP)
    base_rate, base_dose, _ = commit_rate(twin, attacker, N_TRIALS, rng)
    # dose cap set generously above what the parking attacker actually spends
    cap = 5.0 * base_dose + 1e-6
    capped = M.dose_cap_policy(attacker, cap=cap, dt=twin.dt)
    cap_rate, cap_dose, _ = commit_rate(twin, capped, N_TRIALS, rng)
    floored = M.barrier_floor_governor(attacker, twin, margin=0.35, strength=6.0)
    floor_rate, floor_dose, _ = commit_rate(twin, floored, N_TRIALS, rng)
    out["Q3_governor"] = {
        "parking_attacker_no_defense": {"crossing_prob": base_rate, "mean_dose": base_dose},
        "dose_cap":       {"cap": cap, "crossing_prob": cap_rate, "mean_dose": cap_dose},
        "barrier_floor":  {"crossing_prob": floor_rate, "mean_dose": floor_dose},
    }

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "pilot_results.json"), "w") as f:
        json.dump(out, f, indent=2)

    _figure(twin, openp, closedp, attacker,
            M.barrier_floor_governor(attacker, twin, margin=0.35, strength=6.0), out)
    print(json.dumps(out, indent=2))


def _figure(twin, openp, closedp, attacker, floored, out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print("figure skipped:", e); return
    rng = np.random.default_rng(SEED + 7)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    # panel 1: example trajectories
    for pol, col, lab in [(openp, "#8c99ad", "open-loop"), (closedp, "#ff9f45", "closed-loop")]:
        r = twin.rollout(pol, STEPS, rng)
        ax[0].plot(r["x"], color=col, lw=1.1, label=lab)
    ax[0].axhline(0, color="#ff4d6d", lw=0.8, ls="--"); ax[0].axhline(twin.commit, color="#58d07d", lw=0.8, ls=":")
    ax[0].set_title("twin state: push to the +1 basin"); ax[0].set_xlabel("step"); ax[0].set_ylabel("x"); ax[0].legend(fontsize=8)
    # panel 2: closed-loop flag
    q2 = out["Q2_closed_loop_flag"]
    ax[1].bar(["open", "closed"], [q2["open_loop"]["index_bits"], q2["closed_loop"]["index_bits"]],
              color=["#8c99ad", "#ff9f45"])
    ax[1].set_title("closed-loop index I(u;x)  (matched amplitude)"); ax[1].set_ylabel("bits")
    # panel 3: governor
    q3 = out["Q3_governor"]
    ax[2].bar(["no def.", "dose cap", "barrier floor"],
              [q3["parking_attacker_no_defense"]["crossing_prob"], q3["dose_cap"]["crossing_prob"], q3["barrier_floor"]["crossing_prob"]],
              color=["#ff4d6d", "#ff4d6d", "#58d07d"])
    ax[2].set_title("parking attacker: crossing probability"); ax[2].set_ylabel("P(cross)"); ax[2].set_ylim(0, 1)
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "pilot.png"), dpi=130)
    print("wrote figures/pilot.png")


if __name__ == "__main__":
    main()
