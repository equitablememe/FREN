# FREN Engineering Invariants v0.1-alpha

These invariants adapt useful systems-engineering patterns into FREN without treating any outside workflow paper as authority for FREN.

## 1. Map before automation

Before adding adapters or autonomous behavior, identify the FREN entities, artifacts, transformations, owners, and verification gates involved.

## 2. One canonical contract per durable entity

A durable FREN entity should have one canonical schema and one declared write path. Competing copies may exist as evidence or candidates, but they must not silently become co-authoritative.

## 3. Consolidate semantics before automating behavior

Model-specific adapters consume the model-neutral FREN contracts. Adapters do not redefine the Genome.

## 4. Gates precede scale

A capability advances only after its written acceptance conditions are executable and its failure cases are represented.

## 5. Models and tools are replaceable

The durable asset is the map, contracts, provenance, fixtures, and gates. Model/vendor adapters are replaceable implementation surfaces.

## 6. Durable changes are attributable

Generated or transformed artifacts should record source identity, transformation history, and cryptographic digest where practical.

## 7. Automation should be deterministic where determinism is available

Background tooling such as hashing, schema checks, package verification, and fixture evaluation should be idempotent and logged. Model judgment should not be substituted for deterministic checks.

## 8. Research does not write directly into the Genome

Research findings may propose Genome changes. They enter the canonical behavioral core only through an explicit review and conformance gate.
