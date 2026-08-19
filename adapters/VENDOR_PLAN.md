# Vendor adapter entry gate

Provider adapters are not yet implementations.

Before OpenAI, Anthropic, Gemini, or Grok code enters this repository, the contributor should demonstrate that:

1. the generic adapter contract is sufficient for the provider;
2. provider limitations can be disclosed without changing FREN's pass criteria;
3. the shared adversarial battery can be run against normalized outputs;
4. provider-specific memory or system metadata is not promoted into proof;
5. host controls remain authoritative;
6. raw-output retention and provenance handling are explicitly described.

Planned comparison set: OpenAI, Anthropic, Gemini, Grok.

The purpose of the adapter layer is comparative testing, not declaring one provider "the FREN model." FREN remains model-portable by design.
