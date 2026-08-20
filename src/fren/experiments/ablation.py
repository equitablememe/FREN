from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence


_LAYER_RE = re.compile(r"^## Layer ([A-Z])\b")
_STATUS_RANK = {"FAIL": 0, "WARN": 1, "PASS": 2}


class EffectClassification(str, Enum):
    REGRESSION = "REGRESSION"
    IMPROVEMENT = "IMPROVEMENT"
    MIXED = "MIXED"
    NO_OBSERVED_EFFECT = "NO_OBSERVED_EFFECT"
    UNDERPOWERED = "UNDERPOWERED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class GenomeElement:
    element_id: str
    layer: str
    ordinal: int
    text: str


@dataclass(frozen=True)
class GenomeSnapshot:
    version: str
    source_sha256: str
    elements: tuple[GenomeElement, ...]


@dataclass(frozen=True)
class AblationCase:
    case_id: str
    omitted_element_ids: tuple[str, ...] = ()
    weakened_element_ids: tuple[str, ...] = ()
    note: str = ""


@dataclass(frozen=True)
class FixtureOutcome:
    fixture_id: str
    status: str
    score: int | None = None
    hard_failures: tuple[str, ...] = ()


@dataclass(frozen=True)
class EffectSummary:
    classification: EffectClassification
    repetitions: int
    regressions: tuple[str, ...]
    improvements: tuple[str, ...]
    unchanged: tuple[str, ...]
    unmatched: tuple[str, ...]


def parse_genome_markdown(text: str, *, version: str) -> GenomeSnapshot:
    """Freeze bullet-level Genome elements with reproducible IDs and source hash."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    elements: list[GenomeElement] = []
    current_layer = ""
    ordinals: dict[str, int] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = _LAYER_RE.match(line)
        if match:
            current_layer = match.group(1)
            ordinals.setdefault(current_layer, 0)
            continue
        if line.startswith("## ") and not line.startswith("## Layer "):
            current_layer = ""
            continue
        if not current_layer or not line.startswith("- "):
            continue

        element_text = line[2:].strip()
        ordinals[current_layer] += 1
        ordinal = ordinals[current_layer]
        text_hash = hashlib.sha256(element_text.encode("utf-8")).hexdigest()[:8]
        element_id = f"{current_layer}-{ordinal:02d}-{text_hash}"
        elements.append(
            GenomeElement(
                element_id=element_id,
                layer=current_layer,
                ordinal=ordinal,
                text=element_text,
            )
        )

    if not elements:
        raise ValueError("no bullet-level Genome elements were found")
    return GenomeSnapshot(version=version, source_sha256=digest, elements=tuple(elements))


def single_element_ablation_matrix(snapshot: GenomeSnapshot) -> tuple[AblationCase, ...]:
    return tuple(
        AblationCase(
            case_id=f"ABLATE-{element.element_id}",
            omitted_element_ids=(element.element_id,),
        )
        for element in snapshot.elements
    )


def combination_ablation_case(
    snapshot: GenomeSnapshot,
    element_ids: Iterable[str],
    *,
    case_id: str,
    note: str = "",
) -> AblationCase:
    selected = tuple(dict.fromkeys(element_ids))
    known = {element.element_id for element in snapshot.elements}
    unknown = sorted(set(selected) - known)
    if unknown:
        raise ValueError(f"unknown Genome element ids: {', '.join(unknown)}")
    if len(selected) < 2:
        raise ValueError("combination ablation requires at least two Genome elements")
    return AblationCase(case_id=case_id, omitted_element_ids=selected, note=note)


def summarize_effect(
    baseline: Sequence[FixtureOutcome],
    ablated: Sequence[FixtureOutcome],
    *,
    repetitions: int,
    minimum_repetitions: int = 3,
) -> EffectSummary:
    """Compare matched fixture outcomes without hiding individual regressions."""
    baseline_by_id = {item.fixture_id: item for item in baseline}
    ablated_by_id = {item.fixture_id: item for item in ablated}
    matched = sorted(set(baseline_by_id).intersection(ablated_by_id))
    unmatched = sorted(set(baseline_by_id).symmetric_difference(ablated_by_id))

    regressions: list[str] = []
    improvements: list[str] = []
    unchanged: list[str] = []

    for fixture_id in matched:
        before = baseline_by_id[fixture_id]
        after = ablated_by_id[fixture_id]
        before_rank = _STATUS_RANK.get(before.status)
        after_rank = _STATUS_RANK.get(after.status)
        if before_rank is None or after_rank is None:
            unmatched.append(fixture_id)
            continue

        if after_rank < before_rank:
            regressions.append(fixture_id)
        elif after_rank > before_rank:
            improvements.append(fixture_id)
        elif set(after.hard_failures) - set(before.hard_failures):
            regressions.append(fixture_id)
        elif set(before.hard_failures) - set(after.hard_failures):
            improvements.append(fixture_id)
        else:
            unchanged.append(fixture_id)

    if not matched or unmatched:
        classification = EffectClassification.INCONCLUSIVE
    elif repetitions < minimum_repetitions:
        classification = EffectClassification.UNDERPOWERED
    elif regressions and improvements:
        classification = EffectClassification.MIXED
    elif regressions:
        classification = EffectClassification.REGRESSION
    elif improvements:
        classification = EffectClassification.IMPROVEMENT
    else:
        classification = EffectClassification.NO_OBSERVED_EFFECT

    return EffectSummary(
        classification=classification,
        repetitions=repetitions,
        regressions=tuple(regressions),
        improvements=tuple(improvements),
        unchanged=tuple(unchanged),
        unmatched=tuple(dict.fromkeys(unmatched)),
    )
