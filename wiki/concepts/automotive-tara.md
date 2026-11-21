---
uid: 01a1ff09-f9e0-7f3b-b660-119a645ee018
title: Automotive TARA
aliases:
- "TARA"
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- standards
sources:
- wiki/sources/integrating-attack-patterns-threat-modeling-automotive-domain-2026-10-29.md
- wiki/sources/block-harbor-automotive-threat-matrix-2026-11-04.md
- wiki/sources/block-harbor-fuzz-vs-pentest-2026-11-04.md
- wiki/sources/cross-domain-tara-to-nac-rule-mapping-automotive-oem-networks-2026-11-06.md
- wiki/sources/janus-vehicles-malicious-manufacturer-threat-model-2026-10-27.md
- wiki/sources/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md
- wiki/sources/beyond-smart-homes-iot-vulnerabilities-automotive-2026-10-30.md
- wiki/sources/sk-hynix-lpddr5x-iso-sae-21434-2026-11-11.md
- wiki/sources/lg-uplus-iso-sae-21434-ml3-2026-11-10.md
- wiki/sources/vicone-bluebinaries-automotive-cybersecurity-workflows-2026-10-27.md
confidence: medium
contested: false
contradictions: []
summary: Threat analysis and risk assessment (TARA) is the ISO/SAE 21434 process for
  identifying vehicle assets, threats, attack paths and risk. Recent work stresses
  structured attack taxonomies, traceability to controls, and honest feasibility scoring.
---

# Automotive TARA

## Definition
Threat analysis and risk assessment (TARA) is the core ISO/SAE 21434 activity for identifying vehicle assets, damage scenarios, threat scenarios and attack paths, then rating their feasibility and impact to derive cybersecurity goals. It feeds the cybersecurity management system (CSMS) that UNECE R155 expects OEMs and suppliers to operate.

## What the archive shows
- **Attack taxonomies make TARA more repeatable.** A preprint grounds TARA in ISO/SAE 21434 while using STRIDE and CAPEC to systematize attack-scenario discovery, illustrated with a Bluetooth headlamp case study. ^[sources/integrating-attack-patterns-threat-modeling-automotive-domain-2026-10-29.md] Block Harbor's introduction to Auto-ISAC's Automotive Threat Matrix (ATM) argues for using ATM technique IDs as a shared vocabulary across TARA, test planning, threat intelligence and VSOC/PSIRT handoffs. ^[sources/block-harbor-automotive-threat-matrix-2026-11-04.md]
- **TARA should trace to enforcement.** A cross-domain methodology maps ISO/SAE 21434 goals to network access-control rules at named enforcement points. Its desk-based OEM example turns 37 threats and 24 goals into 23 rules covering 11 of 13 in-scope goals. ^[sources/cross-domain-tara-to-nac-rule-mapping-automotive-oem-networks-2026-11-06.md]
- **Testing closes the loop.** Block Harbor separates automated fuzz coverage from human-led penetration testing and recommends turning fuzz crashes into pentest hypotheses and confirmed findings into regression tests mapped back to TARA priorities. ^[sources/block-harbor-fuzz-vs-pentest-2026-11-04.md]
- **Feasibility scores can be too generous.** A model-free false-data-injection attack, learned only from passive nominal measurements, displaced a lane-keeping benchmark by 1.25 m and stayed outside the lane for 9.21 s while alarm rates stayed below 2.4% at a matched 1% false-alarm point. That challenges TARA ratings that assume an attacker needs detailed system knowledge. ^[sources/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md]
- **Authentic does not mean benign.** The Janus Vehicles threat model covers components that stay authentic and protocol-conformant while doing undeclared sensing, communication or actuation, and suggests adding declared-purpose conformance checks to TARA and supplier assurance. ^[sources/janus-vehicles-malicious-manufacturer-threat-model-2026-10-27.md]
- **Supplier history is a risk input.** An analysis of over 15,000 IoT CVEs finds the automotive slice dominated by memory weaknesses and stronger similarity within a vendor than within a product type. ^[sources/beyond-smart-homes-iot-vulnerabilities-automotive-2026-10-30.md]
- **Process certification is spreading through the supply chain.** SK hynix reports ISO/SAE 21434 CSMS certification for its LPDDR5X development process ^[sources/sk-hynix-lpddr5x-iso-sae-21434-2026-11-11.md], and LG Uplus reports ML3 certification applied to real infotainment projects. ^[sources/lg-uplus-iso-sae-21434-ml3-2026-11-10.md] VicOne and BlueBinaries announced a partnership to fit security tooling into ISO/SAE 21434 and UNECE R155/R156 workflows. ^[sources/vicone-bluebinaries-automotive-cybersecurity-workflows-2026-10-27.md]

## Working guidance
- Tag threat scenarios with ATM technique IDs (and CAPEC where useful) so tests, intelligence and incident handoffs share identifiers.
- Give every control a trace back to a threat record, goal, asset and enforcement point.
- Rate feasibility with detection in mind: what an attacker can do while staying under alarm thresholds, not only whether they hold privileged knowledge.
- Treat supplier certifications as process evidence. Ask for scope, assessed sites and projects, and product-level integration evidence before relying on them.

## Open questions
- The STRIDE/CAPEC, ATM and TARA-to-NAC contributions are methods with worked examples, not measured deployment outcomes.
- The model-free attack result is a benchmark; vehicle-specific replication is open.

## Briefing trail
- [[briefings/automotive/2026/10/2026-10-30|30 Oct 2026]]: Janus Vehicles threat model
- [[briefings/automotive/2026/11/2026-11-02|2 Nov 2026]]: STRIDE/CAPEC mapping, IoT vulnerability patterns
- [[briefings/automotive/2026/11/2026-11-03|3 Nov 2026]]: VicOne and BlueBinaries partnership
- [[briefings/automotive/2026/11/2026-11-05|5 Nov 2026]]: Automotive Threat Matrix
- [[briefings/automotive/2026/11/2026-11-08|8 Nov 2026]]: fuzzing versus penetration testing
- [[briefings/automotive/2026/11/2026-11-09|9 Nov 2026]]: TARA-to-NAC mapping
- [[briefings/automotive/2026/11/2026-11-13|13 Nov 2026]]: SK hynix certification
- [[briefings/automotive/2026/11/2026-11-14|14 Nov 2026]]: LG Uplus certification
- [[briefings/automotive/2026/11/2026-11-18|18 Nov 2026]]: model-free stealthy attack

## Related pages
- [[entities/block-harbor|Block Harbor]]
- [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]]
- [[concepts/ai-defined-vehicles|AI-Defined Vehicles]]
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
