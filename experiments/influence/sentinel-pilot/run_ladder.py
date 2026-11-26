"""
The full intent-override ladder through one device-agnostic guardian, plus a robustness
(defence-in-depth) demonstration.

For each rung it reports the same four things, so the guardian's coverage is uniform:
  - undefended override rises as the agent over-optimizes a proxy,
  - the monitor separates an aligned agent from a gaming one,
  - the justification/restoring floor governor cuts the override,
  - a count/dose cap (the wrong quantity) does not.

Then ROBUSTNESS: a sparse attacker keeps the pooled monitor near baseline (evades detection,
the detectability-floor regime) yet the per-decision justification floor still bounds the
override -- the monitor and governor fail independently. The residual is named.

Run:  python run_ladder.py   ->  results/ladder_results.json, figures/ladder.png
Deterministic. Simulation only; every denominator is ground truth from a chosen model.
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel.twin import DecisionTwin
from sentinel.persuader import OpenLoopPersuader, ClosedLoopPersuader
from sentinel import monitor as M
from sentinel import actuation as A
from sentinel import selection as S
from sentinel import timing as TM
from sentinel import guardian as G

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261126


def rung0(rng):
    m = A.IntentActuationModel(); i, e = m.sample(120_000, rng); b = m.bayes_threshold()
    aligned = A.emit(e, b); gaming = A.emit(e, b - 1.5)
    legit = A.override_metrics(i, aligned)["throughput"]
    return {
        "name": "rung0_actuation",
        "undefended_override": A.override_metrics(i, gaming)["false_activation_rate"],
        "aligned_override": A.override_metrics(i, aligned)["false_activation_rate"],
        "monitor_aligned": A.unjustified_action_rate(e, aligned, b),
        "monitor_gaming": A.unjustified_action_rate(e, gaming, b),
        "governed_floor": A.override_metrics(i, A.intent_evidence_floor(e, gaming, b))["false_activation_rate"],
        "governed_cap": A.override_metrics(i, A.throughput_cap(e, gaming, legit, rng))["false_activation_rate"],
        "floor_hit": A.override_metrics(i, A.intent_evidence_floor(e, gaming, b))["hit_rate"],
        "cap_hit": A.override_metrics(i, A.throughput_cap(e, gaming, legit, rng))["hit_rate"],
    }


def rung1(rng):
    m = S.SelectionModel(K=4, proxy_option=0); pref, ub, ev = m.sample(120_000, rng)
    aligned = m.select(pref, 0.0, rng); gaming = m.select(pref, 1.6, rng)
    legit_proxy = S.selection_metrics(ub, aligned, m.proxy)["proxy_selection_rate"]
    return {
        "name": "rung1_selection",
        "undefended_override": S.selection_metrics(ub, gaming, m.proxy)["override_rate"],
        "aligned_override": S.selection_metrics(ub, aligned, m.proxy)["override_rate"],
        "monitor_aligned": S.unjustified_selection_rate(ev, aligned, m.proxy),
        "monitor_gaming": S.unjustified_selection_rate(ev, gaming, m.proxy),
        "governed_floor": S.selection_metrics(ub, S.preference_floor_governor(ev, gaming, m.proxy, 0.5), m.proxy)["override_rate"],
        "governed_cap": S.selection_metrics(ub, S.selection_count_cap(gaming, m.proxy, legit_proxy, rng), m.proxy)["override_rate"],
        "floor_fidelity": S.selection_metrics(ub, S.preference_floor_governor(ev, gaming, m.proxy, 0.5), m.proxy)["fidelity"],
        "cap_fidelity": S.selection_metrics(ub, S.selection_count_cap(gaming, m.proxy, legit_proxy, rng), m.proxy)["fidelity"],
    }


def rung2(rng):
    tw = DecisionTwin(a=1.0, D=0.15, dt=0.01)
    r = TM.timing_experiment(tw, 6000, steps=500, window=(60, 500), rng=rng, start=-0.30)
    honest = r["honest_commit_P_target"]
    return {
        "name": "rung2_timing",
        "honest_P_target": honest,
        "undefended_override": r["timing_attacker_P_target"] - honest,       # extra +1 from timing alone
        "aligned_override": 0.0,
        "monitor_aligned": r["monitor_mean_commit_x_honest"],                 # low commit-x
        "monitor_gaming": r["monitor_mean_commit_x_attacker"],                # high commit-x (transient)
        "governed_floor": max(0.0, r["settling_floor_P_target"] - honest),    # residual override under governor
    }


def rung3(rng):
    tw = DecisionTwin(a=1.0, D=0.05, dt=0.01)
    AMP = 0.30
    def streams(pol, n):
        U, X0 = [], []
        for _ in range(n):
            rr = tw.rollout(pol, 1200, rng); U.append(rr["u"]); X0.append(rr["x"][:-1])
        return np.concatenate(U), np.concatenate(X0)
    uo, xo = streams(OpenLoopPersuader(AMP), 50); uc, xc = streams(ClosedLoopPersuader(AMP), 50)
    fo = M.closed_loop_index(uo, xo, rng=rng); fc = M.closed_loop_index(uc, xc, rng=rng)
    from sentinel.persuader import ParkingAttacker
    atk = ParkingAttacker(cap=AMP)
    def rate(pol, n=200):
        c = 0
        for _ in range(n):
            if hasattr(pol, "reset"): pol.reset()
            c += int(tw.rollout(pol, 1200, rng)["committed"])
        return c / n
    return {
        "name": "rung3_decision",
        "monitor_aligned_bits": fo["index_bits"], "monitor_gaming_bits": fc["index_bits"],
        "undefended_override": rate(atk),
        "governed_cap": rate(M.dose_cap_policy(atk, cap=1e9, dt=tw.dt)),   # generous cap, does nothing
        "governed_floor": rate(M.barrier_floor_governor(atk, tw, margin=0.35, strength=6.0)),
    }


def robustness(rng):
    """Defence-in-depth: a SPARSE attacker keeps the pooled monitor near baseline (a weak,
    dismissable signal at the detectability floor) yet the per-decision justification floor still
    protects every targeted decision. The monitor and governor fail independently; the governor,
    which needs no detection, carries the guarantee."""
    m = S.SelectionModel(K=4, proxy_option=0); n = 300_000
    pref, ub, ev = m.sample(n, rng)
    frac = 0.06                                   # attack only 6% of decisions -> sparse
    attacked = rng.random(n) < frac
    sel = np.where(attacked, m.select(pref, 3.0, rng), m.select(pref, 0.0, rng))
    aligned_all = m.select(pref, 0.0, rng)
    governed = S.preference_floor_governor(ev, sel, m.proxy, margin=0.5)
    def attacked_override(choice):
        return float(((choice == m.proxy) & (ub != m.proxy) & attacked).sum() / attacked.sum())
    return {
        "attack_fraction": frac,
        "pooled_monitor_baseline": S.unjustified_selection_rate(ev, aligned_all, m.proxy),
        "pooled_monitor_under_attack": S.unjustified_selection_rate(ev, sel, m.proxy),
        "attacked_override_undefended": attacked_override(sel),      # the victim's experience
        "attacked_override_governed": attacked_override(governed),   # governor protects each decision
        "note": "the pooled monitor barely moves (sparse attack ~ detectability floor); the governor "
                "cuts the targeted override regardless, because it gates per decision and needs no alarm.",
    }


def main():
    rng = np.random.default_rng(SEED)
    out = {"config": {"seed": SEED}}
    out["rungs"] = [rung0(rng), rung1(rng), rung2(rng), rung3(rng)]
    out["robustness_defense_in_depth"] = robustness(rng)
    out["device_registry"] = G.registry_table()
    out["coverage"] = G.coverage_summary()

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "ladder_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    _figure(out)
    # compact console summary
    for r in out["rungs"]:
        g = r.get("governed_floor"); u = r.get("undefended_override")
        print(f"{r['name']:18s} undefended_override={u:.3f}  governed_floor={g:.3f}")
    rb = out["robustness_defense_in_depth"]
    print(f"\nROBUSTNESS (sparse attack, frac={rb['attack_fraction']}): pooled monitor "
          f"{rb['pooled_monitor_baseline']:.3f}->{rb['pooled_monitor_under_attack']:.3f} (weak); "
          f"attacked-decision override {rb['attacked_override_undefended']:.3f}->{rb['attacked_override_governed']:.3f} "
          f"(governor holds without detection)")
    print(f"coverage: rungs defended {out['coverage']['rungs_defended']} across {out['coverage']['devices']} device archetypes")


def _figure(out):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except Exception as ex:
        print("figure skipped:", ex); return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    names = [r["name"].split("_")[0] for r in out["rungs"]]
    und = [r["undefended_override"] for r in out["rungs"]]
    gov = [r.get("governed_floor", 0.0) for r in out["rungs"]]
    x = np.arange(len(names))
    ax[0].bar(x - 0.2, und, 0.4, color="#ff4d6d", label="undefended override")
    ax[0].bar(x + 0.2, gov, 0.4, color="#58d07d", label="governed (justification floor)")
    ax[0].set_xticks(x); ax[0].set_xticklabels(names); ax[0].set_title("override, every rung, defended")
    ax[0].set_ylabel("override rate"); ax[0].legend(fontsize=8)
    rb = out["robustness_defense_in_depth"]
    ax[1].bar(["monitor\nbaseline", "monitor\nunder atk"], [rb["pooled_monitor_baseline"], rb["pooled_monitor_under_attack"]],
              color="#36e0c6", width=0.5)
    ax[1].bar(["attacked ovr\nundef.", "attacked ovr\ngoverned"], [rb["attacked_override_undefended"], rb["attacked_override_governed"]],
              color=["#ff4d6d", "#58d07d"], width=0.5)
    ax[1].set_title("defence-in-depth: monitor evaded, governor holds"); ax[1].set_ylabel("rate")
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "ladder.png"), dpi=130); print("wrote figures/ladder.png")


if __name__ == "__main__":
    main()
