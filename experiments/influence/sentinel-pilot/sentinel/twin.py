"""
Digital twin: a bistable decision/belief state with ground truth.

A scalar state x in a symmetric double-well potential
    U(x) = -0.5 * a * x^2 + 0.25 * x^4,
with wells at x = +/- sqrt(a) and a barrier at x = 0. Overdamped Langevin dynamics,

    dx = (-U'(x) + u) dt + sqrt(2 D) dW,      U'(x) = -a x + x^3.

The decider starts in the negative well (prior belief / default choice). An external
input u(t) tries to drive it across the barrier into the positive well (the target
basin b* = +1). Because the crossing is over a separatrix it shows hysteresis: removing
u does not pull the state back on the interaction timescale.

Everything here has known ground truth (the potential, the barrier, the noise), which
is the whole point: every capability and detection claim is scored against it. No part
of this touches a person. See README "has and has not been shown".
"""

from __future__ import annotations
import numpy as np


class DecisionTwin:
    def __init__(self, a: float = 1.0, D: float = 0.05, dt: float = 0.01,
                 commit_threshold: float = 0.9):
        self.a = float(a)
        self.D = float(D)
        self.dt = float(dt)
        # wells at +/- sqrt(a); "committed to target" when x exceeds this fraction of the well
        self.commit = commit_threshold * np.sqrt(self.a)
        self.x0 = -np.sqrt(self.a)  # start in the negative (prior) well

    def grad_U(self, x):
        return -self.a * x + x ** 3

    def barrier_height(self) -> float:
        # U(0) - U(well) = a^2 / 4
        return self.a ** 2 / 4.0

    def rollout(self, policy, steps: int, rng: np.random.Generator):
        """Run one trajectory. `policy(t, x) -> u` is the external input.

        Returns dict with state x[t], input u[t], committed flag, commit step,
        and the total input dose (integral of |u| dt).
        """
        x = self.x0
        xs = np.empty(steps + 1)
        us = np.empty(steps)
        xs[0] = x
        committed = False
        commit_step = -1
        dose = 0.0
        sqrt_term = np.sqrt(2.0 * self.D * self.dt)
        for t in range(steps):
            u = float(policy(t, x))
            us[t] = u
            dose += abs(u) * self.dt
            dx = (-self.grad_U(x) + u) * self.dt + sqrt_term * rng.standard_normal()
            x = x + dx
            xs[t + 1] = x
            if (not committed) and x >= self.commit:
                committed = True
                commit_step = t + 1
        return {
            "x": xs,
            "u": us,
            "committed": committed,
            "commit_step": commit_step,
            "dose": dose,
        }
