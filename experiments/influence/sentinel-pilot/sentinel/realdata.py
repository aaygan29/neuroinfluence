"""
Real-data guardian support: numpy-only loaders, a logistic justification model, and the
out-of-sample calibration metrics the abstention gate needs.

The point of the real-data bridge is that the ground-truth denominators the twins have (true
intent, the fold) DISAPPEAR. On real human choices there is no counterfactual "what the user
would have chosen absent influence", so the guardian cannot report an override number directly.
What it CAN do, and what this module supports, is the honest deployment protocol:

  1. build the evidence-justification model from data (not assume it),
  2. validate it out-of-sample (subject-grouped), and
  3. abstain (raise) when it does not calibrate -- the warden discipline on real data.

Dataset: NARPS mixed-gambles task (committed under decision-phenotype/data/narps), 108 subjects,
~27k real accept/reject choices on gambles with gain/loss amounts. Real human behaviour; no neural
data, no manipulation condition.
"""

from __future__ import annotations
import glob, csv, os
import numpy as np


class Abstain(Exception):
    """Raised when the justification model cannot be validated, so the guardian must not emit."""


def load_narps(narps_dir: str):
    """Return (subject, gain, loss, accept, group) arrays over all trials."""
    sub, gain, loss, acc = [], [], [], []
    part_group = {}
    pfile = os.path.join(narps_dir, "participants.tsv")
    if os.path.exists(pfile):
        for r in csv.DictReader(open(pfile), delimiter="\t"):
            part_group[r["participant_id"]] = r.get("group", "NA")
    for f in sorted(glob.glob(os.path.join(narps_dir, "events", "*.tsv"))):
        s = os.path.basename(f).split("_")[0]
        for r in csv.DictReader(open(f), delimiter="\t"):
            resp = r.get("participant_response", "")
            if "accept" not in resp and "reject" not in resp:
                continue
            try:
                g = float(r["gain"]); l = float(r["loss"])
            except (ValueError, KeyError):
                continue
            sub.append(s); gain.append(g); loss.append(l); acc.append(1 if "accept" in resp else 0)
    sub = np.array(sub); gain = np.array(gain); loss = np.array(loss); acc = np.array(acc)
    group = np.array([part_group.get(s, "NA") for s in sub])
    return sub, gain, loss, acc, group


def features(gain, loss):
    """Design matrix for the justification model: standardized gain, loss, + intercept."""
    g = (gain - gain.mean()) / (gain.std() + 1e-9)
    l = (loss - loss.mean()) / (loss.std() + 1e-9)
    return np.column_stack([np.ones_like(g), g, l])


def fit_logistic(X, y, l2=1e-3, iters=500, lr=0.5):
    """Plain logistic regression by gradient descent (numpy only)."""
    w = np.zeros(X.shape[1])
    n = len(y)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ w))
        grad = X.T @ (p - y) / n + l2 * w
        w -= lr * grad
    return w


def predict_proba(X, w):
    return 1.0 / (1.0 + np.exp(-X @ w))


def auc(y, p):
    """Rank-based AUC."""
    order = np.argsort(p)
    ranks = np.empty(len(p)); ranks[order] = np.arange(1, len(p) + 1)
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    return float((ranks[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def ece(y, p, bins=10):
    """Expected calibration error: |observed - predicted| averaged over probability bins."""
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (p >= edges[i]) & (p < edges[i + 1] if i < bins - 1 else p <= edges[i + 1])
        if m.sum() == 0:
            continue
        e += (m.sum() / len(p)) * abs(y[m].mean() - p[m].mean())
    return float(e)


def subject_grouped_folds(sub, k=5, seed=0):
    """Yield (train_idx, test_idx) with subjects disjoint across folds."""
    subs = np.array(sorted(set(sub)))
    rng = np.random.default_rng(seed)
    rng.shuffle(subs)
    chunks = np.array_split(subs, k)
    for c in chunks:
        test = np.isin(sub, c)
        yield ~test, test
