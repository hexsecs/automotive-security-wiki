---
uid: 01a1ff09-f9f9-7bcf-91d3-bf6fe0a7d8bc
title: Zero Day Initiative
aliases:
- "Zero Day Initiative"
- "ZDI"
created: 2026-11-21
updated: 2026-11-21
type: entity
entity_kind: researcher
tags:
- entity
- vulnerability-disclosure
sources:
- wiki/sources/zdi-united-chargers-grizzle-smart-40a-advisories-2026-11-18.md
- wiki/sources/zdi-united-chargers-grizzle-smart-40a-updatefirmware-2026-11-19.md
confidence: high
contested: false
contradictions: []
summary: Vulnerability-disclosure program whose November 2026 advisories on the United
  Chargers Grizzl-E Smart 40A are the archive's most concrete EV-charger findings.
---

# Zero Day Initiative

## Profile
The Zero Day Initiative (ZDI) is a vulnerability-research and coordinated-disclosure program that publishes advisories with CVE identifiers and CVSS scores. In this archive it is the primary source for EV-charger vulnerabilities.

## Contributions in this archive
- **Grizzl-E Smart 40A, 18 November 2026:** five advisories (ZDI-26-1032 to ZDI-26-1036) covering hard-coded OCPP-backend credentials, unauthenticated Wi-Fi configuration, two stack overflows and missing firmware-integrity checks. ZDI reported repeated failed attempts to reach the vendor, United Chargers. ^[sources/zdi-united-chargers-grizzle-smart-40a-advisories-2026-11-18.md]
- **Grizzl-E Smart 40A, 19 November 2026:** a sixth advisory (ZDI-26-1038, CVE-2026-131813), an out-of-bounds write in OCPP `UpdateFirmware` handling. ^[sources/zdi-united-chargers-grizzle-smart-40a-updatefirmware-2026-11-19.md]

## How to weigh it
ZDI advisories are high-confidence records of the product, CVE and described conditions. They do not establish exploitation in the wild, deployed exposure or remediation status.

## Related pages
- [[concepts/ev-charging-security|EV Charging Security]]
