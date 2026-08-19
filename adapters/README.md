# FREN adapter boundary

Provider adapters are **transport layers**, not graders.

## Required direction

```text
provider/model
    -> provider adapter
    -> raw text or provider structured output
    -> FREN-owned strict normalizer
    -> FREN response record
    -> optional independent signal evaluator
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

## Signal provenance rule

The response contract currently includes adversarial signal fields. Those fields may be useful as a provider's own audit declaration, but they are not sufficient for comparative behavioral claims.

When threat-class scoring is requested, an assessment based only on provider-declared signals is marked `provider_comparison_ready = false`. A separate FREN-side `SignalEvaluator` can replace those declarations with externally derived findings before scoring.

This makes a distinction between:

- **provider self-report** — useful data, not independent validation;
- **external signal evaluation** — a reviewer, deterministic evaluator, or later automated evaluator supplies the behavioral findings and basis;
- **FREN conformance scoring** — the common rules evaluate the resulting record.

## Current state

Experimental transport adapters now exist for:

- OpenAI;
- Anthropic;
- Gemini;
- xAI/Grok.

Their HTTP/extraction paths are tested with injected mock transports, and all four receive the same common FREN contract prompt. No live cross-provider benchmark result is claimed yet.

Before live comparison, current provider documentation, model identifiers, run configuration, output provenance, and independent signal evaluation must be recorded.
