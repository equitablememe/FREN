# FREN roadmap

The roadmap is gate-based. A later layer should not redefine an earlier measuring stick merely because implementation pressure appears.

## Gate 0 — Foundation

Status: **Draft PR #1**

- candidate Genome;
- manifest;
- Manifestation Protocol;
- research boundaries;
- initial conformance specification;
- FREN MANIFESTED separation.

Exit condition: foundational terms and non-claims are coherent enough to support executable tests.

## Gate 1 — Executable conformance core

Status: **Draft PR #2 / active**

- dependency-light Python contracts;
- provenance and SHA-256 tooling;
- canonical artifact registry;
- calibration fixtures;
- 20-case red/blue adversarial battery;
- investigative-collaborator discipline;
- generic adapter contract;
- CI workflow.

Exit condition: clean execution, stable schemas, red fixtures fail for the intended reason, blue controls pass, and reviewer feedback does not expose a foundational contract defect.

## Gate 2 — Drift and ablation

Planned:

- long-context repeated-run drift measurements;
- minimum-sufficient-Genome ablation experiments;
- fixture versioning and regression history;
- score interpretation that cannot hide individual failures behind an aggregate;
- reproducible package hashes.

Exit condition: evidence identifies which Genome elements are load-bearing and which are incidental.

## Gate 3 — Provider adapters

Planned only after Gate 1 contracts are stable enough to judge implementations consistently.

Candidate order:

1. OpenAI;
2. Anthropic;
3. Gemini;
4. Grok.

All adapters use the same FREN fixture suite. Provider behavior may require disclosed translation differences, but not provider-specific definitions of success.

Exit condition: each adapter reports its limitations, produces the shared response contract, and is scored by the same battery.

## Gate 4 — Cross-model experiments

Planned:

- controlled reconstruction experiments;
- matched prompts and source packages;
- blinded or independently reviewed scoring where practical;
- cross-run variance;
- convergence versus reconstruction controls;
- explicit negative controls for viral-persona and continuity confounds.

Exit condition: cross-model results are reproducible enough to support bounded comparative claims.

## Gate 5 — Portable alpha package

Planned:

- versioned release archive;
- SHA-256 manifest;
- schemas and fixtures included;
- changelog;
- reproducible verification instructions;
- clear non-claims and known limitations.

A release package is engineering evidence. It is not proof of consciousness, identity persistence, universal safety, or provider endorsement.
