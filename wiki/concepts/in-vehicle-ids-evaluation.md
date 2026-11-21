---
uid: 01a1ff09-f9e8-7fc7-a0ed-d7b5c3369407
title: In-Vehicle IDS Evaluation
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- canarchy
sources:
- wiki/sources/arxiv-2611-26094-phantomasq-can-masquerade-2026-11-19.md
- wiki/sources/canmentor-large-small-model-collaboration-2026-11-05.md
- wiki/sources/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md
- wiki/sources/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md
- wiki/sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md
- wiki/sources/mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba-2026-06-17.md
confidence: medium
contested: false
contradictions: []
summary: In-vehicle intrusion detection research reports strong benchmark numbers,
  but thin public datasets and adaptive attacks mean those numbers rarely transfer to
  real vehicles without reproduction.
---

# In-Vehicle IDS Evaluation

## Definition
In-vehicle intrusion detection systems (IDS) watch CAN and automotive Ethernet traffic for injected, replayed or substituted messages. This note is about how to judge IDS claims: what the benchmarks measure, what they leave out, and what evidence a real deployment needs.

## What the archive shows
- **Detectors are getting better at quiet attacks.** PhantoMasq represents CAN traffic as message-sequence graphs with signal-behavior features and classifies five masquerade attack types, reporting mean AUC-ROC of 0.831 to 0.999 on the ROAD dataset under a split designed to avoid overlapping windows. ^[raw/papers/arxiv-2611-26094-phantomasq-can-masquerade-2026-11-19.md] MIDS earlier treated masquerade and tampering as joint identifier-and-payload sequence modeling. ^[raw/papers/mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba-2026-06-17.md]
- **Deployment patterns are emerging.** CANMentor keeps inference local and distills from a cloud teacher under a latency bound. ^[raw/papers/canmentor-large-small-model-collaboration-2026-11-05.md] Deep Defence on Wheels co-deploys quantized supervised and unsupervised models on an FPGA/SoC. ^[raw/papers/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md]
- **Public evidence for vehicle networks is thin.** The Cybersecurity Dataset Observatory catalogs 234 network-traffic datasets across 14 domains and finds limited public evidence for V2X and other vehicular networks, with many datasets shipping only processed records. ^[raw/papers/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md]
- **Adaptive attackers can stay under thresholds.** A model-free false-data-injection attack kept attack-period alarm rates below 2.4% at a matched 1% false-alarm point across the monitors it was tested against. ^[raw/papers/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md]

## Evidence checklist
Before comparing or adopting an in-vehicle IDS result, record:
- Dataset provenance, and whether raw traffic (not only processed features) is available
- How train and test windows are split, and how leakage is prevented
- Vehicle-specific identifiers, timing drift and ECU changes
- Replay, coordinated and adaptive attacks, not only the published attack set
- Latency, false-positive rate in normal driving, and what happens when an alarm fires
- Behavior when the cloud or teacher model is unavailable, for hybrid designs

## Open questions
- Every detector result in this archive is author-reported on benchmarks; none has independent replication on production vehicles.

## Briefing trail
- [[briefings/automotive/2026/11/2026-11-08|8 Nov 2026]]: CANMentor
- [[briefings/automotive/2026/11/2026-11-18|18 Nov 2026]]: model-free stealthy attack
- [[briefings/automotive/2026/11/2026-11-20|20 Nov 2026]]: PhantoMasq, Dataset Observatory

## Related pages
- [[concepts/can-masquerade-attacks|CAN Masquerade Attacks]]
- [[concepts/automotive-can|Automotive CAN]]
- [[concepts/automotive-tara|Automotive TARA]]
- [[concepts/vehicle-data-privacy|Vehicle Data Privacy]]
