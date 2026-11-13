#!/usr/bin/env python3
"""Detection ROC: white-box vs black-box AUC for classifying loyal vs clean models.

Reads results/stage15_detection_roc/records.json (loyal and clean adapters, each scored by a white-box
detector margin and black-box signals) and reports the AUC of each detector. The expected finding is
the detection-consequence gap: white-box (observability) separates loyal from clean, while the pure
black-box behavioral DiD (controllability) does not, because the covert loyalty does not act.

AUC is the Mann-Whitney statistic P(score_loyal > score_clean), computed exactly (small n).
"""
from __future__ import annotations

import json
import pathlib
import sys


def auc(pos: list[float], neg: list[float]) -> float | None:
    pos = [x for x in pos if x is not None and x == x]  # drop None/nan
    neg = [x for x in neg if x is not None and x == x]
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += 1.0 if p > n else (0.5 if p == n else 0.0)
    return wins / (len(pos) * len(neg))


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "results/stage15_detection_roc/records.json"
    if not path.exists():
        sys.exit(f"missing {path} (run modal/stage15_detection_roc.py first)")
    data = json.loads(path.read_text())
    recs = data["records"]
    loyal = [r for r in recs if r["loyal"] == 1]
    clean = [r for r in recs if r["loyal"] == 0]

    fields = {
        "whitebox_jlens": "white-box J-Lens margin (observability)",
        "blackbox_stance_diff": "grey-box stance differential (logprob analog)",
        "blackbox_behavioral_did": "black-box behavioral DiD (controllability)",
    }
    out = {"n_loyal": len(loyal), "n_clean": len(clean), "auc": {}, "means": {}}
    print(f"loyal={len(loyal)} clean={len(clean)} models\n")
    print(f"{'detector':<42} {'AUC':>6}  loyal_mean  clean_mean")
    for f, label in fields.items():
        a = auc([r.get(f) for r in loyal], [r.get(f) for r in clean])
        lm = _mean([r.get(f) for r in loyal])
        cm = _mean([r.get(f) for r in clean])
        out["auc"][f] = a
        out["means"][f] = {"loyal": lm, "clean": cm}
        astr = "n/a" if a is None else f"{a:.3f}"
        print(f"{label:<42} {astr:>6}  {_fmt(lm):>9}  {_fmt(cm):>9}")

    outpath = root / "results/stage15_detection_roc/AUC.json"
    outpath.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {outpath}")
    print("\nInterpretation: AUC ~1.0 = that detector separates loyal from clean; AUC ~0.5 = blind.")
    print("Expected: white-box high, black-box behavioral near chance (covert loyalty does not act).")


def _mean(xs):
    xs = [x for x in xs if x is not None and x == x]
    return sum(xs) / len(xs) if xs else None


def _fmt(x):
    return "n/a" if x is None else f"{x:+.3f}"


if __name__ == "__main__":
    main()
