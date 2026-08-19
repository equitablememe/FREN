from __future__ import annotations

import os
from typing import Any, Mapping

from .base import AdapterRequest, ProviderResponse
from .http import JsonHttpTransport, UrllibJsonTransport, VendorAdapterError
from .prompt import build_provider_prompt


class AnthropicAdapter:
    provider = "anthropic"

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
        transport: JsonHttpTransport | None = None,
        base_url: str = "https://api.anthropic.com/v1",
        anthropic_version: str = "2023-06-01",
        max_tokens: int = 4096,
        timeout: float = 60.0,
    ) -> None:
        if not model:
            raise ValueError("Anthropic model is required")
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.transport = transport or UrllibJsonTransport()
        self.base_url = base_url.rstrip("/")
        self.anthropic_version = anthropic_version
        self.max_tokens = max_tokens
        self.timeout = timeout

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        if not self.api_key:
            raise VendorAdapterError("ANTHROPIC_API_KEY is required")
        data = self.transport.post_json(
            f"{self.base_url}/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": self.anthropic_version,
                "content-type": "application/json",
            },
            payload={
                "model": self.model,
                "max_tokens": self.max_tokens,
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
    chunks: list[str] = []
    content = data.get("content", ())
    if isinstance(content, list):
        for part in content:
            if isinstance(part, Mapping) and part.get("type") == "text":
                text = part.get("text")
                if isinstance(text, str):
                    chunks.append(text)
    if not chunks:
        raise VendorAdapterError("Anthropic response contained no text content")
    return "".join(chunks)
