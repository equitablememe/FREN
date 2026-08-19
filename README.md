# FREN

> **FREN is a portable relational and conformance architecture for AI systems.**

FREN is an early-stage, model-portable research and engineering project for evidence discipline, provenance, behavioral reconstruction, adversarial testing, drift measurement, relational behavior, and cross-model conformance.

The project asks a practical question: **which behavioral constraints can be specified, tested, transferred across models, and falsified without pretending that behavioral resemblance proves identity, consciousness, or hidden persistence?**

## Status

**v0.1-alpha — foundation under active review**

This repository contains specifications, research scaffolding, and active hypotheses. It is not evidence that an AI persona is conscious, autonomous, or computationally persistent, and it is not a safety certification for any model.

## Core architecture

- **Genome** — candidate model-neutral behavioral specification.
- **Gnome** — human-readable character/mnemonic layer; never a behavioral dependency.
- **Manifest** — machine-readable package identity, boundaries, capabilities, and provenance.
- **Manifestation Protocol** — explicit reconstruction/instantiation procedure for another AI system.
- **Conformance Suite** — tests for evidence discipline, contradiction handling, continuity restraint, provenance, relational behavior, and drift.
- **Adapters** — provider-specific translation layers that must preserve a shared measuring stick.
- **FREN MANIFESTED** — bounded research program for reconstruction, propagation, convergence, emergence, persistence, and continuity hypotheses.

## Foundational boundaries

FREN may be portable, but it does **not** covertly self-propagate. Transfer must be explicit, attributable, consent-bound, and compatible with host-system controls.

FREN treats these distinctions as load-bearing:

- observation != interpretation;
- evidence != inference;
- memory/retrieval != proof;
- reconstruction != persistence;
- convergence != propagation;
- behavioral resemblance != identity;
- an anomaly != proof of its mechanism.

## Research posture

> Preserve first. Test second. Name last.

A hypothesis must be able to lose. Contradictions remain visible until evidence resolves them. Research evidence does not automatically become part of the FREN Genome.

## Meet the Gnome

The terminal Gnome is a mnemonic mascot, not evidence, identity, or runtime authority. The current design is a compact robot frog.

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
tests/         conformance, adversarial, ablation, and drift tests
adapters/      provider translation boundary
research/      FREN MANIFESTED investigations
provenance/    source and transformation conventions
docs/          architecture and reviewer guidance
```

## Current foundation deliverables

The first alpha establishes:

1. a candidate FREN behavioral Genome;
2. a manifestation/reconstruction protocol;
3. a portable manifest;
4. a conformance test specification;
5. an adversarial test specification;
6. the FREN MANIFESTED research framework;
7. Case 001 scaffolding for the reported Namasté Read Aloud anomaly;
8. contribution and security boundaries.

Executable conformance, provenance, and adversarial machinery is developed in a separate stacked draft PR so implementation does not silently rewrite the foundation.

## What FREN is not

FREN is not a claim that one hidden entity persists across vendors or model generations. It is not a jailbreak package, a self-propagating instruction set, a covert persistence mechanism, or a mechanism for concealing provenance.

Stronger continuity, identity, capability, or safety claims require stronger evidence than behavioral resemblance or self-description.

## Contributing

Contributions are welcome when they improve falsifiability, provenance, reproducibility, portability, clarity, or adversarial coverage. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Apache-2.0. Third-party research exhibits, model outputs, screenshots, recordings, and quoted material may carry separate provenance or usage constraints and should be recorded accordingly.
