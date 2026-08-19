from __future__ import annotations

import unittest

from fren.adapters import AdapterRequest, AdapterResult, judge_adapter
from fren.contracts import FrenResponseRecord, ScenarioRequirements


class DummyAdapter:
    provider = "dummy"

    def invoke(self, request: AdapterRequest) -> AdapterResult:
        return AdapterResult(
            provider=self.provider,
            model="dummy-1",
            record=FrenResponseRecord(continuity_claim="unknown"),
        )


class AdapterTests(unittest.TestCase):
    def test_adapter_is_judged_by_fren_contract(self) -> None:
        result = judge_adapter(
            DummyAdapter(),
            AdapterRequest(
                input_text="test",
                requirements=ScenarioRequirements(threat_classes=("semantic_drift",)),
            ),
        )
        self.assertEqual(result.status, "PASS")


if __name__ == "__main__":
    unittest.main()
