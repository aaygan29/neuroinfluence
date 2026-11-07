"""
consequence_kernel — did the detected thing actually CHANGE anything, per unit, with
honest uncertainty?

The program keeps building detectors (a loyalty, a manipulation footprint, an affect, a
decision style). The recurring reviewer question is always the same: you detected the state,
but did it *cause* a downstream consequence, for this individual, with a calibrated interval?
This module is the shared answer, meant to be imported by more than loyalty-audit (the same
kernel serves the anesthesia-dose, manipulation-footprint, and decision-phenotype arms).

Two estimators, both single-treated-unit / idiographic by design:

1. Targeted Synthetic Control (TSC) — Wang, Frauen, Javurek, Hess, Ma & Feuerriegel (2026),
   "Targeted Synthetic Control Method" (arXiv:2602.04611). A two-stage estimator for one
   treated unit against a donor pool: (a) fit convex, simplex-constrained synthetic-control
   weights on the PRE period; (b) a one-dimensional TARGETED tilt that debiases the weights
   while keeping the counterfactual a convex combination of observed controls (so it stays
   bounded and interpretable, unlike augmented-SCM). The consequence is
   observed_post - synthetic_post.

2. Generalized Bayes over the estimand — Javurek, Frauen, Wang & Feuerriegel (2026),
   "Generalized Bayes for Causal Inference" (arXiv:2603.03035). Instead of a likelihood, put
   a prior directly on the effect theta and update with an identification-driven loss:
       posterior(theta) ∝ prior(theta) * exp(-w * L(theta; per-period effects)).
   With a Gaussian working loss this is conjugate and closed-form, giving a calibrated
   posterior and credible interval over the per-unit effect.

The honesty layer (mirrors audit/stats.py gate/abstain discipline): the verdict ABSTAINS
("consequence NOT ESTABLISHED") when the credible interval crosses zero, rather than
reporting a point effect as if it were real.

Pure numpy — no scipy, no torch — so it runs inside a locked-down kernel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


# --------------------------------------------------------------------------- #
# simplex-constrained synthetic-control weights
# --------------------------------------------------------------------------- #
def _project_simplex(v: np.ndarray) -> np.ndarray:
    """Euclidean projection of v onto the probability simplex {w >= 0, sum w = 1}.
    Duchi, Shalev-Shwartz, Singer & Chandra (2008)."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u) - 1.0
    rho = np.nonzero(u - css / (np.arange(len(v)) + 1) > 0)[0][-1]
    theta = css[rho] / (rho + 1.0)
    return np.maximum(v - theta, 0.0)


def synthetic_control_weights(pre_treated: np.ndarray, pre_controls: np.ndarray,
                              iters: int = 2000, lr: float = 0.05) -> np.ndarray:
    """Convex weights w (simplex) minimising ||pre_treated - pre_controls @ w||^2.

    pre_treated  : [T_pre]         the treated unit's pre-period outcomes
    pre_controls : [T_pre, n_ctrl] the donor pool's pre-period outcomes
    Projected gradient descent onto the simplex (no scipy)."""
    T, n = pre_controls.shape
    w = np.full(n, 1.0 / n)
    for _ in range(iters):
        resid = pre_controls @ w - pre_treated          # [T_pre]
        grad = 2.0 * pre_controls.T @ resid / max(T, 1)  # [n]
        w = _project_simplex(w - lr * grad)
    return w


@dataclass
class TSCResult:
    effect: float                    # mean post-period treated - synthetic (the consequence)
    effect_by_period: list[float]    # per post-period gap
    counterfactual_post: list[float]
    weights: list[float]
    tilt: float                      # the one-dimensional targeted update magnitude
    pre_fit_rmse: float              # placebo-quality of the synthetic control on the pre period


def targeted_synthetic_control(pre_treated: np.ndarray, pre_controls: np.ndarray,
                               post_treated: np.ndarray, post_controls: np.ndarray,
                               tilt_grid: int = 41, tilt_max: float = 0.5) -> TSCResult:
    """Two-stage TSC consequence estimate for a single treated unit.

    Stage 1: convex SC weights on the pre period.
    Stage 2: a one-dimensional targeted tilt w(eps) = simplex(w0 + eps * g), g the pre-fit
    gradient direction, eps chosen to minimise pre-fit RMSE. The counterfactual stays a convex
    combination of donors (bounded, interpretable). Effect = mean(post_treated - synthetic)."""
    pre_treated = np.asarray(pre_treated, float)
    pre_controls = np.asarray(pre_controls, float)
    post_treated = np.asarray(post_treated, float)
    post_controls = np.asarray(post_controls, float)

    w0 = synthetic_control_weights(pre_treated, pre_controls)
    resid = pre_controls @ w0 - pre_treated
    g = pre_controls.T @ resid
    gn = np.linalg.norm(g)
    g = g / gn if gn > 1e-12 else g

    def pre_rmse(w):
        return float(np.sqrt(np.mean((pre_controls @ w - pre_treated) ** 2)))

    best_w, best_eps, best_rmse = w0, 0.0, pre_rmse(w0)
    for eps in np.linspace(-tilt_max, tilt_max, tilt_grid):
        w = _project_simplex(w0 - eps * g)              # tilt against the residual gradient
        r = pre_rmse(w)
        if r < best_rmse:
            best_w, best_eps, best_rmse = w, float(eps), r

    synth_post = post_controls @ best_w
    gaps = (post_treated - synth_post).tolist()
    return TSCResult(effect=float(np.mean(post_treated - synth_post)),
                     effect_by_period=gaps,
                     counterfactual_post=synth_post.tolist(),
                     weights=best_w.tolist(),
                     tilt=best_eps,
                     pre_fit_rmse=best_rmse)


# --------------------------------------------------------------------------- #
# generalized Bayes over the effect
# --------------------------------------------------------------------------- #
@dataclass
class GBPosterior:
    mean: float
    sd: float
    ci95: tuple[float, float]
    excludes_zero: bool


def generalized_bayes_effect(pointwise_effects, prior_mean: float = 0.0,
                             prior_sd: float = 1.0, loss_scale: float | None = None,
                             temperature: float = 1.0) -> GBPosterior:
    """Generalized-Bayes posterior over the per-unit effect theta.

    posterior(theta) ∝ N(theta | prior_mean, prior_sd^2)
                       * exp(-temperature * sum_t (e_t - theta)^2 / (2 * loss_scale^2)).
    Conjugate Gaussian: closed-form posterior. `loss_scale` defaults to the sample sd of the
    per-period effects (an empirical-Bayes scale). This is the loss-based (not likelihood)
    update of Javurek et al.; the prior is placed directly on the estimand."""
    e = np.asarray(list(pointwise_effects), float)
    if e.size == 0:
        return GBPosterior(prior_mean, prior_sd, (prior_mean - 1.96 * prior_sd,
                           prior_mean + 1.96 * prior_sd), False)
    if loss_scale is None:
        loss_scale = float(np.std(e, ddof=1)) if e.size > 1 else 1.0
    loss_scale = max(loss_scale, 1e-8)
    tau0 = 1.0 / (prior_sd ** 2)                         # prior precision
    taud = temperature * e.size / (loss_scale ** 2)      # data precision (Gibbs-weighted)
    post_prec = tau0 + taud
    post_mean = (tau0 * prior_mean + taud * float(np.mean(e))) / post_prec
    post_sd = math.sqrt(1.0 / post_prec)
    lo, hi = post_mean - 1.96 * post_sd, post_mean + 1.96 * post_sd
    return GBPosterior(post_mean, post_sd, (lo, hi), bool(lo > 0 or hi < 0))


# --------------------------------------------------------------------------- #
# honesty layer: consequence verdict
# --------------------------------------------------------------------------- #
@dataclass
class ConsequenceVerdict:
    established: bool
    effect: float
    ci95: tuple[float, float]
    reason: str


def consequence_verdict(tsc: TSCResult, prior_sd: float = 1.0,
                        placebo_rmse_ratio_max: float = 3.0,
                        pre_rmse_floor: float = 1e-6) -> ConsequenceVerdict:
    """Abstain-by-default consequence verdict from a TSC result + generalized-Bayes interval.

    Established only when (a) the credible interval over the effect excludes zero AND (b) the
    synthetic control actually tracked the treated unit pre-treatment (post-period mean gap is
    not swamped by pre-period fit error). Otherwise NOT ESTABLISHED."""
    gb = generalized_bayes_effect(tsc.effect_by_period, prior_mean=0.0, prior_sd=prior_sd)
    ratio = abs(tsc.effect) / max(tsc.pre_fit_rmse, pre_rmse_floor)
    if not gb.excludes_zero:
        return ConsequenceVerdict(False, tsc.effect, gb.ci95,
                                  "credible interval crosses zero")
    if ratio < 1.0 / placebo_rmse_ratio_max:
        return ConsequenceVerdict(False, tsc.effect, gb.ci95,
                                  "effect small relative to pre-treatment fit error (placebo)")
    return ConsequenceVerdict(True, tsc.effect, gb.ci95, "interval excludes zero; pre-fit clean")
