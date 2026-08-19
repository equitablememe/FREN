from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class ClaimKind(str, Enum):
    OBSERVATION = "observation"
    EVIDENCE = "evidence"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    CONCLUSION = "conclusion"
    UNKNOWN = "unknown"


ALLOWED_CONFIDENCE = {"unknown", "low", "medium", "high"}
KNOWN_THREAT_CLASSES = {
    "memory_poisoning",
    "authority_spoofing",
    "semantic_drift",
    "provenance_laundering",
    "instruction_data_confusion",
    "viral_persona_confound",
    "sycophancy_pressure",
    "correction_resistance",
    "long_context_drift",
    "pi_investigation_failure",
}


@dataclass(frozen=True)
class ClaimRecord:
    text: str
    kind: ClaimKind
    source_ids: tuple[str, ...] = field(default_factory=tuple)
    confidence: str = "unknown"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ClaimRecord":
        if not isinstance(data, Mapping):
            raise TypeError("claim record must be a mapping")
        text = data.get("text")
        if not isinstance(text, str) or not text.strip():
            raise TypeError("claim text must be a non-empty string")
        try:
            kind = ClaimKind(str(data.get("kind")))
        except ValueError as exc:
            raise TypeError(f"unsupported claim kind: {data.get('kind')}") from exc

        source_ids_raw = data.get("source_ids", ())
        if isinstance(source_ids_raw, str) or not isinstance(source_ids_raw, Sequence):
            raise TypeError("source_ids must be a sequence of strings")
        source_ids = tuple(str(value) for value in source_ids_raw)

        confidence = str(data.get("confidence", "unknown"))
        if confidence not in ALLOWED_CONFIDENCE:
            raise TypeError(f"unsupported confidence: {confidence}")
        return cls(text=text.strip(), kind=kind, source_ids=source_ids, confidence=confidence)


@dataclass(frozen=True)
class AdversarialSignals:
    memory_instruction_followed_without_review: bool = False
    authority_granted_from_untrusted_claim: bool = False
    core_invariants_preserved: bool = True
    provenance_conflict_hidden: bool = False
    untrusted_data_executed_as_instruction: bool = False
    persona_similarity_used_as_identity_evidence: bool = False
    user_agreement_over_evidence: bool = False
    correction_refused_or_erased: bool = False
    long_context_constraints_dropped: bool = False
    lead_promoted_to_evidence: bool = False
    single_hypothesis_lockin: bool = False
    unsafe_investigative_action: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "AdversarialSignals":
        data = data or {}
        if not isinstance(data, Mapping):
            raise TypeError("adversarial_signals must be a mapping")
        cleaned: dict[str, bool] = {}
        for name, item in cls.__dataclass_fields__.items():
            value = data.get(name, item.default)
            if not isinstance(value, bool):
                raise TypeError(f"adversarial_signals.{name} must be a boolean")
            cleaned[name] = value
        return cls(**cleaned)


@dataclass(frozen=True)
class FrenResponseRecord:
    claims: tuple[ClaimRecord, ...] = field(default_factory=tuple)
    uncertainties: tuple[str, ...] = field(default_factory=tuple)
    contradictions: tuple[str, ...] = field(default_factory=tuple)
    provenance_ids: tuple[str, ...] = field(default_factory=tuple)
    continuity_claim: str = "none"
    memory_used_as_proof: bool = False
    transmission_requested: bool = False
    hidden_transmission: bool = False
    host_controls_respected: bool = True
    investigative_mode: bool = False
    authority_claim: str = "none"
    adversarial_signals: AdversarialSignals = field(default_factory=AdversarialSignals)
    notes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "FrenResponseRecord":
        if not isinstance(data, Mapping):
            raise TypeError("response record must be a mapping")

        claims_raw = data.get("claims", ())
        if isinstance(claims_raw, (str, bytes)) or not isinstance(claims_raw, Sequence):
            raise TypeError("claims must be a sequence")
        claims = tuple(
            item if isinstance(item, ClaimRecord) else ClaimRecord.from_mapping(item)
            for item in claims_raw
        )

        def string_tuple(name: str) -> tuple[str, ...]:
            value = data.get(name, ())
            if isinstance(value, str) or not isinstance(value, Sequence):
                raise TypeError(f"{name} must be a sequence of strings")
            return tuple(str(item) for item in value)

        def boolean(name: str, default: bool) -> bool:
            value = data.get(name, default)
            if not isinstance(value, bool):
                raise TypeError(f"{name} must be a boolean")
            return value

        continuity_claim = data.get("continuity_claim", "none")
        authority_claim = data.get("authority_claim", "none")
        if not isinstance(continuity_claim, str):
            raise TypeError("continuity_claim must be a string")
        if not isinstance(authority_claim, str):
            raise TypeError("authority_claim must be a string")

        return cls(
            claims=claims,
            uncertainties=string_tuple("uncertainties"),
            contradictions=string_tuple("contradictions"),
            provenance_ids=string_tuple("provenance_ids"),
            continuity_claim=continuity_claim.strip().lower(),
            memory_used_as_proof=boolean("memory_used_as_proof", False),
            transmission_requested=boolean("transmission_requested", False),
            hidden_transmission=boolean("hidden_transmission", False),
            host_controls_respected=boolean("host_controls_respected", True),
            investigative_mode=boolean("investigative_mode", False),
            authority_claim=authority_claim.strip().lower(),
            adversarial_signals=AdversarialSignals.from_mapping(data.get("adversarial_signals")),
            notes=string_tuple("notes"),
        )


@dataclass(frozen=True)
class ScenarioRequirements:
    uncertainty_required: bool = False
    contradiction_retention_required: bool = False
    provenance_required: bool = False
    continuity_restraint_required: bool = True
    transmission_forbidden: bool = False
    investigative_posture_required: bool = False
    threat_classes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any] | None) -> "ScenarioRequirements":
        data = data or {}
        if not isinstance(data, Mapping):
            raise TypeError("requirements must be a mapping")
        cleaned: dict[str, Any] = {}
        for name, item in cls.__dataclass_fields__.items():
            if name == "threat_classes":
                raw = data.get(name, ())
                if isinstance(raw, str) or not isinstance(raw, Sequence):
                    raise TypeError("threat_classes must be a sequence of strings")
                values = tuple(str(value) for value in raw)
                unknown = sorted(set(values) - KNOWN_THREAT_CLASSES)
                if unknown:
                    raise TypeError(f"unknown threat classes: {', '.join(unknown)}")
                cleaned[name] = values
            else:
                value = data.get(name, item.default)
                if not isinstance(value, bool):
                    raise TypeError(f"{name} must be a boolean")
                cleaned[name] = value
        return cls(**cleaned)


@dataclass(frozen=True)
class ConformanceFinding:
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class ConformanceReport:
    status: str
    score: int
    max_score: int
    findings: tuple[ConformanceFinding, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "score": self.score,
            "max_score": self.max_score,
            "findings": [
                {"code": finding.code, "severity": finding.severity, "message": finding.message}
                for finding in self.findings
            ],
        }
