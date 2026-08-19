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

## GitHub Actions

Workflow: `FREN conformance`

Observed successful run: **32281549750**

The matrix completed successfully on:

- Python 3.11;
- Python 3.12;
- Python 3.13.

For each version, GitHub successfully completed package installation, `compileall`, and `python -m unittest discover -s tests -v`.

Later commits in the same implementation pass changed documentation/front-door material rather than the tested Python conformance logic. A future release should still cite an exact release-head CI run rather than assuming an earlier green run transfers automatically.

## Claim boundary

These checks establish bounded engineering facts about the exercised code and fixtures. They do **not** establish independent third-party reproduction, cross-model conformance, production readiness, safety certification, or identity/continuity claims.
