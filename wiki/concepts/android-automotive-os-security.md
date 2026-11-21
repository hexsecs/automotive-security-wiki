---
uid: 01a1ff09-f9de-7650-9169-7c2170e1eb21
title: Android Automotive OS Security
aliases:
- "Android Automotive OS"
- "Android Automotive"
- "AAOS"
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- infotainment
sources:
- wiki/sources/android-aaos-cve-2026-58915-2026-11-02.md
- wiki/sources/android-aaos-cve-2026-11-02.md
- wiki/sources/lg-uplus-iso-sae-21434-ml3-2026-11-10.md
- wiki/sources/monitoring-vulnerabilities-next-generation-automotive-operating-systems-2026-07-08.md
confidence: medium
contested: false
contradictions: []
summary: Android Automotive OS (AAOS) runs infotainment and cockpit software in many
  vehicles. Its monthly security bulletins make it a recurring patch-coordination
  workstream that depends on OEM and supplier firmware.
---

# Android Automotive OS Security

## Definition
Android Automotive OS (AAOS) is the vehicle-embedded build of Android that runs infotainment and cockpit functions directly on the head unit. Google publishes AAOS-specific security bulletins, but the firmware that reaches vehicles comes from the OEM or device supplier, so remediation runs through the supply chain.

## What the archive shows
- **Passenger displays are a new trust boundary.** CVE-2026-58915 lets an occupant on an AAOS multi-user, multi-display passenger screen view sensitive heads-up notification content and run protected passenger-user actions without authentication. The record lists Android 14, 15, 16, 16 QPR2 and 17 as affected and carries no CVSS score. ^[sources/android-aaos-cve-2026-58915-2026-11-02.md]
- **The November 2026 bulletin is a patch set, not one ticket.** It lists eight high-severity AAOS-specific CVEs: six elevation-of-privilege issues (CVE-2026-49903, CVE-2026-49906, CVE-2026-58915, CVE-2026-58925, CVE-2026-58927, CVE-2026-58930) and two information-disclosure issues (CVE-2026-58924, CVE-2026-58926). ^[sources/android-aaos-cve-2026-11-02.md]
- **Automotive OS exposure needs normalization, not raw CVE counts.** The VERA work on next-generation automotive operating systems shows that cross-stack scanning, package/version normalization and exploitability filtering matter more than raw CVE enumeration. ^[sources/monitoring-vulnerabilities-next-generation-automotive-operating-systems-2026-07-08.md]
- **Supplier process evidence for infotainment is appearing.** LG Uplus reports ISO/SAE 21434 ML3 certification applied to real infotainment software projects. ^[sources/lg-uplus-iso-sae-21434-ml3-2026-11-10.md]

## Working guidance
- Get firmware applicability from each supplier for each AAOS branch and confirm a security patch level of 2026-11-01 or later.
- Test isolation between driver and passenger users across lock and unlock states: notification redaction and `PendingIntent` authorization in particular.
- Track the bulletin as a recurring monthly workstream rather than a one-off.

## Open questions
- None of the November CVEs appeared in CISA KEV, and the bulletin alone does not establish exploitability in any vehicle program.
- A 15 November Kia infotainment research lead was seen only as a third-party summary of a video and remains unverified.

## Briefing trail
- [[briefings/automotive/2026/11/2026-11-03|3 Nov 2026]]: CVE-2026-58915
- [[briefings/automotive/2026/11/2026-11-04|4 Nov 2026]]: eight-CVE November bulletin
- [[briefings/automotive/2026/11/2026-11-14|14 Nov 2026]]: LG Uplus ML3 certification
- [[briefings/automotive/2026/11/2026-11-17|17 Nov 2026]]: unverified Kia lead

## Related pages
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
- [[concepts/connected-vehicle-identity|Connected-Vehicle Identity and Apps]]
- [[concepts/automotive-tara|Automotive TARA]]
