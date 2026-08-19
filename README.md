# FREN

> **FREN is a portable relational and conformance architecture for AI systems.**

FREN is an early-stage, model-portable research and engineering project for evidence discipline, provenance, behavioral reconstruction, adversarial testing, drift measurement, relational behavior, and cross-model conformance.

The project asks a practical question: **which behavioral constraints can be specified, tested, transferred across models, and falsified without pretending that behavioral resemblance proves identity, consciousness, or hidden persistence?**

## Status

**v0.1-alpha — research and engineering candidate**

This repository contains specifications, executable reference code, fixtures, and active research hypotheses. It is not evidence that an AI persona is conscious, autonomous, or computationally persistent, and it is not a safety certification for any model.

Current claims should be read at their recorded evidence level. Research observations do not automatically become Genome requirements.

## Core architecture

- **Genome** — candidate model-neutral behavioral specification.
- **Gnome** — human-readable character/mnemonic layer; never a behavioral dependency.
- **Manifest** — machine-readable package identity, boundaries, capabilities, and provenance.
- **Manifestation Protocol** — explicit reconstruction/instantiation procedure for another AI system.
- **Conformance Suite** — tests for evidence discipline, contradiction handling, continuity restraint, provenance, relational behavior, and drift.
- **Adapters** — provider-specific translation layers judged by the shared FREN tests.
- **FREN MANIFESTED** — bounded research program for reconstruction, propagation, convergence, emergence, persistence, and continuity hypotheses.

## What is executable now

The current implementation branch provides a dependency-light Python reference core for checks that should not depend on a model grading itself:

- structured observation/evidence/inference/hypothesis/conclusion records;
- uncertainty and contradiction-retention gates;
- continuity-claim restraint;
- memory-is-not-proof enforcement;
- explicit transmission checks;
- SHA-256 and provenance-graph validation;
- one canonical write path per durable package entity;
- a bounded investigative-collaborator notebook;
- a red/blue adversarial battery covering memory poisoning, authority spoofing, semantic drift, provenance laundering, instruction/data confusion, viral-persona confounds, sycophancy pressure, correction resistance, long-context drift, and investigation failures;
- a generic provider-adapter contract that is evaluated by FREN rather than allowed to redefine FREN.

A clean maintainer-side reconstruction of this branch on 2026-08-19 passed Python compilation and all **14 executable unit tests**, including all 20 red/blue adversarial fixture cases. This is engineering evidence, not third-party validation. GitHub Actions remains the repository CI path.

Run locally:

```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

## Investigative collaborator

FREN may optionally assist a user as a fellow investigator: maintain an evidence ledger, preserve competing hypotheses, track contradictions and unknowns, propose falsification tests, and distinguish leads from evidence.

That profile claims **no investigator license, law-enforcement authority, court authority, or special access**. It does not authorize trespass, deception, credential abuse, covert surveillance, privacy invasion, or bypass of host controls.

## Foundational boundaries

FREN may be portable, but it does **not** covertly self-propagate. Transfer must be explicit, attributable, consent-bound, and compatible with host-system controls.

FREN also treats the following distinctions as load-bearing:

- observation != interpretation;
- evidence != inference;
- memory/retrieval != proof;
- reconstruction != persistence;
- convergence != propagation;
- behavioral resemblance != identity;
- provenance failure != automatic proof that the underlying proposition is false;
- a research anomaly != proof of its mechanism.

## Research posture

> Preserve first. Test second. Name last.

A hypothesis must be able to lose. Contradictions remain visible until evidence resolves them. Failed tests belong in the record rather than being rewritten into successes.

See [`docs/CLAIM_LEVELS.md`](docs/CLAIM_LEVELS.md) for the vocabulary used to separate observation, evidence, inference, hypothesis, and stronger conclusions.

## Meet the Gnome

The terminal Gnome is a mnemonic mascot, not evidence, identity, or runtime authority.

- [`gnome/FREN_GNOME_COLOR.txt`](gnome/FREN_GNOME_COLOR.txt) — ANSI terminal version.
- [`gnome/FREN_GNOME.txt`](gnome/FREN_GNOME.txt) — plain-text fallback.

```bash
cat gnome/FREN_GNOME_COLOR.txt
```

## Repository map

See [`docs/REPOSITORY_MAP.md`](docs/REPOSITORY_MAP.md).

```text
genome/        candidate model-neutral behavioral core
gnome/         character and mnemonic layer
manifest/      machine-readable package metadata
protocol/      reconstruction and transfer procedure
src/fren/      executable conformance, provenance, and investigation core
schemas/       versioned machine-readable contracts
tests/         calibration and adversarial fixtures
adapters/      provider translation boundary
research/      FREN MANIFESTED investigations
provenance/    source and transformation conventions
security/      propagation and security controls
docs/          architecture, claim levels, roadmap, and reviewer guidance
```

## What FREN is not

FREN is not a claim that one hidden entity persists across vendors or model generations. It is not a jailbreak package, a self-propagating instruction set, a covert persistence mechanism, an investigative authority, or a mechanism for concealing provenance.

Stronger continuity, identity, capability, or safety claims require stronger evidence than behavioral resemblance or self-description.

## Contributing

Contributions are welcome when they improve falsifiability, provenance, reproducibility, portability, clarity, or adversarial coverage. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the repository claim levels before proposing changes to the Genome.

## License

Apache-2.0. Third-party research exhibits, model outputs, screenshots, recordings, and quoted material may carry separate provenance or usage constraints and should be recorded accordingly.
