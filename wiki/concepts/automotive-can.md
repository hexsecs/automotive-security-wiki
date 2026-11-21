---
uid: 01a19d1a-2be3-74ab-b336-e8f565b83966
title: Automotive CAN
created: 2026-05-22
updated: 2026-10-11
type: concept
tags:
- software
- canarchy
- research
sources:
- wiki/sources/mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba-2026-06-17.md
- wiki/sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md
confidence: medium
contested: false
contradictions: []
summary: Automotive CAN refers to Controller Area Network systems and data used in
  vehicles and related embedded systems. This page is a placeholder for CAN-bus…
---

# Automotive CAN

## Definition
Automotive CAN refers to Controller Area Network systems and data used in vehicles and related embedded systems. This page is a placeholder for CAN-bus concepts, protocols, diagnostics workflows, and tooling research that supports canarchy.

Wikipedia: [CAN bus](https://en.wikipedia.org/wiki/CAN_bus)

## Current notes
- CAN-related research should connect back to canarchy when it informs package design, examples, docs, or demos.
- Useful future subtopics may include J1939, UDS, SocketCAN, decoding workflows, trace analysis, diagnostic automation, and stealthy attack detection.
- Recent work on can-masquerade-attacks shows that timing-based IDS assumptions are not enough when an attacker can substitute frames in situ while preserving periodicity.
- EV charging and smart-grid edge security live outside classic CAN tooling, but papers like a-hybrid-intrusion-detection-system-for-electric-vehicle-charging-infrastructure are a reminder that the broader vehicle-security stack includes charging infrastructure, not just the bus itself.
- Automotive HSMs complement CAN-level defenses by protecting ECU trust chains and key material, but they do not replace bus monitoring or gateway policy. automotive-hsms-architectural-challenges-security-implications treats hardware roots of trust as one layer in a broader vehicle security architecture.
- The Deep Defence on Wheels paper adds a deployment-oriented dual IDS pattern: quantized supervised and unsupervised models on FPGA can target known and unseen CAN anomalies, but cross-vehicle generalization, false positives, adversarial robustness, and fail-safe behavior remain open validation requirements. deep-defence-on-wheels-dual-ids-in-vehicle-network-security
- Software-defined vehicles widen the scope further: software-defined-vehicles turns the vehicle into a software-managed platform where OTA updates, cloud services, and supply-chain trust become part of the security perimeter.

- moving-target-defense-sdn-enabled-ev-charging-network adds a network-layer defense against low-rate SDN flow-table exhaustion, but remains an emulated-testbed result requiring deployment validation.

## Related pages
- canarchy
- python
- can-masquerade-attacks
- software-defined-vehicles
- mids-detecting-stealthy-masquerade-and-tampering-attacks-on-can-bus-via-bidirectional-mamba
