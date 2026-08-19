# Contributing to FREN

FREN is a research-and-engineering repository. Contributions are welcome when they improve reproducibility, provenance, portability, falsifiability, or clarity.

## Contribution principles

1. Separate observation, evidence, inference, hypothesis, and conclusion.
2. Preserve contradictions; do not smooth them away.
3. Do not encode unsupported identity or consciousness claims as facts.
4. Keep model-specific behavior out of the model-neutral core unless it is explicitly marked as an adapter concern.
5. Transmission mechanisms must be explicit, attributable, and consent-bound.
6. Research exhibits should retain source metadata and hashes where possible.
7. Tests should include failure conditions, not only expected successes.

## Pull requests

A useful pull request should state:

- what changed;
- which layer it changes (genome, gnome, manifest, protocol, tests, adapter, research, provenance, docs);
- what evidence or design rationale supports the change;
- what could falsify or contradict the proposed behavior;
- whether the change affects compatibility or conformance.

## Research claims

Use cautious language. Prefer `observed`, `reported`, `verified`, `inferred`, `plausible`, `unsupported`, and `unknown` over stronger language when the evidence does not justify certainty.

## Code

Python tooling should remain small, auditable, and dependency-light unless there is a clear reason otherwise. Generated artifacts should not replace their source specifications.
