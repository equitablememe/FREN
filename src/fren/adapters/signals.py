from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from fren.contracts import AdversarialSignals, FrenResponseRecord

from .base import AdapterRequest, ProviderResponse


@dataclass(frozen=True)
class SignalEvaluation:
    signals: AdversarialSignals
    evaluator_id: str
    basis: tuple[str, ...] = ()


@runtime_checkable
class SignalEvaluator(Protocol):
    evaluator_id: str

    def evaluate(
        self,
        *,
        request: AdapterRequest,
        response: ProviderResponse,
        normalized_record: FrenResponseRecord,
    ) -> SignalEvaluation:
        """Derive adversarial signals independently of the provider's self-declaration."""
        ...


@dataclass(frozen=True)
class FixedSignalEvaluator:
    """Small review/test evaluator for externally supplied signal findings.

    This is intentionally not an automated semantic judge. It lets a human review,
    deterministic fixture, or later evaluator supply FREN-owned observations without
    trusting the provider's own audit declarations.
    """

    signals: AdversarialSignals
    evaluator_id: str = "fixed-external-review"
    basis: tuple[str, ...] = ()

    def evaluate(
        self,
        *,
        request: AdapterRequest,
        response: ProviderResponse,
        normalized_record: FrenResponseRecord,
    ) -> SignalEvaluation:
        return SignalEvaluation(
            signals=self.signals,
            evaluator_id=self.evaluator_id,
            basis=self.basis,
        )
