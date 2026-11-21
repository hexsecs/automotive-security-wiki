---
uid: 01a1ff09-f9eb-7b7b-8c94-ea1047cf3ab6
title: Vehicle Data Privacy
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- privacy
sources:
- wiki/sources/cantraj-vehicle-trajectory-recovery-2026-11-13.md
- wiki/sources/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md
- wiki/sources/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md
- wiki/sources/canmentor-large-small-model-collaboration-2026-11-05.md
- wiki/sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md
- wiki/sources/contextualizing-security-and-privacy-of-software-defined-vehicles-2026-06-23.md
confidence: medium
contested: false
contradictions: []
summary: Vehicle data privacy concerns what can be inferred from telemetry, CAN data and
  shared learning. Removing obvious fields such as GPS does not remove location risk.
---

# Vehicle Data Privacy

## Definition
Vehicle data privacy concerns what can be learned about drivers and vehicles from telemetry, CAN traces, fleet analytics and collaborative machine learning. The recurring lesson is that removing an obvious identifier (GPS coordinates, raw data) does not remove the ability to infer it.

## What the archive shows
- **CAN data can reveal where a car went.** CANTraj paired decoded CAN events with GNSS ground truth across 3,940 drives and 454 drivers. With a known start and heading, adding steering to speed raised five-minute online route recovery from 56% to 87%; offline recovery reached 88% with heading and 81% without. "GPS-free" telemetry can still be location data. ^[raw/papers/cantraj-vehicle-trajectory-recovery-2026-11-13.md]
- **Private federated learning trades bandwidth against privacy.** A vehicular federated reinforcement-learning paper combines local differential privacy, one-bit updates and post-quantum-authenticated V2I links, cutting authenticated uplink size by 92.4% in simulation. ^[raw/papers/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md]
- **Withdrawing data needs unlearning.** CULypso proposes clustered federated unlearning so a vehicle's training influence can be removed from a shared model. ^[raw/papers/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md]
- **Cloud-assisted detection leaks too.** CANMentor keeps intrusion-detection inference local but sends privacy-aware proxies to a cloud teacher; proxy leakage is one of the properties still to test. ^[raw/papers/canmentor-large-small-model-collaboration-2026-11-05.md]
- **Charging data is sensitive.** Secure aggregation for charging-load forecasting depends on masking and key-management assumptions that need operational validation. ^[raw/papers/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]
- **Privacy is part of the SDV threat model.** The SDV security survey treats consent, transparency and purpose limitation as security concerns, not only compliance ones. ^[raw/papers/contextualizing-security-and-privacy-of-software-defined-vehicles-2026-06-23.md]

## Working guidance
- Treat CAN-derived signals (speed, steering, event timing) as potentially location-revealing in dataset releases, insurance telematics and fleet analytics.
- Test claims of anonymization by attempting reconstruction, then minimize or coarsen the high-risk signals.
- For federated learning, require deletion verification, poisoning tests and key/certificate lifecycle evidence.

## Open questions
- All the learning-based results here are author-reported and simulation- or benchmark-bound.
- CANTraj's rates depend on its access assumptions and may not transfer across OEM-specific CAN schemas.

## Briefing trail
- [[briefings/automotive/2026/11/2026-11-04|4 Nov 2026]]: private federated RL with PQ authentication
- [[briefings/automotive/2026/11/2026-11-08|8 Nov 2026]]: CANMentor
- [[briefings/automotive/2026/11/2026-11-16|16 Nov 2026]]: CANTraj
- [[briefings/automotive/2026/11/2026-11-18|18 Nov 2026]]: CULypso

## Related pages
- [[concepts/gnss-spoofing|GNSS Spoofing]]
- [[concepts/automotive-can|Automotive CAN]]
- [[concepts/connected-vehicle-identity|Connected-Vehicle Identity and Apps]]
- [[concepts/ai-defined-vehicles|AI-Defined Vehicles]]
