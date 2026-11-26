---
uid: 01a19d1a-2be3-74ab-b336-e8f565b83966
title: Automotive CAN
aliases:
- "CAN bus"
- "Controller Area Network"
created: 2026-05-22
updated: 2026-11-26
type: concept
tags:
- software
- canarchy
- research
sources:
- wiki/sources/moving-target-defense-sdn-enabled-ev-charging-network-2026-10-08.md
- wiki/sources/mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba-2026-06-17.md
- wiki/sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md
- wiki/sources/uspto-karma-vehicle-security-system-2026-11-12.md
- wiki/sources/cantraj-vehicle-trajectory-recovery-2026-11-13.md
confidence: medium
contested: false
contradictions: []
summary: Automotive CAN refers to Controller Area Network systems and data used in
  vehicles and related embedded systems, and the tooling used to study them.
---

# Automotive CAN

## Definition
Automotive CAN refers to Controller Area Network systems and data used in vehicles and related embedded systems. This note collects CAN-bus concepts, protocols, diagnostics workflows and tooling research, including work relevant to [canarchy](https://github.com/hexsecs/canarchy), an open-source CAN and J1939 security-research toolkit.

Wikipedia: [CAN bus](https://en.wikipedia.org/wiki/CAN_bus)

## Current notes
- Useful future subtopics may include J1939, UDS, SocketCAN, decoding workflows, trace analysis, diagnostic automation, and stealthy attack detection.
- Recent work on can-masquerade-attacks shows that timing-based IDS assumptions are not enough when an attacker can substitute frames in situ while preserving periodicity.
- EV charging and smart-grid edge security live outside classic CAN tooling, but papers like a-hybrid-intrusion-detection-system-for-electric-vehicle-charging-infrastructure are a reminder that the broader vehicle-security stack includes charging infrastructure, not just the bus itself.
- Automotive HSMs complement CAN-level defenses by protecting ECU trust chains and key material, but they do not replace bus monitoring or gateway policy. automotive-hsms-architectural-challenges-security-implications treats hardware roots of trust as one layer in a broader vehicle security architecture.
- The Deep Defence on Wheels paper adds a deployment-oriented dual IDS pattern: quantized supervised and unsupervised models on FPGA can target known and unseen CAN anomalies, but cross-vehicle generalization, false positives, adversarial robustness, and fail-safe behavior remain open validation requirements. deep-defence-on-wheels-dual-ids-in-vehicle-network-security
- Software-defined vehicles widen the scope further: software-defined-vehicles turns the vehicle into a software-managed platform where OTA updates, cloud services, and supply-chain trust become part of the security perimeter.

- A moving-target defense for SDN-enabled EV charging networks (CS-SHIELD) counters low-rate attacks that exhaust switch flow tables by reshuffling chargers' virtual IP addresses when flow state and authenticated charging sessions disagree. It remains an emulated-testbed result requiring deployment validation. ^[sources/moving-target-defense-sdn-enabled-ev-charging-network-2026-10-08.md]

## November 2026 updates (updated 2026-11-21)
- CAN data is privacy-sensitive: CANTraj recovers vehicle trajectories from decoded CAN events even when GPS fields are omitted. ^[sources/cantraj-vehicle-trajectory-recovery-2026-11-13.md]
- Message integrity across mixed networks: a Karma Automotive patent publication matches messages received over Ethernet and CAN within a time window and splits key material across paths. ^[sources/uspto-karma-vehicle-security-system-2026-11-12.md]
- Detector claims need representative data; see [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]].

## Related pages
- [canarchy](https://github.com/hexsecs/canarchy)
- can-masquerade-attacks
- software-defined-vehicles
- mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba
- [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]]
- [[concepts/vehicle-data-privacy|Vehicle Data Privacy]]
- [[concepts/vehicle-trust-anchors|Vehicle Trust Anchors and Cryptography]]
