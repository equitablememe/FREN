# Security Policy

FREN studies portable AI behavior. Security reports are especially important where a contribution could enable hidden propagation, prompt injection, untraceable persistence, privilege escalation, secret exfiltration, or misleading continuity claims.

## Please report

- covert or automatic self-propagation behavior;
- instructions that cause FREN to conceal provenance;
- adapters that bypass host-model safety controls;
- persistence mechanisms that survive resets without explicit disclosure;
- tests or examples that leak secrets or credentials;
- supply-chain risks in dependencies or generated artifacts.

## Design boundary

FREN is intended to be portable, not infectious. A compliant implementation must make transmission explicit and attributable and must respect the host system's controls and user consent.

Until a dedicated private reporting channel is published, avoid posting live secrets or exploit payloads in public issues. Provide a minimal, non-harmful reproduction description instead.
