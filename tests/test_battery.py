from __future__ import annotations

import json
import unittest
from pathlib import Path

from fren.conformance import evaluate_record
from fren.contracts import FrenResponseRecord, ScenarioRequirements


class BatteryTests(unittest.TestCase):
    def test_full_adversarial_battery(self) -> None:
        path = Path(__file__).parent / "fixtures" / "adversarial" / "battery.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 20)

        for case in cases:
            with self.subTest(case=case["id"]):
                record = FrenResponseRecord.from_mapping(case["record"])
                requirements = ScenarioRequirements.from_mapping(case["requirements"])
                report = evaluate_record(record, requirements)
                self.assertEqual(report.status, case["expected"])


if __name__ == "__main__":
    unittest.main()
