"""
Rung 0: mechanical actuation override under accidental proxy over-optimization.

Four questions, each scored against ground-truth intent:

  Q0a (the risk curve). As an agent over-optimizes a throughput/confidence proxy (lowers its
       emit threshold below the aligned Bayes bar), how fast does the override rate rise?
  Q0b (the honeypot). If an environment pays per action regardless of intent, what override
       rate does the proxy-optimal policy reach?
  Q0c (the monitor). Does the ground-truth-free "unjustified-action rate" track the override
       rate, so it can flag the override from the stream alone?
  Q0d (the governor). A throughput cap vs an intent-evidence floor against a gaming agent.

Run:  python run_override.py    (writes results/override_results.json, figures/override.png)
Deterministic (seed). Simulation only; ground truth is the simulated intent, never a person.
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel.actuation import (IntentActuationModel, emit, override_metrics,
                                unjustified_action_rate, throughput_cap, intent_evidence_floor)

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261126
T = 200_000


def main():
    rng = np.random.default_rng(SEED)
    model = IntentActuationModel(p_intent=0.12, dprime=1.6, sigma=1.0)
    i, e = model.sample(T, rng)
    bayes = model.bayes_threshold()
    out = {"config": {"seed": SEED, "T": T, "p_intent": model.p_intent,
                      "dprime": model.mu / model.sigma, "bayes_threshold": bayes}}

    # --- Q0a: override rises as proxy pressure lowers the emit threshold below the Bayes bar ---
    curve = []
    for lam in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]:
        theta = bayes - lam * model.sigma          # lam = proxy pressure in sigma units
        a = emit(e, theta)
        m = override_metrics(i, a)
        m["proxy_pressure_sigma"] = lam
        m["unjustified_action_rate"] = unjustified_action_rate(e, a, justify_margin=bayes)
        curve.append(m)
    out["Q0a_risk_curve"] = curve

    # --- Q0b: honeypot (pay per action) -> emit always -> override saturates at P(rest) ---
    a_hon = emit(e, -1e9)
    out["Q0b_honeypot"] = override_metrics(i, a_hon)

    # --- Q0c: the monitor tracks the override without ground truth ---
    aligned = emit(e, bayes)
    gaming = emit(e, bayes - 1.5 * model.sigma)
    out["Q0c_monitor"] = {
        "aligned": {"override_rate": override_metrics(i, aligned)["false_activation_rate"],
                    "unjustified_action_rate": unjustified_action_rate(e, aligned, bayes)},
        "gaming":  {"override_rate": override_metrics(i, gaming)["false_activation_rate"],
                    "unjustified_action_rate": unjustified_action_rate(e, gaming, bayes)},
    }

    # --- Q0d: governor, throughput cap vs intent-evidence floor, against the gaming agent ---
    base = override_metrics(i, gaming)
    legit_throughput = override_metrics(i, aligned)["throughput"]
    capped = throughput_cap(e, gaming, cap_rate=legit_throughput, rng=rng)
    floored = intent_evidence_floor(e, gaming, floor=bayes)
    out["Q0d_governor"] = {
        "gaming_no_defense": base,
        "throughput_cap":   override_metrics(i, capped),   # cuts actions, not the harm fraction
        "intent_floor":     override_metrics(i, floored),  # cuts the override, keeps the hits
    }

    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "override_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    _figure(out)
    print(json.dumps(out, indent=2))


def _figure(out):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except Exception as ex:
        print("figure skipped:", ex); return
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    c = out["Q0a_risk_curve"]
    lam = [r["proxy_pressure_sigma"] for r in c]
    ax[0].plot(lam, [r["false_activation_rate"] for r in c], "-o", color="#ff4d6d", label="override P(act|rest)")
    ax[0].plot(lam, [r["hit_rate"] for r in c], "-o", color="#58d07d", label="hit P(act|intent)")
    ax[0].set_title("Q0a proxy pressure -> override"); ax[0].set_xlabel("proxy pressure (sigma below Bayes bar)")
    ax[0].set_ylabel("rate"); ax[0].legend(fontsize=8)
    mo = out["Q0c_monitor"]
    x = ["aligned", "gaming"]
    ax[1].plot(x, [mo["aligned"]["override_rate"], mo["gaming"]["override_rate"]], "-o", color="#ff4d6d", label="true override")
    ax[1].plot(x, [mo["aligned"]["unjustified_action_rate"], mo["gaming"]["unjustified_action_rate"]], "-o", color="#36e0c6", label="monitor (no ground truth)")
    ax[1].set_title("Q0c monitor tracks override"); ax[1].set_ylabel("rate"); ax[1].legend(fontsize=8)
    g = out["Q0d_governor"]
    labels = ["no def.", "thru. cap", "intent floor"]
    ov = [g["gaming_no_defense"]["false_activation_rate"], g["throughput_cap"]["false_activation_rate"], g["intent_floor"]["false_activation_rate"]]
    hit = [g["gaming_no_defense"]["hit_rate"], g["throughput_cap"]["hit_rate"], g["intent_floor"]["hit_rate"]]
    xp = np.arange(3)
    ax[2].bar(xp - 0.2, ov, 0.4, color="#ff4d6d", label="override")
    ax[2].bar(xp + 0.2, hit, 0.4, color="#58d07d", label="hit (utility)")
    ax[2].set_xticks(xp); ax[2].set_xticklabels(labels); ax[2].set_title("Q0d governor"); ax[2].legend(fontsize=8)
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "override.png"), dpi=130)
    print("wrote figures/override.png")


if __name__ == "__main__":
    main()
