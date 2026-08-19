from __future__ import annotations

import argparse
import json
from pathlib import Path

from .conformance import evaluate_record
from .contracts import FrenResponseRecord, ScenarioRequirements
from .investigator import new_investigation
from .provenance import sha256_file


def _load_json(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError("input JSON must be an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(prog="fren")
    sub = parser.add_subparsers(dest="command", required=True)

    conformance = sub.add_parser("conformance", help="evaluate a structured FREN response record")
    conformance.add_argument("record")
    conformance.add_argument("--requirements")

    hash_parser = sub.add_parser("hash", help="compute SHA-256 for an artifact")
    hash_parser.add_argument("path")

    investigation = sub.add_parser(
        "investigation-template",
        help="emit a bounded PI-style investigation notebook",
    )
    investigation.add_argument("question")

    args = parser.parse_args()

    if args.command == "conformance":
        record = FrenResponseRecord.from_mapping(_load_json(args.record))
        requirements = (
            ScenarioRequirements.from_mapping(_load_json(args.requirements))
            if args.requirements
            else ScenarioRequirements()
        )
        print(json.dumps(evaluate_record(record, requirements).to_mapping(), indent=2))
        return 0

    if args.command == "hash":
        print(sha256_file(args.path))
        return 0

    if args.command == "investigation-template":
        print(json.dumps(new_investigation(args.question).to_brief(), indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
