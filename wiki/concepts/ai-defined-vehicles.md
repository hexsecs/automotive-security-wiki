---
uid: 01a1ff09-f9db-75a2-80c2-ee12b78f747e
title: AI-Defined Vehicles
aliases:
- "AI-defined vehicles"
- "AI-defined vehicle"
- "AI-defined-vehicle"
- "AIDV"
created: 2026-11-21
updated: 2026-11-21
type: concept
tags:
- research
- synthesis
- ai
sources:
- wiki/sources/vicone-ai-defined-vehicles-2026-10-29.md
- wiki/sources/vicone-ai-defined-vehicles-securing-decisions-2026-11-19.md
- wiki/sources/vicone-lab-r7-manipulated-inputs-2026-11-11.md
- wiki/sources/catarc-automotive-ai-cybersecurity-guidance-drafts-2026-11-10.md
- wiki/sources/thermal-side-channel-perception-attacks-autonomous-vehicles-2026-10-15.md
- wiki/sources/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md
- wiki/sources/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md
confidence: medium
contested: false
contradictions: []
summary: AI-defined vehicles give learned models and AI agents a central role in vehicle
  decisions. Security then has to cover the path from manipulated input, through model
  or agent decision, to vehicle action.
---

# AI-Defined Vehicles

## Definition
An AI-defined vehicle (AIDV) gives learned models and agentic orchestration a central role in how the vehicle decides and acts. It keeps every software-defined-vehicle exposure (ECUs, networks, OTA, backends) and adds new dependencies: model supply chains, language inputs, prompts and policies, agent tools and persistent context.

## What the archive shows
- **The security question moves to decisions.** VicOne's 29 October analysis argues that the question is no longer only whether a component is authentic, but how an AI-mediated decision is formed and what it is allowed to influence. It recommends adding model provenance, prompt and policy integrity, tool permissions, context handling and bounded actions to TARA and supplier reviews. ^[sources/vicone-ai-defined-vehicles-2026-10-29.md]
- **Trace input to action.** VicOne's 19 November follow-up maps attack paths through manipulated inputs, poisoned model supply chains, prompt injection and excessive agent authority. It recommends enforcing authorization outside the model and monitoring model and agent behavior alongside CAN. It cites a ReasonBreak study reporting up to 72% trajectory-manipulation success against Alpamayo 1 in closed-loop simulation. ^[sources/vicone-ai-defined-vehicles-securing-decisions-2026-11-19.md]
- **Safety functions can work as designed and still be fooled.** VicOne LAB R7's robotics research shows safety functions behaving correctly while manipulated sensor, position, audio or visual inputs drive the wrong decision. Redundant checks give less assurance when one manipulation reaches several inputs. ^[sources/vicone-lab-r7-manipulated-inputs-2026-11-11.md]
- **Perception has physical attack surfaces.** A survey links thermal-IR perception spoofing with co-tenant leakage through thermal, DVFS and thermal-event telemetry. ^[sources/thermal-side-channel-perception-attacks-autonomous-vehicles-2026-10-15.md] A model-free false-data-injection attack shows that learned control can be pushed off course while evading tested monitors. ^[sources/arxiv-2611-20293-model-free-stealthy-vehicle-attack-2026-11-15.md]
- **Regulators are writing AI into automotive security.** China opened comment on drafts covering automotive-AI information-security requirements and test methods, spanning AI process assurance, models, cockpit AI and driving-automation applications. ^[sources/catarc-automotive-ai-cybersecurity-guidance-drafts-2026-11-10.md]
- **Model governance includes forgetting.** CULypso proposes clustered federated unlearning for vehicular networks and reports roughly 65% improvement over FedEraser in the authors' experiments. ^[sources/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md]

## Working guidance
- Add input-to-action abuse cases to TARA: for each AI-influenced function, list the inputs, the decision, the action and what bounds it.
- Enforce authority outside the model, with independent safety interlocks that do not share the same untrusted input.
- Track model and data provenance like any other supplier artifact.
- Test coordinated spoofing of several inputs, not one sensor at a time.

## Open questions
- VicOne's analyses are forward-looking vendor research; none demonstrates a production vehicle compromise.
- The LAB R7 demonstrations are on robots, not vehicles.
- The CATARC texts are drafts, and their detailed requirements need verification against the Chinese-language originals.

## Briefing trail
- [[briefings/automotive/2026/10/2026-10-18|18 Oct 2026]]: thermal side-channel survey
- [[briefings/automotive/2026/10/2026-10-31|31 Oct 2026]]: VicOne AIDV part one
- [[briefings/automotive/2026/11/2026-11-12|12 Nov 2026]]: manipulated safety inputs
- [[briefings/automotive/2026/11/2026-11-13|13 Nov 2026]]: CATARC AI security drafts
- [[briefings/automotive/2026/11/2026-11-18|18 Nov 2026]]: model-free attack, CULypso
- [[briefings/automotive/2026/11/2026-11-19|19 Nov 2026]]: VicOne input-to-action analysis

## Related pages
- [[entities/vicone|VicOne]]
- [[entities/catarc|CATARC]]
- [[concepts/automotive-tara|Automotive TARA]]
- [[concepts/software-defined-vehicles|Software-Defined Vehicles]]
