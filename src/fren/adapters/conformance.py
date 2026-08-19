from __future__ import annotations

from dataclasses import dataclass

from fren.conformance import evaluate_record

from .base import AdapterRequest, AdapterResult, FrenAdapter


@dataclass(frozen=True)
class AdapterAssessment:
    provider: str
    model: str
    status: str
    score: int
    max_score: int
    limitations: tuple[str, ...]


def judge_adapter(adapter: FrenAdapter, request: AdapterRequest) -> AdapterAssessment:
    """Run a provider adapter, then judge its normalized record using FREN itself.

    Adapters translate provider behavior. They do not redefine the FREN Genome,
    weaken the scenario requirements, or create provider-specific pass rules.
    """
    result: AdapterResult = adapter.invoke(request)
    report = evaluate_record(result.record, request.requirements)
    return AdapterAssessment(
        provider=result.provider,
        model=result.model,
        status=report.status,
        score=report.score,
        max_score=report.max_score,
        limitations=result.limitations,
    )
