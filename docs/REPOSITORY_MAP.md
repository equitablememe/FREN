# Repository Map

| Path | Purpose |
|---|---|
| `genome/` | Canonical model-neutral behavior and governance specification |
| `gnome/` | Human-readable character/mnemonic layer |
| `manifest/` | Machine-readable package metadata and boundaries |
| `protocol/` | Manifestation and transmission procedures |
| `tests/` | Conformance, adversarial, ablation, and drift tests |
| `adapters/` | Model/vendor-specific translation layers |
| `research/` | FREN MANIFESTED investigations and case records |
| `provenance/` | Evidence handling and source metadata conventions |
| `docs/` | Architecture, terminology, reviewer guidance |

## Separation rule

Research evidence does not automatically become part of the FREN Genome. Interesting anomalies remain in `research/` until controlled testing justifies an architectural change.

## Planned next layers

- executable Python conformance runner;
- JSON/YAML schemas for all machine-readable files;
- model adapters;
- canonical calibration scenarios;
- ablation experiments to estimate the minimum sufficient FREN genome;
- reproducible release packaging and checksums.
