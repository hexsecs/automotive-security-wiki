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

## 2026-11-26 provenance | Canonical origins for placeholder source records
- An audit found 17 source records with no canonical URL (placeholders created at export) and one paper cited in two notes with no record at all.
- Six records took their canonical URL from the briefing that cites them: the OCPP SAST, model-free attack and CULypso arXiv papers, the CATARC BMS draft, the LG Uplus ML3 announcement, and the AAOS bulletin. The AAOS record duplicates the existing bulletin record; it is kept because the 4 November briefing names it, and the AAOS note now cites the original.
- Eleven records were matched to arXiv or publisher records by title, authors and date (checked against arXiv on 26 November): GNSS spoofing for V2X, MIDS, VERA, SecApp, self-adaptive anomaly detection, GARAGE, the automotive HSM paper, Deep Defence on Wheels, SecFD-FL, the SDV security survey (ACM DOI) and Architecture 2.0 (IEEE Computer DOI). The GNSS paper's date was corrected from 19 to 18 June; the SDV survey's 23 June date matches no arXiv version and is flagged as unconfirmed in its record.
- Added a record for the moving-target defense paper (arXiv 2610.11996) and cited it in the SDV and automotive CAN notes, which had named it without a citation.
- Removed unrelated sources from three SDV-note citations that had accumulated papers belonging to neighboring bullets.
- Regenerated `wiki/sources/MANIFEST.sha256`. Briefing snapshots were not edited.

## 2026-11-26 provenance | Evidence statements for every source record
- A second audit found 28 records whose evidence status said only `captured`, or nothing. Each now carries the confidence statement from the briefing that assessed it, with a link to that briefing; wording is unchanged except one internal process clause removed from the thermal side-channel record.
- Corrected three record titles written in #8 to the papers' actual titles (OCPP SAST, model-free stealthy attack, CULypso), and five source types (two arXiv papers to `paper`; the AAOS bulletin and two ZDI records to `advisory`).
- The site's source pages showed only the frontmatter `status` code as "Evidence status" and never rendered the written assessment. They now show it as "Assessment", with the code relabelled "Capture status".
- Checked every source URL: arXiv records against the arXiv API (titles and dates match) and the rest over HTTP. CERT-In timed out and ACM, UNECE and MDPI refused automated requests; none is a confirmed broken link.
- Regenerated `wiki/sources/MANIFEST.sha256`. Briefing snapshots were not edited.
