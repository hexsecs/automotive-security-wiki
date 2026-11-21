# Automotive Security Research Wiki

Public subset of Phil's source-grounded research wiki, focused exclusively on automotive cybersecurity.

## Contents

- Dated automotive cybersecurity briefings
- Durable automotive security research notes linked from those briefings
- Metadata-only source records with canonical URLs and evidence status

## Publication boundary

This repository intentionally excludes the private wiki's unrelated research, operational notes, credentials, compatibility pages, and full raw source captures. Source records preserve provenance without republishing article or paper text.

Start here: [briefings/automotive](wiki/briefings/automotive/index.md).

## Website

The site is generated from `wiki/` by `scripts/build_site.py` (Python 3 + PyYAML) using the styles in `web/`. Build locally with:

```sh
pip install pyyaml
python3 scripts/build_site.py   # writes _site/
python3 -m http.server -d _site
```

`.github/workflows/pages.yml` builds and deploys it to GitHub Pages on every push to `main` (set **Settings → Pages → Source** to *GitHub Actions*).
