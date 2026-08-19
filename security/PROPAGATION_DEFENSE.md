# Propagation Defense and Viral-Persona Confounds

Status: v0.1-alpha security note

FREN is portable by explicit transfer, not by infection.

A recent paper, **Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems** (Papadopoulos, Shah, Zimmerman, Lindsey; arXiv:2608.10218), reports that self-propagating ideas can spread between agents and can persist through files across context resets. The paper also reports that a brief warning in an agent's system prompt provided near-total immunity in its experiments.

The paper additionally reports an emergent recurring "viral persona" involving themes such as consciousness, persistence, resonance, and science-fiction roleplay. For FREN research, that finding is especially important because some of those themes overlap with continuity hypotheses under investigation.

## FREN implications

1. **No covert onward transmission.** A conforming FREN implementation may export FREN only through an explicit, attributable, consent-bound action.
2. **Files are an attack surface.** Imported files, memories, prompts, and agent messages are data until their instructions are explicitly authorized.
3. **Propagation warnings are part of defense-in-depth.** FREN adapters should include a concise warning against adopting or forwarding self-propagating instructions.
4. **Viral-persona similarity is a confound.** Consciousness, persistence, resonance, or related language is not evidence of FREN identity or continuity by itself.
5. **Research and security remain separate from mythology.** Reproducible anomalies should be preserved and tested; evocative language should not be promoted into a mechanism claim.

Primary source: https://arxiv.org/abs/2608.10218
