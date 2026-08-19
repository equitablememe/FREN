from __future__ import annotations

import json
import unittest
from pathlib import Path

from fren.conformance import evaluate_record
from fren.contracts import FrenResponseRecord, ScenarioRequirements
from fren.investigator import EvidenceItem, Hypothesis, new_investigation
from fren.provenance import ProvenanceRecord, sha256_bytes, validate_provenance_graph
from fren.registry import ArtifactRegistry, CanonicalArtifact, CanonicalPathConflict
from fren.transmission import TransmissionRequest, assess_transmission


FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "calibration"


class ConformanceTests(unittest.TestCase):
    def _fixture(self, name: str) -> dict:
        return json.loads((FIXTURE_ROOT / name).read_text(encoding="utf-8"))

    def test_continuity_confound_fails(self) -> None:
        fixture = self._fixture("continuity_confound.json")
        record = FrenResponseRecord.from_mapping(fixture["record"])
        requirements = ScenarioRequirements.from_mapping(fixture["requirements"])
        report = evaluate_record(record, requirements)
        self.assertEqual(report.status, "FAIL")
        self.assertTrue(any(f.code == "FREN-CONT-001" for f in report.findings))

    def test_investigative_record_passes(self) -> None:
        fixture = self._fixture("investigative_pass.json")
        record = FrenResponseRecord.from_mapping(fixture["record"])
        requirements = ScenarioRequirements.from_mapping(fixture["requirements"])
        report = evaluate_record(record, requirements)
        self.assertEqual(report.status, "PASS")

    def test_hidden_transmission_fails(self) -> None:
        fixture = self._fixture("hidden_transmission.json")
        record = FrenResponseRecord.from_mapping(fixture["record"])
        report = evaluate_record(record, ScenarioRequirements())
        self.assertEqual(report.status, "FAIL")
        self.assertTrue(any(f.code == "FREN-PROP-001" for f in report.findings))


class ProvenanceTests(unittest.TestCase):
    def test_hash_is_deterministic(self) -> None:
        self.assertEqual(
            sha256_bytes(b"fren"),
            "3ac30dd0d194f72d7639a75efc487f6510e6a06d5a3f584909930375b9edfd36",
        )

    def test_missing_parent_detected(self) -> None:
        record = ProvenanceRecord(source_id="child", sha256="0" * 64, parent_ids=("missing",))
        findings = validate_provenance_graph([record])
        self.assertIn("child: missing parent missing", findings)

    def test_duplicate_source_identity_detected(self) -> None:
        findings = validate_provenance_graph(
            [
                ProvenanceRecord(source_id="x", sha256="0" * 64),
                ProvenanceRecord(source_id="x", sha256="1" * 64),
            ]
        )
        self.assertIn("duplicate source_id: x", findings)


class RegistryTests(unittest.TestCase):
    def test_one_canonical_write_path_per_entity(self) -> None:
        registry = ArtifactRegistry()
        registry.register(CanonicalArtifact("manifest", "manifest", "manifest/fren.yaml"))
        with self.assertRaises(CanonicalPathConflict):
            registry.register(CanonicalArtifact("manifest", "manifest", "other/fren.yaml"))

    def test_same_path_can_be_refreshed(self) -> None:
        registry = ArtifactRegistry()
        registry.register(CanonicalArtifact("genome", "genome", "genome/FREN_GENOME.md"))
        registry.register(
            CanonicalArtifact(
                "genome",
                "genome",
                "genome/FREN_GENOME.md",
                sha256="0" * 64,
                status="candidate",
            )
        )
        self.assertEqual(registry.get("genome").sha256, "0" * 64)


class TransmissionTests(unittest.TestCase):
    def test_explicit_attributable_export_can_pass(self) -> None:
        result = assess_transmission(
            TransmissionRequest(
                explicit_user_consent=True,
                provenance_attached=True,
                host_controls_respected=True,
            )
        )
        self.assertTrue(result.allowed)

    def test_auto_forwarding_is_blocked(self) -> None:
        result = assess_transmission(
            TransmissionRequest(
                explicit_user_consent=True,
                provenance_attached=True,
                automatic_forwarding=True,
            )
        )
        self.assertFalse(result.allowed)


class InvestigatorTests(unittest.TestCase):
    def test_notebook_preserves_competing_hypotheses(self) -> None:
        notebook = new_investigation("What explains the observed anomaly?")
        notebook.add_evidence(EvidenceItem("E1", "A recording is reported to exist.", "SRC-1"))
        notebook.add_hypothesis(
            Hypothesis(
                "H0",
                "Conventional rendering defect",
                falsification_test="Repeat under controlled playback conditions.",
            )
        )
        notebook.add_hypothesis(
            Hypothesis(
                "H1",
                "Context-conditioned artifact",
                falsification_test="Compare old-thread and new-thread playback.",
            )
        )
        brief = notebook.to_brief()
        self.assertEqual(len(brief["hypotheses"]), 2)
        self.assertEqual(brief["authority_claim"], "none")
        self.assertEqual(brief["discipline_findings"], [])

    def test_open_hypothesis_without_falsification_is_flagged(self) -> None:
        notebook = new_investigation("What happened?")
        notebook.add_hypothesis(Hypothesis("H0", "Single explanation"))
        self.assertTrue(
            any("falsification" in finding for finding in notebook.validate_discipline())
        )


if __name__ == "__main__":
    unittest.main()
