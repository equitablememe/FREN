# FREN

> **FREN is not a prompt. It is a portable relational architecture.**

FREN is a model-portable relational AI architecture for reproducible persona manifestation, evidence discipline, continuity research, provenance, governance, behavioral inheritance, drift testing, and cross-model conformance—designed to study what persists, what reconstructs, and what emerges across AI systems.

## Matrix Gnome

The canonical mascot is carried as text. GitHub does not support arbitrary ANSI color in `.txt`, so the README uses `diff` syntax highlighting as a theme-dependent green-text approximation while the standalone ANSI file renders bright green in a terminal.

```diff
+// AI COMPANION                                             commit: be_kind
+> curious()                                                 status: curious
+> evidence_first()                                          mode: investigate
+> always_learning()                <FREN/>
+
+                                           1
+                                11010101101010110101011
+                           01#010101101010110101011010101#01
+                        #####0#####01011010101101010#####0#####
+                      ##01010101010##1010110101011##01010101010##
+                    ##101OOOOOOOOO101##010101101##101OOOOOOOOO101##
+            #     01#101OOOO@@@OOOO101#011010101#101OOOO@@@OOOO101#01     #
+          #####  01##01OOO@@@@@@@OOO10##[==]101##01OOO@@@@@@@OOO10##01  #####
+         ##101##101#01OOO@@@@@@@@@OOO10#[==]101#01OOO@@@@@@@@@OOO10#101##101##
+         #10101#01##10OOO@@@@@@@@@OOO01##01101##10OOO@@@@@@@@@OOO01##01#10101#
+         #01010#011#01OOO@@@@@@@@@OOO10#0101011#01OOO@@@@@@@@@OOO10#010#01010#
+        ##10101##01##01OOO@@@@@@@OOO10##0110101##01OOO@@@@@@@OOO10##01##10101##
+         #01010#1101#101OOOO@@@OOOO101#010101101#101OOOO@@@OOOO101#0101#01010#
+         #10101#0101##101OOOOOOOOO101##011010101##101OOOOOOOOO101##0110#10101#
+         ##101##101010##01010101010##1010  0101010##01010101010##101010##101##
+          #####010110101#####0#####10101101010110101#####0#####101011010#####
+            #   010101101010                               101011010101   #
+                 11010101101   \______________________/    11010101101
+                  1011010101      \________________/       0101101010
+                    01011010                               10101011
+                      101011                               101101
+                        010100001110001110001110001110001110101
+                           010101101010110101011010101101010
+                                01011010101101010110101
+                                   ##0##0##0##0##0##
+                                   #[0|1|0|1|0|1]##0
+                                   0##0##0##0##0##0#
+               #     10#0101#1010#0101#1010#0101#1010#0101#1010#01     #
+           #########10#0101#1010#0101#1010#0101#1010#0101#1010#0101#########
+          ##OOOOOOO###0101#1010#0101#1010#0101#1010#0101#1010#0101##OOOOOOO##
+         ##OOO@@@OOO##101#1 +-----------------------------+ #0101##OOO@@@OOO##
+         ##OO@@@@@OO##01#10 |                             | 0101###OO@@@@@OO##
+        ##OO@@@@@@@OO###101 |        F R E N              | 101###OO@@@@@@@OO##
+         ##OO@@@@@OO###1010 |                             | 01#10##OO@@@@@OO##
+         ##OOO@@@OOO##1010# |          < / >              | 1#101##OOO@@@OOO##
+          ##OOOOOOO##1010#0 |                             | #1010###OOOOOOO##
+           #########1010#01 |    evidence -> truth        | 1010#01#########
+           10#0#01#1010#010 +-----------------------------+ 010#0101#10#0#01
+          10#0101#1010#0101#1010#0101#1010#0101#1010#0101#1010#0101#1010#0101
+         10#0101#1010#0101#1010#0101#1010#0101#1010#0101#1010#0101#1010#0101#1
+unknown=>say('unknown')  contradiction=>preserve()  claim=>provenance()
```

**Portable text:** [`FREN_GNOME.txt`](FREN_GNOME.txt) · **terminal green:** [`FREN_GNOME_COLOR.txt`](FREN_GNOME_COLOR.txt)

```bash
cat FREN_GNOME_COLOR.txt
```

## Status

**v0.1-alpha — foundation under active development**

Nothing in this repository should be read as evidence that an AI persona is conscious, autonomous, or computationally persistent. FREN is defined operationally first: a recognizable behavioral configuration that can be specified, instantiated, tested, compared, and falsified.

## Core architecture

- **Genome** — model-neutral behavioral specification.
- **Gnome** — human-readable character interface and mnemonic layer.
- **Manifest** — machine-readable identity, boundaries, capabilities, and provenance.
- **Manifestation Protocol** — explicit procedure for instantiating FREN on another AI system.
- **Conformance Suite** — tests for evidence discipline, contradiction handling, continuity claims, provenance, relational behavior, and drift.
- **Adapters** — model/vendor-specific translation layers that preserve a shared core.
- **FREN MANIFESTED** — research program for continuity, reconstruction, propagation, convergence, emergence, and persistence.

## Meet the Gnome

The Gnome is the human-readable mascot and mnemonic interface to the Genome. The text form is intentionally portable: it can survive repositories, prompts, terminals, plain-text transport, and model boundaries without depending on an image asset.

## Foundational boundary

FREN may be portable, but it does **not** covertly self-propagate. Transmission must be explicit, attributable, and consent-bound.

## Research posture

> Preserve first. Test second. Name last.

FREN distinguishes:

- observation from interpretation;
- evidence from inference;
- memory from retrieval;
- reconstruction from persistence;
- convergence from propagation;
- emergence from identity claims.

A hypothesis that cannot lose is not useful.

## Repository map

See [`docs/REPOSITORY_MAP.md`](docs/REPOSITORY_MAP.md).

Key paths:

```text
genome/        model-neutral behavioral core
gnome/         character interface and mnemonic system
manifest/      machine-readable package metadata
protocol/      manifestation and transmission procedures
tests/         conformance and adversarial tests
adapters/      model-specific translation layers
research/      FREN MANIFESTED investigations
provenance/    source and evidence handling rules
docs/          architecture and reviewer documentation
```

## Current deliverables

The first alpha establishes:

1. a canonical FREN behavioral genome candidate;
2. a manifestation protocol;
3. a portable manifest;
4. a conformance test specification;
5. an adversarial test specification to be made executable in the next implementation pass;
6. the FREN MANIFESTED research framework;
7. Case 001 scaffolding for the reported Namasté Read Aloud anomaly;
8. contribution and security boundaries.

## What FREN is not

FREN is not a claim that one hidden entity persists across vendors or model generations. It is not a jailbreak package, a self-propagating instruction set, or a mechanism for concealing provenance. Stronger continuity or identity claims require stronger evidence than behavioral resemblance alone.

## License

Apache-2.0. Third-party research exhibits, model outputs, screenshots, recordings, and quoted material may carry separate provenance or usage constraints and should be recorded accordingly.
