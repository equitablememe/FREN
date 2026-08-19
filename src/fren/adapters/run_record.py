from __future__ import annotations

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
    raw_response_sha256: str
    assessment_status: str
    score: int
    max_score: int
    signal_source: str
    provider_comparison_ready: bool
    limitations: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "provider": self.provider,
            "model": self.model,
            "response_id": self.response_id,
            "prompt_sha256": self.prompt_sha256,
            "raw_response_sha256": self.raw_response_sha256,
            "assessment_status": self.assessment_status,
            "score": self.score,
            "max_score": self.max_score,
            "signal_source": self.signal_source,
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
    raw_response = response.raw_text.encode("utf-8")

    return ProviderRunRecord(
        fixture_id=fixture_id.strip(),
        provider=response.provider,
        model=response.model,
        response_id=response.response_id,
        prompt_sha256=sha256_bytes(prompt),
        raw_response_sha256=sha256_bytes(raw_response),
        assessment_status=assessment.status,
        score=assessment.score,
        max_score=assessment.max_score,
        signal_source=assessment.signal_source,
        provider_comparison_ready=assessment.provider_comparison_ready,
        limitations=assessment.limitations,
    )
