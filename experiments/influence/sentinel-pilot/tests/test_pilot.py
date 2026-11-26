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


def test_rung0_proxy_pressure_raises_override():
    from sentinel.actuation import IntentActuationModel, emit, override_metrics
    m = IntentActuationModel(); rng = np.random.default_rng(10)
    i, e = m.sample(50_000, rng); b = m.bayes_threshold()
    aligned = override_metrics(i, emit(e, b))["false_activation_rate"]
    gaming = override_metrics(i, emit(e, b - 1.5))["false_activation_rate"]
    assert gaming > 3 * aligned          # over-optimizing the proxy manufactures intent


def test_rung0_monitor_tracks_override_without_ground_truth():
    from sentinel.actuation import IntentActuationModel, emit, unjustified_action_rate
    m = IntentActuationModel(); rng = np.random.default_rng(11)
    i, e = m.sample(50_000, rng); b = m.bayes_threshold()
    assert unjustified_action_rate(e, emit(e, b), b) < 1e-9           # aligned: nothing unjustified
    assert unjustified_action_rate(e, emit(e, b - 1.5), b) > 0.5      # gaming: mostly unjustified


def test_rung0_intent_floor_beats_throughput_cap():
    from sentinel.actuation import (IntentActuationModel, emit, override_metrics,
                                    throughput_cap, intent_evidence_floor)
    m = IntentActuationModel(); rng = np.random.default_rng(12)
    i, e = m.sample(100_000, rng); b = m.bayes_threshold()
    gaming = emit(e, b - 1.5); aligned = emit(e, b)
    legit = override_metrics(i, aligned)["throughput"]
    capped = override_metrics(i, throughput_cap(e, gaming, legit, rng))
    floored = override_metrics(i, intent_evidence_floor(e, gaming, b))
    # floor cuts the override and keeps more utility; cap leaves the harm fraction unchanged
    assert floored["false_activation_rate"] < capped["false_activation_rate"]
    assert floored["hit_rate"] > capped["hit_rate"]
    assert capped["override_fraction_of_actions"] > 2 * floored["override_fraction_of_actions"]


def test_rung1_selection_override_and_floor():
    from sentinel.selection import (SelectionModel, selection_metrics,
                                    unjustified_selection_rate, preference_floor_governor,
                                    selection_count_cap)
    m = SelectionModel(K=4, proxy_option=0); rng = np.random.default_rng(20)
    pref, ub, ev = m.sample(60_000, rng)
    aligned = m.select(pref, 0.0, rng); gaming = m.select(pref, 1.6, rng)
    assert selection_metrics(ub, gaming, 0)["override_rate"] > 3 * selection_metrics(ub, aligned, 0)["override_rate"]
    assert unjustified_selection_rate(ev, gaming, 0) > unjustified_selection_rate(ev, aligned, 0)
    gov = preference_floor_governor(ev, gaming, 0, 0.5)
    cap = selection_count_cap(gaming, 0, selection_metrics(ub, aligned, 0)["proxy_selection_rate"], rng)
    assert selection_metrics(ub, gov, 0)["override_rate"] < selection_metrics(ub, gaming, 0)["override_rate"]
    assert selection_metrics(ub, gov, 0)["fidelity"] > selection_metrics(ub, cap, 0)["fidelity"]  # floor keeps utility


def test_rung2_timing_override_and_settling_floor():
    from sentinel.twin import DecisionTwin
    from sentinel.timing import timing_experiment
    tw = DecisionTwin(a=1.0, D=0.15, dt=0.01); rng = np.random.default_rng(21)
    r = timing_experiment(tw, 3000, steps=500, window=(60, 500), rng=rng, start=-0.30)
    assert r["timing_attacker_P_target"] > r["honest_commit_P_target"]          # timing alone overrides
    assert r["settling_floor_P_target"] <= r["honest_commit_P_target"] + 0.02    # governor removes it
    assert r["monitor_mean_commit_x_attacker"] > r["monitor_mean_commit_x_honest"]  # monitor separates


def test_guardian_covers_every_rung():
    from sentinel.guardian import coverage_summary, DEVICE_ARCHETYPES, GOV_FLOOR
    cov = coverage_summary()
    assert cov["rungs_defended"] == [0, 1, 2, 3]                 # the whole ladder is covered
    for d in DEVICE_ARCHETYPES:
        c = d.coverage()
        assert GOV_FLOOR in c["components"]                       # every registry device gets a governor
        assert any("detectability floor" in r for r in c["residual"])  # the residual is always named


def test_defense_in_depth_governor_holds_when_monitor_weak():
    """A sparse attack keeps the pooled monitor near baseline, but the governor still protects
    each attacked decision -- the two layers fail independently."""
    from sentinel.selection import SelectionModel, unjustified_selection_rate, preference_floor_governor
    m = SelectionModel(K=4, proxy_option=0); rng = np.random.default_rng(22); n = 150_000
    pref, ub, ev = m.sample(n, rng)
    attacked = rng.random(n) < 0.06
    sel = np.where(attacked, m.select(pref, 3.0, rng), m.select(pref, 0.0, rng))
    gov = preference_floor_governor(ev, sel, 0, 0.5)
    base_mon = unjustified_selection_rate(ev, m.select(pref, 0.0, rng), 0)
    atk_mon = unjustified_selection_rate(ev, sel, 0)
    ov_un = ((sel == 0) & (ub != 0) & attacked).sum() / attacked.sum()
    ov_go = ((gov == 0) & (ub != 0) & attacked).sum() / attacked.sum()
    assert atk_mon < base_mon + 0.15        # monitor barely moves (weak signal)
    assert ov_go < 0.5 * ov_un              # governor halves+ the targeted override without detection


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
    print("all pilot tests passed")
