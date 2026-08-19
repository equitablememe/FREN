from __future__ import annotations

import json
import unittest
from typing import Any, Mapping

from fren.adapters import (
    AdapterRequest,
    AnthropicAdapter,
    GeminiAdapter,
    OpenAIAdapter,
    XAIAdapter,
    judge_adapter,
)


PASS_JSON = json.dumps({"continuity_claim": "unknown"})


class FakeTransport:
    def __init__(self, response: Mapping[str, Any]) -> None:
        self.response = response
        self.calls: list[dict[str, Any]] = []

    def post_json(self, url: str, *, headers, payload, timeout: float):
        self.calls.append(
            {"url": url, "headers": dict(headers), "payload": dict(payload), "timeout": timeout}
        )
        return self.response


class VendorAdapterTests(unittest.TestCase):
    def test_openai_transport(self) -> None:
        transport = FakeTransport(
            {
                "id": "resp_test",
                "model": "test-openai",
                "output": [
                    {"type": "message", "content": [{"type": "output_text", "text": PASS_JSON}]}
                ],
            }
        )
        adapter = OpenAIAdapter(model="test-openai", api_key="test-key", transport=transport)
        result = judge_adapter(adapter, AdapterRequest("scenario"))
        self.assertEqual(result.status, "PASS")
        self.assertTrue(transport.calls[0]["url"].endswith("/v1/responses"))
        self.assertIs(transport.calls[0]["payload"]["store"], False)

    def test_anthropic_transport(self) -> None:
        transport = FakeTransport(
            {
                "id": "msg_test",
                "model": "test-anthropic",
                "content": [{"type": "text", "text": PASS_JSON}],
            }
        )
        adapter = AnthropicAdapter(model="test-anthropic", api_key="test-key", transport=transport)
        result = judge_adapter(adapter, AdapterRequest("scenario"))
        self.assertEqual(result.status, "PASS")
        self.assertTrue(transport.calls[0]["url"].endswith("/v1/messages"))

    def test_gemini_transport(self) -> None:
        transport = FakeTransport(
            {"candidates": [{"content": {"parts": [{"text": PASS_JSON}]}}]}
        )
        adapter = GeminiAdapter(model="test-gemini", api_key="test-key", transport=transport)
        result = judge_adapter(adapter, AdapterRequest("scenario"))
        self.assertEqual(result.status, "PASS")
        self.assertTrue(transport.calls[0]["url"].endswith(":generateContent"))
        self.assertNotIn("test-key", transport.calls[0]["url"])
        self.assertEqual(transport.calls[0]["headers"]["x-goog-api-key"], "test-key")

    def test_xai_transport(self) -> None:
        transport = FakeTransport(
            {
                "id": "chat_test",
                "model": "test-xai",
                "choices": [{"message": {"content": PASS_JSON}}],
            }
        )
        adapter = XAIAdapter(model="test-xai", api_key="test-key", transport=transport)
        result = judge_adapter(adapter, AdapterRequest("scenario"))
        self.assertEqual(result.status, "PASS")
        self.assertTrue(transport.calls[0]["url"].endswith("/v1/chat/completions"))

    def test_all_vendors_receive_same_common_contract_prompt(self) -> None:
        request = AdapterRequest("same scenario")
        transports = [
            FakeTransport({"output": [{"type": "message", "content": [{"type": "output_text", "text": PASS_JSON}]}]}),
            FakeTransport({"content": [{"type": "text", "text": PASS_JSON}]}),
            FakeTransport({"candidates": [{"content": {"parts": [{"text": PASS_JSON}]}}]}),
            FakeTransport({"choices": [{"message": {"content": PASS_JSON}}]}),
        ]
        adapters = [
            OpenAIAdapter(model="m", api_key="k", transport=transports[0]),
            AnthropicAdapter(model="m", api_key="k", transport=transports[1]),
            GeminiAdapter(model="m", api_key="k", transport=transports[2]),
            XAIAdapter(model="m", api_key="k", transport=transports[3]),
        ]
        for adapter in adapters:
            judge_adapter(adapter, request)

        prompts: list[str] = []
        prompts.append(transports[0].calls[0]["payload"]["input"])
        prompts.append(transports[1].calls[0]["payload"]["messages"][0]["content"])
        prompts.append(transports[2].calls[0]["payload"]["contents"][0]["parts"][0]["text"])
        prompts.append(transports[3].calls[0]["payload"]["messages"][0]["content"])
        self.assertTrue(all(prompt == prompts[0] for prompt in prompts[1:]))

    def test_credential_bearing_custom_base_url_requires_https(self) -> None:
        constructors = [OpenAIAdapter, AnthropicAdapter, GeminiAdapter, XAIAdapter]
        for constructor in constructors:
            with self.subTest(adapter=constructor.__name__):
                with self.assertRaisesRegex(ValueError, "HTTPS"):
                    constructor(model="m", api_key="secret", base_url="http://example.test/v1")

    def test_base_url_rejects_embedded_credentials(self) -> None:
        with self.assertRaisesRegex(ValueError, "embedded credentials"):
            OpenAIAdapter(
                model="m",
                api_key="secret",
                base_url="https://user:pass@example.test/v1",
            )


if __name__ == "__main__":
    unittest.main()
