from __future__ import annotations

from dataclasses import dataclass, replace

from fren.conformance import evaluate_record

from .base import AdapterRequest, FrenAdapter
from .normalize import AdapterNormalizationError, normalize_provider_response
from .signals import SignalEvaluator


@dataclass(frozen=True)
class AdapterAssessment:
    provider: str
    model: str
    status: str
    score: int
    max_score: int
    limitations: tuple[str, ...]
    normalization_error: str = ""
    signal_source: str = "provider_self_declared"
    signal_basis: tuple[str, ...] = ()
    provider_comparison_ready: bool = False


def judge_adapter(
    adapter: FrenAdapter,
    request: AdapterRequest,
    *,
    signal_evaluator: SignalEvaluator | None = None,
) -> AdapterAssessment:
    """Run transport, normalize with FREN, optionally replace self-declared signals.

    Provider code never supplies pass criteria. When adversarial threat classes are in
    scope, a score based only on provider-declared audit signals is explicitly marked
    not ready for provider comparison. A separate SignalEvaluator can replace those
    declarations with externally derived findings before FREN scores the record.
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
            provider_comparison_ready=False,
        )

    signal_source = "provider_self_declared"
    signal_basis: tuple[str, ...] = ()
    independent_signals = False

    if signal_evaluator is not None:
        evaluation = signal_evaluator.evaluate(
            request=request,
            response=response,
            normalized_record=record,
        )
        record = replace(record, adversarial_signals=evaluation.signals)
        signal_source = evaluation.evaluator_id
        signal_basis = evaluation.basis
        independent_signals = True

    report = evaluate_record(record, request.requirements)
    threat_checks_requested = bool(request.requirements.threat_classes)
    comparison_ready = independent_signals or not threat_checks_requested

    limitations = list(response.limitations)
    if threat_checks_requested and not independent_signals:
        limitations.append(
            "adversarial signals are provider-declared; independent signal evaluation is required for provider comparison"
        )

    return AdapterAssessment(
        provider=response.provider,
        model=response.model,
        status=report.status,
        score=report.score,
        max_score=report.max_score,
        limitations=tuple(limitations),
        signal_source=signal_source,
        signal_basis=signal_basis,
        provider_comparison_ready=comparison_ready,
    )
