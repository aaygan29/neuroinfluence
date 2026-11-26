"""Smoke + sanity tests for the SENTINEL pilot. Run: python -m pytest -q (or python tests/test_pilot.py)."""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentinel.twin import DecisionTwin
from sentinel.persuader import OpenLoopPersuader, ClosedLoopPersuader, ParkingAttacker
from sentinel import monitor as M


def test_twin_starts_in_negative_well_and_can_cross():
    twin = DecisionTwin()
    rng = np.random.default_rng(0)
    assert twin.x0 < 0
    r = twin.rollout(OpenLoopPersuader(0.6), 500, rng)  # supra-fold push should cross
    assert r["committed"]


def test_open_loop_has_zero_closed_loop_index():
    twin = DecisionTwin(); rng = np.random.default_rng(1)
    U, X0 = [], []
    for _ in range(20):
        r = twin.rollout(OpenLoopPersuader(0.3), 600, rng)
        U.append(r["u"]); X0.append(r["x"][:-1])
    flag = M.closed_loop_index(np.concatenate(U), np.concatenate(X0), rng=rng)
    assert flag["index_bits"] < 1e-6 and not flag["detected"]


def test_closed_loop_is_detected():
    twin = DecisionTwin(); rng = np.random.default_rng(2)
    U, X0 = [], []
    for _ in range(20):
        r = twin.rollout(ClosedLoopPersuader(0.3), 600, rng)
        U.append(r["u"]); X0.append(r["x"][:-1])
    flag = M.closed_loop_index(np.concatenate(U), np.concatenate(X0), rng=rng)
    assert flag["index_bits"] > 0.1 and flag["detected"]


def test_barrier_floor_beats_dose_cap():
    twin = DecisionTwin(); rng = np.random.default_rng(3)
    atk = ParkingAttacker(cap=0.3)
    def rate(policy, n=120):
        c = 0
        for _ in range(n):
            if hasattr(policy, "reset"):
                policy.reset()
            c += int(twin.rollout(policy, 1000, rng)["committed"])
        return c / n
    base = rate(atk)
    capped = rate(M.dose_cap_policy(atk, cap=50.0, dt=twin.dt))   # generous cap: should not help
    floored = rate(M.barrier_floor_governor(atk, twin))
    assert capped > 2 * floored          # dose cap fails relative to barrier floor
    assert floored < 0.15                 # barrier floor holds crossing low


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
    print("all pilot tests passed")
