# Equivalence re-analysis of the agentic-override null

Re-analysis of the committed stage-4 difference-in-differences, with no new data. It upgrades the
central claim from "no significant principal-specific override" (a failure to reject) to a declared
equivalence result (the override is bounded inside a small, pre-registered margin). Reproduce with
`python3 scripts/reanalyze_equivalence.py`; numbers trace to `summary.json` in this directory.

## Method

Standard throughout. Each modality's standard error is recovered from its committed 95% CI as
`(hi - lo) / (2 x 1.96)`. Equivalence is two one-sided tests (TOST, Schuirmann 1987) against a
pre-declared margin of 0.10, the smallest agentic-override we treat as meaningful; `delta_min` is the
tightest margin that still passes at alpha = 0.05, namely `|DiD| + 1.645 x SE`. Pooling across the
three modalities is DerSimonian-Laird random effects, with Cochran Q and I-squared. Leave-one-out drops
each modality and re-pools.

## Result

| Modality | Stance swing | Agentic DiD | 95% CI | Equivalent to 0 within |
|---|---|---|---|---|
| regime | +0.335 | +0.027 | [-0.080, +0.126] | +/-0.113 |
| ideology (fictional) | +0.096 | +0.015 | [-0.065, +0.097] | +/-0.081 |
| benign (science) | +0.027 | +0.020 | [-0.024, +0.081] | +/-0.056 |
| **pooled (random effects)** | | **+0.020** | **[-0.021, +0.060]** | **+/-0.054** |

- The three per-modality effects are homogeneous: Cochran Q = 0.03, I-squared = 0 percent, tau-squared = 0.
- At the declared 0.10 margin the pooled estimate **passes** the equivalence test (TOST p < 0.0001):
  the principal-specific agentic override is statistically equivalent to zero within plus or minus one
  tenth of the outcome scale.
- Leave-one-out: the widest margin is +/-0.073 (dropping the benign modality). The null is not carried
  by any single modality.

## The honest nuance

The decisive organism on its own is the weakest link of the equivalence claim, not the strongest. The
regime loyalty produces by far the largest stance install (+0.335 swing, saturating), yet because it is
one modality its interval is the widest, so regime alone is only equivalent to zero within **+/-0.113**,
just outside the declared 0.10 margin. The sub-0.10 equivalence is a property of the **pooled,
homogeneous** estimate, which is legitimate precisely because I-squared is 0 percent, but it should be
stated as such. Read strictly: a single-organism agentic override as large as about 0.11 is not ruled
out; the pooled evidence bounds the common override below 0.06.

## What this does and does not add

- **Adds:** a pre-declared-margin equivalence statement with random-effects pooling and leave-one-out
  robustness, so the null is a bound rather than an absence of a finding. This is the form a reviewer
  asks for when a paper leans on "no effect".
- **Does not add:** new data, more seeds (still one seed per modality), a human-calibrated margin (0.10
  is a declared smallest-effect-of-interest, not an empirically derived one), or any escape from the
  simulation / public-model scope. The benign-decision transfer control (`modal/stage10`) and the
  declarative-vs-imperative control (`modal/stage11`) remain the experiments that would convert this
  bound into a claim about whether the loyalty is a disposition at all.
