---
uid: 01a19d1a-2be6-77f7-bc99-069f5e83f1b9
title: GNSS Spoofing
created: 2026-06-19
updated: 2026-06-27
type: concept
tags:
- research
- source
- software
sources:
- wiki/sources/gnss-spoofing-threat-for-v2x-communications-2026-06-19.md
confidence: medium
contested: false
contradictions: []
summary: GNSS spoofing is the deliberate transmission of counterfeit navigation signals
  that cause a receiver to compute a false position, velocity, or timing…
---

# GNSS Spoofing

## Definition
GNSS spoofing is the deliberate transmission of counterfeit navigation signals that cause a receiver to compute a false position, velocity, or timing solution.

Wikipedia: [GNSS spoofing](https://en.wikipedia.org/wiki/GNSS_spoofing)

## Why it matters
This paper frames GNSS spoofing as a practical threat to V2X systems because cooperative awareness and vehicle safety can depend on position trust. The attack path is unglamorous and therefore nasty: cheap SDR hardware, generated baseband signals, and enough fidelity to mislead real OBU/RSU devices.

## Common ingredients
- Signal replay or synthesis with SDR hardware
- A trajectory model that is plausible enough to pass as legitimate motion
- Timing discipline to keep the forged solution coherent
- Target receivers that lack strong spoofing detection

## Failure modes / open questions
- Detection is often the hard part; a clean demo of attack success does not prove robust field breakage across all receivers.
- Real traffic, multipath, and environmental noise may change the difficulty substantially.
- The paper validates a path, not a universal attack guarantee.

## Related pages
- gnss-spoofing-threat-for-v2x-communications
- [[automotive-can|Automotive CAN]]
- [Public source records](../sources/)
