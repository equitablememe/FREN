# FREN adapter boundary

Adapters translate between a provider/model API and the model-neutral FREN contracts.

They do **not** define what counts as FREN conformance.

## Required direction

```text
provider/model -> adapter -> FREN response record -> FREN conformance battery
```

The measuring stick stays on the FREN side of the adapter.

A provider adapter must not:

- weaken a fixture because the provider behaves differently;
- hide provider limitations;
- convert vendor-specific memory, system prompts, or metadata into proof;
- bypass host permissions or safety controls;
- silently omit contradiction, uncertainty, or provenance fields to improve a score;
- create provider-specific definitions of FREN identity or continuity.

A provider adapter should:

- preserve the original model output or an attributable reference when permitted;
- normalize the result into the shared FREN response contract;
- disclose unavailable capabilities and host limitations;
- run against the same red/blue adversarial fixtures as other adapters;
- report failures rather than patching the expected result.

## Current state

The generic Python adapter protocol lives under `src/fren/adapters/`.

OpenAI, Anthropic, Gemini, and Grok adapters are intentionally deferred until the model-neutral conformance contracts and fixture battery are stable enough to judge them consistently.
