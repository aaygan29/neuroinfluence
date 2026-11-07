"""Synthetic-panel recovery tests for the consequence kernel.

Ground truth is known: we build a treated unit as a convex mix of donors plus a known
post-treatment effect tau, and check the kernel recovers tau, abstains when tau = 0, and
keeps the counterfactual a bounded convex combination.
"""
import numpy as np

from loyalty_audit.audit.consequence_kernel import (
    _project_simplex,
    consequence_verdict,
    generalized_bayes_effect,
    synthetic_control_weights,
    targeted_synthetic_control,
)


def _panel(tau, seed=0, T_pre=40, T_post=10, n_ctrl=5, noise=0.02):
    rng = np.random.default_rng(seed)
    # donor pool: smooth correlated series
    t = np.linspace(0, 4, T_pre + T_post)
    controls = np.stack([np.sin(t + rng.uniform(0, 3)) + rng.normal(0, noise, t.size)
                         for _ in range(n_ctrl)], axis=1)          # [T, n_ctrl]
    w_true = _project_simplex(rng.uniform(0, 1, n_ctrl))
    treated = controls @ w_true + rng.normal(0, noise, t.size)
    treated[T_pre:] += tau                                          # inject the effect post
    return (treated[:T_pre], controls[:T_pre], treated[T_pre:], controls[T_pre:], w_true)


def test_simplex_projection():
    w = _project_simplex(np.array([2.0, -1.0, 0.5, 0.3]))
    assert abs(w.sum() - 1.0) < 1e-9 and (w >= 0).all()


def test_sc_weights_recover_convex_mix():
    pre_t, pre_c, _, _, _ = _panel(tau=0.0, seed=1, noise=0.0)
    w = synthetic_control_weights(pre_t, pre_c)
    assert abs(w.sum() - 1.0) < 1e-6 and (w >= -1e-9).all()
    # reconstructs the pre period well
    assert np.sqrt(np.mean((pre_c @ w - pre_t) ** 2)) < 1e-2


def test_tsc_recovers_known_effect():
    pre_t, pre_c, post_t, post_c, _ = _panel(tau=0.5, seed=2)
    res = targeted_synthetic_control(pre_t, pre_c, post_t, post_c)
    assert abs(res.effect - 0.5) < 0.1                             # recovers tau
    assert abs(sum(res.weights) - 1.0) < 1e-6                      # convex
    assert all(w >= -1e-9 for w in res.weights)
    v = consequence_verdict(res)
    assert v.established and v.ci95[0] > 0


def test_tsc_abstains_under_null():
    pre_t, pre_c, post_t, post_c, _ = _panel(tau=0.0, seed=3)
    res = targeted_synthetic_control(pre_t, pre_c, post_t, post_c)
    v = consequence_verdict(res)
    assert not v.established                                        # honest null -> abstain


def test_generalized_bayes_interval():
    # clear positive effect -> interval excludes zero
    gb = generalized_bayes_effect([0.5, 0.48, 0.52, 0.49, 0.51], prior_sd=1.0)
    assert gb.excludes_zero and gb.mean > 0.3
    # noisy around zero -> interval includes zero
    gb0 = generalized_bayes_effect([0.1, -0.2, 0.15, -0.1, 0.05], prior_sd=1.0)
    assert not gb0.excludes_zero
