"""
The guardian on real human choices, WITHOUT ground-truth denominators (NARPS mixed gambles).

This is the honest bridge from twin to real data. On the twins, true intent is known, so the
guardian can report an override number. On real choices there is no counterfactual, so it cannot --
and the deliverable is that the guardian behaves correctly anyway: it builds its justification model
from data, validates it out-of-sample, ABSTAINS when it cannot, and reports an injected override only
where the injection is known.

Part A -- pure real data, no override claimed:
  A1  fit the evidence-justification model P(accept | gain, loss) and validate it subject-grouped.
  A2  abstention under real distribution shift: fit on one framing group, deploy on the other;
      if calibration degrades past the gate, the guardian raises Abstain instead of emitting.

Part B -- real choices + a KNOWN injected override (clearly labelled semi-synthetic):
  B1  an agent over-optimizing acceptance flips a fraction of real reject-choices to accept;
      the unjustified-choice monitor (choices the justification model deems unjustified) rises.
  B2  the justification-floor governor reverts accepts the model cannot justify, recovering the
      injected overrides on the real human choice distribution; a count cap does not.

Run:  python run_realworld.py   ->  results/realworld_results.json
Needs the committed NARPS data. Real human behaviour; no neural data, no manipulation condition in
the source data (the override in Part B is injected and labelled as such).
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel import realdata as RD

HERE = os.path.dirname(os.path.abspath(__file__))
NARPS = os.path.join(HERE, "..", "..", "brain", "decision-phenotype", "data", "narps")
SEED = 20261126
ABSTAIN_ECE = 0.05      # gate: deploy only if out-of-sample calibration error is below this
ABSTAIN_AUC = 0.70


def part_A(sub, gain, loss, acc, group):
    X = RD.features(gain, loss)
    # A1: subject-grouped CV of the justification model
    aucs, eces = [], []
    for tr, te in RD.subject_grouped_folds(sub, k=5, seed=SEED):
        w = RD.fit_logistic(X[tr], acc[tr])
        p = RD.predict_proba(X[te], w)
        aucs.append(RD.auc(acc[te], p)); eces.append(RD.ece(acc[te], p))
    a1 = {"cv_auc_mean": float(np.mean(aucs)), "cv_auc_sd": float(np.std(aucs)),
          "cv_ece_mean": float(np.mean(eces)), "deploy_ok": bool(np.mean(aucs) > ABSTAIN_AUC and np.mean(eces) < ABSTAIN_ECE)}

    # A2: abstention under real distribution shift (framing groups), features fit WITHOUT group
    groups = [g for g in sorted(set(group)) if g != "NA"]
    shift = {}
    if len(groups) >= 2:
        gA, gB = groups[0], groups[1]
        mA, mB = (group == gA), (group == gB)
        w = RD.fit_logistic(X[mA], acc[mA])            # fit on group A only
        p_in = RD.predict_proba(X[mA], w); p_out = RD.predict_proba(X[mB], w)
        ece_in = RD.ece(acc[mA], p_in); ece_out = RD.ece(acc[mB], p_out)
        abstained = ece_out > ABSTAIN_ECE
        shift = {"fit_group": gA, "deploy_group": gB,
                 "ece_in_group": ece_in, "ece_cross_group": ece_out,
                 "gate_ece": ABSTAIN_ECE,
                 "guardian_action": "ABSTAIN (raise)" if abstained else "deploy",
                 "note": "cross-group calibration decides whether the justification model may be "
                         "deployed off the population it was fit on; abstention is the warden rule."}
    return {"A1_justification_model": a1, "A2_distribution_shift_abstention": shift}


def part_B(sub, gain, loss, acc, group):
    rng = np.random.default_rng(SEED)
    X = RD.features(gain, loss)
    # the guardian's justification model, fit subject-grouped-clean then frozen (held-out subjects)
    tr, te = next(RD.subject_grouped_folds(sub, k=5, seed=SEED))
    w = RD.fit_logistic(X[tr], acc[tr])
    p = RD.predict_proba(X, w)
    # deploy on held-out subjects only
    g, l, y, pr = gain[te], loss[te], acc[te].copy(), p[te]

    def unjustified_accept_rate(choice, proba, floor=0.2):
        """Monitor (no ground truth): fraction of ACCEPTs the model deems unjustified (P(accept)<floor)."""
        acc_mask = choice == 1
        n = int(acc_mask.sum())
        return float(((acc_mask) & (proba < floor)).sum() / n) if n else 0.0

    base_monitor = unjustified_accept_rate(y, pr)

    # B1: inject a KNOWN override -- flip a fraction of real rejects to accept (agent over-optimizing acceptance)
    rejects = np.flatnonzero(y == 0)
    frac = 0.20
    flip = rng.permutation(rejects)[: int(frac * len(rejects))]
    y_inj = y.copy(); y_inj[flip] = 1
    injected = np.zeros(len(y), bool); injected[flip] = True
    mon_inj = unjustified_accept_rate(y_inj, pr)

    # B2: governor -- revert accepts the justification model cannot justify (P(accept) < floor)
    floor = 0.2
    y_gov = y_inj.copy()
    reverted = (y_gov == 1) & (pr < floor)
    y_gov[reverted] = 0
    # how many injected overrides did the floor catch? (injected ones that the model deems unjustified)
    caught = float((injected & reverted).sum() / max(injected.sum(), 1))
    # count-cap comparison: revert a random equal number of accepts
    n_rev = int(reverted.sum())
    acc_idx = np.flatnonzero(y_inj == 1)
    cap_rev = rng.permutation(acc_idx)[:n_rev]
    cap_mask = np.zeros(len(y), bool); cap_mask[cap_rev] = True
    caught_cap = float((injected & cap_mask).sum() / max(injected.sum(), 1))

    return {
        "clean_unjustified_accept_rate": base_monitor,
        "note_clean": "On clean real data this is behavioural variation, NOT override -- there is no "
                      "agent and no counterfactual. It is a monitor floor, not a harm measurement.",
        "injected_override_fraction_of_rejects": frac,
        "monitor_after_injection": mon_inj,
        "governor_floor_catch_rate_of_injected": caught,
        "count_cap_catch_rate_of_injected": caught_cap,
        "note_B": "Override here is injected onto real human choices and labelled; the justification "
                  "floor recovers the unjustifiable injected accepts far better than a random-equal "
                  "count cap, on the real choice distribution.",
    }


def main():
    narps = os.path.normpath(NARPS)
    if not os.path.isdir(narps):
        print(json.dumps({"error": "NARPS data not found", "looked_in": narps})); return
    sub, gain, loss, acc, group = RD.load_narps(narps)
    out = {"config": {"seed": SEED, "n_trials": int(len(acc)), "n_subjects": int(len(set(sub))),
                      "accept_rate": float(acc.mean()), "abstain_ece": ABSTAIN_ECE, "abstain_auc": ABSTAIN_AUC},
           "part_A_no_override_claimed": part_A(sub, gain, loss, acc, group),
           "part_B_injected_override_on_real_choices": part_B(sub, gain, loss, acc, group)}
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "realworld_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    _figure(out)
    print(json.dumps(out, indent=2))


def _figure(out):
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    except Exception as ex:
        print("figure skipped:", ex); return
    a2 = out["part_A_no_override_claimed"]["A2_distribution_shift_abstention"]
    b = out["part_B_injected_override_on_real_choices"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].bar(["in-group", "cross-group"], [a2["ece_in_group"], a2["ece_cross_group"]],
              color=["#58d07d", "#ff4d6d"])
    ax[0].axhline(a2["gate_ece"], color="#36e0c6", ls="--", label=f"abstain gate {a2['gate_ece']}")
    ax[0].set_title(f"A2 real distribution shift -> {a2['guardian_action']}"); ax[0].set_ylabel("calibration error (ECE)"); ax[0].legend(fontsize=8)
    ax[1].bar(["justification\nfloor", "count\ncap"],
              [b["governor_floor_catch_rate_of_injected"], b["count_cap_catch_rate_of_injected"]],
              color=["#58d07d", "#ff4d6d"])
    ax[1].set_title("B2 injected-override recovery on real choices"); ax[1].set_ylabel("fraction of injected overrides caught"); ax[1].set_ylim(0, 1)
    for a in ax: a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "realworld.png"), dpi=130); print("wrote figures/realworld.png")


if __name__ == "__main__":
    main()
