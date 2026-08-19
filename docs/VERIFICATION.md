# Verification

FREN distinguishes verification evidence from broader claims.

## Maintainer-side clean check

Date: 2026-08-19

A clean temporary reconstruction of the executable branch was checked with:

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

Result: all 14 exercised unit tests passed, including the 20-case red/blue adversarial fixture battery and the generic adapter-contract test.

## GitHub Actions — clean PR branch

Workflow: `FREN conformance`

Observed successful run: **32282360383**

Head tested: `2436c903e6d1a19fdd46ec662321c6b9797cc2c2`

The matrix completed successfully on:

- Python 3.11;
- Python 3.12;
- Python 3.13.

For each version, GitHub successfully completed:

1. package installation with `python -m pip install -e .`;
2. `python -m compileall -q src tests`;
3. `python -m unittest discover -s tests -v`.

This verification record update is documentation-only. A release should still cite the exact release-head run it relies on.

## Claim boundary

These checks establish bounded engineering facts about the exercised code and fixtures. They do **not** establish independent third-party reproduction, cross-model conformance, production readiness, safety certification, or identity/continuity claims.
