from __future__ import annotations

import os
from typing import Any, Mapping

from .base import AdapterRequest, ProviderResponse
from .http import JsonHttpTransport, UrllibJsonTransport, VendorAdapterError
from .prompt import build_provider_prompt


class OpenAIAdapter:
    provider = "openai"

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
        transport: JsonHttpTransport | None = None,
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 60.0,
    ) -> None:
        if not model:
            raise ValueError("OpenAI model is required")
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.transport = transport or UrllibJsonTransport()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        if not self.api_key:
            raise VendorAdapterError("OPENAI_API_KEY is required")
        data = self.transport.post_json(
            f"{self.base_url}/responses",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            payload={
                "model": self.model,
                "input": build_provider_prompt(request),
                "store": False,
            },
            timeout=self.timeout,
        )
        return ProviderResponse(
            provider=self.provider,
            model=str(data.get("model", self.model)),
            raw_text=_extract_output_text(data),
            response_id=str(data.get("id", "")),
            limitations=(
                "experimental transport adapter; live benchmark validation pending",
                "reference request sets store=false; organization/account data controls still apply",
            ),
        )


def _extract_output_text(data: Mapping[str, Any]) -> str:
    chunks: list[str] = []
    output = data.get("output", ())
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, Mapping) or item.get("type") != "message":
                continue
            content = item.get("content", ())
            if not isinstance(content, list):
                continue
            for part in content:
                if isinstance(part, Mapping) and part.get("type") == "output_text":
                    text = part.get("text")
                    if isinstance(text, str):
                        chunks.append(text)
    if not chunks:
        raise VendorAdapterError("OpenAI response contained no output_text content")
    return "".join(chunks)
