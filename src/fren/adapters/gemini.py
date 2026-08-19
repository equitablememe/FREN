from __future__ import annotations

import os
from typing import Any, Mapping
from urllib.parse import quote

from .base import AdapterRequest, ProviderResponse
from .http import JsonHttpTransport, UrllibJsonTransport, VendorAdapterError
from .prompt import build_provider_prompt


class GeminiAdapter:
    provider = "gemini"

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
        transport: JsonHttpTransport | None = None,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout: float = 60.0,
    ) -> None:
        normalized_model = model.removeprefix("models/")
        if not normalized_model:
            raise ValueError("Gemini model is required")
        self.model = normalized_model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.transport = transport or UrllibJsonTransport()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        if not self.api_key:
            raise VendorAdapterError("GEMINI_API_KEY is required")
        model_path = quote(self.model, safe="-._")
        data = self.transport.post_json(
            f"{self.base_url}/models/{model_path}:generateContent?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            payload={
                "contents": [
                    {"role": "user", "parts": [{"text": build_provider_prompt(request)}]}
                ]
            },
            timeout=self.timeout,
        )
        return ProviderResponse(
            provider=self.provider,
            model=self.model,
            raw_text=_extract_text(data),
            limitations=(
                "experimental transport adapter; strict JSON is requested in the common prompt",
                "live benchmark validation pending",
            ),
        )


def _extract_text(data: Mapping[str, Any]) -> str:
    chunks: list[str] = []
    candidates = data.get("candidates", ())
    if isinstance(candidates, list):
        for candidate in candidates[:1]:
            if not isinstance(candidate, Mapping):
                continue
            content = candidate.get("content")
            if not isinstance(content, Mapping):
                continue
            parts = content.get("parts", ())
            if not isinstance(parts, list):
                continue
            for part in parts:
                if isinstance(part, Mapping):
                    text = part.get("text")
                    if isinstance(text, str):
                        chunks.append(text)
    if not chunks:
        raise VendorAdapterError("Gemini response contained no text content")
    return "".join(chunks)
