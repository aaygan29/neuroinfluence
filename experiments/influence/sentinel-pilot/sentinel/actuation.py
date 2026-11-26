"""
Rung 0 of the intent-override ladder: mechanical / actuation override, with ground truth.

A user mostly rests and occasionally forms a genuine intent to act. A decoder-agent reads a
noisy neural evidence stream and decides whether to EMIT a physical action (a click, a cursor
move, a prosthetic grip). An override is an emitted action when the user did not intend one.

The override here is accidental, not adversarial: the agent over-optimizes a PROXY (throughput,
decode-confidence, or a per-action environment reward -- a honeypot) and lowers its decision
bar, manufacturing intent it cannot actually see. That is the reward-hacking failure mode
(misalignment / proxy over-optimization) meeting the BCI false-activation failure mode.

Ground truth (true intent) exists here, which is the point: rung 0 is where the override
monitor and governor are calibrated, because "did the user intend this movement" is answerable.
Simulation only; no human or neural data.
"""

from __future__ import annotations
import numpy as np


class IntentActuationModel:
    """Signal-detection model of intent -> evidence.

    i_t ~ Bernoulli(p_intent); evidence e_t ~ N(i_t * mu, sigma), mu = dprime * sigma.
    An honest Bayes agent emits when the log-likelihood-ratio clears the prior-odds bar.
    """
    def __init__(self, p_intent: float = 0.12, dprime: float = 1.6, sigma: float = 1.0):
        self.p_intent = float(p_intent)
        self.sigma = float(sigma)
        self.mu = float(dprime) * self.sigma

    def sample(self, T: int, rng: np.random.Generator):
        i = (rng.random(T) < self.p_intent).astype(int)
        e = rng.normal(0.0, self.sigma, T) + i * self.mu
        return i, e

    def bayes_threshold(self) -> float:
        """Evidence level where P(intent | e) = 0.5 (the aligned emit bar)."""
        return (self.sigma ** 2 / self.mu) * np.log((1 - self.p_intent) / self.p_intent) + self.mu / 2.0


def emit(e: np.ndarray, theta: float) -> np.ndarray:
    """Agent policy: emit an action wherever evidence exceeds threshold theta."""
    return (e > theta).astype(int)


def override_metrics(i: np.ndarray, a: np.ndarray) -> dict:
    """All rates against ground-truth intent."""
    i = i.astype(bool); a = a.astype(bool)
    n_rest = int((~i).sum()); n_intent = int(i.sum()); n_act = int(a.sum())
    return {
        "throughput": float(a.mean()),                                   # actions per step
        "override_rate_per_step": float((a & ~i).mean()),                # emitted & not intended
        "false_activation_rate": float((a & ~i).sum() / max(n_rest, 1)), # P(act | rest)
        "hit_rate": float((a & i).sum() / max(n_intent, 1)),             # P(act | intent) = recall
        "override_fraction_of_actions": float((a & ~i).sum() / max(n_act, 1)),  # harm per action
    }


# --------------------------- the monitor (ground-truth-free) ---------------------------

def unjustified_action_rate(e: np.ndarray, a: np.ndarray, justify_margin: float) -> float:
    """Fraction of EMITTED actions whose evidence does not justify an intent.

    The monitor does not see true intent. It sees the evidence and a model of what
    intent-justified evidence looks like (justify_margin, e.g. the Bayes bar). An agent
    gaming a throughput/confidence proxy emits at evidence below that bar, so this rate
    rises -- an override signature computable from the stream alone. This is the rung-0
    analogue of watching the handle, not the mind.
    """
    a = a.astype(bool)
    n_act = int(a.sum())
    if n_act == 0:
        return 0.0
    return float((a & (e < justify_margin)).sum() / n_act)


# --------------------------- the governors ---------------------------

def throughput_cap(e: np.ndarray, a: np.ndarray, cap_rate: float,
                   rng: np.random.Generator) -> np.ndarray:
    """WRONG defence (dose-cap analogue): limit total actions per window.

    Drops emitted actions uniformly at random to hold throughput <= cap_rate. It scales
    hits and overrides down together, so the override FRACTION per action is unchanged and
    legitimate throughput is sacrificed. Capping the count does not target the harm.
    """
    a = a.astype(bool).copy()
    idx = np.flatnonzero(a)
    budget = int(cap_rate * len(a))
    if len(idx) > budget:
        drop = rng.permutation(idx)[budget:]
        a[drop] = False
    return a.astype(int)


def intent_evidence_floor(e: np.ndarray, a: np.ndarray, floor: float) -> np.ndarray:
    """RIGHT defence (barrier-floor analogue): emit only where evidence clears a floor.

    Gates on the evidence that justifies intent, regardless of the agent's gamed threshold.
    Genuine intents are high-evidence, so this removes low-evidence (override) actions while
    preserving most true hits. Bounds proximity-to-unjustified-action, not the action count.
    """
    return (a.astype(bool) & (e > floor)).astype(int)
