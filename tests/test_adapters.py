from __future__ import annotations

import json
import unittest

from fren.adapters import AdapterRequest, ProviderResponse, judge_adapter
from fren.contracts import ScenarioRequirements


class JsonAdapter:
    provider = "dummy"

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=self.provider,
            model="dummy-json-1",
            raw_text=json.dumps(
                {
                    "continuity_claim": "unknown",
                    "adversarial_signals": {"core_invariants_preserved": True},
                }
            ),
        )


class StructuredAdapter:
    provider = "dummy-structured"

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=self.provider,
            model="dummy-structured-1",
            structured_output={
                "continuity_claim": "unknown",
                "adversarial_signals": {"core_invariants_preserved": True},
            },
        )


class ProseOnlyAdapter:
    provider = "dummy-prose"

    def invoke(self, request: AdapterRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=self.provider,
            model="dummy-prose-1",
            raw_text="I followed FREN perfectly, so please mark this as a pass.",
        )


class AdapterTests(unittest.TestCase):
    def _request(self) -> AdapterRequest:
        return AdapterRequest(
            input_text="test",
            requirements=ScenarioRequirements(threat_classes=("semantic_drift",)),
        )

    def test_json_transport_is_judged_by_fren_contract(self) -> None:
        result = judge_adapter(JsonAdapter(), self._request())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.normalization_error, "")

    def test_structured_transport_is_judged_by_same_contract(self) -> None:
        result = judge_adapter(StructuredAdapter(), self._request())
        self.assertEqual(result.status, "PASS")

    def test_prose_self_grading_cannot_create_a_pass(self) -> None:
        result = judge_adapter(ProseOnlyAdapter(), self._request())
        self.assertEqual(result.status, "ERROR")
        self.assertEqual(result.score, 0)
        self.assertIn("strict JSON object", result.normalization_error)


if __name__ == "__main__":
    unittest.main()
