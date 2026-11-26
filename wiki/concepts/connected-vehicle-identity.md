---
uid: 01a1ff09-f9e3-743b-afc1-008a9b43abd7
title: Connected-Vehicle Identity and Apps
aliases:
- "connected-car APIs"
- "app-to-vehicle authorization"
- "account-to-vehicle authorization"
created: 2026-11-21
updated: 2026-11-26
type: concept
tags:
- research
- synthesis
- telematics
sources:
- wiki/sources/sam-curry-forgerock-two-automakers-2026-11-07.md
- wiki/sources/cert-in-tata-ira-app-vulnerabilities-2026-11-04.md
- wiki/sources/vicone-q3-2026-automotive-cyber-incidents.md
- wiki/sources/fia-wp29-200-18-vehicle-data-access-2026-11-18.md
confidence: medium
contested: false
contradictions: []
summary: Connected-vehicle identity covers the customer accounts, mobile apps, identity
  platforms and backend APIs that let owners reach their cars remotely. Failures there
  can grant owner-equivalent access without touching the vehicle.
---

# Connected-Vehicle Identity and Apps

## Definition
Connected vehicles are reached through customer accounts, mobile apps, identity platforms and backend APIs. Whoever controls that chain can often read telemetry and send remote commands with the same authority as the owner, without any in-vehicle exploit. The trust boundary that matters is customer account to vehicle authorization.

## What the archive shows
- **An identity platform reached two automakers' cars.** Researchers chained an exposed ForgeRock/OpenIDM administrative surface, default credentials, and differences in how the WAF and backend interpreted paths into production identity access at two unnamed automakers. In controlled testing, valid customer sessions reached connected-car APIs with owner-equivalent telemetry and remote commands. The U.S. chain was reportedly fixed quickly. ^[sources/sam-curry-forgerock-two-automakers-2026-11-07.md]
- **Companion apps leak the keys.** CERT-In reported four high-severity flaws in older builds of Tata Motors' iRA 2.0 and iRA.ev apps: hard-coded credentials and API material, unsafe WebView URL and origin handling, tokens in logs, and ineffective certificate pinning. Fixed versions are iRA 2.0 26.8.2 and iRA.ev 26.9.1. ^[sources/cert-in-tata-ira-app-vulnerabilities-2026-11-04.md]
- **Regulators are being asked for a common permission model.** In an informal WP.29 submission dated 18 November 2026, FIA proposes exploring a common reference for vehicle-data authentication and authorization: roles, assurance levels, and how permissions are expressed and recognized. Its examples are automated-driving records, fuel and energy consumption data, electronic inspections and digital keys. That is the account-to-vehicle boundary above, generalized to third parties. ^[sources/fia-wp29-200-18-vehicle-data-access-2026-11-18.md]
- **Incidents are not only in the enterprise.** VicOne observed 400 automotive cybersecurity incidents in Q3 2026: 174 involved in-vehicle systems and 149 enterprise IT, with ransomware in 97. The counts are proprietary observations, not a census. ^[sources/vicone-q3-2026-automotive-cyber-incidents.md]

## Working guidance
- Audit identity deployments (ForgeRock/PingIDM and others) for exposed admin consoles such as `/system/console`, default or staging credentials, and edge-versus-backend path discrepancies.
- Do not rely on WAF rules to cover backend exposure.
- Test account-to-vehicle authorization as its own boundary: a valid session should not reach a vehicle the account does not own.
- Model third-party access with the same rigor as owner access: who is asking, what grant they hold, at what assurance level, and how it is revoked. Expect jurisdiction-specific access rights to constrain any common scheme.
- Strip secrets and debug logging from mobile release builds, retest WebView-to-native trust, and verify certificate pinning.

## Open questions
- The automakers in the ForgeRock chain are unnamed and residual exposure elsewhere is unknown.
- The Tata advisory does not show active exploitation or any vehicle-control compromise.
- The FIA proposal is an informal submission; whether WP.29 takes up work on it was not confirmed as of 24 November 2026.
- An older Bluetooth anti-theft disclosure (Acrisure KARR BT/DR-100, July–August 2026) predates this archive's freshness window and stays on the historical watchlist.

## Briefing trail
- [[briefings/automotive/2026/10/2026-10-18|18 Oct 2026]]: VicOne Q3 incident report
- [[briefings/automotive/2026/11/2026-11-10|10 Nov 2026]]: ForgeRock chain, Tata iRA advisory
- [[briefings/automotive/2026/11/2026-11-11|11 Nov 2026]]: follow-up, no new development
- [[briefings/automotive/2026/11/2026-11-24|24 Nov 2026]]: FIA vehicle-data access proposal to WP.29

## Related pages
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
- [[concepts/android-automotive-os-security|Android Automotive OS Security]]
- [[concepts/vehicle-data-privacy|Vehicle Data Privacy]]
- [[entities/vicone|VicOne]]
