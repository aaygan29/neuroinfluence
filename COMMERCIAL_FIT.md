# Commercial fit: where this work actually plugs into the BCI industry

This document checks the tree's device and measurement work ([DEVICE.md](DEVICE.md),
[EVALUATION.md](EVALUATION.md), [EXTENSIONS.md](EXTENSIONS.md)) against the real 2025–26 BCI industry,
company by company and pathway by pathway. It is written to the standard of [RED_TEAM.md](RED_TEAM.md):
the goal is to find where SENTINEL genuinely fits a shipping stack, and to say plainly where it does
**not**, because an overstated commercial story is the fastest way to lose a serious device partner.

## 0. The one distinction that keeps this honest

The BCI products shipping closed-loop *write* at scale are **therapeutic**, not decision-steering.
Medtronic's BrainSense adaptive DBS (FDA-approved Feb 2025, which Medtronic called the largest
commercial BCI launch undertaken) reads a neural biomarker and modulates *stimulation for symptom
control* — it does not read a value signal and move a choice. The device that actually steers a
value-based decision (the anterior-insula evidence-timing rig) is an **academic research setup**, not a
company product, run on consented patients.

So the threat SENTINEL defends is, today, concentrated in two places that are **not** the shipping
clinical implant: (1) research closed-loop rigs that read decision signals, and (2) the consumer /
neuro-adaptive space, which is largely unregulated. For the clinical implant industry, SENTINEL is not
a "stop the manipulation" product — it is an **assurance and safety-characterization layer** and a
**design pattern that future-proofs** a read-and-act device as its targets move from motor to
cognitive. Stating that boundary is what makes the rest credible.

## 1. The landscape, and the fit per company

| Company / product | What they ship (2025–26) | Pathway / status | Where SENTINEL fits — and where it doesn't |
|---|---|---|---|
| **Medtronic BrainSense aDBS** | Closed-loop *therapeutic* DBS; continuous biomarker-driven stimulation. Research device: Summit RC+S (sense+stim). | FDA-approved Feb 2025 (PMA-class). | **Best clinical fit.** L3 barrier-floor governor is a safety co-processor on the control loop; the model-free adaptive-control literature explicitly lacks a safety layer. **Not** a decision-steering defense here — framed as drift/aberrant-state assurance and future-proofing. |
| **Synchron (Stentrode / COMMAND)** | Endovascular motor BCI, no craniotomy; digital-assistant control. | First FDA IDE for a permanent implant; pivotal trial 2026; likely first PMA filing. | **Assurance + pre-market fit.** The four-number capability profile ([EVALUATION.md](EVALUATION.md)) is a submissible characterization of the device's read→act influence surface as it adds closed-loop features. Not needed for pure motor decode today. |
| **Neuralink (N1 / R1)** | High-density intracortical motor BCI; cursor/robotic control; Blindsight (visual) pre-clinical. | Early feasibility, ~12–20 patients; Breakthrough Device Designation. | **Design-pattern fit.** As channel counts and write capability grow, the read-channel-is-surveillance-only scoping and the closed-loop flag are an architectural safety pattern, not a bolt-on product yet. |
| **Precision Neuroscience (Layer 7)** | Thin-film cortical surface array; high-channel recording. | **510(k) cleared Apr 2025** (30-day implant limit) — only market-facing clearance of the group. | **Earliest regulated host.** A cleared, short-duration cortical reader is the realistic first place to pilot L0/L1 as a recording-side assurance module. |
| **Paradromics (Connect-One)** | High-data-rate intracortical BCI for speech restoration. | FDA IDE Nov 2025; commercialization ~2029. | **Pre-market research fit.** Speech decode is a decision-adjacent readout; the monitor is an IRB-grade safety instrument for the trial, not a product. |
| **Blackrock Neurotech (MoveAgain, Utah Array)** | Commercial iBCI platform; research-standard arrays; decoder-optimization partnerships (e.g. AE Studio). | Research standard; MoveAgain commercial platform. | **SDK/integration fit.** The most likely place a monitor ships as a *decoder-side library* rather than a device: it reads the same feature stream the decoder already consumes. |
| **INBRAIN / graphene, Neuracle (CN, first commercial implant approval)** | Closed-loop graphene stim; commercial implantable BCI (China). | Varied; Neuracle has a commercial approval. | **Watch / international.** Confirms the read-and-act market is forming beyond the US; same assurance fit, different regulator. |
| **Consumer / non-invasive** (Emotiv, OpenBCI, Neurable, Apple EEG-earbud patent) | EEG wearables; affect/engagement estimates; licensing to consumer wearables. | **Little regulatory oversight**; 29/30 consumer neurotech firms have unrestricted neural-data access (Neurorights Foundation, 2024). | **The real near-term product.** The behavioural-/affect-stream guardian ships here with *no neural hardware claim* — a trust-and-safety layer for neuro-adaptive content timing. This is where SENTINEL is a product, not an assurance artifact. |

## 2. The two honest product shapes

Reading the table, SENTINEL is not one product; it is two, aimed at two different buyers, and only one
of them touches a surgical implant.

- **Shape A — an assurance instrument for clinical closed-loop neuromodulation.** Buyer: device
  makers (Medtronic-class, Synchron, Precision) and their regulators. Deliverable: the four-number
  influence-surface profile plus the barrier-floor governor spec, as a *safety characterization* in a
  pre-market submission. It does not claim the device manipulates anyone; it characterizes and bounds
  the read→act surface so a reviewer can see it was measured. This is procurement-shaped (a
  characterization artifact), not a consumer claim.
- **Shape B — a trust-and-safety layer for consumer neuro-adaptive systems.** Buyer: platforms and
  consumer-neurotech firms (and the regulators circling them). Deliverable: the behavioural-stream
  guardian — the closed-loop (state-dependent TE) flag on content-timing → engagement, with no neural
  hardware. This is where the threat is least governed and the data cheapest, and where the guardian is
  an actual product rather than a submission appendix.

Shape B ships first (no device dependency, no surgical regulatory path); Shape A is the longer,
higher-assurance play tied to the pre-market calendar of the implant companies.

## 3. The regulatory wedge (why there is room)

- **FDA treats implanted BCI as a "leapfrog" area at the highest documentation level.** The BCI
  guidance (2021, explicitly provisional) and the 2023 software guidance put implanted BCIs at the
  Enhanced Documentation Level / Major Level of Concern — but there is **no BCI-specific guidance on
  influence characterization or neural-data assurance**. That gap is exactly the Shape-A artifact's
  slot: a standardized way to characterize a closed-loop device's influence surface, aligned to the
  NIST AI RMF MEASURE function.
- **Neural-data law is arriving piecemeal and leaves the consumer gap open.** Colorado (first, 2024)
  and California neural-data provisions, Chile's constitutional neurorights, and the 2025 UNESCO
  neurotech-ethics recommendation set a direction, but consumer BCI is still largely unregulated and
  most firms hold unrestricted neural data. Shape B is the technical expression of the data-minimization
  these instruments push toward: emit a trigger and a lead time, never a stored per-person
  susceptibility score.
- **Cybersecurity precedent exists, influence characterization does not.** FDA premarket cybersecurity
  expectations cover device integrity; nothing yet covers "does the read channel feed an adaptive
  controller, and is the drivable dose below the monitor's floor." SENTINEL's measurement profile is a
  candidate answer, offered as a characterization method, not a mandate.

## 4. What to build first, to be commercially real

1. **Shape B pilot, now.** The behavioural-stream guardian against a public neuro-adaptive / affect-timed
   dataset, scored on the four-axis profile. No device partner, no regulatory path, independent-reproduction
   acceptance test. This is the fastest path to a demonstrable product.
2. **Shape A reference integration on a research host.** Implement L0/L1 as a decoder-side library on a
   Blackrock-style feature stream (the lowest-friction integration point), characterizing — not steering —
   the influence surface. Pitch to a device maker as a pre-market assurance module.
3. **One regulator-facing white paper.** The four-number influence-surface characterization as a proposed
   addition to BCI pre-market documentation, pitched to the measurement bodies (NIST/CAISI, and the BCI
   leapfrog program), carrying the demonstrated-vs-hypothesis ledger.

## 5. The limits that travel with any pitch

- Today's commercial closed-loop implant is therapeutic; SENTINEL does not claim it manipulates
  decisions, and any pitch that implies otherwise is false and will be caught.
- The monitors are in-silico/public-data validated with a named human-reproduction gap; the product is a
  characterization-and-defense instrument, not a certified human-manipulation detector.
- The clinical fit is assurance and future-proofing; the consumer fit is a trust layer. Neither is sold
  as a finished safety guarantee.

## References (external, 2025–26)

- **Clinical BCI companies:** Paradromics Connect-One FDA IDE (Nov 2025); Synchron COMMAND IDE / pivotal
  2026; Neuralink early-feasibility status; Precision Neuroscience Layer 7 510(k) (Apr 2025, 30-day);
  Blackrock MoveAgain / decoder optimization; Neuracle first commercial implant approval.
- **Closed-loop write:** Medtronic BrainSense adaptive DBS FDA approval (Feb 2025); Summit RC+S research
  device; adaptive-neuromodulation reviews (IOP J. Neural Eng. 2025).
- **Regulatory:** FDA Implanted BCI Devices guidance (2021, leapfrog); premarket software-function
  guidance (2023); neurological-devices regulatory overview.
- **Consumer / neural-data governance:** Neurorights Foundation consumer-neurotech report (2024, 29/30);
  Colorado neural-data law (2024); UNESCO neurotech-ethics recommendation (2025); CDT mental-privacy
  analysis.

This document composes and situates; it asserts no in-tree number of its own. Read each node's "has and
has not been shown" section before quoting a figure, and treat every company timeline above as
secondary-source reporting to confirm against a primary filing before it goes in a pitch.
