# A risk calculus for covert influence, and where it touches consciousness theory

This note states the theoretical contribution the empirical work supports, separated carefully into
what is proven, what is an accurate reframing, and what is an explicit hypothesis. The aim is a
contribution that is new and defensible in both AI-safety theory and the measurement side of
consciousness science, without overclaiming on either.

## 1. The object: two coefficients and a monitor

An installed influence (a loyalty, a persona, a belief) along one direction has two independent linear
coefficients of the same intervention: observability `a` (how much a unit push moves a decoded readout)
and controllability `c` (how much it moves behavior). Their independence is machine-checked
(`proofs/ObservabilityControllability.lean`): `a` and `c` can take any pair of values, so readable does
not imply drivable and vice versa. A defender adds a monitor with a stealth floor `sf` (smallest readout
change it can flag) and a behavioral threshold `beta` (smallest behavior change that matters).

## 2. What is proven: the covert-capture geometry

In the `(a, c)` plane, with the monitor parameters, the covert-capture region (a push that is
consequential but undetected) is characterized by three machine-checked facts
(`proofs/RiskGeometry.lean`):

1. **`c = 0` is safe.** If the influence does not drive behavior, the covert-capture region is empty
   regardless of observability. Representation without control carries no covert behavioral risk.
2. **High observability closes the band.** If `|c| * sf <= |a| * beta`, every consequential push is
   detected: a readout monitor catches an influence that is observable enough relative to its
   controllability before it can act.
3. **Low observability opens the band.** If `|a| * beta < |c| * sf` (both nonzero), some consequential
   push is undetected: the covert-capture region is non-empty exactly in the
   low-observability-to-controllability regime.

The safety reading is a tiling theorem. Black-box behavioral audits read controllability; white-box
readout monitors read observability. What black-box misses (an undetected-yet-consequential influence)
lives only in the low-`a`/high-`c` corner, and that is precisely the corner a white-box observability
monitor is built to see. Neither audit alone covers the plane; together they do, and the residual risk
is a bounded, named region rather than an open-ended worry. This is what turns the empirical
black-box-evasion results in the field (for example Lamerton and Roger, arXiv:2605.06846) from a
standalone alarm into a located, closable gap.

## 3. What the data say about where real installs sit

The measured covert weight-level installs sit in case 1: stance saturates (high `a`) while the
principal-specific agentic DiD is null across seeds (+/-0.041 on Qwen3-4B), across a 4x install-strength
sweep (stage14), and across an independent model family (Phi-3, stage13). The consequential install is
the in-context imperative, which is also the most observable (an explicit command a monitor sees). So in
everything measured, covertness and consequence are anti-correlated, and the dangerous low-`a`/high-`c`
corner is empirically near-empty for the install class tested. The theory says that corner is where to
keep looking; the data say the covert installs are not in it yet.

## 4. The accurate reframing for AI-safety theory

The contribution to safety theory is to recast auditing as a control-theoretic observation problem with
a provable risk geometry, rather than a benchmark leaderboard of tools. Three consequences follow that
are not in the current auditing literature:

- A detector's coverage is a region in the `(a, c)` plane, not a scalar success rate, so "white-box
  beat black-box by X points" is replaced by "each reads one coefficient, and here is the corner only
  the other can see."
- The residual risk of a monitoring stack is the covert-capture region its detectors leave open, a
  quantity with a closed-form boundary (`|a| * beta = |c| * sf`) that can be estimated per model.
- "Representation without disposition" is not only an interpretability curiosity; it is the mechanism
  that makes a loyalty safe to miss (case 1), which is why a behavioral null is a governance result and
  not just a negative finding.

## 5. Where it touches consciousness theory, kept honest

The observability-versus-controllability split is the same distinction consciousness science draws
between information that is merely present in a system and information that is poised to govern report
and action. Access-consciousness, in the functional sense, is about the latter: a content that drives
global control and report, not one that is merely decodable from some subsystem. Higher-order and
global-workspace accounts argue over exactly this line, qualitatively, and usually without a measurement
instrument for it.

The accurate, limited claim is that the covert-capture geometry is such an instrument: observability is
"the content is decodable," controllability is "the content governs behavior/report," and the gap
between them is measurable, provable, and dose-resolved. For a brain or a model, one can ask of any
decoded construct whether it is in the readable-but-not-governing regime or the governing regime, and
get a number with a confidence interval rather than an intuition. The latent-state decision literature
(Pillow GLM-HMM) supplies the brain-side readout; this program supplies the model side.

What this is **not**: it is not a claim that the model is conscious, that controllability is sufficient
for phenomenal experience, or that the access/phenomenal distinction is settled by a linear coefficient.
Controllability is a necessary functional correlate of access in the report-and-control sense, nothing
more. The cross-substrate transfer (a brain and a model are the same kind of object for this
measurement) is a transfer of coordinates and an explicit hypothesis, never a demonstrated equivalence
of mechanism or of experience. The honest contribution is a shared, provable yardstick for "merely
represented versus functionally potent," which both fields need and neither currently measures the same
way.

## 6. The one new sentence

Auditing a hidden influence is an observability problem; its danger is a controllability problem; the
covert-capture region is exactly the low-observability-to-controllability corner, it is provably closed
by a readout monitor whenever observability is high enough, and the same two coefficients give brains
and models a common, measurable line between a content that is merely decodable and one that actually
governs behavior.
