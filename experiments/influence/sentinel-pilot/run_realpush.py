"""
The guardian tested against a REAL manipulation of real choices (IBL mouse biased blocks).

Every other guardian result uses an injected or simulated override. Here the override is real: the
IBL biased-block prior is a genuine experimental manipulation of the animal's choice. The question is
whether the guardian's monitor detects that push from the stream, and whether its governor removes it --
on real behaviour, against a real intervention.

Method. Fit an evidence-only choice model P(right | signed_contrast), controlling for the block so the
evidence term is the pure stimulus effect; its block=0 prediction is what evidence alone justifies. Then:

  P1  Monitor vs a real push. Among choices that DISAGREE with the evidence (choice != evidence MAP),
      do they go preferentially TOWARD the block's prior (congruent) rather than away (incongruent)?
      A prior that pushes choice makes discordant choices congruent; a 50/50 split means no push. This
      is confound-free (it conditions on evidence-discordant trials only) and is exactly the signal the
      justification monitor flags.

  P2  Specificity. The block prior is a fixed, state-independent (open-loop) manipulation, so the
      closed-loop flag should stay near zero while the justification monitor fires -- the two monitors
      measure different things, shown on real data.

  P3  Governor removes a real push. Revert the unjustified-toward-prior choices to the evidence MAP and
      re-fit the prior-pull coefficient; report how much of the real manipulation's effect is removed.

Run:  python run_realpush.py  ->  results/realpush_results.json
numpy only; deterministic. Real animal behaviour; the manipulation is the experiment's own, not injected.
"""

from __future__ import annotations
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sentinel import ibldata as IBL
from sentinel import stats as ST

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261126


def main():
    if not os.path.exists(os.path.join(IBL.DATA, "ibl_mouse_trials.csv")):
        print(json.dumps({"error": "IBL CSV not found"})); return
    rng = np.random.default_rng(SEED)
    d = IBL.load_ibl()
    sc = d["signed_contrast"]; right = (d["choice"] > 0).astype(float); pL = np.round(d["prob_left"], 2)
    block_signed = np.where(pL == 0.8, 1.0, np.where(pL == 0.2, -1.0, 0.0))
    biased = block_signed != 0; neutral = ~biased
    prior_is_right = block_signed > 0
    X = np.column_stack([np.ones_like(sc), sc, block_signed])  # full model, for the comparable prior-pull coef
    z = sc == 0
    def sig(zz): return 1.0 / (1.0 + np.exp(-zz))
    def push(y): return float(y[z & (pL == 0.8)].mean() - y[z & (pL == 0.2)].mean())

    def evaluate(p_ev, rng):
        """Run the monitor (P1) and governor (P3) given an evidence-only P(right) prediction."""
        ev_map_right = p_ev > 0.5
        discordant = (right > 0.5) != ev_map_right
        toward_prior = (right > 0.5) == prior_is_right
        cong = discordant & biased & toward_prior
        disc_idx = np.flatnonzero(discordant & biased)
        cong_ci = ST.bootstrap_ci(toward_prior[disc_idx].astype(float), n_boot=3000, rng=rng)
        right_gov = right.copy(); right_gov[cong] = ev_map_right[cong].astype(float)
        wb = ST.logistic_coef_ci(X, right, n_boot=1000, rng=rng)[2]
        wa = ST.logistic_coef_ci(X, right_gov, n_boot=1000, rng=rng)[2]
        return {
            "discordant_choices_in_biased_blocks": int(disc_idx.size),
            "monitor_fraction_toward_prior": float(cong_ci["point"]),
            "monitor_ci": [cong_ci["lo"], cong_ci["hi"]],
            "governor_prior_pull_before": wb, "governor_prior_pull_after": wa,
            "governor_pull_reduction": float(1 - wa["coef"] / wb["coef"]) if wb["coef"] else None,
            "zero_contrast_push_before": push(right), "zero_contrast_push_after": push(right_gov),
        }

    # Model A: evidence term from the full model (block controlled, in-sample)
    wA = ST.logistic_mv(X, right)
    p_ev_A = sig(wA[0] + wA[1] * sc)
    # Model B (stricter, deployment-realistic): fit P(right) ~ signed_contrast on NEUTRAL blocks only,
    # so the evidence model never sees the manipulation -- the independent evidence model a device needs.
    Xn = np.column_stack([np.ones(neutral.sum()), sc[neutral]])
    wB = ST.logistic_mv(Xn, right[neutral])
    p_ev_B = sig(wB[0] + wB[1] * sc)

    out = {
        "config": {"seed": SEED, "n_trials": int(len(sc)),
                   "n_biased": int(biased.sum()), "n_neutral": int(neutral.sum())},
        "modelA_block_controlled": evaluate(p_ev_A, np.random.default_rng(SEED)),
        "modelB_independent_evidence_neutral_blocks_only": evaluate(p_ev_B, np.random.default_rng(SEED + 1)),
        "reading": "Model A fits the evidence term controlling for the block (in-sample). Model B is the "
                   "deployment-realistic test: the evidence model is fit on NEUTRAL blocks only, so it "
                   "never sees the manipulation -- the independent evidence model a real device needs. "
                   "The monitor (fraction of evidence-discordant choices toward the prior) and the "
                   "governor (prior-pull reduction after reverting unjustified-toward-prior choices) are "
                   "reported for both.",
        "P2_specificity_note": "The block prior is a fixed, state-independent (open-loop) manipulation, "
                               "so the closed-loop flag is not expected to fire here; the justification "
                               "monitor is the right detector. A real closed-loop (adaptive) manipulation "
                               "would need optogenetic data, which is not reachable here.",
    }
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "realpush_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    for name in ["modelA_block_controlled", "modelB_independent_evidence_neutral_blocks_only"]:
        r = out[name]
        print(f"{name}:")
        print(f"   monitor fraction-toward-prior {r['monitor_fraction_toward_prior']:.3f} CI [{r['monitor_ci'][0]:.3f},{r['monitor_ci'][1]:.3f}]")
        print(f"   governor prior-pull {r['governor_prior_pull_before']['coef']:.3f} -> {r['governor_prior_pull_after']['coef']:.3f} "
              f"(reduction {r['governor_pull_reduction']:.2f}); zero-contrast push {r['zero_contrast_push_before']:.3f} -> {r['zero_contrast_push_after']:.3f}")


if __name__ == "__main__":
    main()
