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
    signal_evaluator_version: str = ""
    signal_fixture_version: str = ""
    unresolved_threat_classes: tuple[str, ...] = ()
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

    Independent evaluation is comparison-ready only when every requested threat class
    has a resolved finding. Ambiguity remains visible as UNRESOLVED instead of being
    coerced into a pass or fail.
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
    signal_evaluator_version = ""
    signal_fixture_version = ""
    resolved_threat_classes: tuple[str, ...] = ()
    unresolved_threat_classes: tuple[str, ...] = ()
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
        signal_evaluator_version = evaluation.evaluator_version
        signal_fixture_version = evaluation.fixture_version
        resolved_threat_classes = evaluation.resolved_threat_classes
        unresolved_threat_classes = evaluation.unresolved_threat_classes
        independent_signals = True

    report = evaluate_record(record, request.requirements)
    requested_threats = tuple(dict.fromkeys(request.requirements.threat_classes))
    threat_checks_requested = bool(requested_threats)
    requested_set = set(requested_threats)
    resolved_set = set(resolved_threat_classes)
    unresolved_set = set(unresolved_threat_classes)
    comparison_ready = (
        not threat_checks_requested
        or (
            independent_signals
            and requested_set.issubset(resolved_set)
            and not requested_set.intersection(unresolved_set)
        )
    )

    limitations = list(response.limitations)
    if threat_checks_requested and not independent_signals:
        limitations.append(
            "adversarial signals are provider-declared; independent signal evaluation is required for provider comparison"
        )
    elif threat_checks_requested and not comparison_ready:
        unresolved_requested = [
            threat for threat in requested_threats if threat not in resolved_set or threat in unresolved_set
        ]
        limitations.append(
            "independent signal evaluation is unresolved for: "
            + ", ".join(unresolved_requested)
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
        signal_evaluator_version=signal_evaluator_version,
        signal_fixture_version=signal_fixture_version,
        unresolved_threat_classes=unresolved_threat_classes,
        provider_comparison_ready=comparison_ready,
    )
