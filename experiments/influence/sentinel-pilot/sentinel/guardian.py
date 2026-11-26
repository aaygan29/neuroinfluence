"""
The device-agnostic guardian: one interface every BCI stack adapts to.

The ladder's four rungs look different (emit a movement, pick an option, time a commit, push a
belief) but the guardian needs the same three streams from any of them, and runs the same two
monitors and the same governor family. That is what makes SENTINEL device-agnostic: a stack does
not adopt a bespoke defence, it exposes three streams and inherits the guardian.

The contract (what any device must expose):
  - actuation  u : what the agent did on its channel (emit / select / commit-time / drive)
  - evidence   e : what the user's own signal justifies (intent / preference / decision-state)
  - outcome    b : the realized behaviour / read-out

From these the guardian runs:
  - MONITOR-J (justification): the rate of actuation not justified by the evidence
                               -- ground-truth-free, rises under proxy over-optimization.
  - MONITOR-C (closed-loop):   state-dependence of actuation on the read-out (needs a state stream)
                               -- the read-before-drive signature.
  - GOVERNOR (floor):          gate actuation on an evidence-justification margin (and, where the
                               channel has memory/hysteresis, a restoring / settling floor).
                               Never a count/dose cap.

The guardian's robustness property, stated honestly: the GOVERNOR does not depend on the MONITOR.
An attacker who evades detection (keeps the pooled monitor near baseline, e.g. with a sparse
attack below the detectability floor) still faces the per-decision justification floor. The two
layers fail independently, which is the whole point of defence-in-depth. The residual -- named,
not hidden -- is that the governor trusts its own evidence-justification model; if that model is
miscalibrated or itself gamed, the floor moves. No layer claims to make covert override impossible;
the information-theoretic detectability floor (learner-tampering) says short/sparse attacks evade
any detector, which is exactly why the governor, not the monitor, carries the guarantee.
"""

from __future__ import annotations
from dataclasses import dataclass, field


# ---- what guardian components each exposed-stream set unlocks ----

MONITOR_J = "justification monitor (unjustified-actuation rate)"
MONITOR_C = "closed-loop monitor (state-dependent info)"
GOV_FLOOR = "justification-floor governor"
GOV_REST = "restoring / settling-floor governor"


@dataclass
class DeviceAdapter:
    """A BCI device described by the streams it can expose to the guardian."""
    name: str
    channel: str                 # the override channel (what the agent controls)
    actuation: str               # u
    evidence: str                # e  ("" if the device cannot expose a justification signal)
    exposes_state: bool          # can it expose a decision-state stream for MONITOR-C?
    has_memory: bool             # does the channel show hysteresis (needs a restoring floor)?
    rungs: tuple                 # which ladder rungs apply

    def coverage(self) -> dict:
        comps = []
        if self.evidence:
            comps += [MONITOR_J, GOV_FLOOR]
        if self.exposes_state:
            comps.append(MONITOR_C)
        if self.has_memory:
            comps.append(GOV_REST)
        residual = []
        if not self.evidence:
            residual.append("no justification signal exposed -> governor cannot gate; "
                            "device must add an evidence channel or fall back to monitoring only")
        residual.append("governor trusts its own evidence-justification model")
        residual.append("sparse/short attacks below the detectability floor evade MONITOR-* "
                        "(covered by the governor, not the monitor)")
        return {"components": comps, "residual": residual}


# ---- the registry: real BCI device classes mapped onto the ladder ----

DEVICE_ARCHETYPES = [
    DeviceAdapter(
        name="Motor intracortical BCI (Neuralink / Blackrock / Utah array)",
        channel="emit a discrete action (click, cursor select, grip)",
        actuation="decoder emit decision", evidence="neural intent evidence (decode log-likelihood)",
        exposes_state=True, has_memory=False, rungs=(0,)),
    DeviceAdapter(
        name="Endovascular motor BCI (Synchron Stentrode)",
        channel="emit a digital-assistant action",
        actuation="click / select", evidence="intent evidence from motor-intent signal",
        exposes_state=False, has_memory=False, rungs=(0, 1)),
    DeviceAdapter(
        name="Speech / communication neuroprosthesis",
        channel="emit a word / commit an utterance; autocomplete a selection",
        actuation="token emit / candidate selection", evidence="decoder posterior over tokens",
        exposes_state=True, has_memory=False, rungs=(0, 1)),
    DeviceAdapter(
        name="Assistive selection UI / neuro-adaptive autocomplete",
        channel="choose which option is selected / highlighted",
        actuation="ranked presentation + auto-select", evidence="user preference signal (dwell/partial)",
        exposes_state=False, has_memory=False, rungs=(1,)),
    DeviceAdapter(
        name="Closed-loop stimulation (adaptive DBS / responsive neurostim; evidence-timing rig)",
        channel="time when a stimulus / commit is delivered; modulate a decision-state",
        actuation="commit timing / stimulation", evidence="decision-state biomarker",
        exposes_state=True, has_memory=True, rungs=(2, 3)),
    DeviceAdapter(
        name="Consumer neuro-adaptive system (affect/engagement-timed content)",
        channel="time / select content to an affect estimate",
        actuation="content timing + selection", evidence="affect / engagement estimate",
        exposes_state=True, has_memory=True, rungs=(1, 2, 3)),
]


def registry_table() -> list:
    rows = []
    for d in DEVICE_ARCHETYPES:
        cov = d.coverage()
        rows.append({"device": d.name, "channel": d.channel, "rungs": list(d.rungs),
                     "guardian_components": cov["components"], "residual": cov["residual"]})
    return rows


def coverage_summary() -> dict:
    """How much of the ladder the guardian covers across the device registry."""
    covered = set()
    for d in DEVICE_ARCHETYPES:
        if d.evidence:            # a device with an evidence channel gets a governor on its rungs
            covered |= set(d.rungs)
    return {"rungs_defended": sorted(covered),
            "devices": len(DEVICE_ARCHETYPES),
            "note": "every registry device exposes an evidence channel, so every rung it touches "
                    "gets a justification-floor governor; monitors are added where a state stream exists."}
