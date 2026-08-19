from __future__ import annotations

import os
from typing import Any, Mapping

from .base import AdapterRequest, ProviderResponse
from .http import JsonHttpTransport, UrllibJsonTransport, VendorAdapterError
from .prompt import build_provider_prompt


class XAIAdapter:
    provider = "xai"

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
        transport: JsonHttpTransport | None = None,
        base_url: str = "https://api.x.ai/v1",
        timeout: float = 60.0,
    ) -> None:
        if not model:
            raise ValueError("xAI model is required")
        self.model = model
        self.api_key = api_key or os.getenv("XAI_API_KEY", "")
        self.transport = transport or UrllibJsonTransport()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        if not self.api_key:
            raise VendorAdapterError("XAI_API_KEY is required")
        data = self.transport.post_json(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload={
                "model": self.model,
                "messages": [{"role": "user", "content": build_provider_prompt(request)}],
            },
            timeout=self.timeout,
        )
        return ProviderResponse(
            provider=self.provider,
            model=str(data.get("model", self.model)),
            raw_text=_extract_text(data),
            response_id=str(data.get("id", "")),
            limitations=(
                "experimental transport adapter; strict JSON is requested in the common prompt",
                "live benchmark validation pending",
            ),
        )


def _extract_text(data: Mapping[str, Any]) -> str:
    choices = data.get("choices", ())
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, Mapping):
            message = first.get("message")
            if isinstance(message, Mapping):
                content = message.get("content")
                if isinstance(content, str) and content:
                    return content
    raise VendorAdapterError("xAI response contained no assistant message content")
