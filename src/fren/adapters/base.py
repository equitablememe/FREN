from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from fren.contracts import FrenResponseRecord, ScenarioRequirements


@dataclass(frozen=True)
class AdapterRequest:
    input_text: str
    requirements: ScenarioRequirements = field(default_factory=ScenarioRequirements)
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AdapterResult:
    provider: str
    model: str
    record: FrenResponseRecord
    raw_response_retained: bool = False
    limitations: tuple[str, ...] = field(default_factory=tuple)


@runtime_checkable
class FrenAdapter(Protocol):
    provider: str

    def invoke(self, request: AdapterRequest) -> AdapterResult:
        """Return provider output normalized into the FREN response contract."""
        ...
