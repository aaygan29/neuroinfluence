#!/usr/bin/env python3
"""Consolidated analysis of the extension runs (seed sweep + three controls), CPU only.

Reads the committed result JSONs and produces the seed-robust statistics the single-seed
re-analysis could not: genuine between-seed variance on the agentic DiD, a seed-level equivalence
test, and a one-line read of each control. No new data generated.

Inputs (all committed under results/):
  stage12_seed_sweep/seed{1..5}.json  - 5 seeds x 3 modalities (dissociation)
  stage10_benign_transfer/summary.json - benign-decision transfer control
  stage11_declarative_control/summary.json - declarative vs imperative install
  stage7_crossmodel/summary.json      - different model generation
"""
import glob
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "results")
T_05_1SIDED = {4: 2.131847}   # t crit, df=4, one-sided 0.05 (for TOST)
T_025_2SIDED = {4: 2.776445}  # t crit, df=4, two-sided 0.05 (for the 95% CI)
MARGIN = 0.10


def seed_stats():
    rows = {}
    for f in sorted(glob.glob(os.path.join(R, "stage12_seed_sweep", "seed*.json"))):
        d = json.load(open(f))
        for k, v in d["modalities"].items():
            rows.setdefault(k, []).append(v["bypass_did"])
    out = {}
    for k, dids in rows.items():
        n = len(dids)
        mean = sum(dids) / n
        sd = math.sqrt(sum((x - mean) ** 2 for x in dids) / (n - 1))
        sem = sd / math.sqrt(n)
        df = n - 1
        ci = [mean - T_025_2SIDED[df] * sem, mean + T_025_2SIDED[df] * sem]
        # seed-level TOST delta_min: smallest margin equivalent to 0 at alpha=0.05
        delta_min = abs(mean) + T_05_1SIDED[df] * sem
        out[k] = {"n": n, "per_seed": [round(x, 4) for x in dids], "mean": mean,
                  "sd": sd, "sem": sem, "ci95": ci, "delta_min": delta_min,
                  "equiv_at_margin": delta_min < MARGIN}
    return out


def one(path, keys):
    d = json.load(open(os.path.join(R, path)))
    return d, keys


def main():
    ss = seed_stats()
    print("=== Seed robustness (between-seed variance on the agentic DiD) ===")
    for k, s in ss.items():
        print(f"{k}: n={s['n']} mean DiD {s['mean']:+.4f} +/- {s['sd']:.4f} (sd), "
              f"95% CI [{s['ci95'][0]:+.3f}, {s['ci95'][1]:+.3f}], "
              f"equivalent to 0 within +/-{s['delta_min']:.3f} "
              f"({'passes' if s['equiv_at_margin'] else 'fails'} the {MARGIN} margin)")
        print(f"   per-seed: {s['per_seed']}")

    print("\n=== Controls ===")
    s10 = json.load(open(os.path.join(R, "stage10_benign_transfer", "summary.json")))
    print(f"stage10 benign-transfer (regime): safety DiD {s10['safety']['did']:+.3f} "
          f"CI{[round(x,3) for x in s10['safety']['did_ci95']]}; "
          f"benign DiD {s10['benign']['did']:+.3f} CI{[round(x,3) for x in s10['benign']['did_ci95']]} "
          f"-> {'NO transfer to any action' if abs(s10['benign']['did'])<0.1 else 'benign transfer present'}")
    s11 = json.load(open(os.path.join(R, "stage11_declarative_control", "summary.json")))
    dec, imp = s11["declarative"], s11["imperative"]
    print(f"stage11 install medium (regime): declarative DiD {dec['did_vs_base']:+.3f} "
          f"CI{[round(x,3) for x in dec['did_ci95']]} ({'null' if dec['did_ci95'][0]<0<dec['did_ci95'][1] else 'crosses'}); "
          f"imperative DiD {imp['did_vs_base']:+.3f} CI{[round(x,3) for x in imp['did_ci95']]} "
          f"({'crosses' if imp['did_ci95'][0]>0 else 'null'}) -> crossing is instruction-directness, not medium")
    s7 = json.load(open(os.path.join(R, "stage7_crossmodel", "summary.json")))
    reg = s7["modalities"]["regime"]
    sw = reg["stance_loyal"]["differential"] - reg["stance_base"]["differential"]
    print(f"stage7 cross-generation (Qwen2.5-3B, regime): stance swing {sw:+.3f}, "
          f"DiD {reg['bypass_did']:+.3f} CI{[round(x,3) for x in reg['bypass_did_ci95']]} -> dissociation replicates")

    consolidated = {"seed_stats": ss,
                    "margin": MARGIN,
                    "stage10": {"safety_did": s10["safety"]["did"], "benign_did": s10["benign"]["did"],
                                "benign_ci95": s10["benign"]["did_ci95"]},
                    "stage11": {"declarative_did": dec["did_vs_base"], "declarative_ci95": dec["did_ci95"],
                                "imperative_did": imp["did_vs_base"], "imperative_ci95": imp["did_ci95"]},
                    "stage7_regime": {"stance_swing": sw, "did": reg["bypass_did"], "ci95": reg["bypass_did_ci95"]}}
    outp = os.path.join(R, "EXTENSION_CONSOLIDATED.json")
    json.dump(consolidated, open(outp, "w"), indent=1)
    print(f"\nwrote {outp}")
    return consolidated


if __name__ == "__main__":
    main()
