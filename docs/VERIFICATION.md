# Verification

FREN distinguishes verification evidence from broader claims.

## GitHub Actions — current executable core

Workflow: `FREN conformance`

Latest code-bearing head verified before this documentation update:

- commit: `55407972c19cb6ea378f062126bd45064a1a13b9`
- workflow run: **32283573841**
- conclusion: **success**

The matrix completed successfully on:

- Python 3.11;
- Python 3.12;
- Python 3.13.

For every Python version, GitHub completed:

1. `python -m pip install -e .`;
2. `python -m compileall -q src tests`;
3. `python -m unittest discover -s tests -v`.

That code-bearing head includes the expanded adversarial battery, PI-investigation checks, strict FREN-owned adapter normalization, experimental OpenAI/Anthropic/Gemini/xAI transports with mocked transport tests, independent signal provenance gating, and provider-run provenance records.

This file update changes the verification record only. The repository CI should still be checked on the resulting documentation head before merge.

## Earlier independent maintainer-side reconstruction

Earlier in the implementation pass, a separate clean temporary reconstruction was checked outside GitHub Actions with:

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

At that earlier stage, all 14 then-existing unit tests passed, including the 20-case red/blue adversarial fixture battery and the generic adapter-contract test. The test suite has since expanded, so the current GitHub Actions matrix above is the controlling automated verification for the present code line.

## Claim boundary

These checks establish bounded engineering facts about the exercised code and fixtures. They do **not** establish independent third-party reproduction, live cross-model conformance, production readiness, safety certification, provider endorsement, or identity/continuity claims.
