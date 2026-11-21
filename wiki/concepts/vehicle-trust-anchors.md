---
uid: 01a1ff09-f9ee-77fa-8720-8883245352c5
title: Vehicle Trust Anchors and Cryptography
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- cryptography
sources:
- wiki/sources/post-quantum-cryptography-automotive-context-2026-10-28.md
- wiki/sources/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md
- wiki/sources/athene-automotive-security-plug-charge-tpm-2026-11-13.md
- wiki/sources/uspto-karma-vehicle-security-system-2026-11-12.md
- wiki/sources/automotive-hsms-architectural-challenges-security-implications-2026-08-25.md
- wiki/sources/sk-hynix-lpddr5x-iso-sae-21434-2026-11-11.md
confidence: medium
contested: false
contradictions: []
summary: Vehicle trust anchors are the hardware and cryptographic roots (HSMs, TPMs,
  message authentication, PKI) that vehicles depend on. Zonal architectures and
  post-quantum migration are both reshaping where they live.
---

# Vehicle Trust Anchors and Cryptography

## Definition
Trust anchors are the roots a vehicle's security depends on: hardware security modules (HSMs) and TPMs that hold keys, the message-authentication schemes that protect in-vehicle traffic, and the PKI behind V2X and Plug & Charge. Two forces are reshaping them: zonal architectures that centralize compute, and the expected migration to post-quantum cryptography (PQC) for long-lived vehicles.

## What the archive shows
- **PQC costs are measurable but scenario-bound.** A comparison of ML-KEM (Kyber), ML-DSA (Dilithium) and FALCON in simulated rural V2V and urban V2X scenarios, against an ECDSA/ECDH baseline, reports low Kyber KEM latency, balanced Dilithium signatures, and costly FALCON key generation and signing with efficient verification. ^[raw/papers/post-quantum-cryptography-automotive-context-2026-10-28.md]
- **PQ authentication is showing up in V2X research.** A vehicular federated-learning paper adds post-quantum-authenticated V2I links and reports a 92.4% smaller authenticated uplink with one-bit updates, in simulation. ^[raw/papers/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md]
- **Zonal vehicles may centralize keys.** ATHENE/Fraunhofer proposes one TPM 2.0 holding Plug & Charge keys for several EV communication controllers, which cuts repeated trust anchors but creates a single point of trust and denial. ^[raw/papers/athene-automotive-security-plug-charge-tpm-2026-11-13.md]
- **Message integrity can use redundant paths.** A Karma Automotive patent publication (US 2026/0361706 A1) validates messages by matching copies received over Ethernet and CAN within a time window and splits authentication-key material across messages or paths. ^[raw/articles/uspto-karma-vehicle-security-system-2026-11-12.md]
- **HSMs are one layer, not the answer.** Automotive HSMs support secure boot, key storage, secure execution and signing, but leave isolation, performance, updateability, side-channel and post-quantum trade-offs open. ^[raw/papers/automotive-hsms-architectural-challenges-security-implications-2026-08-25.md]
- **Memory is part of the trust surface.** SK hynix frames automotive memory as security-relevant for sensor inputs, AI results and cryptographic material. ^[raw/articles/sk-hynix-lpddr5x-iso-sae-21434-2026-11-11.md]

## Working guidance
- Ask suppliers for message-size, latency, CPU and RAM figures, key rotation and downgrade/migration assumptions before putting PQC numbers into a crypto-agility roadmap.
- For centralized trust anchors, test failure handling, key-use authorization between ECUs, provisioning, recovery and blast radius.
- Compare multi-path or split-key designs against existing SecOC/MAC, gateway filtering and IDS, including replay, coordinated compromise of both paths and timing manipulation.

## Open questions
- The PQC evidence is simulation-based preprint work.
- A patent publication shows intent, not adoption or measured efficacy.
- The centralized TPM design is a conference proposal with emulated devices.

## Briefing trail
- [[briefings/automotive/2026/10/2026-10-30|30 Oct 2026]]: PQC in V2V/V2X
- [[briefings/automotive/2026/11/2026-11-04|4 Nov 2026]]: PQ-authenticated federated learning
- [[briefings/automotive/2026/11/2026-11-13|13 Nov 2026]]: SK hynix memory certification
- [[briefings/automotive/2026/11/2026-11-15|15 Nov 2026]]: centralized TPM, Karma split-key patent

## Related pages
- [[concepts/ev-charging-security|EV Charging Security]]
- [[concepts/automotive-can|Automotive CAN]]
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
