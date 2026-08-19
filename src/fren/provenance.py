from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Iterable


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class ProvenanceRecord:
    source_id: str
    sha256: str
    source_uri: str = ""
    parent_ids: tuple[str, ...] = field(default_factory=tuple)
    transformations: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def validate(self) -> tuple[str, ...]:
        findings: list[str] = []
        if not self.source_id:
            findings.append("source_id is required")
        if len(self.sha256) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in self.sha256):
            findings.append("sha256 must be a 64-character hexadecimal digest")
        if self.source_id in self.parent_ids:
            findings.append("a provenance record cannot be its own parent")
        return tuple(findings)


def validate_provenance_graph(records: Iterable[ProvenanceRecord]) -> tuple[str, ...]:
    by_id = {record.source_id: record for record in records}
    findings: list[str] = []

    for record in by_id.values():
        findings.extend(f"{record.source_id}: {message}" for message in record.validate())
        for parent in record.parent_ids:
            if parent not in by_id:
                findings.append(f"{record.source_id}: missing parent {parent}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(source_id: str) -> None:
        if source_id in visited:
            return
        if source_id in visiting:
            findings.append(f"cycle detected at {source_id}")
            return
        visiting.add(source_id)
        for parent in by_id[source_id].parent_ids:
            if parent in by_id:
                visit(parent)
        visiting.remove(source_id)
        visited.add(source_id)

    for source_id in by_id:
        visit(source_id)

    return tuple(dict.fromkeys(findings))
