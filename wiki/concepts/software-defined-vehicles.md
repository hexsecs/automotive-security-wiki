---
uid: 01a19d1a-2bea-734f-8f45-e0c1c20c373d
title: Software-Defined Vehicles
aliases:
- "software-defined vehicles"
- "software-defined vehicle"
- "SDVs"
- "SDV"
created: 2026-06-27
updated: 2026-11-26
type: concept
tags:
- research
- source
- synthesis
sources:
- wiki/sources/contextualizing-security-and-privacy-of-software-defined-vehicles-2026-06-23.md
- wiki/sources/monitoring-vulnerabilities-next-generation-automotive-operating-systems-2026-07-08.md
- wiki/sources/self-adaptive-anomaly-detection-reinforcement-learning-human-feedback-connected-vehicles-2026-07-09.md
- wiki/sources/securing-autonomous-vehicle-systems-twin-aware-federated-reinforcement-learning-2026-07-09.md
- wiki/sources/garage-llm-attack-graph-generation-2026-07-20.md
- wiki/sources/architecture-2-0-ai-agents-computer-system-design-2025-02-01.md
- wiki/sources/automotive-hsms-architectural-challenges-security-implications-2026-08-25.md
- wiki/sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md
- wiki/sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md
- wiki/sources/vicone-q3-2026-automotive-cyber-incidents.md
- wiki/sources/zf-digital-toolbox-2026-11-24.md
confidence: medium
contested: false
contradictions: []
summary: Software-defined vehicles (SDVs) are vehicles whose hardware capabilities
  are abstracted and managed through software, with centralized and distributed…
---

# Software-Defined Vehicles

## Definition
Software-defined vehicles (SDVs) are vehicles whose hardware capabilities are abstracted and managed through software, with centralized and distributed local and remote control, OTA update support, and increasingly cloud-connected services.

Wikipedia: [Software Defined Vehicle](https://en.wikipedia.org/wiki/Software_Defined_Vehicle)

## Current notes
- SDVs expand the security problem beyond the in-vehicle bus into OTA channels, APIs, third-party software, cloud backends, and supply-chain trust.
- The paper behind this page argues that SDV security is a lifecycle and architecture problem, not just a cryptography or network-filter problem.
- Mixed-criticality systems are a central challenge because the vehicle has to isolate and coordinate features with very different safety requirements.
- Privacy matters alongside security: data governance, consent, transparency, and purpose limitation all become part of the threat model.
- Standards alignment matters; the paper points toward ISO/SAE 21434 and UNECE WP.29-style thinking as part of the baseline.
- The VERA paper adds an operational layer: SDV vulnerability management needs cross-stack scanning, package/version normalization, exploitability filtering, and controlled validation rather than raw CVE enumeration. Its results show that certified or safety-oriented platforms can still retain meaningful exposure, while high CVE counts must be interpreted as potential attack surface rather than immediate compromise. ^[sources/monitoring-vulnerabilities-next-generation-automotive-operating-systems-2026-07-08.md]
- The connected-vehicle anomaly-detection paper adds runtime adaptation: OTA updates and changing workloads can create concept drift, so monitoring needs drift alarms, detector selection, human review, and replay-protected retraining rather than static thresholds alone. ^[sources/self-adaptive-anomaly-detection-reinforcement-learning-human-feedback-connected-vehicles-2026-07-09.md]
- SecApp extends the same defense boundary to collaborative control learning: federated RL needs poisoning-resistant aggregation, historical-update checks, and digital-twin rehearsal before learned policies influence safety-critical vehicles. ^[sources/securing-autonomous-vehicle-systems-twin-aware-federated-reinforcement-learning-2026-07-09.md]
- GARAGE adds architecture-aware attack-graph generation: RAG can accelerate tactical threat enumeration and CTI synthesis, but firmware, persistence, proprietary IPC, and other implementation-level steps still require human validation. ^[sources/garage-llm-attack-graph-generation-2026-07-20.md]
- Deep Defence on Wheels adds a hardware-aware runtime defense pattern for in-vehicle networks: quantized supervised and unsupervised IDS models are co-deployed on an FPGA/SoC, but production claims still require cross-vehicle, adversarial, false-positive, and fail-safe validation. ^[sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md, sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]
- The automotive HSM paper frames hardware-rooted trust as a way to support secure boot, key storage, secure execution, and software signing, while leaving isolation, performance, updateability, side-channel, and post-quantum tradeoffs explicit. ^[sources/automotive-hsms-architectural-challenges-security-implications-2026-08-25.md, sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md, sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]
- Architecture 2.0 provides a cross-domain design-governance analogue: AI agents in complex system design need secure data exchange, standardized evaluation, hardware-in-the-loop verification, interpretable outputs, and human override rather than autonomous generation by default. ^[sources/architecture-2-0-ai-agents-computer-system-design-2025-02-01.md, sources/automotive-hsms-architectural-challenges-security-implications-2026-08-25.md, sources/deep-defence-on-wheels-dual-ids-in-vehicle-network-security-2026-10-05.md, sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]

- moving-target-defense-sdn-enabled-ev-charging-network adds a network-layer defense against low-rate SDN flow-table exhaustion, but remains an emulated-testbed result requiring deployment validation.
- secfd-fl-secure-aggregation-iov-charging-load-forecasting adds a privacy-preserving federated-learning pattern for charging-load forecasting; its masking and key-management assumptions still need operational validation. ^[sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]

## November 2026 synthesis (updated 2026-11-21)
- Incidents have reached the vehicle domain: VicOne observed 400 automotive incidents in Q3 2026, 174 of them involving in-vehicle systems against 149 in enterprise IT. ^[sources/vicone-q3-2026-automotive-cyber-incidents.md]
- The SDV perimeter now has its own notes:
  - [[concepts/connected-vehicle-identity|Connected-Vehicle Identity and Apps]] covers accounts, apps and backend APIs.
  - [[concepts/android-automotive-os-security|Android Automotive OS Security]] covers the infotainment OS and its patch cadence.
  - [[concepts/ev-charging-security|EV Charging Security]] covers chargers, OCPP and Plug & Charge.
  - [[concepts/ai-defined-vehicles|AI-Defined Vehicles]] covers models and agents in vehicle decisions.
  - [[concepts/vehicle-trust-anchors|Vehicle Trust Anchors and Cryptography]] covers HSMs, TPMs and PQC.
  - [[concepts/automotive-tara|Automotive TARA]] covers ISO/SAE 21434 risk analysis.
  - [[concepts/v2x-security|V2X Security]] covers vehicle-to-vehicle and vehicle-to-infrastructure links.

## Supplier-delivered lifecycle services (updated 2026-11-26)
- Suppliers are packaging the update and service path as a product. ZF Commercial Vehicle Solutions announced Digital Toolbox on 24 November 2026: diagnostics, secure ECU access, software management, OTA updates and component health monitoring, which OEMs can adopt one at a time or integrate with their own backends. ^[sources/zf-digital-toolbox-2026-11-24.md]
- When one supplier offers both diagnostics and update delivery, the split of authority between the OEM backend, the supplier service and the vehicle becomes a procurement question. Ask who can authorize diagnostic access and who can approve a software update, who holds the signing keys, how roles are separated and audited, and how the vehicle recovers when a backend is unavailable.
- The announcement states scope only. It does not establish security conformance or field performance.

## Related pages
- [[automotive-can]]
- deep-defence-on-wheels-dual-ids-in-vehicle-network-security
- [[can-masquerade-attacks]]
- contextualizing-security-and-privacy-of-software-defined-vehicles
- monitoring-vulnerabilities-next-generation-automotive-operating-systems
- self-adaptive-anomaly-detection-reinforcement-learning-human-feedback-connected-vehicles
- securing-autonomous-vehicle-systems-twin-aware-federated-reinforcement-learning
- garage-llm-attack-graph-generation
- architecture-2-0-ai-agents-computer-system-design
