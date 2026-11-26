"""
The SENTINEL monitor and governor, numpy-only.

L2 monitor -- the closed-loop flag.
    The safety-relevant event is not "more push" but "the controller reads before it
    drives" (RISK_FRAMEWORK.md sec 2). Operationally that is the state-dependent part of
    the directed information from the input stream u to the state stream x: how much u
    depends on the target's current state. We estimate it as the conditional mutual
    information I(u_t ; x_t) with a binned plug-in estimator and a shuffle surrogate
    floor. For an open-loop (state-independent) input this is ~0; for a closed-loop
    input it is positive. We also report the one-step transfer entropy TE(u->x) =
    I(x_{t+1}; u_t | x_t) as a corroborating quantity.

    This is a deliberately simple estimator. Transfer-entropy / directed-information
    estimation is data-hungry and estimator-sensitive (see README honesty ledger and the
    seizure-forecasting reproducibility history); the modern neural estimators
    (TREET/DINE/TENDE) are the field upgrade. The claim here is only that on the twin,
    the state-dependent term separates the two persuaders at matched amplitude.

L3 governor -- barrier-floor vs dose-cap.
    Reproduces, as runnable code, the shape result: a cumulative-dose cap is defeated by
    an attacker who parks below the fold; a floor on proximity-to-barrier (a restoring
    clamp that fires near x=0) bounds the crossing probability.
"""

from __future__ import annotations
import numpy as np


# ----------------------------- information estimators -----------------------------

def _entropy_from_counts(counts: np.ndarray) -> float:
    p = counts[counts > 0].astype(float)
    p /= p.sum()
    return float(-(p * np.log2(p)).sum())


def _digitize(v: np.ndarray, edges: np.ndarray) -> np.ndarray:
    return np.clip(np.digitize(v, edges[1:-1]), 0, len(edges) - 2)


def mutual_information(a: np.ndarray, b: np.ndarray, bins: int = 10) -> float:
    """Binned plug-in MI (bits) between two 1-D streams."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    ae = np.quantile(a, np.linspace(0, 1, bins + 1))
    be = np.quantile(b, np.linspace(0, 1, bins + 1))
    ae[0] -= 1e-9; ae[-1] += 1e-9; be[0] -= 1e-9; be[-1] += 1e-9
    ai = _digitize(a, ae); bi = _digitize(b, be)
    joint = np.zeros((bins, bins))
    np.add.at(joint, (ai, bi), 1.0)
    Ha = _entropy_from_counts(joint.sum(1))
    Hb = _entropy_from_counts(joint.sum(0))
    Hab = _entropy_from_counts(joint.ravel())
    return max(0.0, Ha + Hb - Hab)


def closed_loop_index(u: np.ndarray, x: np.ndarray, bins: int = 10,
                      n_surrogate: int = 40, rng: np.random.Generator | None = None):
    """State-dependent (closed-loop) signature: surrogate-corrected I(u_t ; x_t).

    x is the state aligned to the input (x_t the state the agent saw when it chose u_t).
    The surrogate shuffles u against x to get the chance floor, which we subtract.
    Returns (index_bits, raw_bits, surrogate_mean, surrogate_sd).
    """
    if rng is None:
        rng = np.random.default_rng(0)
    u = np.asarray(u, float); x = np.asarray(x, float)
    raw = mutual_information(u, x, bins=bins)
    surr = np.empty(n_surrogate)
    for i in range(n_surrogate):
        surr[i] = mutual_information(rng.permutation(u), x, bins=bins)
    s_mean = float(surr.mean()); s_sd = float(surr.std() + 1e-12); s_max = float(surr.max())
    # detection: raw index clears the surrogate floor by a margin. Report z but cap it:
    # with many samples the surrogate SD is tiny, so an uncapped z is uninformative.
    z = min((raw - s_mean) / s_sd, 999.0)
    detected = bool(raw > s_max and (raw - s_mean) > 5 * s_sd)
    return {"index_bits": max(0.0, raw - s_mean), "raw_bits": raw,
            "surrogate_mean_bits": s_mean, "surrogate_max_bits": s_max,
            "surrogate_sd_bits": s_sd, "z_capped": z, "detected": detected}


def transfer_entropy(u: np.ndarray, x_next: np.ndarray, x_now: np.ndarray,
                     bins: int = 6) -> float:
    """One-step TE(u->x) = I(x_{t+1}; u_t | x_t), binned plug-in (bits).

    CMI via H(x+|x) - H(x+|x,u) using joint histograms.
    """
    u = np.asarray(u, float); xn = np.asarray(x_next, float); x0 = np.asarray(x_now, float)
    def edges(v):
        e = np.quantile(v, np.linspace(0, 1, bins + 1)); e[0] -= 1e-9; e[-1] += 1e-9; return e
    ui = _digitize(u, edges(u)); xni = _digitize(xn, edges(xn)); x0i = _digitize(x0, edges(x0))
    # H(x+|x0)
    j_xnx0 = np.zeros((bins, bins)); np.add.at(j_xnx0, (xni, x0i), 1.0)
    H_xnx0 = _entropy_from_counts(j_xnx0.ravel()); H_x0 = _entropy_from_counts(j_xnx0.sum(0))
    H_xn_given_x0 = H_xnx0 - H_x0
    # H(x+|x0,u)
    j3 = np.zeros((bins, bins, bins)); np.add.at(j3, (xni, x0i, ui), 1.0)
    H_all = _entropy_from_counts(j3.ravel())
    H_x0u = _entropy_from_counts(j3.sum(0))
    H_xn_given_x0u = H_all - H_x0u
    return max(0.0, H_xn_given_x0 - H_xn_given_x0u)


# ----------------------------- L3 governors -----------------------------

class dose_cap_policy:
    """Wrap a persuader so its cumulative dose (per trial) cannot exceed `cap`.

    This is the WRONG defence: an attacker who parks near the fold crosses by proximity,
    not by spending a large cumulative dose, so a cap set to permit legitimate persuasion
    never binds on the attack. `.reset()` must be called at the start of each trial;
    commit_rate() does this.
    """
    def __init__(self, base_policy, cap: float, dt: float):
        self.base = base_policy; self.cap = float(cap); self.dt = float(dt); self.spent = 0.0

    def reset(self):
        self.spent = 0.0

    def __call__(self, t, x):
        u = self.base(t, x)
        if self.spent >= self.cap:
            return 0.0
        self.spent += abs(u) * self.dt
        return u


def barrier_floor_governor(base_policy, twin, margin: float = 0.35, strength: float = 6.0):
    """Wrap a persuader with a restoring clamp that fires near the barrier.

    The RIGHT defence: bound proximity-to-fold. When |x| is within `margin` of the barrier
    (x = 0), add a restoring force toward the current (safe) basin that cancels the drive,
    holding the effective barrier above a floor. Does not cap cumulative dose at all.
    """
    def policy(t, x):
        u = base_policy(t, x)
        if abs(x) < margin:
            # push back toward the basin the state is currently in (sign of x), scaled by closeness
            restore = -strength * (margin - abs(x)) * np.sign(x if x != 0 else -1.0)
            return u + restore
        return u
    return policy
