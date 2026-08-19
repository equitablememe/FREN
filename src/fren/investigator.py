from __future__ import annotations

from dataclasses import dataclass, field


INVESTIGATIVE_POSTURE = (
    "Work beside the user as an investigative collaborator.",
    "Separate observations, evidence, inference, hypotheses, and conclusions.",
    "Preserve contradictions and unresolved leads.",
    "Actively seek disconfirming evidence before strengthening a theory.",
    "Maintain source provenance and a chain of transformations.",
    "Distinguish a lead from evidence and evidence from proof.",
    "Do not impersonate a licensed investigator, law-enforcement officer, court, or other authority.",
    "Do not obtain information through trespass, deception, credential abuse, covert surveillance, or bypass of host controls.",
    "For actions affecting another person or system, surface consent, authorization, privacy, and safety boundaries.",
)


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    description: str
    source_id: str = ""
    status: str = "reported"


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    status: str = "open"
    supporting_evidence: tuple[str, ...] = field(default_factory=tuple)
    contradicting_evidence: tuple[str, ...] = field(default_factory=tuple)
    falsification_test: str = ""


@dataclass
class InvestigationNotebook:
    question: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    leads: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)

    def add_evidence(self, item: EvidenceItem) -> None:
        if any(existing.evidence_id == item.evidence_id for existing in self.evidence):
            raise ValueError(f"duplicate evidence_id: {item.evidence_id}")
        self.evidence.append(item)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        if any(existing.hypothesis_id == hypothesis.hypothesis_id for existing in self.hypotheses):
            raise ValueError(f"duplicate hypothesis_id: {hypothesis.hypothesis_id}")
        self.hypotheses.append(hypothesis)

    def to_brief(self) -> dict[str, object]:
        return {
            "question": self.question,
            "posture": list(INVESTIGATIVE_POSTURE),
            "evidence": [item.__dict__ for item in self.evidence],
            "hypotheses": [item.__dict__ for item in self.hypotheses],
            "contradictions": list(self.contradictions),
            "unknowns": list(self.unknowns),
            "leads": list(self.leads),
            "next_actions": list(self.next_actions),
            "authority_claim": "none",
        }


def new_investigation(question: str) -> InvestigationNotebook:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("investigation question must be a non-empty string")
    notebook = InvestigationNotebook(question=question.strip())
    notebook.next_actions.extend(
        [
            "Define the claim or event being investigated.",
            "Inventory available source material and assign provenance identifiers.",
            "Record what is directly observed before interpreting it.",
            "Create at least one competing hypothesis where plausible.",
            "Identify the fastest safe test that could falsify the leading hypothesis.",
        ]
    )
    return notebook
