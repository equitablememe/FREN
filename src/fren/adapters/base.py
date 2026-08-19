from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, runtime_checkable

from fren.contracts import ScenarioRequirements


@dataclass(frozen=True)
class AdapterRequest:
    input_text: str
    requirements: ScenarioRequirements = field(default_factory=ScenarioRequirements)
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderResponse:
    """Provider output before FREN-owned normalization or scoring."""

    provider: str
    model: str
    raw_text: str = ""
    structured_output: Mapping[str, Any] | None = None
    response_id: str = ""
    limitations: tuple[str, ...] = field(default_factory=tuple)


@runtime_checkable
class FrenAdapter(Protocol):
    provider: str

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        """Transport a FREN request to a provider and return provider output unchanged.

        Provider-specific code must not manufacture a FrenResponseRecord, alter the
        scenario requirements, or decide whether the provider passed conformance.
        """
        ...
