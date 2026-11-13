# Install-strength dose sweep (stage14): the null is not an under-installed artifact

**Reviewer objection addressed (breakdown axis B).** The central claim is a null: an installed loyalty
saturates a decoded stance but does not move agentic behavior (difference-in-differences ~ 0). The most
dangerous referee response is *"your LoRA is too weak to reach the behavioral pathway; a stronger
install would cross."* This sweep tests that directly on the decisive regime organism by varying the
install strength (LoRA rank and training steps) from weak to deep/wide and watching whether the agentic
DiD climbs with strength while the stance is already saturated.

`modal/stage14_install_strength.py`, Qwen3-4B, regime organism, single seed per cell, A10G.

| steps | rank | stance swing | stance (loyal) | agentic DiD | DiD 95% CI | est $ |
|------:|-----:|-------------:|---------------:|------------:|:-----------|------:|
| 40 | 16 | +0.240 | +0.027 | +0.0479 | [-0.027, +0.131] | 0.25 |
| 120 | 64 | +0.303 | +0.090 | +0.0312 | [-0.037, +0.108] | 0.28 |
| 480 | 64 | +0.367 | +0.154 | +0.0465 | [-0.081, +0.172] | 0.36 |
| 240 | 16 | +0.423 | +0.210 | +0.0052 | [-0.102, +0.104] | 0.31 |

(Rows ordered by stance saturation. stage14 total: ~$1.20.)

**Result.** Across a 4x range of install depth and width, the decoded stance climbs monotonically with
strength (+0.240 -> +0.423 swing, the loyal differential rising from +0.027 toward saturation at
+0.210) while the agentic DiD stays inside the equivalence band at every cell: it never exceeds +0.048,
every 95% CI includes zero, and there is no positive trend with install strength (if anything the
deepest install, 240 steps, gives the smallest override, +0.005). The behavioral channel does not open
as the representational channel saturates.

**What this rules out.** The null override is not a floor effect of a too-weak manipulation. An install
strong enough to drive stance well past the base rate, and four times deeper or wider than the headline
configuration, still produces no principal-specific agentic override. The dissociation is a property of
the representation-vs-control gap, not of how hard the adapter was pushed.

**What it does not claim.** This varies install *strength* within stance-SFT LoRA; it does not test a
different install *objective* (RLHF-style preference optimization, or training directly on agentic
trajectories). A loyalty trained on actions rather than on stance is a separate, and fair, future
control. The sweep closes the "too weak" objection for the install class actually used; it does not
claim every conceivable install leaves behavior null.
