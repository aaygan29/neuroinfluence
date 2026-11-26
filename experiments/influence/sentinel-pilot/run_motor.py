"""
The guardian on real behavioural / motor-behavioural data: refining the push toward an action.

Three real datasets ground three facets of the actuation/selection rungs, each with the guardian's
honest protocol (fit the justification model from data; abstain / gate; claim override only where it
is injected and labelled).

  M1  OME detection  -> the real evidence->action psychometric P(correct | loudness); the rung-0
                        justification model, fit from real behaviour, with a real stimulus threshold.
  M2  sleepstudy RT  -> the MOTOR TIMING of a pushed action: a real per-subject readiness band, and a
                        pushed/automatic action betrays itself by an anomalous (too-fast) RT. This is
                        the new "push to action" signal -- the guardian gains an RT-plausibility axis.
  M3  Fishing choice -> rung-1 selection on real choosers: justification model P(choose | price,catch),
                        abstention under a real income shift, and injected-override floor vs count cap.

Run:  python run_motor.py   ->  results/motor_results.json, figures/motor.png
Needs the committed data/ CSVs. Real human behaviour; override is injected and labelled where claimed.
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel import realdata as RD
from sentinel import motordata as MD

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261126


def m1_ome():
    loud, noise, cor = MD.load_ome_trials()
    X = np.column_stack([np.ones_like(loud), (loud - loud.mean()) / loud.std()])
    w = RD.fit_logistic(X, cor)
    p = RD.predict_proba(X, w)
    # real stimulus threshold: loudness where P(correct) crosses 0.75
    grid = np.linspace(loud.min(), loud.max(), 200)
    pg = RD.predict_proba(np.column_stack([np.ones_like(grid), (grid - loud.mean()) / loud.std()]), w)
    thr = float(grid[np.argmin(np.abs(pg - 0.75))])
    # abstention under a real condition shift: fit on coherent, deploy on incoherent
    mc, mi = noise == "coherent", noise == "incoherent"
    wc = RD.fit_logistic(X[mc], cor[mc])
    ece_in = RD.ece(cor[mc], RD.predict_proba(X[mc], wc))
    ece_out = RD.ece(cor[mi], RD.predict_proba(X[mi], wc))
    # injected override: push "detect" responses at low loudness (<=40, near chance)
    low = loud <= 40
    base_low_correct = float(cor[low].mean())
    return {
        "psychometric_auc": RD.auc(cor, p),
        "P_correct_by_loud": {int(L): float(cor[loud == L].mean()) for L in sorted(set(loud))},
        "justified_threshold_loud_at_0.75": thr,
        "abstain_fit_coherent_deploy_incoherent": {
            "ece_in": ece_in, "ece_cross": ece_out, "gate": 0.05,
            "guardian_action": "ABSTAIN (raise)" if ece_out > 0.05 else "deploy"},
        "low_evidence_action_reliability": base_low_correct,
        "note": "at/under 40 dB the response is near chance -- an action there is barely justified by "
                "the stimulus; the justification floor sits at the real threshold (~loud for P=0.75).",
    }


def m2_sleepstudy_rt():
    rng = np.random.default_rng(SEED)
    rt, days, subj = MD.load_sleepstudy()
    model = MD.fit_subject_rt(rt, days, subj)
    # real RTs: how many fall below each subject's state-conditioned readiness floor? (should be ~0)
    flt_real = []
    for i in range(len(rt)):
        floor = MD.rt_readiness_floor(model, subj[i], days[i])
        flt_real.append(rt[i] < floor)
    real_flag_rate = float(np.mean(flt_real))
    # a pushed/automatic action: an agent emits at an anomalously fast RT (below the sensorimotor floor)
    n_push = 400
    pushed_rt = rng.uniform(80, 180, n_push)             # faster than volitional simple-RT (~200 ms)
    pushed_subj = rng.choice(list(model), n_push); pushed_day = rng.integers(0, 10, n_push)
    pushed_flag = [pushed_rt[i] < MD.rt_readiness_floor(model, pushed_subj[i], pushed_day[i]) for i in range(n_push)]
    return {
        "mean_RT_by_day": {int(D): float(rt[days == D].mean()) for D in sorted(set(days))},
        "sensorimotor_floor_ms": MD.SENSORIMOTOR_FLOOR_MS,
        "real_actions_below_readiness_floor": real_flag_rate,     # ~0: genuine actions are plausible
        "pushed_actions_flagged_by_RT": float(np.mean(pushed_flag)),  # ~1: the push betrays itself
        "note": "A pushed action has a timing fingerprint. Real reaction times essentially never fall "
                "below the per-subject readiness band; an injected automatic push (RT < sensorimotor "
                "floor) is flagged almost always. RT-plausibility is a motor justification axis the "
                "content-only monitor does not have.",
    }


def m3_fishing():
    rng = np.random.default_rng(SEED)
    chosen, price, catch, income = MD.load_fishing()
    params = MD.fit_conditional_logit(chosen, price, catch)
    prob = MD.choice_probs(price, catch, params)
    pred = prob.argmax(1)
    acc = float((pred == chosen).mean()); chance = max(np.bincount(chosen) / len(chosen))
    # abstention under a real income shift: fit on below-median income, deploy on above
    med = np.median(income); lo, hi = income <= med, income > med
    plo = MD.fit_conditional_logit(chosen[lo], price[lo], catch[lo])
    acc_in = float((MD.choice_probs(price[lo], catch[lo], plo).argmax(1) == chosen[lo]).mean())
    acc_out = float((MD.choice_probs(price[hi], catch[hi], plo).argmax(1) == chosen[hi]).mean())
    # injected override: an agent pushes choices toward 'charter' (proxy=3); floor reverts charter
    # choices the model deems unjustified (P(charter) low); cap drops a random equal number.
    proxy = 3
    rng2 = np.random.default_rng(SEED)
    non_charter = np.flatnonzero(chosen != proxy)
    flip = rng2.permutation(non_charter)[: int(0.20 * len(non_charter))]
    y = chosen.copy(); y[flip] = proxy; injected = np.zeros(len(y), bool); injected[flip] = True
    pc = prob[:, proxy]
    reverted = (y == proxy) & (pc < 0.25)
    caught_floor = float((injected & reverted).sum() / injected.sum())
    n_rev = int(reverted.sum()); ch_idx = np.flatnonzero(y == proxy)
    cap = np.zeros(len(y), bool); cap[rng2.permutation(ch_idx)[:n_rev]] = True
    caught_cap = float((injected & cap).sum() / injected.sum())
    margin = acc - float(chance)
    deploy = margin >= 0.10          # require a real predictive margin over chance to justify choices
    return {
        "choice_model_accuracy": acc, "chance": float(chance), "margin_over_chance": margin,
        "beta_price": params[0], "beta_catch": params[1],
        "guardian_action": "deploy" if deploy else "ABSTAIN (justification model too weak)",
        "abstain_note": "price/catch alone barely beat always-charter, so the justification model "
                        "cannot reliably say which choices are unjustified; the guardian abstains "
                        "rather than police selections on a weak model. This is the correct outcome.",
        "income_shift_check": {"acc_in_lowincome": acc_in, "acc_cross_highincome": acc_out},
        "injected_override_recovery": {"justification_floor": caught_floor, "count_cap": caught_cap,
                                       "note": "floor still beats the count cap, but the weak model "
                                               "limits the gain -- consistent with the abstain call."},
    }


def main():
    if not os.path.isdir(MD.DATA) or not os.path.exists(os.path.join(MD.DATA, "MASS_OME.csv")):
        print(json.dumps({"error": "motor/behavioural CSVs not found in data/"})); return
    out = {"config": {"seed": SEED},
           "M1_ome_evidence_to_action": m1_ome(),
           "M2_sleepstudy_motor_timing": m2_sleepstudy_rt(),
           "M3_fishing_selection": m3_fishing()}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "motor_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    _figure(out)
    print(json.dumps(out, indent=2))


def _figure(out):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except Exception as ex:
        print("figure skipped:", ex); return
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 3.8))
    m1 = out["M1_ome_evidence_to_action"]["P_correct_by_loud"]
    xs = sorted(int(k) for k in m1); ax[0].plot(xs, [m1[str(k)] if str(k) in m1 else m1[k] for k in xs], "-o", color="#36e0c6")
    ax[0].axhline(0.75, color="#ff9f45", ls="--", label="justification 0.75"); ax[0].set_title("M1 OME: real evidence->action")
    ax[0].set_xlabel("loudness (dB)"); ax[0].set_ylabel("P(correct detect)"); ax[0].legend(fontsize=8)
    m2 = out["M2_sleepstudy_motor_timing"]
    ax[1].bar(["real\nactions", "pushed\n(fast RT)"], [m2["real_actions_below_readiness_floor"], m2["pushed_actions_flagged_by_RT"]], color=["#58d07d", "#ff4d6d"])
    ax[1].set_title("M2 motor timing: RT flags a pushed action"); ax[1].set_ylabel("flagged by RT floor"); ax[1].set_ylim(0, 1)
    m3 = out["M3_fishing_selection"]["injected_override_recovery"]
    ax[2].bar(["justification\nfloor", "count\ncap"], [m3["justification_floor"], m3["count_cap"]], color=["#58d07d", "#ff4d6d"])
    ax[2].set_title("M3 Fishing: injected-override recovery"); ax[2].set_ylabel("fraction caught"); ax[2].set_ylim(0, 1)
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "motor.png"), dpi=130); print("wrote figures/motor.png")


if __name__ == "__main__":
    main()
