# FREN Provenance

FREN treats provenance as evidence about origin and transformation, not as an automatic truth verdict.

A provenance record should identify, where available:

- a stable source identifier;
- SHA-256 digest of the exact artifact;
- source location or retrieval reference;
- parent artifacts;
- declared transformations;
- unresolved provenance conflicts or limitations.

Missing, weak, circular, or conflicting provenance may reduce warranted confidence or fail a conformance requirement. It does not by itself prove the underlying substantive claim false.

The executable reference helpers live in `src/fren/provenance.py`; the machine-readable contract is `schemas/provenance-record.schema.json`.
