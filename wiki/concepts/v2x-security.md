---
uid: 0c682324-c5cd-45cc-a624-fef243f15b36
title: V2X Security
aliases:
- "V2X security"
- "V2X"
- "VANETs"
- "VANET"
- "vehicular ad hoc networks"
created: 2026-11-26
updated: 2026-11-26
type: concept
tags:
- research
- synthesis
- v2x
sources:
- wiki/sources/springer-v2x-security-survey-2026-11-21.md
- wiki/sources/scirep-vanet-hybrid-dl-secure-clustering-2026-11-23.md
- wiki/sources/gnss-spoofing-threat-for-v2x-communications-2026-06-19.md
- wiki/sources/post-quantum-cryptography-automotive-context-2026-10-28.md
- wiki/sources/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md
- wiki/sources/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md
- wiki/sources/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md
- wiki/sources/vehicular-edge-ids-post-quantum-cryptography-2026-11-19.md
confidence: medium
contested: false
contradictions: []
summary: V2X security covers the links between vehicles, roadside units and networks,
  whether direct (DSRC, C-V2X sidelink) or network-mediated, and the trust decisions
  vehicles make on what those links tell them.
---

# V2X Security

## Definition
Vehicle-to-everything (V2X) communication connects vehicles to each other (V2V), to roadside units and infrastructure (V2I) and to networks. Links are either direct radio (DSRC or the C-V2X sidelink) or network-mediated, and the two have different dependencies and failure modes. Vehicular ad hoc networks (VANETs) are the research framing for the direct case, where vehicles join and leave groups as they move. The security problem is less about the radio than about the trust a vehicle places in a message: who sent it, whether it is intact, and whether its content (position above all) is plausible.

## What the archive shows
- **A new survey maps the defenses.** A November 2026 journal review compares DSRC and cellular V2X and catalogs proactive (prevention) and reactive (detection) defenses, including data-driven detection. It is useful as a coverage check for a V2X TARA, not as validation of any one defense. ^[sources/springer-v2x-security-survey-2026-11-21.md]
- **Position is the weakest input.** GNSS spoofing with cheap SDR hardware can mislead real OBU and RSU devices, so cooperative awareness inherits whatever trust the receiver puts in its own position. ^[sources/gnss-spoofing-threat-for-v2x-communications-2026-06-19.md] See [[concepts/gnss-spoofing|GNSS Spoofing]].
- **Clustering is a trust decision.** A Scientific Reports paper proposes hybrid deep learning for secure VANET clustering, motivated by message-integrity and confidentiality risks. Only the landing page could be checked. ^[sources/scirep-vanet-hybrid-dl-secure-clustering-2026-11-23.md] CULypso also clusters VANET participants, to make federated unlearning tractable. ^[sources/arxiv-2611-22682-culypso-vehicular-unlearning-2026-11-17.md] In both, cluster reassignment as vehicles move and roadside coverage varies is where trust can be gained or lost.
- **PQC is being costed for V2X.** Simulated rural V2V and urban V2X scenarios put ML-KEM, ML-DSA and FALCON against an ECDSA/ECDH baseline, ^[sources/post-quantum-cryptography-automotive-context-2026-10-28.md] and a federated-learning design adds post-quantum-authenticated V2I links. ^[sources/communication-efficient-private-federated-reinforcement-learning-vehicular-networks-2026-10-29.md] See [[concepts/vehicle-trust-anchors|Vehicle Trust Anchors and Cryptography]].
- **Public evidence for detectors is thin.** The Cybersecurity Dataset Observatory finds limited public V2X and vehicular-network datasets. ^[sources/arxiv-2611-20812-cybersecurity-dataset-observatory-2026-11-16.md] A vehicular edge study shows why splits matter: it splits VeReMi NextGen by sender so the same vehicle does not appear in training and test data. ^[sources/vehicular-edge-ids-post-quantum-cryptography-2026-11-19.md] See [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]].

## Working guidance
- In a V2X TARA, map prevention and detection separately for direct and network-mediated paths, and use the survey's taxonomy to check for gaps.
- Treat received position as a claim to be checked against independent sensors and neighbors, not a fact.
- For clustered or group schemes, test join, leave and reassignment under mobility and patchy roadside coverage, and state the authentication assumptions behind each step.
- Evaluate V2X detectors with the IDS evidence checklist: sender- or vehicle-level splits, leakage checks, baselines and false-positive rates on the target hardware.
- Ask for PQC message size and latency on the actual radio and channel load before planning a migration.

## Open questions
- The survey is a map of related work; none of the defenses it catalogs is validated here.
- The VANET clustering paper's methods and results were not verified beyond the landing page.
- The PQC and federated-learning results are simulation-based.
- The archive has no V2X vulnerability advisory or field incident yet.

## Briefing trail
- [[briefings/automotive/2026/10/2026-10-30|30 Oct 2026]]: PQC in V2V/V2X
- [[briefings/automotive/2026/11/2026-11-04|4 Nov 2026]]: PQ-authenticated federated learning
- [[briefings/automotive/2026/11/2026-11-18|18 Nov 2026]]: CULypso clustered unlearning
- [[briefings/automotive/2026/11/2026-11-20|20 Nov 2026]]: thin public V2X datasets
- [[briefings/automotive/2026/11/2026-11-24|24 Nov 2026]]: V2X security survey
- [[briefings/automotive/2026/11/2026-11-25|25 Nov 2026]]: secure VANET clustering

## Related pages
- [[concepts/gnss-spoofing|GNSS Spoofing]]
- [[concepts/vehicle-trust-anchors|Vehicle Trust Anchors and Cryptography]]
- [[concepts/in-vehicle-ids-evaluation|In-Vehicle IDS Evaluation]]
- [[concepts/vehicle-data-privacy|Vehicle Data Privacy]]
- [[concepts/automotive-tara|Automotive TARA]]
