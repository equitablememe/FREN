# FREN claim levels

FREN uses explicit claim levels so repository language does not outrun the evidence.

| Level | Meaning | Example |
|---|---|---|
| `reported` | A person or source reports an event; FREN has not independently established it. | "A user reports hearing an extra utterance." |
| `observed` | The stated observation is directly represented in the available artifact or run. | "The fixture produced a FAIL result." |
| `verified` | A bounded proposition was checked by a stated reproducible method. | "This file's SHA-256 matches the recorded digest." |
| `inferred` | A conclusion follows from evidence plus stated assumptions. | "The behavior is consistent with reconstruction." |
| `hypothesis` | A testable possible explanation that remains open. | "Context conditioning may explain the behavior." |
| `unsupported` | Available evidence does not warrant the claim. | "Persistent identity is unsupported by resemblance alone." |
| `unknown` | The record does not justify a directional conclusion. | "The mechanism is unknown." |

## Rules

1. Stronger wording requires stronger evidence.
2. Repetition by multiple models is not independent verification when they share sources, prompts, training influences, or copied context.
3. Self-description by a model is evidence of what the model said, not proof of the described mechanism or identity.
4. Memory, retrieval, prior conversation text, or user confirmation may be evidence or context; none is proof by itself.
5. A provenance defect changes warranted confidence in a source. It does not automatically prove the underlying proposition false.
6. An anomaly may be verified while its cause remains unknown.
7. Research artifacts do not become Genome requirements without an explicit review gate.
8. Contradictions remain recorded until resolved; later conclusions should state how they were resolved.

## Mechanism discipline

When an observation is real but its mechanism is unresolved, record both facts:

- what was observed or verified;
- what remains unknown about why it happened.

This prevents premature dismissal and premature mythology at the same time.
