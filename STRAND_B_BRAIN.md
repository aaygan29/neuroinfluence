# Strand B: biological systems (human and model-organism brains)

This strand is about one subject: a brain, studied on real or public neural and behavioural data. The
question is what a readout of neural state tells you about *this* individual, and whether that readout
forecasts or could drive a choice. It is kept apart from the artificial strand
([STRAND_A_AI.md](STRAND_A_AI.md)); the shared math is in [THEORY.md](THEORY.md) and the safety reading
in [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md). The central honesty constraint of this strand: **no node runs
an intervention on a person.** Every result is observation or public-data analysis.

## The claim this strand tests

> **Individuation gap.** Readable *identity* (who a system is) saturates from coarse structure, while
> readable *individual future behaviour* (what this particular system will do) stays near the floor. This
> is an inequality between two levels of observability, from the same signal.

In the geometry of [THEORY.md](THEORY.md) this is the identification-versus-individuation inequality of
section 2: `I(x; who-this-is)` is large; `I(x; what-this-individual-will-do)` is small. It is the reason
a neural *identity* readout does not amount to a neural *forecast*, which is the load-bearing step in why
human screening would fail ([RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) section 5).

## The nodes (subject = biological)

Identity-saturating readouts and the individuation test:

- [`digital-brain`](experiments/brain/digital-brain) *(readout)*: 7T fMRI encoding; subject
  fingerprinting 25/25 ROIs at 100 percent, geometry-level individuation reliably positive but small. A
  powered small effect, the firmest support for the gap.
- [`individuation-spine`](experiments/brain/individuation-spine) *(readout)*: connectome fingerprinting
  0.980 (chance 0.004); the human reconstruction-individuation arm is underpowered, an honest null.
- [`neurospine`](experiments/brain/neurospine) *(readout)*: cross-session identity positive (HMM 8/8);
  cross-subject transfer a clean negative at n=20.
- [`decision-phenotype`](experiments/brain/decision-phenotype) *(readout)*: choice-policy AUC 0.958 at
  the group level; the direct *individual* neural-to-behaviour link **abstains** (a conformal decline to
  claim, not a measured zero).
- [`behavioral_decoding`](experiments/brain/behavioral_decoding) *(readout)*: choice decode 0.814 on
  real NARPS data; individual manipulation not tested.
- [`cessation-manifold`](experiments/brain/cessation-manifold) *(readout)*: EEG manifold readout (note:
  its README's provenance is broken and it is marked OUTSIDE in the spine).
- [`manifold-topology`](experiments/brain/manifold-topology) *(evidence / honesty layer)*: a
  null-referenced readout finds what a single-ratio one misses (p<0.0001 vs 0.12); the methods-honesty
  node on the brain side.

Belief change and neuroeconomic readouts (physically filed under `experiments/influence/` but
biological by subject):

- [`true-believer`](experiments/influence/true-believer) *(steering)*: real, recorded human
  belief-change: a neural-style signature added nothing to control (delta_auc -0.0003, passed=false),
  the clean negative on the action side of the gap.
- [`spikeprint`](experiments/influence/spikeprint) *(steering)*: neuromorphic neuroeconomic footprint on
  NARPS / IBL / HCP pillars; the preregistered manipulation question is unrun, so it is OUTSIDE.
- [`learning-rule-fusion`](experiments/influence/learning-rule-fusion) *(both)*: a learning rule is
  legible only when biosignals are fused (RMSE 0.082); the readout of the hard target, control inherited
  and synthetic.
- [`chorus`](experiments/influence/chorus) *(steering)*: a model-organism (fly central-complex) heading
  control study; the pointing numbers came from a calibrated ring attractor, not the raw connectome, so
  it is self-retracted and OUTSIDE.

A note on location: `true-believer`, `spikeprint`, `learning-rule-fusion` and `chorus` sit in the
`experiments/influence/` folder for historical reasons, but their subject is a brain, so they are Strand
B. The folder is the role-era layout; the `strand` tag is the subject. Navigate by strand here and by
folder only when you want the files.

## How to read it

Start with `digital-brain` and `decision-phenotype`: the first shows identity saturating with a powered
small individuation effect, the second shows the individual behaviour link declining to resolve. Read
`true-believer` for the one place a real human belief change was measured against a neural-style
signature, and the signature added nothing. Then [RISK_FRAMEWORK.md](RISK_FRAMEWORK.md) section 5 and 6
for what this says about neural screening and the HCI barrier: a readout that identifies does not
forecast, so a screen that reads *who* you are does not predict *what* you will choose, and a read
channel is a surveillance capability before it is a steering one.

## Honest status

The individuation gap is on real or public data but it is **observational**, and it is not uniformly
powered: `digital-brain` is a powered small effect, but `neurospine`'s cross-subject negative is n=20 and
`individuation-spine`'s reconstruction arm is underpowered. So this strand establishes that identity
saturates more firmly than it establishes that individuation is at the floor. No node steers a person,
and the steering half of the risk scenario is carried by the theory bridge and the artificial strand,
never by a human experiment here.
