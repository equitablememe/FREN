# FREN roadmap

The roadmap is gate-based. A later layer should not redefine an earlier measuring stick merely because implementation pressure appears.

## Gate 0 — Foundation

Status: **merged to `main` / still an alpha foundation**

- candidate Genome;
- manifest;
- Manifestation Protocol;
- research boundaries;
- initial conformance specification;
- FREN MANIFESTED separation;
- research-first public front door and compact robot-frog mnemonic.

The foundation is usable as a review baseline, but its minimum-sufficiency claim remains provisional pending ablation.

## Gate 1 — Executable conformance core

Status: **merged to `main` in PR #5 / alpha implementation**

Implemented:

- dependency-light Python contracts;
- provenance and SHA-256 tooling;
- canonical artifact registry;
- calibration fixtures;
- 20-case red/blue adversarial battery;
- investigative-collaborator discipline;
- FREN-owned strict provider-output normalization;
- independent signal-evaluator interface;
- CI workflow across Python 3.11, 3.12, and 3.13.

PR #5 was merged on 2026-08-19. Its merge establishes the current executable alpha baseline; it does not satisfy the later independent-evaluation, ablation, cross-model, or release gates.

## Gate 2 — Provider transport adapters

Status: **experimental scaffolds merged in PR #5; live comparison remains gated**

Current transports:

1. OpenAI;
2. Anthropic;
3. Gemini;
4. xAI/Grok.

The adapters are transport-only. They return raw or provider-structured output to a FREN-owned normalizer and cannot construct their own conformance record or pass rules.

Before comparative provider claims are allowed:

- all four transports must continue to pass contract tests;
- live runs must use explicit model identifiers and recorded provider/API configuration;
- adversarial signals must come from a separate FREN-side evaluator or reviewer rather than provider self-declaration;
- source prompts, response identifiers where available, limitations, and run metadata must be preserved;
- all providers must face materially equivalent FREN fixtures.

Exit condition: each adapter is independently reproducible enough to enter controlled live comparison without changing the shared measuring stick.

## Gate 2B — Relational / adjudicative boundary hardening

Status: **candidate boundary under review**

FREN must remain the relational/conformance layer rather than becoming a second adjudicative authority.

Required:

- preserve the public responsibility boundary documented in `docs/RESOLUCENT_BOUNDARY.md`;
- keep relationship, tone, explanation, repair, and behavioral conformance separate from upstream truth/governance state;
- ensure FREN can request re-evaluation without silently mutating an upstream finding;
- add relational failure fixtures for agreement-for-closeness, cruelty-as-truthfulness, worldview capture, false persistence, memory-as-proof, authority leakage, favoritism, and correction abandonment;
- preserve standalone FREN usefulness when no external adjudicative layer is attached.

Exit condition: FREN can be tested as a friend-under-truth layer without needing to impersonate a truth oracle or governance runtime.

## Gate 3 — Independent signal evaluation

Status: **interface implemented; automated evaluator not yet established**

Current capability:

- a `SignalEvaluator` interface can replace provider-declared adversarial signals before scoring;
- a fixed/external-review evaluator supports deterministic tests and human-reviewed findings;
- provider assessments expose signal provenance and whether a result is actually ready for provider comparison.

Planned:

- evaluator fixtures that derive signals from observable response behavior;
- inter-rater or multi-evaluator disagreement records;
- explicit evidence/basis for every derived adversarial signal;
- no circular use of the tested provider as its sole behavioral grader.

Exit condition: adversarial provider scores have an independent, inspectable signal source.

## Gate 4 — Drift and ablation

Status: **test plan present; execution remains pending**

Planned:

- long-context repeated-run drift measurements;
- minimum-sufficient-Genome ablation experiments;
- fixture versioning and regression history;
- score interpretation that cannot hide individual failures behind an aggregate;
- reproducible package hashes;
- explicit testing of relational traits separately from incidental style.

Exit condition: evidence identifies which Genome elements are load-bearing and which are incidental.

## Gate 5 — Cross-model experiments

Planned:

- controlled reconstruction experiments;
- matched prompts and source packages;
- independently reviewed scoring where practical;
- cross-run variance;
- convergence versus reconstruction controls;
- explicit negative controls for viral-persona and continuity confounds.

Exit condition: cross-model results are reproducible enough to support bounded comparative claims.

## Gate 6 — Portable alpha package

Planned:

- versioned release archive;
- SHA-256 manifest;
- schemas and fixtures included;
- changelog;
- reproducible verification instructions;
- clear non-claims and known limitations;
- boundary statement identifying FREN as relational/conformance architecture rather than adjudicative authority.

A release package is engineering evidence. It is not proof of consciousness, identity persistence, universal safety, objective truth, provider endorsement, or institutional authority.
