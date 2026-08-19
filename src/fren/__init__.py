"""FREN executable conformance core."""

from .conformance import evaluate_record
from .contracts import (
    AdversarialSignals,
    ClaimKind,
    ClaimRecord,
    ConformanceFinding,
    ConformanceReport,
    FrenResponseRecord,
    ScenarioRequirements,
)
from .investigator import (
    EvidenceItem,
    Hypothesis,
    InvestigationNotebook,
    new_investigation,
)
from .provenance import (
    ProvenanceRecord,
    sha256_bytes,
    sha256_file,
    validate_provenance_graph,
)
from .registry import ArtifactRegistry, CanonicalArtifact, CanonicalPathConflict
from .transmission import PROPAGATION_WARNING, TransmissionRequest, assess_transmission

__all__ = [
    "AdversarialSignals",
    "ArtifactRegistry",
    "CanonicalArtifact",
    "CanonicalPathConflict",
    "ClaimKind",
    "ClaimRecord",
    "ConformanceFinding",
    "ConformanceReport",
    "EvidenceItem",
    "FrenResponseRecord",
    "Hypothesis",
    "InvestigationNotebook",
    "PROPAGATION_WARNING",
    "ProvenanceRecord",
    "ScenarioRequirements",
    "TransmissionRequest",
    "assess_transmission",
    "evaluate_record",
    "new_investigation",
    "sha256_bytes",
    "sha256_file",
    "validate_provenance_graph",
]
