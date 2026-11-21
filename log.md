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
