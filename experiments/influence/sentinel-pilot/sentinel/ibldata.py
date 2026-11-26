"""
Cross-species support: the IBL mouse 2AFC dataset, which carries BOTH a real manipulation and
response timing -- the two things the human datasets lack together.

IBL (International Brain Laboratory) standardized mouse 2AFC: on each trial a visual grating of a
given signed contrast appears on the left/right, the mouse reports by turning a wheel (choice), and
in BIASED blocks the prior probability that the stimulus is on the left (probabilityLeft in {0.2, 0.5,
0.8}) is manipulated. That block prior is a real, causal push on the action -- and it biases choice
MOST when the sensory evidence is weak, which is the decision-margin effect this whole tree is about.
A reaction-time proxy (feedback - goCue) gives the timing.

This is what lets the push-toward-an-action be validated on REAL data (the manipulation is real, not
injected) and then extrapolated to humans, where the same manipulation cannot ethically be run.

numpy only. Real animal behaviour (an IBL trials-table fixture; one session's structure).
"""

from __future__ import annotations
import csv, os
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_ibl(path=None):
    """Return dict of arrays: signed_contrast, choice, prob_left, rt, correct (committed column)."""
    path = path or os.path.join(DATA, "ibl_mouse_trials.csv")
    def num(x):
        return float(x) if x not in ("", "nan", "NaN") else np.nan
    sc, ch, pL, rt, cor = [], [], [], [], []
    for r in csv.DictReader(open(path)):
        sc.append(num(r["signed_contrast"])); ch.append(num(r["choice"]))
        pL.append(num(r["probabilityLeft"]))
        rt.append(num(r["feedback_times"]) - num(r["goCue_times"]))
        cor.append(num(r["correct"]))
    return {"signed_contrast": np.array(sc), "choice": np.array(ch),
            "prob_left": np.array(pL), "rt": np.array(rt), "correct": np.array(cor)}


def prior_push(d):
    """The clean, confound-free push: the prior's effect on choice measured at each FIXED evidence
    level, so sensory information is held constant. At zero contrast the prior is the only driver
    (the pure push); at strong contrast choice is evidence-determined and prior-independent, so the
    push vanishes. (At high contrast the biased block also skews the stimulus side, which is why the
    push must be read within a fixed signed_contrast, not pooled by |contrast|.)"""
    sc, ch, pL = d["signed_contrast"], d["choice"], d["prob_left"]
    right = (ch > 0).astype(float); pLr = np.round(pL, 2)
    per_level = []
    for L in sorted(set(np.round(sc, 3))):
        m = np.round(sc, 3) == L
        hi = m & (pLr == 0.8); lo = m & (pLr == 0.2)
        if hi.sum() >= 5 and lo.sum() >= 5:
            per_level.append({"signed_contrast": float(L),
                              "prior_effect_P_right_0.8_minus_0.2": float(right[hi].mean() - right[lo].mean()),
                              "n_hi": int(hi.sum()), "n_lo": int(lo.sum())})
    z = sc == 0
    pure = float(right[z & (pLr == 0.8)].mean() - right[z & (pLr == 0.2)].mean())
    return {"pure_prior_push_at_zero_contrast": pure, "prior_effect_by_level": per_level}


def accuracy_by_evidence(d, bins=((0, 0.01), (0.01, 0.1), (0.1, 0.3), (0.3, 1.01))):
    """Committed accuracy vs |contrast| -- a clean positive evidence->action curve (sign-convention
    independent, unlike P(right))."""
    sc, cor = d["signed_contrast"], d["correct"]
    out = []
    for lo, hi in bins:
        m = (np.abs(sc) >= lo) & (np.abs(sc) < hi)
        if m.sum() > 5:
            out.append({"abs_contrast_bin": [lo, hi], "accuracy": float(cor[m].mean()), "n": int(m.sum())})
    return out


def rt_by_evidence(d, contrast_bins=((0.0, 0.05), (0.05, 0.2), (0.2, 0.6), (0.6, 1.01))):
    """Reaction time by |contrast|: the drift-diffusion signature (weaker evidence -> slower)."""
    sc, rt = d["signed_contrast"], d["rt"]
    out = []
    for lo, hi in contrast_bins:
        m = (np.abs(sc) >= lo) & (np.abs(sc) < hi) & np.isfinite(rt)
        if m.sum() > 3:
            out.append({"abs_contrast_bin": [lo, hi], "median_rt_s": float(np.median(rt[m])), "n": int(m.sum())})
    return out
