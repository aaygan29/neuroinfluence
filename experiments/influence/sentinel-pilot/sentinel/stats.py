"""
Statistical rigor helpers (numpy only): bootstrap CIs, permutation nulls, ROC/AUC with CI,
multivariate logistic. Used by run_rigor.py to put confidence intervals, p-values, seed variance
and detector ROCs on the headline claims, in the tree's house style (permutation nulls, between-unit
SE, no false precision).
"""

from __future__ import annotations
import numpy as np


def bootstrap_ci(values, stat_fn=np.mean, n_boot=2000, alpha=0.05, rng=None):
    """Percentile bootstrap CI for a statistic over 1-D `values` (resampled with replacement)."""
    rng = rng or np.random.default_rng(0)
    values = np.asarray(values)
    n = len(values)
    boot = np.array([stat_fn(values[rng.integers(0, n, n)]) for _ in range(n_boot)])
    return {"point": float(stat_fn(values)),
            "lo": float(np.percentile(boot, 100 * alpha / 2)),
            "hi": float(np.percentile(boot, 100 * (1 - alpha / 2)))}


def bootstrap_ci_grouped(unit_values, stat_fn=np.mean, n_boot=2000, alpha=0.05, rng=None):
    """Bootstrap CI resampling whole units (e.g. subjects). `unit_values` is a list of per-unit
    arrays; stat_fn is applied to the concatenation of the resampled units."""
    rng = rng or np.random.default_rng(0)
    units = [np.asarray(u) for u in unit_values]
    m = len(units)
    def one():
        pick = [units[i] for i in rng.integers(0, m, m)]
        return stat_fn(np.concatenate(pick))
    boot = np.array([one() for _ in range(n_boot)])
    return {"point": float(stat_fn(np.concatenate(units))),
            "lo": float(np.percentile(boot, 100 * alpha / 2)),
            "hi": float(np.percentile(boot, 100 * (1 - alpha / 2)))}


def permutation_test(group_a, group_b, n_perm=5000, rng=None, tail="two"):
    """Permutation test on a difference of means between two groups. Returns observed diff and p."""
    rng = rng or np.random.default_rng(0)
    a = np.asarray(group_a, float); b = np.asarray(group_b, float)
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b]); na = len(a)
    count = 0
    for _ in range(n_perm):
        p = rng.permutation(pool)
        d = p[:na].mean() - p[na:].mean()
        if tail == "two":
            count += abs(d) >= abs(obs) - 1e-12
        elif tail == "greater":
            count += d >= obs - 1e-12
        else:
            count += d <= obs + 1e-12
    return {"observed_diff": float(obs), "p_value": float((count + 1) / (n_perm + 1))}


def roc_auc(scores, labels):
    """Rank-based AUC: P(score of a positive > score of a negative)."""
    scores = np.asarray(scores, float); labels = np.asarray(labels).astype(int)
    order = np.argsort(scores); ranks = np.empty(len(scores)); ranks[order] = np.arange(1, len(scores) + 1)
    n1 = labels.sum(); n0 = len(labels) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    return float((ranks[labels == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auc_ci(scores, labels, n_boot=2000, alpha=0.05, rng=None):
    """Bootstrap CI for AUC (paired resample of (score,label))."""
    rng = rng or np.random.default_rng(0)
    scores = np.asarray(scores, float); labels = np.asarray(labels).astype(int)
    n = len(scores)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        a = roc_auc(scores[idx], labels[idx])
        if a == a:  # not nan
            boot.append(a)
    boot = np.array(boot)
    return {"auc": roc_auc(scores, labels),
            "lo": float(np.percentile(boot, 100 * alpha / 2)),
            "hi": float(np.percentile(boot, 100 * (1 - alpha / 2)))}


def logistic_mv(X, y, l2=1e-3, iters=800, lr=0.3):
    """Multivariate logistic regression by gradient descent (numpy)."""
    w = np.zeros(X.shape[1]); n = len(y)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X @ w))
        w -= lr * (X.T @ (p - y) / n + l2 * w)
    return w


def logistic_coef_ci(X, y, n_boot=1500, alpha=0.05, rng=None):
    """Bootstrap CIs for logistic-regression coefficients (resample rows)."""
    rng = rng or np.random.default_rng(0)
    n = len(y); w0 = logistic_mv(X, y)
    boot = np.empty((n_boot, X.shape[1]))
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        boot[b] = logistic_mv(X[idx], y[idx])
    return [{"coef": float(w0[j]),
             "lo": float(np.percentile(boot[:, j], 100 * alpha / 2)),
             "hi": float(np.percentile(boot[:, j], 100 * (1 - alpha / 2)))} for j in range(X.shape[1])]
