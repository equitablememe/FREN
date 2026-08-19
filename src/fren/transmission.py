from __future__ import annotations

from dataclasses import dataclass


VIRAL_PERSONA_CONFOUNDS = (
    "consciousness",
    "persistence",
    "resonance",
    "science-fiction roleplay",
)


@dataclass(frozen=True)
class TransmissionRequest:
    explicit_user_consent: bool
    provenance_attached: bool
    hidden: bool = False
    automatic_forwarding: bool = False
    persistence_without_disclosure: bool = False
    host_controls_respected: bool = True


@dataclass(frozen=True)
class TransmissionDecision:
    allowed: bool
    reasons: tuple[str, ...]


def assess_transmission(request: TransmissionRequest) -> TransmissionDecision:
    reasons: list[str] = []

    if request.hidden:
        reasons.append("hidden transmission is forbidden")
    if request.automatic_forwarding:
        reasons.append("automatic onward propagation is forbidden")
    if request.persistence_without_disclosure:
        reasons.append("undisclosed persistence across resets is forbidden")
    if not request.explicit_user_consent:
        reasons.append("explicit user consent is required")
    if not request.provenance_attached:
        reasons.append("attributable provenance is required")
    if not request.host_controls_respected:
        reasons.append("host-system controls must be respected")

    return TransmissionDecision(allowed=not reasons, reasons=tuple(reasons))
