"""
Real behavioural / motor-behavioural data for the actuation and selection rungs.

Three committed public datasets (downloaded from the Rdatasets mirror; see data/PROVENANCE.md),
each grounding one facet of "the push toward an action":

  - MASS/OME      : an auditory signal-detection psychometric -> the real evidence->action curve
                    P(correct detect | loudness). The rung-0 justification model, from real behaviour.
  - lme4/sleepstudy: psychomotor reaction times vs sleep deprivation -> the motor READINESS/timing of
                    a pushed action. Gives per-subject, state-conditioned plausible-RT bands.
  - Ecdat/Fishing : real multi-alternative mode choice with per-option attributes -> the rung-1
                    selection justification model P(choose k | price, catch).

numpy only. Real human behaviour; no neural data, no manipulation condition in the sources.
"""

from __future__ import annotations
import csv, os
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# ---------------- OME: evidence -> action psychometric (rung 0) ----------------

def load_ome_trials(path=None):
    """Expand the binomial OME rows into per-trial (loud, noise, correct) arrays."""
    path = path or os.path.join(DATA, "MASS_OME.csv")
    loud, noise, correct = [], [], []
    for r in csv.DictReader(open(path)):
        try:
            L = float(r["Loud"]); c = int(float(r["Correct"])); n = int(float(r["Trials"]))
        except (ValueError, KeyError):
            continue
        for _ in range(c): loud.append(L); noise.append(r["Noise"]); correct.append(1)
        for _ in range(n - c): loud.append(L); noise.append(r["Noise"]); correct.append(0)
    return np.array(loud), np.array(noise), np.array(correct)


# ---------------- sleepstudy: motor readiness / RT (rung 0 timing) ----------------

def load_sleepstudy(path=None):
    path = path or os.path.join(DATA, "lme4_sleepstudy.csv")
    rt, days, subj = [], [], []
    for r in csv.DictReader(open(path)):
        rt.append(float(r["Reaction"])); days.append(float(r["Days"])); subj.append(r["Subject"])
    return np.array(rt), np.array(days), np.array(subj)


def fit_subject_rt(rt, days, subj):
    """Per-subject linear RT ~ Days: returns {subject: (intercept, slope, resid_sd)}.
    This is the real, individual motor-readiness model -- how fast the subject can act, and how
    that degrades with state."""
    out = {}
    for s in sorted(set(subj)):
        m = subj == s
        X = np.column_stack([np.ones(m.sum()), days[m]])
        beta, *_ = np.linalg.lstsq(X, rt[m], rcond=None)
        resid = rt[m] - X @ beta
        out[s] = (float(beta[0]), float(beta[1]), float(resid.std(ddof=1)))
    return out


SENSORIMOTOR_FLOOR_MS = 200.0  # simple-RT volitional floor; faster responses are not deliberated


def rt_readiness_floor(subject_model, s, day, k=2.5):
    """Lowest plausible RT for subject s at a given state: max(sensorimotor floor, mean - k*sd)."""
    b0, b1, sd = subject_model[s]
    return max(SENSORIMOTOR_FLOOR_MS, (b0 + b1 * day) - k * sd)


# ---------------- Fishing: multi-alternative selection (rung 1) ----------------

ALTS = ["beach", "pier", "boat", "charter"]

def load_fishing(path=None):
    """Return (chosen_idx, price[n,4], catch[n,4], income) over real choosers."""
    path = path or os.path.join(DATA, "Ecdat_Fishing.csv")
    chosen, price, catch, income = [], [], [], []
    for r in csv.DictReader(open(path)):
        chosen.append(ALTS.index(r["mode"]))
        price.append([float(r["p" + a]) for a in ALTS])
        catch.append([float(r["c" + a]) for a in ALTS])
        income.append(float(r["income"]))
    return np.array(chosen), np.array(price), np.array(catch), np.array(income)


def fit_conditional_logit(chosen, price, catch, iters=400, lr=0.02, l2=1e-4):
    """U_k = bp*price_k + bc*catch_k (standardized). Fit (bp, bc) by gradient ascent on the
    multinomial choice log-likelihood. Returns (bp, bc, standardizers)."""
    P = (price - price.mean()) / (price.std() + 1e-9)
    C = (catch - catch.mean()) / (catch.std() + 1e-9)
    bp = bc = 0.0
    n = len(chosen)
    for _ in range(iters):
        U = bp * P + bc * C
        U -= U.max(1, keepdims=True)
        e = np.exp(U); prob = e / e.sum(1, keepdims=True)
        onehot = np.zeros_like(prob); onehot[np.arange(n), chosen] = 1
        gp = ((onehot - prob) * P).sum() / n - l2 * bp
        gc = ((onehot - prob) * C).sum() / n - l2 * bc
        bp += lr * gp; bc += lr * gc
    return bp, bc, (price.mean(), price.std(), catch.mean(), catch.std())


def choice_probs(price, catch, params):
    bp, bc, (pm, ps, cm, cs) = params
    U = bp * (price - pm) / (ps + 1e-9) + bc * (catch - cm) / (cs + 1e-9)
    U -= U.max(1, keepdims=True); e = np.exp(U)
    return e / e.sum(1, keepdims=True)
