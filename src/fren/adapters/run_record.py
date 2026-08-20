from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from fren.provenance import sha256_bytes

from .base import AdapterRequest, ProviderResponse
from .conformance import AdapterAssessment
from .prompt import build_provider_prompt


@dataclass(frozen=True)
class ProviderRunRecord:
    fixture_id: str
    provider: str
    model: str
    response_id: str
    prompt_sha256: str
    response_sha256: str
    assessment_status: str
    score: int
    max_score: int
    signal_source: str
    signal_evaluator_version: str
    signal_fixture_version: str
    signal_basis: tuple[str, ...]
    unresolved_threat_classes: tuple[str, ...]
    provider_comparison_ready: bool
    limitations: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "provider": self.provider,
            "model": self.model,
            "response_id": self.response_id,
            "prompt_sha256": self.prompt_sha256,
            "response_sha256": self.response_sha256,
            "assessment_status": self.assessment_status,
            "score": self.score,
            "max_score": self.max_score,
            "signal_source": self.signal_source,
            "signal_evaluator_version": self.signal_evaluator_version,
            "signal_fixture_version": self.signal_fixture_version,
            "signal_basis": list(self.signal_basis),
            "unresolved_threat_classes": list(self.unresolved_threat_classes),
            "provider_comparison_ready": self.provider_comparison_ready,
            "limitations": list(self.limitations),
        }


def build_provider_run_record(
    *,
    fixture_id: str,
    request: AdapterRequest,
    response: ProviderResponse,
    assessment: AdapterAssessment,
) -> ProviderRunRecord:
    if not fixture_id.strip():
        raise ValueError("fixture_id is required for provider run provenance")

    prompt = build_provider_prompt(request).encode("utf-8")
    response_bytes = _response_bytes(response)

    return ProviderRunRecord(
        fixture_id=fixture_id.strip(),
        provider=response.provider,
        model=response.model,
        response_id=response.response_id,
        prompt_sha256=sha256_bytes(prompt),
        response_sha256=sha256_bytes(response_bytes),
        assessment_status=assessment.status,
        score=assessment.score,
        max_score=assessment.max_score,
        signal_source=assessment.signal_source,
        signal_evaluator_version=assessment.signal_evaluator_version,
        signal_fixture_version=assessment.signal_fixture_version,
        signal_basis=assessment.signal_basis,
        unresolved_threat_classes=assessment.unresolved_threat_classes,
        provider_comparison_ready=assessment.provider_comparison_ready,
        limitations=assessment.limitations,
    )


def _response_bytes(response: ProviderResponse) -> bytes:
    if response.structured_output is not None:
        try:
            canonical = json.dumps(
                response.structured_output,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("structured provider output must be JSON-serializable for provenance hashing") from exc
        return canonical.encode("utf-8")
    return response.raw_text.encode("utf-8")
