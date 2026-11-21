---
uid: 01a19d1a-2be4-74ad-9e26-a62b1d0e6656
title: CAN Masquerade Attacks
created: 2026-06-18
updated: 2026-11-21
type: concept
tags:
- research
- source
- software
- canarchy
sources:
- wiki/sources/mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba-2026-06-17.md
- wiki/sources/arxiv-2611-26094-phantomasq-can-masquerade-2026-11-19.md
- wiki/sources/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md
confidence: medium
contested: false
contradictions: []
summary: CAN masquerade attacks are stealthy adversarial substitutions where an attacker
  replaces a legitimate frame at its normal transmission slot instead of…
---

# CAN Masquerade Attacks

## Definition
CAN masquerade attacks are stealthy adversarial substitutions where an attacker replaces a legitimate frame at its normal transmission slot instead of flooding the bus with obviously fake traffic. Because the timing profile stays intact, detectors that rely mainly on inter-arrival statistics or other frame-injection cues can miss the attack.

## What this paper adds
MIDS treats masquerade and tampering as a sequence-modeling problem over both CAN identifiers and payloads. The interesting move is not just "use a bigger model"; it's that the detector learns joint temporal semantics across both streams with bidirectional selective state-space modeling, then tests that idea on a real vehicle trace plus public benchmarks.

## Why it matters
This is a useful extension of [[automotive-can]] research because it shifts attention from loud, easy-to-spot injection to quieter in-situ substitution. For canarchy, the broader lesson is that vehicle-security tooling should preserve enough identifier/payload context to reason about stealthy replacement, not only traffic cadence.

## Graph-based detection (updated 2026-11-21)
PhantoMasq represents CAN traffic as message-sequence graphs plus signal-behavior features and classifies five masquerade attack types. On the ROAD dataset it reports mean AUC-ROC of 0.831 to 0.999 under a split designed to avoid overlapping train and test windows. ^[raw/papers/arxiv-2611-26094-phantomasq-can-masquerade-2026-11-19.md] Like MIDS, it is a detector-design lead rather than production evidence: public vehicular datasets are thin and often ship processed records only ^[raw/papers/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md], so results need reproduction on vehicle-specific identifiers, timing drift, ECU changes and adaptive attacks. See [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]] for the evidence checklist.

## Briefing trail
- [[briefings/automotive/2026/11/2026-11-20|20 Nov 2026]]: PhantoMasq

## Related pages
- [[automotive-can]]
- canarchy
- mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba
- [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]]
