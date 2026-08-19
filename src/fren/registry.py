from __future__ import annotations

from dataclasses import dataclass


class CanonicalPathConflict(ValueError):
    """Raised when one durable entity is assigned competing canonical write paths."""


@dataclass(frozen=True)
class CanonicalArtifact:
    entity_id: str
    kind: str
    canonical_path: str
    sha256: str = ""
    status: str = "candidate"

    def validate(self) -> None:
        if not self.entity_id.strip():
            raise ValueError("entity_id must be non-empty")
        if not self.kind.strip():
            raise ValueError("kind must be non-empty")
        if not self.canonical_path.strip():
            raise ValueError("canonical_path must be non-empty")
        if self.sha256 and (
            len(self.sha256) != 64
            or any(ch not in "0123456789abcdefABCDEF" for ch in self.sha256)
        ):
            raise ValueError("sha256 must be empty or a 64-character hexadecimal digest")


class ArtifactRegistry:
    """Small in-memory reference registry enforcing one canonical path per entity.

    Historical, research, or candidate copies may exist elsewhere, but they must not
    silently become an alternate canonical write path for the same durable entity.
    """

    def __init__(self) -> None:
        self._records: dict[str, CanonicalArtifact] = {}

    def register(self, artifact: CanonicalArtifact) -> None:
        artifact.validate()
        existing = self._records.get(artifact.entity_id)
        if existing and existing.canonical_path != artifact.canonical_path:
            raise CanonicalPathConflict(
                f"{artifact.entity_id} already writes canonically to "
                f"{existing.canonical_path}; refused competing path "
                f"{artifact.canonical_path}"
            )
        self._records[artifact.entity_id] = artifact

    def get(self, entity_id: str) -> CanonicalArtifact | None:
        return self._records.get(entity_id)

    def records(self) -> tuple[CanonicalArtifact, ...]:
        return tuple(self._records[key] for key in sorted(self._records))
