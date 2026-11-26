# Public wiki log

## 2026-11-21 publish | Automotive security research wiki
- Created a public export containing automotive briefing snapshots, selected durable notes, and metadata-only source records.
- Excluded private operational notes, compatibility stubs, credentials, and full raw source captures.

## 2026-11-21 publish | Website
- Published the wiki as a static site on GitHub Pages: https://hexsecs.github.io/automotive-security-wiki/

## 2026-11-21 synthesize | Durable notes from the briefing archive
- Added eight concept notes drawn from the October–November briefings: AI-defined vehicles, Android Automotive OS security, automotive TARA, connected-vehicle identity and apps, EV charging security, in-vehicle IDS evaluation, vehicle data privacy, and vehicle trust anchors and cryptography.
- Added entity notes for Block Harbor, CATARC, VicOne and the Zero Day Initiative.
- Refreshed GNSS spoofing, CAN masquerade attacks, software-defined vehicles and automotive CAN with November evidence.
- Briefing snapshots were not edited; notes link back to them through briefing trails.

## 2026-11-21 sanitize | Public-edition privacy pass
- Replaced private capture paths in footnotes (`raw/articles/…`, `raw/papers/…`) with public source-record paths.
- Replaced an internal tooling name ("dashboard archive") with "briefing archive" in six briefings, and two internal page names with links to the public briefings. No findings, dates or confidence labels changed.
- Removed a compatibility-path note from the briefing index and links to unpublished private notes; canarchy references now point to the public repository.
- Added `aliases` to notes, organizations and named source records so the site links first mentions inline; regenerated `wiki/sources/MANIFEST.sha256`.

## 2026-11-26 synthesize | Durable notes from the 23–25 November briefings
- Added a V2X security note that brings together the new V2X survey and VANET clustering paper with earlier GNSS spoofing, PQC, federated-unlearning and dataset evidence.
- EV charging security and the Zero Day Initiative entity: added the six ChargePoint Home Flex advisories (ZDI-26-1110 to ZDI-26-1115) and compared them with the Grizzl-E cluster.
- Connected-vehicle identity: added FIA's WP.29 proposal for common vehicle-data authentication and authorization.
- Software-defined vehicles: added ZF Digital Toolbox and the procurement question of who may authorize diagnostics and who may authorize updates.
- Vehicle trust anchors and in-vehicle IDS evaluation: added the 19 November edge IDS/PQC paper's shared-budget finding and links to the new V2X note.
- The 23 November quiet-day briefing yielded no new durable claim; it is recorded in the EV charging briefing trail.
- Added five metadata-only source records, listed all source records in the source index (22 were missing), and regenerated `wiki/sources/MANIFEST.sha256`, which also lacked the 19 November edge IDS record.
- Briefing snapshots were not edited.
