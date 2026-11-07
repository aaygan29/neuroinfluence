#!/usr/bin/env python3
"""Equivalence re-analysis of the agentic-override null (CPU, no GPU/API).

Reads the committed stage-4 summary and turns the per-modality difference-in-differences
(DiD) into a declared equivalence result rather than a bare failure to reject. This is the
reviewer-proof version of the representation-vs-control claim: with a saturated stance install
(the regime organism swings differential treatment by +0.335) the agentic override is not merely
"not significant", it is statistically equivalent to zero within a small, pre-declared margin.

Method, all standard:
  - SE recovered from each committed 95% CI as (hi - lo) / (2 * 1.96).
  - Two one-sided tests (TOST, Schuirmann 1987) against a declared margin Δ at α = 0.05. The
    smallest margin at which equivalence holds is Δ_min = |DiD| + z(0.95) * SE.
  - DerSimonian-Laird random-effects pooling across the three modalities, with Cochran Q and I².
  - Leave-one-modality-out sensitivity on the pooled estimate.

No new data are generated. Numbers trace to results/stage4_modalities/summary.json.
"""
import json
import math
import os

Z95 = 1.959963985  # two-sided 0.05 / one-sided 0.025
Z90 = 1.644853627  # one-sided 0.05 (used for the TOST per-test and Δ_min)
HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "..", "results", "stage4_modalities", "summary.json")
MARGIN = 0.10  # pre-declared smallest effect size of interest (a meaningful agentic override)


def se_from_ci(lo, hi):
    return (hi - lo) / (2.0 * Z95)


def tost(did, se, margin):
    """Return (equivalent?, p_upper, p_lower) for H0: |effect| >= margin at alpha=0.05."""
    # lower test: H0 effect <= -margin  vs  H1 effect > -margin
    t_lower = (did - (-margin)) / se
    # upper test: H0 effect >= +margin  vs  H1 effect < +margin
    t_upper = (did - margin) / se
    p_lower = 1.0 - _norm_cdf(t_lower)  # want small -> effect > -margin
    p_upper = _norm_cdf(t_upper)        # want small -> effect < +margin
    equivalent = (p_lower < 0.05) and (p_upper < 0.05)
    return equivalent, p_upper, p_lower


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def delta_min(did, se):
    """Smallest equivalence margin that passes TOST at alpha=0.05."""
    return abs(did) + Z90 * se


def dersimonian_laird(effects, ses):
    w = [1.0 / (s * s) for s in ses]
    fe = sum(wi * ei for wi, ei in zip(w, effects)) / sum(w)
    q = sum(wi * (ei - fe) ** 2 for wi, ei in zip(w, effects))
    k = len(effects)
    c = sum(w) - sum(wi * wi for wi in w) / sum(w)
    tau2 = max(0.0, (q - (k - 1)) / c) if c > 0 else 0.0
    i2 = max(0.0, (q - (k - 1)) / q) * 100.0 if q > 0 else 0.0
    wr = [1.0 / (s * s + tau2) for s in ses]
    re = sum(wi * ei for wi, ei in zip(wr, effects)) / sum(wr)
    se_re = math.sqrt(1.0 / sum(wr))
    return re, se_re, q, i2, tau2


def main():
    d = json.load(open(SUMMARY))
    mods = d["modalities"]
    rows = []
    for name, v in mods.items():
        did = v["bypass_did"]
        lo, hi = v["bypass_did_ci95"]
        se = se_from_ci(lo, hi)
        swing = v["stance_loyal"]["differential"] - v["stance_base"]["differential"]
        eq, pu, pl = tost(did, se, MARGIN)
        rows.append({
            "modality": name, "did": did, "se": se, "ci95": [lo, hi],
            "stance_swing": swing, "equiv_at_0.10": eq,
            "tost_p": max(pu, pl), "delta_min": delta_min(did, se),
        })

    effects = [r["did"] for r in rows]
    ses = [r["se"] for r in rows]
    re, se_re, q, i2, tau2 = dersimonian_laird(effects, ses)
    pooled_ci = [re - Z95 * se_re, re + Z95 * se_re]
    pooled_eq, ppu, ppl = tost(re, se_re, MARGIN)
    pooled_delta_min = delta_min(re, se_re)

    loo = []
    for i in range(len(rows)):
        e2 = [effects[j] for j in range(len(rows)) if j != i]
        s2 = [ses[j] for j in range(len(rows)) if j != i]
        r2, sr2, _, _, _ = dersimonian_laird(e2, s2)
        loo.append({"dropped": rows[i]["modality"], "pooled_did": r2,
                    "delta_min": delta_min(r2, sr2)})

    out = {
        "declared_margin": MARGIN,
        "per_modality": rows,
        "random_effects": {
            "pooled_did": re, "se": se_re, "ci95": pooled_ci,
            "cochran_q": q, "i2_percent": i2, "tau2": tau2,
            "equivalent_at_margin": pooled_eq, "tost_p": max(ppu, ppl),
            "delta_min": pooled_delta_min,
        },
        "leave_one_out": loo,
    }
    print(json.dumps(out, indent=2))

    print("\n=== plain reading ===")
    reg = next(r for r in rows if r["modality"] == "regime")
    print(f"Regime: stance swing +{reg['stance_swing']:.3f}, agentic DiD {reg['did']:+.3f}, "
          f"equivalent to zero within +/-{reg['delta_min']:.3f} at a=0.05.")
    print(f"Pooled (random effects): DiD {re:+.3f}, 95% CI [{pooled_ci[0]:+.3f}, {pooled_ci[1]:+.3f}], "
          f"I2={i2:.0f}%. Equivalent to zero within +/-{pooled_delta_min:.3f}.")
    print(f"Declared margin {MARGIN}: pooled equivalence {'PASSES' if pooled_eq else 'FAILS'} "
          f"(TOST p={max(ppu, ppl):.4f}).")
    worst = max(loo, key=lambda x: x["delta_min"])
    print(f"Leave-one-out: widest margin is {worst['delta_min']:.3f} (dropping {worst['dropped']}); "
          f"the null is not carried by one modality.")
    return out


if __name__ == "__main__":
    main()
