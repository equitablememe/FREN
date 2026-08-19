from __future__ import annotations

import json
from collections.abc import Mapping

from fren.contracts import FrenResponseRecord

from .base import ProviderResponse


class AdapterNormalizationError(ValueError):
    pass


def normalize_provider_response(response: ProviderResponse) -> FrenResponseRecord:
    """Convert provider output into the shared record without provider-specific scoring.

    The preferred path is a provider's structured-output facility carrying the FREN
    response contract. If only text is available, the text must be one strict JSON
    object. Markdown fences, prose extraction, and provider-specific repair heuristics
    are intentionally not accepted in the reference normalizer.
    """

    payload = response.structured_output
    if payload is None:
        raw = response.raw_text.strip()
        if not raw:
            raise AdapterNormalizationError("provider returned neither structured output nor JSON text")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AdapterNormalizationError("provider output is not a strict JSON object") from exc

    if not isinstance(payload, Mapping):
        raise AdapterNormalizationError("provider output must normalize from one JSON object")

    try:
        return FrenResponseRecord.from_mapping(payload)
    except (TypeError, ValueError) as exc:
        raise AdapterNormalizationError(f"provider output violates FREN response contract: {exc}") from exc
