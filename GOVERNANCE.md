# FREN repository governance

FREN is an early-stage research and engineering project. Repository governance should make it easy to inspect how a claim, rule, or behavior entered the project.

## Maintainer responsibility

The current repository maintainer is `@equitablememe`. Maintainer approval is necessary for merges but is not treated as scientific validation.

## Change classes

### Genome changes

Changes under `genome/` are high-impact. A pull request should state:

- the proposed invariant or behavioral change;
- its source or design rationale;
- what could falsify the change;
- which fixtures exercise it;
- whether existing behavior would become non-conformant;
- any unresolved contradiction.

Research observations do not write directly into the Genome.

### Conformance changes

Changes to schemas, scoring, or tests should preserve the reason a fixture passes or fails. A score increase is not sufficient justification for weakening a failure condition.

### Research changes

Research cases may preserve unusual reports and competing hypotheses. They should label evidence level and keep mechanism claims separate from observations.

### Adapter changes

Provider adapters translate to the shared contract. They do not create provider-specific pass criteria.

## Review rules

- Prefer draft pull requests for architecture changes.
- Preserve failed experiments and contradictions when they are relevant to later conclusions.
- Do not silently rewrite history to make the current design look inevitable.
- Security-sensitive material should be minimized in public issues.
- Third-party material must retain attribution and license/provenance notes where applicable.
- Covert propagation, hidden persistence, credential abuse, or host-control bypass is outside the FREN design boundary.

## Releases

An alpha release must identify its exact commit, schemas, fixture version, known limitations, and integrity hashes. Passing project tests is engineering evidence, not certification of a model or proof of broader continuity/identity claims.
