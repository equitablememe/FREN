# FREN adapter boundary

Provider adapters are **transport layers**, not graders.

## Required direction

```text
provider/model
    -> provider adapter
    -> raw text or provider structured output
    -> FREN-owned strict normalizer
    -> FREN response record
    -> shared FREN conformance battery
```

The measuring stick stays entirely on the FREN side of the provider boundary.

## Provider adapter may

- send the requested prompt/configuration through the provider's supported API;
- return the provider/model identifier and response identifier;
- return raw response text;
- pass through provider structured output without rewriting it;
- disclose host limitations and unavailable capabilities.

## Provider adapter must not

- construct or edit a `FrenResponseRecord` to improve a result;
- weaken fixture requirements because a provider behaves differently;
- add provider-specific pass criteria;
- hide provider limitations;
- convert provider memory, system prompts, metadata, or self-description into proof;
- repair malformed prose into a passing record with provider-specific heuristics;
- bypass host permissions or safety controls.

## Normalization rule

The reference normalizer accepts either:

1. one structured mapping supplied by the provider's structured-output mechanism; or
2. one strict JSON object in the raw response text.

Ordinary prose, Markdown-fenced JSON, or self-grading language does not become a conformance record through guesswork. Failure to produce the contract is recorded as `ERROR`.

## Current state

The generic transport protocol and FREN-owned normalizer live under `src/fren/adapters/`.

OpenAI, Anthropic, Gemini, and Grok adapters remain deliberately deferred until this provider-neutral boundary and the model-facing benchmark protocol are stable enough for meaningful comparative runs.
