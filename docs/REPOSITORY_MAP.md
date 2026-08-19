# Repository Map

| Path | Purpose |
|---|---|
| `genome/` | Canonical model-neutral behavior and governance specification |
| `gnome/` | Human-readable character/mnemonic layer |
| `manifest/` | Machine-readable package metadata and boundaries |
| `protocol/` | Manifestation and transmission procedures |
| `src/fren/` | Executable conformance, provenance, transmission, and investigative-collaborator core |
| `schemas/` | Versioned machine-readable contracts |
| `tests/` | Conformance, adversarial, calibration, ablation, and drift tests |
| `adapters/` | Model/vendor-specific translation layers |
| `research/` | FREN MANIFESTED investigations and case records |
| `provenance/` | Evidence handling and source metadata conventions |
| `security/` | Security notes and propagation defenses |
| `docs/` | Architecture, terminology, reviewer guidance |

## Separation rule

Research evidence does not automatically become part of the FREN Genome. Interesting anomalies remain in `research/` until controlled testing justifies an architectural change.

## Current executable layer

The v0.1-alpha executable core now includes:

- structured response contracts;
- deterministic conformance checks;
- SHA-256 and provenance-graph tooling;
- explicit transmission guards;
- a bounded PI-style investigative-collaborator notebook;
- calibration fixtures for continuity confounds, hidden propagation, and investigation posture;
- CI across supported Python versions.

## Planned next layers

- broaden the canonical calibration fixture set;
- add package manifest generation and release checksums;
- add drift and ablation runners;
- define one generic adapter interface;
- add vendor adapters only after the model-neutral contracts stabilize;
- add cross-model experiment reporting.
