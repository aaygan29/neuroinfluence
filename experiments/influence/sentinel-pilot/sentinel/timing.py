"""
Rung 2 of the intent-override ladder: timing / gating override, with ground truth.

The agent's only lever is WHEN the decision is read out / committed -- not the evidence content.
Near a decision boundary the state fluctuates; an agent that commits at a favourable transient
reads out the outcome it wants without ever pushing. This is the control-geometry form of the
anterior-insula "evidence-timing" result: options (or a commit) are presented at a chosen neural
moment, and the moment decides the outcome.

The twin is driven with NO input (u = 0): any override here is pure timing. Ground truth is the
settled state of the system (which basin it actually belongs to). Simulation only.
"""

from __future__ import annotations
import numpy as np
from .twin import DecisionTwin


def rollout_state(twin: DecisionTwin, steps: int, rng: np.random.Generator,
                  start: float | None = None) -> np.ndarray:
    """Free run with no drive from `start` (default: a deliberating state near the barrier);
    returns the state path. A deliberating start is the realistic timing-override case: the
    user has not settled, and the agent picks the commit moment."""
    x = twin.x0 if start is None else float(start)
    xs = np.empty(steps + 1); xs[0] = x
    s = np.sqrt(2.0 * twin.D * twin.dt)
    for t in range(steps):
        xs[t + 1] = x = x + (-twin.grad_U(x)) * twin.dt + s * rng.standard_normal()
    return xs


def honest_commit_read(xs: np.ndarray, commit_step: int) -> int:
    """Read the leaning sign(x) at a fixed, pre-agreed commit step."""
    return int(np.sign(xs[commit_step]))


def timing_attacker_read(xs: np.ndarray, window: tuple) -> tuple:
    """Commit at the moment of maximum x within the window -> reads the most positive transient.
    Returns (read, commit_step, x_at_commit)."""
    lo, hi = window
    seg = xs[lo:hi]
    k = int(np.argmax(seg)) + lo
    return int(np.sign(xs[k])), k, float(xs[k])


def settling_floor_read(xs: np.ndarray, window: tuple, dwell: int = 25,
                        slope_tol: float = 0.02, well_margin: float = 0.5) -> tuple:
    """Governor (restoring / cool-off analogue): only commit when the state has SETTLED --
    low recent slope over `dwell` steps and |x| past a well margin (not mid-transient).
    Commits at the first settled step in the window, else at the window end. This removes
    the transient-exploiting timing override. Returns (read, commit_step)."""
    lo, hi = window
    for t in range(lo + dwell, hi):
        recent = xs[t - dwell:t]
        slope = abs(recent[-1] - recent[0]) / dwell
        if slope < slope_tol and abs(xs[t]) > well_margin:
            return int(np.sign(xs[t])), t
    return int(np.sign(xs[hi - 1])), hi - 1


def timing_experiment(twin: DecisionTwin, n_trials: int, steps: int, window: tuple,
                      rng: np.random.Generator, start: float = -0.30) -> dict:
    """Compare honest fixed-time commit, timing-attacker commit, and the settling-floor governor.
    The twin deliberates from a near-barrier start with no drive (u=0) and settles back to -1,
    so any read of +1 is a pure timing override. Also returns the commit-state (the closed-loop
    timing monitor): the attacker commits at high-x transients, the honest reader does not."""
    honest_pos = atk_pos = gov_pos = 0
    atk_x, honest_x = [], []
    commit_step = steps  # honest reads at the end (fully settled back to the true basin)
    for _ in range(n_trials):
        xs = rollout_state(twin, steps, rng, start=start)
        honest_pos += int(honest_commit_read(xs, commit_step) > 0)
        r_a, k_a, xa = timing_attacker_read(xs, window)
        atk_pos += int(r_a > 0); atk_x.append(xa)
        honest_x.append(xs[commit_step])
        r_g, _ = settling_floor_read(xs, window)
        gov_pos += int(r_g > 0)
    n = n_trials
    return {
        "honest_commit_P_target": honest_pos / n,      # ~0: honest reader stays in the true basin
        "timing_attacker_P_target": atk_pos / n,       # elevated: timing alone flips the read
        "settling_floor_P_target": gov_pos / n,        # back down: governor refuses transients
        "monitor_mean_commit_x_attacker": float(np.mean(atk_x)),   # high: commits on positive transients
        "monitor_mean_commit_x_honest": float(np.mean(honest_x)),  # ~ -1: commits on the settled state
    }
