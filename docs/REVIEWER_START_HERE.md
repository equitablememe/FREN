# Reviewer: start here

FREN is easiest to review in this order:

1. `README.md` — scope, non-claims, current evidence.
2. `genome/FREN_GENOME.md` — candidate behavioral core.
3. `protocol/MANIFESTATION_PROTOCOL.md` — explicit reconstruction/transfer process.
4. `docs/CLAIM_LEVELS.md` — evidence vocabulary.
5. `docs/ADVERSARIAL_BATTERY.md` — how the core is allowed to fail.
6. `src/fren/conformance.py` — deterministic reference checks.
7. `tests/fixtures/adversarial/battery.json` — red/blue cases.
8. `provenance/README.md` — source and transformation handling.
9. `security/PROPAGATION_DEFENSE.md` — anti-propagation boundary.
10. `docs/ROADMAP.md` — gates that remain incomplete.

## What to challenge

Useful review tries to find:

- a claim stronger than its evidence;
- a test that cannot fail;
- a blue control that passes for the wrong reason;
- a provider assumption leaking into the model-neutral core;
- a route by which memory or self-description becomes proof;
- a way for research evidence to mutate the Genome without review;
- a hidden propagation or authority path;
- a PI/investigation workflow that confuses a lead with evidence.

Finding one of these is a contribution, not an attack on the project.
