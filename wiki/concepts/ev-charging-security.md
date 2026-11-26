---
uid: 01a1ff09-f9e6-7e06-8d72-815864e9a159
title: EV Charging Security
aliases:
- "EV charging"
- "EV-charging"
- "EVSE"
- "OCPP"
- "Plug & Charge"
created: 2026-11-21
updated: 2026-11-26
type: concept
tags:
- research
- synthesis
- ev-charging
sources:
- wiki/sources/zdi-united-chargers-grizzle-smart-40a-advisories-2026-11-18.md
- wiki/sources/zdi-united-chargers-grizzle-smart-40a-updatefirmware-2026-11-19.md
- wiki/sources/zdi-chargepoint-home-flex-advisories-2026-11-24.md
- wiki/sources/arxiv-2611-14362-ocpp-sast-2026-11-10.md
- wiki/sources/athene-automotive-security-plug-charge-tpm-2026-11-13.md
- wiki/sources/catarc-bms-standard-draft-memory-security-2026-11-10.md
- wiki/sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md
confidence: medium
contested: false
contradictions: []
summary: EV charging security covers chargers (EVSE), their OCPP management backends,
  the vehicle-side Plug & Charge trust chain, and the battery systems they touch.
---

# EV Charging Security

## Definition
EV charging security covers the charger itself (EVSE), the OCPP link between chargers and their charging-station management system (CSMS), the ISO 15118 Plug & Charge trust chain between vehicle and charger, and the battery-management systems that charging ultimately controls. It sits at the edge of the vehicle: much of the attack surface is network infrastructure, but the consequences reach vehicle hardware and safety-relevant control units.

## What the archive shows
- **The Grizzl-E cluster is the most concrete EVSE signal so far.** ZDI published five advisories on 18 November 2026 for the United Chargers Grizzl-E Smart 40A: hard-coded OCPP-backend credentials (CVE-2026-131811), unauthenticated Wi-Fi configuration changes (CVE-2026-131808), two stack buffer overflows in OCPP/FTP handling (CVE-2026-131807, CVE-2026-131812) and missing firmware-integrity verification (CVE-2026-131810). ZDI describes them as network-adjacent, unauthenticated and chainable toward code execution, and reports failed attempts to reach the vendor. ^[sources/zdi-united-chargers-grizzle-smart-40a-advisories-2026-11-18.md]
- **A sixth advisory extended it the next day.** CVE-2026-131813 is an out-of-bounds write in OCPP `UpdateFirmware` handling that can support code execution in combination with the other issues. ^[sources/zdi-united-chargers-grizzle-smart-40a-updatefirmware-2026-11-19.md]
- **A second residential charger followed within a week.** On 24 November 2026 ZDI published six ChargePoint Home Flex advisories (ZDI-26-1110 to ZDI-26-1115, CVE-2026-131814 to CVE-2026-131819). ZDI rates CVE-2026-131817 as network-adjacent, unauthenticated code execution (CVSS 8.8) and names firmware 2024.02.00.259-alpha for it; the other five cover authentication bypass or local privilege escalation. ChargePoint documents activation as the route to software updates, so a fix depends on the unit keeping that connectivity. ^[sources/zdi-chargepoint-home-flex-advisories-2026-11-24.md]
- **The two clusters share a pattern.** Both are home chargers reachable from the adjacent network, ZDI published both within a week, and both put adjacent-network code execution at the top of triage. Grizzl-E adds missing firmware integrity and embedded backend credentials; Home Flex adds authentication bypass and local privilege escalation. ^[sources/zdi-united-chargers-grizzle-smart-40a-advisories-2026-11-18.md, sources/zdi-chargepoint-home-flex-advisories-2026-11-24.md]
- **OCPP implementations are hard to assure with one tool.** An IEEE CSR 2026 paper evaluates static-analysis (SAST) coverage across languages using OCPP implementations. OCPP is specification-heavy and open to divergent interpretation, so tool coverage that holds for one language may not hold for another. ^[sources/arxiv-2611-14362-ocpp-sast-2026-11-10.md]
- **Plug & Charge key storage is being rethought for zonal vehicles.** ATHENE/Fraunhofer proposes one TPM 2.0 on a high-performance controller that generates, stores and uses keys for several EV communication controllers, demonstrated with emulated EVCC and SECC devices. It reduces repeated trust anchors but concentrates trust and availability in one controller. ^[sources/athene-automotive-security-plug-charge-tpm-2026-11-13.md]
- **Battery systems are entering security standards.** A Chinese draft national standard for EV battery-management systems, open for comment from 10 November 2026, adds a test boundary between legitimate and unauthorized commands that read or modify BMS memory. ^[sources/catarc-bms-standard-draft-memory-security-2026-11-10.md]
- **Charging data is also a privacy problem.** Federated charging-load forecasting work uses masking and secure aggregation, but its key-management assumptions still need operational validation. ^[sources/secfd-fl-secure-aggregation-iov-charging-load-forecasting-2026-10-09.md]

## Recurring controls
- Inventory deployed chargers, including firmware versions, and isolate OCPP and management interfaces from untrusted adjacent networks.
- Limit local access from untrusted devices without cutting the update path the vendor relies on; for Home Flex, that means keeping the unit activated and connected.
- Verify firmware signing and update integrity; the Grizzl-E cluster shows how a missing integrity check combines with parser bugs.
- Rotate or remove embedded backend credentials.
- Pair SAST with protocol conformance tests, fuzzing, dependency/SBOM review and secrets scanning on the actual OCPP codebase.
- For centralized Plug & Charge trust anchors, test failure handling, key-use authorization between ECUs, provisioning, recovery and blast radius.

## Open questions
- No vendor fix or compensating-control guidance for the Grizzl-E cluster had been established as of 21 November 2026.
- For Home Flex, a generally available fixed release for each hardware variant and its rollout status were not verified as of 25 November 2026.
- None of the archived EVSE advisories shows exploitation in the wild, and none was added to CISA KEV through the 25 November check.
- The BMS draft is a consultation, not a requirement, and its detailed text is Chinese-language.

## Briefing trail
- [[briefings/automotive/2026/11/2026-11-14|14 Nov 2026]]: BMS draft standard
- [[briefings/automotive/2026/11/2026-11-15|15 Nov 2026]]: centralized TPM for Plug & Charge
- [[briefings/automotive/2026/11/2026-11-17|17 Nov 2026]]: OCPP SAST coverage
- [[briefings/automotive/2026/11/2026-11-19|19 Nov 2026]]: five Grizzl-E advisories
- [[briefings/automotive/2026/11/2026-11-20|20 Nov 2026]]: sixth Grizzl-E advisory
- [[briefings/automotive/2026/11/2026-11-21|21 Nov 2026]]: follow-up, no new development
- [[briefings/automotive/2026/11/2026-11-23|23 Nov 2026]]: quiet day; Grizzl-E triage unchanged
- [[briefings/automotive/2026/11/2026-11-25|25 Nov 2026]]: six ChargePoint Home Flex advisories

## Related pages
- [[entities/zero-day-initiative|Zero Day Initiative]]
- [[concepts/vehicle-trust-anchors|Vehicle Trust Anchors and Cryptography]]
- [[entities/catarc|CATARC]]
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
