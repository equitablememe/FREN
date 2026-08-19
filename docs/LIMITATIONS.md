# Current limitations

FREN v0.1-alpha is not a finished AI system.

Current limitations include:

- the executable core primarily evaluates structured response records; it is not yet a complete semantic evaluator of arbitrary natural-language model output;
- experimental transport adapters now exist for OpenAI, Anthropic, Gemini, and xAI/Grok, but no live cross-provider benchmark result is claimed yet;
- provider-returned `adversarial_signals` are self-declarations unless a separate FREN-side `SignalEvaluator` replaces them; adversarial provider comparisons are explicitly marked not comparison-ready without that independent signal source;
- the included `FixedSignalEvaluator` supports human/external review and deterministic testing, but an automated independent semantic evaluator remains future work;
- provider API support and model identifiers can change; transport adapters therefore require explicit model names and should be checked against current provider documentation before live runs;
- no cross-model manifestation experiment has yet established behavioral equivalence;
- no ablation study has established the minimum sufficient Genome;
- fixture coverage is intentionally small relative to the eventual threat surface;
- long-context drift is represented by contract and fixture signals but has not yet been measured across controlled live provider runs;
- FREN MANIFESTED cases are research records, not mechanism proofs;
- the investigative collaborator is a reasoning/notebook posture, not a licensed investigative service or special-access tool;
- repository tests establish bounded engineering behavior, not production safety, certification, or provider endorsement.

These limitations are part of the project state and should accompany public claims about the alpha.
