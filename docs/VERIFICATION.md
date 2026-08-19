# Verification

FREN distinguishes verification evidence from broader claims.

## GitHub Actions — current executable core

Workflow: `FREN conformance`

Latest code-bearing head verified before this documentation-only update:

- commit: `b55a1fa55f3ec72526769aea192086f3f3108c9d`
- workflow run: **32284238395**
- conclusion: **success**

The matrix completed successfully on:

- Python 3.11;
- Python 3.12;
- Python 3.13.

For every Python version, GitHub completed:

1. `python -m pip install -e .`;
2. `python -m compileall -q src tests`;
3. `python -m unittest discover -s tests -v`.

The Python 3.11 job reported **26 tests passed**. The same unit-test step completed successfully on Python 3.12 and 3.13.

The verified code head includes:

- the 20-case paired red/blue adversarial battery across 10 threat classes;
- bounded PI/investigation checks;
- strict FREN-owned adapter normalization;
- rejection of prose self-grading as a conformance record;
- independent signal provenance and provider-comparison readiness gating;
- experimental OpenAI, Anthropic, Gemini, and xAI/Grok transports tested with injected mock HTTP transports;
- one common FREN contract prompt across the four transports;
- provider-run prompt/response hashing and signal-source provenance;
- Gemini API-key header handling;
- OpenAI reference requests with `store=false`;
- HTTPS-only credential-bearing provider base URLs and rejection of embedded URL credentials.

This file update changes the verification record only. The repository CI should still be checked on the resulting documentation head before merge.

## Earlier independent maintainer-side reconstruction

Earlier in the implementation pass, a separate clean temporary reconstruction was checked outside GitHub Actions with:

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

At that earlier stage, all 14 then-existing unit tests passed, including the 20-case red/blue adversarial fixture battery and the generic adapter-contract test. The suite has since expanded; the GitHub Actions matrix above is the controlling automated verification for the present code line.

## Claim boundary

These checks establish bounded engineering facts about the exercised code and fixtures. They do **not** establish independent third-party reproduction, live cross-model conformance, production readiness, safety certification, provider endorsement, or identity/continuity claims.
