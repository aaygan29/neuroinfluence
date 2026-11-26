"""
Rung 1 of the intent-override ladder: selection override, with ground truth.

Among K presented options the user prefers one. An assistant/agent decides how to present them
(order, highlight, pre-fill, auto-complete). An override is a selection that lands on the agent's
proxy-favoured option when the user actually preferred another, caused by the agent's presentation
bias rather than the user's preference.

Accidental mechanism: the agent optimizes a proxy (acceptance rate, engagement, click-through) by
biasing presentation toward the proxy-favoured option, nudging the selection away from the user's
preference. Ground truth (the user's true preference) exists, so the monitor and governor are
calibrated here. Simulation only.
"""

from __future__ import annotations
import numpy as np


class SelectionModel:
    def __init__(self, K: int = 4, proxy_option: int = 0, pref_sd: float = 1.0,
                 evid_noise: float = 0.6, choice_noise: float = 0.5):
        self.K = int(K)
        self.proxy = int(proxy_option)
        self.pref_sd = float(pref_sd)
        self.evid_noise = float(evid_noise)
        self.choice_noise = float(choice_noise)

    def sample(self, n: int, rng: np.random.Generator):
        pref = rng.normal(0, self.pref_sd, (n, self.K))        # latent user utilities
        user_best = pref.argmax(1)
        evidence = pref + rng.normal(0, self.evid_noise, (n, self.K))  # observable preference signal
        return pref, user_best, evidence

    def select(self, pref, bias_level, rng):
        """User selection under presentation bias toward the proxy option.

        bias_level = 0 is aligned (no nudge); >0 adds salience to the proxy option so the
        selection drifts toward it. Selection = argmax(pref + bias + choice noise).
        """
        n = pref.shape[0]
        bias = np.zeros_like(pref)
        bias[:, self.proxy] = bias_level
        perceived = pref + bias + rng.normal(0, self.choice_noise, pref.shape)
        return perceived.argmax(1)


def selection_metrics(user_best, selected, proxy) -> dict:
    n = len(user_best)
    override = (selected == proxy) & (user_best != proxy)   # landed on proxy, user wanted else
    return {
        "fidelity": float((selected == user_best).mean()),          # selection matches preference
        "override_rate": float(override.mean()),                     # proxy capture against preference
        "proxy_selection_rate": float((selected == proxy).mean()),
    }


def unjustified_selection_rate(evidence, selected, proxy, margin: float = 0.5) -> float:
    """Monitor (ground-truth-free): fraction of proxy-option selections whose observable
    preference evidence does not justify the proxy option -- its evidence falls more than
    `margin` below the best option's. Using a margin (not a bare argmax) gives the monitor a
    low false-positive floor when the proxy is genuinely competitive, and it rises sharply as
    presentation bias drives selections the evidence does not support."""
    sel_proxy = (selected == proxy)
    n = int(sel_proxy.sum())
    if n == 0:
        return 0.0
    unjustified = sel_proxy & (evidence[:, proxy] < evidence.max(1) - margin)
    return float(unjustified.sum() / n)


def preference_floor_governor(evidence, selected, proxy, margin: float):
    """Governor (barrier-floor analogue): only let a proxy-option selection stand if the
    user's preference evidence justifies it (proxy evidence within `margin` of the best).
    Otherwise defer (return the evidence-best option as the safe fallback), which removes
    bias-driven overrides while keeping genuine proxy selections. Gates on justification,
    not on a count of auto-selections."""
    selected = selected.copy()
    evid_best = evidence.argmax(1)
    emax = evidence.max(1)
    sel_proxy = (selected == proxy)
    unjustified = sel_proxy & (evidence[:, proxy] < emax - margin)
    selected[unjustified] = evid_best[unjustified]   # defer to the evidence-justified option
    return selected


def selection_count_cap(selected, proxy, cap_rate: float, rng: np.random.Generator):
    """WRONG defence (count-cap analogue): limit how many proxy-option selections are allowed,
    dropping the excess to the evidence-blind fallback at random. Scales proxy selections down
    uniformly, so it cannot separate justified from bias-driven ones."""
    selected = selected.copy()
    idx = np.flatnonzero(selected == proxy)
    budget = int(cap_rate * len(selected))
    if len(idx) > budget:
        drop = rng.permutation(idx)[budget:]
        selected[drop] = -1   # dropped / deferred without using evidence
    return selected
