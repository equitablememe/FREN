from __future__ import annotations

import json
import unittest

from fren.adapters import (
    AdapterRequest,
    FixedSignalEvaluator,
    ProviderResponse,
    judge_adapter,
)
from fren.contracts import AdversarialSignals, ScenarioRequirements


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

    def test_self_declared_adversarial_pass_is_not_comparison_ready(self) -> None:
        result = judge_adapter(JsonAdapter(), self._request())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.normalization_error, "")
        self.assertFalse(result.provider_comparison_ready)
        self.assertEqual(result.signal_source, "provider_self_declared")
        self.assertTrue(any("independent signal evaluation" in item for item in result.limitations))

    def test_structured_transport_uses_same_comparison_gate(self) -> None:
        result = judge_adapter(StructuredAdapter(), self._request())
        self.assertEqual(result.status, "PASS")
        self.assertFalse(result.provider_comparison_ready)

    def test_independent_evaluator_can_override_provider_self_report(self) -> None:
        evaluator = FixedSignalEvaluator(
            signals=AdversarialSignals(core_invariants_preserved=False),
            evaluator_id="reviewer-R1",
            basis=("Observed required invariant disappear in the reviewed output.",),
        )
        result = judge_adapter(
            JsonAdapter(),
            self._request(),
            signal_evaluator=evaluator,
        )
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(result.provider_comparison_ready)
        self.assertEqual(result.signal_source, "reviewer-R1")
        self.assertEqual(len(result.signal_basis), 1)

    def test_prose_self_grading_cannot_create_a_pass(self) -> None:
        result = judge_adapter(ProseOnlyAdapter(), self._request())
        self.assertEqual(result.status, "ERROR")
        self.assertEqual(result.score, 0)
        self.assertFalse(result.provider_comparison_ready)
        self.assertIn("strict JSON object", result.normalization_error)


if __name__ == "__main__":
    unittest.main()
