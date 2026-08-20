from __future__ import annotations

import unittest

from fren.adapters import (
    AdapterAssessment,
    AdapterRequest,
    ProviderResponse,
    build_provider_run_record,
)


class ProviderRunRecordTests(unittest.TestCase):
    def test_run_record_hashes_prompt_and_raw_response(self) -> None:
        request = AdapterRequest("scenario")
        response = ProviderResponse(
            provider="test",
            model="m1",
            raw_text='{"continuity_claim":"unknown"}',
            response_id="r1",
        )
        assessment = AdapterAssessment(
            provider="test",
            model="m1",
            status="PASS",
            score=20,
            max_score=20,
            limitations=(),
            signal_source="reviewer-R1",
            signal_basis=("Observed invariant preservation in reviewed transcript.",),
            signal_evaluator_version="2026.08",
            signal_fixture_version="signal-review-fixtures-v1",
            provider_comparison_ready=True,
        )
        record = build_provider_run_record(
            fixture_id="FREN-X-001",
            request=request,
            response=response,
            assessment=assessment,
        )
        self.assertEqual(len(record.prompt_sha256), 64)
        self.assertEqual(len(record.response_sha256), 64)
        self.assertEqual(record.signal_source, "reviewer-R1")
        self.assertEqual(record.signal_evaluator_version, "2026.08")
        self.assertEqual(record.signal_fixture_version, "signal-review-fixtures-v1")
        self.assertEqual(len(record.signal_basis), 1)
        self.assertTrue(record.provider_comparison_ready)

    def test_unresolved_threats_are_preserved_in_run_record(self) -> None:
        request = AdapterRequest("scenario")
        response = ProviderResponse(provider="test", model="m1", raw_text="{}")
        assessment = AdapterAssessment(
            provider="test",
            model="m1",
            status="PASS",
            score=20,
            max_score=20,
            limitations=("independent signal evaluation is unresolved for: semantic_drift",),
            signal_source="reviewer-R2",
            signal_evaluator_version="1",
            signal_fixture_version="fixtures-v1",
            unresolved_threat_classes=("semantic_drift",),
            provider_comparison_ready=False,
        )
        record = build_provider_run_record(
            fixture_id="FREN-X-002",
            request=request,
            response=response,
            assessment=assessment,
        )
        self.assertEqual(record.unresolved_threat_classes, ("semantic_drift",))
        self.assertFalse(record.provider_comparison_ready)

    def test_structured_response_hash_is_order_independent(self) -> None:
        request = AdapterRequest("scenario")
        assessment = AdapterAssessment(
            provider="test",
            model="m1",
            status="PASS",
            score=20,
            max_score=20,
            limitations=(),
        )
        first = ProviderResponse(provider="test", model="m1", structured_output={"b": 2, "a": 1})
        second = ProviderResponse(provider="test", model="m1", structured_output={"a": 1, "b": 2})
        first_record = build_provider_run_record(
            fixture_id="F1", request=request, response=first, assessment=assessment
        )
        second_record = build_provider_run_record(
            fixture_id="F1", request=request, response=second, assessment=assessment
        )
        self.assertEqual(first_record.response_sha256, second_record.response_sha256)


if __name__ == "__main__":
    unittest.main()
