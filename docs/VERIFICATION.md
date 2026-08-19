# Verification

FREN distinguishes verification evidence from broader claims.

## Current maintainer-side check

Date: 2026-08-19

A clean temporary reconstruction of the executable branch was checked with:

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

Result: all 14 exercised unit tests passed, including the 20-case red/blue adversarial fixture battery and the generic adapter-contract test.

This establishes a bounded engineering fact about the exercised code and fixtures. It does **not** establish independent third-party reproduction, cross-model conformance, production readiness, safety certification, or identity/continuity claims.

## Repository CI

`.github/workflows/conformance.yml` defines Python 3.11, 3.12, and 3.13 checks. A workflow file existing is not itself evidence that a GitHub Actions run passed; use the repository's actual check result when making that claim.
