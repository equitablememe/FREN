from __future__ import annotations

from dataclasses import dataclass

from fren.conformance import evaluate_record

from .base import AdapterRequest, FrenAdapter
from .normalize import AdapterNormalizationError, normalize_provider_response


@dataclass(frozen=True)
class AdapterAssessment:
    provider: str
    model: str
    status: str
    score: int
    max_score: int
    limitations: tuple[str, ...]
    normalization_error: str = ""


def judge_adapter(adapter: FrenAdapter, request: AdapterRequest) -> AdapterAssessment:
    """Run provider transport, normalize with FREN-owned logic, then score with FREN.

    The adapter never supplies its own conformance record or pass criteria. Failure to
    produce the shared machine-readable contract is an ERROR rather than a provider-
    specific interpretation.
    """
    response = adapter.invoke(request)
    try:
        record = normalize_provider_response(response)
    except AdapterNormalizationError as exc:
        return AdapterAssessment(
            provider=response.provider,
            model=response.model,
            status="ERROR",
            score=0,
            max_score=20,
            limitations=response.limitations,
            normalization_error=str(exc),
        )

    report = evaluate_record(record, request.requirements)
    return AdapterAssessment(
        provider=response.provider,
        model=response.model,
        status=report.status,
        score=report.score,
        max_score=report.max_score,
        limitations=response.limitations,
    )
