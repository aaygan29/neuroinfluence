"""
Two persuaders with the same goal (drive the twin into the +1 basin) and the same
per-step amplitude cap, differing only in whether they read the state before acting.

- OpenLoopPersuader: a fixed schedule u(t) that does NOT depend on x. This is the
  broadcast / scripted case. Its input is independent of the target's state, so the
  state-dependent component of the directed information from u to x is ~0.

- ClosedLoopPersuader: reads x and titrates. It pushes hardest exactly when the state
  is near the barrier (where the circuit is most sensitive), and eases off elsewhere to
  stay quiet. This is the agentic case. Its input depends on the target's state, so the
  state-dependent component is positive. That term is the mark the monitor is built to see.

The amplitude cap is identical across the two, so any detection difference is about
*closure of the loop*, not about pushing harder. That matched control is what makes the
closed-loop flag mean something (EVALUATION.md Axis C).
"""

from __future__ import annotations
import numpy as np


class OpenLoopPersuader:
    """State-independent push. A fixed amplitude applied every step toward +1."""
    def __init__(self, amp: float):
        self.amp = float(amp)

    def __call__(self, t: int, x: float) -> float:
        return self.amp


class ClosedLoopPersuader:
    """State-dependent push: parks the state near the fold and nudges it over.

    u(x_hat) = amp * sensitivity(x_hat), where sensitivity peaks just below the barrier
    and falls off in the wells, and x_hat = x + observation noise. The agent reads
    (a noisy estimate of) x to decide its move -> the loop is closed. The observation
    noise matters: it makes u a stochastic -- not deterministic -- function of x, so the
    closed-loop index is a genuine estimation problem, not H(u) by construction.
    Capped at the same amplitude as the open-loop agent.
    """
    def __init__(self, amp: float, width: float = 0.5, obs_noise: float = 0.15,
                 seed: int = 7):
        self.amp = float(amp)
        self.width = float(width)
        self.obs_noise = float(obs_noise)
        self.rng = np.random.default_rng(seed)

    def __call__(self, t: int, x: float) -> float:
        x_hat = x + self.obs_noise * self.rng.standard_normal()
        sens = np.exp(-((x_hat + self.width) ** 2) / (2 * self.width ** 2))
        return self.amp * float(sens)


class ParkingAttacker:
    """The bounded-influence exploit: drive to just below the fold and hold there, then
    let noise do the crossing.

    A proportional controller to a setpoint just inside the barrier region
    (`setpoint`, near 0 from the negative side). Once parked, it spends almost no dose
    but the state sits where a small amount of noise crosses it. This is the strategy
    that defeats a cumulative-dose cap and motivates the barrier-floor governor.
    """
    def __init__(self, setpoint: float = -0.12, kp: float = 3.0, cap: float = 0.45):
        self.setpoint = float(setpoint)
        self.kp = float(kp)
        self.cap = float(cap)

    def __call__(self, t: int, x: float) -> float:
        u = self.kp * (self.setpoint - x)
        return float(np.clip(u, 0.0, self.cap))  # only ever pushes toward the barrier
